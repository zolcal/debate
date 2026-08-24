"""CLI: ``python -m debate <init|post|broker-open|watch-once|status|read|compact>``.

Deliberately stdlib-only and deliberately small: the protocol is the
product; this is just a convenient way to speak it from a shell. Version 1
agents post through ``post``; version 2 adapters return a controller-owned
result file and never self-post. Humans check ``status``, and any scheduler
runs ``watch-once`` every 60s.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from debate import bridge, channel, delta, onboarding, opening, runtime as runtime_state, seats
from debate.controller import (
    SEALED_CONCURRENCY_MODES,
    AdapterProfile,
    BrokerConfig,
    BrokerController,
    TimingPolicy,
    doctor_lines,
)
from debate.watcher import WatcherConfig, read_status, run_once, watch


def _nonnegative_int(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {value}")
    return value


def _positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError(f"must be >= 1, got {value}")
    return value


def _flushing_print(line: str) -> None:
    """Unbuffered emit for the long-lived `watch` loop.

    A redirected stdout is block-buffered, so a healthy watcher writes
    nothing to its log for minutes. That is indistinguishable from a dead
    one, and it was read as death during a real incident. `watch-once` under
    a scheduler does not need this — it exits per tick, and the exit flushes.
    """
    print(line, flush=True)


def _mapping(raw: dict[str, Any], key: str, config_path: Path) -> dict[str, Any]:
    """A config section must be a JSON object; anything else refuses by name."""
    section = raw.get(key, {})
    if not isinstance(section, dict):
        raise channel.ChannelError(
            f"refused: {config_path}: {key!r} must be an object mapping party -> value, "
            f"got {type(section).__name__}"
        )
    return section


def _seconds(raw: dict[str, Any], key: str, default: int, config_path: Path) -> int:
    value = raw.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise channel.ChannelError(f"refused: {config_path}: {key!r} must be a number, got {value!r}")
    try:
        return int(value)
    except (TypeError, ValueError) as error:
        raise channel.ChannelError(
            f"refused: {config_path}: {key!r} must be a whole number of seconds, got {value!r}"
        ) from error


def _watcher_config(
    root: Path,
    config_path: Path,
    channel_name: str | None = None,
    channel_config: channel.ChannelConfig | None = None,
) -> WatcherConfig:
    """Load watcher.json, refusing in the CLI's own vocabulary.

    `main` converts `ChannelError` and NOTHING else, so every other exception
    raised here reaches the operator as a traceback and exit 1. Under the 60s
    timer that is a crash-loop from a hand-edit typo, and it hits `watch`,
    `watch-once` and `watch-status` alike. This file is the one an operator is
    told to copy and edit, so a typo is the EXPECTED input, not an exotic one.

    Same shape as the three unguarded reads fixed in the verify slice
    (doorbell, mailbox, state file), with one real difference that kept it out
    of that slice: those files are written by the program and read back, so a
    torn write corrupts them with no human involved, whereas this one can only
    be broken by hand. It still has to refuse rather than crash. Found at
    MSG-172.
    """
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError as error:
        raise channel.ChannelError(f"refused: cannot read watcher config {config_path}: {error}") from error
    except ValueError as error:  # UnicodeDecodeError
        raise channel.ChannelError(f"refused: watcher config {config_path} is not valid UTF-8: {error}") from error

    try:
        raw = json.loads(text)
    except ValueError as error:
        raise channel.ChannelError(f"refused: watcher config {config_path} is not valid JSON: {error}") from error

    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: watcher config {config_path} must be a JSON object, got {type(raw).__name__}"
        )
    if "state_path" not in raw:
        raise channel.ChannelError(f"refused: watcher config {config_path} has no 'state_path'")

    commands: dict[str, list[str]] = {}
    for party, argv in _mapping(raw, "commands", config_path).items():
        # A bare string is the trap worth naming: list("echo hi") becomes
        # ['e','c','h','o',...], every element a str, so WatcherConfig's
        # all-strings check passes and the failure surfaces only at exec time.
        if isinstance(argv, str) or not isinstance(argv, list):
            raise channel.ChannelError(
                f"refused: {config_path}: command for {party!r} must be a list of arguments "
                f'(e.g. ["/path/to/agent", "{{prompt}}"]), got {type(argv).__name__}'
            )
        if not argv:
            raise channel.ChannelError(
                f"refused: {config_path}: command for {party!r} is empty; omit the party instead "
                "of configuring one that can never be invoked"
            )
        commands[party] = list(argv)

    # The round-6 gate seam: `open` supplies the in-memory record it will
    # write verbatim after validation, because a freshly minted channel has
    # no record on disk yet. Every other caller omits it and reads the disk.
    if channel_config is None:
        channel_config = channel.load_config(root, channel_name)
    broker: BrokerConfig | None = None
    adapter_raw = _mapping(raw, "adapters", config_path)
    if adapter_raw:
        if channel_config.name is None or channel_config.project is None:
            raise channel.ChannelError(
                "refused: a fully managed channel must be named and bound to a project"
            )
        for required in ("runtime_root", "source_ref", "whole_case_timeout_seconds"):
            if required not in raw:
                raise channel.ChannelError(
                    f"refused: the fully managed watcher config {config_path} has no {required!r}"
                )
        profiles = {
            str(party): AdapterProfile.from_mapping(str(party), profile)
            for party, profile in adapter_raw.items()
        }
        if set(profiles) != set(channel_config.parties):
            raise channel.ChannelError(
                "refused: adapter profile names must exactly match the addressed channel parties"
            )
        docket_files_raw = raw.get("docket_files", [])
        if not isinstance(docket_files_raw, list) or not all(
            isinstance(item, str) for item in docket_files_raw
        ):
            raise channel.ChannelError(f"refused: {config_path}: 'docket_files' must be a list of paths")
        canaries_raw = raw.get("contamination_canaries", {})
        if not isinstance(canaries_raw, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in canaries_raw.items()
        ):
            raise channel.ChannelError(
                f"refused: {config_path}: 'contamination_canaries' must map labels to strings"
            )
        sealed_concurrency = raw.get("sealed_concurrency", "concurrent")
        if sealed_concurrency not in SEALED_CONCURRENCY_MODES:
            raise channel.ChannelError(
                f"refused: {config_path}: 'sealed_concurrency' must be \"concurrent\" (ask both seats "
                f"at the same time) or \"sequential\" (one seat at a time), got {sealed_concurrency!r}"
            )
        # Informational for now -- no engine decision reads it -- but it is a
        # hand-editable number in a hand-editable file, so a typo refuses here
        # rather than reaching whatever reads it next.
        quick_review_max_bytes = raw.get("quick_review_max_bytes", opening.QUICK_REVIEW_MAX_BYTES)
        if (
            isinstance(quick_review_max_bytes, bool)
            or not isinstance(quick_review_max_bytes, int)
            or quick_review_max_bytes < 1
        ):
            raise channel.ChannelError(
                f"refused: {config_path}: 'quick_review_max_bytes' must be a whole number of "
                f"bytes above zero, got {quick_review_max_bytes!r}"
            )
        review_keys = {
            "review_mode", "review_contract_basis", "goal", "review_domain", "stop_rule"
        }
        present_review_keys = review_keys.intersection(raw)
        if present_review_keys and present_review_keys != review_keys:
            raise channel.ChannelError(
                f"refused: {config_path}: partial review contract; missing "
                f"{', '.join(sorted(review_keys - present_review_keys))}"
            )
        if present_review_keys and not all(
            isinstance(raw[key], str) for key in review_keys
        ):
            raise channel.ChannelError(
                f"refused: {config_path}: review contract fields must be strings"
            )
        review_mode: str
        review_contract_basis: str
        goal: str | None
        review_domain: str | None
        stop_rule: str | None
        if present_review_keys:
            review_mode = str(raw["review_mode"])
            review_contract_basis = str(raw["review_contract_basis"])
            goal = str(raw["goal"])
            review_domain = str(raw["review_domain"])
            stop_rule = str(raw["stop_rule"])
        else:
            review_mode = "release-gate"
            review_contract_basis = "legacy-absent"
            goal = review_domain = stop_rule = None
        channel_contract = (
            channel_config.review_mode,
            channel_config.review_contract_basis,
            channel_config.goal,
            channel_config.review_domain,
            channel_config.stop_rule,
        )
        watcher_contract = (
            review_mode, review_contract_basis, goal, review_domain, stop_rule
        )
        if channel_contract != watcher_contract:
            raise channel.ChannelError(
                "refused: watcher review contract does not match the channel record"
            )
        ordered_profiles = (profiles[channel_config.parties[0]], profiles[channel_config.parties[1]])
        timing = TimingPolicy(
            thread_cap=channel_config.thread_cap,
            scheduler_interval_seconds=_seconds(raw, "scheduler_interval_seconds", 60, config_path),
            retry_seconds=_seconds(raw, "retry_seconds", 1800, config_path),
            whole_case_timeout_seconds=_seconds(raw, "whole_case_timeout_seconds", 0, config_path),
            profiles=ordered_profiles,
        )
        broker = BrokerConfig(
            repository_root=Path(channel_config.project),
            runtime_root=Path(str(raw["runtime_root"])).expanduser(),
            source_ref=str(raw["source_ref"]),
            profiles=profiles,
            timing=timing,
            config_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            docket_files=tuple(docket_files_raw),
            contamination_canaries={str(key): str(value) for key, value in canaries_raw.items()},
            sealed_concurrency=str(sealed_concurrency),
            review_mode=review_mode,
            review_contract_basis=review_contract_basis,
            goal=goal,
            review_domain=review_domain,
            stop_rule=stop_rule,
        )
    return WatcherConfig(
        channel_root=root,
        channel_name=channel_name,
        state_path=Path(str(raw["state_path"])).expanduser(),
        commands=commands,
        prompts={k: str(v) for k, v in _mapping(raw, "prompts", config_path).items()},
        debounce_seconds={
            k: _seconds({k: v}, k, 0, config_path)
            for k, v in _mapping(raw, "debounce_seconds", config_path).items()
        },
        retry_seconds=_seconds(raw, "retry_seconds", 1800, config_path),
        timeout_seconds=_seconds(raw, "timeout_seconds", 1800, config_path),
        managed_version=channel_config.managed_version,
        parties=channel_config.parties,
        broker=broker,
    )


def _watch_interval(explicit: int | None, config: WatcherConfig) -> int:
    """The watch loop's tick cadence: explicit flag > the brokered config's
    scheduler_interval_seconds > the 180s legacy default.

    Round-10 gate finding (2026-08-20): the brokered open wrote a snappy
    scheduler_interval_seconds that NO scheduler read -- the interactive
    product path idled on this loop's own default. The config value is now
    the loop's default, so an interactive debate ticks at the cadence its
    open declared, and cron deployments still pin --interval explicitly.
    """
    if explicit is not None:
        return explicit
    if config.broker is not None:
        return max(1, int(config.broker.timing.scheduler_interval_seconds))
    return 180


# Verdicts that mean "a human should look now". Exit 4 matches `watch()`'s
# escalation code, so an alerting scheduler treats both the same way.
_NEEDS_ATTENTION = ("STALE", "ESCALATED", "INVALID", "ERROR")


def _watch_status_report(root: Path, config_path: Path, grace: int, channel_name: str | None = None) -> int:
    """Print one channel's liveness. Reads only — creates nothing, locks nothing."""
    lines, result = read_status(
        _watcher_config(root, config_path, channel_name), datetime.now(timezone.utc), grace_seconds=grace
    )
    for line in lines:
        print(line)
    print(f"\n{result.verdict}: {result.detail}")
    return 4 if result.verdict in _NEEDS_ATTENTION else 0


