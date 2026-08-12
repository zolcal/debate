"""``debate setup`` — wire the two seats of a channel that already exists.

Plan: docs/plans/2026-08-04-setup-wizard.md (APPROVED MSG-36). `init` scaffolds
the channel skeleton; everything that makes two agents actually argue — the
watcher config, the pinned prompts, the channel's PROTOCOL.md — was hand-rolled,
and that step is where this project's own expensive mistakes lived. The wizard
moves that failure surface into the tool.

Shape pinned at review: ``interview() -> SetupSpec`` (terminal I/O only) and
``apply(spec) -> [written paths]`` (validation, then writes), a plain dataclass
in the middle. Unit tests drive ``apply`` from fixture specs; nothing needs a
pty.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import tempfile
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Callable

from . import channel
from .watcher import WatcherConfig

# The six incident-driven clauses of the live prompts, none optional (§2.4):
# the two-gate check (non-empty thread AND turn), fresh evidence, read via
# `debate read`, review-append-at-END, post-then-stop — plus PROTOCOL.md first
# and explicit --root/--channel addressing so the prompt stays correct the day
# a second channel shares the folder.
PROMPT_TEMPLATE = (
    "It is your turn as '{party}' on the debate channel {channel_name}. "
    "First read {channel_root}/PROTOCOL.md. Then read ONLY the open thread via "
    "`debate read --root {channel_root} --channel {channel_name}` -- never the whole "
    "mailbox. Immediately before acting, verify {channel_root}/{channel_name}.signal.json "
    "still shows a NON-EMPTY thread AND turn=='{party}' -- if either fails, exit without "
    "posting. Act on what the thread asks: for verdicts cite YOUR OWN fresh evidence "
    "(your own checkout, your own runs), never evidence quoted from the request. When "
    "reviewing a plan document, append your review as a dated section at the END of the "
    "document -- never edit its body. Post via `debate post --root {channel_root} "
    "--channel {channel_name} --from {party}`, then stop."
)

DEFAULTS_PATH = Path("~/.config/debate/setup-defaults.json")

# A guard against the obvious accident, not a scanner: seat credentials belong
# in a self-sourcing wrapper (§2.5); nothing key-shaped may reach the config.
SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|token|secret|bearer|passwd|password|credential"
    r"|sk-[a-z0-9]{16,})")


@dataclass
class SetupSpec:
    """Everything ``apply`` needs, and nothing it has to go ask for."""

    channel_root: Path
    channel_name: str
    parties: tuple[str, ...]
    commands: dict[str, list[str] | None]  # None = human-driven seat
    config_path: Path
    state_path: Path
    thread_cap: int
    debounce_seconds: dict[str, int] = field(default_factory=dict)
    retry_seconds: int = 1800
    timeout_seconds: int = 1800
    overwrite: bool = False


def split_argv(text: str) -> list[str]:
    """Windows paths carry backslashes; POSIX shlex eats them (C:\\Users ->
    C:Users) and the mangled head then fails the executable check. Non-POSIX
    mode keeps them; quoting still works for the space-in-path case."""
    return shlex.split(text, posix=os.name != "nt")


def defaults_path() -> Path:
    return Path(os.environ.get("DEBATE_SETUP_DEFAULTS", str(DEFAULTS_PATH))).expanduser()


def load_defaults() -> dict[str, object]:
    try:
        raw = json.loads(defaults_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return raw if isinstance(raw, dict) else {}


def store_defaults(spec: SetupSpec) -> Path:
    """Remember the last answers — a defaults cache, deliberately not a registry.

    The provenance channel is stored so the next run can SHOW where a suggested
    command came from ("glm" here may not be "glm" elsewhere); it stays a
    suggestion the operator confirms, never a claim about what a seat is.
    """
    path = defaults_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "channel": spec.channel_name,
        "commands": spec.commands,
        "debounce_seconds": spec.debounce_seconds,
        "retry_seconds": spec.retry_seconds,
        "timeout_seconds": spec.timeout_seconds,
    }, indent=2), encoding="utf-8")
    return path


def derive_paths(root: Path, name: str, project: Path | None) -> tuple[Path, Path]:
    """(config_path, state_path) — derived, never asked (§2.2).

    The watcher config lands at the repo toplevel (the recorded project when the
    channel carries one, else the channel folder's parent — the same two-tier
    rule as `_derived_project`). The state stem is the channel id; the
    foreign-stamp guard for a cross-root id collision is TICK-time
    (`_verify_channel_binding`), not a setup-time check (glm MSG-36, note i).
    """
    toplevel = project if project is not None else root.resolve().parent
    config_path = toplevel / f"{name}.watcher.json"
    state_path = Path("~/.local/state/debate").expanduser() / f"{name}.json"
    return config_path, state_path


def build_prompt(party: str) -> str:
    """The pinned template with the party baked in; the channel placeholders
    stay for `command_for`'s single-pass expansion. The party name is embedded
    because the sender and turn checks are exact equality — hand-editing the
    channel's parties afterwards makes this seat exit every turn."""
    return PROMPT_TEMPLATE.replace("{party}", party)


