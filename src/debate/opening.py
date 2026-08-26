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
import hashlib
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, Sequence, cast

from . import channel
from .seats import Registry, Seat, catalog_declares_isolation
from .setup import SetupSpec, build_prompt, derive_paths, scaffold_protocol, validate

_SLUG_KEEP = re.compile(r"[^a-z0-9-]+")

# How much review material still counts as a small review, in bytes (16 KiB).
# Below it a quick pair is enough; at or above it the strongest pair is worth
# its cost. A per-debate setting: every open may say its own number.
QUICK_REVIEW_MAX_BYTES = 16384
PRODUCT_THREAD_CAP = 12
ORDINARY_THREAD_CAP = PRODUCT_THREAD_CAP
RELEASE_GATE_THREAD_CAP = PRODUCT_THREAD_CAP


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
    thread_cap: int = PRODUCT_THREAD_CAP
    allow_identical_seats: bool = False
    allow_mismatched_pair: bool = False
    docket_files: tuple[str, ...] = ()  # project-relative review inputs for the seats
    # Where the line between a small review and a full one falls for THIS
    # debate, in bytes; recorded for the tools that suggest a pair later.
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES
    # What a seat re-reads in the discussion round: just the two published
    # verdicts (the default) or the whole review material again.
    deliberation_input: str = "verdicts"
    goal: str = ""
    review_domain: str = ""
    stop_rule: str = ""
    review_mode: str = "ordinary"
    # The installed host echoes these values from the immediately preceding
    # read-only preparation. Direct library callers may omit them for
    # compatibility, but the product CLI requires both and the engine always
    # re-prepares the selected pair before the first write.
    preparation_revision: str | None = None
    confirmed_budget: ReviewBudget | None = None


@dataclass(frozen=True)
class ReviewBudget:
    thread_cap: int
    seat_turn_ceiling: int
    nested_launch_ceiling: int
    clean_seat_turns: int = 2
    clean_nested_launches: int = 2

    def as_dict(self) -> dict[str, int]:
        return {
            "thread_cap": self.thread_cap,
            "clean_seat_turns": self.clean_seat_turns,
            "clean_nested_launches": self.clean_nested_launches,
            "seat_turn_ceiling": self.seat_turn_ceiling,
            "nested_launch_ceiling": self.nested_launch_ceiling,
        }


def resolve_review_thread_cap(review_mode: str, requested: int | None) -> int:
    if review_mode not in channel.REVIEW_MODES:
        raise channel.ChannelError(
            f"refused: review mode must be one of {channel.REVIEW_MODES}, got {review_mode!r}"
        )
    if requested not in (None, PRODUCT_THREAD_CAP):
        raise channel.ChannelError(
            f"refused: new product reviews use thread cap {PRODUCT_THREAD_CAP} exactly; "
            f"got {requested}"
        )
    return PRODUCT_THREAD_CAP


def review_budget(thread_cap: int, retry_limits: Sequence[int]) -> ReviewBudget:
    if thread_cap < 2:
        raise channel.ChannelError("refused: review thread cap must be at least 2")
    if len(retry_limits) != 2 or any(limit not in (0, 1) for limit in retry_limits):
        raise channel.ChannelError("refused: a review budget needs two retry limits, each 0 or 1")
    turns = thread_cap - 1
    launches = turns * (max(retry_limits) + 1)
    return ReviewBudget(thread_cap, turns, launches)


def _review_contract(spec: BrokeredOpenSpec) -> dict[str, str]:
    if spec.review_mode not in channel.REVIEW_MODES:
        raise channel.ChannelError(
            f"refused: review mode must be one of {channel.REVIEW_MODES}, got {spec.review_mode!r}"
        )
    fields = {
        "goal": spec.goal.strip(),
        "review_domain": spec.review_domain.strip(),
        "stop_rule": spec.stop_rule.strip(),
    }
    missing = [name for name, value in fields.items() if not value]
    if missing:
        raise channel.ChannelError(
            "refused: a new product debate needs a non-empty review contract; "
            f"missing {', '.join(missing)}"
        )
    return {**fields, "review_mode": spec.review_mode, "review_contract_basis": "recorded"}


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
PREVIOUS_PROJECT_PAIR_REASON = "previous-project-pair"


def _fallback_pair_reason(wanted: str, actual: str) -> str:
    return f"no symmetric {wanted} pair is available; using a symmetric {actual} pair"


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


