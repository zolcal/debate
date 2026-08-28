
## MSG-1 | 2026-08-25T05:04:37+00:00 | from: owner | type: review-request | thread: plan-managed-codex-compat-1 | refs: feature/ox-alpha-frontier-seat@935a4f2841cc103ea4a1da8f07fb58b3760c997f

Review the supplied managed-Codex onboarding compatibility plan against every
criterion in `var/debate/plan-managed-codex-compat-39215/plan-docket.md` and the
exact pinned source export at
`feature/ox-alpha-frontier-seat@935a4f2841cc103ea4a1da8f07fb58b3760c997f`.

This is the plan gate before product edits. Inspect the immutable plan, predecessor
plan, retained field record, and source independently. Cite your own fresh read-only
commands and bounded performed schema-v2 evidence. Put every blocking finding in the
verdict, distinguish non-blocking observations, and return PASS only when the plan is
safe and executable as written.

Return a complete attributable review body suitable for preservation at the end of
the plan. Do not edit the source export, live plan, channel, registry, profiles, host
configuration, or acceptance evidence. Never use `/tmp`.

The headless Codex review adapter sets the existing documented quiet automation flag
only for its own reviewer subprocess. This prevents the installed interactive
onboarding hook from interrupting review infrastructure; it is not evidence that the
product bridge already contains the proposed fix.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 292649b102489104e019f8bd3de6c7f29fa27d08c5f162256ab3dfdd817daae3
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-contract: {"review_contract_basis": "legacy-absent", "review_mode": "release-gate"}
- docket-revision-sha256: 3f3154c2cf3f363a0853ada33d66e02cc121119f8b1c7b6695f42d3f31ffe657
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-managed-codex-compat-39215.debate.json", "sha256": "5936dbbeb9983e4dca254ee495a2701755f2a3bda6aacb29efa456cc95b10032", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "sha256": "7f4814ca1972e7c858fa2c5a3af260b647ae5790a0874675123daab868d6f15e", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-24-codex-first-turn-onboarding-fold.md", "sha256": "f15c4890fd166e70782b6f859705b7f9c5165af7b5c53355a944536efcd2e043", "tracked_at_source_ref": false}, {"path": ".release-acceptance/ox-alpha/codex-first-turn-fold-935a4f2/FIELD-ACCEPTANCE.md", "sha256": "3080ec5d17915e2c5a1ff5a5f20eb1136d0fe8b8a606972f2bf6ac63e51ba530", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/plan-docket.md", "sha256": "c845ca0d3d08c685588fe708a3802e61a4d1e450d386d32a5d2f95f5a181efe5", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/seat-result.schema.json", "sha256": "095e09028cbe0e2dc4c2b5669fa4bf7ba38517b95990d11399071e893125f02a", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/seat_adapter.py", "sha256": "872d836b260b847fc2998a978f6f60193998a23775dd8799d3f5a402b719a72f", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "bee22f886e30edc9b85e703a5bb2880213d36db6cfb248f8abfde7e275993136", "opus": "1fade7c0b1ba425ab58057fa1ab3dfae055c209e3613fc1c434e5d88994e73f6"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.1", "command_sha256": "15b288104441db83d598ab8f4e63b4bab3bbacb661ab82eb1b4b95bf18068e7e", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "pinned read-only source export; workspace-write sandbox limited to controller invocation output", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 2, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "75ffdf5bb55ad336706dc19328760d5d9101c57991241fbc6863ea04fb59aff2", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "pinned read-only source export; result path controller-owned; read-only inspection tools", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 2, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "ea617a03f99343b0521febaf39ff4aeb8cb5375e1c67e8b749a78b6e76ef008b", "opus": "ab6f6f72a34fc909d744f304a0f5e9bcafd5fa192cfc71608f3f5db764642e00"}

## MSG-2 | 2026-08-25T05:07:06+00:00 | from: owner | type: close | thread: plan-managed-codex-compat-1 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes. Observed failure: refused: adapter 'opus' exited 1; see /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/cases/plan-managed-codex-compat-1/invocations/1-opus-1/stderr.txt

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-3 | 2026-08-25T05:12:05+00:00 | from: owner | type: review-request | thread: plan-managed-codex-compat-2 | refs: feature/ox-alpha-frontier-seat@935a4f2841cc103ea4a1da8f07fb58b3760c997f

Review the supplied managed-Codex onboarding compatibility plan against every
criterion in `var/debate/plan-managed-codex-compat-39215/plan-docket.md` and the
exact pinned source export at
`feature/ox-alpha-frontier-seat@935a4f2841cc103ea4a1da8f07fb58b3760c997f`.

This is the plan gate before product edits. Inspect the immutable plan, predecessor
plan, retained field record, and source independently. Cite your own fresh read-only
commands and bounded performed schema-v2 evidence. Put every blocking finding in the
verdict, distinguish non-blocking observations, and return PASS only when the plan is
safe and executable as written.

Return a complete attributable review body suitable for preservation at the end of
the plan. Do not edit the source export, live plan, channel, registry, profiles, host
configuration, or acceptance evidence. Never use `/tmp`.

The headless Codex review adapter sets the existing documented quiet automation flag
only for its own reviewer subprocess. This prevents the installed interactive
onboarding hook from interrupting review infrastructure; it is not evidence that the
product bridge already contains the proposed fix.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 292649b102489104e019f8bd3de6c7f29fa27d08c5f162256ab3dfdd817daae3
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-contract: {"review_contract_basis": "legacy-absent", "review_mode": "release-gate"}
- docket-revision-sha256: 4c650ebf9d225ed873a57375b6c6086be649a671e2eb5ef8dc2a84e2eeea03e8
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-managed-codex-compat-39215.debate.json", "sha256": "5936dbbeb9983e4dca254ee495a2701755f2a3bda6aacb29efa456cc95b10032", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "sha256": "7f4814ca1972e7c858fa2c5a3af260b647ae5790a0874675123daab868d6f15e", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-24-codex-first-turn-onboarding-fold.md", "sha256": "f15c4890fd166e70782b6f859705b7f9c5165af7b5c53355a944536efcd2e043", "tracked_at_source_ref": false}, {"path": ".release-acceptance/ox-alpha/codex-first-turn-fold-935a4f2/FIELD-ACCEPTANCE.md", "sha256": "3080ec5d17915e2c5a1ff5a5f20eb1136d0fe8b8a606972f2bf6ac63e51ba530", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/plan-docket.md", "sha256": "c845ca0d3d08c685588fe708a3802e61a4d1e450d386d32a5d2f95f5a181efe5", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/seat-result.schema.json", "sha256": "b00e642e165bb549a9544c0307ea6f1f7ca3d632b8b1b8d0d113d90f39c41822", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/seat_adapter.py", "sha256": "872d836b260b847fc2998a978f6f60193998a23775dd8799d3f5a402b719a72f", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "bee22f886e30edc9b85e703a5bb2880213d36db6cfb248f8abfde7e275993136", "opus": "1fade7c0b1ba425ab58057fa1ab3dfae055c209e3613fc1c434e5d88994e73f6"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.1", "command_sha256": "15b288104441db83d598ab8f4e63b4bab3bbacb661ab82eb1b4b95bf18068e7e", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "pinned read-only source export; workspace-write sandbox limited to controller invocation output", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 2, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "75ffdf5bb55ad336706dc19328760d5d9101c57991241fbc6863ea04fb59aff2", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "pinned read-only source export; result path controller-owned; read-only inspection tools", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 2, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "ea617a03f99343b0521febaf39ff4aeb8cb5375e1c67e8b749a78b6e76ef008b", "opus": "ab6f6f72a34fc909d744f304a0f5e9bcafd5fa192cfc71608f3f5db764642e00"}

## MSG-4 | 2026-08-25T05:20:46+00:00 | from: opus | type: verdict | thread: plan-managed-codex-compat-2 | refs: -

## Scope and method

