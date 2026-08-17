"""The host seat registry: what this machine can seat, discovered honestly.

One registry per machine (~/.config/debate/seats.json). Discovery merges the
packaged catalog against PATH; it adds and marks, it never deletes -- a
vanished binary is history worth keeping, and manual entries belong to the
operator alone. Seat identity is ``vendor/submodel`` with an optional
``@effort``; per owner ruling 4 (plan, 2026-08-15) each seat carries ONE OR
MORE endpoint argvs and v1 selection is always the first-listed.
"""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import channel
from .seat_catalog import CATALOG
from .setup import SECRET_PATTERN

REGISTRY_PATH = Path("~/.config/debate/seats.json")
REGISTRY_VERSION = 1


@dataclass
class SmokeStatus:
    at: str
    result: str  # "pass" | "fail"


@dataclass
class Seat:
    seat_id: str
    vendor: str
    submodel: str
    effort: str | None
    commands: list[list[str]]  # endpoint options; v1 selection = commands[0]
    source: str  # "catalog" | "manual"
    present: bool
    smoke: SmokeStatus | None


@dataclass
class Registry:
    tool_version: str = ""
    discovered_at: str = ""
    seats: dict[str, Seat] = field(default_factory=dict)
    last_pair: dict[str, list[str]] = field(default_factory=dict)  # "" = global


def registry_path() -> Path:
    return Path(os.environ.get("DEBATE_SEATS_REGISTRY", str(REGISTRY_PATH))).expanduser()


def _seat_from_raw(seat_id: str, raw: object) -> Seat:
    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} must be an object, got {type(raw).__name__}"
        )
    commands_raw = raw.get("commands")
    if not isinstance(commands_raw, list) or not commands_raw or not all(
        isinstance(argv, list) and argv and all(isinstance(part, str) for part in argv)
        for argv in commands_raw
    ):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} needs one or more endpoint argvs "
            "(a list of non-empty string lists)"
        )
    smoke_raw = raw.get("smoke")
    smoke = None
    if smoke_raw is not None:
        if not isinstance(smoke_raw, dict) or not smoke_raw.get("at") or not smoke_raw.get("result"):
            raise channel.ChannelError(f"refused: registry seat {seat_id!r} has a malformed smoke record")
        smoke = SmokeStatus(at=str(smoke_raw["at"]), result=str(smoke_raw["result"]))
    present_raw = raw.get("present", True)
    if not isinstance(present_raw, bool):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} 'present' must be true or false, "
            f"got {present_raw!r}"
        )
    effort = raw.get("effort")
    return Seat(
        seat_id=seat_id,
        vendor=str(raw.get("vendor", "")),
        submodel=str(raw.get("submodel", "")),
        effort=str(effort) if effort is not None else None,
        commands=[list(argv) for argv in commands_raw],
        source=str(raw.get("source", "manual")),
        present=present_raw,
        smoke=smoke,
    )


def load_registry() -> Registry:
    path = registry_path()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        return Registry()
    except ValueError as error:
        raise channel.ChannelError(f"refused: unreadable seat registry {path}: {error}") from error
    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: seat registry {path} must be a JSON object, got {type(raw).__name__}"
        )
    seats_raw = raw.get("seats", {})
    if not isinstance(seats_raw, dict):
        raise channel.ChannelError(f"refused: seat registry {path} 'seats' must be an object")
    last_pair_raw = raw.get("last_pair", {})
    if not isinstance(last_pair_raw, dict):
        raise channel.ChannelError(f"refused: seat registry {path} 'last_pair' must be an object")
    registry = Registry(
        tool_version=str(raw.get("tool_version", "")),
        discovered_at=str(raw.get("discovered_at", "")),
    )
    for seat_id, seat_raw in seats_raw.items():
        registry.seats[str(seat_id)] = _seat_from_raw(str(seat_id), seat_raw)
    for project, pair in last_pair_raw.items():
        if not isinstance(pair, list) or not all(isinstance(item, str) for item in pair):
            raise channel.ChannelError(
                f"refused: seat registry {path} last_pair for {project!r} must be a list of seat ids"
            )
        registry.last_pair[str(project)] = list(pair)
    return registry


def screen_credentials(registry: Registry) -> None:
    """Refuse anything key-shaped in any endpoint argv (wizard rule)."""
    for seat in registry.seats.values():
        for argv in seat.commands:
            for part in argv:
                if SECRET_PATTERN.search(part):
                    raise channel.ChannelError(
                        f"refused: seat {seat.seat_id!r} command looks credential-shaped; "
                        "seat credentials belong in a self-sourcing wrapper, never the registry"
                    )


