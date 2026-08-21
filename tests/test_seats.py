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
    # round-7 fold: an absent seat is a MISSING BINARY -> FAIL, with the
    # removal remedy named in the line
    report = seats.check(reg, which=_which_from({}), now="t3")
    assert any("glm/glm-5.3" in line and "remove" in line for line in report.fails)
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
    with pytest.raises(channel.ChannelError, match="PRESENT"):
        seats.remove_seat(reg, "glm/glm-5.3")
    # round-7 fold: an ABSENT catalog seat may be removed as cleanup
    reg.seats["glm/glm-5.3"].present = False
    seats.remove_seat(reg, "glm/glm-5.3")
    assert "glm/glm-5.3" not in reg.seats


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


def test_discover_prefers_first_listed_binary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Slice 1: 'wrapper binary preferred over bare CLI when both resolve' --
    binaries are probed in catalog order, first hit wins."""
    from debate import seat_catalog

    entry = seat_catalog.CatalogEntry(
        vendor="dual", binaries=("dual-agent", "dual"), submodels=("one",),
        known_efforts=(), invocation=("{binary}", "{prompt}"),
        submodel_argv=(), effort_argv=(), notes="synthetic two-binary entry",
    )
    monkeypatch.setattr(seats, "CATALOG", (entry,))
    _registry_env(tmp_path, monkeypatch)
    wrapper = tmp_path / "dual-agent"
    bare = tmp_path / "dual"
    for tool in (wrapper, bare):
        tool.write_text("#!/bin/sh\n", encoding="utf-8")
        tool.chmod(0o755)
    reg = seats.load_registry()
    reg, _ = seats.discover(
        reg, which=_which_from({"dual-agent": str(wrapper), "dual": str(bare)}), now="t"
    )
    assert reg.seats["dual/one"].commands[0][0] == str(wrapper)


def test_derived_source_taxonomy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Round-8 fold: derived @effort entries carry source='derived' and are
    the ONLY entries the refresh may touch; manual means operator-authored
    and is absolutely untouched (D2 literal)."""
    _registry_env(tmp_path, monkeypatch)
    old = tmp_path / "claude"
    old.write_text("#!/bin/sh\n", encoding="utf-8")
    old.chmod(0o755)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"claude": str(old)}), now="t0")
    seats.add_effort_seat(reg, "claude/opus@high")
    assert reg.seats["claude/opus@high"].source == "derived"
    base = list(reg.seats["claude/opus"].commands[0])
    # an operator-authored seat that HAPPENS to have the exact derived shape
    reg.seats["claude/opus@low"] = seats.Seat(
        "claude/opus@low", "claude", "opus", "low",
        [base + ["--effort", "low"]], "manual", True, None,
    )
    new = tmp_path / "moved" / "claude"
    new.parent.mkdir()
    new.write_text("#!/bin/sh\n", encoding="utf-8")
    new.chmod(0o755)
    reg, _ = seats.discover(reg, which=_which_from({"claude": str(new)}), now="t1")
    assert reg.seats["claude/opus@high"].commands[0][0] == str(new), "derived refreshes"
    assert reg.seats["claude/opus@low"].commands[0][0] == str(old), (
        "manual is NEVER touched, even in the exact derived shape"
    )
    # a derived seat is recreatable, so removal is allowed
    seats.remove_seat(reg, "claude/opus@high")
    assert "claude/opus@high" not in reg.seats


# --- Slice C1: catalog isolation/config-home/capability data, declared -----
# manual-seat flags, wrapper sibling scan -------------------------------------


def test_old_registry_without_new_fields_loads_defaults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = _registry_env(tmp_path, monkeypatch)
    path.write_text(json.dumps({
        "registry_version": 1,
        "tool_version": "0.7.0",
        "discovered_at": "t0",
        "seats": {
            "glm/glm-5.3": {
                "vendor": "glm",
                "submodel": "glm-5.3",
                "effort": None,
                "commands": [["/usr/bin/glm-agent", "{prompt}"]],
                "source": "catalog",
                "present": True,
                "smoke": None,
                "cost_mode": "unknown",
            }
        },
        "last_pair": {},
    }), encoding="utf-8")
    reg = seats.load_registry()
    seat = reg.seats["glm/glm-5.3"]
    assert seat.capability_class is None
    assert seat.isolation_argv == []
    assert seat.no_persistence_argv == []
    assert seat.config_home is None


