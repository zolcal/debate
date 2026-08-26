"""Run an ordinary prompt-taking CLI as a controller adapter.

The controller (``debate.controller``) drives every seat as a subprocess: it
writes an ``input.json``, runs the seat's recorded command inside a sandboxed
environment with the pinned source export as the working directory, and then
reads a ``result.json`` back. Until now that meant somebody had to hand-write
an adapter script per seat -- the prompt text, the schema, the fail-closed
checks, all copied by hand.

This module is that script, written once and parameterised. It takes a seat
command that has one place for the question (the ``{prompt}`` marker in the
recorded argv), builds the review prompt from the controller's input payload,
runs the seat exactly once, and turns whatever the seat printed into the
controller's result file -- or refuses, writing nothing, with a single plain
line on standard error.

It is deliberately fail-closed. Every check that cannot be satisfied ends the
run with exit status 2 and no result file, so a seat can never be counted as
having reviewed something it did not actually review.
"""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn, Sequence

from . import channel, result_contract, seats, telemetry


# The one place in a recorded seat argv where the question text goes.
PROMPT_MARKER = "{prompt}"

# Where the operator's real home directory is, for seats that are authorised to
# read the operator's own vendor configuration folder. The controller's sandbox
# rewrites HOME, so the location has to be handed in deliberately.
REAL_HOME_ENV = "DEBATE_BRIDGE_REAL_HOME"

# How much review material may be quoted into a prompt. Past this the run is
# refused rather than truncated: a seat that reviews half the material and does
# not know it silently returns a worthless verdict.
INLINE_LIMIT_ENV = "DEBATE_BRIDGE_INLINE_LIMIT_BYTES"
# The whole prompt travels as ONE argument, and an operating system caps how
# long a single argument may be -- 128 KiB on Linux (MAX_ARG_STRLEN). A limit
# above that cap is unreachable: the launch fails with "argument list too long"
# before the limit is ever tested, so the seat sees nothing and the operator
# reads a launch error instead of the real problem. 96 KiB leaves room for the
# rest of the prompt inside the cap (final review wave, C2).
DEFAULT_INLINE_LIMIT_BYTES = 96 * 1024

# One sentence for one problem: the material did not fit in a single argument.
# Both the size check below and the operating system's own refusal of an
# over-long argument list say exactly this.
MATERIAL_TOO_LARGE_REFUSAL = (
    "refused: the review material is too large to send inline; use a custom seat command"
)

# How much of the seat's own output is echoed and kept. The controller scans
# what we print for contamination canaries, so it has to reach it -- but a
# runaway seat must not fill the disk either.
OUTPUT_LIMIT_BYTES = 1024 * 1024

LEGACY_RESULT_SCHEMA_VERSION = result_contract.LEGACY_RESULT_SCHEMA_VERSION
RESULT_SCHEMA_VERSION = result_contract.EVIDENCE_RESULT_SCHEMA_VERSION
CONTRACT_SAFE_RESULT_SCHEMA_VERSION = result_contract.CONTRACT_SAFE_RESULT_SCHEMA_VERSION
DECISIONS = ("PASS", "NO_PASS")
DELIBERATION_INPUTS = ("verdicts", "full")
ISOLATION_FLAG_BASES = ("catalogued", "declared")
VERIFICATION_BASES = ("catalogued", "declared")

# The passes that come after the first, sealed one. Only these record what the
# seat was given to read; the first pass always reads everything.
LATER_PHASES = ("open", "deliberation")

# What the result file says the seat actually read this pass, per mode. The
# record is the reader's, not the flag's, so it names the thing read.
RECORDED_DELIBERATION_INPUT = {"verdicts": "verdicts-only", "full": "full-docket"}

# The only keys a seat's answer block may carry. Anything else -- a 'sender'
# above all, which is the controller's to write -- means the seat answered a
# different question than the one it was asked, so the run is refused.
ANSWER_KEYS = frozenset(
    {"schema_version", "entry_type", "decision", "body", "verification"}
)
LEGACY_ANSWER_KEYS = frozenset({"schema_version", "entry_type", "decision", "body"})

INSTRUCTION_HEADER = "## Your task"
DOCKET_HEADER = "## The review material"
SOURCE_HEADER = "## The code under review"
TRANSCRIPT_HEADER = "## The debate so far"


ADVERSARIAL_STANCE = """Stance for THIS pass (first, sealed pass): work ADVERSARIALLY.
Assume the work is defective until your own evidence proves otherwise. Hunt
contradictions between every rule the work claims to honor and what it actually
does; probe each claim by trying to break it, not by confirming it; a criterion
counts as satisfied only when your attempt to break it failed. The verdict bar is
UNCHANGED: PASS only when every criterion in the review material holds on your own
evidence -- the stance directs your search, never the bar."""

