"""What a seat re-reads in the discussion round, and what that leaves behind.

The default is now the two published verdicts: after the sealed pass the whole
review material is not sent a second time. The law this has to keep is the
protocol's (s5): nothing is resumed. Every pass is a fresh process, and the
only thing carrying the debate forward is the PUBLIC record -- the two
verdicts already published in the thread. No session, no token, no
continuation handle, anywhere.

Everything below runs the real product path: a fully managed open from the
registry, the real command line, and the real watch loop, with stand-in seats
that answer instantly. The stand-ins deliberately do NOT echo the question they
were handed, so what the case leaves on disk is the engine's own doing and not
a seat quoting its prompt back.

Three cases are driven, once each, and shared by the tests that only read what
they left behind: the default mode, the same case with the whole material
re-sent, and -- as the golden -- the same case again through a HAND-AUTHORED
adapter, which speaks the controller's file protocol directly and records
nothing at all about what it read.
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import pytest

from debate import bridge, channel, seats
from debate.__main__ import main

NOW = "2026-08-20T12:00:00+00:00"

SEAT_NAMES = ("mytool", "othertool")

THREAD = "does-it-answer-42"

VERDICT_BODY = "I ran the check the review material asks for; this is my position."

# The stand-in vendor command line. argv[1] is its call log, argv[2] a file of
# the decisions it gives in order (the last one repeating). It prints its
# answer block and NOTHING else: never the question, never its own argv.
QUIET_VENDOR_CLI = '''\
import json
import sys
from pathlib import Path

log = Path(sys.argv[1])
answers = Path(sys.argv[2]).read_text(encoding="utf-8").strip().split(",")
before = len(log.read_text(encoding="utf-8").splitlines()) if log.exists() else 0
with open(log, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({"call": before + 1}) + "\\n")
print("```json")
print(json.dumps({
    "schema_version": 1,
    "entry_type": "verdict",
    "decision": answers[min(before, len(answers) - 1)],
    "body": "%s",
}))
print("```")
''' % VERDICT_BODY

# The same seat as a HAND-AUTHORED adapter: it speaks the controller's file
# protocol itself, so Debate's runner never wraps it -- and it writes no word
# about what it read. Same decisions, same body, same reported model, so the
# only thing it can differ in is what the runner would have added.
HAND_AUTHORED_ADAPTER = '''\
import json
import sys
from pathlib import Path

log = Path(sys.argv[1])
answers = Path(sys.argv[2]).read_text(encoding="utf-8").strip().split(",")
before = len(log.read_text(encoding="utf-8").splitlines()) if log.exists() else 0
with open(log, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({"call": before + 1}) + "\\n")
Path(sys.argv[4]).write_text(json.dumps({
    "schema_version": 1,
    "entry_type": "verdict",
    "decision": answers[min(before, len(answers) - 1)],
    "body": "%s",
    "runtime_model": "model",
}), encoding="utf-8")
''' % VERDICT_BODY


def _seat_row(argv: list[str], *, vendor: str, submodel: str) -> dict[str, object]:
    return {
        "vendor": vendor,
        "submodel": submodel,
        "effort": None,
        "commands": [argv],
        "source": "manual",
        "present": True,
        "smoke": None,
        "cost_mode": "local",
        "capability_class": "frontier",
        # Neither flag names a session, so any such word on disk afterwards is
        # the engine's own and not a seat command quoted back.
        "isolation_argv": ["--no-config"],
        "no_persistence_argv": ["--no-history"],
        "config_home": None,
    }


def _git(project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(project), "-c", "user.email=t@t", "-c", "user.name=t", *arguments],
        capture_output=True, text=True, check=True,
    )


@dataclass
class World:
    """A project with two approved seats whose answers the test scripts."""

    project: Path
    head: str
    home: Path
    answers: dict[str, Path]

    def says(self, seat: str, *decisions: str) -> None:
        self.answers[seat].write_text(",".join(decisions), encoding="utf-8")


def _make_world(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, hand_authored: bool = False
) -> World:
    """One project, two approved seats, one registry -- all under `tmp_path`.

    With `hand_authored`, the two seats speak the controller's file protocol
    themselves; otherwise they are ordinary question-taking commands that
    Debate's own runner wraps.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)
    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")
    tool = tmp_path / "stand_in_seat.py"
    tool.write_text(HAND_AUTHORED_ADAPTER if hand_authored else QUIET_VENDOR_CLI, encoding="utf-8")
    logs = {name: tmp_path / f"calls-{name}.jsonl" for name in SEAT_NAMES}
    answers = {name: tmp_path / f"answers-{name}.txt" for name in SEAT_NAMES}
    tail = ["{input_path}", "{result_path}"] if hand_authored else ["{prompt}"]
    rows: dict[str, object] = {}
    for name in SEAT_NAMES:
        answers[name].write_text("PASS", encoding="utf-8")
        rows[f"{name}/model"] = _seat_row(
            [sys.executable, str(tool), str(logs[name]), str(answers[name]), *tail],
            vendor=name, submodel="model",
        )
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps({
            "registry_version": 1,
            "tool_version": "test",
            "discovered_at": NOW,
            "seats": rows,
            "last_pair": {},
        }) + "\n",
        encoding="utf-8",
    )
    project = tmp_path / "project"
    project.mkdir()
    (project / ".gitignore").write_text("collab/\nvar/\ndebate-profile.json\n", encoding="utf-8")
    (project / "docket.md").write_text(
        "# What to check\n\nThe project module answers 42. PASS only if it does.\n",
        encoding="utf-8",
    )
    (project / "project_module.py").write_text("VALUE = 42\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", "-b", "main", str(project)], check=True)
    _git(project, "add", ".")
    _git(project, "commit", "-qm", "fixture")
    (project / seats.PROFILE_NAME).write_text(
        json.dumps({
            "profile_version": 1,
            "allowlist": [f"{name}/model" for name in SEAT_NAMES],
        }) + "\n",
        encoding="utf-8",
    )
    home = tmp_path / "home"
    home.mkdir()
    return World(
        project=project,
        head=_git(project, "rev-parse", "HEAD").stdout.strip(),
        home=home,
        answers=answers,
    )


