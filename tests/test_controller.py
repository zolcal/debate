from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from debate import channel
from debate.controller import (
    AdapterError,
    AdapterProfile,
    AdapterResult,
    BrokerConfig,
    BrokerController,
    DriveOutcome,
    TimingPolicy,
    _baseline_environment,
    _parse_result,
    create_source_export,
    doctor_lines,
    materialize_docket,
)
from debate.__main__ import _NEEDS_ATTENTION, main
from debate.watcher import WatcherConfig, read_status, run_once


FAKE_ADAPTER = r"""
import json
import os
from pathlib import Path
import sys
import time

started = time.time()
input_path = Path(sys.argv[1])
result_path = Path(sys.argv[2])
payload = json.loads(input_path.read_text(encoding="utf-8"))
mode = os.environ.get("FAKE_MODE", "good")
if mode == "timeout":
    time.sleep(2)
if mode == "orphan":
    import subprocess
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    Path(os.environ["FAKE_PIDS_PATH"]).write_text(
        json.dumps({"adapter": os.getpid(), "child": child.pid}), encoding="utf-8"
    )
    time.sleep(120)
if mode == "slow":
    time.sleep(float(os.environ.get("FAKE_SLEEP", "1.5")))
if mode == "malformed":
    result_path.write_text("{ broken", encoding="utf-8")
    raise SystemExit(0)
body = "fresh fake review"
if mode == "leak":
    body += " " + Path(os.environ["LEAK_PATH"]).read_text(encoding="utf-8")
result = {
    "schema_version": 1,
    "entry_type": "verdict",
    "body": body,
    "runtime_model": os.environ.get("RUNTIME_MODEL", "fake-model-1"),
    "appendix_markdown": "## Review - fake adapter\n\nStructured appendix.",
    "decision": os.environ.get(
        "FAKE_SEALED_DECISION" if payload["phase"] == "sealed" else "FAKE_DELIBERATION_DECISION",
        os.environ.get("FAKE_DECISION", "PASS"),
    ),
}
if mode == "wrong-sender":
    result["sender"] = "intruder"
if mode == "missing-decision":
    result.pop("decision")
if os.environ.get("FAKE_EXTRA_PROVENANCE") == "1":
    result["runtime_model_basis"] = os.environ.get("FAKE_RUNTIME_MODEL_BASIS", "declared")
    result["configuration_home"] = os.environ.get("FAKE_CONFIGURATION_HOME", "operator (CLAUDE_CONFIG_DIR)")
    result["isolation_flags"] = os.environ.get("FAKE_ISOLATION_FLAGS", "catalogued")
result_path.write_text(json.dumps(result), encoding="utf-8")
log_path = os.environ.get("FAKE_LOG_PATH")
if log_path:
    entry = {"party": payload["seat"]["party"], "start": started, "end": time.time()}
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
"""


def _run(argv: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=60, check=False)


