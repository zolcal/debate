"""Onboarding inspect/approve and the brokered product open (plan Slice 1B).

Discovery is neutralized by pointing PATH at an empty directory, so the
catalog finds nothing and the fixtures own every candidate. Fake seats use
absolute command heads (/bin/sh, python3) that resolve without PATH.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Any

import pytest



from debate import channel, onboarding, opening, seats
from debate.__main__ import _watcher_config

def _hermetic_path() -> str:
    """Discovery must find no agent CLIs. POSIX keeps the literal system
    dirs; Windows substitutes git's own directory (git shims and nothing
    else), because /usr/bin does not exist there and the fixtures' git
    subprocesses still need to resolve (field finding F25)."""
    if os.name == "nt":
        git = shutil.which("git")
        return str(Path(git).parent) if git else ""
    return "/usr/bin:/bin"


NOW = "2026-08-19T12:00:00+00:00"
REVIEW_CONTRACT: dict[str, Any] = {
    "goal": "Establish whether the fixture satisfies its recorded criterion.",
    "review_domain": "The pinned fixture source and docket.",
    "stop_rule": "Stop after the bounded checks and a decisive verdict.",
}


def _write_registry(path: Path, seats_obj: dict[str, object]) -> None:
    from debate import __version__

    payload = {
        "registry_version": 1,
        "tool_version": __version__,
        "discovered_at": NOW,
        "seats": seats_obj,
        "last_pair": {},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def _seat(command: list[str], *, vendor: str | None = None, submodel: str = "fake", cost_mode: str = "unknown") -> dict[str, object]:
    return {
        "cost_mode": cost_mode,
        "vendor": vendor if vendor is not None else command[0].rsplit("/", 1)[-1],
        "submodel": submodel,
        "effort": None,
        "commands": [command],
        "source": "manual",
        "present": True,
        "smoke": None,
        "verification_argv": [],
        "verification_basis": "declared",
        "result_schema_version": 2,
    }


def _snapshot(root: Path) -> list[tuple[str, float, int]]:
    return [
        (str(p), p.stat().st_mtime, p.stat().st_size if p.is_file() else -1)
        for p in sorted(root.rglob("*"))
    ]


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    registry = tmp_path / "config" / "seats.json"
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry))
    # System dirs keep git/sh available while excluding the user-level agent
    # CLIs (~/.local/bin), so catalog discovery finds nothing it can seat.
    monkeypatch.setenv("PATH", _hermetic_path())
    return registry, project


def test_inspect_is_read_only_and_labels_existing(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    registry, project = isolated
    _write_registry(registry, {"probe/fake": _seat([sys.executable, "{prompt}"])})
    before = _snapshot(tmp_path)
    report = onboarding.inspect(str(project), now=NOW)
    assert _snapshot(tmp_path) == before
    candidates = report["candidates"]
    assert isinstance(candidates, list) and len(candidates) == 1
    row = candidates[0]
    assert isinstance(row, dict)
    assert row["seat_id"] == "probe/fake"
    assert row["existing"] is True
    assert row["present"] is True
    revision = report["candidate_revision"]
    assert isinstance(revision, str) and len(revision) == 64
    # Deterministic: a second scan of the unchanged world gives the same revision.
    assert onboarding.inspect(str(project), now="2026-08-19T13:00:00+00:00")[
        "candidate_revision"
    ] == revision


def test_manual_bridge_seat_is_addable(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """A brokered bridge command ({input_path}/{result_path}, no {prompt})
    is a legal manual seat -- Slice 2 acceptance seeds fake seats this way."""
    registry = seats.Registry()
    script = _fake_adapter_script(tmp_path, "gamma")
    seats.add_seat(
        registry, "gamma/fake",
        f"{sys.executable} {script} {{input_path}} {{result_path}}",
    )
    assert registry.seats["gamma/fake"].source == "manual"
    with pytest.raises(channel.ChannelError, match="marker"):
        seats.add_seat(registry, "delta/fake", f'"{sys.executable}" -c pass')


def test_inspect_fresh_machine_has_no_candidates(isolated: tuple[Path, Path]) -> None:
    _, project = isolated
    report = onboarding.inspect(str(project), now=NOW)
    assert report["candidates"] == []
    assert report["existing_registry_state"] == "missing"


def test_approve_requires_confirmed_and_nonempty(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, {"probe/fake": _seat([sys.executable, "{prompt}"])})
    report = onboarding.inspect(str(project), now=NOW)
    revision = str(report["candidate_revision"])
    with pytest.raises(channel.ChannelError, match="--confirmed"):
        onboarding.approve(
            str(project), allow=["probe/fake"], candidate_revision=revision,
            confirmed=False, now=NOW,
        )
    with pytest.raises(channel.ChannelError, match="zero selected"):
        onboarding.approve(
            str(project), allow=[], candidate_revision=revision, confirmed=True, now=NOW,
        )


def test_approve_revision_mismatch_is_refused(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, {"probe/fake": _seat([sys.executable, "{prompt}"])})
    with pytest.raises(channel.ChannelError, match="candidate set changed"):
        onboarding.approve(
            str(project), allow=["probe/fake"], candidate_revision="0" * 64,
            confirmed=True, now=NOW,
        )


def test_approve_writes_both_files_and_status_reports_ready(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(registry, {"probe/fake": _seat([sys.executable, "{prompt}"])})
    report = onboarding.inspect(str(project), now=NOW)
    after = onboarding.approve(
        str(project), allow=["probe/fake"],
        candidate_revision=str(report["candidate_revision"]),
        confirmed=True, now=NOW,
    )
    assert after["profile_state"] == "approved"
    assert after["attention"] == "ready"
    profile = json.loads((project / "debate-profile.json").read_text(encoding="utf-8"))
    assert profile == {"profile_version": 1, "allowlist": ["probe/fake"]}
    saved = json.loads(registry.read_text(encoding="utf-8"))
    assert "probe/fake" in saved["seats"]


def test_approve_refuses_unknown_and_unrunnable_seats(isolated: tuple[Path, Path]) -> None:
    registry, project = isolated
    _write_registry(
        registry,
        {
            "probe/fake": _seat([sys.executable, "{prompt}"]),
            "gone/fake": _seat(["/nonexistent/debate-test-binary", "{prompt}"]),
        },
    )
    report = onboarding.inspect(str(project), now=NOW)
    revision = str(report["candidate_revision"])
    with pytest.raises(channel.ChannelError, match="not a detected candidate"):
        onboarding.approve(
            str(project), allow=["never/seen"], candidate_revision=revision,
            confirmed=True, now=NOW,
        )
    with pytest.raises(channel.ChannelError, match="not currently runnable"):
        onboarding.approve(
            str(project), allow=["gone/fake"], candidate_revision=revision,
            confirmed=True, now=NOW,
        )


def test_approve_transaction_failure_leaves_both_files_byte_identical(
    isolated: tuple[Path, Path],
) -> None:
    registry, project = isolated
    _write_registry(registry, {"probe/fake": _seat([sys.executable, "{prompt}"])})
    (project / "debate-profile.json").write_text(
        json.dumps({"profile_version": 1, "allowlist": ["probe/fake"]}) + "\n",
        encoding="utf-8",
    )
    registry_before = registry.read_bytes()
    profile_before = (project / "debate-profile.json").read_bytes()
    report = onboarding.inspect(str(project), now=NOW)
    project.chmod(stat.S_IRUSR | stat.S_IXUSR)  # profile temp creation will fail
    try:
        with pytest.raises(channel.ChannelError, match="approval write failed"):
            onboarding.approve(
                str(project), allow=["probe/fake"],
                candidate_revision=str(report["candidate_revision"]),
                confirmed=True, now=NOW,
            )
    finally:
        project.chmod(stat.S_IRWXU)
    assert registry.read_bytes() == registry_before
    assert (project / "debate-profile.json").read_bytes() == profile_before
    leftovers = [p for p in registry.parent.iterdir() if p.name.startswith(".debate-")]
    assert leftovers == []


# --- the brokered product open ----------------------------------------------


def _fake_adapter_script(tmp_path: Path, name: str) -> Path:
    script = tmp_path / f"{name}.py"
    script.write_text(
        "import json, sys\n"
        "result = {\n"
        "    'schema_version': 2,\n"
        "    'entry_type': 'verdict',\n"
        "    'decision': 'PASS',\n"
        f"    'body': 'stub verdict from {name}: PASS on own reading',\n"
        f"    'runtime_model': '{name}-model',\n"
        "    'verification': {'status': 'performed', 'items': [\n"
        "        {'command': 'python fixture probe', 'exit_status': 0, 'output': 'fixture passed'}\n"
        "    ]},\n"
        "}\n"
        "with open(sys.argv[2], 'w', encoding='utf-8') as handle:\n"
        "    json.dump(result, handle)\n",
        encoding="utf-8",
    )
    return script


def _brokered_registry(registry: Path, tmp_path: Path) -> None:
    _write_registry(
        registry,
        {
            "alpha/fake": _seat(
                [sys.executable, str(_fake_adapter_script(tmp_path, "alpha")),
                 "{input_path}", "{result_path}"],
                vendor="alpha", cost_mode="local",
            ),
            "beta/fake": _seat(
                [sys.executable, str(_fake_adapter_script(tmp_path, "beta")),
                 "{input_path}", "{result_path}"],
                vendor="beta", cost_mode="local",
            ),
        },
    )


def _git_project(project: Path) -> None:
    import subprocess

    subprocess.run(["git", "init", "-q", str(project)], check=True)
    (project / "README").write_text("stub\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(project), "-c", "user.email=t@t", "-c", "user.name=t",
         "add", "README"], check=True,
    )
    subprocess.run(
        ["git", "-C", str(project), "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-qm", "stub"], check=True,
    )


def _head(project: Path) -> str:
    import subprocess

    return subprocess.run(
        ["git", "-C", str(project), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def test_brokered_open_refuses_without_profile(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"), source_ref=_head(project), author_vendor="claude",
        **REVIEW_CONTRACT,
    )
    with pytest.raises(channel.ChannelError, match="no approved seats"):
        opening.open_debate_brokered(
            spec, seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )
    assert not root.exists() or list(root.iterdir()) == []


def _approve_all(project: Path) -> None:
    report = onboarding.inspect(str(project), now=NOW)
    onboarding.approve(
        str(project), allow=["alpha/fake", "beta/fake"],
        candidate_revision=str(report["candidate_revision"]), confirmed=True, now=NOW,
    )


def test_brokered_open_identity_guard(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "alpha/fake"), source_ref=_head(project), author_vendor="claude",
        **REVIEW_CONTRACT,
    )
    with pytest.raises(channel.ChannelError, match="same seat twice"):
        opening.open_debate_brokered(
            spec, seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )
    assert not root.exists() or list(root.iterdir()) == []


def test_brokered_open_refuses_prompt_style_seats(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """Slice C5 moved this refusal: a seat that only takes a question text is
    now wrapped and admitted, but ONLY with its verified isolation and
    no-history settings on record. This one has neither, so it is refused --
    at the admission rule, before anything else looks at the pair."""
    registry, project = isolated
    _write_registry(
        registry,
        {
            # Explicit vendors: both heads are sys.executable (portable fake
            # seats), and the derived-vendor default would trip the
            # identical-weights guard before the refusal under test.
            "alpha/fake": _seat([sys.executable, "{prompt}"], vendor="alpha"),
            "beta/fake": _seat(
                [sys.executable, str(_fake_adapter_script(tmp_path, "beta")),
                 "{input_path}", "{result_path}"],
                vendor="beta",
            ),
        },
    )
    _git_project(project)
    report = onboarding.inspect(str(project), now=NOW)
    onboarding.approve(
        str(project), allow=["alpha/fake", "beta/fake"],
        candidate_revision=str(report["candidate_revision"]), confirmed=True, now=NOW,
    )
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"), source_ref=_head(project), author_vendor="claude",
        **REVIEW_CONTRACT,
    )
    with pytest.raises(channel.ChannelError, match="isolated mode a managed debate needs"):
        opening.open_debate_brokered(
            spec, seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )
    assert not root.exists() or list(root.iterdir()) == []


def test_brokered_open_mints_managed_v2_with_provenance(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"), source_ref=_head(project), author_vendor="claude",
        **REVIEW_CONTRACT,
    )
    live_registry = seats.load_registry()
    result = opening.open_debate_brokered(
        spec, live_registry, load_config_fn=_watcher_config, now=NOW, tool_version="test",
    )
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    assert record["managed_version"] == 2
    assert record["supervisor"] == "owner"
    parties = record["parties"]
    assert sorted(parties) == sorted(record["seats"].keys() - {"picked_at", "tool_version"})
    for party in parties:
        block = record["seats"][party]
        assert block["author_relationship"] == "author-independent"
        assert block["provider"] and block["requested_model"]
        assert block["cost_mode"] == "local"
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    assert set(config["adapters"]) == set(parties)
    assert config["source_ref"] == spec.source_ref
    assert live_registry.last_pair[opening.project_key(root)] == ["alpha/fake", "beta/fake"]


def test_author_vendor_derives_the_recorded_relationship(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    """A seat sharing the declared author vendor is recorded
    author-affiliated; the relationship is derived from a declaration,
    never guessed (branch-gate round-1 finding)."""
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"),
        source_ref=_head(project), author_vendor="alpha",
        **REVIEW_CONTRACT,
    )
    result = opening.open_debate_brokered(
        spec, seats.load_registry(), load_config_fn=_watcher_config,
        now=NOW, tool_version="test",
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    relationships = {
        party: config["adapters"][party]["author_relationship"]
        for party in record["parties"]
    }
    assert relationships["alpha"] == "author-affiliated"
    assert relationships["beta"] == "author-independent"
    assert record["seats"]["alpha"]["author_relationship"] == "author-affiliated"
    with pytest.raises(channel.ChannelError, match="author-vendor"):
        opening.open_debate_brokered(
            opening.BrokeredOpenSpec(
                root=project / "collab2", label="stub", pair=("alpha/fake", "beta/fake"),
                source_ref=_head(project), author_vendor="  ",
                **REVIEW_CONTRACT,
            ),
            seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )


def test_padded_author_vendor_still_matches_and_typo_is_refused(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    """Round-2 findings: ' alpha ' must record the alpha seat as
    author-affiliated (normalization, codex MSG-7), and an unknown vendor
    refuses instead of silently degrading to author-independent (opus S3)."""
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=root, label="stub", pair=("alpha/fake", "beta/fake"),
            source_ref=_head(project), author_vendor=" Alpha ",
            **REVIEW_CONTRACT,
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=NOW, tool_version="test",
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    assert config["adapters"]["alpha"]["author_relationship"] == "author-affiliated"
    root2 = project / "collab2"
    with pytest.raises(channel.ChannelError, match="matches no catalog or"):
        opening.open_debate_brokered(
            opening.BrokeredOpenSpec(
                root=root2, label="stub", pair=("alpha/fake", "beta/fake"),
                source_ref=_head(project), author_vendor="clade",
                **REVIEW_CONTRACT,
            ),
            seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )
    assert not root2.exists() or list(root2.iterdir()) == []


def test_cli_brokered_open_requires_author_vendor(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    from debate.__main__ import main

    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    rc = main([
        "open", "--brokered", "--root", str(project / "collab"),
        "--label", "stub", "--pair", "alpha/fake,beta/fake",
    ])
    assert rc != 0  # ChannelError -> refused, nonzero exit


def test_approved_profile_is_world_readable(isolated: tuple[Path, Path]) -> None:
    """The profile is a COMMITTABLE project file: 0644, not mkstemp's 0600."""
    registry, project = isolated
    _write_registry(registry, {"probe/fake": _seat([sys.executable, "{prompt}"])})
    report = onboarding.inspect(str(project), now=NOW)
    onboarding.approve(
        str(project), allow=["probe/fake"],
        candidate_revision=str(report["candidate_revision"]), confirmed=True, now=NOW,
    )
    mode = (project / "debate-profile.json").stat().st_mode & 0o777
    assert mode == 0o644


