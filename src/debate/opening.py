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
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

from . import channel
from .seats import Registry, Seat
from .setup import build_prompt, derive_paths, scaffold_protocol

_SLUG_KEEP = re.compile(r"[^a-z0-9-]+")


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


@dataclass
class OpenResult:
    channel_name: str
    config_path: Path
    hints: list[str]


def project_key(root: Path) -> str:
    """The `last_pair` key: the git toplevel, never the --root folder (H4)."""
    return channel._derived_project(root)


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
    head = seat.commands[0][0]
    if Path(head).is_absolute():
        resolvable = Path(head).exists()
    else:
        resolvable = shutil.which(head) is not None
    if not resolvable:
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


def pick_pair(
    registry: Registry,
    *,
    project: str,
    requested: tuple[str, str] | None,
    assume_yes: bool,
    ask: Callable[[str], str],
    allow_identical: bool = False,
) -> tuple[str, str]:
    """The owner picks; the previous pick is the one-Enter default. When the
    project carries a `debate-profile.json`, the picker is RESTRICTED to its
    allowlist (section 2.10's second layer, ruling 5)."""
    from .seats import PROFILE_NAME, load_profile

    profile = load_profile(project, registry)

    def allowed(seat_id: str) -> bool:
        return profile is None or seat_id in profile.allowlist

    if requested is None:
        usable = None
        for default in (registry.last_pair.get(project), registry.last_pair.get("")):
            if not default or len(default) != 2 or not all(allowed(sid) for sid in default):
                continue  # a default outside the allowlist is DROPPED
            try:
                _seatable(registry, default[0])
                _seatable(registry, default[1])
                usable = (default[0], default[1])
                break
            except channel.ChannelError:
                continue  # a default containing an unseatable seat is DROPPED
        if assume_yes:
            if usable is None:
                raise channel.ChannelError(
                    "refused: --yes needs a usable default pair and none exists; "
                    "pass --pair a,b"
                )
            requested = usable
        else:
            listing = ", ".join(
                sid for sid, seat in sorted(registry.seats.items())
                if seat.present and allowed(sid)
            )
            prompt = f"seatable: {listing}\npick two seats (a,b)"
            prompt += f" [default: {usable[0]},{usable[1]}]: " if usable else ": "
            answer = ask(prompt).strip()
            if not answer:
                if usable is None:
                    raise channel.ChannelError("refused: no default pair to accept")
                requested = usable
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
    for seat in (first, second):
        if seat.smoke is None or seat.smoke.result != "pass":
            state = "unsmoked" if seat.smoke is None else "smoke-failed"
            if assume_yes and seat.smoke is None:
                continue  # --yes covers the unsmoked warning, never identity
            if seat.smoke is not None and seat.smoke.result != "pass":
                raise channel.ChannelError(
                    f"refused: seat {seat.seat_id!r} last smoke FAILED at "
                    f"{seat.smoke.at}; fix the seat or re-smoke it first"
                )
            answer = ask(
                f"seat {seat.seat_id!r} is {state} (smoke is opt-in; a pass "
                "proves only the seat contract). Seat it anyway? [y/N]: "
            ).strip().lower()
            if answer not in ("y", "yes"):
                raise channel.ChannelError(
                    f"refused: {seat.seat_id!r} is unsmoked and was not confirmed"
                )
    _identity_guard(first, second, allow_identical=allow_identical)
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
    from .seats import screen_credentials

    screen_credentials(registry)
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

    name = channel.generate_channel_id(spec.root, label=spec.label)
    project = project_key(spec.root)
    config_path, state_path = derive_paths(spec.root, name, Path(project))

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
        },
        parties[1]: {
            "seat": second.seat_id,
            "effort": second.effort,
            "command": list(second.commands[0]),
            "smoke_at": second.smoke.at if second.smoke is not None else None,
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
