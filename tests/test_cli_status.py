"""CLI status: parked/turnless/unknown lines, JSON age, --stale-after semantics."""
from __future__ import annotations

from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main


@pytest.fixture()
def parked_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    return root


def _turnless_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-old", "x")
    channel.post(root, "alpha", "close", "t-old", "closing")
    channel.post(root, "owner", "verdict", "t-new", "supervisor opener")
    return root


def test_status_prints_parked_age_and_json_field(parked_channel: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status", "--root", str(parked_channel)]) == 0
    out = capsys.readouterr().out
    assert '"turn_age_seconds":' in out
    assert "turn 'alpha' parked 0h00m on 't-one' (seq 1)" in out


def test_stale_after_boundary(parked_channel: Path) -> None:
    assert main(["status", "--root", str(parked_channel), "--stale-after", "0"]) == 3   # age >= 0 always
    assert main(["status", "--root", str(parked_channel), "--stale-after", "3600"]) == 0


def test_stale_after_rejects_negative(parked_channel: Path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["status", "--root", str(parked_channel), "--stale-after", "-1"])
    assert excinfo.value.code == 2


def test_status_turnless_thread_supervisor_required(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _turnless_channel(tmp_path)
    assert main(["status", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "open with no turn" in out and "supervisor close required" in out
    assert '"turn_age_seconds"' not in out


def test_status_unknown_age_line_and_exit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the CLI's unknown-age contract: the line, the omitted JSON field, and exit 3."""
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "x")
    monkeypatch.setattr(channel, "turn_parked_since", lambda r, now: (None, 1))
    assert main(["status", "--root", str(root), "--stale-after", "999999"]) == 3
    # and without --stale-after: exit 0, unknown-age line printed, no JSON age field
    assert main(["status", "--root", str(root)]) == 0


def test_stale_after_trips_on_turnless_thread_at_any_threshold(tmp_path: Path) -> None:
    root = _turnless_channel(tmp_path)
    assert main(["status", "--root", str(root), "--stale-after", "999999"]) == 3  # unconditionally stuck
