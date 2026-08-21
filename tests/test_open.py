"""Slice 3: `debate open` -- mint a debate with its pair picked at birth."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Mapping

import pytest

from debate import channel, opening, seats
from debate.__main__ import _watcher_config, main


def _registry_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(path))
    # The basetemp lives INSIDE the checkout (pyproject pins .pytest-tmp), so
    # without a ceiling _derived_project resolves the enclosing repo and every
    # open writes its toplevel config into the real working tree.
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    return path


def _seat(seat_id: str, argv: list[str], *, present: bool = True,
          smoke: seats.SmokeStatus | None = None, effort: str | None = None) -> seats.Seat:
    vendor, _, submodel = seat_id.partition("/")
    return seats.Seat(
        seat_id=seat_id, vendor=vendor, submodel=submodel.split("@", 1)[0],
        effort=effort, commands=[argv], source="manual", present=present, smoke=smoke,
    )


def _smoked(at: str = "2026-08-16T00:00:00+00:00") -> seats.SmokeStatus:
    return seats.SmokeStatus(at=at, result="pass")


def _two_seat_registry(tmp_path: Path) -> seats.Registry:
    reg = seats.Registry()
    a = tmp_path / "agent-a"
    b = tmp_path / "agent-b"
    for tool in (a, b):
        tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        tool.chmod(0o755)
    reg.seats["alpha/one"] = _seat("alpha/one", [str(a), "{prompt}"], smoke=_smoked())
    reg.seats["beta/two"] = _seat("beta/two", [str(b), "{prompt}"], smoke=_smoked())
    return reg


# --- the _watcher_config seam (round-6 gate fold) ---------------------------


def test_watcher_config_seam_default_unchanged(tmp_path: Path) -> None:
    """Omitting channel_config keeps the disk-read path: a fresh root refuses."""
    config = tmp_path / "w.json"
    config.write_text(json.dumps({"state_path": str(tmp_path / "s.json"), "commands": {}}),
                      encoding="utf-8")
    with pytest.raises(channel.ChannelError, match="refused"):
        _watcher_config(tmp_path, config, "nope-12345")


def test_watcher_config_seam_accepts_in_memory_record(tmp_path: Path) -> None:
    """With an in-memory ChannelConfig the loader round-trips on a root that
    holds NO channel record -- the `open` case."""
    state = tmp_path / "state" / "x.json"
    config = tmp_path / "w.json"
    config.write_text(json.dumps({
        "state_path": str(state),
        "commands": {"alpha": ["/bin/echo", "{prompt}"], "beta": ["/bin/echo", "{prompt}"]},
    }), encoding="utf-8")
    mem = channel.ChannelConfig(
        parties=("alpha", "beta"), supervisor="owner", thread_cap=12,
        name="fresh-12345", project=str(tmp_path), managed_version=channel.MANAGED_VERSION,
    )
    loaded = _watcher_config(tmp_path / "collab", config, "fresh-12345", channel_config=mem)
    assert loaded.managed_problem() is None


# --- pick_pair --------------------------------------------------------------


def _no_ask(prompt: str) -> str:
    raise AssertionError(f"unexpected interactive prompt: {prompt}")


def test_pick_pair_requested_pair_validated(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
        assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    assert pair == ("alpha/one", "beta/two")


def test_pick_pair_absent_seat_refused(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    reg.seats["alpha/one"].present = False
    with pytest.raises(channel.ChannelError, match="alpha/one"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
            assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )


def test_pick_pair_unknown_seat_refused(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    with pytest.raises(channel.ChannelError, match="gamma/three"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("gamma/three", "beta/two"),
            assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )


def test_pick_pair_unsmoked_needs_confirmation_yes_covers(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    reg.seats["alpha/one"].smoke = None
    # --yes covers the unsmoked warning...
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
        assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    assert pair == ("alpha/one", "beta/two")
    # ...interactively it asks, and a refusal answer refuses.
    answers = iter(["n"])
    with pytest.raises(channel.ChannelError, match="unsmoked"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
            assume_yes=False, ask=lambda prompt: next(answers), now="2026-08-17T00:00:00+00:00",
    )


def test_pick_pair_identity_guard(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    tool = tmp_path / "agent-a"
    reg.seats["alpha/one@low"] = _seat(
        "alpha/one@low", [str(tool), "{prompt}", "--effort", "low"],
        smoke=_smoked(), effort="low",
    )
    # same seat id twice: refused without the flag, even with --yes
    with pytest.raises(channel.ChannelError, match="same"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "alpha/one"),
            assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    # same vendor/submodel at two DIFFERENT efforts: the warning fires all the
    # same -- effort ignored, same weights
    with pytest.raises(channel.ChannelError, match="weights|identical|monologue"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "alpha/one@low"),
            assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    # --allow-identical-seats covers vendor/submodel identity...
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "alpha/one@low"),
        assume_yes=True, ask=_no_ask, allow_identical=True, now="2026-08-17T00:00:00+00:00",
    )
    assert pair == ("alpha/one", "alpha/one@low")
    # ...but identical SELECTED argv refuses ALWAYS.
    reg.seats["alpha/clone"] = _seat("alpha/clone", [str(tool), "{prompt}"], smoke=_smoked())
    with pytest.raises(channel.ChannelError, match="argv"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "alpha/clone"),
            assume_yes=True, ask=_no_ask, allow_identical=True, now="2026-08-17T00:00:00+00:00",
    )


def test_pick_pair_default_from_last_pair(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    # A remembered pair is only offered while both its seats could still be
    # seated under Debate's control (A2 fix round 1), so the fixture's seats
    # carry the settings that admit them.
    for seat in reg.seats.values():
        seat.isolation_argv = ["--no-config"]
        seat.no_persistence_argv = ["--no-history"]
    reg.last_pair[str(tmp_path)] = ["alpha/one", "beta/two"]
    # Enter accepts the project default
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=None,
        assume_yes=False, ask=lambda prompt: "", now="2026-08-17T00:00:00+00:00",
    )
    assert pair == ("alpha/one", "beta/two")
    # a default containing an unseatable seat is DROPPED, not offered; with
    # --yes and no usable default: refuse
    reg.seats["alpha/one"].present = False
    with pytest.raises(channel.ChannelError, match="default"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=None,
            assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )


# --- open_debate ------------------------------------------------------------


def _open_spec(root: Path, **kwargs: object) -> opening.OpenSpec:
    defaults: dict[str, object] = dict(
        root=root, label="market-research", pair=("alpha/one", "beta/two"),
        supervisor="owner", thread_cap=12, allow_identical_seats=False,
        assume_yes=True,
    )
    defaults.update(kwargs)
    return opening.OpenSpec(**defaults)  # type: ignore[arg-type]


def _load_fn(root: Path, config_path: Path, name: str | None,
             mem: channel.ChannelConfig) -> object:
    return _watcher_config(root, config_path, name, channel_config=mem)


def test_open_debate_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = _two_seat_registry(tmp_path)
    root = tmp_path / "collab"
    root.mkdir()
    result = opening.open_debate(
        _open_spec(root), reg, load_config_fn=_watcher_config,
        now="2026-08-16T03:00:00+00:00", tool_version="0.7.0",
    )
    assert result.channel_name.startswith("market-research-")
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    assert record["parties"] == ["alpha", "beta"]
    prov = record["seats"]
    assert prov["picked_at"] == "2026-08-16T03:00:00+00:00"
    assert prov["tool_version"] == "0.7.0"
    assert prov["alpha"]["seat"] == "alpha/one"
    assert prov["alpha"]["effort"] is None
    assert prov["alpha"]["command"][-1] == "{prompt}" or "{prompt}" in prov["alpha"]["command"]
    # load_config round-trips the record with the extra key ignored
    loaded = channel.load_config(root, result.channel_name)
    assert loaded.parties == ("alpha", "beta")
    # watcher config written at the derived toplevel, loader-valid
    assert result.config_path.is_file()
    loaded_cfg = _watcher_config(root, result.config_path, result.channel_name)
    assert loaded_cfg.managed_problem() is None
    # PROTOCOL scaffolded; last_pair recorded project + global
    assert (root / "PROTOCOL.md").is_file()
    assert reg.last_pair[str(opening.project_key(root))] == ["alpha/one", "beta/two"]
    assert reg.last_pair[""] == ["alpha/one", "beta/two"]
    assert result.hints


def test_open_debate_shared_vendor_party_names_are_slugs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.Registry()
    a = tmp_path / "agent-a"
    a.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    a.chmod(0o755)
    reg.seats["codex/gpt-5.6-sol@low"] = _seat(
        "codex/gpt-5.6-sol@low", [str(a), "{prompt}", "--effort", "low"],
        smoke=_smoked(), effort="low",
    )
    reg.seats["codex/gpt-5.6-sol@high"] = _seat(
        "codex/gpt-5.6-sol@high", [str(a), "{prompt}", "--effort", "high"],
        smoke=_smoked(), effort="high",
    )
    root = tmp_path / "collab"
    root.mkdir()
    result = opening.open_debate(
        _open_spec(root, pair=("codex/gpt-5.6-sol@low", "codex/gpt-5.6-sol@high"),
                   allow_identical_seats=True),
        reg, load_config_fn=_watcher_config,
        now="t", tool_version="0.7.0",
    )
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    assert record["parties"] == ["codex-gpt-5-6-sol-low", "codex-gpt-5-6-sol-high"]


def test_open_debate_nothing_written_on_validation_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = _two_seat_registry(tmp_path)
    root = tmp_path / "collab"
    root.mkdir()

    def refusing_load(
        r: Path, c: Path, n: str | None,
        channel_config: channel.ChannelConfig | None = None,
    ) -> object:
        raise channel.ChannelError("refused: forced for the empty-root test")

    with pytest.raises(channel.ChannelError, match="forced"):
        opening.open_debate(
            _open_spec(root), reg, load_config_fn=refusing_load,  # type: ignore[arg-type]
            now="t", tool_version="0.7.0",
        )
    assert list(root.iterdir()) == [], "the target root stays empty on pre-write failure"


def test_open_debate_leaves_setup_defaults_cache_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    cache = tmp_path / "setup-defaults.json"
    cache.write_text('{"channel": "before"}', encoding="utf-8")
    monkeypatch.setenv("DEBATE_SETUP_DEFAULTS", str(cache))
    reg = _two_seat_registry(tmp_path)
    root = tmp_path / "collab"
    root.mkdir()
    opening.open_debate(
        _open_spec(root), reg, load_config_fn=_watcher_config,
        now="t", tool_version="0.7.0",
    )
    assert cache.read_text(encoding="utf-8") == '{"channel": "before"}', (
        "open must NEVER touch the wizard's defaults cache (plan fold H2)"
    )


# --- CLI --------------------------------------------------------------------


def test_cli_open_on_multichannel_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = _two_seat_registry(tmp_path)
    seats.save_registry(reg)
    root = tmp_path / "collab"
    root.mkdir()
    # a root ALREADY holding several channels: open must not be refused by
    # discovery it never needed (plan fold B2)
    for stem in ("a-11111", "b-22222"):
        (root / f"{stem}.debate.json").write_text(
            json.dumps({"parties": ["x", "y"], "supervisor": "owner", "name": stem}),
            encoding="utf-8",
        )
    monkeypatch.chdir(tmp_path)
    rc = main([
        "open", "--root", str(root), "--label", "market-research",
        "--pair", "alpha/one,beta/two", "--yes",
    ])
    assert rc == 0
    out = capsys.readouterr().out
    assert "market-research-" in out


# --- Slice 4: the project profile (section 2.10's second layer, ruling 5) ---


def _write_profile(project_dir: Path, payload: object) -> Path:
    path = project_dir / seats.PROFILE_NAME
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_load_profile_missing_file_is_none(tmp_path: Path) -> None:
    assert seats.load_profile(str(tmp_path), seats.Registry()) is None


def test_load_profile_fail_closed(tmp_path: Path) -> None:
    reg = seats.Registry()
    reg.seats["alpha/one"] = seats.Seat(
        seat_id="alpha/one", vendor="alpha", submodel="one", effort=None,
        commands=[["/x/a", "{prompt}"]], source="manual", present=True, smoke=None,
    )
    path = tmp_path / seats.PROFILE_NAME
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(channel.ChannelError, match=str(path.name)):
        seats.load_profile(str(tmp_path), reg)
    _write_profile(tmp_path, {"profile_version": 2, "allowlist": ["alpha/one"]})
    with pytest.raises(channel.ChannelError, match="profile_version"):
        seats.load_profile(str(tmp_path), reg)
    _write_profile(tmp_path, {"profile_version": 1, "allowlist": ["ghost/nine"]})
    with pytest.raises(channel.ChannelError, match="ghost/nine"):
        seats.load_profile(str(tmp_path), reg)
    _write_profile(tmp_path, {"profile_version": 1, "allowlist": []})
    with pytest.raises(channel.ChannelError, match="delete"):
        seats.load_profile(str(tmp_path), reg)
    _write_profile(tmp_path, {"profile_version": 1, "allowlist": ["alpha/one"]})
    profile = seats.load_profile(str(tmp_path), reg)
    assert profile is not None and profile.allowlist == ("alpha/one",)


def test_pick_pair_profile_restricts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    reg = _two_seat_registry(tmp_path)
    tool = tmp_path / "agent-c"
    tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    tool.chmod(0o755)
    reg.seats["gamma/three"] = _seat("gamma/three", [str(tool), "{prompt}"], smoke=_smoked())
    _write_profile(tmp_path, {"profile_version": 1, "allowlist": ["alpha/one", "beta/two"]})
    # --pair outside the allowlist: refused naming the profile file
    with pytest.raises(channel.ChannelError, match=seats.PROFILE_NAME):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("gamma/three", "beta/two"),
            assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    # allowlisted pair passes
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
        assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    assert pair == ("alpha/one", "beta/two")
    # a last_pair default outside the allowlist is DROPPED (no default offered)
    reg.last_pair[str(tmp_path)] = ["gamma/three", "beta/two"]
    with pytest.raises(channel.ChannelError, match="default"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=None, assume_yes=True, ask=_no_ask, now="2026-08-17T00:00:00+00:00",
    )
    # the interactive listing shows only allowlisted seats
    prompts: list[str] = []

    def capture(prompt: str) -> str:
        prompts.append(prompt)
        return "alpha/one,beta/two"

    opening.pick_pair(reg, project=str(tmp_path), requested=None, assume_yes=False, ask=capture, now="2026-08-17T00:00:00+00:00",
    )
    assert "gamma/three" not in prompts[0]


# --- branch-gate round-1 folds ----------------------------------------------


def test_open_refuses_existing_toplevel_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = _two_seat_registry(tmp_path)
    root = tmp_path / "collab"
    root.mkdir()
    spec = _open_spec(root)
    import debate.opening as op

    monkeypatch.setattr(
        channel, "generate_channel_id", lambda r, label=None: f"{label}-99999"
    )
    (tmp_path / "market-research-99999.watcher.json").write_text("{}", encoding="utf-8")
    with pytest.raises(channel.ChannelError, match="exists"):
        op.open_debate(spec, reg, load_config_fn=_watcher_config, now="t", tool_version="v")
    assert list(root.iterdir()) == [], "nothing written behind the refusal"


def test_open_refuses_uncreatable_state_dir_before_any_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = _two_seat_registry(tmp_path)
    root = tmp_path / "collab"
    root.mkdir()
    blocker = tmp_path / "state-blocker"
    blocker.write_text("a file where a directory must go", encoding="utf-8")
    import debate.opening as op

    monkeypatch.setattr(
        op, "derive_paths",
        lambda r, n, p: (tmp_path / f"{n}.watcher.json", blocker / "sub" / f"{n}.json"),
    )
    with pytest.raises(channel.ChannelError, match="state directory"):
        op.open_debate(
            _open_spec(root), reg, load_config_fn=_watcher_config, now="t", tool_version="v"
        )
    assert list(root.iterdir()) == [], "the round-1 live-proof failure shape is refused pre-write"


def test_cli_seats_list_json_is_machine_readable_after_upgrade(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    main(["seats", "discover"])
    reg = seats.load_registry()
    reg.tool_version = "0.0.1"  # force the upgrade re-scan on the next command
    seats.save_registry(reg)
    capsys.readouterr()
    assert main(["seats", "list", "--json"]) == 0
    captured = capsys.readouterr()
    json.loads(captured.out)  # stdout is pure JSON; diagnostics live on stderr


def test_cli_seats_list_shows_notes_and_efforts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.Registry()
    tool = tmp_path / "claude"
    tool.write_text("#!/bin/sh\n", encoding="utf-8")
    tool.chmod(0o755)
    reg.seats["claude/opus"] = _seat("claude/opus", [str(tool), "-p", "{prompt}"], smoke=_smoked())
    seats.save_registry(reg)
    monkeypatch.chdir(tmp_path)
    assert main(["seats", "list"]) == 0
    out = capsys.readouterr().out
    assert "note:" in out
    assert "efforts:" in out and "high" in out
    assert main(["seats", "list", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["claude/opus"]["known_efforts"]
    assert payload["claude/opus"]["notes"]


def test_smoke_requires_confirmation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _registry_env(tmp_path, monkeypatch)
    reg = seats.Registry()
    reg.seats["fake/one"] = _seat("fake/one", ["/bin/false", "{prompt}"])
    with pytest.raises(channel.ChannelError, match="not confirmed"):
        seats.smoke_seat(reg, "fake/one", now="t", ask=lambda prompt: "n")
    assert reg.seats["fake/one"].smoke is None, "no spend, no record"
    result = seats.smoke_seat(
        reg, "fake/one", scratch_base=tmp_path / "s", now="t", assume_yes=True
    )
    assert result == "fail"


def test_stale_warning_cannot_be_bypassed_without_clock(tmp_path: Path) -> None:
    """Round-3 salvaged codex finding: the clock is REQUIRED -- a caller
    cannot silently skip the stale warning by omitting it."""
    import inspect

    sig = inspect.signature(opening.pick_pair)
    assert sig.parameters["now"].default is inspect.Parameter.empty


def test_discover_never_clobbers_manual_custom_effort_seat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Round-3 salvaged codex finding: derived-refresh touches only seats
    actually DERIVED from the old base argv; a manual custom command stays."""
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(tmp_path / "r.json"))
    wrapper = tmp_path / "claude"
    wrapper.write_text("#!/bin/sh\n", encoding="utf-8")
    wrapper.chmod(0o755)
    custom = tmp_path / "echo-agent"
    custom.write_text("#!/bin/sh\n", encoding="utf-8")
    custom.chmod(0o755)
    reg = seats.Registry()
    reg, _ = seats.discover(reg, which=lambda n: {"claude": str(wrapper)}.get(n), now="t1")
    seats.add_seat(reg, "claude/opus@high", f"{custom} {{prompt}}")
    moved = tmp_path / "elsewhere" / "claude"
    moved.parent.mkdir()
    moved.write_text("#!/bin/sh\n", encoding="utf-8")
    moved.chmod(0o755)
    reg, _ = seats.discover(reg, which=lambda n: {"claude": str(moved)}.get(n), now="t2")
    assert reg.seats["claude/opus@high"].commands[0] == [str(custom), "{prompt}"], (
        "a manual custom-command @effort seat is the operator's own"
    )


