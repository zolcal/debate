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
  invocation counts) must not pollute the shared channel directory.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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

    if count == 0:
        return Decision(turn, None, f"first invocation for seq {seq}")
    if count == 1 and age is not None and age >= config.retry_seconds:
        return Decision(turn, None, f"retry for seq {seq} after {int(age)}s without a reply")
    if count >= 2 and age is not None and age >= config.retry_seconds:
        already = set(state.get("escalated", []))
        key = f"{thread}:{seq}"
        if key not in already:
            return Decision(
                None,
                f"thread {thread!r} stuck on {turn!r} at seq {seq} after {count} invocations",
                "retries exhausted",
            )
        return Decision(None, None, f"seq {seq} already escalated")
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


def run_once(config: WatcherConfig) -> list[str]:
    """One watcher tick: mirror new entries, maybe invoke, maybe escalate.

    Returns the lines a scheduler should surface to the supervisor (stdout,
    chat webhook, wherever). State is persisted BEFORE launching an agent so
    a crash mid-invocation cannot double-fire the same seq.
    """
    from debate import channel  # local import keeps module load light

    output: list[str] = []
    signal = channel.read_signal(config.channel_root)
    state = _load_state(config.state_path)

    entries = channel.read_entries(config.channel_root)
    last_mirrored = int(state.get("last_mirrored_seq", 0))
    output.extend(new_entry_lines(entries, last_mirrored))
    state["last_mirrored_seq"] = max([last_mirrored, *[e.seq for e in entries]])

    seq = int(str(signal.get("seq", 0)))
    decision = decide(signal, state, config, datetime.now(timezone.utc))
    if decision.escalate:
        output.append(f"ESCALATE: {decision.escalate}")
        state = record_escalation(state, str(signal.get("thread", "")), seq)
    elif decision.invoke:
        state = record_invocation(state, seq, datetime.now(timezone.utc))
        _save_state(config.state_path, state)  # before the expensive child
        argv = config.command_for(decision.invoke)
        assert argv is not None  # decide() only returns invocable parties
        proc = subprocess.run(
            argv,
            cwd=config.channel_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=config.timeout_seconds,
            creationflags=CREATE_NO_WINDOW,
        )
        status = "ok" if proc.returncode == 0 else f"exit {proc.returncode}"
        output.append(f"invoked {decision.invoke} for seq {signal.get('seq')}: {status}")
        refreshed = channel.read_entries(config.channel_root)
        output.extend(new_entry_lines(refreshed, int(state.get("last_mirrored_seq", 0))))
        state["last_mirrored_seq"] = max(
            [int(state.get("last_mirrored_seq", 0)), *[e.seq for e in refreshed]]
        )

    _save_state(config.state_path, state)
    return output


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
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
