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

# Only a REAL extension makes a token a file name. "any dot plus a letter" also
# swallowed a word glued to a sentence's full stop by a missing space, which is
# prose with a typo, not a file (fix round 2).
_FILE_EXTENSIONS = frozenset(
    "json jsonl md py sh bash txt toml yml yaml cfg ini js ts html css log csv service".split()
)


def _is_literal_token(text: str, start: int, end: int) -> bool:
    left = start
    while left > 0 and not text[left - 1].isspace():
        left -= 1
    right = end
    while right < len(text) and not text[right].isspace():
        right += 1
    token = text[left:right].strip(_WRAPPING)
    if token.startswith("-") or "/" in token:
        return True
    return "." in token and token.rpartition(".")[2].lower() in _FILE_EXTENSIONS


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


_FENCE = re.compile(r"^[ \t]*(```|~~~)[ \t]*([A-Za-z0-9_+-]*)", re.MULTILINE)
_INLINE_CODE = re.compile(r"(`+)(?:.|\n)*?\1")
# Fences whose comment leader is `#`. An untagged fence is shell by convention
# in this README; anything else (json, python, ...) is blanked whole.
_HASH_COMMENT_FENCES = frozenset(("", "bash", "sh", "shell", "console", "zsh", "text"))
# A markdown link's destination is a file name or a URL -- a reference the
# reader clicks or opens, exactly as literal as a command example.
_LINK_TARGET = re.compile(r"\]\([^)\s]+")


def _is_prose_comment(line: str) -> bool:
    """A `#` comment line inside a shell fence is prose, not syntax.

    A shebang is not a comment -- it is the first line the kernel reads.
    """
    stripped = line.strip()
    return stripped.startswith("#") and not stripped.startswith("#!")


def _strip_code(text: str) -> str:
    """Blank out code, keeping line numbers -- but NOT the prose inside it.

    A command example is syntax the reader types, so `{prompt}` inside one is
    the seat-command contract, not product prose (controller ruling, C6 fix
    round 1). A `#` COMMENT inside a shell fence is the opposite: sentences
    written to the reader, which is exactly where a stale jargon line hides
    (fix round 2). So in a fence whose comment leader is `#`, command lines are
    blanked and comment lines stay in the scan; every other fence, and every
    inline-code span, is blanked whole.
    """
    fences = list(_FENCE.finditer(text))
    for opening_fence, closing_fence in zip(fences[::2], fences[1::2]):
        end = text.find("\n", closing_fence.end())
        end = len(text) if end < 0 else end
        if opening_fence.group(2).lower() not in _HASH_COMMENT_FENCES:
            text = _blank(text, opening_fence.start(), end)
            continue
        cursor = opening_fence.start()
        for line in text[opening_fence.start():end].splitlines(keepends=True):
            stop = cursor + len(line)
            if not _is_prose_comment(line):
                text = _blank(text, cursor, stop)
            cursor = stop
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

# Words the engine keeps in a named constant and speaks from somewhere else --
# a refusal a predicate RETURNS rather than raises, or the reason a suggestion
# carries. The NAME is the declaration: `..._REFUSAL` and `..._REASON` are read
# as things a user will see (fix round 2).
SPOKEN_CONSTANT = re.compile(r"_(REFUSAL|REASON)$")


def _is_spoken_list(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id in SPOKEN_LISTS


def _is_spoken_constant(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and SPOKEN_CONSTANT.search(node.id) is not None


def _spoken_in(node: ast.AST) -> list[tuple[int, str]]:
    spoken: list[tuple[int, str]] = []
    for child in ast.walk(node):
        if isinstance(child, (ast.Assign, ast.AnnAssign)):
            targets = child.targets if isinstance(child, ast.Assign) else [child.target]
            if child.value is not None and isinstance(child.value, ast.List) and any(
                _is_spoken_list(target) for target in targets
            ):
                spoken.extend((child.lineno, text) for text in _strings(child.value))
            if child.value is not None and any(
                _is_spoken_constant(target) for target in targets
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


# --- the scanner's own blind spots, kept closed ------------------------------

_FENCE_WITH_JARGON_COMMENT = """Text above.

```bash
# The 0.8 product default: mint a BROKERED managed version 2 channel instead.
debate open --root ./collab --label market-research
```

Text below.
"""

_FENCE_WITH_JARGON_COMMAND = """Text above.

```bash
# The 0.8 product default: start a fully managed debate instead.
debate open --brokered --root ./collab --label market-research
```

Text below.
"""


def test_a_comment_inside_a_code_fence_is_prose_and_is_reported() -> None:
    """The shape that slipped through round 1: stale jargon in a `#` comment."""
    found = _violations(_strip_code(_FENCE_WITH_JARGON_COMMENT), "fixture.md")
    assert [line.split(" -- ")[0] for line in found] == [
        "fixture.md:4: says 'brokered'",
        "fixture.md:4: says 'managed version'",
    ], found


def test_a_command_inside_a_code_fence_is_syntax_and_is_not_reported() -> None:
    """The same block with the jargon only where the reader types it."""
    assert not _violations(_strip_code(_FENCE_WITH_JARGON_COMMAND), "fixture.md")


def test_a_shebang_is_not_a_comment() -> None:
    assert not _is_prose_comment("#!/bin/sh")
    assert _is_prose_comment("  # a sentence about brokered things")


def test_a_word_glued_to_a_full_stop_is_not_a_file_name() -> None:
    """The round-2 minor: 'sentence.Brokered' is a typo, not a file."""
    glued = "one sentence.brokered is what a missing space looks like"
    assert _violations(glued, "fixture.md")
    assert not _violations("see watcher.brokered.example.json for the shape", "fixture.md")


def test_a_refusal_kept_in_a_constant_is_scanned_like_a_refusal() -> None:
    """The blind spot fix round 2 closed: a refusal that a predicate RETURNS
    reads to the scanner as an ordinary assignment, not as a refusal. Naming
    the constant `..._REFUSAL` (or `..._REASON`) puts it back in the scan.
    """
    from debate import opening

    live = {text for _path, _line, text in engine_strings()}
    assert opening.NO_ISOLATION_SETTINGS_REFUSAL in live
    assert opening.NO_QUESTION_MARKER_REFUSAL in live
    assert opening.QUICK_PAIR_REASON in live
