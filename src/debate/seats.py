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
    effort = raw.get("effort")
    return Seat(
        seat_id=seat_id,
        vendor=str(raw.get("vendor", "")),
        submodel=str(raw.get("submodel", "")),
        effort=str(effort) if effort is not None else None,
        commands=[list(argv) for argv in commands_raw],
        source=str(raw.get("source", "manual")),
        present=bool(raw.get("present", True)),
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


def save_registry(registry: Registry) -> Path:
    """Validate fully -- credential screen included -- then write once."""
    for seat in registry.seats.values():
        for argv in seat.commands:
            for part in argv:
                if SECRET_PATTERN.search(part):
                    raise channel.ChannelError(
                        f"refused: seat {seat.seat_id!r} command looks credential-shaped; "
                        "seat credentials belong in a self-sourcing wrapper, never the registry"
                    )
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
