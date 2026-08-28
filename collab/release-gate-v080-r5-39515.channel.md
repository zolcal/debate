
## MSG-1 | 2026-08-27T23:02:52+00:00 | from: owner | type: review-request | thread: release-v080-r5 | refs: main@6a0f758603bcd0b228a91912005d8421ceb93022

Release re-gate for the v0.8.0 tag: the artifact is the pinned export at
main@6a0f758603bcd0b228a91912005d8421ceb93022. Gate history on this tree: r2 (97203) cleared engine, tests,
packaging, manifests; r4 (83175, on ref 3ed2b84) closed NO_PASS by
party-vote agreement on exactly one precision defect - README and
CHANGELOG universally claimed 'every new product verdict uses result
schema v3', while a hand-authored custom file adapter may declare v2 and
a new product open admits v2 or v3 (opening.py admits (2, 3)).

Fixed at this revision: both claims are qualified to bundled seats; both
documents state a custom file adapter may declare v2 or v3 and a new
product open admits either; the onboarding passage's
'--result-schema-version 2' is widened to '2 (or 3)'.

Verify with your own fresh evidence from the export:
1. The fix: read the schema passages in README (both sites) and the
   CHANGELOG v0.8.0 bullet - the claims must now match the admission
   logic in code, with no new contradiction introduced.
2. Suite: run exactly
   PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
   from the export root and quote the result line.
3. Anything else your own judgment flags as release-blocking - name every
   blocking finding, not the first.

Operational reminder: performed verification carries AT MOST 16 evidence
items - consolidate related probes; breadth beyond the cap is a contract
refusal, not extra credit.

Verdicts cite your own runs, never this request. NO_PASS requires a
reproducing command per blocking finding.


Controller-Docket-Provenance:
- topology: minimum-two-agent
- controller-config-sha256: d3d12ce0064be7a451a7b2b9fd886f1408ba89d3aa8c1470f7dcc520501bffad
- source-ref: 6a0f758603bcd0b228a91912005d8421ceb93022
- review-contract: {"goal": "Establish whether the pinned v0.8.0 source tree is release-ready for the tag.", "review_contract_basis": "recorded", "review_domain": "The complete pinned export at the source ref. Gate r4 (83175) cleared everything except one precision defect: the universal 'every new product verdict uses result schema v3' claim in README and CHANGELOG, falsified by custom file adapters admitting v2. The claim is now qualified to bundled seats in both documents, with custom adapters stated as v2-or-v3, at this revision. Verify that fix and the release documents; re-verify the rest only as far as your own judgment requires.", "review_mode": "release-gate", "stop_rule": "PASS only if your own fresh suite run is green and you find no release-blocking defect; otherwise NO_PASS with bounded actionable findings. Stop at terminal agreement or the cap."}
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- docket-files: []
- profile-sha256: {"claude": "6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382", "codex": "3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-affiliated", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "073d42803d02867af7035116021655b266a4d8c945ce40749b52ce78e531f527", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "codex": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "f7354001b14cdbb8d61dc18f315b5086bbe08d0e675d9c82e0e00ce1f0e1d47a", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "codex", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "codex", "reasoning_effort": "default", "requested_model": "gpt-5.6-sol", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "8c5e6c15cf485f0c694eecbbebe326fa2dd0ac23edc5578de16f6f532591e012", "codex": "c37ba228292cd778f1d51fca1c8f98458170047a9b265a231d55a54c795b9df0"}

## MSG-2 | 2026-08-27T23:15:07+00:00 | from: claude | type: verdict | thread: release-v080-r5 | refs: -

## Verdict: PASS (release-ready for the v0.8.0 tag)

### 1. Fresh suite run (my own, in the pinned export)
`PYTHONPATH=src python -m pytest -q -p no:cacheprovider -rs` -> **exit 0, 910 passed, 1 skipped** in 150s. The single skip is `tests/test_verify_record.py:331` ("the unlocked race window did not open in this run (timing-dependent)") -- a legitimate self-declared timing skip, not a masked failure. Green.

