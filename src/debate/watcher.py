"""The watcher: a dumb poller that wakes the expensive brains.

Runs from any scheduler (cron, Task Scheduler, a while-loop) every few
minutes. Reads the doorbell, decides — via pure functions, so every decision
is unit-testable — whether a party's agent should be invoked, and shells out
to the command configured for that party. No LLM runs when nothing changed.

Design rules, each one paid for in production (see docs/case-study):

- **Gate on an open thread, not just the turn.** After a ``close`` the turn
  field means nothing; a watcher firing on turn alone burns an agent
  invocation on an empty mailbox.
- **Once per seq.** An invocation that produced no reply is retried once
  after ``retry_seconds``, then escalated to the supervisor — never looped.
- **Debounce.** A live human-driven session may be about to answer; the
  watcher waits ``debounce_seconds`` of unchanged turn before firing, and
  treats its own trigger as a *fallback*, not the primary path.
- **Fixed prompts.** The command and prompt for each party are pinned in
  config — the watcher never composes free-form instructions.
- **State lives outside the channel.** The watcher's memory (last seen seq,
  invocation counts) must not pollute the shared channel directory. Enforced
  at config construction: a ``state_path`` that resolves inside
  ``channel_root`` is refused.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from debate.channel import ChannelError

# Windows: suppress the console window a scheduled invocation would flash.
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


@dataclass(frozen=True)
class WatcherConfig:
    """Per-party invocation commands plus timing knobs.

    ``commands`` maps party name -> argv list. The placeholder ``{prompt}``
    in any argv element is replaced with that party's pinned prompt from
    ``prompts``. Parties without a command are never invoked (a human-driven
    party can simply have no entry).
    """

    channel_root: Path
    state_path: Path
    commands: dict[str, list[str]] = field(default_factory=dict)
    prompts: dict[str, str] = field(default_factory=dict)
    debounce_seconds: dict[str, int] = field(default_factory=dict)
    retry_seconds: int = 30 * 60
    timeout_seconds: int = 30 * 60

    def __post_init__(self) -> None:
        state = self.state_path.resolve()
        root = self.channel_root.resolve()
        if state == root or state.is_relative_to(root):
            raise ChannelError(
                f"refused: state_path {self.state_path} resolves inside the channel root "
                f"{self.channel_root}; the watcher's memory must live outside the shared folder"
            )
        for party, argv in self.commands.items():
            if not all(isinstance(part, str) for part in argv):
                raise ChannelError(f"refused: command for {party!r} has non-string elements: {argv!r}")

    def command_for(self, party: str) -> list[str] | None:
        argv = self.commands.get(party)
        if not argv:
            return None
        prompt = self.prompts.get(party, "")
        return [part.replace("{prompt}", prompt) for part in argv]


@dataclass(frozen=True)
class Decision:
    """What one watcher tick decided, and why — the why is the audit trail."""

    invoke: str | None  # party to invoke, or None
    escalate: str | None  # escalation message for the supervisor, or None
    reason: str


def decide(
    signal: dict[str, Any],
    state: dict[str, Any],
    config: WatcherConfig,
    now: datetime,
) -> Decision:
    """Pure decision core: no I/O, no clock reads, fully unit-testable."""
    turn = str(signal.get("turn", ""))
    thread = str(signal.get("thread", ""))
    seq = int(signal.get("seq", 0))

    if not thread:
        return Decision(None, None, "no open thread")
    if not turn:
        return Decision(None, None, "no turn set")
    if config.command_for(turn) is None:
        return Decision(None, None, f"no command configured for {turn!r}")

    updated_at = _parse_stamp(str(signal.get("updated_at", "")))
    debounce = int(config.debounce_seconds.get(turn, 0))
    if debounce and updated_at is not None and (now - updated_at).total_seconds() < debounce:
        return Decision(None, None, f"debouncing {turn!r} ({debounce}s)")

    invocations = dict(state.get("invocations", {}))
    record = dict(invocations.get(str(seq), {}))
    count = int(record.get("count", 0))
    last_at = _parse_stamp(str(record.get("last_at", "")))
    age = (now - last_at).total_seconds() if last_at is not None else None

    if f"{thread}:{seq}" in set(state.get("escalated", [])):
        return Decision(None, None, f"seq {seq} already escalated")
    if count == 0:
        return Decision(turn, None, f"first invocation for seq {seq}")
    if count == 1 and age is not None and age >= config.retry_seconds:
        return Decision(turn, None, f"retry for seq {seq} after {int(age)}s without a reply")
    if count >= 2 and age is not None and age >= config.retry_seconds:
        return Decision(
            None,
            f"thread {thread!r} stuck on {turn!r} at seq {seq} after {count} invocations",
            "retries exhausted",
        )
    return Decision(None, None, f"waiting on seq {seq} (invoked {count}x)")


def record_invocation(state: dict[str, Any], seq: int, now: datetime) -> dict[str, Any]:
    invocations = dict(state.get("invocations", {}))
    record = dict(invocations.get(str(seq), {}))
    invocations[str(seq)] = {
        "count": int(record.get("count", 0)) + 1,
        "last_at": now.isoformat(timespec="seconds"),
    }
    return {**state, "invocations": invocations}


def record_escalation(state: dict[str, Any], thread: str, seq: int) -> dict[str, Any]:
    escalated = set(state.get("escalated", []))
    escalated.add(f"{thread}:{seq}")
    return {**state, "escalated": sorted(escalated)}


def new_entry_lines(entries: list[Any], after_seq: int) -> list[str]:
    """One-line summaries of entries newer than after_seq — mirror these to
    wherever the supervisor already looks (chat, log, notification)."""
    lines = []
    for entry in entries:
        if entry.seq <= after_seq:
            continue
        first = next((ln.strip() for ln in entry.body.splitlines() if ln.strip()), "(empty)")
        lines.append(f"{entry.thread or '-'} MSG-{entry.seq} {entry.sender} {entry.entry_type}: {first[:160]}")
    return lines


def tick_lock_path(state_path: Path) -> Path:
    return state_path.with_suffix(state_path.suffix + ".lock")


class WatcherLock:
    """OS-level advisory lock on ``<state>.lock`` - the kernel is the referee.

    ``fcntl.flock`` (POSIX) / ``msvcrt.locking`` (Windows) release when the
    holder exits or crashes, so there is NO staleness logic, NO pid probing,
    and NO takeover race by construction. The pid+stamp content is
    diagnostics only; the file is never unlinked (inert when unlocked).
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._handle: Any = None

    def acquire(self) -> bool:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(self._path, "a+", encoding="utf-8")
        try:
            if sys.platform == "win32":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            handle.close()
            return False
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        handle.seek(0)
        handle.truncate()
        handle.write(f"{os.getpid()}\n{stamp}\n")
        handle.flush()
        self._handle = handle
        return True

    def release(self) -> None:
        if self._handle is None:
            return
        try:
            if sys.platform == "win32":
                import msvcrt

                self._handle.seek(0)
                msvcrt.locking(self._handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        finally:
            self._handle.close()
            self._handle = None


def run_once(config: WatcherConfig) -> list[str]:
    lock = WatcherLock(tick_lock_path(config.state_path))
    if not lock.acquire():
        raise ChannelError(f"refused: another watcher is driving {tick_lock_path(config.state_path)}")
    try:
        return _run_once_locked(config)
    finally:
        lock.release()


def _run_once_locked(config: WatcherConfig) -> list[str]:
    """One watcher tick: mirror new entries, maybe invoke, maybe escalate.

    Returns the lines a scheduler should surface to the supervisor (stdout,
    chat webhook, wherever). State is persisted BEFORE launching an agent so
    a crash mid-invocation cannot double-fire the same seq.
    """
    from debate import channel  # local import keeps module load light

    output: list[str] = []
    state = _load_state(config.state_path)

    # Snapshot + decide + record under the CHANNEL WRITER LOCK: a mid-post
    # writer cannot hold it, so signal and mailbox are consistent here by
    # construction. Lock order: watcher lock (held by our caller) BEFORE the
    # writer lock - never the reverse, so no cycle. The child launch happens
    # AFTER release: an agent posting its reply via the CLI must not deadlock
    # against its own watcher.
    with channel.exclusive(config.channel_root):
        signal = channel.read_signal(config.channel_root)
        entries = channel.read_entries(config.channel_root)
        seq = int(str(signal.get("seq", 0)))
        mailbox_seq = max((entry.seq for entry in entries), default=0)

        last_mirrored = int(state.get("last_mirrored_seq", 0))
        output.extend(new_entry_lines(entries, last_mirrored))
        state["last_mirrored_seq"] = max([last_mirrored, *[e.seq for e in entries]])

        if mailbox_seq > seq:
            # A non-CLI writer violated append-then-signal mid-flight; the
            # consistent-snapshot invariant failed - act on nothing this tick.
            output.append(
                f"mailbox ahead of signal (entries at {mailbox_seq}, signal at {seq}); deferring to next tick"
            )
            _save_state(config.state_path, state)
            return output

        decision = decide(signal, state, config, datetime.now(timezone.utc))
        if decision.escalate:
            output.append(f"ESCALATE: {decision.escalate}")
            state = record_escalation(state, str(signal.get("thread", "")), seq)
        elif decision.invoke:
            state = record_invocation(state, seq, datetime.now(timezone.utc))
        elif decision.reason.endswith("already escalated"):
            output.append(f"STUCK: seq {seq} escalated; supervisor action required")
        _save_state(config.state_path, state)  # recorded before the expensive child

    if decision.invoke:
        argv = config.command_for(decision.invoke)
        assert argv is not None  # decide() only returns invocable parties
        try:
            # No cwd override: the agent runs where the watcher runs. The
            # documented pattern is `cd <project> && debate watch-once --root
            # <channel>`, so the watcher's cwd IS the project root - and every
            # relative path in a pinned prompt (PROTOCOL.md, `debate read
            # --root collab`) resolves there. Launching inside the channel
            # root broke them all (found by a real review round, 2026-07-16).
            proc = subprocess.run(
                argv,
                text=True,
                stdin=subprocess.DEVNULL,  # an inherited tty/pipe stdin hung a real agent for 3h
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=config.timeout_seconds,
                creationflags=CREATE_NO_WINDOW,
            )
        except subprocess.TimeoutExpired:
            # Already on the books; the once-per-seq retry machinery takes it from here.
            output.append(
                f"invoked {decision.invoke} for seq {seq}: TIMEOUT after {config.timeout_seconds}s (killed)"
            )
        except (OSError, ValueError) as error:
            # A missing binary or bad argv will not heal on retry: terminal.
            output.append(f"invoke failed for {decision.invoke}: {error}")
            output.append(
                f"ESCALATE: cannot launch agent for {decision.invoke!r} "
                f"on thread {signal.get('thread')!r} - fix the watcher config"
            )
            state = record_escalation(state, str(signal.get("thread", "")), seq)
        else:
            status = "ok" if proc.returncode == 0 else f"exit {proc.returncode}"
            output.append(f"invoked {decision.invoke} for seq {seq}: {status}")
        refreshed = channel.read_entries(config.channel_root)
        output.extend(new_entry_lines(refreshed, int(state.get("last_mirrored_seq", 0))))
        state["last_mirrored_seq"] = max(
            [int(state.get("last_mirrored_seq", 0)), *[e.seq for e in refreshed]]
        )

    _save_state(config.state_path, state)
    return output


def watch(
    config: WatcherConfig,
    *,
    interval_seconds: int,
    until_close: bool,
    max_ticks: int | None,
    emit: Callable[[str], None],
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """Foreground run-to-completion loop: own the lock, tick, sleep, repeat.

    The lock is held for the PROCESS lifetime so a second watch - or a cron
    watch-once - is refused even while this one sleeps. Exit codes: 0 thread
    closed (with until_close), 4 escalated or stuck (supervisor must look),
    5 max-ticks, 6 another live watcher holds the lock. 130 is CLI-only.
    """
    from debate import channel  # local import keeps module load light

    lock = WatcherLock(tick_lock_path(config.state_path))
    if not lock.acquire():
        emit(f"another watcher is driving {tick_lock_path(config.state_path)} - exiting")
        return 6
    ticks = 0
    try:
        while True:
            lines = _run_once_locked(config)
            for line in lines:
                emit(line)
            if any(line.startswith(("ESCALATE:", "STUCK:")) for line in lines):
                return 4
            ticks += 1
            if until_close and not str(channel.read_signal(config.channel_root).get("thread", "")):
                emit(f"thread closed after {ticks} tick(s) - exiting")
                return 0
            if max_ticks is not None and ticks >= max_ticks:
                emit(f"max ticks ({max_ticks}) reached - exiting")
                return 5
            sleep(interval_seconds)
    finally:
        lock.release()


def _parse_stamp(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"last_mirrored_seq": 0, "invocations": {}, "escalated": []}
    return dict(json.loads(path.read_text(encoding="utf-8")))


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.tmp{os.getpid()}")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
