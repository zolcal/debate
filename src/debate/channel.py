"""The channel: an append-only message log plus a machine-parseable doorbell.

Two independent agents (any two CLI-invocable harnesses — different vendors,
different machines-in-principle) exchange messages through two files:

- ``CHANNEL.md``  — the mailbox: append-only, human-readable, git-diffable.
- ``signal.json`` — the doorbell: tiny, machine-parseable, cheap to poll.

Everything a watcher needs is in the doorbell; everything a human auditor
needs is in the mailbox. All writes go through :func:`post` — the single
place the protocol is *enforced* rather than requested:

- **Turn alternation** binds within an open thread. An out-of-turn post is
  refused, not warned about. With no thread open, either party may post
  (otherwise whoever closed a thread could never open the next one).
- **One open thread at a time.** Posting a different slug while a thread is
  open is refused. ``force=True`` overrides this — and is honoured only for
  the supervisor; a party asking for force is refused outright.
- **Write-then-signal ordering.** The mailbox append lands before the
  doorbell is replaced (atomically, via tmp-file rename), so a watcher that
  fires on ``seq`` never reads a half-written entry.
- **One writer at a time.** ``post`` and ``compact`` serialize on a
  transient ``.lock`` file in the channel root (a crashed holder's lock is
  broken after 30 seconds), so a check-then-write can never interleave with
  another writer's.
- **The supervisor never takes a turn.** Supervisor posts land in the record
  and bump ``seq`` but do not flip whose turn it is.
- **Thread opening requires an action.** With no thread open, a party may open
  one only via review-request, question, info, or one-shot close correction.
  Verdict and fix-report are refused (supervisor exempt).

What this module deliberately does NOT do: run agents, schedule anything, or
talk to the network. Enforcement of *behavior beyond the mailbox* (what an
agent does to a repo, for instance) is out of scope here and must be treated
as advisory — see the trust model in the README.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

CONFIG_NAME = "debate.json"
CHANNEL_NAME = "CHANNEL.md"
SIGNAL_NAME = "signal.json"
LOCK_NAME = ".lock"

# Writers (post, compact) serialize on a transient lock file. A holder that
# crashed is assumed dead after the stale window — both operations complete
# in milliseconds, so 30s of silence means a corpse, not a slow writer.
_LOCK_TIMEOUT_SECONDS = 5.0
_LOCK_STALE_SECONDS = 30.0

ENTRY_TYPES = ("review-request", "verdict", "fix-report", "question", "info", "close")

# Types that may START a discussion. verdict/fix-report are replies by nature;
# close stays an opener for the documented one-shot close-correction idiom.
OPENER_TYPES: tuple[str, ...] = ("review-request", "question", "info", "close")

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_HEADER_RE = re.compile(
    r"^## MSG-(?P<seq>\d+) \| (?P<ts>[^|]+) \| from: (?P<sender>[\w-]+) "
    r"\| type: (?P<type>[\w-]+) \| thread: (?P<thread>[^|]+) \| refs: (?P<refs>.*)$"
)


class ChannelError(Exception):
    """A refused operation. The message says why; nothing was written."""


@dataclass(frozen=True)
class ChannelConfig:
    """Two named parties plus a supervisor, fixed at channel init."""

    parties: tuple[str, str]
    supervisor: str
    thread_cap: int = 8

    def __post_init__(self) -> None:
        names = (*self.parties, self.supervisor)
        if len(set(names)) != 3:
            raise ChannelError(f"parties and supervisor must be three distinct names, got {names}")
        for name in names:
            if not _SLUG_RE.fullmatch(name):
                raise ChannelError(f"invalid party name {name!r} (lowercase alphanumerics and dashes)")
        if self.thread_cap < 2:
            raise ChannelError("thread_cap must be >= 2 (a request and a reply)")

    def other(self, party: str) -> str:
        a, b = self.parties
        if party == a:
            return b
        if party == b:
            return a
        raise ChannelError(f"unknown party {party!r}; channel parties are {self.parties}")


@dataclass(frozen=True)
class Entry:
    seq: int
    timestamp: str
    sender: str
    entry_type: str
    thread: str
    refs: str
    body: str


def init_channel(root: Path, parties: tuple[str, str], supervisor: str, thread_cap: int = 8) -> ChannelConfig:
    """Create a channel directory: config + empty mailbox + fresh doorbell."""
    config = ChannelConfig(parties=parties, supervisor=supervisor, thread_cap=thread_cap)
    root.mkdir(parents=True, exist_ok=True)
    config_path = root / CONFIG_NAME
    if config_path.exists():
        raise ChannelError(f"channel already initialized at {root}")
    _atomic_write(
        config_path,
        json.dumps(
            {"parties": list(config.parties), "supervisor": config.supervisor, "thread_cap": config.thread_cap},
            indent=2,
        ),
    )
    (root / CHANNEL_NAME).touch()
    _atomic_write(root / SIGNAL_NAME, json.dumps(_fresh_signal(), indent=2))
    return config


def load_config(root: Path) -> ChannelConfig:
    raw = json.loads((root / CONFIG_NAME).read_text(encoding="utf-8"))
    parties = raw["parties"]
    if not isinstance(parties, list) or len(parties) != 2:
        raise ChannelError(f"config parties must be a two-item list, got {parties!r}")
    return ChannelConfig(
        parties=(str(parties[0]), str(parties[1])),
        supervisor=str(raw["supervisor"]),
        thread_cap=int(raw.get("thread_cap", 8)),
    )


def read_signal(root: Path) -> dict[str, object]:
    path = root / SIGNAL_NAME
    if not path.exists():
        return _fresh_signal()
    try:
        return dict(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError) as error:
        # A torn/truncated write or a file that vanished mid-read must refuse
        # deterministically - callers only guard for ChannelError, and a raw
        # JSONDecodeError/OSError would otherwise surface as a traceback.
        raise ChannelError(f"refused: unreadable signal file {path}: {error}") from error


def read_entries(root: Path) -> list[Entry]:
    """Parse the mailbox. Malformed lines between headers ride along as body."""
    path = root / CHANNEL_NAME
    if not path.exists():
        return []
    entries: list[Entry] = []
    header: dict[str, str] | None = None
    body: list[str] = []

    def flush() -> None:
        if header is not None:
            entries.append(
                Entry(
                    seq=int(header["seq"]),
                    timestamp=header["ts"].strip(),
                    sender=header["sender"],
                    entry_type=header["type"],
                    thread=header["thread"].strip(),
                    refs=header["refs"].strip(),
                    body="\n".join(body).strip(),
                )
            )

    for line in path.read_text(encoding="utf-8").splitlines():
        match = _HEADER_RE.match(line)
        if match:
            flush()
            header = match.groupdict()
            body = []
        elif header is not None:
            body.append(line)
    flush()
    return entries


def thread_entries(root: Path, thread: str) -> list[Entry]:
    return [entry for entry in read_entries(root) if entry.thread == thread]


def turn_parked_since(root: Path, now: datetime) -> tuple[int | None, int] | None:
    """(age_seconds, assigning_seq) for the parked turn of the open thread.

    The turn is assigned by the last PARTY-authored entry of the OPEN thread:
    supervisor interjections preserve the turn but refresh ``updated_at``, so
    the signal alone measures channel idleness - the wrong thing. Outer None:
    no open thread, or the thread has no turn (supervisor opener - a
    supervisor-only state, since turn enforcement refuses both parties).
    age None: both the party stamp and ``updated_at`` are malformed - age is
    unknown, never fabricated. This function never raises on its own account -
    the sole exception is :class:`ChannelError` propagated from ``read_signal``
    when ``signal.json`` itself is unreadable (torn write, vanished file); that
    is a refused-channel condition, not something to paper over as "unknown".
    """
    signal = read_signal(root)
    open_thread = str(signal.get("thread", ""))
    if not open_thread or not str(signal.get("turn", "")):
        return None
    config = load_config(root)
    stamp_text = ""
    try:
        seq = _as_int(signal.get("seq", 0))
    except (ChannelError, ValueError, TypeError):
        seq = 0  # corrupt/missing seq: never raise, just report unknown
    for entry in reversed(read_entries(root)):
        if entry.thread == open_thread and entry.sender in config.parties:
            stamp_text, seq = entry.timestamp, entry.seq
            break
    stamp = _parse_ts(stamp_text)
    if stamp is None:
        stamp = _parse_ts(str(signal.get("updated_at", "")))  # conservative fallback
    if stamp is None:
        return (None, seq)  # both malformed: unknown, not fabricated
    return (max(0, int((now - stamp).total_seconds())), seq)


def post(
    root: Path,
    sender: str,
    entry_type: str,
    thread: str,
    body: str,
    refs: str = "",
    force: bool = False,
) -> str:
    """Validate against the protocol, append the entry, bump the doorbell.

    Returns the assigned entry id; raises :class:`ChannelError` when the post
    is refused — in that case nothing was written.
    """
    config = load_config(root)
    body = body.strip()
    if not body:
        raise ChannelError("refused: empty body")
    if entry_type not in ENTRY_TYPES:
        raise ChannelError(f"refused: unknown entry type {entry_type!r} (one of {ENTRY_TYPES})")
    if sender != config.supervisor and sender not in config.parties:
        raise ChannelError(f"refused: unknown sender {sender!r} (parties {config.parties}, supervisor {config.supervisor!r})")
    if not _SLUG_RE.fullmatch(thread):
        raise ChannelError(f"refused: invalid thread slug {thread!r} (lowercase alphanumerics and dashes)")
    if force and sender != config.supervisor:
        raise ChannelError(
            f"refused: force is supervisor-only (supervisor {config.supervisor!r}); "
            "a party cannot bypass one-thread-at-a-time"
        )

    with exclusive(root):
        signal = read_signal(root)
        open_thread = str(signal.get("thread", ""))
        if sender != config.supervisor and not open_thread and entry_type not in OPENER_TYPES:
            raise ChannelError(
                f"refused: {entry_type!r} cannot open a thread - only review-request/question/info "
                "(or a one-shot close correction) may start one"
            )
        # Turn alternation binds only WITHIN an open thread; with no thread open,
        # either party may post to start one (a closer must be able to open next).
        if sender != config.supervisor and _as_int(signal["seq"]) > 0 and open_thread and signal["turn"] != sender:
            raise ChannelError(f"refused: not your turn (turn={signal['turn']}); double-posting is how loops start")
        if open_thread and thread != open_thread and not force:
            raise ChannelError(f"refused: thread '{open_thread}' is open; one thread at a time (force to override)")
        if open_thread and thread == open_thread and entry_type != "close":
            count = len(thread_entries(root, thread))
            if count >= config.thread_cap:
                raise ChannelError(
                    f"refused: thread '{thread}' is at its {config.thread_cap}-entry cap; "
                    "the supervisor must post or the thread must be closed"
                )

        seq = _as_int(signal["seq"]) + 1
        entry_id = f"MSG-{seq}"
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        header = f"## {entry_id} | {stamp} | from: {sender} | type: {entry_type} | thread: {thread} | refs: {refs or '-'}"
        with (root / CHANNEL_NAME).open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(f"\n{header}\n\n{body}\n")

        # A turn is only meaningful WITHIN an open thread. On close, clear it
        # along with the thread — leaving it pointing at the non-closer invites
        # watchers to fire on a turn that no longer means anything. (Lesson from
        # the first production deployment: see docs/case-study.)
        if entry_type == "close":
            new_turn = ""
        elif sender == config.supervisor:
            new_turn = str(signal["turn"])
        else:
            new_turn = config.other(sender)
        # A supervisor interjection on a different slug (force) must not re-point
        # the doorbell away from the open thread — it lands in the record only.
        if entry_type == "close":
            new_thread = ""
        elif sender == config.supervisor and open_thread:
            new_thread = open_thread
        else:
            new_thread = thread
        _atomic_write(
            root / SIGNAL_NAME,
            json.dumps(
                {
                    "seq": seq,
                    "turn": new_turn,
                    "thread": new_thread,
                    "last_entry": entry_id,
                    "updated_at": stamp,
                },
                indent=2,
            ),
        )
        return entry_id


ARCHIVE_DIR = "archive"
ARCHIVE_INDEX = "INDEX.md"
_ARCHIVE_BANNER = (
    "> Older closed threads relocate verbatim to archive/ (see archive/INDEX.md). "
    "Entries are never edited - `debate compact` only moves them."
)
_SHA_RE = re.compile(r"@([0-9a-fA-F]{7,40})\b")


@dataclass(frozen=True)
class RawEntry:
    """One mailbox entry with its exact on-disk text (header line + body)."""

    seq: int
    thread: str
    entry_type: str
    timestamp: str
    raw: str  # verbatim: the header line through the last line before the next header


def read_raw(path: Path) -> tuple[str, list[RawEntry]]:
    """Split a mailbox file into (preamble, entries), preserving bytes.

    ``preamble`` is everything before the first entry header (readers ignore
    it); each entry's ``raw`` is its exact text, so
    ``preamble + "".join(e.raw for e in entries)`` reproduces the file —
    including CRLF line endings, if the mailbox was imported from or checked
    out on a system that uses them (``newline=""`` disables translation).
    """
    if not path.exists():
        return "", []
    with path.open(encoding="utf-8", newline="") as handle:
        text = handle.read()
    preamble: list[str] = []
    entries: list[RawEntry] = []
    current: dict[str, str] | None = None
    block: list[str] = []

    def flush() -> None:
        if current is not None:
            entries.append(
                RawEntry(
                    seq=int(current["seq"]),
                    thread=current["thread"].strip(),
                    entry_type=current["type"],
                    timestamp=current["ts"].strip(),
                    raw="".join(block),
                )
            )

    for line in text.splitlines(keepends=True):
        match = _HEADER_RE.match(line.rstrip("\r\n"))
        if match:
            flush()
            current = match.groupdict()
            block = [line]
        elif current is None:
            preamble.append(line)
        else:
            block.append(line)
    flush()
    return "".join(preamble), entries


def compact(
    root: Path,
    keep_days: float = 14.0,
    now: datetime | None = None,
    dry_run: bool = False,
) -> list[str]:
    """Relocate old CLOSED threads to ``archive/`` — the mailbox stays small,
    the record stays complete.

    A thread is eligible when it is not the open thread, its last entry is a
    ``close``, and that entry is older than ``keep_days``. Eligible entries
    move VERBATIM (never edited, never re-rendered) to
    ``archive/CHANNEL-<YYYY-MM>.md`` — the month of the thread's last entry —
    and one line per thread lands in ``archive/INDEX.md``.

    Concurrency: the write phase runs under the channel's writer lock (the
    same one ``post`` takes), and the kept entries are re-read FRESH inside
    the lock and selected by seq — a concurrent post can wait, or land
    before or after, but can never be overwritten. Crash ordering mirrors
    write-then-signal: archive files are appended BEFORE the mailbox is
    rewritten, so an interruption can duplicate an entry across the two
    places but never lose one. As defense-in-depth against writers that
    bypass the lock, the rewrite is refused if the doorbell seq changed
    since planning.
    """
    signal = read_signal(root)
    seq_before = _as_int(signal["seq"])
    open_thread = str(signal.get("thread", ""))
    stamp_now = now or datetime.now(timezone.utc)

    preamble, entries = read_raw(root / CHANNEL_NAME)
    by_thread: dict[str, list[RawEntry]] = {}
    order: list[str] = []
    for entry in entries:
        if entry.thread not in by_thread:
            order.append(entry.thread)
        by_thread.setdefault(entry.thread, []).append(entry)

    eligible: list[str] = []
    for thread in order:
        if thread == open_thread:
            continue
        last = max(by_thread[thread], key=lambda e: e.seq)
        if last.entry_type != "close":
            continue
        last_at = _parse_ts(last.timestamp)
        if last_at is None:
            continue  # unparseable stamp: leave the thread alone, never guess
        if (stamp_now - last_at).total_seconds() < keep_days * 86400:
            continue
        eligible.append(thread)

    if not eligible:
        return ["nothing to compact"]

    moving = set(eligible)
    moves: dict[str, list[str]] = {}  # archive file name -> raw blocks, in mailbox order
    index_lines: list[str] = []
    report: list[str] = []
    for thread in eligible:
        blocks = by_thread[thread]
        last = max(blocks, key=lambda e: e.seq)
        last_at = _parse_ts(last.timestamp)
        assert last_at is not None  # eligibility filtered unparseable stamps
        name = f"CHANNEL-{last_at:%Y-%m}.md"
        moves.setdefault(name, []).extend(e.raw for e in blocks)
        seqs = sorted(e.seq for e in blocks)
        index_lines.append(
            f"- {thread}: MSG-{seqs[0]}..MSG-{seqs[-1]} ({len(seqs)} entries, closed {last.timestamp}) -> {name}"
        )
        report.append(f"archived {thread}: MSG-{seqs[0]}..MSG-{seqs[-1]} ({len(seqs)} entries) -> {name}")

    if dry_run:
        return ["dry-run, nothing written", *report]

    archived_seqs = {e.seq for thread in moving for e in by_thread[thread]}

    with exclusive(root):
        # Defense-in-depth: planning happened outside the lock; a writer that
        # bypasses the lock (hand edits, an old client) shows up as a moved seq.
        if _as_int(read_signal(root)["seq"]) != seq_before:
            raise ChannelError("refused: the channel changed while compacting; run again")

        # Re-read FRESH inside the lock and keep by seq, not by planning
        # snapshot: entries archived are closed and immutable, so anything
        # else — whatever its thread slug — is kept exactly as found.
        preamble, entries = read_raw(root / CHANNEL_NAME)
        kept_raw = "".join(e.raw for e in entries if e.seq not in archived_seqs)
        if _ARCHIVE_BANNER not in preamble:
            preamble = f"{_ARCHIVE_BANNER}\n{preamble}" if preamble.strip() else f"{_ARCHIVE_BANNER}\n"

        archive_root = root / ARCHIVE_DIR
        archive_root.mkdir(exist_ok=True)
        for name, raws in moves.items():
            with (archive_root / name).open("a", encoding="utf-8", newline="") as handle:
                for raw in raws:
                    if not raw.startswith("\n"):
                        handle.write("\n")
                    handle.write(raw)
        with (archive_root / ARCHIVE_INDEX).open("a", encoding="utf-8", newline="") as handle:
            for line in index_lines:
                handle.write(line + "\n")
        _atomic_write(root / CHANNEL_NAME, preamble + kept_raw)
    return report


def verify_refs(refs: str, repo: Path) -> None:
    """Refuse refs whose cited commits do not exist in ``repo``.

    Convention: refs cite ``name@sha``. Every ``@sha`` found must resolve to
    a commit. Born from a real incident: a close message once cited a hash
    written down BEFORE the commit existed — wrong by construction — and a
    correction entry had to follow. This check refuses that post instead.
    """
    import subprocess  # local import keeps module load light

    shas = _SHA_RE.findall(refs)
    if not shas:
        raise ChannelError(f"refused: --verify-refs found no name@sha citation in refs {refs!r}")
    for sha in shas:
        try:
            result = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except FileNotFoundError as error:
            raise ChannelError("refused: --verify-refs needs git on PATH") from error
        if result.returncode != 0:
            raise ChannelError(f"refused: refs cite {sha!r}, which is not a commit in {repo}")


def _parse_ts(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)


def _fresh_signal() -> dict[str, object]:
    return {"seq": 0, "turn": "", "thread": "", "last_entry": "", "updated_at": ""}


def _as_int(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ChannelError(f"corrupt signal: expected an integer, got {value!r}")
    return int(value)


@contextmanager
def exclusive(root: Path) -> Iterator[None]:
    """Hold the channel's writer lock: O_EXCL-create ``root/.lock``.

    Advisory but honoured by every shipped writer (``post``, ``compact``),
    which makes each one's check-then-write atomic with respect to the
    others. A lock older than the stale window belongs to a crashed holder
    and is broken; waiting past the timeout refuses rather than queueing
    forever.
    """
    import time  # local import keeps module load light

    lock = root / LOCK_NAME
    deadline = time.monotonic() + _LOCK_TIMEOUT_SECONDS
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                age = time.time() - lock.stat().st_mtime
            except OSError:
                continue  # released between our open and stat; try again now
            if age > _LOCK_STALE_SECONDS:
                lock.unlink(missing_ok=True)  # crashed holder
                continue
            if time.monotonic() > deadline:
                raise ChannelError(
                    f"refused: another writer holds {lock} (crashed holders are "
                    f"cleared after {_LOCK_STALE_SECONDS:.0f}s; try again)"
                ) from None
            time.sleep(0.05)
    try:
        yield
    finally:
        os.close(fd)
        lock.unlink(missing_ok=True)


def _atomic_write(path: Path, content: str) -> None:
    # newline="" writes content byte-for-byte: a mailbox rewrite must never
    # translate line endings (Windows text mode would turn LF into CRLF).
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content)
    tmp.replace(path)