def _debate_ignore_hint(project: Path) -> str | None:
    """Suggest one hidden runtime ignore; never edit the repository."""
    import subprocess

    probe = subprocess.run(
        ["git", "-C", str(project), "check-ignore", "-q", ".debate/"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if probe.returncode == 0:
        return None
    return "ignore suggestion: add .debate/ to the project's .gitignore"


def _wanted_class(docket_bytes: int, quick_review_max_bytes: int) -> str:
    return "light" if docket_bytes < quick_review_max_bytes else "frontier"


# The two admission refusals, kept as named constants so the plain-words scan
# reads them: a refusal a predicate RETURNS looks like any other assignment to
# a scanner that only watches what is raised or printed (fix round 2).
NO_QUESTION_MARKER_REFUSAL = (
    "cannot take part in a fully managed debate: its command has nowhere to put the "
    "question, and it does not take the two files a managed pass hands over either. "
    "Record a command that takes the question text (debate seats add), or one that "
    "reads a request file and writes an answer file"
)

NO_ISOLATION_SETTINGS_REFUSAL = (
    "can't yet run in the isolated mode a managed debate needs: tell me how it turns "
    "off its settings, plugins and session saving and I'll record that (debate seats "
    "add ... --isolation-argv ... --no-persistence-argv ...), or use a custom seat "
    "command"
)

# The same gap, for a seat Debate itself put in the registry AND whose tool the
# packaged catalog has verified settings for. Asking the operator to declare
# what the catalog already knows is misleading advice: the entry is simply
# older than the catalog, so the fix is a refresh.
STALE_CATALOGUED_SEAT_REFUSAL = (
    "can't yet run in the isolated mode a managed debate needs: this seat comes from "
    "a tool Debate knows; run: debate seats discover to refresh it, then try again"
)

# And the third case: Debate catalogues this tool but has verified NO isolation
# settings for it, so a refresh would change nothing. The registry refuses to
# take a command for a catalog seat id, which makes a custom seat under a NEW
# id the only path that actually works.
NO_CATALOGUED_ISOLATION_REFUSAL = (
    "can't yet run in the isolated mode a managed debate needs: Debate has no verified "
    "isolation settings for this tool yet; register a custom seat with this command "
    "under a new seat id and declare how it turns off its settings, plugins and session "
    "saving (debate seats add <vendor>/<name> --command ... --isolation-argv ... "
    "--no-persistence-argv ...), or use a custom seat command"
)

NO_VERIFICATION_CAPABILITY_REFUSAL = (
    "can't yet run a trustworthy product review: no catalogued or operator-declared "
    "verification capability is recorded; re-discover a catalog seat or register a "
    "manual seat with --verification-capable and any documented --verification-argv"
)

NO_V2_WRAPPER_REFUSAL = (
    "speaks the file adapter protocol but is not declared for result schema v2; "
    "register the wrapper with --verification-capable --result-schema-version 2 "
    "and make its result include the mandatory verification object"
)


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
        if seat.verification_basis not in ("catalogued", "declared"):
            return f"refused: seat {seat.seat_id!r} {NO_VERIFICATION_CAPABILITY_REFUSAL}"
        if seat.result_schema_version != 2:
            return f"refused: seat {seat.seat_id!r} {NO_V2_WRAPPER_REFUSAL}"
        return None
    if "{prompt}" not in argv:
        return f"refused: seat {seat.seat_id!r} {NO_QUESTION_MARKER_REFUSAL}"
    # Admission, and the only admission: no verified isolation and no-history
    # settings, no managed run. There is no flag that waives this.
    if not seat.isolation_argv or not seat.no_persistence_argv:
        if seat.source in ("catalog", "derived"):
            if catalog_declares_isolation(seat.vendor):
                return f"refused: {seat.seat_id} {STALE_CATALOGUED_SEAT_REFUSAL}"
            return f"refused: {seat.seat_id} {NO_CATALOGUED_ISOLATION_REFUSAL}"
        return f"refused: {seat.seat_id} {NO_ISOLATION_SETTINGS_REFUSAL}"
    if seat.config_home:
        from .seats import validate_config_home

        try:
            validate_config_home(seat.config_home, home=real_home)
        except channel.ChannelError as error:
            return str(error)
    from .seats import validate_credential_env

    try:
        validate_credential_env(seat.credential_env)
    except channel.ChannelError as error:
        return str(error)
    missing_credentials = [name for name in seat.credential_env if not os.environ.get(name)]
    if missing_credentials:
        return (
            f"refused: seat {seat.seat_id!r} needs credential environment "
            f"{', '.join(missing_credentials)} in the launching process"
        )
    if seat.verification_basis not in ("catalogued", "declared"):
        return f"refused: seat {seat.seat_id!r} {NO_VERIFICATION_CAPABILITY_REFUSAL}"
    return None


def _is_typed_number(answer: str) -> bool:
    """Whether an answer at the pair prompt is somebody typing a menu number.

    A leading sign counts: "-1" is a number a person typed, and reading it as
    half of a pair of seat ids would explain the wrong mistake.
    """
    body = answer[1:] if answer[:1] in ("+", "-") else answer
    return bool(body) and body.isdigit()


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
    registry: Registry,
    allowlist: tuple[str, ...] | None,
    real_home: Path,
    require_admissible: bool,
) -> list[Seat]:
    """Every seat this project may put in a suggestion, in seat-id order.

    The admission rule exists because Debate's own runner needs the seat's
    settings; the older open never uses that runner, so it asks for presence
    and approval only (`require_admissible=False`).
    """
    from .seats import head_resolves

    return [
        seat
        for seat_id, seat in sorted(registry.seats.items())
        if seat.present
        and (allowlist is None or seat_id in allowlist)
        and head_resolves(seat.commands[0][0])
        and (not require_admissible or admission_problem(seat, real_home=real_home) is None)
    ]


def remembered_pair(
    registry: Registry,
    *,
    project: str,
    allowlist: tuple[str, ...] | None,
    real_home: Path | None = None,
    require_admissible: bool = True,
    include_global: bool = True,
) -> tuple[str, str] | None:
    """The pair this project used last time, if it can still be seated.

    A remembered pair outside the project's approved list, or one naming a
    seat that has since vanished, is DROPPED rather than offered. Where the
    pair will run under Debate's control, one naming a seat that can no longer
    do that is dropped too. Never having said how strong its seats are does
    NOT drop it: it is the user's own last choice, offered as exactly that.
    """
    home = _home(real_home)
    candidates = [registry.last_pair.get(project)]
    if include_global:
        candidates.append(registry.last_pair.get(""))
    for default in candidates:
        if not default or len(default) != 2:
            continue
        if allowlist is not None and not all(seat_id in allowlist for seat_id in default):
            continue
        try:
            first = _seatable(registry, default[0])
            second = _seatable(registry, default[1])
        except channel.ChannelError:
            continue
        if not _pairable(first, second):
            continue
        if require_admissible and any(
            admission_problem(seat, real_home=home) is not None for seat in (first, second)
        ):
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
    require_admissible: bool = True,
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
    offerable = _offerable_seats(
        registry, allowlist, _home(real_home), require_admissible
    )

    def symmetric_pair(capability_class: str) -> tuple[str, str] | None:
        matched = [
            seat for seat in offerable if seat.capability_class == capability_class
        ]
        same_vendor: tuple[str, str] | None = None
        for index, first in enumerate(matched):
            for second in matched[index + 1:]:
                if not _pairable(first, second):
                    continue
                if first.vendor != second.vendor:
                    return first.seat_id, second.seat_id
                if same_vendor is None:
                    same_vendor = (first.seat_id, second.seat_id)
        return same_vendor

    preferred = symmetric_pair(wanted)
    if preferred is not None:
        return PairSuggestion(preferred, reason)
    for alternate in sorted(
        {
            seat.capability_class
            for seat in offerable
            if seat.capability_class is not None and seat.capability_class != wanted
        }
    ):
        fallback = symmetric_pair(alternate)
        if fallback is not None:
            return PairSuggestion(fallback, _fallback_pair_reason(wanted, alternate))
    return None if last_pair is None else PairSuggestion(last_pair, REMEMBERED_PAIR_REASON)


def suggest_pair(
    registry: Registry,
    *,
    allowlist: tuple[str, ...] | None,
    docket_bytes: int,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    last_pair: tuple[str, str] | None,
    real_home: Path | None = None,
    require_admissible: bool = True,
) -> tuple[str, str] | None:
    """The suggested pair alone, for callers with no use for the reason."""
    found = suggest_pair_with_reason(
        registry, allowlist=allowlist, docket_bytes=docket_bytes,
        quick_review_max_bytes=quick_review_max_bytes, last_pair=last_pair,
        real_home=real_home, require_admissible=require_admissible,
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
    require_admissible: bool = True,
) -> list[tuple[str, str]]:
    """The suggestion first, then every other pair this project could seat.

    The rest are ordered by how well they fit the size of this review: the
    matched pairs of the right strength first, then the other evenly matched
    ones, then the uneven ones.
    """
    wanted = _wanted_class(docket_bytes, quick_review_max_bytes)
    offerable = _offerable_seats(
        registry, allowlist, _home(real_home), require_admissible
    )
    ranked: list[tuple[int, str, str]] = []
    for index, first in enumerate(offerable):
        for second in offerable[index + 1:]:
            if not _pairable(first, second):
                continue
            if suggestion is not None and {first.seat_id, second.seat_id} == set(suggestion):
                continue
            kind = classify_pair(first, second)
            if kind == "symmetric" and first.capability_class == wanted:
                rank = 0
            elif kind == "symmetric":
                rank = 1
            else:
                rank = 2
            ranked.append((rank, first.seat_id, second.seat_id))
    choices = [(first, second) for _rank, first, second in sorted(ranked)]
    return choices if suggestion is None else [suggestion, *choices]


def pair_menu(
    registry: Registry,
    *,
    allowlist: tuple[str, ...] | None,
    suggestion: PairSuggestion | None,
    docket_bytes: int,
    quick_review_max_bytes: int = QUICK_REVIEW_MAX_BYTES,
    real_home: Path | None = None,
    require_admissible: bool = True,
    limit: int = PAIR_MENU_LIMIT,
) -> list[str]:
    """The choices as a numbered list, the first one carrying its reason."""
    choices = pair_choices(
        registry, allowlist=allowlist,
        suggestion=None if suggestion is None else suggestion.pair,
        docket_bytes=docket_bytes, quick_review_max_bytes=quick_review_max_bytes,
        real_home=real_home, require_admissible=require_admissible,
    )
    if not choices:
        return []
    first_line = f"1  {choices[0][0]} + {choices[0][1]}"
    if suggestion is not None:
        first_line += f"  --  {suggestion.reason}"
    lines = [first_line]
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
    require_admissible: bool,
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
                require_admissible=require_admissible,
            ),
            real_home=real_home, require_admissible=require_admissible,
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
                real_home=real_home, require_admissible=require_admissible,
            )[:PAIR_MENU_LIMIT]
            for line in pair_menu(
                registry, allowlist=allowlist, suggestion=suggestion,
                docket_bytes=docket_bytes, quick_review_max_bytes=quick_review_max_bytes,
                real_home=real_home, require_admissible=require_admissible,
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
            elif _is_typed_number(answer):
                # A number outside the list is a mistyped MENU answer; telling
                # the operator a pair is two seat ids answers a question they
                # did not ask (final review wave, M2).
                raise channel.ChannelError(
                    f"refused: pick a number between 1 and {len(shown)}, or two "
                    f"seat ids (a,b); got {answer!r}"
                )
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
    # Plan 3.6's order: selection, identity, admission, then the uneven-pair
    # gate. Admission is the one nothing waives, so a pair that is both
    # inadmissible and uneven must hear about admission (final wave, M3).
    if require_admissible:
        for seat in (first, second):
            problem = admission_problem(seat, real_home=_home(real_home))
            if problem is not None:
                raise channel.ChannelError(problem)
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
    # Keep validation scratch project-local and inside the final path's
    # filesystem and permission boundary.
    with tempfile.TemporaryDirectory(prefix=".debate-open-", dir=Path(project)) as scratch:
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
    seat: Seat,
    *,
    tool_version: str,
    author_vendor: str,
    real_home: Path,
    deliberation_input: str = "verdicts",
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
    problem = admission_problem(seat, real_home=real_home)
    if problem is not None:
        raise channel.ChannelError(problem)
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
                "seat-declared credential names are inherited only at launch; their raw values "
                "are visible to the seat process and tools but are not serialized"
                if seat.credential_env
                else "seat bridge is self-authenticating; the controller handles no credentials"
            ),
            "permission_policy": (
                "controller-bound invocation from a pinned read-only source export"
            ),
            "settings_sources": [],
            **({"credential_env": list(seat.credential_env)} if seat.credential_env else {}),
            "environment_allowlist": ["PATH", "LANG", "LC_ALL", *seat.credential_env],
            "timeout_seconds": 1200,
            "retry_limit": 1,
            "session_persistence": False,
            "isolation_mode": "advisory",
            "result_schema_version": seat.result_schema_version,
        }
    from .bridge import SUBCOMMAND

    command = [
        sys.executable, "-m", "debate", SUBCOMMAND,
        "--seat-id", seat.seat_id,
        "--vendor", seat.vendor,
        "--submodel", seat.submodel,
        "--argv-json", json.dumps(seat.commands[0]),
        "--isolation-argv-json", json.dumps(seat.isolation_argv),
        "--no-persistence-argv-json", json.dumps(seat.no_persistence_argv),
        "--verification-argv-json", json.dumps(seat.verification_argv),
        "--verification-basis", str(seat.verification_basis),
        "--result-schema-version", "2",
        *(
            ["--credential-env-json", json.dumps(seat.credential_env)]
            if seat.credential_env
            else []
        ),
        "--deliberation-input", deliberation_input,
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
            "the declared credential is inherited by name only at launch; its raw value is "
            "visible to the seat process and tools but is not serialized"
            if seat.credential_env
            else "the tool authenticates itself through its own configuration folder; "
            "Debate handles no credentials"
        ),
        "permission_policy": (
            "controller-bound invocation from a pinned read-only source export; the "
            "tool's own settings, plugins and session saving are turned off"
        ),
        "settings_sources": [],
        **({"credential_env": list(seat.credential_env)} if seat.credential_env else {}),
        # The sandbox drops every name it was not handed, so the two pointers
        # the wrapper needs -- where Debate itself is installed, and where the
        # operator's home directory is -- travel with the profile.
        "environment": {
            "PYTHONPATH": str(Path(__file__).resolve().parent.parent),
            "DEBATE_BRIDGE_REAL_HOME": str(real_home),
        },
        "environment_allowlist": [*_INHERITED_ENVIRONMENT, *seat.credential_env],
        "timeout_seconds": 1200,
        "retry_limit": 1,
        "session_persistence": False,
        "isolation_mode": "advisory",
        "result_schema_version": 2,
    }


