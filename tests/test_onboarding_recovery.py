"""Migration, recovery, and honest non-happy paths (plan Slice 3)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest



from debate import channel, onboarding
from debate.controller import _baseline_environment

def _hermetic_path() -> str:
    """Discovery must find no agent CLIs. POSIX keeps the literal system
    dirs; Windows substitutes git's own directory (git shims and nothing
    else), because /usr/bin does not exist there and the fixtures' git
    subprocesses still need to resolve (field finding F25)."""
    if os.name == "nt":
        git = shutil.which("git")
        return str(Path(git).parent) if git else ""
    return "/usr/bin:/bin"


REPO_ROOT = Path(__file__).resolve().parent.parent
NOW = "2026-08-19T12:00:00+00:00"


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    registry = tmp_path / "config" / "seats.json"
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry))
    monkeypatch.setenv("PATH", _hermetic_path())
    return registry, project


def _registry_payload(tool_version: str, seats_obj: dict[str, object]) -> dict[str, object]:
    return {
        "registry_version": 1,
        "tool_version": tool_version,
        "discovered_at": "2026-07-01T00:00:00+00:00",
        "seats": seats_obj,
        "last_pair": {"": ["old/one", "old/two"]},
    }


def _seat(command: list[str], *, vendor: str, smoke: dict[str, str] | None = None) -> dict[str, object]:
    return {
        "vendor": vendor,
        "submodel": "fake",
        "effort": None,
        "commands": [command],
        "source": "manual",
        "present": True,
        "smoke": smoke,
    }


def test_upgrade_from_07_registry_shows_candidates_but_approves_nothing(
    isolated: tuple[Path, Path],
) -> None:
    """A pre-0.8 registry (old tool_version, remembered last_pair) is
    candidate input only: labelled existing, state stale, nothing approved."""
    registry, project = isolated
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        json.dumps(
            _registry_payload(
                "0.6.0",
                {
                    "old/one": _seat([sys.executable, "{prompt}"], vendor="old"),
                    "old/two": _seat(["/bin/dash", "{prompt}"], vendor="older"),
                },
            )
        ),
        encoding="utf-8",
    )
    report = onboarding.inspect(str(project), now=NOW)
    assert report["existing_registry_state"] == "stale"
    candidates = report["candidates"]
    assert isinstance(candidates, list)
    labelled = {str(row["seat_id"]): row["existing"] for row in candidates if isinstance(row, dict)}
    assert labelled["old/one"] is True and labelled["old/two"] is True
    state = onboarding.status(str(project))
    assert state["profile_state"] == "missing"
    assert state["attention"] == "offer_setup"
    assert state["approved_seats"] == []  # last_pair never became approval


def test_no_detected_clis_reports_none_and_refuses_empty_approval(
    isolated: tuple[Path, Path],
) -> None:
    _, project = isolated
    report = onboarding.inspect(str(project), now=NOW)
    assert report["candidates"] == []
    with pytest.raises(channel.ChannelError, match="zero selected"):
        onboarding.approve(
            str(project), allow=[], candidate_revision=str(report["candidate_revision"]),
            confirmed=True, now=NOW,
        )
    assert not (project / "debate-profile.json").exists()


def _approved_project(registry: Path, project: Path, seats_obj: dict[str, object], allow: list[str]) -> None:
    from debate import __version__

    payload = _registry_payload(__version__, seats_obj)
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps(payload), encoding="utf-8")
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": allow}), encoding="utf-8"
    )


def test_stale_smoke_offers_refresh_and_is_labelled(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _approved_project(
        registry, project,
        {"probe/fake": _seat([sys.executable, "{prompt}"], vendor="probe",
                             smoke={"at": "2026-01-01T00:00:00+00:00", "result": "pass"})},
        ["probe/fake"],
    )
    report = onboarding.status(str(project))
    assert report["attention"] == "offer_refresh"
    approved = report["approved_seats"]
    assert isinstance(approved, list)
    first = approved[0]
    assert isinstance(first, dict) and first["smoke"] == "stale"


def test_duplicate_selected_command_is_explained(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _approved_project(
        registry, project,
        {
            "a/fake": _seat([sys.executable, "{prompt}"], vendor="a"),
            "b/fake": _seat([sys.executable, "{prompt}"], vendor="b"),
        },
        ["a/fake", "b/fake"],
    )
    report = onboarding.status(str(project))
    reasons = report["reasons"]
    assert isinstance(reasons, list)
    assert any("IDENTICAL selected command" in reason for reason in reasons)


def test_non_ascii_project_name(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    _, _ = isolated
    project = tmp_path / "projekt-ékezet"
    project.mkdir()
    report = onboarding.status(str(project))
    assert report["attention"] == "offer_setup"
    for line in onboarding.status_lines(report):
        line.encode("utf-8")  # renders; ASCII rule applies to the words, not the path


def test_bundled_engine_wins_over_a_path_debate(tmp_path: Path) -> None:
    """scripts/debate-plugin runs the BUNDLED engine even when a decoy
    `debate` package sits first on the caller's PYTHONPATH."""
    decoy = tmp_path / "decoy"
    (decoy / "debate").mkdir(parents=True)
    (decoy / "debate" / "__init__.py").write_text(
        "raise SystemExit('decoy debate package must never load')", encoding="utf-8"
    )
    launcher = REPO_ROOT / "scripts" / (
        "debate-plugin.cmd" if os.name == "nt" else "debate-plugin"
    )
    proc = subprocess.run(
        [str(launcher), "onboarding", "status", "--project", str(tmp_path), "--json"],
        capture_output=True, text=True, timeout=30,
        env={
            **_baseline_environment(),
            "PATH": os.pathsep.join([str(Path(sys.executable).parent), _hermetic_path()]),
            "PYTHONPATH": str(decoy),
            "DEBATE_SEATS_REGISTRY": str(tmp_path / "reg.json"),
        },
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = json.loads(proc.stdout)
    from debate import __version__

    assert report["product_version"] == __version__
    assert report["attention"] == "offer_setup"