@dataclass
class Case:
    """One finished debate: where its record is, and where its files are."""

    root: Path
    name: str
    config_path: Path
    runtime_root: Path
    world: World


def _run_case(world: World, *, mode: str | None) -> Case:
    """Open a fully managed debate through the real command line and drive it
    to a typed close, with the seats split on the sealed pass."""
    root = world.project / "collab"
    world.says("othertool", "NO_PASS", "PASS")
    argv = [
        "open",
        "--root", str(root),
        "--label", "discussion",
        "--brokered",
        "--pair", "mytool/model,othertool/model",
        "--source-ref", world.head,
        "--author-vendor", "claude",
        "--docket-file", "docket.md",
        "--yes",
    ]
    if mode is not None:
        argv += ["--deliberation-input", mode]
    assert main(argv) == 0
    names = sorted(path.name[: -len(".debate.json")] for path in root.glob("*.debate.json"))
    assert len(names) == 1, names
    name = names[0]
    config_path = world.project / f"{name}.watcher.json"

    assert main([
        "broker-open",
        "--root", str(root),
        "--channel", name,
        "--config", str(config_path),
        "--thread", THREAD,
        "--first-seat", "mytool",
        "--refs", f"main@{world.head[:12]}",
        "--body", "Verify the criterion in the review material against the pinned source.",
    ]) == 0
    assert main([
        "watch",
        "--root", str(root),
        "--channel", name,
        "--config", str(config_path),
        "--until-close",
    ]) == 0
    return Case(
        root=root,
        name=name,
        config_path=config_path,
        runtime_root=world.project / "var" / "debate" / name,
        world=world,
    )


def _case(
    tmp_path_factory: pytest.TempPathFactory, folder: str, *, mode: str | None, hand_authored: bool
) -> Iterator[Case]:
    with pytest.MonkeyPatch.context() as patch:
        world = _make_world(
            tmp_path_factory.mktemp(folder), patch, hand_authored=hand_authored
        )
        yield _run_case(world, mode=mode)


# One run each, shared by every test that only READS what the run left behind.
@pytest.fixture(scope="module")
def default_case(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Case]:
    yield from _case(tmp_path_factory, "default", mode=None, hand_authored=False)


@pytest.fixture(scope="module")
def full_case(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Case]:
    yield from _case(tmp_path_factory, "full", mode="full", hand_authored=False)


