"""The seat catalog: which vendor CLIs discovery knows how to find.

Curated DATA, versioned with the tool -- a tool upgrade re-triggers
discovery precisely because the new catalog may know seats the old one did
not. Every string below is pinned against the installed CLI's own help or a
proven production invocation, never from memory (plan rule, "no guessing"):

- claude: ``--model``/``--effort`` flags read from ``claude --help`` on this
  machine 2026-08-16; the alias and effort values are the ones the
  repository's own brokered opus seat has run in production since 2026-08-06.
- codex: the ``codex-agent`` wrapper defers model AND effort to
  ``~/.codex/config.toml`` (pin gpt-5.6-sol verified 2026-08-15) -- the
  single-seat rule applies.
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
and codex's are the production bridges' flags, run on every gate since
2026-08-06; kimi, glm and deepseek carry NEITHER (nothing verified for them
yet), so both fields are empty for those three entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

CAPABILITY_CLASSES = ("frontier", "light")

# The documented vendor configuration-home variables -- the ONLY names a
# config_home declaration may name without also clearing the reserved/sandbox
# checks in seats.validate_config_home.
VENDOR_CONFIG_HOME_VARS: frozenset[str] = frozenset({"CLAUDE_CONFIG_DIR", "CODEX_HOME"})


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
    # "VAR=relative/dir": the vendor's documented configuration-home
    # variable and its folder, relative to $HOME. None means undeclared.
    config_home: str | None = None


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
        config_home="CLAUDE_CONFIG_DIR=.claude",
    ),
    CatalogEntry(
        vendor="codex",
        binaries=("codex-agent",),
        submodels=("gpt-5.6-sol",),
        known_efforts=("xhigh",),
        invocation=("{binary}", "{prompt}"),
        submodel_argv=(),
        effort_argv=(),
        notes="wrapper defers model and effort to ~/.codex/config.toml (pin verified 2026-08-15)",
        sibling_pattern="codex*-agent",
        capability_classes={"gpt-5.6-sol": "frontier"},
        isolation_argv=("--ignore-user-config", "--ignore-rules"),
        no_persistence_argv=("--ephemeral",),
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
