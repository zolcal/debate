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
- kimi: the kimi-code CLI selects its model alias via ``-m`` (aliases read
  from ``~/.kimi-code/config.toml`` 2026-08-16); thinking effort lives in
  that config's ``[thinking]`` table, NOT in argv, so ``known_efforts`` is
  recorded with an empty ``effort_argv``.
- deepseek: the ``deepseek-flash-agent`` wrapper env-pins deepseek-v4-flash
  (verified 2026-08-16) -- single-seat rule.

grok is deliberately ABSENT: its CLI's model selection could not be verified
from ``--help`` on this machine, and the catalog ships only verified strings.

The single-seat rule (plan D1): an entry whose ``submodel_argv`` is empty
lists EXACTLY the one submodel its binary verifiably pins; discovery seeds
one seat per submodel ONLY for entries that can select one via argv.
"""

from __future__ import annotations

from dataclasses import dataclass


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


CATALOG: tuple[CatalogEntry, ...] = (
    CatalogEntry(
        vendor="claude",
        binaries=("claude",),
        submodels=("opus", "sonnet", "haiku"),
        known_efforts=("low", "medium", "high"),
        invocation=("{binary}", "-p", "{prompt}"),
        submodel_argv=("--model", "{submodel}"),
        effort_argv=("--effort", "{effort}"),
        notes="flags from claude --help; opus/high proven by the 02750 brokered seat",
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
    ),
)
