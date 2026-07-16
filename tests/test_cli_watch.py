"""CLI watch: arg validation, exit-code pass-through, KeyboardInterrupt mapping."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main


def _setup(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    cfg = tmp_path / "watcher.json"
    cfg.write_text(json.dumps({"state_path": str(tmp_path / "state.json")}), encoding="utf-8")
    return root, cfg


@pytest.mark.parametrize("flag", ["--interval", "--max-ticks"])
@pytest.mark.parametrize("value", ["0", "-1"])
def test_watch_rejects_nonpositive(tmp_path: Path, flag: str, value: str) -> None:
    root, cfg = _setup(tmp_path)
    with pytest.raises(SystemExit) as excinfo:
        main(["watch", "--root", str(root), "--config", str(cfg), flag, value])
    assert excinfo.value.code == 2


@pytest.mark.parametrize("code", [0, 4, 5, 6])
def test_watch_passes_exit_codes_through(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, code: int) -> None:
    import debate.__main__ as cli

    root, cfg = _setup(tmp_path)
    monkeypatch.setattr(cli, "watch", lambda *a, **k: code)
    assert main(["watch", "--root", str(root), "--config", str(cfg)]) == code


def test_watch_maps_keyboard_interrupt_to_130(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import debate.__main__ as cli

    root, cfg = _setup(tmp_path)

    def raising_watch(*args: object, **kwargs: object) -> int:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, "watch", raising_watch)
    assert main(["watch", "--root", str(root), "--config", str(cfg)]) == 130
