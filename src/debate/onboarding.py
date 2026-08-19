"""Installation-driven onboarding: the product-path state machine (v0.8).

The session-start hook and the onboarding skill speak to the engine through
this module's JSON-first surface. One deliberate difference from the 0.7
direct CLI: the PRODUCT path treats a missing project profile as NOT
APPROVED (``profile_state: "missing"`` -> ``attention: "offer_setup"``),
while the legacy direct CLI keeps treating a missing profile as unrestricted
for 0.7 compatibility. Detection is evidence, not approval.

``status`` is read-only by construction: it never writes a registry or
profile, never runs discovery, never invokes a seat, and never raises on
broken state -- broken is a STATE it reports, because the session-start hook
must render it as a short repair notice, not crash the host session.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import channel, seats

SCHEMA_VERSION = 1

ATTENTION_READY = "ready"
ATTENTION_OFFER_SETUP = "offer_setup"
ATTENTION_OFFER_REFRESH = "offer_refresh"
ATTENTION_REPAIR = "repair_required"


def _require_absolute(project: str) -> Path:
    path = Path(project)
    if not path.is_absolute():
        raise channel.ChannelError(
            f"refused: --project must be an absolute path, got {project!r}"
        )
    return path


def _smoke_word(seat: seats.Seat) -> str:
    if seat.smoke is None:
        return "never"
    return seat.smoke.result


def status(project: str) -> dict[str, object]:
    """Read-only onboarding state for one project root (absolute path)."""
    from . import __version__

    project_path = _require_absolute(project)
    reasons: list[str] = []
    registry_state = "missing"
    profile_state = "missing"
    approved: list[dict[str, object]] = []

    registry: seats.Registry | None = None
    if not seats.registry_path().exists():
        reasons.append("no seat registry on this machine yet")
    else:
        try:
            registry = seats.load_registry()
        except channel.ChannelError as error:
            registry_state = "broken"
            reasons.append(str(error))
        else:
            if registry.tool_version == __version__:
                registry_state = "current"
            else:
                registry_state = "stale"
                reasons.append(
                    f"registry was written by debate {registry.tool_version or 'unknown'}; "
                    f"this engine is {__version__} (rescan required)"
                )

    profile_file = project_path / seats.PROFILE_NAME
    if registry_state == "broken":
        if profile_file.exists():
            profile_state = "broken"
            reasons.append(
                "project profile cannot be validated against a broken registry"
            )
    else:
        try:
            profile = seats.load_profile(str(project_path), registry or seats.Registry())
        except channel.ChannelError as error:
            profile_state = "broken"
            reasons.append(str(error))
        else:
            if profile is not None:
                profile_state = "approved"
                from datetime import datetime, timezone

                now = datetime.now(timezone.utc).isoformat(timespec="seconds")
                seen_commands: dict[str, str] = {}
                for seat_id in profile.allowlist:
                    seat = (registry or seats.Registry()).seats[seat_id]
                    present = seat.present and seats.head_resolves(seat.commands[0][0])
                    if not present:
                        reasons.append(
                            f"approved seat {seat_id} is not currently runnable "
                            f"(binary missing: {seat.commands[0][0]})"
                        )
                    smoke_word = _smoke_word(seat)
                    if seat.smoke is not None and seat.smoke.result == "fail":
                        reasons.append(
                            f"approved seat {seat_id} failed its last smoke at {seat.smoke.at}"
                        )
                    elif seat.smoke is not None and seat.smoke.result == "pass":
                        age = seats._days_between(seat.smoke.at, now)
                        if age is not None and age > seats.STALE_AFTER_DAYS:
                            smoke_word = "stale"
                            reasons.append(
                                f"approved seat {seat_id} smoke pass is {age:.0f}d old "
                                "(refresh is opt-in)"
                            )
                    argv_key = "\x00".join(seat.commands[0])
                    if argv_key in seen_commands:
                        reasons.append(
                            f"approved seats {seen_commands[argv_key]} and {seat_id} run the "
                            "IDENTICAL selected command; the open-time identity guard will "
                            "refuse this pair"
                        )
                    else:
                        seen_commands[argv_key] = seat_id
                    approved.append(
                        {
                            "seat_id": seat_id,
                            "present": present,
                            "smoke": smoke_word,
                        }
                    )

    if registry_state == "broken" or profile_state == "broken":
        attention = ATTENTION_REPAIR
    elif profile_state == "missing":
        attention = ATTENTION_OFFER_SETUP
    elif any(not entry["present"] for entry in approved):
        attention = ATTENTION_REPAIR
    elif registry_state == "stale" or any(
        entry["smoke"] in ("fail", "stale") for entry in approved
    ):
        attention = ATTENTION_OFFER_REFRESH
    else:
        attention = ATTENTION_READY

    return {
        "schema_version": SCHEMA_VERSION,
        "product_version": __version__,
        "project_root": str(project_path),
        "registry_state": registry_state,
        "profile_state": profile_state,
        "approved_seats": approved,
        "reasons": reasons,
        "attention": attention,
    }


def _candidates(registry: seats.Registry, existing_ids: set[str]) -> list[dict[str, object]]:
    """Sanitized candidate rows, deterministically ordered. `existing_ids`
    labels what came from a pre-existing registry: existing state is
    candidate INPUT, visibly labelled, never silent approval."""
    rows: list[dict[str, object]] = []
    for seat_id, seat in sorted(registry.seats.items()):
        rows.append(
            {
                "seat_id": seat_id,
                "vendor": seat.vendor,
                "submodel": seat.submodel,
                "effort": seat.effort,
                "command": list(seat.commands[0]),
                "source": seat.source,
                "present": seat.present and seats.head_resolves(seat.commands[0][0]),
                "smoke": _smoke_word(seat),
                "existing": seat_id in existing_ids,
            }
        )
    return rows


def _candidate_revision(rows: list[dict[str, object]]) -> str:
    import hashlib

    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _scan(now: str) -> tuple[seats.Registry, set[str], str]:
    """In-memory catalog x PATH discovery merged over the existing registry.
    Returns (merged registry, pre-existing seat ids, existing-state word).
    WRITES NOTHING: seats.discover mutates only the in-memory object."""
    from . import __version__

    existing_state = "missing"
    registry = seats.Registry()
    if seats.registry_path().exists():
        try:
            registry = seats.load_registry()
        except channel.ChannelError:
            existing_state = "broken"
            registry = seats.Registry()
        else:
            existing_state = "current" if registry.tool_version == __version__ else "stale"
    existing_ids = set(registry.seats)
    registry, _diff = seats.discover(registry, now=now)
    seats.screen_credentials(registry)
    return registry, existing_ids, existing_state


def inspect(project: str, *, now: str) -> dict[str, object]:
    """Catalog/PATH discovery in memory: no model call, no write. Returns
    sanitized candidates plus a deterministic candidate_revision that
    `approve` must echo back (acting on a changed candidate set is refused)."""
    project_path = _require_absolute(project)
    registry, existing_ids, existing_state = _scan(now)
    rows = _candidates(registry, existing_ids)
    return {
        "schema_version": SCHEMA_VERSION,
        "project_root": str(project_path),
        "existing_registry_state": existing_state,
        "candidates": rows,
        "candidate_revision": _candidate_revision(rows),
    }


def approve(
    project: str,
    *,
    allow: list[str],
    candidate_revision: str,
    confirmed: bool,
    now: str,
) -> dict[str, object]:
    """Rescan, verify the candidate revision, validate the selected ids, then
    TRANSACTIONALLY write the machine registry and the project profile: every
    failure before the atomic replaces leaves both prior files byte-identical.
    `confirmed` may be passed only after a user answer in the current turn --
    that obligation is the calling skill's, stated in its instructions."""
    import os
    import tempfile

    project_path = _require_absolute(project)
    if not confirmed:
        raise channel.ChannelError(
            "refused: approve requires --confirmed, and the onboarding skill may "
            "pass it only after the user answered in the current turn"
        )
    if not allow:
        raise channel.ChannelError(
            "refused: zero selected seats; onboarding stays incomplete rather than "
            "writing a misleading empty profile"
        )
    duplicates = sorted({seat_id for seat_id in allow if allow.count(seat_id) > 1})
    if duplicates:
        raise channel.ChannelError(
            f"refused: duplicate --allow ids: {', '.join(duplicates)}"
        )
    registry, existing_ids, _existing_state = _scan(now)
    rows = _candidates(registry, existing_ids)
    revision = _candidate_revision(rows)
    if revision != candidate_revision:
        raise channel.ChannelError(
            "refused: the candidate set changed since inspection "
            f"(expected {candidate_revision[:12]}..., found {revision[:12]}...); "
            "re-run inspect and re-confirm with the user"
        )
    present_by_id = {str(row["seat_id"]): bool(row["present"]) for row in rows}
    for seat_id in allow:
        if seat_id not in registry.seats:
            raise channel.ChannelError(
                f"refused: {seat_id!r} is not a detected candidate"
            )
        if not present_by_id[seat_id]:
            raise channel.ChannelError(
                f"refused: {seat_id!r} is not currently runnable; approving it "
                "would record a seat that cannot debate"
            )

    registry_target = seats.registry_path()
    profile_target = project_path / seats.PROFILE_NAME
    registry_target.parent.mkdir(parents=True, exist_ok=True)
    registry_text = json.dumps(seats.registry_payload(registry), indent=2) + "\n"
    profile_text = (
        json.dumps({"profile_version": 1, "allowlist": list(allow)}, indent=2) + "\n"
    )
    # Both temp files are fully written and fsynced BEFORE the first replace,
    # so every preparation failure leaves both prior files byte-identical.
    temps: list[str] = []
    try:
        registry_fd, registry_tmp = tempfile.mkstemp(
            prefix=".debate-registry-", dir=str(registry_target.parent)
        )
        temps.append(registry_tmp)
        with os.fdopen(registry_fd, "w", encoding="utf-8") as handle:
            handle.write(registry_text)
            handle.flush()
            os.fsync(handle.fileno())
        profile_fd, profile_tmp = tempfile.mkstemp(
            prefix=".debate-profile-", dir=str(project_path)
        )
        temps.append(profile_tmp)
        with os.fdopen(profile_fd, "w", encoding="utf-8") as handle:
            handle.write(profile_text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(registry_tmp, registry_target)
        temps.remove(registry_tmp)
        os.replace(profile_tmp, profile_target)
        temps.remove(profile_tmp)
    except OSError as error:
        for leftover in temps:
            try:
                os.unlink(leftover)
            except OSError:
                pass
        raise channel.ChannelError(f"refused: approval write failed: {error}") from error
    return status(str(project_path))


def status_lines(report: dict[str, object]) -> list[str]:
    """Human rendering of a status report; pure ASCII (Windows-safe rule)."""
    lines = [
        f"project: {report['project_root']}",
        f"registry: {report['registry_state']}  profile: {report['profile_state']}"
        f"  attention: {report['attention']}",
    ]
    approved = report["approved_seats"]
    if isinstance(approved, list):
        for entry in approved:
            if isinstance(entry, dict):
                lines.append(
                    f"  seat {entry['seat_id']}: "
                    f"{'present' if entry['present'] else 'MISSING'}, smoke {entry['smoke']}"
                )
    reasons = report["reasons"]
    if isinstance(reasons, list):
        for reason in reasons:
            lines.append(f"  note: {reason}")
    return lines
