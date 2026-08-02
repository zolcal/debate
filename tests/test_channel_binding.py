"""Slice 1 of docs/plans/2026-08-01-channel-identity-binding.md (APPROVED MSG-122).

A state file must know which channel it serves. Two channels sharing one state
file silently share `last_mirrored_seq`, `invocations` (keyed by BARE seq) and
`escalated` — so channel A's MSG-42 satisfies once-per-seq for channel B's
MSG-42, and B's first real invocation arrives late and mislabelled as a retry.
The binding is a comparison of two values already on disk: nothing in memory,
nothing that dies with a process.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from debate import channel
from debate.__main__ import main
from debate.channel import ChannelError
from debate.watcher import WatcherConfig, run_once

STAMP_KEY = "channel_root"


def make_channel(tmp_path: Path, name: str = "chan") -> Path:
    root = tmp_path / name
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    return root


def config(root: Path, state_path: Path, **overrides: Any) -> WatcherConfig:
    defaults: dict[str, Any] = dict(
        channel_root=root, state_path=state_path, commands={}, prompts={},
        debounce_seconds={}, retry_seconds=1800,
    )
    defaults.update(overrides)
    return WatcherConfig(**defaults)


def write_state(path: Path, **extra: Any) -> None:
    payload: dict[str, Any] = {"last_mirrored_seq": 7, "invocations": {"7": {"count": 1, "last_at": "x"}},
                               "escalated": ["t:7"]}
    payload.update(extra)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def test_a_state_file_bound_to_another_channel_refuses_the_tick(tmp_path: Path) -> None:
    """The whole point. Without this, the second channel's ticks quietly ride
    the first channel's bookkeeping."""
    mine = make_channel(tmp_path, "mine")
    theirs = tmp_path / "theirs"
    state_path = tmp_path / "state.json"
    write_state(state_path, **{STAMP_KEY: str(theirs.resolve())})

    with pytest.raises(ChannelError) as caught:
        run_once(config(mine, state_path))

    message = str(caught.value)
    assert str(mine.resolve()) in message, "the refusal must name the channel that was refused"
    assert str(theirs.resolve()) in message, "and the channel the state file belongs to"
    assert str(state_path) in message, "and which file to fix"


def test_the_refusal_says_edit_the_stamp_and_warns_against_deleting(tmp_path: Path) -> None:
    """The obvious recovery is the wrong one: deleting the state file clears
    once-per-seq for the CURRENT seq, so a seat already working is invoked a
    second time — a worse failure than the one being recovered from."""
    mine = make_channel(tmp_path, "mine")
    state_path = tmp_path / "state.json"
    write_state(state_path, **{STAMP_KEY: str((tmp_path / "theirs").resolve())})

    with pytest.raises(ChannelError) as caught:
        run_once(config(mine, state_path))

    message = str(caught.value).lower()
    assert "edit" in message
    assert "delet" in message, "the message must steer away from deleting the state file"


def test_a_refused_tick_leaves_the_state_file_byte_identical(tmp_path: Path) -> None:
    """A guard that mutates what it guards is worse than no guard: it would
    corrupt the very bookkeeping the other channel depends on."""
    mine = make_channel(tmp_path, "mine")
    state_path = tmp_path / "state.json"
    write_state(state_path, **{STAMP_KEY: str((tmp_path / "theirs").resolve())})
    before = state_path.read_bytes()

    with pytest.raises(ChannelError):
        run_once(config(mine, state_path))

    assert state_path.read_bytes() == before


def test_an_unstamped_state_file_is_adopted_without_disturbing_its_contents(tmp_path: Path) -> None:
    """Trust on first use: every state file that exists today is unstamped, and
    a migration step nobody runs is a migration that never happens."""
    mine = make_channel(tmp_path, "mine")
    state_path = tmp_path / "state.json"
    write_state(state_path)  # no stamp

    run_once(config(mine, state_path))

    saved = json.loads(state_path.read_text(encoding="utf-8"))
    assert saved[STAMP_KEY] == str(mine.resolve())
    assert saved["invocations"] == {"7": {"count": 1, "last_at": "x"}}, "adoption must not disturb bookkeeping"
    assert saved["escalated"] == ["t:7"]


def test_a_matching_stamp_ticks_normally(tmp_path: Path) -> None:
    mine = make_channel(tmp_path, "mine")
    state_path = tmp_path / "state.json"
    write_state(state_path, **{STAMP_KEY: str(mine.resolve())})

    run_once(config(mine, state_path))  # must not raise

    assert json.loads(state_path.read_text(encoding="utf-8"))[STAMP_KEY] == str(mine.resolve())


def test_the_same_channel_reached_by_a_symlink_is_the_same_channel(tmp_path: Path) -> None:
    """`collab`, `./collab` and a symlinked path are one channel. Comparing
    unresolved strings would refuse a channel because of how it was spelled."""
    mine = make_channel(tmp_path, "mine")
    link = tmp_path / "link-to-mine"
    link.symlink_to(mine, target_is_directory=True)
    state_path = tmp_path / "state.json"
    write_state(state_path, **{STAMP_KEY: str(mine.resolve())})

    run_once(config(link, state_path))  # must not raise


def test_cli_exits_one_when_the_binding_is_wrong(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    mine = make_channel(tmp_path, "mine")
    state_path = tmp_path / "state.json"
    write_state(state_path, **{STAMP_KEY: str((tmp_path / "theirs").resolve())})
    config_path = tmp_path / "watcher.json"
    config_path.write_text(json.dumps({"state_path": str(state_path)}), encoding="utf-8")

    code = main(["watch-once", "--root", str(mine), "--config", str(config_path)])

    assert code == 1
    assert "channel" in capsys.readouterr().err.lower()
