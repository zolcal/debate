"""Slice C5: honest pairing -- classification, the uneven-pair gate, precedence.

A debate between a lightweight model and a frontier model is legal and
sometimes wanted, but it is never the silent default: Debate says what it
sees and makes the operator answer for it.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable

import pytest

from debate import channel, opening, seats
from debate.__main__ import _watcher_config
from test_open import _fake_tool, _raw_seat, managed_project

NOW = "2026-08-20T12:00:00+00:00"

FORBIDDEN_WORDS = (
    "bridge",
    "brokered",
    "managed version",
    "{prompt}",
    "{input_path}",
    "{result_path}",
    "placeholder",
)


def _no_ask(prompt: str) -> str:
    raise AssertionError(f"unexpected question: {prompt}")


def _seat(
    seat_id: str,
    tool: Path,
    *,
    capability_class: str | None = None,
    source: str = "catalog",
    extra: str = "",
) -> seats.Seat:
    vendor, _, submodel = seat_id.partition("/")
    argv = [str(tool), extra, "{prompt}"] if extra else [str(tool), "{prompt}"]
    return seats.Seat(
        seat_id=seat_id, vendor=vendor, submodel=submodel.split("@", 1)[0], effort=None,
        commands=[argv], source=source, present=True,
        smoke=seats.SmokeStatus(at=NOW, result="pass"),
        capability_class=capability_class,
    )


def _pair_registry(
    tmp_path: Path, first_class: str | None, second_class: str | None
) -> seats.Registry:
    registry = seats.Registry()
    registry.seats["big/one"] = _seat(
        "big/one", _fake_tool(tmp_path, "big"), capability_class=first_class,
    )
    registry.seats["small/two"] = _seat(
        "small/two", _fake_tool(tmp_path, "small"), capability_class=second_class,
    )
    return registry


def _pick(
    registry: seats.Registry,
    tmp_path: Path,
    *,
    assume_yes: bool = False,
    ask: Callable[[str], str] = _no_ask,
    allow_mismatched_pair: bool = False,
) -> tuple[str, str]:
    return opening.pick_pair(
        registry, project=str(tmp_path), requested=("big/one", "small/two"),
        assume_yes=assume_yes, ask=ask, now=NOW,
        allow_mismatched_pair=allow_mismatched_pair,
    )


# --- classification ---------------------------------------------------------


def test_classify_pair_matrix(tmp_path: Path) -> None:
    tool = _fake_tool(tmp_path, "tool")
    frontier = _seat("big/one", tool, capability_class="frontier")
    other_frontier = _seat("big/three", tool, capability_class="frontier")
    light = _seat("small/two", tool, capability_class="light")
    undeclared = _seat("plain/four", tool)
    assert opening.classify_pair(frontier, other_frontier) == "symmetric"
    assert opening.classify_pair(light, light) == "symmetric"
    assert opening.classify_pair(frontier, light) == "mismatched"
    assert opening.classify_pair(light, frontier) == "mismatched"
    assert opening.classify_pair(frontier, undeclared) == "undeclared"
    assert opening.classify_pair(undeclared, light) == "undeclared"
    assert opening.classify_pair(undeclared, undeclared) == "undeclared"


def test_effort_variant_seats_inherit_their_class(tmp_path: Path) -> None:
    """A tool-derived `@effort` seat carries the base seat's class, so an
    effort variant of a frontier model still reads as an even pairing."""
    tool = _fake_tool(tmp_path, "tool")
    base = _seat("codex/gpt-5.6-sol", tool, capability_class="frontier")
    derived = _seat(
        "codex/gpt-5.6-sol@high", tool, capability_class="frontier", source="derived",
    )
    assert derived.source == "derived"
    assert opening.classify_pair(base, derived) == "symmetric"


# --- the gate on the interactive pick ---------------------------------------


def test_uneven_pair_is_warned_and_confirmed_by_number(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    registry = _pair_registry(tmp_path, "frontier", "light")
    asked: list[str] = []

    def keep(prompt: str) -> str:
        asked.append(prompt)
        return "1"

    assert _pick(registry, tmp_path, ask=keep) == ("big/one", "small/two")
    printed = capsys.readouterr().out
    assert "frontier" in printed and "light" in printed
    assert "one-sided verdict" in printed
    assert asked and "1 keep this pair" in asked[0] and "2 pick again" in asked[0]


def test_uneven_pair_declined_or_unanswered_is_refused(tmp_path: Path) -> None:
    for answer in ("2", "", "yes"):
        registry = _pair_registry(tmp_path, "light", "frontier")
        with pytest.raises(channel.ChannelError, match="pair not confirmed"):
            _pick(registry, tmp_path, ask=lambda prompt: answer)


def test_yes_does_not_confirm_an_uneven_pair(tmp_path: Path) -> None:
    registry = _pair_registry(tmp_path, "frontier", "light")
    with pytest.raises(channel.ChannelError) as caught:
        _pick(registry, tmp_path, assume_yes=True)
    message = str(caught.value)
    assert "--allow-mismatched-pair" in message
    assert "one-sided verdict" in message


def test_the_explicit_flag_seats_an_uneven_pair_silently(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    registry = _pair_registry(tmp_path, "frontier", "light")
    assert _pick(registry, tmp_path, assume_yes=True, allow_mismatched_pair=True) == (
        "big/one", "small/two",
    )
    assert capsys.readouterr().out == ""


def test_even_pair_says_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    registry = _pair_registry(tmp_path, "frontier", "frontier")
    assert _pick(registry, tmp_path, assume_yes=True) == ("big/one", "small/two")
    assert capsys.readouterr().out == ""


def test_undeclared_class_notes_and_continues(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    registry = _pair_registry(tmp_path, "frontier", None)
    assert _pick(registry, tmp_path, assume_yes=True) == ("big/one", "small/two")
    printed = capsys.readouterr().out
    assert "no declared capability class" in printed
    assert "pairing may be uneven" in printed


# --- precedence -------------------------------------------------------------


def test_identity_guard_fires_before_the_uneven_pair_gate(tmp_path: Path) -> None:
    """Same seat twice AND a class difference: the identity refusal wins."""
    registry = _pair_registry(tmp_path, "frontier", "light")
    with pytest.raises(channel.ChannelError, match="same seat twice"):
        opening.pick_pair(
            registry, project=str(tmp_path), requested=("big/one", "big/one"),
            assume_yes=True, ask=_no_ask, now=NOW,
        )


def test_admission_fires_before_the_uneven_pair_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A seat with no verified isolation settings is refused for that reason,
    not for the class difference that also holds."""
    first = _fake_tool(tmp_path, "frontier-tool")
    second = _fake_tool(tmp_path, "light-tool")
    project, head = managed_project(
        tmp_path, monkeypatch,
        {
            "big/one": _raw_seat(
                [str(first), "{prompt}"], vendor="big", submodel="one",
                source="catalog", capability_class="frontier",
                isolation_argv=["--strict-mcp-config"],
                no_persistence_argv=["--no-session-persistence"],
            ),
            "small/two": _raw_seat(
                [str(second), "{prompt}"], vendor="small", submodel="two",
                source="catalog", capability_class="light",
            ),
        },
        ["big/one", "small/two"],
    )
    with pytest.raises(channel.ChannelError) as caught:
        opening.open_debate_brokered(
            opening.BrokeredOpenSpec(
                root=project / "collab", label="stub", pair=("big/one", "small/two"),
                source_ref=head, author_vendor="big",
            ),
            seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test", real_home=tmp_path,
        )
    message = str(caught.value)
    assert "--isolation-argv" in message
    assert "--allow-mismatched-pair" not in message