def protocol_template() -> str:
    return (resources.files("debate") / "protocol_template.md").read_text(encoding="utf-8")


def scaffold_protocol(root: Path, thread_cap: int) -> Path | None:
    """Copy the packaged PROTOCOL template in — ONLY if absent, never clobbered.

    The pinned prompt's first instruction is to read it and `init` does not
    create it, so without this a first-time user's seat fails at its first
    step. The thread-cap bracket is filled from the channel config; the
    [main]/load-bearing brackets stay for the user (R2 precision note 4).
    """
    target = root / "PROTOCOL.md"
    if target.exists():
        return None
    text = protocol_template().replace("[12]", f"[{thread_cap}]", 1)
    target.write_text(text, encoding="utf-8")
    return target


def validate(spec: SetupSpec) -> None:
    """Every check, before anything is written (§2.6)."""
    for party, argv in spec.commands.items():
        if party not in spec.parties:
            raise channel.ChannelError(
                f"refused: {party!r} is not a party of channel {spec.channel_name!r} "
                f"(parties: {', '.join(spec.parties)})")
        if argv is None:
            continue
        if not argv:
            raise channel.ChannelError(f"refused: empty command for {party!r}")
        for part in argv:
            if SECRET_PATTERN.search(part):
                raise channel.ChannelError(
                    f"refused: the command for {party!r} looks like it carries a "
                    f"credential; keys never reach the config -- use a "
                    f"self-sourcing wrapper (plan section 2.5)")
        head = argv[0]
        resolved = shutil.which(head)
        if resolved is None:
            candidate = Path(head).expanduser()
            if not (candidate.is_file() and os.access(candidate, os.X_OK)):
                raise channel.ChannelError(
                    f"refused: {party!r} command {head!r} is neither on PATH nor an "
                    f"existing executable file")
    if spec.config_path.exists() and not spec.overwrite:
        raise channel.ChannelError(
            f"refused: {spec.config_path} exists; re-run confirming the overwrite "
            f"(or pass --yes)")
    # Creatable is CHECKED here, created only in the write phase — validation
    # writes nothing, not even a directory (gate finding, MSG-33).
    ancestor = spec.state_path.parent
    while not ancestor.exists():
        if ancestor.parent == ancestor:
            break
        ancestor = ancestor.parent
    if not os.access(ancestor, os.W_OK):
        raise channel.ChannelError(
            f"refused: state directory {spec.state_path.parent} is not creatable "
            f"({ancestor} is not writable)")


def apply(spec: SetupSpec,
          load_config_fn: Callable[[Path, Path, str | None], WatcherConfig]) -> list[Path]:
    """Validate, round-trip the assembled config through the real loader, then
    write. Returns the written paths. Nothing is written until every check
    passes; the round-trip makes `WatcherConfig.__post_init__`'s refusals
    (state inside the channel root, foreign binding) fire at setup time, not at
    the first scheduler tick."""
    validate(spec)
    config = {
        "state_path": str(spec.state_path),
        "commands": {p: argv for p, argv in spec.commands.items() if argv},
        "prompts": {p: build_prompt(p) for p, argv in spec.commands.items() if argv},
        "debounce_seconds": {p: spec.debounce_seconds.get(p, 0)
                             for p, argv in spec.commands.items() if argv},
        "retry_seconds": spec.retry_seconds,
        "timeout_seconds": spec.timeout_seconds,
    }
    # The probe lives in a scratch dir OUTSIDE every target path, so a loader
    # refusal leaves the project byte-untouched (gate finding, MSG-33). The
    # loader is REQUIRED -- an optional one made this whole gate skippable by
    # default (gate finding, MSG-36 F1).
    with tempfile.TemporaryDirectory(prefix="debate-setup-") as scratch:
        probe = Path(scratch) / spec.config_path.name
        probe.write_text(json.dumps(config, indent=2), encoding="utf-8")
        loaded = load_config_fn(spec.channel_root, probe, spec.channel_name or None)
    # The object that already knows one definition of validity gets asked at
    # setup time, not at the first scheduler tick (gate finding, MSG-32): a
    # managed channel needs a command for every party, so a "human-driven"
    # seat -- the plan's pre-managed pattern -- refuses here.
    problem = loaded.managed_problem()
    if problem is not None:
        raise channel.ChannelError(
            f"refused: this configuration would be INVALID to the watcher -- "
            f"{problem}. Managed channels need a watcher command for every "
            f"party; the human-driven seat is the legacy/unmanaged pattern.")

    written: list[Path] = []
    spec.state_path.parent.mkdir(parents=True, exist_ok=True)
    spec.config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    written.append(spec.config_path)
    scaffolded = scaffold_protocol(spec.channel_root, spec.thread_cap)
    if scaffolded is not None:
        written.append(scaffolded)
    written.append(store_defaults(spec))
    return written


