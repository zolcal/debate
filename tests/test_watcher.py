from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import os
import json
import subprocess
import sys
import time

import pytest

from debate.channel import ChannelError, init_channel, post, read_entries
from debate.watcher import (
    WatcherConfig,
    WatcherLock,
    decide,
    new_entry_lines,
    record_escalation,
    record_invocation,
    run_once,
    tick_lock_path,
    watch,
)

NOW = datetime(2026, 7, 6, 12, 0, 0, tzinfo=timezone.utc)


def make_channel(tmp_path: Path) -> Path:
    """A channel with one open thread: beta requested review on t-one; turn=alpha; seq=1."""
    from debate import channel

    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    return root


def config(tmp_path: Path, **overrides: Any) -> WatcherConfig:
    # State lives OUTSIDE the channel root (enforced by WatcherConfig) —
    # tmp_path is the channel root, so state goes to a per-test sibling.
    defaults: dict[str, Any] = dict(
        channel_root=tmp_path,
        state_path=tmp_path.parent / (tmp_path.name + "-watcher-state.json"),
        commands={"bob": ["echo", "{prompt}"]},
        prompts={"bob": "it is your turn"},
        debounce_seconds={},
        retry_seconds=1800,
    )
    defaults.update(overrides)
    return WatcherConfig(**defaults)


def signal(
    seq: int = 1,
    turn: str = "bob",
    thread: str = "feature-x",
    updated_at: str = "2026-07-06T11:00:00+00:00",
) -> dict[str, Any]:
    return {"seq": seq, "turn": turn, "thread": thread, "last_entry": f"MSG-{seq}", "updated_at": updated_at}


LOCK_HOLDER_CODE = """
import sys, time, pathlib
lock_path = pathlib.Path(sys.argv[1]); ready = pathlib.Path(sys.argv[2])
handle = open(lock_path, "a+")
if sys.platform == "win32":
    import msvcrt; handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
else:
    import fcntl; fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
ready.write_text("held")
time.sleep(30)
"""


def _hold_lock_in_child(lock: Path, ready: Path) -> subprocess.Popen[bytes]:
    lock.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, "-c", LOCK_HOLDER_CODE, str(lock), str(ready)])
    deadline = time.monotonic() + 10
    while not ready.exists():
        assert proc.poll() is None, "lock-holder child died"
        assert time.monotonic() < deadline, "lock-holder child never became ready"
        time.sleep(0.02)
    return proc


def _acquire_within(lock_path: Path, seconds: float) -> "WatcherLock":
    """Bounded polling: kernel unlock after process death may be delayed (esp. Windows)."""
    deadline = time.monotonic() + seconds
    lock = WatcherLock(lock_path)
    while True:
        if lock.acquire():
            return lock
        assert time.monotonic() < deadline, f"lock not released within {seconds}s"
        time.sleep(0.05)


def test_state_path_inside_channel_root_is_refused(tmp_path: Path) -> None:
    # Audit finding (thread debate-repo-audit): the README's "watcher memory
    # lives outside the shared folder" is a hard rule, so the config refuses
    # a state_path that resolves inside the channel root.
    with pytest.raises(ChannelError, match="outside the shared folder"):
        config(tmp_path, state_path=tmp_path / "state" / "watcher.json")
    with pytest.raises(ChannelError, match="outside the shared folder"):
        config(tmp_path, state_path=tmp_path)


def test_no_open_thread_means_no_invocation(tmp_path: Path) -> None:
    # The production incident's near-miss: after a close, a stale turn field
    # must not fire an agent at an empty mailbox.
    decision = decide(signal(thread=""), {}, config(tmp_path), NOW)

    assert decision.invoke is None
    assert "no open thread" in decision.reason


def test_no_turn_means_no_invocation(tmp_path: Path) -> None:
    decision = decide(signal(turn=""), {}, config(tmp_path), NOW)

    assert decision.invoke is None


def test_party_without_command_is_never_invoked(tmp_path: Path) -> None:
    # A human-driven party simply has no command entry.
    decision = decide(signal(turn="alice"), {}, config(tmp_path), NOW)

    assert decision.invoke is None
    assert "no command" in decision.reason


def test_first_invocation_fires(tmp_path: Path) -> None:
    decision = decide(signal(), {}, config(tmp_path), NOW)

    assert decision.invoke == "bob"


def test_debounce_holds_fire_within_window(tmp_path: Path) -> None:
    cfg = config(tmp_path, debounce_seconds={"bob": 600})
    fresh = signal(updated_at=(NOW - timedelta(seconds=300)).isoformat(timespec="seconds"))

    assert decide(fresh, {}, cfg, NOW).invoke is None

    stale = signal(updated_at=(NOW - timedelta(seconds=601)).isoformat(timespec="seconds"))
    assert decide(stale, {}, cfg, NOW).invoke == "bob"