def save_registry(registry: Registry) -> Path:
    """Validate fully -- credential screen included -- then write once."""
    screen_credentials(registry)
    path = registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "registry_version": REGISTRY_VERSION,
        "tool_version": registry.tool_version,
        "discovered_at": registry.discovered_at,
        "seats": {
            seat_id: {
                "vendor": seat.vendor,
                "submodel": seat.submodel,
                "effort": seat.effort,
                "commands": seat.commands,
                "source": seat.source,
                "present": seat.present,
                "smoke": (
                    {"at": seat.smoke.at, "result": seat.smoke.result}
                    if seat.smoke is not None
                    else None
                ),
            }
            for seat_id, seat in sorted(registry.seats.items())
        },
        "last_pair": dict(sorted(registry.last_pair.items())),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _assemble_argv(binary_path: str, invocation: tuple[str, ...], extra: list[str]) -> list[str]:
    argv = [binary_path if part == "{binary}" else part for part in invocation]
    return argv + extra


def discover(
    registry: Registry,
    *,
    which: Callable[[str], str | None] = shutil.which,
    now: str,
) -> tuple[Registry, list[str]]:
    """Catalog x PATH -> merged registry plus human-readable diff lines.

    Seeds one seat per submodel ONLY for entries whose argv can select one
    (the single-seat rule); marks vanished catalog seats absent, deletes
    nothing, and never touches a manual entry.
    """
    from . import __version__

    diff: list[str] = []
    seen_ids: set[str] = set()
    for entry in CATALOG:
        binary_path = next(
            (resolved for name in entry.binaries if (resolved := which(name))), None
        )
        if binary_path is None:
            continue
        for submodel in entry.submodels:
            seat_id = f"{entry.vendor}/{submodel}"
            seen_ids.add(seat_id)
            extra = [
                part.replace("{submodel}", submodel) for part in entry.submodel_argv
            ]
            argv = _assemble_argv(str(binary_path), entry.invocation, extra)
            existing = registry.seats.get(seat_id)
            if existing is None:
                registry.seats[seat_id] = Seat(
                    seat_id=seat_id,
                    vendor=entry.vendor,
                    submodel=submodel,
                    effort=None,
                    commands=[argv],
                    source="catalog",
                    present=True,
                    smoke=None,
                )
                diff.append(f"+ {seat_id} ({argv[0]})")
            elif existing.source == "catalog":
                if not existing.present:
                    diff.append(f"~ {seat_id} present again")
                existing.present = True
                existing.commands = [argv] + existing.commands[1:]
    for seat in registry.seats.values():
        if seat.source == "catalog" and seat.seat_id not in seen_ids and seat.present:
            base = seat.seat_id.split("@", 1)[0]
            if base not in seen_ids:
                seat.present = False
                diff.append(f"- {seat.seat_id} marked absent (binary gone)")
    registry.discovered_at = now
    registry.tool_version = __version__
    return registry, diff


# --- Slice 2: freshness, upgrade trigger, manual seats, smoke ---------------

STALE_AFTER_DAYS = 30


@dataclass
class CheckReport:
    """Exit 3 iff ``fails`` is nonempty -- real breakage only (plan fold H1):
    a binary that no longer resolves, or a smoke that RAN AND FAILED.
    Never-smoked is informational and stale smoke a warning, both exit 0 --
    smoke is opt-in (owner ruling 1), and an exit code that stays red until
    the owner pays for smoke would convert opt-in into a toll."""

    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)


def _days_between(earlier: str, later: str) -> float | None:
    from datetime import datetime

    try:
        delta = datetime.fromisoformat(later) - datetime.fromisoformat(earlier)
    except (ValueError, TypeError):
        return None  # unparseable or naive-vs-aware: no staleness verdict
    return delta.total_seconds() / 86400.0


def check(
    registry: Registry,
    *,
    which: Callable[[str], str | None] = shutil.which,
    now: str,
) -> CheckReport:
    report = CheckReport()
    for seat_id, seat in sorted(registry.seats.items()):
        binary = seat.commands[0][0]
        if Path(binary).is_absolute():
            # A same-named binary elsewhere on PATH must not mask a broken pin.
            resolvable = Path(binary).exists()
        else:
            resolvable = which(binary) is not None
        if not resolvable:
            report.fails.append(f"FAIL {seat_id}: binary missing ({binary})")
            continue
        if seat.smoke is None:
            report.infos.append(
                f"INFO {seat_id}: never smoked (opt-in: debate seats smoke {seat_id})"
            )
            continue
        if seat.smoke.result != "pass":
            report.fails.append(f"FAIL {seat_id}: smoke failed at {seat.smoke.at}")
            continue
        age = _days_between(seat.smoke.at, now)
        if age is not None and age > STALE_AFTER_DAYS:
            report.warns.append(
                f"WARN {seat_id}: smoke stale ({age:.0f}d; refresh via debate seats smoke)"
            )
    return report


