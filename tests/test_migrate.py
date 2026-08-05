"""`debate migrate` (v0.4 Slice 2): rename a legacy channel in place.

A pure rename — the mailbox and archive bytes are never rewritten (the
acceptance test is byte-identity, archive included; pinned at plan review,
fold N3b, MSG-2). The config is the one file that changes content: it gains
the generated ``name``, because identity is recorded there.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from debate import channel
from debate.channel import ChannelError
from debate.__main__ import main


def _legacy_channel_with_archive(root: Path) -> tuple[bytes, bytes, bytes]:
    """A legacy channel with one archived thread and one live one.

    Returns (mailbox, archive month file, archive index) bytes before migration.
    """
    channel.init_channel(root, ("alice", "bob"), "owner")
    channel.post(root, "alice", "question", "t-old", "ping")
    channel.post(root, "bob", "close", "t-old", "done")
    channel.compact(root, keep_days=1.0, now=datetime.now(timezone.utc) + timedelta(days=30))
    channel.post(root, "alice", "question", "t-live", "still here")
    month = sorted((root / "archive").glob("CHANNEL-*.md"))
    assert len(month) == 1
    return (
        (root / "CHANNEL.md").read_bytes(),
        month[0].read_bytes(),
        (root / "archive" / "INDEX.md").read_bytes(),
    )


def test_migrate_renames_every_file_and_keeps_bytes(tmp_path: Path) -> None:
    mailbox, month, index = _legacy_channel_with_archive(tmp_path)

    cid = channel.migrate_channel(tmp_path, label="alpha")

    assert not (tmp_path / "CHANNEL.md").exists()
    assert not (tmp_path / "debate.json").exists()
    assert not (tmp_path / "signal.json").exists()
    assert not (tmp_path / "archive" / "INDEX.md").exists()
    assert not list((tmp_path / "archive").glob("CHANNEL-*.md"))
    assert (tmp_path / f"{cid}.channel.md").read_bytes() == mailbox
    assert (tmp_path / "archive" / f"{cid}-INDEX.md").read_bytes() == index
    new_month = sorted((tmp_path / "archive").glob(f"{cid}-????-??.md"))
    assert len(new_month) == 1 and new_month[0].read_bytes() == month


def test_migrate_records_the_id_in_the_config(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")

    cid = channel.migrate_channel(tmp_path, label="alpha")

    raw = json.loads((tmp_path / f"{cid}.debate.json").read_text(encoding="utf-8"))
    assert raw["name"] == cid
    assert raw["parties"] == ["alice", "bob"]
    config = channel.load_config(tmp_path, name=cid)
    assert config.name == cid


def test_migrated_channel_verifies_and_reads_identically(tmp_path: Path) -> None:
    _legacy_channel_with_archive(tmp_path)
    before = [
        (entry.seq, entry.thread, entry.body) for entry in channel.read_entries(tmp_path)
    ]
    assert not [f for f in channel.verify_record(tmp_path) if f.level == channel.ANOMALY]

    cid = channel.migrate_channel(tmp_path, label="alpha")

    after = [
        (entry.seq, entry.thread, entry.body)
        for entry in channel.read_entries(tmp_path, name=cid)
    ]
    assert after == before
    assert not [f for f in channel.verify_record(tmp_path, name=cid) if f.level == channel.ANOMALY]


def test_migrate_preserves_the_open_thread_and_posting_continues(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")
    channel.post(tmp_path, "alice", "question", "t-live", "still here")

    cid = channel.migrate_channel(tmp_path, label="alpha")

    signal = channel.read_signal(tmp_path, name=cid)
    assert signal["thread"] == "t-live" and signal["turn"] == "bob"
    channel.post(tmp_path, "bob", "close", "t-live", "done", name=cid)
    assert channel.read_signal(tmp_path, name=cid)["thread"] == ""


def test_migrate_without_a_legacy_channel_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ChannelError, match="no legacy channel"):
        channel.migrate_channel(tmp_path, label="alpha")


def test_migrate_twice_is_refused(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")
    channel.migrate_channel(tmp_path, label="alpha")

    with pytest.raises(ChannelError, match="no legacy channel"):
        channel.migrate_channel(tmp_path, label="alpha")


def test_migrate_survives_an_absent_doorbell(tmp_path: Path) -> None:
    """signal.json is gitignored; a fresh clone migrates without one."""
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")
    (tmp_path / "signal.json").unlink()

    cid = channel.migrate_channel(tmp_path, label="alpha")

    assert not (tmp_path / f"{cid}.signal.json").exists()
    assert channel.read_signal(tmp_path, name=cid)["seq"] == 0  # fresh, not an error


def test_cli_migrate_prints_the_id_and_the_operator_edits(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")

    rc = main(["migrate", "--root", str(tmp_path), "--label", "alpha"])

    assert rc == 0
    out = capsys.readouterr().out
    created = sorted(tmp_path.glob("alpha-*.debate.json"))
    assert len(created) == 1
    cid = created[0].name[: -len(".debate.json")]
    assert cid in out
    # The operator owes two edits; the tool must name both.
    assert "watcher" in out and "state_path" in out
    assert f"debate-watch-{cid}" in out


def test_cli_migrate_refuses_on_a_named_only_folder(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", "--root", str(tmp_path), "--parties", "alice,bob", "--label", "alpha"]) == 0

    rc = main(["migrate", "--root", str(tmp_path)])

    assert rc == 1
    assert "no legacy channel" in capsys.readouterr().err