def test_once_per_seq_then_timed_retry_then_escalate(tmp_path: Path) -> None:
    cfg = config(tmp_path)
    state: dict[str, Any] = {}

    # First invocation fires and is recorded.
    assert decide(signal(), state, cfg, NOW).invoke == "bob"
    state = record_invocation(state, 1, NOW)

    # Immediately after: no re-fire (once per seq).
    assert decide(signal(), state, cfg, NOW + timedelta(seconds=60)).invoke is None

    # After retry_seconds without a reply: exactly one retry.
    later = NOW + timedelta(seconds=1801)
    assert decide(signal(), state, cfg, later).invoke == "bob"
    state = record_invocation(state, 1, later)

    # After the retry also times out: escalation, not a third invocation.
    much_later = later + timedelta(seconds=1801)
    decision = decide(signal(), state, cfg, much_later)
    assert decision.invoke is None
    assert decision.escalate is not None

    # Escalations are once-per-thread:seq — never spammed.
    state = record_escalation(state, "feature-x", 1)
    again = decide(signal(), state, cfg, much_later + timedelta(seconds=3600))
    assert again.invoke is None
    assert again.escalate is None


def test_new_seq_resets_the_invocation_budget(tmp_path: Path) -> None:
    cfg = config(tmp_path)
    state = record_invocation({}, 1, NOW)

    decision = decide(signal(seq=2), state, cfg, NOW + timedelta(seconds=30))

    assert decision.invoke == "bob"


def test_new_entry_lines_are_incremental(tmp_path: Path) -> None:
    init_channel(tmp_path, ("alice", "bob"), "owner")
    post(tmp_path, "alice", "review-request", "feature-x", "please review this branch")
    post(tmp_path, "bob", "verdict", "feature-x", "APPROVE — no findings")
    entries = read_entries(tmp_path)

    assert len(new_entry_lines(entries, after_seq=0)) == 2
    lines = new_entry_lines(entries, after_seq=1)
    assert len(lines) == 1
    assert "MSG-2 bob verdict" in lines[0]


def test_run_once_invokes_configured_command_and_mirrors_reply(tmp_path: Path) -> None:
    init_channel(tmp_path, ("alice", "bob"), "owner")
    post(tmp_path, "alice", "review-request", "feature-x", "please review")

    # bob's "agent" is a real subprocess that posts a verdict via the CLI —
    # an end-to-end tick without any LLM.
    import sys

    reply_cmd = [
        sys.executable,
        "-m",
        "debate",
        "post",
        "--root",
        str(tmp_path),
        "--from",
        "bob",
        "--type",
        "verdict",
        "--thread",
        "feature-x",
        "--body",
        "APPROVE {prompt}",
    ]
    cfg = config(tmp_path, commands={"bob": reply_cmd}, prompts={"bob": "(prompt text)"})

    output = run_once(cfg)

    entries = read_entries(tmp_path)
    assert len(entries) == 2
    assert entries[1].sender == "bob"
    assert entries[1].body == "APPROVE (prompt text)"
    assert any("invoked bob" in line for line in output)
    # The reply the invocation produced is mirrored in the same tick.
    assert any("MSG-2 bob verdict" in line for line in output)


def test_run_once_records_state_before_launching_the_child(tmp_path: Path) -> None:
    # A crash mid-invocation must not double-fire the same seq on the next
    # tick: the invocation record is persisted before the subprocess runs.
    init_channel(tmp_path, ("alice", "bob"), "owner")
    post(tmp_path, "alice", "review-request", "feature-x", "please review")

    import sys

    failing_cmd = [sys.executable, "-c", "import sys; sys.exit(3)"]
    cfg = config(tmp_path, commands={"bob": failing_cmd})

    output = run_once(cfg)
    assert any("exit 3" in line for line in output)

    # Next tick: same seq, already invoked once, not yet retry-eligible.
    output2 = run_once(cfg)
    assert not any("invoked bob" in line for line in output2)


def test_run_once_does_nothing_quietly_when_nothing_changed(tmp_path: Path) -> None:
    init_channel(tmp_path, ("alice", "bob"), "owner")
    cfg = config(tmp_path)

    assert run_once(cfg) == []


