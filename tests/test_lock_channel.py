"""Slice 2 of docs/plans/2026-08-01-channel-identity-binding.md (APPROVED MSG-122).

The tick lock names the channel it belongs to. The state stamp (Slice 1)
*prevents* the collision; this *diagnoses* a live process during an incident —
which is when nobody wants to be reasoning about `/proc`, and when the MacBook
in this fleet has no `/proc` to reason about.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main
from debate.watcher import WatcherLock, probe_lock

LEGACY_HOLDER = """
import sys, time, pathlib
lock_path = pathlib.Path(sys.argv[1]); ready = pathlib.Path(sys.argv[2])
handle = open(lock_path, "a+")
import fcntl; fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
handle.seek(0); handle.truncate()
handle.write("424242\\n2026-08-02T09:00:00+00:00\\n")   # two lines: pre-Slice-2 format
handle.flush()
ready.write_text("held")
time.sleep(30)
"""


def _hold(code: str, lock: Path, ready: Path) -> "subprocess.Popen[bytes]":
    lock.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, "-c", code, str(lock), str(ready)])
    deadline = time.monotonic() + 10
    while not ready.exists():
        assert proc.poll() is None, "lock-holder child died"
        assert time.monotonic() < deadline, "lock-holder child never became ready"
        time.sleep(0.02)
    return proc


def test_acquire_records_the_channel_as_a_third_line(tmp_path: Path) -> None:
    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"

    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    try:
        lines = lock_path.read_text(encoding="utf-8").splitlines()
    finally:
        lock.release()

    assert len(lines) == 3, f"expected pid/stamp/channel, got {lines!r}"
    assert lines[2] == str(root.resolve())


def test_probe_reports_the_channel_of_a_live_holder(tmp_path: Path) -> None:
    """The question both incidents actually asked: whose watcher is this?"""
    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"

    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    try:
        # A second probe cannot take the lock, so it reads the holder's note.
        result = probe_lock(lock_path)
    finally:
        lock.release()

    assert result.held is True
    assert result.channel == str(root.resolve())


def test_a_legacy_two_line_lock_reads_as_unknown_never_as_a_match(tmp_path: Path) -> None:
    """A lock written before this slice has no channel line. It must degrade to
    "unknown" — reporting it as belonging to whichever channel happens to be
    asking would invent exactly the answer this slice exists to provide."""
    lock_path = tmp_path / "state.json.lock"
    proc = _hold(LEGACY_HOLDER, lock_path, tmp_path / "ready")
    try:
        result = probe_lock(lock_path)
    finally:
        proc.kill()
        proc.wait()

    assert result.held is True
    assert result.pid == 424242, "the pid line still parses"
    assert result.channel is None, "a missing channel line is unknown, not a match"


def test_acquire_rewrites_a_legacy_note_rather_than_appending(tmp_path: Path) -> None:
    """`acquire` truncates: a stale two-line note must not leave a fourth line
    of someone else's history behind."""
    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"
    lock_path.write_text("999\n2020-01-01T00:00:00+00:00\n", encoding="utf-8")

    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    try:
        lines = lock_path.read_text(encoding="utf-8").splitlines()
    finally:
        lock.release()

    assert len(lines) == 3
    assert "999" not in lines[0]


def test_a_released_lock_still_parses(tmp_path: Path) -> None:
    """The file is never unlinked by design; a stale note must not crash a probe."""
    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"
    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    lock.release()

    result = probe_lock(lock_path)

    assert result.held is False
    assert result.channel is None, "a free lock names no holder, and no holder's channel"


def test_a_refused_tick_names_the_holders_channel(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The wrong-process kill in one line: the refusal must say which channel
    the competing driver serves, so the operator can tell it is not theirs."""
    mine = tmp_path / "mine"
    channel.init_channel(mine, ("alpha", "beta"), "owner")
    theirs = tmp_path / "theirs"
    theirs.mkdir()
    state_path = tmp_path / "state.json"
    config_path = tmp_path / "watcher.json"
    config_path.write_text(json.dumps({"state_path": str(state_path)}), encoding="utf-8")

    holder = WatcherLock(tmp_path / "state.json.lock", channel_root=theirs)
    assert holder.acquire()
    try:
        code = main(["watch-once", "--root", str(mine), "--config", str(config_path)])
    finally:
        holder.release()

    err = capsys.readouterr().err
    assert code == 1
    assert str(theirs.resolve()) in err, f"the refusal must name the holder's channel: {err!r}"
