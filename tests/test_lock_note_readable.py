"""Windows regression: the holder's note must stay readable while the lock is held.

CI (windows-latest, 3.10) found what two Linux reviewers could not. POSIX
`flock` is ADVISORY and whole-file, so readers are unaffected. Windows
`msvcrt.locking` is MANDATORY over a byte RANGE — and the lock was taken on
byte 0, exactly where the note is written. Result: `probe_lock` could never
read the note on Windows, so `watch-status` reported HELD with no pid, no
stamp and no channel, and the refusal could not name the competing driver.
The whole diagnostic point of the lock note, absent on one platform.

Fix: lock a sentinel byte far past the note. These tests are the regression
guard and they are meaningful on EVERY platform — on POSIX they simply always
held, which is why the gap survived review.
"""

from __future__ import annotations

from pathlib import Path

from debate.watcher import WatcherLock, probe_lock


def test_the_note_is_readable_while_the_lock_is_held(tmp_path: Path) -> None:
    """The bug in one assertion. On Windows this raised PermissionError."""
    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"

    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    try:
        text = lock_path.read_text(encoding="utf-8")
    finally:
        lock.release()

    assert text.splitlines()[2] == str(root.resolve())


def test_probe_names_the_holder_while_the_lock_is_held(tmp_path: Path) -> None:
    """What the operator actually needs mid-incident: who holds it, and for
    which channel. Returned all-None on Windows."""
    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"

    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    try:
        state = probe_lock(lock_path)
    finally:
        lock.release()

    assert state.held is True
    assert state.pid is not None, "a held lock must name its holder on every platform"
    assert state.stamp != ""
    assert state.channel == str(root.resolve())


def test_the_sentinel_byte_is_past_any_plausible_note(tmp_path: Path) -> None:
    """The fix only works while the note cannot grow into the locked byte. A
    note is three short lines; the offset must leave obvious headroom."""
    from debate.watcher import _LOCK_BYTE_OFFSET

    root = tmp_path / "collab"
    root.mkdir()
    lock_path = tmp_path / "state.json.lock"
    lock = WatcherLock(lock_path, channel_root=root)
    assert lock.acquire()
    try:
        written = len(lock_path.read_bytes())
    finally:
        lock.release()

    assert written < _LOCK_BYTE_OFFSET, f"note is {written}B, sentinel at {_LOCK_BYTE_OFFSET}B"
    assert _LOCK_BYTE_OFFSET >= 4096, "leave room for long absolute paths"
