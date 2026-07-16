import dataclasses
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from debate import channel
from debate.channel import (
    ChannelError,
    init_channel,
    post,
    read_entries,
    read_signal,
)


@pytest.fixture
def root(tmp_path: Path) -> Path:
    init_channel(tmp_path, ("alice", "bob"), "owner")
    return tmp_path


def test_init_creates_config_mailbox_and_fresh_doorbell(root: Path) -> None:
    signal = read_signal(root)

    assert signal == {"seq": 0, "turn": "", "thread": "", "last_entry": "", "updated_at": ""}
    assert read_entries(root) == []


def test_init_refuses_double_init(tmp_path: Path) -> None:
    init_channel(tmp_path, ("alice", "bob"), "owner")

    with pytest.raises(ChannelError, match="already initialized"):
        init_channel(tmp_path, ("alice", "bob"), "owner")


def test_init_refuses_duplicate_names(tmp_path: Path) -> None:
    with pytest.raises(ChannelError, match="distinct"):
        init_channel(tmp_path, ("alice", "alice"), "owner")
    with pytest.raises(ChannelError, match="distinct"):
        init_channel(tmp_path, ("alice", "bob"), "bob")


def test_post_appends_entry_and_flips_turn(root: Path) -> None:
    entry_id = post(root, "alice", "review-request", "feature-x", "please review", refs="feature-x@abc123")

    assert entry_id == "MSG-1"
    signal = read_signal(root)
    assert signal["seq"] == 1
    assert signal["turn"] == "bob"
    assert signal["thread"] == "feature-x"
    entries = read_entries(root)
    assert len(entries) == 1
    assert entries[0].sender == "alice"
    assert entries[0].refs == "feature-x@abc123"
    assert entries[0].body == "please review"


def test_out_of_turn_post_is_refused_within_open_thread(root: Path) -> None:
    post(root, "alice", "review-request", "feature-x", "please review")

    with pytest.raises(ChannelError, match="not your turn"):
        post(root, "alice", "info", "feature-x", "me again")

    # Nothing was written by the refused post.
    assert len(read_entries(root)) == 1
    assert read_signal(root)["seq"] == 1


def test_second_thread_refused_while_one_is_open(root: Path) -> None:
    post(root, "alice", "review-request", "feature-x", "please review")

    with pytest.raises(ChannelError, match="one thread at a time"):
        post(root, "bob", "review-request", "feature-y", "different thing")


def test_close_clears_thread_AND_turn(root: Path) -> None:
    # A turn is only meaningful within an open thread. The first production
    # deployment flipped the turn on close, leaving the doorbell pointing at
    # the non-closer with no thread open — meaningless state that watchers
    # must then know to ignore.
    post(root, "alice", "review-request", "feature-x", "please review")
    post(root, "bob", "verdict", "feature-x", "APPROVE")
    post(root, "alice", "close", "feature-x", "merged, closing")

    signal = read_signal(root)
    assert signal["thread"] == ""
    assert signal["turn"] == ""


def test_closer_can_open_the_next_thread(root: Path) -> None:
    # Turn alternation binds within a thread; if it persisted across thread
    # boundaries, whoever closed could never open the next one.
    post(root, "alice", "review-request", "feature-x", "please review")
    post(root, "bob", "verdict", "feature-x", "APPROVE")
    post(root, "alice", "close", "feature-x", "merged, closing")

    entry_id = post(root, "alice", "review-request", "feature-y", "next one")

    assert entry_id == "MSG-4"
    assert read_signal(root)["thread"] == "feature-y"


def test_one_shot_close_leaves_no_open_thread(root: Path) -> None:
    # The record-correction idiom: a close-type post with a fresh slug drops
    # an entry into the log without opening a thread — so no watcher fires.
    post(root, "alice", "close", "record-correction", "correcting MSG-2: branch was already merged")

    signal = read_signal(root)
    assert signal["seq"] == 1
    assert signal["thread"] == ""
    assert signal["turn"] == ""


def test_supervisor_posts_do_not_flip_the_turn(root: Path) -> None:
    post(root, "alice", "review-request", "feature-x", "please review")

    post(root, "owner", "info", "feature-x", "context from the human")

    signal = read_signal(root)
    assert signal["seq"] == 2
    assert signal["turn"] == "bob"  # still bob's turn


def test_supervisor_may_post_out_of_turn(root: Path) -> None:
    post(root, "alice", "review-request", "feature-x", "please review")
    post(root, "bob", "verdict", "feature-x", "REQUEST CHANGES")

    # alice's turn now — owner interjects anyway, then alice still moves.
    post(root, "owner", "question", "feature-x", "why is criterion 3 skipped?")
    entry_id = post(root, "alice", "fix-report", "feature-x", "fixed, criterion 3 addressed")

    assert entry_id == "MSG-4"


