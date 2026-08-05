"""CLI: ``python -m debate <init|post|status|read|compact|watch-once>``.

Deliberately stdlib-only and deliberately small: the protocol is the
product; this is just a convenient way to speak it from a shell. Agents post
through ``post`` (never by editing the channel files), humans check
``status``, and any scheduler runs ``watch-once`` every few minutes.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from debate import channel
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


def _watcher_config(root: Path, config_path: Path, channel_name: str | None = None) -> WatcherConfig:
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
    )


# Verdicts that mean "a human should look now". Exit 4 matches `watch()`'s
# escalation code, so an alerting scheduler treats both the same way.
_NEEDS_ATTENTION = ("STALE", "ESCALATED")


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

    p_init = sub.add_parser("init", help="create a channel directory")
    p_init.add_argument("--root", type=Path, default=Path("."))
    p_init.add_argument("--parties", required=True, help="two comma-separated party names, e.g. claude,glm")
    p_init.add_argument("--supervisor", default="owner")
    p_init.add_argument("--thread-cap", type=int, default=8)
    p_init.add_argument(
        "--label",
        default=None,
        help="human-readable half of the generated channel id <label>-<NNNNN> "
        "(default: the enclosing repo's directory name)",
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

    args = parser.parse_args(argv)

    try:
        # One resolution, up front: which channel in --root is being addressed?
        # None means the legacy layout; init is the one command that CREATES
        # a channel and therefore never discovers one.
        name: str | None = None
        if args.command not in ("init", "migrate"):
            name = channel.discover_channel(args.root, getattr(args, "channel", None))

        if args.command == "init":
            parties = tuple(part.strip() for part in args.parties.split(",") if part.strip())
            if len(parties) != 2:
                raise channel.ChannelError(f"--parties needs exactly two names, got {parties}")
            channel_id = channel.generate_channel_id(args.root, label=args.label)
            channel.init_channel(args.root, (parties[0], parties[1]), args.supervisor, args.thread_cap, name=channel_id)
            print(
                f"initialized channel {channel_id!r} at {args.root} "
                f"(parties {parties[0]!r}/{parties[1]!r}, supervisor {args.supervisor!r})"
            )
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
            print(f"migrated legacy channel at {root_shown} -> {channel_id!r}")
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
