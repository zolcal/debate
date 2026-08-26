"""The seat catalog: which vendor CLIs discovery knows how to find.

Curated DATA, versioned with the tool -- a tool upgrade re-triggers
discovery precisely because the new catalog may know seats the old one did
not. Every string below is pinned against the installed CLI's own help or a
proven production invocation, never from memory (plan rule, "no guessing"):

- claude: ``--model``/``--effort`` flags read from ``claude --help`` on this
  machine 2026-08-16; the alias and effort values are the ones the
  repository's own brokered opus seat has run in production since 2026-08-06.
- codex: the native ``codex exec`` command selects the model explicitly and
  pins reasoning effort through a command-line config override.  Its
  ``--ignore-user-config``, ``--ignore-rules`` and ``--ephemeral`` flags were
  read from ``codex exec --help`` and parser-checked together on 2026-08-26.
  The old one-argument ``codex-agent`` wrapper was removed from the catalog:
  it discarded every isolation flag Debate appended after the prompt.
- glm: the ``glm-agent`` wrapper env-pins glm-5.3 (verified 2026-08-15) --
  single-seat rule.
- kimi: DECLARED DEVIATION from the plan's wrapper-first seed order, under
  the Slice-1 correct-the-seeds mandate: the ``kimi-agent`` wrapper execs
  ``kimi -p "$1"`` and forwards ONLY the prompt (verified 2026-08-15), so
  it cannot carry the ``-m`` selection flag -- listing it ahead of the bare
  CLI would break submodel selection and collapse the vendor to a single
  pin. The bare, selectable CLI is seeded instead. The kimi-code CLI
  selects its model alias via ``-m`` (aliases read
  from ``~/.kimi-code/config.toml`` 2026-08-16); thinking effort lives in
  that config's ``[thinking]`` table, NOT in argv -- so the entry records
  the config-level tier in ``known_efforts`` for DISPLAY while its
  ``effort_argv`` stays empty (config-level tiers are never derivable).
- deepseek: the ``deepseek-flash-agent`` wrapper env-pins deepseek-v4-flash
  (verified 2026-08-16) -- single-seat rule.

grok is deliberately ABSENT: its CLI's model selection could not be verified
from ``--help`` on this machine, and the catalog ships only verified strings.

The single-seat rule (plan D1): an entry whose ``submodel_argv`` is empty
lists EXACTLY the one submodel its binary verifiably pins; discovery seeds
one seat per submodel ONLY for entries that can select one via argv.

``isolation_argv``/``no_persistence_argv`` are VERIFIED strings too: claude's
are production bridge flags and codex's come from the native CLI help and a
zero-call parser check; kimi, glm and deepseek carry NEITHER (nothing verified
for them yet), so both fields are empty for those three entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

CAPABILITY_CLASSES = ("frontier", "light")

# The documented vendor configuration-home variables -- the ONLY names a
# config_home declaration may name without also clearing the reserved/sandbox
# checks in seats.validate_config_home.
VENDOR_CONFIG_HOME_VARS: frozenset[str] = frozenset({"CLAUDE_CONFIG_DIR", "CODEX_HOME"})

# Credential values never enter catalog or registry data. A seat may name only
# one of these operator-environment variables for launch-time inheritance.
KNOWN_CREDENTIAL_ENV_VARS: frozenset[str] = frozenset({"OPENROUTER_API_KEY"})


@dataclass(frozen=True)
class CatalogEntry:
    """One vendor the discovery scan knows how to probe."""

    vendor: str
    binaries: tuple[str, ...]
    submodels: tuple[str, ...]
    known_efforts: tuple[str, ...]
    invocation: tuple[str, ...]
    submodel_argv: tuple[str, ...]
    effort_argv: tuple[str, ...]
    notes: str
    # A glob for OTHER wrapper binaries that might sit beside this entry's
    # own catalogued binary on PATH (seats.scan_siblings). None opts a bare
    # CLI (claude, kimi) out of sibling scanning entirely.
    sibling_pattern: str | None = None
    # submodel -> "frontier" | "light"; a submodel absent from this mapping
    # is undeclared (no capability class asserted).
    capability_classes: dict[str, str] = field(default_factory=dict)
    # VERIFIED extra argv that makes the CLI ignore its user settings,
    # plugins and hooks while it reviews, and that stops it from persisting
    # a session, respectively. Never guessed -- empty means nothing verified.
    isolation_argv: tuple[str, ...] = ()
    no_persistence_argv: tuple[str, ...] = ()
    # VERIFIED arguments that let a headless review inspect files and run
    # bounded checks. A capable wrapper may need no extra argv.
    verification_argv: tuple[str, ...] = ()
    verification_capable: bool = False
    # "VAR=relative/dir": the vendor's documented configuration-home
    # variable and its folder, relative to $HOME. None means undeclared.
    config_home: str | None = None
    # Code-known credential variable NAMES only. Values are resolved from the
    # launching process at adapter launch and are never serialized.
    credential_env: tuple[str, ...] = ()
    # Optional revisioned third-party data-use notice. Approval records only
    # the accepted revision in the project profile.
    data_policy_revision: str | None = None
    data_policy_notice: str | None = None
    # Current catalog observation shown during inspect, never copied into the
    # host registry or project profile. Time-sensitive by definition.
    price_observation: str | None = None


CATALOG: tuple[CatalogEntry, ...] = (
    CatalogEntry(
        vendor="claude",
        binaries=("claude",),
        submodels=("opus", "sonnet", "haiku"),
        known_efforts=("low", "medium", "high"),
        invocation=("{binary}", "-p", "{prompt}"),
        submodel_argv=("--model", "{submodel}"),
        effort_argv=("--effort", "{effort}"),
        notes="--model/--effort flags read from claude --help 2026-08-16; the opus alias at high effort is production-proven by the 02750 brokered seat; other aliases and tiers are from the same help text",
        sibling_pattern=None,  # bare CLI, not itself a *-agent wrapper
        capability_classes={"opus": "frontier", "sonnet": "frontier", "haiku": "light"},
        isolation_argv=(
            "--safe-mode", "--setting-sources", "", "--strict-mcp-config",
            "--disable-slash-commands",
        ),
        no_persistence_argv=("--no-session-persistence",),
        verification_argv=(
            "--permission-mode", "dontAsk",
            "--tools", "Read,Grep,Glob,Bash",
            "--allowedTools", "Read,Grep,Glob,Bash",
        ),
        verification_capable=True,
        config_home="CLAUDE_CONFIG_DIR=.claude",
    ),
    CatalogEntry(
        vendor="stealth",
        binaries=("claude-ox",),
        submodels=("ox-alpha",),
        known_efforts=("max",),
        invocation=("{binary}", "-p", "{prompt}"),
        submodel_argv=(),
        effort_argv=(),
        notes=(
            "claude-ox pins OpenRouter stealth/ox-alpha at max effort; anonymous-provider "
            "limited preview, checked 2026-08-23; current zero price is not guaranteed"
        ),
        sibling_pattern=None,
        capability_classes={"ox-alpha": "frontier"},
        isolation_argv=(
            "--safe-mode", "--setting-sources", "", "--strict-mcp-config",
            "--disable-slash-commands",
        ),
        no_persistence_argv=("--no-session-persistence",),
        verification_argv=(
            "--permission-mode", "dontAsk",
            "--tools", "Read,Grep,Glob,Bash",
            "--allowedTools", "Read,Grep,Glob,Bash",
        ),
        verification_capable=True,
        config_home="CLAUDE_CONFIG_DIR=.claude-ox",
        credential_env=("OPENROUTER_API_KEY",),
        data_policy_revision="openrouter-stealth-eula-2026-08-23",
        data_policy_notice=(
            "Ox Alpha is an anonymous-provider limited preview. OpenRouter's binding Stealth EULA "
            "permits content retention, sharing, training, and a broad content license. Use only "
            "non-sensitive material. The generic OpenRouter key is visible to the Ox process and "
            "potentially its tools, putting every route and allowance available to that key in scope."
        ),
        price_observation=(
            "Observed 2026-08-23: $0/M input and output; this API-backed preview "
            "price is time-sensitive and not guaranteed."
        ),
    ),
    CatalogEntry(
        vendor="codex",
        binaries=("codex",),
        submodels=("gpt-5.6-sol", "gpt-5.6-terra"),
        known_efforts=("xhigh",),
        invocation=(
            "{binary}", "exec", "--skip-git-repo-check",
            "--sandbox", "workspace-write", "-c",
            'model_reasoning_effort="xhigh"', "{prompt}",
        ),
        submodel_argv=("--model", "{submodel}"),
        effort_argv=(),
        notes=(
            "native codex exec pins model and xhigh effort on argv; isolation/no-history "
            "flags read from codex exec --help and parser-checked 2026-08-26; "
            "--skip-git-repo-check is load-bearing in the base invocation too, because "
            "seat smoke scratch dirs and controller source exports are not git repositories "
            "and codex exec refuses any untrusted non-repo CWD without it (field finding F7); "
            "gpt-5.6-sol is plan-dependent (a ChatGPT-account 400 rejects it on some plans, "
            "field finding F8) while gpt-5.6-terra is production-proven on subscription "
            "OAuth by every 02750 brokered gate, so both are catalogued and smoke decides "
            "per machine; --sandbox workspace-write is load-bearing too, because a "
            "self-posting seat must write the mailbox and lock in its CWD and the default "
            "sandbox denied exactly that lock write (field finding F10)"
        ),
        sibling_pattern=None,
        capability_classes={"gpt-5.6-sol": "frontier", "gpt-5.6-terra": "frontier"},
        isolation_argv=("--ignore-user-config", "--ignore-rules"),
        no_persistence_argv=("--ephemeral",),
        verification_argv=(
            # --skip-git-repo-check and --sandbox live in the base invocation;
            # codex's parser refuses a repeated flag, and the managed bridge
            # composes both layers into one argv (field finding F13).
            "--approve-for-me",
        ),
        verification_capable=True,
        config_home="CODEX_HOME=.codex",
    ),
    CatalogEntry(
        vendor="glm",
        binaries=("glm-agent",),
        submodels=("glm-5.3",),
        known_efforts=(),
        invocation=("{binary}", "{prompt}"),
        submodel_argv=(),
        effort_argv=(),
        notes="wrapper env-pins ANTHROPIC_MODEL=glm-5.3 (verified 2026-08-15)",
        sibling_pattern="glm*-agent",
        capability_classes={},  # glm-5.3 undeclared
        isolation_argv=(),
        no_persistence_argv=(),
        config_home=None,
    ),
    CatalogEntry(
        vendor="kimi",
        binaries=("kimi",),
        submodels=(
            "kimi-code/k3",
            "kimi-code/kimi-for-coding",
            "kimi-code/kimi-for-coding-highspeed",
        ),
        known_efforts=("high",),
        invocation=("{binary}", "-p", "{prompt}"),
        submodel_argv=("-m", "{submodel}"),
        effort_argv=(),
        notes="aliases from ~/.kimi-code/config.toml; thinking effort is config-level, not argv",
        sibling_pattern=None,  # bare CLI, not itself a *-agent wrapper
        capability_classes={
            "kimi-code/k3": "frontier",
            "kimi-code/kimi-for-coding-highspeed": "light",
            # "kimi-code/kimi-for-coding" undeclared
        },
        isolation_argv=(),
        no_persistence_argv=(),
        config_home=None,
    ),
    CatalogEntry(
        vendor="deepseek",
        binaries=("deepseek-flash-agent",),
        submodels=("deepseek-v4-flash",),
        known_efforts=(),
        invocation=("{binary}", "{prompt}"),
        submodel_argv=(),
        effort_argv=(),
        notes="wrapper env-pins deepseek-v4-flash (verified 2026-08-16); dsh headless is a future entry",
        sibling_pattern="deepseek*-agent",
        capability_classes={"deepseek-v4-flash": "light"},
        isolation_argv=(),
        no_persistence_argv=(),
        config_home=None,
    ),
)
