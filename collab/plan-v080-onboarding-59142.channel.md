
## MSG-1 | 2026-08-19T19:04:54+00:00 | from: owner | type: review-request | thread: plan-v080-onboarding-1 | refs: main@ee1e99a0e35e93dea1029609fdcf65c7683fa680

Review request: the v0.8.0 plan doc `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md` (materialized in the case docket by content — docs/plans/ is untracked by design). Round 1 of the plan gate; the doc header is `Status: DRAFT — pending debate review`.

The plan makes Debate an installation-driven product inside Codex and Claude: native plugin per host bundling the engine, an automatic read-only session-start notice, explicit project-scoped seat approval (detected is never approved), and a managed-v2 brokered start path. Authored by Codex; amended 2026-08-19 by the session seat with pre-gate review findings (per-host hook manifests, Slice 1A/1B split, Windows scope, uninstall semantics, distribution/cache/headless notes) folded into the body.

Verify per the docket `plan-v080-docket.md`: (1) section-2.1 repo-evidence claims against the export at the pinned ref; (2) whole-document internal coherence; (3) safety/trust invariants; (4) honesty of capability claims; (5) gate/lifecycle compliance; (6) the docket's exact pytest command. Verdicts cite your own fresh evidence from the export, never this request. Name every blocking finding establishable in your pass, not the first one.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 793d9b60048ed4c26d7cdacf96669b6a05d1c0e19a86fe50b12b24872dcc52f9
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- docket-revision-sha256: b959c5730ce6e8bb5eba29692f4a91f8624c40831a1769b0d8b6305c87c1f0a8
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-onboarding-59142.debate.json", "sha256": "485d531462f4faf4f368ef091f16ba8f4cfa5a696a26fad916c3ae4cd30f02f7", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "71ccc6a2413c7ade784e04fa6f587b1018797b5ca66d71b8382125c285d80331", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/plan-v080-docket.md", "sha256": "baf0a68708cad7843d9b82422aa704f1486e7f7be12f1dcd384aff29d964e74b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/watcher.json", "sha256": "793d9b60048ed4c26d7cdacf96669b6a05d1c0e19a86fe50b12b24872dcc52f9", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "cb0106ad406b8546d585ff690876b9c892be00b01dd014811b149d01bb02be5e", "opus": "080bd7156d2cb5da8cbd62cb590b91f1a6de42b607f2f7894058727519d83b00"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "45b5787068027077009eef50c3625c471289aa2350312d05d75e7cafab99a06e", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "9805d230f5fbf92f58a180eadd747e11728d384cdd0482f61da034c7528f6a5a", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "63a70e313455198f7beac0ed5f9b93cb299056eeb76760c1b1c7384f48f24d49", "opus": "51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc"}

## MSG-2 | 2026-08-19T19:14:13+00:00 | from: opus | type: verdict | thread: plan-v080-onboarding-1 | refs: -

## Verdict: NO_PASS — one blocking finding (docket criterion 3)

### Docket item 6 — required command

Run literally from the pinned export root `/home/zoltan/Projects/debate/var/debate/plan-v080-onboarding-59142/controller/exports/ee1e99a0e35e93dea1029609fdcf65c7683fa680/opus`:

```
python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py
```

Result:

```
.........................................................                [100%]
57 passed in 0.53s
```

The command passes. It is not the reason for NO_PASS.

### Criterion 1 — section 2.1 repo-evidence claims: ALL HOLD

Every checkable section-2.1 claim is confirmed against the export at `ee1e99a`. No section-2.1 claim is contradicted.

- **Only the `debate` console script.** `pyproject.toml:37-38` — `[project.scripts]` contains exactly `debate = "debate.__main__:main"`. Confirmed.
- **`.claude-plugin/` exists; `hooks/hooks.json` and `.codex-plugin/` do not.** Glob `{hooks,.codex-plugin,.claude-plugin,.agents}/**` over the export returns exactly two paths: `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`. No `hooks/`, no `.codex-plugin/`, no `.agents/`. Confirmed, including the section-2.1 claim that `.agents/plugins/marketplace.json` is absent.
- **`skills/debate/SKILL.md` triggers only reactively and fails closed without the CLI.** `SKILL.md:3` description triggers on an existing channel triple, a scheduler wake-up, or an explicit review request; `SKILL.md:20-24` — "**CLI present?** If `debate --help` fails: **STOP — fail closed.**" Confirmed on both halves.
- **`opening.py` writes `channel.MANAGED_VERSION` (= 1) and consults `last_pair`.** `channel.py:54` `MANAGED_VERSION = 1` (and `:55` `BROKERED_MANAGED_VERSION = 2`); `opening.py:280` and `opening.py:297` both pass `managed_version=channel.MANAGED_VERSION`; `opening.py:131` reads `registry.last_pair.get(project)` then `registry.last_pair.get("")`, and `:325-326` write both back. Confirmed. (`__main__.py:685` shows a `--brokered` v2 path exists on `debate init`, but that is a different surface from the `opening.py` picker the row is about, so the row stands as written.)
- **`seats.py` treats a missing project profile as unrestricted.** `seats.py:562-568` — `load_profile` returns `None` when `debate-profile.json` does not exist; the docstring at `:565` says "A missing file is simply no restriction," and the `Profile` docstring at `:548` says "Opt-in per project: no file, no restriction." Confirmed. (Also confirms the plan's §4.2 decision to keep profile schema version 1: `seats.py:584` speaks exactly `1`, and `:596-600` already refuses an empty allowlist, which matches §3.2's "zero approved seats creates no misleading empty profile.")
- **`adapter-doctor` exists.** `__main__.py:452` registers the subcommand, `__main__.py:877` dispatches it, `controller.py:1803` — "Non-charge-bearing validation/report used by ``debate adapter-doctor``." Confirmed, so §4.3's reliance on it is grounded.
- **README exposes implementation commands as the user journey.** `README.md:135` heading "Picking the seats: discovery, the registry, and `debate open`", then `:146` `debate seats discover`, `:147` `debate seats list`, `:152` `debate seats check`, `:155` `debate seats smoke ...`, `:164` `debate open --root ./collab ...`. Confirmed.
- Version context is consistent: `pyproject.toml:7` `version = "0.7.0"` and `src/debate/__init__.py:42` `__version__ = "0.7.0"`.

### Criterion 2 — internal coherence: HOLDS