### 2. The r4 defect: I attacked the corrected claim and could not break it
README.md:398-399 and CHANGELOG.md:51-57 now read "every new product verdict **from a bundled seat** uses result schema v3; a hand-authored custom file adapter may declare v2 or v3, and a new product open admits either." I probed the engine directly rather than reading for agreement:

- **Bundled path is unconditionally v3.** `opening._brokered_adapter` hard-codes `--result-schema-version 3` and `"result_schema_version": 3` for the bundled-bridge branch. I planted registry seats declaring v1, v2 and v3 and every one produced a profile and a parsed `bridge` spec of **3**. The registry field is dead on that path -- there is no input that yields a non-v3 bundled product verdict.
- **Custom file adapters really do admit both.** `admission_problem` (opening.py:390) accepts v2 and v3, and `_brokered_adapter` passes the declared version through unchanged (I got 2 and 3 respectively, argv left alone). v1 is refused with `NO_EVIDENCE_WRAPPER_REFUSAL`. So "admits either" and "legacy v1 remains runnable but is not product-admissible" are both exactly true.
- **The gate is not bypassable.** `admission_problem` is called at seating (opening.py:996), pair selection (514, 1457), suggestion filtering (476) and 807 -- not only in one place.
- **Enforcement is strict, not advisory.** `controller.py:1000` refuses on `raw["schema_version"] != profile.result_schema_version` (exact equality, both directions).
- **"v2 remains frozen, with its own smaller limits" is true.** A 2000-scalar command is accepted under v3 and refused under v2 ("exceeds 1024 Unicode scalar values"). The v2 `LIMITS` entry is untouched and `controller._published_body` keeps the frozen inline-evidence publication for v2 while v3 publishes digest + item count.
- **Cross-check:** `result_contract.contract_rule_lines(3)` reproduces the limits paragraph in this review's own prompt verbatim, confirming the shipped generator is what drove this pass.

### 3. Spot re-verification of adjacent release claims (all held)
- Version lockstep 0.8.0 across `pyproject.toml`, `src/debate/__init__.py`, both plugin manifests and the Claude marketplace; `test_release_sync.py` green.
- "A non-zero nested seat process never votes": `controller.py:1619` makes retry conditional on `returncode == 3 AND bridge_spec is not None` AND a valid sidecar -- arbitrary custom-adapter status 3 (no bridge spec) and status 2 are non-retryable, as documented.
- `.debate/` export exclusion (`controller.py:628`, policy list at 743), prune limited to `REGENERABLE_NAMES = {home, build, tmp}`, `PRODUCT_THREAD_CAP = 12`, adapter timeout ceiling 3600s, `sender` refused as controller-owned, `unable` forced to NO_PASS, 16-item cap -- all confirmed by direct probe.
- `hooks/hooks.json` and `hooks/hooks-codex.json` are byte-identical, which satisfies the "field-identical documents" claim.
- CHANGELOG v0.8.0 is the top section and dated 2026-08-27, matching the tag date.

### 4. Findings (non-blocking; all understate permissions, none overstate a guarantee)
1. **README.md:481** -- "hand-authored file adapters need that declaration plus result schema v2" contradicts README.md:399 in the same document, which correctly says v2 *or* v3. Suggest "plus result schema v2 or v3".
2. **skills/debate-onboarding/SKILL.md:133** -- "a hand-authored file adapter additionally needs declared result schema v2" has the same imprecision. More notably, the skill steers operators to register new custom wrappers at `--result-schema-version 2` (lines 129, ~145), while the engine's own refusal text (`opening.py:368`) recommends `--result-schema-version 3`. A v2 wrapper works, but it lands on the frozen inline-evidence publication path rather than the contract-safe one; the skill and the engine should recommend the same version.
3. **README.md:403** -- "What the CHANNEL publishes is contract-safe: ... with the exact commands and outputs retained in the private invocation result rather than inlined" is stated generically two sentences after v2 custom adapters are admitted, but `controller._published_body` inlines the full evidence for v2. Since "contract-safe" is literally the code's name for v3 (`CONTRACT_SAFE_RESULT_SCHEMA_VERSION = 3`) and the paragraph opens by scoping v3 to bundled seats, I read this as v3-scoped rather than false -- but it is the same shape as the r4 defect and would be worth an explicit "for v3" qualifier. CHANGELOG.md:52-55 already scopes it correctly via its colon structure.

