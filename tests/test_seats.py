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


def test_smoke_composes_the_full_seat_recipe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Field finding F16: a bare-argv smoke under-equips the seat -- a
    headless claude authenticated, read the thread, and correctly refused to
    post, because the permission flags live in the layers the bridge composes
    for every managed turn. The smoke must run that same composition."""
    from debate import setup as setup_module

    _registry_env(tmp_path, monkeypatch)
    reg = seats.load_registry()
    reg.seats["fake/one"] = seats.Seat(
        seat_id="fake/one", vendor="fake", submodel="one", effort=None,
        commands=[["/bin/false", "{prompt}"]], source="manual", present=True,
        smoke=None,
    )
    seat = reg.seats["fake/one"]
    seat.isolation_argv = ["--iso"]
    seat.no_persistence_argv = ["--no-save"]
    seat.verification_argv = ["--verify"]
    captured: list[list[str] | None] = []

    def fake_smoke(
        spec: setup_module.SetupSpec, *,
        scratch_base: Path | None = None,
        emit: Callable[[str], None] = print,
    ) -> list[str]:
        captured.append(spec.commands["fake"])
        return []

    monkeypatch.setattr(setup_module, "smoke", fake_smoke)
    result = seats.smoke_seat(
        reg, "fake/one", scratch_base=tmp_path / "scratch",
        now="t", assume_yes=True,
    )
    assert result == "pass"
    assert captured == [[
        "/bin/false", "{prompt}", "--iso", "--no-save", "--verify",
    ]]


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
    # The catalog's canonical POSIX argv is the subject here; the Windows
    # sandbox pin (danger-full-access) has its own test below.
    monkeypatch.setattr(seats, "_is_windows", lambda: False)
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
    assert claude_opus.verification_argv == [
        "--permission-mode", "dontAsk",
        "--tools", "Read,Grep,Glob,Bash",
        "--allowedTools", "Read,Grep,Glob,Bash",
    ]
    assert claude_opus.verification_basis == "catalogued"

    reg, _ = seats.discover(
        reg,
        which=_which_from({"codex": "/x/codex"}),
        now="t2",
    )
    codex = reg.seats["codex/gpt-5.6-sol"]
    assert codex.commands == [[
        "/x/codex", "exec", "--skip-git-repo-check",
        "--sandbox", "workspace-write", "-c",
        'model_reasoning_effort="xhigh"',
        "{prompt}", "--model", "gpt-5.6-sol",
    ]]
    assert codex.isolation_argv == ["--ignore-user-config", "--ignore-rules"]
    assert codex.no_persistence_argv == ["--ephemeral"]
    assert codex.verification_argv == []
    assert codex.verification_basis == "catalogued"

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
    assert derived.verification_argv == base.verification_argv
    assert derived.verification_basis == base.verification_basis
    assert derived.result_schema_version == base.result_schema_version


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


def test_cli_seats_add_records_explicit_verification_and_v2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    tool = Path(_real_tool(tmp_path))
    assert main([
        "seats", "add", "custom/verifier",
        "--command", f"{tool} {{input_path}} {{result_path}}",
        "--verification-capable",
        "--verification-argv=--allow-read --allow-shell",
        "--result-schema-version", "2",
    ]) == 0
    seat = seats.load_registry().seats["custom/verifier"]
    assert seat.verification_basis == "declared"
    assert seat.verification_argv == ["--allow-read", "--allow-shell"]
    assert seat.result_schema_version == 2


def test_cli_seats_add_accepts_result_schema_v3(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The engine's own refusal text tells operators to register with
    # --result-schema-version 3; the parser must accept it (release-gate
    # finding, 2026-08-27: choices=(1, 2) rejected the documented value).
    from debate.__main__ import main

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    tool = Path(_real_tool(tmp_path))
    assert main([
        "seats", "add", "custom/verifier",
        "--command", f"{tool} {{input_path}} {{result_path}}",
        "--verification-capable",
        "--verification-argv=--allow-read --allow-shell",
        "--result-schema-version", "3",
    ]) == 0
    seat = seats.load_registry().seats["custom/verifier"]
    assert seat.verification_basis == "declared"
    assert seat.result_schema_version == 3


def test_v2_manual_adapter_needs_explicit_verification_declaration(tmp_path: Path) -> None:
    tool = Path(_real_tool(tmp_path))
    with pytest.raises(channel.ChannelError, match="verification-capable"):
        seats.add_seat(
            seats.Registry(),
            "custom/verifier",
            f"{tool} {{input_path}} {{result_path}}",
            which=_which_from({str(tool): str(tool)}),
            result_schema_version=2,
        )


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
    """(a) The catalog KNOWS this tool's isolation settings, so a flag-less
    entry is simply an out-of-date registry, and the refusal says so."""
    from debate import opening

    path = _registry_env(tmp_path, monkeypatch)
    _v07_shaped_registry(path)
    reg = seats.load_registry()
    problem = opening.admission_problem(reg.seats[seat_id], real_home=tmp_path)
    assert problem is not None
    assert "debate seats discover" in problem
    assert "--isolation-argv" not in problem


def test_the_catalog_only_declares_isolation_for_the_tools_it_verified() -> None:
    """The fact the three-way refusal turns on, pinned against the catalog."""
    assert seats.catalog_declares_isolation("claude")
    assert seats.catalog_declares_isolation("codex")
    for vendor in ("kimi", "glm", "deepseek"):
        assert not seats.catalog_declares_isolation(vendor), vendor
    assert not seats.catalog_declares_isolation("nosuchvendor")


@pytest.mark.parametrize("vendor,submodel", [
    ("kimi", "kimi-code/k3"), ("glm", "glm-5.3"), ("deepseek", "deepseek-v4-flash"),
])
def test_a_catalogued_tool_with_nothing_verified_is_told_to_register_a_new_seat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, vendor: str, submodel: str
) -> None:
    """(b) Debate catalogues this tool but has verified NO isolation settings
    for it, so a refresh would change nothing. `seats add` refuses a catalog
    id, which makes a custom seat under a NEW id the only truthful path."""
    from debate import opening

    _registry_env(tmp_path, monkeypatch)
    tool = tmp_path / "tool"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    seat = seats.Seat(
        seat_id=f"{vendor}/{submodel}", vendor=vendor, submodel=submodel, effort=None,
        commands=[[str(tool), "{prompt}"]], source="catalog", present=True, smoke=None,
    )
    problem = opening.admission_problem(seat, real_home=tmp_path)
    assert problem is not None
    assert "no verified isolation settings" in problem
    assert "new seat id" in problem
    assert "debate seats discover" not in problem
    # The advice has to be actionable: the registry really does refuse the
    # catalog id, which is why the message says to pick a new one.
    reg = seats.load_registry()
    reg.seats[seat.seat_id] = seat
    with pytest.raises(channel.ChannelError, match="catalog seat"):
        seats.add_seat(
            reg, seat.seat_id, f"{tool} {{prompt}}",
            isolation_argv=["--iso"], no_persistence_argv=["--forget"],
        )


def test_a_flagless_manual_seat_is_told_to_declare_its_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(c) The operator authored this seat, so the two declaration paths are
    the honest advice and the seat id it already has is fine."""
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


