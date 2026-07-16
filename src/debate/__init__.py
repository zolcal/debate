"""debate — a tiny file-based protocol for two AI agents that review each other's work.

Enforced turns, an append-only audit log, and a human supervisor who can
always see everything. See README.md for the trust model.
"""

from debate.channel import (
    ChannelConfig,
    ChannelError,
    Entry,
    RawEntry,
    compact,
    init_channel,
    load_config,
    post,
    read_entries,
    read_raw,
    read_signal,
    verify_refs,
)
from debate.watcher import Decision, WatcherConfig, decide, run_once

__all__ = [
    "ChannelConfig",
    "ChannelError",
    "Decision",
    "Entry",
    "RawEntry",
    "WatcherConfig",
    "compact",
    "decide",
    "init_channel",
    "load_config",
    "post",
    "read_entries",
    "read_raw",
    "read_signal",
    "run_once",
    "verify_refs",
]

__version__ = "0.3.0"
