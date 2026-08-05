"""CLI surface of per-instance channel naming (v0.4, Slice 1).

`debate init` always generates an id; every other command discovers the
channel from --root and accepts --channel to disambiguate. Slice 1's two
end-to-end claims (pinned at plan review, MSG-2): file-level isolation (two
inits in one folder cannot clobber each other) AND the discovery refusal
(two channels without --channel refuse, naming both).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main


def _init(root: Path, label: str, parties: str = "alice,bob") -> str:
    before = set(root.glob("*.debate.json"))
    assert main(["init", "--root", str(root), "--parties", parties, "--label", label]) == 0
    created = sorted(set(root.glob("*.debate.json")) - before)
    assert len(created) == 1
    return created[0].name[: -len(".debate.json")]


def test_cli_init_generates_and_prints_the_channel_id(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cid = _init(tmp_path, "alpha")

    assert re.fullmatch(r"alpha-\d{5}", cid)
    assert cid in capsys.readouterr().out
    raw = json.loads((tmp_path / f"{cid}.debate.json").read_text(encoding="utf-8"))
    assert raw["name"] == cid


def test_cli_init_creates_a_missing_root_folder(tmp_path: Path) -> None:
    """`debate init --root ./collab` on a not-yet-existing folder is the
    README's documented first command; id generation must not choke on it."""
    root = tmp_path / "not" / "yet" / "collab"

    assert main(["init", "--root", str(root), "--parties", "alice,bob", "--label", "demo"]) == 0
    assert len(list(root.glob("demo-*.debate.json"))) == 1


def test_cli_init_twice_yields_two_channels_and_no_overwrite(tmp_path: Path) -> None:
    first = _init(tmp_path, "alpha")
    before = (tmp_path / f"{first}.debate.json").read_bytes()

    second = _init(tmp_path, "alpha", parties="carol,dave")

    assert first != second
    assert (tmp_path / f"{first}.debate.json").read_bytes() == before
    assert (tmp_path / f"{second}.debate.json").exists()


def test_cli_invalid_label_is_refused(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["init", "--root", str(tmp_path), "--parties", "alice,bob", "--label", "Bad Label"])

    assert rc == 1
    assert "label" in capsys.readouterr().err


def test_cli_status_discovers_the_single_named_channel(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cid = _init(tmp_path, "alpha")
    channel.post(tmp_path, "alice", "question", "t-one", "ping", name=cid)

    assert main(["status", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "t-one" in out


def test_cli_two_channels_without_channel_flag_refuse_naming_both(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    first = _init(tmp_path, "alpha")
    second = _init(tmp_path, "beta", parties="carol,dave")

    rc = main(["status", "--root", str(tmp_path)])

    assert rc == 1
    err = capsys.readouterr().err
    assert first in err and second in err and "--channel" in err


def test_cli_channel_flag_routes_the_post_to_the_right_mailbox(tmp_path: Path) -> None:
    first = _init(tmp_path, "alpha")
    second = _init(tmp_path, "beta", parties="carol,dave")

    rc = main(
        [
            "post",
            "--root",
            str(tmp_path),
            "--channel",
            first,
            "--from",
            "alice",
            "--type",
            "question",
            "--thread",
            "t-one",
            "--body",
            "for alpha only",
        ]
    )

    assert rc == 0
    assert [e.body for e in channel.read_entries(tmp_path, name=first)] == ["for alpha only"]
    assert channel.read_entries(tmp_path, name=second) == []


def test_cli_unknown_channel_refuses_and_lists_available(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cid = _init(tmp_path, "alpha")

    rc = main(["status", "--root", str(tmp_path), "--channel", "nosuch-99999"])

    assert rc == 1
    err = capsys.readouterr().err
    assert "nosuch-99999" in err and cid in err


def test_cli_read_follows_a_named_channels_archive(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from datetime import datetime, timedelta, timezone

    cid = _init(tmp_path, "alpha")
    channel.post(tmp_path, "alice", "question", "t-old", "ping", name=cid)
    channel.post(tmp_path, "bob", "close", "t-old", "done", name=cid)
    channel.compact(
        tmp_path, keep_days=1.0, now=datetime.now(timezone.utc) + timedelta(days=30), name=cid
    )

    assert main(["read", "--root", str(tmp_path), "--thread", "t-old"]) == 0
    out = capsys.readouterr().out
    assert "ping" in out and "done" in out


def test_cli_verify_runs_against_the_named_channel(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cid = _init(tmp_path, "alpha")
    channel.post(tmp_path, "alice", "question", "t-one", "ping", name=cid)

    assert main(["verify", "--root", str(tmp_path)]) == 0
    assert "record verifies clean" in capsys.readouterr().out


def test_cli_watch_once_ticks_a_named_channel(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The watcher must resolve the named channel's doorbell, not the legacy path."""
    root = tmp_path / "chan"
    root.mkdir()
    cid = _init(root, "alpha")
    channel.post(root, "alice", "question", "t-one", "ping", name=cid)
    config_path = tmp_path / "watcher.json"
    config_path.write_text(
        json.dumps({"state_path": str(tmp_path / "state" / "watch.json")}), encoding="utf-8"
    )

    rc = main(["watch-once", "--root", str(root), "--config", str(config_path)])

    assert rc == 0
    # The tick saw the named channel's open thread — not "no open thread",
    # which is what reading the absent legacy signal.json would produce.
    assert "t-one" not in capsys.readouterr().err
    state = json.loads((tmp_path / "state" / "watch.json").read_text(encoding="utf-8"))
    assert state["last_mirrored_seq"] == 1


def test_cli_legacy_channel_stays_fully_usable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The live channel keeps working unchanged until Slice 4 migrates it."""
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")
    channel.post(tmp_path, "alice", "question", "t-one", "ping")

    assert main(["status", "--root", str(tmp_path)]) == 0
    assert "t-one" in capsys.readouterr().out
    assert main(["verify", "--root", str(tmp_path)]) == 0
