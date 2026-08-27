"""Onboarding state machine: `debate onboarding status` (plan Slice 1A).

The product path treats a missing profile as NOT approved (offer_setup),
never as unrestricted access -- that reading belongs to the 0.7 direct CLI
alone. status() is read-only by construction: these tests assert zero
filesystem writes for every state it can report.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from debate import channel, onboarding, seats
from debate import __version__

NOW = "2026-08-19T12:00:00+00:00"


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
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
    report = onboarding.status(str(project))
    assert report["registry_state"] == "current"
    assert report["profile_state"] == "missing"
    assert report["attention"] == "offer_setup"


def test_approved_and_present_is_ready_and_quiet(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
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
    _write_registry(registry, tool_version="0.0.1", seats_obj={"probe/fake": _seat(sys.executable)})
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
                sys.executable, smoke={"at": "2026-08-19T00:00:00+00:00", "result": "fail"}
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
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
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
    _write_registry(registry, tool_version="0.0.1", seats_obj={"probe/fake": _seat(sys.executable)})
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


# --- Slice C2: detected launcher scripts as candidate rows -----------------
#
# I3 (detection is never approval): a sibling row must be visible in inspect
# but NEVER writable through approve. scan_siblings itself is monkeypatched
# in every test below (the brief's preferred seam) so these tests stay
# independent of whatever wrapper binaries happen to sit on the real PATH;
# PATH is additionally pinned to system dirs so catalog discovery (which DOES
# read the real PATH) never seats an incidental binary like this host's own
# `claude` CLI.


def _sibling(
    vendor: str = "deepseek",
    binary_name: str = "deepseek-pro-agent",
    binary_path: str = "/opt/bin/deepseek-pro-agent",
) -> seats.SiblingCandidate:
    return seats.SiblingCandidate(
        vendor=vendor,
        binary_name=binary_name,
        binary_path=binary_path,
        seat_id=f"{vendor}/wrapper:{binary_name}",
    )


def test_inspect_lists_sibling_as_candidate_row(
    isolated: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    sibling = _sibling()
    monkeypatch.setattr(seats, "scan_siblings", lambda: [sibling])
    report = onboarding.inspect(str(project), now=NOW)
    candidates = report["candidates"]
    assert isinstance(candidates, list)
    seat_ids = [row["seat_id"] for row in candidates]
    # Combined registry + sibling rows, one sort over the union.
    assert seat_ids == ["deepseek/wrapper:deepseek-pro-agent", "probe/fake"]
    row = candidates[0]
    assert row == {
        "seat_id": "deepseek/wrapper:deepseek-pro-agent",
        "vendor": "deepseek",
        "submodel": None,
        "effort": None,
        "command": ["/opt/bin/deepseek-pro-agent"],
        "source": "unverified-wrapper",
        "present": True,
        "smoke": "never",
        "cost_mode": "unknown",
        "existing": False,
    }


def test_candidate_revision_changes_when_sibling_appears_or_vanishes(
    isolated: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    _, project = isolated
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setattr(seats, "scan_siblings", lambda: [])
    empty_revision = onboarding.inspect(str(project), now=NOW)["candidate_revision"]
    monkeypatch.setattr(seats, "scan_siblings", lambda: [_sibling()])
    with_sibling_revision = onboarding.inspect(str(project), now=NOW)["candidate_revision"]
    assert empty_revision != with_sibling_revision


def test_inspect_with_sibling_present_writes_nothing(
    isolated: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setattr(seats, "scan_siblings", lambda: [_sibling()])
    before = _snapshot(tmp_path)
    onboarding.inspect(str(project), now=NOW)
    assert _snapshot(tmp_path) == before


def test_approve_refuses_sibling_id_with_declaration_hint(
    isolated: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    sibling = _sibling()
    monkeypatch.setattr(seats, "scan_siblings", lambda: [sibling])
    report = onboarding.inspect(str(project), now=NOW)
    revision = str(report["candidate_revision"])
    before = _snapshot(tmp_path)
    with pytest.raises(channel.ChannelError) as exc_info:
        onboarding.approve(
            str(project), allow=[sibling.seat_id], candidate_revision=revision,
            confirmed=True, now=NOW,
        )
    message = str(exc_info.value)
    assert "detected launcher script" in message
    assert "not a registered seat" in message
    assert "debate seats add" in message
    assert sibling.seat_id in message
    assert _snapshot(tmp_path) == before
    assert not (project / "debate-profile.json").exists()


def test_approve_refuses_mixed_allow_of_real_seat_and_sibling(
    isolated: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    sibling = _sibling()
    monkeypatch.setattr(seats, "scan_siblings", lambda: [sibling])
    report = onboarding.inspect(str(project), now=NOW)
    revision = str(report["candidate_revision"])
    before = _snapshot(tmp_path)
    with pytest.raises(channel.ChannelError, match="detected launcher script"):
        onboarding.approve(
            str(project), allow=["probe/fake", sibling.seat_id],
            candidate_revision=revision, confirmed=True, now=NOW,
        )
    assert _snapshot(tmp_path) == before
    assert not (project / "debate-profile.json").exists()


def test_sibling_never_appears_in_status_approved_seats(
    isolated: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """approve refuses the sibling id even though the candidate_revision echo
    is correct -- a profile can never contain one because approve refuses it
    before any write, so status() can never surface it."""
    registry, project = isolated
    _write_registry(registry, tool_version=__version__, seats_obj={"probe/fake": _seat(sys.executable)})
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    sibling = _sibling()
    monkeypatch.setattr(seats, "scan_siblings", lambda: [sibling])
    report = onboarding.inspect(str(project), now=NOW)
    revision = str(report["candidate_revision"])
    with pytest.raises(channel.ChannelError, match="detected launcher script"):
        onboarding.approve(
            str(project), allow=[sibling.seat_id], candidate_revision=revision,
            confirmed=True, now=NOW,
        )
    status_report = onboarding.status(str(project))
    assert status_report["approved_seats"] == []
    assert status_report["profile_state"] == "missing"
