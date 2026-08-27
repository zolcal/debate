"""Ox Alpha catalog, credential transport, and revisioned policy consent."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, cast
from unittest.mock import patch

import pytest

from debate import bridge, channel, controller, onboarding, opening, seats
from debate.__main__ import main

NOW = "2026-08-23T12:00:00+00:00"
POLICY_REVISION = "openrouter-stealth-eula-2026-08-23"


def _which(mapping: dict[str, str]) -> Callable[[str], str | None]:
    return mapping.get


def _launcher(path: Path, name: str = "claude-ox") -> Path:
    launcher = path / name
    launcher.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    # Windows which() resolves via PATHEXT only: a .cmd twin makes the same
    # binary name discoverable there (field finding F25).
    launcher.with_suffix(".cmd").write_text("@exit /b 0\r\n", encoding="utf-8")
    launcher.chmod(0o755)
    return launcher


def _ox_seat(launcher: Path) -> seats.Seat:
    registry, _ = seats.discover(
        seats.Registry(), which=_which({"claude-ox": str(launcher)}), now=NOW
    )
    return registry.seats["stealth/ox-alpha"]


def _other_seat() -> seats.Seat:
    return seats.Seat(
        seat_id="other/frontier",
        vendor="other",
        submodel="frontier",
        effort=None,
        commands=[["/bin/sh", "{input_path}", "{result_path}"]],
        source="manual",
        present=True,
        smoke=None,
        cost_mode="local",
        capability_class="frontier",
        verification_basis="declared",
        result_schema_version=2,
    )


def _git_project(path: Path) -> None:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)


def _open_spec(project: Path) -> opening.BrokeredOpenSpec:
    return opening.BrokeredOpenSpec(
        root=project,
        label="ox-policy-probe",
        pair=("stealth/ox-alpha", "other/frontier"),
        source_ref="a" * 40,
        author_vendor="codex",
        allow_mismatched_pair=False,
        goal="Verify the bounded public fixture.",
        review_domain="The pinned public fixture only.",
        stop_rule="Stop after the bounded check and verdict.",
    )


def test_catalog_discovers_one_honest_frontier_ox_seat(tmp_path: Path) -> None:
    launcher = _launcher(tmp_path)
    seat = _ox_seat(launcher)

    assert seat.commands == [[str(launcher), "-p", "{prompt}"]]
    assert seat.cost_mode == "unknown"
    assert seat.capability_class == "frontier"
    assert seat.config_home == "CLAUDE_CONFIG_DIR=.claude-ox"
    assert seat.credential_env == ["OPENROUTER_API_KEY"]
    assert seat.data_policy_revision == POLICY_REVISION
    assert seat.data_policy_notice is not None
    assert "anonymous-provider" in seat.data_policy_notice
    assert seat.verification_basis == "catalogued"
    assert seat.isolation_argv and seat.no_persistence_argv


def test_credential_name_is_bounded_and_value_never_serialized(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launcher = _launcher(tmp_path)
    seat = _ox_seat(launcher)
    secret = "or-secret-fixture-value-123456789"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)

    adapter = opening._brokered_adapter(
        seat, tool_version="test", author_vendor="codex", real_home=tmp_path
    )
    encoded = json.dumps(adapter, sort_keys=True)
    environment_allowlist = adapter["environment_allowlist"]
    assert isinstance(environment_allowlist, list)
    assert environment_allowlist[-1] == "OPENROUTER_API_KEY"
    assert secret not in encoded
    assert hashlib.sha256(secret.encode()).hexdigest() not in encoded
    assert "visible to the seat process and tools" in str(adapter["authentication_mode"])

    seats.validate_credential_env(["OPENROUTER_API_KEY"])
    with pytest.raises(channel.ChannelError, match="code-known"):
        seats.validate_credential_env(["AWS_SECRET_ACCESS_KEY"])
    with pytest.raises(channel.ChannelError, match="duplicate"):
        seats.validate_credential_env(["OPENROUTER_API_KEY", "OPENROUTER_API_KEY"])

    manual = seats.Registry()
    seats.add_seat(
        manual,
        "stealth/manual-ox",
        "/bin/sh {prompt}",
        which=_which({"/bin/sh": "/bin/sh"}),
        credential_env=["OPENROUTER_API_KEY"],
    )
    assert manual.seats["stealth/manual-ox"].credential_env == ["OPENROUTER_API_KEY"]
    with pytest.raises(channel.ChannelError, match="code-known"):
        seats.add_seat(
            manual,
            "stealth/bad",
            "/bin/sh {prompt}",
            which=_which({"/bin/sh": "/bin/sh"}),
            credential_env=["LD_PRELOAD"],
        )


def test_generic_key_reaches_only_the_nested_ox_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launcher = _launcher(tmp_path)
    seat = _ox_seat(launcher)
    secret = "or-nested-seat-fixture-123456789"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)
    monkeypatch.setenv("UNRELATED_SECRET", "must-not-cross")
    mapping = opening._brokered_adapter(
        seat, tool_version="test", author_vendor="codex", real_home=tmp_path
    )
    profile = controller.AdapterProfile.from_mapping("stealth", mapping)
    config = cast(
        controller.BrokerConfig,
        SimpleNamespace(repository_root=tmp_path),
    )
    adapter_environment = controller._adapter_environment(
        config, profile, tmp_path / "runtime"
    )
    assert adapter_environment["OPENROUTER_API_KEY"] == secret
    assert "UNRELATED_SECRET" not in adapter_environment

    command = mapping["command"]
    assert isinstance(command, list)
    spec = bridge.parse_bridge_command(command)
    assert spec is not None
    assert spec.credential_env == ("OPENROUTER_API_KEY",)
    with patch.dict("os.environ", adapter_environment, clear=True):
        nested_environment = bridge.seat_environment(spec)
    assert nested_environment["OPENROUTER_API_KEY"] == secret
    assert "UNRELATED_SECRET" not in nested_environment

    manifest_text = json.dumps(profile.sanitized_manifest(), sort_keys=True)
    assert "OPENROUTER_API_KEY" in manifest_text
    assert secret not in manifest_text
    assert hashlib.sha256(secret.encode()).hexdigest() not in manifest_text

    digest = hashlib.sha256(secret.encode()).hexdigest()
    completed = subprocess.CompletedProcess(
        args=[str(launcher)],
        returncode=3,
        stdout=f"seat leaked {secret}",
        stderr=f"seat leaked digest {digest}",
    )
    redacted = bridge.redact_seat_output(
        completed,
        credential_env=("OPENROUTER_API_KEY",),
        environment=adapter_environment,
    )
    retained = redacted.stdout + redacted.stderr
    assert secret not in retained
    assert digest not in retained
    assert "[redacted credential OPENROUTER_API_KEY]" in retained
    assert "[redacted digest OPENROUTER_API_KEY]" in retained
    controller_retained = controller._redact_credential_material(
        completed.stdout + completed.stderr, profile, adapter_environment
    )
    assert secret not in controller_retained
    assert digest not in controller_retained
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(controller.AdapterError, match="needs credential environment"):
            controller._adapter_environment(config, profile, tmp_path / "missing-key-runtime")


def test_legacy_payload_stays_free_of_new_optional_fields() -> None:
    registry = seats.Registry()
    registry.seats["legacy/seat"] = _other_seat()
    registry.seats["legacy/seat"].seat_id = "legacy/seat"
    payload = seats.registry_payload(registry)
    raw = payload["seats"]
    assert isinstance(raw, dict)
    row = raw["legacy/seat"]
    assert isinstance(row, dict)
    assert "credential_env" not in row
    assert "data_policy_revision" not in row
    assert "data_policy_notice" not in row


def test_onboarding_requires_and_records_exact_policy_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _launcher(bin_dir)
    registry_path = tmp_path / "config" / "seats.json"
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    monkeypatch.setenv("PATH", str(bin_dir))

    report = onboarding.inspect(str(project), now=NOW)
    candidates = report["candidates"]
    assert isinstance(candidates, list) and len(candidates) == 1
    row = candidates[0]
    assert isinstance(row, dict)
    assert row["seat_id"] == "stealth/ox-alpha"
    assert row["credential_env"] == ["OPENROUTER_API_KEY"]
    assert row["data_policy_revision"] == POLICY_REVISION
    assert "generic OpenRouter key" in str(row["data_policy_notice"])
    assert "$0/M" in str(row["price_observation"])
    assert "time-sensitive" in str(row["price_observation"])

    assert main(["onboarding", "inspect", "--project", str(project)]) == 0
    rendered = capsys.readouterr().out
    assert "$0/M" in rendered
    assert "time-sensitive" in rendered

    revision = str(report["candidate_revision"])
    with pytest.raises(channel.ChannelError, match="explicit acceptance"):
        onboarding.approve(
            str(project),
            allow=["stealth/ox-alpha"],
            candidate_revision=revision,
            confirmed=True,
            now=NOW,
        )
    with pytest.raises(channel.ChannelError, match="explicit acceptance"):
        onboarding.approve(
            str(project),
            allow=["stealth/ox-alpha"],
            candidate_revision=revision,
            confirmed=True,
            now=NOW,
            accepted_policies={"stealth/ox-alpha": "old-revision"},
        )

    status = onboarding.approve(
        str(project),
        allow=["stealth/ox-alpha"],
        candidate_revision=revision,
        confirmed=True,
        now=NOW,
        accepted_policies={"stealth/ox-alpha": POLICY_REVISION},
    )
    assert status["attention"] == "ready"
    profile = json.loads((project / seats.PROFILE_NAME).read_text(encoding="utf-8"))
    assert profile == {
        "profile_version": 1,
        "allowlist": ["stealth/ox-alpha"],
        "data_policy_acceptances": {"stealth/ox-alpha": POLICY_REVISION},
    }

    saved_registry = seats.load_registry()
    saved_registry.seats["stealth/ox-alpha"].data_policy_revision = (
        "openrouter-stealth-eula-2026-08-24"
    )
    seats.save_registry(saved_registry)
    stale = onboarding.status(str(project))
    assert stale["attention"] == "offer_refresh"
    approved = stale["approved_seats"]
    assert isinstance(approved, list)
    approved_row = approved[0]
    assert isinstance(approved_row, dict)
    assert approved_row["data_policy_accepted"] is False
    reasons = stale["reasons"]
    assert isinstance(reasons, list)
    assert any("needs acceptance" in str(reason) for reason in reasons)


def test_changed_policy_and_missing_key_refuse_before_channel_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launcher = _launcher(tmp_path)
    ox = _ox_seat(launcher)
    other = _other_seat()
    registry = seats.Registry(seats={ox.seat_id: ox, other.seat_id: other})
    project = tmp_path / "project"
    _git_project(project)
    profile_path = project / seats.PROFILE_NAME
    profile_path.write_text(
        json.dumps(
            {
                "profile_version": 1,
                "allowlist": [ox.seat_id, other.seat_id],
                "data_policy_acceptances": {ox.seat_id: POLICY_REVISION},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    initial_paths = sorted(str(path.relative_to(project)) for path in project.rglob("*"))

    ox.data_policy_revision = "openrouter-stealth-eula-2026-08-24"
    with pytest.raises(channel.ChannelError, match="needs project acceptance"):
        opening.open_debate_brokered(
            _open_spec(project),
            registry,
            load_config_fn=lambda *_args, **_kwargs: pytest.fail("config loader called"),
            now=NOW,
            tool_version="test",
            real_home=tmp_path,
        )
    assert sorted(str(path.relative_to(project)) for path in project.rglob("*")) == initial_paths

    ox.data_policy_revision = POLICY_REVISION
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(channel.ChannelError, match="needs credential environment OPENROUTER_API_KEY"):
        opening.open_debate_brokered(
            _open_spec(project),
            registry,
            load_config_fn=lambda *_args, **_kwargs: pytest.fail("config loader called"),
            now=NOW,
            tool_version="test",
            real_home=tmp_path,
        )
    assert sorted(str(path.relative_to(project)) for path in project.rglob("*")) == initial_paths


def test_missing_credential_refuses_smoke_before_confirmation_or_scratch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launcher = _launcher(tmp_path)
    ox = _ox_seat(launcher)
    registry = seats.Registry(seats={ox.seat_id: ox})
    scratch = tmp_path / "smoke-scratch"
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    def forbidden_ask(_question: str) -> str:
        pytest.fail("missing credential reached the spend confirmation")

    monkeypatch.setattr(
        "debate.setup.smoke",
        lambda *_args, **_kwargs: pytest.fail("missing credential invoked setup.smoke"),
    )

    with pytest.raises(channel.ChannelError, match="needs credential environment"):
        seats.smoke_seat(
            registry,
            ox.seat_id,
            scratch_base=scratch,
            now=NOW,
            ask=forbidden_ask,
        )

    assert not scratch.exists()
    assert ox.smoke is None


def test_cli_policy_acceptance_parser_is_exact() -> None:
    assert onboarding.parse_policy_acceptances(
        [f"stealth/ox-alpha={POLICY_REVISION}"]
    ) == {"stealth/ox-alpha": POLICY_REVISION}
    with pytest.raises(channel.ChannelError, match="SEAT=REVISION"):
        onboarding.parse_policy_acceptances(["stealth/ox-alpha"])
    with pytest.raises(channel.ChannelError, match="duplicate"):
        onboarding.parse_policy_acceptances(
            [f"stealth/ox-alpha={POLICY_REVISION}", "stealth/ox-alpha=other"]
        )