def test_thread_cap_refuses_further_posts_but_allows_close(root: Path) -> None:
    init_signal_cap = 2  # smallest legal cap: request + reply
    (root / "debate.json").write_text(
        json.dumps({"parties": ["alice", "bob"], "supervisor": "owner", "thread_cap": init_signal_cap}),
        encoding="utf-8",
    )
    post(root, "alice", "review-request", "feature-x", "please review")
    post(root, "bob", "verdict", "feature-x", "APPROVE")

    with pytest.raises(ChannelError, match="cap"):
        post(root, "alice", "fix-report", "feature-x", "one more thing")

    # close is always allowed — a capped thread must be closable.
    post(root, "alice", "close", "feature-x", "closing at cap")
    assert read_signal(root)["thread"] == ""


def test_unknown_sender_type_and_slug_are_refused(root: Path) -> None:
    with pytest.raises(ChannelError, match="unknown sender"):
        post(root, "mallory", "info", "feature-x", "hello")
    with pytest.raises(ChannelError, match="unknown entry type"):
        post(root, "alice", "decree", "feature-x", "hello")
    with pytest.raises(ChannelError, match="invalid thread slug"):
        post(root, "alice", "info", "Feature X!", "hello")
    with pytest.raises(ChannelError, match="empty body"):
        post(root, "alice", "info", "feature-x", "   ")


def test_force_is_supervisor_only(root: Path) -> None:
    # "One open thread at a time" is advertised as enforced-hard; force is
    # the supervisor's override, and a PARTY asking for it must be refused
    # (audit finding, thread debate-repo-audit).
    post(root, "alice", "review-request", "feature-x", "please review")

    with pytest.raises(ChannelError, match="supervisor-only"):
        post(root, "bob", "info", "urgent-note", "out-of-band note", force=True)
    assert len(read_entries(root)) == 1  # nothing was written

    entry_id = post(root, "owner", "info", "urgent-note", "out-of-band note", force=True)
    assert entry_id == "MSG-2"
    # The supervisor's forced interjection takes no turn AND does not
    # re-point the doorbell away from the open thread.
    signal = read_signal(root)
    assert signal["turn"] == "bob"
    assert signal["thread"] == "feature-x"


def test_write_then_signal_ordering_survives_partial_read(root: Path) -> None:
    # The doorbell is replaced atomically AFTER the mailbox append: a reader
    # that sees the new seq must find the entry already in the mailbox.
    post(root, "alice", "review-request", "feature-x", "please review")

    signal = read_signal(root)
    entries = read_entries(root)
    seq = signal["seq"]
    assert isinstance(seq, int)
    assert [e.seq for e in entries] == list(range(1, seq + 1))


def test_multiline_bodies_round_trip(root: Path) -> None:
    body = "line one\n\n  indented line\nlast line"
    post(root, "alice", "review-request", "feature-x", body)

    assert read_entries(root)[0].body == body


def _open_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "review please")  # assigns turn=alpha, seq 1
    return root


def test_turn_parked_since_survives_supervisor_interjection(tmp_path: Path) -> None:
    root = _open_channel(tmp_path)
    channel.post(root, "owner", "info", "t-one", "supervisor note")  # preserves turn, refreshes updated_at
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    result = channel.turn_parked_since(root, now)
    assert result is not None
    age, seq = result
    assert seq == 1
    assert age is not None and age >= 3 * 3600  # NOT reset by the interjection


def test_turn_parked_since_none_when_no_open_thread(tmp_path: Path) -> None:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    assert channel.turn_parked_since(root, datetime.now(timezone.utc)) is None


def test_turn_parked_since_none_for_turnless_supervisor_opened_thread(tmp_path: Path) -> None:
    """Supervisor opener leaves turn empty: both parties are turn-refused (channel.py:220),
    so there is no parked party — a supervisor-only state. The open-thread scan filter is
    exercised here: the only party entries belong to the closed thread and must not leak in."""
    root = _open_channel(tmp_path)
    channel.post(root, "alpha", "verdict", "t-one", "ok")
    channel.post(root, "beta", "close", "t-one", "closing")
    channel.post(root, "owner", "verdict", "t-new", "supervisor opener")  # open thread, turn ""
    assert channel.turn_parked_since(root, datetime.now(timezone.utc)) is None