@pytest.fixture(scope="module")
def hand_authored_case(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Case]:
    yield from _case(tmp_path_factory, "hand", mode="full", hand_authored=True)


def _verdicts(case: Case) -> tuple[list[channel.Entry], list[channel.Entry]]:
    """The published verdicts, split into the sealed pair and the later ones."""
    entries = [
        entry
        for entry in channel.read_entries(case.root, case.name)
        if entry.entry_type == "verdict"
    ]
    sealed = [entry for entry in entries if "- phase: sealed" in entry.body]
    later = [entry for entry in entries if "- phase: deliberation" in entry.body]
    assert len(sealed) + len(later) == len(entries)
    return sealed, later


def _closing_body(case: Case) -> str:
    entries = channel.read_entries(case.root, case.name)
    assert entries[-1].entry_type == "close"
    return entries[-1].body


def _sealed_records(case: Case) -> dict[str, dict[str, object]]:
    """What the private case file kept of each seat's sealed position."""
    state = json.loads(
        (case.runtime_root / "cases" / THREAD / "case.json").read_text(encoding="utf-8")
    )
    records = {}
    for party, record in state["sealed_submissions"].items():
        assert isinstance(record["result"], dict)
        records[str(party)] = dict(record["result"])
    return records


def test_by_default_a_discussion_round_re_reads_only_the_two_verdicts(default_case: Case) -> None:
    assert "terminal-result: PASS" in _closing_body(default_case)
    sealed, later = _verdicts(default_case)
    assert len(sealed) == 2
    assert len(later) == 2
    for entry in later:
        assert "- deliberation-input: verdicts-only" in entry.body
    for entry in sealed:
        assert "- deliberation-input:" not in entry.body


def test_the_whole_review_material_is_re_read_when_the_operator_asks_for_it(
    full_case: Case,
) -> None:
    assert "terminal-result: PASS" in _closing_body(full_case)
    sealed, later = _verdicts(full_case)
    assert len(later) == 2
    for entry in later:
        assert "- deliberation-input: full-docket" in entry.body
    for entry in sealed:
        assert "- deliberation-input:" not in entry.body


# What differs between two runs of the same case no matter what: the channel's
# own id, where it lives, the commit under review, and every hash and timestamp.
_HASH = re.compile(r"\b[0-9a-f]{40,64}\b")
_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+\d{2}:\d{2}|Z)?")


def _shaped(case: Case) -> list[str]:
    """The published record, with everything unrepeatable spelled generically."""
    world = case.world
    text = channel.mailbox_path(case.root, case.name).read_text(encoding="utf-8")
    text = text.replace(case.name, "<channel>").replace(str(world.project), "<project>")
    text = text.replace(world.head, "<commit>").replace(world.head[:12], "<commit>")
    text = _HASH.sub("<hash>", text)
    text = _TIME.sub("<time>", text)
    return [line.rstrip() for line in text.splitlines()]


def _differing_lines(left: list[str], right: list[str]) -> list[str]:
    """Every line one record has and the other does not, either way round."""
    return [
        line[2:]
        for line in difflib.ndiff(left, right)
        if line.startswith(("+ ", "- "))
    ]


def test_the_two_modes_leave_the_same_record_apart_from_that_one_line(
    default_case: Case, full_case: Case
) -> None:
    """The mode changes what a seat READS, and nothing else about the case."""
    default_record = _shaped(default_case)
    full_record = _shaped(full_case)

    assert len(default_record) == len(full_record)
    differences = [
        (left, right) for left, right in zip(default_record, full_record) if left != right
    ]
    assert differences == [
        ("- deliberation-input: verdicts-only", "- deliberation-input: full-docket"),
        ("- deliberation-input: verdicts-only", "- deliberation-input: full-docket"),
    ]


# The golden. A hand-authored adapter goes through the SAME controller, so
# every line of the record is produced by the same code -- except the lines
# that describe the runner itself, and those are enumerated here with the
# reason each one is expected to differ. Anything else differing is a
# regression in output that both modes would otherwise share.
ALLOWED_GOLDEN_DIFFERENCES = (
    # the runner names itself; a hand-authored adapter names itself
    "- cli-version: ",
    # C4: an ordinary command line cannot verify which model answered
    "- runtime-model-basis: ",
    # C4: where the runner's isolation arguments came from; a hand-authored
    # adapter went through no such arguments and reports none
    "- isolation-flags: ",
    # B1: what the discussion round re-read; only the runner records it
    "- deliberation-input: ",
    # the recorded adapter manifests -- different commands, by construction
    "- sanitized-profile-manifests: ",
)