ANALYTICAL_STANCE = """Stance for THIS pass (deliberation): work ANALYTICALLY.
Re-verify every finding now in the debate -- the other seat's AND your own earlier
ones -- against fresh evidence. Retract your own finding when it does not survive
re-verification; adopt the other seat's when it does. Name every judgment call
explicitly instead of passing it silently. The verdict bar is UNCHANGED: PASS only
when every criterion in the review material holds on your own evidence -- the
stance directs your weighing, never the bar."""

ORDINARY_STANCE = """Stance for THIS bounded ordinary pass: try to falsify the
recorded acceptance criteria inside the recorded review domain. Treat observations
outside that domain as non-blocking notes. Make one focused pass and stop at the
recorded stop rule. PASS still requires every in-domain criterion to survive your
own fresh evidence; the bounded stance narrows the search, never the verdict bar."""

ISOLATION_RULES = """Rules for this pass:
- Never read a live debate channel, any parent runtime, user memory, settings,
  hooks, plugins, or MCP servers. Your evidence comes from the material below and
  from the code export, and from nothing else.
- Never write to /tmp. Write nothing outside the folders this run gave you.
- Do not edit the code export. It is the pinned artifact under review.
- Run exactly the verification the review material asks for, using the
  project-local paths already present in your environment.
- Do not include private reasoning in your answer."""

LEGACY_ANSWER_RULES = """End your reply with one fenced json code block and nothing after
it. The block must hold exactly this object, with your own decision and body:

```json
{
  "schema_version": 1,
  "entry_type": "verdict",
  "decision": "PASS",
  "body": "your review, as markdown; never empty"
}
```

Use "PASS" only when your own inspection and your own fresh command output satisfy
every criterion in the review material; otherwise use "NO_PASS" and name the
blocking evidence. The body must cite the exact command you ran and what it
printed. Put no other keys in that block -- not a sender, not a name, nothing."""

ANSWER_RULES = """End your reply with one fenced json code block and nothing after
it. The block must hold exactly this object, with your own decision and body:

```json
{
  "schema_version": 2,
  "entry_type": "verdict",
  "decision": "PASS",
  "body": "your review, as markdown; never empty",
  "verification": {
    "status": "performed",
    "items": [
      {"command": "the exact command", "exit_status": 0, "output": "bounded output excerpt"}
    ]
  }
}
```

Use "PASS" only when your own inspection and your own fresh command output satisfy
every criterion in the review material; otherwise use "NO_PASS" and name the
blocking evidence. The body must cite the exact command you ran and what it
printed. If you genuinely cannot execute verification, use exactly
`{"status":"unable","reason":"..."}` and decide NO_PASS. Read-only inspection
commands count as performed. This evidence is your declaration, not proof supplied
by the schema. Put no other keys in that block -- not a sender, not a name,
nothing."""

CONTRACT_SAFE_ANSWER_RULES = f"""End your reply with one fenced json code block and nothing after
it. The block must hold exactly this object, with your own decision and body:

```json
{{
  "schema_version": 3,
  "entry_type": "verdict",
  "decision": "PASS",
  "body": "your concise review, as markdown; never empty",
  "verification": {{
    "status": "performed",
    "items": [
      {{"command": "the exact command", "exit_status": 0, "output": "bounded output excerpt"}}
    ]
  }}
}}
```

Use "PASS" only when your own inspection and your own fresh command output satisfy
every criterion in the review material; otherwise use "NO_PASS" and name the
blocking evidence. Summarize verification in the body; keep exact commands and
output in the verification object. If you genuinely cannot execute verification,
use exactly `{{"status":"unable","reason":"..."}}` and decide NO_PASS. Read-only
inspection commands count as performed. This evidence is your declaration, not
proof supplied by the schema. {result_contract.contract_rule_lines(3)} Put no
other keys in that block -- not a sender, not a name, nothing."""


class Refusal(Exception):
    """A fail-closed stop: one plain line on standard error, exit status 2."""


class NestedSeatFailure(Exception):
    """The seat process failed: diagnostics exist, no result exists, exit 3."""


@dataclass(frozen=True)
class BridgeSpec:
    """A seat command that this module can run, as recorded in an adapter command."""

    seat_id: str
    vendor: str
    submodel: str
    argv: tuple[str, ...]
    isolation_argv: tuple[str, ...]
    no_persistence_argv: tuple[str, ...]
    verification_argv: tuple[str, ...]
    verification_basis: str | None
    result_schema_version: int
    config_home: str | None
    credential_env: tuple[str, ...]
    deliberation_input: str
    isolation_flags_basis: str


# --- the command line -------------------------------------------------------