def test_registry_round_trip_preserves_new_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg.seats["claude/opus"] = seats.Seat(
        seat_id="claude/opus", vendor="claude", submodel="opus", effort=None,
        commands=[["/usr/bin/claude", "-p", "{prompt}", "--model", "opus"]],
        source="catalog", present=True, smoke=None,
        capability_class="frontier",
        isolation_argv=["--safe-mode", "--strict-mcp-config"],
        no_persistence_argv=["--no-session-persistence"],
        config_home="CLAUDE_CONFIG_DIR=.claude",
    )
    seats.save_registry(reg)
    again = seats.load_registry()
    seat = again.seats["claude/opus"]
    assert seat.capability_class == "frontier"
    assert seat.isolation_argv == ["--safe-mode", "--strict-mcp-config"]
    assert seat.no_persistence_argv == ["--no-session-persistence"]
    assert seat.config_home == "CLAUDE_CONFIG_DIR=.claude"


def test_seat_from_raw_refuses_bad_capability_class(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(channel.ChannelError, match="refused"):
        seats._seat_from_raw("x/y", {
            "vendor": "x", "submodel": "y", "effort": None,
            "commands": [["/bin/tool", "{prompt}"]],
            "source": "manual", "present": True, "smoke": None,
            "capability_class": "medium",
        })


def test_seat_from_raw_refuses_a_stored_config_home_of_the_wrong_shape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Shape only at load: `VAR=dir`, both sides non-empty. The variable name
    and folder rules need the operator's real home and run at declaration and
    at admission instead (final review wave, I1)."""
    with pytest.raises(channel.ChannelError, match="refused"):
        seats._seat_from_raw("x/y", {
            "vendor": "x", "submodel": "y", "effort": None,
            "commands": [["/bin/tool", "{prompt}"]],
            "source": "manual", "present": True, "smoke": None,
            "config_home": "noequalssign",
        })
    loaded = seats._seat_from_raw("x/y", {
        "vendor": "x", "submodel": "y", "effort": None,
        "commands": [["/bin/tool", "{prompt}"]],
        "source": "manual", "present": True, "smoke": None,
        "config_home": "1ABC=.m",
    })
    assert loaded.config_home == "1ABC=.m"


def test_add_seat_refuses_colon_in_model_part(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    reg = seats.load_registry()
    with pytest.raises(channel.ChannelError, match="must not contain ':'"):
        seats.add_seat(
            reg, "custom/wrapper:mytool", f"{tool} {{prompt}}",
            which=_which_from({str(tool): str(tool)}),
        )


def test_add_seat_stores_declarations(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    reg = seats.load_registry()
    seats.add_seat(
        reg, "custom/one", f"{tool} {{prompt}}",
        which=_which_from({str(tool): str(tool)}),
        capability_class="frontier",
        isolation_argv=["--iso"],
        no_persistence_argv=["--no-persist"],
        config_home="MYTOOL_HOME=.mytool",
        home=home,
    )
    seat = reg.seats["custom/one"]
    assert seat.capability_class == "frontier"
    assert seat.isolation_argv == ["--iso"]
    assert seat.no_persistence_argv == ["--no-persist"]
    assert seat.config_home == "MYTOOL_HOME=.mytool"


def test_add_seat_append_path_applies_declarations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    reg = seats.load_registry()
    seats.add_seat(reg, "custom/one", f"{tool} {{prompt}}", which=_which_from({str(tool): str(tool)}))
    assert reg.seats["custom/one"].capability_class is None
    # None/empty on the append path leaves the stored value untouched.
    seats.add_seat(
        reg, "custom/one", f"{tool} --alt {{prompt}}",
        which=_which_from({str(tool): str(tool)}),
    )
    assert reg.seats["custom/one"].capability_class is None
    assert reg.seats["custom/one"].isolation_argv == []
    # A non-empty declaration on the append path APPLIES.
    seats.add_seat(
        reg, "custom/one", f"{tool} --alt2 {{prompt}}",
        which=_which_from({str(tool): str(tool)}),
        capability_class="light",
        isolation_argv=["--iso"],
        no_persistence_argv=["--no-persist"],
        config_home="MYTOOL_HOME=.mytool",
        home=home,
    )
    seat = reg.seats["custom/one"]
    assert seat.capability_class == "light"
    assert seat.isolation_argv == ["--iso"]
    assert seat.no_persistence_argv == ["--no-persist"]
    assert seat.config_home == "MYTOOL_HOME=.mytool"


def test_discover_fills_catalog_seat_declarations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(
        reg,
        which=_which_from({
            "claude": "/x/claude",
            "kimi": "/x/kimi",
            "deepseek-flash-agent": "/x/deepseek-flash-agent",
        }),
        now="t1",
    )
    assert reg.seats["claude/haiku"].capability_class == "light"
    assert reg.seats["claude/opus"].capability_class == "frontier"
    assert reg.seats["kimi/kimi-code/kimi-for-coding"].capability_class is None
    assert reg.seats["deepseek/deepseek-v4-flash"].capability_class == "light"

    claude_opus = reg.seats["claude/opus"]
    assert claude_opus.isolation_argv == [
        "--safe-mode", "--setting-sources", "", "--strict-mcp-config",
        "--disable-slash-commands",
    ]
    assert claude_opus.no_persistence_argv == ["--no-session-persistence"]
    assert claude_opus.config_home == "CLAUDE_CONFIG_DIR=.claude"

    deepseek = reg.seats["deepseek/deepseek-v4-flash"]
    assert deepseek.isolation_argv == []
    assert deepseek.no_persistence_argv == []
    assert deepseek.config_home is None


def test_add_effort_seat_inherits_declarations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg, _ = seats.discover(reg, which=_which_from({"claude": "/x/claude"}), now="t1")
    seats.add_effort_seat(reg, "claude/opus@high")
    derived = reg.seats["claude/opus@high"]
    base = reg.seats["claude/opus"]
    assert derived.capability_class == base.capability_class
    assert derived.isolation_argv == base.isolation_argv
    assert derived.no_persistence_argv == base.no_persistence_argv
    assert derived.config_home == base.config_home


# --- validate_config_home: the exact matrix ---------------------------------


@pytest.mark.parametrize("value", [
    "HOME=.config",
    "XDG_CONFIG_HOME=x",
    "TMPDIR=t",
    "PATH=p",
    "GIT_DIR=g",
    "PYTEST_DISABLE_PLUGIN_AUTOLOAD=x",
    "DEBATE_BRIDGE_REAL_HOME=x",
    "mytool=.m",
    "1ABC=.m",
    "A-B=.m",
    "noequalssign",
    "MYTOOL_HOME=/etc",
    "MYTOOL_HOME=../x",
    "MYTOOL_HOME=",
])
def test_validate_config_home_refuses(tmp_path: Path, value: str) -> None:
    home = tmp_path / "home"
    home.mkdir()
    with pytest.raises(channel.ChannelError, match="refused"):
        seats.validate_config_home(value, home=home)


@pytest.mark.parametrize("value,expected_var", [
    ("CLAUDE_CONFIG_DIR=.claude", "CLAUDE_CONFIG_DIR"),
    ("CODEX_HOME=.codex", "CODEX_HOME"),
    ("MYTOOL_HOME=.mytool", "MYTOOL_HOME"),
    ("MYTOOL_HOME=.config/mytool", "MYTOOL_HOME"),
])
def test_validate_config_home_accepts(tmp_path: Path, value: str, expected_var: str) -> None:
    home = tmp_path / "home"
    home.mkdir()
    var, resolved = seats.validate_config_home(value, home=home)
    assert var == expected_var
    assert resolved.is_relative_to(home.resolve())
    assert resolved != home.resolve()


def test_cli_seats_add_with_new_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    assert main([
        "seats", "add", "custom/one",
        "--command", f"{tool} {{prompt}}",
        "--capability-class", "frontier",
        "--isolation-argv", "--iso --flag",
        "--no-persistence-argv=--no-persist",
        "--config-home", "MYTOOL_HOME=.mytool",
    ]) == 0
    reg = seats.load_registry()
    seat = reg.seats["custom/one"]
    assert seat.capability_class == "frontier"
    assert seat.isolation_argv == ["--iso", "--flag"]
    assert seat.no_persistence_argv == ["--no-persist"]
    assert seat.config_home == "MYTOOL_HOME=.mytool"


def test_cli_seats_add_refuses_bad_config_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    tool = tmp_path / "mytool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    rc = main([
        "seats", "add", "custom/one",
        "--command", f"{tool} {{prompt}}",
        "--config-home", "HOME=.config",
    ])
    assert rc == 1
    message = capsys.readouterr().err.lower()
    assert "refused" in message
    assert "bridge" not in message
    assert "brokered" not in message
    assert "placeholder" not in message


def test_cli_seats_remove_help_names_every_removable_class(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The help text must match `remove_seat`'s actual law.

    It said "remove a MANUAL seat" while the law removes manual, derived and
    ABSENT-catalog seats and refuses only a PRESENT catalog one, so an
    operator reading `--help` would think a stranded derivation was stuck.
    """
    from debate.__main__ import main

    with pytest.raises(SystemExit):
        main(["seats", "remove", "--help"])
    help_text = capsys.readouterr().out.lower()
    assert "manual" in help_text
    assert "derived" in help_text
    assert "absent" in help_text
    assert "present catalog" in help_text


# --- final review wave C1: derived seats inherit the catalog's declarations --


def _v07_shaped_registry(path: Path) -> None:
    """A registry written by v0.7: a catalog seat and its `@effort` derivation,
    neither carrying the fields v0.8 added, plus a manual seat of the same shape.
    """
    row = {
        "vendor": "claude",
        "submodel": "opus",
        "source": "catalog",
        "present": True,
        "smoke": None,
        "cost_mode": "unknown",
    }
    path.write_text(json.dumps({
        "registry_version": 1,
        "tool_version": "0.7.0",
        "discovered_at": "t0",
        "seats": {
            "claude/opus": {
                **row,
                "effort": None,
                "commands": [["/x/claude", "-p", "{prompt}", "--model", "opus"]],
            },
            "claude/opus@high": {
                **row,
                "source": "derived",
                "effort": "high",
                "commands": [[
                    "/x/claude", "-p", "{prompt}", "--model", "opus", "--effort", "high",
                ]],
            },
            "mine/own": {
                "vendor": "mine",
                "submodel": "own",
                "effort": None,
                "commands": [["/x/mine", "{prompt}"]],
                "source": "manual",
                "present": True,
                "smoke": None,
                "cost_mode": "unknown",
            },
        },
        "last_pair": {},
    }), encoding="utf-8")


def test_discover_gives_a_derived_seat_its_base_seat_declarations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A v0.7 registry upgraded in place: the derived `@effort` seat must pick
    up the catalog's isolation flags even though its base argv did not move."""
    path = _registry_env(tmp_path, monkeypatch)
    _v07_shaped_registry(path)
    reg = seats.load_registry()
    reg, _diff = seats.discover(reg, which=_which_from({"claude": "/x/claude"}), now="t1")

    base = reg.seats["claude/opus"]
    derived = reg.seats["claude/opus@high"]
    assert base.isolation_argv == [
        "--safe-mode", "--setting-sources", "", "--strict-mcp-config",
        "--disable-slash-commands",
    ]
    assert derived.isolation_argv == base.isolation_argv
    assert derived.no_persistence_argv == base.no_persistence_argv == ["--no-session-persistence"]
    assert derived.config_home == base.config_home == "CLAUDE_CONFIG_DIR=.claude"
    assert derived.capability_class == base.capability_class == "frontier"
    # The base argv did not move, so the derived command is left exactly as it was.
    assert derived.commands[0] == [
        "/x/claude", "-p", "{prompt}", "--model", "opus", "--effort", "high",
    ]


def test_discover_never_touches_a_manual_seat_declaration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = _registry_env(tmp_path, monkeypatch)
    _v07_shaped_registry(path)
    reg = seats.load_registry()
    reg, _diff = seats.discover(reg, which=_which_from({"claude": "/x/claude"}), now="t1")
    manual = reg.seats["mine/own"]
    assert manual.isolation_argv == []
    assert manual.no_persistence_argv == []
    assert manual.config_home is None
    assert manual.capability_class is None


def test_a_refreshed_derived_seat_is_admissible(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from debate import opening

    path = _registry_env(tmp_path, monkeypatch)
    _v07_shaped_registry(path)
    reg = seats.load_registry()
    before = opening.admission_problem(reg.seats["claude/opus@high"], real_home=tmp_path)
    assert before is not None
    reg, _diff = seats.discover(reg, which=_which_from({"claude": "/x/claude"}), now="t1")
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    assert opening.admission_problem(reg.seats["claude/opus@high"], real_home=home) is None


@pytest.mark.parametrize("seat_id", ["claude/opus", "claude/opus@high"])
def test_a_flagless_catalogued_seat_is_told_to_refresh_not_to_declare(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, seat_id: str
) -> None:
    """A seat Debate itself catalogued cannot be missing flags the operator
    must supply -- the registry is simply out of date, and the refusal says so."""
    from debate import opening

    path = _registry_env(tmp_path, monkeypatch)
    _v07_shaped_registry(path)
    reg = seats.load_registry()
    problem = opening.admission_problem(reg.seats[seat_id], real_home=tmp_path)
    assert problem is not None
    assert "debate seats discover" in problem
    assert "--isolation-argv" not in problem


def test_a_flagless_manual_seat_is_told_to_declare_its_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from debate import opening

    path = _registry_env(tmp_path, monkeypatch)
    _v07_shaped_registry(path)
    reg = seats.load_registry()
    problem = opening.admission_problem(reg.seats["mine/own"], real_home=tmp_path)
    assert problem is not None
    assert "--isolation-argv" in problem
    assert "debate seats discover" not in problem


# --- final review wave I1: a stored config home is SHAPE-checked at load ----


def _registry_with_stored_config_home(path: Path, value: str) -> None:
    path.write_text(json.dumps({
        "registry_version": 1,
        "tool_version": "test",
        "discovered_at": "t0",
        "seats": {
            "mine/own": {
                "vendor": "mine",
                "submodel": "own",
                "effort": None,
                "commands": [["/x/mine", "{prompt}"]],
                "source": "manual",
                "present": True,
                "smoke": None,
                "cost_mode": "unknown",
                "isolation_argv": ["--offline"],
                "no_persistence_argv": ["--forget"],
                "config_home": value,
            }
        },
        "last_pair": {},
    }), encoding="utf-8")


def test_a_registry_holding_an_unusable_config_home_still_loads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One bad row must not brick every command that reads the registry: the
    full folder rule belongs at `seats add` and at admission, both of which
    check it against the operator's real home (final review wave, I1)."""
    path = _registry_env(tmp_path, monkeypatch)
    _registry_with_stored_config_home(path, "HOME=.config")
    reg = seats.load_registry()
    assert reg.seats["mine/own"].config_home == "HOME=.config"


def test_seats_list_still_works_with_an_unusable_config_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from debate.__main__ import main

    path = _registry_env(tmp_path, monkeypatch)
    _registry_with_stored_config_home(path, "HOME=.config")
    monkeypatch.chdir(tmp_path)
    assert main(["seats", "list"]) == 0
    assert "mine/own" in capsys.readouterr().out


def test_seats_remove_still_works_with_an_unusable_config_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from debate.__main__ import main

    path = _registry_env(tmp_path, monkeypatch)
    _registry_with_stored_config_home(path, "HOME=.config")
    monkeypatch.chdir(tmp_path)
    assert main(["seats", "remove", "mine/own"]) == 0
    assert "mine/own" not in seats.load_registry().seats


def test_admission_refuses_the_unusable_config_home_with_the_folder_rule(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from debate import opening

    path = _registry_env(tmp_path, monkeypatch)
    _registry_with_stored_config_home(path, "HOME=.config")
    reg = seats.load_registry()
    problem = opening.admission_problem(reg.seats["mine/own"], real_home=tmp_path)
    assert problem is not None
    assert "config-home" in problem


@pytest.mark.parametrize("value", ["noequalssign", "MYTOOL_HOME=", "=.mytool", "A=B=C"])
def test_a_stored_config_home_of_the_wrong_shape_still_refuses_at_load(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    """The SHAPE is all the loader can judge without the operator's real home,
    and a row that is not `VAR=dir` at all is unusable everywhere."""
    path = _registry_env(tmp_path, monkeypatch)
    _registry_with_stored_config_home(path, value)
    with pytest.raises(channel.ChannelError, match="refused"):
        seats.load_registry()
