"""Slice C5: honest pairing -- classification, the uneven-pair gate, precedence.

A debate between a lightweight model and a frontier model is legal and
sometimes wanted, but it is never the silent default: Debate says what it
sees and makes the operator answer for it.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Callable

import pytest

from debate import channel, opening, seats
from debate.__main__ import _watcher_config
from test_open import _fake_tool, _raw_seat, managed_project

NOW = "2026-08-20T12:00:00+00:00"
REVIEW_CONTRACT: dict[str, Any] = {
    "goal": "Review the pairing fixture.",
    "review_domain": "The fixture and its recorded acceptance criteria.",
    "stop_rule": "Stop after the fixture criteria are resolved.",
}

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
        # A seat a fully managed debate would admit. The pick now checks
        # admission BEFORE the uneven-pair gate (final wave, M3), so a fixture
        # that never declared these would be refused for the wrong reason.
        isolation_argv=["--no-config"],
        no_persistence_argv=["--no-history"],
        verification_basis="catalogued" if source == "catalog" else "declared",
        result_schema_version=2,
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
        registry, require_admissible=True, project=str(tmp_path), requested=("big/one", "small/two"),
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
            registry, require_admissible=True, project=str(tmp_path), requested=("big/one", "big/one"),
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
                source="manual", capability_class="light",
            ),
        },
        ["big/one", "small/two"],
    )
    with pytest.raises(channel.ChannelError) as caught:
        opening.open_debate_brokered(
            opening.BrokeredOpenSpec(
                root=project / "collab", label="stub", pair=("big/one", "small/two"),
                source_ref=head, author_vendor="big", **REVIEW_CONTRACT,
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
        source_ref=head, author_vendor="big", **REVIEW_CONTRACT,
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
        **REVIEW_CONTRACT,
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
    "small review, quick pair",
    "full review, strongest pair",
    "the pair you picked last time",
    "pick a number, or two seats (a,b)",
)

MAIN_MARKERS = (
    "the two seats run under Debate's control with you as supervisor",
    "a product open with --pair needs --preparation-revision",
    "a fully managed debate needs --author-vendor",
    "seat a lightweight model against a frontier model anyway",
    "without --pair, print the read-only product preparation as JSON",
    "how much review material still counts as a small review",
)

# The pairing helpers are new in full, so every string in them is scanned.
NEW_PAIRING_FUNCTIONS = (
    "classify_pair",
    "_uneven_pair_sentence",
    "_pair_gate",
    "docket_byte_size",
    "suggest_pair",
    "pair_choices",
    "pair_menu",
)


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


# --- the size-proportional suggestion (A2) ----------------------------------


def _admissible(
    seat_id: str,
    tool: Path,
    *,
    capability_class: str | None = None,
    isolated: bool = True,
) -> seats.Seat:
    """A seat a fully managed debate would actually admit: it takes a question
    and its isolation and no-saving settings are both on record."""
    seat = _seat(seat_id, tool)
    seat.capability_class = capability_class
    if not isolated:
        seat.isolation_argv = []
        seat.no_persistence_argv = []
    return seat


def _suggestion_registry(tmp_path: Path, **classes: str | None) -> seats.Registry:
    registry = seats.Registry()
    for name, capability_class in classes.items():
        seat_id = name.replace("__", "/")
        registry.seats[seat_id] = _admissible(
            seat_id, _fake_tool(tmp_path, name), capability_class=capability_class,
        )
    return registry


FOUR_SEATS = {
    "claude__haiku": "light",
    "deepseek__flash": "light",
    "claude__opus": "frontier",
    "deepseek__pro": "frontier",
}


def test_a_small_docket_suggests_a_quick_symmetric_pair(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=200,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) == ("claude/haiku", "deepseek/flash")


def test_a_large_docket_suggests_the_strongest_symmetric_pair(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=opening.QUICK_REVIEW_MAX_BYTES,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) == ("claude/opus", "deepseek/pro")


def test_without_a_matching_pair_the_remembered_one_stands(tmp_path: Path) -> None:
    registry = _suggestion_registry(
        tmp_path, claude__opus="frontier", deepseek__pro="frontier",
    )
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES,
        last_pair=("claude/opus", "deepseek/pro"),
    ) == ("claude/opus", "deepseek/pro")


def test_nothing_to_suggest_and_nothing_remembered_suggests_nothing(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, claude__opus="frontier")
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) is None


def test_a_seat_a_managed_debate_cannot_admit_is_never_suggested(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, claude__haiku="light")
    registry.seats["deepseek/flash"] = _admissible(
        "deepseek/flash", _fake_tool(tmp_path, "deepseek-flash"),
        capability_class="light", isolated=False,
    )
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) is None


def test_a_seat_with_no_declared_class_is_never_suggested(tmp_path: Path) -> None:
    registry = _suggestion_registry(
        tmp_path, claude__haiku="light", deepseek__flash=None,
    )
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) is None


def test_two_seats_from_one_vendor_pair_up_only_as_a_last_resort(tmp_path: Path) -> None:
    registry = _suggestion_registry(
        tmp_path, claude__haiku="light", claude__mini="light",
    )
    same_vendor = opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    )
    assert same_vendor == ("claude/haiku", "claude/mini")
    registry.seats["deepseek/flash"] = _admissible(
        "deepseek/flash", _fake_tool(tmp_path, "deepseek-flash"), capability_class="light",
    )
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) == ("claude/haiku", "deepseek/flash")


def test_a_missing_preferred_pair_falls_back_to_an_approved_symmetric_pair(
    tmp_path: Path,
) -> None:
    """Half of the quick pair is not approved here, so the strongest approved
    symmetric pair is offered with an honest fallback reason."""
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    approved = ("claude/haiku", "claude/opus", "deepseek/pro")
    suggestion = opening.suggest_pair_with_reason(
        registry, allowlist=approved, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    )
    assert suggestion is not None
    assert suggestion.pair == ("claude/opus", "deepseek/pro")
    assert suggestion.reason == (
        "no symmetric light pair is available; using a symmetric frontier pair"
    )
    assert opening.suggest_pair(
        registry, allowlist=approved, docket_bytes=opening.QUICK_REVIEW_MAX_BYTES,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    ) == ("claude/opus", "deepseek/pro")


# --- the numbered list ------------------------------------------------------


def _numbered(lines: list[str]) -> list[str]:
    return [line for line in lines if line.strip()[:1].isdigit()]


def test_the_menu_numbers_every_choice_and_reasons_the_first(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    suggestion = opening.suggest_pair_with_reason(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    )
    lines = opening.pair_menu(
        registry, allowlist=None, suggestion=suggestion, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES,
    )
    numbered = _numbered(lines)
    assert numbered[0].startswith("1  claude/haiku + deepseek/flash")
    assert "small review, quick pair" in numbered[0]
    assert [line.split()[0] for line in numbered] == [
        str(index) for index in range(1, len(numbered) + 1)
    ]
    assert len(numbered) <= 6


def test_the_menu_reasons_a_full_review_by_its_size(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    big = opening.QUICK_REVIEW_MAX_BYTES + 1
    suggestion = opening.suggest_pair_with_reason(
        registry, allowlist=None, docket_bytes=big,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    )
    lines = opening.pair_menu(
        registry, allowlist=None, suggestion=suggestion, docket_bytes=big,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES,
    )
    assert "full review, strongest pair" in _numbered(lines)[0]


def test_a_long_menu_is_capped_and_says_how_many_it_left_out(tmp_path: Path) -> None:
    registry = _suggestion_registry(
        tmp_path,
        claude__haiku="light", deepseek__flash="light", zed__small="light",
        claude__opus="frontier", deepseek__pro="frontier", zed__big="frontier",
    )
    suggestion = opening.suggest_pair_with_reason(
        registry, allowlist=None, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES, last_pair=None,
    )
    lines = opening.pair_menu(
        registry, allowlist=None, suggestion=suggestion, docket_bytes=10,
        quick_review_max_bytes=opening.QUICK_REVIEW_MAX_BYTES,
    )
    assert len(_numbered(lines)) == 6
    assert any("more" in line for line in lines)


# --- pick_pair consumes both ------------------------------------------------


def test_the_pick_shows_the_numbered_list_and_takes_a_number(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    pair = opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=False,
        ask=lambda prompt: "", now=NOW, docket_bytes=10,
    )
    printed = capsys.readouterr().out
    assert "1  claude/haiku + deepseek/flash" in printed
    assert "small review, quick pair" in printed
    assert pair == ("claude/haiku", "deepseek/flash")


def test_yes_accepts_the_first_item(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    assert opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=True,
        ask=_no_ask, now=NOW, docket_bytes=opening.QUICK_REVIEW_MAX_BYTES,
    ) == ("claude/opus", "deepseek/pro")


def test_an_uneven_remembered_pair_is_never_the_first_item(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The remembered pair was a lightweight model against a frontier one; a
    matched pair exists, so the matched pair leads and --yes takes it."""
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    registry.last_pair[str(tmp_path)] = ["claude/opus", "deepseek/flash"]
    assert opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=True,
        ask=_no_ask, now=NOW, docket_bytes=10,
    ) == ("claude/haiku", "deepseek/flash")