def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Define the flags once, so the live command and the reader cannot drift."""
    parser.add_argument("--seat-id", required=True, help="the registry id of the seat being run")
    parser.add_argument("--vendor", required=True, help="the seat's vendor id")
    parser.add_argument("--submodel", required=True, help="the model the seat command pins")
    parser.add_argument(
        "--argv-json",
        required=True,
        metavar="JSON",
        help="the seat's recorded command, as a JSON list of strings",
    )
    parser.add_argument(
        "--isolation-argv-json",
        default="[]",
        metavar="JSON",
        help="verified review-isolation arguments, as a JSON list of strings",
    )
    parser.add_argument(
        "--no-persistence-argv-json",
        default="[]",
        metavar="JSON",
        help="verified arguments that stop the seat keeping a session, as a JSON list of strings",
    )
    parser.add_argument(
        "--verification-argv-json",
        default="[]",
        metavar="JSON",
        help="verified arguments that allow bounded inspection and checks",
    )
    parser.add_argument(
        "--verification-basis",
        default=None,
        choices=VERIFICATION_BASES,
        help="whether verification capability is catalogued or operator-declared",
    )
    parser.add_argument(
        "--result-schema-version",
        type=int,
        default=LEGACY_RESULT_SCHEMA_VERSION,
        choices=(
            LEGACY_RESULT_SCHEMA_VERSION,
            RESULT_SCHEMA_VERSION,
            CONTRACT_SAFE_RESULT_SCHEMA_VERSION,
        ),
        help="the result contract this recorded bridge command speaks",
    )
    parser.add_argument(
        "--config-home",
        default=None,
        metavar="VAR=dir",
        help="let the seat read one folder of the operator's own configuration",
    )
    parser.add_argument(
        "--credential-env-json",
        default="[]",
        metavar="JSON",
        help="code-known credential variable names inherited by this seat",
    )
    parser.add_argument(
        "--deliberation-input",
        default="full",
        choices=DELIBERATION_INPUTS,
        help="whether the later passes repeat the review material or lean on the debate so far",
    )
    parser.add_argument(
        "--isolation-flags-basis",
        required=True,
        choices=ISOLATION_FLAG_BASES,
        help="whether the isolation arguments came from the catalog or from the operator",
    )
    parser.add_argument("input_path", metavar="INPUT_PATH", help="the file the controller wrote for this pass")
    parser.add_argument("result_path", metavar="RESULT_PATH", help="the file the controller expects back")
    return parser


class _SilentParser(argparse.ArgumentParser):
    """An argument parser that raises instead of printing usage and exiting."""

    def error(self, message: str) -> NoReturn:
        raise Refusal(message)

    def exit(self, status: int = 0, message: str | None = None) -> NoReturn:
        raise Refusal(message or "")


def _string_list(raw: str, what: str) -> tuple[str, ...]:
    try:
        value = json.loads(raw)
    except ValueError as error:
        raise Refusal(f"refused: {what} is not readable JSON: {error}") from error
    if not isinstance(value, list) or not all(isinstance(part, str) for part in value):
        raise Refusal(f"refused: {what} must be a list of text arguments")
    return tuple(str(part) for part in value)


def spec_from_arguments(args: argparse.Namespace) -> BridgeSpec:
    credential_env = _string_list(
        str(args.credential_env_json), "the credential environment names"
    )
    try:
        seats.validate_credential_env(list(credential_env))
    except channel.ChannelError as error:
        raise Refusal(str(error)) from error
    return BridgeSpec(
        seat_id=str(args.seat_id),
        vendor=str(args.vendor),
        submodel=str(args.submodel),
        argv=_string_list(str(args.argv_json), "the seat command"),
        isolation_argv=_string_list(str(args.isolation_argv_json), "the isolation arguments"),
        no_persistence_argv=_string_list(str(args.no_persistence_argv_json), "the no-history arguments"),
        verification_argv=_string_list(
            str(args.verification_argv_json), "the verification arguments"
        ),
        verification_basis=(
            str(args.verification_basis) if args.verification_basis is not None else None
        ),
        result_schema_version=int(args.result_schema_version),
        config_home=None if args.config_home is None else str(args.config_home),
        credential_env=credential_env,
        deliberation_input=str(args.deliberation_input),
        isolation_flags_basis=str(args.isolation_flags_basis),
    )


# The hidden subcommand's name on the command line. Kept plain because
# argparse prints the full list of choices when a subcommand is misspelled,
# which puts every registered name in front of a user (final review wave, M1).
SUBCOMMAND = "run-seat"


def _subcommand_index(argv: Sequence[str]) -> int | None:
    """Where the subcommand sits in a full adapter command, if this is one of ours."""
    for index, token in enumerate(argv):
        if token != SUBCOMMAND:
            continue
        head = list(argv[:index])
        if head[-2:] == ["-m", "debate"]:
            return index
        if len(head) == 1 and Path(head[0]).name in ("debate", "debate.exe"):
            return index
    return None


def parse_bridge_command(argv: Sequence[str]) -> BridgeSpec | None:
    """Read a recorded adapter command back into a spec, or ``None`` if it is not ours.

    The doctor and the channel-opening flow use this to answer "what seat does
    this adapter actually run?" without re-deriving the command themselves.
    """
    index = _subcommand_index(argv)
    if index is None:
        return None
    parser = configure_parser(_SilentParser(prog=f"debate {SUBCOMMAND}", add_help=False))
    try:
        return spec_from_arguments(parser.parse_args(list(argv[index + 1:])))
    except (Refusal, SystemExit):
        return None


# --- the prompt -------------------------------------------------------------


def _mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise Refusal(f"refused: this pass was described without its {key} details")
    return value


def _review_contract(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("review_contract")
    if value is None:
        return {
            "review_mode": "release-gate",
            "review_contract_basis": "legacy-absent",
        }
    if not isinstance(value, dict):
        raise Refusal("refused: this pass has unreadable review-contract details")
    return value


def _instruction_block(payload: dict[str, Any]) -> str:
    """Block 1: who the seat is and the rules that hold for every pass alike.

    Phase-independent on purpose -- together with the docket and source blocks
    it forms a byte-identical prefix across a case's calls, so a provider that
    caches a shared prefix can reuse it. The pass's stance (adversarial for the
    sealed pass, analytical for later ones) lives in the phase block instead.
    """
    seat = _mapping(payload, "seat")
    who = (
        f"You are the seat named {seat.get('party', 'unknown')!r} in a two-seat review "
        f"of somebody else's work. Your relationship to the author is "
        f"{seat.get('author_relationship', 'unstated')!r}."
    )
    contract = _review_contract(payload)
    mode = str(contract.get("review_mode", ""))
    basis = str(contract.get("review_contract_basis", ""))
    if mode not in channel.REVIEW_MODES:
        raise Refusal(f"refused: this pass has invalid review mode {mode!r}")
    if basis == "recorded":
        required = {
            name: contract.get(name) for name in ("goal", "review_domain", "stop_rule")
        }
        if any(not isinstance(value, str) or not value.strip() for value in required.values()):
            raise Refusal("refused: this pass has an incomplete recorded review contract")
        contract_text = (
            "Review contract (recorded):\n"
            f"- mode: {mode}\n"
            f"- goal: {required['goal']}\n"
            f"- valid domain: {required['review_domain']}\n"
            f"- stop rule: {required['stop_rule']}"
        )
    elif basis == "legacy-absent" and mode == "release-gate":
        contract_text = (
            "Review contract: legacy-absent. No goal, domain, or stop text was "
            "recorded; retain release-gate adversarial behavior without inventing it."
        )
    else:
        raise Refusal("refused: this pass has an invalid review-contract basis")
    result = _mapping(payload, "result")
    schema_version = result.get("schema_version", LEGACY_RESULT_SCHEMA_VERSION)
    if schema_version not in result_contract.SUPPORTED_RESULT_SCHEMA_VERSIONS:
        raise Refusal(f"refused: this pass requests unknown result schema {schema_version!r}")
    answer_rules = {
        LEGACY_RESULT_SCHEMA_VERSION: LEGACY_ANSWER_RULES,
        RESULT_SCHEMA_VERSION: ANSWER_RULES,
        CONTRACT_SAFE_RESULT_SCHEMA_VERSION: CONTRACT_SAFE_ANSWER_RULES,
    }.get(schema_version)
    if answer_rules is None:
        raise Refusal(f"refused: unsupported result schema version {schema_version}")
    return "\n\n".join(
        [INSTRUCTION_HEADER, who, contract_text, ISOLATION_RULES, answer_rules]
    )


def _inline_limit() -> int:
    raw = os.environ.get(INLINE_LIMIT_ENV)
    if raw is None:
        return DEFAULT_INLINE_LIMIT_BYTES
    try:
        limit = int(raw)
    except ValueError as error:
        raise Refusal(f"refused: the inline size limit {raw!r} is not a whole number of bytes") from error
    if limit <= 0:
        raise Refusal(f"refused: the inline size limit {raw!r} must be greater than zero")
    return limit


def _docket_block(payload: dict[str, Any]) -> str:
    docket = _mapping(payload, "docket")
    root = Path(str(docket.get("root", "")))
    records = docket.get("files")
    if not isinstance(records, list):
        raise Refusal("refused: this pass was described without a list of review files")
    paths: list[tuple[str, str, Path]] = []
    total = 0
    for record in records:
        if not isinstance(record, dict) or "path" not in record:
            raise Refusal("refused: one of the review files was described without its path")
        relative = str(record["path"])
        absolute = root / relative
        try:
            total += absolute.stat().st_size
        except OSError as error:
            raise Refusal(f"refused: cannot read the review file {relative}: {error}") from error
        paths.append((relative, str(record.get("sha256", "")), absolute))
    limit = _inline_limit()
    if total > limit:
        raise Refusal(MATERIAL_TOO_LARGE_REFUSAL)
    sections = [
        DOCKET_HEADER,
        "Every file below is quoted in full. Together they are the criteria your verdict answers to.",
    ]
    for relative, digest, absolute in paths:
        try:
            text = absolute.read_text(encoding="utf-8")
        except OSError as error:
            raise Refusal(f"refused: cannot read the review file {relative}: {error}") from error
        except UnicodeError as error:
            raise Refusal(f"refused: the review file {relative} is not text and cannot be quoted") from error
        sections.append(f"### {relative} (sha256 {digest})\n\n{text}")
    return "\n\n".join(sections)


def _source_block(payload: dict[str, Any]) -> str:
    source = _mapping(payload, "source")
    return "\n\n".join(
        [
            SOURCE_HEADER,
            f"The complete pinned code export is at {source.get('root', '')}. "
            f"It is the state of {source.get('ref', 'the work')} and nothing else; "
            f"its manifest hash is {source.get('manifest_sha256', '')}.",
            "Read it with your own tools -- open files, search it, run the checks the review "
            "material asks for. Do not change it.",
        ]
    )


def _has_transcript(payload: dict[str, Any]) -> bool:
    entries = payload.get("current_thread")
    return isinstance(entries, list) and bool(entries)


def _phase_block(payload: dict[str, Any], phase: str) -> str:
    """Block 4: the part that is NOT shared across a case's calls.

    The pass's stance always goes first (adversarial for the sealed pass,
    analytical for later ones); a later pass with a published debate appends
    it, quoted in full, and the instruction to re-verify it. Kept last, after
    the phase-independent instruction, docket and source blocks, so those
    three form a byte-identical prefix a provider can cache across the case.
    """
    contract = _review_contract(payload)
    ordinary = contract.get("review_mode") == "ordinary"
    sections = [
        (ORDINARY_STANCE if ordinary else ADVERSARIAL_STANCE)
        if phase == "sealed"
        else ANALYTICAL_STANCE
    ]
    if phase != "sealed" and _has_transcript(payload):
        entries = payload["current_thread"]
        sections.append(TRANSCRIPT_HEADER)
        sections.append("These entries are already published. Read every one before you answer.")
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            heading = f"### {entry.get('id', 'entry')} from {entry.get('sender', 'the other seat')}"
            kind = str(entry.get("type", ""))
            refs = str(entry.get("refs", ""))
            if kind:
                heading += f" ({kind})"
            if refs:
                heading += f", about {refs}"
            sections.append(f"{heading}\n\n{entry.get('body', '')}")
        sections.append(
            "Answer with your own verdict for this round: re-verify what is claimed above against "
            "fresh evidence, say plainly what you now retract or adopt, and decide."
        )
    return "\n\n".join(sections)


def _quotes_review_material(phase: str, deliberation_input: str) -> bool:
    """The later passes may lean on the published verdicts instead of the files.

    The first pass always carries the material -- there is nothing else to lean
    on -- so ``verdicts`` only changes the later passes.
    """
    return phase == "sealed" or deliberation_input == "full"


def build_prompt(payload: dict[str, Any], *, deliberation_input: str) -> str:
    """Assemble the seat's prompt: task, material, code -- the stable prefix a
    provider can cache across a case's calls -- then the pass's stance and,
    for a later pass, the debate so far."""
    phase = str(payload.get("phase", ""))
    blocks = [_instruction_block(payload)]
    if _quotes_review_material(phase, deliberation_input):
        blocks.append(_docket_block(payload))
    blocks.append(_source_block(payload))
    if phase != "sealed" and not _has_transcript(payload) and not _quotes_review_material(phase, deliberation_input):
        # Fail closed. Leaning on the debate so far only works when there IS
        # one; with neither the published verdicts nor the review material
        # the seat would be asked to review out of thin air.
        raise Refusal(
            "refused: this pass was told to lean on the debate so far, and the debate "
            "so far is empty"
        )
    blocks.append(_phase_block(payload, phase))
    return "\n\n".join(blocks)


# --- running the seat -------------------------------------------------------


def seat_argv(spec: BridgeSpec, prompt: str) -> list[str]:
    """The seat's own command with the question filled in, plus the verified flags."""
    places = sum(part.count(PROMPT_MARKER) for part in spec.argv)
    if places != 1:
        raise Refusal(
            "refused: this seat's recorded command must have exactly one place for the "
            f"question text, and it has {places}"
        )
    filled = [part.replace(PROMPT_MARKER, prompt) for part in spec.argv]
    return (
        filled
        + list(spec.isolation_argv)
        + list(spec.no_persistence_argv)
        + list(spec.verification_argv)
    )


