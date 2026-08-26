"""Small, privacy-safe phase telemetry for managed Debate invocations."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path


SCHEMA_VERSION = 1
_SAFE_TEXT = re.compile(r"^[A-Za-z0-9_.@:/-]{1,64}$")
_FIELDS = frozenset(
    {
        "party",
        "seat_id",
        "phase",
        "sequence",
        "attempt",
        "returncode",
        "duration_ms",
        "schema_version",
        "file_count",
        "apparent_bytes",
        "allocated_bytes",
    }
)


@dataclass(frozen=True)
class StorageMetrics:
    file_count: int
    apparent_bytes: int
    allocated_bytes: int


def storage_metrics(root: Path) -> StorageMetrics:
    """Measure retained regular files without following symlinks."""
    file_count = 0
    apparent_bytes = 0
    allocated_bytes = 0
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        stat = path.stat()
        file_count += 1
        apparent_bytes += stat.st_size
        allocated_bytes += stat.st_blocks * 512
    return StorageMetrics(file_count, apparent_bytes, allocated_bytes)


class PhaseTelemetry:
    """Append controlled numeric/enum events relative to one monotonic start."""

    def __init__(self, path: Path, *, component: str, started_ns: int | None = None) -> None:
        if not _SAFE_TEXT.fullmatch(component):
            raise ValueError("telemetry component is not a safe enum")
        self.path = path
        self.component = component
        self.started_ns = started_ns if started_ns is not None else time.monotonic_ns()

    def elapsed_ms(self) -> float:
        return round((time.monotonic_ns() - self.started_ns) / 1_000_000, 3)

    def emit(self, event: str, **fields: str | int | float) -> None:
        if not _SAFE_TEXT.fullmatch(event):
            raise ValueError("telemetry event is not a safe enum")
        unknown = sorted(set(fields) - _FIELDS)
        if unknown:
            raise ValueError(f"unsupported telemetry fields: {', '.join(unknown)}")
        for value in fields.values():
            if isinstance(value, str) and not _SAFE_TEXT.fullmatch(value):
                raise ValueError("telemetry text must be a short safe enum")
            if isinstance(value, bool) or not isinstance(value, (str, int, float)):
                raise ValueError("telemetry values must be safe enums or numbers")
        payload = {
            "telemetry_schema_version": SCHEMA_VERSION,
            "component": self.component,
            "event": event,
            "elapsed_ms": self.elapsed_ms(),
            **fields,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