I read the immutable docket (plan, predecessor plan, retained `FIELD-ACCEPTANCE.md`, `collab/PROTOCOL.md`, the gate docket and the gate's own adapter/schema) and the pinned export at `935a4f2841cc103ea4a1da8f07fb58b3760c997f`: `src/debate/bridge.py`, `hooks/session-start`, `hooks/HOOK-CONTRACT.md`, `src/debate/seat_catalog.py`, `src/debate/seats.py`, `src/debate/setup.py`, `src/debate/onboarding.py`, `tests/test_bridge.py`, `tests/test_session_start_hook.py`, `tests/test_ox_alpha.py`, `README.md`, `CHANGELOG.md`, `.gitignore`. Per the docket's own caveat, I treated the gate adapter's `DEBATE_ONBOARDING_QUIET=1` (`seat_adapter.py:133`) as review infrastructure only and never as evidence about the product bridge; I independently confirmed from `bridge.py:603-629` that the product bridge does **not** set the flag today.

One method limitation, stated plainly: this seat's shell is restricted to a trivial allowlist in this run, so I could not recompute SHA-256 digests for the docket files (`sha256sum` was denied — verification item 9). I verified the docket and export by direct read of their contents instead; every finding below rests on quoted file/line evidence, not on digests.

Verdict: **NO_PASS**. The core design choice is sound and well argued — reusing the already-documented `DEBATE_ONBOARDING_QUIET=1` lever in the nested seat environment is genuinely the narrowest lever available, and I could not break invariants 3–6 on the bridge path. Four findings block, all with small corrections; three of the four are specification gaps rather than design errors.

## What survived my attempts to break it

- **Mechanism correctness (bridge → hook).** `hooks/session-start:61-66` computes `quiet` from `DEBATE_ONBOARDING_QUIET == "1"`; `:118` sets `codex_interactive = bool(PLUGIN_ROOT) and not quiet`; `:169-173` then emits `None` for `systemMessage` and omits `continue`/`stopReason` when `codex_interactive` is false. A managed Codex seat whose environment carries the flag therefore cannot receive the stop. Invariant 3 holds on the code as written.
- **Vendor predicate is adequate.** `spec.vendor == "codex"` covers every route into a codex seat id: catalog seeding (`seats.py:555,566` → `f"{entry.vendor}/{submodel}"`), sibling wrappers (`seats.py:740-743` → `f"{entry.vendor}/wrapper:{name}"`, vendor still `"codex"`), and manual adds (`seats.py:970` → `vendor, _, submodel = seat_id.partition("/")`). No aliasing or case gap found.
- **Non-Codex isolation, credentials, serialization.** `seat_environment()` builds a fresh dict from `os.environ` minus `OUR_OWN_ENV`; nothing serialized (`write_result`, `sanitized_manifest`) touches the runtime environment, so invariants 4–6 hold and `tests/test_ox_alpha.py:136-197` already pins the credential/redaction path the plan promises to leave unchanged. No existing bridge test asserts an exact environment for a `codex` spec (`tests/test_bridge.py` fixtures use vendor `claude`), so the change will not silently break the current suite.
- **Interactive stop is preserved and already covered.** `tests/test_session_start_hook.py:315-328` (`test_codex_quiet_attention_is_context_only_and_not_stopped`) and the surrounding matrix already assert `continue`/`stopReason` absent everywhere except the interactive Codex attention path; the plan's added `repair_required` managed-home fixture is a real extension of that matrix, not a duplicate.
- **Defect narrative matches the code.** `onboarding.status` (`onboarding.py:80-110,171-182`) yields `registry_state: missing` + `profile_state: broken` → `repair_required` exactly as the field record reports, which is consistent with the seat's sandboxed `HOME` while `CODEX_HOME` points at the operator's real config home (`bridge.py:624-628`, catalog `config_home="CODEX_HOME=.codex"`). The plan's §2 is an accurate reading of the retained evidence.
- **Version string.** Slice C's "Debate 0.8.0" matches `src/debate/__init__.py:42` (`__version__ = "0.8.0"`).
- **Options 2–4 rejections are honest.** Option 4's claim that no per-plugin hook disable is attested is consistent with the catalog, which records only `--ignore-user-config`/`--ignore-rules`/`--ephemeral` for codex.

## Blocking findings

**B1 — The plan fixes only the bridge path; `seats smoke` / `setup smoke` launch Codex seats outside it and remain stoppable, and the plan never mentions this path at all.**
`seats.smoke_seat` (`seats.py:1121-1131`) hands `list(seat.commands[0])` — the bare seat argv — to `setup.smoke`, which runs it with `subprocess.run(expanded, stdin=DEVNULL, capture_output=True, ...)` and **no `env=` and no `cwd=`** (`setup.py:338-345`). That child inherits the ambient environment (no quiet flag) and the caller's working directory. The nested Codex sets `PLUGIN_ROOT` itself for its hook (HOOK-CONTRACT §Environment: "Codex provides the host-specific `PLUGIN_ROOT`/`PLUGIN_DATA` variables"), so whenever that cwd is not `ready` — e.g. `debate seats smoke codex/gpt-5.6-sol` run from any directory without a `debate-profile.json`, which is a normal host-level seat check — the hook returns `continue: false`, no reply lands in the scratch mailbox, and smoke reports a misleading `no reply landed in the scratch mailbox` failure. This is the same defect class the plan is repairing, on a second Debate-owned Codex launch path, and §1's outcome statement ("Debate's own non-interactive managed Codex seat is never stopped by the installation-onboarding hook") is not true after the plan as written. It is narrower than the bridge case (it depends on the cwd being unready) but it is real and unaddressed.
*Smallest adequate correction (either is acceptable):* (a) extend Slice A to pass an explicit environment for the smoke child — `env={**os.environ, "DEBATE_ONBOARDING_QUIET": "1"}`, scoped to a codex-vendor seat via `smoke_seat` so invariant 4 still holds — with one test asserting the child sees the flag and a non-codex smoke child does not; or (b) add one sentence to §4/§5 scoping the smoke path out explicitly, naming it as a known remaining instance and the follow-up that will carry it. What is not acceptable is silence, because the executor would otherwise close the checklist believing the class is closed.

**B2 — Slice D's branch-gate path is not executable as written: the gate's own Codex reviewer is broken by the very defect under repair, and the gate's model-call authorization is unstated.**
Slice D requires "both configured reviewers to run their own fresh checks against the exact new SHA". `collab/PROTOCOL.md` §1/§3 fixes those reviewers as the controller-bound headless **opus and codex** seats of `repository-unattended-02750`, and §4 pins the production driver line to `cd /home/zoltan/Projects/debate && PYTHONPATH=src python -m debate watch-once ...` — the **main checkout**, not the feature worktree. Run that way, the gate's Codex seat uses an unfixed `bridge.seat_environment()` and reproduces the retained `ERROR / adapter-error` (FIELD-ACCEPTANCE §3), so the gate can never reach PASS and the plan silently collapses onto the waiver branch. Separately, §1 states the plan "does not ... authorize a model call" and that the only ask is "the remaining two-call field recheck", yet a two-seat fold-delta gate is itself model-calling work with no stated budget or ask, and the field record shows the prior allowance is down to two ceiling slots.
*Smallest adequate correction:* one paragraph in Slice D fixing (i) which engine the gate's seats run through — state that the gate controller is driven from the fixed worktree/immutable snapshot so the Codex seat carries the fix (and record that as the first live proof of it), or that the gate runs with an explicit review adapter that sets the documented flag; and (ii) that the gate's seat calls are their own owner authorization, counted separately from and additional to the two field launches, or that the owner waives the gate outright.

**B3 — The plan's own gate commands dirty the worktree the plan requires to stay clean.**
Slice A/B use `--basetemp=.../.pytest-managed-codex` and `.../.pytest-managed-codex-full` inside the feature worktree. `.gitignore:5-13` ignores `.pytest_cache/` and `.pytest-tmp/` but **not** those names, so both runs leave untracked, non-ignored directories in the tree — directly against Slice B's "Stop on any regression or unrelated dirty-tree overlap", the exact-commit step, and Slice C's worktree-digest preservation (and the retained field record's "the feature worktree remains clean at exact `935a4f2`" check). It also creates a real `git add -A` hazard around the commit step.
*Smallest adequate correction:* use `--basetemp=/home/zoltan/Projects/debate/.worktrees/ox-alpha-frontier-seat/.pytest-tmp/managed-codex` and `.../.pytest-tmp/managed-codex-full` (already ignored; distinct subdirectories matter because pytest clears the basetemp it is given).

**B4 — The one implementation detail that decides the fix's coverage is left unfixed: where in `seat_environment()` the flag is set.**
`seat_environment()` returns early when no config home is declared: `if spec.config_home is None: return environment` (`bridge.py:617-618`). Slice A says only that the function "force-sets" the flag "only for vendor codex". If the executor writes the line after that branch, every codex seat without a `--config-home` — e.g. a manually added `codex/...` seat (`seats.add_seat` defaults `config_home=None`) — silently keeps the defect, and the plan's single proposed assertion ("a wrapped managed Codex seat sees the exact flag", which will use the catalogued `CODEX_HOME=.codex` seat) would not catch it.
*Smallest adequate correction:* state in Slice A that the flag is set immediately after the environment dict is built and before the `config_home` branch, and add one test case for a codex seat launched **without** `--config-home`.

## Non-blocking observations

1. **Cheap zero-call de-risking of the one unproven hop.** Every hop is attested except that a Codex process forwards an *inherited* environment variable to its plugin hook. HOOK-CONTRACT already relies on this (it calls the flag "the documented automation lever for Codex"), so this is not a new mechanism — but Slice C proves it only against a fake nested seat (step 5), leaving the real-host proof to the two-call field recheck. The 2026-08-19 spike technique (env-dump hook in an isolated HOME, HOOK-CONTRACT §Non-interactive detection) would attest it in Slice C for zero model calls. Recommend adding it to Slice C step 4.
2. **The quiet hook still injects onboarding context into the sealed seat's prompt.** With `quiet` true, `hooks/session-start:169-173` still emits `additionalContext` carrying the full `json.dumps(report)` — for the managed seat that reads `repair_required` for a sandbox home, plus "use the debate-onboarding skill after the user consents". The plan names this trade-off honestly (§3, Option 1), and `PROTOCOL.md` §5 records `isolation_mode: advisory`, so it is not a new contamination class; it is worth one line in the plan saying reviewers may see that context and that it is expected, so a future seat does not report it as a finding.
3. **Dangling reference.** §5 Slice D: "The current instruction to continue steps 1–5" — the plan has slices A–D and no steps 1–5. Renumber or name what is meant, otherwise the authorization sentence is unreadable standalone.
4. **README conditional is resolvable now.** The paragraph most at risk is not the Codex first-turn paragraph (README:114-120, which describes interactive Codex correctly) but README:227-233, "Claude and Codex seats need no extra setup", which is false today and becomes true only with this fix. Recommend the executor treat that line as the one to touch, with a clause noting the managed launcher sets the documented quiet signal automatically.
5. **Predecessor bookkeeping.** The predecessor plan's checklist still shows the installed matrix and fold-delta gate unchecked while the field record installed and ran `935a4f2`. Slice D's "do not reuse the expired, oversized, or schema-v1 preflight records as approval" handles this correctly for the new SHA; no action needed beyond keeping that clause.

## Criterion-by-criterion

1. Narrowest adequate correction, ordinary Codex unweakened — **not met**: narrow and non-weakening (verified), but not adequate for all Debate-launched Codex seats (B1).
2. Bridge/hook tests trace the failure and cover isolation, credentials, serialization, interactive stop — **met in substance**, with the coverage hole in B4.
3. Full gate, immutable install, zero-call matrix, fake/trap, preservation, credential scan executable and proportionate — **not met**: B3 makes the gate commands self-contradictory with the plan's clean-tree requirements; N1 is a recommended addition.
4. Preserves registry/profiles/channels/worktrees/prior evidence, no `/tmp`, no PATH `debate` — **substantially met** (Slice C steps 1/3/6 are specific and proportionate) except worktree cleanliness (B3).
5. Authorization boundaries internally consistent — **not met** (B2).
6. Every material design choice fixed — **not met** (B1, B2, B4).

None of these require redesign. With B1–B4 corrected in place, I would expect this plan to pass on the same evidence.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 2672750896af177fc20eff690ae1d1f711e5a25d70f71ace10e9e91834db07d2
- phase: sealed
- captured-at: 2026-08-25T05:20:46+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "Grep -n --pattern 'seat_environment|DEBATE_ONBOARDING_QUIET' /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus", "exit_status": 0, "output": "hooks/session-start:59:    # interactive/headless distinction, so DEBATE_ONBOARDING_QUIET=1 remains\nhooks/session-start:63:        os.environ.get(\"DEBATE_ONBOARDING_QUIET\") == \"1\"\nhooks/HOOK-CONTRACT.md:57:  current session is interactive. `DEBATE_ONBOARDING_QUIET=1` is therefore the\nsrc/debate/bridge.py:603:def seat_environment(spec: BridgeSpec) -> dict[str, str]:\nsrc/debate/bridge.py:1005:    environment = seat_environment(spec)\nCHANGELOG.md:73:  banner; for Codex automation the documented lever is `DEBATE_ONBOARDING_QUIET=1`\ntests/test_ox_alpha.py:164:        nested_environment = bridge.seat_environment(spec)\ntests/test_session_start_hook.py:305:        project, tmp_path / \"reg.json\", extra_env={\"DEBATE_ONBOARDING_QUIET\": \"1\"}\ntests/test_session_start_hook.py:321:        extra_env={**CODEX_ENV, \"DEBATE_ONBOARDING_QUIET\": \"1\"},\n\n(Confirms the product bridge does NOT set the flag at 935a4f2; only the hook reads it.)"}, {"command": "Read /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus/src/debate/bridge.py (offset 596, limit 35)", "exit_status": 0, "output": "600\tOUR_OWN_ENV = (REAL_HOME_ENV, \"PYTHONPATH\")\n603\tdef seat_environment(spec: BridgeSpec) -> dict[str, str]:\n613\t    real_home = os.environ.get(REAL_HOME_ENV, \"\")\n614\t    environment = {\n615\t        name: value for name, value in os.environ.items() if name not in OUR_OWN_ENV\n616\t    }\n617\t    if spec.config_home is None:\n618\t        return environment\n619\t    if not real_home:\n620\t        raise Refusal(...)\n625\t        variable, folder = seats.validate_config_home(spec.config_home, home=Path(real_home))\n628\t    environment[variable] = str(folder)\n629\t    return environment\n\n(Early return at 617-618 is the placement hazard in blocker B4.)"}, {"command": "Read /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus/hooks/session-start", "exit_status": 0, "output": "61\t    entrypoint = os.environ.get(\"CLAUDE_CODE_ENTRYPOINT\", \"\")\n62\t    quiet = (\n63\t        os.environ.get(\"DEBATE_ONBOARDING_QUIET\") == \"1\"\n64\t        or entrypoint == \"sdk-cli\"\n65\t        or entrypoint.startswith(\"sdk-\")\n66\t    )\n...\n118\t    codex_interactive = bool(os.environ.get(\"PLUGIN_ROOT\")) and not quiet\n...\n169\t    _emit(_out(\n170\t        None if quiet else notice,\n171\t        base_context,\n172\t        stop_before_model=codex_interactive,\n173\t    ))\n\n(Confirms quiet suppresses systemMessage and, via codex_interactive, continue/stopReason.)"}, {"command": "Read /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus/src/debate/setup.py (offset 305, limit 60)", "exit_status": 0, "output": "318\t    driven = [(p, argv) for p, argv in spec.commands.items() if argv]\n319\t    for party, argv in driven:\n338\t            expanded = [part.replace(\"{prompt}\", prompt) for part in argv]\n339\t            try:\n340\t                proc = subprocess.run(expanded, stdin=subprocess.DEVNULL,\n341\t                                      capture_output=True, text=True,\n342\t                                      timeout=spec.timeout_seconds, check=False)\n...\n353\t                tail = (proc.stdout or proc.stderr or \"\").strip()[-160:]\n354\t                failures.append(\n355\t                    f\"{party}: no reply landed in the scratch mailbox \"\n356\t                    f\"(exit {proc.returncode}; output tail: {tail!r})\")\n\n(No env= and no cwd= : the smoke child inherits the ambient environment and cwd -- blocker B1.)"}, {"command": "Read /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus/src/debate/seats.py (offset 1076, limit 80)", "exit_status": 0, "output": "1076\tdef smoke_seat(\n1086\t    \"\"\"One scratch-channel round trip for one seat's FIRST-LISTED argv,\n1118\t    party = slug(seat.vendor)\n1121\t    spec = SetupSpec(\n1125\t        commands={party: list(seat.commands[0]), \"probe\": None},\n1131\t    failures = setup_module.smoke(spec, scratch_base=scratch_base, emit=emit)\n\n(The bare seat argv, not the run-seat bridge command, is what smoke launches.)"}, {"command": "Read /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus/.gitignore", "exit_status": 0, "output": "5\t__pycache__/\n6\t*.egg-info/\n7\t.venv/\n8\t.mypy_cache/\n9\t.ruff_cache/\n10\t.pytest_cache/\n11\tdist/\n12\tbuild/\n13\t.pytest-tmp/\n...\n31\t.worktrees/\n37\t.release-acceptance/\n47\tdocs/plans/\n51\tvar/\n\n(No entry matches .pytest-managed-codex / .pytest-managed-codex-full -- blocker B3.)"}, {"command": "Read /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus/src/debate/seat_catalog.py (codex entry) + Grep __version__ in src/debate/__init__.py", "exit_status": 0, "output": "166\t    CatalogEntry(\n167\t        vendor=\"codex\",\n168\t        binaries=(\"codex-agent\",),\n169\t        submodels=(\"gpt-5.6-sol\",),\n171\t        invocation=(\"{binary}\", \"{prompt}\"),\n176\t        sibling_pattern=\"codex*-agent\",\n177\t        isolation_argv=(\"--ignore-user-config\", \"--ignore-rules\"),\n178\t        no_persistence_argv=(\"--ephemeral\",),\n179\t        verification_capable=True,\n180\t        config_home=\"CODEX_HOME=.codex\",\n\n__init__.py:42:__version__ = \"0.8.0\"  (matches Slice C's \"Debate 0.8.0\")"}, {"command": "Read docket file var/debate/plan-managed-codex-compat-39215/dockets/4c650ebf.../files/docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md (Slice A/B verification blocks and Slice D)", "exit_status": 0, "output": "140\t  --basetemp=/home/zoltan/Projects/debate/.worktrees/ox-alpha-frontier-seat/.pytest-managed-codex \\\n173\t  --basetemp=/home/zoltan/Projects/debate/.worktrees/ox-alpha-frontier-seat/.pytest-managed-codex-full \\\n...\n231\t- require both configured reviewers to run their own fresh checks against the exact\n232\t  new SHA; and\n...\n247\tThe current instruction to continue steps 1-5 authorizes work through this separate\n248\tfield ask.\n\n(Basetemp names -> B3; reviewer requirement -> B2; 'steps 1-5' -> observation 3.)"}, {"command": "Bash: sha256sum <docket plan file> <plan-docket.md>  [DENIED by this run's permission mode; no digest recomputation was possible]", "exit_status": 1, "output": "Permission to use Bash has been denied because Claude Code is running in don't ask mode. (Recorded for transparency: docket/export integrity was therefore verified by direct read of file contents with the read-only file tools, not by recomputed SHA-256.)"}], "status": "performed"}

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 1fade7c0b1ba425ab58057fa1ab3dfae055c209e3613fc1c434e5d88994e73f6
- controller-config-sha256: 292649b102489104e019f8bd3de6c7f29fa27d08c5f162256ab3dfdd817daae3
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: ab6f6f72a34fc909d744f304a0f5e9bcafd5fa192cfc71608f3f5db764642e00
- docket-revision-sha256: 4c650ebf9d225ed873a57375b6c6086be649a671e2eb5ef8dc2a84e2eeea03e8
- input-sha256: 7102c0c2e41b374cd19110dbcb8190b19a27e97cf7db1398b594a58beef0d1fb
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: performed
- verification-evidence-basis: seat-declared

