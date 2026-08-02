"""Slice 2 of docs/plans/2026-08-01-watcher-liveness-and-ops-gaps.md (APPROVED MSG-119).

Watcher output must say WHICH channel it is about, and must appear while the
process is still alive. Both incidents turned on the opposite: `ps` showed a
watcher and nobody could tell which project it served, and an empty `nohup` log
was read as a dead process when it was only a buffered one.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from debate import channel
from debate.watcher import WatcherConfig, watch


def make_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    return root


def config(root: Path, **overrides: Any) -> WatcherConfig:
    defaults: dict[str, Any] = dict(
        channel_root=root,
        state_path=root.parent / "watcher-state.json",
        commands={},
        prompts={},
        debounce_seconds={},
        retry_seconds=1800,
    )
    defaults.update(overrides)
    return WatcherConfig(**defaults)


def _fail_sleep(_seconds: float) -> None:
    raise AssertionError("watch() must not sleep in these tests")


def test_watch_banner_names_the_channel_and_state_before_any_tick(tmp_path: Path) -> None:
    """`ps` cannot tell two watchers apart — same binary, same `--root collab`.
    The first line of output must, or the operator is back to reading /proc."""
    root = make_channel(tmp_path)
    cfg = config(root)
    lines: list[str] = []

    watch(cfg, interval_seconds=1, until_close=False, max_ticks=1, emit=lines.append, sleep=_fail_sleep)

    assert lines, "watch() must announce itself even when the tick does nothing"
    banner = lines[0]
    assert str(root.resolve()) in banner
    assert str(cfg.state_path) in banner


def test_every_emitted_line_carries_the_channel_tag(tmp_path: Path) -> None:
    """Two watchers' logs interleaved in one journal are useless without a tag
    on each line — the banner alone scrolls away."""
    root = make_channel(tmp_path)
    cfg = config(root)
    lines: list[str] = []

    watch(cfg, interval_seconds=1, until_close=False, max_ticks=1, emit=lines.append, sleep=_fail_sleep)

    tag = f"[{cfg.state_path.stem}]"
    assert all(line.startswith(tag) for line in lines), f"untagged: {[ln for ln in lines if not ln.startswith(tag)]}"


def test_watch_output_is_visible_while_the_process_is_still_running(tmp_path: Path) -> None:
    """G5, as an executable test. Block-buffered stdout under redirection made
    an empty log look like a dead watcher during the 2026-07-28 session. The
    banner must reach the file BEFORE the process exits — so this asserts on a
    still-running process, not on its final output."""
    root = make_channel(tmp_path)
    state_path = tmp_path / "watcher-state.json"
    config_path = tmp_path / "watcher.json"
    config_path.write_text(json.dumps({"state_path": str(state_path)}), encoding="utf-8")
    log = tmp_path / "watch.log"

    with log.open("w", encoding="utf-8") as handle:
        proc = subprocess.Popen(
            [sys.executable, "-m", "debate", "watch", "--root", str(root),
             "--config", str(config_path), "--interval", "30", "--max-ticks", "2"],
            stdout=handle,
            stderr=subprocess.STDOUT,
            env={**dict(__import__("os").environ), "PYTHONPATH": str(Path.cwd() / "src")},
        )
        try:
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                if str(root.resolve()) in log.read_text(encoding="utf-8"):
                    break
                assert proc.poll() is None, "process exited before the banner was readable — that is the bug"
                time.sleep(0.1)
            else:  # pragma: no cover - only on a genuine buffering regression
                raise AssertionError(f"banner never appeared while running; log held {log.read_text()!r}")
        finally:
            proc.kill()
            proc.wait()
