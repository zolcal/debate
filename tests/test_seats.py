"""Slice 1: the seat catalog and the host registry.

The catalog is curated data (one entry per vendor); the registry is machine
state at ~/.config/debate/seats.json. Discovery merges, never clobbers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pytest

from debate import channel, seats
from debate.seat_catalog import CATALOG


# --- catalog shape: statically enforced law ---------------------------------


def test_catalog_entries_are_complete() -> None:
    assert CATALOG
    vendors = [entry.vendor for entry in CATALOG]
    assert len(vendors) == len(set(vendors)), "vendor ids must be unique"
    for entry in CATALOG:
        assert entry.vendor
        assert entry.binaries
        assert entry.submodels
        assert any("{prompt}" in part for part in entry.invocation), entry.vendor
        assert any("{binary}" in part for part in entry.invocation), entry.vendor


def test_catalog_effort_argv_pairs_with_known_efforts() -> None:
    for entry in CATALOG:
        if entry.effort_argv:
            assert any("{effort}" in part for part in entry.effort_argv), entry.vendor
            assert entry.known_efforts, (
                f"{entry.vendor}: an effort flag with no known tiers is a catalog bug"
            )


def test_catalog_single_seat_rule() -> None:
    for entry in CATALOG:
        if entry.submodel_argv:
            assert any("{submodel}" in part for part in entry.submodel_argv), entry.vendor
        else:
            assert len(entry.submodels) == 1, (
                f"{entry.vendor}: a binary that cannot select a submodel via argv "
                "contributes exactly ONE seat named by its verified pin"
            )


# --- registry load/save -----------------------------------------------------


def _registry_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(path))
    return path


def test_load_registry_missing_file_is_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    assert reg.seats == {}
    assert reg.last_pair == {}


def test_registry_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg.seats["glm/glm-5.3"] = seats.Seat(
        seat_id="glm/glm-5.3", vendor="glm", submodel="glm-5.3", effort=None,
        commands=[["/usr/bin/glm-agent", "{prompt}"]], source="catalog",
        present=True, smoke=None,
    )
    seats.save_registry(reg)
    assert path.is_file()
    again = seats.load_registry()
    assert again.seats["glm/glm-5.3"].commands == [["/usr/bin/glm-agent", "{prompt}"]]
    assert again.seats["glm/glm-5.3"].effort is None


def test_load_registry_refuses_non_object(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = _registry_env(tmp_path, monkeypatch)
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(channel.ChannelError, match="refused"):
        seats.load_registry()


def test_save_registry_screens_credentials(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg.seats["x/y"] = seats.Seat(
        seat_id="x/y", vendor="x", submodel="y", effort=None,
        commands=[["/bin/tool", "--api-key", "sk-abcdefghijklmnopqr"]],
        source="manual", present=True, smoke=None,
    )
    with pytest.raises(channel.ChannelError, match="credential"):
        seats.save_registry(reg)


# --- discovery: catalog x PATH, merge never clobber -------------------------


def _which_from(mapping: dict[str, str]) -> Callable[[str], str | None]:
    def which(name: str) -> str | None:
        return mapping.get(name)
    return which


def test_discover_selectable_entry_seeds_one_seat_per_submodel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, diff = seats.discover(
        reg, which=_which_from({"kimi": "/opt/nvm/kimi"}), now="2026-08-16T00:00:00+00:00"
    )
    kimi_seats = [s for s in reg.seats.values() if s.vendor == "kimi"]
    assert len(kimi_seats) >= 2, "a submodel-selectable binary seeds one seat per submodel"
    for seat in kimi_seats:
        assert seat.effort is None
        assert len(seat.commands) == 1
        argv = seat.commands[0]
        assert argv[0] == "/opt/nvm/kimi"
        assert "{prompt}" in argv
        assert seat.submodel in argv, "the pipe must actually select what the id claims"
    assert any("kimi" in line for line in diff)


def test_discover_pin_internal_entry_seeds_exactly_one_seat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(
        reg, which=_which_from({"glm-agent": "/home/u/.local/bin/glm-agent"}),
        now="2026-08-16T00:00:00+00:00",
    )
    glm_seats = [s for s in reg.seats.values() if s.vendor == "glm"]
    assert len(glm_seats) == 1, "single-seat rule: no identical-argv siblings"
    assert glm_seats[0].seat_id == "glm/glm-5.3"


def test_rediscover_marks_absent_never_deletes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(
        reg, which=_which_from({"glm-agent": "/x/glm-agent"}), now="t1"
    )
    reg.seats["custom/one"] = seats.Seat(
        seat_id="custom/one", vendor="custom", submodel="one", effort=None,
        commands=[["/x/custom", "{prompt}"]], source="manual", present=True, smoke=None,
    )
    reg, diff = seats.discover(reg, which=_which_from({}), now="t2")
    assert reg.seats["glm/glm-5.3"].present is False, "vanished binaries are marked absent"
    assert "glm/glm-5.3" in reg.seats, "never deleted"
    assert reg.seats["custom/one"].present is True, "manual entries untouched"
    assert any("absent" in line for line in diff)


def test_discover_is_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    mapping = {"glm-agent": "/x/glm-agent"}
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from(mapping), now="t1")
    first = {sid: seat.commands for sid, seat in reg.seats.items()}
    reg, diff = seats.discover(reg, which=_which_from(mapping), now="t2")
    assert {sid: seat.commands for sid, seat in reg.seats.items()} == first
    assert not any("+" in line for line in diff) or diff == []


# --- CLI: seats runs without --root and without channel discovery -----------


def test_cli_seats_discover_and_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    # A CWD holding a multi-channel root must be irrelevant: the guard treats
    # `seats` like `init` (review fold, B2).
    root = tmp_path / "collab"
    root.mkdir()
    (root / "a-11111.debate.json").write_text("{}", encoding="utf-8")
    (root / "b-22222.debate.json").write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert main(["seats", "discover"]) == 0
    out = capsys.readouterr().out
    assert "seats" in out or "discover" in out or "+" in out

    assert main(["seats", "list"]) == 0
    out = capsys.readouterr().out
    assert "present" in out or "seat" in out

    assert main(["seats", "list", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload, dict)


def test_cli_seats_output_is_ascii(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    main(["seats", "discover"])
    main(["seats", "list"])
    out = capsys.readouterr().out
    out.encode("ascii")


# --- Slice 2: freshness (H1 semantics), upgrade trigger, add/remove, smoke --


def _real_tool(tmp_path: Path) -> str:
    tool = tmp_path / "glm-agent"
    tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    tool.chmod(0o755)
    return str(tool)


def test_check_clean_registry_is_empty_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"glm-agent": _real_tool(tmp_path)}), now="t1")
    reg.seats["glm/glm-5.3"].smoke = seats.SmokeStatus(at="2026-08-16T00:00:00+00:00", result="pass")
    report = seats.check(reg, which=_which_from({}), now="2026-08-16T01:00:00+00:00")
    assert report.fails == [] and report.warns == [] and report.infos == []


def test_check_missing_binary_is_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"glm-agent": "/x/glm-agent"}), now="t1")
    report = seats.check(reg, which=_which_from({}), now="2026-08-16T01:00:00+00:00")
    assert any("glm/glm-5.3" in line for line in report.fails)


def test_check_failed_smoke_is_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"glm-agent": _real_tool(tmp_path)}), now="t1")
    reg.seats["glm/glm-5.3"].smoke = seats.SmokeStatus(at="2026-08-16T00:00:00+00:00", result="fail")
    report = seats.check(reg, which=_which_from({}), now="2026-08-16T01:00:00+00:00")
    assert any("smoke" in line for line in report.fails)


def test_check_never_smoked_is_info_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A fresh post-discover registry MUST exit clean: smoke is opt-in (ruling 1)."""
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"glm-agent": _real_tool(tmp_path)}), now="t1")
    report = seats.check(reg, which=_which_from({}), now="2026-08-16T01:00:00+00:00")
    assert report.fails == []
    assert report.warns == []
    assert any("never smoked" in line for line in report.infos)


