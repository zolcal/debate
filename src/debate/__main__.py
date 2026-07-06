"""CLI: ``python -m debate <init|post|status|watch-once>``.

Deliberately stdlib-only and deliberately small: the protocol is the
product; this is just a convenient way to speak it from a shell. Agents post
through ``post`` (never by editing the channel files), humans check
``status``, and any scheduler runs ``watch-once`` every few minutes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from debate import channel
from debate.watcher import WatcherConfig, run_once


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

    p_status = sub.add_parser("status", help="print the doorbell and open-thread tail")
    p_status.add_argument("--root", type=Path, default=Path("."))

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
            print(json.dumps(signal, indent=2))
            thread = str(signal.get("thread", ""))
            if thread:
                for entry in channel.thread_entries(args.root, thread):
                    print(f"  MSG-{entry.seq} {entry.sender} {entry.entry_type}")
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