def test_turn_parked_since_open_thread_filter_skips_foreign_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Genuinely exercise the open-thread scan filter (the turnless test above returns
    before scanning): inject a NEWER party entry on a foreign thread and prove the
    assignment still comes from the open thread's own party entry."""
    import dataclasses

    root = _open_channel(tmp_path)  # open thread t-one, opener seq 1 by beta
    entries = channel.read_entries(root)
    foreign = dataclasses.replace(entries[-1], seq=99, thread="t-foreign",
                                  timestamp="2026-07-15T23:00:00+00:00")
    monkeypatch.setattr(channel, "read_entries", lambda r: [*entries, foreign])
    now = datetime(2026, 7, 16, 0, 0, 0, tzinfo=timezone.utc)
    result = channel.turn_parked_since(root, now)
    assert result is not None
    _, seq = result
    assert seq == 1  # the foreign newer entry was skipped by the thread filter


def test_turn_parked_since_naive_stamp_counts_as_utc(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _open_channel(tmp_path)
    entries = channel.read_entries(root)
    naive = [dataclasses.replace(e, timestamp="2026-07-15T00:00:00") for e in entries]  # no tzinfo
    monkeypatch.setattr(channel, "read_entries", lambda r: naive)
    now = datetime(2026, 7, 15, 2, 0, 0, tzinfo=timezone.utc)
    result = channel.turn_parked_since(root, now)
    assert result is not None
    age, _ = result
    assert age == 2 * 3600  # exact: naive parsed as UTC


def test_turn_parked_since_malformed_party_stamp_falls_back_to_updated_at(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _open_channel(tmp_path)
    entries = channel.read_entries(root)
    broken = [dataclasses.replace(e, timestamp="not-a-stamp") for e in entries]
    monkeypatch.setattr(channel, "read_entries", lambda r: broken)
    updated_at = datetime.fromisoformat(str(channel.read_signal(root)["updated_at"]))
    now = updated_at + timedelta(hours=2)  # make the fallback value distinctly nonzero
    result = channel.turn_parked_since(root, now)
    assert result is not None
    age, _ = result
    assert age is not None and abs(age - 2 * 3600) <= 2  # the FALLBACK value, not a fabricated 0


def test_turn_parked_since_both_stamps_malformed_reports_unknown(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _open_channel(tmp_path)
    entries = channel.read_entries(root)
    broken = [dataclasses.replace(e, timestamp="not-a-stamp") for e in entries]
    monkeypatch.setattr(channel, "read_entries", lambda r: broken)
    signal = dict(channel.read_signal(root))
    signal["updated_at"] = "also-garbage"
    monkeypatch.setattr(channel, "read_signal", lambda r: signal)
    result = channel.turn_parked_since(root, datetime.now(timezone.utc))
    assert result is not None
    age, seq = result
    assert age is None and seq == 1  # unknown age - never a fabricated number, never a raise


def test_turn_parked_since_never_raises_on_corrupted_signal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A corrupted signal.json missing 'seq' and 'updated_at' entirely must not raise:
    the docstring promises turn_parked_since never does, but signal["seq"] direct-indexing
    used to raise KeyError on exactly this shape."""
    root = _open_channel(tmp_path)
    monkeypatch.setattr(channel, "read_signal", lambda r: {"thread": "t-one", "turn": "alpha"})
    result = channel.turn_parked_since(root, datetime.now(timezone.utc))
    # The whole point is that this doesn't raise; the shape is secondary
    # (e.g. (None, 0) if nothing else can be recovered).
    assert result is None or isinstance(result, tuple)


def make_closed_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "review please")
    channel.post(root, "alpha", "verdict", "t-one", "APPROVE")
    channel.post(root, "beta", "close", "t-one", "merged, closing")
    return root


@pytest.mark.parametrize("entry_type", ["verdict", "fix-report"])
def test_verdict_and_fix_report_cannot_open_a_thread(tmp_path: Path, entry_type: str) -> None:
    """A stray verdict once reopened a CLOSED thread (baseline test, 2026-07-15)."""
    root = make_closed_channel(tmp_path)
    with pytest.raises(ChannelError, match="cannot open a thread"):
        channel.post(root, "alpha", entry_type, "t-one", "stray reply")


@pytest.mark.parametrize("entry_type", ["review-request", "question", "info", "close"])
def test_opener_types_may_open_a_thread(tmp_path: Path, entry_type: str) -> None:
    """close stays an opener: the one-shot close-correction idiom is shipped contract
    (PROTOCOL.md:51, tests/test_channel.py:102, docs/case-study.md:81)."""
    root = make_closed_channel(tmp_path)
    channel.post(root, "alpha", entry_type, "t-two", "legitimate opener")


def test_supervisor_verdict_with_nothing_open_creates_turnless_open_thread(tmp_path: Path) -> None:
    root = make_closed_channel(tmp_path)
    channel.post(root, "owner", "verdict", "t-one", "supervisor correction on the record")
    signal = channel.read_signal(root)
    assert signal["thread"] == "t-one"   # supervisor posts are exempt and open the slug
    assert signal["turn"] == ""          # with no turn assigned - the supervisor-only state of D2
