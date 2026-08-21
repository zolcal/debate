"""Operator-facing output must be pure ASCII.

CI (windows-latest) hit `UnicodeDecodeError: byte 0xb7` reading a watcher log:
the banner used `·` (U+00B7), and Windows `print()` to a REDIRECTED stream uses
the locale encoding (cp1252), not UTF-8. So the log was not valid UTF-8 and any
reader assuming UTF-8 — the sane default, and what our own test did — fails.

The tool is stdlib-only and cross-platform by design; decorative typography in
log lines is a portability liability for no benefit. Source comments and
docstrings are unaffected: Python reads source as UTF-8 regardless of locale.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from debate import channel
from debate.watcher import LockState, WatcherConfig, read_status, status

NOW = datetime(2026, 8, 3, 12, 0, 0, tzinfo=timezone.utc)
HELD = LockState(held=True, pid=4242, stamp="2026-08-03T11:00:00+00:00", cwd="/x", channel="/y")


def _assert_ascii(text: str, where: str) -> None:
    bad = {c: hex(ord(c)) for c in text if ord(c) > 127}
    assert not bad, f"non-ASCII in {where}: {bad} -> would be written in the locale encoding on Windows"


def test_the_status_report_is_ascii(tmp_path: Path) -> None:
    root = tmp_path / "collab"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    cfg = WatcherConfig(channel_root=root, state_path=tmp_path / "state.json")

    lines, result = read_status(cfg, NOW)

    for line in lines:
        _assert_ascii(line, "watch-status report")
    _assert_ascii(f"{result.verdict}: {result.detail}", "watch-status verdict")


def test_every_status_verdict_detail_is_ascii(tmp_path: Path) -> None:
    """Walk the whole taxonomy: a verdict reached only during an incident is
    exactly the one nobody would notice was unreadable."""
    root = tmp_path / "collab"
    root.mkdir()
    cfg = WatcherConfig(
        channel_root=root, state_path=tmp_path / "state.json",
        commands={"bob": ["echo"]}, prompts={"bob": "go"}, debounce_seconds={"bob": 60},
    )
    cases: list[tuple[dict[str, Any], dict[str, Any]]] = [
        ({"seq": 1, "turn": "", "thread": "", "updated_at": ""}, {}),                      # IDLE
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T11:59:30+00:00"}, {}),  # DRIVING
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"}, {}),  # STALE uninvoked
        ({"seq": 1, "turn": "kimi", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"}, {}), # MANUAL
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T11:00:00+00:00"},
         {"invocations": {"1": {"count": 1, "last_at": "2026-08-03T11:55:00+00:00"}}}),    # INVOKED
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"},
         {"invocations": {"1": {"count": 1, "last_at": "2026-08-03T09:00:00+00:00"}}}),    # STALE invoked
        ({"seq": 1, "turn": "bob", "thread": "t", "updated_at": "2026-08-03T11:00:00+00:00"},
         {"escalated": ["t:1"]}),                                                          # ESCALATED
    ]
    seen = set()
    for signal, state in cases:
        for lock in (LockState(False, None, "", None), HELD):
            result = status(signal, state, cfg, NOW, lock)
            seen.add(result.verdict)
            _assert_ascii(f"{result.verdict}: {result.detail}", f"verdict {result.verdict}")

    invalid = status(
        {"seq": 1, "turn": "alice", "thread": "t", "updated_at": "2026-08-03T09:00:00+00:00"},
        {},
        WatcherConfig(
            channel_root=root,
            state_path=tmp_path / "managed-state.json",
            commands={"bob": ["echo"]},
            managed_version=1,
            parties=("bob", "alice"),
        ),
        NOW,
        LockState(False, None, "", None),
    )
    seen.add(invalid.verdict)
    _assert_ascii(f"{invalid.verdict}: {invalid.detail}", "verdict INVALID")

    assert seen == {"IDLE", "DRIVING", "STALE", "MANUAL", "INVOKED", "ESCALATED", "INVALID"}, seen


def test_refusal_messages_are_ascii(tmp_path: Path) -> None:
    """BOTH branches of the watch-once refusal, not just the reachable-by-default
    one. The held branch is the incident-time message an operator reads out of a
    redirected log — and it kept an em-dash for a whole round because the test
    only ever exercised the absent-lock branch (MSG-151 F1)."""
    from unittest.mock import patch

    from debate import watcher as watcher_module
    from debate.channel import ChannelError
    from debate.watcher import _refusal_message, _verify_channel_binding

    _assert_ascii(_refusal_message(tmp_path / "absent.lock"), "watch-once refusal (lock free)")

    with patch.object(watcher_module, "probe_lock", return_value=HELD):
        held_message = _refusal_message(tmp_path / "held.lock")
    _assert_ascii(held_message, "watch-once refusal (lock HELD)")
    assert "pid 4242" in held_message, "the held branch must actually have been taken"

    cfg = WatcherConfig(channel_root=tmp_path / "mine", state_path=tmp_path / "state.json")
    try:
        _verify_channel_binding({"channel_root": str(tmp_path / "theirs")}, cfg)
    except ChannelError as error:
        _assert_ascii(str(error), "channel-binding refusal")
    else:  # pragma: no cover
        raise AssertionError("expected a refusal")


def test_no_string_literal_in_the_watcher_can_carry_non_ascii() -> None:
    """The class, not the instance. Three separate line-targeted fixes each
    missed a sibling string; an AST sweep cannot. Docstrings are exempt —
    Python reads source as UTF-8 regardless of locale, and they never reach a
    stream."""

    # Widened from watcher.py alone after the setup-wizard gate (MSG-36 F2)
    # found the sweep's scoping let a NEW module ship the package's first
    # non-ASCII runtime literals. Every module, one loop, no scoping to rot.
    package = Path(__file__).resolve().parent.parent / "src" / "debate"
    for source_file in sorted(package.glob("*.py")):
        _sweep_one_module(source_file)


# The one documented exception, named constant by constant. `R3_CLAUSE` is
# protocol TEXT, not output: it is fixed word for word (a test pins it
# byte-exact against the plan), it is written into a round docket with an
# explicit `encoding="utf-8"`, and a seat reads it from that file. Nothing
# prints it, so the cp1252 hazard this law exists for cannot reach it -- and
# its em dashes (U+2014) are part of the wording the seats read. Naming the
# one constant keeps every other literal in that module under the law.
PROTOCOL_TEXT_EXCEPTIONS: dict[str, tuple[str, ...]] = {
    "delta.py": ("R3_CLAUSE",),
}


def _exempt_constants(tree: Any, names: tuple[str, ...]) -> set[int]:
    """ids of the module-level string constants bound to the named globals."""
    import ast

    exempt: set[int] = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
            continue
        if any(isinstance(target, ast.Name) and target.id in names for target in node.targets):
            exempt.add(id(node.value))
    return exempt


def _sweep_one_module(source_file: Path) -> None:
    import ast

    tree = ast.parse(source_file.read_text(encoding="utf-8"))
    exempt = _exempt_constants(tree, PROTOCOL_TEXT_EXCEPTIONS.get(source_file.name, ()))

    docstrings = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and body:
            first = body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(
                first.value.value, str
            ):
                docstrings.add(id(first.value))

    offenders = [
        (node.lineno, node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in docstrings
        and id(node) not in exempt
        and any(ord(char) > 127 for char in node.value)
    ]

    assert not offenders, f"non-ASCII string literals reachable by print/emit: {offenders}"


def test_every_protocol_text_exception_is_still_needed() -> None:
    """An exception for an ASCII constant is a stale exception."""
    from debate import delta

    for name in PROTOCOL_TEXT_EXCEPTIONS["delta.py"]:
        text = getattr(delta, name)
        assert any(ord(char) > 127 for char in text), f"{name} is ASCII now; drop its exception"
