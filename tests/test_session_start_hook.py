"""Hook contract tests: hooks/session-start (plan Slice 1A).

The hook is exercised exactly as a host runs it: a subprocess with a JSON
event on stdin and the plugin root in the environment. Every case asserts
exit 0 (a hook must never break a host session), valid JSON on stdout, and
-- for the whole battery -- zero filesystem writes and zero seat
invocations (a sentinel seat command must remain unexecuted).
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
CODEX_ENV = {"PLUGIN_ROOT": str(REPO_ROOT)}


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
                        "commands": [[sys.executable, "{prompt}"]],
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


def _write_attention_state(project: Path, registry: Path, attention: str) -> None:
    if attention == "offer_setup":
        return
    _write_ready_state(project, registry)
    if attention == "offer_refresh":
        raw = json.loads(registry.read_text(encoding="utf-8"))
        raw["tool_version"] = "0.0.1"
        registry.write_text(json.dumps(raw), encoding="utf-8")
        return
    if attention == "repair_required":
        (project / "debate-profile.json").write_text("{broken", encoding="utf-8")
        return
    raise AssertionError(f"unexpected attention fixture: {attention}")


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
    assert "fresh host process" in context
    assert "continue" not in payload
    assert "stopReason" not in payload


@pytest.mark.parametrize("attention", ["offer_setup", "offer_refresh", "repair_required"])
def test_codex_attention_stops_first_turn_before_model(
    tmp_path: Path, attention: str
) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_attention_state(project, registry, attention)
    before = _snapshot(tmp_path)

    payload, _, _ = _run(project, registry, extra_env=CODEX_ENV)

    assert _snapshot(tmp_path) == before
    assert payload["continue"] is False
    assert payload["stopReason"] == (
        "Debate setup attention stopped this first Codex prompt before model inference."
    )
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "Codex stopped this first prompt before it reached the model" in message
    assert "repeat it to continue normally" in message
    assert 'reply "set up Debate"' in message
    context = payload["hookSpecificOutput"]
    assert isinstance(context, dict)
    assert f'"attention": "{attention}"' in str(context["additionalContext"])


@pytest.mark.parametrize("attention", ["offer_setup", "offer_refresh", "repair_required"])
def test_claude_attention_warns_without_stopping(
    tmp_path: Path, attention: str
) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_attention_state(project, registry, attention)

    payload, _, _ = _run(project, registry)

    assert "systemMessage" in payload
    assert "continue" not in payload
    assert "stopReason" not in payload


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
    assert "every new channel start" in context
    assert "continue" not in payload
    assert "stopReason" not in payload


def test_codex_healthy_project_is_quiet_and_not_stopped(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_ready_state(project, registry)

    payload, _, _ = _run(project, registry, extra_env=CODEX_ENV)

    assert "systemMessage" not in payload
    assert "continue" not in payload
    assert "stopReason" not in payload


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
    assert "continue" not in payload
    assert "stopReason" not in payload


def test_codex_malformed_input_warns_but_fails_open(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    payload, stderr, _ = _run(
        project,
        tmp_path / "reg.json",
        stdin="{not json",
        extra_env=CODEX_ENV,
    )
    assert "malformed" in str(payload.get("systemMessage"))
    assert "malformed" in stderr
    assert "continue" not in payload
    assert "stopReason" not in payload


def test_missing_engine_is_a_visible_error(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    empty_root = tmp_path / "empty-plugin"
    empty_root.mkdir()
    payload, _, _ = _run(project, tmp_path / "reg.json", plugin_root=empty_root)
    message = payload.get("systemMessage")
    assert isinstance(message, str)
    assert "engine is missing" in message or "reinstall" in message
    assert "continue" not in payload
    assert "stopReason" not in payload


def test_codex_missing_engine_warns_but_fails_open(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    empty_root = tmp_path / "empty-plugin"
    empty_root.mkdir()
    payload, _, _ = _run(
        project,
        tmp_path / "reg.json",
        plugin_root=empty_root,
        extra_env=CODEX_ENV,
    )
    assert "engine is missing" in str(payload.get("systemMessage")) or "reinstall" in str(
        payload.get("systemMessage")
    )
    assert "continue" not in payload
    assert "stopReason" not in payload


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
    assert "continue" not in payload
    assert "stopReason" not in payload


def test_codex_quiet_attention_is_context_only_and_not_stopped(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    payload, _, _ = _run(
        project,
        tmp_path / "reg.json",
        extra_env={**CODEX_ENV, "DEBATE_ONBOARDING_QUIET": "1"},
    )
    assert "systemMessage" not in payload
    assert "continue" not in payload
    assert "stopReason" not in payload
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    assert "offer_setup" in str(hso["additionalContext"])


def test_codex_quiet_repair_required_is_context_only_and_not_stopped(
    tmp_path: Path,
) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}),
        encoding="utf-8",
    )

    payload, _, _ = _run(
        project,
        registry,
        extra_env={**CODEX_ENV, "DEBATE_ONBOARDING_QUIET": "1"},
    )

    assert "systemMessage" not in payload
    assert "continue" not in payload
    assert "stopReason" not in payload
    hso = payload["hookSpecificOutput"]
    assert isinstance(hso, dict)
    assert "repair_required" in str(hso["additionalContext"])


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
    _, _, elapsed_codex = _run(
        tmp_path / "proj",
        tmp_path / "codex-reg.json",
        extra_env=CODEX_ENV,
    )
    assert _snapshot(tmp_path) == before
    assert elapsed_ready < 8 and elapsed_setup < 8 and elapsed_codex < 8


def test_hook_never_launches_an_approved_seat(tmp_path: Path) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    registry = tmp_path / "reg" / "seats.json"
    _write_ready_state(project, registry)
    invoked = tmp_path / "seat-was-invoked"
    raw = json.loads(registry.read_text(encoding="utf-8"))
    raw["seats"]["probe/fake"]["commands"] = [
        [sys.executable, "-c", f"from pathlib import Path; Path({str(invoked)!r}).touch()"]
    ]
    registry.write_text(json.dumps(raw), encoding="utf-8")

    _run(project, registry, extra_env=CODEX_ENV)

    assert not invoked.exists()


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
    # Field finding F24: the Microsoft Store "python3" shim prints an ad and
    # EXITS 0, so python3 must come LAST -- any chain it appears earlier in
    # is swallowed on Windows. py.exe and python.exe report honest failures,
    # so the chain resolves left to right on every platform.
    assert hook["command"].startswith("py -3 ")
    assert " || python " in hook["command"]
    assert hook["command"].rstrip().count("|| python3 ") == 1
    assert hook["command"].index("py -3") < hook["command"].index("|| python ") < hook["command"].index("|| python3 ")
    assert hook["timeout"] == 10
    assert hook["async"] is False


def test_manifests_are_field_identical_documents() -> None:
    """The 2026-06-26 Codex parser incident plus the branch-gate round-1
    finding: the two manifests must be DEEP-EQUAL documents, not merely
    equal at the hook-entry level."""
    claude = json.loads((REPO_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    codex = json.loads((REPO_ROOT / "hooks" / "hooks-codex.json").read_text(encoding="utf-8"))
    assert claude == codex