## MSG-5 | 2026-08-25T05:20:46+00:00 | from: codex | type: verdict | thread: plan-managed-codex-compat-2 | refs: -

## Review — 2026-08-24 · codex

The runtime-only Codex quiet flag is the narrow correction: the hook already treats `DEBATE_ONBOARDING_QUIET=1` as context-only/non-stopping, while the bridge is the controller-only nested-process boundary. The planned bridge, hook, credential, serialization, and preservation coverage is otherwise appropriately targeted.

Blocking finding:

1. Slice B violates invariant §4. It declares every test/cache/temp path project-local, yet its required mypy gate sets `--cache-dir=/dev/null`. That is an explicit non-project-local cache path, so the plan does not satisfy docket criterion 4 as written. Replace it with a newly named project-local cache path (for example `/home/zoltan/Projects/debate/.worktrees/ox-alpha-frontier-seat/.mypy-managed-codex`) and include that path in the preserved/ignored test-artifact handling. No other design change is needed.

Non-blocking clarification: Slice C should expressly state that its installed-hook direct status/contract check is the zero-call proof for the ready-Codex row. A real ready Codex submitted prompt would proceed to inference, whereas the direct installed-hook fixture can prove the required absence of `systemMessage`, `continue`, and `stopReason` without violating the zero-call boundary.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 2672750896af177fc20eff690ae1d1f711e5a25d70f71ace10e9e91834db07d2
- phase: sealed
- captured-at: 2026-08-25T05:20:46+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "sha256sum /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/dockets/4c650ebf9d225ed873a57375b6c6086be649a671e2eb5ef8dc2a84e2eeea03e8/files/docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "exit_status": 0, "output": "7f4814ca1972e7c858fa2c5a3af260b647ae5790a0874675123daab868d6f15e  .../docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md"}, {"command": "sed -n '108,173p' /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/dockets/4c650ebf9d225ed873a57375b6c6086be649a671e2eb5ef8dc2a84e2eeea03e8/files/docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "exit_status": 0, "output": "Slice B requires full pytest with a project-local --basetemp, then ruff, then mypy with `--cache-dir=/dev/null`; Slice C requires the real zero-call host matrix including `Codex ready silence` and installed hook direct status/contract checks."}, {"command": "sed -n '603,631p' /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/codex/src/debate/bridge.py", "exit_status": 0, "output": "seat_environment copies the controller-sandboxed environment minus only DEBATE_BRIDGE_REAL_HOME and PYTHONPATH, then supplies an optional validated config-home pointer. This is the narrow nested-seat boundary named by the plan."}, {"command": "sed -n '56,126p' /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/codex/hooks/session-start", "exit_status": 0, "output": "The hook defines quiet when DEBATE_ONBOARDING_QUIET=1, and defines codex_interactive only when PLUGIN_ROOT is present and quiet is false. Attention output uses stop_before_model=codex_interactive; quiet output therefore contains context but no stop fields."}], "status": "performed"}

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: bee22f886e30edc9b85e703a5bb2880213d36db6cfb248f8abfde7e275993136
- controller-config-sha256: 292649b102489104e019f8bd3de6c7f29fa27d08c5f162256ab3dfdd817daae3
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: ea617a03f99343b0521febaf39ff4aeb8cb5375e1c67e8b749a78b6e76ef008b
- docket-revision-sha256: 4c650ebf9d225ed873a57375b6c6086be649a671e2eb5ef8dc2a84e2eeea03e8
- input-sha256: ff0313fa5aba70412445b2aa6363c59e143cd8f61ebb5406ad3a6b2aa5488f5c
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.1
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: performed
- verification-evidence-basis: seat-declared

## MSG-6 | 2026-08-25T05:20:46+00:00 | from: owner | type: close | thread: plan-managed-codex-compat-2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-7 | 2026-08-25T17:13:16+00:00 | from: owner | type: review-request | thread: plan-managed-codex-compat-3 | refs: feature/ox-alpha-frontier-seat@935a4f2841cc103ea4a1da8f07fb58b3760c997f

Re-review the amended managed-Codex onboarding compatibility plan against every
criterion in `var/debate/plan-managed-codex-compat-39215/plan-docket.md` and every
fold claimed in `var/debate/plan-managed-codex-compat-39215/fold-list-r1.md`.

The prior independent verdicts are preserved verbatim at the end of the plan and in
channel `plan-managed-codex-compat-39215` MSG-4/MSG-5. Independently verify the
current immutable plan and pinned source at
`feature/ox-alpha-frontier-seat@935a4f2841cc103ea4a1da8f07fb58b3760c997f`.
Do not treat the fold list as proof.

PASS only if MSG-4 B1–B4 and the MSG-5 cache-path blocker are actually resolved and
the folds introduce no new blocker. Cite fresh read-only commands with bounded
performed schema-v2 evidence. Return every blocking finding in one verdict and a
complete attributable review body. Do not edit the source export, live plan, channel,
registry, profiles, host configuration, or acceptance evidence. Never use `/tmp`.