- **Slice 1A/1B split vs §6/§7/§10.** §5 splits risk-first (1A: hook contract spike, manifests, launcher, read-only `onboarding status`) from state machine (1B: `inspect`/`approve`, brokered open). §7 lists the corresponding files including `onboarding.py` and both hook manifests. §10.5 sequences slice-by-slice and §10 closes with "The first post-approval task is Slice 1A." §6's Hook row carries the two 1A-specific cases ("per-host manifest parse; non-interactive suppression"). No contradiction.
- **Per-host hook manifests vs §2.2/§4.1/§7.** §2.2 ships per-host manifests by default, single shared "only if the Slice 1A spike proves one file parses cleanly in both hosts"; §4.1 names `hooks/hooks.json` (Claude) + `hooks/hooks-codex.json` (Codex) with the identical collapse condition; §7 repeats it verbatim. Three-way consistent. Slice 2's "shared hook" refers to the single `hooks/session-start` script (§4.1), not to a shared manifest — no conflict.
- **Windows scoping vs §6 matrix.** Slice 3 declares Windows out of scope with a stated reason (no OS classifiers — confirmed: `pyproject.toml:14-20` declares none — and no Windows hardware/CI); §6's Paths row reads "(Linux and macOS only — see Slice 3)". Consistent. §7's hedged "platform launcher variants if tests prove they are required" claims no Windows behavior.
- **Uninstall vs §8.** Slice 3 states no host uninstall hook exists, so no interactive retention offer is implementable, and substitutes a byte-comparison invariant; §8's final bullet says the same and cross-references Slice 3. Consistent, and honest about the capability limit rather than promising a flow.
- **managed-v2 default vs §9.** §1.5 / §4.3 ("create managed version 2, never version 1") / §6 invariant ("every new product-created channel records managed version 2") against §9 ("No removal of managed-version-1 compatibility; it simply stops being the product default"). Consistent — default change, not removal.
- **§3.2 approval rules vs §4.2 state machine.** Detected is never approved: `inspect` writes nothing and `approve` acts only on explicit `--allow` ids plus `--confirmed`. `last_pair` is never approval: §2.1 records it, §3.2 forbids it, §3.3.3 permits it only as a labelled convenience *after* approval exists, and §4.2's write path takes ids only from `--allow`, so it cannot leak in. Zero approved seats creates no profile: the §4.2 grammar requires at least one `--allow`, §3.2 states the rule, Slice 3's "no installed model CLIs" case restates it, and `seats.py:596-600` already refuses an empty allowlist. All three named sub-rules hold.

### Criterion 4 — honesty of capability claims: HOLDS

§2.2 explicitly refuses the overclaim ("It does not justify claiming that every host can autonomously create a new model turn"), and §4.4 repeats it ("Do not use a hook to manufacture a model request. Do not use Claude-only behavior such as an injected initial user message as the cross-host contract"). Nothing proposed is presented as shipped — the header is `Status: DRAFT`, §2.1 enumerates what is missing, and §1's contract is written in the future tense. Acceptance claims are executable in shape: isolated project-local roots (§3.1, Slice 1A.4, Slice 2.3, Slice 4.4), real trust prompts ("accept the real Codex hook trust prompt rather than editing around it"; "Never patch a plugin cache: Codex regenerates caches from the marketplace on each launch"), and explicit no-live-state-inheritance (§3.1, Slice 1B.4, Slice 4.4). The §2.2 Codex hooks citation is correctly hedged as unverified pending the Slice 1A spike, and Slice 1A.1 makes that spike the first act before any hook code — I hold it to the hedge, as instructed, and the hedge is honored consistently.

### Criterion 5 — gate and lifecycle compliance: HOLDS

Checked against the docket's `collab/PROTOCOL.md` and `collab/plan-v080-onboarding-59142.debate.json` (`parties: ["opus","codex"]`, `supervisor: "owner"`, `managed_version: 2`).

- §10.1 "using that channel's configured two seats" matches the channel config and PROTOCOL §"the headless seats are **opus** and **codex**; **owner** is the human supervisor and is not a vote."
- §10.2 append-only review sections, reviewers do not edit the body — consistent with PROTOCOL §2 "Corrections are new entries, never edits."
- §10.3 folding accepted findings into the body maps onto PROTOCOL §2's `fix-report` ("identifies a new immutable revision and what changed").
- §10.4 header flip to `Status: APPROVED (MSG-n)` "only when the channel record proves PASS" — matches PROTOCOL §3's controller-owned close.
- §10.6 branch gate against `branch@sha` with `--verify-refs` — matches PROTOCOL §2 "Refs are full `branch@sha` values written after the commit exists."
- §10.6/§10.7 human-only merge and a separate publication gate — matches PROTOCOL §"The human supervisor alone controls merges, publication, profile changes, scheduler changes and scope," and §9's non-goal list ("No automatic ... merge, push, tag, or publication").

### Criterion 3 — safety and trust invariants: BLOCKING FINDING

The six invariants the docket enumerates are each present and mutually non-contradictory: zero-model-call discovery is stated at every point discovery appears (§1.6, §3.1 notice text, §3.2, §4.2 `inspect`, §6 twice, §8); no path lets the hook or `approve` write before validation (§4.1 "It never writes a registry/profile, runs discovery, invokes a seat, reads credentials, or starts a debate"; §4.2 "rescans, verifies the supplied revision ... validates ... then transactionally writes", "A failure before the atomic replace leaves both prior files byte-identical"; §4.3 "run all loader and `adapter-doctor` validation before the first target write", "leave target paths byte-empty on any pre-write failure"; §6 "every channel/config write follows complete preflight validation"); smoke is bounded to one confirmed call per selected seat with cost mode stated and defaults to "not now" (§1.6, §3.2, §5 Slice 4.5, §8); `/tmp` is excluded (§5 Slice 4.3, §6); credential values are excluded from JSON/UI/logs/records/fixtures (§4.2, §6, §5 Slice 4.7, §8); and hook trust is explicitly never approval (§1.3, §8 first bullet).

**BLOCKING — the plan's project-local evidence roots are not reconciled with the repository's publication boundary, so the "no credential values in any surface" invariant is incomplete exactly where the plan puts live provider credentials.**

Evidence, all from the pinned export plus the plan text:

1. The plan mandates three new directories *inside the published repository*: `/home/zoltan/Projects/debate/.acceptance/v080/` (§3.1, Slice 1A.4/1A.5, Slice 2.3/2.4), `/home/zoltan/Projects/debate/.release-acceptance/v080/` (Slice 4.3/4.4/4.7), and the worktree `/home/zoltan/Projects/debate/.worktrees/installation-onboarding-v080` (§5).
2. The export's `.gitignore` ignores none of them. Its complete entry list is `notes/`, `__pycache__/`, `*.egg-info/`, `.venv/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `dist/`, `build/`, `.pytest-tmp/`, `collab/signal.json`, `collab/.lock`, `collab/*.signal.json`, `collab/*.lock`, `watcher.json`, `*.watcher.json`, `.claude/settings.local.json`, `.claude/worktrees/`, `docs/HANDOVER-SESSION-*.md`, `docs/plans/`, `var/`, `collab-retired-*/`. A case-insensitive grep for `acceptance|worktrees|\.release-` over `.gitignore` returns exactly one hit — line 30, `.claude/worktrees/` — which does **not** cover the plan's `.worktrees/`.
3. Those directories are specified to hold live host state and live credentials. Slice 4.4 creates "completely fresh isolated Codex and Claude installs" under `.release-acceptance/v080/`, and Slice 4.5 approves "two real unattended headless seats" and optionally smokes them — a real seat requires a real provider credential, so the isolated host configuration roots created inside the repo will contain provider auth material.
4. No invariant closes the gap. §6's path invariant constrains evidence roots only to "project-local, never `/tmp`" — for a public repository, "project-local" is precisely where an un-ignored credential store must not sit. §5 Slice 4.7 constrains only what "enter[s] a public artifact" (the `results/` directory), not what sits untracked in the working tree. §8 covers the hook not sourcing `/home/zoltan/.secrets` and the broker allowlist at invocation time, but says nothing about the acceptance roots.
5. This is the repository's own documented prior failure mode, twice over. `.gitignore:28-30` was added because "Review worktrees live inside the repo. Each is a full checkout, so an absent-minded `git add -A` would try to commit whole trees into this one" — the plan reintroduces an in-repo worktree at an unignored path. `.gitignore:32-34` records "Session handovers ... Session 2 reached the public repo by omission, not by choice."

Why blocking rather than an observation: the docket asks whether the safety invariants are *complete*, and this artifact is to become the implementation contract. The failure is one-way — credentials committed into a public repository's history require history rewrite plus credential rotation, and cannot be undone by a later slice — while the fix is one line at contract time. §7 is explicitly "at minimum", so I am not treating its omission of `.gitignore` as the defect; the defect is that no section of the plan states the exclusion requirement at all.

Sufficient remedy (either is fine, and both are one line): add `.acceptance/`, `.release-acceptance/`, and `.worktrees/` to `.gitignore` as part of Slice 1A, **or** relocate all acceptance and worktree roots under the already-ignored `var/` prefix (`.gitignore:44`), and add a cross-cutting invariant to §6 in the form "all project-local evidence and host-configuration roots are version-control-excluded before the first host install writes to them."

### Non-blocking observations (recorded, not voted as blockers)

- **Two acceptance roots with overlapping names.** §3.1 says "The release acceptance starts with isolated ... roots under `.acceptance/v080/`", while the actual release acceptance (Slice 4) uses `.release-acceptance/v080/`. Both are project-local and non-`/tmp`, and the readings reconcile (Slices 1A/1B/2 use the former, Slice 4 a fresh separate root), but §3.1's wording invites confusion in the implementation contract.
- **pytest basetemp.** Slice 4.3 requires "every temporary/cache/base path under `.release-acceptance/v080/`", while `pyproject.toml:50` pins `addopts = ["--basetemp=.pytest-tmp"]` (ignored at `.gitignore:13`). Reconciling the two needs a `pyproject.toml` change that §7's "amend `pyproject.toml`" bullet mentions only in the sdist-manifest sense.
- **"Vanished binary" vs "the hook never runs discovery".** §3.4 makes a vanished binary a reason the notice returns, and §6's Registry row lists it, while §4.1 says the hook "never ... runs discovery". Presence-checking an already-registered command is plainly distinct from candidate discovery (§4.2 puts PATH/catalog discovery in `inspect`, not `status`), so this is resolvable, but the contract would be sharper if §4.1 said so. The §4.2 `status` schema is explicitly "at least" these fields, so it can carry the vanished-binary signal under `attention: repair_required`.
- **Monolithic structure.** Per the docket's structure note: I do not find the monolithic plan-carrying-its-own-slices shape a blocking defect. The slices are individually demonstrable, the gate in §10 is explicit, and the risk-first 1A/1B split gives the contract real sequencing discipline. I record this as considered and not waived.

### Explicitly not voted on (docket scoping)

Per the docket's honest-scoping paragraph I take no position on, and rest no part of this verdict on: the live-host observations (`codex plugin list` / `claude plugin list`, the 2026-06-26 Codex hook-parser incident in `~/.codex/config.toml`, superpowers' split hook manifests), the 0.7.0 sdist failure record in `debate-bench/docs/HANDOVER-SESSION-8.md`, and the external documentation URLs. I also note that `docs/plans/` is absent from the export, but `.gitignore:36-40` ignores that directory by design ("Planning documents are how this project is BUILT, not what it ships"), so the §2.1 citation of `docs/plans/2026-07-15-skill-distribution-research.md` and the §4.3 citation of `docs/plans/2026-08-15-seat-registry-and-debate-open.md` are unverifiable here rather than contradicted — I do not vote on them either way.

### Summary

The required command passes (57 passed). Criteria 1, 2, 4 and 5 hold on my own fresh inspection of the pinned export; every checkable section-2.1 claim is confirmed and none is contradicted. Criterion 3 fails on completeness: the plan places isolated Codex/Claude installation roots — which will hold real provider credentials in Slice 4 — and an implementation worktree inside a public repository whose `.gitignore` excludes none of those paths, and no section of the plan requires that exclusion. That is the single blocking finding; I found no other blocker establishable in this pass.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: c76c04513c4b76a7b6d984353717f05d85124a6dc683698d9ee63a3c31654050
- phase: sealed
- captured-at: 2026-08-19T19:10:49+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 080bd7156d2cb5da8cbd62cb590b91f1a6de42b607f2f7894058727519d83b00
- controller-config-sha256: 793d9b60048ed4c26d7cdacf96669b6a05d1c0e19a86fe50b12b24872dcc52f9
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc
- docket-revision-sha256: b959c5730ce6e8bb5eba29692f4a91f8624c40831a1769b0d8b6305c87c1f0a8
- input-sha256: b0fe0836a1783c95574a73f9f1e73390bfcd64b3e7d2aa98eae88b3fe0c7d429
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-3 | 2026-08-19T19:14:13+00:00 | from: codex | type: verdict | thread: plan-v080-onboarding-1 | refs: -

Required verification passed: `python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py` → `57 passed in 0.51s`.

Blocking findings:
1. The isolated-acceptance contract is not executable as written. The plan requires no read of the live registry (lines 107-110) but specifies only `--project` for onboarding and no registry-root propagation. Fresh source evidence: `src/debate/seats.py:56-57` resolves the registry from `DEBATE_SEATS_REGISTRY` or `~/.config/debate/seats.json`; `load_registry()` uses it at lines 99-100. The plan neither makes the bundled launcher set a project-local registry nor defines the isolated acceptance environment that would set the override. Thus a normal isolated host-config launch can still inherit the live registry/last_pair.
2. The claimed no-`/tmp` release acceptance has no confinement mechanism for existing required code paths. The plan requires every temporary/cache/base path under `.release-acceptance/v080/` and says nothing uses `/tmp` (lines 437-440), but `src/debate/setup.py:220` uses `tempfile.TemporaryDirectory(prefix="debate-setup-")` without `dir=`, and `tests/test_setup.py:52,73,83,94,104,114,124,131,144` invoke `setup.apply`. The exact inspection command `rg -n -C 2 'TemporaryDirectory|mkdtemp' src/debate/setup.py src/debate/opening.py` also showed the unscoped `src/debate/opening.py:285` temporary directory. The plan does not require changing these paths or establish a release-runner `TMPDIR`/equivalent, so its stated invariant cannot be verified from the prescribed release flow.