def test_cost_mode_declaration_paths(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """seats add --cost-mode declares on creation; the append path APPLIES a
    non-unknown declaration (round-2: silent no-op refused); set_cost_mode
    declares for ANY existing seat; smoke confirmation names the cost."""
    registry = seats.Registry()
    script = _fake_adapter_script(tmp_path, "delta")
    seats.add_seat(
        registry, "delta/fake",
        f"{sys.executable} {script} {{input_path}} {{result_path}}",
        cost_mode="local",
    )
    assert registry.seats["delta/fake"].cost_mode == "local"
    seats.add_seat(
        registry, "delta/fake",
        f"{sys.executable} {script} extra {{input_path}} {{result_path}}",
        cost_mode="subscription",
    )
    assert registry.seats["delta/fake"].cost_mode == "subscription"  # applied, not ignored
    seats.set_cost_mode(registry, "delta/fake", "api")
    assert registry.seats["delta/fake"].cost_mode == "api"
    with pytest.raises(channel.ChannelError, match="cost_mode"):
        seats.set_cost_mode(registry, "delta/fake", "free")
    with pytest.raises(channel.ChannelError, match="no seat"):
        seats.set_cost_mode(registry, "missing/seat", "local")
    prompts: list[str] = []

    def deny(prompt: str) -> str:
        prompts.append(prompt)
        return "n"

    with pytest.raises(channel.ChannelError, match="not confirmed"):
        seats.smoke_seat(registry, "delta/fake", now=NOW, ask=deny)
    assert prompts and "cost mode: api" in prompts[0]


def test_v1_open_refuses_bridge_seats(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """The symmetric guard: the legacy v1 open refuses brokered bridges (no
    {prompt}) exactly as the brokered open refuses prompt-style seats --
    found live when a weak model took the legacy path with bridge seats."""
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    spec = opening.OpenSpec(root=root, label="stub", pair=("alpha/fake", "beta/fake"))
    with pytest.raises(channel.ChannelError, match="nowhere to put the question text"):
        opening.open_debate(
            spec, seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )
    assert not root.exists() or list(root.iterdir()) == []


def test_brokered_open_docket_files_snapshot_and_prewrite_refusal(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    missing = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"),
        source_ref=_head(project), author_vendor="claude", docket_files=("no-such-file.md",),
        **REVIEW_CONTRACT,
    )
    with pytest.raises(channel.ChannelError, match="docket file"):
        opening.open_debate_brokered(
            missing, seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test",
        )
    assert not root.exists() or list(root.iterdir()) == []
    good = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"),
        source_ref=_head(project), author_vendor="claude", docket_files=("README",),
        **REVIEW_CONTRACT,
    )
    result = opening.open_debate_brokered(
        good, seats.load_registry(), load_config_fn=_watcher_config,
        now=NOW, tool_version="test",
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    assert config["docket_files"] == ["README"]


def test_docket_file_escapes_are_refused_pre_write(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    """Round-3 finding (codex MSG-11): an absolute docket path or a ../
    traversal must refuse BEFORE any target write -- pathlib joins an
    absolute path by replacing the base, and the controller's later refusal
    would land after the channel exists."""
    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    outside = tmp_path / "outside.md"
    outside.write_text("outside the project\n", encoding="utf-8")
    root = project / "collab"
    for bad in (str(outside), "../outside.md"):
        with pytest.raises(channel.ChannelError, match="project-relative|escapes the project"):
            opening.open_debate_brokered(
                opening.BrokeredOpenSpec(
                    root=root, label="stub", pair=("alpha/fake", "beta/fake"),
                    source_ref=_head(project), author_vendor="claude",
                    docket_files=(bad,),
                    **REVIEW_CONTRACT,
                ),
                seats.load_registry(), load_config_fn=_watcher_config,
                now=NOW, tool_version="test",
            )
        assert not root.exists() or list(root.iterdir()) == []


def test_cli_set_cost_mode_wiring(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """Opus round-3 observation 2: the argparse wiring itself."""
    from debate.__main__ import main

    registry, _ = isolated
    _brokered_registry(registry, tmp_path)
    rc = main(["seats", "set-cost-mode", "alpha/fake", "subscription"])
    assert rc == 0
    assert seats.load_registry().seats["alpha/fake"].cost_mode == "subscription"


def test_add_seat_append_validates_cost_mode(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """Opus round-3 observation 1: the append path validates cost_mode too."""
    registry = seats.Registry()
    script = _fake_adapter_script(tmp_path, "epsilon")
    seats.add_seat(
        registry, "epsilon/fake",
        f"{sys.executable} {script} {{input_path}} {{result_path}}",
    )
    with pytest.raises(channel.ChannelError, match="cost_mode"):
        seats.add_seat(
            registry, "epsilon/fake",
            f"{sys.executable} {script} more {{input_path}} {{result_path}}",
            cost_mode="gratis",
        )


def test_concurrent_smoke_results_both_survive(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    """Field finding (2026-08-20): two concurrent `seats smoke` processes each
    held a stale in-memory registry and the LAST save clobbered the other's
    result. update_registry applies only the observed result to a fresh load
    under a lock, so both survive the exact interleaving that lost one."""
    registry, _ = isolated
    _brokered_registry(registry, tmp_path)

    # Process A loads its stale snapshot...
    stale_snapshot = seats.load_registry()
    smoke_a = seats.SmokeStatus(at=NOW, result="pass")
    stale_snapshot.seats["alpha/fake"].smoke = smoke_a
    # ...meanwhile process B records beta's result through the locked path.
    smoke_b = seats.SmokeStatus(at=NOW, result="pass")

    def apply_b(fresh: seats.Registry) -> None:
        fresh.seats["beta/fake"].smoke = smoke_b

    seats.update_registry(apply_b)

    # Process A now applies ONLY alpha's observed result (the fixed path) --
    # the old `save_registry(stale_snapshot)` would have erased beta's PASS.
    def apply_a(fresh: seats.Registry) -> None:
        fresh.seats["alpha/fake"].smoke = smoke_a

    seats.update_registry(apply_a)
    final = seats.load_registry()
    assert final.seats["alpha/fake"].smoke is not None
    assert final.seats["beta/fake"].smoke is not None


def test_update_registry_lock_contention_times_out(isolated: tuple[Path, Path], tmp_path: Path) -> None:
    registry, _ = isolated
    _brokered_registry(registry, tmp_path)
    lock = seats.registry_path().parent / (seats.registry_path().name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("held", encoding="utf-8")
    try:
        with pytest.raises(channel.ChannelError, match="registry lock"):
            seats.update_registry(lambda fresh: None, timeout_seconds=0.2)
    finally:
        lock.unlink()


def test_cli_smoke_uses_config_local_scratch_and_locked_apply(
    isolated: tuple[Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Field finding (2026-08-20): smoke scratch defaulted to the system temp
    dir. The CLI must pass a scratch base under the registry's own directory
    and apply results through the locked path."""
    from debate.__main__ import main

    registry, _ = isolated
    _brokered_registry(registry, tmp_path)
    captured: dict[str, object] = {}

    def fake_smoke(reg: seats.Registry, seat_id: str, **kwargs: object) -> str:
        captured["scratch_base"] = kwargs.get("scratch_base")
        reg.seats[seat_id].smoke = seats.SmokeStatus(at=NOW, result="pass")
        return "pass"

    monkeypatch.setattr(seats, "smoke_seat", fake_smoke)
    rc = main(["seats", "smoke", "alpha/fake", "--yes"])
    assert rc == 0
    scratch = captured["scratch_base"]
    assert isinstance(scratch, Path)
    assert scratch.parent == seats.registry_path().parent
    assert seats.load_registry().seats["alpha/fake"].smoke is not None


def test_stub_debate_reaches_typed_close(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    """The Slice 1B end-to-end: approve -> brokered open -> broker-open a
    case -> the controller drives both fake seats to a typed close. The
    human/session never votes; the record verifies clean."""
    import subprocess

    registry, project = isolated
    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("alpha/fake", "beta/fake"), source_ref=_head(project), author_vendor="claude",
        **REVIEW_CONTRACT,
    )
    live_registry = seats.load_registry()
    result = opening.open_debate_brokered(
        spec, live_registry, load_config_fn=_watcher_config, now=NOW, tool_version="test",
    )
    name = result.channel_name
    config_path = result.config_path
    # Speed the controller up for the test; the product default stays 60s.
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["scheduler_interval_seconds"] = 1
    config["retry_seconds"] = 1
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    src_dir = Path(__file__).resolve().parent.parent / "src"
    env = {
        "PATH": _hermetic_path(),
        "PYTHONPATH": str(src_dir),
        "DEBATE_SEATS_REGISTRY": str(registry),
        "HOME": str(tmp_path),
    }

    def run(*argv: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            [sys.executable, "-m", "debate", *argv],
            capture_output=True, text=True, env=env, timeout=timeout, check=False,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return proc

    run(
        "broker-open", "--root", str(root), "--channel", name,
        "--config", str(config_path), "--thread", "stub-case-1",
        "--first-seat", json.loads((root / f"{name}.debate.json").read_text())["parties"][0],
        "--body", "Stub review request: both fake seats return PASS.",
    )
    run(
        "watch", "--root", str(root), "--channel", name,
        "--config", str(config_path), "--until-close", timeout=120,
    )
    status_proc = run("status", "--root", str(root), "--channel", name)
    status = json.loads(status_proc.stdout[: status_proc.stdout.rindex("}") + 1])
    assert status["phase"] == "terminal"
    assert status["terminal_result"] == "PASS"
    assert status["close_reason"] == "party-vote-agreement"
    run("verify", "--root", str(root), "--channel", name)
    mailbox = (root / f"{name}.channel.md").read_text(encoding="utf-8")
    record = json.loads((root / f"{name}.debate.json").read_text(encoding="utf-8"))
    for party in record["parties"]:
        assert f"from: {party} | type: verdict" in mailbox
    # The human supervisor opened and closed; it never voted.
    assert "from: owner | type: verdict" not in mailbox