def test_agent_is_launched_with_stdin_detached(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An inherited tty/pipe stdin hung a real review for 3h (court-dict, 2026-07-15)."""
    root = make_channel(tmp_path)
    seen: dict[str, Any] = {}

    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        seen.update(kwargs)
        return subprocess.CompletedProcess(argv, 0, stdout="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    run_once(config(root, commands={"alpha": ["agent"]}, prompts={"alpha": "go"}))
    assert seen["stdin"] is subprocess.DEVNULL


def test_agent_timeout_is_reported_not_raised(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(
        root,
        commands={"alpha": [sys.executable, "-c", "import time; time.sleep(5)"]},
        prompts={"alpha": "go"},
        timeout_seconds=1,
    )
    lines = run_once(cfg)  # must not raise
    assert any("TIMEOUT after 1s (killed)" in line for line in lines)
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert state["invocations"]["1"]["count"] == 1  # retry machinery still armed


def test_missing_binary_escalates_and_never_relaunches(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": ["/nonexistent/bin/agent-xyz"]}, prompts={"alpha": "go"})
    first = run_once(cfg)
    assert any(line.startswith("invoke failed for alpha:") for line in first)
    assert any(line.startswith("ESCALATE:") for line in first)
    second = run_once(cfg)  # later tick: escalation is terminal
    assert not any("invoke failed" in line for line in second)
    assert not any(line.startswith("ESCALATE:") for line in second)
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert state["invocations"]["1"]["count"] == 1  # exactly one launch attempt ever


def test_escalated_seq_is_never_retried_even_after_retry_window(tmp_path: Path) -> None:
    state = {
        "invocations": {"1": {"count": 1, "last_at": "2020-01-01T00:00:00+00:00"}},
        "escalated": ["t-one:1"],
    }
    cfg = config(tmp_path, commands={"alpha": ["agent"]}, prompts={"alpha": "go"})
    decision = decide(signal(turn="alpha", thread="t-one", seq=1), state, cfg, NOW)
    assert decision.invoke is None
    assert decision.reason.endswith("already escalated")


def test_non_string_command_elements_are_refused_at_config_time(tmp_path: Path) -> None:
    with pytest.raises(ChannelError, match="command"):
        config(tmp_path, commands={"alpha": ["agent", 42]})


def test_run_once_refused_while_live_process_holds_lock(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})
    child = _hold_lock_in_child(tick_lock_path(cfg.state_path), tmp_path / "ready")
    try:
        with pytest.raises(ChannelError, match="another watcher"):
            run_once(cfg)
    finally:
        child.kill()
        child.wait(timeout=10)


def test_lock_released_by_kernel_when_holder_dies(tmp_path: Path) -> None:
    """No staleness logic exists anywhere: the OS releases a crashed holder's lock."""
    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})
    child = _hold_lock_in_child(tick_lock_path(cfg.state_path), tmp_path / "ready")
    child.kill()
    child.wait(timeout=10)
    lock = _acquire_within(tick_lock_path(cfg.state_path), 10.0)  # bounded poll, not immediate
    lock.release()


def test_two_opens_in_one_process_conflict(tmp_path: Path) -> None:
    """flock binds to the open file description: in-process exclusion is real."""
    lock_path = tmp_path / "state.json.lock"
    first = WatcherLock(lock_path)
    assert first.acquire() is True
    second = WatcherLock(lock_path)
    assert second.acquire() is False
    first.release()
    third = WatcherLock(lock_path)
    assert third.acquire() is True
    third.release()


def test_state_tmp_files_are_pid_unique_and_cleaned(tmp_path: Path) -> None:
    from debate.watcher import _save_state

    target = tmp_path / "state.json"
    _save_state(target, {"x": 1})
    assert target.exists()
    assert list(tmp_path.glob("state.json.tmp*")) == []  # renamed away, pid-unique name


def _fail_sleep(seconds: float) -> None:
    raise AssertionError("watch slept - expected exit before any sleep")


def _post_cmd(root: Path, sender: str, entry_type: str, thread: str, body: str) -> list[str]:
    """An 'agent' that speaks the protocol: posts one entry via the real library."""
    src = Path(__file__).resolve().parents[1] / "src"
    code = (
        "import sys; sys.path.insert(0, {src!r}); from pathlib import Path; "
        "from debate import channel; "
        "channel.post(Path({root!r}), {sender!r}, {entry_type!r}, {thread!r}, {body!r})"
    ).format(src=str(src), root=str(root), sender=sender, entry_type=entry_type, thread=thread, body=body)
    return [sys.executable, "-c", code]


def test_watch_until_close_exits_zero(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": _post_cmd(root, "alpha", "close", "t-one", "done, closing")},
                 prompts={"alpha": "go"})
    lines: list[str] = []
    code = watch(cfg, interval_seconds=1, until_close=True, max_ticks=5, emit=lines.append, sleep=_fail_sleep)
    assert code == 0
    assert any("thread closed after 1 tick" in line for line in lines)


def test_watch_new_escalation_exits_four(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 2, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": []}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=3,
                 emit=lambda s: None, sleep=_fail_sleep) == 4


