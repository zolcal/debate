"""Tests for v0.2 housekeeping: compact, read, and refs verification.

Motivated by production numbers: the original channel reached 63 messages /
112 KB in four days — an agent naively reading the whole mailbox would burn
a quarter of its context window on history it doesn't need.
"""

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from debate.__main__ import main
from debate.channel import (
    ChannelError,
    compact,
    init_channel,
    post,
    read_entries,
    read_raw,
    read_signal,
    verify_refs,
)

FUTURE = datetime(2027, 1, 1, tzinfo=timezone.utc)  # far after any test post's stamp

MULTILINE = "verdict line one\n\n  indented evidence: 27 passed\nlast line"


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """Two closed threads (one with a multiline body) and one open thread."""
    init_channel(tmp_path, ("alice", "bob"), "owner")
    post(tmp_path, "alice", "review-request", "old-one", "please review old-one")
    post(tmp_path, "bob", "verdict", "old-one", MULTILINE)
    post(tmp_path, "alice", "close", "old-one", "merged, closing")
    post(tmp_path, "bob", "review-request", "old-two", "please review old-two")
    post(tmp_path, "alice", "verdict", "old-two", "REQUEST CHANGES")
    post(tmp_path, "bob", "close", "old-two", "withdrawn, closing")
    post(tmp_path, "alice", "review-request", "live-one", "please review live-one")
    return tmp_path


def test_compact_moves_closed_threads_verbatim(root: Path) -> None:
    report = compact(root, keep_days=0, now=FUTURE)

    assert len(report) == 2 and all("archived" in line for line in report)
    # The mailbox now holds only the open thread; the doorbell is untouched.
    remaining = read_entries(root)
    assert [e.thread for e in remaining] == ["live-one"]
    signal = read_signal(root)
    assert signal["seq"] == 7
    assert signal["thread"] == "live-one"
    # The archive holds the moved entries with bodies byte-identical.
    archives = list((root / "archive").glob("CHANNEL-*.md"))
    assert len(archives) == 1
    _, archived = read_raw(archives[0])
    assert [e.thread for e in archived] == ["old-one"] * 3 + ["old-two"] * 3
    assert MULTILINE in archived[1].raw
    # One index line per archived thread.
    index = (root / "archive" / "INDEX.md").read_text(encoding="utf-8")
    assert "old-one: MSG-1..MSG-3 (3 entries" in index
    assert "old-two: MSG-4..MSG-6 (3 entries" in index
    # The banner warns readers where the rest of the record lives.
    assert "archive/" in (root / "CHANNEL.md").read_text(encoding="utf-8").splitlines()[0]


def test_compact_respects_keep_days_and_is_idempotent(root: Path) -> None:
    assert compact(root, keep_days=36500, now=FUTURE) == ["nothing to compact"]

    compact(root, keep_days=0, now=FUTURE)
    assert compact(root, keep_days=0, now=FUTURE) == ["nothing to compact"]


def test_compact_never_touches_open_or_unclosed_threads(tmp_path: Path) -> None:
    init_channel(tmp_path, ("alice", "bob"), "owner")
    post(tmp_path, "alice", "review-request", "feature-x", "review pls")
    post(tmp_path, "bob", "verdict", "feature-x", "APPROVE")
    # feature-x is open (no close): nothing is eligible even at keep_days=0.
    assert compact(tmp_path, keep_days=0, now=FUTURE) == ["nothing to compact"]
    assert len(read_entries(tmp_path)) == 2


def test_compact_dry_run_writes_nothing(root: Path) -> None:
    before = (root / "CHANNEL.md").read_text(encoding="utf-8")

    report = compact(root, keep_days=0, now=FUTURE, dry_run=True)

    assert report[0] == "dry-run, nothing written"
    assert (root / "CHANNEL.md").read_text(encoding="utf-8") == before
    assert not (root / "archive").exists()


