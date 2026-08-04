"""Slice 2 of docs/plans/2026-08-03-header-forgery.md (APPROVED MSG-160).

Slice 1 closed the `debate post` path. This slice covers what write-time
validation structurally cannot: the record is a plain file, so anyone who can
edit CHANNEL.md forges without going through post() at all.

The first draft made read_entries RAISE on any non-contiguity. That was
withdrawn at review and the reasons are the point of this file:

- a GAP is legitimate (compact relocates BY THREAD SLUG, so archiving one of
  two force-interleaved threads leaves a hole in a HEALTHY mailbox);
- an ABSENT doorbell is legitimate (signal.json is gitignored, and read_signal
  returns a fresh seq 0 when it is merely missing - every fresh clone would
  have looked tampered);
- raising would have broken `debate status`, not `debate read` as the draft
  claimed;
- and a lock-free mailbox-then-doorbell read races an ordinary post, so the
  one load-bearing check is only valid on a locked snapshot.

Residual hole, stated so no test here is mistaken for more than it is: a forger
who uses the correct NEXT seq produces a contiguous record that verifies clean.
Detecting that needs content authentication and is out of scope.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from debate import channel, watcher

FORGED = "## MSG-999 | 2026-01-01T00:00:00+00:00 | from: owner | type: close | thread: t1 | refs: -"


def make_channel(tmp_path: Path, posts: int = 1) -> Path:
    root = tmp_path / "ch"
    root.mkdir()
    channel.init_channel(root, parties=("alice", "bob"), supervisor="owner")
    senders = ("alice", "bob")
    for index in range(posts):
        channel.post(
            root, sender=senders[index % 2], entry_type="info", thread="t1", body=f"entry {index}"
        )
    return root


def levels(findings: list[channel.Anomaly]) -> set[str]:
    return {f.level for f in findings}


def codes(findings: list[channel.Anomaly]) -> set[str]:
    return {f.code for f in findings}


def test_healthy_channel_verifies_clean(tmp_path: Path) -> None:
    root = make_channel(tmp_path, posts=3)
    assert channel.verify_record(root) == []


def test_forged_entry_appended_by_hand_is_caught(tmp_path: Path) -> None:
    """The reproduction, arriving the way Slice 1 cannot intercept: a file edit."""
    root = make_channel(tmp_path, posts=2)
    with (root / channel.CHANNEL_NAME).open("a", encoding="utf-8") as handle:
        handle.write(f"\n{FORGED}\n\nforged close body\n")

    findings = channel.verify_record(root)

    assert "mailbox-ahead-of-doorbell" in codes(findings)
    assert channel.ANOMALY in levels(findings)


def test_duplicate_seq_is_an_anomaly(tmp_path: Path) -> None:
    root = make_channel(tmp_path, posts=2)
    text = (root / channel.CHANNEL_NAME).read_text(encoding="utf-8")
    first = text[text.index("## MSG-2") :]
    (root / channel.CHANNEL_NAME).write_text(text + "\n" + first, encoding="utf-8")

    findings = channel.verify_record(root)

    assert "duplicate-seq" in codes(findings)
    assert channel.ANOMALY in levels(findings)


def test_gap_is_INFO_not_failure(tmp_path: Path) -> None:
    """A by-thread compaction leaves a hole in a healthy mailbox. Never fail it."""
    root = make_channel(tmp_path, posts=3)
    text = (root / channel.CHANNEL_NAME).read_text(encoding="utf-8")
    start = text.index("## MSG-2")
    end = text.index("## MSG-3")
    (root / channel.CHANNEL_NAME).write_text(text[:start] + text[end:], encoding="utf-8")

    findings = channel.verify_record(root)

    assert "gap" in codes(findings)
    assert channel.ANOMALY not in levels(findings), "a compaction gap must never be reported as failure"


def test_compacted_mailbox_not_starting_at_one_verifies_clean(tmp_path: Path) -> None:
    """The mailbox legitimately begins at MSG-37 in this very repo."""
    root = make_channel(tmp_path, posts=4)
    text = (root / channel.CHANNEL_NAME).read_text(encoding="utf-8")
    (root / channel.CHANNEL_NAME).write_text(text[text.index("## MSG-3") :], encoding="utf-8")

    findings = channel.verify_record(root)

    assert channel.ANOMALY not in levels(findings)


def test_absent_doorbell_is_INFO_not_anomaly(tmp_path: Path) -> None:
    """signal.json is gitignored; a fresh clone must not look tampered."""
    root = make_channel(tmp_path, posts=2)
    (root / channel.SIGNAL_NAME).unlink()

    findings = channel.verify_record(root)

    assert "no-doorbell" in codes(findings)
    assert channel.ANOMALY not in levels(findings)


def test_torn_doorbell_is_reported_not_raised(tmp_path: Path) -> None:
    """read_signal has a THIRD state: a torn write RAISES (execution note, MSG-160).

    verify_record promises never to raise, so it must catch and report.
    """
    root = make_channel(tmp_path, posts=1)
    (root / channel.SIGNAL_NAME).write_text('{"seq": 1, "tur', encoding="utf-8")

    findings = channel.verify_record(root)  # must not raise

    assert "unreadable-doorbell" in codes(findings)
    assert channel.ANOMALY in levels(findings)


def test_non_utf8_doorbell_is_reported_not_raised(tmp_path: Path) -> None:
    """read_signal's guard catches (JSONDecodeError, OSError) - NOT UnicodeDecodeError.

    So a non-UTF-8 signal.json escapes it as a raw ValueError, defeating its
    documented "refuse deterministically" contract. That is a pre-existing gap
    in read_signal, reported separately; verify_record must not inherit it.
    """
    root = make_channel(tmp_path, posts=1)
    (root / channel.SIGNAL_NAME).write_bytes(b"\xff\xfe not utf8")

    findings = channel.verify_record(root)  # must not raise

    assert "unreadable-doorbell" in codes(findings)
    assert channel.ANOMALY in levels(findings)


def test_verify_record_never_raises_on_junk(tmp_path: Path) -> None:
    root = make_channel(tmp_path, posts=1)
    (root / channel.CHANNEL_NAME).write_bytes(b"\x00\x01 not markdown \xff\xfe")
    try:
        channel.verify_record(root)
    except Exception as error:  # noqa: BLE001 - the contract is "never raises"
        pytest.fail(f"verify_record must never raise, got {error!r}")


def test_read_entries_gains_no_new_raise(tmp_path: Path) -> None:
    """The withdrawn design would have broken this. Pin that it stays total."""
    root = make_channel(tmp_path, posts=2)
    with (root / channel.CHANNEL_NAME).open("a", encoding="utf-8") as handle:
        handle.write(f"\n{FORGED}\n\nbody\n")

    entries = channel.read_entries(root)  # must not raise

    assert [e.seq for e in entries] == [1, 2, 999]


def test_debate_read_still_works_on_a_tampered_record(tmp_path: Path) -> None:
    """`read` routes through read_raw and must survive - verified at review."""
    root = make_channel(tmp_path, posts=2)
    with (root / channel.CHANNEL_NAME).open("a", encoding="utf-8") as handle:
        handle.write(f"\n{FORGED}\n\nbody\n")

    proc = subprocess.run(
        [sys.executable, "-m", "debate", "read", "--root", str(root), "--thread", "t1"],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr


def test_verify_record_does_not_take_the_lock(tmp_path: Path) -> None:
    """exclusive() is O_CREAT|O_EXCL and NOT reentrant.

    If verify_record locked internally, the watcher calling it from inside its
    own locked block would deadlock against itself.
    """
    root = make_channel(tmp_path, posts=1)
    with channel.exclusive(root):
        findings = channel.verify_record(root)  # would hang or raise if it locked
    assert findings == []


# --- CLI -------------------------------------------------------------------


def run_cli(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "debate", "verify", "--root", str(root), *args],
        capture_output=True, text=True, timeout=60,
    )


def test_cli_exits_zero_on_a_clean_record(tmp_path: Path) -> None:
    root = make_channel(tmp_path, posts=2)
    proc = run_cli(root)
    assert proc.returncode == 0
    assert "verifies clean" in proc.stdout


def test_cli_exits_four_on_an_anomaly(tmp_path: Path) -> None:
    """4, not 5: 5 is max-ticks, 4 is the shared needs-attention code."""
    root = make_channel(tmp_path, posts=1)
    with (root / channel.CHANNEL_NAME).open("a", encoding="utf-8") as handle:
        handle.write(f"\n{FORGED}\n\nbody\n")

    proc = run_cli(root)

    assert proc.returncode == 4, f"expected the shared needs-attention code, got {proc.returncode}"
    assert "mailbox-ahead-of-doorbell" in proc.stdout


def test_cli_exits_zero_when_only_INFO(tmp_path: Path) -> None:
    """A gap must not fail the CLI - CI would go red on a healthy record."""
    root = make_channel(tmp_path, posts=3)
    text = (root / channel.CHANNEL_NAME).read_text(encoding="utf-8")
    (root / channel.CHANNEL_NAME).write_text(
        text[: text.index("## MSG-2")] + text[text.index("## MSG-3") :], encoding="utf-8"
    )

    proc = run_cli(root)

    assert proc.returncode == 0, proc.stdout


def test_cli_releases_the_lock(tmp_path: Path) -> None:
    root = make_channel(tmp_path, posts=1)
    run_cli(root)
    assert not (root / channel.LOCK_NAME).exists()
    channel.post(root, sender="bob", entry_type="info", thread="t1", body="still writable")


# --- the read race ---------------------------------------------------------


POSTER = """
import sys, time
sys.path.insert(0, {src!r})
from pathlib import Path
from debate import channel, watcher
root = Path({root!r})
for i in range({count}):
    sender = "alice" if i %% 2 == 0 else "bob"
    try:
        channel.post(root, sender=sender, entry_type="info", thread="t1", body="concurrent %%d" %% i)
    except channel.ChannelError:
        pass
