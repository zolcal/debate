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
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from debate import bridge, channel, seats
from debate.__main__ import main

NOW = "2026-08-20T12:00:00+00:00"

SEAT_NAMES = ("mytool", "othertool")

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
    "body": "I ran the check the review material asks for; this is my position.",
}))
print("```")
'''


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


def _make_world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    """One project, two approved seats, one registry -- all under `tmp_path`."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")
    tool = tmp_path / "quiet_vendor_cli.py"
    tool.write_text(QUIET_VENDOR_CLI, encoding="utf-8")
    logs = {name: tmp_path / f"calls-{name}.jsonl" for name in SEAT_NAMES}
    answers = {name: tmp_path / f"answers-{name}.txt" for name in SEAT_NAMES}
    rows: dict[str, object] = {}
    for name in SEAT_NAMES:
        answers[name].write_text("PASS", encoding="utf-8")
        rows[f"{name}/model"] = _seat_row(
            [sys.executable, str(tool), str(logs[name]), str(answers[name]), "{prompt}"],
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


@pytest.fixture()
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    return _make_world(tmp_path / "first", monkeypatch)


@dataclass
class Case:
    """One finished debate: where its record is, and where its files are."""

    root: Path
    name: str
    config_path: Path
    runtime_root: Path


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
    runtime_root = world.project / "var" / "debate" / name

    assert main([
        "broker-open",
        "--root", str(root),
        "--channel", name,
        "--config", str(config_path),
        "--thread", "does-it-answer-42",
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
    return Case(root=root, name=name, config_path=config_path, runtime_root=runtime_root)


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


def test_by_default_a_discussion_round_re_reads_only_the_two_verdicts(world: World) -> None:
    case = _run_case(world, mode=None)

    assert "terminal-result: PASS" in _closing_body(case)
    sealed, later = _verdicts(case)
    assert len(sealed) == 2
    assert len(later) == 2
    for entry in later:
        assert "- deliberation-input: verdicts-only" in entry.body
    for entry in sealed:
        assert "- deliberation-input:" not in entry.body


def test_the_whole_review_material_is_re_read_when_the_operator_asks_for_it(world: World) -> None:
    case = _run_case(world, mode="full")

    assert "terminal-result: PASS" in _closing_body(case)
    sealed, later = _verdicts(case)
    assert len(later) == 2
    for entry in later:
        assert "- deliberation-input: full-docket" in entry.body
    for entry in sealed:
        assert "- deliberation-input:" not in entry.body


# What differs between two runs of the same case no matter what: the channel's
# own id, where it lives, and every hash and timestamp in it.
_HASH = re.compile(r"\b[0-9a-f]{40,64}\b")
_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+\d{2}:\d{2}|Z)?")


def _shaped(case: Case, world: World) -> list[str]:
    """The published record, with everything unrepeatable spelled generically."""
    text = channel.mailbox_path(case.root, case.name).read_text(encoding="utf-8")
    text = text.replace(case.name, "<channel>").replace(str(world.project), "<project>")
    text = text.replace(world.head, "<commit>").replace(world.head[:12], "<commit>")
    text = _HASH.sub("<hash>", text)
    text = _TIME.sub("<time>", text)
    return [line.rstrip() for line in text.splitlines()]


def test_the_two_modes_leave_the_same_record_apart_from_that_one_line(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, world: World
) -> None:
    """The mode changes what a seat READS, and nothing else about the case."""
    default_case = _run_case(world, mode=None)
    default_record = _shaped(default_case, world)

    second = _make_world(tmp_path / "second", monkeypatch)
    full_case = _run_case(second, mode="full")
    full_record = _shaped(full_case, second)

    assert len(default_record) == len(full_record)
    differences = [
        (left, right) for left, right in zip(default_record, full_record) if left != right
    ]
    assert differences == [
        ("- deliberation-input: verdicts-only", "- deliberation-input: full-docket"),
        ("- deliberation-input: verdicts-only", "- deliberation-input: full-docket"),
    ]


# Words that would prove a pass was RESUMED rather than started fresh.
CONTINUITY_WORDS = re.compile(r"continuation|session|token", re.IGNORECASE)

# The only hits allowed, and both are evidence FOR the law rather than against
# it: a declaration that a seat keeps nothing has to name the thing it turns
# off. Anything else -- a handle, an id, a key -- is a finding.
DECLARED_OFF = (
    # the recorded adapter manifest, per seat
    re.compile(r'"session_persistence": false'),
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
            if not CONTINUITY_WORDS.search(line):
                continue
            if any(allowed.search(line) for allowed in DECLARED_OFF):
                continue
            hits.append(f"{path}:{number}: {line.strip()}")
    return hits


def test_nothing_the_case_leaves_behind_carries_a_resumable_handle(world: World) -> None:
    """Section 5 of the protocol, checked against what is actually on disk."""
    case = _run_case(world, mode=None)

    assert _continuity_hits(case.root) == []
    assert _continuity_hits(case.runtime_root) == []


def test_the_recorded_seat_command_carries_the_chosen_mode(world: World) -> None:
    case = _run_case(world, mode=None)
    config = json.loads(case.config_path.read_text(encoding="utf-8"))
    for adapter in config["adapters"].values():
        spec = bridge.parse_bridge_command([str(part) for part in adapter["command"]])
        assert spec is not None
        assert spec.deliberation_input == "verdicts"
