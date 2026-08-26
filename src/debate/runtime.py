"""Inspect and explicitly prune one terminal managed Debate runtime.

Only isolated invocation ``home``, ``build`` and ``tmp`` trees are
regenerable. Every channel/case/input/result/stream/provenance artifact stays.
"""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from . import channel
from .watcher import WatcherConfig, WatcherLock, tick_lock_path

REGENERABLE_NAMES = frozenset({"home", "build", "tmp"})
RECEIPT_NAME = "prune-receipts.jsonl"


@dataclass(frozen=True)
class RuntimeReport:
    channel_name: str
    runtime_root: Path
    retained_bytes: int
    regenerable_bytes: int
    regenerable_paths: tuple[Path, ...]

    @property
    def total_bytes(self) -> int:
        return self.retained_bytes + self.regenerable_bytes


def _tree_bytes(path: Path) -> int:
    """Logical file bytes, without following symlinks."""
    if path.is_symlink():
        return path.lstat().st_size
    if path.is_file():
        return path.stat().st_size
    total = 0
    if not path.exists():
        return total
    for root, directories, files in os.walk(path, followlinks=False):
        root_path = Path(root)
        for name in directories:
            candidate = root_path / name
            if candidate.is_symlink():
                total += candidate.lstat().st_size
        for name in files:
            candidate = root_path / name
            try:
                total += candidate.lstat().st_size
            except OSError as error:
                raise channel.ChannelError(
                    f"refused: cannot inspect runtime path {candidate}: {error}"
                ) from error
    return total


def _regenerable_paths(runtime_root: Path) -> tuple[Path, ...]:
    candidates: list[Path] = []
    cases = runtime_root / "cases"
    if not cases.is_dir():
        return ()
    for case_root in sorted(cases.iterdir()):
        invocations = case_root / "invocations"
        if not invocations.is_dir():
            continue
        for invocation in sorted(invocations.iterdir()):
            if not invocation.is_dir() or invocation.is_symlink():
                continue
            for name in sorted(REGENERABLE_NAMES):
                candidate = invocation / name
                if candidate.exists() or candidate.is_symlink():
                    candidates.append(candidate)
    return tuple(candidates)


def inspect(config: WatcherConfig, channel_name: str) -> RuntimeReport:
    if config.channel_name != channel_name or config.broker is None:
        raise channel.ChannelError(
            f"refused: watcher config is not the fully managed channel {channel_name!r}"
        )
    runtime_root = config.broker.runtime_root.resolve()
    if runtime_root.name != channel_name:
        raise channel.ChannelError(
            f"refused: runtime directory {runtime_root.name!r} does not match channel "
            f"{channel_name!r}"
        )
    candidates = _regenerable_paths(runtime_root)
    regenerable = sum(_tree_bytes(path) for path in candidates)
    total = _tree_bytes(runtime_root)
    return RuntimeReport(
        channel_name=channel_name,
        runtime_root=runtime_root,
        retained_bytes=max(0, total - regenerable),
        regenerable_bytes=regenerable,
        regenerable_paths=candidates,
    )


def _terminal_cases(runtime_root: Path) -> None:
    cases_root = runtime_root / "cases"
    if not cases_root.is_dir():
        raise channel.ChannelError(
            f"refused: runtime {runtime_root} has no cases directory to prune"
        )
    cases = [path for path in sorted(cases_root.iterdir()) if path.is_dir()]
    if not cases:
        raise channel.ChannelError(f"refused: runtime {runtime_root} has no cases to prune")
    for case_root in cases:
        case_path = case_root / "case.json"
        try:
            raw = json.loads(case_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as error:
            raise channel.ChannelError(
                f"refused: cannot validate case state {case_path}: {error}"
            ) from error
        if not isinstance(raw, dict) or raw.get("phase") != "terminal":
            raise channel.ChannelError(
                f"refused: case {case_root.name!r} is not terminal; no runtime state was pruned"
            )


def _validated_targets(report: RuntimeReport) -> tuple[Path, ...]:
    runtime = report.runtime_root.resolve()
    targets: list[Path] = []
    for candidate in report.regenerable_paths:
        if candidate.name not in REGENERABLE_NAMES:
            raise channel.ChannelError(f"refused: unsafe prune target name {candidate}")
        if candidate.is_symlink():
            raise channel.ChannelError(f"refused: prune target is a symlink: {candidate}")
        expected_invocations = candidate.parent.parent
        if expected_invocations.name != "invocations":
            raise channel.ChannelError(f"refused: prune target is outside an invocation: {candidate}")
        resolved = candidate.resolve()
        if not resolved.is_relative_to(runtime):
            raise channel.ChannelError(f"refused: prune target escapes runtime: {candidate}")
        targets.append(resolved)
    return tuple(targets)


def _append_receipt(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def prune(
    *,
    channel_root: Path,
    channel_name: str,
    config_path: Path,
    load_config: Callable[[Path, Path, str], WatcherConfig],
    tool_version: str,
    confirmed: bool,
) -> RuntimeReport:
    if not confirmed:
        raise channel.ChannelError(
            "refused: runtime pruning needs --yes after inspection; nothing was deleted"
        )
    initial = load_config(channel_root, config_path, channel_name)
    if initial.broker is None:
        raise channel.ChannelError("refused: runtime pruning needs a fully managed watcher config")
    lock = WatcherLock(tick_lock_path(initial.state_path), channel_root)
    if not lock.acquire():
        raise channel.ChannelError(
            "refused: the exact channel watcher lock is held; nothing was deleted"
        )
    try:
        # Re-read every mutable binding while the watcher is excluded.
        current = load_config(channel_root, config_path, channel_name)
        if current.broker is None or current.channel_name != channel_name:
            raise channel.ChannelError(
                "refused: watcher config no longer matches the requested channel"
            )
        if current.state_path.resolve() != initial.state_path.resolve():
            raise channel.ChannelError(
                "refused: watcher state binding changed while acquiring the channel lock"
            )
        signal = channel.read_signal(channel_root, channel_name)
        if signal.get("phase") != "terminal":
            raise channel.ChannelError(
                "refused: the channel is not terminal; no runtime state was pruned"
            )
        report = inspect(current, channel_name)
        _terminal_cases(report.runtime_root)
        targets = _validated_targets(report)
        receipt_path = report.runtime_root / RECEIPT_NAME
        intent_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        common = {
            "schema_version": 1,
            "intent_id": intent_id,
            "channel": channel_name,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tool_version": tool_version,
            "validated_paths": [str(path) for path in targets],
            "regenerable_bytes": report.regenerable_bytes,
        }
        _append_receipt(receipt_path, {**common, "event": "prune-intent"})
        freed = 0
        for target in targets:
            freed += _tree_bytes(target)
            shutil.rmtree(target)
        _append_receipt(
            receipt_path,
            {**common, "event": "prune-complete", "freed_bytes": freed},
        )
        return inspect(current, channel_name)
    finally:
        lock.release()
