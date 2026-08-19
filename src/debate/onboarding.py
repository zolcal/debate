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
                for seat_id in profile.allowlist:
                    seat = (registry or seats.Registry()).seats[seat_id]
                    present = seat.present and seats.head_resolves(seat.commands[0][0])
                    if not present:
                        reasons.append(
                            f"approved seat {seat_id} is not currently runnable "
                            f"(binary missing: {seat.commands[0][0]})"
                        )
                    if seat.smoke is not None and seat.smoke.result == "fail":
                        reasons.append(
                            f"approved seat {seat_id} failed its last smoke at {seat.smoke.at}"
                        )
                    approved.append(
                        {
                            "seat_id": seat_id,
                            "present": present,
                            "smoke": _smoke_word(seat),
                        }
                    )

    if registry_state == "broken" or profile_state == "broken":
        attention = ATTENTION_REPAIR
    elif profile_state == "missing":
        attention = ATTENTION_OFFER_SETUP
    elif any(not entry["present"] for entry in approved):
        attention = ATTENTION_REPAIR
    elif registry_state == "stale" or any(entry["smoke"] == "fail" for entry in approved):
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
