"""Per-instance channel naming (v0.4, Slice 1).

A channel gets a generated instance id at init: ``<label>-<NNNNN>``. The label
defaults to the enclosing git repo's directory name, falls back to the channel
folder's PARENT directory name outside any repo, and ``--label`` overrides in
every case (pinned at plan review, fold N4, MSG-2). The id is generated once
and stored — never re-derived — so it is stable under later renames.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

from debate import channel
from debate.channel import ChannelError


def test_generated_id_is_label_dash_five_digits(tmp_path: Path) -> None:
    cid = channel.generate_channel_id(tmp_path, label="alpha")

    assert re.fullmatch(r"alpha-\d{5}", cid)


def test_label_defaults_to_git_toplevel_basename(tmp_path: Path) -> None:
    repo = tmp_path / "my-repo"
    root = repo / "collab"
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)

    cid = channel.generate_channel_id(root)

    assert re.fullmatch(r"my-repo-\d{5}", cid)


def test_label_falls_back_to_parent_dir_name_outside_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The suite's tmp dir lives INSIDE this repo, so "outside any git repo"
    # must be simulated: the ceiling stops git's upward discovery at tmp_path.
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    root = tmp_path / "someproj" / "collab"
    root.mkdir(parents=True)

    cid = channel.generate_channel_id(root)

    assert re.fullmatch(r"someproj-\d{5}", cid)


def test_derived_label_is_sanitized_to_slug(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A directory name is nobody's words — lowercase it and slug the rest.

    (Refuse-never-neutralize applies to record content, not to a convenience
    default the operator can always override with --label.)
    """
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    root = tmp_path / "My_Repo.X" / "collab"
    root.mkdir(parents=True)

    cid = channel.generate_channel_id(root)

    assert re.fullmatch(r"my-repo-x-\d{5}", cid)


def test_explicit_invalid_label_is_refused_not_sanitized(tmp_path: Path) -> None:
    """An EXPLICIT label is the operator's words: refuse, never neutralize."""
    with pytest.raises(ChannelError, match="label"):
        channel.generate_channel_id(tmp_path, label="My Repo")


def test_unsalvageable_derived_label_asks_for_explicit_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    root = tmp_path / "---" / "collab"
    root.mkdir(parents=True)

    with pytest.raises(ChannelError, match="--label"):
        channel.generate_channel_id(root)


def test_init_named_channel_writes_prefixed_files_and_records_name(tmp_path: Path) -> None:
    import json

    config = channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")

    assert config.name == "alpha-11111"
    assert (tmp_path / "alpha-11111.debate.json").exists()
    assert (tmp_path / "alpha-11111.channel.md").exists()
    assert (tmp_path / "alpha-11111.signal.json").exists()
    raw = json.loads((tmp_path / "alpha-11111.debate.json").read_text(encoding="utf-8"))
    assert raw["name"] == "alpha-11111"
    assert raw["managed_version"] == 1
    assert raw["thread_cap"] == 12
    # The legacy filenames must NOT appear: this channel is born named.
    assert not (tmp_path / "debate.json").exists()
    assert not (tmp_path / "CHANNEL.md").exists()


def test_legacy_init_keeps_the_old_layout_and_no_managed_marker(tmp_path: Path) -> None:
    """Unnamed callers keep the 0.3.1 shape while adopting cap 12."""
    import json

    config = channel.init_channel(tmp_path, ("alice", "bob"), "owner")

    assert config.name is None
    raw = json.loads((tmp_path / "debate.json").read_text(encoding="utf-8"))
    assert "name" not in raw
    assert "managed_version" not in raw