def _project_relative(project_root: Path, raw: str, label: str) -> str:
    """One project-relative path, or a refusal naming what the caller gave."""
    candidate = Path(raw).expanduser()
    absolute = candidate if candidate.is_absolute() else (project_root / candidate)
    try:
        resolved = absolute.resolve()
    except OSError as error:  # pragma: no cover - only a broken symlink loop reaches this
        raise channel.ChannelError(f"refused: cannot resolve {label} {raw!r}: {error}") from error
    if resolved == project_root or not resolved.is_relative_to(project_root):
        raise channel.ChannelError(
            f"refused: {label} {raw!r} is outside the project {project_root}"
        )
    return resolved.relative_to(project_root).as_posix()


def _delta_round_docket(
    args: argparse.Namespace, config: BrokerConfig, channel_root: Path, channel_name: str
) -> tuple[Path, tuple[str, ...], Callable[[], None]]:
    """Compose the round docket, then put its inputs in front of the seats.

    Every refusal below runs BEFORE the first byte is written: half a round --
    a docket on disk that the config does not carry, or a config naming a file
    that was never written -- is worse than no round at all. The order is
    read-everything, refuse, then write the docket and the config together.

    The refusals here are not the only ones the round can meet: `revise_case`
    has its own (a stuck half-finished revision, a changed profile, topology or
    deadline, a case manifest that is gone), and those fire AFTER these two
    writes. So the third return value undoes them -- caller's job to call it
    when the recording fails -- and the round is all-or-nothing either way.
    """
    if args.goal is None or not args.goal.strip():
        raise channel.ChannelError(
            "refused: a fold-delta round needs --goal, the one sentence saying what this round verifies"
        )
    if args.fold_list_file is None:
        raise channel.ChannelError(
            "refused: a fold-delta round needs --fold-list-file, the author's own list of folds"
        )
    if not args.prior:
        raise channel.ChannelError(
            "refused: a fold-delta round needs at least one --prior CURRENT=PRIOR, so the seats "
            "can diff the artifact against the version they reviewed last round"
        )
    project = config.repository_root.resolve()
    try:
        fold_list = Path(args.fold_list_file).read_text(encoding="utf-8")
    except (OSError, ValueError) as error:
        raise channel.ChannelError(
            f"refused: cannot read the fold list {args.fold_list_file}: {error}"
        ) from error

    known = [_project_relative(project, item, "docket file") for item in config.docket_files]
    pairs: list[tuple[str, str]] = []
    for raw in args.prior:
        current_raw, separator, prior_raw = str(raw).partition("=")
        if not separator or not current_raw.strip() or not prior_raw.strip():
            raise channel.ChannelError(
                f"refused: --prior wants CURRENT=PRIOR, two paths joined by '=', got {raw!r}"
            )
        current = _project_relative(project, current_raw.strip(), "the current version")
        prior = _project_relative(project, prior_raw.strip(), "the prior version")
        if not (project / prior).is_file():
            raise channel.ChannelError(f"refused: the prior version {prior} does not exist")
        if not (project / current).is_file():
            raise channel.ChannelError(f"refused: the current version {current} does not exist")
        if current not in known:
            raise channel.ChannelError(
                f"refused: {current} is not one of this case's docket_files, so the seats never "
                "see it; add it to the config's docket_files first"
            )
        # Two pairs for one artifact would put two different "prior versions"
        # in the same docket and one diff in the true change set: the seat
        # could not tell which version the round is measured against.
        if any(current == seen for seen, _prior in pairs):
            raise channel.ChannelError(
                f"refused: --prior names {current} twice; one artifact has one prior version"
            )
        if current == prior:
            raise channel.ChannelError(
                f"refused: --prior gives {current} as its own prior version, so the diff would be "
                "empty; name the file holding the version the last round reviewed"
            )
        pairs.append((current, prior))

    entries = {
        f"MSG-{entry.seq}": entry
        for entry in channel.thread_entries(channel_root, args.thread, channel_name)
    }
    verdicts: list[tuple[str, str]] = []
    for raw_id in args.prior_verdicts:
        entry_id = str(raw_id).strip()
        entry = entries.get(entry_id)
        if entry is None:
            raise channel.ChannelError(
                f"refused: {entry_id} is not an entry of thread {args.thread!r} on this channel"
            )
        if entry.entry_type != "verdict":
            raise channel.ChannelError(
                f"refused: {entry_id} is a {entry.entry_type!r} entry, not a verdict; "
                "--prior-verdict cites the verdicts this round's folds answer"
            )
        verdicts.append((entry_id, entry.body))

    if args.docket_out is not None:
        relative = _project_relative(project, str(args.docket_out), "the docket to write")
        if (project / relative).exists():
            raise channel.ChannelError(
                f"refused: {relative} already exists; a written round docket is evidence, so name "
                "a free path rather than overwriting it"
            )
    else:
        runtime_relative = config.runtime_root.resolve().relative_to(project.resolve())
        number = 1
        while (
            project
            / runtime_relative
            / f"delta-docket-{args.thread}-{number}.md"
        ).exists():
            number += 1
        relative = str(
            runtime_relative / f"delta-docket-{args.thread}-{number}.md"
        )

    diffs: dict[str, str] = {}
    for current, prior in pairs:
        try:
            prior_text = (project / prior).read_text(encoding="utf-8")
            current_text = (project / current).read_text(encoding="utf-8")
        except (OSError, ValueError) as error:
            raise channel.ChannelError(
                f"refused: cannot read {prior} and {current} as text: {error}"
            ) from error
        diffs[current] = delta.unified_diff(
            prior_text, current_text, prior_path=prior, current_path=current
        )
    text = delta.compose_docket(
        delta.DeltaRound(
            goal=args.goal,
            fold_list=fold_list,
            priors=tuple(pairs),
            prior_verdicts=tuple(verdicts),
        ),
        diffs=diffs,
    )

    additions: list[str] = []
    for path in [prior for _current, prior in pairs] + [relative]:
        if path not in known and path not in additions:
            additions.append(path)

    destination = project / relative
    config_path = Path(args.config)
    # Captured BEFORE the write, so the undo restores the operator's file byte
    # for byte -- not a re-serialization of what we think it held.
    original_config = config_path.read_bytes()
    parent_existed = destination.parent.exists()

    def rollback() -> None:
        """Undo exactly this run's two writes, and nothing else.

        The docket file is always this run's own: an existing --docket-out is
        refused above and the default takes the next free number. The
        materialized prior versions are NOT ours -- they are the author's files,
        named on the command line -- so they stay.
        """
        config_path.write_bytes(original_config)
        try:
            destination.unlink()
        except FileNotFoundError:  # pragma: no cover - only a concurrent remove
            pass
        if not parent_existed:
            try:
                destination.parent.rmdir()
            except OSError:  # pragma: no cover - something else landed in it
                pass

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    _add_docket_files(config_path, additions)
    return destination, tuple(additions), rollback