def test_discover_preserves_manual_seat_that_merely_extends_base_argv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Round-5 converged finding: a manual @effort seat whose command merely
    STARTS WITH the base argv is not derived and is never re-derived; only
    the exact base+fragment shape is."""
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(tmp_path / "r.json"))
    old = tmp_path / "claude"
    old.write_text("#!/bin/sh\n", encoding="utf-8")
    old.chmod(0o755)
    reg = seats.Registry()
    reg, _ = seats.discover(reg, which=lambda n: {"claude": str(old)}.get(n), now="t0")
    base = list(reg.seats["claude/opus"].commands[0])
    # codex's reproduction: base + effort fragment + an operator's extra flag
    reg.seats["claude/opus@high"] = seats.Seat(
        "claude/opus@high", "claude", "opus", "high",
        [base + ["--effort", "high", "--manual-wrapper-flag"]],
        "manual", True, None,
    )
    # a true derivation for contrast
    seats.add_effort_seat(reg, "claude/opus@low")
    new = tmp_path / "moved" / "claude"
    new.parent.mkdir()
    new.write_text("#!/bin/sh\n", encoding="utf-8")
    new.chmod(0o755)
    reg, _ = seats.discover(reg, which=lambda n: {"claude": str(new)}.get(n), now="t1")
    assert reg.seats["claude/opus@high"].commands[0][-1] == "--manual-wrapper-flag", (
        "the operator's command is never clobbered"
    )
    assert reg.seats["claude/opus@high"].commands[0][0] == str(old), "untouched entirely"
    assert reg.seats["claude/opus@low"].commands[0][0] == str(new), (
        "the exact derived shape IS re-derived"
    )


def test_upgrade_stamp_persists_on_clean_rescan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Round-6 converged finding: the version stamp persists even when the
    re-scan diff is empty, so the mismatch re-scan cannot refire forever."""
    from debate import __version__

    _registry_env(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path)
    main(["seats", "discover"])
    reg = seats.load_registry()
    reg.tool_version = "0.0.1"
    seats.save_registry(reg)
    capsys.readouterr()
    assert main(["seats", "check"]) == 0
    capsys.readouterr()
    assert seats.load_registry().tool_version == __version__, (
        "the stamp must reach the FILE, not just memory"
    )