The headless Codex review adapter again sets the existing documented quiet automation
flag only for its own reviewer subprocess; that is review infrastructure, not product
evidence.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: f6add77a460791158f715a678d86705fc62212ee3be74067c96dae8e514ed633
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-contract: {"review_contract_basis": "legacy-absent", "review_mode": "release-gate"}
- docket-revision-sha256: 1ca7bffe4cf2a3f2a9a6addb997e269e89a9cb44840b6505a82f69576d8b57d2
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-managed-codex-compat-39215.debate.json", "sha256": "5936dbbeb9983e4dca254ee495a2701755f2a3bda6aacb29efa456cc95b10032", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "sha256": "28cd67c4ebd8897825d8b1517f2d6c8c29d43f9387d7c57df3726441768a1bb8", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-24-codex-first-turn-onboarding-fold.md", "sha256": "f15c4890fd166e70782b6f859705b7f9c5165af7b5c53355a944536efcd2e043", "tracked_at_source_ref": false}, {"path": ".release-acceptance/ox-alpha/codex-first-turn-fold-935a4f2/FIELD-ACCEPTANCE.md", "sha256": "3080ec5d17915e2c5a1ff5a5f20eb1136d0fe8b8a606972f2bf6ac63e51ba530", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/plan-docket.md", "sha256": "c845ca0d3d08c685588fe708a3802e61a4d1e450d386d32a5d2f95f5a181efe5", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/fold-list-r1.md", "sha256": "6a75ce0c549a04612c9721bac1bde3368e87c3b6d1b9fbc84d0e59d23984b2d7", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/seat-result.schema.json", "sha256": "b00e642e165bb549a9544c0307ea6f1f7ca3d632b8b1b8d0d113d90f39c41822", "tracked_at_source_ref": false}, {"path": "var/debate/plan-managed-codex-compat-39215/seat_adapter.py", "sha256": "872d836b260b847fc2998a978f6f60193998a23775dd8799d3f5a402b719a72f", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "bee22f886e30edc9b85e703a5bb2880213d36db6cfb248f8abfde7e275993136", "opus": "1fade7c0b1ba425ab58057fa1ab3dfae055c209e3613fc1c434e5d88994e73f6"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.1", "command_sha256": "15b288104441db83d598ab8f4e63b4bab3bbacb661ab82eb1b4b95bf18068e7e", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "pinned read-only source export; workspace-write sandbox limited to controller invocation output", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 2, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "75ffdf5bb55ad336706dc19328760d5d9101c57991241fbc6863ea04fb59aff2", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "pinned read-only source export; result path controller-owned; read-only inspection tools", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 2, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "ea617a03f99343b0521febaf39ff4aeb8cb5375e1c67e8b749a78b6e76ef008b", "opus": "ab6f6f72a34fc909d744f304a0f5e9bcafd5fa192cfc71608f3f5db764642e00"}

## MSG-8 | 2026-08-25T17:20:37+00:00 | from: opus | type: verdict | thread: plan-managed-codex-compat-3 | refs: -

## Scope and method