def test_full_mode_matches_an_adapter_that_records_nothing_about_what_it_read(
    full_case: Case, hand_authored_case: Case
) -> None:
    """Golden: `full` mode changes nothing a pre-B1 record did not already say."""
    differences = _differing_lines(_shaped(full_case), _shaped(hand_authored_case))

    unexpected = [
        line for line in differences if not line.startswith(ALLOWED_GOLDEN_DIFFERENCES)
    ]
    assert unexpected == []
    # and the one line this slice adds is really there, on both later entries
    assert [line for line in differences if line.startswith("- deliberation-input: ")] == [
        "- deliberation-input: full-docket",
        "- deliberation-input: full-docket",
    ]


def test_a_sealed_private_record_says_nothing_about_a_later_pass(
    full_case: Case, hand_authored_case: Case
) -> None:
    """The same golden, one layer down: the private sealed records."""
    wrapped = _sealed_records(full_case)
    hand_authored = _sealed_records(hand_authored_case)

    assert sorted(wrapped) == sorted(hand_authored) == sorted(SEAT_NAMES)
    for party in SEAT_NAMES:
        assert wrapped[party]["deliberation_input"] is None
        assert hand_authored[party]["deliberation_input"] is None
        differing = {
            key
            for key in set(wrapped[party]) | set(hand_authored[party])
            if wrapped[party].get(key) != hand_authored[party].get(key)
        }
        assert differing == {"runtime_model_basis", "isolation_flags"}


# Words that would prove a pass was RESUMED rather than started fresh.
CONTINUITY_WORDS = re.compile(r"continuation|session|token", re.IGNORECASE)

# The only spans allowed to carry such a word, and both are evidence FOR the
# law rather than against it: a declaration that a seat keeps nothing has to
# name the thing it turns off. Only the matched SPAN is excused, never the rest
# of its line -- the recorded manifests are one long single-line object, so a
# whole-line exception would hide anything else written on it.
DECLARED_OFF = (
    # the recorded adapter manifest, per seat -- also one level of JSON
    # escaping deeper, where a later pass carries the opening entry's body
    re.compile(r'\\?"session_persistence\\?": false'),
    # the recorded permission policy, per seat
    re.compile(r"session saving are turned off"),
)

# The protocol document is shipped with every channel folder; it is the rules,
# not this case's record, and it discusses unattended sessions in prose.
SHIPPED_DOCUMENT = "PROTOCOL.md"


def _continuity_hits(root: Path) -> list[str]:
    hits: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == SHIPPED_DOCUMENT:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            remainder = line
            for allowed in DECLARED_OFF:
                remainder = allowed.sub("", remainder)
            if CONTINUITY_WORDS.search(remainder):
                hits.append(f"{path}:{number}: {line.strip()}")
    return hits


def test_nothing_the_case_leaves_behind_carries_a_resumable_handle(default_case: Case) -> None:
    """Section 5 of the protocol, checked against what is actually on disk."""
    assert _continuity_hits(default_case.root) == []
    assert _continuity_hits(default_case.runtime_root) == []


def test_the_scan_still_sees_a_handle_written_beside_an_allowed_declaration(
    tmp_path: Path,
) -> None:
    """The excuse is the span, not the line: the manifests are ONE line."""
    planted = tmp_path / "case.json"
    planted.write_text(
        '{"session_persistence": false, "resume_key": "session-9f2c", "x": 1}\n',
        encoding="utf-8",
    )
    hits = _continuity_hits(tmp_path)
    assert len(hits) == 1
    assert "resume_key" in hits[0]

    planted.write_text('{"session_persistence": false, "x": 1}\n', encoding="utf-8")
    assert _continuity_hits(tmp_path) == []


def test_the_recorded_seat_command_carries_the_chosen_mode(default_case: Case) -> None:
    config = json.loads(default_case.config_path.read_text(encoding="utf-8"))
    for adapter in config["adapters"].values():
        spec = bridge.parse_bridge_command([str(part) for part in adapter["command"]])
        assert spec is not None
        assert spec.deliberation_input == "verdicts"
