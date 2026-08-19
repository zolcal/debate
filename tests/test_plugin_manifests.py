"""Plugin manifest schema checks (plan Slice 4 lane 'manifest-schema')."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _load(relative: str) -> dict[str, object]:
    raw = json.loads((REPO / relative).read_text(encoding="utf-8"))
    assert isinstance(raw, dict), relative
    return raw


def test_claude_plugin_manifest() -> None:
    plugin = _load(".claude-plugin/plugin.json")
    assert plugin["name"] == "debate"
    assert "pip install debate" not in str(plugin["description"])  # engine is bundled


def test_claude_marketplace_manifest() -> None:
    marketplace = _load(".claude-plugin/marketplace.json")
    plugins = marketplace["plugins"]
    assert isinstance(plugins, list) and len(plugins) == 1
    entry = plugins[0]
    assert isinstance(entry, dict)
    assert entry["name"] == "debate"
    assert entry["source"] == "./"


def test_codex_plugin_manifest() -> None:
    plugin = _load(".codex-plugin/plugin.json")
    assert plugin["name"] == "debate"
    skills = plugin["skills"]
    assert isinstance(skills, str)
    assert (REPO / skills).is_dir()


def test_codex_marketplace_manifest() -> None:
    marketplace = _load(".agents/plugins/marketplace.json")
    plugins = marketplace["plugins"]
    assert isinstance(plugins, list) and len(plugins) == 1
    entry = plugins[0]
    assert isinstance(entry, dict)
    source = entry["source"]
    assert isinstance(source, dict)
    # Codex resolves the path against the MARKETPLACE ROOT (the directory
    # holding .agents/plugins/marketplace.json), so '.' means the repo root.
    assert source == {"source": "local", "path": "."}


def test_plugin_ships_everything_the_hook_and_skills_need() -> None:
    for relative in (
        "hooks/hooks.json",
        "hooks/hooks-codex.json",
        "hooks/session-start",
        "scripts/debate-plugin",
        "skills/debate/SKILL.md",
        "skills/debate-onboarding/SKILL.md",
        "src/debate/onboarding.py",
    ):
        assert (REPO / relative).is_file(), relative
