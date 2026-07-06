from datetime import datetime, timedelta, timezone
from pathlib import Path

from debate.channel import init_channel, post, read_entries
from debate.watcher import (
    WatcherConfig,
    decide,
    new_entry_lines,
    record_escalation,
    record_invocation,
    run_once,
)

NOW = datetime(2026, 7, 6, 12, 0, 0, tzinfo=timezone.utc)


def config(tmp_path: Path, **overrides) -> WatcherConfig:
    defaults = dict(
        channel_root=tmp_path,
        state_path=tmp_path / "state" / "watcher.json",
        commands={"bob": ["echo", "{prompt}"]},
        prompts={"bob": "it is your turn"},
        debounce_seconds={},
        retry_seconds=1800,
    )
    defaults.update(overrides)
    return WatcherConfig(**defaults)  # type: ignore[arg-type]


def signal(seq=1, turn="bob", thread="feature-x", updated_at="2026-07-06T11:00:00+00:00"):
    return {"seq": seq, "turn": turn, "thread": thread, "last_entry": f"MSG-{seq}", "updated_at": updated_at}


def test_no_open_thread_means_no_invocation(tmp_path):
    # The production incident's near-miss: after a close, a stale turn field
    # must not fire an agent at an empty mailbox.
    decision = decide(signal(thread=""), {}, config(tmp_path), NOW)

    assert decision.invoke is None
    assert "no open thread" in decision.reason


def test_no_turn_means_no_invocation(tmp_path):
    decision = decide(signal(turn=""), {}, config(tmp_path), NOW)

    assert decision.invoke is None


def test_party_without_command_is_never_invoked(tmp_path):
    # A human-driven party simply has no command entry.
    decision = decide(signal(turn="alice"), {}, config(tmp_path), NOW)

    assert decision.invoke is None
    assert "no command" in decision.reason


def test_first_invocation_fires(tmp_path):
    decision = decide(signal(), {}, config(tmp_path), NOW)

    assert decision.invoke == "bob"


def test_debounce_holds_fire_within_window(tmp_path):
    cfg = config(tmp_path, debounce_seconds={"bob": 600})
    fresh = signal(updated_at=(NOW - timedelta(seconds=300)).isoformat(timespec="seconds"))

    assert decide(fresh, {}, cfg, NOW).invoke is None

    stale = signal(updated_at=(NOW - timedelta(seconds=601)).isoformat(timespec="seconds"))
    assert decide(stale, {}, cfg, NOW).invoke == "bob"


def test_once_per_seq_then_timed_retry_then_escalate(tmp_path):
    cfg = config(tmp_path)
    state: dict = {}

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


def test_new_seq_resets_the_invocation_budget(tmp_path):
    cfg = config(tmp_path)
    state = record_invocation({}, 1, NOW)

    decision = decide(signal(seq=2), state, cfg, NOW + timedelta(seconds=30))

    assert decision.invoke == "bob"


def test_new_entry_lines_are_incremental(tmp_path):
    init_channel(tmp_path, ("alice", "bob"), "owner")
    post(tmp_path, "alice", "review-request", "feature-x", "please review this branch")
    post(tmp_path, "bob", "verdict", "feature-x", "APPROVE — no findings")
    entries = read_entries(tmp_path)

    assert len(new_entry_lines(entries, after_seq=0)) == 2
    lines = new_entry_lines(entries, after_seq=1)
    assert len(lines) == 1
    assert "MSG-2 bob verdict" in lines[0]


def test_run_once_invokes_configured_command_and_mirrors_reply(tmp_path):
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


def test_run_once_records_state_before_launching_the_child(tmp_path):
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


def test_run_once_does_nothing_quietly_when_nothing_changed(tmp_path):
    init_channel(tmp_path, ("alice", "bob"), "owner")
    cfg = config(tmp_path)

    assert run_once(cfg) == []