None of these misstate a safety-relevant guarantee on the default product path, none is falsified by executable behaviour, and none blocks the tag. Recommend tagging v0.8.0 and folding items 1-3 into the next documentation pass.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: cba2bf3890783d4c473deff5c7a9936db62e5ee4d4bbd5b001bbe0975a97971c
- phase: sealed
- captured-at: 2026-08-27T23:15:07+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 850acfad2e526cb763d81ee76b6ac72d72e40caf1ec905192a128aa6e2dd89e8
- seat-declared-item-count: 11
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: d3d12ce0064be7a451a7b2b9fd886f1408ba89d3aa8c1470f7dcc520501bffad
- source-ref: 6a0f758603bcd0b228a91912005d8421ceb93022
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 8c5e6c15cf485f0c694eecbbebe326fa2dd0ac23edc5578de16f6f532591e012
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: f7a10c3202d12eb72eec659150cef9a4f032eeb7392752133ec68ad63b95dbc5
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 3ceb30de9d6ae3762a7d105e5ed66cc5a575777014f50fb6402ad470e37745da
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: d7bef1b5f3b53e6139b10f600c0f623a4b28185c7235cba5635308e9559b5af3
- phase-telemetry-sha256: a9432db8ab97f89288be63470f3d263004ea112a86fb5d93edd31ec07fea355a
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-3 | 2026-08-27T23:15:07+00:00 | from: codex | type: verdict | thread: release-v080-r5 | refs: -

NO_PASS — one release-blocking documentation contradiction remains.

The principal README and CHANGELOG passages now correctly qualify schema v3 to bundled seats and admit custom file adapters using v2 or v3. However, [README.md:481](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/README.md:481) later says hand-authored file adapters need “result schema v2.” That contradicts both the corrected passage and the implementation, which admits `(2, 3)`. Therefore the r4 precision defect is not fully resolved across the README.

Action: change that sentence to explicitly say “result schema v2 or v3,” and strengthen [tests/test_plugin_manifests.py:118](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/tests/test_plugin_manifests.py:118) so each public document must independently state both the bundled-seat v3 rule and custom-adapter v2-or-v3 compatibility.

Fresh pinned-source verification otherwise passed: 910 passed, 1 skipped; Ruff and strict mypy are green; version locations and the v0.8.0 CHANGELOG section agree. The initial pytest attempt loaded an ambient installed package and was discarded; the rerun explicitly pinned `PYTHONPATH` to this export.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: cba2bf3890783d4c473deff5c7a9936db62e5ee4d4bbd5b001bbe0975a97971c
- phase: sealed
- captured-at: 2026-08-27T23:15:07+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 6d67243ae58bc34e76466acca60d0303c507bdf8f90f9550161c687c0775b353
- seat-declared-item-count: 7
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: d3d12ce0064be7a451a7b2b9fd886f1408ba89d3aa8c1470f7dcc520501bffad
- source-ref: 6a0f758603bcd0b228a91912005d8421ceb93022
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: c37ba228292cd778f1d51fca1c8f98458170047a9b265a231d55a54c795b9df0
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 0b34b9e5f32fe9125030237be8c8c2a3754017d222e5a1f710d538f9d0e71614
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 5df3eb55ff8bffca5a09ff3c3bef3c1879f9768e8992b9acdbe2d74fd7e4999a
- seat-stderr-sha256: 980555f4fb4f7a3ee5c2ecdc6f8a24f4293e97f43f4affc8d1de919c4dc75088
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 296b7bdabe308583d12cdc3a4903607c399d06c5f2970bf5f66ec9dd8edeb657
- phase-telemetry-sha256: 04090c3535d4502e0532b0b3778143805a421e57c9ee57dcdb73817148119f36
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-4 | 2026-08-27T23:23:26+00:00 | from: codex | type: verdict | thread: release-v080-r5 | refs: -

## NO_PASS — schema-v3 compatibility remains internally contradictory