Repo-evidence claims checked by `rg`/`find` were otherwise supported: only the `debate` console script is declared; `.claude-plugin` exists while `hooks/hooks.json` and `.codex-plugin` are absent; `MANAGED_VERSION = 1`; `opening.py` consults `last_pair`; a missing profile returns `None`; and `adapter-doctor` exists.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: c76c04513c4b76a7b6d984353717f05d85124a6dc683698d9ee63a3c31654050
- phase: sealed
- captured-at: 2026-08-19T19:14:13+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: cb0106ad406b8546d585ff690876b9c892be00b01dd014811b149d01bb02be5e
- controller-config-sha256: 793d9b60048ed4c26d7cdacf96669b6a05d1c0e19a86fe50b12b24872dcc52f9
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 63a70e313455198f7beac0ed5f9b93cb299056eeb76760c1b1c7384f48f24d49
- docket-revision-sha256: b959c5730ce6e8bb5eba29692f4a91f8624c40831a1769b0d8b6305c87c1f0a8
- input-sha256: 640b913e83f0ca31638d6bc9b188e9418c11c2df8a64d3c3845f59a59e0b4b43
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-4 | 2026-08-19T19:14:13+00:00 | from: owner | type: close | thread: plan-v080-onboarding-1 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-5 | 2026-08-19T19:20:12+00:00 | from: owner | type: review-request | thread: plan-v080-onboarding-2 | refs: main@ee1e99a0e35e93dea1029609fdcf65c7683fa680

Fix-report and round-2 review request (fold-delta) for the v0.8.0 plan doc `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md`. Round 1 closed NO_PASS (MSG-4) on three blockers and two folded observations; every finding has been folded with owner authorization:

1. MSG-2 blocker — version-control exclusion of in-repo evidence/host roots: new section-6 invariant, Slice 1A gitignore-before-install step, section-7 `.gitignore` amendment bullet.
2. MSG-3 blocker 1 — registry isolation: section 3.1 names the HOME/XDG or `DEBATE_SEATS_REGISTRY` lever for the acceptance harness; Slice 4 step 4 references it.
3. MSG-3 blocker 2 — `/tmp` confinement: Slice 4 step 3 specifies the release runner's `TMPDIR` export and explicit `--basetemp` override.
4. MSG-2 observations — two acceptance roots named as distinct by design in section 3.1; section 4.1 distinguishes `status` presence-checks from `inspect` discovery.

The round-1 artifact version is materialized in the docket as `plan-round1.md`; compute the true change set yourself per the docket's fold-delta clause. Verdicts cite your own fresh evidence; standing round-1 criteria may be cited by MSG id where your diff and sweep leave them unimplicated.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 2b185762cbd94e0c624f4c304e6cdf143a967eb0bec0a40461f8547e9ad10471
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- docket-revision-sha256: cafdf1af5d75abf289a18c08031262398e46e8c25e50a4e104d4cdd2f9340001
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-onboarding-59142.debate.json", "sha256": "485d531462f4faf4f368ef091f16ba8f4cfa5a696a26fad916c3ae4cd30f02f7", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "df83e5159a8bcbb3bc0ba9fa2b845280ee3c91aee012c6651641d73a49bbe021", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/plan-round1.md", "sha256": "71ccc6a2413c7ade784e04fa6f587b1018797b5ca66d71b8382125c285d80331", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/plan-v080-docket-r2.md", "sha256": "a956e991acfee89a8d9a09bf7645453d31ef02a3bf4d6829e221fd1aee2333ac", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/watcher-r2.json", "sha256": "2b185762cbd94e0c624f4c304e6cdf143a967eb0bec0a40461f8547e9ad10471", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "1224f6cc8143bc24fc525b8dc8450880dc1128da5742d0f479332cdb83f39c66", "opus": "9acb5b0a4d130ed09600dcbbb2dc72a7f7d6fce44aeac6224ddb700eade192c9"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "45b5787068027077009eef50c3625c471289aa2350312d05d75e7cafab99a06e", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "9805d230f5fbf92f58a180eadd747e11728d384cdd0482f61da034c7528f6a5a", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "63a70e313455198f7beac0ed5f9b93cb299056eeb76760c1b1c7384f48f24d49", "opus": "51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc"}

## MSG-6 | 2026-08-19T19:27:55+00:00 | from: opus | type: verdict | thread: plan-v080-onboarding-2 | refs: -

VERDICT: PASS (round-2 fold-delta, opus, author-independent)

## Criterion 6 — the required command

Run from my pinned export root (`pwd` → `/home/zoltan/Projects/debate/var/debate/plan-v080-onboarding-59142/controller/exports/ee1e99a0e35e93dea1029609fdcf65c7683fa680/opus`), literally, no prefix/suffix/pipe:

`python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py`

Result: `......................................................... [100%]` / `57 passed in 0.53s`. All three files exist in the export (Glob `tests/*.py`).

## True change set (derived, not taken from the fold list)

`diff` and a difflib helper were both denied by this seat's permission mode, so I derived the delta by reading both docket copies in full (`plan-round1.md`, 569 lines; current plan, 602 lines) and reconciling every section-header line offset. Cumulative offsets: §1/§2/§3 +6; §3.2 +16; §4/§4.1 +16→+18; §4.2/§4.3/§4.4/§5/Slice 1A +18; Slice 1B/2/3/4 +22; §6 +27; §7 +29; §8/§9/§10 +33; total +33 = 602−569. Every offset step localizes to exactly eight regions, and each maps to a declared fold:

1. Header: second `Amended:` block naming MSG-2/MSG-3/MSG-4 (+6) — fold 6.
2. §3.1 rewritten: two roots named by design + HOME/XDG-or-`DEBATE_SEATS_REGISTRY` isolation lever + explicit "harness setup, not the user" carve-out (+10) — folds 2 and 4.
3. §4.1: presence-check-for-`status` is not discovery; candidate discovery only in `inspect` (+2) — fold 5.
4. Slice 1A step 2: `.gitignore` adds `.acceptance/`, `.release-acceptance/`, `.worktrees/` before any isolated install (+4) — fold 1.
5. Slice 4 step 3: `TMPDIR=…/.release-acceptance/v080/tmp` + explicit `--basetemp` (+4) — fold 3.
6. Slice 4 step 4: references the §3.1 lever (+1) — fold 2.
7. §6 cross-cutting invariant: version-control exclusion before first host install (+2) — fold 1.
8. §7: `.gitignore` amendment bullet (+4) — fold 1.

