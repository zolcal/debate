"""debate — a tiny file-based protocol for two AI agents that review each other's work.

Enforced turns, an append-only audit log, and a human supervisor who can
always see everything. See README.md for the trust model.
"""

from debate.channel import ChannelConfig, ChannelError, Entry, init_channel, load_config, post, read_entries, read_signal
from debate.watcher import Decision, WatcherConfig, decide, run_once

__all__ = [
    "ChannelConfig",
    "ChannelError",
    "Decision",
    "Entry",
    "WatcherConfig",
    "decide",
    "init_channel",
    "load_config",
    "post",
    "read_entries",
    "read_signal",
    "run_once",
]

__version__ = "0.1.0"