# What this process was handed to do its own job, and the seat has no use for:
# where Debate itself is installed, and where the operator's home directory is.
# Both are dropped before the seat runs (final review wave, M7).
OUR_OWN_ENV = (REAL_HOME_ENV, "PYTHONPATH")


def seat_environment(spec: BridgeSpec) -> dict[str, str]:
    """This run's own environment -- the controller already sandboxed it -- minus
    what only this process needed, plus one pointer.

    A seat that is authorised to use the operator's own vendor configuration is
    told where it is. Nothing under the operator's home directory is read, listed
    or copied here: only the seat itself ever opens it. The two names that got
    this process going are dropped: the seat neither needs to know where Debate
    is installed nor where the operator's home directory is.
    """
    real_home = os.environ.get(REAL_HOME_ENV, "")
    environment = {
        name: value for name, value in os.environ.items() if name not in OUR_OWN_ENV
    }
    if spec.vendor == "codex":
        environment["DEBATE_ONBOARDING_QUIET"] = "1"
    if spec.config_home is None:
        return environment
    if not real_home:
        raise Refusal(
            "refused: this seat is set up to use a folder in your home directory, but this "
            "run was not told where your home directory is"
        )
    try:
        variable, folder = seats.validate_config_home(spec.config_home, home=Path(real_home))
    except channel.ChannelError as error:
        raise Refusal(str(error)) from error
    if sys.platform == "darwin":
        # macOS keeps the operator's vendor credential in the login Keychain,
        # and the OS resolves that keychain through HOME -- under the
        # controller's sandbox home an operator-configured seat can only print
        # "Not logged in" (field finding F11, 2026-08-26 Mac pass). The
        # config-home authorization directly above already grants this seat
        # the operator's own configuration, so the real HOME widens nothing
        # the profile did not intend.
        environment["HOME"] = real_home
        # The CLI also resolves its credential through USER, which the
        # controller's allowlist strips (field finding F20, established by
        # the field agent's subtractive bisect: the full working environment
        # minus USER alone fails). Derived from the process owner, never
        # from the stripped environment.
        import getpass

        environment.setdefault("USER", getpass.getuser())
        if variable == "CLAUDE_CONFIG_DIR" and folder == Path(real_home) / ".claude":
            # Setting CLAUDE_CONFIG_DIR -- even to the CLI's own default
            # folder -- switches claude to a per-profile credential namespace
            # keyed by the pointer (a SUFFIXED Keychain item; both names were
            # observed side by side in the login keychain), which hides the
            # operator's real login from the seat (field finding F19). With
            # the real HOME restored, the CLI's own default reaches the same
            # folder AND the default Keychain item, so the pointer is omitted
            # exactly when it is redundant.
            return environment
    environment[variable] = str(folder)
    return environment