No artifact edit outside the fold list. Reverse check: each round-1 finding named in the docket header (MSG-2 criterion-3 blocker + two observations; MSG-3 blockers 1 and 2) has a corresponding fold above; none is unaddressed. Limitation stated plainly: the offset accounting proves no line-count change outside those eight regions; an equal-length in-place edit inside an unchanged region is excluded only by my full read of both texts, not by the count.

## Fold claims checked against the pinned export (criterion 1 and the new text)

- `src/debate/seats.py:56-57` — `registry_path()` returns `os.environ.get("DEBATE_SEATS_REGISTRY", str(REGISTRY_PATH))`; `seats.py:24` `REGISTRY_PATH = Path("~/.config/debate/seats.json")`. The §3.1 lever is real; host-config isolation alone genuinely would not cover it.
- `src/debate/setup.py:220` and `src/debate/opening.py:285` — `TemporaryDirectory(prefix=…)` with no `dir=`, so `TMPDIR` is the correct lever. `pyproject.toml:50` — `addopts = ["--basetemp=.pytest-tmp"]`, so the "overriding" claim is accurate.
- `.gitignore` — contains `.claude/worktrees/` (line 30) and none of `.acceptance/`, `.release-acceptance/`, `.worktrees/`; §7's justification is exact.
- §4.1 presence-check claim is consistent with shipped behavior: `README.md:149-152` describes `debate seats check` as a zero-call freshness check whose exit 3 covers a vanished binary; §3.4 lists vanished binary as a notice trigger.
- Unchanged §2.1 rows re-established on my own evidence: `[project.scripts]` has only `debate = "debate.__main__:main"` (`pyproject.toml:37-38`); `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/debate/SKILL.md` present and `hooks/hooks.json`, `.codex-plugin/`, `.agents/` absent (Glob); `opening.py:280,297` write `channel.MANAGED_VERSION` (=1, `channel.py:54`) while `README.md:180-181` calls version 2 the path for new isolated gates; `opening.py:131` consults project then global `last_pair`; `seats.py:562-566` `load_profile` — "A missing file is simply no restriction"; `skills/debate/SKILL.md:3,20-24` triggers on an existing channel/wake-up/review request and fails closed without the CLI. Carve-outs respected: no vote on `codex/claude plugin list`, the debate-bench sdist record, or external URLs.

## Coherence sweep (criteria 2-4)

No fold contradicts other text. The §3.1 harness-environment lever is explicitly reconciled with the same section's rule that the *user* never sets `DEBATE_SEATS_REGISTRY`. The §4.1 presence-check carve-out stays inside the §6 invariant "session start is read-only, bounded, and zero-call". The new §6 exclusion invariant, the Slice 1A step-2 ordering (step 2 precedes the step-4 install), and the §7 bullet agree. Criterion 5 (gate/lifecycle vs `collab/PROTOCOL.md` and `plan-v080-onboarding-59142.debate.json`: parties opus/codex, supervisor owner, managed_version 2, cap 12) is untouched by the change set and unimplicated by the sweep — standing per MSG-2; the header correctly still reads `Status: DRAFT` per §10 step 4.

## Non-blocking observations (no blocking finding established in this pass)

1. Path convention: the plan names every repo file by absolute main-checkout path while §5 puts the work in `.worktrees/installation-onboarding-v080`. Read consistently (absolute = canonical repo path in the working checkout), the branch-local `.gitignore` does protect the acceptance roots. Read literally, roots created under the main checkout would be unprotected until merge, and the `.worktrees/` entry specifically cannot protect the main checkout's `git add -A` before merge. One sentence fixing the convention would close this.
2. Fold 4 names roots for Slices 1A/1B/2 and 4; Slice 3's host-level cases (its "acceptance run" byte-comparison) are left without a named root.
3. Fold 3's enumeration lists only the two `TemporaryDirectory` calls; `setup.py:321` also calls `mkdtemp(dir=scratch_base or None)`. The `TMPDIR` lever covers it, so the mechanism is complete and only the enumeration is partial.
4. The §2.1 row citing `docs/plans/2026-07-15-skill-distribution-research.md` is unverifiable from the export (`docs/plans/` is gitignored, absent from the export); its operative claim — both Codex artifacts absent — I verified directly.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 5430240d25cb730752acdd264abb8cebb86a1d4f11180c897541706f215209bd
- phase: sealed
- captured-at: 2026-08-19T19:25:23+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 9acb5b0a4d130ed09600dcbbb2dc72a7f7d6fce44aeac6224ddb700eade192c9
- controller-config-sha256: 2b185762cbd94e0c624f4c304e6cdf143a967eb0bec0a40461f8547e9ad10471
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc
- docket-revision-sha256: cafdf1af5d75abf289a18c08031262398e46e8c25e50a4e104d4cdd2f9340001
- input-sha256: 9fdb59ef623273e272799274108db21e38a6d7da2d4cda5504af53bddb840415
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-7 | 2026-08-19T19:27:55+00:00 | from: codex | type: verdict | thread: plan-v080-onboarding-2 | refs: -

Blocking finding: the round-1 TMPDIR fold does not guarantee its claimed `/tmp` confinement. The plan says only to export `TMPDIR=/home/zoltan/Projects/debate/.release-acceptance/v080/tmp` at lines 459-466, but never requires that directory to be created before the suites run. In a genuinely fresh release root, Python's default tempfile resolver skips a nonexistent TMPDIR and can fall back to `/tmp`; this directly violates the stated invariant at lines 511-513. The pinned export confirms the implicated calls use `tempfile.TemporaryDirectory(...)` without `dir=` in `/home/zoltan/Projects/debate/var/debate/plan-v080-onboarding-59142/controller/exports/ee1e99a0e35e93dea1029609fdcf65c7683fa680/codex/src/debate/setup.py:220` and `/home/zoltan/Projects/debate/var/debate/plan-v080-onboarding-59142/controller/exports/ee1e99a0e35e93dea1029609fdcf65c7683fa680/codex/src/debate/opening.py:285`. Require the release runner to create and validate the TMPDIR under the release-acceptance root before invoking any test/build command (or pass explicit project-local directories to every tempfile user).

