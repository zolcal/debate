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

# Windows locks a byte RANGE and does so MANDATORILY; POSIX flock is advisory
# and whole-file. Locking byte 0 therefore made the note unreadable on Windows —
# probe_lock returned held-but-nameless, so watch-status could not say WHO held
# the lock or for which channel, which is the entire point of the note. The lock
# is taken on a sentinel byte far past the note instead, so the note stays
# readable everywhere. Found by CI (windows-latest 3.10) after two Linux
# reviewers passed it: on POSIX the failure cannot occur.
_LOCK_BYTE_OFFSET = 1 << 16  # 65536 - orders of magnitude past a 3-line note


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
        """Build the argv for a party, expanding placeholders in ONE fixed order.

        ``{channel_root}`` is expanded inside the prompt text FIRST, then that
        prompt is substituted into argv for ``{prompt}`` — one pass each, and
        argv is never re-scanned afterwards, so nothing arriving *from* the
        prompt body can trigger a second expansion. Order pinned at review
        (MSG-122).

        The point of ``{channel_root}`` is that a pinned prompt saying
        ``./collab`` resolves against the watcher's cwd, and every project in
        this fleet names its channel ``collab``. The watcher deliberately does
        not override the child's cwd, so the prompt has to carry the absolute
        path itself.
        """
        argv = self.commands.get(party)
        if not argv:
            return None
        prompt = self.prompts.get(party, "").replace("{channel_root}", str(self.channel_root.resolve()))
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


@dataclass(frozen=True)
class LockState:
    """What a non-blocking flock probe found. ``held`` is the only trustworthy
    field: the lock FILE persists when free (it is never unlinked), so its pid
    and stamp describe the LAST holder, live or dead."""

    held: bool
    pid: int | None
    stamp: str
    cwd: str | None
    channel: str | None = None  # from the holder's note; None when a pre-Slice-2 lock


@dataclass(frozen=True)
class WatchStatus:
    """One channel's liveness, as a verdict plus the reasoning behind it."""

    verdict: str
    detail: str


def status(
    signal: dict[str, Any],
    state: dict[str, Any],
    config: WatcherConfig,
    now: datetime,
    lock: LockState,
    grace_seconds: int = 120,
) -> WatchStatus:
    """Pure verdict core: no I/O, no clock reads — the same rule as ``decide()``.

    Verdict order is deliberate. ESCALATED outranks everything (a human is
    already owed an answer); MANUAL outranks staleness (a party with no
    configured command is answered by a live session, so "the watcher did not
    fire" is the design, not a fault). Only then do the timing verdicts apply.
    """
    thread = str(signal.get("thread", ""))
    turn = str(signal.get("turn", ""))
    seq = int(signal.get("seq", 0))
    holder = _holder_note(lock)

    if not thread:
        return WatchStatus("IDLE", "no open thread; nothing is waiting to be driven")
    if f"{thread}:{seq}" in set(state.get("escalated", [])):
        return WatchStatus("ESCALATED", f"seq {seq} escalated on {thread!r}; supervisor action required{holder}")
    if not turn:
        return WatchStatus("MANUAL", f"thread {thread!r} has no turn (supervisor opener); no seat is due{holder}")
    if config.command_for(turn) is None:
        return WatchStatus(
            "MANUAL",
            f"turn {turn!r} has no command configured; a live session answers this seat, "
            f"not the watcher{holder}",
        )

    record = dict(dict(state.get("invocations", {})).get(str(seq), {}))
    count = int(record.get("count", 0))

    if count:
        last_at = _parse_stamp(str(record.get("last_at", "")))
        if last_at is None:
            return WatchStatus("STALE", f"seq {seq} invoked {count}x but its stamp is unreadable{holder}")
        age = int((now - last_at).total_seconds())
        if age < config.retry_seconds:
            return WatchStatus(
                "INVOKED",
                f"seq {seq} invoked {count}x, awaiting reply for {age}s of {config.retry_seconds}s{holder}",
            )
        return WatchStatus(
            "STALE",
            f"seq {seq} invoked {count}x, {age}s ago - past the {config.retry_seconds}s retry window, "
            f"so no tick is running{holder}",
        )

    # count == 0: an uninvoked seq has NO invocation record, so its age can only
    # be measured from the doorbell. Pinned at review (MSG-117 F4).
    posted_at = _parse_stamp(str(signal.get("updated_at", "")))
    if posted_at is None:
        return WatchStatus("STALE", f"seq {seq} uninvoked and the signal stamp is unreadable{holder}")
    age = int((now - posted_at).total_seconds())
    due = int(config.debounce_seconds.get(turn, 0)) + grace_seconds
    if age < due:
        return WatchStatus("DRIVING", f"seq {seq} posted {age}s ago, not yet due ({due}s debounce+grace){holder}")
    return WatchStatus(
        "STALE",
        f"seq {seq} uninvoked for {age}s, past its {due}s debounce+grace - nothing is driving {thread!r}{holder}",
    )