def test_compact_aborts_when_the_channel_changes_mid_run(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from debate import channel as channel_module

    before = (root / "CHANNEL.md").read_text(encoding="utf-8")
    real = channel_module.read_signal
    calls = {"n": 0}

    def racing(path: Path) -> dict[str, object]:
        calls["n"] += 1
        signal = real(path)
        if calls["n"] > 1:  # a concurrent post lands after planning
            signal["seq"] = int(str(signal["seq"])) + 1
        return signal

    monkeypatch.setattr(channel_module, "read_signal", racing)
    with pytest.raises(ChannelError, match="changed while compacting"):
        compact(root, keep_days=0, now=FUTURE)
    assert (root / "CHANNEL.md").read_text(encoding="utf-8") == before


def test_posting_continues_after_compact(root: Path) -> None:
    compact(root, keep_days=0, now=FUTURE)

    post(root, "bob", "verdict", "live-one", "APPROVE")

    assert read_signal(root)["seq"] == 8
    assert [e.thread for e in read_entries(root)] == ["live-one", "live-one"]


def test_read_raw_reproduces_the_file(root: Path) -> None:
    preamble, entries = read_raw(root / "CHANNEL.md")

    rebuilt = preamble + "".join(e.raw for e in entries)
    assert rebuilt.encode("utf-8") == (root / "CHANNEL.md").read_bytes()


def _to_crlf(path: Path) -> None:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    path.write_bytes(data)


def test_read_raw_is_byte_exact_on_crlf_mailboxes(root: Path) -> None:
    # A mailbox imported from (or checked out by) a CRLF system must survive
    # parsing byte-for-byte — the "verbatim" claim is not LF-only.
    _to_crlf(root / "CHANNEL.md")

    preamble, entries = read_raw(root / "CHANNEL.md")

    rebuilt = preamble + "".join(e.raw for e in entries)
    assert rebuilt.encode("utf-8") == (root / "CHANNEL.md").read_bytes()
    assert b"\r\n" in (root / "CHANNEL.md").read_bytes()


def test_compact_preserves_crlf_bytes(root: Path) -> None:
    _to_crlf(root / "CHANNEL.md")
    moved = [e for e in read_raw(root / "CHANNEL.md")[1] if e.thread == "old-one"]
    assert moved and all("\r\n" in e.raw for e in moved)  # sanity: CRLF went in

    compact(root, keep_days=0, now=FUTURE)

    archive = next((root / "archive").glob("CHANNEL-*.md"))
    archive_text = archive.read_bytes().decode("utf-8")
    for entry in moved:  # every block relocated byte-identically
        assert entry.raw in archive_text
    # Kept entries keep their CRLF endings through the rewrite.
    kept = (root / "CHANNEL.md").read_bytes()
    assert b"live-one" in kept and b"\r\n" in kept


def test_writers_respect_a_held_lock(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from debate import channel as channel_module

    monkeypatch.setattr(channel_module, "_LOCK_TIMEOUT_SECONDS", 0.2)
    (root / ".lock").touch()

    with pytest.raises(ChannelError, match="another writer"):
        post(root, "bob", "verdict", "live-one", "APPROVE")
    with pytest.raises(ChannelError, match="another writer"):
        compact(root, keep_days=0, now=FUTURE)

    (root / ".lock").unlink()
    post(root, "bob", "verdict", "live-one", "APPROVE")  # lock released -> flows


def test_stale_lock_is_broken(root: Path) -> None:
    import os
    import time

    lock = root / ".lock"
    lock.touch()
    stale = time.time() - 120  # far beyond the 30s stale window
    os.utime(lock, (stale, stale))

    post(root, "bob", "verdict", "live-one", "APPROVE")  # breaks the corpse

    assert read_signal(root)["seq"] == 8
    assert not lock.exists()


def test_read_cli_prints_open_thread_by_default(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["read", "--root", str(root)]) == 0

    out = capsys.readouterr().out
    assert "live-one" in out
    assert "old-one" not in out


def test_read_cli_finds_archived_threads(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    compact(root, keep_days=0, now=FUTURE)

    assert main(["read", "--root", str(root), "--thread", "old-one"]) == 0

    out = capsys.readouterr().out
    assert "MSG-1" in out and "indented evidence: 27 passed" in out


def test_read_cli_since_filters(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["read", "--root", str(root), "--since", "6"]) == 0

    out = capsys.readouterr().out
    assert "MSG-7" in out and "MSG-6" not in out


def test_read_cli_no_open_thread(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    init_channel(tmp_path, ("alice", "bob"), "owner")

    assert main(["read", "--root", str(tmp_path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "no open thread" in captured.err


@pytest.fixture
def git_repo(tmp_path: Path) -> tuple[Path, str]:
    """A one-commit git repo; returns (path, commit sha)."""
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            env={
                "GIT_AUTHOR_NAME": "t",
                "GIT_AUTHOR_EMAIL": "t@example.com",
                "GIT_COMMITTER_NAME": "t",
                "GIT_COMMITTER_EMAIL": "t@example.com",
                "PATH": os.environ["PATH"],
            },
        )
        assert result.returncode == 0, result.stderr
        return result.stdout.strip()

    git("init", "-q")
    (repo / "f.txt").write_text("hello", encoding="utf-8")
    git("add", "f.txt")
    git("commit", "-q", "-m", "c1")
    return repo, git("rev-parse", "--short", "HEAD")


def test_verify_refs_accepts_real_commits_and_refuses_fakes(git_repo: tuple[Path, str]) -> None:
    repo, sha = git_repo

    verify_refs(f"feature-x@{sha}", repo)  # no raise

    with pytest.raises(ChannelError, match="not a commit"):
        verify_refs("feature-x@deadbeef1", repo)
    with pytest.raises(ChannelError, match="no name@sha"):
        verify_refs("just words, no citation", repo)


def test_post_with_verify_refs_blocks_bad_citations(tmp_path: Path, git_repo: tuple[Path, str]) -> None:
    # The incident this exists for: a close message citing a hash that was
    # written down before the commit existed. The post must be refused and
    # nothing written.
    repo, sha = git_repo
    init_channel(tmp_path, ("alice", "bob"), "owner")
    argv = [
        "post",
        "--root",
        str(tmp_path),
        "--from",
        "alice",
        "--type",
        "review-request",
        "--thread",
        "feature-x",
        "--body",
        "review",
        "--verify-refs",
        str(repo),
        "--refs",
    ]

    assert main([*argv, "feature-x@ffffff1"]) == 1
    assert read_entries(tmp_path) == []

    assert main([*argv, f"feature-x@{sha}"]) == 0
    assert len(read_entries(tmp_path)) == 1
