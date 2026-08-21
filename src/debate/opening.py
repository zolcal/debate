"""`debate open`: mint a debate with its pair picked at birth.

One debate = one channel (owner ruling, plan 2026-08-15): born for a subject,
pair pinned for life, closed when the subject resolves. The pair comes from
the host registry; the owner picks, defaulting to the previous pick. ALL
validation runs before the first byte lands in the target root, through the
real loader's `channel_config` seam -- never through `setup.apply`, which
writes the wizard's defaults cache as a side effect (plan fold H2).
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, Sequence

from . import channel
from .seats import Registry, Seat
from .setup import SetupSpec, build_prompt, derive_paths, scaffold_protocol, validate

_SLUG_KEEP = re.compile(r"[^a-z0-9-]+")

# How much review material still counts as a small review, in bytes (16 KiB).
# Below it a quick pair is enough; at or above it the strongest pair is worth
# its cost. A per-debate setting: every open may say its own number.
QUICK_REVIEW_MAX_BYTES = 16384


class _LoadedConfig(Protocol):
    def managed_problem(self) -> str | None: ...


LoadConfigFn = Callable[..., "_LoadedConfig"]


@dataclass
class OpenSpec:
    root: Path
    label: str
    pair: tuple[str, str]
    supervisor: str = "owner"
    thread_cap: int = 12
    allow_identical_seats: bool = False
    assume_yes: bool = False
    allow_mismatched_pair: bool = False


@dataclass
class OpenResult:
    channel_name: str
    config_path: Path
    hints: list[str]


def project_key(root: Path) -> str:
    """The `last_pair` key: the git toplevel, never the --root folder (H4)."""
    return channel._derived_project(root)


@dataclass
class BrokeredOpenSpec:
    """`debate open --brokered`: the v0.8 product path. Managed version 2,
    always; the interactive host stays outside both seats and the human is
    the supervisor."""

    root: Path
    label: str
    pair: tuple[str, str]
    source_ref: str
    author_vendor: str  # the interactive author's vendor (e.g. "claude", "codex")
    runtime_root: Path | None = None
    supervisor: str = "owner"
    thread_cap: int = 12
    allow_identical_seats: bool = False
    allow_mismatched_pair: bool = False
    docket_files: tuple[str, ...] = ()  # project-relative review inputs for the seats
    # Where the line between a small review and a full one falls for THIS
    # debate, in bytes; recorded for the tools that suggest a pair later.
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES


def slugify_seat_id(seat_id: str) -> str:
    """A party name from a seat id, legal under the channel slug rule: every
    char outside [a-z0-9-] becomes '-', runs collapse, edges strip -- so
    codex/gpt-5.6-sol@high -> codex-gpt-5-6-sol-high (fold B3)."""
    slug = _SLUG_KEEP.sub("-", seat_id.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise channel.ChannelError(f"refused: seat id {seat_id!r} slugifies to nothing")
    return slug


def _seatable(registry: Registry, seat_id: str) -> Seat:
    seat = registry.seats.get(seat_id)
    if seat is None:
        raise channel.ChannelError(f"refused: no seat {seat_id!r} in the registry")
    if not seat.present:
        raise channel.ChannelError(
            f"refused: seat {seat_id!r} is marked ABSENT (its binary vanished); "
            "run: debate seats discover"
        )
    from .seats import head_resolves

    head = seat.commands[0][0]
    if not head_resolves(head):
        raise channel.ChannelError(
            f"refused: seat {seat_id!r} command {head!r} no longer resolves; "
            "run: debate seats discover"
        )
    return seat


def _identity_guard(a: Seat, b: Seat, *, allow_identical: bool) -> None:
    if a.seat_id == b.seat_id:
        raise channel.ChannelError(
            f"refused: the same seat twice ({a.seat_id}); "
            "--allow-identical-seats does not cover a literal same-seat pick"
        )
    if a.commands[0] == b.commands[0]:
        raise channel.ChannelError(
            "refused: both picks run the identical SELECTED argv -- one pipe "
            "under two names is never a debate"
        )
    if (a.vendor, a.submodel) == (b.vendor, b.submodel) and not allow_identical:
        raise channel.ChannelError(
            f"refused: {a.seat_id} and {b.seat_id} are the same weights arguing "
            "with themselves (effort ignored -- same vendor/submodel); a "
            "monologue marketed as a debate. Two labels for one serving are "
            "undetectable from outside; pass --allow-identical-seats to seat "
            "this pair anyway"
        )


# What an uneven pair costs, in the words of what was actually observed.
UNEVEN_PAIR_REASON = (
    "a lightweight fast model against a frontier reasoning model often "
    "produces a one-sided verdict and costs an extra deliberation round"
)


def classify_pair(a: Seat, b: Seat) -> str:
    """How evenly matched two seats are: "symmetric", "mismatched" or
    "undeclared" (one of them never declared a capability class)."""
    if a.capability_class is None or b.capability_class is None:
        return "undeclared"
    return "symmetric" if a.capability_class == b.capability_class else "mismatched"


def _uneven_pair_sentence(a: Seat, b: Seat) -> str:
    return (
        f"{a.seat_id} is declared {a.capability_class} and {b.seat_id} is "
        f"declared {b.capability_class}: {UNEVEN_PAIR_REASON}"
    )


def _pair_gate(
    a: Seat,
    b: Seat,
    *,
    allow_mismatched_pair: bool,
    ask: Callable[[str], str] | None,
) -> None:
    """The last gate before a pair is seated (after selection, the identity
    guard and admission). An uneven pair is legal but never silent: where
    somebody can answer, it is a numbered choice; where nobody can (--yes, or
    the fully managed path, which asks nothing), it refuses and names the flag
    that seats it deliberately."""
    kind = classify_pair(a, b)
    if kind == "symmetric":
        return
    if kind == "undeclared":
        print(
            "note: one of these seats has no declared capability class; "
            "pairing may be uneven"
        )
        return
    if allow_mismatched_pair:
        return
    if ask is None:
        raise channel.ChannelError(
            f"refused: {_uneven_pair_sentence(a, b)}. "
            "Pass --allow-mismatched-pair to seat this pair anyway"
        )
    print(f"warning: {_uneven_pair_sentence(a, b)}.")
    if ask("1 keep this pair  2 pick again: ").strip() != "1":
        raise channel.ChannelError("refused: pair not confirmed")


# How many pairs the numbered list shows before it says how many it left out.
PAIR_MENU_LIMIT = 6

QUICK_PAIR_REASON = "small review, quick pair"
FULL_PAIR_REASON = "full review, strongest pair"
REMEMBERED_PAIR_REASON = "the pair you picked last time"


def docket_byte_size(project: str | Path, docket_files: Sequence[str]) -> int:
    """How much review material this debate hands its seats, in bytes.

    Names are project-relative; one that is absolute, missing or unreadable
    counts as nothing, because this only sizes a suggestion. The open itself
    refuses such a name later, with the name in the refusal.
    """
    base = Path(project)
    total = 0
    for name in docket_files:
        candidate = Path(name)
        if candidate.is_absolute():
            continue
        try:
            total += (base / candidate).stat().st_size
        except OSError:
            continue
    return total


def _wanted_class(docket_bytes: int, quick_review_max_bytes: int) -> str:
    return "light" if docket_bytes < quick_review_max_bytes else "frontier"


def admission_problem(seat: Seat, *, real_home: Path) -> str | None:
    """Why a fully managed debate could not seat this one, in the words it
    would refuse with -- or None when it can (plan 3.4).

    ONE test, two readers: seating raises what this returns, and the
    suggestion layer drops any seat it names. A command that reads a request
    file and writes an answer file already speaks the protocol. A command that
    only takes the question text is run under Debate's own runner, and that
    runner needs the seat's isolation and no-saving settings on record, plus a
    configuration folder that still passes the rule that admitted it -- the
    registry may have been hand-edited since it was written.
    """
    argv = " ".join(seat.commands[0])
    if "{input_path}" in argv and "{result_path}" in argv:
        return None
    if "{prompt}" not in argv:
        return (
            f"refused: seat {seat.seat_id!r} cannot take part in a fully managed debate: "
            "its command has nowhere to put the question, and it does not take the two "
            "files a managed pass hands over either. Record a command that takes the "
            "question text (debate seats add), or one that reads a request file and "
            "writes an answer file"
        )
    # Admission, and the only admission: no verified isolation and no-history
    # settings, no managed run. There is no flag that waives this.
    if not seat.isolation_argv or not seat.no_persistence_argv:
        return (
            f"refused: {seat.seat_id} can't yet run in the isolated mode a managed "
            "debate needs: tell me how it turns off its settings, plugins and session "
            "saving and I'll record that (debate seats add ... --isolation-argv ... "
            "--no-persistence-argv ...), or use a custom seat command"
        )
    if seat.config_home:
        from .seats import validate_config_home

        try:
            validate_config_home(seat.config_home, home=real_home)
        except channel.ChannelError as error:
            return str(error)
    return None


def _pairable(first: Seat, second: Seat) -> bool:
    """Two seats the identity guard would let through: different seats,
    different commands, and not one serving under two labels."""
    return (
        first.seat_id != second.seat_id
        and first.commands[0] != second.commands[0]
        and (first.vendor, first.submodel) != (second.vendor, second.submodel)
    )


def _home(real_home: Path | None) -> Path:
    return Path.home() if real_home is None else real_home


def _offerable_seats(
    registry: Registry, allowlist: tuple[str, ...] | None, real_home: Path
) -> list[Seat]:
    """Every seat this project may put in a suggestion, in seat-id order."""
    from .seats import head_resolves

    return [
        seat
        for seat_id, seat in sorted(registry.seats.items())
        if seat.present
        and (allowlist is None or seat_id in allowlist)
        and head_resolves(seat.commands[0][0])
        and admission_problem(seat, real_home=real_home) is None
    ]


def remembered_pair(
    registry: Registry,
    *,
    project: str,
    allowlist: tuple[str, ...] | None,
    real_home: Path | None = None,
) -> tuple[str, str] | None:
    """The pair this project used last time, if it can still be seated.

    A remembered pair outside the project's approved list, one naming a seat
    that has since vanished, or one naming a seat that can no longer run under
    Debate's control is DROPPED rather than offered. Never having said how
    strong its seats are does NOT drop it: it is the user's own last choice,
    and it is offered as exactly that.
    """
    home = _home(real_home)
    for default in (registry.last_pair.get(project), registry.last_pair.get("")):
        if not default or len(default) != 2:
            continue
        if allowlist is not None and not all(seat_id in allowlist for seat_id in default):
            continue
        try:
            first = _seatable(registry, default[0])
            second = _seatable(registry, default[1])
        except channel.ChannelError:
            continue
        if any(admission_problem(seat, real_home=home) is not None for seat in (first, second)):
            continue
        return (default[0], default[1])
    return None


@dataclass(frozen=True)
class PairSuggestion:
    """The pair to lead with and why, carried together so nothing downstream
    has to guess the reason back out of the pair."""

    pair: tuple[str, str]
    reason: str


def suggest_pair_with_reason(
    registry: Registry,
    *,
    allowlist: tuple[str, ...] | None,
    docket_bytes: int,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    last_pair: tuple[str, str] | None,
    real_home: Path | None = None,
) -> PairSuggestion | None:
    """The pair to put first, chosen by how much there is to review.

    Under the limit a small review is enough, so two evenly matched
    lightweight seats lead; at or above it, two evenly matched frontier seats
    do. Different vendors win over the same vendor twice, because two vendors
    disagree more usefully. A seat that could not be seated, or that never
    declared how strong it is, is never part of a FRESH suggestion -- it can
    still be picked by name. With no matched pair to offer, the pair from last
    time stands, and says so.
    """
    wanted = _wanted_class(docket_bytes, quick_review_max_bytes)
    reason = QUICK_PAIR_REASON if wanted == "light" else FULL_PAIR_REASON
    matched = [
        seat for seat in _offerable_seats(registry, allowlist, _home(real_home))
        if seat.capability_class == wanted
    ]
    same_vendor: tuple[str, str] | None = None
    for index, first in enumerate(matched):
        for second in matched[index + 1:]:
            if not _pairable(first, second):
                continue
            if first.vendor != second.vendor:
                return PairSuggestion((first.seat_id, second.seat_id), reason)
            if same_vendor is None:
                same_vendor = (first.seat_id, second.seat_id)
    if same_vendor is not None:
        return PairSuggestion(same_vendor, reason)
    return None if last_pair is None else PairSuggestion(last_pair, REMEMBERED_PAIR_REASON)


def suggest_pair(
    registry: Registry,
    *,
    allowlist: tuple[str, ...] | None,
    docket_bytes: int,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    last_pair: tuple[str, str] | None,
    real_home: Path | None = None,
) -> tuple[str, str] | None:
    """The suggested pair alone, for callers with no use for the reason."""
    found = suggest_pair_with_reason(
        registry, allowlist=allowlist, docket_bytes=docket_bytes,
        quick_review_max_bytes=quick_review_max_bytes, last_pair=last_pair,
        real_home=real_home,
    )
    return None if found is None else found.pair


def pair_choices(
    registry: Registry,
    *,
    allowlist: tuple[str, ...] | None,
    suggestion: tuple[str, str] | None,
    docket_bytes: int,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    real_home: Path | None = None,
) -> list[tuple[str, str]]:
    """The suggestion first, then every other pair this project could seat.

    The rest are ordered by how well they fit the size of this review: the
    matched pairs of the right strength first, then the other evenly matched
    ones, then the uneven ones.
    """
    if suggestion is None:
        return []
    wanted = _wanted_class(docket_bytes, quick_review_max_bytes)
    offerable = _offerable_seats(registry, allowlist, _home(real_home))
    ranked: list[tuple[int, str, str]] = []
    for index, first in enumerate(offerable):
        for second in offerable[index + 1:]:
            if not _pairable(first, second):
                continue
            if {first.seat_id, second.seat_id} == set(suggestion):
                continue
            kind = classify_pair(first, second)
            if kind == "symmetric" and first.capability_class == wanted:
                rank = 0
            elif kind == "symmetric":
                rank = 1
            else:
                rank = 2
            ranked.append((rank, first.seat_id, second.seat_id))
    return [suggestion] + [(first, second) for _rank, first, second in sorted(ranked)]


def pair_menu(
    registry: Registry,
    *,
    allowlist: tuple[str, ...] | None,
    suggestion: PairSuggestion | None,
    docket_bytes: int,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    real_home: Path | None = None,
    limit: int = PAIR_MENU_LIMIT,
) -> list[str]:
    """The choices as a numbered list, the first one carrying its reason."""
    choices = pair_choices(
        registry, allowlist=allowlist,
        suggestion=None if suggestion is None else suggestion.pair,
        docket_bytes=docket_bytes, quick_review_max_bytes=quick_review_max_bytes,
        real_home=real_home,
    )
    if not choices or suggestion is None:
        return []
    lines = [f"1  {choices[0][0]} + {choices[0][1]}  --  {suggestion.reason}"]
    for number, choice in enumerate(choices[1:limit], start=2):
        lines.append(f"{number}  {choice[0]} + {choice[1]}")
    left_out = len(choices) - limit
    if left_out > 0:
        lines.append(f"and {left_out} more")
    return lines


def pick_pair(
    registry: Registry,
    *,
    project: str,
    requested: tuple[str, str] | None,
    assume_yes: bool,
    ask: Callable[[str], str],
    now: str,
    allow_identical: bool = False,
    allow_mismatched_pair: bool = False,
    docket_bytes: int = 0,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    real_home: Path | None = None,
) -> tuple[str, str]:
    """The owner picks; the previous pick is the one-Enter default. When the
    project carries a `debate-profile.json`, the picker is RESTRICTED to its
    allowlist (section 2.10's second layer, ruling 5)."""
    from .seats import PROFILE_NAME, load_profile

    profile = load_profile(project, registry)

    def allowed(seat_id: str) -> bool:
        return profile is None or seat_id in profile.allowlist

    if requested is None:
        # The size of the review material picks the pair to lead with; the
        # pair from last time is what stands when nothing matches it.
        allowlist = None if profile is None else profile.allowlist
        suggestion = suggest_pair_with_reason(
            registry, allowlist=allowlist, docket_bytes=docket_bytes,
            quick_review_max_bytes=quick_review_max_bytes,
            last_pair=remembered_pair(
                registry, project=project, allowlist=allowlist, real_home=real_home,
            ),
            real_home=real_home,
        )
        usable = None if suggestion is None else suggestion.pair
        if assume_yes:
            if usable is None:
                raise channel.ChannelError(
                    "refused: --yes needs a usable default pair and none exists; "
                    "pass --pair a,b"
                )
            requested = usable
        else:
            from .seats import head_resolves as _resolves

            shown = pair_choices(
                registry, allowlist=allowlist, suggestion=usable,
                docket_bytes=docket_bytes, quick_review_max_bytes=quick_review_max_bytes,
                real_home=real_home,
            )[:PAIR_MENU_LIMIT]
            for line in pair_menu(
                registry, allowlist=allowlist, suggestion=suggestion,
                docket_bytes=docket_bytes, quick_review_max_bytes=quick_review_max_bytes,
                real_home=real_home,
            ):
                print(line)
            listing = ", ".join(
                sid for sid, seat in sorted(registry.seats.items())
                if seat.present and allowed(sid) and _resolves(seat.commands[0][0])
            )
            prompt = f"seatable: {listing}\npick a number, or two seats (a,b)"
            prompt += f" [default: {usable[0]},{usable[1]}]: " if usable else ": "
            answer = ask(prompt).strip()
            if not answer:
                if usable is None:
                    raise channel.ChannelError("refused: no default pair to accept")
                requested = usable
            elif answer.isdigit() and 1 <= int(answer) <= len(shown):
                requested = shown[int(answer) - 1]
            else:
                parts = tuple(part.strip() for part in answer.split(",") if part.strip())
                if len(parts) != 2:
                    raise channel.ChannelError(
                        f"refused: a pair is exactly two seat ids, got {answer!r}"
                    )
                requested = (parts[0], parts[1])

    for seat_id in requested:
        if not allowed(seat_id):
            raise channel.ChannelError(
                f"refused: {seat_id!r} is outside this project's allowlist "
                f"({Path(project) / PROFILE_NAME})"
            )
    first = _seatable(registry, requested[0])
    second = _seatable(registry, requested[1])
    from .seats import STALE_AFTER_DAYS, days_between as _days_between

    for seat in (first, second):
        if seat.smoke is not None and seat.smoke.result != "pass":
            raise channel.ChannelError(
                f"refused: seat {seat.seat_id!r} last smoke FAILED at "
                f"{seat.smoke.at}; fix the seat or re-smoke it first"
            )
        state = None
        if seat.smoke is None:
            state = "unsmoked"
        else:
            age = _days_between(seat.smoke.at, now)
            if age is not None and age > STALE_AFTER_DAYS:
                state = f"stale (smoke pass {age:.0f}d old)"
        if state is None:
            continue
        if assume_yes:
            continue  # --yes covers the unsmoked/stale warning, never identity
        answer = ask(
            f"seat {seat.seat_id!r} is {state} (smoke is opt-in; a pass "
            "proves only the seat contract). Seat it anyway? [y/N]: "
        ).strip().lower()
        if answer not in ("y", "yes"):
            raise channel.ChannelError(
                f"refused: {seat.seat_id!r} is {state} and was not confirmed"
            )
    _identity_guard(first, second, allow_identical=allow_identical)
    # --yes accepts the remembered pair; it never answers this question.
    _pair_gate(
        first, second,
        allow_mismatched_pair=allow_mismatched_pair,
        ask=None if assume_yes else ask,
    )
    return requested


def open_debate(
    spec: OpenSpec,
    registry: Registry,
    *,
    load_config_fn: LoadConfigFn,
    now: str,
    tool_version: str,
) -> OpenResult:
    """Validate everything, then write, in order: channel scaffold,
    PROTOCOL.md (only if absent), watcher config, provenance block."""
    from .seats import PROFILE_NAME, load_profile, screen_credentials

    screen_credentials(registry)
    profile = load_profile(project_key(spec.root), registry)
    if profile is not None:
        for seat_id in spec.pair:
            if seat_id not in profile.allowlist:
                raise channel.ChannelError(
                    f"refused: {seat_id!r} is outside this project's allowlist "
                    f"({Path(project_key(spec.root)) / PROFILE_NAME})"
                )
    first = _seatable(registry, spec.pair[0])
    second = _seatable(registry, spec.pair[1])
    _identity_guard(first, second, allow_identical=spec.allow_identical_seats)
    for seat in (first, second):
        if "{prompt}" not in " ".join(seat.commands[0]):
            raise channel.ChannelError(
                f"refused: seat {seat.seat_id!r} has nowhere to put the question text, "
                "so this form of open can never wake it. Open a fully managed debate "
                "with --brokered instead."
            )

    if first.vendor != second.vendor:
        parties = (slugify_seat_id(first.vendor), slugify_seat_id(second.vendor))
    else:
        parties = (slugify_seat_id(first.seat_id), slugify_seat_id(second.seat_id))
    if parties[0] == parties[1]:
        raise channel.ChannelError(
            f"refused: both seats slugify to the party name {parties[0]!r}; "
            "rename one seat so the channel can tell them apart"
        )

    name = channel.generate_channel_id(spec.root, label=spec.label)
    project = project_key(spec.root)
    config_path, state_path = derive_paths(spec.root, name, Path(project))
    validate(
        SetupSpec(
            channel_root=spec.root,
            channel_name=name,
            parties=parties,
            commands={
                parties[0]: list(first.commands[0]),
                parties[1]: list(second.commands[0]),
            },
            config_path=config_path,
            state_path=state_path,
            thread_cap=spec.thread_cap,
            supervisor=spec.supervisor,
        )
    )

    config = {
        "state_path": str(state_path),
        "commands": {
            parties[0]: list(first.commands[0]),
            parties[1]: list(second.commands[0]),
        },
        "prompts": {party: build_prompt(party) for party in parties},
        "debounce_seconds": {party: 0 for party in parties},
        "retry_seconds": 1800,
        "timeout_seconds": 1800,
    }
    in_memory = channel.ChannelConfig(
        parties=parties,
        supervisor=spec.supervisor,
        thread_cap=spec.thread_cap,
        name=name,
        project=project,
        managed_version=channel.MANAGED_VERSION,
    )
    # The probe lives OUTSIDE every target path (setup.apply's own pattern),
    # and the in-memory record feeds the seam: a refusal here leaves the
    # target root byte-empty.
    with tempfile.TemporaryDirectory(prefix="debate-open-") as scratch:
        probe = Path(scratch) / config_path.name
        probe.write_text(json.dumps(config, indent=2), encoding="utf-8")
        loaded = load_config_fn(spec.root, probe, name, channel_config=in_memory)
    problem = loaded.managed_problem()
    if problem is not None:
        raise channel.ChannelError(
            f"refused: this pair would be INVALID to the watcher -- {problem}"
        )

    channel.init_channel(
        spec.root, parties, spec.supervisor, spec.thread_cap,
        name=name, managed_version=channel.MANAGED_VERSION,
    )
    scaffold_protocol(spec.root, spec.thread_cap)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    record_path = spec.root / f"{name}.debate.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["seats"] = {
        "picked_at": now,
        "tool_version": tool_version,
        parties[0]: {
            "seat": first.seat_id,
            "effort": first.effort,
            "command": list(first.commands[0]),
            "smoke_at": first.smoke.at if first.smoke is not None else None,
            "smoke_result": first.smoke.result if first.smoke is not None else None,
        },
        parties[1]: {
            "seat": second.seat_id,
            "effort": second.effort,
            "command": list(second.commands[0]),
            "smoke_at": second.smoke.at if second.smoke is not None else None,
            "smoke_result": second.smoke.result if second.smoke is not None else None,
        },
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    registry.last_pair[project] = [first.seat_id, second.seat_id]
    registry.last_pair[""] = [first.seat_id, second.seat_id]

    hints = [
        f"opened {name} at {spec.root} (parties {parties[0]!r}/{parties[1]!r}, "
        f"supervisor {spec.supervisor!r})",
        f"open the first thread: debate post --root {spec.root} --channel {name} "
        f"--from {spec.supervisor} --type review-request --thread <slug> ...",
        f"drive it: debate watch --root {spec.root} --channel {name} "
        f"--config {config_path} --until-close",
        f"scheduler unit name (convention, not installed): debate-watch-{name}",
    ]
    return OpenResult(channel_name=name, config_path=config_path, hints=hints)


# What a wrapped seat may inherit from the operator's own environment: where
# to find programs, how to format text, which certificates to trust, and which
# proxy to go through. Nothing here carries the operator's tool configuration.
_INHERITED_ENVIRONMENT = [
    "PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
]


def _brokered_adapter(
    seat: Seat, *, tool_version: str, author_vendor: str, real_home: Path
) -> dict[str, object]:
    """Registry seat -> adapter profile mapping (v0.8 minimum). Only honest
    fields: cost mode is the seat's DECLARED value (unknown when undeclared,
    never guessed), the author relationship is DERIVED from the declared
    author vendor (a seat sharing the interactive author's vendor is
    author-affiliated), and the authentication/permission strings describe
    the controller's invocation contract, not per-seat claims.

    Two seat shapes reach this point. A hand-authored adapter, which already
    speaks the controller's file protocol, is recorded verbatim. An ordinary
    seat that only takes a question text is wrapped in Debate's own runner --
    but ONLY when its verified isolation and no-history settings are both on
    record, because that wrapper is the one thing standing between a review
    pass and the operator's live settings, plugins and session history.
    """
    argv = " ".join(seat.commands[0])
    relationship = (
        "author-affiliated"
        if seat.vendor.strip().lower() == author_vendor
        else "author-independent"
    )
    if "{input_path}" in argv and "{result_path}" in argv:
        return {
            "command": list(seat.commands[0]),
            "provider": seat.vendor,
            "requested_model": seat.submodel,
            "author_relationship": relationship,
            "reasoning_effort": seat.effort or "default",
            "cli_version": f"registry seat (debate {tool_version}); bridge-reported at runtime",
            "cost_mode": seat.cost_mode,
            "authentication_mode": (
                "seat bridge is self-authenticating; the controller handles no credentials"
            ),
            "permission_policy": (
                "controller-bound invocation from a pinned read-only source export"
            ),
            "settings_sources": [],
            "environment_allowlist": ["PATH", "LANG", "LC_ALL"],
            "timeout_seconds": 1200,
            "retry_limit": 1,
            "session_persistence": False,
            "isolation_mode": "advisory",
        }
    problem = admission_problem(seat, real_home=real_home)
    if problem is not None:
        raise channel.ChannelError(problem)
    command = [
        sys.executable, "-m", "debate", "bridge",
        "--seat-id", seat.seat_id,
        "--vendor", seat.vendor,
        "--submodel", seat.submodel,
        "--argv-json", json.dumps(seat.commands[0]),
        "--isolation-argv-json", json.dumps(seat.isolation_argv),
        "--no-persistence-argv-json", json.dumps(seat.no_persistence_argv),
        "--isolation-flags-basis",
        "catalogued" if seat.source in ("catalog", "derived") else "declared",
        *(["--config-home", seat.config_home] if seat.config_home else []),
        "{input_path}", "{result_path}",
    ]
    return {
        "command": command,
        "provider": seat.vendor,
        "requested_model": seat.submodel,
        "author_relationship": relationship,
        "reasoning_effort": seat.effort or "default",
        "cli_version": (
            f"registry seat (debate {tool_version}); model identity declared by the registry"
        ),
        "cost_mode": seat.cost_mode,
        "authentication_mode": (
            "the tool authenticates itself through its own configuration folder; "
            "Debate handles no credentials"
        ),
        "permission_policy": (
            "controller-bound invocation from a pinned read-only source export; the "
            "tool's own settings, plugins and session saving are turned off"
        ),
        "settings_sources": [],
        # The sandbox drops every name it was not handed, so the two pointers
        # the wrapper needs -- where Debate itself is installed, and where the
        # operator's home directory is -- travel with the profile.
        "environment": {
            "PYTHONPATH": str(Path(__file__).resolve().parent.parent),
            "DEBATE_BRIDGE_REAL_HOME": str(real_home),
        },
        "environment_allowlist": list(_INHERITED_ENVIRONMENT),
        "timeout_seconds": 1200,
        "retry_limit": 1,
        "session_persistence": False,
        "isolation_mode": "advisory",
    }


def _recorded_isolation(profile: dict[str, object]) -> tuple[str, str]:
    """What the debate record says about one seat's run, read back off the
    command that was actually recorded: where its isolation settings came
    from, and whose tool configuration folder it opens."""
    from . import bridge

    command = profile.get("command")
    spec = (
        bridge.parse_bridge_command([str(part) for part in command])
        if isinstance(command, list)
        else None
    )
    if spec is None:
        return "adapter-owned", "sandbox"
    if spec.config_home is None:
        return spec.isolation_flags_basis, "sandbox"
    return spec.isolation_flags_basis, f"operator ({spec.config_home.partition('=')[0]})"


def open_debate_brokered(
    spec: BrokeredOpenSpec,
    registry: Registry,
    *,
    load_config_fn: LoadConfigFn,
    now: str,
    tool_version: str,
    real_home: Path | None = None,
) -> OpenResult:
    """The v0.8 product open: managed version 2, never 1. Validates the pair,
    the adapter mapping, and the full brokered watcher-config contract
    (loader + adapter-doctor) BEFORE the first byte lands in any target path;
    a refusal leaves every target byte-empty. Requires project approval: the
    product path never runs on a missing profile."""
    from .controller import doctor_lines
    from .seats import PROFILE_NAME, load_profile, screen_credentials

    home = Path.home() if real_home is None else real_home
    screen_credentials(registry)
    project = project_key(spec.root)
    profile = load_profile(project, registry)
    if profile is None:
        raise channel.ChannelError(
            "refused: this project has no approved seats "
            f"(no {Path(project) / PROFILE_NAME}); the product path starts only "
            "after onboarding approval -- run the setup flow first"
        )
    if len(spec.pair) != 2:
        raise channel.ChannelError("refused: a debate seats exactly two")
    for seat_id in spec.pair:
        if seat_id not in profile.allowlist:
            raise channel.ChannelError(
                f"refused: {seat_id!r} is outside this project's allowlist "
                f"({Path(project) / PROFILE_NAME})"
            )
    first = _seatable(registry, spec.pair[0])
    second = _seatable(registry, spec.pair[1])
    _identity_guard(first, second, allow_identical=spec.allow_identical_seats)

    if first.vendor != second.vendor:
        parties = (slugify_seat_id(first.vendor), slugify_seat_id(second.vendor))
    else:
        parties = (slugify_seat_id(first.seat_id), slugify_seat_id(second.seat_id))
    if parties[0] == parties[1]:
        raise channel.ChannelError(
            f"refused: both seats slugify to the party name {parties[0]!r}; "
            "rename one seat so the channel can tell them apart"
        )
    if spec.supervisor in parties:
        raise channel.ChannelError(
            f"refused: the supervisor {spec.supervisor!r} collides with a party "
            "name; the human supervisor never holds a seat"
        )
    if not spec.source_ref.strip():
        raise channel.ChannelError(
            "refused: a fully managed debate needs the commit its seats will review"
        )
    author_vendor = spec.author_vendor.strip().lower()
    if not author_vendor:
        raise channel.ChannelError(
            "refused: a fully managed debate needs --author-vendor (the interactive "
            "author's vendor), so the recorded author relationship is declared, "
            "never guessed"
        )
    # A typo must refuse, never silently degrade to the PERMISSIVE
    # author-independent reading: the declaration is only meaningful against
    # the vendors this open can actually see.
    from .seat_catalog import CATALOG

    known_vendors = {entry.vendor for entry in CATALOG}
    known_vendors.update(seat.vendor.strip().lower() for seat in registry.seats.values())
    if author_vendor not in known_vendors:
        raise channel.ChannelError(
            f"refused: --author-vendor {spec.author_vendor!r} matches no catalog or "
            f"registry vendor; known vendors: {', '.join(sorted(known_vendors))}"
        )

    name = channel.generate_channel_id(spec.root, label=spec.label)
    project_path = Path(project)
    config_path, _v1_state_path = derive_paths(spec.root, name, project_path)
    runtime_root = (
        spec.runtime_root
        if spec.runtime_root is not None
        else project_path / "var" / "debate" / name
    )
    # Brokered state lives BELOW the runtime root (watcher invariant), never
    # in the v1 ~/.local/state location.
    state_path = runtime_root / f"{name}.state.json"

    adapters = {
        parties[0]: _brokered_adapter(
            first, tool_version=tool_version, author_vendor=author_vendor, real_home=home
        ),
        parties[1]: _brokered_adapter(
            second, tool_version=tool_version, author_vendor=author_vendor, real_home=home
        ),
    }
    # Last gate, after admission: nothing on this path can ask a question, so
    # an uneven pair refuses unless the caller already answered for it.
    _pair_gate(
        first, second,
        allow_mismatched_pair=spec.allow_mismatched_pair,
        ask=None,
    )
    first_isolation, first_home = _recorded_isolation(adapters[parties[0]])
    second_isolation, second_home = _recorded_isolation(adapters[parties[1]])
    config: dict[str, object] = {
        "state_path": str(state_path),
        "runtime_root": str(runtime_root),
        "source_ref": spec.source_ref,
        "whole_case_timeout_seconds": 3600,
        # Interactive default: the user is WATCHING this debate. The 60s
        # cron-style tick made a six-message case idle for whole minutes
        # between phases (field finding, 2026-08-20); unattended channels can
        # raise this in their config, the product default stays snappy.
        "scheduler_interval_seconds": 5,
        # How much review material still counts as a small review here.
        "quick_review_max_bytes": spec.quick_review_max_bytes,
        "retry_seconds": 30,
        "adapters": adapters,
        "docket_files": list(spec.docket_files),
        "contamination_canaries": {},
    }
    project_resolved = project_path.resolve()
    for docket_file in spec.docket_files:
        raw = Path(docket_file)
        # `project_path / absolute` REPLACES the base (pathlib semantics), and
        # `..` walks out of it -- both would pass a naive existence check here
        # and only explode in the controller AFTER the channel is written
        # (branch-gate round-3 finding). Refuse pre-write instead.
        if raw.is_absolute():
            raise channel.ChannelError(
                f"refused: docket file {docket_file!r} must be project-relative, "
                "not absolute"
            )
        candidate = (project_path / raw).resolve()
        if not candidate.is_relative_to(project_resolved):
            raise channel.ChannelError(
                f"refused: docket file {docket_file!r} escapes the project root"
            )
        if not candidate.is_file():
            raise channel.ChannelError(
                f"refused: docket file {docket_file!r} does not exist under the project"
            )
    in_memory = channel.ChannelConfig(
        parties=parties,
        supervisor=spec.supervisor,
        thread_cap=spec.thread_cap,
        name=name,
        project=project,
        managed_version=channel.BROKERED_MANAGED_VERSION,
    )
    with tempfile.TemporaryDirectory(prefix="debate-open-") as scratch:
        probe = Path(scratch) / config_path.name
        probe.write_text(json.dumps(config, indent=2), encoding="utf-8")
        loaded = load_config_fn(spec.root, probe, name, channel_config=in_memory)
    problem = loaded.managed_problem()
    if problem is not None:
        raise channel.ChannelError(
            f"refused: this pair would be INVALID to the controller -- {problem}"
        )
    broker = getattr(loaded, "broker", None)
    if broker is not None:
        doctor_lines(broker)  # the adapter-doctor contract, before any write

    channel.init_channel(
        spec.root, parties, spec.supervisor, spec.thread_cap,
        name=name, managed_version=channel.BROKERED_MANAGED_VERSION,
    )
    scaffold_protocol(spec.root, spec.thread_cap)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    record_path = spec.root / f"{name}.debate.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["seats"] = {
        "picked_at": now,
        "tool_version": tool_version,
        parties[0]: {
            "seat": first.seat_id,
            "effort": first.effort,
            "command": list(first.commands[0]),
            "smoke_at": first.smoke.at if first.smoke is not None else None,
            "smoke_result": first.smoke.result if first.smoke is not None else None,
            "provider": first.vendor,
            "requested_model": first.submodel,
            "author_relationship": str(adapters[parties[0]]["author_relationship"]),
            "cost_mode": str(adapters[parties[0]]["cost_mode"]),
            "authentication_mode": str(adapters[parties[0]]["authentication_mode"]),
            "permission_policy": str(adapters[parties[0]]["permission_policy"]),
            "isolation_flags": first_isolation,
            "configuration_home": first_home,
        },
        parties[1]: {
            "seat": second.seat_id,
            "effort": second.effort,
            "command": list(second.commands[0]),
            "smoke_at": second.smoke.at if second.smoke is not None else None,
            "smoke_result": second.smoke.result if second.smoke is not None else None,
            "provider": second.vendor,
            "requested_model": second.submodel,
            "author_relationship": str(adapters[parties[1]]["author_relationship"]),
            "cost_mode": str(adapters[parties[1]]["cost_mode"]),
            "authentication_mode": str(adapters[parties[1]]["authentication_mode"]),
            "permission_policy": str(adapters[parties[1]]["permission_policy"]),
            "isolation_flags": second_isolation,
            "configuration_home": second_home,
        },
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    registry.last_pair[project] = [first.seat_id, second.seat_id]
    registry.last_pair[""] = [first.seat_id, second.seat_id]

    hints = [
        f"opened {name} at {spec.root} (parties {parties[0]!r}/{parties[1]!r}, "
        f"supervisor {spec.supervisor!r}) -- a fully managed debate",
        f"open the docket: debate broker-open --root {spec.root} --channel {name} "
        f"--config {config_path} --thread <case> --first-seat {parties[0]} "
        f"--refs <branch@sha> --body-file <docket-request>",
        f"drive it: debate watch --root {spec.root} --channel {name} "
        f"--config {config_path} --until-close",
    ]
    return OpenResult(channel_name=name, config_path=config_path, hints=hints)