def test_profile_version_bool_refuses(tmp_path: Path) -> None:
    """Round-7 fold: JSON true must not pass the version-1 check (bool==int)."""
    reg = seats.Registry()
    (tmp_path / seats.PROFILE_NAME).write_text(
        json.dumps({"profile_version": True, "allowlist": ["x/y"]}), encoding="utf-8"
    )
    with pytest.raises(channel.ChannelError, match="profile_version"):
        seats.load_profile(str(tmp_path), reg)


def test_open_provenance_carries_smoke_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Round-7 fold: the provenance block records the smoke STATE verbatim."""
    _registry_env(tmp_path, monkeypatch)
    reg = _two_seat_registry(tmp_path)
    root = tmp_path / "collab"
    root.mkdir()
    result = opening.open_debate(
        _open_spec(root), reg, load_config_fn=_watcher_config,
        now="t", tool_version="v",
    )
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    assert record["seats"]["alpha"]["smoke_result"] == "pass"
    assert record["seats"]["alpha"]["smoke_at"] is not None


# --- Slice C5: prompt-style seats join a fully managed debate ---------------

MANAGED_NOW = "2026-08-20T12:00:00+00:00"

NINE_INHERITED_NAMES = [
    "PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
]


def _fake_tool(tmp_path: Path, name: str) -> Path:
    tool = tmp_path / name
    tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    tool.chmod(0o755)
    return tool


def _raw_seat(
    command: list[str],
    *,
    vendor: str,
    submodel: str,
    source: str = "manual",
    capability_class: str | None = None,
    isolation_argv: list[str] | None = None,
    no_persistence_argv: list[str] | None = None,
    config_home: str | None = None,
) -> dict[str, object]:
    return {
        "vendor": vendor,
        "submodel": submodel,
        "effort": None,
        "commands": [command],
        "source": source,
        "present": True,
        "smoke": None,
        "cost_mode": "local",
        "capability_class": capability_class,
        "isolation_argv": list(isolation_argv or []),
        "no_persistence_argv": list(no_persistence_argv or []),
        "config_home": config_home,
    }


def _write_raw_registry(path: Path, rows: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({
            "registry_version": 1,
            "tool_version": "test",
            "discovered_at": MANAGED_NOW,
            "seats": dict(rows),
            "last_pair": {},
        }) + "\n",
        encoding="utf-8",
    )


def _git_project(project: Path) -> str:
    import subprocess

    project.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    (project / "README").write_text("stub\n", encoding="utf-8")
    git = ["git", "-C", str(project), "-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run([*git, "add", "README"], check=True)
    subprocess.run([*git, "commit", "-qm", "stub"], check=True)
    return subprocess.run(
        ["git", "-C", str(project), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def managed_project(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    rows: Mapping[str, object],
    allow: list[str],
) -> tuple[Path, str]:
    """A git project with an approved seat list and a registry on disk.

    The profile is written directly rather than through `onboarding.approve`:
    approve re-scans the machine, and these fixtures own every seat row byte
    for byte.
    """
    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    project = tmp_path / "project"
    head = _git_project(project)
    _write_raw_registry(registry_path, rows)
    (project / seats.PROFILE_NAME).write_text(
        json.dumps({"profile_version": 1, "allowlist": list(allow)}) + "\n",
        encoding="utf-8",
    )
    return project, head


def _package_root() -> str:
    import debate

    return str(Path(debate.__file__).resolve().parent.parent)


def test_prompt_style_seat_is_wrapped_with_its_verified_flags(tmp_path: Path) -> None:
    """A seat that only takes a question text still joins a fully managed
    debate: the recorded command runs it under Debate's own runner, carrying
    the seat's argv, its verified flags and its configuration folder."""
    from debate import bridge

    tool = _fake_tool(tmp_path, "clauded")
    seat = seats.Seat(
        seat_id="claude/sonnet", vendor="claude", submodel="sonnet", effort=None,
        commands=[[str(tool), "-p", "{prompt}"]], source="catalog", present=True,
        smoke=None, cost_mode="subscription", capability_class="frontier",
        isolation_argv=["--strict-mcp-config", "--settings", "{}"],
        no_persistence_argv=["--no-session-persistence"],
        config_home="CLAUDE_CONFIG_DIR=.claude",
    )
    profile = opening._brokered_adapter(
        seat, tool_version="test", author_vendor="codex", real_home=tmp_path,
    )
    command = profile["command"]
    assert isinstance(command, list)
    assert command[:4] == [sys.executable, "-m", "debate", "bridge"]
    assert command[-2:] == ["{input_path}", "{result_path}"]
    spec = bridge.parse_bridge_command(command)
    assert spec is not None
    assert spec.seat_id == "claude/sonnet"
    assert spec.vendor == "claude"
    assert spec.submodel == "sonnet"
    assert spec.argv == (str(tool), "-p", "{prompt}")
    assert spec.isolation_argv == ("--strict-mcp-config", "--settings", "{}")
    assert spec.no_persistence_argv == ("--no-session-persistence",)
    assert spec.config_home == "CLAUDE_CONFIG_DIR=.claude"
    assert spec.isolation_flags_basis == "catalogued"
    assert profile["environment"] == {
        "PYTHONPATH": _package_root(),
        "DEBATE_BRIDGE_REAL_HOME": str(tmp_path),
    }
    assert profile["environment_allowlist"] == NINE_INHERITED_NAMES
    assert profile["requested_model"] == "sonnet"
    assert profile["author_relationship"] == "author-independent"
    assert "expected_runtime_model" not in profile
    assert profile["timeout_seconds"] == 1200
    assert profile["session_persistence"] is False