def interview(*, channel_root: Path, channel_name: str, parties: tuple[str, ...],
              thread_cap: int, project: Path | None,
              flag_commands: dict[str, list[str] | None],
              assume_yes: bool,
              ask: Callable[[str], str] = input) -> SetupSpec:
    """One question per party on a first run; one Enter on every run after.

    Flags ARE the interview: a party covered by --command/--human is never
    asked. --yes takes remembered defaults (or flag answers) without a prompt
    and refuses if neither covers a party — non-interactive means no guessing.
    """
    remembered = load_defaults()
    rem_commands_raw = remembered.get("commands")
    rem_commands: dict[str, object] = (
        dict(rem_commands_raw) if isinstance(rem_commands_raw, dict) else {})
    commands: dict[str, list[str] | None] = dict(flag_commands)

    open_parties = [p for p in parties if p not in commands]
    if open_parties and rem_commands and set(rem_commands) >= set(open_parties):
        lines = [f"Wire seats as last time?  (remembered from channel "
                 f"{remembered.get('channel', '?')})"]
        for p in open_parties:
            argv = rem_commands.get(p)
            shown = " ".join(str(a) for a in argv) if isinstance(argv, list) else "human-driven"
            lines.append(f"  {p:8} -> {shown}")
        answer = "y" if assume_yes else ask("\n".join(lines) + "\n[Y/n] ").strip().lower()
        if answer in ("", "y", "yes"):
            for p in open_parties:
                argv = rem_commands.get(p)
                commands[p] = [str(a) for a in argv] if isinstance(argv, list) else None
            open_parties = []

    if open_parties and assume_yes:
        raise channel.ChannelError(
            "refused: --yes with no remembered or flag-supplied answer for "
            + ", ".join(repr(p) for p in open_parties))
    for p in open_parties:
        raw = ask(f"Command for seat {p!r} (argv; empty = human-driven): ").strip()
        commands[p] = split_argv(raw) if raw else None

    config_path, state_path = derive_paths(channel_root, channel_name, project)
    rem_debounce_raw = remembered.get("debounce_seconds")
    debounce = {p: int(v) for p, v in rem_debounce_raw.items()
                if p in parties and isinstance(v, (int, float))} \
        if isinstance(rem_debounce_raw, dict) else {}
    retry_raw = remembered.get("retry_seconds")
    timeout_raw = remembered.get("timeout_seconds")
    return SetupSpec(
        channel_root=channel_root, channel_name=channel_name, parties=parties,
        commands=commands, config_path=config_path, state_path=state_path,
        thread_cap=thread_cap, debounce_seconds=debounce,
        retry_seconds=int(retry_raw) if isinstance(retry_raw, (int, float)) else 1800,
        timeout_seconds=int(timeout_raw) if isinstance(timeout_raw, (int, float)) else 1800,
        overwrite=assume_yes,
    )


def config_is_gitignored(path: Path) -> bool:
    """True when the enclosing repo already ignores the config. The wizard
    never edits .gitignore — it prints the exact line instead (§2.3)."""
    import subprocess

    try:
        proc = subprocess.run(
            ["git", "-C", str(path.parent), "check-ignore", "-q", str(path)],
            capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return True  # no git, nothing to hint about
    return proc.returncode == 0


def closing_hints(spec: SetupSpec, gitignored: bool) -> list[str]:
    hints = [
        f"scheduler unit name (convention, not installed): debate-watch-{spec.channel_name}",
        f"drive it: debate watch-once --root {spec.channel_root} "
        f"--channel {spec.channel_name} --config {spec.config_path}",
        "commit <id>.debate.json and PROTOCOL.md; the doorbell and lock stay gitignored",
    ]
    if not gitignored:
        hints.append(
            f"add to the repo .gitignore (not edited for you): {spec.config_path.name}")
    return hints