def test_a_typed_number_picks_that_line(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    seen: list[str] = []

    def answer(prompt: str) -> str:
        seen.append(prompt)
        return "2"

    pair = opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=False,
        ask=answer, now=NOW, docket_bytes=10, allow_mismatched_pair=True,
    )
    assert pair != ("claude/haiku", "deepseek/flash")
    assert seen


# --- one admission test, two callers (A2 fix round 1) -----------------------


def test_a_bad_configuration_folder_refuses_and_is_never_suggested(tmp_path: Path) -> None:
    """The registry can be hand-edited after a seat was recorded, so the folder
    rule is re-checked at use. Seating says why; the suggestion just drops it,
    and both read the same rule from the same place."""
    registry = _suggestion_registry(tmp_path, claude__haiku="light")
    stale = _admissible(
        "deepseek/flash", _fake_tool(tmp_path, "deepseek-flash"), capability_class="light",
    )
    stale.config_home = "CLAUDE_CONFIG_DIR=../outside"
    registry.seats["deepseek/flash"] = stale
    elsewhere = tmp_path / "elsewhere"

    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10, last_pair=None, real_home=elsewhere,
    ) is None
    with pytest.raises(channel.ChannelError) as caught:
        opening._brokered_adapter(
            stale, tool_version="test", author_vendor="claude", real_home=elsewhere,
        )
    assert opening.admission_problem(stale, real_home=elsewhere) == str(caught.value)
    assert "'..'" in str(caught.value)


