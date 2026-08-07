"""`watcher.json` is hand-authored, so a typo must refuse, not traceback.

Found at MSG-172 while probing the same unguarded-read pattern that produced
three fixes in the verify slice (doorbell, mailbox, state file). This one was
ruled outside that slice on a real distinction - it dies in `main()` BEFORE the
tick, and unlike those three the config is never written by the program, so it
has no self-corruption trigger - but it is still a crash-loop under the 60s
timer, reachable by a hand-edit typo, and it hits `watch`, `watch-once` AND
`watch-status` alike.

`main()` converts `ChannelError` and nothing else, so every other exception
escapes as a traceback and exit 1. The fix is to refuse in that vocabulary, the
same way `WatcherConfig.__post_init__` already does for a state_path inside the
channel root and for non-string argv elements.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import _watcher_config


def make_channel(tmp_path: Path) -> Path:
    root = tmp_path / "ch"
    root.mkdir()
    channel.init_channel(root, parties=("alice", "bob"), supervisor="owner")
    return root


def valid_config(tmp_path: Path) -> dict[str, object]:
    return {
        "state_path": str(tmp_path / "state" / "w.json"),
        "commands": {"bob": ["/bin/echo", "{prompt}"]},
        "prompts": {"bob": "go"},
        "debounce_seconds": {"bob": 0},
        "retry_seconds": 1800,
        "timeout_seconds": 1800,
    }


def write_config(tmp_path: Path, payload: object) -> Path:
    path = tmp_path / "watcher.json"
    if isinstance(payload, (dict, list, int, float, bool)) or payload is None:
        path.write_text(json.dumps(payload), encoding="utf-8")
    else:
        path.write_text(str(payload), encoding="utf-8")
    return path


def test_a_valid_config_still_loads(tmp_path: Path) -> None:
    """Over-refusal guard: the strictness must not reject a real config."""
    root = make_channel(tmp_path)
    path = write_config(tmp_path, valid_config(tmp_path))

    config = _watcher_config(root, path)

    assert config.commands == {"bob": ["/bin/echo", "{prompt}"]}
    assert config.retry_seconds == 1800


def test_named_managed_channel_binds_both_arbitrary_party_commands(tmp_path: Path) -> None:
    root = tmp_path / "ch"
    channel.init_channel(root, parties=("kimi", "glm"), supervisor="owner", name="pair-11111")
    raw = valid_config(tmp_path)
    raw["commands"] = {"kimi": ["kimi", "-p"], "glm": ["glm-agent"]}
    path = write_config(tmp_path, raw)

    config = _watcher_config(root, path, "pair-11111")

    assert config.managed_version == 1
    assert config.parties == ("kimi", "glm")
    assert config.managed_problem() is None


def test_the_shipped_example_config_still_loads(tmp_path: Path) -> None:
    """The repo's own watcher.example.json must survive the new validation.

    It is the file the README tells a stranger to copy, so if the guard is too
    strict this is where it shows up.
    """
    example = Path(__file__).resolve().parent.parent / "watcher.example.json"
    if not example.exists():
        pytest.skip("no example config in this checkout")
    root = tmp_path / "ch"
    channel.init_channel(root, parties=("claude", "glm"), supervisor="owner", name="example-11111")

    config = _watcher_config(root, example, "example-11111")

    assert config.prompts, "the example must still yield prompts"
    assert all(
        f"--channel {config.state_path.stem}" in prompt for prompt in config.prompts.values()
    ), "the state stem must identify the channel in every pinned prompt"
    assert config.managed_problem() is None


def test_missing_config_file_refuses(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    with pytest.raises(channel.ChannelError) as excinfo:
        _watcher_config(root, tmp_path / "nope.json")
    assert "nope.json" in str(excinfo.value)


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param("{ torn", id="torn-json"),
        pytest.param("42", id="int"),
        pytest.param("null", id="null"),
        pytest.param("[1,2,3]", id="list"),
        pytest.param('"a string"', id="string"),
        pytest.param("true", id="bool"),
    ],
)
def test_non_object_or_unparseable_config_refuses(tmp_path: Path, payload: str) -> None:
    root = make_channel(tmp_path)
    path = tmp_path / "watcher.json"
    path.write_text(payload, encoding="utf-8")

    with pytest.raises(channel.ChannelError):
        _watcher_config(root, path)


def test_non_utf8_config_refuses(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    path = tmp_path / "watcher.json"
    path.write_bytes(b"\xff\xfe not utf8")

    with pytest.raises(channel.ChannelError):
        _watcher_config(root, path)


def test_missing_state_path_refuses_and_names_the_key(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    raw = valid_config(tmp_path)
    del raw["state_path"]
    path = write_config(tmp_path, raw)

    with pytest.raises(channel.ChannelError) as excinfo:
        _watcher_config(root, path)

    assert "state_path" in str(excinfo.value), "the refusal must name the missing key"


@pytest.mark.parametrize("key", ["retry_seconds", "timeout_seconds"])
def test_non_numeric_duration_refuses(tmp_path: Path, key: str) -> None:
    root = make_channel(tmp_path)
    raw = valid_config(tmp_path)
    raw[key] = "30m"
    path = write_config(tmp_path, raw)

    with pytest.raises(channel.ChannelError) as excinfo:
        _watcher_config(root, path)

    assert key in str(excinfo.value)


def test_non_numeric_debounce_refuses(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    raw = valid_config(tmp_path)
    raw["debounce_seconds"] = {"bob": "soon"}
    path = write_config(tmp_path, raw)

    with pytest.raises(channel.ChannelError):
        _watcher_config(root, path)


@pytest.mark.parametrize("key", ["commands", "prompts", "debounce_seconds"])
def test_non_mapping_sections_refuse(tmp_path: Path, key: str) -> None:
    """I hit this one by accident: `debounce_seconds: 0` gave AttributeError."""
    root = make_channel(tmp_path)
    raw = valid_config(tmp_path)
    raw[key] = 0
    path = write_config(tmp_path, raw)

    with pytest.raises(channel.ChannelError) as excinfo:
        _watcher_config(root, path)

    assert key in str(excinfo.value)


def test_command_given_as_a_string_refuses_instead_of_splitting_into_letters(tmp_path: Path) -> None:
    """`list("echo hi")` silently becomes ['e','c','h','o',...].

    Every element is a str, so WatcherConfig's all-strings check passes and the
    failure surfaces only at exec time as a baffling error. Refuse at load.
    """
    root = make_channel(tmp_path)
    raw = valid_config(tmp_path)
    raw["commands"] = {"bob": "/bin/echo hi"}
    path = write_config(tmp_path, raw)

    with pytest.raises(channel.ChannelError) as excinfo:
        _watcher_config(root, path)

    message = str(excinfo.value)
    assert "bob" in message
    assert "list" in message.lower(), f"the refusal should say it wants a list, got: {message}"


def test_empty_command_list_refuses(tmp_path: Path) -> None:
    """An empty argv is silently treated as 'no command' - a party that looks
    configured but can never be invoked."""
    root = make_channel(tmp_path)
    raw = valid_config(tmp_path)
    raw["commands"] = {"bob": []}
    path = write_config(tmp_path, raw)

    with pytest.raises(channel.ChannelError):
        _watcher_config(root, path)


@pytest.mark.parametrize("command", ["watch-once", "watch-status", "watch"])
@pytest.mark.parametrize("corruption", ["missing", "torn", "missing-supervisor"])
def test_named_channel_record_refuses_cleanly_without_legacy_fallback(
    tmp_path: Path, command: str, corruption: str
) -> None:
    root = tmp_path / "ch"
    name = "pair-11111"
    channel.init_channel(root, parties=("alice", "bob"), supervisor="owner", name=name)
    record = root / f"{name}.debate.json"
    if corruption == "missing":
        record.unlink()
    elif corruption == "torn":
        record.write_text("{ torn", encoding="utf-8")
    else:
        record.write_text('{"parties": ["alice", "bob"]}', encoding="utf-8")
    watcher_config = write_config(tmp_path, valid_config(tmp_path))

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "debate",
            command,
            "--root",
            str(root),
            "--channel",
            name,
            "--config",
            str(watcher_config),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert "Traceback" not in proc.stderr, proc.stderr
    assert proc.returncode != 0
    assert "refused" in (proc.stdout + proc.stderr).lower(), (proc.stdout, proc.stderr)


def test_named_watcher_refuses_a_missing_channel_record_instead_of_going_manual(tmp_path: Path) -> None:
    root = tmp_path / "ch"
    name = "pair-11111"
    channel.init_channel(root, parties=("alice", "bob"), supervisor="owner", name=name)
    (root / f"{name}.debate.json").unlink()

    with pytest.raises(channel.ChannelError, match="channel config"):
        from debate.watcher import WatcherConfig

        WatcherConfig(
            channel_root=root,
            channel_name=name,
            state_path=tmp_path / "state.json",
            commands={"alice": ["agent"], "bob": ["agent"]},
        )


def test_legacy_watcher_refuses_an_unreadable_channel_record(tmp_path: Path) -> None:
    root = tmp_path / "ch"
    channel.init_channel(root, parties=("alice", "bob"), supervisor="owner")
    (root / "debate.json").write_text("{ torn", encoding="utf-8")

    with pytest.raises(channel.ChannelError, match="unreadable channel config"):
        from debate.watcher import WatcherConfig

        WatcherConfig(
            channel_root=root,
            state_path=tmp_path / "state.json",
            commands={"alice": ["agent"]},
        )


# --- end to end: no traceback from any watcher subcommand ------------------


@pytest.mark.parametrize("command", ["watch-once", "watch-status"])
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param("{ torn", id="torn-json"),
        pytest.param("42", id="int"),
        pytest.param("[1,2,3]", id="list"),
        pytest.param("null", id="null"),
        pytest.param("{}", id="no-state-path"),
    ],
)
def test_cli_refuses_cleanly_without_a_traceback(tmp_path: Path, command: str, payload: str) -> None:
    root = make_channel(tmp_path)
    path = tmp_path / "watcher.json"
    path.write_text(payload, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "-m", "debate", command, "--root", str(root), "--config", str(path)],
        capture_output=True, text=True, timeout=60,
    )

    assert "Traceback" not in proc.stderr, proc.stderr
    assert proc.returncode != 0, "a bad config must still fail"
    assert "refused" in (proc.stdout + proc.stderr).lower(), (proc.stdout, proc.stderr)


def test_cli_refuses_a_missing_config_without_a_traceback(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    proc = subprocess.run(
        [sys.executable, "-m", "debate", "watch-once", "--root", str(root),
         "--config", str(tmp_path / "absent.json")],
        capture_output=True, text=True, timeout=60,
    )
    assert "Traceback" not in proc.stderr, proc.stderr
    assert proc.returncode != 0
