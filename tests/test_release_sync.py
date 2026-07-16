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
