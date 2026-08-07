from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from debate import channel
from debate.controller import (
    AdapterProfile,
    BrokerConfig,
    BrokerController,
    TimingPolicy,
    create_source_export,
    doctor_lines,
    materialize_docket,
)
from debate.__main__ import main
from debate.watcher import WatcherConfig, run_once


FAKE_ADAPTER = r"""
import json
import os
from pathlib import Path
import sys

input_path = Path(sys.argv[1])
result_path = Path(sys.argv[2])
payload = json.loads(input_path.read_text(encoding="utf-8"))
mode = os.environ.get("FAKE_MODE", "good")
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
}
if mode == "wrong-sender":
    result["sender"] = "intruder"
result_path.write_text(json.dumps(result), encoding="utf-8")
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
) -> AdapterProfile:
    environment = {"FAKE_MODE": mode, "RUNTIME_MODEL": f"{party}-runtime-1", **(additions or {})}
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
    bob_mode: str = "good",
    bob_additions: dict[str, str] | None = None,
    canaries: dict[str, str] | None = None,
    config_sha256: str = "a" * 64,
) -> BrokerConfig:
    profiles = {
        "alice": make_profile("alice", alice_relationship),
        "bob": make_profile("bob", bob_relationship, mode=bob_mode, additions=bob_additions),
    }
    timing = TimingPolicy(
        thread_cap=12,
        scheduler_interval_seconds=60,
        retry_seconds=120,
        whole_case_timeout_seconds=900,
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
    )


def make_channel(repo: Path) -> tuple[Path, str]:
    root = repo / "collab"
    name = "fixture-11111"
    channel.init_channel(
        root,
        ("alice", "bob"),
        "owner",
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
    assert "opened brokered case as MSG-1" in capsys.readouterr().out
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
    assert len(entries) == 2
    assert entries[1].sender == "bob"
    assert "fresh fake review" in entries[1].body
    assert "Controller-Provenance:" in entries[1].body
    assert broker.profile_hashes["bob"] in entries[1].body
    assert sha in entries[1].body
    assert "bob-runtime-1" in entries[1].body
    assert "Structured appendix." in entries[1].body
    assert any("brokered bob" in line for line in output)

    invocation = next((broker.runtime_root / "cases" / "review-one" / "invocations").iterdir())
    payload = json.loads((invocation / "input.json").read_text(encoding="utf-8"))
    assert str(root.resolve()) not in json.dumps(payload)
    assert "current_thread" in payload
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