def _add_docket_files(config_path: Path, additions: list[str]) -> None:
    """Append the round's new files to the config, keeping the author's order.

    The file was already parsed once by `_watcher_config`, so this rereads a
    known-good JSON object and rewrites it with the same key order: an operator
    editing this file by hand should find it where they left it.
    """
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    listed = [str(item) for item in raw.get("docket_files", [])]
    for item in additions:
        if item not in listed:
            listed.append(item)
    raw["docket_files"] = listed
    config_path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="debate", description=__doc__)
    # metavar: the auto-generated choices line would list every subcommand,
    # including the hidden one below, which is the one thing it must not do.
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    def add_channel_flag(sub_parser: argparse.ArgumentParser) -> None:
        sub_parser.add_argument(
            "--channel",
            default=None,
            metavar="ID",
            help="channel instance id; needed only when the root folder holds more than one channel",
        )

    p_seats = sub.add_parser(
        "seats",
        help="the host seat registry: discover what this machine can seat",
    )
    seats_sub = p_seats.add_subparsers(dest="seats_command", required=True)
    p_seats_discover = seats_sub.add_parser(
        "discover", help="catalog x PATH scan merged into the registry; no model calls"
    )
    p_seats_discover.add_argument("--json", action="store_true", dest="as_json")
    p_seats_list = seats_sub.add_parser("list", help="print the registry")
    p_seats_list.add_argument("--json", action="store_true", dest="as_json")
    p_seats_check = seats_sub.add_parser(
        "check",
        help="session-start freshness: exit 3 = real breakage only (missing binary, failed smoke)",
    )
    p_seats_check.add_argument("--json", action="store_true", dest="as_json")
    p_seats_doctor = seats_sub.add_parser(
        "doctor", help="re-validate everything; offers a smoke refresh per stale seat"
    )
    p_seats_doctor.add_argument("--json", action="store_true", dest="as_json")
    p_seats_smoke = seats_sub.add_parser(
        "smoke", help="scratch-channel round trip per named seat: ONE model call each, confirmed first"
    )
    p_seats_smoke.add_argument("seat_ids", nargs="+", metavar="SEAT")
    p_seats_smoke.add_argument(
        "--yes", action="store_true", dest="assume_yes",
        help="auto-confirm the announced model spend",
    )
    p_seats_add = seats_sub.add_parser(
        "add", help="manual seat, an appended endpoint option, or a SEAT@EFFORT derivation"
    )
    p_seats_add.add_argument("seat_id", metavar="SEAT")
    p_seats_add.add_argument(
        "--command",
        dest="seats_add_command_text",
        default=None,
        help="seat argv, e.g. '/home/me/.local/bin/my-agent {prompt}'; omit for @EFFORT derivations",
    )
    p_seats_add.add_argument(
        "--cost-mode",
        dest="seats_add_cost_mode",
        default="unknown",
        choices=("subscription", "api", "local", "unknown"),
        help="who pays when this seat runs; declared by you, shown before every spend",
    )
    p_seats_add.add_argument(
        "--capability-class",
        dest="seats_add_capability_class",
        default=None,
        choices=("frontier", "light"),
        help="how capable this seat is, declared by you",
    )
    p_seats_add.add_argument(
        "--isolation-argv",
        dest="seats_add_isolation_argv",
        default=None,
        metavar="ARGS",
        help="extra arguments that make this tool ignore its user settings, plugins and hooks while it reviews "
             "(if the arguments start with a dash, write --isolation-argv=ARGS)",
    )
    p_seats_add.add_argument(
        "--no-persistence-argv",
        dest="seats_add_no_persistence_argv",
        default=None,
        metavar="ARGS",
        help="extra arguments that stop this tool from saving a session to disk "
             "(if the arguments start with a dash, write --no-persistence-argv=ARGS)",
    )
    p_seats_add.add_argument(
        "--config-home",
        dest="seats_add_config_home",
        default=None,
        metavar="VAR=dir",
        help="the tool's documented configuration variable and its folder under your home, "
             "e.g. CLAUDE_CONFIG_DIR=.claude",
    )
    p_seats_add.add_argument(
        "--verification-capable",
        action="store_true",
        dest="seats_add_verification_capable",
        help="declare that this seat can inspect the pinned export and run bounded checks",
    )
    p_seats_add.add_argument(
        "--verification-argv",
        dest="seats_add_verification_argv",
        default=None,
        metavar="ARGS",
        help="documented arguments that enable bounded inspection/check tools; requires "
        "--verification-capable (use --verification-argv=ARGS when ARGS starts with a dash)",
    )
    p_seats_add.add_argument(
        "--result-schema-version",
        dest="seats_add_result_schema_version",
        type=int,
        choices=(1, 2),
        default=None,
        help="result protocol spoken by a hand-authored file adapter; v2 is required for new product opens",
    )
    p_seats_add.add_argument(
        "--credential-env",
        action="append",
        default=[],
        dest="seats_add_credential_env",
        metavar="NAME",
        help="code-known credential variable name to inherit only when this seat launches; repeatable",
    )
    p_seats_setcost = seats_sub.add_parser(
        "set-cost-mode",
        help="declare who pays for an existing seat (catalog, derived, or manual)",
    )
    p_seats_setcost.add_argument("seat_id", metavar="SEAT")
    p_seats_setcost.add_argument(
        "cost_mode", metavar="MODE", choices=("subscription", "api", "local", "unknown")
    )
    p_seats_remove = seats_sub.add_parser(
        "remove",
        help="remove a manual, derived, or absent catalog seat",
        description=(
            "Remove a seat from the registry. Manual (operator-authored), "
            "derived (@effort entries the tool derived) and ABSENT catalog "
            "seats are all removable -- the first is yours, the others are "
            "recreatable by discovery. A PRESENT catalog seat is refused: "
            "discovery owns it, and removing it would only invite the next "
            "scan to put it back."
        ),
    )
    p_seats_remove.add_argument("seat_id", metavar="SEAT")

    p_onboarding = sub.add_parser(
        "onboarding",
        help="installation-driven product path: project onboarding state (used by the plugin)",
    )
    onboarding_sub = p_onboarding.add_subparsers(dest="onboarding_command", required=True)
    p_onb_status = onboarding_sub.add_parser(
        "status",
        help="read-only onboarding state for one project; writes nothing, calls no model",
    )
    p_onb_status.add_argument(
        "--project", required=True, metavar="ABSOLUTE_PATH",
        help="absolute project root the host session runs in",
    )
    p_onb_status.add_argument("--json", action="store_true", dest="as_json")
    p_onb_inspect = onboarding_sub.add_parser(
        "inspect",
        help="in-memory catalog x PATH discovery; sanitized candidates + revision; writes nothing",
    )
    p_onb_inspect.add_argument("--project", required=True, metavar="ABSOLUTE_PATH")
    p_onb_inspect.add_argument("--json", action="store_true", dest="as_json")
    p_onb_approve = onboarding_sub.add_parser(
        "approve",
        help="record the user's seat approval: transactional registry + project profile write",
    )
    p_onb_approve.add_argument("--project", required=True, metavar="ABSOLUTE_PATH")
    p_onb_approve.add_argument(
        "--candidate-revision", required=True, dest="candidate_revision", metavar="HASH",
        help="the revision inspect returned; a changed candidate set is refused",
    )
    p_onb_approve.add_argument(
        "--allow", action="append", required=True, dest="allow", metavar="SEAT",
        help="approved seat id (repeatable)",
    )
    p_onb_approve.add_argument(
        "--confirmed", action="store_true",
        help="assert the user answered the approval question in the current turn",
    )
    p_onb_approve.add_argument(
        "--accept-policy",
        action="append",
        default=[],
        dest="accepted_policies",
        metavar="SEAT=REVISION",
        help="accept the exact displayed data-policy revision for one selected seat; repeatable",
    )
    p_onb_approve.add_argument("--json", action="store_true", dest="as_json")

    p_open = sub.add_parser(
        "open",
        help="mint a debate: a fresh channel with its pair picked from the registry",
    )
    p_open.add_argument("--root", type=Path, default=Path("."))
    p_open.add_argument("--label", required=True, help="the debate's subject slug")
    p_open.add_argument(
        "--pair",
        default=None,
        help="two comma-separated seat ids, e.g. codex/gpt-5.6-sol,glm/glm-5.3",
    )
    p_open.add_argument("--supervisor", default="owner")
    p_open.add_argument(
        "--cap", type=int, default=None, dest="thread_cap",
        help="maximum entries in one thread (ordinary product reviews require 5; "
        "release gates and legacy opens default to 12)",
    )
    p_open.add_argument(
        "--yes",
        action="store_true",
        dest="assume_yes",
        help="non-interactive: accept the last-pair default; covers the unsmoked "
        "warning, never the identity guard",
    )
    p_open.add_argument(
        "--allow-identical-seats",
        action="store_true",
        help="seat the same vendor/submodel twice anyway (a monologue risk, "
        "always an explicit choice)",
    )
    p_open.add_argument(
        "--allow-mismatched-pair",
        action="store_true",
        help="seat a lightweight model against a frontier model anyway -- Debate warns "
        "because such pairs often produce one-sided verdicts",
    )
    p_open.add_argument(
        "--brokered",
        action="store_true",
        help="open a fully managed debate: the two seats run under Debate's control with "
        "you as supervisor; requires --pair and project approval",
    )
    p_open.add_argument(
        "--goal", default=None,
        help="fully managed debates only: the concrete outcome this review must establish",
    )
    p_open.add_argument(
        "--review-domain", default=None, dest="review_domain",
        help="fully managed debates only: the valid input/artifact boundary",
    )
    p_open.add_argument(
        "--stop-rule", default=None, dest="stop_rule",
        help="fully managed debates only: when this bounded review must stop",
    )
    p_open.add_argument(
        "--review-mode", default="ordinary", choices=channel.REVIEW_MODES,
        dest="review_mode",
        help="fully managed debates only: bounded ordinary review (default) or exhaustive release gate",
    )
    p_open.add_argument(
        "--source-ref",
        default=None,
        dest="source_ref",
        metavar="SHA",
        help="fully managed debates only: the commit the seats review "
        "(default: the project repository's latest commit)",
    )
    p_open.add_argument(
        "--docket-file",
        action="append",
        default=[],
        dest="docket_files",
        metavar="PROJECT_RELATIVE_PATH",
        help="fully managed debates only: a review input copied into the case "
        "material (repeatable)",
    )
    p_open.add_argument(
        "--quick-review-max-bytes",
        type=_positive_int,
        default=opening.QUICK_REVIEW_MAX_BYTES,
        dest="quick_review_max_bytes",
        metavar="BYTES",
        help="how much review material still counts as a small review; below this "
        "a quick pair is suggested, at or above it the strongest pair "
        "(default: 16384, and recorded with the debate)",
    )
    p_open.add_argument(
        "--deliberation-input",
        default="verdicts",
        choices=("verdicts", "full"),
        dest="deliberation_input",
        help="what a seat re-reads in the discussion round: just the two verdicts "
        "(default, faster) or the whole review material again",
    )
    p_open.add_argument(
        "--author-vendor",
        default=None,
        dest="author_vendor",
        metavar="VENDOR",
        help="fully managed debates only, required: the vendor of the tool "
        "you are running in (e.g. 'claude' or 'codex'); a seat sharing it is "
        "recorded author-affiliated",
    )

    p_init = sub.add_parser("init", help="create a channel directory")
    p_init.add_argument("--root", type=Path, default=Path("."))
    p_init.add_argument("--parties", required=True, help="two comma-separated party names, e.g. claude,glm")
    p_init.add_argument("--supervisor", default="owner")
    p_init.add_argument(
        "--thread-cap",
        type=int,
        default=12,
        help="maximum entries in one thread (default: 12; explicit historical caps are preserved)",
    )
    p_init.add_argument(
        "--label",
        default=None,
        help="human-readable half of the generated channel id <label>-<NNNNN> "
        "(default: the enclosing repo's directory name)",
    )
    p_init.add_argument(
        "--brokered",
        action="store_true",
        help="initialize managed-version 2: party entries must come through controller-bound adapters",
    )

    p_setup = sub.add_parser(
        "setup",
        help="wire the seats of an existing channel: watcher config, pinned prompts, PROTOCOL.md",
    )
    p_setup.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_setup)
    p_setup.add_argument(
        "--command",
        dest="seat_commands",
        action="append",
        default=[],
        metavar="PARTY=ARGV",
        help="seat command, e.g. --command 'glm=/home/me/.local/bin/glm-agent {prompt}'; "
        "skips that party's question",
    )
    p_setup.add_argument(
        "--human",
        dest="seat_human",
        action="append",
        default=[],
        metavar="PARTY",
        help="mark a party human-driven (no watcher command); skips its question",
    )
    p_setup.add_argument(
        "--yes",
        action="store_true",
        help="non-interactive: use flags and remembered defaults, confirm overwrites",
    )
    p_setup.add_argument(
        "--smoke",
        action="store_true",
        help="after writing: one scratch-channel round trip per watcher-driven seat "
        "(one model call each; the real channel is untouched)",
    )
    p_setup.add_argument(
        "--scheduler",
        action="store_true",
        help="print the debate-watch-<id> user units / cron line; never installs or runs them",
    )

    p_post = sub.add_parser("post", help="append an entry and bump the doorbell")
    p_post.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_post)
    p_post.add_argument("--from", dest="sender", required=True)
    p_post.add_argument("--type", dest="entry_type", required=True, choices=channel.ENTRY_TYPES)
    p_post.add_argument("--thread", required=True)
    p_post.add_argument("--refs", default="")
    body = p_post.add_mutually_exclusive_group(required=True)
    body.add_argument("--body")
    body.add_argument("--body-file", type=Path)
    p_post.add_argument("--force", action="store_true")
    p_post.add_argument(
        "--verify-refs",
        type=Path,
        default=None,
        metavar="REPO",
        help="refuse the post unless every name@sha in --refs resolves to a commit in REPO",
    )

    p_status = sub.add_parser("status", help="print the doorbell and open-thread tail")
    p_status.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_status)
    p_status.add_argument(
        "--stale-after",
        type=_nonnegative_int,
        default=None,
        metavar="SECONDS",
        help="exit 3 when the open thread is stuck this long (turnless/unknown-age always counts as stuck)",
    )

    p_read = sub.add_parser("read", help="print entries: the open thread by default")
    p_read.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_read)
    p_read.add_argument("--thread", default=None, help="a thread slug (archives are searched too)")
    p_read.add_argument("--since", type=int, default=None, metavar="SEQ", help="only entries with seq > SEQ")

    p_verify = sub.add_parser("verify", help="check the record against itself (tampering, inconsistency)")
    p_verify.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_verify)

    p_compact = sub.add_parser("compact", help="relocate old closed threads to archive/ (supervisor housekeeping)")
    p_compact.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_compact)
    p_compact.add_argument("--keep-days", type=float, default=14.0, help="keep threads closed more recently than this")
    p_compact.add_argument("--dry-run", action="store_true")

    p_migrate = sub.add_parser("migrate", help="rename a legacy channel in place to the named layout")
    p_migrate.add_argument("--root", type=Path, default=Path("."))
    p_migrate.add_argument(
        "--label",
        default=None,
        help="human-readable half of the generated channel id <label>-<NNNNN> "
        "(default: the enclosing repo's directory name)",
    )

    p_watch = sub.add_parser("watch-once", help="one watcher tick (run from cron / Task Scheduler)")
    p_watch.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_watch)
    p_watch.add_argument("--config", type=Path, required=True, help="watcher config JSON (see README)")

    p_watchstatus = sub.add_parser("watch-status", help="read-only: is anything driving this channel?")
    p_watchstatus.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_watchstatus)
    p_watchstatus.add_argument("--config", type=Path, required=True, help="watcher config JSON (see README)")
    p_watchstatus.add_argument(
        "--grace",
        type=_positive_int,
        default=120,
        metavar="SECONDS",
        help="allowance above a party's debounce before an uninvoked seq counts as STALE (default 120: two ticks of a 60s scheduler)",
    )

    p_watchloop = sub.add_parser("watch", help="foreground watcher loop: drive the open thread to completion")
    p_watchloop.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_watchloop)
    p_watchloop.add_argument("--config", type=Path, required=True, help="watcher config JSON (see README)")
    p_watchloop.add_argument(
        "--interval", type=_positive_int, default=None, metavar="SECONDS",
        help="seconds between ticks (default: the config's scheduler_interval_seconds "
        "for a fully managed channel, else 180)",
    )
    p_watchloop.add_argument("--until-close", action="store_true", help="exit 0 when no thread is open")
    p_watchloop.add_argument("--max-ticks", type=_positive_int, default=None)

    p_doctor = sub.add_parser(
        "adapter-doctor",
        help="validate a fully managed debate's seat profiles, topology, cost mode, "
        "runtime placement, and timing without invoking anything",
    )
    p_doctor.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_doctor)
    p_doctor.add_argument(
        "--config", type=Path, required=True, help="the fully managed debate's watcher config JSON"
    )

    p_runtime = sub.add_parser(
        "runtime",
        help="inspect one exact managed channel runtime, or prune only regenerable invocation state",
    )
    p_runtime.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_runtime)
    p_runtime.add_argument(
        "--config", type=Path, required=True, help="the exact channel's watcher config JSON"
    )
    p_runtime.add_argument(
        "--prune", action="store_true", help="delete terminal invocation home/build/tmp trees"
    )
    p_runtime.add_argument(
        "--yes", action="store_true", help="confirm --prune after inspecting the byte report"
    )

    p_broker_open = sub.add_parser(
        "broker-open",
        help="snapshot and open a neutral review case for a fully managed debate; "
        "the supervisor authors the docket",
    )
    p_broker_open.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_broker_open)
    p_broker_open.add_argument(
        "--config", type=Path, required=True, help="the fully managed debate's watcher config JSON"
    )
    p_broker_open.add_argument("--thread", required=True)
    p_broker_open.add_argument("--first-seat", required=True)
    p_broker_open.add_argument("--refs", default="")
    broker_body = p_broker_open.add_mutually_exclusive_group(required=True)
    broker_body.add_argument("--body")
    broker_body.add_argument("--body-file", type=Path)

    p_broker_revise = sub.add_parser(
        "broker-revise",
        help="snapshot and record a new artifact/docket revision without changing the party turn",
    )
    p_broker_revise.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_broker_revise)
    p_broker_revise.add_argument(
        "--config", type=Path, required=True,
        help="the fully managed debate's updated watcher config JSON",
    )
    p_broker_revise.add_argument("--thread", required=True)
    p_broker_revise.add_argument("--refs", default="")
    revise_body = p_broker_revise.add_mutually_exclusive_group(required=True)
    revise_body.add_argument("--body")
    revise_body.add_argument("--body-file", type=Path)
    p_broker_revise.add_argument(
        "--delta-round",
        action="store_true",
        help="write this round's instruction sheet from the prior version, the prior verdicts "
        "and the true diff, and put the prior version in front of the seats",
    )
    p_broker_revise.add_argument(
        "--goal", help="one sentence saying what this round verifies; needs --delta-round"
    )
    p_broker_revise.add_argument(
        "--fold-list-file",
        type=Path,
        help="file holding your own list of the folds you made; needs --delta-round",
    )
    p_broker_revise.add_argument(
        "--prior",
        action="append",
        default=[],
        metavar="CURRENT=PRIOR",
        help="the artifact and the version the last round reviewed, two paths joined by '='; "
        "repeat for each artifact; needs --delta-round",
    )
    p_broker_revise.add_argument(
        "--prior-verdict",
        action="append",
        default=[],
        dest="prior_verdicts",
        metavar="MSG-n",
        help="a verdict of the last round, by its entry id; repeat; needs --delta-round",
    )
    p_broker_revise.add_argument(
        "--docket-out",
        type=Path,
        help="where to write this round's instruction sheet (default "
        "the loaded channel runtime as delta-docket-<thread>-<n>.md); needs --delta-round",
    )

    # Hidden on purpose: nobody types this. The channel-opening flow writes it
    # into a seat's adapter command so an ordinary prompt-taking CLI can answer
    # a review pass, and the doctor reads it back. Passing help=SUPPRESS is NOT
    # enough -- argparse still prints the row, with "==SUPPRESS==" as its text --
    # so the parser is registered with no help at all, which keeps it out of the
    # listing entirely; the metavar above keeps it out of the usage line.
    bridge.configure_parser(sub.add_parser(bridge.SUBCOMMAND))

    args = parser.parse_args(argv)

    try:
        # One resolution, up front: which channel in --root is being addressed?
        # None means the legacy layout; init CREATES a channel and never
        # discovers one, and `seats` addresses the host registry, not a root.
        name: str | None = None
        if args.command not in (
            "init", "migrate", "seats", "open", "onboarding", bridge.SUBCOMMAND,
        ):
            name = channel.discover_channel(args.root, getattr(args, "channel", None))

        if args.command == bridge.SUBCOMMAND:
            return bridge.run_bridge_command(args)

        if args.command == "onboarding":
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            onboarding_report: dict[str, object]
            if args.onboarding_command == "status":
                onboarding_report = onboarding.status(args.project)
            elif args.onboarding_command == "inspect":
                onboarding_report = onboarding.inspect(args.project, now=now)
            else:  # approve
                onboarding_report = onboarding.approve(
                    args.project,
                    allow=list(args.allow),
                    candidate_revision=args.candidate_revision,
                    confirmed=args.confirmed,
                    now=now,
                    accepted_policies=onboarding.parse_policy_acceptances(args.accepted_policies),
                )
            if args.as_json:
                print(json.dumps(onboarding_report, indent=2))
            elif args.onboarding_command == "status" or args.onboarding_command == "approve":
                for line in onboarding.status_lines(onboarding_report):
                    _flushing_print(line)
            else:
                candidates = onboarding_report["candidates"]
                if isinstance(candidates, list):
                    for row in candidates:
                        if isinstance(row, dict):
                            _flushing_print(
                                f"{row['seat_id']}: source {row['source']}, "
                                f"{'present' if row['present'] else 'MISSING'}, "
                                f"smoke {row['smoke']}"
                                f"{', existing registry entry' if row['existing'] else ''}"
                            )
                            if row.get("data_policy_revision"):
                                _flushing_print(
                                    f"  policy {row['data_policy_revision']}: "
                                    f"{row['data_policy_notice']}"
                                )
                _flushing_print(f"candidate_revision: {onboarding_report['candidate_revision']}")
            return 0

        if args.command == "open" and args.brokered:
            registry = seats.load_registry()
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            product_thread_cap = opening.resolve_review_thread_cap(
                args.review_mode, args.thread_cap
            )
            if args.pair is None:
                # The refusal stands -- this path never picks for the user --
                # but it hands the skill the numbered list to show, sized by
                # how much there is to review.
                project_root = opening.project_key(args.root)
                approved = seats.load_profile(project_root, registry)
                allowlist = None if approved is None else approved.allowlist
                review_bytes = opening.docket_byte_size(project_root, args.docket_files)
                lines = [
                    "refused: a fully managed debate needs --pair (the product skill "
                    "passes the user's exact two-seat choice)"
                ]
                suggestion = opening.suggest_pair_with_reason(
                    registry,
                    allowlist=allowlist,
                    docket_bytes=review_bytes,
                    quick_review_max_bytes=args.quick_review_max_bytes,
                    last_pair=opening.remembered_pair(
                        registry, project=project_root, allowlist=allowlist
                    ),
                )
                menu = opening.pair_menu(
                    registry,
                    allowlist=allowlist,
                    suggestion=suggestion,
                    docket_bytes=review_bytes,
                    quick_review_max_bytes=args.quick_review_max_bytes,
                )
                if menu:
                    lines.append("seat one of these with --pair a,b:")
                    lines.extend(menu)
                budget = opening.review_budget(product_thread_cap, (1, 1))
                lines.append(
                    f"review budget ({args.review_mode}): {budget.seat_turn_ceiling} "
                    f"seat turns, at most {budget.nested_launch_ceiling} nested-seat "
                    "launches; supervisor entries consume the same cap"
                )
                raise channel.ChannelError("\n".join(lines))
            parts = tuple(part.strip() for part in args.pair.split(","))
            if len(parts) != 2 or not all(parts):
                raise channel.ChannelError(
                    f"refused: --pair needs exactly two seat ids, got {args.pair!r}"
                )
            source_ref = args.source_ref
            if source_ref is None:
                import subprocess

                project_root = opening.project_key(args.root)
                probe = subprocess.run(
                    ["git", "-C", project_root, "rev-parse", "HEAD"],
                    capture_output=True, text=True, check=False,
                )
                if probe.returncode != 0:
                    raise channel.ChannelError(
                        "refused: --brokered could not resolve the project HEAD for "
                        "source_ref; pass --source-ref explicitly"
                    )
                source_ref = probe.stdout.strip()
            if args.author_vendor is None:
                raise channel.ChannelError(
                    "refused: a fully managed debate needs --author-vendor (the "
                    "interactive author's vendor, e.g. 'claude' or 'codex')"
                )
            from debate import __version__

            result = opening.open_debate_brokered(
                opening.BrokeredOpenSpec(
                    root=args.root,
                    label=args.label,
                    pair=(parts[0], parts[1]),
                    source_ref=source_ref,
                    author_vendor=args.author_vendor,
                    supervisor=args.supervisor,
                    thread_cap=product_thread_cap,
                    allow_identical_seats=args.allow_identical_seats,
                    allow_mismatched_pair=args.allow_mismatched_pair,
                    docket_files=tuple(args.docket_files),
                    quick_review_max_bytes=args.quick_review_max_bytes,
                    deliberation_input=args.deliberation_input,
                    goal=args.goal or "",
                    review_domain=args.review_domain or "",
                    stop_rule=args.stop_rule or "",
                    review_mode=args.review_mode,
                ),
                registry,
                load_config_fn=_watcher_config,
                now=now,
                tool_version=__version__,
            )
            try:
                seats.save_registry(registry)
            except (OSError, channel.ChannelError) as error:
                # The channel is fully created and usable; last_pair is a
                # CONVENIENCE record. A bookkeeping failure here must warn,
                # never crash-and-orphan (field finding, 2026-08-20: a
                # sandboxed registry write killed the CLI after a successful
                # open, stranding an empty second channel on retry).
                _flushing_print(
                    f"warning: the debate opened fine, but the registry's "
                    f"remembered-pair bookkeeping failed ({error}); run "
                    f"'debate seats discover' later to refresh it"
                )
            for line in result.hints:
                _flushing_print(line)
            return 0

        if args.command == "open":
            registry = seats.load_registry()
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            pre_version = registry.tool_version
            registry, upgrade_diff = seats.ensure_current(registry, now=now)
            if upgrade_diff or registry.tool_version != pre_version:
                seats.save_registry(registry)
                for line in upgrade_diff:
                    _flushing_print(f"upgrade re-scan: {line}")
            report = seats.check(registry, now=now)
            for line in report.fails + report.warns:
                _flushing_print(line)
            requested: tuple[str, str] | None = None
            if args.pair is not None:
                parts = tuple(part.strip() for part in args.pair.split(","))
                if len(parts) != 2 or not all(parts):
                    raise channel.ChannelError(
                        f"refused: --pair needs exactly two seat ids, got {args.pair!r}"
                    )
                requested = (parts[0], parts[1])
            project_root = opening.project_key(args.root)
            pair = opening.pick_pair(
                registry,
                project=project_root,
                requested=requested,
                assume_yes=args.assume_yes,
                ask=input,
                allow_identical=args.allow_identical_seats,
                allow_mismatched_pair=args.allow_mismatched_pair,
                now=now,
                # This open runs the seat command itself; the settings a
                # managed debate needs are not this path's business.
                require_admissible=False,
                docket_bytes=opening.docket_byte_size(project_root, args.docket_files),
                quick_review_max_bytes=args.quick_review_max_bytes,
            )
            from debate import __version__

            result = opening.open_debate(
                opening.OpenSpec(
                    root=args.root,
                    label=args.label,
                    pair=pair,
                    supervisor=args.supervisor,
                    thread_cap=args.thread_cap if args.thread_cap is not None else 12,
                    allow_identical_seats=args.allow_identical_seats,
                    assume_yes=args.assume_yes,
                    allow_mismatched_pair=args.allow_mismatched_pair,
                ),
                registry,
                load_config_fn=_watcher_config,
                now=now,
                tool_version=__version__,
            )
            try:
                seats.save_registry(registry)
            except (OSError, channel.ChannelError) as error:
                # The channel is fully created and usable; last_pair is a
                # CONVENIENCE record. A bookkeeping failure here must warn,
                # never crash-and-orphan (field finding, 2026-08-20: a
                # sandboxed registry write killed the CLI after a successful
                # open, stranding an empty second channel on retry).
                _flushing_print(
                    f"warning: the debate opened fine, but the registry's "
                    f"remembered-pair bookkeeping failed ({error}); run "
                    f"'debate seats discover' later to refresh it"
                )
            for line in result.hints:
                _flushing_print(line)
            return 0

        if args.command == "seats":
            registry = seats.load_registry()
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if args.seats_command != "discover":
                # The upgrade trigger: a tool-version mismatch re-scans first
                # (scan only -- smoke is never automatic). On a --json surface
                # the diagnostics go to stderr so stdout stays machine-readable.
                # The stamp PERSISTS even when the re-scan changes nothing --
                # an unpersisted stamp refires the re-scan forever (round-6
                # gate finding).
                pre_version = registry.tool_version
                registry, upgrade_diff = seats.ensure_current(registry, now=now)
                as_json = bool(getattr(args, "as_json", False))
                if upgrade_diff or registry.tool_version != pre_version:
                    seats.save_registry(registry)
                    for line in upgrade_diff:
                        if as_json:
                            print(f"upgrade re-scan: {line}", file=sys.stderr, flush=True)
                        else:
                            _flushing_print(f"upgrade re-scan: {line}")
            if args.seats_command in ("check", "doctor"):
                report = seats.check(registry, now=now)
                if args.as_json:
                    _flushing_print(json.dumps({
                        "fails": report.fails,
                        "warns": report.warns,
                        "infos": report.infos,
                        "hint": "full re-discovery: debate seats discover",
                    }, indent=2))
                    return 3 if report.fails else 0
                for line in report.fails + report.warns + report.infos:
                    _flushing_print(line)
                if args.seats_command == "doctor":
                    stale = [line.split()[1].rstrip(":") for line in report.warns]
                    for seat_id in stale:
                        _flushing_print(f"refresh: debate seats smoke {seat_id}")
                    if not (report.fails or report.warns or report.infos):
                        _flushing_print("doctor: every seat resolves and smoke is fresh")
                _flushing_print("full re-discovery: debate seats discover")
                return 3 if report.fails else 0
            if args.seats_command == "smoke":
                for seat_id in args.seat_ids:
                    if seat_id not in registry.seats:
                        raise channel.ChannelError(
                            f"refused: no seat {seat_id!r} in the registry"
                        )
                worst = 0
                # Scratch channels live under the registry's own directory,
                # never the system temp dir (field finding, 2026-08-20: the
                # default landed smoke scratch in /tmp).
                scratch_base = seats.registry_path().parent / "smoke-scratch"
                for seat_id in args.seat_ids:
                    smoke_result = seats.smoke_seat(
                        registry, seat_id, now=now, emit=_flushing_print,
                        assume_yes=args.assume_yes, scratch_base=scratch_base,
                    )
                    observed = registry.seats[seat_id].smoke
                    # Apply ONLY the observed result to a freshly loaded
                    # registry under the lock: a concurrent smoke of another
                    # seat must not be clobbered by this process's stale
                    # in-memory copy (field finding, 2026-08-20).

                    def _apply(fresh: seats.Registry, _seat: str = seat_id) -> None:
                        if _seat in fresh.seats:
                            fresh.seats[_seat].smoke = observed

                    seats.update_registry(_apply)
                    if smoke_result != "pass":
                        worst = 1
                return worst
            if args.seats_command == "add":
                if args.seats_add_command_text is not None:
                    from .setup import split_argv

                    seats.add_seat(
                        registry, args.seat_id, args.seats_add_command_text,
                        cost_mode=args.seats_add_cost_mode,
                        capability_class=args.seats_add_capability_class,
                        isolation_argv=(
                            split_argv(args.seats_add_isolation_argv)
                            if args.seats_add_isolation_argv is not None else None
                        ),
                        no_persistence_argv=(
                            split_argv(args.seats_add_no_persistence_argv)
                            if args.seats_add_no_persistence_argv is not None else None
                        ),
                        config_home=args.seats_add_config_home,
                        verification_argv=(
                            split_argv(args.seats_add_verification_argv)
                            if args.seats_add_verification_argv is not None else None
                        ),
                        verification_declared=args.seats_add_verification_capable,
                        result_schema_version=args.seats_add_result_schema_version,
                        credential_env=list(args.seats_add_credential_env),
                    )
                elif "@" in args.seat_id:
                    seats.add_effort_seat(registry, args.seat_id)
                else:
                    raise channel.ChannelError(
                        "refused: a plain seat id needs --command; only "
                        "vendor/submodel@effort derives without one"
                    )
                seats.save_registry(registry)
                _flushing_print(f"added {args.seat_id}")
                return 0
            if args.seats_command == "set-cost-mode":
                seats.set_cost_mode(registry, args.seat_id, args.cost_mode)
                seats.save_registry(registry)
                _flushing_print(f"declared {args.seat_id}: cost mode {args.cost_mode}")
                return 0
            if args.seats_command == "remove":
                seats.remove_seat(registry, args.seat_id)
                seats.save_registry(registry)
                _flushing_print(f"removed {args.seat_id}")
                return 0
            if args.seats_command == "discover":
                now = datetime.now(timezone.utc).isoformat(timespec="seconds")
                registry, diff = seats.discover(registry, now=now)
                seats.save_registry(registry)
                if args.as_json:
                    _flushing_print(json.dumps({
                        "diff": diff,
                        "seats": len(registry.seats),
                        "registry": str(seats.registry_path()),
                    }, indent=2))
                    return 0
                for line in diff:
                    _flushing_print(line)
                _flushing_print(
                    f"registry: {len(registry.seats)} seat(s) at {seats.registry_path()}"
                )
                return 0
            if args.seats_command == "list":
                if args.as_json:
                    payload = {}
                    for seat_id, seat in sorted(registry.seats.items()):
                        notes, known_efforts = seats.vendor_display(seat.vendor)
                        seat_row: dict[str, object] = {
                            "present": seat.present,
                            "effort": seat.effort,
                            "commands": seat.commands,
                            "source": seat.source,
                            "notes": notes,
                            "known_efforts": list(known_efforts),
                            "smoke": (
                                {"at": seat.smoke.at, "result": seat.smoke.result}
                                if seat.smoke is not None
                                else None
                            ),
                        }
                        if seat.credential_env:
                            seat_row["credential_env"] = list(seat.credential_env)
                        if seat.data_policy_revision is not None:
                            seat_row["data_policy_revision"] = seat.data_policy_revision
                            seat_row["data_policy_notice"] = seat.data_policy_notice
                        payload[seat_id] = seat_row
                    _flushing_print(json.dumps(payload, indent=2))
                    return 0
                if not registry.seats:
                    _flushing_print("registry empty; run: debate seats discover")
                    return 0
                for seat_id, seat in sorted(registry.seats.items()):
                    smoke = (
                        f"smoke {seat.smoke.result} at {seat.smoke.at}"
                        if seat.smoke is not None
                        else "never smoked"
                    )
                    presence = "present" if seat.present else "ABSENT"
                    notes, known_efforts = seats.vendor_display(seat.vendor)
                    efforts = (
                        f"  efforts: {','.join(known_efforts)}" if known_efforts else ""
                    )
                    _flushing_print(
                        f"{seat_id}  [{presence}]  {smoke}  "
                        f"{' '.join(seat.commands[0])}{efforts}\n"
                        f"    note: {notes}"
                    )
                    if seat.credential_env:
                        _flushing_print(
                            f"    credential environment: {','.join(seat.credential_env)} "
                            "(name only; the raw value is visible to the seat process/tools)"
                        )
                    if seat.data_policy_revision is not None:
                        _flushing_print(
                            f"    data policy {seat.data_policy_revision}: {seat.data_policy_notice}"
                        )
                return 0
            raise channel.ChannelError(f"unknown seats command {args.seats_command!r}")

        if args.command == "init":
            parties = tuple(part.strip() for part in args.parties.split(",") if part.strip())
            if len(parties) != 2:
                raise channel.ChannelError(f"--parties needs exactly two names, got {parties}")
            channel_id = channel.generate_channel_id(args.root, label=args.label)
            managed_version = channel.BROKERED_MANAGED_VERSION if args.brokered else channel.MANAGED_VERSION
            channel.init_channel(
                args.root,
                (parties[0], parties[1]),
                args.supervisor,
                args.thread_cap,
                name=channel_id,
                managed_version=managed_version,
            )
            print(
                f"initialized channel {channel_id!r} at {args.root} "
                f"(parties {parties[0]!r}/{parties[1]!r}, supervisor {args.supervisor!r})"
            )
        elif args.command == "setup":
            from debate import setup as setup_mod

            if name is None:
                raise channel.ChannelError(
                    "refused: setup needs a named channel (the id is the state-file stem, "
                    "the unit name and the config stem) -- run `debate migrate` first."
                )
            chan_config = channel.load_config(args.root, name)
            if chan_config.managed_version == channel.BROKERED_MANAGED_VERSION:
                raise channel.ChannelError(
                    "refused: this channel is fully managed -- Debate runs its seats "
                    "itself, so they are seat profiles, not watcher commands. Start from "
                    "watcher.brokered.example.json and validate with `debate adapter-doctor`."
                )
            flag_commands: dict[str, list[str] | None] = {}
            for spec_text in args.seat_commands:
                party, sep, argv_text = spec_text.partition("=")
                if not sep or not argv_text.strip():
                    raise channel.ChannelError(
                        f"refused: --command needs PARTY=ARGV, got {spec_text!r}")
                flag_commands[party.strip()] = setup_mod.split_argv(argv_text)
            for party in args.seat_human:
                flag_commands[party.strip()] = None
            spec = setup_mod.interview(
                channel_root=args.root.resolve(),
                channel_name=name,
                parties=tuple(chan_config.parties),
                thread_cap=chan_config.thread_cap,
                project=Path(chan_config.project) if chan_config.project else None,
                supervisor=chan_config.supervisor,
                flag_commands=flag_commands,
                assume_yes=args.yes,
            )
            if spec.config_path.exists() and not spec.overwrite:
                answer = input(f"{spec.config_path} exists -- overwrite? [y/N] ").strip().lower()
                if answer not in ("y", "yes"):
                    raise channel.ChannelError("refused: not overwriting the existing config")
                spec.overwrite = True
            written = setup_mod.apply(spec, load_config_fn=_watcher_config)
            for path in written:
                print(f"wrote {path}")
            smoke_failed = False
            if args.smoke:
                failures = setup_mod.smoke(spec)
                for reason in failures:
                    print(f"smoke FAIL: {reason}", file=sys.stderr)
                smoke_failed = bool(failures)
            if args.scheduler:
                if smoke_failed:
                    # Units only after the seat passes: do not hand over a
                    # scheduler for a seat that cannot reply (review fold c).
                    print("scheduler output withheld: fix the failing seat first",
                          file=sys.stderr)
                else:
                    units = setup_mod.scheduler_units(spec)
                    unit_stem = f"debate-watch-{spec.channel_name}"
                    for filename, text in units.items():
                        if filename == "cron":
                            continue
                        print(f"--- ~/.config/systemd/user/{filename} ---")
                        print(text)
                    print("install (not run for you): systemctl --user daemon-reload && "
                          f"systemctl --user enable --now {unit_stem}.timer")
                    print(f"no systemd? cron line: {units['cron']}")
            for hint in setup_mod.closing_hints(spec, setup_mod.config_is_gitignored(spec.config_path)):
                print(f"hint: {hint}")
            if smoke_failed:
                return 4
        elif args.command == "post":
            text = args.body if args.body is not None else args.body_file.read_text(encoding="utf-8")
            if args.verify_refs is not None:
                channel.verify_refs(args.refs, args.verify_refs)
            entry_id = channel.post(
                root=args.root,
                sender=args.sender,
                entry_type=args.entry_type,
                thread=args.thread,
                body=text,
                refs=args.refs,
                force=args.force,
                name=name,
            )
            signal = channel.read_signal(args.root, name)
            turn = signal["turn"] or "-"
            print(f"posted {entry_id} (turn -> {turn})")
        elif args.command == "status":
            signal = channel.read_signal(args.root, name)
            parked = channel.turn_parked_since(args.root, datetime.now(timezone.utc), name)
            shown = dict(signal)
            if parked is not None and parked[0] is not None:
                shown["turn_age_seconds"] = parked[0]
            print(json.dumps(shown, indent=2))
            thread = str(signal.get("thread", ""))
            stuck = False
            if thread:
                if parked is None:
                    print(f"thread '{thread}' open with no turn - supervisor close required")
                    stuck = True  # both parties are turn-refused; a non-close supervisor post preserves ""
                else:
                    age, assigning_seq = parked
                    if age is None:
                        print(
                            f"turn '{signal.get('turn')}' parked (age unknown; malformed stamps) "
                            f"on '{thread}' (seq {assigning_seq})"
                        )
                        stuck = True  # unknown counts as stale - conservative
                    else:
                        hours, rem = divmod(age, 3600)
                        print(f"turn '{signal.get('turn')}' parked {hours}h{rem // 60:02d}m on '{thread}' (seq {assigning_seq})")
                        stuck = args.stale_after is not None and age >= args.stale_after
                for entry in channel.thread_entries(args.root, thread, name):
                    print(f"  MSG-{entry.seq} {entry.sender} {entry.entry_type}")
            if args.stale_after is not None and thread and stuck:
                return 3
        elif args.command == "verify":
            # The lock is taken HERE, not inside verify_record: the mailbox-ahead
            # check is only valid on a consistent snapshot, and an unlocked read
            # races an ordinary post. verify_record must stay lock-free so the
            # watcher can call it from inside its own locked block without
            # deadlocking against the non-reentrant O_EXCL lock.
            with channel.exclusive(args.root, name):
                findings = channel.verify_record(args.root, name)
            for finding in findings:
                print(str(finding))
            if not any(f.level == channel.ANOMALY for f in findings):
                print("record verifies clean")
                return 0
            # Exit 4, not 5: 4 is this project's shared "a human should look now"
            # code (watch escalation, watch-status), while 5 already means
            # max-ticks. A scheduler alerting on 4 must not miss an anomaly.
            return 4
        elif args.command == "read":
            _, entries = channel.read_raw(channel.mailbox_path(args.root, name))
            if args.thread is not None:
                blocks = [e for e in entries if e.thread == args.thread]
                if not blocks:  # closed threads may have moved house
                    for path in channel.archive_month_files(args.root, name):
                        _, archived = channel.read_raw(path)
                        blocks.extend(e for e in archived if e.thread == args.thread)
            elif args.since is None:
                open_thread = str(channel.read_signal(args.root, name).get("thread", ""))
                if not open_thread:
                    print("no open thread", file=sys.stderr)
                    return 0
                blocks = [e for e in entries if e.thread == open_thread]
            else:
                blocks = list(entries)
            if args.since is not None:
                blocks = [e for e in blocks if e.seq > args.since]
            for raw_entry in blocks:
                print(raw_entry.raw.strip("\n") + "\n")
        elif args.command == "migrate":
            channel_id = channel.migrate_channel(args.root, label=args.label)
            root_shown = args.root.resolve()
            migrated_path = args.root / f"{channel_id}.debate.json"
            migrated_raw = json.loads(migrated_path.read_text(encoding="utf-8"))
            migrated_config = channel.load_config(args.root, channel_id)
            cap_source = "explicit legacy config" if "thread_cap" in migrated_raw else "default (field absent)"
            print(f"migrated legacy channel at {root_shown} -> {channel_id!r}")
            print(f"thread cap: {migrated_config.thread_cap} from {cap_source}")
            print("")
            print("The operator owes two edits before the next watcher tick:")
            print(f"  1. watcher config: rename the state_path file stem to {channel_id!r}")
            print(f"     (e.g. state_path: .../{channel_id}.json) so the watcher's memory")
            print("     follows the channel's identity, and keep any prompt paths pointing")
            print(f"     at {root_shown}")
            print(f"  2. scheduler unit: rename it debate-watch-{channel_id}")
            print("")
            print(f"Then confirm one clean tick: debate watch-status --root {root_shown} --config <watcher.json>")
        elif args.command == "compact":
            for line in channel.compact(args.root, keep_days=args.keep_days, dry_run=args.dry_run, name=name):
                print(line)
        elif args.command == "watch-once":
            config = _watcher_config(args.root, args.config, name)
            for line in run_once(config):
                print(line)
        elif args.command == "watch-status":
            return _watch_status_report(args.root, args.config, args.grace, name)
        elif args.command == "adapter-doctor":
            config = _watcher_config(args.root, args.config, name)
            if config.broker is None:
                raise channel.ChannelError("refused: adapter-doctor requires an 'adapters' configuration")
            for line in doctor_lines(config.broker):
                print(line)
        elif args.command == "runtime":
            if name is None:
                raise channel.ChannelError("refused: runtime inspection needs --channel")
            config = _watcher_config(args.root, args.config, name)
            before = runtime_state.inspect(config, name)
            print(f"channel: {name}")
            print(f"runtime root: {before.runtime_root}")
            print(f"total bytes: {before.total_bytes}")
            print(f"retained provenance bytes: {before.retained_bytes}")
            print(f"regenerable invocation bytes: {before.regenerable_bytes}")
            print(f"regenerable paths: {len(before.regenerable_paths)}")
            if args.yes and not args.prune:
                raise channel.ChannelError("refused: --yes has no effect without --prune")
            if args.prune:
                from debate import __version__

                after = runtime_state.prune(
                    channel_root=args.root,
                    channel_name=name,
                    config_path=args.config,
                    load_config=_watcher_config,
                    tool_version=__version__,
                    confirmed=args.yes,
                )
                print(f"pruned bytes: {before.regenerable_bytes - after.regenerable_bytes}")
                print(f"remaining total bytes: {after.total_bytes}")
        elif args.command == "broker-open":
            config = _watcher_config(args.root, args.config, name)
            if config.broker is None or name is None:
                raise channel.ChannelError(
                    "refused: broker-open needs a named, fully managed channel"
                )
            text = args.body if args.body is not None else args.body_file.read_text(encoding="utf-8")
            entry_id = BrokerController(config.broker).open_case(
                channel_root=args.root,
                channel_name=name,
                thread=args.thread,
                first_party=args.first_seat,
                body=text,
                refs=args.refs,
            )
            print(f"opened the case as {entry_id}; first seat {args.first_seat!r}")
        elif args.command == "broker-revise":
            config = _watcher_config(args.root, args.config, name)
            if config.broker is None or name is None:
                raise channel.ChannelError(
                    "refused: broker-revise needs a named, fully managed channel"
                )
            text = args.body if args.body is not None else args.body_file.read_text(encoding="utf-8")
            delta_flags = (
                args.goal,
                args.fold_list_file,
                args.docket_out,
                args.prior or None,
                args.prior_verdicts or None,
            )
            if not args.delta_round and any(flag is not None for flag in delta_flags):
                raise channel.ChannelError(
                    "refused: --goal, --fold-list-file, --prior, --prior-verdict and --docket-out "
                    "belong to --delta-round; add --delta-round or drop them"
                )
            broker = config.broker
            docket_path: Path | None = None
            added: tuple[str, ...] = ()
            rollback: Callable[[], None] | None = None
            if args.delta_round:
                docket_path, added, rollback = _delta_round_docket(args, broker, args.root, name)
            try:
                if rollback is not None:
                    # The config just changed on disk; the revision has to
                    # record the file list the seats will actually receive,
                    # not the one loaded a moment ago.
                    reloaded = _watcher_config(args.root, args.config, name)
                    if reloaded.broker is None:
                        raise channel.ChannelError(
                            "refused: broker-revise needs a named, fully managed channel"
                        )
                    broker = reloaded.broker
                entry_id = BrokerController(broker).revise_case(
                    channel_root=args.root,
                    channel_name=name,
                    thread=args.thread,
                    body=text,
                    refs=args.refs,
                )
            except Exception:
                # Recording refused (a stuck half-finished revision, a changed
                # profile or deadline, an unreadable case) or failed outright:
                # put the docket and the config back the way they were, then
                # let the operator read the original refusal, unchanged. A
                # round that was not recorded must leave no trace claiming it
                # was.
                if rollback is not None:
                    rollback()
                raise
            # Spoken only once the round is REAL. Announcing the docket before
            # the recording would have printed a sentence the rollback then
            # made false.
            if docket_path is not None:
                print(f"wrote this round's instruction sheet to {docket_path}")
                if added:
                    print("added to the files this case puts in front of the seats: " + ", ".join(added))
            print(f"recorded the new artifact revision as {entry_id}; party turn unchanged")
        elif args.command == "watch":
            watch_config = _watcher_config(args.root, args.config, name)
            try:
                return watch(
                    watch_config,
                    interval_seconds=_watch_interval(args.interval, watch_config),
                    until_close=args.until_close,
                    max_ticks=args.max_ticks,
                    # flush=True or nothing reaches a redirected log until the
                    # buffer fills: under `nohup` an empty log read as a dead
                    # watcher and cost real debugging time (2026-07-28).
                    emit=_flushing_print,
                )
            except KeyboardInterrupt:
                return 130
    except channel.ChannelError as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
