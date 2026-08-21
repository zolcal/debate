"""The plain-words law: nothing a user reads speaks the engine's private words.

Two surfaces are scanned. The skill markdown, which the assistant reads aloud
to the user almost verbatim, and the string literals the engine itself prints
or refuses with on the three user-facing command groups (`open`, `seats`,
`onboarding`).

Both surfaces carry deliberate exceptions, and both are narrow:

* Skill markdown may hold facts that are for the assistant only, never for the
  user's ears. Such a span is marked -- a parenthetical opened with the exact
  marker below, or a section whose heading names an engine fact -- and the
  marker is what this test excludes.
* A handful of engine strings must name a literal the caller types (a command
  marker, for instance). Each one is listed below with its reason.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILL_FILES = (
    ROOT / "skills" / "debate-onboarding" / "SKILL.md",
    ROOT / "skills" / "debate" / "SKILL.md",
)

# The words the law bans. "bridge", "brokered" and "placeholder" are whole
# words; the rest are literals. A word never matches when it is spelled as a
# command-line flag (`--brokered`): that is an argument the assistant types,
# not a word said to anyone.
FORBIDDEN: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("bridge", re.compile(r"(?<!-)\bbridges?\b", re.IGNORECASE)),
    ("brokered", re.compile(r"(?<!-)\bbrokered\b", re.IGNORECASE)),
    ("placeholder", re.compile(r"(?<!-)\bplaceholders?\b", re.IGNORECASE)),
    ("managed version", re.compile(r"managed version", re.IGNORECASE)),
    ("{prompt}", re.compile(re.escape("{prompt}"), re.IGNORECASE)),
    ("{input_path}", re.compile(re.escape("{input_path}"), re.IGNORECASE)),
    ("{result_path}", re.compile(re.escape("{result_path}"), re.IGNORECASE)),
    ("operator-owned pin", re.compile(r"operator-owned pin", re.IGNORECASE)),
)

# The exact marker that opens an assistant-only parenthetical. Kept verbatim in
# the skills so this test can find it -- markdown wraps it across lines, so the
# spaces inside it match any run of whitespace.
AGENT_ONLY_MARKER = "(Engine fact for YOU, never for the user's ears:"
AGENT_ONLY_PATTERN = re.compile(r"\s+".join(re.escape(word) for word in AGENT_ONLY_MARKER.split(" ")))
AGENT_ONLY_HEADING = "Engine fact"

_HEADING = re.compile(r"^(#{1,6})\s")

# Engine strings that must name a literal the caller types. Each key is the
# whole string constant, each value the one-line reason it is allowed.
ALLOWED_LITERALS: dict[str, str] = {
    "refused: a seat command needs an executable and either a {prompt} marker "
    "(where the question text goes) or both {input_path} and {result_path} "
    "(a command that reads a request file and writes an answer file)":
        "the seat-command contract has to name the markers the caller types",
    "seat argv, e.g. '/home/me/.local/bin/my-agent {prompt}'; omit for @EFFORT derivations":
        "the same contract, shown as the example the caller copies",
}


def _blank(text: str, start: int, end: int) -> str:
    """Erase a span but keep every newline, so line numbers still line up."""
    erased = "".join("\n" if char == "\n" else " " for char in text[start:end])
    return text[:start] + erased + text[end:]


def _strip_agent_only_sections(text: str) -> str:
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    dropping_level = 0
    for line in lines:
        heading = _HEADING.match(line)
        if heading is not None:
            level = len(heading.group(1))
            if dropping_level and level <= dropping_level:
                dropping_level = 0
            if AGENT_ONLY_HEADING in line:
                dropping_level = level
        if dropping_level:
            kept.append("\n" if line.endswith("\n") else "")
        else:
            kept.append(line)
    return "".join(kept)


def _strip_agent_only_parentheticals(text: str) -> str:
    while True:
        opening = AGENT_ONLY_PATTERN.search(text)
        if opening is None:
            return text
        start = opening.start()
        depth = 0
        end = len(text)
        for index in range(start, len(text)):
            if text[index] == "(":
                depth += 1
            elif text[index] == ")":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        text = _blank(text, start, end)


def user_facing_markdown(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return _strip_agent_only_parentheticals(_strip_agent_only_sections(text))


def _violations(text: str, where: str) -> list[str]:
    found: list[str] = []
    for word, pattern in FORBIDDEN:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            found.append(f"{where}:{line}: says {word!r} -- {text.splitlines()[line - 1].strip()[:90]}")
    return found


def test_skill_markdown_speaks_plain_words() -> None:
    found: list[str] = []
    for path in SKILL_FILES:
        found.extend(_violations(user_facing_markdown(path), str(path)))
    assert not found, "\n".join(found)


# --- the engine's own user-facing strings ------------------------------------

SPEAKING_CALLS = ("print", "_flushing_print")
COMMAND_GROUPS = ("open", "seats", "onboarding")
PARSER_NAMES = re.compile(r"^p_(open|seats|onb|onboarding)")


def _strings(node: ast.AST) -> list[str]:
    """Every string constant under a node, f-string pieces included."""
    return [
        child.value
        for child in ast.walk(node)
        if isinstance(child, ast.Constant) and isinstance(child.value, str)
    ]


def _is_refusal(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr == "ChannelError"
    return isinstance(func, ast.Name) and func.id in ("ChannelError", "Refusal")


def _is_speaking(node: ast.Call) -> bool:
    func = node.func
    return isinstance(func, ast.Name) and func.id in SPEAKING_CALLS


def _help_strings(node: ast.Call) -> list[str]:
    return [
        keyword.value.value
        for keyword in node.keywords
        if keyword.arg in ("help", "description")
        and isinstance(keyword.value, ast.Constant)
        and isinstance(keyword.value.value, str)
    ] + [
        piece
        for keyword in node.keywords
        if keyword.arg in ("help", "description") and isinstance(keyword.value, (ast.JoinedStr, ast.BinOp))
        for piece in _strings(keyword.value)
    ]


def _spoken_in(node: ast.AST) -> list[tuple[int, str]]:
    spoken: list[tuple[int, str]] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if _is_refusal(child) or _is_speaking(child):
            spoken.extend((child.lineno, text) for text in _strings(child))
        spoken.extend((child.lineno, text) for text in _help_strings(child))
    return spoken


def _command_names(test: ast.AST) -> set[str]:
    """Which `args.command == "..."` literals a branch condition names."""
    names: set[str] = set()
    for child in ast.walk(test):
        if not isinstance(child, ast.Compare) or not isinstance(child.left, ast.Attribute):
            continue
        if child.left.attr != "command":
            continue
        for comparator in child.comparators:
            if isinstance(comparator, ast.Constant) and isinstance(comparator.value, str):
                names.add(comparator.value)
    return names


def _main_module_strings(tree: ast.Module) -> list[tuple[int, str]]:
    """Only the `open`, `seats` and `onboarding` surfaces of the CLI module."""
    spoken: list[tuple[int, str]] = []
    parsers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for target in node.targets:
                if isinstance(target, ast.Name) and PARSER_NAMES.match(target.id):
                    parsers.add(target.id)
                    spoken.extend((node.lineno, text) for text in _help_strings(node.value))
        if isinstance(node, ast.If) and _command_names(node.test) & set(COMMAND_GROUPS):
            for statement in node.body:
                spoken.extend(_spoken_in(statement))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "add_argument" or not isinstance(node.func.value, ast.Name):
            continue
        if node.func.value.id in parsers:
            spoken.extend((node.lineno, text) for text in _help_strings(node))
    return spoken


def engine_strings() -> list[tuple[str, int, str]]:
    collected: list[tuple[str, int, str]] = []
    for name in ("opening.py", "onboarding.py", "seats.py"):
        path = ROOT / "src" / "debate" / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        collected.extend((str(path), line, text) for line, text in _spoken_in(tree))
    main_path = ROOT / "src" / "debate" / "__main__.py"
    main_tree = ast.parse(main_path.read_text(encoding="utf-8"))
    collected.extend((str(main_path), line, text) for line, text in _main_module_strings(main_tree))
    return collected


def test_engine_speaks_plain_words_where_the_user_reads() -> None:
    found: list[str] = []
    for path, line, text in engine_strings():
        if text in ALLOWED_LITERALS:
            continue
        for word, pattern in FORBIDDEN:
            if pattern.search(text):
                found.append(f"{path}:{line}: says {word!r} -- {text.strip()[:90]}")
    assert not found, "\n".join(found)


def test_every_allowed_literal_is_still_in_the_engine() -> None:
    """An exception that no longer matches any string is a stale exception."""
    live = {text for _path, _line, text in engine_strings()}
    assert set(ALLOWED_LITERALS) <= live, sorted(set(ALLOWED_LITERALS) - live)