# How many invocation records the report prints before it says it capped.
_INVOCATIONS_SHOWN = 5


def read_status(
    config: WatcherConfig, now: datetime, grace_seconds: int = 120
) -> tuple[list[str], WatchStatus]:
    """Gather one channel's liveness: the report lines plus the verdict.

    The only impure half of watch-status. Reads the doorbell, the state file and
    the lock; writes nothing and creates nothing — a diagnosis must not perturb
    the thing being diagnosed (an absent state file in particular must stay
    absent, or the next real tick inherits a file this command invented).
    """
    from debate import channel  # local import keeps module load light

    signal = channel.read_signal(config.channel_root)
    state = _load_state(config.state_path) if config.state_path.exists() else {}
    lock = probe_lock(tick_lock_path(config.state_path))
    result = status(signal, state, config, now, lock, grace_seconds=grace_seconds)

    present = "present" if config.state_path.exists() else "absent - never ticked"
    lines = [
        f"channel:  {config.channel_root.resolve()}",
        f"state:    {config.state_path} ({present})",
        # One channel = one folder = one state file = one timer unit. The unit
        # name is DERIVED from the state stem rather than remembered, so an
        # operator can see which unit should be driving this channel instead of
        # guessing from `ps` — the guess that killed the wrong process once.
        f"unit:     debate-watch-{config.state_path.stem} (by convention; scheduling is host config)",
        f"signal:   seq {signal.get('seq', 0)} | turn {str(signal.get('turn', '')) or '-'} | "
        f"thread {str(signal.get('thread', '')) or '-'} | updated {signal.get('updated_at', '-')}",
        f"mirrored: last_mirrored_seq {state.get('last_mirrored_seq', 0)}",
    ]
    records = sorted(dict(state.get("invocations", {})).items(), key=lambda kv: int(kv[0]))
    shown = records[-_INVOCATIONS_SHOWN:]
    for seq_key, record in shown:
        entry = dict(record)
        stamp = _parse_stamp(str(entry.get("last_at", "")))
        age = f"{int((now - stamp).total_seconds())}s ago" if stamp else "age unknown"
        lines.append(f"  seq {seq_key}: invoked {entry.get('count', 0)}x, last {age}")
    # Never truncate silently: an unannounced cap reads as "that is all of them".
    if len(records) > len(shown):
        lines.append(f"  ({len(records) - len(shown)} older invocation records not shown)")
    if lock.held:
        lines.append(
            f"lock:     HELD by pid {lock.pid} since {lock.stamp} | "
            f"cwd {lock.cwd or 'unavailable on this platform'}"
        )
    else:
        lines.append("lock:     free (probed, not guessed)")
    return lines, result


def probe_lock(path: Path) -> LockState:
    """Non-blocking flock probe. NEVER infers from file existence.

    The tick lock file outlives its holder by design (``WatcherLock`` never
    unlinks it), so a file on disk proves only that a watcher ran here once —
    reading it as "a watcher is running" is exactly what made incident 2 look
    healthy from the outside. The kernel is the only honest answer, so we ask
    it: if we can take the lock, nobody held it, and we drop it immediately.

    Read-only by contract: a missing file is reported free rather than created.
    """
    if not path.exists():
        return LockState(held=False, pid=None, stamp="", cwd=None)
    try:
        handle = open(path, "a+", encoding="utf-8")
    except OSError:
        return LockState(held=False, pid=None, stamp="", cwd=None)
    try:
        if sys.platform == "win32":
            import msvcrt

            handle.seek(_LOCK_BYTE_OFFSET)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError:
        pid, stamp, channel = _read_lock_note(handle)
        return LockState(held=True, pid=pid, stamp=stamp, cwd=_cwd_of(pid), channel=channel)
    finally:
        handle.close()
    return LockState(held=False, pid=None, stamp="", cwd=None)


