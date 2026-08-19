"""Hook contract tests: hooks/session-start (plan Slice 1A).

The hook is exercised exactly as a host runs it: a subprocess with a JSON
event on stdin and the plugin root in the environment. Every case asserts
exit 0 (a hook must never break a host session), valid JSON on stdout, and
-- for the whole battery -- zero filesystem writes and zero seat
invocations (no seat command exists in these fixtures at all).
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from debate import __version__

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK = REPO_ROOT / "hooks" / "session-start"


def _run(
    project: Path,
    registry: Path,
    *,
    stdin: str | None = None,
    plugin_root: Path | None = None,
    extra_env: dict[str, str] | None = None,
) -> tuple[dict[str, object], str, float]:
    event = stdin if stdin is not None else json.dumps(
        {"session_id": "t", "cwd": str(project), "hook_event_name": "SessionStart"}
    )
    env = {
        "PATH": "/usr/bin:/bin",
        "CLAUDE_PLUGIN_ROOT": str(plugin_root if plugin_root is not None else REPO_ROOT),
        "DEBATE_SEATS_REGISTRY": str(registry),
    }
    if extra_env:
        env.update(extra_env)
    started = time.monotonic()
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=event,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
        check=False,
    )
    elapsed = time.monotonic() - started
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert isinstance(payload, dict)
    return payload, proc.stderr, elapsed


def _snapshot(root: Path) -> list[tuple[str, float, int]]:
    return [
        (str(p), p.stat().st_mtime, p.stat().st_size if p.is_file() else -1)
        for p in sorted(root.rglob("*"))
    ]


def _write_ready_state(project: Path, registry: Path) -> None:
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        json.dumps(
            {
                "registry_version": 1,
                "tool_version": __version__,
                "discovered_at": "2026-08-19T00:00:00+00:00",
                "seats": {
                    "probe/fake": {
                        "vendor": "probe",
                        "submodel": "fake",
                        "effort": None,
                        "commands": [["/bin/sh", "{prompt}"]],
                        "source": "manual",
                        "present": True,
                        "smoke": None,
                    }
                },
                "last_pair": {},
            }
        ),
        encoding="utf-8",
    )
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}),
        encoding="utf-8",
    )


def test_fresh_project_gets_the_setup_notice(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    payload, _, _ = _run(project, tmp_path / "reg" / "seats.json")
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "No agents are approved" in message
    assert "no model calls" in message
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    assert hso["hookEventName"] == "SessionStart"
    context = hso["additionalContext"]
    assert isinstance(context, str)
    assert "offer_setup" in context
    assert "debate-plugin" in context  # launcher path is injected


def test_healthy_project_is_quiet(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_ready_state(project, registry)
    payload, _, _ = _run(project, registry)
    assert "systemMessage" not in payload
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    context = hso["additionalContext"]
    assert isinstance(context, str)
    assert "ready" in context
    assert "debate-plugin" in context


def test_stale_registry_gets_a_refresh_notice(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_ready_state(project, registry)
    raw = json.loads(registry.read_text(encoding="utf-8"))
    raw["tool_version"] = "0.0.1"
    registry.write_text(json.dumps(raw), encoding="utf-8")
    payload, _, _ = _run(project, registry)
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "refresh" in message


def test_broken_profile_gets_a_repair_notice(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_ready_state(project, registry)
    (project / "debate-profile.json").write_text("{broken", encoding="utf-8")
    payload, _, _ = _run(project, registry)
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "repair" in message


def test_malformed_input_is_a_visible_error_not_a_crash(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    payload, stderr, _ = _run(project, tmp_path / "reg.json", stdin="{not json")
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "malformed" in message
    assert "malformed" in stderr


def test_missing_engine_is_a_visible_error(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    empty_root = tmp_path / "empty-plugin"
    empty_root.mkdir()
    payload, _, _ = _run(project, tmp_path / "reg.json", plugin_root=empty_root)
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "engine is missing" in message or "reinstall" in message


def test_project_path_with_spaces(tmp_path: Path) -> None:
    project = tmp_path / "a project with spaces"
    project.mkdir()
    payload, _, _ = _run(project, tmp_path / "reg.json")
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    context = hso["additionalContext"]
    assert isinstance(context, str)
    assert "offer_setup" in context


def test_non_interactive_suppresses_the_banner(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    payload, _, _ = _run(
        project, tmp_path / "reg.json", extra_env={"DEBATE_ONBOARDING_QUIET": "1"}
    )
    assert "systemMessage" not in payload
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    assert "offer_setup" in str(hso["additionalContext"])


def test_claude_headless_entrypoint_suppresses_the_banner(tmp_path: Path) -> None:
    """CLAUDE_CODE_ENTRYPOINT=sdk-cli is the ATTESTED headless signal
    (HOOK-CONTRACT.md spike, 2026-08-19); interactive sessions carry "cli"
    and keep the banner."""
    project = tmp_path / "proj"
    project.mkdir()
    payload, _, _ = _run(
        project, tmp_path / "reg.json", extra_env={"CLAUDE_CODE_ENTRYPOINT": "sdk-cli"}
    )
    assert "systemMessage" not in payload
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    assert "offer_setup" in str(hso["additionalContext"])
    interactive, _, _ = _run(
        project, tmp_path / "reg.json", extra_env={"CLAUDE_CODE_ENTRYPOINT": "cli"}
    )
    assert "systemMessage" in interactive


def test_hook_is_fast_and_writes_nothing(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_ready_state(project, registry)
    before = _snapshot(tmp_path)
    _, _, elapsed_ready = _run(project, registry)
    _, _, elapsed_setup = _run(tmp_path / "proj", tmp_path / "other-reg.json")
    assert _snapshot(tmp_path) == before
    assert elapsed_ready < 8 and elapsed_setup < 8  # manifest timeout is 10s


def test_notices_are_ascii(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    payload, _, _ = _run(project, tmp_path / "reg.json")
    for value in (payload.get("systemMessage", ""), json.dumps(payload)):
        assert isinstance(value, str)
        assert all(ord(c) < 128 for c in value), value


@pytest.mark.parametrize("manifest", ["hooks.json", "hooks-codex.json"])
def test_manifests_parse_and_carry_the_command(manifest: str) -> None:
    raw = json.loads((REPO_ROOT / "hooks" / manifest).read_text(encoding="utf-8"))
    entries = raw["hooks"]["SessionStart"]
    assert len(entries) == 1
    hook = entries[0]["hooks"][0]
    assert hook["type"] == "command"
    assert "${CLAUDE_PLUGIN_ROOT}/hooks/session-start" in hook["command"]
    assert hook["command"].startswith("python3 ")
    assert hook["timeout"] == 10
    assert hook["async"] is False


def test_manifests_are_field_identical_documents() -> None:
    """The 2026-06-26 Codex parser incident plus the branch-gate round-1
    finding: the two manifests must be DEEP-EQUAL documents, not merely
    equal at the hook-entry level."""
    claude = json.loads((REPO_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    codex = json.loads((REPO_ROOT / "hooks" / "hooks-codex.json").read_text(encoding="utf-8"))
    assert claude == codex