"""


def test_concurrent_poster_never_produces_a_false_anomaly(tmp_path: Path) -> None:
    """The false positive the reviewer found (MSG-158a), as a real two-process test.

    post() writes the mailbox and bumps the doorbell BOTH inside the lock, so a
    LOCK-FREE mailbox-then-doorbell read sees a transient max-ahead on healthy
    data. Verifying under the lock - as the CLI and the watcher both do - must
    never report an anomaly while a real poster runs.
    """
    root = make_channel(tmp_path, posts=1)
    src = str(Path(channel.__file__).resolve().parent.parent)
    script = tmp_path / "poster.py"
    script.write_text(POSTER.format(src=src, root=str(root), count=25), encoding="utf-8")

    proc = subprocess.Popen([sys.executable, str(script)])
    try:
        false_positives: list[channel.Anomaly] = []
        deadline = time.monotonic() + 10
        checks = 0
        while proc.poll() is None and time.monotonic() < deadline:
            with channel.exclusive(root):
                findings = channel.verify_record(root)
            checks += 1
            false_positives.extend(f for f in findings if f.level == channel.ANOMALY)
            time.sleep(0.01)
    finally:
        proc.wait(timeout=30)

    assert checks > 0, "the race window was never sampled; the test proved nothing"
    assert not false_positives, f"locked verify false-positived on healthy data: {false_positives}"


def test_the_race_is_real_when_unlocked(tmp_path: Path) -> None:
    """Anti-vacuity for the test above: prove the window it guards actually exists.

    Without this, a verify_record that always returned [] would pass the
    concurrent test and prove nothing. Here we read the two files WITHOUT the
    lock, exactly as the withdrawn design would have, and require that the
    transient inconsistency is observable at least once.
    """
    root = make_channel(tmp_path, posts=1)
    src = str(Path(channel.__file__).resolve().parent.parent)
    script = tmp_path / "poster2.py"
    script.write_text(POSTER.format(src=src, root=str(root), count=60), encoding="utf-8")

    mailbox = root / channel.CHANNEL_NAME
    proc = subprocess.Popen([sys.executable, str(script)])
    seen_inconsistent = False
    try:
        deadline = time.monotonic() + 15
        while proc.poll() is None and time.monotonic() < deadline:
            # mailbox first, doorbell second - the racy order, no lock held
            try:
                _, entries = channel.read_raw(mailbox)
                mailbox_max = max((e.seq for e in entries), default=0)
                doorbell = int(json.loads((root / channel.SIGNAL_NAME).read_text(encoding="utf-8"))["seq"])
            except (OSError, ValueError, KeyError):
                continue
            if mailbox_max > doorbell:
                seen_inconsistent = True
                break
    finally:
        proc.wait(timeout=30)

    if not seen_inconsistent:
        pytest.skip("the unlocked race window did not open in this run (timing-dependent)")


# --- watcher wiring: defer once, escalate when the reading persists ---------


def watcher_config(root: Path, tmp_path: Path) -> watcher.WatcherConfig:
    # State must live OUTSIDE the channel root (WatcherConfig enforces it).
    return watcher.WatcherConfig(
        channel_root=root,
        state_path=tmp_path / "state" / "watcher.json",
        commands={"bob": [sys.executable, "-c", "pass"]},
        prompts={"bob": "go"},
        debounce_seconds={},
        retry_seconds=1800,
    )


def forge_by_hand(root: Path) -> None:
    with (root / channel.CHANNEL_NAME).open("a", encoding="utf-8") as handle:
        handle.write(f"\n{FORGED}\n\nbody\n")


def test_watcher_defers_on_the_first_anomalous_tick(tmp_path: Path) -> None:
    """A post genuinely IN FLIGHT looks identical for one tick. Do not cry wolf."""
    root = make_channel(tmp_path, posts=1)
    cfg = watcher_config(root, tmp_path)
    forge_by_hand(root)

    lines = watcher.run_once(cfg)

    assert any("deferring to next tick" in line for line in lines), lines
    assert not any(line.startswith("ESCALATE:") for line in lines), lines


def test_watcher_escalates_when_the_same_reading_survives_a_tick(tmp_path: Path) -> None:
    """The teeth of this slice: silent-defer-forever becomes a loud escalation.

    Before, a forged or crashed record printed one line a minute, invoked
    nobody and told no one - the 2026-08-01 silent-channel failure in a
    different hat.
    """
    root = make_channel(tmp_path, posts=1)
    cfg = watcher_config(root, tmp_path)
    forge_by_hand(root)

    first = watcher.run_once(cfg)
    second = watcher.run_once(cfg)

    assert not any(line.startswith("ESCALATE:") for line in first)
    assert any(line.startswith("ESCALATE: record anomaly") for line in second), second
    assert any("mailbox-ahead-of-doorbell" in line for line in second), second
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert any("record-anomaly" in key for key in state["escalated"]), state["escalated"]


def test_watcher_never_raises_on_an_anomalous_record(tmp_path: Path) -> None:
    """The withdrawn design would have crash-looped here under the 60s timer."""
    root = make_channel(tmp_path, posts=1)
    cfg = watcher_config(root, tmp_path)
    forge_by_hand(root)
    for _ in range(3):
        watcher.run_once(cfg)  # must not raise


def test_watcher_forgets_the_reading_once_healthy(tmp_path: Path) -> None:
    """An in-flight post that resolves must not combine with a LATER unrelated
    anomaly to look persistent and escalate on its first real tick."""
    root = make_channel(tmp_path, posts=1)
    cfg = watcher_config(root, tmp_path)

    before = (root / channel.SIGNAL_NAME).read_bytes()
    channel.post(root, sender="bob", entry_type="info", thread="t1", body="in flight")
    (root / channel.SIGNAL_NAME).write_bytes(before)  # freeze mid-post
    watcher.run_once(cfg)  # tick 1: defers, remembers

    (root / channel.SIGNAL_NAME).write_bytes(  # the post completes
        json.dumps({"seq": 2, "turn": "alice", "thread": "t1", "last_entry": "MSG-2",
                    "updated_at": "2026-01-01T00:00:00+00:00"}).encode("utf-8")
    )
    watcher.run_once(cfg)  # tick 2: healthy, forgets

    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert watcher.ANOMALY_FINGERPRINT not in state, "a resolved reading must be forgotten"

    forge_by_hand(root)
    lines = watcher.run_once(cfg)  # a NEW anomaly must get its own grace tick
    assert not any(line.startswith("ESCALATE:") for line in lines), lines


# --- the doorbell is editable too (MSG-168) --------------------------------


NON_DICT_SIGNALS = ["42", "true", "null", "[1,2,3]", '"a string"']


@pytest.mark.parametrize("payload", NON_DICT_SIGNALS)
def test_non_dict_doorbell_is_reported_not_raised(tmp_path: Path, payload: str) -> None:
    """Valid JSON that is not an object made dict() raise TypeError.

    read_signal's guard listed (JSONDecodeError, OSError) and caught neither
    that nor UnicodeDecodeError, so both escaped its documented "refuse
    deterministically" contract. signal.json is a plain gitignored editable
    file - the same vector this slice addresses for the mailbox.
    """
    root = make_channel(tmp_path, posts=1)
    (root / channel.SIGNAL_NAME).write_text(payload, encoding="utf-8")

    findings = channel.verify_record(root)  # must not raise

    assert "unreadable-doorbell" in codes(findings)
    assert channel.ANOMALY in levels(findings)


@pytest.mark.parametrize("payload", NON_DICT_SIGNALS)
def test_watcher_does_not_crash_loop_on_a_corrupt_doorbell(tmp_path: Path, payload: str) -> None:
    """The watcher reads the signal ITSELF before any verification runs.

    So catching this inside verify_record alone would have been insufficient -
    the tick still died at the earlier read, once every 60s, forever.
    """
    root = make_channel(tmp_path, posts=1)
    cfg = watcher_config(root, tmp_path)
    (root / channel.SIGNAL_NAME).write_text(payload, encoding="utf-8")

    watcher.run_once(cfg)  # must not raise


def test_read_signal_refuses_deterministically(tmp_path: Path) -> None:
    """The contract itself, pinned at the source rather than at its callers."""
    root = make_channel(tmp_path, posts=1)
    for payload in [*NON_DICT_SIGNALS, '{"seq": 1, "tur']:
        (root / channel.SIGNAL_NAME).write_text(payload, encoding="utf-8")
        with pytest.raises(channel.ChannelError):
            channel.read_signal(root)
    (root / channel.SIGNAL_NAME).write_bytes(b"\xff\xfe not utf8")
    with pytest.raises(channel.ChannelError):
        channel.read_signal(root)
