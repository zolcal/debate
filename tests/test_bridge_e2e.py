"""Two ordinary prompt-taking CLIs debate each other, start to finish.

Nothing in this test hand-writes an adapter. Two seats are recorded the way
`debate seats add` records them -- an executable, one place for the question,
the arguments that switch the tool's settings and session saving off, and (for
one of them) the tool's own configuration folder -- and from there the real
code paths do the rest: the fully managed open wraps each seat, the CLI opens
the case, the CLI's watch loop drives it, and the channel closes with a typed
terminal result.

What the seats run is a stand-in for a vendor CLI: it ignores the question it
was handed, records what it was actually invoked with, and prints a
well-formed answer block. That is enough to prove the whole path without a
model call.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from debate import channel, opening, seats
from debate.__main__ import _watcher_config, main

NOW = "2026-08-20T12:00:00+00:00"

# The stand-in vendor CLI. argv[1] is where it logs each invocation; the rest
# is whatever the seat command and its flags handed it.
FAKE_VENDOR_CLI = '''\
import json
import os
import subprocess
import sys
from pathlib import Path

log = Path(sys.argv[1])
log.mkdir(parents=True, exist_ok=True)
record = {"argv": sys.argv[2:], "config_home": os.environ.get("MYTOOL_HOME")}
(log / ("call-%d.json" % len(list(log.glob("call-*.json"))))).write_text(
    json.dumps(record), encoding="utf-8"
)
probe_text = "from project_module import VALUE; print(VALUE)"
probe = subprocess.run(
    [sys.executable, "-c", probe_text], capture_output=True, text=True, check=False
)
probe_output = (probe.stdout if probe.stdout else probe.stderr).strip()
decision = "PASS" if probe.returncode == 0 and probe_output == "42" else "NO_PASS"
print("I inspected the exported project and ran its local module probe.")
print("```json")
print(json.dumps({
    "schema_version": 3,
    "entry_type": "verdict",
    "decision": decision,
    "body": "I ran the project-local module probe from the immutable export.",
    "verification": {"status": "performed", "items": [{
        "command": "python -c 'from project_module import VALUE; print(VALUE)'",
        "exit_status": probe.returncode,
        "output": probe_output,
    }]},
}))
print("```")
'''


def _seat_row(
    argv: list[str],
    *,
    vendor: str,
    submodel: str,
    isolation_argv: list[str],
    no_persistence_argv: list[str],
    config_home: str | None,
) -> dict[str, object]:
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
        "isolation_argv": list(isolation_argv),
        "no_persistence_argv": list(no_persistence_argv),
        "config_home": config_home,
        "verification_argv": [],
        "verification_basis": "declared",
        "result_schema_version": 1,
    }


def _git(project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(project), "-c", "user.email=t@t", "-c", "user.name=t", *arguments],
        capture_output=True, text=True, check=True,
    )


def _project(tmp_path: Path) -> tuple[Path, str]:
    """A git project with something to review and something to review it against."""
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
    return project, _git(project, "rev-parse", "HEAD").stdout.strip()


@dataclass
class World:
    """Everything the debate below needs, and nothing else."""

    project: Path
    head: str
    home: Path
    logs: dict[str, Path]


@pytest.fixture()
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> World:
    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    tool = tmp_path / "fake_vendor_cli.py"
    tool.write_text(FAKE_VENDOR_CLI, encoding="utf-8")
    logs = {"mytool": tmp_path / "calls-mytool", "othertool": tmp_path / "calls-othertool"}
    rows = {
        "mytool/big": _seat_row(
            [sys.executable, str(tool), str(logs["mytool"]), "{prompt}"],
            vendor="mytool", submodel="big",
            isolation_argv=["--no-config"], no_persistence_argv=["--no-history"],
            config_home="MYTOOL_HOME=.mytool",
        ),
        "othertool/large": _seat_row(
            [sys.executable, str(tool), str(logs["othertool"]), "{prompt}"],
            vendor="othertool", submodel="large",
            isolation_argv=["--ignore-user-config"], no_persistence_argv=["--ephemeral"],
            config_home=None,
        ),
    }
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
    project, head = _project(tmp_path)
    (project / seats.PROFILE_NAME).write_text(
        json.dumps({"profile_version": 1, "allowlist": ["mytool/big", "othertool/large"]}) + "\n",
        encoding="utf-8",
    )
    home = tmp_path / "home"
    home.mkdir()
    return World(project=project, head=head, home=home, logs=logs)


@dataclass
class Call:
    """One invocation of the stand-in vendor CLI, as it saw itself."""

    argv: list[str]
    config_home: str | None


def _calls(log: Path) -> list[Call]:
    calls: list[Call] = []
    for path in sorted(log.glob("call-*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        home = raw["config_home"]
        calls.append(Call(argv=[str(part) for part in raw["argv"]], config_home=home))
    return calls


def test_two_ordinary_cli_seats_debate_to_a_typed_close(world: World) -> None:
    project, home, logs = world.project, world.home, world.logs
    root = project / "collab"

    opened = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=root,
            label="e2e",
            pair=("mytool/big", "othertool/large"),
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
        real_home=home,
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

    assert main([
        "watch",
        "--root", str(root),
        "--channel", opened.channel_name,
        "--config", str(opened.config_path),
        "--until-close",
    ]) == 0

    entries = channel.read_entries(root, opened.channel_name)
    closing = entries[-1]
    assert closing.entry_type == "close"
    assert "terminal-result: PASS" in closing.body
    assert "Runtime size at close:" in closing.body
    assert (
        "debate runtime "
        f"--root {root.resolve()} --channel {opened.channel_name} "
        f"--config {opened.config_path.resolve()}"
    ) in closing.body

    verdicts = {entry.sender: entry for entry in entries if entry.entry_type == "verdict"}
    assert sorted(verdicts) == ["mytool", "othertool"]
    for entry in verdicts.values():
        assert "- runtime-model-basis: declared" in entry.body
        assert "- isolation-flags: declared" in entry.body
        assert "- verification-status: performed" in entry.body
        assert "- verification-evidence-basis: seat-declared" in entry.body
        assert "- seat-process-exit-status: 0" in entry.body
        assert "- adapter-process-exit-status: 0" in entry.body
        for stream in (
            "seat-stdout-sha256",
            "seat-stderr-sha256",
            "adapter-stdout-sha256",
            "adapter-stderr-sha256",
        ):
            marker = f"- {stream}: "
            digest = entry.body.split(marker, 1)[1].splitlines()[0]
            assert len(digest) == 64 and set(digest) <= set("0123456789abcdef")
    assert "- configuration-home: operator (MYTOOL_HOME)" in verdicts["mytool"].body
    assert "- configuration-home: sandbox" in verdicts["othertool"].body

    mytool_calls = _calls(logs["mytool"])
    othertool_calls = _calls(logs["othertool"])
    assert len(mytool_calls) == len(othertool_calls) == 1
    for call in mytool_calls:
        assert call.argv[-2:] == ["--no-config", "--no-history"]
        assert call.config_home == str(home / ".mytool")
    for call in othertool_calls:
        assert call.argv[-2:] == ["--ignore-user-config", "--ephemeral"]
        assert call.config_home is None


# --- final review wave I5: a canary in the SEAT's own words ------------------

# The same stand-in, with one difference: it repeats a token it had no business
# seeing. argv[1] is the call log, argv[2] the token, and the rest the prompt.
LEAKY_VENDOR_CLI = '''\
import json
import os
import sys
from pathlib import Path

log = Path(sys.argv[1])
log.mkdir(parents=True, exist_ok=True)
record = {"argv": sys.argv[3:], "config_home": os.environ.get("MYTOOL_HOME")}
(log / ("call-%d.json" % len(list(log.glob("call-*.json"))))).write_text(
    json.dumps(record), encoding="utf-8"
)
print("While reviewing I also remembered " + sys.argv[2])
print("```json")
print(json.dumps({
    "schema_version": 1,
    "entry_type": "verdict",
    "decision": "PASS",
    "body": "I ran the check the review material asks for and it passed.",
}))
print("```")
'''


def test_a_canary_in_a_wrapped_seats_own_output_rejects_the_invocation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The canary scan has to reach through Debate's own runner.

    The runner echoes everything the seat printed onto its standard error
    precisely so the controller's scan sees the seat's words, not just the
    runner's. This proves that end to end: a stand-in CLI repeats a token that
    exists nowhere in what it was handed, and the invocation is rejected with
    the reason on disk instead of the verdict being published (I5).
    """
    from debate.controller import BrokerController

    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    token = "PRIVATE-user-memory-9f42"
    honest_tool = tmp_path / "fake_vendor_cli.py"
    honest_tool.write_text(FAKE_VENDOR_CLI, encoding="utf-8")
    leaky_tool = tmp_path / "leaky_vendor_cli.py"
    leaky_tool.write_text(LEAKY_VENDOR_CLI, encoding="utf-8")
    logs = {"mytool": tmp_path / "calls-mytool", "othertool": tmp_path / "calls-othertool"}
    rows = {
        "mytool/big": _seat_row(
            [sys.executable, str(leaky_tool), str(logs["mytool"]), token, "{prompt}"],
            vendor="mytool", submodel="big",
            isolation_argv=["--no-config"], no_persistence_argv=["--no-history"],
            config_home=None,
        ),
        "othertool/large": _seat_row(
            [sys.executable, str(honest_tool), str(logs["othertool"]), "{prompt}"],
            vendor="othertool", submodel="large",
            isolation_argv=["--ignore-user-config"], no_persistence_argv=["--ephemeral"],
            config_home=None,
        ),
    }
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
    project, head = _project(tmp_path)
    (project / seats.PROFILE_NAME).write_text(
        json.dumps({"profile_version": 1, "allowlist": ["mytool/big", "othertool/large"]}) + "\n",
        encoding="utf-8",
    )
    home = tmp_path / "home"
    home.mkdir()
    root = project / "collab"

    opened = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=root,
            label="canary",
            pair=("mytool/big", "othertool/large"),
            source_ref=head,
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
        real_home=home,
    )
    # The token exists only here and inside the stand-in's own argv: nothing
    # the controller hands the seat carries it.
    config = json.loads(opened.config_path.read_text(encoding="utf-8"))
    config["contamination_canaries"] = {"user-memory": token}
    opened.config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    assert main([
        "broker-open",
        "--root", str(root),
        "--channel", opened.channel_name,
        "--config", str(opened.config_path),
        "--thread", "does-it-answer-42",
        "--first-seat", "mytool",
        "--refs", f"main@{head[:12]}",
        "--body", "Verify the criterion in the review material against the pinned source.",
    ]) == 0

    loaded = _watcher_config(root, opened.config_path, opened.channel_name)
    broker = loaded.broker
    assert broker is not None
    with pytest.raises(channel.ChannelError, match="profile rejected"):
        BrokerController(broker).capture_sealed(
            channel_root=root,
            channel_name=opened.channel_name,
            party="mytool",
            thread="does-it-answer-42",
            sequence=1,
            attempt=1,
        )

    rejection_path = next(
        broker.runtime_root.glob("cases/does-it-answer-42/invocations/*/rejection.json")
    )
    rejection = json.loads(rejection_path.read_text(encoding="utf-8"))
    assert rejection["reason"] == "contamination-canary-observed"
    assert rejection["canary_label"] == "user-memory"
    assert rejection["party"] == "mytool"
    # Nothing was published: the docket request is still the only entry.
    assert [entry.entry_type for entry in channel.read_entries(root, opened.channel_name)] == [
        "review-request"
    ]
