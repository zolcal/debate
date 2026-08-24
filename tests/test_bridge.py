"""Slice C3: the generic prompt-bridge that wraps a {prompt}-style seat CLI.

Every seat here is a REAL subprocess (a tiny Python script under tmp_path that
records the argv, cwd, environment and stdin it saw), because the whole point
of the module is what the seat process actually receives.
"""

from __future__ import annotations

import builtins
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator

import pytest

from debate import bridge
from debate.__main__ import main


FAKE_SEAT_SOURCE = '''"""A stand-in seat CLI: records its call, then prints what it was told to."""
import json
import os
import sys

record = {
    "argv": sys.argv[1:],
    "cwd": os.getcwd(),
    "stdin": sys.stdin.read(),
    "config_dir": os.environ.get("CLAUDE_CONFIG_DIR"),
    "home": os.environ.get("HOME"),
    "real_home": os.environ.get("DEBATE_BRIDGE_REAL_HOME"),
    "pythonpath": os.environ.get("PYTHONPATH"),
}
with open(os.environ["FAKE_SEAT_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps(record) + "\\n")
sys.stdout.write(os.environ.get("FAKE_SEAT_STDOUT", ""))
sys.stderr.write(os.environ.get("FAKE_SEAT_STDERR", ""))
sys.exit(int(os.environ.get("FAKE_SEAT_EXIT", "0")))
'''


def _verdict_block(decision: str = "PASS", body: str = "I ran the tests and they passed.") -> str:
    payload = {"schema_version": 1, "entry_type": "verdict", "decision": decision, "body": body}
    return "```json\n" + json.dumps(payload, indent=2) + "\n```\n"


class FakeSeat:
    """A real seat CLI subprocess under tmp_path, plus its call log."""

    def __init__(self, script: Path, log: Path, setenv: Callable[[str, str], None]) -> None:
        self.script = script
        self.log = log
        self._setenv = setenv
        self.respond(stdout=_verdict_block())

    @property
    def command(self) -> list[str]:
        return [sys.executable, str(self.script), "--ask", "{prompt}"]

    def respond(self, *, stdout: str = "", stderr: str = "", exit_code: int = 0) -> None:
        self._setenv("FAKE_SEAT_STDOUT", stdout)
        self._setenv("FAKE_SEAT_STDERR", stderr)
        self._setenv("FAKE_SEAT_EXIT", str(exit_code))

    def calls(self) -> list[dict[str, Any]]:
        if not self.log.is_file():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines() if line]

    def prompt(self) -> str:
        calls = self.calls()
        assert len(calls) == 1, calls
        argv = calls[0]["argv"]
        assert isinstance(argv, list)
        return str(argv[1])


@pytest.fixture
def seat(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[FakeSeat]:
    script = tmp_path / "fake-seat.py"
    script.write_text(FAKE_SEAT_SOURCE, encoding="utf-8")
    log = tmp_path / "fake-seat-calls.jsonl"
    monkeypatch.setenv("FAKE_SEAT_LOG", str(log))
    yield FakeSeat(script, log, monkeypatch.setenv)


@dataclass
class Case:
    input_path: Path
    result_path: Path
    source_root: Path
    docket_root: Path
    docket: dict[str, str]

    def sha256(self, relative: str) -> str:
        return hashlib.sha256(self.docket[relative].encode("utf-8")).hexdigest()

    def result(self) -> dict[str, Any]:
        loaded = json.loads(self.result_path.read_text(encoding="utf-8"))
        assert isinstance(loaded, dict)
        return loaded


DEFAULT_DOCKET = {
    "criteria.md": "# The bar\n\nThe suite must be green.\n",
    "notes/extra.md": "A second review file, quoted whole.\n",
}
DEFAULT_TRANSCRIPT = [
    {
        "id": "MSG-4",
        "sender": "alpha",
        "type": "verdict",
        "refs": "branch@abc123",
        "body": "NO_PASS because the migration is untested.",
    },
    {
        "id": "MSG-5",
        "sender": "beta",
        "type": "verdict",
        "refs": "",
        "body": "PASS: I re-ran the suite and it is green.",
    },
]


def _make_case(
    tmp_path: Path,
    *,
    phase: str = "sealed",
    docket: dict[str, str] | None = None,
    transcript: list[dict[str, str]] | None = None,
) -> Case:
    """Write an input.json shaped exactly like the controller's render_input."""
    files = DEFAULT_DOCKET if docket is None else docket
    docket_root = tmp_path / "docket" / "files"
    records: list[dict[str, object]] = []
    for relative, text in files.items():
        target = docket_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        records.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "tracked_at_source_ref": True,
            }
        )
    source_root = tmp_path / "export"
    source_root.mkdir(parents=True, exist_ok=True)
    (source_root / "main.py").write_text("print('hello')\n", encoding="utf-8")
    invocation = tmp_path / "invocation"
    invocation.mkdir(parents=True, exist_ok=True)
    result_path = invocation / "result.json"
    payload: dict[str, object] = {
        "schema_version": 1,
        "phase": phase,
        "thread": "slice-c3",
        "seat": {"party": "alpha", "author_relationship": "independent", "topology": "peer"},
        "source": {"root": str(source_root), "ref": "feature/x", "manifest_sha256": "0" * 64},
        "docket": {"root": str(docket_root), "revision_sha256": "1" * 64, "files": records},
        "result": {
            "path": str(result_path),
            "schema_version": 1,
            "controller_owned_fields": ["sender"],
            "required_fields": ["schema_version", "entry_type", "body", "runtime_model"],
        },
        "instructions": "Inspect the complete pinned source and docket.",
    }
    if phase != "sealed":
        payload["current_thread"] = DEFAULT_TRANSCRIPT if transcript is None else transcript
    input_path = invocation / "input.json"
    input_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return Case(input_path, result_path, source_root, docket_root, dict(files))