def test_the_one_admission_test_answers_for_both_seat_shapes(tmp_path: Path) -> None:
    tool = _fake_tool(tmp_path, "tool")
    ready = _admissible("claude/haiku", tool, capability_class="light")
    assert opening.admission_problem(ready, real_home=tmp_path) is None
    handwritten = _seat("hand/written", tool)
    handwritten.commands = [[str(tool), "{input_path}", "{result_path}"]]
    assert opening.admission_problem(handwritten, real_home=tmp_path) is None
    unflagged = _admissible("small/two", tool, capability_class="light", isolated=False)
    unflagged.source = "manual"  # the seat the declaration advice is for
    problem = opening.admission_problem(unflagged, real_home=tmp_path)
    assert problem is not None and "--isolation-argv" in problem
    # Debate's own entry for a tool it has verified NOTHING for (here: a vendor
    # the catalog does not carry at all) is sent down the new-seat-id path, not
    # told to refresh -- a refresh could not add settings the catalog lacks.
    unflagged.source = "catalog"
    catalogued = opening.admission_problem(unflagged, real_home=tmp_path)
    assert catalogued is not None and "no verified isolation settings" in catalogued
    assert "debate seats discover" not in catalogued


def test_a_remembered_pair_that_lost_its_flags_is_not_suggested(tmp_path: Path) -> None:
    """A seat can lose the settings that let it run under Debate's control
    after it was last used; the pair from last time is then no pair at all."""
    registry = _suggestion_registry(
        tmp_path, claude__haiku="light", deepseek__flash="light",
    )
    registry.seats["claude/haiku"].isolation_argv = []
    registry.last_pair[str(tmp_path)] = ["claude/haiku", "deepseek/flash"]
    assert opening.remembered_pair(
        registry, project=str(tmp_path), allowlist=None, real_home=tmp_path,
    ) is None
    with pytest.raises(channel.ChannelError, match="usable default pair"):
        opening.pick_pair(
            registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=True,
            ask=_no_ask, now=NOW, docket_bytes=10, real_home=tmp_path,
        )