def ensure_current(
    registry: Registry,
    *,
    which: Callable[[str], str | None] = shutil.which,
    now: str,
) -> tuple[Registry, list[str]]:
    """The upgrade trigger: a version mismatch re-runs the catalog scan --
    scan only, smoke is never automatic."""
    from . import __version__

    if registry.tool_version == __version__:
        return registry, []
    return discover(registry, which=which, now=now)


def add_seat(
    registry: Registry,
    seat_id: str,
    command_text: str,
    *,
    which: Callable[[str], str | None] = shutil.which,
) -> None:
    """Create a manual seat, or APPEND an endpoint option to an existing
    manual one (another provider account of the SAME serving, section 2.9;
    a different serving is its own seat -- section 2.10). Selection stays
    first-listed (owner ruling 4)."""
    from .setup import split_argv

    if "/" not in seat_id:
        raise channel.ChannelError(
            f"refused: seat id {seat_id!r} must be vendor/submodel"
        )
    argv = split_argv(command_text)
    if not argv or "{prompt}" not in " ".join(argv):
        raise channel.ChannelError(
            "refused: a seat command needs an executable and a {prompt} placeholder"
        )
    head = argv[0]
    if which(head) is None and not Path(head).exists():
        raise channel.ChannelError(f"refused: seat command {head!r} does not resolve")
    for part in argv:
        if SECRET_PATTERN.search(part):
            raise channel.ChannelError(
                "refused: command looks credential-shaped; credentials belong in a "
                "self-sourcing wrapper, never the registry"
            )
    existing = registry.seats.get(seat_id)
    if existing is not None:
        if existing.source != "manual":
            raise channel.ChannelError(
                f"refused: {seat_id!r} is a catalog seat; endpoint options on catalog "
                "seats come from discovery"
            )
        existing.commands.append(argv)
        return
    vendor, _, submodel = seat_id.partition("/")
    base_id, _, effort = seat_id.partition("@")
    registry.seats[seat_id] = Seat(
        seat_id=seat_id,
        vendor=vendor,
        submodel=submodel.split("@", 1)[0],
        effort=effort or None,
        commands=[argv],
        source="manual",
        present=True,
        smoke=None,
    )


def add_effort_seat(registry: Registry, seat_id: str) -> None:
    """Derive vendor/submodel@effort from its base seat: derived argv = the
    base's FIRST-LISTED endpoint option plus the catalog's effort fragment."""
    base_id, sep, effort = seat_id.partition("@")
    if not sep or not effort:
        raise channel.ChannelError(
            f"refused: {seat_id!r} is not a vendor/submodel@effort id"
        )
    if seat_id in registry.seats:
        raise channel.ChannelError(
            f"refused: {seat_id!r} is already in the registry; remove it first "
            "(the registry never clobbers an existing seat)"
        )
    base = registry.seats.get(base_id)
    if base is None:
        raise channel.ChannelError(
            f"refused: base seat {base_id!r} is not in the registry"
        )
    entry = next((e for e in CATALOG if e.vendor == base.vendor), None)
    if entry is None or not entry.effort_argv:
        raise channel.ChannelError(
            f"refused: {base.vendor!r} takes no effort via argv "
            "(a wrapper-internal effort is a different wrapper: use seats add --command)"
        )
    if effort not in entry.known_efforts:
        raise channel.ChannelError(
            f"refused: effort {effort!r} is not in {base.vendor!r} known_efforts "
            f"{list(entry.known_efforts)}"
        )
    derived_argv = list(base.commands[0]) + [
        part.replace("{effort}", effort) for part in entry.effort_argv
    ]
    registry.seats[seat_id] = Seat(
        seat_id=seat_id,
        vendor=base.vendor,
        submodel=base.submodel,
        effort=effort,
        commands=[derived_argv],
        source="manual",
        present=base.present,
        smoke=None,
    )