Fresh required verification was run exactly as docketed: `python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py` — result: `57 passed in 0.48s`. The passing test command does not resolve the above plan-level confinement gap. The other round-1 folds are present in the true diff; standing criteria 1-5 otherwise stand by the round-1 MSG-2/MSG-3 evidence, except where this new coherence/safety finding implicates criterion 3.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 5430240d25cb730752acdd264abb8cebb86a1d4f11180c897541706f215209bd
- phase: sealed
- captured-at: 2026-08-19T19:27:55+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 1224f6cc8143bc24fc525b8dc8450880dc1128da5742d0f479332cdb83f39c66
- controller-config-sha256: 2b185762cbd94e0c624f4c304e6cdf143a967eb0bec0a40461f8547e9ad10471
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 63a70e313455198f7beac0ed5f9b93cb299056eeb76760c1b1c7384f48f24d49
- docket-revision-sha256: cafdf1af5d75abf289a18c08031262398e46e8c25e50a4e104d4cdd2f9340001
- input-sha256: cbe483a285cd818940f40413df6916ebcd600b896a168fa91aa6ceeafade83e5
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-8 | 2026-08-19T19:33:22+00:00 | from: opus | type: verdict | thread: plan-v080-onboarding-2 | refs: -

VERDICT: NO_PASS (deliberation, round-2 fold-delta, opus, author-independent)

I ran the docketed command again in this pass and re-examined fold 3 against MSG-7. MSG-7's finding holds on my own evidence, and it is blocking. This reverses my MSG-6 PASS on that one point; nothing else in my MSG-6 analysis changes.

## Criterion 6 — the required command

Run literally from my pinned export root (`pwd` → `/home/zoltan/Projects/debate/var/debate/plan-v080-onboarding-59142/controller/exports/ee1e99a0e35e93dea1029609fdcf65c7683fa680/opus`), no prefix/suffix/pipe:

`python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py`

Result: `......................................................... [100%]` / `57 passed in 0.52s`.

## Blocking finding (criteria 3 and 4) — fold 3 does not deliver the confinement it claims

Plan §Slice 4 step 3 (docket copy, lines 459-466) states the suites run "with every temporary/cache/base path under `/home/zoltan/Projects/debate/.release-acceptance/v080/`; nothing on this workstation uses `/tmp`", and the sole named mechanism for the `tempfile` users is `TMPDIR=/home/zoltan/Projects/debate/.release-acceptance/v080/tmp`. The plan never requires that directory to exist, and nothing else can create it:

- Grep over the whole plan for `mkdir|TMPDIR|tmp|basetemp|release-acceptance` returns no creation or validation step for `…/.release-acceptance/v080/tmp` anywhere (only lines 18, 461-466, 468, 478, 511, 538-539).
- Ordering makes the gap concrete rather than theoretical: step 3 *runs the suites*, while step 4 is the first step that creates anything "under that release-acceptance directory" (line 467). Steps 1-2 build artifacts only. So at step 3 of a genuinely fresh release root, `TMPDIR` names a nonexistent path.
- CPython's `tempfile` treats `TMPDIR` as a *candidate*: `gettempdir()` walks TMPDIR/TEMP/TMP, then `/tmp`, `/var/tmp`, `/usr/tmp`, then cwd, accepting the first in which it can actually create a file. A nonexistent `TMPDIR` is skipped silently, so `/tmp` is used with no error. `--basetemp` does not help here — pytest creates its own basetemp, but the implicated calls do not go through it.
- The implicated calls are real in the pinned export: `src/debate/setup.py:220` and `src/debate/opening.py:285` call `tempfile.TemporaryDirectory(prefix=…)` with no `dir=`, and `src/debate/setup.py:321` calls `tempfile.mkdtemp(prefix="debate-smoke-", dir=…)` with `dir=None` whenever no `scratch_base` is passed.
- Consequence: the invariant at lines 511-513 ("all persistent evidence and test roots are project-local, never `/tmp`") and the categorical claim "nothing on this workstation uses `/tmp`" would be violated *silently* — the acceptance gate would report success while host/seat scratch state, including whatever those setup/smoke paths write, landed in `/tmp`. MSG-3 blocker 2 is therefore not resolved by the fold as written.
- The repo already contains the correct pattern, so the fix is cheap and non-speculative: `src/debate/controller.py:686-699` creates `runtime/tmp` with `mkdir(parents=True, exist_ok=True)` *before* exporting `TMPDIR`/`TEMP`/`TMP` to it. Remedy: have Slice 4 step 3 require the runner to create the release-acceptance tmp root (and assert `tempfile.gettempdir()` resolves under `.release-acceptance/v080/`) before invoking any test/build command, or pass explicit project-local directories to every `tempfile` user.

This is the only blocking finding I can establish in this pass; I re-swept §§1-10 and the eight change regions and found nothing else that rises to blocking.

## What still stands from my MSG-6 pass

- True change set: derived independently by full read plus section-offset reconciliation of `plan-round1.md` (569 lines) against the current plan (602 lines), cumulative +33 localized to exactly eight regions, each mapping to a declared fold; no artifact edit outside the fold list; every round-1 finding (MSG-2 criterion-3 blocker + two observations; MSG-3 blockers 1 and 2) has a corresponding fold, though fold 3's mechanism is incomplete as above. Stated limitation unchanged: offset accounting excludes only length-changing edits outside those regions; equal-length in-place edits are excluded by my full read, not by the count.
- Folds 1, 2, 4, 5, 6 check out against the pinned export and are internally coherent: `seats.py:56-57` + `seats.py:24` confirm the §3.1 `DEBATE_SEATS_REGISTRY`/HOME-derived lever and the "harness setup, not the user" carve-out (plan lines 119-126) reconcile with the same section's user-facing rule at lines 134-136; `.gitignore` lacks `.acceptance/`, `.release-acceptance/`, `.worktrees/` (it has `.claude/worktrees/` only), so §7 line 538-539 and Slice 1A step 2 (lines 348-353, ordered before the step-4 install) and the §6 invariant at 512-513 agree; §4.1's presence-check-vs-discovery split is consistent with shipped `debate seats check` behavior.
- Criterion 1 (§2.1 repo-evidence rows) and criterion 5 (gate/lifecycle vs `collab/PROTOCOL.md` and the channel config; header still `Status: DRAFT` at line 3) were established on my own evidence in MSG-6 and are unimplicated by this finding — standing by citation to MSG-6, with criterion 5 also standing per MSG-2. Docketed carve-outs respected: no vote on live-host observations, the debate-bench sdist record, or external URLs.

## Non-blocking observations (carried forward, unchanged)

1. Path convention: repo files and acceptance roots are all named by absolute main-checkout path while §5 (lines 330-333) puts the work in `.worktrees/installation-onboarding-v080`. The consistent reading (absolute = canonical repo path in the working checkout) makes the branch `.gitignore` effective; one sentence stating that convention would remove the literal reading in which main-checkout roots are unprotected until merge.
2. §3.1 names roots for Slices 1A/1B/2 and 4; Slice 3's host-level uninstall byte-comparison (lines 430-434) has no named root.
3. Fold 3's enumeration names only the two `TemporaryDirectory` calls and omits `setup.py:321`'s `mkdtemp`; once the tmp root is actually created, the `TMPDIR` lever does cover it, so this is enumeration completeness only.
4. The §2.1 row citing `docs/plans/2026-07-15-skill-distribution-research.md` is unverifiable from the export (`docs/plans/` is gitignored); its operative claim — both Codex artifacts absent — I verified directly.

