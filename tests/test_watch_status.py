"""Slice 1 of docs/plans/2026-08-01-watcher-liveness-and-ops-gaps.md (APPROVED MSG-119).

`debate watch-status`: a read-only answer to "is anything driving this channel?".
The verdict logic is a pure function so every state is testable without a clock,
a scheduler, or a live agent — the same discipline `decide()` follows.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import subprocess
import sys
import time

import pytest

from debate.__main__ import main
from debate.watcher import LockState, WatcherConfig, WatcherLock, probe_lock, status

LOCK_HOLDER_CODE = """
import sys, time, pathlib
lock_path = pathlib.Path(sys.argv[1]); ready = pathlib.Path(sys.argv[2])
handle = open(lock_path, "a+")
if sys.platform == "win32":
    import msvcrt; handle.seek(1 << 16); msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
else:
    import fcntl; fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
handle.seek(0); handle.truncate()
handle.write("999999\\n2026-08-02T11:00:00+00:00\\n"); handle.flush()
ready.write_text("held")
time.sleep(30)
"""


def _hold_lock_in_child(lock: Path, ready: Path) -> "subprocess.Popen[bytes]":
    lock.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, "-c", LOCK_HOLDER_CODE, str(lock), str(ready)])
    deadline = time.monotonic() + 10
    while not ready.exists():
        assert proc.poll() is None, "lock-holder child died"
        assert time.monotonic() < deadline, "lock-holder child never became ready"
        time.sleep(0.02)
    return proc

NOW = datetime(2026, 8, 2, 12, 0, 0, tzinfo=timezone.utc)


def config(tmp_path: Path, **overrides: Any) -> WatcherConfig:
    defaults: dict[str, Any] = dict(
        channel_root=tmp_path,
        state_path=tmp_path.parent / (tmp_path.name + "-watcher-state.json"),
        commands={"bob": ["echo", "{prompt}"]},
        prompts={"bob": "it is your turn"},
        debounce_seconds={"bob": 60},
        retry_seconds=1800,
    )
    defaults.update(overrides)
    return WatcherConfig(**defaults)


def signal(
    seq: int = 1,
    turn: str = "bob",
    thread: str = "feature-x",
    updated_at: str = "2026-08-02T11:59:00+00:00",
) -> dict[str, Any]:
    return {"seq": seq, "turn": turn, "thread": thread, "last_entry": f"MSG-{seq}", "updated_at": updated_at}


FREE_LOCK = LockState(held=False, pid=None, stamp="", cwd=None)


def test_no_open_thread_is_idle_not_stale(tmp_path: Path) -> None:
    """A closed channel is healthy. Staleness is not even computed — there is
    nothing anyone is waiting for."""
    result = status(signal(turn="", thread=""), {}, config(tmp_path), NOW, FREE_LOCK)

    assert result.verdict == "IDLE"
    assert "no open thread" in result.detail


def test_escalated_seq_outranks_every_other_verdict(tmp_path: Path) -> None:
    """An escalated seq needs a human. It must not be reported as merely
    waiting, however recent the invocation was."""
    state = {"escalated": ["feature-x:1"], "invocations": {"1": {"count": 2, "last_at": "2026-08-02T11:59:30+00:00"}}}

    result = status(signal(), state, config(tmp_path), NOW, FREE_LOCK)

    assert result.verdict == "ESCALATED"
    assert "supervisor" in result.detail


def test_invoked_and_still_within_retry_window_is_healthy(tmp_path: Path) -> None:
    """The seat was woken 10 minutes ago and retry_seconds is 30. Nothing is
    wrong — this is the commonest state of a live review."""
    state = {"invocations": {"1": {"count": 1, "last_at": "2026-08-02T11:50:00+00:00"}}}

    result = status(signal(), state, config(tmp_path), NOW, FREE_LOCK)

    assert result.verdict == "INVOKED"
    assert "600s" in result.detail and "1800s" in result.detail


def test_invoked_past_the_retry_window_is_stale(tmp_path: Path) -> None:
    """decide() would have fired a retry by now. That it has not means no tick
    is running — the channel is unattended, not patient."""
    state = {"invocations": {"1": {"count": 1, "last_at": "2026-08-02T10:00:00+00:00"}}}

    result = status(signal(), state, config(tmp_path), NOW, FREE_LOCK)

    assert result.verdict == "STALE"
    assert "retry" in result.detail


def test_fresh_uninvoked_post_within_debounce_is_driving(tmp_path: Path) -> None:
    """Posted 60s ago with a 60s debounce and 120s grace: not yet due. Reporting
    STALE here would cry wolf on every healthy post."""
    result = status(signal(updated_at="2026-08-02T11:59:00+00:00"), {}, config(tmp_path), NOW, FREE_LOCK)

    assert result.verdict == "DRIVING"


def test_uninvoked_past_debounce_plus_grace_is_stale(tmp_path: Path) -> None:
    """Incident 2 in one assertion: a review-request sitting uninvoked while
    everyone assumes a watcher is running. STALE is measured from the SIGNAL,
    because an uninvoked seq has no invocation record to measure from."""
    result = status(signal(updated_at="2026-08-02T11:40:00+00:00"), {}, config(tmp_path), NOW, FREE_LOCK)

    assert result.verdict == "STALE"
    assert "uninvoked" in result.detail and "1200s" in result.detail


def test_human_driven_turn_is_manual_never_stale(tmp_path: Path) -> None:
    """A party with no `commands` entry is answered by a live session, not by
    the watcher. Reporting STALE would cry wolf on this channel's own most
    common state — kimi holds the turn and has no configured command."""
    result = status(
        signal(turn="kimi", updated_at="2026-08-02T09:00:00+00:00"), {}, config(tmp_path), NOW, FREE_LOCK
    )

    assert result.verdict == "MANUAL"
    assert "no command configured" in result.detail


def test_stale_verdict_names_the_lock_holder_when_one_is_live(tmp_path: Path) -> None:
    """During an incident the next question is always 'whose watcher is that?'.
    The pid is only quoted because the PROBE proved it live."""
    lock = LockState(held=True, pid=4242, stamp="2026-08-02T11:58:00+00:00", cwd="/home/zoltan/Projects/other")

    result = status(signal(updated_at="2026-08-02T11:40:00+00:00"), {}, config(tmp_path), NOW, lock)

    assert result.verdict == "STALE"
    assert "4242" in result.detail and "/home/zoltan/Projects/other" in result.detail


def test_probe_reports_free_despite_a_leftover_lock_file(tmp_path: Path) -> None:
    """The §6 free-lock fixture. The .lock file is NEVER unlinked, so a released
    lock still leaves a file naming a long-dead pid. Testing existence instead of
    probing would report a driver that does not exist — the precise mistake that
    made incident 2 look fine from the outside."""
    lock_path = tmp_path / "state.json.lock"
    released = WatcherLock(lock_path)
    assert released.acquire()
    released.release()

    assert lock_path.exists(), "the lock file must survive release; that is the trap being tested"
    result = probe_lock(lock_path)

    assert result.held is False
    assert result.pid is None, "a free lock must not name a holder, even though the file still has one"


def test_probe_reports_held_and_names_the_live_holder(tmp_path: Path) -> None:
    lock_path = tmp_path / "state.json.lock"
    ready = tmp_path / "ready"
    proc = _hold_lock_in_child(lock_path, ready)
    try:
        result = probe_lock(lock_path)

        assert result.held is True
        assert result.pid == 999999
        assert result.stamp == "2026-08-02T11:00:00+00:00"
    finally:
        proc.kill()
        proc.wait()


def test_probe_on_a_missing_lock_file_is_free_not_an_error(tmp_path: Path) -> None:
    """A channel whose watcher has never run has no lock file at all."""
    result = probe_lock(tmp_path / "never-ran.json.lock")

    assert result.held is False
    assert result.pid is None


def _watcher_config_file(tmp_path: Path, state_path: Path) -> Path:
    import json

    path = tmp_path / "watcher.json"
    path.write_text(
        json.dumps(
            {
                "state_path": str(state_path),
                "commands": {"alpha": ["echo", "{prompt}"]},
                "prompts": {"alpha": "your turn"},
                "debounce_seconds": {"alpha": 60},
                "retry_seconds": 1800,
            }
        ),
        encoding="utf-8",
    )
    return path


def test_cli_watch_status_reports_a_stale_channel_and_exits_nonzero(
    tmp_path: Path, capsys: "pytest.CaptureFixture[str]"
) -> None:
    """End-to-end: the incident-2 picture from a real channel on disk, in one
    command. Exit is non-zero so a scheduler or a human can alert on it."""
    from debate import channel

    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    state_path = tmp_path / "state.json"
    state_path.write_text('{"last_mirrored_seq": 0, "invocations": {}, "escalated": []}', encoding="utf-8")
    old = "2020-01-01T00:00:00+00:00"
    signal_path = root / "signal.json"
    import json as _json

    payload = _json.loads(signal_path.read_text(encoding="utf-8"))
    payload["updated_at"] = old
    signal_path.write_text(_json.dumps(payload), encoding="utf-8")

    code = main(["watch-status", "--root", str(root), "--config", str(_watcher_config_file(tmp_path, state_path))])

    out = capsys.readouterr().out
    assert "STALE" in out
    assert "seq 1" in out
    assert str(root) in out, "the report must name the channel it is about"
    assert code == 4


def test_cli_watch_status_creates_no_files(tmp_path: Path, capsys: "pytest.CaptureFixture[str]") -> None:
    """Read-only by contract: diagnosing a sick channel must not perturb it —
    no state file, no lock file, nothing for the next tick to trip over."""
    from debate import channel

    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    state_path = tmp_path / "absent-state.json"

    code = main(["watch-status", "--root", str(root), "--config", str(_watcher_config_file(tmp_path, state_path))])

    assert code == 0, "a channel with no open thread is IDLE, which is healthy"
    assert not state_path.exists(), "watch-status must never create the state file"
    assert not (tmp_path / "absent-state.json.lock").exists(), "watch-status must never create the lock file"


def test_report_says_how_many_invocations_it_hid(tmp_path: Path) -> None:
    """The report shows the most recent few, but a truncation nobody announces
    reads as 'this is all of them'. Say what was dropped."""
    from debate.watcher import read_status

    state_path = tmp_path / "state.json"
    invocations = {str(n): {"count": 1, "last_at": "2026-08-02T11:00:00+00:00"} for n in range(1, 9)}
    import json as _json

    state_path.write_text(_json.dumps({"last_mirrored_seq": 8, "invocations": invocations}), encoding="utf-8")
    from debate import channel

    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")

    lines, _ = read_status(config(root, state_path=state_path), NOW)

    assert any("3 older invocation records not shown" in line for line in lines)
