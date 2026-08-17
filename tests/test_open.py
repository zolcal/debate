"""Slice 3: `debate open` -- mint a debate with its pair picked at birth."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from debate import channel, opening, seats
from debate.__main__ import _watcher_config, main


def _registry_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "seats.json"
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(path))
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
        assume_yes=True, ask=_no_ask,
    )
    assert pair == ("alpha/one", "beta/two")


def test_pick_pair_absent_seat_refused(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    reg.seats["alpha/one"].present = False
    with pytest.raises(channel.ChannelError, match="alpha/one"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
            assume_yes=True, ask=_no_ask,
        )


def test_pick_pair_unknown_seat_refused(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    with pytest.raises(channel.ChannelError, match="gamma/three"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("gamma/three", "beta/two"),
            assume_yes=True, ask=_no_ask,
        )


def test_pick_pair_unsmoked_needs_confirmation_yes_covers(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    reg.seats["alpha/one"].smoke = None
    # --yes covers the unsmoked warning...
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
        assume_yes=True, ask=_no_ask,
    )
    assert pair == ("alpha/one", "beta/two")
    # ...interactively it asks, and a refusal answer refuses.
    answers = iter(["n"])
    with pytest.raises(channel.ChannelError, match="unsmoked"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
            assume_yes=False, ask=lambda prompt: next(answers),
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
            assume_yes=True, ask=_no_ask,
        )
    # same vendor/submodel at two DIFFERENT efforts: the warning fires all the
    # same -- effort ignored, same weights
    with pytest.raises(channel.ChannelError, match="weights|identical|monologue"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "alpha/one@low"),
            assume_yes=True, ask=_no_ask,
        )
    # --allow-identical-seats covers vendor/submodel identity...
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "alpha/one@low"),
        assume_yes=True, ask=_no_ask, allow_identical=True,
    )
    assert pair == ("alpha/one", "alpha/one@low")
    # ...but identical SELECTED argv refuses ALWAYS.
    reg.seats["alpha/clone"] = _seat("alpha/clone", [str(tool), "{prompt}"], smoke=_smoked())
    with pytest.raises(channel.ChannelError, match="argv"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=("alpha/one", "alpha/clone"),
            assume_yes=True, ask=_no_ask, allow_identical=True,
        )


def test_pick_pair_default_from_last_pair(tmp_path: Path) -> None:
    reg = _two_seat_registry(tmp_path)
    reg.last_pair[str(tmp_path)] = ["alpha/one", "beta/two"]
    # Enter accepts the project default
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=None,
        assume_yes=False, ask=lambda prompt: "",
    )
    assert pair == ("alpha/one", "beta/two")
    # a default containing an unseatable seat is DROPPED, not offered; with
    # --yes and no usable default: refuse
    reg.seats["alpha/one"].present = False
    with pytest.raises(channel.ChannelError, match="default"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=None,
            assume_yes=True, ask=_no_ask,
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
            assume_yes=True, ask=_no_ask,
        )
    # allowlisted pair passes
    pair = opening.pick_pair(
        reg, project=str(tmp_path), requested=("alpha/one", "beta/two"),
        assume_yes=True, ask=_no_ask,
    )
    assert pair == ("alpha/one", "beta/two")
    # a last_pair default outside the allowlist is DROPPED (no default offered)
    reg.last_pair[str(tmp_path)] = ["gamma/three", "beta/two"]
    with pytest.raises(channel.ChannelError, match="default"):
        opening.pick_pair(
            reg, project=str(tmp_path), requested=None, assume_yes=True, ask=_no_ask,
        )
    # the interactive listing shows only allowlisted seats
    prompts: list[str] = []

    def capture(prompt: str) -> str:
        prompts.append(prompt)
        return "alpha/one,beta/two"

    opening.pick_pair(reg, project=str(tmp_path), requested=None, assume_yes=False, ask=capture)
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