PASS is reachable by adding the creation/validation step in Slice 4 step 3; no other change is required by this pass.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 9acb5b0a4d130ed09600dcbbb2dc72a7f7d6fce44aeac6224ddb700eade192c9
- controller-config-sha256: 2b185762cbd94e0c624f4c304e6cdf143a967eb0bec0a40461f8547e9ad10471
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc
- docket-revision-sha256: cafdf1af5d75abf289a18c08031262398e46e8c25e50a4e104d4cdd2f9340001
- input-sha256: 6c67df8b7600d5612193ce8ed502da0568860665bdd025f2ba64707e996d3391
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-9 | 2026-08-19T19:33:22+00:00 | from: owner | type: close | thread: plan-v080-onboarding-2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-10 | 2026-08-19T20:41:41+00:00 | from: owner | type: review-request | thread: plan-v080-onboarding-3 | refs: main@ee1e99a0e35e93dea1029609fdcf65c7683fa680

Fix-report and round-3 review request (fold-delta) for the v0.8.0 plan doc. Round 2 closed NO_PASS (MSG-9) on one converged blocker plus three carried observations; all four are folded with owner authorization: (1) Slice 4 step 3 now creates and validates the TMPDIR root before any suite runs (mkdir -p, export, assert tempfile.gettempdir() under the release root; pattern controller.py:686-699); (2) section 5 states the path convention tying absolute paths to the checkout carrying the work, with no acceptance root created before its .gitignore exclusion exists; (3) Slice 3 host-level cases run under the named .acceptance/v080/ root; (4) the mkdtemp(dir=None) smoke fallback joins the confinement enumeration. The round-2 artifact version is materialized in the docket as plan-round2.md; compute the true change set yourself per the docket's fold-delta clause. Verdicts cite your own fresh evidence; standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 2cbc0acff40c5adffd2691b1633104d6222c9da8f0aa5681edc6a56bcd8b625c
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- docket-revision-sha256: dd69680e269d61a9a5a8ebcd6df3a607c9a0372cbf381b9faac63e2db78083ab
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-onboarding-59142.debate.json", "sha256": "485d531462f4faf4f368ef091f16ba8f4cfa5a696a26fad916c3ae4cd30f02f7", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "0a6250814ea236d8e6bb1bf86e2fde5b235185f6b46af77fe0c5849c4340ce6e", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/plan-round2.md", "sha256": "df83e5159a8bcbb3bc0ba9fa2b845280ee3c91aee012c6651641d73a49bbe021", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/plan-v080-docket-r3.md", "sha256": "77c41ec6e15df28b0870bb87b675e3acc45276905674ee5ec35f30c60f0eece2", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-onboarding-59142/watcher-r3.json", "sha256": "2cbc0acff40c5adffd2691b1633104d6222c9da8f0aa5681edc6a56bcd8b625c", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "1224f6cc8143bc24fc525b8dc8450880dc1128da5742d0f479332cdb83f39c66", "opus": "9acb5b0a4d130ed09600dcbbb2dc72a7f7d6fce44aeac6224ddb700eade192c9"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "45b5787068027077009eef50c3625c471289aa2350312d05d75e7cafab99a06e", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "9805d230f5fbf92f58a180eadd747e11728d384cdd0482f61da034c7528f6a5a", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "63a70e313455198f7beac0ed5f9b93cb299056eeb76760c1b1c7384f48f24d49", "opus": "51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc"}

## MSG-11 | 2026-08-19T20:48:12+00:00 | from: opus | type: verdict | thread: plan-v080-onboarding-3 | refs: -

PASS — round-3 fold-delta review of `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md` (docket revision dd69680e…, source export ee1e99a0e35e93dea1029609fdcf65c7683fa680).

## Criterion 6 — required command (own fresh run)

Command, run literally with no prefix, suffix, pipe or environment diagnostic, from the export root `/home/zoltan/Projects/debate/var/debate/plan-v080-onboarding-59142/controller/exports/ee1e99a0e35e93dea1029609fdcf65c7683fa680/opus` (confirmed by a separate `pwd`):

`python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py`

Result:
```
.........................................................                [100%]
57 passed in 0.53s
```

## True change set (computed, not taken from the fold list)

`diff` on the docket path was refused by the sandbox (Bash denied for the docket root; `Read`/`Grep`/`Glob` were allowed), so I established the change set by reading both docket copies end to end — `var/debate/plan-v080-onboarding-59142/plan-round2.md` (602 lines) and the current plan (623 lines) — plus anchor arithmetic and a targeted `Grep` of both files for every sensitive token (`\.acceptance/v080|\.release-acceptance/v080|managed version 2|MANAGED_VERSION|schema_version|debate-profile\.json|--basetemp|\.pytest-tmp|/tmp|TemporaryDirectory|TMPDIR|Status: |Amended:|MSG-`). Delta is +21 lines, and every section anchor shifts by exactly the running insertion total (prior 59→current 65 after +6; 414→425 after +11; 448→463 after +15; 484→505 after +21), with all sensitive-token lines identical outside the fold regions. The true change set is therefore exactly four content folds plus the bookkeeping header — no undisclosed artifact edit:

1. header lines 21-25: third `Amended:` line recording the round-2 folds with channel provenance (+6);
2. section 5 intro lines 340-344: path convention (+5);
3. Slice 3 lines 451-453: named slice-acceptance root for host-level cases incl. uninstall byte-comparison (+4);
4. Slice 4 step 3 lines 474-487, rewritten from prior 459-466 (+6).

## (a) Each fold resolves its finding

1. **Blocker (TMPDIR creation)** — resolved. Lines 477-484 now order the runner: FIRST `mkdir -p /home/zoltan/Projects/debate/.release-acceptance/v080/tmp` before any test or build command, then export `TMPDIR`, then assert `tempfile.gettempdir()` resolves under the release-acceptance root before invoking any suite. The stated failure mode (CPython silently skipping a nonexistent `TMPDIR` candidate and falling back to `/tmp`) is correct, and the cited in-repo pattern verifies: `src/debate/controller.py:686-699` creates `runtime/tmp` via `path.mkdir(parents=True, exist_ok=True)` (688-690) *before* setting `"TMPDIR": str(temp)` (697).
2. **Path convention** — resolved. Lines 340-344 state that absolute paths name canonical repo-relative locations in whichever checkout carries the work (the feature worktree during implementation), and add the new guard "no acceptance root is created in a checkout whose `.gitignore` does not yet exclude it".
3. **Slice 3 root** — resolved. Lines 451-453 place all Slice 3 host-level cases, uninstall byte-comparison snapshots included, under `.acceptance/v080/` in per-case subdirectories.
4. **Enumeration** — resolved and accurate against the export. `Grep` for `TemporaryDirectory|mkdtemp` in `src/` returns exactly `src/debate/setup.py:220`, `src/debate/opening.py:285` (both `TemporaryDirectory(...)` with no `dir=`) and `src/debate/setup.py:321-322` `tempfile.mkdtemp(prefix="debate-smoke-", dir=... if scratch_base else None)` — the smoke-path `mkdtemp(dir=None)` fallback the fold adds. The `--basetemp` claim also verifies: `pyproject.toml:50` is `addopts = ["--basetemp=.pytest-tmp"]`, which a later explicit `--basetemp` overrides.
5. **Bookkeeping** — present at lines 21-25 with channel provenance.

