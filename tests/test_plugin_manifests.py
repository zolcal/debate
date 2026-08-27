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


def test_installed_onboarding_skill_carries_the_field_fold_contract() -> None:
    skill = (REPO / "skills/debate-onboarding/SKILL.md").read_text(encoding="utf-8")
    for row in (
        "| Subject |",
        "| Exact artifact |",
        "| Mode |",
        "| Goal |",
        "| Valid review domain |",
        "| Acceptance criteria |",
        "| Verification commands |",
        "| Stop rule |",
        "| Seats |",
        "| Clean path |",
        "| Enforced maximum |",
    ):
        assert row in skill
    for contract in (
        "Only the owner declares a change trivial",
        "this creates one NEW channel",
        "supervisor posts consume the same entry cap",
        "seat-declared evidence",
        "isolation remains advisory",
        "--verification-capable --result-schema-version 3",
        "historical verdict remains in the append-only record",
        "fresh correction slug",
        "Enter keeps A + B; choose a number to change; cancel stops",
        "--preparation-revision <exact preparation_revision>",
        "--confirmed-budget <selected seat_turn_ceiling>,<selected nested_launch_ceiling>",
        "sequence N of M",
        "no prior call authorization carries forward",
        "Every new product channel",
        "uses cap 12",
    ):
        assert contract in skill
    assert "verified by the schema" not in skill.lower()
    assert "cap 5" not in skill.lower()


def test_public_docs_name_upgrade_compatibility_and_safe_pruning() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    combined = readme + "\n" + changelog
    for phrase in (
        "result schema v3",
        "legacy-absent",
        "seat-declared",
        ".debate/runtime/<channel>/",
        "--prune --yes",
        "invocation `home/build/tmp`",
    ):
        assert phrase in combined
    # The shipped product default is schema v3 for bundled seats, and a custom
    # file adapter may declare v2 or v3; each public doc must state BOTH rules on
    # its own — a combined check let the CHANGELOG drift to v2, and an unqualified
    # universal v3 claim contradicted the (2, 3) admission logic (release-gate
    # findings, 2026-08-27).
    for document in (readme, changelog):
        lowered = document.lower()
        assert "result schema v3" in lowered
        assert "from a bundled seat" in lowered
        assert "v2 or v3" in lowered
        assert "schema v2 with" not in lowered
    assert "hostile-code safe" not in combined.lower()


def test_public_docs_pin_host_specific_onboarding_timing() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    contract = (REPO / "hooks" / "HOOK-CONTRACT.md").read_text(encoding="utf-8")

    assert "unready project opens in Claude Code" in readme
    assert "Codex 0.149.1 keeps prompt-free startup silent" in readme
    assert "stops that turn before inference" in readme
    assert "does not send\nor replay the stopped prompt" in readme
    assert "On your next launch in a project" not in readme
    assert "first submitted\n  turn" in changelog
    assert "zero first-turn network requests" in contract
    assert "malformed/broken-hook\n  error paths" in contract
