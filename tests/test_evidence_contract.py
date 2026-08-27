"""Result schema v2 is bounded, mandatory, and still only seat-declared."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from debate import bridge
from debate.controller import AdapterError, AdapterProfile, AdapterResult, _parse_result


def _profile(version: int = 2) -> AdapterProfile:
    return AdapterProfile(
        party="seat-a",
        command=(sys.executable, "adapter.py", "{input_path}", "{result_path}"),
        provider="fixture",
        requested_model="fixture-model",
        author_relationship="author-independent",
        reasoning_effort="default",
        cli_version="fixture",
        cost_mode="local",
        authentication_mode="fixture",
        permission_policy="fixture",
        settings_sources=(),
        result_schema_version=version,
    )


def _result(
    *,
    decision: str = "PASS",
    verification: object = None,
    version: int = 2,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": version,
        "entry_type": "verdict",
        "decision": decision,
        "body": "Fresh bounded review.",
        "runtime_model": "fixture-model",
    }
    if version in (2, 3):
        payload["verification"] = (
            {
                "status": "performed",
                "items": [
                    {"command": "python -m pytest -q", "exit_status": 0, "output": "3 passed"}
                ],
            }
            if verification is None
            else verification
        )
    return payload


def _parse(tmp_path: Path, payload: dict[str, object], *, version: int = 2) -> AdapterResult:
    path = tmp_path / "result.json"
    encoded = json.dumps(payload, ensure_ascii=False)
    try:
        encoded.encode("utf-8")
    except UnicodeEncodeError:
        # JSON escapes let the production parser receive an isolated surrogate
        # for its own explicit rejection path.
        encoded = json.dumps(payload)
    path.write_text(encoded, encoding="utf-8")
    return _parse_result(path, "seat-a", _profile(version))


def _seat_answer(payload: dict[str, object]) -> str:
    return "```json\n" + json.dumps(payload, ensure_ascii=False) + "\n```\n"


def _seat_payload(payload: dict[str, object]) -> dict[str, object]:
    answer = dict(payload)
    answer.pop("runtime_model", None)
    return answer


def test_performed_and_unable_are_accepted_and_labelled(tmp_path: Path) -> None:
    performed = _parse(tmp_path, _result())
    assert performed.verification_status == "performed"
    assert performed.verification_evidence_basis == "seat-declared"
    unable = _parse(
        tmp_path,
        _result(
            decision="NO_PASS",
            verification={"status": "unable", "reason": "the interpreter is unavailable"},
        ),
    )
    assert unable.verification_status == "unable"


@pytest.mark.parametrize(
    "verification, match",
    [
        (None, "verification must be an object"),
        ({"status": "performed", "items": [], "extra": 1}, "exactly status and items"),
        ({"status": "performed", "items": []}, "needs 1 to 16"),
        (
            {
                "status": "performed",
                "items": [{"command": "probe", "exit_status": True, "output": "ok"}],
            },
            "exit_status must be an integer",
        ),
        (
            {
                "status": "performed",
                "items": [{"command": "", "exit_status": 0, "output": "ok"}],
            },
            "command must be non-empty",
        ),
        ({"status": "unable", "reason": ""}, "reason must be non-empty"),
    ],
)
def test_controller_rejects_missing_extra_empty_and_bad_types(
    tmp_path: Path, verification: object, match: str
) -> None:
    payload = _result(verification=verification)
    if verification is None:
        payload.pop("verification")
    elif verification == {"status": "unable", "reason": ""}:
        payload["decision"] = "NO_PASS"
    with pytest.raises(AdapterError, match=match):
        _parse(tmp_path, payload)
    with pytest.raises(bridge.Refusal, match=match):
        bridge.parse_answer_with_verification(
            _seat_answer(_seat_payload(payload)), schema_version=2
        )


def test_empty_output_is_honest_evidence(tmp_path: Path) -> None:
    """Field finding F21 (gate-5, 2026-08-27): a silent-success probe -- an
    assert chain that prints nothing and exits 0 -- is legitimate evidence;
    the executed command and its exit status carry it. Refusing the empty
    string refused the truth, ERROR-closed a live case, and would teach
    seats to pad output. The empty COMMAND stays refused (test above)."""
    payload = _result(
        verification={
            "status": "performed",
            "items": [
                {
                    "command": "python3 -c \"import slugify; assert slugify.slugify('') == 'untitled'\"",
                    "exit_status": 0,
                    "output": "",
                }
            ],
        }
    )
    parsed = _parse(tmp_path, payload)
    assert parsed.verification is not None
    items = parsed.verification["items"]
    assert isinstance(items, list)
    assert items[0]["output"] == ""


def test_unable_cannot_pass_in_both_validators(tmp_path: Path) -> None:
    payload = _result(
        verification={"status": "unable", "reason": "cannot run the requested probe"}
    )
    with pytest.raises(AdapterError, match="must decide NO_PASS"):
        _parse(tmp_path, payload)
    with pytest.raises(bridge.Refusal, match="must decide NO_PASS"):
        bridge.parse_answer_with_verification(
            _seat_answer(_seat_payload(payload)), schema_version=2
        )


@pytest.mark.parametrize(
    "field, value, match",
    [
        ("command", "x" * 1025, "1024 Unicode scalar"),
        ("command", "\U0001f642" * 1024 + "x", "1024 Unicode scalar"),
        ("output", "x" * 8193, "8192 Unicode scalar"),
        ("output", "\U0001f642" * 8192 + "x", "8192 Unicode scalar"),
        ("command", "\ud800", "isolated surrogate"),
    ],
    # Short ids on purpose (field finding F25): pytest exports the full test
    # id via PYTEST_CURRENT_TEST, and an 8192-emoji id blows the Windows
    # 32767-character environment limit before the test even runs — and made
    # every log unreadable everywhere.
    ids=["cmd-ascii-over", "cmd-emoji-over", "out-ascii-over", "out-emoji-over", "cmd-surrogate"],
)
def test_scalar_utf8_and_surrogate_limits(
    tmp_path: Path, field: str, value: str, match: str
) -> None:
    item = {"command": "probe", "exit_status": 0, "output": "ok"}
    item[field] = value
    payload = _result(verification={"status": "performed", "items": [item]})
    with pytest.raises(AdapterError, match=match):
        _parse(tmp_path, payload)
    with pytest.raises(bridge.Refusal, match=match):
        bridge.parse_answer_with_verification(
            _seat_answer(_seat_payload(payload)), schema_version=2
        )


def test_exact_text_and_item_boundaries_pass_both_validators(tmp_path: Path) -> None:
    items = [
        {
            "command": "\U0001f642" * 1024,
            "exit_status": 0,
            "output": "ok" if index else "\U0001f642" * 8192,
        }
        for index in range(16)
    ]
    payload = _result(verification={"status": "performed", "items": items})
    assert _parse(tmp_path, payload).verification_status == "performed"
    decision, _body, verification = bridge.parse_answer_with_verification(
        _seat_answer(_seat_payload(payload)), schema_version=2
    )
    assert decision == "PASS"
    assert verification is not None and len(verification["items"]) == 16

    unable = _result(
        decision="NO_PASS",
        verification={"status": "unable", "reason": "\U0001f642" * 1024},
    )
    assert _parse(tmp_path, unable).verification_status == "unable"
    bridge.parse_answer_with_verification(
        _seat_answer(_seat_payload(unable)), schema_version=2
    )


def test_utf8_byte_limit_and_aggregate_limit(tmp_path: Path) -> None:
    # 1024 scalar values but 4097 UTF-8 bytes.
    too_many_bytes = "\U0001f642" * 1024 + "a"
    with pytest.raises(AdapterError, match="Unicode scalar|UTF-8 bytes"):
        _parse(
            tmp_path,
            _result(
                verification={
                    "status": "performed",
                    "items": [
                        {"command": too_many_bytes, "exit_status": 0, "output": "ok"}
                    ],
                }
            ),
        )
    payload = _result(
        verification={
            "status": "performed",
            "items": [{"command": too_many_bytes, "exit_status": 0, "output": "ok"}],
        }
    )
    with pytest.raises(bridge.Refusal, match="Unicode scalar|UTF-8 bytes"):
        bridge.parse_answer_with_verification(
            _seat_answer(_seat_payload(payload)), schema_version=2
        )
    items = [
        {"command": f"probe {index}", "exit_status": 0, "output": "\U0001f642" * 8192}
        for index in range(16)
    ]
    with pytest.raises(AdapterError, match="canonical verification JSON"):
        _parse(tmp_path, _result(verification={"status": "performed", "items": items}))
    aggregate_payload = _result(
        verification={"status": "performed", "items": items}
    )
    with pytest.raises(bridge.Refusal, match="canonical verification JSON"):
        bridge.parse_answer_with_verification(
            _seat_answer(_seat_payload(aggregate_payload)), schema_version=2
        )


def test_item_limit_and_outer_result_limit_are_separate(tmp_path: Path) -> None:
    items = [
        {"command": f"probe {index}", "exit_status": 0, "output": "ok"}
        for index in range(17)
    ]
    with pytest.raises(AdapterError, match="1 to 16"):
        _parse(tmp_path, _result(verification={"status": "performed", "items": items}))
    item_payload = _result(verification={"status": "performed", "items": items})
    with pytest.raises(bridge.Refusal, match="1 to 16"):
        bridge.parse_answer_with_verification(
            _seat_answer(_seat_payload(item_payload)), schema_version=2
        )
    payload = _result()
    payload["body"] = "x" * (1024 * 1024)
    with pytest.raises(AdapterError, match="1 MiB"):
        _parse(tmp_path, payload)


def test_legacy_v1_custom_adapter_remains_evidence_absent(tmp_path: Path) -> None:
    result = _parse(tmp_path, _result(version=1), version=1)
    assert result.decision == "PASS"
    assert result.verification is None
    assert result.verification_status == "absent"
    assert _profile(1).sanitized_manifest()["result_schema_version"] == 1


def test_prompt_never_claims_schema_authenticates_truth() -> None:
    assert "not proof supplied" in bridge.ANSWER_RULES
    assert "by the schema" in bridge.ANSWER_RULES
    assert "verified by the schema" not in bridge.ANSWER_RULES.lower()


def test_v3_accepts_realistic_long_command_while_v2_stays_frozen(tmp_path: Path) -> None:
    command = "python -m pytest " + "tests/test_contract.py::case " * 70
    assert len(command) > 1024
    verification = {
        "status": "performed",
        "items": [{"command": command, "exit_status": 0, "output": "1 passed"}],
    }
    with pytest.raises(AdapterError, match="exceeds 1024 Unicode scalar values"):
        _parse(tmp_path, _result(verification=verification), version=2)

    result = _parse(
        tmp_path,
        _result(verification=verification, version=3),
        version=3,
    )
    assert result.verification == verification
    decision, _body, seat_verification = bridge.parse_answer_with_verification(
        _seat_answer(_seat_payload(_result(verification=verification, version=3))),
        schema_version=3,
    )
    assert decision == "PASS"
    assert seat_verification == verification


def test_v3_prompt_discloses_the_enforced_command_limit() -> None:
    assert "65536 Unicode scalars / 262144 UTF-8 bytes" in bridge.CONTRACT_SAFE_ANSWER_RULES
    assert '"schema_version": 3' in bridge.CONTRACT_SAFE_ANSWER_RULES