def _validate_author_vendor(registry: Registry, author_vendor: str) -> str:
    normalized = author_vendor.strip().lower()
    if not normalized:
        raise channel.ChannelError(
            "refused: a fully managed debate needs --author-vendor (the interactive "
            "author's vendor), so the recorded author relationship is declared, "
            "never guessed"
        )
    from .seat_catalog import CATALOG

    known_vendors = {entry.vendor for entry in CATALOG}
    known_vendors.update(seat.vendor.strip().lower() for seat in registry.seats.values())
    if normalized not in known_vendors:
        raise channel.ChannelError(
            f"refused: --author-vendor {author_vendor!r} matches no catalog or "
            f"registry vendor; known vendors: {', '.join(sorted(known_vendors))}"
        )
    return normalized


def _accepted_product_allowlist(
    registry: Registry,
    *,
    project: str,
) -> tuple[str, ...]:
    """Current-project seats whose profile and current policy revision agree."""
    from .seats import PROFILE_NAME, load_profile

    profile = load_profile(project, registry)
    if profile is None:
        raise channel.ChannelError(
            "refused: this project has no approved seats "
            f"(no {Path(project) / PROFILE_NAME}); the product path starts only "
            "after onboarding approval -- run the setup flow first"
        )
    accepted: list[str] = []
    for seat_id in profile.allowlist:
        selected = registry.seats[seat_id]
        revision = selected.data_policy_revision
        if revision is not None and profile.data_policy_acceptances.get(seat_id) != revision:
            continue
        accepted.append(seat_id)
    return tuple(accepted)