def test_operator_declared_flags_are_recorded_as_declared(tmp_path: Path) -> None:
    tool = _fake_tool(tmp_path, "own-agent")
    seat = seats.Seat(
        seat_id="own/agent", vendor="own", submodel="agent", effort=None,
        commands=[[str(tool), "{prompt}"]], source="manual", present=True,
        smoke=None, isolation_argv=["--offline"], no_persistence_argv=["--forget"],
    )
    from debate import bridge

    profile = opening._brokered_adapter(
        seat, tool_version="test", author_vendor="codex", real_home=tmp_path,
    )
    command = profile["command"]
    assert isinstance(command, list)
    spec = bridge.parse_bridge_command(command)
    assert spec is not None
    assert spec.isolation_flags_basis == "declared"
    assert spec.config_home is None
    assert "--config-home" not in command


def test_hand_authored_adapter_seat_is_left_alone(tmp_path: Path) -> None:
    tool = _fake_tool(tmp_path, "adapter")
    seat = seats.Seat(
        seat_id="own/adapter", vendor="own", submodel="adapter", effort=None,
        commands=[[str(tool), "{input_path}", "{result_path}"]], source="manual",
        present=True, smoke=None,
    )
    profile = opening._brokered_adapter(
        seat, tool_version="test", author_vendor="codex", real_home=tmp_path,
    )
    assert profile["command"] == [str(tool), "{input_path}", "{result_path}"]
    assert profile["environment_allowlist"] == ["PATH", "LANG", "LC_ALL"]
    assert "environment" not in profile


def test_prompt_style_seat_without_verified_flags_is_refused(tmp_path: Path) -> None:
    """Admission is the flags rule alone, and there is no way around it."""
    tool = _fake_tool(tmp_path, "kimi")
    for isolation, persistence in (([], []), (["--offline"], []), ([], ["--forget"])):
        seat = seats.Seat(
            seat_id="kimi/k3", vendor="kimi", submodel="k3", effort=None,
            commands=[[str(tool), "{prompt}"]], source="catalog", present=True,
            smoke=None, isolation_argv=list(isolation),
            no_persistence_argv=list(persistence),
        )
        with pytest.raises(channel.ChannelError) as caught:
            opening._brokered_adapter(
                seat, tool_version="test", author_vendor="codex", real_home=tmp_path,
            )
        message = str(caught.value)
        assert "kimi/k3" in message
        assert "--isolation-argv" in message and "--no-persistence-argv" in message


def test_seat_with_flags_and_no_configuration_folder_is_admitted(tmp_path: Path) -> None:
    tool = _fake_tool(tmp_path, "glm")
    seat = seats.Seat(
        seat_id="glm/glm-5.3", vendor="glm", submodel="glm-5.3", effort=None,
        commands=[[str(tool), "{prompt}"]], source="manual", present=True, smoke=None,
        isolation_argv=["--offline"], no_persistence_argv=["--forget"],
    )
    profile = opening._brokered_adapter(
        seat, tool_version="test", author_vendor="codex", real_home=tmp_path,
    )
    command = profile["command"]
    assert isinstance(command, list)
    assert "--config-home" not in command


def test_seat_command_of_neither_shape_is_refused(tmp_path: Path) -> None:
    tool = _fake_tool(tmp_path, "mute")
    seat = seats.Seat(
        seat_id="mute/one", vendor="mute", submodel="one", effort=None,
        commands=[[str(tool), "--go"]], source="manual", present=True, smoke=None,
        isolation_argv=["--offline"], no_persistence_argv=["--forget"],
    )
    with pytest.raises(channel.ChannelError) as caught:
        opening._brokered_adapter(
            seat, tool_version="test", author_vendor="codex", real_home=tmp_path,
        )
    assert "mute/one" in str(caught.value)


def test_hand_edited_configuration_folder_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A registry edited by hand to point a seat at the whole home directory
    is refused BEFORE a debate can be opened. The registry loader is the first
    gate that sees it, so that is where the refusal lands; the open re-checks
    the same rule against the operator's real home directory."""
    registry_path = tmp_path / "config" / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry_path))
    tool = _fake_tool(tmp_path, "hand-edited")
    _write_raw_registry(registry_path, {
        "hand/edited": _raw_seat(
            [str(tool), "{prompt}"], vendor="hand", submodel="edited",
            isolation_argv=["--offline"], no_persistence_argv=["--forget"],
            config_home="HOME=.config",
        ),
    })
    with pytest.raises(channel.ChannelError, match="config-home"):
        seats.load_registry()


def test_managed_open_wraps_both_seats_end_to_end(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from debate.controller import doctor_lines

    first = _fake_tool(tmp_path, "agent-one")
    second = _fake_tool(tmp_path, "agent-two")
    project, head = managed_project(
        tmp_path, monkeypatch,
        {
            "claude/sonnet": _raw_seat(
                [str(first), "-p", "{prompt}"], vendor="claude", submodel="sonnet",
                source="catalog", capability_class="frontier",
                isolation_argv=["--strict-mcp-config"],
                no_persistence_argv=["--no-session-persistence"],
                config_home="CLAUDE_CONFIG_DIR=.claude",
            ),
            "codex/gpt-5.6-sol": _raw_seat(
                [str(second), "exec", "{prompt}"], vendor="codex", submodel="gpt-5.6-sol",
                source="manual", capability_class="frontier",
                isolation_argv=["--ignore-user-config"],
                no_persistence_argv=["--ephemeral"],
            ),
        },
        ["claude/sonnet", "codex/gpt-5.6-sol"],
    )
    root = project / "collab"
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=root, label="stub", pair=("claude/sonnet", "codex/gpt-5.6-sol"),
            source_ref=head, author_vendor="claude",
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=MANAGED_NOW, tool_version="test", real_home=tmp_path,
    )
    loaded = _watcher_config(root, result.config_path, result.channel_name)
    assert loaded.managed_problem() is None
    assert loaded.broker is not None
    lines = doctor_lines(loaded.broker)
    assert any(
        "configuration home OPERATOR (CLAUDE_CONFIG_DIR)" in line
        and "isolation flags catalogued" in line
        for line in lines
    )
    assert any(
        "configuration home SANDBOX" in line and "isolation flags declared" in line
        for line in lines
    )
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    assert record["seats"]["claude"]["isolation_flags"] == "catalogued"
    assert record["seats"]["claude"]["configuration_home"] == "operator (CLAUDE_CONFIG_DIR)"
    assert record["seats"]["codex"]["isolation_flags"] == "declared"
    assert record["seats"]["codex"]["configuration_home"] == "sandbox"


def test_hand_authored_adapter_pair_records_adapter_owned_isolation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = _fake_tool(tmp_path, "adapter-one")
    second = _fake_tool(tmp_path, "adapter-two")
    project, head = managed_project(
        tmp_path, monkeypatch,
        {
            "alpha/fake": _raw_seat(
                [str(first), "{input_path}", "{result_path}"],
                vendor="alpha", submodel="fake",
            ),
            "beta/fake": _raw_seat(
                [str(second), "{input_path}", "{result_path}"],
                vendor="beta", submodel="fake",
            ),
        },
        ["alpha/fake", "beta/fake"],
    )
    root = project / "collab"
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=root, label="stub", pair=("alpha/fake", "beta/fake"),
            source_ref=head, author_vendor="claude",
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=MANAGED_NOW, tool_version="test",
    )
    record = json.loads((root / f"{result.channel_name}.debate.json").read_text(encoding="utf-8"))
    for party in ("alpha", "beta"):
        assert record["seats"][party]["isolation_flags"] == "adapter-owned"
        assert record["seats"][party]["configuration_home"] == "sandbox"


def test_same_vendor_pair_with_different_models_is_admitted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The identity guard is unchanged: one vendor, two models is a debate.
    Their classes differ, so the uneven-pair choice is made explicitly."""
    tool = _fake_tool(tmp_path, "claude-tool")
    project, head = managed_project(
        tmp_path, monkeypatch,
        {
            "claude/sonnet": _raw_seat(
                [str(tool), "-p", "sonnet", "{prompt}"], vendor="claude", submodel="sonnet",
                source="catalog", capability_class="frontier",
                isolation_argv=["--strict-mcp-config"],
                no_persistence_argv=["--no-session-persistence"],
            ),
            "claude/haiku": _raw_seat(
                [str(tool), "-p", "haiku", "{prompt}"], vendor="claude", submodel="haiku",
                source="catalog", capability_class="light",
                isolation_argv=["--strict-mcp-config"],
                no_persistence_argv=["--no-session-persistence"],
            ),
        },
        ["claude/sonnet", "claude/haiku"],
    )
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=project / "collab", label="stub",
            pair=("claude/sonnet", "claude/haiku"),
            source_ref=head, author_vendor="codex", allow_mismatched_pair=True,
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=MANAGED_NOW, tool_version="test", real_home=tmp_path,
    )
    record = json.loads(
        (project / "collab" / f"{result.channel_name}.debate.json").read_text(encoding="utf-8")
    )
    assert sorted(record["parties"]) == ["claude-haiku", "claude-sonnet"]


def test_yes_alone_refuses_an_uneven_remembered_pair(tmp_path: Path) -> None:
    """--yes accepts the remembered pair; it never answers a later question."""
    reg = seats.Registry()
    first = _fake_tool(tmp_path, "big")
    second = _fake_tool(tmp_path, "small")
    reg.seats["big/one"] = seats.Seat(
        seat_id="big/one", vendor="big", submodel="one", effort=None,
        commands=[[str(first), "{prompt}"]], source="catalog", present=True,
        smoke=_smoked(), capability_class="frontier",
        isolation_argv=["--no-config"], no_persistence_argv=["--no-history"],
    )
    reg.seats["small/two"] = seats.Seat(
        seat_id="small/two", vendor="small", submodel="two", effort=None,
        commands=[[str(second), "{prompt}"]], source="catalog", present=True,
        smoke=_smoked(), capability_class="light",
        isolation_argv=["--offline"], no_persistence_argv=["--forget"],
    )
    reg.last_pair[str(tmp_path)] = ["big/one", "small/two"]
    with pytest.raises(channel.ChannelError) as caught:
        opening.pick_pair(
            reg, project=str(tmp_path), requested=None, assume_yes=True,
            ask=_no_ask, now="2026-08-20T00:00:00+00:00",
        )
    assert "--allow-mismatched-pair" in str(caught.value)


# --- Slice A2: the size-proportional suggestion and its size limit ----------


def _quick_pair_project(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, str]:
    """Four approved seats: a quick pair and a strongest pair, both admissible."""
    rows = {
        "claude/haiku": _raw_seat(
            [str(_fake_tool(tmp_path, "claude-haiku")), "{prompt}"],
            vendor="claude", submodel="haiku", source="catalog",
            capability_class="light",
            isolation_argv=["--strict-mcp-config"],
            no_persistence_argv=["--no-session-persistence"],
        ),
        "deepseek/flash": _raw_seat(
            [str(_fake_tool(tmp_path, "deepseek-flash")), "{prompt}"],
            vendor="deepseek", submodel="flash", source="catalog",
            capability_class="light",
            isolation_argv=["--offline"], no_persistence_argv=["--forget"],
        ),
        "claude/opus": _raw_seat(
            [str(_fake_tool(tmp_path, "claude-opus")), "{prompt}"],
            vendor="claude", submodel="opus", source="catalog",
            capability_class="frontier",
            isolation_argv=["--strict-mcp-config"],
            no_persistence_argv=["--no-session-persistence"],
        ),
        "deepseek/pro": _raw_seat(
            [str(_fake_tool(tmp_path, "deepseek-pro")), "{prompt}"],
            vendor="deepseek", submodel="pro", source="catalog",
            capability_class="frontier",
            isolation_argv=["--offline"], no_persistence_argv=["--forget"],
        ),
    }
    return managed_project(
        tmp_path, monkeypatch, rows,
        ["claude/haiku", "deepseek/flash", "claude/opus", "deepseek/pro"],
    )


def test_managed_open_records_the_small_review_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project, head = _quick_pair_project(tmp_path, monkeypatch)
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=project / "collab", label="stub",
            pair=("claude/opus", "deepseek/pro"),
            source_ref=head, author_vendor="claude",
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=MANAGED_NOW, tool_version="test", real_home=tmp_path,
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    assert config["quick_review_max_bytes"] == opening.QUICK_REVIEW_MAX_BYTES == 16384
    loaded = _watcher_config(project / "collab", result.config_path, result.channel_name)
    assert loaded.managed_problem() is None


def test_the_small_review_limit_is_a_per_debate_setting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project, head = _quick_pair_project(tmp_path, monkeypatch)
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=project / "collab", label="stub",
            pair=("claude/opus", "deepseek/pro"),
            source_ref=head, author_vendor="claude",
            quick_review_max_bytes=4096,
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=MANAGED_NOW, tool_version="test", real_home=tmp_path,
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    assert config["quick_review_max_bytes"] == 4096


def test_a_hand_edited_small_review_limit_refuses_instead_of_crashing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project, head = _quick_pair_project(tmp_path, monkeypatch)
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=project / "collab", label="stub",
            pair=("claude/opus", "deepseek/pro"),
            source_ref=head, author_vendor="claude",
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now=MANAGED_NOW, tool_version="test", real_home=tmp_path,
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    config["quick_review_max_bytes"] = "sixteen thousand"
    result.config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    with pytest.raises(channel.ChannelError, match="quick_review_max_bytes"):
        _watcher_config(project / "collab", result.config_path, result.channel_name)


def test_the_docket_size_is_the_sum_of_its_files(tmp_path: Path) -> None:
    (tmp_path / "one.md").write_text("x" * 100, encoding="utf-8")
    (tmp_path / "two.md").write_text("y" * 20, encoding="utf-8")
    assert opening.docket_byte_size(str(tmp_path), ("one.md", "two.md")) == 120
    assert opening.docket_byte_size(str(tmp_path), ()) == 0
    assert opening.docket_byte_size(str(tmp_path), ("missing.md",)) == 0


def test_cli_managed_open_without_a_pair_offers_a_numbered_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    project, _head = _quick_pair_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    rc = main([
        "open", "--brokered", "--root", str(project / "collab"),
        "--label", "market-research", "--author-vendor", "claude",
    ])
    assert rc == 1
    printed = capsys.readouterr().err
    assert "a fully managed debate needs --pair" in printed
    assert "1  claude/haiku + deepseek/flash" in printed
    assert "small review, quick pair" in printed
    assert "2  " in printed


def test_cli_managed_open_sizes_its_suggestion_by_the_review_material(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    project, _head = _quick_pair_project(tmp_path, monkeypatch)
    (project / "big-docket.md").write_text("z" * 20000, encoding="utf-8")
    monkeypatch.chdir(project)
    rc = main([
        "open", "--brokered", "--root", str(project / "collab"),
        "--label", "market-research", "--author-vendor", "claude",
        "--docket-file", "big-docket.md",
    ])
    assert rc == 1
    printed = capsys.readouterr().err
    assert "1  claude/opus + deepseek/pro" in printed
    assert "full review, strongest pair" in printed
