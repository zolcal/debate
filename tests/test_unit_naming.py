"""Slice 4 of docs/plans/2026-08-01-channel-identity-binding.md (APPROVED MSG-122).

G4: the `debate-watch-<state-file-stem>` convention lived only in a comment
inside the unit file it names. Two channels whose stems collide produce one
systemd unit that silently overwrites the other — and colliding log tags on top
(found independently at MSG-128). Docs state the rule; `watch-status` shows the
name so an operator can see which unit SHOULD be driving.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from debate import channel
from debate.watcher import WatcherConfig, read_status

REPO_ROOT = Path(__file__).resolve().parent.parent
NOW = datetime(2026, 8, 2, 12, 0, 0, tzinfo=timezone.utc)


def test_watch_status_names_the_unit_that_should_drive_this_channel(tmp_path: Path) -> None:
    """During incident 1 the operator could not tell which unit belonged to
    which channel, so they killed the wrong process. The report now says."""
    root = tmp_path / "collab"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    cfg = WatcherConfig(channel_root=root, state_path=tmp_path / "debate-myproject.json")

    lines, _ = read_status(cfg, NOW)

    assert any("debate-watch-debate-myproject" in line for line in lines), (
        f"the conventional unit name must appear in the report: {lines!r}"
    )


def test_the_unit_name_tracks_the_state_stem_not_the_channel_name(tmp_path: Path) -> None:
    """Two channels both named `collab` are the norm in this fleet; the STEM is
    what distinguishes them, which is why the convention keys on it."""
    root = tmp_path / "collab"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    cfg = WatcherConfig(channel_root=root, state_path=tmp_path / "debate-other.json")

    lines, _ = read_status(cfg, NOW)

    assert any("debate-watch-debate-other" in line for line in lines)
    assert not any("debate-watch-collab" in line for line in lines)


def test_protocol_states_the_one_channel_one_state_one_unit_rule() -> None:
    """The rule was a comment inside the unit file it described — invisible to
    anyone setting up the second channel."""
    protocol = (REPO_ROOT / "PROTOCOL.md").read_text(encoding="utf-8")

    assert "one state file" in protocol.lower()
    assert "debate-watch-" in protocol, "the unit-naming convention must be written down"


def test_readme_states_the_rule_for_people_adding_a_second_channel() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "debate-watch-" in readme, "the naming convention must reach the public docs"
