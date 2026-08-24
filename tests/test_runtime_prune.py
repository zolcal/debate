"""Exact-channel runtime inspection and terminal-only cache pruning."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from debate import channel, runtime
from debate.__main__ import _watcher_config, main
from debate.watcher import WatcherLock, tick_lock_path


def _profile(party: str) -> dict[str, object]:
    return {
        "command": [sys.executable, "adapter.py", "{input_path}", "{result_path}"],
        "provider": party,
        "requested_model": "fixture",
        "author_relationship": "author-independent",
        "reasoning_effort": "default",
        "cli_version": "fixture",
        "cost_mode": "local",
        "authentication_mode": "fixture",
        "permission_policy": "fixture",
        "settings_sources": [],
        "environment_allowlist": ["PATH"],
        "retry_limit": 1,
        "result_schema_version": 1,
    }


def _world(
    tmp_path: Path, *, terminal: bool = True, legacy_runtime: bool = False
) -> tuple[Path, str, Path, Path]:
    project = tmp_path / "project"
    root = project / "collab"
    name = "prune-fixture-12345"
    runtime_root = (
        project / "var" / "debate" / name
        if legacy_runtime
        else project / ".debate" / "runtime" / name
    )
    config_path = project / ".debate" / "channels" / name / "watcher.json"
    project.mkdir(parents=True)
    channel.init_channel(
        root,
        ("alpha", "beta"),
        "owner",
        name=name,
        managed_version=channel.BROKERED_MANAGED_VERSION,
    )
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        json.dumps(
            {
                "state_path": str(runtime_root / "watcher-state.json"),
                "runtime_root": str(runtime_root),
                "source_ref": "0" * 40,
                "whole_case_timeout_seconds": 900,
                "scheduler_interval_seconds": 5,
                "retry_seconds": 30,
                "adapters": {
                    "alpha": _profile("alpha"),
                    "beta": _profile("beta"),
                },
                "docket_files": [],
            }
        ),
        encoding="utf-8",
    )
    deadline = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    channel.post(
        root,
        "owner",
        "review-request",
        "case-one",
        "fixture",
        name=name,
        _initial_turn="alpha",
        _managed_phase="docket",
        _case_deadline=deadline,
    )
    case_root = runtime_root / "cases" / "case-one"
    invocation = case_root / "invocations" / "1-alpha-1"
    for directory in ("home", "build", "tmp"):
        target = invocation / directory
        target.mkdir(parents=True)
        (target / "cache.bin").write_bytes((directory * 17).encode())
    (invocation / "input.json").write_text("{}", encoding="utf-8")
    (invocation / "result.json").write_text("{}", encoding="utf-8")
    (invocation / "stdout.txt").write_text("seat output", encoding="utf-8")
    (invocation / "stderr.txt").write_text("", encoding="utf-8")
    (case_root / "case.json").write_text(
        json.dumps({"phase": "terminal" if terminal else "deliberation"}),
        encoding="utf-8",
    )
    if terminal:
        channel.close_managed_case(
            root,
            thread="case-one",
            result="PASS",
            close_reason="fixture",
            body="fixture close",
            name=name,
        )
    return root, name, config_path, runtime_root


def test_inspection_is_read_only_and_splits_retained_from_regenerable(tmp_path: Path) -> None:
    root, name, config_path, runtime_root = _world(tmp_path)
    config = _watcher_config(root, config_path, name)
    before = sorted((str(path), path.stat().st_mtime_ns) for path in runtime_root.rglob("*"))
    report = runtime.inspect(config, name)
    after = sorted((str(path), path.stat().st_mtime_ns) for path in runtime_root.rglob("*"))
    assert before == after
    assert report.regenerable_bytes > 0
    assert report.retained_bytes > 0
    assert {path.name for path in report.regenerable_paths} == {"home", "build", "tmp"}


def test_prune_requires_confirmation_and_terminal_case(tmp_path: Path) -> None:
    root, name, config_path, _runtime_root = _world(tmp_path)
    with pytest.raises(channel.ChannelError, match="needs --yes"):
        runtime.prune(
            channel_root=root,
            channel_name=name,
            config_path=config_path,
            load_config=_watcher_config,
            tool_version="test",
            confirmed=False,
        )
    open_root, open_name, open_config, _ = _world(tmp_path / "other", terminal=False)
    with pytest.raises(channel.ChannelError, match="not terminal"):
        runtime.prune(
            channel_root=open_root,
            channel_name=open_name,
            config_path=open_config,
            load_config=_watcher_config,
            tool_version="test",
            confirmed=True,
        )


def test_prune_holds_watcher_lock_and_retains_evidence(tmp_path: Path) -> None:
    root, name, config_path, runtime_root = _world(tmp_path)
    config = _watcher_config(root, config_path, name)
    lock = WatcherLock(tick_lock_path(config.state_path), root)
    assert lock.acquire()
    try:
        with pytest.raises(channel.ChannelError, match="watcher lock is held"):
            runtime.prune(
                channel_root=root,
                channel_name=name,
                config_path=config_path,
                load_config=_watcher_config,
                tool_version="test",
                confirmed=True,
            )
    finally:
        lock.release()
    invocation = runtime_root / "cases" / "case-one" / "invocations" / "1-alpha-1"
    before = runtime.inspect(config, name)
    after = runtime.prune(
        channel_root=root,
        channel_name=name,
        config_path=config_path,
        load_config=_watcher_config,
        tool_version="test",
        confirmed=True,
    )
    assert after.regenerable_bytes == 0
    assert before.regenerable_bytes > 0
    for name_to_remove in ("home", "build", "tmp"):
        assert not (invocation / name_to_remove).exists()
    for name_to_keep in ("input.json", "result.json", "stdout.txt", "stderr.txt"):
        assert (invocation / name_to_keep).is_file()
    receipts = [
        json.loads(line)
        for line in (runtime_root / runtime.RECEIPT_NAME).read_text().splitlines()
    ]
    assert [item["event"] for item in receipts] == ["prune-intent", "prune-complete"]
    assert receipts[1]["freed_bytes"] == before.regenerable_bytes
    # Idempotent: a second confirmed prune records zero work and preserves evidence.
    again = runtime.prune(
        channel_root=root,
        channel_name=name,
        config_path=config_path,
        load_config=_watcher_config,
        tool_version="test",
        confirmed=True,
    )
    assert again.regenerable_bytes == 0
    assert (invocation / "result.json").is_file()


def test_prune_lock_remains_held_through_both_receipts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, name, config_path, _runtime_root = _world(tmp_path)
    config = _watcher_config(root, config_path, name)
    original = runtime._append_receipt
    lock_observations: list[bool] = []

    def checked(path: Path, payload: dict[str, object]) -> None:
        competitor = WatcherLock(tick_lock_path(config.state_path), root)
        acquired = competitor.acquire()
        lock_observations.append(acquired)
        if acquired:
            competitor.release()
        original(path, payload)

    monkeypatch.setattr(runtime, "_append_receipt", checked)
    runtime.prune(
        channel_root=root,
        channel_name=name,
        config_path=config_path,
        load_config=_watcher_config,
        tool_version="test",
        confirmed=True,
    )
    assert lock_observations == [False, False]


def test_legacy_runtime_partial_invocation_and_interrupted_intent_are_safe(
    tmp_path: Path,
) -> None:
    root, name, config_path, runtime_root = _world(tmp_path, legacy_runtime=True)
    invocation = runtime_root / "cases" / "case-one" / "invocations" / "1-alpha-1"
    # A partly-created invocation is normal after interruption.
    for absent in ("build", "tmp"):
        target = invocation / absent
        for child in target.iterdir():
            child.unlink()
        target.rmdir()
    receipt_path = runtime_root / runtime.RECEIPT_NAME
    receipt_path.write_text(
        json.dumps({"event": "prune-intent", "intent_id": "interrupted-old"}) + "\n",
        encoding="utf-8",
    )
    before = runtime.inspect(_watcher_config(root, config_path, name), name)
    assert {path.name for path in before.regenerable_paths} == {"home"}
    runtime.prune(
        channel_root=root,
        channel_name=name,
        config_path=config_path,
        load_config=_watcher_config,
        tool_version="test",
        confirmed=True,
    )
    assert not (invocation / "home").exists()
    assert (invocation / "result.json").is_file()
    events = [json.loads(line)["event"] for line in receipt_path.read_text().splitlines()]
    assert events == ["prune-intent", "prune-intent", "prune-complete"]


def test_symlink_target_and_wrong_channel_config_refuse_without_mutation(tmp_path: Path) -> None:
    root, name, config_path, runtime_root = _world(tmp_path)
    home = runtime_root / "cases" / "case-one" / "invocations" / "1-alpha-1" / "home"
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "keep.txt").write_text("keep", encoding="utf-8")
    for child in home.iterdir():
        child.unlink()
    home.rmdir()
    home.symlink_to(outside, target_is_directory=True)
    with pytest.raises(channel.ChannelError, match="symlink"):
        runtime.prune(
            channel_root=root,
            channel_name=name,
            config_path=config_path,
            load_config=_watcher_config,
            tool_version="test",
            confirmed=True,
        )
    assert (outside / "keep.txt").is_file()
    raw = json.loads(config_path.read_text())
    wrong_runtime = runtime_root.parent / "different-channel"
    raw["runtime_root"] = str(wrong_runtime)
    raw["state_path"] = str(wrong_runtime / "watcher-state.json")
    config_path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(channel.ChannelError, match="does not match channel"):
        runtime.prune(
            channel_root=root,
            channel_name=name,
            config_path=config_path,
            load_config=_watcher_config,
            tool_version="test",
            confirmed=True,
        )


def test_cli_inspection_and_prune_surfaces(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root, name, config_path, _runtime_root = _world(tmp_path)
    assert main([
        "runtime", "--root", str(root), "--channel", name, "--config", str(config_path)
    ]) == 0
    assert "retained provenance bytes:" in capsys.readouterr().out
    assert main([
        "runtime", "--root", str(root), "--channel", name, "--config", str(config_path),
        "--prune",
    ]) == 1
    assert "needs --yes" in capsys.readouterr().err


def test_five_sparse_channels_report_and_prune_only_regenerable_scope(tmp_path: Path) -> None:
    total = 0
    worlds: list[tuple[Path, str, Path, Path]] = []
    for index in range(5):
        root, name, config_path, runtime_root = _world(tmp_path / f"channel-{index}")
        worlds.append((root, name, config_path, runtime_root))
        sparse = (
            runtime_root
            / "cases"
            / "case-one"
            / "invocations"
            / "1-alpha-1"
            / "home"
            / "sparse-cache.bin"
        )
        with sparse.open("wb") as handle:
            handle.truncate(140 * 1024 * 1024)
            handle.flush()
            os.fsync(handle.fileno())
        total += runtime.inspect(_watcher_config(root, config_path, name), name).regenerable_bytes
    assert total >= 5 * 140 * 1024 * 1024
    for root, name, config_path, runtime_root in worlds:
        report = runtime.prune(
            channel_root=root,
            channel_name=name,
            config_path=config_path,
            load_config=_watcher_config,
            tool_version="test",
            confirmed=True,
        )
        assert report.regenerable_bytes == 0
        assert (runtime_root / "cases" / "case-one" / "case.json").is_file()
