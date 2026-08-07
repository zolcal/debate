"""Brokered, provenance-carrying invocation of generic review adapters.

This module is deliberately independent of vendor CLIs.  It prepares a pinned
source export and immutable docket, renders phase-limited input, launches one
configured adapter with a clean environment, validates its result file, and
posts under the seat identity bound by the controller.  The adapter never
receives the live channel path and never chooses its sender.

The boundary is honest: a clean environment, read-only export, Git ceiling and
contamination canaries protect against accidental context drift.  They do not
make a same-user process hostile-code safe.  Profiles therefore record whether
an external OS sandbox is actually enforced.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import tarfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from debate import channel

RESULT_SCHEMA_VERSION = 1
AUTHOR_RELATIONSHIPS = ("author-affiliated", "author-independent")
SEAT_DECISIONS = ("PASS", "NO_PASS")
COST_MODES = ("subscription", "api", "local", "unknown")
ISOLATION_MODES = ("advisory", "os-enforced")
_PINNED_REF = re.compile(r"^[0-9a-f]{40}$")
_TOOL_CACHE_NAMES = {".pytest_cache", ".pytest-tmp", ".mypy_cache", ".ruff_cache", "__pycache__"}
_RESERVED_ENV = {
    "CLAUDE_CONFIG_DIR",
    "CODEX_HOME",
    "HOME",
    "XDG_CONFIG_HOME",
    "XDG_CACHE_HOME",
    "XDG_DATA_HOME",
    "TMPDIR",
    "TEMP",
    "TMP",
    "GIT_CEILING_DIRECTORIES",
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_INDEX_FILE",
    "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    "GIT_CONFIG_GLOBAL",
    "GIT_CONFIG_SYSTEM",
    "GIT_CONFIG_COUNT",
    "PYTEST_ADDOPTS",
    "PYTHONDONTWRITEBYTECODE",
}


class AdapterError(channel.ChannelError):
    """A broker refusal.  ``retryable`` is consumed by the watcher."""

    def __init__(
        self, message: str, *, retryable: bool = False, close_reason: str = "adapter-error"
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.close_reason = close_reason


def _canonical_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _bytes_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp{os.getpid()}")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def _string_list(raw: object, field_name: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise channel.ChannelError(f"refused: adapter field {field_name!r} must be a list of strings")
    if not allow_empty and not raw:
        raise channel.ChannelError(f"refused: adapter field {field_name!r} must not be empty")
    return tuple(raw)


@dataclass(frozen=True)
class AdapterProfile:
    party: str
    command: tuple[str, ...]
    provider: str
    requested_model: str
    author_relationship: str
    reasoning_effort: str
    cli_version: str
    cost_mode: str
    authentication_mode: str
    permission_policy: str
    settings_sources: tuple[str, ...]
    environment_allowlist: tuple[str, ...] = ()
    environment: dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 1800
    retry_limit: int = 1
    session_persistence: bool = False
    isolation_mode: str = "advisory"
    expected_runtime_model: str | None = None

    def __post_init__(self) -> None:
        if not self.command or not all(isinstance(part, str) and part for part in self.command):
            raise channel.ChannelError(f"refused: adapter command for {self.party!r} must contain string arguments")
        joined = "\n".join(self.command)
        for placeholder in ("{input_path}", "{result_path}"):
            if placeholder not in joined:
                raise channel.ChannelError(
                    f"refused: adapter command for {self.party!r} must contain {placeholder}"
                )
        if self.author_relationship not in AUTHOR_RELATIONSHIPS:
            raise channel.ChannelError(
                f"refused: author_relationship for {self.party!r} must be one of {AUTHOR_RELATIONSHIPS}"
            )
        for name, value in (
            ("provider", self.provider),
            ("requested_model", self.requested_model),
            ("reasoning_effort", self.reasoning_effort),
            ("cli_version", self.cli_version),
            ("authentication_mode", self.authentication_mode),
            ("permission_policy", self.permission_policy),
        ):
            if not value.strip():
                raise channel.ChannelError(
                    f"refused: adapter field {name!r} for {self.party!r} must not be empty"
                )
        if self.cost_mode not in COST_MODES:
            raise channel.ChannelError(f"refused: cost_mode for {self.party!r} must be one of {COST_MODES}")
        if self.isolation_mode not in ISOLATION_MODES:
            raise channel.ChannelError(
                f"refused: isolation_mode for {self.party!r} must be one of {ISOLATION_MODES}"
            )
        if self.session_persistence:
            raise channel.ChannelError(
                f"refused: managed adapter {self.party!r} enables session persistence; every turn must be fresh"
            )
        if self.settings_sources:
            raise channel.ChannelError(
                f"refused: managed adapter {self.party!r} enables live settings sources "
                f"{self.settings_sources}; project settings remain evidence, not execution policy"
            )
        if isinstance(self.timeout_seconds, bool) or not 1 <= self.timeout_seconds <= 3600:
            raise channel.ChannelError(
                f"refused: timeout_seconds for {self.party!r} must be between 1 and 3600"
            )
        if isinstance(self.retry_limit, bool) or self.retry_limit not in (0, 1):
            raise channel.ChannelError(f"refused: retry_limit for {self.party!r} must be 0 or 1")
        overlap = sorted(
            key
            for key in self.environment
            if key in _RESERVED_ENV or key.startswith("GIT_CONFIG_")
        )
        if overlap:
            raise channel.ChannelError(
                f"refused: adapter {self.party!r} attempts to override controller-owned environment: "
                f"{', '.join(overlap)}"
            )
        inherited_overlap = sorted(
            key
            for key in self.environment_allowlist
            if key in _RESERVED_ENV or key.startswith("GIT_CONFIG_")
        )
        if inherited_overlap:
            raise channel.ChannelError(
                f"refused: adapter {self.party!r} attempts to inherit user/runtime configuration: "
                f"{', '.join(inherited_overlap)}"
            )
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in self.environment.items()):
            raise channel.ChannelError(f"refused: adapter environment for {self.party!r} must map strings to strings")
        if not all(isinstance(key, str) for key in self.environment_allowlist):
            raise channel.ChannelError(
                f"refused: adapter environment_allowlist for {self.party!r} must contain strings"
            )

    @classmethod
    def from_mapping(cls, party: str, raw: object) -> "AdapterProfile":
        if not isinstance(raw, dict):
            raise channel.ChannelError(f"refused: adapter profile for {party!r} must be a JSON object")
        required = (
            "command",
            "provider",
            "requested_model",
            "author_relationship",
            "reasoning_effort",
            "cli_version",
            "cost_mode",
            "authentication_mode",
            "permission_policy",
            "settings_sources",
        )
        missing = [key for key in required if key not in raw]
        if missing:
            raise channel.ChannelError(
                f"refused: adapter profile for {party!r} is missing: {', '.join(missing)}"
            )
        environment = raw.get("environment", {})
        if not isinstance(environment, dict):
            raise channel.ChannelError(f"refused: adapter environment for {party!r} must be a JSON object")
        try:
            timeout = int(raw.get("timeout_seconds", 1800))
            retry = int(raw.get("retry_limit", 1))
        except (TypeError, ValueError) as error:
            raise channel.ChannelError(
                f"refused: adapter timing for {party!r} must contain integers"
            ) from error
        return cls(
            party=party,
            command=_string_list(raw["command"], "command", allow_empty=False),
            provider=str(raw["provider"]),
            requested_model=str(raw["requested_model"]),
            expected_runtime_model=(
                str(raw["expected_runtime_model"]) if raw.get("expected_runtime_model") is not None else None
            ),
            author_relationship=str(raw["author_relationship"]),
            reasoning_effort=str(raw["reasoning_effort"]),
            cli_version=str(raw["cli_version"]),
            cost_mode=str(raw["cost_mode"]),
            authentication_mode=str(raw["authentication_mode"]),
            permission_policy=str(raw["permission_policy"]),
            settings_sources=_string_list(raw["settings_sources"], "settings_sources"),
            environment_allowlist=_string_list(raw.get("environment_allowlist", []), "environment_allowlist"),
            environment={str(key): str(value) for key, value in environment.items()},
            timeout_seconds=timeout,
            retry_limit=retry,
            session_persistence=bool(raw.get("session_persistence", False)),
            isolation_mode=str(raw.get("isolation_mode", "advisory")),
        )

    def sanitized_manifest(self) -> dict[str, object]:
        env_hashes = {key: _bytes_hash(value.encode("utf-8")) for key, value in sorted(self.environment.items())}
        command_hash = _canonical_hash(list(self.command))
        return {
            "schema_version": 1,
            "party": self.party,
            "provider": self.provider,
            "requested_model": self.requested_model,
            "expected_runtime_model": self.expected_runtime_model,
            "author_relationship": self.author_relationship,
            "reasoning_effort": self.reasoning_effort,
            "cli_version": self.cli_version,
            "cost_mode": self.cost_mode,
            "authentication_mode": self.authentication_mode,
            "permission_policy": self.permission_policy,
            "settings_sources": list(self.settings_sources),
            "environment_allowlist": list(self.environment_allowlist),
            "environment_additions": env_hashes,
            "timeout_seconds": self.timeout_seconds,
            "retry_limit": self.retry_limit,
            "session_persistence": self.session_persistence,
            "isolation_mode": self.isolation_mode,
            "command_sha256": command_hash,
            "result_schema_version": RESULT_SCHEMA_VERSION,
        }

    @property
    def profile_sha256(self) -> str:
        return _canonical_hash(self.sanitized_manifest())


@dataclass(frozen=True)
class TimingPolicy:
    thread_cap: int
    scheduler_interval_seconds: int
    retry_seconds: int
    whole_case_timeout_seconds: int
    profiles: tuple[AdapterProfile, AdapterProfile]

    def __post_init__(self) -> None:
        for name, value in (
            ("thread_cap", self.thread_cap),
            ("scheduler_interval_seconds", self.scheduler_interval_seconds),
            ("retry_seconds", self.retry_seconds),
            ("whole_case_timeout_seconds", self.whole_case_timeout_seconds),
        ):
            if isinstance(value, bool) or value <= 0:
                raise channel.ChannelError(f"refused: managed timing field {name} must be a positive integer")
        if len(self.profiles) != 2:
            raise channel.ChannelError("refused: managed timing requires exactly two adapter profiles")

    @property
    def unconstrained_seconds(self) -> int:
        slowest = max(
            profile.timeout_seconds * (profile.retry_limit + 1)
            + self.retry_seconds * profile.retry_limit
            + self.scheduler_interval_seconds * (profile.retry_limit + 1)
            for profile in self.profiles
        )
        return self.thread_cap * slowest

    @property
    def enforced_seconds(self) -> int:
        return min(self.unconstrained_seconds, self.whole_case_timeout_seconds)

    def report(self) -> dict[str, int]:
        return {
            "thread_cap": self.thread_cap,
            "unconstrained_schedule_seconds": self.unconstrained_seconds,
            "whole_case_timeout_seconds": self.whole_case_timeout_seconds,
            "enforced_terminal_bound_seconds": self.enforced_seconds,
        }


@dataclass(frozen=True)
class BrokerConfig:
    repository_root: Path
    runtime_root: Path
    source_ref: str
    profiles: dict[str, AdapterProfile]
    timing: TimingPolicy
    config_sha256: str
    docket_files: tuple[str, ...] = ()
    contamination_canaries: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        repo = self.repository_root.resolve()
        runtime = self.runtime_root.resolve()
        expected_root = (repo / "var" / "debate").resolve()
        if runtime == expected_root or not runtime.is_relative_to(expected_root):
            raise channel.ChannelError(
                f"refused: managed runtime_root {runtime} must be a case directory below {expected_root}"
            )
        relative_parts = runtime.relative_to(repo).parts
        bad = sorted(_TOOL_CACHE_NAMES.intersection(relative_parts))
        if bad:
            raise channel.ChannelError(
                f"refused: managed runtime_root may not live under tool-managed caches: {', '.join(bad)}"
            )
        if not _PINNED_REF.fullmatch(self.source_ref):
            raise channel.ChannelError(
                f"refused: source_ref must be a full 40-character commit SHA, got {self.source_ref!r}"
            )
        if len(self.profiles) != 2:
            raise channel.ChannelError("refused: a brokered debate requires exactly two adapter profiles")
        if any(party != profile.party for party, profile in self.profiles.items()):
            raise channel.ChannelError(
                "refused: each brokered adapter mapping key must equal the profile's recorded party"
            )
        if {profile.party for profile in self.timing.profiles} != set(self.profiles) or any(
            self.profiles[profile.party] != profile for profile in self.timing.profiles
        ):
            raise channel.ChannelError(
                "refused: timing profiles must be the same two brokered adapter profiles"
            )
        independent = sum(
            profile.author_relationship == "author-independent" for profile in self.profiles.values()
        )
        if independent == 0:
            raise channel.ChannelError(
                "refused: a managed gate requires at least one author-independent seat"
            )
        if not self.config_sha256 or not re.fullmatch(r"[0-9a-f]{64}", self.config_sha256):
            raise channel.ChannelError("refused: controller config_sha256 must be a SHA-256 hex digest")
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in self.contamination_canaries.items()):
            raise channel.ChannelError("refused: contamination_canaries must map labels to strings")
        if any(not value for value in self.contamination_canaries.values()):
            raise channel.ChannelError("refused: contamination canary values must not be empty")
        if len(set(self.contamination_canaries.values())) != len(self.contamination_canaries):
            raise channel.ChannelError("refused: contamination canary values must be unique")
        if len(set(self.docket_files)) != len(self.docket_files):
            raise channel.ChannelError("refused: docket_files must not contain duplicate paths")

    @property
    def topology(self) -> str:
        independent = sum(
            profile.author_relationship == "author-independent" for profile in self.profiles.values()
        )
        return "recommended-three-agent" if independent == 2 else "minimum-two-agent"

    @property
    def profile_hashes(self) -> dict[str, str]:
        return {party: profile.profile_sha256 for party, profile in sorted(self.profiles.items())}


@dataclass(frozen=True)
class SourceExport:
    party: str
    root: Path
    source_ref: str
    manifest_path: Path
    manifest_sha256: str
    files: dict[str, str]
    excluded: tuple[str, ...]


@dataclass(frozen=True)
class DocketRevision:
    root: Path
    revision_sha256: str
    manifest_path: Path
    files: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class AdapterResult:
    entry_type: str
    body: str
    refs: str
    appendix_markdown: str
    runtime_model: str
    decision: str | None


@dataclass(frozen=True)
class BrokerOutcome:
    entry_id: str
    party: str
    profile_sha256: str
    source_manifest_sha256: str
    docket_revision_sha256: str
    input_sha256: str
    runtime_model: str
    diagnostics_root: Path
    decision: str | None = None


@dataclass(frozen=True)
class DriveOutcome:
    phase: str
    detail: str
    terminal_result: str | None = None
    close_reason: str | None = None


def _git(repository_root: Path, args: list[str], *, binary: bool = False) -> bytes | str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repository_root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=not binary,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise channel.ChannelError(f"refused: cannot inspect source repository {repository_root}: {error}") from error
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace") if binary else str(proc.stderr)
        raise channel.ChannelError(
            f"refused: git {' '.join(args)} failed in {repository_root}: {stderr.strip()}"
        )
    return proc.stdout


def _safe_member(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or not path.parts or any(part in ("", ".", "..") for part in path.parts):
        raise channel.ChannelError(f"refused: unsafe path {name!r} in pinned source export")
    return path


def _is_separated(path: PurePosixPath) -> bool:
    return path.parts[0] in ("collab", "var", ".git")


def _write_export_member(archive: tarfile.TarFile, member: tarfile.TarInfo, root: Path) -> None:
    relative = _safe_member(member.name)
    destination = root.joinpath(*relative.parts)
    if member.isdir():
        destination.mkdir(parents=True, exist_ok=True)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if member.isfile():
        source = archive.extractfile(member)
        if source is None:
            raise channel.ChannelError(f"refused: cannot extract {member.name!r} from source archive")
        with destination.open("wb") as handle:
            shutil.copyfileobj(source, handle)
        destination.chmod(member.mode & 0o777)
        return
    if member.issym():
        target = PurePosixPath(member.linkname)
        if target.is_absolute() or ".." in target.parts:
            raise channel.ChannelError(
                f"refused: source symlink {member.name!r} escapes the isolated export"
            )
        destination.symlink_to(member.linkname)
        return
    raise channel.ChannelError(f"refused: unsupported archive member {member.name!r}")


def _tree_files(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            files[relative] = "symlink:" + os.readlink(path)
        elif path.is_file():
            files[relative] = _file_hash(path)
    return files


def _make_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_symlink():
            continue
        mode = path.stat().st_mode
        path.chmod((mode & ~0o222) | (0o111 if path.is_dir() else 0))
    root.chmod((root.stat().st_mode & ~0o222) | 0o111)


def create_source_export(config: BrokerConfig, party: str) -> SourceExport:
    resolved = str(_git(config.repository_root, ["rev-parse", f"{config.source_ref}^{{commit}}"])).strip()
    if resolved != config.source_ref:
        raise channel.ChannelError(
            f"refused: source_ref {config.source_ref} resolved to a different commit {resolved}"
        )
    export_parent = config.runtime_root / "exports" / config.source_ref
    export_root = export_parent / party
    manifest_path = export_parent / f"{party}.manifest.json"
    if export_root.exists() or manifest_path.exists():
        if not export_root.is_dir() or not manifest_path.is_file():
            raise channel.ChannelError(f"refused: incomplete existing source export for {party!r}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise channel.ChannelError(f"refused: unreadable source manifest {manifest_path}: {error}") from error
        current = _tree_files(export_root)
        if current != manifest.get("files"):
            raise channel.ChannelError(f"refused: immutable source export for {party!r} changed after creation")
        return SourceExport(
            party=party,
            root=export_root,
            source_ref=config.source_ref,
            manifest_path=manifest_path,
            manifest_sha256=_file_hash(manifest_path),
            files=current,
            excluded=tuple(manifest.get("excluded", [])),
        )

    export_parent.mkdir(parents=True, exist_ok=True)
    export_root.mkdir(parents=True)
    archive_bytes = _git(config.repository_root, ["archive", "--format=tar", config.source_ref], binary=True)
    assert isinstance(archive_bytes, bytes)
    excluded: list[str] = []
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
            for member in archive.getmembers():
                relative = _safe_member(member.name)
                if _is_separated(relative):
                    excluded.append(member.name)
                    continue
                _write_export_member(archive, member, export_root)
    except tarfile.TarError as error:
        raise channel.ChannelError(f"refused: unreadable git archive for {config.source_ref}: {error}") from error
    files = _tree_files(export_root)
    manifest = {
        "schema_version": 1,
        "source_ref": config.source_ref,
        "party": party,
        "files": files,
        "excluded": sorted(set(excluded)),
        "exclusion_policy": ["collab/", "var/", ".git/"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _make_read_only(export_root)
    return SourceExport(
        party=party,
        root=export_root,
        source_ref=config.source_ref,
        manifest_path=manifest_path,
        manifest_sha256=_file_hash(manifest_path),
        files=files,
        excluded=tuple(sorted(set(excluded))),
    )


def _tracked_bytes(repository_root: Path, source_ref: str, relative: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", str(repository_root), "cat-file", "-e", f"{source_ref}:{relative}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30,
    )
    if proc.returncode != 0:
        return None
    data = _git(repository_root, ["show", f"{source_ref}:{relative}"], binary=True)
    assert isinstance(data, bytes)
    return data


def materialize_docket(config: BrokerConfig) -> DocketRevision:
    repo = config.repository_root.resolve()
    records: list[dict[str, object]] = []
    payloads: list[tuple[str, bytes]] = []
    for raw_path in config.docket_files:
        path = Path(raw_path)
        absolute = path.resolve() if path.is_absolute() else (repo / path).resolve()
        if not absolute.is_relative_to(repo) or absolute == repo:
            raise channel.ChannelError(f"refused: docket file {raw_path!r} is outside repository {repo}")
        relative = absolute.relative_to(repo).as_posix()
        pinned = _tracked_bytes(repo, config.source_ref, relative)
        tracked = pinned is not None
        if pinned is None:
            try:
                pinned = absolute.read_bytes()
            except OSError as error:
                raise channel.ChannelError(f"refused: cannot read cited docket file {absolute}: {error}") from error
        payloads.append((relative, pinned))
        records.append(
            {
                "path": relative,
                "sha256": _bytes_hash(pinned),
                "tracked_at_source_ref": tracked,
            }
        )
    revision_sha = _canonical_hash(records)
    docket_root = config.runtime_root / "dockets" / revision_sha
    manifest_path = docket_root / "manifest.json"
    if docket_root.exists():
        if not manifest_path.is_file():
            raise channel.ChannelError(f"refused: incomplete immutable docket revision {docket_root}")
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise channel.ChannelError(f"refused: unreadable docket manifest {manifest_path}: {error}") from error
        if existing.get("files") != records or existing.get("revision_sha256") != revision_sha:
            raise channel.ChannelError(f"refused: immutable docket manifest changed at {docket_root}")
        for record in records:
            materialized = docket_root / "files" / str(record["path"])
            if not materialized.is_file() or _file_hash(materialized) != record["sha256"]:
                raise channel.ChannelError(
                    f"refused: immutable docket file changed after creation: {record['path']}"
                )
        return DocketRevision(docket_root, revision_sha, manifest_path, tuple(records))
    files_root = docket_root / "files"
    files_root.mkdir(parents=True)
    for relative, data in payloads:
        destination = files_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    manifest = {
        "schema_version": 1,
        "source_ref": config.source_ref,
        "revision_sha256": revision_sha,
        "files": records,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _make_read_only(docket_root)
    return DocketRevision(docket_root, revision_sha, manifest_path, tuple(records))


def _adapter_environment(config: BrokerConfig, profile: AdapterProfile, runtime: Path) -> dict[str, str]:
    environment = {key: os.environ[key] for key in profile.environment_allowlist if key in os.environ}
    environment.update(profile.environment)
    home = runtime / "home"
    build = runtime / "build"
    temp = runtime / "tmp"
    for path in (home, build, temp, home / ".config", home / ".cache", home / ".local" / "share"):
        path.mkdir(parents=True, exist_ok=True)
    environment.update(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_DATA_HOME": str(home / ".local" / "share"),
            "TMPDIR": str(temp),
            "TEMP": str(temp),
            "TMP": str(temp),
            "GIT_CEILING_DIRECTORIES": str(config.repository_root.resolve()),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PYTEST_ADDOPTS": f"-p no:cacheprovider --basetemp={build / 'pytest'}",
        }
    )
    return environment


def _parse_result(path: Path, party: str, profile: AdapterProfile) -> AdapterResult:
    try:
        data = path.read_bytes()
    except OSError as error:
        raise AdapterError(f"refused: adapter {party!r} did not create its result file: {error}") from error
    if len(data) > 1024 * 1024:
        raise AdapterError(f"refused: adapter {party!r} result exceeds the 1 MiB limit")
    try:
        raw = json.loads(data.decode("utf-8"))
    except (UnicodeError, ValueError) as error:
        raise AdapterError(f"refused: adapter {party!r} result is not valid UTF-8 JSON: {error}") from error
    if not isinstance(raw, dict):
        raise AdapterError(f"refused: adapter {party!r} result must be a JSON object")
    if "sender" in raw:
        raise AdapterError(
            f"refused: adapter {party!r} supplied controller-owned field 'sender'; sender is seat-bound"
        )
    if raw.get("schema_version") != RESULT_SCHEMA_VERSION:
        raise AdapterError(
            f"refused: adapter {party!r} result schema_version must be {RESULT_SCHEMA_VERSION}"
        )
    entry_type = raw.get("entry_type")
    if entry_type not in ("verdict", "fix-report", "question", "info"):
        raise AdapterError(f"refused: adapter {party!r} supplied invalid entry_type {entry_type!r}")
    body = raw.get("body")
    runtime_model = raw.get("runtime_model")
    if not isinstance(body, str) or not body.strip():
        raise AdapterError(f"refused: adapter {party!r} result body must be a non-empty string")
    if not isinstance(runtime_model, str) or not runtime_model.strip():
        raise AdapterError(f"refused: adapter {party!r} must report its resolved runtime_model")
    if profile.expected_runtime_model is not None and runtime_model != profile.expected_runtime_model:
        raise AdapterError(
            f"refused: adapter {party!r} resolved model {runtime_model!r}, "
            f"expected {profile.expected_runtime_model!r}"
        )
    refs = raw.get("refs", "")
    appendix = raw.get("appendix_markdown", "")
    if not isinstance(refs, str) or len(refs.splitlines()) > 1:
        raise AdapterError(f"refused: adapter {party!r} refs must be a single string line")
    if not isinstance(appendix, str):
        raise AdapterError(f"refused: adapter {party!r} appendix_markdown must be a string")
    decision = raw.get("decision")
    if entry_type == "verdict":
        if decision not in SEAT_DECISIONS:
            raise AdapterError(
                f"refused: adapter {party!r} verdict decision must be one of {SEAT_DECISIONS}"
            )
    elif decision is not None:
        raise AdapterError(
            f"refused: adapter {party!r} supplied a decision on non-verdict entry type {entry_type!r}"
        )
    return AdapterResult(
        entry_type,
        body.strip(),
        refs,
        appendix.strip(),
        runtime_model.strip(),
        str(decision) if decision is not None else None,
    )


class BrokerController:
    def __init__(self, config: BrokerConfig, *, now: datetime | None = None) -> None:
        self.config = config
        self._fixed_now = now

    def _now(self) -> datetime:
        return self._fixed_now or datetime.now(timezone.utc)

    def _case_path(self, thread: str) -> Path:
        return self.config.runtime_root / "cases" / thread / "case.json"

    def _load_case(self, thread: str) -> dict[str, object]:
        path = self._case_path(thread)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise channel.ChannelError(f"refused: unreadable brokered case {thread!r}: {error}") from error
        if not isinstance(raw, dict) or raw.get("thread") != thread:
            raise channel.ChannelError(f"refused: invalid brokered case state for {thread!r}")
        return raw

    def _write_case(self, thread: str, state: dict[str, object]) -> None:
        _atomic_json(self._case_path(thread), state)

    @staticmethod
    def _deadline_from(state: dict[str, object], thread: str) -> datetime:
        try:
            deadline = datetime.fromisoformat(str(state["deadline"]).replace("Z", "+00:00"))
        except (KeyError, ValueError) as error:
            raise channel.ChannelError(f"refused: open case {thread!r} has an unreadable deadline") from error
        if deadline.tzinfo is None:
            raise channel.ChannelError(f"refused: open case {thread!r} deadline is not timezone-aware")
        return deadline

    def _revision_record(
        self, exports: dict[str, SourceExport], docket: DocketRevision
    ) -> dict[str, object]:
        revision: dict[str, object] = {
            "source_ref": self.config.source_ref,
            "source_manifests": {
                party: export.manifest_sha256 for party, export in sorted(exports.items())
            },
            "docket_revision_sha256": docket.revision_sha256,
            "docket_files": list(docket.files),
            "config_sha256": self.config.config_sha256,
        }
        revision["revision_sha256"] = _canonical_hash(revision)
        return revision

    def _prepare_case(self, thread: str) -> tuple[dict[str, SourceExport], DocketRevision, datetime]:
        exports = {party: create_source_export(self.config, party) for party in sorted(self.config.profiles)}
        docket = materialize_docket(self.config)
        revision = self._revision_record(exports, docket)
        case_root = self.config.runtime_root / "cases" / thread
        manifest_path = self._case_path(thread)
        identity = {
            "schema_version": 1,
            "thread": thread,
            "source_ref": self.config.source_ref,
            "source_manifests": {
                party: export.manifest_sha256 for party, export in sorted(exports.items())
            },
            "docket_revision_sha256": docket.revision_sha256,
            "profile_sha256": self.config.profile_hashes,
            "config_sha256": self.config.config_sha256,
            "topology": self.config.topology,
        }
        if manifest_path.exists():
            try:
                existing = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as error:
                raise channel.ChannelError(f"refused: unreadable open-case manifest {manifest_path}: {error}") from error
            if existing.get("pending_revision") is not None:
                raise channel.ChannelError(
                    f"refused: open case {thread!r} has a half-finished broker-revise; "
                    "re-run broker-revise before invoking a seat"
                )
            for key, value in identity.items():
                if existing.get(key) != value:
                    raise channel.ChannelError(
                        f"refused: open case {thread!r} changed {key}; create a new case instead of drifting provenance"
                    )
            try:
                deadline = datetime.fromisoformat(str(existing["deadline"]).replace("Z", "+00:00"))
            except (KeyError, ValueError) as error:
                raise channel.ChannelError(f"refused: open case {thread!r} has an unreadable deadline") from error
            return exports, docket, deadline
        case_root.mkdir(parents=True, exist_ok=True)
        now = self._now()
        deadline = now + timedelta(seconds=self.config.timing.whole_case_timeout_seconds)
        manifest = {
            **identity,
            "opened_at": now.isoformat(timespec="seconds"),
            "deadline": deadline.isoformat(timespec="seconds"),
            "timing": self.config.timing.report(),
            "profiles": {
                party: profile.sanitized_manifest() for party, profile in sorted(self.config.profiles.items())
            },
            "docket_files": list(docket.files),
            "revisions": [revision],
            "phase": "docket",
            "sealed_submissions": {},
            "latest_votes": {},
        }
        _atomic_json(manifest_path, manifest)
        return exports, docket, deadline

    def render_input(
        self,
        *,
        party: str,
        phase: str,
        thread: str,
        result_path: Path,
        source: SourceExport,
        docket: DocketRevision,
        transcript: list[dict[str, str]] | None,
    ) -> dict[str, object]:
        if phase not in ("sealed", "open", "deliberation"):
            raise channel.ChannelError(f"refused: unsupported adapter input phase {phase!r}")
        if phase == "sealed" and transcript:
            raise channel.ChannelError("refused: a sealed adapter input may not contain an opponent transcript")
        profile = self.config.profiles[party]
        payload: dict[str, object] = {
            "schema_version": 1,
            "phase": phase,
            "thread": thread,
            "seat": {
                "party": party,
                "author_relationship": profile.author_relationship,
                "topology": self.config.topology,
            },
            "source": {
                "root": str(source.root),
                "ref": source.source_ref,
                "manifest_sha256": source.manifest_sha256,
            },
            "docket": {
                "root": str(docket.root / "files"),
                "revision_sha256": docket.revision_sha256,
                "files": list(docket.files),
            },
            "result": {
                "path": str(result_path),
                "schema_version": RESULT_SCHEMA_VERSION,
                "controller_owned_fields": ["sender"],
                "required_fields": [
                    "schema_version",
                    "entry_type",
                    "body",
                    "runtime_model",
                    "decision (PASS or NO_PASS for verdicts)",
                ],
            },
            "instructions": (
                "Inspect the complete pinned source and docket. Write only the structured result file. "
                "Do not edit the source, do not access a Debate channel, and do not include private reasoning."
            ),
        }
        if phase in ("open", "deliberation"):
            payload["current_thread"] = transcript or []
        encoded = json.dumps(payload, sort_keys=True)
        for label, token in self.config.contamination_canaries.items():
            if token and token in encoded:
                raise channel.ChannelError(
                    f"refused: controller leaked contamination canary {label!r} into {party!r} input"
                )
        return payload

    def open_case(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        thread: str,
        first_party: str,
        body: str,
        refs: str = "",
    ) -> str:
        """Snapshot a neutral case, then open it as supervisor with a seat due."""
        if first_party not in self.config.profiles:
            raise channel.ChannelError(
                f"refused: first_party {first_party!r} has no adapter profile in this case"
            )
        exports, docket, deadline = self._prepare_case(thread)
        case_state = self._load_case(thread)
        recorded_first = case_state.get("first_party")
        if recorded_first not in (None, first_party):
            raise channel.ChannelError(
                f"refused: case {thread!r} already records first_party {recorded_first!r}"
            )
        case_state.update({"phase": "docket", "first_party": first_party})
        self._write_case(thread, case_state)
        channel_config = channel.load_config(channel_root, channel_name)
        provenance = (
            "\n\nController-Docket-Provenance:\n"
            f"- topology: {self.config.topology}\n"
            f"- controller-config-sha256: {self.config.config_sha256}\n"
            f"- source-ref: {self.config.source_ref}\n"
            f"- docket-revision-sha256: {docket.revision_sha256}\n"
            f"- docket-files: {json.dumps(list(docket.files), sort_keys=True)}\n"
            f"- profile-sha256: {json.dumps(self.config.profile_hashes, sort_keys=True)}\n"
            f"- sanitized-profile-manifests: "
            f"{json.dumps({party: profile.sanitized_manifest() for party, profile in sorted(self.config.profiles.items())}, sort_keys=True)}\n"
            f"- source-manifest-sha256: "
            f"{json.dumps({party: export.manifest_sha256 for party, export in sorted(exports.items())}, sort_keys=True)}"
        )
        return channel.post(
            channel_root,
            channel_config.supervisor,
            "review-request",
            thread,
            body + provenance,
            refs=refs,
            name=channel_name,
            _initial_turn=first_party,
            _managed_phase="docket",
            _case_deadline=deadline.isoformat(timespec="seconds"),
        )

    def revise_case(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        thread: str,
        body: str,
        refs: str = "",
    ) -> str:
        """Snapshot an amended artifact and record it without changing the turn."""
        exports = {party: create_source_export(self.config, party) for party in sorted(self.config.profiles)}
        docket = materialize_docket(self.config)
        revision = self._revision_record(exports, docket)
        revision_sha = str(revision["revision_sha256"])
        manifest_path = self.config.runtime_root / "cases" / thread / "case.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise channel.ChannelError(
                f"refused: cannot revise absent or unreadable open case {thread!r}: {error}"
            ) from error
        if manifest.get("profile_sha256") != self.config.profile_hashes:
            raise channel.ChannelError(
                f"refused: open case {thread!r} changed profile_sha256; a profile change requires a new case"
            )
        if manifest.get("topology") != self.config.topology:
            raise channel.ChannelError(
                f"refused: open case {thread!r} changed topology; a topology change requires a new case"
            )
        if manifest.get("timing") != self.config.timing.report():
            raise channel.ChannelError(
                f"refused: open case {thread!r} changed its timing/deadline policy"
            )
        revisions = list(manifest.get("revisions", []))
        if any(item.get("revision_sha256") == revision_sha for item in revisions if isinstance(item, dict)):
            raise channel.ChannelError(
                f"refused: artifact revision {revision_sha} is already recorded for case {thread!r}"
            )
        pending = manifest.get("pending_revision")
        if pending is not None and pending != revision:
            raise channel.ChannelError(
                f"refused: case {thread!r} has a different half-finished revision; finish that revision first"
            )
        if pending is None:
            manifest["pending_revision"] = revision
            _atomic_json(manifest_path, manifest)

        provenance = (
            "\n\nController-Revision-Provenance:\n"
            f"- revision-sha256: {revision_sha}\n"
            f"- controller-config-sha256: {self.config.config_sha256}\n"
            f"- source-ref: {self.config.source_ref}\n"
            f"- docket-revision-sha256: {docket.revision_sha256}\n"
            f"- docket-files: {json.dumps(list(docket.files), sort_keys=True)}\n"
            f"- source-manifest-sha256: "
            f"{json.dumps({party: export.manifest_sha256 for party, export in sorted(exports.items())}, sort_keys=True)}"
        )
        matching = [
            entry
            for entry in channel.read_entries(channel_root, channel_name)
            if entry.thread == thread and f"revision-sha256: {revision_sha}" in entry.body
        ]
        if matching:
            entry_id = f"MSG-{matching[-1].seq}"
        else:
            channel_config = channel.load_config(channel_root, channel_name)
            entry_id = channel.post(
                channel_root,
                channel_config.supervisor,
                "info",
                thread,
                body + provenance,
                refs=refs,
                name=channel_name,
            )

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("pending_revision") != revision:
            raise channel.ChannelError(
                f"refused: case {thread!r} revision state changed while it was being recorded"
            )
        revisions = list(manifest.get("revisions", []))
        revisions.append({**revision, "record_entry": entry_id})
        manifest.update(
            {
                "source_ref": self.config.source_ref,
                "source_manifests": revision["source_manifests"],
                "docket_revision_sha256": docket.revision_sha256,
                "docket_files": list(docket.files),
                "config_sha256": self.config.config_sha256,
                "revisions": revisions,
            }
        )
        manifest.pop("pending_revision", None)
        _atomic_json(manifest_path, manifest)
        return entry_id

    def _invoke(
        self,
        *,
        party: str,
        phase: str,
        thread: str,
        sequence: int,
        attempt: int,
        transcript: list[dict[str, str]] | None,
    ) -> tuple[AdapterResult, dict[str, str | Path]]:
        if party not in self.config.profiles:
            raise channel.ChannelError(f"refused: no adapter profile bound to party {party!r}")
        exports, docket, deadline = self._prepare_case(thread)
        remaining = (deadline - self._now()).total_seconds()
        if remaining <= 0:
            raise AdapterError(
                f"refused: whole-case deadline expired for thread {thread!r}",
                close_reason="case-deadline-expired",
            )
        profile = self.config.profiles[party]
        invocation_root = self.config.runtime_root / "cases" / thread / "invocations" / f"{sequence}-{party}-{attempt}"
        if invocation_root.exists():
            raise AdapterError(f"refused: invocation path already exists: {invocation_root}")
        invocation_root.mkdir(parents=True)
        result_path = invocation_root / "result.json"
        input_path = invocation_root / "input.json"
        source = exports[party]
        payload = self.render_input(
            party=party,
            phase=phase,
            thread=thread,
            result_path=result_path,
            source=source,
            docket=docket,
            transcript=transcript,
        )
        input_bytes = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        input_path.write_bytes(input_bytes)
        input_path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        replacements = {
            "{input_path}": str(input_path),
            "{result_path}": str(result_path),
            "{export_root}": str(source.root),
            "{docket_root}": str(docket.root / "files"),
        }
        argv: list[str] = []
        for argument in profile.command:
            expanded = argument
            for marker, value in replacements.items():
                expanded = expanded.replace(marker, value)
            argv.append(expanded)
        environment = _adapter_environment(self.config, profile, invocation_root)
        timeout = min(profile.timeout_seconds, remaining)
        try:
            proc = subprocess.run(
                argv,
                cwd=source.root,
                env=environment,
                text=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as error:
            deadline_limited = timeout >= remaining
            raise AdapterError(
                f"adapter {party!r} timed out after {timeout:g}s within the whole-case budget",
                retryable=(not deadline_limited and attempt <= profile.retry_limit),
                close_reason="case-deadline-expired" if deadline_limited else "adapter-timeout",
            ) from error
        except (OSError, ValueError) as error:
            raise AdapterError(f"refused: cannot launch adapter {party!r}: {error}") from error
        stdout_path = invocation_root / "stdout.txt"
        stderr_path = invocation_root / "stderr.txt"
        stdout_path.write_text(proc.stdout, encoding="utf-8")
        stderr_path.write_text(proc.stderr, encoding="utf-8")
        combined = proc.stdout + "\n" + proc.stderr
        if result_path.exists():
            try:
                combined += "\n" + result_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                pass
        for label, token in self.config.contamination_canaries.items():
            if token and token in combined:
                rejection = {
                    "reason": "contamination-canary-observed",
                    "canary_label": label,
                    "party": party,
                    "profile_sha256": profile.profile_sha256,
                }
                (invocation_root / "rejection.json").write_text(
                    json.dumps(rejection, indent=2, sort_keys=True), encoding="utf-8"
                )
                raise AdapterError(
                    f"refused: adapter {party!r} exposed contamination canary {label!r}; profile rejected"
                )
        if proc.returncode != 0:
            raise AdapterError(f"refused: adapter {party!r} exited {proc.returncode}; see {stderr_path}")
        if _tree_files(source.root) != source.files:
            raise AdapterError(f"refused: adapter {party!r} modified its immutable source export")
        result = _parse_result(result_path, party, profile)
        return result, {
            "input_sha256": _bytes_hash(input_bytes),
            "source_manifest_sha256": source.manifest_sha256,
            "docket_revision_sha256": docket.revision_sha256,
            "diagnostics_root": invocation_root,
        }

    def _published_body(
        self,
        *,
        party: str,
        result: AdapterResult,
        evidence: dict[str, str | Path],
        phase: str,
        reveal_id: str | None = None,
    ) -> str:
        profile = self.config.profiles[party]
        appendix = f"\n\n{result.appendix_markdown}" if result.appendix_markdown else ""
        typed = f"\n\nController-Decision:\n- decision: {result.decision}" if result.decision else ""
        reveal = (
            f"\n\nController-Sealed-Reveal:\n- reveal-id: {reveal_id}\n- phase: sealed"
            if reveal_id is not None
            else ""
        )
        provenance = (
            "\n\nController-Provenance:\n"
            f"- phase: {phase}\n"
            f"- topology: {self.config.topology}\n"
            f"- author-relationship: {profile.author_relationship}\n"
            f"- profile-sha256: {profile.profile_sha256}\n"
            f"- controller-config-sha256: {self.config.config_sha256}\n"
            f"- source-ref: {self.config.source_ref}\n"
            f"- source-manifest-sha256: {evidence['source_manifest_sha256']}\n"
            f"- docket-revision-sha256: {evidence['docket_revision_sha256']}\n"
            f"- input-sha256: {evidence['input_sha256']}\n"
            f"- requested-model: {profile.requested_model}\n"
            f"- runtime-model: {result.runtime_model}\n"
            f"- reasoning-effort: {profile.reasoning_effort}\n"
            f"- cli-version: {profile.cli_version}\n"
            f"- isolation-mode: {profile.isolation_mode}"
        )
        return result.body + appendix + typed + reveal + provenance

    @staticmethod
    def _result_record(result: AdapterResult, evidence: dict[str, str | Path]) -> dict[str, object]:
        return {
            "result": {
                "entry_type": result.entry_type,
                "body": result.body,
                "refs": result.refs,
                "appendix_markdown": result.appendix_markdown,
                "runtime_model": result.runtime_model,
                "decision": result.decision,
            },
            "evidence": {key: str(value) for key, value in evidence.items()},
            "record_sha256": _canonical_hash(
                {
                    "entry_type": result.entry_type,
                    "body": result.body,
                    "refs": result.refs,
                    "appendix_markdown": result.appendix_markdown,
                    "runtime_model": result.runtime_model,
                    "decision": result.decision,
                    "evidence": {key: str(value) for key, value in evidence.items()},
                }
            ),
        }

    @staticmethod
    def _recorded_result(record: dict[str, object]) -> tuple[AdapterResult, dict[str, str | Path]]:
        raw_result = record.get("result")
        raw_evidence = record.get("evidence")
        if not isinstance(raw_result, dict) or not isinstance(raw_evidence, dict):
            raise channel.ChannelError("refused: malformed private sealed submission")
        try:
            result = AdapterResult(
                entry_type=str(raw_result["entry_type"]),
                body=str(raw_result["body"]),
                refs=str(raw_result.get("refs", "")),
                appendix_markdown=str(raw_result.get("appendix_markdown", "")),
                runtime_model=str(raw_result["runtime_model"]),
                decision=str(raw_result["decision"]),
            )
        except KeyError as error:
            raise channel.ChannelError("refused: incomplete private sealed submission") from error
        evidence = {str(key): str(value) for key, value in raw_evidence.items()}
        return result, evidence

    def capture_sealed(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        party: str,
        thread: str,
        sequence: int,
        attempt: int,
    ) -> AdapterResult:
        """Capture one initial position privately; publish nothing."""
        state = self._load_case(thread)
        submissions = dict(state.get("sealed_submissions", {}))
        existing = submissions.get(party)
        if isinstance(existing, dict):
            return self._recorded_result(existing)[0]
        if state.get("phase") not in ("docket", "sealed", "reveal"):
            raise channel.ChannelError(
                f"refused: cannot capture a sealed position while case phase is {state.get('phase')!r}"
            )
        result, evidence = self._invoke(
            party=party,
            phase="sealed",
            thread=thread,
            sequence=sequence,
            attempt=attempt,
            transcript=None,
        )
        if result.entry_type != "verdict" or result.decision not in SEAT_DECISIONS:
            raise AdapterError(f"refused: sealed adapter {party!r} must return a typed verdict")
        state = self._load_case(thread)
        deadline = self._deadline_from(state, thread)
        if self._now() >= deadline:
            raise AdapterError(
                f"refused: whole-case deadline expired during sealed invocation for {thread!r}",
                close_reason="case-deadline-expired",
            )
        submissions = dict(state.get("sealed_submissions", {}))
        if party not in submissions:
            submissions[party] = self._result_record(result, evidence)
            state.update({"phase": "sealed", "sealed_submissions": submissions})
            self._write_case(thread, state)
        missing = [seat for seat in self.config.profiles if seat not in submissions]
        if missing:
            channel.update_managed_phase(
                channel_root,
                thread=thread,
                phase="sealed",
                turn=missing[0],
                deadline=deadline.isoformat(timespec="seconds"),
                name=channel_name,
            )
        return result

    def _close_terminal(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        thread: str,
        result: str,
        close_reason: str,
    ) -> DriveOutcome:
        state = self._load_case(thread)
        existing_result = state.get("terminal_result")
        if state.get("phase") == "terminal":
            if existing_result != result or state.get("close_reason") != close_reason:
                raise channel.ChannelError(
                    f"refused: terminal case {thread!r} already records "
                    f"{existing_result!r}/{state.get('close_reason')!r}"
                )
            return DriveOutcome("terminal", f"already terminal as {result}", result, close_reason)
        body = (
            f"Controller closed the managed case as {result}. "
            f"Reason: {close_reason}. Supervisor messages were not counted as party votes."
        )
        entry_id = channel.close_managed_case(
            channel_root,
            thread=thread,
            result=result,
            close_reason=close_reason,
            body=body,
            name=channel_name,
        )
        state = self._load_case(thread)
        state.update(
            {
                "phase": "terminal",
                "terminal_result": result,
                "close_reason": close_reason,
                "terminal_entry": entry_id,
            }
        )
        self._write_case(thread, state)
        return DriveOutcome("terminal", f"{entry_id} closed {result}: {close_reason}", result, close_reason)

    def close_error(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        thread: str,
        close_reason: str,
    ) -> DriveOutcome:
        return self._close_terminal(
            channel_root=channel_root,
            channel_name=channel_name,
            thread=thread,
            result="ERROR",
            close_reason=close_reason,
        )

    def recover_terminal_state(
        self, *, channel_root: Path, channel_name: str, thread: str
    ) -> DriveOutcome:
        """Repair case.json after a crash that already committed the typed channel close."""
        signal = channel.read_signal(channel_root, channel_name)
        if signal.get("phase") != "terminal" or signal.get("case_thread") != thread:
            raise channel.ChannelError(f"refused: channel does not record {thread!r} as its terminal case")
        result = str(signal.get("terminal_result", ""))
        reason = str(signal.get("close_reason", ""))
        if result not in channel.TERMINAL_RESULTS or not reason:
            raise channel.ChannelError(f"refused: terminal channel state for {thread!r} is incomplete")
        state = self._load_case(thread)
        state.update(
            {
                "phase": "terminal",
                "terminal_result": result,
                "close_reason": reason,
                "terminal_entry": signal.get("last_entry"),
            }
        )
        self._write_case(thread, state)
        return DriveOutcome("terminal", f"recovered terminal {result}: {reason}", result, reason)

    def _agreement(self, state: dict[str, object]) -> tuple[str, str] | None:
        votes = state.get("latest_votes", {})
        if not isinstance(votes, dict) or set(votes) != set(self.config.profiles):
            return None
        decisions = {str(record.get("decision")) for record in votes.values() if isinstance(record, dict)}
        if len(decisions) != 1:
            return None
        decision = decisions.pop()
        if decision not in SEAT_DECISIONS:
            return None
        if decision == "PASS":
            agreeing_independent = any(
                self.config.profiles[party].author_relationship == "author-independent"
                and isinstance(votes.get(party), dict)
                and votes[party].get("decision") == "PASS"
                for party in self.config.profiles
            )
            if not agreeing_independent:
                return None
        return decision, "party-vote-agreement"

    def reveal_pair(
        self, *, channel_root: Path, channel_name: str, thread: str
    ) -> DriveOutcome:
        state = self._load_case(thread)
        submissions = state.get("sealed_submissions", {})
        if not isinstance(submissions, dict) or set(submissions) != set(self.config.profiles):
            raise channel.ChannelError("refused: both sealed positions must exist before reveal")
        first_party = str(state.get("first_party", ""))
        if first_party not in self.config.profiles:
            raise channel.ChannelError(f"refused: case {thread!r} has no valid first_party")
        reveal_id = str(
            state.get("reveal_id")
            or _canonical_hash(
                {
                    "thread": thread,
                    "submissions": {
                        party: submissions[party].get("record_sha256")
                        for party in sorted(submissions)
                        if isinstance(submissions[party], dict)
                    },
                }
            )
        )
        state.update({"phase": "reveal", "reveal_id": reveal_id})
        self._write_case(thread, state)
        revealed: list[channel.RevealSubmission] = []
        votes: dict[str, dict[str, object]] = {}
        for party in self.config.profiles:
            record = submissions[party]
            if not isinstance(record, dict):
                raise channel.ChannelError("refused: malformed private sealed submission")
            result, evidence = self._recorded_result(record)
            revealed.append(
                channel.RevealSubmission(
                    sender=party,
                    entry_type="verdict",
                    body=self._published_body(
                        party=party,
                        result=result,
                        evidence=evidence,
                        phase="sealed",
                        reveal_id=reveal_id,
                    ),
                    refs=result.refs,
                )
            )
            votes[party] = {
                "decision": result.decision,
                "author_relationship": self.config.profiles[party].author_relationship,
                "phase": "sealed",
                "reveal_id": reveal_id,
            }
        deadline = self._deadline_from(state, thread)
        entry_ids = channel.commit_reveal_pair(
            channel_root,
            thread=thread,
            submissions=(revealed[0], revealed[1]),
            reveal_id=reveal_id,
            next_turn=first_party,
            deadline=deadline.isoformat(timespec="seconds"),
            name=channel_name,
        )
        state = self._load_case(thread)
        state.update(
            {
                "phase": "deliberation",
                "reveal_entries": list(entry_ids),
                "latest_votes": votes,
            }
        )
        self._write_case(thread, state)
        agreement = self._agreement(state)
        if agreement is not None:
            return self._close_terminal(
                channel_root=channel_root,
                channel_name=channel_name,
                thread=thread,
                result=agreement[0],
                close_reason=agreement[1],
            )
        return DriveOutcome("deliberation", f"revealed {entry_ids[0]} and {entry_ids[1]}; votes disagree")

    def drive_case(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        thread: str,
        sequence: int,
        attempt: int,
    ) -> DriveOutcome:
        """Advance exactly one managed case to its next stable public state."""
        self._prepare_case(thread)
        state = self._load_case(thread)
        signal = channel.read_signal(channel_root, channel_name)
        if signal.get("phase") == "terminal":
            return self.recover_terminal_state(
                channel_root=channel_root, channel_name=channel_name, thread=thread
            )
        deadline = self._deadline_from(state, thread)
        if self._now() >= deadline:
            return self.close_error(
                channel_root=channel_root,
                channel_name=channel_name,
                thread=thread,
                close_reason="case-deadline-expired",
            )
        first_party = str(state.get("first_party", ""))
        if first_party not in self.config.profiles:
            raise channel.ChannelError(f"refused: case {thread!r} has no valid first_party")
        phase = str(state.get("phase", "docket"))
        if phase == "docket":
            state["phase"] = "sealed"
            self._write_case(thread, state)
            channel.update_managed_phase(
                channel_root,
                thread=thread,
                phase="sealed",
                turn=first_party,
                deadline=deadline.isoformat(timespec="seconds"),
                name=channel_name,
            )
            phase = "sealed"
        if phase in ("sealed", "reveal"):
            other = next(party for party in self.config.profiles if party != first_party)
            order = (first_party, other)
            for party in order:
                current = self._load_case(thread)
                submissions = current.get("sealed_submissions", {})
                if not isinstance(submissions, dict) or party not in submissions:
                    try:
                        self.capture_sealed(
                            channel_root=channel_root,
                            channel_name=channel_name,
                            party=party,
                            thread=thread,
                            sequence=sequence,
                            attempt=attempt,
                        )
                    except AdapterError as error:
                        if error.close_reason == "case-deadline-expired":
                            return self.close_error(
                                channel_root=channel_root,
                                channel_name=channel_name,
                                thread=thread,
                                close_reason=error.close_reason,
                            )
                        raise
            return self.reveal_pair(channel_root=channel_root, channel_name=channel_name, thread=thread)
        if phase != "deliberation":
            raise channel.ChannelError(f"refused: unknown managed case phase {phase!r}")
        entries = channel.thread_entries(channel_root, thread, channel_name)
        channel_config = channel.load_config(channel_root, channel_name)
        if len(entries) >= channel_config.thread_cap:
            return self._close_terminal(
                channel_root=channel_root,
                channel_name=channel_name,
                thread=thread,
                result="NO_PASS",
                close_reason="thread-cap-exhausted",
            )
        turn = str(signal.get("turn", ""))
        if turn not in self.config.profiles:
            raise channel.ChannelError(f"refused: deliberation has invalid turn {turn!r}")
        transcript = [
            {
                "id": f"MSG-{entry.seq}",
                "sender": entry.sender,
                "type": entry.entry_type,
                "refs": entry.refs,
                "body": entry.body,
            }
            for entry in entries
        ]
        outcome = self.invoke_and_post(
            channel_root=channel_root,
            channel_name=channel_name,
            party=turn,
            thread=thread,
            sequence=sequence,
            attempt=attempt,
            transcript=transcript,
            phase="deliberation",
        )
        state = self._load_case(thread)
        agreement = self._agreement(state)
        if agreement is not None:
            return self._close_terminal(
                channel_root=channel_root,
                channel_name=channel_name,
                thread=thread,
                result=agreement[0],
                close_reason=agreement[1],
            )
        if len(channel.thread_entries(channel_root, thread, channel_name)) >= channel_config.thread_cap:
            return self._close_terminal(
                channel_root=channel_root,
                channel_name=channel_name,
                thread=thread,
                result="NO_PASS",
                close_reason="thread-cap-exhausted",
            )
        return DriveOutcome("deliberation", f"published {outcome.entry_id}; votes still disagree")

    def invoke_and_post(
        self,
        *,
        channel_root: Path,
        channel_name: str,
        party: str,
        thread: str,
        sequence: int,
        attempt: int,
        transcript: list[dict[str, str]],
        phase: str = "deliberation",
    ) -> BrokerOutcome:
        result, evidence = self._invoke(
            party=party,
            phase=phase,
            thread=thread,
            sequence=sequence,
            attempt=attempt,
            transcript=transcript,
        )
        profile = self.config.profiles[party]
        entry_id = channel.post(
            channel_root,
            party,
            result.entry_type,
            thread,
            self._published_body(
                party=party,
                result=result,
                evidence=evidence,
                phase="deliberation" if phase == "open" else phase,
            ),
            refs=result.refs,
            name=channel_name,
            _brokered=True,
        )
        state = self._load_case(thread)
        if result.decision is not None:
            votes = dict(state.get("latest_votes", {}))
            votes[party] = {
                "decision": result.decision,
                "author_relationship": profile.author_relationship,
                "phase": "deliberation" if phase == "open" else phase,
                "entry_id": entry_id,
            }
            state.update({"phase": "deliberation", "latest_votes": votes})
            self._write_case(thread, state)
        return BrokerOutcome(
            entry_id=entry_id,
            party=party,
            profile_sha256=profile.profile_sha256,
            source_manifest_sha256=str(evidence["source_manifest_sha256"]),
            docket_revision_sha256=str(evidence["docket_revision_sha256"]),
            input_sha256=str(evidence["input_sha256"]),
            runtime_model=result.runtime_model,
            diagnostics_root=Path(evidence["diagnostics_root"]),
            decision=result.decision,
        )


def doctor_lines(config: BrokerConfig) -> list[str]:
    """Non-charge-bearing validation/report used by ``debate adapter-doctor``."""
    resolved = str(_git(config.repository_root, ["rev-parse", f"{config.source_ref}^{{commit}}"])).strip()
    if resolved != config.source_ref:
        raise channel.ChannelError(
            f"refused: source_ref {config.source_ref} does not resolve to the recorded commit"
        )
    for party, profile in sorted(config.profiles.items()):
        executable = profile.command[0]
        if "{" in executable or "}" in executable:
            raise channel.ChannelError(
                f"refused: adapter executable for {party!r} may not be a generated placeholder"
            )
        if Path(executable).is_absolute():
            available = Path(executable).is_file()
        else:
            search_path = profile.environment.get("PATH")
            if search_path is None and "PATH" in profile.environment_allowlist:
                search_path = os.environ.get("PATH")
            available = search_path is not None and shutil.which(executable, path=search_path) is not None
        if not available:
            raise channel.ChannelError(
                f"refused: adapter executable for {party!r} is not available: {executable!r}"
            )
    lines = [
        f"topology: {config.topology}",
        f"source ref: {config.source_ref}",
        f"runtime root: {config.runtime_root.resolve()}",
    ]
    for party, profile in sorted(config.profiles.items()):
        lines.append(
            f"seat {party}: provider={profile.provider} requested_model={profile.requested_model} "
            f"relationship={profile.author_relationship} authentication={profile.authentication_mode} "
            f"cost_mode={profile.cost_mode} "
            f"isolation={profile.isolation_mode} profile_sha256={profile.profile_sha256}"
        )
    timing = config.timing.report()
    lines.append(f"unconstrained schedule: {timing['unconstrained_schedule_seconds']}s")
    lines.append(f"whole-case deadline: {timing['whole_case_timeout_seconds']}s")
    lines.append(f"enforced terminal bound: {timing['enforced_terminal_bound_seconds']}s")
    lines.append("doctor: configuration valid; no adapter invoked and no charge incurred")
    return lines
