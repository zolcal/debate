"""A complete debate round trip in one file, no API keys, no agents.

Run it:

    python examples/demo.py

Both "agents" here are scripted stand-ins — the point is to watch the
protocol mechanics: the doorbell, the turn enforcement, the watcher deciding
whom to wake, and the append-only record accumulating. Swap either party's
command for a real agent invocation (``claude -p ...``, or anything else
that can read files and run a shell command) and the mechanics are identical.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from debate.channel import ChannelError, init_channel, post, read_entries, read_signal
from debate.watcher import WatcherConfig, run_once


def main() -> None:
    root = Path(tempfile.mkdtemp(prefix="debate-demo-")) / "collab"
    print(f"channel: {root}\n")

    # --- 1. Create the channel: two parties and a supervisor. -------------
    init_channel(root, ("builder", "reviewer"), "owner")

    # --- 2. The builder opens a review thread. -----------------------------
    post(
        root,
        "builder",
        "review-request",
        "demo-feature",
        "Please review branch demo-feature at commit abc123.\n"
        "Verify: the new parser handles empty input; tests pass.",
        refs="demo-feature@abc123",
    )
    print("builder posted a review-request; doorbell now:")
    print(f"  {read_signal(root)}\n")

    # --- 3. Turn enforcement is a refusal, not a warning. ------------------
    try:
        post(root, "builder", "info", "demo-feature", "one more thing...")
    except ChannelError as error:
        print(f"builder tries to double-post -> {error}\n")

    # --- 4. The watcher wakes the reviewer. --------------------------------
    # The reviewer's "agent" is a subprocess that posts a verdict via the
    # CLI — exactly where a real agent invocation would go.
    reviewer_cmd = [
        sys.executable, "-m", "debate", "post",
        "--root", str(root),
        "--from", "reviewer",
        "--type", "verdict",
        "--thread", "demo-feature",
        "--refs", "demo-feature@abc123",
        "--body", "APPROVE — verified empty-input handling; my own run: 27 tests pass at abc123.",
    ]
    config = WatcherConfig(
        channel_root=root,
        state_path=root.parent / "watcher-state.json",
        commands={"reviewer": reviewer_cmd},
        prompts={"reviewer": "(a pinned prompt would go here)"},
    )
    print("watcher tick #1:")
    for line in run_once(config):
        print(f"  {line}")
    print()

    # --- 5. The builder closes; close clears thread AND turn. --------------
    post(root, "builder", "close", "demo-feature", "Merged on the APPROVE. Closing.")
    print("builder closed the thread; doorbell now:")
    print(f"  {read_signal(root)}\n")

    print("watcher tick #2 (nothing to do — and it knows why):")
    lines = run_once(config)
    print(f"  {lines if lines else '(quiet: no open thread, nobody invoked)'}\n")

    # --- 6. The record. -----------------------------------------------------
    print("the record:")
    for entry in read_entries(root):
        print(f"  MSG-{entry.seq} {entry.sender:9s} {entry.entry_type:15s} {entry.body.splitlines()[0][:60]}")
    print(f"\nfull transcript: {root / 'CHANNEL.md'}")


if __name__ == "__main__":
    main()
