"""The channel: an append-only message log plus a machine-parseable doorbell.

Two independent agents (any two CLI-invocable harnesses — different vendors,
different machines-in-principle) exchange messages through two files:

- ``CHANNEL.md``  — the mailbox: append-only, human-readable, git-diffable.
- ``signal.json`` — the doorbell: tiny, machine-parseable, cheap to poll.

Everything a watcher needs is in the doorbell; everything a human auditor
needs is in the mailbox. All writes go through :func:`post` — called directly
for legacy/version 1 channels and only by the controller for version 2 — the single
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
MANAGED_VERSION = 1
BROKERED_MANAGED_VERSION = 2
SUPPORTED_MANAGED_VERSIONS = (MANAGED_VERSION, BROKERED_MANAGED_VERSION)

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


# A channel is either LEGACY (the 0.3.1 module-constant filenames above) or
# NAMED: files carry the instance id generated at init, so several channels
# can share one folder without clobbering each other. ``name=None`` means
# legacy throughout this module — the pre-0.4 call signature keeps its exact
# pre-0.4 behavior.
def _config_path(root: Path, name: str | None) -> Path:
    return root / (CONFIG_NAME if name is None else f"{name}.debate.json")


def mailbox_path(root: Path, name: str | None = None) -> Path:
    return root / (CHANNEL_NAME if name is None else f"{name}.channel.md")


def _signal_path(root: Path, name: str | None) -> Path:
    return root / (SIGNAL_NAME if name is None else f"{name}.signal.json")


def _lock_path(root: Path, name: str | None) -> Path:
    return root / (LOCK_NAME if name is None else f"{name}.lock")


@dataclass(frozen=True)
class ChannelConfig:
    """Two named parties plus a supervisor, fixed at channel init.

    ``name`` is the channel's instance id (``<label>-<NNNNN>``), generated
    once at init and stored — or ``None`` for a legacy-layout channel.
    ``project`` is the absolute path of the repo this channel serves; when
    set, ``post`` refuses citations that resolve to any other repo.
    """

    parties: tuple[str, str]
    supervisor: str
    thread_cap: int = 12
    name: str | None = None
    project: str | None = None
    managed_version: int | None = None

    def __post_init__(self) -> None:
        names = (*self.parties, self.supervisor)
        if len(set(names)) != 3:
            raise ChannelError(f"parties and supervisor must be three distinct names, got {names}")
        for name in names:
            if not _SLUG_RE.fullmatch(name):
                raise ChannelError(f"invalid party name {name!r} (lowercase alphanumerics and dashes)")
        if self.thread_cap < 2:
            raise ChannelError("thread_cap must be >= 2 (a request and a reply)")
        if isinstance(self.managed_version, bool) or self.managed_version not in (None, *SUPPORTED_MANAGED_VERSIONS):
            raise ChannelError(
                f"unsupported managed_version {self.managed_version!r}; "
                f"this release supports {SUPPORTED_MANAGED_VERSIONS}"
            )

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


def discover_channel(root: Path, channel: str | None = None) -> str | None:
    """Resolve which channel in ``root`` a command addresses.

    Returns the instance id, or ``None`` for the legacy layout. An explicit
    ``channel`` must exist; without one, exactly one channel in the folder is
    used — two or more is a refusal naming each, because guessing between
    channels is how a message lands in the wrong project's record. An empty
    folder resolves to legacy: 0.3.1 read a fresh doorbell there, and
    discovery must not turn that into a refusal.
    """
    named = sorted(path.name[: -len(".debate.json")] for path in root.glob("*.debate.json"))
    if channel is not None:
        if channel in named:
            return channel
        available = ", ".join(named) if named else "none"
        raise ChannelError(
            f"refused: no channel named {channel!r} in {root} (named channels here: {available})"
        )
    has_legacy = (root / CONFIG_NAME).exists()
    candidates: list[str | None] = ([None] if has_legacy else []) + list(named)
    if len(candidates) > 1:
        shown = ", ".join("legacy (debate.json)" if c is None else c for c in candidates)
        raise ChannelError(
            f"refused: {root} holds more than one channel ({shown}); pass --channel <id>"
        )
    return candidates[0] if candidates else None


def migrate_channel(root: Path, label: str | None = None) -> str:
    """Rename a legacy channel in place to the named layout; return its new id.

    A pure rename: the mailbox and every archive file move byte-untouched —
    ``verify``/``read`` before and after is the acceptance test, archive
    included. The config is the ONE file whose content changes: it gains the
    generated ``name``, because identity is recorded there. Runs under the
    legacy writer lock so a concurrent ``post`` can never land between two
    renames and strand a half-migrated channel.
    """
    if not (root / CONFIG_NAME).exists():
        raise ChannelError(
            f"refused: no legacy channel at {root} (nothing named {CONFIG_NAME}); "
            "named channels never need migrating"
        )
    with exclusive(root):
        raw = json.loads((root / CONFIG_NAME).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ChannelError(f"refused: {root / CONFIG_NAME} is not a JSON object; fix it before migrating")
        # Crash-safe ordering: the id is committed into the LEGACY config
        # before any file moves. A migration interrupted at any later point
        # leaves a channel still discoverable as legacy, carrying the id it
        # was moving to - a re-run reads it back and finishes the same
        # migration instead of generating a second id and stranding the
        # already-renamed files.
        recorded = raw.get("name")
        if isinstance(recorded, str) and _SLUG_RE.fullmatch(recorded):
            name = recorded  # resuming an interrupted migration
        else:
            name = generate_channel_id(root, label=label)
            raw["name"] = name
            # A migrated channel gains the project binding a named init would
            # have recorded - otherwise a legacy channel could never be bound.
            raw.setdefault("project", _derived_project(root))
            _atomic_write(root / CONFIG_NAME, json.dumps(raw, indent=2))
        # Mailbox, doorbell and archive RENAME - bytes never pass through
        # this process. Missing files are skipped: the doorbell is gitignored
        # and legitimately absent, and a resumed run finds some already moved.
        if (root / CHANNEL_NAME).exists():
            (root / CHANNEL_NAME).rename(mailbox_path(root, name))
        if (root / SIGNAL_NAME).exists():
            (root / SIGNAL_NAME).rename(_signal_path(root, name))
        archive = root / ARCHIVE_DIR
        if archive.is_dir():
            for path in sorted(archive.glob("CHANNEL-*.md")):
                month = path.name[len("CHANNEL-") : -len(".md")]
                path.rename(archive / _archive_month_name(name, month))
            if (archive / ARCHIVE_INDEX).exists():
                (archive / ARCHIVE_INDEX).rename(archive / _archive_index_name(name))
        _atomic_write(_config_path(root, name), json.dumps(raw, indent=2))
        (root / CONFIG_NAME).unlink()
    return name


def _random_digits() -> str:
    import secrets  # local import keeps module load light

    return f"{secrets.randbelow(100000):05d}"


def _derived_project(root: Path) -> str:
    """The absolute path of the repo this channel serves.

    The enclosing git repo's toplevel; outside any repo, the channel
    folder's parent — the same two-tier rule as the label, kept in path form.
    """
    import subprocess  # local import keeps module load light

    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return str(Path(result.stdout.strip()).resolve())
    except (OSError, subprocess.SubprocessError):
        pass
    return str(root.resolve().parent)


def _derived_label(root: Path) -> str:
    """Default label: the enclosing repo's directory name.

    Pinned at plan review (fold N4, MSG-2): basename of
    ``git rev-parse --show-toplevel`` for the channel folder; outside any git
    repo, the channel folder's PARENT directory basename. Derived names are
    sanitized to the slug grammar — a directory name is nobody's recorded
    words, and the operator can always override with an explicit label.
    """
    import subprocess  # local import keeps module load light

    raw = ""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            raw = Path(result.stdout.strip()).name
    except (OSError, subprocess.SubprocessError):
        raw = ""
    if not raw:
        raw = root.resolve().parent.name
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]", "-", raw.lower())).strip("-")
    if not slug or not _SLUG_RE.fullmatch(slug):
        raise ChannelError(
            f"refused: cannot derive a channel label from {raw!r}; pass --label explicitly"
        )
    return slug


def generate_channel_id(root: Path, label: str | None = None) -> str:
    """Generate the channel's instance id: ``<label>-<NNNNN>``.

    The id is generated ONCE, here, and stored in the config — never
    re-derived — so it stays stable when the folder or project is renamed.
    An EXPLICIT label is the operator's words and is refused when invalid,
    never sanitized. Collisions with files already in ``root`` regenerate;
    exhausting the retries refuses rather than reusing an id.
    """
    if label is not None:
        if not _SLUG_RE.fullmatch(label):
            raise ChannelError(f"invalid label {label!r} (lowercase alphanumerics and dashes)")
    else:
        label = _derived_label(root)
    for _ in range(100):
        candidate = f"{label}-{_random_digits()}"
        if not any(root.glob(f"{candidate}.*")):
            return candidate
    raise ChannelError(
        f"refused: could not find a free channel id for label {label!r} in {root} after 100 tries"
    )


def init_channel(
    root: Path,
    parties: tuple[str, str],
    supervisor: str,
    thread_cap: int = 12,
    name: str | None = None,
    managed_version: int | None = None,
) -> ChannelConfig:
    """Create a channel: config + empty mailbox + fresh doorbell.

    With ``name`` the files carry the id prefix (``<name>.debate.json``,
    ``<name>.channel.md``, ``<name>.signal.json``), so several channels can
    coexist in one folder. Without it, the legacy 0.3.1 filenames and absent
    managed marker are preserved; the corrected default cap is 12 everywhere.
    """
    if name is not None and not _SLUG_RE.fullmatch(name):
        raise ChannelError(f"invalid channel name {name!r} (lowercase alphanumerics and dashes)")
    project = _derived_project(root) if name is not None else None
    # Every newly named channel is managed. The unnamed library path exists
    # only for 0.3.x compatibility; migration preserves its absent marker so
    # an old human-driven channel is never silently reclassified.
    if name is not None and managed_version is None:
        managed_version = MANAGED_VERSION
    config = ChannelConfig(
        parties=parties,
        supervisor=supervisor,
        thread_cap=thread_cap,
        name=name,
        project=project,
        managed_version=managed_version,
    )
    root.mkdir(parents=True, exist_ok=True)
    config_path = _config_path(root, name)
    if config_path.exists():
        what = f"channel {name!r}" if name is not None else "channel"
        raise ChannelError(f"{what} already initialized at {root}")
    payload: dict[str, object] = {
        "parties": list(config.parties),
        "supervisor": config.supervisor,
        "thread_cap": config.thread_cap,
    }
    if name is not None:
        # A named channel records the project and managed version it serves;
        # the legacy library path keeps the old shape and records neither.
        payload["name"] = name
        payload["project"] = project
        payload["managed_version"] = config.managed_version
    _atomic_write(config_path, json.dumps(payload, indent=2))
    mailbox_path(root, name).touch()
    _atomic_write(_signal_path(root, name), json.dumps(_fresh_signal(), indent=2))
    return config


def load_config(root: Path, name: str | None = None) -> ChannelConfig:
    path = _config_path(root, name)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ChannelError(f"refused: unreadable channel config {path}: {error}") from error
    if not isinstance(raw, dict):
        raise ChannelError(
            f"refused: channel config {path} must be a JSON object, got {type(raw).__name__}"
        )
    try:
        parties = raw["parties"]
        supervisor = raw["supervisor"]
    except KeyError as error:
        raise ChannelError(f"refused: channel config {path} is missing required key {error.args[0]!r}") from error
    if not isinstance(parties, list) or len(parties) != 2:
        raise ChannelError(f"config parties must be a two-item list, got {parties!r}")
    if name is not None and raw.get("name") != name:
        # Identity lives in the file stem AND the recorded id; when they
        # disagree, which one is the channel? Refuse rather than guess.
        raise ChannelError(
            f"refused: {_config_path(root, name).name} records name {raw.get('name')!r}, "
            f"which disagrees with its filename; fix the config before using this channel"
        )
    project = raw.get("project")
    managed_version = raw.get("managed_version")
    if isinstance(managed_version, bool) or (
        managed_version is not None and not isinstance(managed_version, int)
    ):
        raise ChannelError(
            f"refused: {_config_path(root, name).name} records invalid "
            f"managed_version {managed_version!r}"
        )
    try:
        return ChannelConfig(
            parties=(str(parties[0]), str(parties[1])),
            supervisor=str(supervisor),
            thread_cap=int(raw.get("thread_cap", 12)),
            name=name,
            project=str(project) if project is not None else None,
            managed_version=managed_version,
        )
    except (TypeError, ValueError) as error:
        raise ChannelError(f"refused: invalid channel config {path}: {error}") from error


def read_signal(root: Path, name: str | None = None) -> dict[str, object]:
    path = _signal_path(root, name)
    if not path.exists():
        return _fresh_signal()
    try:
        return dict(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError, TypeError, ValueError) as error:
        # A torn/truncated write or a file that vanished mid-read must refuse
        # deterministically - callers only guard for ChannelError, and a raw
        # error would otherwise surface as a traceback.
        #
        # The tuple originally listed (JSONDecodeError, OSError) and therefore
        # did NOT cover what the line above can actually throw:
        #   - valid non-dict JSON (42, true, null, [1,2]) -> dict() raises
        #     TypeError;
        #   - non-UTF-8 bytes -> read_text raises UnicodeDecodeError (a
        #     ValueError, and NOT a JSONDecodeError).
        # Both escaped the contract. This is not cosmetic: the watcher reads
        # the signal itself before it reaches any verification, so either input
        # crash-looped the tick under the 60s timer - the exact silent/loud
        # failure the verify slice exists to remove. signal.json is a plain
        # gitignored editable file, i.e. the same "anyone who can edit it"
        # vector as the mailbox. Found at review, MSG-168.
        raise ChannelError(f"refused: unreadable signal file {path}: {error}") from error


def read_entries(root: Path, name: str | None = None) -> list[Entry]:
    """Parse the mailbox. Malformed lines between headers ride along as body."""
    path = mailbox_path(root, name)
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


def thread_entries(root: Path, thread: str, name: str | None = None) -> list[Entry]:
    return [entry for entry in read_entries(root, name) if entry.thread == thread]


def turn_parked_since(root: Path, now: datetime, name: str | None = None) -> tuple[int | None, int] | None:
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
    signal = read_signal(root, name)
    open_thread = str(signal.get("thread", ""))
    if not open_thread or not str(signal.get("turn", "")):
        return None
    config = load_config(root, name)
    stamp_text = ""
    try:
        seq = _as_int(signal.get("seq", 0))
    except (ChannelError, ValueError, TypeError):
        seq = 0  # corrupt/missing seq: never raise, just report unknown
    for entry in reversed(read_entries(root, name)):
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
    name: str | None = None,
    _brokered: bool = False,
    _initial_turn: str | None = None,
) -> str:
    """Validate against the protocol, append the entry, bump the doorbell.

    Returns the assigned entry id; raises :class:`ChannelError` when the post
    is refused — in that case nothing was written.
    """
    config = load_config(root, name)
    body = body.strip()
    if not body:
        raise ChannelError("refused: empty body")
    if entry_type not in ENTRY_TYPES:
        raise ChannelError(f"refused: unknown entry type {entry_type!r} (one of {ENTRY_TYPES})")
    if sender != config.supervisor and sender not in config.parties:
        raise ChannelError(f"refused: unknown sender {sender!r} (parties {config.parties}, supervisor {config.supervisor!r})")
    if config.managed_version == BROKERED_MANAGED_VERSION and sender in config.parties and not _brokered:
        raise ChannelError(
            "refused: managed party entries are controller-brokered; the adapter may not "
            "self-assert --from or post directly"
        )
    if _initial_turn is not None:
        if (
            config.managed_version != BROKERED_MANAGED_VERSION
            or sender != config.supervisor
            or entry_type != "review-request"
            or _initial_turn not in config.parties
        ):
            raise ChannelError(
                "refused: an initial party turn is controller-only, supervisor-authored, "
                "and valid only for a brokered review-request"
            )
    if not _SLUG_RE.fullmatch(thread):
        raise ChannelError(f"refused: invalid thread slug {thread!r} (lowercase alphanumerics and dashes)")
    # The mailbox is re-parsed line-anchored by _HEADER_RE, so a BODY line in
    # that grammar becomes a real entry - a forged one, attributable to anyone,
    # and indistinguishable from a genuine entry in `git diff`. Quoting a prior
    # message is the accidental path into this, which is why the refusal below
    # says how to quote safely instead of just saying no. Checked against the
    # SAME pattern the parser uses: a second hand-maintained pattern would drift
    # and reopen the hole silently. Runs on the STRIPPED body and before the
    # lock, so a refusal costs no lock and reflects exactly what would be
    # written.
    for offset, line in enumerate(body.splitlines(), start=1):
        if _HEADER_RE.match(line):
            raise ChannelError(
                f"refused: body line {offset} would parse as an entry header and forge an "
                f"entry into the record: {line!r}. Quote it as a blockquote ('> ## MSG-...') "
                "or inside a code fence. Indenting the FIRST line does not work - the body "
                "is stripped before it is written."
            )
    # refs is interpolated into the header LINE, so a line break in it splits
    # that line and everything after the break is re-parsed as record structure.
    #
    # Do NOT hand-list separators here. `read_entries` re-splits the file with
    # str.splitlines(), which breaks on a SUPERSET of \n and \r: \v \f \x1c
    # \x1d \x1e \x85 (NEL)   (LS)   (PS). The first version of this
    # guard listed \n and \r only, and all five exotic separators still forged
    # an entry through refs (found at review, MSG-163) - the same "a second
    # hand-maintained pattern drifts and reopens the hole" failure the body
    # guard above is written to avoid, one field over. So ask the parser's own
    # mechanism whether this value survives a split unchanged.
    lines = refs.splitlines()
    if lines and (len(lines) > 1 or lines[0] != refs):
        raise ChannelError(
            "refused: refs must be a single line - it is written into the entry header, "
            f"and a line break there forges an entry when the record is re-parsed: {refs!r}"
        )
    if force and sender != config.supervisor:
        raise ChannelError(
            f"refused: force is supervisor-only (supervisor {config.supervisor!r}); "
            "a party cannot bypass one-thread-at-a-time"
        )
    # One channel carries one project. A bound channel refuses citations that
    # resolve anywhere but its own repo - this is the rule that would have
    # stopped the MSG-180 cross-post (a debate-bench review conducted through
    # this repo's channel) at the moment it happened, not a week later.
    # force is already supervisor-only by the check above, so the escape
    # hatch stays where every other escape hatch lives. Runs before the lock:
    # a refusal costs no lock, and nothing was written.
    if config.project is not None and not force:
        _refuse_foreign_refs(refs, Path(config.project))

    with exclusive(root, name):
        signal = read_signal(root, name)
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
        if open_thread and _initial_turn is not None:
            raise ChannelError("refused: a controller initial turn can only open a new thread")
        if open_thread and thread == open_thread and entry_type != "close":
            count = len(thread_entries(root, thread, name))
            if count >= config.thread_cap:
                raise ChannelError(
                    f"refused: thread '{thread}' is at its {config.thread_cap}-entry cap; "
                    "the supervisor must post or the thread must be closed"
                )

        seq = _as_int(signal["seq"]) + 1
        entry_id = f"MSG-{seq}"
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        header = f"## {entry_id} | {stamp} | from: {sender} | type: {entry_type} | thread: {thread} | refs: {refs or '-'}"
        with mailbox_path(root, name).open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(f"\n{header}\n\n{body}\n")

        # A turn is only meaningful WITHIN an open thread. On close, clear it
        # along with the thread — leaving it pointing at the non-closer invites
        # watchers to fire on a turn that no longer means anything. (Lesson from
        # the first production deployment: see docs/case-study.)
        if entry_type == "close":
            new_turn = ""
        elif _initial_turn is not None:
            new_turn = _initial_turn
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
            _signal_path(root, name),
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
_SHA_RE = re.compile(r"@([0-9a-fA-F]{7,40})\b")


def _archive_index_name(name: str | None) -> str:
    return ARCHIVE_INDEX if name is None else f"{name}-INDEX.md"


def _archive_month_name(name: str | None, month: str) -> str:
    return f"CHANNEL-{month}.md" if name is None else f"{name}-{month}.md"


def archive_month_files(root: Path, name: str | None = None) -> list[Path]:
    """This channel's archive month files, sorted. The month pattern
    (????-??) cannot match the -INDEX file, so no filtering is needed."""
    archive = root / ARCHIVE_DIR
    if not archive.is_dir():
        return []
    pattern = "CHANNEL-*.md" if name is None else f"{name}-????-??.md"
    return sorted(archive.glob(pattern))


def _archive_banner(name: str | None) -> str:
    index = _archive_index_name(name)
    return (
        f"> Older closed threads relocate verbatim to archive/ (see archive/{index}). "
        "Entries are never edited - `debate compact` only moves them."
    )


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


ANOMALY = "ANOMALY"
INFO = "INFO"


@dataclass(frozen=True)
class Anomaly:
    """One finding from :func:`verify_record`.

    ``ANOMALY`` means the record disagrees with itself and a human should look.
    ``INFO`` is a legitimate-but-notable shape (a compaction gap, a missing
    doorbell) that must NEVER be reported as failure — refusing those was the
    first draft of this slice and it would have rejected healthy records.
    """

    level: str
    code: str
    detail: str

    def __str__(self) -> str:
        return f"{self.level}: {self.code} - {self.detail}"


def _record_files(root: Path, name: str | None = None) -> list[Path]:
    """The channel's mailbox plus every one of ITS archive files, in reading order."""
    files = [mailbox_path(root, name), *archive_month_files(root, name)]
    return [path for path in files if path.exists()]


