"""The host seat registry: what this machine can seat, discovered honestly.

One registry per machine (~/.config/debate/seats.json). Discovery merges the
packaged catalog against PATH; it adds and marks, it never deletes -- a
vanished binary is history worth keeping, and manual entries belong to the
operator alone. Seat identity is ``vendor/submodel`` with an optional
``@effort``; per owner ruling 4 (plan, 2026-08-15) each seat carries ONE OR
MORE endpoint argvs and v1 selection is always the first-listed.
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import channel
from .seat_catalog import (
    CATALOG,
    CAPABILITY_CLASSES,
    KNOWN_CREDENTIAL_ENV_VARS,
    VENDOR_CONFIG_HOME_VARS,
)
from .setup import SECRET_PATTERN

REGISTRY_PATH = Path("~/.config/debate/seats.json")
REGISTRY_VERSION = 1

# Environment names the sandbox itself relies on -- a config_home declaration
# may never redirect one of these, on top of the controller's _RESERVED_ENV
# (checked separately, lazy-imported to avoid an import cycle).
SANDBOX_ENV: frozenset[str] = frozenset({
    "HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME", "TMPDIR",
    "TEMP", "TMP", "GIT_CEILING_DIRECTORIES", "PYTHONDONTWRITEBYTECODE",
    "PYTEST_DISABLE_PLUGIN_AUTOLOAD", "PYTEST_ADDOPTS", "PATH", "PYTHONPATH",
    "DEBATE_BRIDGE_REAL_HOME",
})

_CONFIG_HOME_VAR_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")
_DATA_POLICY_REVISION_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
DATA_POLICY_NOTICE_MAX_CHARS = 4096


@dataclass
class SmokeStatus:
    at: str
    result: str  # "pass" | "fail"


@dataclass
class Seat:
    seat_id: str
    vendor: str
    submodel: str
    effort: str | None
    commands: list[list[str]]  # endpoint options; v1 selection = commands[0]
    source: str  # "catalog" (discovery-owned) | "derived" (tool-derived
    # @effort entries, re-derived when their base argv moves) | "manual"
    # (operator-authored -- NEVER touched by the tool)
    present: bool
    smoke: SmokeStatus | None
    # Who pays when this seat runs. Declared, never guessed: the catalog
    # cannot know how a CLI is authenticated on THIS machine, so discovery
    # leaves "unknown" and the operator declares better via
    # `seats add --cost-mode`. Values mirror the controller's COST_MODES.
    cost_mode: str = "unknown"
    # "frontier" | "light" | None (undeclared). Catalog seats inherit it from
    # seat_catalog.CatalogEntry.capability_classes; manual seats declare it
    # via `seats add --capability-class`.
    capability_class: str | None = None
    # VERIFIED extra argv for review isolation and for suppressing session
    # persistence, respectively -- see CatalogEntry's fields of the same name.
    isolation_argv: list[str] = field(default_factory=list)
    no_persistence_argv: list[str] = field(default_factory=list)
    # "VAR=relative/dir": SHAPE-checked at load, fully validated by
    # validate_config_home at declaration and at admission. None = undeclared.
    config_home: str | None = None
    verification_argv: list[str] = field(default_factory=list)
    verification_basis: str | None = None  # "catalogued" | "declared"
    result_schema_version: int = 1
    credential_env: list[str] = field(default_factory=list)
    data_policy_revision: str | None = None
    data_policy_notice: str | None = None


COST_MODES = ("subscription", "api", "local", "unknown")


@dataclass
class Registry:
    tool_version: str = ""
    discovered_at: str = ""
    seats: dict[str, Seat] = field(default_factory=dict)
    last_pair: dict[str, list[str]] = field(default_factory=dict)  # "" = global


def registry_path() -> Path:
    return Path(os.environ.get("DEBATE_SEATS_REGISTRY", str(REGISTRY_PATH))).expanduser()


def config_home_shape(value: str) -> None:
    """The part of the config-home rule the LOADER can judge: ``VAR=dir``, both
    sides non-empty.

    The rest of the rule -- which variable names are allowed, and that the
    folder resolves strictly inside the operator's home -- needs the real home
    directory, which the loader does not have and must not guess. Running the
    full rule at load time let ONE hand-edited row break every command that
    reads the registry, `seats list` and `seats remove` included, so the
    operator could not even see or delete the offending seat (final review
    wave, I1). The full rule runs where it belongs: at `seats add`, and at
    admission, which re-checks it against the real home every time.
    """
    if value.count("=") != 1:
        raise channel.ChannelError(
            f"refused: config-home {value!r} must look like VAR=dir (a "
            "variable name, an equals sign, and a folder)"
        )
    var, _, dir_part = value.partition("=")
    if not var or not dir_part:
        raise channel.ChannelError(
            f"refused: config-home {value!r} must look like VAR=dir, with "
            "both the variable name and the folder non-empty"
        )


def validate_credential_env(names: list[str]) -> None:
    """Accept only unique, source-controlled credential variable names."""
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise channel.ChannelError(
            f"refused: duplicate credential environment names: {', '.join(duplicates)}"
        )
    unknown = sorted(set(names) - KNOWN_CREDENTIAL_ENV_VARS)
    if unknown:
        raise channel.ChannelError(
            "refused: credential environment names are code-known, not arbitrary; "
            f"unsupported: {', '.join(unknown)}"
        )


def validate_data_policy(revision: str | None, notice: str | None) -> None:
    """Keep third-party policy declarations paired, printable, and bounded."""
    if (revision is None) != (notice is None):
        raise channel.ChannelError(
            "refused: data_policy_revision and data_policy_notice must be declared together"
        )
    if revision is None or notice is None:
        return
    if not _DATA_POLICY_REVISION_PATTERN.fullmatch(revision):
        raise channel.ChannelError(
            "refused: data_policy_revision must be 1-128 lowercase letters, digits, dots, "
            "underscores, or hyphens"
        )
    if not notice.strip() or len(notice) > DATA_POLICY_NOTICE_MAX_CHARS:
        raise channel.ChannelError(
            f"refused: data_policy_notice must be 1-{DATA_POLICY_NOTICE_MAX_CHARS} characters"
        )
    if not notice.isprintable():
        raise channel.ChannelError(
            "refused: data_policy_notice must contain printable text without control characters"
        )


def validate_config_home(value: str, *, home: Path) -> tuple[str, Path]:
    """Validate a declared ``VAR=relative/dir`` config-home pointer.

    Refuses (with a plain-words message) unless ALL hold: ``value`` is
    exactly one ``VAR=dir`` with both sides non-empty; ``VAR`` is one of the
    documented vendor variables (CLAUDE_CONFIG_DIR, CODEX_HOME) OR looks like
    an environment variable name and is neither reserved by the controller
    nor part of the sandbox's own environment; and ``dir`` is a relative path
    with no ``..`` segment that resolves strictly inside ``home``.

    Returns ``(VAR, resolved_dir)`` on success -- callers that persist the
    declaration store the ORIGINAL ``VAR=dir`` string, never the resolved path.
    """
    config_home_shape(value)
    var, _, dir_part = value.partition("=")
    if var not in VENDOR_CONFIG_HOME_VARS:
        if not _CONFIG_HOME_VAR_PATTERN.match(var):
            raise channel.ChannelError(
                f"refused: config-home variable {var!r} must look like an "
                "environment variable name: uppercase letters, digits and "
                "underscores, starting with a letter"
            )
        from .controller import _RESERVED_ENV

        if var in _RESERVED_ENV or var in SANDBOX_ENV:
            raise channel.ChannelError(
                f"refused: config-home variable {var!r} is already used by "
                "this tool or its sandbox and cannot be redirected"
            )
    dir_path = Path(dir_part)
    if dir_path.is_absolute():
        raise channel.ChannelError(
            f"refused: config-home folder {dir_part!r} must be relative to "
            "your home directory, not an absolute path"
        )
    if ".." in dir_path.parts:
        raise channel.ChannelError(
            f"refused: config-home folder {dir_part!r} must not contain a "
            "'..' segment"
        )
    home_resolved = home.resolve()
    resolved = (home / dir_path).resolve()
    if resolved == home_resolved or not resolved.is_relative_to(home_resolved):
        raise channel.ChannelError(
            f"refused: config-home folder {dir_part!r} must resolve to a "
            "folder strictly inside your home directory"
        )
    return var, resolved


def _seat_from_raw(seat_id: str, raw: object) -> Seat:
    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} must be an object, got {type(raw).__name__}"
        )
    commands_raw = raw.get("commands")
    if not isinstance(commands_raw, list) or not commands_raw or not all(
        isinstance(argv, list) and argv and all(isinstance(part, str) for part in argv)
        for argv in commands_raw
    ):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} needs one or more endpoint argvs "
            "(a list of non-empty string lists)"
        )
    smoke_raw = raw.get("smoke")
    smoke = None
    if smoke_raw is not None:
        if not isinstance(smoke_raw, dict) or not smoke_raw.get("at") or smoke_raw.get("result") not in ("pass", "fail"):
            raise channel.ChannelError(f"refused: registry seat {seat_id!r} has a malformed smoke record")
        smoke = SmokeStatus(at=str(smoke_raw["at"]), result=str(smoke_raw["result"]))
    present_raw = raw.get("present", True)
    if not isinstance(present_raw, bool):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} 'present' must be true or false, "
            f"got {present_raw!r}"
        )
    effort = raw.get("effort")
    cost_mode = str(raw.get("cost_mode", "unknown"))
    if cost_mode not in COST_MODES:
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} cost_mode {cost_mode!r} "
            f"must be one of {COST_MODES}"
        )
    capability_class_raw = raw.get("capability_class")
    capability_class = str(capability_class_raw) if capability_class_raw is not None else None
    if capability_class is not None and capability_class not in CAPABILITY_CLASSES:
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} capability_class {capability_class!r} "
            f"must be one of {CAPABILITY_CLASSES}"
        )
    isolation_argv_raw = raw.get("isolation_argv", [])
    if not isinstance(isolation_argv_raw, list) or not all(
        isinstance(part, str) for part in isolation_argv_raw
    ):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} isolation_argv must be a list of strings"
        )
    no_persistence_argv_raw = raw.get("no_persistence_argv", [])
    if not isinstance(no_persistence_argv_raw, list) or not all(
        isinstance(part, str) for part in no_persistence_argv_raw
    ):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} no_persistence_argv must be a list of strings"
        )
    config_home_raw = raw.get("config_home")
    config_home = str(config_home_raw) if config_home_raw is not None else None
    if config_home is not None:
        config_home_shape(config_home)
    verification_argv_raw = raw.get("verification_argv", [])
    if not isinstance(verification_argv_raw, list) or not all(
        isinstance(part, str) for part in verification_argv_raw
    ):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} verification_argv must be a list of strings"
        )
    verification_basis_raw = raw.get("verification_basis")
    verification_basis = (
        str(verification_basis_raw) if verification_basis_raw is not None else None
    )
    if verification_basis not in (None, "catalogued", "declared"):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} verification_basis must be catalogued or declared"
        )
    result_schema_version = raw.get("result_schema_version", 1)
    if isinstance(result_schema_version, bool) or result_schema_version not in (1, 2, 3):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} result_schema_version must be 1, 2 or 3"
        )
    credential_env_raw = raw.get("credential_env", [])
    if not isinstance(credential_env_raw, list) or not all(
        isinstance(name, str) for name in credential_env_raw
    ):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} credential_env must be a list of strings"
        )
    credential_env = list(credential_env_raw)
    validate_credential_env(credential_env)
    data_policy_revision_raw = raw.get("data_policy_revision")
    data_policy_notice_raw = raw.get("data_policy_notice")
    if data_policy_revision_raw is not None and not isinstance(data_policy_revision_raw, str):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} data_policy_revision must be a string"
        )
    if data_policy_notice_raw is not None and not isinstance(data_policy_notice_raw, str):
        raise channel.ChannelError(
            f"refused: registry seat {seat_id!r} data_policy_notice must be a string"
        )
    data_policy_revision = data_policy_revision_raw
    data_policy_notice = data_policy_notice_raw
    validate_data_policy(data_policy_revision, data_policy_notice)
    return Seat(
        seat_id=seat_id,
        vendor=str(raw.get("vendor", "")),
        submodel=str(raw.get("submodel", "")),
        effort=str(effort) if effort is not None else None,
        commands=[list(argv) for argv in commands_raw],
        source=str(raw.get("source", "manual")),
        present=present_raw,
        smoke=smoke,
        cost_mode=cost_mode,
        capability_class=capability_class,
        isolation_argv=list(isolation_argv_raw),
        no_persistence_argv=list(no_persistence_argv_raw),
        config_home=config_home,
        verification_argv=list(verification_argv_raw),
        verification_basis=verification_basis,
        result_schema_version=result_schema_version,
        credential_env=credential_env,
        data_policy_revision=data_policy_revision,
        data_policy_notice=data_policy_notice,
    )


def load_registry() -> Registry:
    path = registry_path()
    if not path.exists():
        return Registry()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise channel.ChannelError(f"refused: unreadable seat registry {path}: {error}") from error
    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: seat registry {path} must be a JSON object, got {type(raw).__name__}"
        )
    version = raw.get("registry_version", REGISTRY_VERSION)
    if version != REGISTRY_VERSION:
        raise channel.ChannelError(
            f"refused: seat registry {path} has registry_version {version!r}; "
            f"this tool speaks {REGISTRY_VERSION}"
        )
    seats_raw = raw.get("seats", {})
    if not isinstance(seats_raw, dict):
        raise channel.ChannelError(f"refused: seat registry {path} 'seats' must be an object")
    last_pair_raw = raw.get("last_pair", {})
    if not isinstance(last_pair_raw, dict):
        raise channel.ChannelError(f"refused: seat registry {path} 'last_pair' must be an object")
    registry = Registry(
        tool_version=str(raw.get("tool_version", "")),
        discovered_at=str(raw.get("discovered_at", "")),
    )
    for seat_id, seat_raw in seats_raw.items():
        registry.seats[str(seat_id)] = _seat_from_raw(str(seat_id), seat_raw)
    for project, pair in last_pair_raw.items():
        if not isinstance(pair, list) or not all(isinstance(item, str) for item in pair):
            raise channel.ChannelError(
                f"refused: seat registry {path} last_pair for {project!r} must be a list of seat ids"
            )
        registry.last_pair[str(project)] = list(pair)
    return registry


def screen_credentials(registry: Registry) -> None:
    """Refuse anything key-shaped in endpoint or capability argv."""
    for seat in registry.seats.values():
        validate_credential_env(seat.credential_env)
        validate_data_policy(seat.data_policy_revision, seat.data_policy_notice)
        for argv in (
            *seat.commands,
            seat.isolation_argv,
            seat.no_persistence_argv,
            seat.verification_argv,
        ):
            for part in argv:
                if SECRET_PATTERN.search(part):
                    raise channel.ChannelError(
                        f"refused: seat {seat.seat_id!r} command looks credential-shaped; "
                        "credentials enter only through a code-known --credential-env name, "
                        "never through registry argv"
                    )


def registry_payload(registry: Registry) -> dict[str, object]:
    """The registry's canonical JSON shape (shared by save_registry and the
    onboarding transaction, so the two writers can never drift)."""
    return {
        "registry_version": REGISTRY_VERSION,
        "tool_version": registry.tool_version,
        "discovered_at": registry.discovered_at,
        "seats": {
            seat_id: {
                "vendor": seat.vendor,
                "submodel": seat.submodel,
                "effort": seat.effort,
                "commands": seat.commands,
                "source": seat.source,
                "present": seat.present,
                "smoke": (
                    {"at": seat.smoke.at, "result": seat.smoke.result}
                    if seat.smoke is not None
                    else None
                ),
                "cost_mode": seat.cost_mode,
                "capability_class": seat.capability_class,
                "isolation_argv": seat.isolation_argv,
                "no_persistence_argv": seat.no_persistence_argv,
                "config_home": seat.config_home,
                "verification_argv": seat.verification_argv,
                "verification_basis": seat.verification_basis,
                "result_schema_version": seat.result_schema_version,
                **({"credential_env": seat.credential_env} if seat.credential_env else {}),
                **(
                    {
                        "data_policy_revision": seat.data_policy_revision,
                        "data_policy_notice": seat.data_policy_notice,
                    }
                    if seat.data_policy_revision is not None
                    else {}
                ),
            }
            for seat_id, seat in sorted(registry.seats.items())
        },
        "last_pair": dict(sorted(registry.last_pair.items())),
    }


def save_registry(registry: Registry) -> Path:
    """Validate fully -- credential screen included -- then write ATOMICALLY
    (tmp + os.replace): a reader never sees a torn registry."""
    import tempfile

    screen_credentials(registry)
    path = registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".seats-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(registry_payload(registry), indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        channel.atomic_replace(Path(tmp), path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path


def update_registry(
    mutate: Callable[[Registry], None], *, timeout_seconds: float = 15.0
) -> Registry:
    """Serialized read-modify-write: lock, load FRESH, mutate, save, unlock.

    Exists because two concurrent `seats smoke` processes each held a stale
    in-memory registry and the last save clobbered the other's result (field
    finding, 2026-08-20). Apply an observed result through this, never by
    saving a registry object loaded minutes ago."""
    import time

    lock = registry_path().parent / (registry_path().name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise channel.ChannelError(
                    f"refused: registry lock {lock} is held; another debate "
                    "process is writing the registry -- retry, or remove the "
                    "lock file if its owner is gone"
                ) from None
            time.sleep(0.05)
    try:
        registry = load_registry()
        mutate(registry)
        save_registry(registry)
        return registry
    finally:
        try:
            os.unlink(str(lock))
        except OSError:
            pass


def catalog_declares_isolation(vendor: str) -> bool:
    """Whether the packaged catalog carries BOTH verified flag lists for this
    vendor.

    Only then can `debate seats discover` fill a flag-less catalog seat in. For
    a vendor the catalog knows but has verified nothing for (kimi, glm and
    deepseek today), a refresh would change nothing, so telling the operator to
    run one would be false advice -- see `opening.admission_problem`.
    """
    entry = next((e for e in CATALOG if e.vendor == vendor), None)
    return entry is not None and bool(entry.isolation_argv) and bool(entry.no_persistence_argv)


def _assemble_argv(binary_path: str, invocation: tuple[str, ...], extra: list[str]) -> list[str]:
    argv = [binary_path if part == "{binary}" else part for part in invocation]
    if os.name == "nt":
        # Windows codex has no granular sandbox: workspace-write blocks ALL
        # shell execution, read-only access included (field finding F27,
        # model-verified on the box), so the only runnable policy there is
        # danger-full-access — substituted at discovery and therefore
        # recorded honestly in the seat's pinned command. The product's own
        # layers (read-only exports, result contract, controller-owned
        # writes) remain the working isolation, exactly as the protocol's
        # advisory mode states.
        argv = ["danger-full-access" if part == "workspace-write" else part for part in argv]
    return argv + extra


def discover(
    registry: Registry,
    *,
    which: Callable[[str], str | None] = shutil.which,
    now: str,
) -> tuple[Registry, list[str]]:
    """Catalog x PATH -> merged registry plus human-readable diff lines.

    A submodel-selectable entry seeds one seat per submodel; a pin-internal
    entry (empty submodel_argv) seeds EXACTLY ONE seat named by its verified
    pin -- the single-seat rule. Marks vanished catalog seats absent, deletes
    nothing, never touches a manual entry, and refreshes the derived @effort
    seats of any catalog seat whose argv it rewrites.
    """
    from . import __version__

    diff: list[str] = []
    seen_ids: set[str] = set()
    # Every catalog seat this scan refreshed, by id: the source a derived
    # @effort seat inherits its declarations from below.
    refreshed: dict[str, Seat] = {}
    for entry in CATALOG:
        binary_path = next(
            (resolved for name in entry.binaries if (resolved := which(name))), None
        )
        if binary_path is None:
            continue
        for submodel in entry.submodels:
            seat_id = f"{entry.vendor}/{submodel}"
            seen_ids.add(seat_id)
            extra = [
                part.replace("{submodel}", submodel) for part in entry.submodel_argv
            ]
            argv = _assemble_argv(str(binary_path), entry.invocation, extra)
            capability_class = entry.capability_classes.get(submodel)
            existing = registry.seats.get(seat_id)
            if existing is None:
                registry.seats[seat_id] = Seat(
                    seat_id=seat_id,
                    vendor=entry.vendor,
                    submodel=submodel,
                    effort=None,
                    commands=[argv],
                    source="catalog",
                    present=True,
                    smoke=None,
                    capability_class=capability_class,
                    isolation_argv=list(entry.isolation_argv),
                    no_persistence_argv=list(entry.no_persistence_argv),
                    config_home=entry.config_home,
                    verification_argv=list(entry.verification_argv),
                    verification_basis="catalogued" if entry.verification_capable else None,
                    result_schema_version=1,
                    credential_env=list(entry.credential_env),
                    data_policy_revision=entry.data_policy_revision,
                    data_policy_notice=entry.data_policy_notice,
                )
                diff.append(f"+ {seat_id} ({argv[0]})")
                refreshed[seat_id] = registry.seats[seat_id]
            elif existing.source == "catalog":
                refreshed[seat_id] = existing
                if not existing.present:
                    diff.append(f"~ {seat_id} present again")
                existing.present = True
                old_argv = list(existing.commands[0])
                base_changed = old_argv != argv
                existing.commands = [argv] + existing.commands[1:]
                existing.capability_class = capability_class
                existing.isolation_argv = list(entry.isolation_argv)
                existing.no_persistence_argv = list(entry.no_persistence_argv)
                existing.config_home = entry.config_home
                existing.verification_argv = list(entry.verification_argv)
                existing.verification_basis = (
                    "catalogued" if entry.verification_capable else None
                )
                existing.credential_env = list(entry.credential_env)
                existing.data_policy_revision = entry.data_policy_revision
                existing.data_policy_notice = entry.data_policy_notice
                if base_changed:
                    for derived in registry.seats.values():
                        if derived.source != "derived":
                            continue  # manual entries are NEVER touched (D2)
                        if derived.effort is None or not entry.effort_argv:
                            continue
                        if derived.seat_id.split("@", 1)[0] != seat_id:
                            continue
                        # Only a seat whose argv is EXACTLY the old base plus
                        # the substituted effort fragment is auto-derived; a
                        # prefix match is not enough (an operator command may
                        # merely start with the base argv) -- anything else is
                        # the operator's own and is never clobbered.
                        fragment = [
                            part.replace("{effort}", derived.effort)
                            for part in entry.effort_argv
                        ]
                        if derived.commands[0] != old_argv + fragment:
                            continue
                        derived.commands[0] = argv + fragment
                        diff.append(f"~ {derived.seat_id} re-derived from the new base argv")
    # A derived @effort seat is the catalog's seat under another name, so it
    # carries the catalog's declarations WHETHER OR NOT the base argv moved.
    # Gating this on a changed argv left a registry written before the catalog
    # grew these fields flag-less forever, and the operator was told to declare
    # what the catalog already knew (final review wave, C1). Manual seats are
    # never touched: those declarations are the operator's own.
    for derived_seat in registry.seats.values():
        if derived_seat.source != "derived":
            continue
        base_seat = refreshed.get(derived_seat.seat_id.split("@", 1)[0])
        if base_seat is None:
            continue
        inherited = (
            base_seat.capability_class,
            list(base_seat.isolation_argv),
            list(base_seat.no_persistence_argv),
            base_seat.config_home,
            list(base_seat.verification_argv),
            base_seat.verification_basis,
            base_seat.result_schema_version,
            list(base_seat.credential_env),
            base_seat.data_policy_revision,
            base_seat.data_policy_notice,
        )
        if inherited != (
            derived_seat.capability_class,
            derived_seat.isolation_argv,
            derived_seat.no_persistence_argv,
            derived_seat.config_home,
            derived_seat.verification_argv,
            derived_seat.verification_basis,
            derived_seat.result_schema_version,
            derived_seat.credential_env,
            derived_seat.data_policy_revision,
            derived_seat.data_policy_notice,
        ):
            diff.append(
                f"~ {derived_seat.seat_id} took over {base_seat.seat_id}'s recorded settings"
            )
        derived_seat.capability_class = base_seat.capability_class
        derived_seat.isolation_argv = list(base_seat.isolation_argv)
        derived_seat.no_persistence_argv = list(base_seat.no_persistence_argv)
        derived_seat.config_home = base_seat.config_home
        derived_seat.verification_argv = list(base_seat.verification_argv)
        derived_seat.verification_basis = base_seat.verification_basis
        derived_seat.result_schema_version = base_seat.result_schema_version
        derived_seat.credential_env = list(base_seat.credential_env)
        derived_seat.data_policy_revision = base_seat.data_policy_revision
        derived_seat.data_policy_notice = base_seat.data_policy_notice
    for seat in registry.seats.values():
        if seat.source == "catalog" and seat.seat_id not in seen_ids and seat.present:
            base = seat.seat_id.split("@", 1)[0]
            if base not in seen_ids:
                seat.present = False
                diff.append(f"- {seat.seat_id} marked absent (binary gone)")
    registry.discovered_at = now
    registry.tool_version = __version__
    return registry, diff


# --- Slice C1: wrapper-sibling scan ------------------------------------------


@dataclass(frozen=True)
class SiblingCandidate:
    """An executable on PATH that looks like another wrapper for a vendor
    whose OWN catalogued wrapper is already resolvable -- a candidate for
    `seats add`, never seated automatically. Zero model calls, zero writes."""

    vendor: str
    binary_name: str
    binary_path: str
    seat_id: str  # f"{vendor}/wrapper:{binary_name}"


def scan_siblings(
    *,
    which: Callable[[str], str | None] = shutil.which,
    path_entries: Callable[[], list[str]] | None = None,
) -> list[SiblingCandidate]:
    """Executable file names on PATH matching a catalog entry's
    ``sibling_pattern``, excluding the entry's own catalogued binary names,
    for entries whose own binary resolves via ``which``. An entry whose own
    binary does NOT resolve, or whose ``sibling_pattern`` is None (claude,
    kimi -- bare CLIs), contributes nothing. One row per name (first PATH
    directory wins, matching ``which``'s own precedence); reads no file's
    contents; rows are sorted by seat_id."""
    dirs = path_entries() if path_entries is not None else os.environ.get("PATH", "").split(os.pathsep)
    names: dict[str, str] = {}
    for directory in dirs:
        if not directory:
            continue
        try:
            entries = sorted(os.listdir(directory))
        except OSError:
            continue
        for name in entries:
            if name in names:
                continue
            candidate = os.path.join(directory, name)
            if not os.path.isfile(candidate) or not os.access(candidate, os.X_OK):
                continue
            names[name] = candidate
    rows: list[SiblingCandidate] = []
    for entry in CATALOG:
        if entry.sibling_pattern is None:
            continue
        if not any(which(binary) for binary in entry.binaries):
            continue
        for name, path in names.items():
            if name in entry.binaries:
                continue
            if fnmatch.fnmatchcase(name, entry.sibling_pattern):
                rows.append(SiblingCandidate(
                    vendor=entry.vendor,
                    binary_name=name,
                    binary_path=path,
                    seat_id=f"{entry.vendor}/wrapper:{name}",
                ))
    return sorted(rows, key=lambda row: row.seat_id)


# --- Slice 2: freshness, upgrade trigger, manual seats, smoke ---------------

STALE_AFTER_DAYS = 30


@dataclass
class CheckReport:
    """Exit 3 iff ``fails`` is nonempty -- real breakage only (plan fold H1):
    a binary that no longer resolves, or a smoke that RAN AND FAILED.
    Never-smoked is informational and stale smoke a warning, both exit 0 --
    smoke is opt-in (owner ruling 1), and an exit code that stays red until
    the owner pays for smoke would convert opt-in into a toll."""

    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)


def head_resolves(head: str, which: Callable[[str], str | None] = shutil.which) -> bool:
    """The project's ONE definition of a resolvable seat command head
    (setup.validate's, used by add, check, and the open pick path alike):
    an ABSOLUTE head must itself be an executable file (a same-named binary
    elsewhere on PATH must not mask a broken pin); any other head resolves
    on PATH or as an existing executable file after ~ expansion. A 0644 file
    is never a seat."""
    if Path(head).is_absolute():
        return Path(head).is_file() and os.access(head, os.X_OK)
    if which(head) is not None:
        return True
    candidate = Path(head).expanduser()
    return candidate.is_file() and os.access(candidate, os.X_OK)


def slug(text: str) -> str:
    """The channel slug rule applied to a name: [a-z0-9-] only, runs
    collapsed, edges stripped."""
    import re as _re

    cleaned = _re.sub(r"[^a-z0-9-]+", "-", text.lower())
    cleaned = _re.sub(r"-{2,}", "-", cleaned).strip("-")
    if not cleaned:
        raise channel.ChannelError(f"refused: {text!r} slugifies to nothing")
    return cleaned


def days_between(earlier: str, later: str) -> float | None:
    from datetime import datetime

    try:
        delta = datetime.fromisoformat(later) - datetime.fromisoformat(earlier)
    except (ValueError, TypeError):
        return None  # unparseable or naive-vs-aware: no staleness verdict
    return delta.total_seconds() / 86400.0


def check(
    registry: Registry,
    *,
    which: Callable[[str], str | None] = shutil.which,
    now: str,
) -> CheckReport:
    report = CheckReport()
    for seat_id, seat in sorted(registry.seats.items()):
        if not seat.present:
            report.fails.append(
                f"FAIL {seat_id}: binary missing (absent since discovery; "
                f"re-install it, or clean up via: debate seats remove {seat_id})"
            )
            continue
        binary = seat.commands[0][0]
        if not head_resolves(binary, which):
            report.fails.append(f"FAIL {seat_id}: binary missing ({binary})")
            continue
        if seat.smoke is None:
            report.infos.append(
                f"INFO {seat_id}: never smoked (opt-in: debate seats smoke {seat_id})"
            )
            continue
        if seat.smoke.result != "pass":
            report.fails.append(f"FAIL {seat_id}: smoke failed at {seat.smoke.at}")
            continue
        age = days_between(seat.smoke.at, now)
        if age is not None and age > STALE_AFTER_DAYS:
            report.warns.append(
                f"WARN {seat_id}: smoke stale ({age:.0f}d; refresh via debate seats smoke)"
            )
    return report


def ensure_current(
    registry: Registry,
    *,
    which: Callable[[str], str | None] = shutil.which,
    now: str,
) -> tuple[Registry, list[str]]:
    """The upgrade trigger: a version mismatch re-runs the catalog scan --
    scan only, smoke is never automatic."""
    from . import __version__

    if registry.tool_version == __version__:
        return registry, []
    return discover(registry, which=which, now=now)


def add_seat(
    registry: Registry,
    seat_id: str,
    command_text: str,
    *,
    which: Callable[[str], str | None] = shutil.which,
    cost_mode: str = "unknown",
    capability_class: str | None = None,
    isolation_argv: list[str] | None = None,
    no_persistence_argv: list[str] | None = None,
    config_home: str | None = None,
    verification_argv: list[str] | None = None,
    verification_declared: bool = False,
    result_schema_version: int | None = None,
    credential_env: list[str] | None = None,
    home: Path | None = None,
) -> None:
    """Create a manual seat, or APPEND an endpoint option to an existing
    manual one (another provider account of the SAME serving, section 2.9;
    a different serving is its own seat -- section 2.10). Selection stays
    first-listed (owner ruling 4).

    The declared fields (capability_class, isolation_argv,
    no_persistence_argv, config_home) follow the SAME rule as cost_mode on
    the append path: a non-None/non-empty declaration APPLIES, None/empty
    leaves the stored value untouched."""
    from .setup import split_argv

    if "/" not in seat_id:
        raise channel.ChannelError(
            f"refused: seat id {seat_id!r} must be vendor/submodel"
        )
    model_part = seat_id.split("/", 1)[1]
    if ":" in model_part:
        raise channel.ChannelError(
            f"refused: seat id {seat_id!r} must not contain ':' in the "
            "model part (that namespace is reserved for wrapper-sibling ids)"
        )
    if capability_class is not None and capability_class not in CAPABILITY_CLASSES:
        raise channel.ChannelError(
            f"refused: capability_class {capability_class!r} must be one of "
            f"{CAPABILITY_CLASSES}"
        )
    if config_home is not None:
        validate_config_home(config_home, home=home if home is not None else Path.home())
    if result_schema_version not in (None, 1, 2, 3):
        raise channel.ChannelError("refused: result_schema_version must be 1, 2 or 3")
    validate_credential_env(list(credential_env or []))
    if verification_argv and not verification_declared:
        raise channel.ChannelError(
            "refused: --verification-argv needs the explicit --verification-capable declaration"
        )
    argv = split_argv(command_text)
    joined = " ".join(argv)
    prompt_style = "{prompt}" in joined
    bridge_style = "{input_path}" in joined and "{result_path}" in joined
    if not argv or not (prompt_style or bridge_style):
        raise channel.ChannelError(
            "refused: a seat command needs an executable and either a {prompt} "
            "marker (where the question text goes) or both {input_path} and "
            "{result_path} (a command that reads a request file and writes an "
            "answer file)"
        )
    head = argv[0]
    if not head_resolves(head, which):
        raise channel.ChannelError(
            f"refused: seat command {head!r} is neither on PATH nor an existing "
            "executable file"
        )
    for part in [
        *argv,
        *(isolation_argv or []),
        *(no_persistence_argv or []),
        *(verification_argv or []),
    ]:
        if SECRET_PATTERN.search(part):
            raise channel.ChannelError(
                "refused: command looks credential-shaped; credentials belong in a "
                "code-known --credential-env declaration, never registry argv"
            )
    if bridge_style and result_schema_version in (2, 3) and not verification_declared:
        raise channel.ChannelError(
            "refused: a result-schema-v2 wrapper needs --verification-capable"
        )
    if cost_mode not in COST_MODES:
        raise channel.ChannelError(
            f"refused: cost_mode {cost_mode!r} must be one of {COST_MODES}"
        )
    existing = registry.seats.get(seat_id)
    if existing is not None:
        if existing.source != "manual":
            raise channel.ChannelError(
                f"refused: {seat_id!r} is a catalog seat; endpoint options on catalog "
                "seats come from discovery"
            )
        existing.commands.append(argv)
        # A declared cost mode on the append path APPLIES (a silent no-op was
        # the branch-gate round-2 finding); "unknown" leaves the declaration
        # untouched rather than regressing it. The four new fields follow the
        # same rule.
        if cost_mode != "unknown":
            existing.cost_mode = cost_mode
        if capability_class is not None:
            existing.capability_class = capability_class
        if isolation_argv:
            existing.isolation_argv = list(isolation_argv)
        if no_persistence_argv:
            existing.no_persistence_argv = list(no_persistence_argv)
        if config_home:
            existing.config_home = config_home
        if verification_declared:
            existing.verification_basis = "declared"
            existing.verification_argv = list(verification_argv or [])
        if result_schema_version is not None:
            existing.result_schema_version = result_schema_version
        if credential_env:
            existing.credential_env = list(credential_env)
        return
    vendor, _, submodel = seat_id.partition("/")
    base_id, _, effort = seat_id.partition("@")
    registry.seats[seat_id] = Seat(
        seat_id=seat_id,
        vendor=vendor,
        submodel=submodel.split("@", 1)[0],
        effort=effort or None,
        commands=[argv],
        source="manual",
        present=True,
        smoke=None,
        cost_mode=cost_mode,
        capability_class=capability_class,
        isolation_argv=list(isolation_argv) if isolation_argv else [],
        no_persistence_argv=list(no_persistence_argv) if no_persistence_argv else [],
        config_home=config_home,
        verification_argv=list(verification_argv or []),
        verification_basis="declared" if verification_declared else None,
        result_schema_version=result_schema_version or 1,
        credential_env=list(credential_env or []),
    )


def set_cost_mode(registry: Registry, seat_id: str, cost_mode: str) -> None:
    """Declare who pays for ANY existing seat -- catalog, derived, or manual.
    The declaration is the operator's; discovery never touches it, so a
    catalog seat's cost mode survives re-scans. This is the product path's
    only way to move a discovered seat off 'unknown' (branch-gate round-2
    finding: cost_mode must be declarable, not vacuously unknown)."""
    if cost_mode not in COST_MODES:
        raise channel.ChannelError(
            f"refused: cost_mode {cost_mode!r} must be one of {COST_MODES}"
        )
    seat = registry.seats.get(seat_id)
    if seat is None:
        raise channel.ChannelError(f"refused: no seat {seat_id!r} in the registry")
    seat.cost_mode = cost_mode


def add_effort_seat(registry: Registry, seat_id: str) -> None:
    """Derive vendor/submodel@effort from its base seat: derived argv = the
    base's FIRST-LISTED endpoint option plus the catalog's effort fragment."""
    base_id, sep, effort = seat_id.partition("@")
    if not sep or not effort:
        raise channel.ChannelError(
            f"refused: {seat_id!r} is not a vendor/submodel@effort id"
        )
    if seat_id in registry.seats:
        raise channel.ChannelError(
            f"refused: {seat_id!r} is already in the registry; remove it first "
            "(the registry never clobbers an existing seat)"
        )
    base = registry.seats.get(base_id)
    if base is None:
        raise channel.ChannelError(
            f"refused: base seat {base_id!r} is not in the registry"
        )
    entry = next((e for e in CATALOG if e.vendor == base.vendor), None)
    if entry is None or not entry.effort_argv:
        raise channel.ChannelError(
            f"refused: {base.vendor!r} takes no effort via argv "
            "(a wrapper-internal effort is a different wrapper: use seats add --command)"
        )
    if effort not in entry.known_efforts:
        raise channel.ChannelError(
            f"refused: effort {effort!r} is not in {base.vendor!r} known_efforts "
            f"{list(entry.known_efforts)}"
        )
    derived_argv = list(base.commands[0]) + [
        part.replace("{effort}", effort) for part in entry.effort_argv
    ]
    registry.seats[seat_id] = Seat(
        seat_id=seat_id,
        vendor=base.vendor,
        submodel=base.submodel,
        effort=effort,
        commands=[derived_argv],
        source="derived",
        present=base.present,
        smoke=None,
        cost_mode=base.cost_mode,
        capability_class=base.capability_class,
        isolation_argv=list(base.isolation_argv),
        no_persistence_argv=list(base.no_persistence_argv),
        config_home=base.config_home,
        verification_argv=list(base.verification_argv),
        verification_basis=base.verification_basis,
        result_schema_version=base.result_schema_version,
        credential_env=list(base.credential_env),
        data_policy_revision=base.data_policy_revision,
        data_policy_notice=base.data_policy_notice,
    )


def remove_seat(registry: Registry, seat_id: str) -> None:
    seat = registry.seats.get(seat_id)
    if seat is None:
        raise channel.ChannelError(f"refused: no seat {seat_id!r} in the registry")
    if seat.source == "catalog" and seat.present:
        raise channel.ChannelError(
            f"refused: {seat_id!r} is a PRESENT catalog seat; discovery owns it "
            "(an ABSENT catalog seat may be removed as cleanup)"
        )
    del registry.seats[seat_id]


def smoke_seat(
    registry: Registry,
    seat_id: str,
    *,
    scratch_base: Path | None = None,
    now: str,
    emit: Callable[[str], None] = print,
    assume_yes: bool = False,
    ask: Callable[[str], str] = input,
) -> str:
    """One scratch-channel round trip for one seat's FIRST-LISTED argv,
    through setup's own smoke machinery. The cost is announced and CONFIRMED
    before the spend (auto-yes under --yes, ruling 1); the result is recorded
    in the registry either way; returns "pass" or "fail"."""
    from .setup import SetupSpec
    from . import setup as setup_module

    seat = registry.seats.get(seat_id)
    if seat is None:
        raise channel.ChannelError(f"refused: no seat {seat_id!r} in the registry")
    validate_credential_env(seat.credential_env)
    missing_credentials = [
        name for name in seat.credential_env if not os.environ.get(name)
    ]
    if missing_credentials:
        raise channel.ChannelError(
            f"refused: seat {seat.seat_id!r} needs credential environment "
            f"{', '.join(missing_credentials)} in the launching process"
        )
    if not assume_yes:
        answer = ask(
            f"smoke {seat_id}: this spends ONE model call "
            f"({seat.commands[0][0]} ...; cost mode: {seat.cost_mode}"
            f"{' -- undeclared, treat as potentially metered' if seat.cost_mode == 'unknown' else ''}"
            "). Proceed? [y/N]: "
        ).strip().lower()
        if answer not in ("y", "yes"):
            raise channel.ChannelError(
                f"refused: smoke of {seat_id!r} not confirmed (pass --yes to auto-confirm)"
            )
    if scratch_base is not None:
        scratch_base.mkdir(parents=True, exist_ok=True)
    party = slug(seat.vendor)
    if party == "probe":
        party = "seatprobe"
    # The bridge composes invocation + isolation + no-persistence +
    # verification argv into one command line for every managed turn; a smoke
    # of the bare base argv proves a different animal. Field finding F16: a
    # headless claude with no permission flags authenticated, read the
    # thread, and correctly refused to post -- the seat obeyed its contract
    # against an under-equipped harness. Smoke runs the full composition.
    composed = (
        list(seat.commands[0])
        + list(seat.isolation_argv)
        + list(seat.no_persistence_argv)
        + list(seat.verification_argv)
    )
    spec = SetupSpec(
        channel_root=Path("."),
        channel_name=f"smoke-{party}",
        parties=(party, "probe"),
        commands={party: composed, "probe": None},
        config_path=Path("unused-config.json"),
        state_path=Path("unused-state.json"),
        thread_cap=12,
        timeout_seconds=300,
    )
    failures = setup_module.smoke(spec, scratch_base=scratch_base, emit=emit)
    result = "fail" if failures else "pass"
    seat.smoke = SmokeStatus(at=now, result=result)
    for line in failures:
        emit(f"smoke {seat_id}: {line}")
    return result


# --- Slice 4: the project profile (section 2.10's second layer, ruling 5) ---

PROFILE_NAME = "debate-profile.json"


@dataclass
class Profile:
    """The per-project allowlist: which subset of the host registry may
    debate in this project. References registry entries by id, never
    redefines them (section 2.10 verbatim); pinned-effort ids ARE the pin
    mechanism. Opt-in per project: no file, no restriction."""

    allowlist: tuple[str, ...]
    data_policy_acceptances: dict[str, str] = field(default_factory=dict)


def vendor_display(vendor: str) -> tuple[str, tuple[str, ...]]:
    """(notes, known_efforts) for `seats list` -- the wrapper-pin drift limit
    is only honest if the display actually names where the pin lives (D1)."""
    entry = next((e for e in CATALOG if e.vendor == vendor), None)
    if entry is None:
        return ("manual seat; the operator owns its pin", ())
    return (entry.notes, entry.known_efforts)


def load_profile(project: str, registry: Registry) -> Profile | None:
    """Fail-closed: a malformed file, an unknown version, an id the registry
    does not carry, or an EMPTY allowlist all refuse with the offender named.
    A missing file is simply no restriction."""
    path = Path(project) / PROFILE_NAME
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise channel.ChannelError(
            f"refused: unreadable project profile {path}: {error}"
        ) from error
    except ValueError as error:
        raise channel.ChannelError(
            f"refused: unreadable project profile {path}: {error}"
        ) from error
    if not isinstance(raw, dict):
        raise channel.ChannelError(
            f"refused: project profile {path} must be a JSON object"
        )
    version_raw = raw.get("profile_version")
    if not isinstance(version_raw, int) or isinstance(version_raw, bool) or version_raw != 1:
        raise channel.ChannelError(
            f"refused: project profile {path} has profile_version "
            f"{version_raw!r}; this tool speaks 1"
        )
    allowlist_raw = raw.get("allowlist")
    if not isinstance(allowlist_raw, list) or not all(
        isinstance(item, str) for item in allowlist_raw
    ):
        raise channel.ChannelError(
            f"refused: project profile {path} 'allowlist' must be a list of seat ids"
        )
    if not allowlist_raw:
        raise channel.ChannelError(
            f"refused: project profile {path} has an EMPTY allowlist, which would "
            "ban every seat; delete the file instead"
        )
    for seat_id in allowlist_raw:
        if seat_id not in registry.seats:
            raise channel.ChannelError(
                f"refused: project profile {path} allowlists {seat_id!r}, which is "
                "not in the registry; run: debate seats discover"
            )
    acceptances_raw = raw.get("data_policy_acceptances", {})
    if not isinstance(acceptances_raw, dict) or not all(
        isinstance(seat_id, str) and isinstance(revision, str)
        for seat_id, revision in acceptances_raw.items()
    ):
        raise channel.ChannelError(
            f"refused: project profile {path} 'data_policy_acceptances' must map seat ids to revisions"
        )
    outside = sorted(set(acceptances_raw) - set(allowlist_raw))
    if outside:
        raise channel.ChannelError(
            f"refused: project profile {path} accepts policy for non-allowlisted seats: "
            f"{', '.join(outside)}"
        )
    return Profile(
        allowlist=tuple(allowlist_raw),
        data_policy_acceptances={str(key): str(value) for key, value in acceptances_raw.items()},
    )


# Backwards-compatible alias (pre-0.8 internal name).
_days_between = days_between
