"""Version lockstep: pyproject, package, and both plugin manifests must agree."""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_all_four_version_locations_agree() -> None:
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE)
    assert match is not None
    version = match.group(1)

    import debate

    assert debate.__version__ == version
    plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["version"] == version
    marketplace = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["metadata"]["version"] == version
    codex_plugin = json.loads((REPO / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert codex_plugin["version"] == version


def test_active_product_text_has_one_cap_twelve_policy() -> None:
    active = [
        REPO / "README.md",
        REPO / "CHANGELOG.md",
        REPO / "skills" / "debate-onboarding" / "SKILL.md",
        REPO / "src" / "debate" / "opening.py",
        REPO / "src" / "debate" / "__main__.py",
    ]
    forbidden = (
        re.compile(r"\bcap[- ]?5\b", re.IGNORECASE),
        re.compile(r"\bfour vote-producing\b", re.IGNORECASE),
        re.compile(r"\beight nested(?:-seat)? launches\b", re.IGNORECASE),
        re.compile(r"\bfour-review\b", re.IGNORECASE),
        re.compile(r"\bfour-launch\b", re.IGNORECASE),
    )
    hits: list[str] = []
    for path in active:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            if pattern.search(text):
                hits.append(f"{path.relative_to(REPO)}: {pattern.pattern}")
    assert hits == []
