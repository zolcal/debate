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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from debate import channel, opening, seats
from debate.controller import AdapterProfile, BrokerConfig, BrokerController, TimingPolicy, doctor_lines
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
            raise channel.ChannelError("refused: brokered adapters require a named project-bound channel")
        for required in ("runtime_root", "source_ref", "whole_case_timeout_seconds"):
            if required not in raw:
                raise channel.ChannelError(
                    f"refused: brokered watcher config {config_path} has no {required!r}"
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="debate", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

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
    p_open.add_argument("--cap", type=int, default=12, dest="thread_cap",
                        help="maximum entries in one thread")
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
    p_watchloop.add_argument("--interval", type=_positive_int, default=180, metavar="SECONDS")
    p_watchloop.add_argument("--until-close", action="store_true", help="exit 0 when no thread is open")
    p_watchloop.add_argument("--max-ticks", type=_positive_int, default=None)

    p_doctor = sub.add_parser(
        "adapter-doctor",
        help="validate brokered profiles, topology, cost mode, runtime placement, and timing without invocation",
    )
    p_doctor.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_doctor)
    p_doctor.add_argument("--config", type=Path, required=True, help="brokered watcher config JSON")

    p_broker_open = sub.add_parser(
        "broker-open",
        help="snapshot and open a neutral brokered review case; the supervisor authors the docket",
    )
    p_broker_open.add_argument("--root", type=Path, default=Path("."))
    add_channel_flag(p_broker_open)
    p_broker_open.add_argument("--config", type=Path, required=True, help="brokered watcher config JSON")
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
    p_broker_revise.add_argument("--config", type=Path, required=True, help="updated brokered watcher config JSON")
    p_broker_revise.add_argument("--thread", required=True)
    p_broker_revise.add_argument("--refs", default="")
    revise_body = p_broker_revise.add_mutually_exclusive_group(required=True)
    revise_body.add_argument("--body")
    revise_body.add_argument("--body-file", type=Path)

    args = parser.parse_args(argv)

    try:
        # One resolution, up front: which channel in --root is being addressed?
        # None means the legacy layout; init CREATES a channel and never
        # discovers one, and `seats` addresses the host registry, not a root.
        name: str | None = None
        if args.command not in ("init", "migrate", "seats", "open"):
            name = channel.discover_channel(args.root, getattr(args, "channel", None))

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
            pair = opening.pick_pair(
                registry,
                project=opening.project_key(args.root),
                requested=requested,
                assume_yes=args.assume_yes,
                ask=input,
                allow_identical=args.allow_identical_seats,
                now=now,
            )
            from debate import __version__

            result = opening.open_debate(
                opening.OpenSpec(
                    root=args.root,
                    label=args.label,
                    pair=pair,
                    supervisor=args.supervisor,
                    thread_cap=args.thread_cap,
                    allow_identical_seats=args.allow_identical_seats,
                    assume_yes=args.assume_yes,
                ),
                registry,
                load_config_fn=_watcher_config,
                now=now,
                tool_version=__version__,
            )
            seats.save_registry(registry)
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
                for seat_id in args.seat_ids:
                    smoke_result = seats.smoke_seat(
                        registry, seat_id, now=now, emit=_flushing_print,
                        assume_yes=args.assume_yes,
                    )
                    seats.save_registry(registry)
                    if smoke_result != "pass":
                        worst = 1
                return worst
            if args.seats_command == "add":
                if args.seats_add_command_text is not None:
                    seats.add_seat(registry, args.seat_id, args.seats_add_command_text)
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
                        payload[seat_id] = {
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
                    "refused: this channel is managed version 2 (brokered) -- its seats are "
                    "adapter profiles, not watcher commands. Start from "
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
        elif args.command == "broker-open":
            config = _watcher_config(args.root, args.config, name)
            if config.broker is None or name is None:
                raise channel.ChannelError("refused: broker-open requires a named brokered channel")
            text = args.body if args.body is not None else args.body_file.read_text(encoding="utf-8")
            entry_id = BrokerController(config.broker).open_case(
                channel_root=args.root,
                channel_name=name,
                thread=args.thread,
                first_party=args.first_seat,
                body=text,
                refs=args.refs,
            )
            print(f"opened brokered case as {entry_id}; first seat {args.first_seat!r}")
        elif args.command == "broker-revise":
            config = _watcher_config(args.root, args.config, name)
            if config.broker is None or name is None:
                raise channel.ChannelError("refused: broker-revise requires a named brokered channel")
            text = args.body if args.body is not None else args.body_file.read_text(encoding="utf-8")
            entry_id = BrokerController(config.broker).revise_case(
                channel_root=args.root,
                channel_name=name,
                thread=args.thread,
                body=text,
                refs=args.refs,
            )
            print(f"recorded brokered artifact revision as {entry_id}; party turn unchanged")
        elif args.command == "watch":
            try:
                return watch(
                    _watcher_config(args.root, args.config, name),
                    interval_seconds=args.interval,
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