def verify_record(root: Path, name: str | None = None) -> list[Anomaly]:
    """Check the record against itself. Pure: reads only, and NEVER raises.

    The caller owns the lock. This deliberately does not take one:
    :func:`exclusive` is ``O_CREAT | O_EXCL`` and therefore not reentrant, so a
    self-locking version called from inside the watcher's own locked block
    would deadlock against itself.

    What is and is not an anomaly was settled by review (MSG-156/158/160), and
    the negative results matter more than the positive ones:

    - A GAP is legitimate. ``compact`` relocates BY THREAD SLUG, so archiving
      one of two force-interleaved threads leaves a hole in a healthy mailbox.
    - A DUPLICATE seq is reported, because ``post`` appends to the mailbox
      before bumping the doorbell and a crash in that window repeats a number —
      that is worth a human's attention even though it is not forgery.
    - MAILBOX MAX > DOORBELL is the load-bearing check: compaction only ever
      removes LOW seqs and never writes the doorbell, and ``force`` always sets
      the doorbell to the new seq, so under every legitimate HISTORY the
      mailbox maximum cannot exceed it. It is valid only on a consistent
      snapshot, which is why the caller must hold the lock — reading the two
      files unlocked races an ordinary ``post`` and false-positives on healthy
      data.
    - An ABSENT doorbell is INFO, not failure: ``read_signal`` returns a fresh
      ``seq 0`` when the file is merely missing, and ``signal.json`` is
      gitignored, so a fresh clone would otherwise look tampered.
    """
    findings: list[Anomaly] = []
    mailbox_max = 0
    mailbox_name = mailbox_path(root, name).name

    for path in _record_files(root, name):
        try:
            _, entries = read_raw(path)
        except (OSError, ValueError) as error:
            # ValueError covers UnicodeDecodeError: read_raw decodes as UTF-8,
            # and a record corrupted to non-UTF-8 bytes is exactly the sort of
            # damage this function exists to REPORT rather than die on. Caught
            # by this file's own never-raises test.
            findings.append(Anomaly(ANOMALY, "unreadable-record", f"{path.name}: {error}"))
            continue
        seqs = [entry.seq for entry in entries]
        if path.name == mailbox_name:
            mailbox_max = max(seqs, default=0)

        seen: set[int] = set()
        for seq in seqs:
            if seq in seen:
                findings.append(
                    Anomaly(ANOMALY, "duplicate-seq", f"{path.name}: MSG-{seq} appears more than once")
                )
            seen.add(seq)

        ordered = sorted(seen)
        gaps = [
            (low, high)
            for low, high in zip(ordered, ordered[1:])
            if high != low + 1
        ]
        for low, high in gaps:
            findings.append(
                Anomaly(INFO, "gap", f"{path.name}: MSG-{low} -> MSG-{high} (legitimate after a by-thread compaction)")
            )

    signal_path = _signal_path(root, name)
    if not signal_path.exists():
        findings.append(
            Anomaly(INFO, "no-doorbell", f"{signal_path.name} is absent; the mailbox-ahead check needs it and was skipped")
        )
        return findings
    try:
        signal = read_signal(root, name)
        doorbell = _as_int(signal.get("seq", 0))
    except (ChannelError, OSError, ValueError) as error:
        # read_signal has a THIRD state beyond absent and parseable: a torn
        # write RAISES ChannelError (execution note carried from MSG-160).
        #
        # OSError/ValueError are here because read_signal's own guard catches
        # (JSONDecodeError, OSError) and therefore does NOT convert a
        # UnicodeDecodeError - a non-UTF-8 doorbell escapes it as a raw
        # ValueError, defeating its documented "refuse deterministically"
        # contract. Found while probing this slice; verify_record must not
        # inherit that hole, since it promises never to raise. The underlying
        # read_signal gap is reported separately - it is not this slice's fix.
        findings.append(Anomaly(ANOMALY, "unreadable-doorbell", f"{signal_path.name}: {error}"))
        return findings

    if mailbox_max > doorbell:
        findings.append(
            Anomaly(
                ANOMALY,
                "mailbox-ahead-of-doorbell",
                f"mailbox holds MSG-{mailbox_max} but the doorbell is at seq {doorbell}; "
                "an entry was written without going through post()",
            )
        )
    return findings


