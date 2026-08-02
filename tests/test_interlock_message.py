"""Slice 3 of docs/plans/2026-08-01-watcher-liveness-and-ops-gaps.md (APPROVED MSG-119).

G2: two driving modes silently sabotage each other. A `watch-once` tick refused
by a competing driver used to say only which lock file was busy — leaving the
operator to find the holder by hand, which is how incident 1 ended with the
wrong process killed.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main

HOLDER_CODE = """
import sys, time, pathlib
lock_path = pathlib.Path(sys.argv[1]); ready = pathlib.Path(sys.argv[2])
handle = open(lock_path, "a+")
import fcntl; fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
handle.seek(0); handle.truncate()
handle.write("777001\\n2026-08-02T09:15:00+00:00\\n"); handle.flush()
ready.write_text("held")
time.sleep(30)
"""


def _hold(lock: Path, ready: Path) -> "subprocess.Popen[bytes]":
    lock.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, "-c", HOLDER_CODE, str(lock), str(ready)])
    deadline = time.monotonic() + 10
    while not ready.exists():
        assert proc.poll() is None, "lock-holder child died"
        assert time.monotonic() < deadline, "lock-holder child never became ready"
        time.sleep(0.02)
    return proc


@pytest.mark.skipif(sys.platform == "win32", reason="holder helper uses fcntl")
def test_refused_tick_names_the_holder_and_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The refusal must answer the operator's real question — WHO is driving —
    and it must exit 1. The exit code is pinned by a test because this doc
    claimed 6 for two rounds and nobody had run it (MSG-117 F1)."""
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    state_path = tmp_path / "state.json"
    config_path = tmp_path / "watcher.json"
    config_path.write_text(json.dumps({"state_path": str(state_path)}), encoding="utf-8")

    proc = _hold(tmp_path / "state.json.lock", tmp_path / "ready")
    try:
        code = main(["watch-once", "--root", str(root), "--config", str(config_path)])
    finally:
        proc.kill()
        proc.wait()

    err = capsys.readouterr().err
    assert code == 1, "run_once raises ChannelError; the CLI maps it to 1 — 6 belongs to watch()"
    assert "777001" in err, "the refusal must name the holder pid"
    assert "2026-08-02T09:15:00+00:00" in err, "and when it took the lock"
    assert "watch-status" in err, "and where to look next"


BLANK_NOTE_HOLDER = """
import sys, time, pathlib
lock_path = pathlib.Path(sys.argv[1]); ready = pathlib.Path(sys.argv[2])
handle = open(lock_path, "a+")
import fcntl; fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
handle.seek(0); handle.truncate(); handle.flush()   # mid-rewrite: lock HELD, note blank
ready.write_text("held")
time.sleep(30)
"""


@pytest.mark.skipif(sys.platform == "win32", reason="holder helper uses fcntl")
def test_refusal_never_invents_a_pid_when_the_holder_note_is_blank(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`acquire()` truncates before it writes, so a probe can land on a held
    lock whose note is empty — observed live during a review round. The lock is
    real and the refusal must stand, but the pid is NOT known, and a message
    that guessed one would send an operator to kill an unrelated process. That
    is incident 1 with extra steps."""
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    state_path = tmp_path / "state.json"
    config_path = tmp_path / "watcher.json"
    config_path.write_text(json.dumps({"state_path": str(state_path)}), encoding="utf-8")

    lock_path = tmp_path / "state.json.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, "-c", BLANK_NOTE_HOLDER, str(lock_path), str(tmp_path / "ready")])
    deadline = time.monotonic() + 10
    while not (tmp_path / "ready").exists():
        assert proc.poll() is None, "lock-holder child died"
        assert time.monotonic() < deadline, "lock-holder child never became ready"
        time.sleep(0.02)
    try:
        code = main(["watch-once", "--root", str(root), "--config", str(config_path)])
    finally:
        proc.kill()
        proc.wait()

    err = capsys.readouterr().err
    assert code == 1, "a blank note does not make the lock any less held"
    assert "pid unknown (holder was rewriting its note)" in err
    assert not re.search(r"pid \d", err), f"a pid was invented from an empty note: {err!r}"
