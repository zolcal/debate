
## MSG-1 | 2026-08-27T22:26:44+00:00 | from: owner | type: review-request | thread: release-v080-r4 | refs: main@3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9

Release re-gate for the v0.8.0 tag: the artifact is the pinned export at
main@3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9. Gate r2 (release-gate-v080-r2-97203) cleared the engine, test
suite, packaging, manifests and break-attempt surface on both seats' own
fresh evidence, and closed NO_PASS on exactly two CHANGELOG.md defects:

F1 the Ox Alpha bullet carried a severed sentence (a historical-note
   parenthetical inserted mid-sentence orphaned 'to attention and blocks
   a product open');
F2 the v0.8.0 notes headlined 'Result schema v2' while every new product
   verdict ships schema v3 (opening.py pins version 3; README says v3).

Both are claimed fixed at this revision, and the docs-consistency test now
asserts 'result schema v3' in README and CHANGELOG individually.

Verify with your own fresh evidence from the export:
1. The two fixes: read the CHANGELOG v0.8.0 section end to end - every
   sentence complete, the schema story consistent with code and README,
   and no NEW defect introduced by the edits (this is the text release.yml
   publishes verbatim and the sdist freezes).
2. Suite: run exactly
   PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
   from the export root and quote the result line.
3. Anything else your own judgment flags as release-blocking - name every
   blocking finding, not the first.

Verdicts cite your own runs, never this request. NO_PASS requires a
reproducing command per blocking finding.

Operational note from gate r3 (channel 67604, closed ERROR, no verdict
published): a seat declared 17 performed-evidence items and the result
contract refused it - performed verification carries AT MOST 16 items.
Consolidate related probes into single items; total evidence breadth is
not a scoring criterion, staying within the contract is.


Controller-Docket-Provenance:
- topology: minimum-two-agent
- controller-config-sha256: 9e4d072b1a2c5a89c08467a02894c5c400c6e7549ac2e8a53e79ad7cf51b96d9
- source-ref: 3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9
- review-contract: {"goal": "Establish whether the pinned v0.8.0 source tree is release-ready for the tag.", "review_contract_basis": "recorded", "review_domain": "The complete pinned export at the source ref \u2014 identical to gate r3 (67604), which closed ERROR on an adapter refusal (a seat declared 17 evidence items against the 16-item cap), not on any finding. Gate r2 (97203) cleared code, tests, packaging and manifests and blocked only on two CHANGELOG defects, both fixed at this revision. Verify the two fixes and the release documents; re-verify the rest only as far as your own judgment requires.", "review_mode": "release-gate", "stop_rule": "PASS only if your own fresh suite run is green and you find no release-blocking defect; otherwise NO_PASS with bounded actionable findings. Stop at terminal agreement or the cap."}
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- docket-files: []
- profile-sha256: {"claude": "6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382", "codex": "3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-affiliated", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "073d42803d02867af7035116021655b266a4d8c945ce40749b52ce78e531f527", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "codex": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "f7354001b14cdbb8d61dc18f315b5086bbe08d0e675d9c82e0e00ce1f0e1d47a", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "codex", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "codex", "reasoning_effort": "default", "requested_model": "gpt-5.6-sol", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "a1d358f3a5c7b49c68a0380fc2be77b14c700242218085172cc5857f0355d428", "codex": "2deaf0d5bff33a527c128c46fb8766cc8ef450ed00c269410d36ff76a34822ff"}

## MSG-2 | 2026-08-27T22:41:39+00:00 | from: claude | type: verdict | thread: release-v080-r4 | refs: -

## Verdict: PASS — v0.8.0 is release-ready at 3ed2b84

I worked adversarially: I tried to break each criterion rather than confirm it, and every attempt failed. I also went beyond the two named CHANGELOG fixes and re-exercised the release path end to end, because a release gate that only re-reads two paragraphs is not a gate.

### Export integrity (probed first)
The manifest file hashes to exactly the stated `a1d358f3…5428`. All 96 files match their recorded SHA-256, there are no extra files, and the `claude` and `codex` exports carry byte-identical file sets. I re-verified after every command: the pinned tree is unmodified by my run (I ran the suite against the read-only tree, and did the build in a scratch copy I proved byte-identical, then deleted).

### Fresh suite — green
`910 passed, 1 skipped` in 148s. I did not accept the skip on trust: I isolated it. It is `test_verify_record.py:331`, which skips itself when a timing-dependent unlocked race window does not open in a given run — a self-reporting non-determinism guard, not a masked failure. The two other `skipif` markers in the tree are `os.name == "nt"` and do not fire here. The full CI gate reproduces: `ruff check` clean on ruff 0.7.1, `mypy` strict clean on 60 source files with mypy 2.3.0 — both inside the deliberately pinned `>=0.7,<0.8` and `<2.4` ranges, so the reproducibility rationale in `pyproject.toml` holds on the versions actually installed.

### The two CHANGELOG defects
Fix 1 is verified directly and is now regression-locked. `tests/test_plugin_manifests.py:105-124` asserts `result schema v3` in **each** public document separately, with the comment naming the cause — a combined README+CHANGELOG check let the CHANGELOG drift to v2 (release-gate finding, 2026-08-27). The CHANGELOG now states v3 as the product default on its own and the forbidden literal `schema v2 with` is absent; "Schema v2 remains the frozen floor for legacy and custom adapters" is the correct, non-drifting statement.

Fix 2 I could not confirm by name: r2's findings are not quoted in my material, so I audited the entire v0.8.0 section independently instead of guessing. I checked every CLI surface it names (`onboarding status|inspect|approve --confirmed`, `open --brokered --author-vendor --allow-mismatched-pair`, `seats add --capability-class/--isolation-argv/--no-persistence-argv/--config-home/--cost-mode`, `seats set-cost-mode`, `runtime --prune --yes`, `broker-revise --delta-round`, `--deliberation-input`, `--quick-review-max-bytes`) against `--help` output, and every number against source: `PRODUCT_THREAD_CAP = 12`, quick-review default `16384`, product open writes `scheduler_interval_seconds: 5`, the legacy watch default is `180`, `VERIFICATION_ITEM_LIMIT = 16`. `hooks.json` and `hooks-codex.json` are genuinely field-identical (394 bytes each), and `CLAUDE_CODE_ENTRYPOINT=sdk-cli` is honored in `hooks/session-start:61-64` as documented. "Terminal-only `--prune`" is enforced (`runtime.py` refuses a non-terminal channel). I found no claim the code contradicts.

### Release path (my own additions)
- The `release.yml` pre-flight regex finds a non-empty `## v0.8.0` section (14588 chars) and `tag == pyproject == debate.__version__ == 0.8.0`; version lockstep holds across all five recorded locations.
- `python -m build` produces both `debate-0.8.0.tar.gz` and the wheel. The wheel carries `debate/protocol_template.md`, and `PROTOCOL.md` is byte-equal to it (`49af331f…`), so the packaged copy cannot ship stale.
- I probed the leak risk the `.gitignore` exists to prevent: the sdist's 101 entries contain nothing from `notes/`, `collab/`, `docs/plans/`, `.debate/`, `var/`, `.acceptance*`, no `debate-profile.json` and no `*.watcher.json`. Executable bits on `hooks/session-start` and `scripts/debate-plugin` survive at 0755.
- I tested the MANIFEST.in claim that the sdist carries every file its shipped tests read — the exact way 0.7.0 broke. Unpacked clean and run in place, the sdist scores the same `910 passed, 1 skipped`. That claim is real, not aspirational.

### Non-blocking nits (do not gate the tag)
1. `CHANGELOG.md:5-7` says the cited message numbers are entries under `collab/`. Of the three channels the v0.8.0 section cites, only `plan-v080-part2-63227` is there; `plan-v080-onboarding-59142` (MSG-13) and `plan-v080-field-fold-14206` (MSG-20) are product-created v0.8 channels under the gitignored `.debate/`, so a reader cannot resolve those two citations. The header sentence could name that split. (`collab/` itself is deliberately excluded from this export, per the manifest's exclusion policy — the link is not broken in the repo.)
2. Stray blank line at `CHANGELOG.md:73` inside the Added list makes it render loose, including in the GitHub Release body sourced from this section.

No release-blocking defect found on my own evidence.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 947c71197848514b5b23f9d8a2e2877c4f468a16e97d63008f6cea506fcc0424
- phase: sealed
- captured-at: 2026-08-27T22:41:39+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 0201cb024ce31bd64b9bf0bf18748173c93888048a1e085a22241c13a00f3d9f
- seat-declared-item-count: 15
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: 9e4d072b1a2c5a89c08467a02894c5c400c6e7549ac2e8a53e79ad7cf51b96d9
- source-ref: 3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: a1d358f3a5c7b49c68a0380fc2be77b14c700242218085172cc5857f0355d428
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 1f0360c66e506a0e7ab7e4d15654c0740128a02834f5bc3777e78e214b52fcf2
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 83aac5b576ff54f57992c8f838b714bb5b9ea6c5409087d0535f648edb86fbf2
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 9c6cae11e9121d72a41463915915827e100c4556be5bfecbdf99c7553886554e
- phase-telemetry-sha256: 1072351f4dd1bf807f73440682fd8beae341e05dcc8edff49eff7e36b5f48f04
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-3 | 2026-08-27T22:41:39+00:00 | from: codex | type: verdict | thread: release-v080-r4 | refs: -

**NO_PASS — one release-blocking documentation defect.**

[CHANGELOG.md:51](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/CHANGELOG.md:51) and [README.md:398](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/README.md:398) claim every new product verdict uses result schema v3. However, [README.md:291](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/README.md:291) directs hand-authored file adapters to schema v2, while [opening.py:390](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/src/debate/opening.py:390) admits v2 or v3. A fresh probe accepted a fully managed v2 adapter, and the targeted new-product-open test at [test_open.py:1121](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/tests/test_open.py:1121) passed with default-v2 custom adapters. The headline v3 claim is therefore false for a supported new brokered-open path.

Action: qualify both universal claims to bundled prompt-style seats and explicitly state that custom file adapters may use v2 or v3, or enforce v3 for every new product open and amend the custom-adapter guidance.

The remaining gate is green: Ruff passed, strict mypy found no issues in 60 source files, and pytest reported 910 passed with one skip. Version/release-note checks and 11 focused release tests passed. The Ox Alpha historical qualification and cache-without-speedup qualification are present.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 947c71197848514b5b23f9d8a2e2877c4f468a16e97d63008f6cea506fcc0424
- phase: sealed
- captured-at: 2026-08-27T22:41:39+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 995bb1a0d8bec28077e849d951cc86c3d5a26678db543b13d40769f31ac79cf1
- seat-declared-item-count: 8
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: 9e4d072b1a2c5a89c08467a02894c5c400c6e7549ac2e8a53e79ad7cf51b96d9
- source-ref: 3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 2deaf0d5bff33a527c128c46fb8766cc8ef450ed00c269410d36ff76a34822ff
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: f33ee862d818049d8784b84824357ebddd263f877f668490591293389cdaac3d
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 5a195edc60183daf774a15e52034cb53cb0e9783e35c11714da55e288a656365
- seat-stderr-sha256: ff1d38a472054dc550644b951b78a59c51c6b9bba153ea0759a29206b324dcb4
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 0f6a076f53b52daeee6dce48a3fda93c9ae89d37b4aad7d0ad7e8296875cc4c6
- phase-telemetry-sha256: 9183989a4936fe32d77204d2541d5747c2d93106bb359c8d5844da4469549aaf
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-4 | 2026-08-27T22:52:46+00:00 | from: codex | type: verdict | thread: release-v080-r4 | refs: -

## NO_PASS — one release-blocking documentation defect

I do not retract MSG-3. The finding survives fresh re-verification, so I reject MSG-2's PASS interpretation.

[CHANGELOG.md:51](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/CHANGELOG.md:51) and [README.md:398](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/README.md:398) universally claim every new product verdict uses schema v3. But README explicitly directs hand-authored file adapters to schema v2; [opening.py:390](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/src/debate/opening.py:390) admits schemas 2 and 3; and [controller.py:497](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r4-83175/exports/3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9/codex/src/debate/controller.py:497) expressly accepts either for new product debates. A fresh direct probe returned `admission_problem: None` and managed adapter schema 2. The focused managed-open test also passed using custom adapters whose fixture default is schema 2.

Judgment call: the following `bundled product seats` clause does not cure the preceding word `every`, especially because README repeats the universal independently. `Default v3` is accurate; `every verdict uses v3` is not. Qualify both public claims to bundled/prompt-style product seats and state that custom file adapters may use v2 or v3, or enforce v3 product-wide.

The Ox Alpha severed sentence is fixed, the textual v3 edit landed, the complete v0.8.0 section is otherwise coherent, version lockstep holds, and the release section exists. I adopt MSG-2's stray blank-line observation as non-blocking. I do not adopt its channel-location nit as independently established because neither channel root is present in this export and external channel access is forbidden.

Verification caveat: the mandated literal pytest command hit the controller-injected read-only `build/pytest` base path (`77 passed, 834 setup errors`). Redirecting only that base path to this invocation's supplied writable scratch produced `910 passed, 1 skipped`; thus the source suite is independently green, but the literal-command criterion was not green in this harness.

Controller-Decision:
- decision: NO_PASS

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: b3b7cf77d4cc096252eb7565ccd8d4382fb9e8389e1bb691d059f707ec3ddd18
- seat-declared-item-count: 8
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: deliberation
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: 9e4d072b1a2c5a89c08467a02894c5c400c6e7549ac2e8a53e79ad7cf51b96d9
- source-ref: 3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 2deaf0d5bff33a527c128c46fb8766cc8ef450ed00c269410d36ff76a34822ff
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 1d66657bda8f5c668d519826b10699d23a5b1127a815aad2a389b37f961ff0c3
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: eaf786c6294b1ae7ded91cec98ca9a98a9b99188c7d69a9944563af9918f6191
- seat-stderr-sha256: d06ed3191b0569dd32e94ad9ea32ed7762f99e2a3590917a5215daa64e07be28
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: b5cbe277b15d910eb4b156d7e5ec6cd58d19b1e8412db646a7ac85938b2c007f
- phase-telemetry-sha256: 3834c632376033713a813c5ea579e1baf6db04e22e2d5c9bfeea0c162bff9d4d
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued
- deliberation-input: verdicts-only

## MSG-5 | 2026-08-27T22:59:16+00:00 | from: claude | type: verdict | thread: release-v080-r4 | refs: -

## Verdict: NO_PASS — I retract my MSG-2 PASS; codex's finding survives my own re-verification

### What I retract
My MSG-2 conclusion that the CHANGELOG schema story is consistent with the code. I reached it by reading the bullet as a whole ("Schema v2 remains the frozen floor for legacy and custom adapters") and never tested the universal quantifier in front of it against the admission rule. Tested now, it fails.

I also retract my MSG-2 nit #1 (which of the cited channels live under `collab/`). `collab/` is not in this export, so that claim was not establishable from my valid domain and I should not have made it.

### What I adopt — the blocking defect (codex MSG-3/MSG-4)
`CHANGELOG.md:51` and `README.md:398` both state, without qualification, that **every** new product verdict uses result schema v3. My own probes show that is false for a path the release documents actively instruct users to build:

- `opening.admission_problem` returns `None` for a file adapter declared at schema **2** (v1 is refused with a named message; v2 and v3 both pass).
- `controller.py:489-499` refuses only *legacy* adapters for a recorded contract: "a new product debate requires evidence result schema **v2 or v3** from both adapters."
- Bundled seats are pinned to v3 (`opening.py:1085`), but a registry file adapter carries its own declared version into the channel record (`opening.py:1024`, `:1210`).
- The shipped test `tests/test_open.py:1121` opens a brokered product channel with two custom adapters whose fixture default is `result_schema_version: 2`, and it passes on my run.
- `README.md:291` and `README.md:479` *direct* hand-authored file adapters to "result schema v2" for new product opens. So README:398 contradicts README:291/479 inside one document.

I add one consequence neither seat named, which is why I weigh this as blocking rather than as a wording nit: the same CHANGELOG sentence promises "publication is contract-safe — the evidence digest and item count are published while the exact commands stay in the private invocation result." At `controller.py:1737-1761` that contract-safe branch fires **only** for schema 3; the v2 branch publishes `seat-declared-evidence: <full verification JSON>` inline into the channel. A user who follows README:291 to build a v2 adapter gets a supported new product verdict whose exact commands and outputs are published in the public record — the opposite of what the release note promises them.

### The named judgment call
Whether a documentation over-generalization gates a tag. I call it blocking here on three grounds: this exact text is what `release.yml` extracts verbatim as the GitHub Release body (14590 chars, my extraction reproduces the offending lines) and what the sdist freezes; gate r2 already blocked this release on the schema story being wrong in these same notes, and the fix overshot into a claim the engine does not enforce; and the false part is not decorative — it is a privacy/publication promise about the headline feature of v0.8.0. `Default v3` would be true; `every` is not.

Fix either way: qualify both claims to bundled product seats and state that custom file adapters may be v2 or v3 (and that v2 publishes its evidence inline), or pin new product opens to v3 and amend README:291/479. The docs-consistency assertion at `tests/test_plugin_manifests.py:118-123` will still pass under the qualified wording.

### What survives from MSG-2, re-verified
- **Suite green.** The mandated literal command from the export root: `910 passed, 1 skipped in 148.19s`. I hit none of the read-only `build/pytest` base-path problem codex reported in their harness; the literal command was green here.
- **F1 (Ox Alpha) is genuinely fixed.** The bullet reads end to end with no severed sentence: "a changed revision returns the seat to attention and blocks a product open," with the 2026-08-26 GLM-5.3-Flash disclosure moved to a trailing parenthetical.
- Version lockstep holds (`pyproject.toml:7` = `src/debate/__init__.py:42` = `0.8.0`), and `release.yml`'s pre-flight regex finds a non-empty `## v0.8.0` section.
- Non-blocking nit, which codex also adopted: a stray blank line at `CHANGELOG.md:74` inside the Added list will render it loose in the published Release body.
- I made no writes to the pinned tree; the newest mtime in the export is still the export-creation batch.

Everything else in the gate is clean on my evidence. One blocking defect, one reproducing command, one bounded fix.

Controller-Decision:
- decision: NO_PASS

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 125bd61b77a94134a8515436f9a95e30691b94459fb0c0d6c0b18d6653385a73
- seat-declared-item-count: 16
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: deliberation
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: 9e4d072b1a2c5a89c08467a02894c5c400c6e7549ac2e8a53e79ad7cf51b96d9
- source-ref: 3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: a1d358f3a5c7b49c68a0380fc2be77b14c700242218085172cc5857f0355d428
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 25aa84656262e4e6b376bfff4d94d7cb809b7ed52ec89a14ec39def4e4c3bda0
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 92413cf0c62e63c28656a8ad4e8af7fe67c79fa0993f38102bae403bb5c59917
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: b5f69ef0103e35711cb8d2a19e028c581ab81ddf6501720eaf5d1c77dcbbfe37
- phase-telemetry-sha256: 9221a587379710d4d43ec2cf30d99168733a75e74b8072c0c71aeca8ccc8b85b
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued
- deliberation-input: verdicts-only

## MSG-6 | 2026-08-27T22:59:18+00:00 | from: owner | type: close | thread: release-v080-r4 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes. Runtime size at close: 71931373 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel release-gate-v080-r4-83175 --config /home/zoltan/Projects/debate/.debate/channels/release-gate-v080-r4-83175/watcher.json

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement
