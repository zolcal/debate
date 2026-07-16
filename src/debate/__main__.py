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

from debate import channel
from debate.watcher import WatcherConfig, run_once


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="debate", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a channel directory")
    p_init.add_argument("--root", type=Path, default=Path("."))
    p_init.add_argument("--parties", required=True, help="two comma-separated party names, e.g. claude,glm")
    p_init.add_argument("--supervisor", default="owner")
    p_init.add_argument("--thread-cap", type=int, default=8)

    p_post = sub.add_parser("post", help="append an entry and bump the doorbell")
    p_post.add_argument("--root", type=Path, default=Path("."))
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
    p_status.add_argument(
        "--stale-after",
        type=_nonnegative_int,
        default=None,
        metavar="SECONDS",
        help="exit 3 when the open thread is stuck this long (turnless/unknown-age always counts as stuck)",
    )

    p_read = sub.add_parser("read", help="print entries: the open thread by default")
    p_read.add_argument("--root", type=Path, default=Path("."))
    p_read.add_argument("--thread", default=None, help="a thread slug (archives are searched too)")
    p_read.add_argument("--since", type=int, default=None, metavar="SEQ", help="only entries with seq > SEQ")

    p_compact = sub.add_parser("compact", help="relocate old closed threads to archive/ (supervisor housekeeping)")
    p_compact.add_argument("--root", type=Path, default=Path("."))
    p_compact.add_argument("--keep-days", type=float, default=14.0, help="keep threads closed more recently than this")
    p_compact.add_argument("--dry-run", action="store_true")

    p_watch = sub.add_parser("watch-once", help="one watcher tick (run from cron / Task Scheduler)")
    p_watch.add_argument("--root", type=Path, default=Path("."))
    p_watch.add_argument("--config", type=Path, required=True, help="watcher config JSON (see README)")

    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            parties = tuple(part.strip() for part in args.parties.split(",") if part.strip())
            if len(parties) != 2:
                raise channel.ChannelError(f"--parties needs exactly two names, got {parties}")
            channel.init_channel(args.root, (parties[0], parties[1]), args.supervisor, args.thread_cap)
            print(f"initialized channel at {args.root} (parties {parties[0]!r}/{parties[1]!r}, supervisor {args.supervisor!r})")
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
            )
            signal = channel.read_signal(args.root)
            turn = signal["turn"] or "-"
            print(f"posted {entry_id} (turn -> {turn})")
        elif args.command == "status":
            signal = channel.read_signal(args.root)
            parked = channel.turn_parked_since(args.root, datetime.now(timezone.utc))
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
                for entry in channel.thread_entries(args.root, thread):
                    print(f"  MSG-{entry.seq} {entry.sender} {entry.entry_type}")
            if args.stale_after is not None and thread and stuck:
                return 3
        elif args.command == "read":
            _, entries = channel.read_raw(args.root / channel.CHANNEL_NAME)
            if args.thread is not None:
                blocks = [e for e in entries if e.thread == args.thread]
                if not blocks:  # closed threads may have moved house
                    archive = args.root / channel.ARCHIVE_DIR
                    for path in sorted(archive.glob("CHANNEL-*.md")) if archive.is_dir() else []:
                        _, archived = channel.read_raw(path)
                        blocks.extend(e for e in archived if e.thread == args.thread)
            elif args.since is None:
                open_thread = str(channel.read_signal(args.root).get("thread", ""))
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
        elif args.command == "compact":
            for line in channel.compact(args.root, keep_days=args.keep_days, dry_run=args.dry_run):
                print(line)
        elif args.command == "watch-once":
            raw = json.loads(args.config.read_text(encoding="utf-8"))
            config = WatcherConfig(
                channel_root=args.root,
                state_path=Path(raw["state_path"]),
                commands={k: list(v) for k, v in raw.get("commands", {}).items()},
                prompts={k: str(v) for k, v in raw.get("prompts", {}).items()},
                debounce_seconds={k: int(v) for k, v in raw.get("debounce_seconds", {}).items()},
                retry_seconds=int(raw.get("retry_seconds", 1800)),
                timeout_seconds=int(raw.get("timeout_seconds", 1800)),
            )
            for line in run_once(config):
                print(line)
    except channel.ChannelError as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
