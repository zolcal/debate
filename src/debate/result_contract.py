"""Versioned verification-result contracts shared by bridge and controller.

Schema v2 is a frozen compatibility surface.  Schema v3 keeps the same shape
but raises its disclosed inline bounds enough for real generated verification
commands while remaining below the controller's one-MiB result ceiling.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


LEGACY_RESULT_SCHEMA_VERSION = 1
EVIDENCE_RESULT_SCHEMA_VERSION = 2
CONTRACT_SAFE_RESULT_SCHEMA_VERSION = 3
SUPPORTED_RESULT_SCHEMA_VERSIONS = (
    LEGACY_RESULT_SCHEMA_VERSION,
    EVIDENCE_RESULT_SCHEMA_VERSION,
    CONTRACT_SAFE_RESULT_SCHEMA_VERSION,
)
VERIFICATION_ITEM_LIMIT = 16


@dataclass(frozen=True)
class VerificationLimits:
    command_scalars: int
    command_bytes: int
    output_scalars: int
    output_bytes: int
    reason_scalars: int
    reason_bytes: int
    object_bytes: int


LIMITS = {
    # Frozen v2 limits.  Do not widen these: old records must keep their exact
    # validation semantics.
    EVIDENCE_RESULT_SCHEMA_VERSION: VerificationLimits(
        command_scalars=1024,
        command_bytes=4096,
        output_scalars=8192,
        output_bytes=32768,
        reason_scalars=1024,
        reason_bytes=4096,
        object_bytes=262144,
    ),
    # The verification object stays below the controller's 1 MiB outer cap,
    # leaving more than 256 KiB for the rest of the result.
    CONTRACT_SAFE_RESULT_SCHEMA_VERSION: VerificationLimits(
        command_scalars=65536,
        command_bytes=262144,
        output_scalars=32768,
        output_bytes=131072,
        reason_scalars=4096,
        reason_bytes=16384,
        object_bytes=786432,
    ),
}


class VerificationContractError(ValueError):
    """The declared evidence does not satisfy its versioned contract."""


def has_verification(schema_version: int) -> bool:
    return schema_version in LIMITS


def limits_for(schema_version: int) -> VerificationLimits:
    try:
        return LIMITS[schema_version]
    except KeyError as error:
        raise VerificationContractError(
            f"result schema v{schema_version} has no verification contract"
        ) from error


def _bounded_text(
    value: object,
    *,
    field_name: str,
    scalar_limit: int,
    byte_limit: int,
    allow_empty: bool = False,
) -> str:
    if not isinstance(value, str) or (not value and not allow_empty):
        raise VerificationContractError(
            f"verification {field_name} must be non-empty text"
        )
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise VerificationContractError(
            f"verification {field_name} contains an isolated surrogate"
        )
    if len(value) > scalar_limit:
        raise VerificationContractError(
            f"verification {field_name} exceeds {scalar_limit} Unicode scalar values"
        )
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise VerificationContractError(
            f"verification {field_name} is not valid UTF-8"
        ) from error
    if len(encoded) > byte_limit:
        raise VerificationContractError(
            f"verification {field_name} exceeds {byte_limit} UTF-8 bytes"
        )
    return value


def validate_verification(
    value: object,
    *,
    decision: str | None,
    schema_version: int,
) -> dict[str, Any]:
    """Validate and normalize seat-declared evidence for v2 or v3."""
    limits = limits_for(schema_version)
    if not isinstance(value, dict):
        raise VerificationContractError("verification must be an object")
    status = value.get("status")
    if status == "performed":
        if set(value) != {"status", "items"}:
            raise VerificationContractError(
                "performed verification must contain exactly status and items"
            )
        items = value.get("items")
        if not isinstance(items, list) or not 1 <= len(items) <= VERIFICATION_ITEM_LIMIT:
            raise VerificationContractError(
                f"performed verification needs 1 to {VERIFICATION_ITEM_LIMIT} items"
            )
        normalized_items: list[dict[str, Any]] = []
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict) or set(item) != {
                "command",
                "exit_status",
                "output",
            }:
                raise VerificationContractError(
                    f"verification item {index} must contain exactly command, "
                    "exit_status and output"
                )
            exit_status = item.get("exit_status")
            if isinstance(exit_status, bool) or not isinstance(exit_status, int):
                raise VerificationContractError(
                    f"verification item {index} exit_status must be an integer"
                )
            normalized_items.append(
                {
                    "command": _bounded_text(
                        item.get("command"),
                        field_name=f"item {index} command",
                        scalar_limit=limits.command_scalars,
                        byte_limit=limits.command_bytes,
                    ),
                    "exit_status": exit_status,
                    # Empty output is honest evidence: a silent-success probe
                    # (an assert chain that prints nothing and exits 0) has
                    # its command and exit status as the evidence. Refusing
                    # the empty string refused the truth and killed a live
                    # case (field finding F21); it would teach seats to pad.
                    "output": _bounded_text(
                        item.get("output"),
                        field_name=f"item {index} output",
                        scalar_limit=limits.output_scalars,
                        byte_limit=limits.output_bytes,
                        allow_empty=True,
                    ),
                }
            )
        normalized: dict[str, Any] = {
            "status": "performed",
            "items": normalized_items,
        }
    elif status == "unable":
        if set(value) != {"status", "reason"}:
            raise VerificationContractError(
                "unable verification must contain exactly status and reason"
            )
        if decision != "NO_PASS":
            raise VerificationContractError(
                "a seat unable to verify must decide NO_PASS"
            )
        normalized = {
            "status": "unable",
            "reason": _bounded_text(
                value.get("reason"),
                field_name="unable reason",
                scalar_limit=limits.reason_scalars,
                byte_limit=limits.reason_bytes,
            ),
        }
    else:
        raise VerificationContractError(
            "verification status must be performed or unable"
        )
    encoded = json.dumps(
        normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    if len(encoded) > limits.object_bytes:
        raise VerificationContractError(
            f"canonical verification JSON exceeds {limits.object_bytes} UTF-8 bytes"
        )
    return normalized


def contract_rule_lines(schema_version: int) -> str:
    """Human-readable limits embedded in the exact prompt contract."""
    limits = limits_for(schema_version)
    return (
        f"Use at most {VERIFICATION_ITEM_LIMIT} verification items. Each command is limited "
        f"to {limits.command_scalars} Unicode scalars / {limits.command_bytes} UTF-8 bytes; "
        f"each output excerpt to {limits.output_scalars} scalars / {limits.output_bytes} bytes; "
        f"an unable reason to {limits.reason_scalars} scalars / {limits.reason_bytes} bytes; "
        f"and the canonical verification object to {limits.object_bytes} bytes."
    )