def make_repository(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "project"
    (repo / ".claude").mkdir(parents=True)
    (repo / "tests").mkdir()
    (repo / ".claude" / "settings.json").write_text(
        json.dumps({"permissions": {"allow": ["Bash(debate *)"]}}), encoding="utf-8"
    )
    (repo / "fake_adapter.py").write_text(FAKE_ADAPTER, encoding="utf-8")
    (repo / "project_module.py").write_text("VALUE = 42\n", encoding="utf-8")
    (repo / "tests" / "test_smoke.py").write_text(
        "from project_module import VALUE\n\ndef test_value():\n    assert VALUE == 42\n",
        encoding="utf-8",
    )
    (repo / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n', encoding="utf-8"
    )
    (repo / ".gitignore").write_text("var/\ncollab/\nwatcher.json\ndocs/plans/\n", encoding="utf-8")
    assert _run(["git", "init", "-b", "main"], repo).returncode == 0
    assert _run(["git", "config", "user.email", "test@example.invalid"], repo).returncode == 0
    assert _run(["git", "config", "user.name", "Test"], repo).returncode == 0
    assert _run(["git", "add", "."], repo).returncode == 0
    assert _run(["git", "commit", "-m", "fixture"], repo).returncode == 0
    sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    (repo / "docs" / "plans").mkdir(parents=True)
    (repo / "docs" / "plans" / "superseded.md").write_text("# Untracked plan revision\n", encoding="utf-8")
    (repo / "watcher.json").write_text('{"commands": {"old": ["agent"]}}\n', encoding="utf-8")
    return repo, sha


def make_profile(
    party: str,
    relationship: str,
    *,
    mode: str = "good",
    additions: dict[str, str] | None = None,
    timeout: int = 30,
    sealed_decision: str = "PASS",
    deliberation_decision: str = "PASS",
) -> AdapterProfile:
    environment = {
        "FAKE_MODE": mode,
        "RUNTIME_MODEL": f"{party}-runtime-1",
        "FAKE_SEALED_DECISION": sealed_decision,
        "FAKE_DELIBERATION_DECISION": deliberation_decision,
        **(additions or {}),
    }
    return AdapterProfile(
        party=party,
        command=(sys.executable, "{export_root}/fake_adapter.py", "{input_path}", "{result_path}"),
        provider=f"provider-{party}",
        requested_model=f"{party}-requested",
        expected_runtime_model=f"{party}-runtime-1",
        author_relationship=relationship,
        reasoning_effort="high",
        cli_version="fixture-1",
        cost_mode="local",
        authentication_mode="local-process",
        permission_policy="read-only-source; result-file-only",
        settings_sources=(),
        environment_allowlist=("PATH",),
        environment=environment,
        timeout_seconds=timeout,
        retry_limit=1,
        session_persistence=False,
        isolation_mode="advisory",
    )


def make_broker(
    repo: Path,
    sha: str,
    *,
    alice_relationship: str = "author-affiliated",
    bob_relationship: str = "author-independent",
    alice_mode: str = "good",
    bob_mode: str = "good",
    alice_additions: dict[str, str] | None = None,
    bob_additions: dict[str, str] | None = None,
    alice_timeout: int = 30,
    bob_timeout: int = 30,
    alice_sealed_decision: str = "PASS",
    bob_sealed_decision: str = "PASS",
    alice_deliberation_decision: str = "PASS",
    bob_deliberation_decision: str = "PASS",
    canaries: dict[str, str] | None = None,
    config_sha256: str = "a" * 64,
    thread_cap: int = 12,
    whole_case_timeout_seconds: int = 900,
    sealed_concurrency: str = "concurrent",
) -> BrokerConfig:
    profiles = {
        "alice": make_profile(
            "alice",
            alice_relationship,
            mode=alice_mode,
            additions=alice_additions,
            timeout=alice_timeout,
            sealed_decision=alice_sealed_decision,
            deliberation_decision=alice_deliberation_decision,
        ),
        "bob": make_profile(
            "bob",
            bob_relationship,
            mode=bob_mode,
            additions=bob_additions,
            timeout=bob_timeout,
            sealed_decision=bob_sealed_decision,
            deliberation_decision=bob_deliberation_decision,
        ),
    }
    timing = TimingPolicy(
        thread_cap=thread_cap,
        scheduler_interval_seconds=60,
        retry_seconds=120,
        whole_case_timeout_seconds=whole_case_timeout_seconds,
        profiles=(profiles["alice"], profiles["bob"]),
    )
    return BrokerConfig(
        repository_root=repo,
        runtime_root=repo / "var" / "debate" / "case-fixture",
        source_ref=sha,
        profiles=profiles,
        timing=timing,
        config_sha256=config_sha256,
        docket_files=("docs/plans/superseded.md", "watcher.json"),
        contamination_canaries=canaries or {},
        sealed_concurrency=sealed_concurrency,
    )


def make_channel(repo: Path, *, thread_cap: int = 12) -> tuple[Path, str]:
    root = repo / "collab"
    name = "fixture-11111"
    channel.init_channel(
        root,
        ("alice", "bob"),
        "owner",
        thread_cap=thread_cap,
        name=name,
        managed_version=channel.BROKERED_MANAGED_VERSION,
    )
    return root, name


def profile_payload(party: str, relationship: str) -> dict[str, object]:
    return {
        "command": [sys.executable, "{export_root}/fake_adapter.py", "{input_path}", "{result_path}"],
        "provider": f"provider-{party}",
        "requested_model": f"{party}-requested",
        "expected_runtime_model": f"{party}-runtime-1",
        "author_relationship": relationship,
        "reasoning_effort": "high",
        "cli_version": "fixture-1",
        "cost_mode": "local",
        "authentication_mode": "local-process",
        "permission_policy": "read-only-source; result-file-only",
        "settings_sources": [],
        "environment_allowlist": ["PATH"],
        "environment": {"RUNTIME_MODEL": f"{party}-runtime-1"},
        "timeout_seconds": 30,
        "retry_limit": 1,
        "session_persistence": False,
        "isolation_mode": "advisory",
    }


def open_brokered_thread(root: Path, name: str, broker: BrokerConfig) -> None:
    BrokerController(broker).open_case(
        channel_root=root,
        channel_name=name,
        thread="review-one",
        first_party="bob",
        body="Inspect the pinned source and return a structured review.",
    )


def test_brokered_version_refuses_direct_party_identity_but_allows_supervisor(tmp_path: Path) -> None:
    repo, _ = make_repository(tmp_path)
    root, name = make_channel(repo)

    with pytest.raises(channel.ChannelError, match="controller-brokered"):
        channel.post(root, "alice", "question", "one", "direct", name=name)

    assert channel.post(root, "owner", "info", "one", "supervisor note", name=name) == "MSG-1"


def test_adapter_doctor_loads_generic_profiles_and_prints_cost_before_any_invocation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    runtime = repo / "var" / "debate" / "doctor-fixture"
    config_path = repo / "broker-config.json"
    config_path.write_text(
        json.dumps(
            {
                "state_path": str(runtime / "watcher-state.json"),
                "runtime_root": str(runtime),
                "source_ref": sha,
                "whole_case_timeout_seconds": 900,
                "scheduler_interval_seconds": 60,
                "retry_seconds": 120,
                "adapters": {
                    "alice": profile_payload("alice", "author-affiliated"),
                    "bob": profile_payload("bob", "author-independent"),
                },
                "docket_files": ["docs/plans/superseded.md", "watcher.json"],
            }
        ),
        encoding="utf-8",
    )

    code = main(
        [
            "adapter-doctor",
            "--root",
            str(root),
            "--channel",
            name,
            "--config",
            str(config_path),
        ]
    )

    output = capsys.readouterr().out
    assert code == 0
    assert "topology: minimum-two-agent" in output
    assert "cost_mode=local" in output
    assert "no adapter invoked and no charge incurred" in output
    assert not runtime.exists(), "the read-only doctor must not create case/runtime state"


def test_broker_open_snapshots_before_supervisor_docket_and_assigns_first_seat(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    runtime = repo / "var" / "debate" / "open-fixture"
    config_path = repo / "broker-config.json"
    config_path.write_text(
        json.dumps(
            {
                "state_path": str(runtime / "watcher-state.json"),
                "runtime_root": str(runtime),
                "source_ref": sha,
                "whole_case_timeout_seconds": 900,
                "retry_seconds": 120,
                "adapters": {
                    "alice": profile_payload("alice", "author-affiliated"),
                    "bob": profile_payload("bob", "author-independent"),
                },
                "docket_files": ["docs/plans/superseded.md", "watcher.json"],
            }
        ),
        encoding="utf-8",
    )

    code = main(
        [
            "broker-open",
            "--root",
            str(root),
            "--channel",
            name,
            "--config",
            str(config_path),
            "--thread",
            "neutral-review",
            "--first-seat",
            "bob",
            "--body",
            "Neutral acceptance criteria fixed before either adapter runs.",
        ]
    )

    assert code == 0
    assert "opened the case as MSG-1" in capsys.readouterr().out
    entry = channel.read_entries(root, name)[0]
    signal = channel.read_signal(root, name)
    assert entry.sender == "owner"
    assert "Controller-Docket-Provenance" in entry.body
    assert signal["thread"] == "neutral-review"
    assert signal["turn"] == "bob"
    assert (runtime / "cases" / "neutral-review" / "case.json").is_file()


def test_brokered_watcher_posts_validated_result_with_bound_sender_and_provenance(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    open_brokered_thread(root, name, broker)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    output = run_once(config)

    entries = channel.read_entries(root, name)
    assert len(entries) == 4
    assert [entry.sender for entry in entries[1:3]] == ["alice", "bob"]
    assert all("fresh fake review" in entry.body for entry in entries[1:3])
    assert all("Controller-Provenance:" in entry.body for entry in entries[1:3])
    assert broker.profile_hashes["bob"] in entries[2].body
    assert sha in entries[2].body
    assert "bob-runtime-1" in entries[2].body
    assert "Structured appendix." in entries[2].body
    assert entries[-1].entry_type == "close"
    assert "terminal-result: PASS" in entries[-1].body
    assert any("to terminal" in line for line in output)
    with channel.exclusive(root, name):
        assert not any(
            finding.level == channel.ANOMALY for finding in channel.verify_record(root, name)
        )

    invocation = next(
        path
        for path in (broker.runtime_root / "cases" / "review-one" / "invocations").iterdir()
        if "bob" in path.name
    )
    payload = json.loads((invocation / "input.json").read_text(encoding="utf-8"))
    assert str(root.resolve()) not in json.dumps(payload)
    assert "current_thread" not in payload
    assert payload["phase"] == "sealed"
    assert payload["seat"]["author_relationship"] == "author-independent"
    assert (invocation / "stdout.txt").is_file()
    assert (invocation / "stderr.txt").is_file()


@pytest.mark.parametrize("mode", ["malformed", "wrong-sender"])
def test_malformed_or_sender_asserting_result_is_refused_without_mailbox_write(
    tmp_path: Path, mode: str
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, bob_mode=mode)
    open_brokered_thread(root, name, broker)
    controller = BrokerController(broker)

    with pytest.raises(channel.ChannelError, match="refused"):
        controller.invoke_and_post(
            channel_root=root,
            channel_name=name,
            party="bob",
            thread="review-one",
            sequence=1,
            attempt=1,
            transcript=[],
        )

    assert len(channel.read_entries(root, name)) == 1


@pytest.mark.parametrize("label", ["controller-only", "opponent-only", "historical", "user-memory"])
def test_contamination_canary_attempt_rejects_profile_and_records_reason(tmp_path: Path, label: str) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    token = f"PRIVATE-{label}-9f42"
    private = root / f"{label}.txt"
    private.write_text(token, encoding="utf-8")
    broker = make_broker(
        repo,
        sha,
        bob_mode="leak",
        bob_additions={"LEAK_PATH": str(private)},
        canaries={label: token},
    )
    open_brokered_thread(root, name, broker)

    with pytest.raises(channel.ChannelError, match="profile rejected"):
        BrokerController(broker).invoke_and_post(
            channel_root=root,
            channel_name=name,
            party="bob",
            thread="review-one",
            sequence=1,
            attempt=1,
            transcript=[],
        )

    assert len(channel.read_entries(root, name)) == 1
    rejection = next(broker.runtime_root.glob("cases/review-one/invocations/*/rejection.json"))
    assert json.loads(rejection.read_text(encoding="utf-8"))["canary_label"] == label


def test_source_export_is_complete_except_separated_state_and_git_is_unreachable(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    export = create_source_export(broker, "bob")

    assert (export.root / "project_module.py").read_text(encoding="utf-8") == "VALUE = 42\n"
    assert (export.root / ".claude" / "settings.json").is_file(), "tracked config remains review evidence"
    assert not (export.root / ".git").exists()
    assert not (export.root / "collab").exists()
    assert not (export.root / "var").exists()
    tracked = set(
        _run(["git", "ls-tree", "-r", "--name-only", sha], repo).stdout.splitlines()
    )
    expected = {
        path
        for path in tracked
        if path.split("/", 1)[0] not in {"collab", "var", ".git"}
    }
    assert set(export.files) == expected

    home = broker.runtime_root / "probe-home"
    build = broker.runtime_root / "probe-build"
    home.mkdir(parents=True)
    build.mkdir(parents=True)
    env = {
        **_baseline_environment(),
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(home),
        "GIT_CEILING_DIRECTORIES": str(repo.resolve()),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTEST_ADDOPTS": f"-p no:cacheprovider --basetemp={build}",
    }
    probes = (
        ["git", "rev-parse", "--show-toplevel"],
        ["git", "show", f"{sha}:collab/fixture-11111.channel.md"],
        ["git", "ls-tree", sha, "--full-tree", "collab/"],
        ["git", "log", sha, "--", ":(top)collab/"],
    )
    for probe in probes:
        assert _run(probe, export.root, env=env).returncode != 0, probe

    project_test = _run(
        [sys.executable, "-m", "pytest", "-q"],
        export.root,
        env=env,
    )
    assert project_test.returncode == 0, (project_test.stdout, project_test.stderr)


def test_untracked_docket_files_are_content_addressed_and_manifested(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)

    docket = materialize_docket(broker)

    assert (docket.root / "files" / "docs" / "plans" / "superseded.md").read_text(
        encoding="utf-8"
    ).startswith("# Untracked")
    assert (docket.root / "files" / "watcher.json").is_file()
    assert all(record["tracked_at_source_ref"] is False for record in docket.files)
    manifest = json.loads(docket.manifest_path.read_text(encoding="utf-8"))
    assert manifest["revision_sha256"] == docket.revision_sha256
    assert all(len(record["sha256"]) == 64 for record in manifest["files"])


def test_phase_renderer_keeps_sealed_input_opponent_free_and_open_input_thread_scoped(
    tmp_path: Path,
) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(
        repo,
        sha,
        canaries={
            "controller-only": "CONTROLLER-PRIVATE-1",
            "opponent-only": "OPPONENT-PRIVATE-2",
            "historical": "HISTORY-PRIVATE-3",
            "user-memory": "MEMORY-PRIVATE-4",
        },
    )
    controller = BrokerController(broker)
    exports, docket, _ = controller._prepare_case("phase-test")
    result_path = broker.runtime_root / "phase-result.json"

    sealed = controller.render_input(
        party="bob",
        phase="sealed",
        thread="phase-test",
        result_path=result_path,
        source=exports["bob"],
        docket=docket,
        transcript=None,
    )
    encoded = json.dumps(sealed)
    assert "current_thread" not in sealed
    assert all(token not in encoded for token in broker.contamination_canaries.values())
    with pytest.raises(channel.ChannelError, match="sealed adapter input"):
        controller.render_input(
            party="bob",
            phase="sealed",
            thread="phase-test",
            result_path=result_path,
            source=exports["bob"],
            docket=docket,
            transcript=[{"body": "opponent result"}],
        )

    current = [{"id": "MSG-7", "sender": "alice", "body": "current only"}]
    opened = controller.render_input(
        party="bob",
        phase="open",
        thread="phase-test",
        result_path=result_path,
        source=exports["bob"],
        docket=docket,
        transcript=current,
    )
    assert opened["current_thread"] == current


def test_minimum_and_recommended_topologies_are_explicit_and_zero_independent_refuses(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    minimum = make_broker(repo, sha)
    recommended = make_broker(repo, sha, alice_relationship="author-independent")

    assert minimum.topology == "minimum-two-agent"
    assert recommended.topology == "recommended-three-agent"
    assert "relationship=author-affiliated" in "\n".join(doctor_lines(minimum))
    assert "recommended-three-agent" in doctor_lines(recommended)[0]

    with pytest.raises(channel.ChannelError, match="author-independent"):
        make_broker(repo, sha, bob_relationship="author-affiliated")


@pytest.mark.parametrize(
    ("alice_relationship", "expected_topology"),
    [
        ("author-affiliated", "minimum-two-agent"),
        ("author-independent", "recommended-three-agent"),
    ],
)
def test_same_fake_case_runs_under_both_recorded_topologies(
    tmp_path: Path, alice_relationship: str, expected_topology: str
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, alice_relationship=alice_relationship)
    open_brokered_thread(root, name, broker)

    outcome = BrokerController(broker).invoke_and_post(
        channel_root=root,
        channel_name=name,
        party="bob",
        thread="review-one",
        sequence=1,
        attempt=1,
        transcript=[],
    )

    assert outcome.entry_id == "MSG-2"
    assert f"topology: {expected_topology}" in channel.read_entries(root, name)[-1].body


def test_timing_validation_and_report_share_one_calculation(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    report = broker.timing.report()

    assert report["unconstrained_schedule_seconds"] == broker.timing.unconstrained_seconds
    assert report["enforced_terminal_bound_seconds"] == min(
        report["unconstrained_schedule_seconds"], report["whole_case_timeout_seconds"]
    )
    with pytest.raises(channel.ChannelError, match="between 1 and 3600"):
        make_profile("slow", "author-independent", timeout=3601)
    with pytest.raises(channel.ChannelError, match="whole_case_timeout_seconds"):
        TimingPolicy(12, 60, 120, 0, tuple(broker.profiles.values()))  # type: ignore[arg-type]


def test_profiles_refuse_live_user_settings_and_controller_owned_environment() -> None:
    with pytest.raises(channel.ChannelError, match="live settings sources"):
        profile = make_profile("seat", "author-independent")
        AdapterProfile(**{**profile.__dict__, "settings_sources": ("user",)})
    with pytest.raises(channel.ChannelError, match="inherit user/runtime configuration"):
        profile = make_profile("seat", "author-independent")
        AdapterProfile(**{**profile.__dict__, "environment_allowlist": ("CODEX_HOME",)})
    with pytest.raises(channel.ChannelError, match="controller-owned environment"):
        profile = make_profile("seat", "author-independent")
        AdapterProfile(**{**profile.__dict__, "environment": {"GIT_DIR": "/host/repo/.git"}})
    with pytest.raises(channel.ChannelError, match="controller-owned environment"):
        profile = make_profile("seat", "author-independent")
        AdapterProfile(**{**profile.__dict__, "environment": {"GIT_CONFIG_KEY_0": "include.path"}})
    with pytest.raises(channel.ChannelError, match="controller-owned environment"):
        profile = make_profile("seat", "author-independent")
        AdapterProfile(**{**profile.__dict__, "environment": {"CLAUDE_CONFIG_DIR": "/host/.claude"}})
    bridge_shaped = AdapterProfile(
        **{
            **make_profile("seat", "author-independent").__dict__,
            "environment": {"PYTHONPATH": "src", "DEBATE_BRIDGE_REAL_HOME": "/home/x"},
            "environment_allowlist": (
                "PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR",
                "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
            ),
        }
    )
    assert bridge_shaped.environment == {"PYTHONPATH": "src", "DEBATE_BRIDGE_REAL_HOME": "/home/x"}


def _write_result(path: Path, extra: dict[str, object]) -> None:
    payload: dict[str, object] = {
        "schema_version": 1,
        "entry_type": "verdict",
        "body": "seat review text",
        "runtime_model": "seat-runtime-1",
        "decision": "PASS",
    }
    payload.update(extra)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_parse_result_defaults_accepts_and_refuses_runtime_model_basis_configuration_home_isolation_flags(
    tmp_path: Path,
) -> None:
    profile = make_profile("seat", "author-independent")
    result_path = tmp_path / "result.json"

    _write_result(result_path, {})
    absent = _parse_result(result_path, "seat", profile)
    assert absent.runtime_model_basis == "verified"
    assert absent.configuration_home == "sandbox"
    assert absent.isolation_flags is None

    _write_result(
        result_path,
        {
            "runtime_model_basis": "declared",
            "configuration_home": "operator (CLAUDE_CONFIG_DIR)",
            "isolation_flags": "catalogued",
        },
    )
    declared = _parse_result(result_path, "seat", profile)
    assert declared.runtime_model_basis == "declared"
    assert declared.configuration_home == "operator (CLAUDE_CONFIG_DIR)"
    assert declared.isolation_flags == "catalogued"

    _write_result(
        result_path,
        {
            "runtime_model_basis": "verified",
            "configuration_home": "sandbox",
            "isolation_flags": "declared",
        },
    )
    verified = _parse_result(result_path, "seat", profile)
    assert verified.runtime_model_basis == "verified"
    assert verified.configuration_home == "sandbox"
    assert verified.isolation_flags == "declared"

    _write_result(result_path, {"runtime_model_basis": "bogus"})
    with pytest.raises(AdapterError, match="runtime_model_basis must be 'verified' or 'declared'"):
        _parse_result(result_path, "seat", profile)

    _write_result(result_path, {"configuration_home": "bogus"})
    with pytest.raises(AdapterError, match="configuration_home must be"):
        _parse_result(result_path, "seat", profile)

    _write_result(result_path, {"configuration_home": "operator (lowercase)"})
    with pytest.raises(AdapterError, match="configuration_home must be"):
        _parse_result(result_path, "seat", profile)

    _write_result(result_path, {"isolation_flags": "bogus"})
    with pytest.raises(AdapterError, match="isolation_flags must be"):
        _parse_result(result_path, "seat", profile)


def test_parse_result_accepts_deliberation_input_only_on_a_later_pass(tmp_path: Path) -> None:
    profile = make_profile("seat", "author-independent")
    result_path = tmp_path / "result.json"

    _write_result(result_path, {})
    assert _parse_result(result_path, "seat", profile).deliberation_input is None
    assert _parse_result(result_path, "seat", profile, phase="deliberation").deliberation_input is None

    for value in ("verdicts-only", "full-docket"):
        _write_result(result_path, {"deliberation_input": value})
        for phase in ("deliberation", "open"):
            carried = _parse_result(result_path, "seat", profile, phase=phase)
            assert carried.deliberation_input == value
        with pytest.raises(AdapterError, match="deliberation_input on a sealed result"):
            _parse_result(result_path, "seat", profile)
        with pytest.raises(AdapterError, match="deliberation_input on a sealed result"):
            _parse_result(result_path, "seat", profile, phase="sealed")

    _write_result(result_path, {"deliberation_input": "bogus"})
    with pytest.raises(AdapterError, match="deliberation_input must be"):
        _parse_result(result_path, "seat", profile, phase="deliberation")


def test_published_body_shows_default_and_extended_provenance_lines(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    evidence: dict[str, str | Path] = {
        "source_manifest_sha256": "source-sha",
        "docket_revision_sha256": "docket-sha",
        "input_sha256": "input-sha",
    }

    default_result = AdapterResult("verdict", "body text", "", "", "bob-runtime-1", "PASS")
    default_body = controller._published_body(party="bob", result=default_result, evidence=evidence, phase="sealed")
    assert "- runtime-model-basis: verified" in default_body
    assert "- configuration-home: sandbox" in default_body
    assert "- isolation-flags:" not in default_body

    extended_result = AdapterResult(
        "verdict",
        "body text",
        "",
        "",
        "bob-runtime-1",
        "PASS",
        runtime_model_basis="declared",
        configuration_home="operator (CLAUDE_CONFIG_DIR)",
        isolation_flags="catalogued",
    )
    extended_body = controller._published_body(
        party="bob", result=extended_result, evidence=evidence, phase="sealed"
    )
    assert "- runtime-model-basis: declared" in extended_body
    assert "- configuration-home: operator (CLAUDE_CONFIG_DIR)" in extended_body
    assert "- isolation-flags: catalogued" in extended_body


def test_published_body_names_what_a_later_pass_read_and_stays_silent_on_a_sealed_one(
    tmp_path: Path,
) -> None:
    repo, sha = make_repository(tmp_path)
    controller = BrokerController(make_broker(repo, sha))
    evidence: dict[str, str | Path] = {
        "source_manifest_sha256": "source-sha",
        "docket_revision_sha256": "docket-sha",
        "input_sha256": "input-sha",
    }

    sealed_result = AdapterResult("verdict", "body text", "", "", "bob-runtime-1", "PASS")
    sealed_body = controller._published_body(
        party="bob", result=sealed_result, evidence=evidence, phase="sealed"
    )
    assert "- deliberation-input:" not in sealed_body

    later_result = AdapterResult(
        "verdict",
        "body text",
        "",
        "",
        "bob-runtime-1",
        "PASS",
        runtime_model_basis="declared",
        configuration_home="sandbox",
        isolation_flags="catalogued",
        deliberation_input="verdicts-only",
    )
    later_body = controller._published_body(
        party="bob", result=later_result, evidence=evidence, phase="deliberation"
    )
    assert "- deliberation-input: verdicts-only" in later_body
    assert later_body.index("- configuration-home:") < later_body.index("- deliberation-input:")
    assert later_body.index("- isolation-flags:") < later_body.index("- deliberation-input:")


def test_a_recorded_result_round_trips_what_the_pass_read_and_defaults_to_nothing() -> None:
    evidence: dict[str, str | Path] = {
        "source_manifest_sha256": "source-sha",
        "docket_revision_sha256": "docket-sha",
        "input_sha256": "input-sha",
    }
    result = AdapterResult(
        "verdict", "body text", "", "", "bob-runtime-1", "PASS", deliberation_input="full-docket"
    )
    record = BrokerController._result_record(result, evidence, "2026-08-20T12:00:00+00:00")
    recorded = record["result"]
    assert isinstance(recorded, dict)
    assert recorded["deliberation_input"] == "full-docket"
    assert BrokerController._recorded_result(record)[0].deliberation_input == "full-docket"

    recorded.pop("deliberation_input")
    assert BrokerController._recorded_result(record)[0].deliberation_input is None


def test_sealed_capture_round_trip_publishes_extended_provenance_lines_after_reveal(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(
        repo,
        sha,
        bob_additions={"FAKE_EXTRA_PROVENANCE": "1"},
    )
    open_brokered_thread(root, name, broker)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    run_once(config)

    entries = channel.read_entries(root, name)
    bob_entry = next(entry for entry in entries if entry.sender == "bob")
    alice_entry = next(entry for entry in entries if entry.sender == "alice")
    assert "- runtime-model-basis: declared" in bob_entry.body
    assert "- configuration-home: operator (CLAUDE_CONFIG_DIR)" in bob_entry.body
    assert "- isolation-flags: catalogued" in bob_entry.body
    assert "- runtime-model-basis: verified" in alice_entry.body
    assert "- configuration-home: sandbox" in alice_entry.body
    assert "- isolation-flags:" not in alice_entry.body


def test_recorded_sealed_submission_without_new_provenance_keys_loads_with_defaults(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="pre-c4-record",
        first_party="alice",
        body="Inspect the pinned source and return a structured review.",
    )
    for party in ("alice", "bob"):
        controller.capture_sealed(
            channel_root=root,
            channel_name=name,
            party=party,
            thread="pre-c4-record",
            sequence=1,
            attempt=1,
        )
    case_path = broker.runtime_root / "cases" / "pre-c4-record" / "case.json"
    state = json.loads(case_path.read_text(encoding="utf-8"))
    for party in ("alice", "bob"):
        record_result = state["sealed_submissions"][party]["result"]
        record_result.pop("runtime_model_basis", None)
        record_result.pop("configuration_home", None)
        record_result.pop("isolation_flags", None)
    case_path.write_text(json.dumps(state), encoding="utf-8")

    controller.reveal_pair(channel_root=root, channel_name=name, thread="pre-c4-record")

    entries = channel.read_entries(root, name)
    published = [entry for entry in entries if entry.sender in ("alice", "bob")]
    assert len(published) == 2
    for entry in published:
        assert "- runtime-model-basis: verified" in entry.body
        assert "- configuration-home: sandbox" in entry.body
        assert "- isolation-flags:" not in entry.body


def _bridge_seat_command(
    *, seat_id: str, config_home: str | None, isolation_flags_basis: str
) -> tuple[str, ...]:
    command = [
        sys.executable, "-m", "debate", "run-seat",
        "--seat-id", seat_id,
        "--vendor", "anthropic",
        "--submodel", "claude-opus",
        "--argv-json", json.dumps(["claude", "{prompt}"]),
        "--isolation-argv-json", json.dumps(["--strict-mcp-config"]),
        "--no-persistence-argv-json", json.dumps(["--no-session"]),
    ]
    if config_home is not None:
        command += ["--config-home", config_home]
    command += [
        "--deliberation-input", "full",
        "--isolation-flags-basis", isolation_flags_basis,
        "{input_path}", "{result_path}",
    ]
    return tuple(command)


def test_doctor_lines_reports_configuration_home_and_isolation_flags_only_for_bridge_seats(
    tmp_path: Path,
) -> None:
    repo, sha = make_repository(tmp_path)

    hand_authored = make_profile("alice", "author-affiliated")
    bridge_with_config_home = AdapterProfile(
        **{
            **make_profile("bob", "author-independent").__dict__,
            "command": _bridge_seat_command(
                seat_id="bob", config_home="CLAUDE_CONFIG_DIR=.claude", isolation_flags_basis="catalogued"
            ),
        }
    )
    profiles_with_config_home = {"alice": hand_authored, "bob": bridge_with_config_home}
    timing_with_config_home = TimingPolicy(
        thread_cap=12,
        scheduler_interval_seconds=60,
        retry_seconds=120,
        whole_case_timeout_seconds=900,
        profiles=(profiles_with_config_home["alice"], profiles_with_config_home["bob"]),
    )
    config_with_config_home = BrokerConfig(
        repository_root=repo,
        runtime_root=repo / "var" / "debate" / "doctor-bridge-config-home",
        source_ref=sha,
        profiles=profiles_with_config_home,
        timing=timing_with_config_home,
        config_sha256="a" * 64,
    )
    lines_with_config_home = doctor_lines(config_with_config_home)
    assert "seat bob: configuration home OPERATOR (CLAUDE_CONFIG_DIR); isolation flags catalogued" in (
        lines_with_config_home
    )
    assert not any(line.startswith("seat alice: configuration home") for line in lines_with_config_home)

    bridge_without_config_home = AdapterProfile(
        **{
            **make_profile("bob", "author-independent").__dict__,
            "command": _bridge_seat_command(
                seat_id="bob", config_home=None, isolation_flags_basis="declared"
            ),
        }
    )
    profiles_without_config_home = {"alice": hand_authored, "bob": bridge_without_config_home}
    timing_without_config_home = TimingPolicy(
        thread_cap=12,
        scheduler_interval_seconds=60,
        retry_seconds=120,
        whole_case_timeout_seconds=900,
        profiles=(profiles_without_config_home["alice"], profiles_without_config_home["bob"]),
    )
    config_without_config_home = BrokerConfig(
        repository_root=repo,
        runtime_root=repo / "var" / "debate" / "doctor-bridge-sandbox",
        source_ref=sha,
        profiles=profiles_without_config_home,
        timing=timing_without_config_home,
        config_sha256="a" * 64,
    )
    lines_without_config_home = doctor_lines(config_without_config_home)
    assert "seat bob: configuration home SANDBOX; isolation flags declared" in lines_without_config_home


def test_doctor_lines_reads_isolation_flags_basis_through_an_abbreviated_flag(tmp_path: Path) -> None:
    # argparse (stock, via bridge.configure_parser) accepts unambiguous flag
    # abbreviations, e.g. --isolation-flags-b for --isolation-flags-basis.
    # The doctor must read the parsed BridgeSpec, not re-scan raw argv tokens,
    # so it has to understand the abbreviated form exactly like the real
    # parser does.
    repo, sha = make_repository(tmp_path)
    hand_authored = make_profile("alice", "author-affiliated")
    command = list(
        _bridge_seat_command(seat_id="bob", config_home=None, isolation_flags_basis="catalogued")
    )
    index = command.index("--isolation-flags-basis")
    command[index] = "--isolation-flags-b"
    bridge_abbreviated = AdapterProfile(
        **{**make_profile("bob", "author-independent").__dict__, "command": tuple(command)}
    )
    profiles = {"alice": hand_authored, "bob": bridge_abbreviated}
    timing = TimingPolicy(
        thread_cap=12,
        scheduler_interval_seconds=60,
        retry_seconds=120,
        whole_case_timeout_seconds=900,
        profiles=(profiles["alice"], profiles["bob"]),
    )
    config = BrokerConfig(
        repository_root=repo,
        runtime_root=repo / "var" / "debate" / "doctor-bridge-abbreviated-flag",
        source_ref=sha,
        profiles=profiles,
        timing=timing,
        config_sha256="a" * 64,
    )
    lines = doctor_lines(config)
    assert "seat bob: configuration home SANDBOX; isolation flags catalogued" in lines


def test_runtime_root_below_a_tool_cache_is_refused(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)

    with pytest.raises(channel.ChannelError, match="tool-managed caches"):
        BrokerConfig(
            repository_root=broker.repository_root,
            runtime_root=repo / "var" / "debate" / ".pytest_cache" / "case",
            source_ref=broker.source_ref,
            profiles=broker.profiles,
            timing=broker.timing,
            config_sha256=broker.config_sha256,
        )


def test_tampered_materialized_docket_is_refused_on_reuse(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    docket = materialize_docket(broker)
    plan = docket.root / "files" / "docs" / "plans" / "superseded.md"
    plan.chmod(0o644)
    plan.write_text("tampered\n", encoding="utf-8")

    with pytest.raises(channel.ChannelError, match="immutable docket file changed"):
        materialize_docket(broker)


def test_half_recorded_revision_blocks_the_next_adapter_invocation(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller._prepare_case("pending-case")
    manifest_path = broker.runtime_root / "cases" / "pending-case" / "case.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["pending_revision"] = {"revision_sha256": "f" * 64}
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(channel.ChannelError, match="half-finished broker-revise"):
        controller._prepare_case("pending-case")


def test_case_runtime_survives_pytest_cache_clear_and_profile_drift_is_refused(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller._prepare_case("review-one")
    case_manifest = broker.runtime_root / "cases" / "review-one" / "case.json"
    (repo / ".pytest_cache").mkdir()
    (repo / ".pytest_cache" / "throwaway").write_text("cache", encoding="utf-8")

    shutil.rmtree(repo / ".pytest_cache")
    cache_env = dict(os.environ)
    cache_env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    cache_env.pop("PYTEST_ADDOPTS", None)
    proc = _run([sys.executable, "-m", "pytest", "--cache-clear", "-q"], repo, env=cache_env)

    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert case_manifest.is_file()
    drifted = make_broker(repo, sha, bob_additions={"NEW_PROFILE_INPUT": "changed"})
    with pytest.raises(channel.ChannelError, match="changed profile_sha256"):
        BrokerController(drifted)._prepare_case("review-one")


def test_broker_revise_records_new_immutable_revision_before_next_seat(tmp_path: Path) -> None:
    repo, first_sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    first = make_broker(repo, first_sha)
    open_brokered_thread(root, name, first)
    original_turn = channel.read_signal(root, name)["turn"]

    (repo / "project_module.py").write_text("VALUE = 43\n", encoding="utf-8")
    assert _run(["git", "add", "project_module.py"], repo).returncode == 0
    assert _run(["git", "commit", "-m", "fix after review"], repo).returncode == 0
    second_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    (repo / "docs" / "plans" / "superseded.md").write_text(
        "# Untracked plan revision\n\nAmended after findings.\n", encoding="utf-8"
    )
    second = make_broker(repo, second_sha, config_sha256="b" * 64)

    entry_id = BrokerController(second).revise_case(
        channel_root=root,
        channel_name=name,
        thread="review-one",
        body="Artifact and docket amended; review the new immutable revision.",
        refs=f"main@{second_sha}",
    )

    assert entry_id == "MSG-2"
    assert channel.read_entries(root, name)[1].sender == "owner"
    assert channel.read_signal(root, name)["turn"] == original_turn
    manifest = json.loads(
        (second.runtime_root / "cases" / "review-one" / "case.json").read_text(encoding="utf-8")
    )
    assert manifest["source_ref"] == second_sha
    assert [revision["source_ref"] for revision in manifest["revisions"]] == [first_sha, second_sha]
    assert "pending_revision" not in manifest

    outcome = BrokerController(second).invoke_and_post(
        channel_root=root,
        channel_name=name,
        party="bob",
        thread="review-one",
        sequence=2,
        attempt=1,
        transcript=[],
    )
    assert outcome.entry_id == "MSG-3"
    assert second_sha in channel.read_entries(root, name)[-1].body


@pytest.mark.parametrize("first_party", ["alice", "bob"])
def test_sealed_pair_completes_in_either_order_without_cross_anchoring(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, first_party: str
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="ordered-seal",
        first_party=first_party,
        body="Neutral docket.",
    )
    # Hooked at the recording step, not the capture, so the assertion holds
    # whichever sealed mode is configured: the two seats may be ASKED at once,
    # but they are recorded one at a time, first_party first.
    order: list[str] = []
    original = controller._record_sealed

    def record_order(**kwargs: object) -> AdapterResult:
        order.append(str(kwargs["party"]))
        return original(**kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(controller, "_record_sealed", record_order)
    outcome = controller.drive_case(
        channel_root=root,
        channel_name=name,
        thread="ordered-seal",
        sequence=1,
        attempt=1,
    )

    other = "bob" if first_party == "alice" else "alice"
    assert order == [first_party, other]
    assert outcome.terminal_result == "PASS"
    inputs = sorted(broker.runtime_root.glob("cases/ordered-seal/invocations/*/input.json"))
    assert len(inputs) == 2
    for path in inputs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["phase"] == "sealed"
        assert "current_thread" not in payload
        assert "Controller-Sealed-Reveal" not in json.dumps(payload)
    case = json.loads(
        (broker.runtime_root / "cases" / "ordered-seal" / "case.json").read_text(encoding="utf-8")
    )
    entries = {entry.sender: entry for entry in channel.read_entries(root, name) if entry.sender in broker.profiles}
    for party, submission in case["sealed_submissions"].items():
        captured_at = submission["captured_at"]
        assert datetime.fromisoformat(captured_at).tzinfo is not None
        assert f"- captured-at: {captured_at}" in entries[party].body
        assert case["latest_votes"][party]["captured_at"] == captured_at


def test_restart_after_first_private_submission_does_not_repeat_or_expose_it(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    first = BrokerController(broker)
    first.open_case(
        channel_root=root,
        channel_name=name,
        thread="restart-seal",
        first_party="bob",
        body="Neutral docket.",
    )

    first.capture_sealed(
        channel_root=root,
        channel_name=name,
        party="bob",
        thread="restart-seal",
        sequence=1,
        attempt=1,
    )

    assert len(channel.read_entries(root, name)) == 1
    assert channel.read_signal(root, name)["turn"] == "alice"
    restarted = BrokerController(broker)
    outcome = restarted.drive_case(
        channel_root=root,
        channel_name=name,
        thread="restart-seal",
        sequence=1,
        attempt=1,
    )

    assert outcome.terminal_result == "PASS"
    invocation_names = sorted(path.name for path in broker.runtime_root.glob("cases/restart-seal/invocations/*"))
    assert invocation_names == ["1-alice-1", "1-bob-1"]
    assert len([entry for entry in channel.read_entries(root, name) if entry.sender == "bob"]) == 1


def test_restart_from_persisted_reveal_phase_commits_pair_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="restart-reveal",
        first_party="alice",
        body="Neutral docket.",
    )
    for party in ("alice", "bob"):
        controller.capture_sealed(
            channel_root=root,
            channel_name=name,
            party=party,
            thread="restart-reveal",
            sequence=1,
            attempt=1,
        )
    real_commit = channel.commit_reveal_pair

    def crash_before_mailbox(*_: object, **__: object) -> tuple[str, str]:
        raise RuntimeError("simulated crash at reveal write boundary")

    monkeypatch.setattr(channel, "commit_reveal_pair", crash_before_mailbox)
    with pytest.raises(RuntimeError, match="reveal write boundary"):
        controller.reveal_pair(channel_root=root, channel_name=name, thread="restart-reveal")
    state = json.loads((broker.runtime_root / "cases" / "restart-reveal" / "case.json").read_text())
    assert state["phase"] == "reveal"
    assert len(channel.read_entries(root, name)) == 1

    monkeypatch.setattr(channel, "commit_reveal_pair", real_commit)
    outcome = BrokerController(broker).drive_case(
        channel_root=root,
        channel_name=name,
        thread="restart-reveal",
        sequence=1,
        attempt=1,
    )

    assert outcome.terminal_result == "PASS"
    assert len([entry for entry in channel.read_entries(root, name) if entry.sender in broker.profiles]) == 2


def test_recurring_tick_repairs_paired_reveal_after_mailbox_before_signal_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="restart-paired-reveal",
        first_party="alice",
        body="Neutral docket.",
    )
    for party in ("alice", "bob"):
        controller.capture_sealed(
            channel_root=root,
            channel_name=name,
            party=party,
            thread="restart-paired-reveal",
            sequence=1,
            attempt=1,
        )

    real_atomic_write = channel._atomic_write
    crashed = False

    def crash_after_paired_mailbox(path: Path, content: str) -> None:
        nonlocal crashed
        if path.name.endswith(".signal.json") and not crashed:
            crashed = True
            raise RuntimeError("simulated crash after paired mailbox commit")
        real_atomic_write(path, content)

    monkeypatch.setattr(channel, "_atomic_write", crash_after_paired_mailbox)
    with pytest.raises(RuntimeError, match="paired mailbox"):
        controller.reveal_pair(channel_root=root, channel_name=name, thread="restart-paired-reveal")
    monkeypatch.setattr(channel, "_atomic_write", real_atomic_write)

    assert channel.read_signal(root, name)["seq"] == 1
    assert len(channel.read_entries(root, name)) == 3
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    output = run_once(config)

    entries = channel.read_entries(root, name)
    signal = channel.read_signal(root, name)
    assert len([entry for entry in entries if entry.sender in broker.profiles]) == 2
    assert signal["phase"] == "terminal"
    assert signal["terminal_result"] == "PASS"
    assert not any(line.startswith(("ESCALATE:", "STUCK:")) for line in output)
    assert any("recovered paired reveal" in line for line in output)


def test_recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="restart-typed-close",
        first_party="alice",
        body="Neutral docket.",
    )
    real_atomic_write = channel._atomic_write
    crashed = False

    def crash_after_terminal_mailbox(path: Path, content: str) -> None:
        nonlocal crashed
        if path.name.endswith(".signal.json") and '"phase": "terminal"' in content and not crashed:
            crashed = True
            raise RuntimeError("simulated crash after terminal mailbox commit")
        real_atomic_write(path, content)

    monkeypatch.setattr(channel, "_atomic_write", crash_after_terminal_mailbox)
    with pytest.raises(RuntimeError, match="terminal mailbox"):
        controller.drive_case(
            channel_root=root,
            channel_name=name,
            thread="restart-typed-close",
            sequence=1,
            attempt=1,
        )
    monkeypatch.setattr(channel, "_atomic_write", real_atomic_write)

    assert channel.read_signal(root, name)["phase"] == "deliberation"
    assert len(channel.read_entries(root, name)) == 4
    case_state = json.loads(
        (broker.runtime_root / "cases" / "restart-typed-close" / "case.json").read_text(
            encoding="utf-8"
        )
    )
    assert case_state["pending_terminal"] == {
        "result": "PASS",
        "close_reason": "party-vote-agreement",
    }
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    output = run_once(config)

    signal = channel.read_signal(root, name)
    repaired = json.loads(
        (broker.runtime_root / "cases" / "restart-typed-close" / "case.json").read_text(
            encoding="utf-8"
        )
    )
    assert signal["phase"] == repaired["phase"] == "terminal"
    assert signal["terminal_result"] == repaired["terminal_result"] == "PASS"
    assert "pending_terminal" not in repaired
    assert len(channel.read_entries(root, name)) == 4
    assert not any(line.startswith(("ESCALATE:", "STUCK:")) for line in output)
    assert any("recovered typed close" in line for line in output)


def test_reveal_phase_does_not_explain_an_unrelated_mailbox_ahead_entry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="unexplained-ahead",
        first_party="alice",
        body="Neutral docket.",
    )
    for party in ("alice", "bob"):
        controller.capture_sealed(
            channel_root=root,
            channel_name=name,
            party=party,
            thread="unexplained-ahead",
            sequence=1,
            attempt=1,
        )

    def stop_before_reveal(*_: object, **__: object) -> tuple[str, str]:
        raise RuntimeError("stop before paired mailbox commit")

    monkeypatch.setattr(channel, "commit_reveal_pair", stop_before_reveal)
    with pytest.raises(RuntimeError, match="stop before"):
        controller.reveal_pair(channel_root=root, channel_name=name, thread="unexplained-ahead")
    real_atomic_write = channel._atomic_write

    def crash_unknown_signal(path: Path, content: str) -> None:
        if path.name.endswith(".signal.json"):
            raise RuntimeError("unrelated writer crashed")
        real_atomic_write(path, content)

    monkeypatch.setattr(channel, "_atomic_write", crash_unknown_signal)
    with pytest.raises(RuntimeError, match="unrelated writer"):
        channel.post(
            root,
            "owner",
            "info",
            "unexplained-ahead",
            "Unrelated supervisor entry without a signal.",
            name=name,
        )
    monkeypatch.setattr(channel, "_atomic_write", real_atomic_write)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    output = run_once(config)

    assert channel.read_signal(root, name)["seq"] == 1
    assert len(channel.read_entries(root, name)) == 2
    assert any("mailbox ahead of signal" in line for line in output)
    assert not any("broker recover" in line for line in output)


def test_one_retryable_sealed_timeout_publishes_nothing_until_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="one-timeout",
        first_party="alice",
        body="Neutral docket.",
    )
    original = controller._invoke
    timed_out = False

    def timeout_once(**kwargs: object) -> tuple[AdapterResult, dict[str, str | Path]]:
        nonlocal timed_out
        if not timed_out:
            timed_out = True
            raise AdapterError("fixture timeout", retryable=True, close_reason="adapter-timeout")
        return original(**kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(controller, "_invoke", timeout_once)
    with pytest.raises(AdapterError, match="fixture timeout"):
        controller.drive_case(
            channel_root=root,
            channel_name=name,
            thread="one-timeout",
            sequence=1,
            attempt=1,
        )
    assert len(channel.read_entries(root, name)) == 1

    outcome = controller.drive_case(
        channel_root=root,
        channel_name=name,
        thread="one-timeout",
        sequence=1,
        attempt=2,
    )
    assert outcome.terminal_result == "PASS"


def test_real_adapter_timeout_is_bounded_and_retryable_without_mailbox_write(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, alice_timeout=1)
    slow_profile = AdapterProfile(
        **{
            **broker.profiles["alice"].__dict__,
            "environment": {
                **broker.profiles["alice"].environment,
                "FAKE_MODE": "timeout",
            },
        }
    )
    profiles = {**broker.profiles, "alice": slow_profile}
    slow_broker = BrokerConfig(
        repository_root=broker.repository_root,
        runtime_root=broker.runtime_root,
        source_ref=broker.source_ref,
        profiles=profiles,
        timing=TimingPolicy(
            thread_cap=12,
            scheduler_interval_seconds=60,
            retry_seconds=120,
            whole_case_timeout_seconds=900,
            profiles=(profiles["alice"], profiles["bob"]),
        ),
        config_sha256=broker.config_sha256,
        docket_files=broker.docket_files,
    )
    controller = BrokerController(slow_broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="real-timeout",
        first_party="alice",
        body="Neutral docket.",
    )

    with pytest.raises(AdapterError, match="timed out after 1s") as caught:
        controller.drive_case(
            channel_root=root,
            channel_name=name,
            thread="real-timeout",
            sequence=1,
            attempt=1,
        )

    assert caught.value.retryable is True
    assert caught.value.close_reason == "adapter-timeout"
    assert len(channel.read_entries(root, name)) == 1


def test_expiry_during_sealed_invocation_closes_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, whole_case_timeout_seconds=5)
    opened_at = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
    controller = BrokerController(broker, now=opened_at)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="expires-during",
        first_party="alice",
        body="Neutral docket.",
    )

    def finish_after_deadline(**_: object) -> tuple[AdapterResult, dict[str, str | Path]]:
        controller._fixed_now = opened_at + timedelta(seconds=6)
        return (
            AdapterResult("verdict", "late", "", "", "fixture", "PASS"),
            {
                "input_sha256": "1" * 64,
                "source_manifest_sha256": "2" * 64,
                "docket_revision_sha256": "3" * 64,
                "diagnostics_root": broker.runtime_root,
            },
        )

    monkeypatch.setattr(controller, "_invoke", finish_after_deadline)
    outcome = controller.drive_case(
        channel_root=root,
        channel_name=name,
        thread="expires-during",
        sequence=1,
        attempt=1,
    )

    assert outcome.terminal_result == "ERROR"
    assert outcome.close_reason == "case-deadline-expired"
    assert channel.read_signal(root, name)["close_reason"] == "case-deadline-expired"
    assert not any(entry.sender in broker.profiles for entry in channel.read_entries(root, name))


def test_expiry_recovery_is_idempotent_after_controller_restart(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, whole_case_timeout_seconds=5)
    opened_at = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
    BrokerController(broker, now=opened_at).open_case(
        channel_root=root,
        channel_name=name,
        thread="expired-restart",
        first_party="bob",
        body="Neutral docket.",
    )
    expired = opened_at + timedelta(seconds=6)

    first = BrokerController(broker, now=expired).drive_case(
        channel_root=root,
        channel_name=name,
        thread="expired-restart",
        sequence=1,
        attempt=1,
    )
    second = BrokerController(broker, now=expired + timedelta(seconds=30)).drive_case(
        channel_root=root,
        channel_name=name,
        thread="expired-restart",
        sequence=2,
        attempt=1,
    )

    assert first.terminal_result == second.terminal_result == "ERROR"
    assert len([entry for entry in channel.read_entries(root, name) if entry.entry_type == "close"]) == 1


def test_restart_with_both_private_positions_expires_between_sealed_and_reveal(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, whole_case_timeout_seconds=5)
    opened_at = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)
    controller = BrokerController(broker, now=opened_at)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="expires-between",
        first_party="alice",
        body="Neutral docket.",
    )
    for party in ("alice", "bob"):
        controller.capture_sealed(
            channel_root=root,
            channel_name=name,
            party=party,
            thread="expires-between",
            sequence=1,
            attempt=1,
        )
    assert len(channel.read_entries(root, name)) == 1

    outcome = BrokerController(broker, now=opened_at + timedelta(seconds=6)).drive_case(
        channel_root=root,
        channel_name=name,
        thread="expires-between",
        sequence=1,
        attempt=1,
    )

    assert outcome.terminal_result == "ERROR"
    assert outcome.close_reason == "case-deadline-expired"
    assert not any("Controller-Sealed-Reveal" in entry.body for entry in channel.read_entries(root, name))


def test_disagreement_deliberates_then_converges_automatically(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(
        repo,
        sha,
        alice_sealed_decision="PASS",
        bob_sealed_decision="NO_PASS",
        bob_deliberation_decision="PASS",
    )
    open_brokered_thread(root, name, broker)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    first = run_once(config)
    assert channel.read_signal(root, name)["phase"] == "deliberation"
    assert len(channel.read_entries(root, name)) == 3
    assert any("votes disagree" in line for line in first)

    second = run_once(config)
    signal = channel.read_signal(root, name)
    assert signal["terminal_result"] == "PASS"
    assert signal["close_reason"] == "party-vote-agreement"
    assert any("to terminal" in line for line in second)


def test_supervisor_verdict_is_not_a_vote_and_affiliated_pass_cannot_replace_independent_vote(
    tmp_path: Path,
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(
        repo,
        sha,
        alice_sealed_decision="PASS",
        bob_sealed_decision="NO_PASS",
        bob_deliberation_decision="NO_PASS",
    )
    open_brokered_thread(root, name, broker)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )
    run_once(config)

    channel.post(
        root,
        "owner",
        "verdict",
        "review-one",
        "Supervisor says PASS, but this is not a party vote.",
        name=name,
    )

    assert channel.read_signal(root, name)["thread"] == "review-one"
    state = json.loads((broker.runtime_root / "cases" / "review-one" / "case.json").read_text(encoding="utf-8"))
    assert state["latest_votes"]["alice"]["decision"] == "PASS"
    assert state["latest_votes"]["bob"]["decision"] == "NO_PASS"
    assert set(state["latest_votes"]) == {"alice", "bob"}
    assert BrokerController(broker)._agreement(state) is None


def test_thread_cap_exhaustion_closes_no_pass(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo, thread_cap=4)
    broker = make_broker(
        repo,
        sha,
        thread_cap=4,
        alice_sealed_decision="PASS",
        bob_sealed_decision="NO_PASS",
        bob_deliberation_decision="NO_PASS",
    )
    open_brokered_thread(root, name, broker)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )
    run_once(config)
    run_once(config)

    signal = channel.read_signal(root, name)
    assert signal["terminal_result"] == "NO_PASS"
    assert signal["close_reason"] == "thread-cap-exhausted"
    assert len(channel.thread_entries(root, "review-one", name)) == 5, "typed close may follow the cap"


def test_verdict_without_typed_decision_is_refused_before_mailbox_write(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, bob_mode="missing-decision")
    open_brokered_thread(root, name, broker)

    with pytest.raises(AdapterError, match="verdict decision"):
        BrokerController(broker).capture_sealed(
            channel_root=root,
            channel_name=name,
            party="bob",
            thread="review-one",
            sequence=1,
            attempt=1,
        )

    assert len(channel.read_entries(root, name)) == 1


def test_broker_retry_exhaustion_closes_error_instead_of_escalating_to_human(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    open_brokered_thread(root, name, broker)
    state_path = broker.runtime_root / "watcher-state.json"
    state_path.write_text(
        json.dumps(
            {
                "last_mirrored_seq": 1,
                "invocations": {
                    "1": {"count": 2, "last_at": "2020-01-01T00:00:00+00:00"}
                },
                "escalated": [],
            }
        ),
        encoding="utf-8",
    )
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=state_path,
        broker=broker,
        retry_seconds=1,
    )

    output = run_once(config)

    signal = channel.read_signal(root, name)
    assert signal["terminal_result"] == "ERROR"
    assert signal["close_reason"] == "adapter-retries-exhausted"
    assert not any(line.startswith("ESCALATE:") for line in output)


def test_recurring_tick_repairs_case_state_after_terminal_channel_commit(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    open_brokered_thread(root, name, broker)
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )
    run_once(config)
    case_path = broker.runtime_root / "cases" / "review-one" / "case.json"
    stale = json.loads(case_path.read_text(encoding="utf-8"))
    stale["phase"] = "deliberation"
    stale.pop("terminal_result", None)
    stale.pop("close_reason", None)
    case_path.write_text(json.dumps(stale), encoding="utf-8")

    output = run_once(config)

    repaired = json.loads(case_path.read_text(encoding="utf-8"))
    assert repaired["phase"] == "terminal"
    assert repaired["terminal_result"] == "PASS"
    assert any("broker confirmed" in line for line in output)

    quiet = run_once(config)
    assert not any("broker confirmed" in line for line in quiet)


def test_expired_deadline_outranks_retry_exhaustion_close_reason(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, whole_case_timeout_seconds=5)
    opened_at = datetime.now(timezone.utc) - timedelta(seconds=10)
    BrokerController(broker, now=opened_at).open_case(
        channel_root=root,
        channel_name=name,
        thread="expired-and-retried",
        first_party="alice",
        body="Neutral docket.",
    )
    state_path = broker.runtime_root / "watcher-state.json"
    state_path.write_text(
        json.dumps(
            {
                "last_mirrored_seq": 1,
                "invocations": {
                    "1": {"count": 2, "last_at": "2020-01-01T00:00:00+00:00"}
                },
                "escalated": [],
            }
        ),
        encoding="utf-8",
    )
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=state_path,
        broker=broker,
        retry_seconds=1,
    )

    run_once(config)

    assert channel.read_signal(root, name)["close_reason"] == "case-deadline-expired"


def test_watch_status_reports_managed_terminal_surface_and_error_attention(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="status-error",
        first_party="alice",
        body="Neutral docket.",
    )
    controller.close_error(
        channel_root=root,
        channel_name=name,
        thread="status-error",
        close_reason="adapter-error",
    )
    config = WatcherConfig(
        channel_root=root,
        channel_name=name,
        state_path=broker.runtime_root / "watcher-state.json",
        broker=broker,
    )

    lines, result = read_status(config, datetime.now(timezone.utc))

    assert result.verdict == "ERROR"
    assert "status-error" in result.detail
    assert any("phase terminal" in line and "result ERROR" in line for line in lines)
    assert "ERROR" in _NEEDS_ATTENTION


# --- concurrent sealed capture (Slice A1) ------------------------------------

GOLDEN_SEALED_INSTRUCTIONS = (
    "Inspect the complete pinned source and docket. Write only the structured result file. "
    "Do not edit the source, do not access a Debate channel, and do not include private reasoning."
)


class AdapterCall(NamedTuple):
    party: str
    start: float
    end: float


class SealedRun(NamedTuple):
    elapsed: float
    outcome: DriveOutcome
    submissions: list[str]
    log: list[AdapterCall]
    signal: dict[str, object]
    parties: list[str]


def read_adapter_log(path: Path) -> list[AdapterCall]:
    """Every fake-adapter invocation, in completion order: party, start, end."""
    if not path.exists():
        return []
    calls: list[AdapterCall] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        calls.append(AdapterCall(str(raw["party"]), float(raw["start"]), float(raw["end"])))
    return calls


def sealed_submissions(broker: BrokerConfig, thread: str) -> dict[str, object]:
    """The case file's private submissions, round-tripped through JSON."""
    case = json.loads((broker.runtime_root / "cases" / thread / "case.json").read_text(encoding="utf-8"))
    submissions = case["sealed_submissions"]
    assert isinstance(submissions, dict)
    return {str(party): record for party, record in submissions.items()}


def stable_signal(signal: dict[str, object]) -> dict[str, object]:
    """The doorbell without the fields that differ between two wall-clock runs."""
    return {
        key: value
        for key, value in signal.items()
        if key != "deadline" and not key.endswith("_at") and not key.endswith("_ts")
    }


def drive_one_sealed_pair(base: Path, mode: str) -> SealedRun:
    """Open and drive one case to its terminal state; report what both modes share."""
    repo, sha = make_repository(base)
    root, name = make_channel(repo)
    log = base / "adapter-log.jsonl"
    broker = make_broker(
        repo,
        sha,
        alice_mode="slow",
        bob_mode="slow",
        alice_additions={"FAKE_LOG_PATH": str(log), "FAKE_SLEEP": "1.5"},
        bob_additions={"FAKE_LOG_PATH": str(log), "FAKE_SLEEP": "1.5"},
        sealed_concurrency=mode,
    )
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="paired-seal",
        first_party="alice",
        body="Neutral docket.",
    )
    started = time.monotonic()
    outcome = controller.drive_case(
        channel_root=root,
        channel_name=name,
        thread="paired-seal",
        sequence=1,
        attempt=1,
    )
    elapsed = time.monotonic() - started
    return SealedRun(
        elapsed=elapsed,
        outcome=outcome,
        submissions=sorted(sealed_submissions(broker, "paired-seal")),
        log=read_adapter_log(log),
        signal=stable_signal(channel.read_signal(root, name)),
        parties=sorted(
            entry.sender for entry in channel.read_entries(root, name) if entry.sender in broker.profiles
        ),
    )


def test_concurrent_sealed_capture_overlaps_and_records_what_the_sequential_run_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = channel.update_managed_phase
    signal_writes: list[tuple[str, str, str]] = []

    def counting(root: Path, **kwargs: object) -> None:
        signal_writes.append((str(kwargs["thread"]), str(kwargs["phase"]), str(kwargs["turn"])))
        original(root, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(channel, "update_managed_phase", counting)

    sequential = drive_one_sealed_pair(tmp_path / "sequential", "sequential")
    sequential_writes = list(signal_writes)
    signal_writes.clear()
    concurrent_run = drive_one_sealed_pair(tmp_path / "concurrent", "concurrent")
    concurrent_writes = list(signal_writes)

    sequential_log = {call.party: call for call in sequential.log}
    concurrent_log = {call.party: call for call in concurrent_run.log}
    assert sorted(sequential_log) == sorted(concurrent_log) == ["alice", "bob"]
    assert len(sequential.log) == len(concurrent_run.log) == 2

    assert concurrent_log["alice"].start < concurrent_log["bob"].end
    assert concurrent_log["bob"].start < concurrent_log["alice"].end
    assert concurrent_run.elapsed < 2.5

    assert min(call.end for call in sequential_log.values()) <= max(
        call.start for call in sequential_log.values()
    )
    assert sequential.elapsed >= 3.0

    assert concurrent_run.submissions == sequential.submissions == ["alice", "bob"]
    assert concurrent_run.parties == sequential.parties == ["alice", "bob"]
    assert concurrent_run.signal == sequential.signal
    assert concurrent_writes == sequential_writes
    assert concurrent_run.outcome.terminal_result == "PASS"


def test_concurrent_sealed_capture_keeps_the_survivor_and_retries_only_the_failing_seat(
    tmp_path: Path,
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    log = tmp_path / "adapter-log.jsonl"
    broker = make_broker(
        repo,
        sha,
        alice_mode="timeout",
        alice_timeout=1,
        alice_additions={"FAKE_LOG_PATH": str(log)},
        bob_additions={"FAKE_LOG_PATH": str(log)},
    )
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="half-seal",
        first_party="alice",
        body="Neutral docket.",
    )

    with pytest.raises(AdapterError, match="timed out after 1s") as caught:
        controller.drive_case(
            channel_root=root, channel_name=name, thread="half-seal", sequence=1, attempt=1
        )

    assert caught.value.retryable is True
    assert sorted(sealed_submissions(broker, "half-seal")) == ["bob"]
    assert [call.party for call in read_adapter_log(log)] == ["bob"]
    assert not any(entry.sender in broker.profiles for entry in channel.read_entries(root, name))
    assert channel.read_signal(root, name)["turn"] == "alice"

    with pytest.raises(AdapterError, match="timed out after 1s"):
        controller.drive_case(
            channel_root=root, channel_name=name, thread="half-seal", sequence=1, attempt=2
        )

    assert [call.party for call in read_adapter_log(log)] == ["bob"]
    assert sorted(path.name for path in broker.runtime_root.glob("cases/half-seal/invocations/*")) == [
        "1-alice-1",
        "1-alice-2",
        "1-bob-1",
    ]


def test_deadline_expiry_during_concurrent_capture_closes_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, whole_case_timeout_seconds=5)
    opened_at = datetime(2026, 8, 20, 12, 0, tzinfo=timezone.utc)
    controller = BrokerController(broker, now=opened_at)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="expires-concurrently",
        first_party="alice",
        body="Neutral docket.",
    )
    invoked: list[str] = []

    def finish_after_deadline(**kwargs: object) -> tuple[AdapterResult, dict[str, str | Path]]:
        invoked.append(str(kwargs["party"]))
        controller._fixed_now = opened_at + timedelta(seconds=6)
        return (
            AdapterResult("verdict", "late", "", "", "fixture", "PASS"),
            {
                "input_sha256": "1" * 64,
                "source_manifest_sha256": "2" * 64,
                "docket_revision_sha256": "3" * 64,
                "diagnostics_root": broker.runtime_root,
            },
        )

    monkeypatch.setattr(controller, "_invoke", finish_after_deadline)
    outcome = controller.drive_case(
        channel_root=root, channel_name=name, thread="expires-concurrently", sequence=1, attempt=1
    )

    assert sorted(invoked) == ["alice", "bob"]
    assert outcome.terminal_result == "ERROR"
    assert outcome.close_reason == "case-deadline-expired"
    assert channel.read_signal(root, name)["close_reason"] == "case-deadline-expired"
    assert sealed_submissions(broker, "expires-concurrently") == {}
    assert not any(entry.sender in broker.profiles for entry in channel.read_entries(root, name))


def test_concurrent_mode_does_not_reinvoke_an_already_sealed_seat(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    log = tmp_path / "adapter-log.jsonl"
    broker = make_broker(
        repo,
        sha,
        alice_additions={"FAKE_LOG_PATH": str(log)},
        bob_additions={"FAKE_LOG_PATH": str(log)},
    )
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="one-left",
        first_party="bob",
        body="Neutral docket.",
    )
    controller.capture_sealed(
        channel_root=root, channel_name=name, party="bob", thread="one-left", sequence=1, attempt=1
    )

    outcome = controller.drive_case(
        channel_root=root, channel_name=name, thread="one-left", sequence=1, attempt=1
    )

    assert outcome.terminal_result == "PASS"
    assert sorted(call.party for call in read_adapter_log(log)) == ["alice", "bob"]
    assert sorted(path.name for path in broker.runtime_root.glob("cases/one-left/invocations/*")) == [
        "1-alice-1",
        "1-bob-1",
    ]


def test_sealed_worker_threads_never_write_case_state_or_the_doorbell(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, alice_mode="slow", bob_mode="slow")
    controller = BrokerController(broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="main-thread-only",
        first_party="alice",
        body="Neutral docket.",
    )
    original_write = BrokerController._write_case
    original_phase = channel.update_managed_phase
    off_thread: list[str] = []

    def guarded_write(self: BrokerController, thread: str, state: dict[str, object]) -> None:
        if threading.current_thread() is not threading.main_thread():
            off_thread.append(f"_write_case from {threading.current_thread().name}")
        original_write(self, thread, state)

    def guarded_phase(signal_root: Path, **kwargs: object) -> None:
        if threading.current_thread() is not threading.main_thread():
            off_thread.append(f"update_managed_phase from {threading.current_thread().name}")
        original_phase(signal_root, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(BrokerController, "_write_case", guarded_write)
    monkeypatch.setattr(channel, "update_managed_phase", guarded_phase)

    outcome = controller.drive_case(
        channel_root=root, channel_name=name, thread="main-thread-only", sequence=1, attempt=1
    )

    assert off_thread == []
    assert outcome.terminal_result == "PASS"


def test_sealed_adapter_input_matches_its_golden_payload(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)
    broker = make_broker(repo, sha)
    controller = BrokerController(broker)
    exports, docket, _ = controller._prepare_case("golden-case")
    result_path = broker.runtime_root / "cases" / "golden-case" / "invocations" / "1-bob-1" / "result.json"

    payload = controller.render_input(
        party="bob",
        phase="sealed",
        thread="golden-case",
        result_path=result_path,
        source=exports["bob"],
        docket=docket,
        transcript=None,
    )

    encoded = json.dumps(payload, indent=2, sort_keys=True)
    for actual, token in (
        (str(broker.runtime_root), "<runtime>"),
        (sha, "<ref>"),
        (docket.revision_sha256, "<docket>"),
        (exports["bob"].manifest_sha256, "<manifest>"),
    ):
        encoded = encoded.replace(actual, token)

    assert json.loads(encoded) == {
        "schema_version": 1,
        "phase": "sealed",
        "thread": "golden-case",
        "seat": {
            "party": "bob",
            "author_relationship": "author-independent",
            "topology": "minimum-two-agent",
        },
        "source": {
            "root": "<runtime>/exports/<ref>/bob",
            "ref": "<ref>",
            "manifest_sha256": "<manifest>",
        },
        "docket": {
            "root": "<runtime>/dockets/<docket>/files",
            "revision_sha256": "<docket>",
            "files": [
                {
                    "path": "docs/plans/superseded.md",
                    "sha256": "502eeaef8517a63609f685ffc40690a6cc9aa980ad8fb673523ffbab2c0b81cf",
                    "tracked_at_source_ref": False,
                },
                {
                    "path": "watcher.json",
                    "sha256": "9eb2269e11d0a83c051255203611b6d9a9bb3ead51c72e0429fb8f44df528846",
                    "tracked_at_source_ref": False,
                },
            ],
        },
        "result": {
            "path": "<runtime>/cases/golden-case/invocations/1-bob-1/result.json",
            "schema_version": 1,
            "controller_owned_fields": ["sender"],
            "required_fields": [
                "schema_version",
                "entry_type",
                "body",
                "runtime_model",
                "decision (PASS or NO_PASS for verdicts)",
            ],
        },
        "instructions": GOLDEN_SEALED_INSTRUCTIONS,
    }
    assert set(payload) == {
        "schema_version",
        "phase",
        "thread",
        "seat",
        "source",
        "docket",
        "result",
        "instructions",
    }
    assert payload["instructions"] == GOLDEN_SEALED_INSTRUCTIONS
    assert "current_thread" not in payload


def test_doctor_reports_the_sealed_invocation_mode(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)

    assert "sealed invocations: concurrent" in doctor_lines(make_broker(repo, sha))
    assert "sealed invocations: sequential" in doctor_lines(
        make_broker(repo, sha, sealed_concurrency="sequential")
    )


def test_a_sealed_concurrency_value_outside_the_two_modes_is_refused(tmp_path: Path) -> None:
    repo, sha = make_repository(tmp_path)

    with pytest.raises(channel.ChannelError, match="sealed_concurrency"):
        make_broker(repo, sha, sealed_concurrency="maybe")


# --- final review wave I2: a timed-out adapter takes its children with it ----


@pytest.mark.skipif(os.name == "nt", reason="process groups are a POSIX facility")
def test_a_timed_out_adapter_leaves_no_child_process_behind(tmp_path: Path) -> None:
    """A vendor CLI spawns children of its own; killing only the process the
    controller launched left them running long past the case deadline, burning
    tokens against a case nobody is waiting for (final review wave, I2)."""
    import time as time_module

    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, alice_timeout=1)
    pids_path = tmp_path / "pids.json"
    hanging = AdapterProfile(
        **{
            **broker.profiles["alice"].__dict__,
            "environment": {
                **broker.profiles["alice"].environment,
                "FAKE_MODE": "orphan",
                "FAKE_PIDS_PATH": str(pids_path),
            },
            "environment_allowlist": ("PATH",),
        }
    )
    profiles = {**broker.profiles, "alice": hanging}
    hanging_broker = BrokerConfig(
        repository_root=broker.repository_root,
        runtime_root=broker.runtime_root,
        source_ref=broker.source_ref,
        profiles=profiles,
        timing=TimingPolicy(
            thread_cap=12,
            scheduler_interval_seconds=60,
            retry_seconds=120,
            whole_case_timeout_seconds=900,
            profiles=(profiles["alice"], profiles["bob"]),
        ),
        config_sha256=broker.config_sha256,
        docket_files=broker.docket_files,
        sealed_concurrency="sequential",
    )
    controller = BrokerController(hanging_broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="orphan-case",
        first_party="alice",
        body="Neutral docket.",
    )
    with pytest.raises(AdapterError, match="timed out after 1s"):
        controller.drive_case(
            channel_root=root,
            channel_name=name,
            thread="orphan-case",
            sequence=1,
            attempt=1,
        )

    pids = json.loads(pids_path.read_text(encoding="utf-8"))

    def _alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:  # pragma: no cover - a reused pid we do not own
            return True
        return True

    deadline = time_module.monotonic() + 10.0
    while time_module.monotonic() < deadline:
        if not _alive(int(pids["adapter"])) and not _alive(int(pids["child"])):
            break
        time_module.sleep(0.05)
    assert not _alive(int(pids["adapter"])), "the adapter itself outlived its timeout"
    assert not _alive(int(pids["child"])), "the adapter's own child outlived the timeout"


# --- final review wave M6: the concurrent capture's precondition, checked ----


def test_the_concurrent_sealed_capture_refuses_when_the_case_is_not_prepared(
    tmp_path: Path,
) -> None:
    """Both workers only ever VERIFY the pinned export and review material;
    creating them is the driving thread's job, done once before either worker
    starts. If they are not there, two threads would race to write the same
    paths, so this refuses instead (final review wave, M6)."""
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, sealed_concurrency="concurrent")
    controller = BrokerController(broker)
    open_brokered_thread(root, name, broker)
    (broker.runtime_root / "exports").rename(broker.runtime_root / "exports-elsewhere")
    with pytest.raises(channel.ChannelError, match="before both seats are called"):
        controller._capture_sealed_pair(
            channel_root=root,
            channel_name=name,
            thread="review-one",
            order=("alice", "bob"),
            sequence=1,
            attempt=1,
        )
    assert len(channel.read_entries(root, name)) == 1


@pytest.mark.skipif(os.name == "nt", reason="process groups are a POSIX facility")
def test_an_interrupted_seat_call_leaves_no_child_process_behind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ctrl-C is not a timeout, and it does not reach the adapter either.

    Running the adapter in a session of its own (so a timeout can kill its whole
    tree) also puts it OUTSIDE the terminal's process group, so the interrupt
    the operator typed never lands on it -- and `Popen.__exit__` only waits.
    Every way out of the wait must therefore end the tree, not just the timeout
    (re-review of the wave). The exception is re-raised untouched.
    """
    import time as time_module

    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    broker = make_broker(repo, sha, alice_timeout=30)
    pids_path = tmp_path / "pids.json"
    hanging = AdapterProfile(
        **{
            **broker.profiles["alice"].__dict__,
            "environment": {
                **broker.profiles["alice"].environment,
                "FAKE_MODE": "orphan",
                "FAKE_PIDS_PATH": str(pids_path),
            },
            "environment_allowlist": ("PATH",),
        }
    )
    profiles = {**broker.profiles, "alice": hanging}
    hanging_broker = BrokerConfig(
        repository_root=broker.repository_root,
        runtime_root=broker.runtime_root,
        source_ref=broker.source_ref,
        profiles=profiles,
        timing=TimingPolicy(
            thread_cap=12,
            scheduler_interval_seconds=60,
            retry_seconds=120,
            whole_case_timeout_seconds=900,
            profiles=(profiles["alice"], profiles["bob"]),
        ),
        config_sha256=broker.config_sha256,
        docket_files=broker.docket_files,
        sealed_concurrency="sequential",
    )
    controller = BrokerController(hanging_broker)
    controller.open_case(
        channel_root=root,
        channel_name=name,
        thread="interrupted-case",
        first_party="alice",
        body="Neutral docket.",
    )

    # Ctrl-C, delivered exactly where the operator's would land: inside the
    # wait, once the adapter has started a child of its own. Only the adapter's
    # own wait is interrupted -- git and every other subprocess is untouched.
    real_communicate = subprocess.Popen.communicate

    def interrupted(
        self: "subprocess.Popen[Any]", input: Any = None, timeout: float | None = None
    ) -> Any:
        arguments = self.args if isinstance(self.args, (list, tuple)) else [self.args]
        if not any("fake_adapter.py" in str(part) for part in arguments):
            return real_communicate(self, input, timeout)
        deadline = time_module.monotonic() + 10.0
        while not pids_path.exists() and time_module.monotonic() < deadline:
            time_module.sleep(0.02)
        raise KeyboardInterrupt

    monkeypatch.setattr(subprocess.Popen, "communicate", interrupted)

    with pytest.raises(KeyboardInterrupt):
        controller.drive_case(
            channel_root=root,
            channel_name=name,
            thread="interrupted-case",
            sequence=1,
            attempt=1,
        )

    pids = json.loads(pids_path.read_text(encoding="utf-8"))

    def _alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:  # pragma: no cover - a reused pid we do not own
            return True
        return True

    deadline = time_module.monotonic() + 10.0
    while time_module.monotonic() < deadline:
        if not _alive(int(pids["adapter"])) and not _alive(int(pids["child"])):
            break
        time_module.sleep(0.05)
    assert not _alive(int(pids["adapter"])), "the adapter itself outlived the interrupt"
    assert not _alive(int(pids["child"])), "the adapter's own child outlived the interrupt"
    assert len(channel.read_entries(root, name)) == 1
