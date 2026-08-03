"""Operator-facing output must be pure ASCII.

CI (windows-latest) hit `UnicodeDecodeError: byte 0xb7` reading a watcher log:
the banner used `·` (U+00B7), and Windows `print()` to a REDIRECTED stream uses
the locale encoding (cp1252), not UTF-8. So the log was not valid UTF-8 and any
reader assuming UTF-8 — the sane default, and what our own test did — fails.

The tool is stdlib-only and cross-platform by design; decorative typography in
log lines is a portability liability for no benefit. Source comments and
docstrings are unaffected: Python reads source as UTF-8 regardless of locale.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from debate import channel
from debate.watcher import LockState, WatcherConfig, read_status, status

NOW = datetime(2026, 8, 3, 12, 0, 0, tzinfo=timezone.utc)
HELD = LockState(held=True, pid=4242, stamp="2026-08-03T11:00:00+00:00", cwd="/x", channel="/y")


def _assert_ascii(text: str, where: str) -> None:
    bad = {c: hex(ord(c)) for c in text if ord(c) > 127}
    assert not bad, f"non-ASCII in {where}: {bad} -> would be written in the locale encoding on Windows"


def test_the_status_report_is_ascii(tmp_path: Path) -> None:
    root = tmp_path / "collab"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    cfg = WatcherConfig(channel_root=root, state_path=tmp_path / "state.json")

    lines, result = read_status(cfg, NOW)

    for line in lines:
        _assert_ascii(line, "watch-status report")
    _assert_ascii(f"{result.verdict}: {result.detail}", "watch-status verdict")


def test_every_status_verdict_detail_is_ascii(tmp_path: Path) -> None:
    """Walk the whole taxonomy: a verdict reached only during an incident is
    exactly the one nobody would notice was unreadable."""
    root = tmp_path / "collab"
    root.mkdir()
    cfg = WatcherConfig(
        channel_root=root, state_path=tmp_path / "state.json",
        commands={"bob": ["echo"]}, prompts={"bob": "go"}, debounce_seconds={"bob": 60},
    )
    cases: list[tuple[dict[str, Any], dict[str, Any]]] = [
        ({"seq": 1, "turn": "", "thread": "", "updated_at": ""}, {}),                      # IDLE
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T11:59:30+00:00"}, {}),  # DRIVING
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"}, {}),  # STALE uninvoked
        ({"seq": 1, "turn": "kimi", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"}, {}), # MANUAL
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T11:00:00+00:00"},
         {"invocations": {"1": {"count": 1, "last_at": "2026-08-03T11:55:00+00:00"}}}),    # INVOKED
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"},
         {"invocations": {"1": {"count": 1, "last_at": "2026-08-03T09:00:00+00:00"}}}),    # STALE invoked
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T11:00:00+00:00"},
         {"escalated": ["t:1"]}),                                                          # ESCALATED
    ]
    seen = set()
    for signal, state in cases:
        for lock in (LockState(False, None, "", None), HELD):
            result = status(signal, state, cfg, NOW, lock)
            seen.add(result.verdict)
            _assert_ascii(f"{result.verdict}: {result.detail}", f"verdict {result.verdict}")

    assert seen == {"IDLE", "DRIVING", "STALE", "MANUAL", "INVOKED", "ESCALATED"}, seen


def test_refusal_messages_are_ascii(tmp_path: Path) -> None:
    """Both refusals are read during an incident, often out of a redirected log."""
    from debate.watcher import _refusal_message, _verify_channel_binding
    from debate.channel import ChannelError

    _assert_ascii(_refusal_message(tmp_path / "absent.lock"), "watch-once refusal")

    cfg = WatcherConfig(channel_root=tmp_path / "mine", state_path=tmp_path / "state.json")
    try:
        _verify_channel_binding({"channel_root": str(tmp_path / "theirs")}, cfg)
    except ChannelError as error:
        _assert_ascii(str(error), "channel-binding refusal")
    else:  # pragma: no cover
        raise AssertionError("expected a refusal")