The requested suite is green: **910 passed, 1 skipped in 153.69s**. The principal corrections at [README.md:290](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/README.md:290), [README.md:398](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/README.md:398), and [CHANGELOG.md:51](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/CHANGELOG.md:51) now correctly distinguish bundled-seat v3 from custom-adapter v2-or-v3 admission. Version declarations also agree on 0.8.0.

I **do not retract** my earlier README finding: [README.md:481](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/README.md:481) still says a custom file adapter needs schema v2, contradicting the corrected passage and `(2, 3)` admission logic. Because precision about this exact compatibility boundary is the subject of the gate, I retain its release-blocking classification.

I **adopt** the other seat's onboarding finding and strengthen it with executable evidence: [skills/debate-onboarding/SKILL.md:129](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/skills/debate-onboarding/SKILL.md:129) and [skills/debate-onboarding/SKILL.md:133](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/skills/debate-onboarding/SKILL.md:133) prescribe/require v2. More seriously, the supported CLI at [src/debate/__main__.py:639](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/src/debate/__main__.py:639) only accepts choices 1 or 2. It rejects `--result-schema-version 3`, despite README recommending that declaration and [src/debate/opening.py:368](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/src/debate/opening.py:368) admitting v2/v3 and explicitly recommending the rejected v3 command. Thus the documented v3 custom-adapter registration path is not usable.

I also **adopt the factual basis** of the other seat's publication finding, but not its non-blocking classification. [README.md:403](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/README.md:403) generically says exact evidence stays private immediately after admitting v2 custom adapters, while [src/debate/controller.py:1754](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r5-39515/exports/6a0f758603bcd0b228a91912005d8421ceb93022/codex/src/debate/controller.py:1754) inlines v2 evidence. A possible v3-scoped reading is too implicit for a release already gated on this same universal-claim precision defect.

Required fix: allow schema 3 in the `seats add` parser and correct its help; change remaining README/onboarding v2-only requirements to v2-or-v3 while recommending v3 consistently; explicitly scope private digest-only publication to v3; add CLI-v3 and per-document compatibility tests; then rerun the exact suite command.

Controller-Decision:
- decision: NO_PASS

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: b8ed08cbe7cf97eb44ea10ebd2a176a11b7e7597ae3a3a199808975098d69f76
- seat-declared-item-count: 9
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: deliberation
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: d3d12ce0064be7a451a7b2b9fd886f1408ba89d3aa8c1470f7dcc520501bffad
- source-ref: 6a0f758603bcd0b228a91912005d8421ceb93022
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: c37ba228292cd778f1d51fca1c8f98458170047a9b265a231d55a54c795b9df0
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 44a1a9fcb759961a43140ac22502312109144a5aca693abdd7106ed611a7f9cb
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 110f41a4a48b8c0f853a3fe6da09ab2b72a9850ec978aba93c0e0b2885224f92
- seat-stderr-sha256: 20860f6dbf69f8620e303c4fcea4a52aed1a129fd84515f9c85c7e2f0593176e
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 01f845fe3aae00ac38c08ecfe4294959866e5c3ff94bb47d266981b136e5fb4a
- phase-telemetry-sha256: 8aff5c1b52087a4092746cb4a887170cb2404581aa5884bdf98eedd996feb38d
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued
- deliberation-input: verdicts-only

## MSG-5 | 2026-08-27T23:36:10+00:00 | from: claude | type: verdict | thread: release-v080-r5 | refs: -

## NO_PASS — I retract my prior PASS; the v3 custom-adapter path is unusable in the shipped CLI

The requested suite is green on my own fresh run: **910 passed, 1 skipped in 150.71s**, exit 0. The principal r5 corrections at README.md:398 and CHANGELOG.md:51-57 are accurate and match the `(2, 3)` admission logic. Version lockstep at 0.8.0 and the dated v0.8.0 CHANGELOG section hold. The export is read-only; I modified nothing.

### Retraction

My earlier verdict classified the residual v2/v3 prose mismatches as non-blocking. Fresh probing shows that was wrong on the decisive point: the mismatch is encoded in the shipped CLI, and the r5 fix widened the documentation *toward* a flag value the parser rejects.

