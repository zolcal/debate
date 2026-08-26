"""Privacy and storage contracts for per-invocation phase telemetry."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from debate.telemetry import PhaseTelemetry, storage_metrics


def test_phase_telemetry_keeps_only_controlled_enums_and_numbers(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    writer = PhaseTelemetry(path, component="controller")
    writer.emit(
        "adapter_finished",
        party="codex",
        phase="sealed",
        sequence=1,
        attempt=1,
        returncode=0,
        duration_ms=12.5,
    )
    event = json.loads(path.read_text(encoding="utf-8"))
    assert event == {
        "telemetry_schema_version": 1,
        "component": "controller",
        "event": "adapter_finished",
        "elapsed_ms": event["elapsed_ms"],
        "party": "codex",
        "phase": "sealed",
        "sequence": 1,
        "attempt": 1,
        "returncode": 0,
        "duration_ms": 12.5,
    }
    assert event["elapsed_ms"] >= 0
    assert "command" not in event
    assert "output" not in event
    assert "path" not in event


def test_phase_telemetry_refuses_content_bearing_fields(tmp_path: Path) -> None:
    writer = PhaseTelemetry(tmp_path / "events.jsonl", component="bridge")
    with pytest.raises(ValueError, match="unsupported telemetry fields"):
        writer.emit("seat_finished", output="private model output")
    with pytest.raises(ValueError, match="short safe enum"):
        writer.emit("seat_finished", seat_id="contains private prose")


def test_storage_metrics_counts_apparent_and_allocated_bytes(tmp_path: Path) -> None:
    (tmp_path / "one").write_bytes(b"abc")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "two").write_bytes(b"12345")
    (tmp_path / "link").symlink_to(tmp_path / "one")
    measured = storage_metrics(tmp_path)
    assert measured.file_count == 2
    assert measured.apparent_bytes == 8
    assert measured.allocated_bytes >= measured.apparent_bytes
