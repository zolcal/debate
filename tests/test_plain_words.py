"""The plain-words law: nothing a user reads speaks the engine's private words.

Everything a user reads from this product is scanned: the skill markdown the
assistant reads aloud almost verbatim, the README's prose, and every string
the engine itself shows -- `--help` text for every subcommand, every refusal,
every printed line and every hint.

The exceptions are narrow, and each has a rule of its own:

* Skill markdown may hold facts that are for the assistant only, never for the
  user's ears. Such a span is marked -- a parenthetical opened with the exact
  marker below, or a section whose heading names an engine fact -- and the
  marker is what this test excludes.
* A command EXAMPLE in the README is syntax the reader types, not prose about
  the product, so fenced blocks and inline-code spans are exempt there. The
  prose around them is not.
* A literal token is not prose either: a flag (`--brokered`), a path, or a
  file name (`watcher.brokered.example.json`) is something the reader types or
  opens, and no amount of better wording can rename it.
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

README = ROOT / "README.md"

ENGINE_MODULES = ("opening.py", "onboarding.py", "seats.py", "__main__.py")

# The words the law bans. "bridge", "brokered" and "placeholder" are whole
# words; the rest are literals.
FORBIDDEN: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("bridge", re.compile(r"\bbridges?\b", re.IGNORECASE)),
    ("brokered", re.compile(r"\bbrokered\b", re.IGNORECASE)),
    ("placeholder", re.compile(r"\bplaceholders?\b", re.IGNORECASE)),
    ("managed version", re.compile(r"managed version", re.IGNORECASE)),
    ("{prompt}", re.compile(re.escape("{prompt}"), re.IGNORECASE)),
    ("{input_path}", re.compile(re.escape("{input_path}"), re.IGNORECASE)),
    ("{result_path}", re.compile(re.escape("{result_path}"), re.IGNORECASE)),
    ("operator-owned pin", re.compile(r"operator-owned pin", re.IGNORECASE)),
)

# A hit inside a literal token -- a flag, a path, a file name -- is not the
# product saying the word. What merely WRAPS a token in prose (quotes, markdown
# emphasis, sentence punctuation) is not part of the token.
_WRAPPING = "`*_\"'()[]{}.,;:!?"


def _is_literal_token(text: str, start: int, end: int) -> bool:
    left = start
    while left > 0 and not text[left - 1].isspace():
        left -= 1
    right = end
    while right < len(text) and not text[right].isspace():
        right += 1
    token = text[left:right].strip(_WRAPPING)
    return token.startswith("-") or "/" in token or re.search(r"\.\w", token) is not None


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
    "seat command, e.g. --command 'glm=/home/me/.local/bin/glm-agent {prompt}'; "
    "skips that party's question":
        "the wizard's own copy of that example",
    ' must be a list of arguments (e.g. ["/path/to/agent", "{prompt}"]), got ':
        "the watcher-config command contract, which has to show the marker's place",
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


_FENCE = re.compile(r"^\s*(```|~~~)", re.MULTILINE)
_INLINE_CODE = re.compile(r"(`+)(?:.|\n)*?\1")
# A markdown link's destination is a file name or a URL -- a reference the
# reader clicks or opens, exactly as literal as a command example.
_LINK_TARGET = re.compile(r"\]\([^)\s]+")


def _strip_code(text: str) -> str:
    """Blank out fenced blocks and inline-code spans, keeping line numbers.

    A command example is syntax the reader types, so `{prompt}` inside one is
    the seat-command contract, not product prose (controller ruling, C6 fix
    round 1). Everything around the code is prose and stays in the scan.
    """
    fences = list(_FENCE.finditer(text))
    for opening_fence, closing_fence in zip(fences[::2], fences[1::2]):
        end = text.find("\n", closing_fence.end())
        text = _blank(text, opening_fence.start(), len(text) if end < 0 else end)
    while True:
        span = _INLINE_CODE.search(text)
        if span is None:
            break
        text = _blank(text, span.start(), span.end())
    for link in _LINK_TARGET.finditer(text):
        text = _blank(text, link.start() + 2, link.end())
    return text


def user_facing_prose(path: Path) -> str:
    return _strip_code(path.read_text(encoding="utf-8"))


def _violations(text: str, where: str) -> list[str]:
    found: list[str] = []
    for word, pattern in FORBIDDEN:
        for match in pattern.finditer(text):
            if _is_literal_token(text, match.start(), match.end()):
                continue
            line = text.count("\n", 0, match.start()) + 1
            found.append(f"{where}:{line}: says {word!r} -- {text.splitlines()[line - 1].strip()[:90]}")
    return found


def test_readme_prose_speaks_plain_words() -> None:
    found = _violations(user_facing_prose(README), str(README))
    assert not found, "\n".join(found)


def test_skill_markdown_speaks_plain_words() -> None:
    found: list[str] = []
    for path in SKILL_FILES:
        found.extend(_violations(user_facing_markdown(path), str(path)))
    assert not found, "\n".join(found)


# --- the engine's own user-facing strings ------------------------------------

SPEAKING_CALLS = ("print", "_flushing_print")


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


# Lines the engine builds first and prints later: `hints` come back from an
# open, `reasons` and `lines` are what `status_lines` renders.
SPOKEN_LISTS = ("hints", "reasons", "lines")


def _is_spoken_list(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id in SPOKEN_LISTS


def _spoken_in(node: ast.AST) -> list[tuple[int, str]]:
    spoken: list[tuple[int, str]] = []
    for child in ast.walk(node):
        if isinstance(child, (ast.Assign, ast.AnnAssign)):
            targets = child.targets if isinstance(child, ast.Assign) else [child.target]
            if child.value is not None and isinstance(child.value, ast.List) and any(
                _is_spoken_list(target) for target in targets
            ):
                spoken.extend((child.lineno, text) for text in _strings(child.value))
            continue
        if not isinstance(child, ast.Call):
            continue
        if isinstance(child.func, ast.Attribute) and child.func.attr in ("append", "extend"):
            if _is_spoken_list(child.func.value):
                spoken.extend((child.lineno, text) for argument in child.args for text in _strings(argument))
        if _is_refusal(child) or _is_speaking(child):
            spoken.extend((child.lineno, text) for text in _strings(child))
        spoken.extend((child.lineno, text) for text in _help_strings(child))
    return spoken


def engine_strings() -> list[tuple[str, int, str]]:
    """Every string the engine can put in front of a user, module by module.

    The CLI module is scanned WHOLE: `--help` belongs to every subcommand, not
    just the three the product flow drives (controller ruling, C6 fix round 1).
    """
    collected: list[tuple[str, int, str]] = []
    for name in ENGINE_MODULES:
        path = ROOT / "src" / "debate" / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        collected.extend((str(path), line, text) for line, text in _spoken_in(tree))
    return collected


def test_engine_speaks_plain_words_where_the_user_reads() -> None:
    found: list[str] = []
    for path, line, text in engine_strings():
        if text in ALLOWED_LITERALS:
            continue
        for word, pattern in FORBIDDEN:
            for match in pattern.finditer(text):
                if _is_literal_token(text, match.start(), match.end()):
                    continue
                found.append(f"{path}:{line}: says {word!r} -- {text.strip()[:90]}")
    assert not found, "\n".join(found)


def test_every_allowed_literal_is_still_in_the_engine() -> None:
    """An exception that no longer matches any string is a stale exception."""
    live = {text for _path, _line, text in engine_strings()}
    assert set(ALLOWED_LITERALS) <= live, sorted(set(ALLOWED_LITERALS) - live)