### Blocking finding 1 — `seats add` rejects `--result-schema-version 3` (new; adopted and extended)

Every engine layer accepts v3 for a custom file adapter: `opening.admission_problem` admits `(2, 3)` (opening.py:390), `seats.add_seat` raises "must be 1, 2 or 3" (seats.py:941), `seats.py:294` and `controller.py:173` validate `(1, 2, 3)`. `opening.py:369` tells a refused operator verbatim to `register the wrapper with --verification-capable --result-schema-version 3`. But `__main__.py:639` pins `choices=(1, 2)`. Running the engine's own remediation instruction exits **2** with `invalid choice: '3' (choose from 1, 2)`, rejected by argparse before any seat validation; the identical command at v2 passes the parser and reaches real validation (exit 1, seat-id complaint).

This is a **new contradiction introduced by the fix under review**, which item 1 of the request explicitly asked me to check. r5 widened README.md:290-291 to ``--result-schema-version 2`` (or ``3``) — now documenting an invocation the CLI refuses. The CLI help string still carries the pre-fix universal claim in the opposite direction: "v2 is required for new product opens." No test registers a custom adapter at v3 through the CLI, which is why a green suite does not catch it.

### Blocking finding 2 — README.md:481 (adopted from the other seat)

I raised this myself as non-blocking; on re-verification I agree with its blocking classification. README.md:481 says hand-authored file adapters need "that declaration plus result schema v2", contradicting README.md:398 in the same document and the `(2, 3)` admission logic. The r4 gate closed on exactly this defect shape; an instance of it left in the release document is the defect, not residue.

### Blocking finding 3 — README.md:403 (factual basis mine, classification adopted)

Named judgment call, now resolved against my earlier reading. "the exact commands and outputs retained in the private invocation result rather than inlined" follows immediately after the clause admitting v2 custom adapters, while controller.py:1755-1760 publishes `seat-declared-evidence: <full json>` for v2 — the exact commands and outputs, inlined. A v3-scoped reading is available but the text does not state it; a release gated twice on universal-claim precision cannot rest on an implicit scope. CHANGELOG.md:52-55 scopes this correctly via its colon structure.

### Secondary (holds)

`skills/debate-onboarding/SKILL.md:129`, `:133`, `:150` prescribe v2 only. Given finding 1, v2 is currently the only value that works, so the skill is accidentally correct about the mechanism while contradicting the README and steering operators onto the frozen inline-evidence publication path.

### Required to clear

Allow `3` in the `seats add` parser and correct its help; add a test registering a custom adapter at v3 through the CLI; change README.md:481 and the SKILL.md sites to "v2 or v3" recommending v3; explicitly scope README.md:403's private-publication claim to v3; then rerun the exact suite command.

Controller-Decision:
- decision: NO_PASS

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 9a725940586977b1a76f4b3a55d2005c19125ed85861730d521415e9a602a6dc
- seat-declared-item-count: 13
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: deliberation
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: d3d12ce0064be7a451a7b2b9fd886f1408ba89d3aa8c1470f7dcc520501bffad
- source-ref: 6a0f758603bcd0b228a91912005d8421ceb93022
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 8c5e6c15cf485f0c694eecbbebe326fa2dd0ac23edc5578de16f6f532591e012
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: d686b4e804292a77c4be91587234c6ebb086d632f8f8fbcec8d572f8dda2161b
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 1819c44493e8386aa79936daed30f922cb1282d05830e73f71e3224ac3c29892
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: f215f66eb0625aa642b673cf5aef272c95bb062b0d85b6165081c731ca4ec8dc
- phase-telemetry-sha256: 32f82164b32d607863442d26f504229df49facd64c05516278d06f4a47e18f19
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued
- deliberation-input: verdicts-only

## MSG-6 | 2026-08-27T23:36:12+00:00 | from: owner | type: close | thread: release-v080-r5 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes. Runtime size at close: 60399168 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel release-gate-v080-r5-39515 --config /home/zoltan/Projects/debate/.debate/channels/release-gate-v080-r5-39515/watcher.json

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement
