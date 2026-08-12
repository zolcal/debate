"""`debate setup` — Slices 1-3 of docs/plans/2026-08-04-setup-wizard.md."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from debate import channel, setup
from debate.__main__ import _watcher_config, main

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _defaults_in_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEBATE_SETUP_DEFAULTS", str(tmp_path / "cache" / "defaults.json"))


def make_channel(tmp_path: Path, label: str = "proj") -> tuple[Path, str]:
    root = tmp_path / "collab"
    root.mkdir(exist_ok=True)
    name = channel.generate_channel_id(root, label=label)
    channel.init_channel(root, ("alpha", "beta"), "owner", 12, name=name)
    return root, name


def seat_script(tmp_path: Path) -> Path:
    script = tmp_path / "seat.sh"
    script.write_text("#!/bin/sh\nexit 0\n")
    script.chmod(0o755)
    return script


def spec_for(root: Path, name: str, tmp_path: Path,
             commands: dict[str, list[str] | None]) -> setup.SetupSpec:
    return setup.SetupSpec(
        channel_root=root, channel_name=name, parties=("alpha", "beta"),
        commands=commands,
        config_path=tmp_path / f"{name}.watcher.json",
        state_path=tmp_path / "state" / f"{name}.json",
        thread_cap=12,
    )


def test_apply_watcher_driven_pair_round_trips_the_real_loader(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": [str(script), "{prompt}"], "beta": [str(script), "{prompt}"]})
    written = setup.apply(spec, load_config_fn=_watcher_config)
    config = json.loads(spec.config_path.read_text())
    assert set(config["commands"]) == {"alpha", "beta"}
    for party, prompt in config["prompts"].items():
        assert f"turn=='{party}'" in prompt
        assert "--channel {channel_name}" in prompt
        assert "{channel_root}/PROTOCOL.md" in prompt
        assert "END" in prompt  # review-append clause present
    loaded = _watcher_config(root, spec.config_path, name)
    assert loaded.command_for("alpha") is not None
    assert spec.config_path in written


def test_human_seat_on_managed_channel_refuses_at_setup_time(tmp_path: Path) -> None:
    """MSG-32: managed v1 needs a command per party; the config the watcher
    would call INVALID must refuse at setup, in the watcher's own words."""
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": None, "beta": [str(script), "{prompt}"]})
    with pytest.raises(channel.ChannelError, match="INVALID.*missing adapter command"):
        setup.apply(spec, load_config_fn=_watcher_config)
    assert not spec.config_path.exists()
    assert not spec.state_path.parent.exists(), "no write on refusal, not even a dir"


