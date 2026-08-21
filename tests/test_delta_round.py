"""The fold-delta round: the protocol clauses, the composer, and the CLI.

Round N+1 of a gate review verifies FOLDS, not the artifact from scratch, and
that only works when the seats can see the prior version themselves. This file
pins the three things that make that possible: the clause texts (byte-exact --
the copies below are the law, pasted here so a silent edit to the engine's copy
fails), the composer that arranges goal + clauses + priors + prior verdicts +
the author's fold list + the TRUE diff, and the CLI that refuses before it
writes anything.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from debate import channel, delta
from debate.__main__ import main
from debate.controller import BrokerController

from test_controller import make_channel, make_repository, profile_payload


# --- the clauses, pasted verbatim --------------------------------------------

R0_GOAL_PREFIX = "GOAL: "

R2_CLAUSE = (
    "Name EVERY blocking finding you can establish in this pass, not the first "
    "one; write the list so that a second pass by you would find nothing new. A "
    "verdict citing one blocker while others are establishable in the same pass is "
    "an incomplete verdict."
)

R3_CLAUSE = (
    "This is a fold-delta round. The change set is SCOPED to the artifact(s) under "
    "review; round scaffolding — the docket instruction sheet itself, which "
    "necessarily changes every round — is excluded by name. Compute the TRUE change "
    "set yourself by diffing the artifact against the prior version INCLUDED IN "
    "THIS DOCKET (named in the fold list header) — never trust the author's fold "
    "list as the change inventory; an artifact edit absent from the fold list is "
    "itself an unresolved finding. Then verify (a) that each fold in the true "
    "change set resolves its round-N finding, (b) the REVERSE: every round-N "
    "finding has a corresponding fold — a finding with no fold is unresolved, and "
    "(c) a coherence sweep: whether any change contradicts ANY other part of the "
    "artifact. Criteria that passed in round N stand UNLESS the true change set or "
    "the sweep implicates them — establish implicated ones on your own fresh "
    "evidence; for the rest, CITE the round-N verdict (MSG id) where your own "
    "evidence established them: standing is a citation, never an omission."
)


def test_the_protocol_clauses_are_byte_exact() -> None:
    assert delta.R0_GOAL_PREFIX == R0_GOAL_PREFIX
    assert delta.R2_CLAUSE == R2_CLAUSE
    assert delta.R3_CLAUSE == R3_CLAUSE


# --- the composer ------------------------------------------------------------

PRIOR_TEXT = "line one\nold line\nline three\n"
CURRENT_TEXT = "line one\nnew line\nline three\n"
FOLD_LIST = "1. Finding 1: the bullet now names the documented vendor branch.\n2. Bookkeeping: an Amended line."


def make_round() -> tuple[delta.DeltaRound, dict[str, str]]:
    round_ = delta.DeltaRound(
        goal="verify that the round-1 folds resolve the round-1 findings",
        fold_list=FOLD_LIST,
        priors=(("docs/plans/plan.md", "var/debate/priors/plan-round1.md"),),
        prior_verdicts=(
            ("MSG-32", "NO_PASS: the bridge test bullet contradicts 3.4."),
            ("MSG-33", "NO_PASS: two findings, both blocking."),
        ),
    )
    diffs = {
        "docs/plans/plan.md": delta.unified_diff(
            PRIOR_TEXT,
            CURRENT_TEXT,
            prior_path="var/debate/priors/plan-round1.md",
            current_path="docs/plans/plan.md",
        )
    }
    return round_, diffs


def test_compose_docket_arranges_goal_clauses_priors_verdicts_fold_list_and_true_diff() -> None:
    round_, diffs = make_round()

    text = delta.compose_docket(round_, diffs=diffs)

    assert text.startswith("GOAL: verify that the round-1 folds resolve the round-1 findings\n")
    assert R2_CLAUSE in text
    assert R3_CLAUSE in text
    assert "Prior version: `var/debate/priors/plan-round1.md`" in text
    assert "Current version: `docs/plans/plan.md`" in text
    assert "### MSG-32" in text
    assert "NO_PASS: the bridge test bullet contradicts 3.4." in text
    assert "### MSG-33" in text
    assert "NO_PASS: two findings, both blocking." in text
    assert FOLD_LIST in text
    assert "```diff" in text
    assert "--- var/debate/priors/plan-round1.md" in text
    assert "+++ docs/plans/plan.md" in text
    assert "-old line" in text
    assert "+new line" in text
    # The order is the protocol's order: goal, then the two clauses, then the
    # inputs the clauses send the seat to.
    assert (
        text.index(R2_CLAUSE)
        < text.index(R3_CLAUSE)
        < text.index("Prior version:")
        < text.index("### MSG-32")
        < text.index(FOLD_LIST)
        < text.index("```diff")
    )


def test_compose_docket_refuses_an_artifact_with_no_computed_diff() -> None:
    """The engine arranges; it never invents the missing half of the record."""
    round_, _diffs = make_round()

    with pytest.raises(channel.ChannelError, match="no diff"):
        delta.compose_docket(round_, diffs={})


# --- the CLI -----------------------------------------------------------------

THREAD = "review-one"
PRIOR = "var/debate/priors/plan-round1.md"
CURRENT = "docs/plans/superseded.md"


class Case:
    def __init__(self, repo: Path, root: Path, name: str, config_path: Path) -> None:
        self.repo = repo
        self.root = root
        self.name = name
        self.config_path = config_path
        self.runtime = repo / "var" / "debate" / "delta-fixture"


def tree_digest(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def open_case(tmp_path: Path) -> Case:
    repo, sha = make_repository(tmp_path)
    root, name = make_channel(repo)
    runtime = repo / "var" / "debate" / "delta-fixture"
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
                "docket_files": [CURRENT, "watcher.json"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    assert (
        main(
            [
                "broker-open",
                "--root",
                str(root),
                "--channel",
                name,
                "--config",
                str(config_path),
                "--thread",
                THREAD,
                "--first-seat",
                "bob",
                "--body",
                "Acceptance criteria fixed before either seat runs.",
            ]
        )
        == 0
    )
    (repo / PRIOR).parent.mkdir(parents=True, exist_ok=True)
    (repo / PRIOR).write_text("# Untracked plan revision\n\nold line\n", encoding="utf-8")
    (repo / CURRENT).write_text("# Untracked plan revision\n\nnew line\n", encoding="utf-8")
    (repo / "fold-list.md").write_text(FOLD_LIST + "\n", encoding="utf-8")
    return Case(repo, root, name, config_path)


def post_verdict(case: Case, body: str) -> str:
    return channel.post(case.root, "owner", "verdict", THREAD, body, name=case.name)


def delta_argv(
    case: Case, *extra: str, current: str = CURRENT, prior: str = PRIOR, verdict: str = "MSG-2"
) -> list[str]:
    return [
        "broker-revise",
        "--root",
        str(case.root),
        "--channel",
        case.name,
        "--config",
        str(case.config_path),
        "--thread",
        THREAD,
        "--delta-round",
        "--goal",
        "verify that the round-1 folds resolve the round-1 findings",
        "--fold-list-file",
        str(case.repo / "fold-list.md"),
        "--prior",
        f"{current}={prior}",
        "--prior-verdict",
        verdict,
        "--body",
        "Folds recorded; verify them against the prior version in your docket.",
        *extra,
    ]


@pytest.mark.parametrize(
    ("case_name", "prior", "verdict", "expected"),
    [
        ("absent prior", "var/debate/priors/never-written.md", "MSG-2", "does not exist"),
        ("not a verdict", PRIOR, "MSG-1", "not a verdict"),
        ("absent entry", PRIOR, "MSG-99", "is not an entry"),
    ],
)
def test_a_delta_round_refuses_before_it_writes_anything(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    case_name: str,
    prior: str,
    verdict: str,
    expected: str,
) -> None:
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")
    config_before = case.config_path.read_bytes()
    runtime_before = tree_digest(case.runtime)
    record_before = tree_digest(case.root)

    code = main(delta_argv(case, prior=prior, verdict=verdict))

    error = capsys.readouterr().err
    assert code == 1, case_name
    assert expected in error, error
    assert case.config_path.read_bytes() == config_before
    assert tree_digest(case.runtime) == runtime_before
    assert tree_digest(case.root) == record_before
    assert not (case.repo / "var" / "debate" / case.name).exists()


def test_a_delta_round_refuses_a_current_version_that_is_not_a_docket_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")
    (case.repo / "project_module.py").write_text("VALUE = 43\n", encoding="utf-8")
    config_before = case.config_path.read_bytes()
    runtime_before = tree_digest(case.runtime)

    code = main(delta_argv(case, current="project_module.py"))

    error = capsys.readouterr().err
    assert code == 1
    assert "project_module.py" in error
    assert "docket_files" in error
    assert case.config_path.read_bytes() == config_before
    assert tree_digest(case.runtime) == runtime_before


def test_a_delta_round_writes_the_docket_extends_the_docket_files_and_revises_once(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    case = open_case(tmp_path)
    verdict_body = "NO_PASS: the bullet contradicts 3.4; the fold list must resolve it."
    assert post_verdict(case, verdict_body) == "MSG-2"
    original = BrokerController.revise_case
    calls: list[dict[str, Any]] = []

    def counted(self: BrokerController, **kwargs: Any) -> str:
        calls.append(kwargs)
        return str(original(self, **kwargs))

    monkeypatch.setattr(BrokerController, "revise_case", counted)

    code = main(delta_argv(case))

    output = capsys.readouterr().out
    assert code == 0, output
    docket = case.repo / "var" / "debate" / case.name / f"delta-docket-{THREAD}-1.md"
    assert docket.is_file()
    text = docket.read_text(encoding="utf-8")
    assert text.startswith("GOAL: verify that the round-1 folds resolve the round-1 findings\n")
    assert R2_CLAUSE in text
    assert R3_CLAUSE in text
    assert f"Prior version: `{PRIOR}`" in text
    assert f"Current version: `{CURRENT}`" in text
    assert "### MSG-2" in text
    assert verdict_body in text
    assert FOLD_LIST in text
    assert "-old line" in text
    assert "+new line" in text

    raw = json.loads(case.config_path.read_text(encoding="utf-8"))
    assert raw["docket_files"] == [
        CURRENT,
        "watcher.json",
        PRIOR,
        f"var/debate/{case.name}/delta-docket-{THREAD}-1.md",
    ]
    assert len(calls) == 1
    assert str(docket) in output
    assert PRIOR in output
    entries = channel.thread_entries(case.root, THREAD, case.name)
    assert entries[-1].entry_type == "info"
    assert "Controller-Revision-Provenance" in entries[-1].body
    assert f"var/debate/{case.name}/delta-docket-{THREAD}-1.md" in entries[-1].body


def test_a_second_delta_round_takes_the_next_free_number_and_never_overwrites(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")

    assert main(delta_argv(case)) == 0
    capsys.readouterr()
    (case.repo / CURRENT).write_text("# Untracked plan revision\n\nnewer line\n", encoding="utf-8")
    assert main(delta_argv(case)) == 0

    first = case.repo / "var" / "debate" / case.name / f"delta-docket-{THREAD}-1.md"
    second = case.repo / "var" / "debate" / case.name / f"delta-docket-{THREAD}-2.md"
    assert first.is_file() and second.is_file()
    assert "+new line" in first.read_text(encoding="utf-8")
    assert "+newer line" in second.read_text(encoding="utf-8")
    raw = json.loads(case.config_path.read_text(encoding="utf-8"))
    assert raw["docket_files"].count(PRIOR) == 1
    assert raw["docket_files"][-2:] == [
        f"var/debate/{case.name}/delta-docket-{THREAD}-1.md",
        f"var/debate/{case.name}/delta-docket-{THREAD}-2.md",
    ]


def test_a_named_docket_path_that_already_exists_is_refused_rather_than_overwritten(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")
    named = f"var/debate/{case.name}/round-2-docket.md"

    assert main(delta_argv(case, "--docket-out", named)) == 0
    capsys.readouterr()
    written = (case.repo / named).read_bytes()
    config_before = case.config_path.read_bytes()

    code = main(delta_argv(case, "--docket-out", named))

    error = capsys.readouterr().err
    assert code == 1
    assert "already exists" in error
    assert (case.repo / named).read_bytes() == written
    assert case.config_path.read_bytes() == config_before


def test_the_delta_flags_are_refused_without_the_delta_round_flag(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    case = open_case(tmp_path)
    argv = [item for item in delta_argv(case) if item != "--delta-round"]

    code = main(argv)

    assert code == 1
    assert "--delta-round" in capsys.readouterr().err


def test_one_artifact_gets_one_prior_version(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")
    other = "var/debate/priors/plan-round0.md"
    (case.repo / other).write_text("# Untracked plan revision\n\noldest line\n", encoding="utf-8")

    code = main(delta_argv(case, "--prior", f"{CURRENT}={other}"))

    assert code == 1
    assert "twice" in capsys.readouterr().err
    assert not (case.repo / "var" / "debate" / case.name).exists()


def test_an_artifact_is_not_its_own_prior_version(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")

    code = main(delta_argv(case, prior=CURRENT))

    assert code == 1
    assert "its own prior version" in capsys.readouterr().err
    assert not (case.repo / "var" / "debate" / case.name).exists()


def test_a_refused_recording_rolls_the_docket_and_the_config_back(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The writes land before `revise_case` runs, and `revise_case` has its own
    refusals. A round that was not recorded must leave nothing claiming it was.
    """
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")
    config_before = case.config_path.read_bytes()
    runtime_before = tree_digest(case.runtime)
    record_before = tree_digest(case.root)

    def refuse(self: BrokerController, **kwargs: Any) -> str:
        raise channel.ChannelError("refused: the case says otherwise")

    monkeypatch.setattr(BrokerController, "revise_case", refuse)

    code = main(delta_argv(case))

    captured = capsys.readouterr()
    assert code == 1
    assert "the case says otherwise" in captured.err
    assert "instruction sheet" not in captured.out
    assert case.config_path.read_bytes() == config_before
    assert tree_digest(case.runtime) == runtime_before
    assert tree_digest(case.root) == record_before
    assert not (case.repo / "var" / "debate" / case.name).exists()


def test_a_real_revise_refusal_rolls_back_through_the_cli(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The same rollback, driven by a refusal the controller raises for itself:
    a different half-finished revision left in the case manifest."""
    case = open_case(tmp_path)
    post_verdict(case, "NO_PASS: one blocking finding, round 1.")
    manifest_path = case.runtime / "cases" / THREAD / "case.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["pending_revision"] = {"revision_sha256": "f" * 64}
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    config_before = case.config_path.read_bytes()
    manifest_before = manifest_path.read_bytes()
    record_before = tree_digest(case.root)

    code = main(delta_argv(case))

    assert code == 1
    assert "half-finished revision" in capsys.readouterr().err
    assert case.config_path.read_bytes() == config_before
    assert manifest_path.read_bytes() == manifest_before
    assert tree_digest(case.root) == record_before
    assert not (case.repo / "var" / "debate" / case.name).exists()