def test_check_stale_smoke_is_warn(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"glm-agent": _real_tool(tmp_path)}), now="t1")
    reg.seats["glm/glm-5.3"].smoke = seats.SmokeStatus(at="2026-07-01T00:00:00+00:00", result="pass")
    report = seats.check(reg, which=_which_from({}), now="2026-08-16T00:00:00+00:00")
    assert report.fails == []
    assert any("stale" in line for line in report.warns)


def test_ensure_current_same_version_is_noop(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from debate import __version__

    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({}), now="t1")
    assert reg.tool_version == __version__
    reg, diff = seats.ensure_current(reg, which=_which_from({}), now="t2")
    assert diff == []
    assert reg.discovered_at == "t1", "no re-scan when versions match"


def test_ensure_current_version_mismatch_rescans(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg.tool_version = "0.0.1"
    reg, diff = seats.ensure_current(reg, which=_which_from({"glm-agent": "/x/glm-agent"}), now="t2")
    from debate import __version__

    assert reg.tool_version == __version__
    assert any("glm" in line for line in diff)


def test_add_manual_seat_and_append_endpoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    reg = seats.load_registry()
    seats.add_seat(reg, "custom/one", f"{tool} {{prompt}}", which=_which_from({str(tool): str(tool)}))
    assert reg.seats["custom/one"].source == "manual"
    assert reg.seats["custom/one"].commands == [[str(tool), "{prompt}"]]
    # a second serving on an EXISTING manual seat appends an endpoint option
    seats.add_seat(reg, "custom/one", f"{tool} --alt {{prompt}}", which=_which_from({str(tool): str(tool)}))
    assert len(reg.seats["custom/one"].commands) == 2, "append, selection stays first-listed"


def test_add_effort_derivation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"claude": "/x/claude"}), now="t1")
    seats.add_effort_seat(reg, "claude/opus@high")
    derived = reg.seats["claude/opus@high"]
    assert derived.effort == "high"
    assert derived.commands[0][-2:] == ["--effort", "high"]
    with pytest.raises(channel.ChannelError, match="known_efforts"):
        seats.add_effort_seat(reg, "claude/opus@turbo")
    with pytest.raises(channel.ChannelError, match="refused"):
        seats.add_effort_seat(reg, "glm/glm-5.3@high")  # effort not argv-reachable
    with pytest.raises(channel.ChannelError, match="refused"):
        seats.add_effort_seat(reg, "claude/nope@high")  # base seat missing


def test_remove_manual_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"glm-agent": "/x/glm-agent"}), now="t1")
    reg.seats["custom/one"] = seats.Seat(
        seat_id="custom/one", vendor="custom", submodel="one", effort=None,
        commands=[["/x/c", "{prompt}"]], source="manual", present=True, smoke=None,
    )
    seats.remove_seat(reg, "custom/one")
    assert "custom/one" not in reg.seats
    with pytest.raises(channel.ChannelError, match="absent"):
        seats.remove_seat(reg, "glm/glm-5.3")


def test_smoke_seat_records_result(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The smoke reuses setup's scratch-channel machinery with the seat's
    FIRST-LISTED argv; the result lands in the registry either way."""
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg.seats["fake/one"] = seats.Seat(
        seat_id="fake/one", vendor="fake", submodel="one", effort=None,
        commands=[["/bin/false", "{prompt}"]], source="manual", present=True, smoke=None,
    )
    result = seats.smoke_seat(
        reg, "fake/one", scratch_base=tmp_path / "scratch",
        now="2026-08-16T02:00:00+00:00", assume_yes=True,
    )
    assert result == "fail"
    assert reg.seats["fake/one"].smoke is not None
    assert reg.seats["fake/one"].smoke.result == "fail"
    assert reg.seats["fake/one"].smoke.at == "2026-08-16T02:00:00+00:00"


def test_cli_seats_check_exit_codes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    main(["seats", "discover"])
    capsys.readouterr()
    # Fresh post-discover registry: never-smoked is INFO only -> exit 0 (H1).
    assert main(["seats", "check"]) == 0
    out = capsys.readouterr().out
    assert "re-discovery" in out or "discover" in out
    # A seat whose binary is gone -> FAIL -> exit 3.
    reg = seats.load_registry()
    reg.seats["gone/one"] = seats.Seat(
        seat_id="gone/one", vendor="gone", submodel="one", effort=None,
        commands=[["/nonexistent-tool-xyz", "{prompt}"]], source="manual",
        present=True, smoke=None,
    )
    seats.save_registry(reg)
    assert main(["seats", "check"]) == 3
    out = capsys.readouterr().out
    assert "FAIL" in out


def test_cli_seats_add_and_remove(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    assert main(["seats", "add", "custom/one", "--command", f"{tool} {{prompt}}"]) == 0
    reg = seats.load_registry()
    assert "custom/one" in reg.seats
    assert main(["seats", "remove", "custom/one"]) == 0
    assert "custom/one" not in seats.load_registry().seats
