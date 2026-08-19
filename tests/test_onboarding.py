"""Onboarding state machine: `debate onboarding status` (plan Slice 1A).

The product path treats a missing profile as NOT approved (offer_setup),
never as unrestricted access -- that reading belongs to the 0.7 direct CLI
alone. status() is read-only by construction: these tests assert zero
filesystem writes for every state it can report.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from debate import channel, onboarding
from debate import __version__


def _write_registry(path: Path, *, tool_version: str, seats_obj: dict[str, object] | None = None) -> None:
    payload = {
        "registry_version": 1,
        "tool_version": tool_version,
        "discovered_at": "2026-08-19T00:00:00+00:00",
        "seats": seats_obj or {},
        "last_pair": {},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def _seat(command_head: str, *, present: bool = True, smoke: dict[str, str] | None = None) -> dict[str, object]:
    return {
        "vendor": "probe",
        "submodel": "fake",
        "effort": None,
        "commands": [[command_head, "{prompt}"]],
        "source": "manual",
        "present": present,
        "smoke": smoke,
    }


def _snapshot(root: Path) -> list[tuple[str, float, int]]:
    entries = []
    for path in sorted(root.rglob("*")):
        stat = path.stat()
        entries.append((str(path), stat.st_mtime, stat.st_size if path.is_file() else -1))
    return entries


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    registry = tmp_path / "config" / "seats.json"
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry))
    return registry, project


def test_fresh_machine_offers_setup(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    report = onboarding.status(str(project))
    assert report["registry_state"] == "missing"
    assert report["profile_state"] == "missing"
    assert report["attention"] == "offer_setup"
    assert report["approved_seats"] == []
    assert report["schema_version"] == 1
    assert report["product_version"] == __version__


def test_registry_without_profile_still_offers_setup(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat("/bin/sh")})
    report = onboarding.status(str(project))
    assert report["registry_state"] == "current"
    assert report["profile_state"] == "missing"
    assert report["attention"] == "offer_setup"


def test_approved_and_present_is_ready_and_quiet(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat("/bin/sh")})
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}), encoding="utf-8"
    )
    report = onboarding.status(str(project))
    assert report["profile_state"] == "approved"
    assert report["attention"] == "ready"
    assert report["approved_seats"] == [
        {"seat_id": "probe/fake", "present": True, "smoke": "never", "cost_mode": "unknown"}
    ]


def test_stale_registry_offers_refresh(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version="0.0.1", seats_obj={"probe/fake": _seat("/bin/sh")})
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}), encoding="utf-8"
    )
    report = onboarding.status(str(project))
    assert report["registry_state"] == "stale"
    assert report["attention"] == "offer_refresh"
    reasons = report["reasons"]
    assert isinstance(reasons, list)
    assert any("rescan required" in reason for reason in reasons)


def test_vanished_binary_requires_repair(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(
        registry,
        tool_version=__version__,
        seats_obj={"probe/fake": _seat("/nonexistent/debate-test-binary")},
    )
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}), encoding="utf-8"
    )
    report = onboarding.status(str(project))
    assert report["attention"] == "repair_required"
    assert report["approved_seats"] == [
        {"seat_id": "probe/fake", "present": False, "smoke": "never", "cost_mode": "unknown"}
    ]


def test_failed_smoke_offers_refresh(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(
        registry,
        tool_version=__version__,
        seats_obj={
            "probe/fake": _seat(
                "/bin/sh", smoke={"at": "2026-08-19T00:00:00+00:00", "result": "fail"}
            )
        },
    )
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}), encoding="utf-8"
    )
    report = onboarding.status(str(project))
    assert report["attention"] == "offer_refresh"
    reasons = report["reasons"]
    assert isinstance(reasons, list)
    assert any("failed its last smoke" in reason for reason in reasons)


def test_broken_registry_requires_repair(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text("{not json", encoding="utf-8")
    report = onboarding.status(str(project))
    assert report["registry_state"] == "broken"
    assert report["attention"] == "repair_required"


def test_broken_profile_requires_repair(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat("/bin/sh")})
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": []}), encoding="utf-8"
    )
    report = onboarding.status(str(project))
    assert report["profile_state"] == "broken"
    assert report["attention"] == "repair_required"


def test_profile_with_unknown_seat_requires_repair(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={})
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["gone/seat"]}), encoding="utf-8"
    )
    report = onboarding.status(str(project))
    assert report["profile_state"] == "broken"
    assert report["attention"] == "repair_required"


def test_relative_project_is_refused(isolated: tuple[Path, Path]) -> None:
    with pytest.raises(channel.ChannelError, match="absolute"):
        onboarding.status("relative/path")


def test_status_never_writes(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version="0.0.1", seats_obj={"probe/fake": _seat("/bin/sh")})
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}), encoding="utf-8"
    )
    before = _snapshot(tmp_path)
    onboarding.status(str(project))
    onboarding.status(str(project / "missing-subdir-never-created"))
    assert _snapshot(tmp_path) == before


def test_status_lines_are_ascii(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    report = onboarding.status(str(project))
    for line in onboarding.status_lines(report):
        assert all(ord(c) < 128 for c in line), line
