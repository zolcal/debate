"""Slice 3 of docs/plans/2026-08-01-channel-identity-binding.md (APPROVED MSG-122).

Pinned prompts addressed the channel relatively (`./collab`, `--root collab`).
The watcher deliberately does not override the child's cwd, and every project
in this fleet names its channel `collab` — so a seat could resolve the wrong
one. That is the 2026-07-28 wrong-process kill in config form, and the example
config we ship taught it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from debate.watcher import WatcherConfig

REPO_ROOT = Path(__file__).resolve().parent.parent


def config(tmp_path: Path, **overrides: Any) -> WatcherConfig:
    defaults: dict[str, Any] = dict(
        channel_root=tmp_path / "collab",
        state_path=tmp_path / "state.json",
        commands={"glm": ["agent", "{prompt}"]},
        prompts={"glm": "Review channel {channel_root}; post via debate --root {channel_root}."},
        debounce_seconds={},
        retry_seconds=1800,
    )
    defaults.update(overrides)
    return WatcherConfig(**defaults)


def test_channel_root_expands_to_the_resolved_absolute_path(tmp_path: Path) -> None:
    (tmp_path / "collab").mkdir()
    argv = config(tmp_path).command_for("glm")

    assert argv is not None
    prompt = argv[1]
    assert "{channel_root}" not in prompt
    assert prompt.count(str((tmp_path / "collab").resolve())) == 2, "both references expand from one pass"


def test_a_prompt_without_the_placeholder_is_untouched(tmp_path: Path) -> None:
    """No forced migration: existing configs keep working exactly as they did."""
    argv = config(tmp_path, prompts={"glm": "It is your turn on ./collab."}).command_for("glm")

    assert argv == ["agent", "It is your turn on ./collab."]


def test_a_channel_root_in_the_prompt_body_is_not_re_expanded(tmp_path: Path) -> None:
    """Expansion order, pinned at MSG-122: {channel_root} is expanded inside the
    prompt FIRST, then the prompt is substituted into argv. No argv element is
    re-scanned afterwards, so a literal placeholder arriving from message text
    cannot trigger a second pass."""
    (tmp_path / "collab").mkdir()
    sneaky = config(tmp_path, prompts={"glm": "Quote this verbatim: {prompt}"})

    argv = sneaky.command_for("glm")

    assert argv == ["agent", "Quote this verbatim: {prompt}"], "argv must not be re-scanned after substitution"


def test_the_shipped_example_teaches_absolute_addressing(tmp_path: Path) -> None:
    """The example is the file people copy. While it said `./collab`, every
    deployment inherited the ambiguity — this repo's own live config did."""
    example = json.loads((REPO_ROOT / "watcher.example.json").read_text(encoding="utf-8"))

    for party, prompt in example.get("prompts", {}).items():
        assert "{channel_root}" in prompt, f"{party}'s prompt must address the channel absolutely"
        assert not re.search(r"(\./collab|--root collab\b)", prompt), (
            f"{party}'s prompt still addresses the channel relatively: {prompt!r}"
        )


def test_channel_root_is_a_prompt_placeholder_not_an_argv_one(tmp_path: Path) -> None:
    """Scope, and the thing that pins the ORDER: only the prompt text is
    expanded. If expansion were applied across argv after substitution instead,
    this literal would be rewritten — so this test fails the moment the two
    passes are swapped or broadened."""
    (tmp_path / "collab").mkdir()
    cfg = config(tmp_path, commands={"glm": ["agent", "--cwd", "{channel_root}", "{prompt}"]})

    argv = cfg.command_for("glm")

    assert argv is not None
    assert argv[2] == "{channel_root}", "argv is never scanned for {channel_root}; prompts are"