def _argv(
    case: Case,
    seat: FakeSeat,
    *,
    isolation: list[str] | None = None,
    no_persistence: list[str] | None = None,
    extra: list[str] | None = None,
) -> list[str]:
    return [
        bridge.SUBCOMMAND,
        "--seat-id",
        "claude:haiku",
        "--vendor",
        "claude",
        "--submodel",
        "haiku",
        "--argv-json",
        json.dumps(seat.command),
        "--isolation-argv-json",
        json.dumps(["--safe-mode"] if isolation is None else isolation),
        "--no-persistence-argv-json",
        json.dumps(["--no-session-persistence"] if no_persistence is None else no_persistence),
        "--isolation-flags-basis",
        "catalogued",
        *(extra or []),
        str(case.input_path),
        str(case.result_path),
    ]


# --- the prompt -------------------------------------------------------------


def test_prompt_quotes_every_docket_file_with_its_path_and_hash(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    assert main(_argv(case, seat)) == 0
    prompt = seat.prompt()
    for relative, text in case.docket.items():
        assert relative in prompt
        assert case.sha256(relative) in prompt
        assert text in prompt


def test_prompt_block_order_is_instruction_docket_source_phase(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path, phase="deliberation")
    assert main(_argv(case, seat)) == 0
    prompt = seat.prompt()
    instruction = prompt.index(bridge.INSTRUCTION_HEADER)
    docket = prompt.index(bridge.DOCKET_HEADER)
    source = prompt.index(bridge.SOURCE_HEADER)
    phase = prompt.index(bridge.TRANSCRIPT_HEADER)
    assert instruction < docket < source < phase


def test_prompt_order_keeps_the_stable_prefix_first(tmp_path: Path, seat: FakeSeat) -> None:
    """O15: the instruction, docket and source blocks -- the material that
    stays the same across a case's calls -- form a byte-identical prefix, so a
    provider prefix cache can reuse it; the pass's stance (and, for a later
    pass, the debate so far) is confined to the last, round-specific block.
    This is a cost feature only; no speedup is claimed or measured here."""
    # Same docket, same source export for both phases -- only "phase" (and the
    # transcript that comes with it) differs, per the O15 contract.
    sealed = _make_case(tmp_path, phase="sealed")
    assert main(_argv(sealed, seat, extra=["--deliberation-input", "full"])) == 0
    sealed_prompt = seat.prompt()
    sealed_payload = json.loads(sealed.input_path.read_text(encoding="utf-8"))

    deliberation_payload = dict(sealed_payload)
    deliberation_payload["phase"] = "deliberation"
    deliberation_payload["current_thread"] = DEFAULT_TRANSCRIPT
    deliberation_input_path = tmp_path / "deliberation-input.json"
    deliberation_input_path.write_text(json.dumps(deliberation_payload, indent=2, sort_keys=True), encoding="utf-8")
    deliberation = Case(
        input_path=deliberation_input_path,
        result_path=tmp_path / "deliberation-result.json",
        source_root=sealed.source_root,
        docket_root=sealed.docket_root,
        docket=sealed.docket,
    )

    seat.log.unlink()
    assert main(_argv(deliberation, seat, extra=["--deliberation-input", "full"])) == 0
    deliberation_prompt = seat.prompt()

    # (a) the four block markers appear in the order instruction < docket <
    # source < phase in both prompts. The phase block itself opens with the
    # pass's stance rather than a "## " header, so it is located by that text.
    for prompt in (sealed_prompt, deliberation_prompt):
        instruction = prompt.index(bridge.INSTRUCTION_HEADER)
        docket = prompt.index(bridge.DOCKET_HEADER)
        source = prompt.index(bridge.SOURCE_HEADER)
        stance = prompt.index("Stance for THIS pass")
        assert instruction < docket < source < stance
    assert bridge.TRANSCRIPT_HEADER not in sealed_prompt
    deliberation_phase = deliberation_prompt.index("Stance for THIS pass")
    assert deliberation_phase < deliberation_prompt.index(bridge.TRANSCRIPT_HEADER)

    # (b) everything before the phase block is byte-identical between the two
    # phases -- the stable prefix a provider could cache across the case.
    sealed_phase = sealed_prompt.index("Stance for THIS pass")
    assert sealed_prompt[:sealed_phase] == deliberation_prompt[:deliberation_phase]

    # The stance itself lives in the phase block, and only there: adversarial
    # for the sealed pass, analytical for the later one -- never both, and
    # never before the phase block starts.
    assert "ADVERSARIALLY" in sealed_prompt[sealed_phase:]
    assert "ADVERSARIALLY" not in sealed_prompt[:sealed_phase]
    assert "ANALYTICALLY" not in sealed_prompt
    assert "ANALYTICALLY" in deliberation_prompt[deliberation_phase:]
    assert "ANALYTICALLY" not in deliberation_prompt[:deliberation_phase]
    assert "ADVERSARIALLY" not in deliberation_prompt

    # The docket and source blocks -- verified directly, not just by position.
    assert bridge._docket_block(sealed_payload) == bridge._docket_block(deliberation_payload)
    assert bridge._source_block(sealed_payload) == bridge._source_block(deliberation_payload)


def test_sealed_prompt_is_adversarial_and_deliberation_is_analytical(tmp_path: Path, seat: FakeSeat) -> None:
    sealed = _make_case(tmp_path / "sealed", phase="sealed")
    assert main(_argv(sealed, seat)) == 0
    assert "ADVERSARIALLY" in seat.prompt()
    assert bridge.TRANSCRIPT_HEADER not in seat.prompt()

    deliberation = _make_case(tmp_path / "deliberation", phase="deliberation")
    seat.log.unlink()
    assert main(_argv(deliberation, seat)) == 0
    prompt = seat.prompt()
    assert "ANALYTICALLY" in prompt
    for entry in DEFAULT_TRANSCRIPT:
        assert entry["id"] in prompt
        assert entry["sender"] in prompt
        assert entry["body"] in prompt


def test_review_modes_change_only_contract_block_and_sealed_stance(tmp_path: Path) -> None:
    case = _make_case(tmp_path, phase="sealed")
    payload = json.loads(case.input_path.read_text(encoding="utf-8"))
    bounded = {
        "review_contract_basis": "recorded",
        "goal": "Verify the retry helper.",
        "review_domain": "retry.py and its tests.",
        "stop_rule": "Stop after the stated checks resolve the criterion.",
    }
    ordinary_payload = {**payload, "review_contract": {**bounded, "review_mode": "ordinary"}}
    release_payload = {
        **payload,
        "review_contract": {**bounded, "review_mode": "release-gate"},
    }
    ordinary = bridge.build_prompt(ordinary_payload, deliberation_input="full")
    release = bridge.build_prompt(release_payload, deliberation_input="full")
    assert bridge.ORDINARY_STANCE in ordinary
    assert bridge.ADVERSARIAL_STANCE not in ordinary
    assert bridge.ADVERSARIAL_STANCE in release
    assert bridge.ORDINARY_STANCE not in release
    ordinary_contract = (
        "Review contract (recorded):\n"
        "- mode: ordinary\n"
        "- goal: Verify the retry helper.\n"
        "- valid domain: retry.py and its tests.\n"
        "- stop rule: Stop after the stated checks resolve the criterion."
    )
    release_contract = ordinary_contract.replace("mode: ordinary", "mode: release-gate")
    assert ordinary_contract in ordinary
    assert release_contract in release
    assert ordinary.replace(ordinary_contract, "<contract>").replace(
        bridge.ORDINARY_STANCE, "<stance>"
    ) == release.replace(release_contract, "<contract>").replace(
        bridge.ADVERSARIAL_STANCE, "<stance>"
    )

    legacy = bridge.build_prompt(payload, deliberation_input="full")
    assert bridge.ADVERSARIAL_STANCE in legacy
    assert "legacy-absent" in legacy
    assert "Verify the retry helper" not in legacy


def test_verdicts_mode_drops_the_review_files_only_in_deliberation(tmp_path: Path, seat: FakeSeat) -> None:
    sealed = _make_case(tmp_path / "sealed", phase="sealed")
    assert main(_argv(sealed, seat, extra=["--deliberation-input", "verdicts"])) == 0
    assert bridge.DOCKET_HEADER in seat.prompt()

    deliberation = _make_case(tmp_path / "deliberation", phase="deliberation")
    seat.log.unlink()
    assert main(_argv(deliberation, seat, extra=["--deliberation-input", "verdicts"])) == 0
    prompt = seat.prompt()
    assert bridge.DOCKET_HEADER not in prompt
    assert DEFAULT_DOCKET["criteria.md"] not in prompt
    assert DEFAULT_TRANSCRIPT[0]["body"] in prompt


def test_full_mode_keeps_the_review_files_in_deliberation(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path, phase="deliberation")
    assert main(_argv(case, seat, extra=["--deliberation-input", "full"])) == 0
    assert DEFAULT_DOCKET["criteria.md"] in seat.prompt()


def test_the_verdicts_prompt_carries_both_published_verdicts_and_the_instruction(
    tmp_path: Path, seat: FakeSeat
) -> None:
    case = _make_case(tmp_path, phase="deliberation")
    assert main(_argv(case, seat, extra=["--deliberation-input", "verdicts"])) == 0
    prompt = seat.prompt()
    for entry in DEFAULT_TRANSCRIPT:
        assert entry["body"] in prompt
    assert "re-verify what is claimed above against fresh evidence" in prompt
    assert bridge.SOURCE_HEADER in prompt
    assert bridge.DOCKET_HEADER not in prompt


def test_the_sealed_prompt_is_the_same_in_both_modes(tmp_path: Path, seat: FakeSeat) -> None:
    """The first pass has nothing to lean on, so the mode may not touch it."""
    case = _make_case(tmp_path, phase="sealed")
    prompts: dict[str, str] = {}
    for mode in ("verdicts", "full"):
        if seat.log.exists():
            seat.log.unlink()
        assert main(_argv(case, seat, extra=["--deliberation-input", mode])) == 0
        prompts[mode] = seat.prompt()
    assert prompts["verdicts"] == prompts["full"]


@pytest.mark.parametrize("mode", ["verdicts", "full"])
def test_the_no_persistence_flags_are_on_every_pass_in_both_modes(
    tmp_path: Path, seat: FakeSeat, mode: str
) -> None:
    for phase in ("sealed", "deliberation"):
        case = _make_case(tmp_path / f"{mode}-{phase}", phase=phase)
        if seat.log.exists():
            seat.log.unlink()
        assert main(_argv(case, seat, extra=["--deliberation-input", mode])) == 0
        assert seat.calls()[0]["argv"][-2:] == ["--safe-mode", "--no-session-persistence"]


@pytest.mark.parametrize("mode,recorded", [("verdicts", "verdicts-only"), ("full", "full-docket")])
def test_a_deliberation_result_records_what_the_seat_read(
    tmp_path: Path, seat: FakeSeat, mode: str, recorded: str
) -> None:
    case = _make_case(tmp_path, phase="deliberation")
    assert main(_argv(case, seat, extra=["--deliberation-input", mode])) == 0
    assert case.result()["deliberation_input"] == recorded


@pytest.mark.parametrize("mode", ["verdicts", "full"])
def test_a_sealed_result_never_records_what_a_later_pass_would_read(
    tmp_path: Path, seat: FakeSeat, mode: str
) -> None:
    case = _make_case(tmp_path, phase="sealed")
    assert main(_argv(case, seat, extra=["--deliberation-input", mode])) == 0
    assert "deliberation_input" not in case.result()


def test_a_later_pass_with_nothing_published_refuses_before_calling_the_seat(
    tmp_path: Path, seat: FakeSeat, capsys: pytest.CaptureFixture[str]
) -> None:
    """Should never happen -- the controller always hands the debate over --
    so if it does, the seat is not asked to review out of thin air."""
    case = _make_case(tmp_path, phase="deliberation", transcript=[])
    assert main(_argv(case, seat, extra=["--deliberation-input", "verdicts"])) == 2
    assert seat.calls() == []
    assert not case.result_path.exists()
    errors = capsys.readouterr().err.strip().splitlines()
    assert len(errors) == 1
    assert errors[0].startswith("refused:")


def _listing(root: Path) -> list[str]:
    return sorted(str(path.relative_to(root)) for path in root.rglob("*"))


@pytest.mark.parametrize("phase", ["sealed", "deliberation"])
def test_nothing_is_written_outside_the_invocation_folder(
    tmp_path: Path, seat: FakeSeat, phase: str
) -> None:
    case = _make_case(tmp_path / phase, phase=phase)
    docket_before = _listing(case.docket_root)
    source_before = _listing(case.source_root)

    assert main(_argv(case, seat, extra=["--deliberation-input", "verdicts"])) == 0

    assert _listing(case.result_path.parent) == [
        "input.json",
        "result.json",
        "seat-stderr.txt",
        "seat-stdout.txt",
    ]
    assert _listing(case.docket_root) == docket_before
    assert _listing(case.source_root) == source_before


def test_oversized_review_material_refuses_before_calling_the_seat(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    case = _make_case(tmp_path, docket={"criteria.md": "x" * 4096})
    monkeypatch.setenv("DEBATE_BRIDGE_INLINE_LIMIT_BYTES", "128")
    assert main(_argv(case, seat)) == 2
    assert seat.calls() == []
    assert not case.result_path.exists()
    errors = capsys.readouterr().err.strip().splitlines()
    assert len(errors) == 1
    assert "too large" in errors[0]


def test_the_default_inline_limit_fits_one_argument(
    tmp_path: Path, seat: FakeSeat, capsys: pytest.CaptureFixture[str]
) -> None:
    """The whole prompt travels as ONE argument, and an operating system caps
    how long a single argument may be (Linux: 128 KiB). A limit above that cap
    can never be reached -- the launch fails first -- so the default sits below
    it (final review wave, C2)."""
    assert bridge.DEFAULT_INLINE_LIMIT_BYTES == 96 * 1024 == 98304
    case = _make_case(tmp_path, docket={"criteria.md": "x" * (bridge.DEFAULT_INLINE_LIMIT_BYTES + 1)})
    assert main(_argv(case, seat)) == 2
    assert seat.calls() == []
    assert not case.result_path.exists()
    errors = capsys.readouterr().err.strip().splitlines()
    assert len(errors) == 1
    assert errors[0] == bridge.MATERIAL_TOO_LARGE_REFUSAL


def test_an_argument_list_too_long_launch_reads_as_the_same_refusal(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The operating system's own cap is the same problem, found one step later:
    the material did not fit. It must not read as a broken seat command."""
    import errno as errno_module

    case = _make_case(tmp_path)

    def _too_long(*_args: object, **_kwargs: object) -> None:
        raise OSError(errno_module.E2BIG, "Argument list too long")

    monkeypatch.setattr(subprocess, "run", _too_long)
    assert main(_argv(case, seat)) == 2
    assert not case.result_path.exists()
    assert not (case.result_path.parent / "seat-failure.json").exists()
    errors = capsys.readouterr().err.strip().splitlines()
    assert len(errors) == 1
    assert errors[0] == bridge.MATERIAL_TOO_LARGE_REFUSAL


def test_any_other_launch_failure_still_reads_as_a_broken_seat_command(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import errno as errno_module

    case = _make_case(tmp_path)

    def _missing(*_args: object, **_kwargs: object) -> None:
        raise OSError(errno_module.ENOENT, "No such file or directory")

    monkeypatch.setattr(subprocess, "run", _missing)
    assert main(_argv(case, seat)) == 2
    errors = capsys.readouterr().err.strip().splitlines()
    assert len(errors) == 1
    assert "cannot start the seat command" in errors[0]


# --- invocation -------------------------------------------------------------


def test_the_seat_is_called_exactly_once(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    assert main(_argv(case, seat)) == 0
    assert len(seat.calls()) == 1


def test_isolation_and_no_persistence_argv_end_every_invocation(tmp_path: Path, seat: FakeSeat) -> None:
    for phase in ("sealed", "deliberation"):
        case = _make_case(tmp_path / phase, phase=phase)
        if seat.log.exists():
            seat.log.unlink()
        assert main(_argv(case, seat, isolation=["--safe-mode", "--strict"], no_persistence=["--no-history"])) == 0
        argv = seat.calls()[0]["argv"]
        assert argv[-3:] == ["--safe-mode", "--strict", "--no-history"]


@pytest.mark.parametrize("flag", ["--isolation-argv-json", "--no-persistence-argv-json"])
def test_an_empty_isolation_or_no_persistence_list_refuses_without_a_seat_call(
    tmp_path: Path, seat: FakeSeat, capsys: pytest.CaptureFixture[str], flag: str
) -> None:
    case = _make_case(tmp_path)
    if flag == "--isolation-argv-json":
        argv = _argv(case, seat, isolation=[])
    else:
        argv = _argv(case, seat, no_persistence=[])
    assert main(argv) == 2
    assert seat.calls() == []
    assert not case.result_path.exists()
    assert len(capsys.readouterr().err.strip().splitlines()) == 1


def test_the_seat_runs_in_the_source_export_with_stdin_closed(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    assert main(_argv(case, seat)) == 0
    call = seat.calls()[0]
    assert Path(call["cwd"]).resolve() == case.source_root.resolve()
    assert call["stdin"] == ""


def test_seat_output_is_forwarded_and_saved_beside_the_result(
    tmp_path: Path, seat: FakeSeat, capsys: pytest.CaptureFixture[str]
) -> None:
    case = _make_case(tmp_path)
    seat.respond(stdout="chatter before\n" + _verdict_block(), stderr="a warning from the seat\n")
    assert main(_argv(case, seat)) == 0
    captured = capsys.readouterr().err
    assert "chatter before" in captured
    assert "a warning from the seat" in captured
    saved_out = (case.result_path.parent / "seat-stdout.txt").read_text(encoding="utf-8")
    saved_err = (case.result_path.parent / "seat-stderr.txt").read_text(encoding="utf-8")
    assert "chatter before" in saved_out
    assert "a warning from the seat" in saved_err


# --- parsing ----------------------------------------------------------------


def test_the_last_fenced_result_block_wins(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    seat.respond(
        stdout=(
            "Here is a draft:\n"
            + _verdict_block("NO_PASS", "draft verdict")
            + "On reflection:\n"
            + _verdict_block("PASS", "final verdict")
        )
    )
    assert main(_argv(case, seat)) == 0
    result = case.result()
    assert result["decision"] == "PASS"
    assert result["body"] == "final verdict"


FENCED_SNIPPET_BODY = "I ran the suite:\n\n```\n618 passed, 1 skipped\n```\n\nSo it is green."
QUOTED_BLOCK_BODY = (
    "The other seat's answer was malformed:\n\n"
    '```json\n{"schema_version": 1, "entry_type": "verdict"}\n```\n\n'
    "so I re-ran the checks myself."
)


@pytest.mark.parametrize("body", [FENCED_SNIPPET_BODY, QUOTED_BLOCK_BODY])
def test_a_body_that_quotes_a_fenced_snippet_survives_intact(
    tmp_path: Path, seat: FakeSeat, body: str
) -> None:
    case = _make_case(tmp_path)
    seat.respond(stdout="Here is my verdict.\n\n" + _verdict_block("PASS", body))
    assert main(_argv(case, seat)) == 0
    result = case.result()
    assert result["decision"] == "PASS"
    assert result["body"] == body


def test_a_malformed_last_block_refuses_instead_of_taking_an_earlier_one(
    tmp_path: Path, seat: FakeSeat, capsys: pytest.CaptureFixture[str]
) -> None:
    case = _make_case(tmp_path)
    seat.respond(
        stdout=(
            _verdict_block("PASS", "first valid, should be superseded")
            + "\nOn reflection:\n"
            + '```json\n{"schema_version": 1, "entry_type": \n```\n'
        )
    )
    assert main(_argv(case, seat)) == 2
    assert not case.result_path.exists()
    errors = [line for line in capsys.readouterr().err.splitlines() if line.startswith("refused:")]
    assert len(errors) == 1


def test_a_block_quoting_a_fence_with_nothing_after_it_still_wins(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    seat.respond(stdout=_verdict_block("NO_PASS", QUOTED_BLOCK_BODY))
    assert main(_argv(case, seat)) == 0
    result = case.result()
    assert result["decision"] == "NO_PASS"
    assert result["body"] == QUOTED_BLOCK_BODY


def test_the_last_block_still_wins_when_an_earlier_body_quotes_a_fence(
    tmp_path: Path, seat: FakeSeat
) -> None:
    case = _make_case(tmp_path)
    seat.respond(
        stdout=(
            "A first attempt:\n"
            + _verdict_block("NO_PASS", FENCED_SNIPPET_BODY)
            + "On reflection:\n"
            + _verdict_block("PASS", "final verdict")
        )
    )
    assert main(_argv(case, seat)) == 0
    result = case.result()
    assert result["decision"] == "PASS"
    assert result["body"] == "final verdict"


def test_an_unfenced_trailing_object_is_accepted(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    seat.respond(
        stdout='noise {"not": "a verdict"} more\n'
        + json.dumps({"schema_version": 1, "entry_type": "verdict", "decision": "NO_PASS", "body": "tests fail"})
    )
    assert main(_argv(case, seat)) == 0
    assert case.result()["decision"] == "NO_PASS"


BAD_OUTPUTS = {
    "no_block": "I could not decide.\n",
    "malformed": "```json\n{\"schema_version\": 1, \"entry_type\": \n```\n",
    "wrong_decision": "```json\n"
    + json.dumps({"schema_version": 1, "entry_type": "verdict", "decision": "MAYBE", "body": "x"})
    + "\n```\n",
    "wrong_entry_type": "```json\n"
    + json.dumps({"schema_version": 1, "entry_type": "info", "decision": "PASS", "body": "x"})
    + "\n```\n",
    "wrong_schema_version": "```json\n"
    + json.dumps({"schema_version": 2, "entry_type": "verdict", "decision": "PASS", "body": "x"})
    + "\n```\n",
    "empty_body": "```json\n"
    + json.dumps({"schema_version": 1, "entry_type": "verdict", "decision": "PASS", "body": "  "})
    + "\n```\n",
    "sender_key": "```json\n"
    + json.dumps(
        {"schema_version": 1, "entry_type": "verdict", "decision": "PASS", "body": "x", "sender": "alpha"}
    )
    + "\n```\n",
}


@pytest.mark.parametrize("label", sorted(BAD_OUTPUTS))
def test_an_unusable_seat_answer_writes_no_result(
    tmp_path: Path, seat: FakeSeat, capsys: pytest.CaptureFixture[str], label: str
) -> None:
    case = _make_case(tmp_path)
    seat.respond(stdout=BAD_OUTPUTS[label])
    assert main(_argv(case, seat)) == 2
    assert not case.result_path.exists()
    errors = [line for line in capsys.readouterr().err.splitlines() if line.startswith("refused:")]
    assert len(errors) == 1


def test_a_failing_seat_without_an_answer_writes_no_result(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    seat.respond(stdout="", stderr="the seat crashed\n", exit_code=3)
    assert main(_argv(case, seat)) == 3
    assert not case.result_path.exists()
    failure = json.loads((case.result_path.parent / "seat-failure.json").read_text())
    assert failure["seat_process_exit_status"] == 3


# --- the result file --------------------------------------------------------


def test_the_result_records_the_declared_model_and_flag_basis(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    seat.respond(stdout=_verdict_block("NO_PASS", "the suite is red"))
    assert main(_argv(case, seat, extra=["--isolation-flags-basis", "declared"])) == 0
    assert case.result() == {
        "schema_version": 1,
        "entry_type": "verdict",
        "decision": "NO_PASS",
        "body": "the suite is red",
        "runtime_model": "haiku",
        "runtime_model_basis": "declared",
        "configuration_home": "sandbox",
        "isolation_flags": "declared",
    }
    assert case.result_path.read_text(encoding="utf-8").endswith("\n")


def test_a_catalogued_basis_is_echoed_as_catalogued(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    assert main(_argv(case, seat)) == 0
    assert case.result()["isolation_flags"] == "catalogued"


# --- the operator's configuration folder ------------------------------------


def _real_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "operator-home"
    (home / ".claude").mkdir(parents=True)
    monkeypatch.setenv("DEBATE_BRIDGE_REAL_HOME", str(home))
    return home


def test_a_config_home_pointer_reaches_the_seat_as_an_environment_variable(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = _real_home(tmp_path, monkeypatch)
    case = _make_case(tmp_path)
    assert main(_argv(case, seat, extra=["--config-home", "CLAUDE_CONFIG_DIR=.claude"])) == 0
    assert seat.calls()[0]["config_dir"] == str(home / ".claude")
    assert case.result()["configuration_home"] == "operator (CLAUDE_CONFIG_DIR)"


def test_without_a_pointer_the_seat_sees_no_vendor_variable(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path / "sandbox-home"))
    case = _make_case(tmp_path)
    assert main(_argv(case, seat)) == 0
    call = seat.calls()[0]
    assert call["config_dir"] is None
    assert call["home"] == str(tmp_path / "sandbox-home")


@pytest.mark.parametrize("pointer", ["HOME=.config", "CLAUDE_CONFIG_DIR=../elsewhere"])
def test_an_unusable_config_home_pointer_refuses_without_a_seat_call(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], pointer: str
) -> None:
    _real_home(tmp_path, monkeypatch)
    case = _make_case(tmp_path)
    assert main(_argv(case, seat, extra=["--config-home", pointer])) == 2
    assert seat.calls() == []
    assert not case.result_path.exists()
    assert len(capsys.readouterr().err.strip().splitlines()) == 1


def test_a_config_home_pointer_without_a_home_location_refuses(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("DEBATE_BRIDGE_REAL_HOME", raising=False)
    case = _make_case(tmp_path)
    assert main(_argv(case, seat, extra=["--config-home", "CLAUDE_CONFIG_DIR=.claude"])) == 2
    assert seat.calls() == []
    assert len(capsys.readouterr().err.strip().splitlines()) == 1


def test_nothing_under_the_operator_home_is_ever_opened(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = _real_home(tmp_path, monkeypatch)
    case = _make_case(tmp_path)

    def _forbidden(target: object) -> None:
        if not isinstance(target, (str, bytes, os.PathLike)):
            return
        path = os.fspath(target)
        if isinstance(path, bytes):
            path = path.decode("utf-8", "replace")
        if path.startswith(str(home)):
            raise AssertionError(f"the seat runner read {path} under the operator's home directory")

    real_open = builtins.open
    real_read_text = Path.read_text
    real_read_bytes = Path.read_bytes

    def guarded_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        _forbidden(file)
        return real_open(file, *args, **kwargs)

    def guarded_read_text(self: Path, *args: Any, **kwargs: Any) -> str:
        _forbidden(self)
        return real_read_text(self, *args, **kwargs)

    def guarded_read_bytes(self: Path) -> bytes:
        _forbidden(self)
        return real_read_bytes(self)

    monkeypatch.setattr(builtins, "open", guarded_open)
    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    try:
        assert main(_argv(case, seat, extra=["--config-home", "CLAUDE_CONFIG_DIR=.claude"])) == 0
    finally:
        monkeypatch.undo()
    assert seat.calls()[0]["config_dir"] == str(home / ".claude")


# --- reading a command back -------------------------------------------------


def test_parse_bridge_command_round_trips_a_command_built_from_the_same_flags(
    tmp_path: Path, seat: FakeSeat
) -> None:
    case = _make_case(tmp_path)
    command = [sys.executable, "-m", "debate", *_argv(case, seat, extra=["--config-home", "CODEX_HOME=.codex"])]
    spec = bridge.parse_bridge_command(command)
    assert spec is not None
    assert spec.seat_id == "claude:haiku"
    assert spec.vendor == "claude"
    assert spec.submodel == "haiku"
    assert list(spec.argv) == seat.command
    assert list(spec.isolation_argv) == ["--safe-mode"]
    assert list(spec.no_persistence_argv) == ["--no-session-persistence"]
    assert spec.config_home == "CODEX_HOME=.codex"
    assert spec.deliberation_input == "full"
    assert spec.isolation_flags_basis == "catalogued"


def test_parse_bridge_command_reads_a_placeholder_command(tmp_path: Path, seat: FakeSeat) -> None:
    case = _make_case(tmp_path)
    flags = _argv(case, seat)[:-2]
    command = [sys.executable, "-m", "debate", *flags, "{input_path}", "{result_path}"]
    spec = bridge.parse_bridge_command(command)
    assert spec is not None
    assert spec.deliberation_input == "full"


@pytest.mark.parametrize(
    "command",
    [
        [sys.executable, "/home/me/seat_adapter.py", "opus", "{input_path}", "{result_path}"],
        [sys.executable, "-m", "debate", "status", "--root", "collab"],
        [sys.executable, "-m", "debate", "bridge", "--seat-id", "claude:haiku"],
        [sys.executable, "-m", "debate", "run-seat", "--seat-id", "claude:haiku"],
        [],
    ],
)
def test_parse_bridge_command_returns_none_for_other_commands(command: list[str]) -> None:
    assert bridge.parse_bridge_command(command) is None


def test_the_subcommand_is_not_advertised_in_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "debate", "--help"],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
        check=True,
    )
    assert "bridge" not in proc.stdout


def test_an_unknown_subcommand_never_names_a_forbidden_word() -> None:
    """The hidden subcommand is kept out of `--help`, but argparse prints the
    whole list of choices when a subcommand is misspelled -- so its NAME is
    user-facing anyway, and it has to be a plain one (final review wave, M1).
    """
    proc = subprocess.run(
        [sys.executable, "-m", "debate", "deffinitely-not-a-command"],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
        check=False,
    )
    combined = (proc.stdout + proc.stderr).lower()
    assert "invalid choice" in combined
    assert "run-seat" in combined
    for word in ("bridge", "brokered", "placeholder"):
        assert word not in combined, combined


def test_the_seat_never_sees_debates_own_pointers(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Two names travel to this process so it can do its job: where Debate is
    installed, and where the operator's home directory is. Neither is any of
    the seat's business, so neither reaches it (final review wave, M7)."""
    home = _real_home(tmp_path, monkeypatch)
    monkeypatch.setenv("PYTHONPATH", str(tmp_path / "somewhere" / "src"))
    case = _make_case(tmp_path)
    assert main(_argv(case, seat, extra=["--config-home", "CLAUDE_CONFIG_DIR=.claude"])) == 0
    call = seat.calls()[0]
    assert call["real_home"] is None
    assert call["pythonpath"] is None
    # The pointer still did its job: the seat was told where its own folder is.
    assert call["config_dir"] == str(home / ".claude")


def test_the_seat_sees_no_pointers_without_a_configuration_folder_either(
    tmp_path: Path, seat: FakeSeat, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DEBATE_BRIDGE_REAL_HOME", str(tmp_path / "operator-home"))
    monkeypatch.setenv("PYTHONPATH", str(tmp_path / "somewhere" / "src"))
    case = _make_case(tmp_path)
    assert main(_argv(case, seat)) == 0
    call = seat.calls()[0]
    assert call["real_home"] is None
    assert call["pythonpath"] is None