def run_seat(argv: list[str], *, cwd: str, environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
    """Run the seat exactly once. No retry here: a retry is the controller's call."""
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            env=environment,
            text=True,
            errors="replace",
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # No clock of our own on purpose: the controller already runs this
            # whole process under the case-wide budget and kills it there. A
            # second, shorter clock could only cut a seat off before the
            # controller meant to, and would hide that from the case record.
            timeout=None,
            check=False,
        )
    except OSError as error:
        # The operating system refusing an over-long argument list is the size
        # problem again, caught one step later; it must not read as a broken
        # seat command (final review wave, C2).
        if error.errno == errno.E2BIG:
            raise Refusal(MATERIAL_TOO_LARGE_REFUSAL) from error
        raise Refusal(f"refused: cannot start the seat command: {error}") from error
    except ValueError as error:
        raise Refusal(f"refused: cannot start the seat command: {error}") from error


def _capped(text: str) -> str:
    encoded = text.encode("utf-8", errors="replace")
    if len(encoded) <= OUTPUT_LIMIT_BYTES:
        return text
    kept = encoded[:OUTPUT_LIMIT_BYTES].decode("utf-8", errors="ignore")
    return kept + "\n[the rest of this output was left out: it went past 1 MiB]\n"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def save_seat_output(result_path: Path, completed: subprocess.CompletedProcess[str]) -> None:
    """Echo what the seat printed and keep it beside the result.

    Echoing matters beyond debugging: the controller scans everything this
    process prints for its contamination canaries, so the seat's own words have
    to pass through that scan.
    """
    directory = result_path.parent
    directory.mkdir(parents=True, exist_ok=True)
    output = _capped(completed.stdout)
    errors = _capped(completed.stderr)
    (directory / "seat-stdout.txt").write_text(output, encoding="utf-8")
    (directory / "seat-stderr.txt").write_text(errors, encoding="utf-8")
    print(f"the seat command finished with status {completed.returncode}", file=sys.stderr)
    print("--- what the seat printed ---", file=sys.stderr)
    print(output, file=sys.stderr)
    print("--- what the seat reported as errors ---", file=sys.stderr)
    print(errors, file=sys.stderr)