def remove_seat(registry: Registry, seat_id: str) -> None:
    seat = registry.seats.get(seat_id)
    if seat is None:
        raise channel.ChannelError(f"refused: no seat {seat_id!r} in the registry")
    if seat.source != "manual":
        raise channel.ChannelError(
            f"refused: {seat_id!r} is a catalog seat; discovery marks it absent instead"
        )
    del registry.seats[seat_id]


def smoke_seat(
    registry: Registry,
    seat_id: str,
    *,
    scratch_base: Path | None = None,
    now: str,
    emit: Callable[[str], None] = print,
    assume_yes: bool = False,
    ask: Callable[[str], str] = input,
) -> str:
    """One scratch-channel round trip for one seat's FIRST-LISTED argv,
    through setup's own smoke machinery. The cost is announced and CONFIRMED
    before the spend (auto-yes under --yes, ruling 1); the result is recorded
    in the registry either way; returns "pass" or "fail"."""
    from .setup import SetupSpec
    from . import setup as setup_module

    seat = registry.seats.get(seat_id)
    if seat is None:
        raise channel.ChannelError(f"refused: no seat {seat_id!r} in the registry")
    if not assume_yes:
        answer = ask(
            f"smoke {seat_id}: this spends ONE model call "
            f"({seat.commands[0][0]} ...). Proceed? [y/N]: "
        ).strip().lower()
        if answer not in ("y", "yes"):
            raise channel.ChannelError(
                f"refused: smoke of {seat_id!r} not confirmed (pass --yes to auto-confirm)"
            )
    if scratch_base is not None:
        scratch_base.mkdir(parents=True, exist_ok=True)
    party = seat.vendor if seat.vendor != "probe" else "seatprobe"
    spec = SetupSpec(
        channel_root=Path("."),
        channel_name=f"smoke-{party}",
        parties=(party, "probe"),
        commands={party: list(seat.commands[0]), "probe": None},
        config_path=Path("unused-config.json"),
        state_path=Path("unused-state.json"),
        thread_cap=12,
        timeout_seconds=300,
    )
    failures = setup_module.smoke(spec, scratch_base=scratch_base, emit=emit)
    result = "fail" if failures else "pass"
    seat.smoke = SmokeStatus(at=now, result=result)
    for line in failures:
        emit(f"smoke {seat_id}: {line}")
    return result


# --- Slice 4: the project profile (section 2.10's second layer, ruling 5) ---

PROFILE_NAME = "debate-profile.json"


@dataclass
class Profile:
    """The per-project allowlist: which subset of the host registry may
    debate in this project. References registry entries by id, never
    redefines them (section 2.10 verbatim); pinned-effort ids ARE the pin
    mechanism. Opt-in per project: no file, no restriction."""

    allowlist: tuple[str, ...]


def vendor_display(vendor: str) -> tuple[str, tuple[str, ...]]:
    """(notes, known_efforts) for `seats list` -- the wrapper-pin drift limit
    is only honest if the display actually names where the pin lives (D1)."""
    entry = next((e for e in CATALOG if e.vendor == vendor), None)
    if entry is None:
        return ("manual seat; the operator owns its pin", ())
    return (entry.notes, entry.known_efforts)


def load_profile(project: str, registry: Registry) -> Profile | None:
    """Fail-closed: a malformed file, an unknown version, an id the registry
    does not carry, or an EMPTY allowlist all refuse with the offender named.
    A missing file is simply no restriction."""
    path = Path(project) / PROFILE_NAME
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise channel.ChannelError(
            f"refused: unreadable project profile {path}: {error}"
        ) from error
    except ValueError as error:
        raise channel.ChannelError(
            f"refused: unreadable project profile {path}: {error}"
        ) from error
    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: project profile {path} must be a JSON object"
        )
    if raw.get("profile_version") != 1:
        raise channel.ChannelError(
            f"refused: project profile {path} has profile_version "
            f"{raw.get('profile_version')!r}; this tool speaks 1"
        )
    allowlist_raw = raw.get("allowlist")
    if not isinstance(allowlist_raw, list) or not all(
        isinstance(item, str) for item in allowlist_raw
    ):
        raise channel.ChannelError(
            f"refused: project profile {path} 'allowlist' must be a list of seat ids"
        )
    if not allowlist_raw:
        raise channel.ChannelError(
            f"refused: project profile {path} has an EMPTY allowlist, which would "
            "ban every seat; delete the file instead"
        )
    for seat_id in allowlist_raw:
        if seat_id not in registry.seats:
            raise channel.ChannelError(
                f"refused: project profile {path} allowlists {seat_id!r}, which is "
                "not in the registry; run: debate seats discover"
            )
    return Profile(allowlist=tuple(allowlist_raw))