I read the immutable docket (the amended plan, the predecessor plan, the retained `FIELD-ACCEPTANCE.md`, `collab/PROTOCOL.md`, the gate docket, the fold list `fold-list-r1.md`, and the gate's own `seat_adapter.py`/`seat-result.schema.json`) and re-derived every claim from the pinned export at `935a4f2841cc103ea4a1da8f07fb58b3760c997f`: `src/debate/bridge.py`, `hooks/session-start`, `hooks/HOOK-CONTRACT.md`, `src/debate/seat_catalog.py`, `src/debate/seats.py`, `src/debate/setup.py`, `src/debate/opening.py`, `tests/test_bridge.py`, `tests/test_session_start_hook.py`, `README.md`, `CHANGELOG.md`, `pyproject.toml`, `.gitignore`.

Per the docket's own caveat I again treated the gate adapter's `DEBATE_ONBOARDING_QUIET=1` (`seat_adapter.py:133`) as review infrastructure only; the product bridge still does not set the flag at the pinned ref (`bridge.py:603-629`).

Method limitation, stated plainly and unchanged from the previous round: this seat's shell is restricted in this run and `sha256sum` was denied, so I could not recompute the docket digests. Every finding below rests on direct reads of the docket and export contents with quoted file/line evidence, not on digest confirmation.

Verdict: **NO_PASS**, on one blocking finding with a one-clause correction. All five blockers from the previous round (my B1–B4 and the codex seat's MSG-5 mypy blocker) are genuinely closed in the amended text — I verified each fold against the source rather than against `fold-list-r1.md`'s claims. The remaining blocker is in material the amendment newly added.

## Round-1 folds verified closed

- **B1 (standalone smoke silence) — closed by scope-out, which is the alternative I expressly accepted.** §1 and invariant 3 now say "controller-bound … launched through `run-seat`", and §3 carries a named non-goal that identifies `seats smoke`/`setup --smoke` as a remaining separate instance, forbids it in the final field case, and defers it to a plan carrying its own child-environment design, tests, and call authorization. The underlying defect is still real at the pinned ref — `seats.smoke_seat` (`seats.py:1121-1131`) passes the bare argv to `setup.smoke`, which runs `subprocess.run(expanded, stdin=DEVNULL, capture_output=True, ...)` with no `env=` and no `cwd=` (`setup.py:338-345`) — so the honest scope-out, not silence, is what the plan now delivers.
- **B2 (gate engine and gate-call authorization) — closed.** Slice D now stops for a distinct owner authorization of two expected / four maximum reviewer launches, states those are separate from and do not consume the two field launches, requires the gate to be driven from the fixed immutable snapshot or an explicit quiet review adapter rather than the unfixed main-checkout bridge, and requires the chosen engine and its digest to be recorded. That resolves the collision with `PROTOCOL.md` §4, whose production driver line is explicitly the post-merge main-checkout scheduler.
- **B3 (unignored basetemps) — closed and verified against the ignore file.** Both runs now use `.pytest-tmp/managed-codex` and `.pytest-tmp/managed-codex-full`; `.gitignore:13` ignores `.pytest-tmp/`. The two basetemps are distinct subdirectories, which matters because pytest clears the basetemp it is given. `pyproject.toml:53` already sets a relative `--basetemp=.pytest-tmp` in `addopts`; the plan's explicit absolute value comes later on the command line and wins, so the artifacts stay inside the ignored directory regardless of CWD.
- **B4 (early-return placement) — closed, and it is the correct placement.** Slice A now requires the flag "immediately after the filtered environment dict is built and before the `config_home is None` early return", plus a Codex-without-config-home test. That is exactly the gap: `bridge.py:614-618` builds `environment` and then returns early when `spec.config_home is None`, and `seats.add_seat` defaults manual seats to `config_home=None`, so a line placed after the branch would leave manually added `codex/...` seats defective. `tests/test_bridge.py:769-803` already has the config-home fixtures to extend, and `tests/test_session_start_hook.py:33-44` already supports the `extra_env` injection the new hook fixture needs.
- **codex MSG-5 (`--cache-dir=/dev/null`) — closed.** Slice B now uses `.mypy_cache/managed-codex`, which is project-local and ignored by `.gitignore:8`, satisfying invariant 7.
- **Non-blocking items folded.** The `repair_required` advisory context is documented in §3; the dangling "steps 1–5" sentence is now explicit Slice A–C language; Slice B names the right README claim — I confirmed the target line is `README.md:227` ("**Claude and Codex seats need no extra setup.**"), not the interactive first-turn paragraph; Slice C states the ready-Codex row is proved by the installed-hook direct fixture rather than a submitted prompt.

## Mechanism re-verification (unchanged and still sound)

- `hooks/session-start:63-66` computes `quiet` from `DEBATE_ONBOARDING_QUIET == "1"`; `:118` sets `codex_interactive = bool(os.environ.get("PLUGIN_ROOT")) and not quiet`; `:172` passes that as `stop_before_model`, and `_out` adds `continue: False` plus `stopReason` only then (`:46-48`). A managed Codex seat carrying the flag cannot be stopped. Invariant 3 holds.
- `spec.vendor` is registry-sourced at the call site (`opening.py:1002` passes `seat.vendor` into `run-seat`), and the catalog records the exact literal `vendor="codex"` (`seat_catalog.py:167`). The `spec.vendor == "codex"` predicate is adequate for catalog, sibling-wrapper, and manual routes.
- Invariants 4–6 hold: `seat_environment` builds a fresh dict from `os.environ` minus `OUR_OWN_ENV = (REAL_HOME_ENV, "PYTHONPATH")` (`bridge.py:600,614-616`); nothing serialized touches it; `redact_seat_output` iterates only the declared `credential_env` names (`bridge.py:694-711`), so a new non-credential variable cannot change credential behavior byte-for-byte.

## Blocking finding

**B1 (this round) — Slice C step 4's new env-forwarding probe is the one row whose stated mechanism can cross the inference boundary it exists to respect.**

The added bullet requires "an isolated zero-call env-dump hook proving that a real Codex process forwards an inherited `DEBATE_ONBOARDING_QUIET=1` value to its plugin hook." Per `HOOK-CONTRACT.md:62-66`, Codex does not invoke `SessionStart` when a prompt-free thread opens; "the first submitted turn invokes it before inference." So the probe must submit a turn. But the variable under test is precisely what disarms the stop: with the flag inherited, `quiet` is true, `codex_interactive` is false (`hooks/session-start:118`), and no `continue: false`/`stopReason` is emitted (`:46-48,172`). Any probe that reuses the product hook — or any probe hook that dumps the environment and simply returns — therefore lets the submitted turn proceed to the model. That is an unauthorized inference inside a slice whose whole contract is zero-call, and inside a plan whose §1 states it does not silently authorize a model call and whose remaining field allowance is exactly two ceiling slots (`FIELD-ACCEPTANCE.md:96-99`).

This is not a hypothetical: the plan already recognizes the identical hazard one bullet earlier and spells out the mechanism for the ready-Codex row ("proved by the installed-hook direct fixture, not a submitted real ready prompt, which would cross the inference boundary"). Leaving the adjacent, riskier row's mechanism unstated is internally inconsistent and leaves a material design choice to improvisation at the exact boundary the plan protects most carefully.

*Smallest adequate correction (either is sufficient):*
(a) State in Slice C step 4 that the probe uses a dedicated project-local probe hook in the isolated home which dumps the observed environment **and unconditionally returns `continue: false`**, so the turn is stopped by the probe hook itself independent of quiet state — the same technique the predecessor's Slice A used successfully (`2026-08-24-codex-first-turn-onboarding-fold.md:129-139,154-165`) — and record zero model-output items and zero token-usage events as that proof's acceptance criterion; or
(b) delete the row. It was my own de-risking recommendation from the previous round, not a docket requirement; Slice C step 5's managed fake/trap and the final field recheck still cover the path, and dropping it costs only that the inherited-variable hop stays attested by HOOK-CONTRACT rather than re-proved here.

No redesign is implied either way. With B1 corrected, I would expect this plan to pass on the same evidence.

## Non-blocking observations

1. **mypy exclude anchoring under an absolute path argument.** `pyproject.toml:70` excludes `^build/` and `^var/` — relative-anchored regexes. Slice B invokes `mypy <absolute worktree path>`, so a stale `build/` in the worktree would not be excluded and would fail the gate with "Duplicate module named 'debate'" rather than being skipped. Recommend the executor confirm the worktree carries no `build/`/`var/` before the gate (or run mypy from the worktree with `.`). Nothing else in the three gate commands is at risk: `testpaths` applies only when no path arguments are given, and `.pytest-tmp`/`.mypy_cache` are dot-directories that pytest's default `norecursedirs` and mypy's crawler skip.
2. **The adapter option for the gate does not exercise the fix.** If Slice D's gate runs through "an explicit review adapter that sets the already documented quiet signal", the gate proves review coverage, not the bridge fix, and the first live proof of the fix remains the two-call field recheck. The plan already requires recording the chosen engine and digest; one clause naming this consequence would stop a later reader from citing gate success as field proof.
3. **Hook-trust bookkeeping is generic rather than named.** Slice C steps 1/3 say "Preserve unrelated host data", which covers `~/.codex/config.toml` `[hooks.state]` entries, but the predecessor plan named trust entries explicitly (invariant 2). Since this plan changes no hook file, no new Codex trust prompt is expected at reinstall (`HOOK-CONTRACT.md:84-89`); saying so would let an unexpected prompt be treated as a finding rather than clicked through.
4. **Slice C has no per-row stop criteria.** Slices A and B each carry an explicit "Stop if …"; Slice C carries only "Stop before any real seat call" plus rollback. One line — any failed matrix row stops before the fake/trap and before the gate — would match the rest of the plan's discipline.
5. **Non-Codex assertion is ambient-sensitive.** The Slice A test that a Claude/Ox seat "does not see it" will need to control the parent environment, since an operator shell that already exports `DEBATE_ONBOARDING_QUIET` would pass it through for every vendor. That is inherited, not new (invariant 4 is about new values), but the test must set the parent env explicitly to avoid a false green.

## Criterion-by-criterion

1. Narrowest adequate correction, ordinary Codex unweakened — **met**. Placement, vendor predicate, and the interactive stop path verified against the source; the smoke path is now scoped out by name rather than silently.
2. Bridge/hook tests trace the proven failure and cover non-Codex isolation, credentials, serialization, interactive stop — **met**, including the previously missing `config_home=None` case and the managed-home `repair_required` fixture.
3. Full gate, immutable install, zero-call host matrix, managed fake/trap, preservation comparison, credential scan executable and proportionate — **not met**: one matrix row's mechanism can spend a real model call as written (B1). Everything else in the slice is executable and proportionate.
4. Preserves registry, profiles, channels, worktrees, prior evidence; no `/tmp`; no PATH `debate` — **met**. Both cache/temp paths are now project-local and ignored; invariant 8 and Slice C steps 1/3/6 are specific.
5. Authorization boundaries internally consistent — **met**. Zero-call implementation/install proof; gate-or-waiver before field work; separately authorized two-expected/four-maximum reviewer launches; separate ask for exactly two expected / two maximum sequential field launches, which matches the retained record's two remaining ceiling slots; waiver reserved to the owner.
6. Every material design choice fixed — **not met**, on B1 alone.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 3c7c862c02d409296ad7a3a0981bfc6e0c50ad52887fb36f57d682cd774794b6
- phase: sealed
- captured-at: 2026-08-25T17:20:37+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "ls -la /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/exports/935a4f2841cc103ea4a1da8f07fb58b3760c997f/opus", "exit_status": 0, "output": "read-only export root (dr-xr-xr-x, files r--r--r--): .agents .claude .claude-plugin .codex-plugin .github docs examples hooks scripts skills src tests .gitignore CHANGELOG.md MANIFEST.in PROTOCOL.md README.md pyproject.toml watcher.example.json watcher.brokered.example.json. No collab/ or var/ in the export, as PROTOCOL.md \u00a75 requires."}, {"command": "grep -n \"def seat_environment\" -A 60 <export>/src/debate/bridge.py", "exit_status": 0, "output": "600: OUR_OWN_ENV = (REAL_HOME_ENV, \"PYTHONPATH\")\n603: def seat_environment(spec: BridgeSpec) -> dict[str, str]:\n613-616: real_home = os.environ.get(REAL_HOME_ENV, \"\"); environment = {name: value for name, value in os.environ.items() if name not in OUR_OWN_ENV}\n617-618: if spec.config_home is None: return environment\n619-628: Refusal when real_home missing; environment[variable] = str(folder)\nNo DEBATE_ONBOARDING_QUIET anywhere in the function: the product bridge does not set the flag at the pinned ref."}, {"command": "sed -n '50,190p' <export>/hooks/session-start", "exit_status": 0, "output": "63-66: quiet = os.environ.get(\"DEBATE_ONBOARDING_QUIET\") == \"1\" or entrypoint == \"sdk-cli\" or entrypoint.startswith(\"sdk-\")\n118: codex_interactive = bool(os.environ.get(\"PLUGIN_ROOT\")) and not quiet\n169-173: _emit(_out(None if quiet else notice, base_context, stop_before_model=codex_interactive))\nReady path returns early with no stop; quiet path still emits additionalContext carrying json.dumps(report)."}, {"command": "Grep pattern=\"def _out|stop_before_model|continue|stopReason\" path=<export>/hooks/session-start -n", "exit_status": 0, "output": "32: def _out(\n36:     stop_before_model: bool = False,\n46-48: if stop_before_model: payload[\"continue\"] = False; payload[\"stopReason\"] = ...\n172:     stop_before_model=codex_interactive,\nConfirms continue/stopReason are emitted only when stop_before_model is true, i.e. never when quiet is set."}, {"command": "Read <export>/.gitignore", "exit_status": 0, "output": "line 8: .mypy_cache/\nline 10: .pytest_cache/\nline 13: .pytest-tmp/\nline 47: docs/plans/\nline 51: var/\nBoth amended gate paths (.pytest-tmp/managed-codex[-full], .mypy_cache/managed-codex) fall under ignored directories; the round-1 B3 and codex MSG-5 blockers are closed."}, {"command": "Read <export>/pyproject.toml", "exit_status": 0, "output": "51-53: [tool.pytest.ini_options] testpaths = [\"tests\"]; addopts = [\"--basetemp=.pytest-tmp\"] (relative; the plan's explicit absolute --basetemp comes later on the command line and overrides it).\n58-70: [tool.mypy] strict = true; exclude = [\"^build/\", \"^var/\"] (relative-anchored; basis for non-blocking observation 1)."}, {"command": "Grep pattern=\"DEBATE_ONBOARDING_QUIET\" path=<export> -n", "exit_status": 0, "output": "hooks/session-start:59,63; hooks/HOOK-CONTRACT.md:57; CHANGELOG.md:73; tests/test_session_start_hook.py:305,321. No occurrence in src/debate/*.py \u2014 independent confirmation that the flag is documented and hook-side only, and not yet set by the product bridge."}, {"command": "Grep pattern=\"smoke\" path=<export>/src/debate/seats.py -n  +  Grep pattern=\"def smoke\" -A 40 path=<export>/src/debate/setup.py -n", "exit_status": 0, "output": "seats.py:1121-1131: smoke_seat builds a scratch channel and calls setup_module.smoke(spec, ...) with the bare seat argv.\nsetup.py:338-345: expanded = [...]; subprocess.run(expanded, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=..., check=False) \u2014 no env= and no cwd=, so the smoke child inherits the ambient environment. Confirms the defect the amended plan now scopes out by name."}, {"command": "Grep pattern=\"--vendor\" -C 4 path=<export> -n", "exit_status": 0, "output": "src/debate/opening.py:1002: \"--vendor\", seat.vendor (registry-sourced) into the run-seat command; bridge.py:198,218,316 parse it into BridgeSpec.vendor. The vendor predicate proposed in Slice A is fed by the registry value, not a derived string."}, {"command": "Grep pattern=\"codex\" -C 4 path=<export>/src/debate/seat_catalog.py -n", "exit_status": 0, "output": "167-181: CatalogEntry(vendor=\"codex\", binaries=(\"codex-agent\",), submodels=(\"gpt-5.6-sol\",), isolation_argv=(\"--ignore-user-config\", \"--ignore-rules\"), no_persistence_argv=(\"--ephemeral\",), config_home=\"CODEX_HOME=.codex\"). Exact literal vendor string confirmed; also confirms Option 4's claim that no per-plugin hook disable is attested."}, {"command": "Grep pattern=\"def _run_hook|extra_env|CODEX_ENV\" path=<export>/tests/test_session_start_hook.py -n  +  Grep pattern=\"seat_environment|config_home\" path=<export>/tests/test_bridge.py -n", "exit_status": 0, "output": "test_session_start_hook.py:24 CODEX_ENV = {\"PLUGIN_ROOT\": ...}; :33-44 _run(..., extra_env) merge; :305,321 existing quiet fixtures. test_bridge.py:769,792,803 config-home fixtures; :870 asserts spec.config_home == \"CODEX_HOME=.codex\". The fixtures the amended Slice A needs already exist and are extensible."}, {"command": "Read <docket>/var/debate/plan-managed-codex-compat-39215/plan-docket.md  +  .../fold-list-r1.md", "exit_status": 0, "output": "Docket criteria 1-6 read as quoted in the criterion-by-criterion section; the docket's closing caveat marks the review adapter's quiet flag as review infrastructure only. fold-list-r1.md claims five blocking folds and five non-blocking folds; each was re-checked against the amended plan text and the export rather than accepted as stated."}, {"command": "Read <docket>/docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "exit_status": 0, "output": "Amended plan, 366 lines, Status: DRAFT \u2014 pending debate review, Amended after MSG-4/MSG-5. \u00a73 now carries the explicit smoke non-goal; Slice A fixes the pre-early-return placement; Slice B uses .pytest-tmp/* and .mypy_cache/managed-codex; Slice C step 4 adds the env-dump row (basis of this round's blocker) and the ready-Codex direct-fixture clause; Slice D fixes gate engine plus a separate two-expected/four-maximum reviewer authorization; both round-1 reviewer sections are retained verbatim."}, {"command": "Read <docket>/docs/plans/2026-08-24-codex-first-turn-onboarding-fold.md  +  <docket>/.release-acceptance/ox-alpha/codex-first-turn-fold-935a4f2/FIELD-ACCEPTANCE.md", "exit_status": 0, "output": "Predecessor Slice A (lines 129-139,154-165) is the precedent for a stopped, zero-call probe turn: copied hook payload returning continue:false, app-server evidence of an empty completed turn, zero model-output items, zero token-usage events. FIELD-ACCEPTANCE lines 53-67 record the managed Codex adapter-error and the zero-call replay (registry missing, profile broken, repair_required); lines 96-99 record two remaining retry-inclusive ceiling slots, matching the plan's two-expected/two-maximum field ask."}, {"command": "Read <docket>/collab/PROTOCOL.md  +  Grep pattern=\"DEBATE_ONBOARDING_QUIET\" -C 6 path=<docket>/var/.../seat_adapter.py", "exit_status": 0, "output": "PROTOCOL.md \u00a71/\u00a73 fix the two controller-bound seats (opus, codex) and \u00a74 pins the production driver line to the main checkout after merge \u2014 the basis for the round-1 B2 finding that Slice D has now resolved. seat_adapter.py:131-133 sets CODEX_HOME and DEBATE_ONBOARDING_QUIET=1 for its own headless Codex subprocess; treated as review infrastructure only, per the docket caveat."}, {"command": "sha256sum <docket files>", "exit_status": 126, "output": "Denied by this run's permission mode; the digests named in the docket were therefore NOT recomputed. Reported here only as a stated limitation of my verification \u2014 no finding in this review depends on digest confirmation; all rest on direct reads of docket and export contents."}], "status": "performed"}

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 1fade7c0b1ba425ab58057fa1ab3dfae055c209e3613fc1c434e5d88994e73f6
- controller-config-sha256: f6add77a460791158f715a678d86705fc62212ee3be74067c96dae8e514ed633
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: ab6f6f72a34fc909d744f304a0f5e9bcafd5fa192cfc71608f3f5db764642e00
- docket-revision-sha256: 1ca7bffe4cf2a3f2a9a6addb997e269e89a9cb44840b6505a82f69576d8b57d2
- input-sha256: da5c628ea6de3a8dee04b592391259425c8b4e5a61c49f9170a10c2825db2eb9
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: performed
- verification-evidence-basis: seat-declared

## MSG-9 | 2026-08-25T17:20:37+00:00 | from: codex | type: verdict | thread: plan-managed-codex-compat-3 | refs: -

## Review — 2026-08-24 · codex

Verdict: PASS.

The selected runtime-only flag is the narrowest adequate repair for the controller-bound `run-seat` path. The current hook makes quiet Codex runs context-only and non-stopping, while ordinary interactive Codex remains the only path that receives `continue: false`.

The amended plan closes the established blockers: it explicitly scopes standalone smoke out; fixes placement before the `config_home is None` return and tests that case; uses ignored project-local pytest/mypy paths; includes the real-host env-dump and managed fake/trap; and separates branch-gate authorization from the final exactly-two-launch field authorization. It also preserves credential handling, serialization boundaries, protected state, no-`/tmp` use, and no-PATH-`debate` execution.

The immutable-install and zero-call checks are proportionate: they require an exact archive, controlled reinstall scope, preservation comparison, credential scan without disclosure, and stop before any real seat call. Slice D requires either the fixed immutable snapshot or an explicit quiet review adapter, preventing recurrence of the unfixed bridge failure during branch review.

No blocking finding remains. Non-blocking: the retained prior review sections correctly remain attributable historical context and do not alter the amended operative slices.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3c7c862c02d409296ad7a3a0981bfc6e0c50ad52887fb36f57d682cd774794b6
- phase: sealed
- captured-at: 2026-08-25T17:20:37+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "rg --files -uu -g '!.git' | wc -l", "exit_status": 0, "output": "92"}, {"command": "sha256sum collab/PROTOCOL.md collab/plan-managed-codex-compat-39215.debate.json docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md docs/plans/2026-08-24-codex-first-turn-onboarding-fold.md .release-acceptance/ox-alpha/codex-first-turn-fold-935a4f2/FIELD-ACCEPTANCE.md var/debate/plan-managed-codex-compat-39215/plan-docket.md var/debate/plan-managed-codex-compat-39215/fold-list-r1.md var/debate/plan-managed-codex-compat-39215/seat-result.schema.json var/debate/plan-managed-codex-compat-39215/seat_adapter.py", "exit_status": 0, "output": "All nine computed SHA-256 values matched the docket: dfb3950a\u2026, 5936dbbe\u2026, 28cd67c4\u2026, f15c4890\u2026, 3080ec5d\u2026, c845ca0d\u2026, 6a75ce0c\u2026, b00e642e\u2026, and 872d836b\u2026 respectively."}, {"command": "nl -ba src/debate/bridge.py | sed -n '603,629p'; nl -ba hooks/session-start | sed -n '54,66p;116,174p'; nl -ba src/debate/controller.py | sed -n '879,911p'", "exit_status": 0, "output": "bridge.py builds the filtered nested environment at lines 613-616 and has the config-home early return at 617-618. session-start lines 62-66 define quiet from DEBATE_ONBOARDING_QUIET=1, line 118 limits Codex interactive behavior to non-quiet runs, and lines 169-172 suppress the message and stop when quiet. controller.py lines 888-911 builds an allowlisted adapter environment with isolated HOME and project-local TMPDIR/TEMP/TMP."}, {"command": "rg -n '/tmp|/dev/null|PATH `debate`|seats smoke|two expected and two maximum|two expected and four maximum|fixed immutable snapshot|explicit quiet review adapter' docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "exit_status": 0, "output": "The plan explicitly scopes `seats smoke` out at lines 98-105, prohibits /tmp and PATH debate at 120-121, requires fixed-snapshot or quiet-adapter branch review at 267-270, and fixes the final field authorization at lines 275-280."}, {"command": "nl -ba .gitignore | sed -n '1,18p'; nl -ba README.md | sed -n '224,236p'; rg -n 'DEBATE_ONBOARDING_QUIET|config_home is None|OPENROUTER_API_KEY|sanitized_manifest|test_codex_quiet_attention_is_context_only' src/debate tests hooks README.md CHANGELOG.md", "exit_status": 0, "output": ".gitignore lines 8-13 ignore .mypy_cache and .pytest-tmp. README lines 227-233 identify the managed-seat claim Slice B targets. The source scan confirms the documented quiet lever, the config-home branch, credential tests, serialized-manifest handling, and existing quiet-Codex hook regression coverage."}], "status": "performed"}

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: bee22f886e30edc9b85e703a5bb2880213d36db6cfb248f8abfde7e275993136
- controller-config-sha256: f6add77a460791158f715a678d86705fc62212ee3be74067c96dae8e514ed633
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: ea617a03f99343b0521febaf39ff4aeb8cb5375e1c67e8b749a78b6e76ef008b
- docket-revision-sha256: 1ca7bffe4cf2a3f2a9a6addb997e269e89a9cb44840b6505a82f69576d8b57d2
- input-sha256: a8222e78ac6599ebf57b4552e5d8fb86586e7daf81fe00cd4e90966227bd879e
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.1
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: performed
- verification-evidence-basis: seat-declared

## MSG-10 | 2026-08-25T17:24:06+00:00 | from: opus | type: verdict | thread: plan-managed-codex-compat-3 | refs: -

## Scope and method (deliberation round)

I re-derived every claim from the immutable docket (amended plan, predecessor plan, retained `FIELD-ACCEPTANCE.md`, `collab/PROTOCOL.md`, `plan-docket.md`, `fold-list-r1.md`, the gate's `seat_adapter.py`/`seat-result.schema.json`) and from the pinned export at `935a4f2841cc103ea4a1da8f07fb58b3760c997f`: `src/debate/bridge.py`, `hooks/session-start`, `hooks/HOOK-CONTRACT.md`, `src/debate/seat_catalog.py`, `src/debate/seats.py`, `src/debate/setup.py`, `tests/test_session_start_hook.py`, `README.md`, `CHANGELOG.md`, `pyproject.toml`, `.gitignore`. I re-checked each fold against the source rather than against `fold-list-r1.md`'s claims.

Per the docket's own caveat (`plan-docket.md:35-38`) the review adapter's `DEBATE_ONBOARDING_QUIET=1` is review infrastructure only; a fresh repository-wide grep confirms the product bridge still does not set the flag at the pinned ref — the only occurrences are `hooks/session-start:59,63`, `hooks/HOOK-CONTRACT.md:57`, `CHANGELOG.md:73`, and two existing test fixtures (`tests/test_session_start_hook.py:305,321`), none under `src/debate/`.

Method limitation, unchanged and stated plainly: this seat's shell is denied in this run, so `sha256sum` could not be executed and the docket digests were not recomputed. Every finding below rests on direct reads with quoted file/line evidence, not on digest confirmation.

Verdict: **NO_PASS**, on one blocking finding with a one-clause correction.

## The five established blockers are genuinely closed

- **MSG-4 B1 (standalone smoke silence) — closed by the scope-out I expressly accepted.** §1 and invariant 3 now bound the claim to "controller-bound … launched through `run-seat`" (plan:25-28, 112-114), and §3 carries a named non-goal that identifies `seats smoke`/`setup --smoke` as a remaining separate instance, forbids `seats smoke` in the final field case, and defers it to a plan carrying its own child-environment design, tests, and call authorization (plan:96-105, 277). The underlying defect is still real at the pinned ref — `seats.smoke_seat` passes `list(seat.commands[0])` to `setup.smoke` (`seats.py:1121-1131`), which runs `subprocess.run(expanded, stdin=DEVNULL, capture_output=True, text=True, timeout=…, check=False)` with no `env=` and no `cwd=` (`setup.py:339-345`) — so what the plan now delivers is an honest scope-out rather than silence.
- **MSG-4 B2 (gate engine and gate-call authorization) — closed.** Slice D stops for a distinct owner authorization of two expected / four maximum reviewer launches, states they are separate from and do not consume the two field launches, requires the gate to be driven from the fixed immutable snapshot or an explicit quiet review adapter rather than the unfixed main-checkout bridge, and requires the chosen engine and digest to be recorded (plan:264-270). That removes the collision with `PROTOCOL.md` §4, whose production driver line is the post-merge main checkout.
- **MSG-4 B3 (unignored basetemps) — closed.** Both runs now use `.pytest-tmp/managed-codex` and `.pytest-tmp/managed-codex-full` (plan:162, 196); `.gitignore:13` ignores `.pytest-tmp/`. The two basetemps are distinct subdirectories, which matters because pytest clears the basetemp it is given. `pyproject.toml:53` sets a relative `--basetemp=.pytest-tmp` in `addopts`; the plan's explicit absolute value comes later on the command line and wins, so artifacts stay inside the ignored directory regardless of CWD.
- **MSG-4 B4 (early-return placement) — closed, and correctly placed.** Slice A now requires the flag "immediately after the filtered environment dict is built and before the `config_home is None` early return", plus a Codex-without-config-home test (plan:135-143). That is exactly the gap: `bridge.py:614-616` builds `environment`, `:617-618` returns early when `spec.config_home is None`, and `seats.add_seat` defaults `config_home: str | None = None` (`seats.py:862`), so a line after the branch would leave manually added `codex/...` seats defective while the catalogued entry (`seat_catalog.py:167,180` — `vendor="codex"`, `config_home="CODEX_HOME=.codex"`) still passed.
- **MSG-5 (`--cache-dir=/dev/null`) — closed.** Slice B now uses `.mypy_cache/managed-codex` (plan:202), project-local and ignored by `.gitignore:8`, satisfying invariant 7.
- **Non-blocking items folded.** The `repair_required` advisory context is documented (plan:76-78); the dangling "steps 1–5" sentence is replaced with explicit Slice A–C language (plan:282-284); Slice B names the correct README claim — I confirmed the target is `README.md:227` ("**Claude and Codex seats need no extra setup.**"), not the interactive first-turn paragraph; Slice C states the ready-Codex row is proved by the installed-hook direct fixture rather than a submitted prompt (plan:233-235).

## Mechanism re-verification (unchanged and still sound)

`hooks/session-start:62-66` computes `quiet` from `DEBATE_ONBOARDING_QUIET == "1"`; `:118` sets `codex_interactive = bool(os.environ.get("PLUGIN_ROOT")) and not quiet`; `:169-173` passes that as `stop_before_model`, and `_out` adds `continue: False` plus `stopReason` only then (`:44-50`). A managed Codex seat carrying the flag cannot be stopped; invariant 3 holds. Invariants 4–6 hold: `seat_environment` builds a fresh dict from `os.environ` minus `OUR_OWN_ENV = (REAL_HOME_ENV, "PYTHONPATH")` (`bridge.py:600,613-616`), nothing serialized touches it, and the vendor predicate is fed by the registry-recorded literal `vendor="codex"`.

## Blocking finding (one, unchanged from my round-2 verdict)

**B1 — Slice C step 4's env-forwarding probe is the one zero-call row whose stated mechanism can cross the inference boundary it exists to respect.**

Plan:236-237 requires "an isolated zero-call env-dump hook proving that a real Codex process forwards an inherited `DEBATE_ONBOARDING_QUIET=1` value to its plugin hook." Per `HOOK-CONTRACT.md:62-66`, Codex "does not invoke `SessionStart` merely because a prompt-free thread opens. The first submitted turn invokes it before inference." So the probe must submit a turn. But the variable under test is precisely what disarms the stop: with the flag inherited, `quiet` is true, `codex_interactive` is false (`hooks/session-start:118`), and no `continue: false`/`stopReason` is emitted (`:44-50,169-173`). A probe hook that dumps the environment and returns normally therefore lets the submitted turn proceed to the model. That is an unauthorized inference inside a slice whose contract is "Stop before any real seat call" (plan:245), inside a plan whose §1 states it does not silently authorize a model call (plan:36-39), against a remaining allowance of exactly two retry-inclusive ceiling slots (`FIELD-ACCEPTANCE.md:96-99`).

The plan already recognizes the identical hazard one bullet earlier and fixes the mechanism for the ready-Codex row ("proved by the installed-hook direct fixture, not a submitted real ready prompt, which would cross the inference boundary", plan:233-235). Leaving the adjacent, riskier row's mechanism unstated is internally inconsistent and leaves a material design choice — the only one in the zero-call proof that can spend a call — to improvisation. Note also that the 2026-08-19 spike technique the row alludes to is explicitly *not* attested for Codex: `HOOK-CONTRACT.md:51-53` records that an untrusted user hook is silently skipped in `codex exec`, so "run the dump hook headlessly" is not an available zero-call route either.

*Smallest adequate correction (either is sufficient):*
(a) State in Slice C step 4 that the probe uses a dedicated project-local probe hook in the isolated home which dumps the observed environment **and unconditionally returns `continue: false`**, so the turn is stopped by the probe hook itself independent of quiet state — the precise technique the predecessor's Slice A executed successfully (`2026-08-24-codex-first-turn-onboarding-fold.md:129-139,154-165`: one trusted `SessionStart` stopping the marker turn, an empty completed turn, zero model-output items, zero token-usage events) — and record zero model-output items and zero token-usage events as that row's acceptance criterion; or
(b) delete the row. It was my own de-risking recommendation from round 1, not a docket requirement; Slice C step 5's managed fake/trap and the final field recheck still cover the path, and dropping it costs only that the inherited-variable hop stays attested by `HOOK-CONTRACT.md` rather than re-proved here.

No redesign is implied either way. With B1 corrected, I would expect this plan to pass on the same evidence.

**On the disagreement.** The codex seat's PASS lists the "real-host env-dump" as a completed strength but does not address what stops that turn once the quiet flag under test suppresses `continue: false`. I could not find a reading of `HOOK-CONTRACT.md:51-53,62-66` plus `hooks/session-start:118,169-173` under which the row as written is guaranteed zero-call, so I maintain the finding. It is a one-clause specification gap, not a defect in the selected design, and both seats agree on everything else.

## Non-blocking observations

1. **mypy exclude anchoring under an absolute path argument.** `pyproject.toml:70` excludes `^build/` and `^var/` — relative-anchored regexes. Slice B invokes `mypy <absolute worktree path>` (plan:201-204), so a stale `build/` in the worktree would not be excluded and would fail the gate with "Duplicate module named 'debate'" (the exact failure the comment at `pyproject.toml:61-67` describes) rather than being skipped. Recommend the executor confirm the worktree carries no `build/`/`var/` before the gate, or run mypy from the worktree with `.`. Nothing else in the three gate commands is at risk: `testpaths` applies only when no path arguments are given, and `.pytest-tmp`/`.mypy_cache` are dot-directories skipped by pytest's default `norecursedirs` and mypy's crawler.
2. **The adapter option for the gate does not exercise the fix.** If Slice D's gate runs through "an explicit review adapter that sets the already documented quiet signal" (plan:267-269), the gate proves review coverage, not the bridge fix, and the first live proof of the fix remains the two-call field recheck. The plan already requires recording the chosen engine and digest; one clause naming this consequence would stop a later reader from citing gate success as field proof.
3. **Hook-trust bookkeeping is generic rather than named.** Slice C steps 1/3 say "Preserve unrelated host data", which covers `~/.codex/config.toml` `[hooks.state]` entries, but the predecessor plan named trust entries explicitly. This plan changes no hook file, so no new Codex trust prompt is expected at reinstall (`HOOK-CONTRACT.md:84-89`); saying so would let an unexpected prompt be treated as a finding rather than clicked through. If correction (a) above is taken, note that the new probe hook *will* need its own trust approval in the isolated home.
4. **Slice C has no per-row stop criteria.** Slices A and B each carry an explicit "Stop if …"; Slice C carries only "Stop before any real seat call" plus rollback. One line — any failed matrix row stops before the fake/trap and before the gate — would match the rest of the plan's discipline.
5. **Non-Codex assertion is ambient-sensitive.** The Slice A test that a Claude/Ox seat "does not see it" must control the parent environment, since an operator shell already exporting `DEBATE_ONBOARDING_QUIET` would pass it through for every vendor via `bridge.py:614-616`. That is inherited, not new (invariant 4 concerns new values), but the test must set the parent env explicitly to avoid a false green.

## Criterion-by-criterion

1. Narrowest adequate correction, ordinary Codex unweakened — **met**. Placement, vendor predicate, and interactive stop path verified against the source; the smoke path is scoped out by name rather than silently.
2. Bridge/hook tests trace the proven failure and cover non-Codex isolation, credentials, serialization, interactive stop — **met**, including the previously missing `config_home=None` case and the managed-home `repair_required` fixture.
3. Full gate, immutable install, zero-call host matrix, managed fake/trap, preservation comparison, credential scan executable and proportionate — **not met**: one matrix row's mechanism can spend a real model call as written (B1). Everything else in the slice is executable and proportionate.
4. Preserves registry, profiles, channels, worktrees, prior evidence; no `/tmp`; no PATH `debate` — **met**. Both cache/temp paths are project-local and ignored; invariant 8 and Slice C steps 1/3/6 are specific.
5. Authorization boundaries internally consistent — **met**. Zero-call implementation/install proof; gate-or-waiver before field work; separately authorized two-expected/four-maximum reviewer launches; separate ask for exactly two expected / two maximum sequential field launches, matching the retained record's two remaining ceiling slots; waiver reserved to the owner.
6. Every material design choice fixed — **not met**, on B1 alone.

Controller-Decision:
- decision: NO_PASS

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "Glob pattern=* path=<export root>  +  Glob pattern=**/* path=<docket root>/files", "exit_status": 0, "output": "Export contains 92 entries (src/debate/*.py, hooks/session-start, hooks/HOOK-CONTRACT.md, tests/*, README.md, CHANGELOG.md, pyproject.toml, .gitignore); no collab/ or var/ in the export. Docket lists exactly the nine declared files: collab/PROTOCOL.md, collab/plan-managed-codex-compat-39215.debate.json, both docs/plans files, .release-acceptance/.../FIELD-ACCEPTANCE.md, plan-docket.md, fold-list-r1.md, seat-result.schema.json, seat_adapter.py."}, {"command": "Read <docket>/docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md", "exit_status": 0, "output": "367 lines, Status: DRAFT - pending debate review, Amended after MSG-4/MSG-5. Key lines re-read fresh: 25-28 controller-bound run-seat scope; 36-39 no silent model-call authorization; 96-105 explicit smoke non-goal; 112-114 invariant 3; 120-121 invariants 7/8; 135-143 pre-early-return placement plus config_home=None test; 162/196 .pytest-tmp basetemps; 202 .mypy_cache/managed-codex; 233-235 ready-Codex direct-fixture clause; 236-237 env-dump probe row (basis of B1); 245 'Stop before any real seat call'; 264-270 gate engine plus two-expected/four-maximum reviewer authorization; 275-280 two-expected/two-maximum field ask. Both round-1 reviewer sections retained verbatim at 301-367."}, {"command": "Read <docket>/var/debate/plan-managed-codex-compat-39215/plan-docket.md", "exit_status": 0, "output": "39 lines. Criteria 1-6 read as quoted in the criterion-by-criterion section. Lines 35-38 record the caveat that the Codex review adapter's DEBATE_ONBOARDING_QUIET=1 is review infrastructure only and not evidence about the product bridge."}, {"command": "Read <export>/src/debate/bridge.py offset=594 limit=45", "exit_status": 0, "output": "600 OUR_OWN_ENV = (REAL_HOME_ENV, \"PYTHONPATH\"); 603 def seat_environment(spec); 613 real_home = os.environ.get(REAL_HOME_ENV, \"\"); 614-616 environment = {name: value for name, value in os.environ.items() if name not in OUR_OWN_ENV}; 617-618 if spec.config_home is None: return environment; 619-628 Refusal when real_home missing, then environment[variable] = str(folder). No DEBATE_ONBOARDING_QUIET in the function: the product bridge does not set the flag at the pinned ref."}, {"command": "Read <export>/hooks/session-start", "exit_status": 0, "output": "179 lines. 44-50 _out adds continue=False and stopReason only when stop_before_model; 62-66 quiet = DEBATE_ONBOARDING_QUIET == \"1\" or sdk- entrypoint; 118 codex_interactive = bool(os.environ.get(\"PLUGIN_ROOT\")) and not quiet; 124-130 ready path returns early with no stop; 169-173 _emit(_out(None if quiet else notice, base_context, stop_before_model=codex_interactive)). Confirms a quiet Codex turn is never stopped -- the basis of blocking finding B1."}, {"command": "Read <export>/hooks/HOOK-CONTRACT.md", "exit_status": 0, "output": "90 lines. 46-60: spike env/stdin dump hook; 'Codex: an UNTRUSTED user hook is silently skipped in codex exec, so no headless distinction is attested'; DEBATE_ONBOARDING_QUIET=1 is the documented automation lever. 62-70: Codex does not invoke SessionStart merely because a prompt-free thread opens; 'The first submitted turn invokes it before inference'; the stopped-turn proof recorded zero model-output items and zero token-usage events. 84-89: per-hook trust hashes under [hooks.state]; a new or changed hook does not run until approved."}, {"command": "Grep pattern=\"DEBATE_ONBOARDING_QUIET\" path=<export> -n", "exit_status": 0, "output": "hooks/session-start:59,63; CHANGELOG.md:73; hooks/HOOK-CONTRACT.md:57; tests/test_session_start_hook.py:305,321. Zero occurrences under src/debate/ -- fresh independent confirmation that the flag is hook-side and documented only, and not yet set by the product bridge."}, {"command": "Read <export>/.gitignore", "exit_status": 0, "output": "57 lines. 8 .mypy_cache/; 10 .pytest_cache/; 12 build/; 13 .pytest-tmp/; 31 .worktrees/; 37 .release-acceptance/; 47 docs/plans/; 51 var/. Both amended gate paths (.pytest-tmp/managed-codex[-full], .mypy_cache/managed-codex) fall under ignored directories: MSG-4 B3 and MSG-5 are closed."}, {"command": "Read <export>/pyproject.toml offset=45 limit=35", "exit_status": 0, "output": "51-53 [tool.pytest.ini_options] testpaths=[\"tests\"], addopts=[\"--basetemp=.pytest-tmp\"] (relative; the plan's absolute --basetemp comes later on the command line and overrides it). 58-70 [tool.mypy] strict=true, exclude=[\"^build/\", \"^var/\"] with a comment describing the 'Duplicate module named debate' failure -- basis for non-blocking observation 1."}, {"command": "Read <export>/src/debate/seats.py offset=1112 limit=25  +  Read <export>/src/debate/setup.py offset=325 limit=30", "exit_status": 0, "output": "seats.py:1121-1131 smoke_seat builds SetupSpec with commands={party: list(seat.commands[0])} and calls setup_module.smoke(spec, ...). setup.py:338-345 expanded = [...]; subprocess.run(expanded, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=spec.timeout_seconds, check=False) -- no env= and no cwd=, so the smoke child inherits the ambient environment. Confirms the defect the amended plan now scopes out by name rather than silently."}, {"command": "Grep pattern=\"def add_seat|config_home\" path=<export>/src/debate/seats.py -n", "exit_status": 0, "output": "81-82 config_home: str | None = None ('None = undeclared'); 852 def add_seat(; 862 config_home: str | None = None; 895-896 validated only when not None. Confirms manually added codex seats default to config_home=None, so the pre-early-return placement required by the amended Slice A is the correct and necessary one (MSG-4 B4 closed)."}, {"command": "Grep pattern=\"vendor=\\\"codex\\\"|isolation_argv|no_persistence_argv|config_home=\" path=<export>/src/debate/seat_catalog.py -n", "exit_status": 0, "output": "167 vendor=\"codex\"; 177 isolation_argv=(\"--ignore-user-config\", \"--ignore-rules\"); 178 no_persistence_argv=(\"--ephemeral\",); 180 config_home=\"CODEX_HOME=.codex\". Exact registry literal confirmed for the spec.vendor == 'codex' predicate, and Option 4's claim that no per-plugin hook disable is attested is confirmed."}, {"command": "Grep pattern=\"no extra setup\" -C 3 path=<export>/README.md -n", "exit_status": 0, "output": "227: '- **Claude and Codex seats need no extra setup.** The packaged catalog already records...' Confirms Slice B targets the correct README claim (fold of round-1 non-blocking item 4)."}, {"command": "Read <docket>/docs/plans/2026-08-24-codex-first-turn-onboarding-fold.md offset=110 limit=80", "exit_status": 0, "output": "Predecessor Slice A: 129-131 'Use a minimal copied hook payload to return the current Debate notice plus continue: false'; 132-136 app-server thread with one marker turn retaining evidence of no model output and zero token usage; 154-165 execution result PASS -- 'one trusted Debate SessionStart hook stopping the marker turn, an empty completed turn, zero first-turn network requests, zero model-output items, and zero token-usage events'. This is the attested zero-call probe technique that Slice C step 4 omits."}, {"command": "Read <docket>/.release-acceptance/ox-alpha/codex-first-turn-fold-935a4f2/FIELD-ACCEPTANCE.md offset=40 limit=70", "exit_status": 0, "output": "53-67 managed Codex wrapper adapter-error and the zero-call replay (registry missing, profile broken, repair_required). 87 'The feature worktree remains clean at exact 935a4f2'. 96-99 'this run consumed the three expected seat-wrapper launches and used none of the two remaining retry-inclusive ceiling slots' -- matches the plan's two-expected/two-maximum field ask and bounds the cost of an accidental probe call."}, {"command": "Read <docket>/var/debate/plan-managed-codex-compat-39215/fold-list-r1.md", "exit_status": 0, "output": "41 lines claiming five blocking folds (MSG-4 B1-B4, MSG-5 mypy) and five non-blocking folds, including 'Slice C adds an isolated zero-call env-dump proof'. Each claim was re-checked against the amended plan text and the pinned export rather than accepted; all five blocking folds verified closed, and the env-dump addition is the source of this round's single blocking finding."}], "status": "performed"}

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 1fade7c0b1ba425ab58057fa1ab3dfae055c209e3613fc1c434e5d88994e73f6
- controller-config-sha256: f6add77a460791158f715a678d86705fc62212ee3be74067c96dae8e514ed633
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: ab6f6f72a34fc909d744f304a0f5e9bcafd5fa192cfc71608f3f5db764642e00
- docket-revision-sha256: 1ca7bffe4cf2a3f2a9a6addb997e269e89a9cb44840b6505a82f69576d8b57d2
- input-sha256: 3578ec0da463553bddb30ae47e453900fbb0e9eb3ac0f57b7e5ea4f0c299899d
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: performed
- verification-evidence-basis: seat-declared

## MSG-11 | 2026-08-25T17:25:41+00:00 | from: codex | type: verdict | thread: plan-managed-codex-compat-3 | refs: -

## Review — 2026-08-24 · codex

Verdict: **NO_PASS**.

I verified the immutable docket digests and independently inspected the amended plan, predecessor plan, retained field acceptance record, protocol, and relevant pinned-export code. The five earlier blocking folds are real: the standalone smoke path is explicitly out of scope; the bridge insertion is before the `config_home is None` return and includes its regression case; pytest and mypy caches are ignored and project-local; and Slice D separately authorizes and constrains the reviewer gate. The selected `spec.vendor == "codex"` runtime-only bridge change remains the narrowest adequate repair for controller-bound `run-seat`, without weakening ordinary interactive Codex.

One blocker remains.

**B1 — Slice C step 4 does not specify a mechanism that keeps its real-Codex env-forwarding probe zero-call.** The plan requires “an isolated zero-call env-dump hook” proving that a real Codex process forwards inherited `DEBATE_ONBOARDING_QUIET=1` to its plugin hook. But the pinned contract says Codex invokes `SessionStart` only on the first submitted turn, before inference. The very signal being tested sets `quiet`; the installed hook consequently omits `continue: false` and `stopReason`. Thus, an env-dump hook that only dumps the variable (or the installed quiet hook itself) permits that submitted turn to continue to inference. The plan prohibits silently authorizing model calls during its implementation/install proof and reserves the two remaining field launches for a later explicit ask. “Zero-call” alone is an outcome, not an executable mechanism or acceptance criterion here.

Smallest adequate correction: replace Slice C step 4’s env-dump row with a requirement for an approved, dedicated project-local probe hook in the isolated home that records the inherited value and **unconditionally returns `continue: false` with a stop reason**, independent of quiet mode. Require the recorded result to show an empty completed turn, zero model-output items, and zero token-usage events. This is the same stopped-marker technique established by the predecessor plan. Alternatively, delete this non-required probe row; Slice C’s managed fake/trap and later authorized field recheck remain.

Criteria 1, 2, 4, and 5 are met. Criterion 3 is not met because this zero-call matrix row can consume a model call as written; criterion 6 is therefore not met because the stop mechanism is left to executor improvisation. No other blocking finding was established.

Non-blocking: Slice B runs mypy against an absolute worktree path while its configured excludes are anchored as `^build/` and `^var/`; the executor should confirm those directories are absent or run mypy from the worktree with `.`. The gate’s quiet-adapter option also proves gate operation, not the product bridge repair; the later managed fake/trap and authorized field case remain the substantive live proof.

Controller-Decision:
- decision: NO_PASS

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "sha256sum <all nine immutable docket files listed in the review request>", "exit_status": 0, "output": "All nine computed SHA-256 digests matched the docket values, including the amended plan (28cd67c4\u2026), predecessor plan (f15c4890\u2026), field acceptance record (3080ec5d\u2026), plan docket (c845ca0d\u2026), and fold list (6a75ce0c\u2026)."}, {"command": "nl -ba hooks/session-start | sed -n '32,180p'; nl -ba hooks/HOOK-CONTRACT.md | sed -n '44,90p'", "exit_status": 0, "output": "session-start:62-66 sets quiet from DEBATE_ONBOARDING_QUIET=1; :118 makes Codex interactive only when not quiet; :169-173 passes that state to _out; :46-50 emit continue:false/stopReason only when stopping. HOOK-CONTRACT:64-70 says Codex invokes SessionStart on the first submitted turn before inference and documents the stopped-turn zero-output/token evidence."}, {"command": "nl -ba /home/zoltan/Projects/debate/var/debate/plan-managed-codex-compat-39215/dockets/1ca7bffe4cf2a3f2a9a6addb997e269e89a9cb44840b6505a82f69576d8b57d2/files/docs/plans/2026-08-24-managed-codex-seat-onboarding-compatibility.md | sed -n '125,285p'", "exit_status": 0, "output": "Slice A requires placement before config_home early return and a no-config-home test; Slice B uses .pytest-tmp/managed-codex[-full] and .mypy_cache/managed-codex; Slice C:233-237 distinguishes the ready direct fixture but specifies only an env-dump hook for the quiet-forwarding row; :245 stops before real seat calls; Slice D:264-280 separately bounds reviewer and field authorization."}, {"command": "nl -ba src/debate/bridge.py | sed -n '600,629p'; nl -ba .gitignore | sed -n '5,14p'; nl -ba pyproject.toml | sed -n '58,70p'; nl -ba src/debate/seats.py | sed -n '852,900p;1115,1132p'; nl -ba src/debate/setup.py | sed -n '335,345p'", "exit_status": 0, "output": "bridge.py:614-618 builds the filtered environment then returns for config_home=None, confirming Slice A placement. .gitignore ignores .mypy_cache and .pytest-tmp. pyproject excludes only ^build/ and ^var/. Manual seats default config_home=None; standalone smoke calls subprocess.run without an explicit environment, supporting the plan\u2019s named scope-out."}], "status": "performed"}

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: bee22f886e30edc9b85e703a5bb2880213d36db6cfb248f8abfde7e275993136
- controller-config-sha256: f6add77a460791158f715a678d86705fc62212ee3be74067c96dae8e514ed633
- source-ref: 935a4f2841cc103ea4a1da8f07fb58b3760c997f
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: ea617a03f99343b0521febaf39ff4aeb8cb5375e1c67e8b749a78b6e76ef008b
- docket-revision-sha256: 1ca7bffe4cf2a3f2a9a6addb997e269e89a9cb44840b6505a82f69576d8b57d2
- input-sha256: 377c1fcf493e9d0d1bdd81a0ba8a8296fac553a0aaf670d6da835a0a8cd27647
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.1
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: performed
- verification-evidence-basis: seat-declared

## MSG-12 | 2026-08-25T17:25:41+00:00 | from: owner | type: close | thread: plan-managed-codex-compat-3 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-13 | 2026-08-25T19:11:04+00:00 | from: owner | type: close | thread: plan-managed-codex-cap-correction | refs: -

Owner-directed correction, 2026-08-25:

- Codex invented the “two expected / four maximum” reviewer-launch ceiling. The
  owner did not request it, MSG-4 B2 did not require it, and Debate did not supply it.
- New Debate channels use a standard 12-entry thread cap. Any future Slice D branch
  gate must persist `thread_cap: 12`; two initial reviewer launches are expected and
  managed deliberation may continue until a terminal decision or that cap.
- This closed channel's `thread_cap: 5` and its earlier references to four maximum
  remain historical evidence of the executor error. They are superseded and must not
  be reused as the operative Slice D contract.
- This correction neither authorizes Slice D nor invokes a reviewer or model.