def _preparation_reason(suggestion: PairSuggestion | None) -> tuple[str | None, str | None]:
    if suggestion is None:
        return None, None
    if suggestion.reason == REMEMBERED_PAIR_REASON:
        return PREVIOUS_PROJECT_PAIR_REASON, suggestion.reason
    if suggestion.reason == QUICK_PAIR_REASON:
        return "docket-size-light", suggestion.reason
    if suggestion.reason == FULL_PAIR_REASON:
        return "docket-size-frontier", suggestion.reason
    return "capability-fallback", suggestion.reason


def _pair_warning_metadata(first: Seat, second: Seat) -> list[dict[str, object]]:
    kind = classify_pair(first, second)
    if kind == "mismatched":
        return [{
            "code": "mismatched-capability",
            "message": _uneven_pair_sentence(first, second),
            "requires_confirmation": True,
            "open_flag": "--allow-mismatched-pair",
        }]
    if kind == "undeclared":
        return [{
            "code": "undeclared-capability",
            "message": "one of these seats has no declared capability class; pairing may be uneven",
            "requires_confirmation": False,
        }]
    return []


def prepare_brokered_open(
    *,
    root: Path,
    registry: Registry,
    review_mode: str,
    requested_cap: int | None,
    docket_files: Sequence[str],
    quick_review_max_bytes: int,
    author_vendor: str,
    tool_version: str,
    real_home: Path | None = None,
    deliberation_input: str = "verdicts",
) -> dict[str, object]:
    """Build the product's authoritative, read-only start menu.

    The object is safe to discard on cancel. It performs admission and adapter
    construction in memory so every choice carries the retry budget the engine
    would actually record, but it creates no channel/runtime state and invokes
    no seat.
    """
    from .seats import screen_credentials

    thread_cap = resolve_review_thread_cap(review_mode, requested_cap)
    screen_credentials(registry)
    project = project_key(root)
    allowlist = _accepted_product_allowlist(registry, project=project)
    from .seats import load_profile

    profile = load_profile(project, registry)
    assert profile is not None  # _accepted_product_allowlist already refused otherwise
    state_rows: list[dict[str, object]] = []
    for seat_id in profile.allowlist:
        seat = registry.seats[seat_id]
        state_rows.append({
            "seat_id": seat_id,
            "vendor": seat.vendor,
            "submodel": seat.submodel,
            "effort": seat.effort,
            "commands": seat.commands,
            "present": seat.present,
            "capability_class": seat.capability_class,
            "isolation_argv": seat.isolation_argv,
            "no_persistence_argv": seat.no_persistence_argv,
            "config_home": seat.config_home,
            "verification_argv": seat.verification_argv,
            "verification_basis": seat.verification_basis,
            "result_schema_version": seat.result_schema_version,
            "credential_env": seat.credential_env,
            "data_policy_revision": seat.data_policy_revision,
            "accepted_policy_revision": profile.data_policy_acceptances.get(seat_id),
        })
    state_canonical = json.dumps(
        {"profile_allowlist": profile.allowlist, "seats": state_rows},
        sort_keys=True,
        separators=(",", ":"),
    )
    state_revision = hashlib.sha256(state_canonical.encode("utf-8")).hexdigest()
    home = Path.home() if real_home is None else real_home
    normalized_author = _validate_author_vendor(registry, author_vendor)
    review_bytes = docket_byte_size(project, docket_files)
    previous = remembered_pair(
        registry,
        project=project,
        allowlist=allowlist,
        real_home=home,
        require_admissible=True,
        include_global=False,
    )
    suggestion: PairSuggestion | None
    if previous is not None:
        suggestion = PairSuggestion(previous, REMEMBERED_PAIR_REASON)
    else:
        suggestion = suggest_pair_with_reason(
            registry,
            allowlist=allowlist,
            docket_bytes=review_bytes,
            quick_review_max_bytes=quick_review_max_bytes,
            last_pair=None,
            real_home=home,
            require_admissible=True,
        )
    pairs = pair_choices(
        registry,
        allowlist=allowlist,
        suggestion=None if suggestion is None else suggestion.pair,
        docket_bytes=review_bytes,
        quick_review_max_bytes=quick_review_max_bytes,
        real_home=home,
        require_admissible=True,
    )
    reason, reason_text = _preparation_reason(suggestion)
    choices: list[dict[str, object]] = []
    for number, pair in enumerate(pairs, start=1):
        first, second = (registry.seats[pair[0]], registry.seats[pair[1]])
        adapters = (
            _brokered_adapter(
                first,
                tool_version=tool_version,
                author_vendor=normalized_author,
                real_home=home,
                deliberation_input=deliberation_input,
            ),
            _brokered_adapter(
                second,
                tool_version=tool_version,
                author_vendor=normalized_author,
                real_home=home,
                deliberation_input=deliberation_input,
            ),
        )
        budget = review_budget(
            thread_cap,
            [cast(int, adapter["retry_limit"]) for adapter in adapters],
        )
        is_lead = number == 1 and suggestion is not None
        choices.append({
            "number": number,
            "pair": [pair[0], pair[1]],
            "default": previous is not None and pair == previous,
            "reason": reason if is_lead else None,
            "reason_text": reason_text if is_lead else None,
            "warnings": _pair_warning_metadata(first, second),
            "budget": budget.as_dict(),
        })
    default_budget = choices[0]["budget"] if previous is not None and choices else None
    payload: dict[str, object] = {
        "schema_version": 1,
        "project": project,
        "review_mode": review_mode,
        "thread_cap": thread_cap,
        "docket_bytes": review_bytes,
        "state_revision": state_revision,
        "choices": choices,
        "default_pair": None if previous is None else [previous[0], previous[1]],
        "default_reason": PREVIOUS_PROJECT_PAIR_REASON if previous is not None else None,
        "budget": default_budget,
        "budget_scope": "default-pair" if default_budget is not None else "per-choice",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["preparation_revision"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def brokered_preparation_lines(preparation: dict[str, object]) -> list[str]:
    """Human-readable rendering derived only from the structured result."""
    lines = [
        f"project: {preparation['project']}",
        f"review mode: {preparation['review_mode']}; thread cap: {preparation['thread_cap']}",
    ]
    default_pair = preparation.get("default_pair")
    if isinstance(default_pair, list) and len(default_pair) == 2:
        lines.append(
            f"Enter keeps {default_pair[0]} + {default_pair[1]}; "
            "choose a number to change; cancel stops."
        )
    else:
        lines.append("Pick one numbered pair; cancel stops.")
    choices = preparation.get("choices")
    if not isinstance(choices, list) or not choices:
        lines.append("No approved, currently seatable pair is available.")
    else:
        for choice in choices:
            if not isinstance(choice, dict):
                continue
            pair = choice["pair"]
            budget = choice["budget"]
            if not isinstance(pair, list) or not isinstance(budget, dict):
                continue
            marker = " [default]" if choice.get("default") else ""
            reason_text = choice.get("reason_text")
            reason_suffix = f" -- {reason_text}" if reason_text else ""
            lines.append(
                f"{choice['number']}  {pair[0]} + {pair[1]}{marker}{reason_suffix}; "
                f"clean {budget['clean_nested_launches']} launches; maximum "
                f"{budget['seat_turn_ceiling']} seat turns / "
                f"{budget['nested_launch_ceiling']} retry-inclusive launches"
            )
            warnings = choice.get("warnings")
            if isinstance(warnings, list):
                for warning in warnings:
                    if isinstance(warning, dict):
                        lines.append(f"   warning: {warning.get('message', '')}")
    lines.append(f"preparation revision: {preparation['preparation_revision']}")
    return lines


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
    contract = _review_contract(spec)
    expected_cap = resolve_review_thread_cap(spec.review_mode, spec.thread_cap)
    if spec.thread_cap != expected_cap:
        raise channel.ChannelError(
            f"refused: {spec.review_mode} review resolved to thread cap {expected_cap}, "
            f"got {spec.thread_cap}"
        )
    if len(spec.pair) != 2:
        raise channel.ChannelError("refused: a debate seats exactly two")
    current_preparation = prepare_brokered_open(
        root=spec.root,
        registry=registry,
        review_mode=spec.review_mode,
        requested_cap=spec.thread_cap,
        docket_files=spec.docket_files,
        quick_review_max_bytes=spec.quick_review_max_bytes,
        author_vendor=spec.author_vendor,
        tool_version=tool_version,
        real_home=home,
        deliberation_input=spec.deliberation_input,
    )
    if (
        spec.preparation_revision is not None
        and spec.preparation_revision != current_preparation["preparation_revision"]
    ):
        raise channel.ChannelError(
            "refused: the approved profile, seat state, menu, or budget changed after "
            "confirmation; prepare a fresh menu"
        )
    selected_choice = next(
        (
            choice
            for choice in cast(list[dict[str, object]], current_preparation["choices"])
            if set(cast(list[str], choice["pair"])) == set(spec.pair)
        ),
        None,
    )
    if selected_choice is None:
        from .seats import PROFILE_NAME, load_profile

        current_profile = load_profile(project_key(spec.root), registry)
        if current_profile is None:
            raise channel.ChannelError(
                "refused: this project has no approved seats "
                f"(no {Path(project_key(spec.root)) / PROFILE_NAME})"
            )
        for seat_id in spec.pair:
            if seat_id not in current_profile.allowlist:
                raise channel.ChannelError(
                    f"refused: {seat_id!r} is outside this project's allowlist"
                )
        first_selected = _seatable(registry, spec.pair[0])
        second_selected = _seatable(registry, spec.pair[1])
        for selected in (first_selected, second_selected):
            if (
                selected.data_policy_revision is not None
                and current_profile.data_policy_acceptances.get(selected.seat_id)
                != selected.data_policy_revision
            ):
                raise channel.ChannelError(
                    f"refused: seat {selected.seat_id!r} needs project acceptance of "
                    f"data policy {selected.data_policy_revision!r}; re-run onboarding "
                    "inspect and approve"
                )
        _identity_guard(
            first_selected,
            second_selected,
            allow_identical=spec.allow_identical_seats,
        )
        for selected in (first_selected, second_selected):
            problem = admission_problem(selected, real_home=home)
            if problem is not None:
                raise channel.ChannelError(problem)
        raise channel.ChannelError(
            "refused: the selected pair is not in the current prepared menu; "
            "prepare a fresh menu"
        )
    if (
        spec.confirmed_budget is not None
        and spec.confirmed_budget.as_dict() != selected_choice["budget"]
    ):
        raise channel.ChannelError(
            "refused: the confirmed review budget does not match the engine's current "
            "selected-pair budget; prepare and confirm again"
        )
    screen_credentials(registry)
    project = project_key(spec.root)
    profile = load_profile(project, registry)
    if profile is None:
        raise channel.ChannelError(
            "refused: this project has no approved seats "
            f"(no {Path(project) / PROFILE_NAME}); the product path starts only "
            "after onboarding approval -- run the setup flow first"
        )
    for seat_id in spec.pair:
        if seat_id not in profile.allowlist:
            raise channel.ChannelError(
                f"refused: {seat_id!r} is outside this project's allowlist "
                f"({Path(project) / PROFILE_NAME})"
            )
    first = _seatable(registry, spec.pair[0])
    second = _seatable(registry, spec.pair[1])
    for selected in (first, second):
        if selected.data_policy_revision is None:
            continue
        accepted_revision = profile.data_policy_acceptances.get(selected.seat_id)
        if accepted_revision != selected.data_policy_revision:
            raise channel.ChannelError(
                f"refused: seat {selected.seat_id!r} needs project acceptance of data policy "
                f"{selected.data_policy_revision!r}; re-run onboarding inspect and approve"
            )
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
    author_vendor = _validate_author_vendor(registry, spec.author_vendor)

    name = channel.generate_channel_id(spec.root, label=spec.label)
    project_path = Path(project)
    config_path = project_path / ".debate" / "channels" / name / "watcher.json"
    if spec.runtime_root is not None:
        raise channel.ChannelError(
            "refused: a new product debate owns its hidden .debate/runtime/<channel> "
            "path; runtime_root overrides are only supported when loading historical configs"
        )
    runtime_root = project_path / ".debate" / "runtime" / name
    # Brokered state lives BELOW the runtime root (watcher invariant), never
    # in the v1 ~/.local/state location.
    state_path = runtime_root / "watcher-state.json"

    from .bridge import DELIBERATION_INPUTS

    if spec.deliberation_input not in DELIBERATION_INPUTS:
        raise channel.ChannelError(
            f"refused: {spec.deliberation_input!r} is not something a seat can re-read in "
            f"the discussion round; choose one of: {', '.join(DELIBERATION_INPUTS)}"
        )
    adapters = {
        parties[0]: _brokered_adapter(
            first,
            tool_version=tool_version,
            author_vendor=author_vendor,
            real_home=home,
            deliberation_input=spec.deliberation_input,
        ),
        parties[1]: _brokered_adapter(
            second,
            tool_version=tool_version,
            author_vendor=author_vendor,
            real_home=home,
            deliberation_input=spec.deliberation_input,
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
        **contract,
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
        review_mode=spec.review_mode,
        review_contract_basis="recorded",
        goal=contract["goal"],
        review_domain=contract["review_domain"],
        stop_rule=contract["stop_rule"],
    )
    with tempfile.TemporaryDirectory(prefix=".debate-open-", dir=project_path) as scratch:
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
        review_mode=spec.review_mode,
        review_contract_basis="recorded",
        goal=contract["goal"],
        review_domain=contract["review_domain"],
        stop_rule=contract["stop_rule"],
    )
    scaffold_protocol(spec.root, spec.thread_cap)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    record_path = spec.root / f"{name}.debate.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    budget = review_budget(
        spec.thread_cap,
        [cast(int, adapters[party]["retry_limit"]) for party in parties],
    )
    record["review_contract"] = {
        **contract,
        "thread_cap": budget.thread_cap,
        "seat_turn_ceiling": budget.seat_turn_ceiling,
        "nested_launch_ceiling": budget.nested_launch_ceiling,
        "supervisor_entries_consume_cap": True,
    }
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
            "verification_capability": first.verification_basis,
            "result_schema_version": cast(
                int, adapters[parties[0]]["result_schema_version"]
            ),
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
            "verification_capability": second.verification_basis,
            "result_schema_version": cast(
                int, adapters[parties[1]]["result_schema_version"]
            ),
        },
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    registry.last_pair[project] = [first.seat_id, second.seat_id]

    hints = [
        f"opened {name} at {spec.root} (parties {parties[0]!r}/{parties[1]!r}, "
        f"supervisor {spec.supervisor!r}) -- a fully managed debate",
        f"open the docket: debate broker-open --root {spec.root} --channel {name} "
        f"--config {config_path} --thread <case> --first-seat {parties[0]} "
        f"--refs <branch@sha> --body-file <docket-request>",
        f"drive it: debate watch --root {spec.root} --channel {name} "
        f"--config {config_path} --until-close",
        f"review budget: at most {budget.seat_turn_ceiling} seat turns and "
        f"{budget.nested_launch_ceiling} nested-seat launches; supervisor entries "
        "consume the same thread cap",
    ]
    ignore_hint = _debate_ignore_hint(project_path)
    if ignore_hint is not None:
        hints.append(ignore_hint)
    return OpenResult(channel_name=name, config_path=config_path, hints=hints)