def test_managed_open_refuses_an_uneven_pair_without_the_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Nothing asks a question on this path, so an uneven pair refuses and
    names the flag that seats it deliberately."""
    first = _fake_tool(tmp_path, "frontier-tool")
    second = _fake_tool(tmp_path, "light-tool")
    rows = {
        "big/one": _raw_seat(
            [str(first), "{prompt}"], vendor="big", submodel="one",
            source="catalog", capability_class="frontier",
            isolation_argv=["--strict-mcp-config"],
            no_persistence_argv=["--no-session-persistence"],
        ),
        "small/two": _raw_seat(
            [str(second), "{prompt}"], vendor="small", submodel="two",
            source="catalog", capability_class="light",
            isolation_argv=["--offline"], no_persistence_argv=["--forget"],
        ),
    }
    project, head = managed_project(tmp_path, monkeypatch, rows, ["big/one", "small/two"])
    root = project / "collab"
    spec = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("big/one", "small/two"),
        source_ref=head, author_vendor="big",
    )
    with pytest.raises(channel.ChannelError) as caught:
        opening.open_debate_brokered(
            spec, seats.load_registry(), load_config_fn=_watcher_config,
            now=NOW, tool_version="test", real_home=tmp_path,
        )
    assert "--allow-mismatched-pair" in str(caught.value)
    assert not root.exists() or list(root.iterdir()) == []
    allowed = opening.BrokeredOpenSpec(
        root=root, label="stub", pair=("big/one", "small/two"),
        source_ref=head, author_vendor="big", allow_mismatched_pair=True,
    )
    result = opening.open_debate_brokered(
        allowed, seats.load_registry(), load_config_fn=_watcher_config,
        now=NOW, tool_version="test", real_home=tmp_path,
    )
    assert result.channel_name


# --- plain words ------------------------------------------------------------


# Every operator-facing line this slice added or reworded, one marker each.
# The test finds the literal each marker sits in and scans that whole literal,
# so a later edit that drags jargon back into the same message is caught.
OPENING_MARKERS = (
    "can't yet run in the isolated mode a managed debate needs",
    "tell me how it turns off its settings, plugins and session saving",
    "cannot take part in a fully managed debate",
    "model identity declared by the registry",
    "the tool authenticates itself through its own configuration folder",
    "the tool's own settings, plugins and session saving are turned off",
    "one-sided verdict and costs an extra deliberation round",
    "no declared capability class; pairing may be uneven",
    "1 keep this pair",
    "pair not confirmed",
    "Pass --allow-mismatched-pair to seat this pair anyway",
    "fully managed debate",
    "a fully managed debate needs the commit its seats will review",
    "a fully managed debate needs --author-vendor",
)

MAIN_MARKERS = (
    "the two seats run under Debate's control with you as supervisor",
    "a fully managed debate needs --pair",
    "a fully managed debate needs --author-vendor",
    "seat a lightweight model against a frontier model anyway",
)

# The pairing helpers are new in full, so every string in them is scanned.
NEW_PAIRING_FUNCTIONS = ("classify_pair", "_uneven_pair_sentence", "_pair_gate")


def _source(module_name: str) -> str:
    return (Path(opening.__file__).resolve().parent / module_name).read_text(encoding="utf-8")


def _flatten(node: ast.expr) -> str:
    """The text one string literal actually prints, with the values it
    interpolates left out -- only the words the tool wrote are scanned."""
    if isinstance(node, ast.Constant):
        return node.value if isinstance(node.value, str) else ""
    if isinstance(node, ast.JoinedStr):
        return "".join(_flatten(part) for part in node.values)
    return ""


def _literal_around(source: str, marker: str) -> str:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Constant, ast.JoinedStr)):
            continue
        text = _flatten(node)
        if marker in text:
            return text
    raise AssertionError(f"no string literal carries {marker!r}")


def _assert_plain(text: str, where: str) -> None:
    lowered = text.lower()
    found = [word for word in FORBIDDEN_WORDS if word in lowered]
    assert not found, f"jargon in {where}: {found}"


@pytest.mark.parametrize("marker", OPENING_MARKERS)
def test_opening_lines_are_plain_words(marker: str) -> None:
    source = _source("opening.py")
    _assert_plain(_literal_around(source, marker), f"opening.py near {marker!r}")


@pytest.mark.parametrize("marker", MAIN_MARKERS)
def test_command_line_help_and_refusals_are_plain_words(marker: str) -> None:
    source = _source("__main__.py")
    _assert_plain(_literal_around(source, marker), f"__main__.py near {marker!r}")


def test_every_string_in_the_pairing_helpers_is_plain(tmp_path: Path) -> None:
    source = _source("opening.py")
    tree = ast.parse(source)
    seen = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name not in NEW_PAIRING_FUNCTIONS:
            continue
        seen += 1
        docstring = ast.get_docstring(node, clean=False)
        for inner in ast.walk(node):
            if not isinstance(inner, ast.Constant) or not isinstance(inner.value, str):
                continue
            if inner.value == docstring:
                continue
            _assert_plain(inner.value, f"opening.{node.name}")
    assert seen == len(NEW_PAIRING_FUNCTIONS)