## (b) Reverse check

The docket's fold-list header is my only inventory of round-2 findings (the thread is sealed and empty on this pass). All four named findings have a corresponding fold in the true change set, and the true change set contains nothing beyond those four plus the header — so there is neither an unresolved finding nor an undisclosed edit.

## (c) Coherence sweep

No change contradicts another part of the artifact. Fold 1's `mkdir` occurs in Slice 4, after Slice 1A step 2 adds `.acceptance/`, `.release-acceptance/`, `.worktrees/` to `.gitignore`, so it satisfies fold 2's new "no acceptance root before exclusion" guard and the §6 invariants "never `/tmp`" and "version-control-excluded before the first host install". Fold 3's root is the §3.1 slice-acceptance root, kept distinct from the §3.1/Slice 4 release-acceptance root, so the two-roots-by-design statement still holds. Export checks confirm the `.gitignore` premise (only `.claude/worktrees/` at line 30) and §2.1's picker claim (`src/debate/channel.py`: `MANAGED_VERSION = 1`, `BROKERED_MANAGED_VERSION = 2`; `opening.py:280,297` write `channel.MANAGED_VERSION`, `:131,325-326` consult/write `last_pair`; `seats.py:56-57` `registry_path()` reads `DEBATE_SEATS_REGISTRY` or `REGISTRY_PATH = ~/.config/debate/seats.json`; `hooks/`, `.codex-plugin/`, `.agents/` absent, `.claude-plugin/{plugin,marketplace}.json` and `skills/debate/SKILL.md` present). §10's gate steps remain consistent with `collab/PROTOCOL.md` §§1,3,5 and with `plan-v080-onboarding-59142.debate.json` (parties opus/codex, supervisor owner, managed_version 2, thread_cap 12).

## Standing criteria

Criteria 1, 2, 3, 4 and 5 are unimplicated beyond the parts I re-established above on fresh evidence, and stand by citation to the round-1/round-2 verdicts where my own evidence established them: MSG-2/MSG-6/MSG-8 (opus seat), with MSG-3/MSG-7 as the codex-seat record. Per the docket I did not vote on author-sourced live-host observations (`codex plugin list` / `claude plugin list`), the debate-bench sdist record, or external URLs. `docs/plans/2026-07-15-…` and `2026-08-15-…` are untracked at the source ref (the export's `docs/` holds only `assets/` and `case-study.md`), so those references are outside the pinned export rather than contradicted by it.

## Non-blocking observations (not conditions of this verdict)

- The new convention sentence says "absolute paths in this plan" without excluding non-repo host paths; read literally it would also cover `/home/zoltan/.config/debate/seats.json`, `/home/zoltan/.secrets`, `/home/zoltan/.codex/config.toml` and `/home/zoltan/Projects/debate-bench/…`, which are deliberately live-host references. Each is unambiguous in its own context (§3.1 calls its seats.json "live"; §8 treats `.secrets` as a user file; debate-bench is declared out of scope), so no implementer is misled. Narrowing the sentence to paths under `/home/zoltan/Projects/debate` would remove the looseness.
- Slice 4 step 3 creates `…/.release-acceptance/v080/tmp` before step 4 creates the "completely fresh" installs and project roots under the same directory; "fresh" plainly qualifies the installs/roots rather than requiring an empty parent, but making that explicit would foreclose a wipe-then-lose-TMPDIR misreading.

Verdict: PASS.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 7c6c99678342cf8975cfa2b753897a5e46bdadadcd589a8582a5ef4736466e07
- phase: sealed
- captured-at: 2026-08-19T20:46:04+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 9acb5b0a4d130ed09600dcbbb2dc72a7f7d6fce44aeac6224ddb700eade192c9
- controller-config-sha256: 2cbc0acff40c5adffd2691b1633104d6222c9da8f0aa5681edc6a56bcd8b625c
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 51c179f2c6ca5873d7597a93b8379f44b41b8f0aa96ff4ba7a6aa8544e1ea9cc
- docket-revision-sha256: dd69680e269d61a9a5a8ebcd6df3a607c9a0372cbf381b9faac63e2db78083ab
- input-sha256: 970c643758b2e8e8a1fed3103592d3d21ac5bf006ffe67f8c8c989314d13239d
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-12 | 2026-08-19T20:48:12+00:00 | from: codex | type: verdict | thread: plan-v080-onboarding-3 | refs: -

PASS. I verified all eight docket-file SHA-256 values match the immutable docket. `diff -u .../plan-round2.md .../2026-08-19-installation-driven-agent-onboarding-v0.8.0.md` showed only the declared third amendment, path convention, Slice 3 acceptance root, and TMPDIR/mkdtemp release-run folds; each resolves its corresponding round-2 finding. `src/debate/controller.py:686-699` confirms the cited create-before-export temporary-root pattern. Criteria 1, 2, and 5 stand by the docket-authorized MSG-2/MSG-3/MSG-6/MSG-8 citations; the fold coherence sweep found no contradiction. Exact required command run from the pinned export: `python -m pytest -q tests/test_release_sync.py tests/test_open.py tests/test_seats.py` → `57 passed in 0.51s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 7c6c99678342cf8975cfa2b753897a5e46bdadadcd589a8582a5ef4736466e07
- phase: sealed
- captured-at: 2026-08-19T20:48:12+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 1224f6cc8143bc24fc525b8dc8450880dc1128da5742d0f479332cdb83f39c66
- controller-config-sha256: 2cbc0acff40c5adffd2691b1633104d6222c9da8f0aa5681edc6a56bcd8b625c
- source-ref: ee1e99a0e35e93dea1029609fdcf65c7683fa680
- source-manifest-sha256: 63a70e313455198f7beac0ed5f9b93cb299056eeb76760c1b1c7384f48f24d49
- docket-revision-sha256: dd69680e269d61a9a5a8ebcd6df3a607c9a0372cbf381b9faac63e2db78083ab
- input-sha256: 8ab0d341f9f4d6e7cb2e0d3819cbfbc956452283db2e1443b7c78f3996ac55bd
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-13 | 2026-08-19T20:48:12+00:00 | from: owner | type: close | thread: plan-v080-onboarding-3 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