def test_watch_exits_four_on_persisted_escalation_instead_of_spinning(tmp_path: Path) -> None:
    """A cron watch-once already recorded the escalation; a later watch --until-close
    (max_ticks=None!) must terminate loudly on tick one. _fail_sleep guarantees this
    test FAILS rather than hangs if the exit regresses."""
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 1, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": ["t-one:1"]}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    lines: list[str] = []
    assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=None,
                 emit=lines.append, sleep=_fail_sleep) == 4
    assert any(line.startswith("STUCK:") for line in lines)


def test_watch_max_ticks_exits_five(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})  # nobody invocable: ticks are no-ops
    sleeps: list[float] = []
    assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=2,
                 emit=lambda s: None, sleep=sleeps.append) == 5
    assert len(sleeps) == 1  # slept between tick 1 and 2, exited at the cap without a further sleep


def test_second_watch_exits_six_while_first_watch_sleeps(tmp_path: Path) -> None:
    """REAL process-lifetime exclusion: a first watch parked in its sleep still excludes
    both a second watch and a bare run_once."""
    import threading

    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})
    sleeping = threading.Event()
    stop = threading.Event()

    def parked_sleep(seconds: float) -> None:
        sleeping.set()
        stop.wait(timeout=30)

    first_result: list[int] = []
    first = threading.Thread(
        target=lambda: first_result.append(
            watch(cfg, interval_seconds=1, until_close=False, max_ticks=2,
                  emit=lambda s: None, sleep=parked_sleep)
        )
    )
    first.start()
    assert sleeping.wait(timeout=10), "first watch never reached its sleep"
    try:
        lines: list[str] = []
        assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=1,
                     emit=lines.append, sleep=_fail_sleep) == 6
        assert any("another watcher" in line for line in lines)
        with pytest.raises(ChannelError, match="another watcher"):
            run_once(cfg)
    finally:
        stop.set()
        first.join(timeout=30)
    assert first_result == [5]  # first watch finished its max_ticks run cleanly


def _freeze_mid_post(root: Path, sender: str, entry_type: str, thread: str, body: str) -> None:
    """Reproduce a writer paused between mailbox append and signal replace:
    perform a real post, then restore the pre-post signal bytes."""
    from debate import channel as channel_mod

    before = (root / "signal.json").read_bytes()
    channel_mod.post(root, sender, entry_type, thread, body)
    (root / "signal.json").write_bytes(before)


def test_mid_post_state_defers_invocation(tmp_path: Path) -> None:
    root = make_channel(tmp_path)  # signal seq 1, turn=alpha
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    _freeze_mid_post(root, "alpha", "verdict", "t-one", "reply in flight")  # mailbox 2, signal 1
    lines = run_once(cfg)
    assert any("mailbox ahead of signal" in line for line in lines)
    assert not any(line.startswith("invoked ") for line in lines)
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert state.get("invocations", {}) == {}


def test_mid_post_state_defers_new_escalation(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 2, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": []}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    _freeze_mid_post(root, "alpha", "verdict", "t-one", "reply in flight")
    lines = run_once(cfg)  # would have escalated seq 1 - but the world moved
    assert any("mailbox ahead of signal" in line for line in lines)
    assert not any(line.startswith("ESCALATE:") for line in lines)
    assert json.loads(cfg.state_path.read_text(encoding="utf-8"))["escalated"] == []


def test_mid_post_state_suppresses_persisted_stuck_line(tmp_path: Path) -> None:
    """The persisted-escalation STUCK line derives from the same snapshot: with the
    mailbox ahead, the escalated seq is about to be superseded - emitting STUCK
    (and exiting watch with 4) would be false."""
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 1, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": ["t-one:1"]}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    _freeze_mid_post(root, "alpha", "verdict", "t-one", "reply in flight")
    lines = run_once(cfg)
    assert any("mailbox ahead of signal" in line for line in lines)
    assert not any(line.startswith("STUCK:") for line in lines)


def test_agent_inherits_watcher_cwd_not_channel_root(tmp_path: Path) -> None:
    """The documented cron pattern is `cd <project> && debate watch-once --root collab`:
    the project root is the watcher's cwd, and the agent must run there too. Launching
    the child inside the channel root broke every relative path in the pinned prompts
    (PROTOCOL.md, `debate read --root collab`) - found by a real review round."""
    root = make_channel(tmp_path)
    out = tmp_path / "child-cwd.txt"
    cwd_cmd = [sys.executable, "-c", f"import os; open({str(out)!r}, 'w').write(os.getcwd())"]
    cfg = config(root, commands={"alpha": cwd_cmd}, prompts={"alpha": "go"})
    run_once(cfg)
    assert out.read_text() == os.getcwd()          # the watcher's own cwd...
    assert out.read_text() != str(root)            # ...never the channel root