def _read_lock_note(handle: Any) -> tuple[int | None, str, str | None]:
    """pid + stamp from a held lock file, tolerating a mid-rewrite blank.

    ``acquire`` truncates before writing, so a probe can land on an empty or
    half-written file. Observed live during a review round — report the holder
    as unnamed rather than crashing or inventing one.
    """
    try:
        handle.seek(0)
        lines = handle.read().splitlines()
    except OSError:
        return None, "", None
    pid: int | None = None
    if lines:
        try:
            pid = int(lines[0].strip())
        except ValueError:
            pid = None
    stamp = lines[1].strip() if len(lines) > 1 else ""
    channel = lines[2].strip() if len(lines) > 2 else ""
    return pid, stamp, channel or None


def _cwd_of(pid: int | None) -> str | None:
    """The holder's working directory — the channel-identity answer both
    incidents needed. ``/proc`` is Linux-only; elsewhere callers print the pid
    and say the cwd is unavailable rather than guessing."""
    if pid is None or not sys.platform.startswith("linux"):
        return None
    try:
        return os.readlink(f"/proc/{pid}/cwd")
    except OSError:
        return None


def _holder_note(lock: LockState) -> str:
    """Name the lock holder only when the PROBE proved one live: the lock file
    survives release, so its pid is otherwise the last holder, not the current."""
    if not lock.held:
        return ""
    where = lock.cwd or "cwd unavailable on this platform"
    serving = lock.channel or "channel unknown (pre-2026-08 lock)"
    return f" [tick lock held by pid {lock.pid} since {lock.stamp}, {where}, serving {serving}]"


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
    """One-line summaries of entries newer than after_seq - mirror these to
    wherever the supervisor already looks (chat, log, notification).

    NOT COVERED by the ASCII-output guarantee. Every string this module
    *authors* is ASCII, so watcher logs decode identically on every platform
    (Windows print() to a redirected stream uses the locale codepage, not
    UTF-8). These lines are different: they pass through message text somebody
    else wrote, and channel entries have carried em-dashes for months. Forcing
    them ASCII would mean dropping, escaping or transcoding another author's
    words - a product decision, not a typography swap, so it is deliberately
    not made here (ruled at MSG-151 F2). A true end-to-end guarantee wants
    ``sys.stdout.reconfigure(encoding="utf-8")`` at the CLI boundary instead.
    """
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

    def __init__(self, path: Path, channel_root: Path | None = None) -> None:
        self._path = path
        self._channel_root = channel_root
        self._handle: Any = None

    def acquire(self) -> bool:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(self._path, "a+", encoding="utf-8")
        try:
            if sys.platform == "win32":
                import msvcrt

                handle.seek(_LOCK_BYTE_OFFSET)
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
        # Third line: which channel this holder serves. `ps` cannot tell two
        # watchers apart and /proc does not exist off Linux, so the holder says
        # so itself. A pre-Slice-2 note has two lines and reads back as unknown.
        channel = str(self._channel_root.resolve()) if self._channel_root is not None else ""
        handle.write(f"{os.getpid()}\n{stamp}\n{channel}\n")
        handle.flush()
        self._handle = handle
        return True

    def release(self) -> None:
        if self._handle is None:
            return
        try:
            if sys.platform == "win32":
                import msvcrt

                self._handle.seek(_LOCK_BYTE_OFFSET)
                msvcrt.locking(self._handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        finally:
            self._handle.close()
            self._handle = None


def _refusal_message(lock_path: Path) -> str:
    """Name the competing driver, not just the busy file.

    "another watcher is driving <path>" left the operator to find the holder by
    hand — which is how incident 1 ended with the wrong process killed. The
    holder's own note answers it, and `watch-status` answers the rest.
    """
    holder = probe_lock(lock_path)
    if not holder.held:
        return (
            f"refused: another watcher held {lock_path} and released it while we looked; "
            "re-run the tick, or use `debate watch-status` to see the channel's state"
        )
    pid = holder.pid if holder.pid is not None else "unknown (holder was rewriting its note)"
    where = f", cwd {holder.cwd}" if holder.cwd else ""
    serving = f", serving channel {holder.channel}" if holder.channel else ", channel unknown (pre-2026-08 lock)"
    return (
        f"refused: another watcher is driving {lock_path} - pid {pid} since {holder.stamp or 'unknown'}{where}{serving}. "
        "One driver per channel: a scheduler running `watch-once`, OR a long-lived `debate watch` - "
        "never both. Run `debate watch-status --root <channel> --config <watcher.json>` to see which."
    )


def run_once(config: WatcherConfig) -> list[str]:
    lock = WatcherLock(tick_lock_path(config.state_path), channel_root=config.channel_root)
    if not lock.acquire():
        raise ChannelError(_refusal_message(tick_lock_path(config.state_path)))
    try:
        return _run_once_locked(config)
    finally:
        lock.release()


# The state file records which channel wrote it. This is the whole of the
# cross-channel guard: one value on disk compared against the config in hand,
# so a tick on a cold-booted host reaches the same verdict as any other. No
# registry, no daemon, nothing that lives in a process.
CHANNEL_STAMP = "channel_root"
# Last anomalous reading, so a transient in-flight post can be told from a
# permanently wedged or forged record: identical across two ticks == wedged.
ANOMALY_FINGERPRINT = "last_anomaly"


def _verify_channel_binding(state: dict[str, Any], config: WatcherConfig) -> None:
    """Refuse a state file that belongs to a different channel.

    Absent stamp -> adopt (trust on first use): every state file written before
    this existed is unstamped, and a migration step nobody runs is a migration
    that never happens. Paths are compared RESOLVED, so ``collab``, ``./collab``
    and a symlink to it are one channel rather than three.

    This cannot be checked at config construction — the tool only knows about
    channels it has been pointed at. First contact is the earliest moment the
    information exists anywhere.
    """
    stamped = str(state.get(CHANNEL_STAMP, ""))
    if not stamped:
        return
    if Path(stamped).resolve() == config.channel_root.resolve():
        return
    raise ChannelError(
        f"refused: state file {config.state_path} belongs to channel {Path(stamped).resolve()}, "
        f"but this tick is for {config.channel_root.resolve()}. Two channels sharing one state "
        f"file silently share last_mirrored_seq and invocations (keyed by bare seq), so one "
        f"channel's message suppresses the other's invocation. Fix by EDITING the "
        f"{CHANNEL_STAMP!r} key, or by pointing this channel's config at its own state_path - "
        f"do NOT delete the state file: that also clears once-per-seq for the current seq and "
        f"re-invokes a seat that is already working."
    )


def _run_once_locked(config: WatcherConfig) -> list[str]:
    """One watcher tick: mirror new entries, maybe invoke, maybe escalate.

    Returns the lines a scheduler should surface to the supervisor (stdout,
    chat webhook, wherever). State is persisted BEFORE launching an agent so
    a crash mid-invocation cannot double-fire the same seq.
    """
    from debate import channel  # local import keeps module load light

    output: list[str] = []
    state = _load_state(config.state_path)
    # BEFORE mirroring, deciding or invoking: a state file that belongs to a
    # different channel must stop the tick while nothing has been written yet.
    _verify_channel_binding(state, config)
    state[CHANNEL_STAMP] = str(config.channel_root.resolve())

    # Snapshot + decide + record under the CHANNEL WRITER LOCK: a mid-post
    # writer cannot hold it, so signal and mailbox are consistent here by
    # construction. Lock order: watcher lock (held by our caller) BEFORE the
    # writer lock - never the reverse, so no cycle. The child launch happens
    # AFTER release: an agent posting its reply via the CLI must not deadlock
    # against its own watcher.
    with channel.exclusive(config.channel_root):
        # The doorbell is a plain, gitignored, editable file - the same "anyone
        # who can edit it" vector as the mailbox. read_signal REFUSES on a torn,
        # non-UTF-8 or non-object file, and an uncaught refusal HERE is a
        # crash-loop under the 60s timer: precisely the failure this slice
        # exists to remove, arriving through the door we were not watching.
        # Treat it as an anomaly like any other and let the defer/escalate
        # ladder below handle it. (Found at review, MSG-168: broadening
        # read_signal's guard alone was not enough - the tick still died here.)
        doorbell_failure: list[channel.Anomaly] = []
        try:
            signal = channel.read_signal(config.channel_root)
        except channel.ChannelError as error:
            signal = {}
            doorbell_failure = [channel.Anomaly(channel.ANOMALY, "unreadable-doorbell", str(error))]

        entries = channel.read_entries(config.channel_root)
        seq = int(str(signal.get("seq", 0)))
        mailbox_seq = max((entry.seq for entry in entries), default=0)

        last_mirrored = int(state.get("last_mirrored_seq", 0))
        output.extend(new_entry_lines(entries, last_mirrored))
        state["last_mirrored_seq"] = max([last_mirrored, *[e.seq for e in entries]])

        # We are inside the writer lock, so this snapshot is consistent by
        # construction - which is exactly the precondition verify_record needs
        # and cannot establish for itself (the lock is not reentrant).
        # A failed doorbell read IS the finding; re-reading would only rediscover
        # it, and verify_record needs the doorbell to say anything useful anyway.
        findings = doorbell_failure or channel.verify_record(config.channel_root)
        anomalies = [f for f in findings if f.level == channel.ANOMALY]
        if anomalies:
            # An anomalous reading has TWO causes and a SINGLE TICK CANNOT TELL
            # THEM APART:
            #   - a post genuinely IN FLIGHT (the mailbox append landed, the
            #     doorbell bump has not) - transient, resolves next tick;
            #   - a crashed or forged writer - permanent.
            # Escalating the first would cry wolf on healthy traffic, which is
            # exactly why this branch used to defer. But deferring the second
            # is the silent wedge: one line a minute, nobody invoked, nobody
            # told - the 2026-08-01 silent-channel failure in a different hat.
            # So defer ONCE, remember the exact reading, and escalate only when
            # the SAME reading survives a tick. That difference IS the
            # difference between in-flight and wedged.
            fingerprint = "|".join(
                [str(mailbox_seq), str(seq), *sorted(f"{a.code}" for a in anomalies)]
            )
            if state.get(ANOMALY_FINGERPRINT) == fingerprint:
                for anomaly in anomalies:
                    output.append(f"ESCALATE: record anomaly - {anomaly.code}: {anomaly.detail}")
                # Keyed distinctly from the turn-stuck thread:seq escalation
                # below, so neither can mask the other.
                state = record_escalation(state, "record-anomaly", mailbox_seq)
            else:
                state[ANOMALY_FINGERPRINT] = fingerprint
                if mailbox_seq > seq:
                    output.append(
                        f"mailbox ahead of signal (entries at {mailbox_seq}, signal at {seq}); "
                        "deferring to next tick"
                    )
                else:
                    output.append(
                        f"record anomaly ({', '.join(sorted(a.code for a in anomalies))}); "
                        "deferring to next tick"
                    )
            _save_state(config.state_path, state)
            return output

        # Healthy again: forget any prior reading so a resolved in-flight post
        # cannot combine with a LATER unrelated one to look persistent.
        state.pop(ANOMALY_FINGERPRINT, None)

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

    # Every line says WHICH channel it is about. `ps` cannot tell two watchers
    # apart (same binary, same `--root collab` convention), and two watchers'
    # lines interleaved in one journal are unreadable without a per-line tag —
    # the banner alone scrolls away. The tag is the state-file stem, the same
    # identity the systemd unit name uses, so units, locks, state files and
    # log lines all carry one name.
    tag = f"[{config.state_path.stem}]"

    def say(line: str) -> None:
        emit(f"{tag} {line}")

    # Announced BEFORE the lock is attempted: on a refusal the identity of the
    # refused watcher is the whole question.
    say(f"watching {config.channel_root.resolve()} | state {config.state_path}")

    lock = WatcherLock(tick_lock_path(config.state_path), channel_root=config.channel_root)
    if not lock.acquire():
        say(f"another watcher is driving {tick_lock_path(config.state_path)} - exiting")
        return 6
    ticks = 0
    try:
        while True:
            lines = _run_once_locked(config)
            for line in lines:
                say(line)
            if any(line.startswith(("ESCALATE:", "STUCK:")) for line in lines):
                return 4
            ticks += 1
            if until_close and not str(channel.read_signal(config.channel_root).get("thread", "")):
                say(f"thread closed after {ticks} tick(s) - exiting")
                return 0
            if max_ticks is not None and ticks >= max_ticks:
                say(f"max ticks ({max_ticks}) reached - exiting")
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