def test_inlined_credential_is_refused(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": ["run", "--api-key=sk-abcdef0123456789abcdef"], "beta": None})
    with pytest.raises(channel.ChannelError, match="wrapper"):
        setup.apply(spec, load_config_fn=_watcher_config)
    assert not spec.config_path.exists()


def test_flag_form_credential_is_refused_too(tmp_path: Path) -> None:
    """MSG-37: `agent --token VALUE` is two argv elements; the flag element
    alone must trip the guard."""
    root, name = make_channel(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": ["agent", "--token", "some-value"], "beta": None})
    with pytest.raises(channel.ChannelError, match="wrapper"):
        setup.apply(spec, load_config_fn=_watcher_config)
    assert not spec.config_path.exists()


def test_state_path_inside_channel_root_is_refused_at_setup_time(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    spec = spec_for(root, name, tmp_path, {"alpha": [str(script)], "beta": None})
    spec.state_path = root / "state.json"
    with pytest.raises(channel.ChannelError, match="state"):
        setup.apply(spec, load_config_fn=_watcher_config)
    assert not spec.config_path.exists(), "nothing written when validation fails"
    assert not list(spec.config_path.parent.glob(".*setup-probe*")), "no probe residue"


def test_unresolvable_command_is_refused_before_any_write(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": ["/nonexistent/agent-binary"], "beta": None})
    with pytest.raises(channel.ChannelError, match="neither on PATH"):
        setup.apply(spec, load_config_fn=_watcher_config)
    assert not spec.config_path.exists()


def test_protocol_scaffolded_when_absent_and_never_clobbered(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": [str(script)], "beta": [str(script)]})
    spec.thread_cap = 9
    setup.apply(spec, load_config_fn=_watcher_config)
    text = (root / "PROTOCOL.md").read_text()
    assert "[9]" in text and "[12]" not in text.split("\n\n")[0] or "[9]" in text
    (root / "PROTOCOL.md").write_text("owner-edited")
    spec2 = spec_for(root, name, tmp_path,
                    {"alpha": [str(script)], "beta": [str(script)]})
    spec2.config_path = tmp_path / "second.watcher.json"
    setup.apply(spec2, load_config_fn=_watcher_config)
    assert (root / "PROTOCOL.md").read_text() == "owner-edited"


def test_packaged_template_matches_repo_protocol() -> None:
    assert setup.protocol_template() == (REPO / "PROTOCOL.md").read_text(encoding="utf-8")


def test_defaults_round_trip_and_second_run_offers_them(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    spec = spec_for(root, name, tmp_path,
                    {"alpha": [str(script), "{prompt}"], "beta": [str(script), "{prompt}"]})
    setup.apply(spec, load_config_fn=_watcher_config)

    asked: list[str] = []

    def fake_ask(prompt: str) -> str:
        asked.append(prompt)
        return ""  # Enter: accept the remembered answers

    spec2 = setup.interview(
        channel_root=root, channel_name=name, parties=("alpha", "beta"),
        thread_cap=12, project=None, flag_commands={}, assume_yes=False,
        ask=fake_ask)
    assert len(asked) == 1 and "remembered from channel" in asked[0]
    assert name in asked[0]  # provenance shown (glm MSG-36 note ii)
    assert spec2.commands == {"alpha": [str(script), "{prompt}"],
                              "beta": [str(script), "{prompt}"]}


def test_yes_without_defaults_or_flags_refuses(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    with pytest.raises(channel.ChannelError, match="--yes"):
        setup.interview(
            channel_root=root, channel_name=name, parties=("alpha", "beta"),
            thread_cap=12, project=None, flag_commands={}, assume_yes=True)


def test_end_to_end_cli_yes_flags_status_and_config_load(tmp_path: Path,
                                                        capsys: pytest.CaptureFixture[str],
                                                        monkeypatch: pytest.MonkeyPatch) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    # HOME steers expanduser on POSIX; Windows uses USERPROFILE. Set both so
    # the derived state dir stays inside the test tree on every CI lane.
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    code = main([
        "setup", "--root", str(root), "--channel", name,
        "--command", f"alpha={script} {{prompt}}",
        "--command", f"beta={script} {{prompt}}", "--yes",
    ])
    assert code in (0, None)
    out = capsys.readouterr().out
    assert "wrote" in out and "hint:" in out
    # The config lands at the DERIVED toplevel (the channel's recorded project
    # -- here the enclosing repo, since tmp_path lives inside it). Read the
    # actual path from the wizard's own output rather than re-deriving.
    config_path = Path(next(line.split(" ", 1)[1] for line in out.splitlines()
                            if line.startswith("wrote ") and line.endswith(".watcher.json")))
    assert config_path.exists()
    config_path_cleanup = config_path
    loaded = _watcher_config(root, config_path, name)
    argv = loaded.command_for("alpha")
    assert argv is not None and name in " ".join(argv)  # {channel_name} expanded
    assert main(["status", "--root", str(root), "--channel", name]) in (0, None)
    config_path_cleanup.unlink()  # derived toplevel may be the real repo root


def test_two_channels_refuse_without_channel_flag(tmp_path: Path,
                                                  capsys: pytest.CaptureFixture[str]) -> None:
    root, name1 = make_channel(tmp_path, label="one")
    name2 = channel.generate_channel_id(root, label="two")
    channel.init_channel(root, ("alpha", "beta"), "owner", 12, name=name2)
    script = seat_script(tmp_path)
    assert main(["setup", "--root", str(root),
                 "--command", f"alpha={script} {{prompt}}",
                 "--command", f"beta={script} {{prompt}}", "--yes"]) == 1
    err = capsys.readouterr().err
    assert name1 in err and name2 in err  # refusal names both channels
    assert main(["setup", "--root", str(root), "--channel", name1,
                 "--command", f"alpha={script} {{prompt}}",
                 "--command", f"beta={script} {{prompt}}", "--yes"]) == 0
    out = capsys.readouterr().out
    for line in out.splitlines():  # derived toplevel may be the real repo root
        if line.startswith("wrote ") and line.endswith(".watcher.json"):
            Path(line.split(" ", 1)[1]).unlink()


def test_brokered_channel_is_refused_with_pointer(tmp_path: Path,
                                                  capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "collab"
    root.mkdir()
    name = channel.generate_channel_id(root, label="v2")
    channel.init_channel(root, ("alpha", "beta"), "owner", 12, name=name,
                         managed_version=channel.BROKERED_MANAGED_VERSION)
    assert main(["setup", "--root", str(root), "--channel", name, "--yes",
                 "--human", "alpha", "--human", "beta"]) == 1
    err = capsys.readouterr().err
    assert "adapter-doctor" in err


def test_prompt_without_placeholder_is_left_untouched(tmp_path: Path) -> None:
    from debate.watcher import WatcherConfig
    root, name = make_channel(tmp_path)
    config = WatcherConfig(
        channel_root=root, state_path=tmp_path / "s.json",
        commands={"alpha": ["run", "{prompt}"]},
        prompts={"alpha": "no placeholders here"},
        channel_name=name)
    argv = config.command_for("alpha")
    assert argv == ["run", "no placeholders here"]


# ---- Slice 2: the smoke ----------------------------------------------------

def replying_seat(tmp_path: Path, party: str = "alpha") -> list[str]:
    """A fake seat honoring the real contract, portable across CI lanes:
    parse the channel address out of the pinned prompt, find the open thread
    from the doorbell, post a well-formed reply via the CLI."""
    src = Path(__file__).resolve().parents[1] / "src"
    script = tmp_path / f"reply-{party}.py"
    script.write_text(f"""import json, os, re, subprocess, sys
prompt = sys.argv[1]
root = re.search(r"--root (\\S+)", prompt).group(1)
chan = re.search(r"--channel ([A-Za-z0-9-]+)", prompt).group(1)
sig = json.load(open(os.path.join(root, chan + ".signal.json"), encoding="utf-8"))
env = dict(os.environ, PYTHONPATH={str(src)!r})
subprocess.run([sys.executable, "-m", "debate", "post", "--root", root,
                "--channel", chan, "--from", {party!r}, "--type", "info",
                "--thread", sig["thread"], "--body", "pong"], env=env, check=True)
""")
    return [sys.executable, str(script), "{prompt}"]


def smoke_spec(root: Path, name: str, tmp_path: Path,
               commands: dict[str, list[str] | None]) -> setup.SetupSpec:
    spec = spec_for(root, name, tmp_path, commands)
    return spec


def test_smoke_passes_with_a_wellformed_fake_seat(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    argv = replying_seat(tmp_path)
    spec = smoke_spec(root, name, tmp_path, {"alpha": argv, "beta": None})
    lines: list[str] = []
    failures = setup.smoke(spec, scratch_base=tmp_path, emit=lines.append)
    assert failures == []
    assert any("PASS" in line for line in lines)
    assert any("ONE model call" in line for line in lines), "spend printed before spending"
    assert any("NOT consistency" in line for line in lines), "limits stated plainly"
    assert not list(tmp_path.glob("debate-smoke-*")), "scratch removed"


def test_smoke_fails_loudly_for_prose_echo_and_silent_seats(tmp_path: Path) -> None:
    prose = tmp_path / "prose.py"
    prose.write_text("print('sure, I will get right on that')\n")
    silent = tmp_path / "silent.py"
    silent.write_text("pass\n")
    root, name = make_channel(tmp_path)
    spec = smoke_spec(root, name, tmp_path,
                      {"alpha": [sys.executable, str(prose), "{prompt}"],
                       "beta": [sys.executable, str(silent), "{prompt}"]})
    failures = setup.smoke(spec, scratch_base=tmp_path, emit=lambda _line: None)
    assert len(failures) == 2
    assert all("no reply landed" in reason for reason in failures)
    assert any("sure, I will" in reason for reason in failures), "output tail shown"
    assert not list(tmp_path.glob("debate-smoke-*"))


# ---- Slice 3: the scheduler ------------------------------------------------

def test_scheduler_units_content(tmp_path: Path) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    spec = spec_for(root, name, tmp_path, {"alpha": [str(script)], "beta": [str(script)]})
    units = setup.scheduler_units(spec)
    service = units[f"debate-watch-{name}.service"]
    timer = units[f"debate-watch-{name}.timer"]
    assert f"ExecStart={sys.executable} -m debate watch-once" in service
    assert f"--channel {name}" in service
    assert str(spec.config_path.resolve()) in service
    assert "WorkingDirectory=" in service and "Environment=PYTHONPATH=" in service
    assert f"SyslogIdentifier=debate-watch-{name}" in service
    assert "OnUnitActiveSec=1min" in timer and "WantedBy=timers.target" in timer
    assert f"--channel {name}" in units["cron"]
    for text in units.values():
        assert "sk-" not in text and "token" not in text.lower(), "no inline keys"


def test_scheduler_prints_but_never_runs(tmp_path: Path,
                                         capsys: pytest.CaptureFixture[str],
                                         monkeypatch: pytest.MonkeyPatch) -> None:
    root, name = make_channel(tmp_path)
    script = seat_script(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    code = main([
        "setup", "--root", str(root), "--channel", name,
        "--command", f"alpha={script} {{prompt}}",
        "--command", f"beta={script} {{prompt}}", "--yes", "--scheduler",
    ])
    assert code == 0
    out = capsys.readouterr().out
    assert f"~/.config/systemd/user/debate-watch-{name}.service" in out
    assert "not run for you" in out and "cron line:" in out
    for line in out.splitlines():
        if line.startswith("wrote ") and line.endswith(".watcher.json"):
            Path(line.split(" ", 1)[1]).unlink()