def test_a_stale_remembered_pair_gives_way_to_one_that_still_works(
    tmp_path: Path
) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    registry.seats["claude/haiku"].no_persistence_argv = []
    registry.last_pair[str(tmp_path)] = ["claude/haiku", "deepseek/flash"]
    assert opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=True,
        ask=_no_ask, now=NOW, docket_bytes=opening.QUICK_REVIEW_MAX_BYTES,
        real_home=tmp_path,
    ) == ("claude/opus", "deepseek/pro")


def test_a_remembered_pair_that_never_said_how_strong_it_is_still_leads(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The user's own last choice is not disqualified by a missing class: it
    leads as the pair from last time, and the note about it still prints."""
    registry = _suggestion_registry(
        tmp_path, claude__haiku=None, deepseek__flash=None,
    )
    registry.last_pair[str(tmp_path)] = ["claude/haiku", "deepseek/flash"]
    suggestion = opening.suggest_pair_with_reason(
        registry, allowlist=None, docket_bytes=10,
        last_pair=opening.remembered_pair(
            registry, project=str(tmp_path), allowlist=None, real_home=tmp_path,
        ),
        real_home=tmp_path,
    )
    assert suggestion is not None
    assert suggestion.pair == ("claude/haiku", "deepseek/flash")
    assert suggestion.reason == opening.REMEMBERED_PAIR_REASON
    lines = opening.pair_menu(
        registry, allowlist=None, suggestion=suggestion, docket_bytes=10,
        real_home=tmp_path,
    )
    assert lines[0] == (
        f"1  claude/haiku + deepseek/flash  --  {opening.REMEMBERED_PAIR_REASON}"
    )
    assert opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None, assume_yes=True,
        ask=_no_ask, now=NOW, docket_bytes=10, real_home=tmp_path,
    ) == ("claude/haiku", "deepseek/flash")
    assert "no declared capability class" in capsys.readouterr().out


def test_the_reason_follows_where_the_pair_came_from(tmp_path: Path) -> None:
    """A remembered pair is labelled as remembered even when its seats happen
    to be the strength this review calls for -- the reason travels with the
    choice instead of being guessed back from it."""
    registry = _suggestion_registry(
        tmp_path, claude__haiku="light", deepseek__flash="light",
    )
    suggestion = opening.suggest_pair_with_reason(
        registry, allowlist=("claude/haiku",), docket_bytes=10,
        last_pair=("claude/haiku", "deepseek/flash"), real_home=tmp_path,
    )
    assert suggestion is not None
    assert suggestion.pair == ("claude/haiku", "deepseek/flash")
    assert suggestion.reason == opening.REMEMBERED_PAIR_REASON


# --- who the admission rule applies to (A2 fix round 2) ---------------------


def _flagless(tmp_path: Path) -> seats.Registry:
    """Two evenly matched seats that never said how they turn their settings
    off: fine for the older open, not for a debate Debate runs itself."""
    registry = _suggestion_registry(
        tmp_path, claude__haiku="light", deepseek__flash="light",
    )
    for seat in registry.seats.values():
        seat.isolation_argv = []
        seat.no_persistence_argv = []
    return registry


def test_the_older_open_suggests_seats_the_managed_path_could_not(
    tmp_path: Path
) -> None:
    registry = _flagless(tmp_path)
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10, last_pair=None,
        require_admissible=False,
    ) == ("claude/haiku", "deepseek/flash")
    assert opening.pick_pair(
        registry, project=str(tmp_path), requested=None, assume_yes=True,
        ask=_no_ask, now=NOW, docket_bytes=10, require_admissible=False,
    ) == ("claude/haiku", "deepseek/flash")


def test_the_managed_path_never_suggests_them(tmp_path: Path) -> None:
    registry = _flagless(tmp_path)
    assert opening.suggest_pair(
        registry, allowlist=None, docket_bytes=10, last_pair=None,
        require_admissible=True,
    ) is None
    registry.last_pair[str(tmp_path)] = ["claude/haiku", "deepseek/flash"]
    assert opening.remembered_pair(
        registry, project=str(tmp_path), allowlist=None, real_home=tmp_path,
        require_admissible=True,
    ) is None
    assert opening.remembered_pair(
        registry, project=str(tmp_path), allowlist=None, real_home=tmp_path,
        require_admissible=False,
    ) == ("claude/haiku", "deepseek/flash")
    with pytest.raises(channel.ChannelError, match="usable default pair"):
        opening.pick_pair(
            registry, project=str(tmp_path), requested=None, assume_yes=True,
            ask=_no_ask, now=NOW, docket_bytes=10, require_admissible=True,
        )


# --- final review wave M2/M3: the typed answer, and the order of the gates ---


@pytest.mark.parametrize("answer", ["0", "99", "-1"])
def test_an_out_of_range_menu_number_says_which_numbers_exist(
    tmp_path: Path, answer: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """A number outside the list is a mistyped MENU answer, not an attempt at a
    pair of seat ids, and the refusal has to say so (final wave, M2)."""
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    with pytest.raises(channel.ChannelError) as caught:
        opening.pick_pair(
            registry, require_admissible=True, project=str(tmp_path), requested=None,
            assume_yes=False, ask=lambda prompt: answer, now=NOW, docket_bytes=10,
            real_home=tmp_path,
        )
    message = str(caught.value)
    assert "pick a number between 1 and" in message
    assert "two seat ids" in message
    assert "a pair is exactly two seat ids" not in message


def test_a_typed_pair_of_seat_ids_still_reads_as_a_pair(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    assert opening.pick_pair(
        registry, require_admissible=True, project=str(tmp_path), requested=None,
        assume_yes=False, ask=lambda prompt: "claude/opus, deepseek/pro", now=NOW,
        docket_bytes=10, real_home=tmp_path,
    ) == ("claude/opus", "deepseek/pro")


def test_something_that_is_neither_a_number_nor_a_pair_still_says_so(tmp_path: Path) -> None:
    registry = _suggestion_registry(tmp_path, **FOUR_SEATS)
    with pytest.raises(channel.ChannelError, match="exactly two seat ids"):
        opening.pick_pair(
            registry, require_admissible=True, project=str(tmp_path), requested=None,
            assume_yes=False, ask=lambda prompt: "claude/opus", now=NOW,
            docket_bytes=10, real_home=tmp_path,
        )


def test_admission_fires_before_the_mismatch_gate_on_a_requested_pair(
    tmp_path: Path
) -> None:
    """Plan 3.6's order -- selection, identity, admission, then the uneven-pair
    gate. A pair that is BOTH inadmissible and uneven hears about admission,
    because that is the one nothing waives (final wave, M3)."""
    registry = _pair_registry(tmp_path, "frontier", "light")
    registry.seats["small/two"].isolation_argv = []
    with pytest.raises(channel.ChannelError) as caught:
        opening.pick_pair(
            registry, require_admissible=True, project=str(tmp_path),
            requested=("big/one", "small/two"), assume_yes=True, ask=_no_ask,
            now=NOW, real_home=tmp_path,
        )
    message = str(caught.value)
    assert "small/two" in message
    assert "--allow-mismatched-pair" not in message
    assert "one-sided verdict" not in message


def test_the_older_open_never_applies_the_admission_rule(tmp_path: Path) -> None:
    """v1 open runs no seat itself, so it asks for presence and approval only."""
    registry = _pair_registry(tmp_path, "frontier", "frontier")
    registry.seats["small/two"].isolation_argv = []
    assert opening.pick_pair(
        registry, require_admissible=False, project=str(tmp_path),
        requested=("big/one", "small/two"), assume_yes=True, ask=_no_ask, now=NOW,
        real_home=tmp_path,
    ) == ("big/one", "small/two")
