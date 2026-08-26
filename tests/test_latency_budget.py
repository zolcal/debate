"""What the engine itself costs: measured, not asserted from memory.

Two budgets, both driven through the real command line -- open the case, then
run the watch loop to a typed close -- with stand-in seats that answer
instantly. Whatever these tests measure is the engine's own overhead: the
loop, the file protocol, the recording, and nothing else.

B3, the wall clock: a case whose seats agree reaches its typed close inside
ten seconds AT THE LOOP'S OWN CADENCE. No test here shrinks that cadence to
pass -- a budget met only by a tighter tick is a defect report, not a test.

B5, the call count: how many times each seat is actually woken. Two when both
seats agree from the start; four when they disagree once and then agree. Every
extra wake is somebody's money, so the number is pinned.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

from debate import channel, opening, seats
from debate.__main__ import _watcher_config, main

NOW = "2026-08-20T12:00:00+00:00"

# The stand-in for a vendor command line. It answers instantly and remembers:
# argv[1] is its call log (one line per invocation) and argv[2] is a file
# holding the answers it gives, in order, comma separated, the last one
# repeating -- "PASS" always passes, "NO_PASS,PASS" holds out once and then
# agrees.
COUNTING_VENDOR_CLI = '''\
import json
import sys
from pathlib import Path

log = Path(sys.argv[1])
answers = Path(sys.argv[2]).read_text(encoding="utf-8").strip().split(",")
before = len(log.read_text(encoding="utf-8").splitlines()) if log.exists() else 0
with open(log, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({"call": before + 1}) + "\\n")
print("I read the review material and ran the check it asks for.")
print("```json")
print(json.dumps({
    "schema_version": 3,
    "entry_type": "verdict",
    "decision": answers[min(before, len(answers) - 1)],
    "body": "I ran the check the review material asks for; this is my position.",
    "verification": {"status": "performed", "items": [{
        "command": "python -c fixture-probe", "exit_status": 0, "output": "VALUE = 42"
    }]},
}))
print("```")
'''

BUDGET_SECONDS = 10.0

SEAT_NAMES = ("mytool", "othertool")


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
        "isolation_argv": ["--no-config"],
        "no_persistence_argv": ["--no-history"],
        "config_home": None,
        "verification_argv": [],
        "verification_basis": "declared",
        "result_schema_version": 1,
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
    logs: dict[str, Path]
    answers: dict[str, Path]

    def says(self, seat: str, *decisions: str) -> None:
        self.answers[seat].write_text(",".join(decisions), encoding="utf-8")

    def calls(self, seat: str) -> int:
        log = self.logs[seat]
        if not log.exists():
            return 0
        return len([line for line in log.read_text(encoding="utf-8").splitlines() if line.strip()])


@pytest.fixture()
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    tool = tmp_path / "counting_vendor_cli.py"
    tool.write_text(COUNTING_VENDOR_CLI, encoding="utf-8")
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
        logs=logs,
        answers=answers,
    )


def _open_case(world: World) -> tuple[Path, str, Path]:
    """Open a fully managed debate and its first case, ready for the loop."""
    root = world.project / "collab"
    opened = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=root,
            label="budget",
            pair=("mytool/model", "othertool/model"),
            source_ref=world.head,
            author_vendor="claude",
            docket_files=("docket.md",),
            goal="Establish whether the project module answers 42.",
            review_domain="The pinned project module and docket.",
            stop_rule="Stop after the project-local probe and a decisive verdict.",
        ),
        seats.load_registry(),
        load_config_fn=_watcher_config,
        now=NOW,
        tool_version="test",
        real_home=world.home,
    )
    assert main([
        "broker-open",
        "--root", str(root),
        "--channel", opened.channel_name,
        "--config", str(opened.config_path),
        "--thread", "does-it-answer-42",
        "--first-seat", "mytool",
        "--refs", f"main@{world.head[:12]}",
        "--body", "Verify the criterion in the review material against the pinned source.",
    ]) == 0
    return root, opened.channel_name, opened.config_path


def _watch_to_close(root: Path, channel_name: str, config_path: Path) -> float:
    """Drive the case to its close at the loop's OWN cadence, timed.

    No `--interval` here on purpose: the cadence under test is the one a real
    debate runs at.
    """
    started = time.monotonic()
    assert main([
        "watch",
        "--root", str(root),
        "--channel", channel_name,
        "--config", str(config_path),
        "--until-close",
    ]) == 0
    return time.monotonic() - started


def _closing_body(root: Path, channel_name: str) -> str:
    entries = channel.read_entries(root, channel_name)
    assert entries[-1].entry_type == "close"
    return entries[-1].body


def test_an_agreed_case_closes_inside_the_engine_budget(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    """B3: with seats that answer instantly, what is left is the engine."""
    root, channel_name, config_path = _open_case(world)
    elapsed = _watch_to_close(root, channel_name, config_path)
    assert "terminal-result: PASS" in _closing_body(root, channel_name)
    with capsys.disabled():
        print(f"\nB3 measured: {elapsed:.2f}s to a typed close (budget {BUDGET_SECONDS:.0f}s)")
    assert elapsed < BUDGET_SECONDS, (
        f"the engine took {elapsed:.2f}s to reach a typed close at its own tick "
        f"cadence; the budget is {BUDGET_SECONDS:.0f}s"
    )


def test_an_agreed_case_wakes_each_seat_once(world: World) -> None:
    """B5, first half: one sealed answer each, and nothing more."""
    root, channel_name, config_path = _open_case(world)
    _watch_to_close(root, channel_name, config_path)
    assert "terminal-result: PASS" in _closing_body(root, channel_name)
    counted = {name: world.calls(name) for name in SEAT_NAMES}
    assert counted == {"mytool": 1, "othertool": 1}
    assert sum(counted.values()) == 2


def test_one_lap_of_disagreement_wakes_each_seat_twice(world: World) -> None:
    """B5, second half: a split sealed round costs exactly one more lap."""
    world.says("othertool", "NO_PASS", "PASS")
    root, channel_name, config_path = _open_case(world)
    _watch_to_close(root, channel_name, config_path)
    assert "terminal-result: PASS" in _closing_body(root, channel_name)
    counted = {name: world.calls(name) for name in SEAT_NAMES}
    assert counted == {"mytool": 2, "othertool": 2}
    assert sum(counted.values()) == 4