def test_unknown_or_malformed_managed_version_refuses(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    path = tmp_path / "alpha-11111.debate.json"
    raw = json.loads(path.read_text(encoding="utf-8"))

    for value in (2, True, "1"):
        raw["managed_version"] = value
        path.write_text(json.dumps(raw), encoding="utf-8")
        with pytest.raises(ChannelError, match="managed_version"):
            channel.load_config(tmp_path, name="alpha-11111")


def test_named_channel_round_trips_config_signal_and_post(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")

    config = channel.load_config(tmp_path, name="alpha-11111")
    assert config.name == "alpha-11111"
    assert channel.read_signal(tmp_path, name="alpha-11111")["seq"] == 0

    entry_id = channel.post(
        tmp_path, "alice", "question", "hello", "anyone there?", name="alpha-11111"
    )

    assert entry_id == "MSG-1"
    entries = channel.read_entries(tmp_path, name="alpha-11111")
    assert [entry.body for entry in entries] == ["anyone there?"]
    assert channel.read_signal(tmp_path, name="alpha-11111")["turn"] == "bob"


def test_two_named_channels_in_one_folder_do_not_clobber(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    channel.init_channel(tmp_path, ("carol", "dave"), "owner", name="beta-22222")

    channel.post(tmp_path, "alice", "question", "t1", "for alpha only", name="alpha-11111")

    assert channel.read_entries(tmp_path, name="beta-22222") == []
    assert channel.read_signal(tmp_path, name="beta-22222")["seq"] == 0
    assert channel.load_config(tmp_path, name="beta-22222").parties == ("carol", "dave")


def test_reinit_of_the_same_name_is_refused(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")

    with pytest.raises(ChannelError, match="already initialized"):
        channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")


def test_config_whose_recorded_name_disagrees_with_its_filename_is_refused(tmp_path: Path) -> None:
    """The file stem and the recorded id must agree, or identity is ambiguous."""
    import json

    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    path = tmp_path / "alpha-11111.debate.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["name"] = "beta-22222"
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(ChannelError, match="beta-22222"):
        channel.load_config(tmp_path, name="alpha-11111")


def test_discover_returns_none_for_a_legacy_only_folder(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")

    assert channel.discover_channel(tmp_path) is None


def test_discover_empty_folder_resolves_to_legacy(tmp_path: Path) -> None:
    """0.3.1 ran `status` against an empty folder and reported a fresh doorbell;
    discovery must not turn that into a refusal."""
    assert channel.discover_channel(tmp_path) is None


def test_discover_returns_the_single_named_channel(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")

    assert channel.discover_channel(tmp_path) == "alpha-11111"


def test_discover_two_named_channels_refuses_naming_both(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    channel.init_channel(tmp_path, ("carol", "dave"), "owner", name="beta-22222")

    with pytest.raises(ChannelError, match=r"(?s)alpha-11111.*beta-22222"):
        channel.discover_channel(tmp_path)


def test_discover_legacy_plus_named_refuses_naming_both(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")
    channel.init_channel(tmp_path, ("carol", "dave"), "owner", name="beta-22222")

    with pytest.raises(ChannelError, match=r"(?s)legacy.*beta-22222"):
        channel.discover_channel(tmp_path)


def test_discover_explicit_channel_selects_among_many(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    channel.init_channel(tmp_path, ("carol", "dave"), "owner", name="beta-22222")

    assert channel.discover_channel(tmp_path, "beta-22222") == "beta-22222"


def test_discover_unknown_channel_refuses_and_lists_what_exists(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")

    with pytest.raises(ChannelError, match=r"(?s)nosuch-99999.*alpha-11111"):
        channel.discover_channel(tmp_path, "nosuch-99999")


def _closed_thread_on(root: Path, name: str | None) -> None:
    channel.init_channel(root, ("alice", "bob"), "owner", name=name)
    channel.post(root, "alice", "question", "t-old", "ping", name=name)
    channel.post(root, "bob", "close", "t-old", "done", name=name)


def test_compact_on_a_named_channel_archives_under_its_id(tmp_path: Path) -> None:
    from datetime import datetime, timedelta, timezone

    _closed_thread_on(tmp_path, "alpha-11111")

    report = channel.compact(
        tmp_path, keep_days=1.0, now=datetime.now(timezone.utc) + timedelta(days=30), name="alpha-11111"
    )

    assert any("archived t-old" in line for line in report)
    archive = tmp_path / "archive"
    month_files = sorted(archive.glob("alpha-11111-????-??.md"))
    assert len(month_files) == 1
    assert (archive / "alpha-11111-INDEX.md").exists()
    # Nothing legacy-named may appear: this folder belongs to named channels.
    assert not list(archive.glob("CHANNEL-*.md"))
    assert not (archive / "INDEX.md").exists()
    assert channel.read_entries(tmp_path, name="alpha-11111") == []


def test_verify_record_on_a_named_channel_reads_its_own_archive(tmp_path: Path) -> None:
    from datetime import datetime, timedelta, timezone

    _closed_thread_on(tmp_path, "alpha-11111")
    channel.compact(
        tmp_path, keep_days=1.0, now=datetime.now(timezone.utc) + timedelta(days=30), name="alpha-11111"
    )

    findings = channel.verify_record(tmp_path, name="alpha-11111")

    assert not [f for f in findings if f.level == channel.ANOMALY]


def test_verify_record_on_a_named_channel_detects_a_bypassing_writer(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    with (tmp_path / "alpha-11111.channel.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## MSG-7 | 2026-08-05T00:00:00+00:00 | from: alice | type: info | thread: t | refs: -\n\nforged\n"
        )

    findings = channel.verify_record(tmp_path, name="alpha-11111")

    assert any(f.code == "mailbox-ahead-of-doorbell" for f in findings)


def test_channels_in_one_folder_verify_independently(tmp_path: Path) -> None:
    channel.init_channel(tmp_path, ("alice", "bob"), "owner", name="alpha-11111")
    channel.init_channel(tmp_path, ("carol", "dave"), "owner", name="beta-22222")
    (tmp_path / "beta-22222.channel.md").write_bytes(b"\x00\x01 not utf8 \xff\xfe")

    clean = channel.verify_record(tmp_path, name="alpha-11111")
    broken = channel.verify_record(tmp_path, name="beta-22222")

    assert not [f for f in clean if f.level == channel.ANOMALY]
    assert any(f.code == "unreadable-record" for f in broken)


def test_id_collision_regenerates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    digits = iter(["11111", "11111", "22222"])
    monkeypatch.setattr(channel, "_random_digits", lambda: next(digits))
    (tmp_path / "alpha-11111.debate.json").write_text("{}", encoding="utf-8")

    cid = channel.generate_channel_id(tmp_path, label="alpha")

    assert cid == "alpha-22222"


def test_exhausted_collision_retries_refuse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(channel, "_random_digits", lambda: "11111")
    (tmp_path / "alpha-11111.debate.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ChannelError, match="refused"):
        channel.generate_channel_id(tmp_path, label="alpha")
