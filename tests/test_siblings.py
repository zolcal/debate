"""Slice C1: wrapper-sibling detection -- zero model calls, zero writes.

`scan_siblings` looks for OTHER wrapper binaries next to a vendor's already-
resolved wrapper, using each catalog entry's `sibling_pattern`. It never
touches a bare CLI (claude, kimi) and never reads a candidate's contents.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from debate import seats


def _make_executable(path: Path) -> None:
    path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    path.chmod(0o755)


def _which_from(mapping: dict[str, str]) -> Callable[[str], str | None]:
    def which(name: str) -> str | None:
        return mapping.get(name)
    return which


def test_sibling_found_next_to_resolved_binary(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    flash = bin_dir / "deepseek-flash-agent"
    pro = bin_dir / "deepseek-pro-agent"
    _make_executable(flash)
    _make_executable(pro)
    candidates = seats.scan_siblings(
        which=_which_from({"deepseek-flash-agent": str(flash)}),
        path_entries=lambda: [str(bin_dir)],
    )
    assert len(candidates) == 1
    row = candidates[0]
    assert row.vendor == "deepseek"
    assert row.binary_name == "deepseek-pro-agent"
    assert row.binary_path == str(pro)
    assert row.seat_id == "deepseek/wrapper:deepseek-pro-agent"


def test_sibling_not_found_when_vendor_binary_absent(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pro = bin_dir / "deepseek-pro-agent"
    _make_executable(pro)
    candidates = seats.scan_siblings(
        which=_which_from({}),  # deepseek-flash-agent does not resolve
        path_entries=lambda: [str(bin_dir)],
    )
    assert candidates == []


def test_catalogued_binary_is_never_its_own_sibling(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    flash = bin_dir / "deepseek-flash-agent"
    _make_executable(flash)
    candidates = seats.scan_siblings(
        which=_which_from({"deepseek-flash-agent": str(flash)}),
        path_entries=lambda: [str(bin_dir)],
    )
    assert candidates == []


def test_non_matching_names_never_surface(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    flash = bin_dir / "deepseek-flash-agent"
    _make_executable(flash)
    for name in ("deepseek-tool", "other-agent", "deepseekx"):
        _make_executable(bin_dir / name)
    candidates = seats.scan_siblings(
        which=_which_from({"deepseek-flash-agent": str(flash)}),
        path_entries=lambda: [str(bin_dir)],
    )
    assert candidates == []


def test_claude_and_kimi_never_scan(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    claude = bin_dir / "claude"
    kimi = bin_dir / "kimi"
    _make_executable(claude)
    _make_executable(kimi)
    _make_executable(bin_dir / "claude-foo-agent")
    _make_executable(bin_dir / "kimi-foo-agent")
    candidates = seats.scan_siblings(
        which=_which_from({"claude": str(claude), "kimi": str(kimi)}),
        path_entries=lambda: [str(bin_dir)],
    )
    assert candidates == []


def test_non_executable_file_is_ignored(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    flash = bin_dir / "deepseek-flash-agent"
    _make_executable(flash)
    stray = bin_dir / "deepseek-stray-agent"
    stray.write_text("not executable", encoding="utf-8")  # no chmod +x
    candidates = seats.scan_siblings(
        which=_which_from({"deepseek-flash-agent": str(flash)}),
        path_entries=lambda: [str(bin_dir)],
    )
    assert candidates == []


def test_rows_sanitized_and_sorted(tmp_path: Path) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    codex = bin_dir / "codex-agent"
    deepseek_flash = bin_dir / "deepseek-flash-agent"
    codex_sibling = bin_dir / "codex-two-agent"
    deepseek_sibling = bin_dir / "deepseek-pro-agent"
    for path in (codex, deepseek_flash, codex_sibling, deepseek_sibling):
        _make_executable(path)
    candidates = seats.scan_siblings(
        which=_which_from({
            "codex-agent": str(codex),
            "deepseek-flash-agent": str(deepseek_flash),
        }),
        path_entries=lambda: [str(bin_dir)],
    )
    seat_ids = [c.seat_id for c in candidates]
    assert seat_ids == sorted(seat_ids)
    assert seat_ids == [
        "codex/wrapper:codex-two-agent",
        "deepseek/wrapper:deepseek-pro-agent",
    ]


def test_default_path_entries_uses_os_environ_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    flash = bin_dir / "deepseek-flash-agent"
    pro = bin_dir / "deepseek-pro-agent"
    _make_executable(flash)
    _make_executable(pro)
    monkeypatch.setenv("PATH", str(bin_dir))
    candidates = seats.scan_siblings(which=_which_from({"deepseek-flash-agent": str(flash)}))
    assert [c.binary_name for c in candidates] == ["deepseek-pro-agent"]