def test_no_catalog_entry_repeats_a_flag_across_its_argv_layers() -> None:
    """The managed bridge composes invocation + submodel + effort + isolation
    + no-persistence + verification argv into ONE command line, and codex's
    parser refuses a repeated flag (field finding F13: --skip-git-repo-check
    lived in two layers and every managed codex turn died on it)."""
    for entry in CATALOG:
        composed = [
            *entry.invocation, *entry.submodel_argv, *entry.effort_argv,
            *entry.isolation_argv, *entry.no_persistence_argv,
            *entry.verification_argv,
        ]
        flags = [part for part in composed if part.startswith("--")]
        assert len(flags) == len(set(flags)), (entry.vendor, sorted(flags))


def test_windows_discovery_substitutes_a_runnable_codex_sandbox(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Field finding F27: Windows codex has no granular sandbox --
    workspace-write blocks ALL shell execution there (model-verified on the
    box), so discovery pins danger-full-access on nt and the seat command
    records the truth. POSIX keeps workspace-write."""
    _registry_env(tmp_path, monkeypatch)
    monkeypatch.setattr(seats, "_is_windows", lambda: True)
    reg = seats.load_registry()
    reg, _ = seats.discover(
        reg, which=_which_from({"codex": "/x/codex"}), now="t-nt"
    )
    argv = reg.seats["codex/gpt-5.6-terra"].commands[0]
    assert "danger-full-access" in argv
    assert "workspace-write" not in argv


def test_windows_discovery_resolves_past_a_batch_shim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Field finding F28: an npm .cmd batch shim re-parses argv and feeds a
    seat only the first line of a multi-line prompt. When the npm layout
    ships the vendored native exe, discovery pins THAT; a shim with no exe
    behind it stands as resolved."""
    shim_dir = tmp_path / "npm"
    exe = (
        shim_dir / "node_modules" / "@openai" / "codex" / "node_modules"
        / "@openai" / "codex-win32-x64" / "vendor" / "x86_64-pc-windows-msvc"
        / "bin" / "codex.exe"
    )
    exe.parent.mkdir(parents=True)
    exe.write_bytes(b"MZ")
    shim = shim_dir / "codex.cmd"
    shim.write_text("@echo shim\r\n", encoding="utf-8")

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.setattr(seats, "_is_windows", lambda: True)
    reg = seats.load_registry()
    reg, _ = seats.discover(
        reg, which=_which_from({"codex": str(shim)}), now="t-shim"
    )
    assert reg.seats["codex/gpt-5.6-terra"].commands[0][0] == str(exe)