def redact_seat_output(
    completed: subprocess.CompletedProcess[str],
    *,
    credential_env: tuple[str, ...],
    environment: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    """Redact inherited credentials and their SHA-256 before any output is retained."""
    replacements: list[tuple[str, str]] = []
    for name in credential_env:
        value = environment.get(name, "")
        if not value:
            continue
        replacements.extend(
            [
                (value, f"[redacted credential {name}]"),
                (hashlib.sha256(value.encode("utf-8")).hexdigest(), f"[redacted digest {name}]"),
            ]
        )

    def redact(text: str) -> str:
        for material, replacement in sorted(
            replacements, key=lambda item: len(item[0]), reverse=True
        ):
            text = text.replace(material, replacement)
        return text

    return subprocess.CompletedProcess(
        args=completed.args,
        returncode=completed.returncode,
        stdout=redact(completed.stdout),
        stderr=redact(completed.stderr),
    )


# --- reading the seat's answer ----------------------------------------------


# Only the OPENING fence is matched here, never the closing one. A good verdict
# body quotes what a command printed, and that quote carries fences of its own
# ("```\n618 passed\n```"); a pattern that also matched the closing fence would
# stop at the first fence inside the body and cut the object in half. So the
# fence says where the answer STARTS and the JSON decoder -- which knows a
# string from a delimiter -- finds where it ends.
_OPEN_FENCE = re.compile(r"```[ \t]*json[ \t]*\r?\n", re.IGNORECASE)


def _last_object_after_a_fence(output: str) -> tuple[str, Any, ValueError | None]:
    """Read fenced answer blocks left to right and answer with the LAST one.

    Each decoded block tells us where it ended, so a fence quoted INSIDE it is
    skipped rather than mistaken for the next block -- that is what keeps "the
    last block wins" true for a body that quotes a fenced snippet.

    The last block that was actually ATTEMPTED decides the outcome. A seat that
    prints a draft verdict, thinks again and then botches its final JSON must be
    refused, not credited with the draft it walked away from.
    """
    decoder = json.JSONDecoder()
    fenced = False
    decoded = False
    value: Any = None
    failure: ValueError | None = None
    end_of_last = 0
    for match in _OPEN_FENCE.finditer(output):
        if match.start() < end_of_last:
            # Quoted inside a block we already read: part of that answer's text,
            # not an answer of its own.
            continue
        fenced = True
        start = match.end()
        while start < len(output) and output[start].isspace():
            start += 1
        try:
            candidate, length = decoder.raw_decode(output[start:])
        except ValueError as error:
            # This attempt is the seat's latest word, and it is unreadable.
            failure = error
            decoded = False
            value = None
            continue
        decoded = True
        failure = None
        value = candidate
        end_of_last = start + length
    if decoded:
        return "decoded", value, None
    return ("unreadable" if fenced else "no-fence"), None, failure


def _answer_object(output: str) -> Any:
    outcome, value, failure = _last_object_after_a_fence(output)
    if outcome == "decoded":
        return value
    if outcome == "unreadable":
        raise Refusal(f"refused: the seat's final answer block is not readable JSON: {failure}")
    decoder = json.JSONDecoder()
    for start in range(len(output) - 1, -1, -1):
        if output[start] != "{":
            continue
        try:
            decoded, _ = decoder.raw_decode(output[start:])
        except ValueError:
            continue
        return decoded
    raise Refusal("refused: the seat did not end its reply with an answer block")


def _validated_verification(
    value: object, *, decision: str, schema_version: int = RESULT_SCHEMA_VERSION
) -> dict[str, Any]:
    """Apply the shared versioned evidence contract at the seat boundary."""
    try:
        return result_contract.validate_verification(
            value, decision=decision, schema_version=schema_version
        )
    except result_contract.VerificationContractError as error:
        raise Refusal(f"refused: {error}") from error


def parse_answer_with_verification(
    output: str, *, schema_version: int = LEGACY_RESULT_SCHEMA_VERSION
) -> tuple[str, str, dict[str, Any] | None]:
    """Return ``(decision, body, verification)`` from the seat's words."""
    value = _answer_object(output)
    if not isinstance(value, dict):
        raise Refusal("refused: the seat's answer block is not a single object")
    allowed_keys = (
        ANSWER_KEYS if result_contract.has_verification(schema_version) else LEGACY_ANSWER_KEYS
    )
    extra = sorted(str(key) for key in value if key not in allowed_keys)
    if extra:
        raise Refusal(f"refused: the seat's answer block carries keys that are not its own: {', '.join(extra)}")
    if value.get("schema_version") != schema_version:
        raise Refusal(f"refused: the seat's answer must say schema_version {schema_version}")
    if value.get("entry_type") != "verdict":
        raise Refusal("refused: the seat's answer must be a verdict")
    decision = value.get("decision")
    if decision not in DECISIONS:
        raise Refusal(f"refused: the seat's answer must decide {DECISIONS[0]} or {DECISIONS[1]}")
    body = value.get("body")
    if not isinstance(body, str) or not body.strip():
        raise Refusal("refused: the seat's answer has no review text in it")
    verification = (
        _validated_verification(
            value.get("verification"),
            decision=str(decision),
            schema_version=schema_version,
        )
        if result_contract.has_verification(schema_version)
        else None
    )
    return str(decision), body.strip(), verification


def parse_answer(output: str) -> tuple[str, str]:
    """Backward-compatible v1 answer reader used by legacy bridge tests/callers."""
    decision, body, _verification = parse_answer_with_verification(output)
    return decision, body


def write_result(
    result_path: Path,
    *,
    spec: BridgeSpec,
    decision: str,
    body: str,
    verification: dict[str, Any] | None,
    isolation_flags_basis: str,
    phase: str = "sealed",
) -> None:
    """Write the controller's result file. The controller owns the sender; we never write one."""
    configuration_home = "sandbox"
    if spec.config_home is not None:
        configuration_home = f"operator ({spec.config_home.partition('=')[0]})"
    result: dict[str, Any] = {
        "schema_version": spec.result_schema_version,
        "entry_type": "verdict",
        "decision": decision,
        "body": body,
        "runtime_model": spec.submodel,
        # Declared, never observed: an ordinary CLI does not tell us which model
        # actually answered, so the record says where the name came from.
        "runtime_model_basis": "declared",
        "configuration_home": configuration_home,
        "isolation_flags": isolation_flags_basis,
    }
    if result_contract.has_verification(spec.result_schema_version):
        result["verification"] = verification
        result["verification_basis"] = spec.verification_basis
    if phase in LATER_PHASES:
        # Only the later passes have a choice to record. On the first pass there
        # is nothing but the review material, so saying so would be noise.
        result["deliberation_input"] = RECORDED_DELIBERATION_INPUT[spec.deliberation_input]
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# --- the run ----------------------------------------------------------------


def _read_payload(input_path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise Refusal(f"refused: cannot read what this pass was asked to review: {error}") from error
    if not isinstance(raw, dict):
        raise Refusal("refused: what this pass was asked to review is not a single description")
    return raw


def _run(args: argparse.Namespace) -> int:
    started_ns = time.monotonic_ns()
    spec = spec_from_arguments(args)
    if not spec.isolation_argv or not spec.no_persistence_argv:
        raise Refusal(
            "refused: this seat may only review with its verified isolation and no-history "
            "settings, and this run was given neither in full"
        )
    if result_contract.has_verification(spec.result_schema_version) and spec.verification_basis is None:
        raise Refusal(
            "refused: evidence result schemas need a catalogued or declared verification capability"
        )
    result_path = Path(str(args.result_path))
    phase_telemetry = telemetry.PhaseTelemetry(
        result_path.parent / "bridge-telemetry.jsonl",
        component="bridge",
        started_ns=started_ns,
    )
    payload = _read_payload(Path(str(args.input_path)))
    environment = seat_environment(spec)
    phase = str(payload.get("phase", ""))
    prompt = build_prompt(payload, deliberation_input=spec.deliberation_input)
    argv = seat_argv(spec, prompt)
    source = _mapping(payload, "source")
    phase_telemetry.emit(
        "seat_started",
        seat_id=spec.seat_id,
        phase=phase,
        schema_version=spec.result_schema_version,
    )
    seat_started_ns = time.monotonic_ns()
    completed = run_seat(argv, cwd=str(source.get("root", "")), environment=environment)
    phase_telemetry.emit(
        "seat_finished",
        seat_id=spec.seat_id,
        phase=phase,
        returncode=completed.returncode,
        duration_ms=round((time.monotonic_ns() - seat_started_ns) / 1_000_000, 3),
    )
    completed = redact_seat_output(
        completed, credential_env=spec.credential_env, environment=environment
    )
    save_seat_output(result_path, completed)
    if completed.returncode != 0:
        failure = {
            "schema_version": 1,
            "seat_process_exit_status": completed.returncode,
            "seat_stdout_sha256": _sha256_text(completed.stdout),
            "seat_stderr_sha256": _sha256_text(completed.stderr),
        }
        sidecar = result_path.parent / "seat-failure.json"
        sidecar.write_text(
            json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        raise NestedSeatFailure(
            f"nested seat process exited {completed.returncode}; see {sidecar}"
        )
    parse_started_ns = time.monotonic_ns()
    decision, body, verification = parse_answer_with_verification(
        completed.stdout, schema_version=spec.result_schema_version
    )
    phase_telemetry.emit(
        "result_parsed",
        seat_id=spec.seat_id,
        phase=phase,
        duration_ms=round((time.monotonic_ns() - parse_started_ns) / 1_000_000, 3),
    )
    write_result(
        result_path,
        spec=spec,
        decision=decision,
        body=body,
        verification=verification,
        isolation_flags_basis=spec.isolation_flags_basis,
        phase=phase,
    )
    retained = telemetry.storage_metrics(result_path.parent)
    phase_telemetry.emit(
        "bridge_complete",
        seat_id=spec.seat_id,
        phase=phase,
        file_count=retained.file_count,
        apparent_bytes=retained.apparent_bytes,
        allocated_bytes=retained.allocated_bytes,
    )
    return 0


def run_bridge_command(args: argparse.Namespace) -> int:
    """0 writes a result; 2 is deterministic refusal; 3 is nested-seat failure."""
    try:
        return _run(args)
    except NestedSeatFailure as error:
        print(str(error), file=sys.stderr)
        return 3
    except Refusal as error:
        print(str(error), file=sys.stderr)
        return 2