def compact(
    root: Path,
    keep_days: float = 14.0,
    now: datetime | None = None,
    dry_run: bool = False,
    name: str | None = None,
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
    signal = read_signal(root, name)
    seq_before = _as_int(signal["seq"])
    open_thread = str(signal.get("thread", ""))
    stamp_now = now or datetime.now(timezone.utc)

    preamble, entries = read_raw(mailbox_path(root, name))
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
        month_file = _archive_month_name(name, f"{last_at:%Y-%m}")
        moves.setdefault(month_file, []).extend(e.raw for e in blocks)
        seqs = sorted(e.seq for e in blocks)
        index_lines.append(
            f"- {thread}: MSG-{seqs[0]}..MSG-{seqs[-1]} ({len(seqs)} entries, closed {last.timestamp}) -> {month_file}"
        )
        report.append(f"archived {thread}: MSG-{seqs[0]}..MSG-{seqs[-1]} ({len(seqs)} entries) -> {month_file}")

    if dry_run:
        return ["dry-run, nothing written", *report]

    archived_seqs = {e.seq for thread in moving for e in by_thread[thread]}

    with exclusive(root, name):
        # Defense-in-depth: planning happened outside the lock; a writer that
        # bypasses the lock (hand edits, an old client) shows up as a moved seq.
        if _as_int(read_signal(root, name)["seq"]) != seq_before:
            raise ChannelError("refused: the channel changed while compacting; run again")

        # Re-read FRESH inside the lock and keep by seq, not by planning
        # snapshot: entries archived are closed and immutable, so anything
        # else — whatever its thread slug — is kept exactly as found.
        preamble, entries = read_raw(mailbox_path(root, name))
        kept_raw = "".join(e.raw for e in entries if e.seq not in archived_seqs)
        banner = _archive_banner(name)
        if banner not in preamble:
            preamble = f"{banner}\n{preamble}" if preamble.strip() else f"{banner}\n"

        archive_root = root / ARCHIVE_DIR
        archive_root.mkdir(exist_ok=True)
        for month_file, raws in moves.items():
            with (archive_root / month_file).open("a", encoding="utf-8", newline="") as handle:
                for raw in raws:
                    if not raw.startswith("\n"):
                        handle.write("\n")
                    handle.write(raw)
        with (archive_root / _archive_index_name(name)).open("a", encoding="utf-8", newline="") as handle:
            for line in index_lines:
                handle.write(line + "\n")
        _atomic_write(mailbox_path(root, name), preamble + kept_raw)
    return report


def _refuse_foreign_refs(refs: str, project: Path) -> None:
    """Refuse ``name@sha`` citations that do not resolve in the channel's project.

    Refs WITHOUT a sha citation pass untouched — a plan-doc path is not a
    commit and carries no repo identity. This deliberately reuses the record's
    own citation grammar (``_SHA_RE``): a second hand-maintained pattern here
    would drift from ``verify_refs`` and reopen the cross-post hole one field
    over, the MSG-163 failure shape.
    """
    import subprocess  # local import keeps module load light

    for sha in _SHA_RE.findall(refs):
        try:
            result = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except FileNotFoundError as error:
            raise ChannelError(
                "refused: this channel is bound to a project and checking a citation needs git on PATH"
            ) from error
        if result.returncode != 0:
            raise ChannelError(
                f"refused: refs cite {sha!r}, which is not a commit in this channel's project "
                f"{project}. One channel carries one project - post this review to the channel "
                "of the repo it cites, or the supervisor may force a deliberate exception."
            )


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
def exclusive(root: Path, name: str | None = None) -> Iterator[None]:
    """Hold the channel's writer lock: O_EXCL-create ``root/.lock``
    (``root/<name>.lock`` for a named channel — each channel has its own).

    Advisory but honoured by every shipped writer (``post``, ``compact``),
    which makes each one's check-then-write atomic with respect to the
    others. A lock older than the stale window belongs to a crashed holder
    and is broken; waiting past the timeout refuses rather than queueing
    forever.
    """
    import time  # local import keeps module load light

    lock = _lock_path(root, name)
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
