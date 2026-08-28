
## MSG-1 | 2026-08-27T23:40:48+00:00 | from: owner | type: review-request | thread: release-v080-r6 | refs: main@e0891104111552e8d4ad4803a01f3c8cdc04cd33

Release re-gate for the v0.8.0 tag: the artifact is the pinned export at
main@e0891104111552e8d4ad4803a01f3c8cdc04cd33. Gate history on this tree: r2 (97203) cleared engine, tests,
packaging, manifests; r4 (83175) and r5 (39515) each closed NO_PASS on
result-schema precision, r5 upgrading it to a shipped-CLI defect: the
seats-add parser pinned choices=(1, 2) while opening.py admits (2, 3)
and the engine's refusal text instructs '--result-schema-version 3'.

Fixed at this revision (verify each):
1. __main__.py seats-add parser accepts 1, 2 and 3; help names v2-or-v3
   with v3 recommended. Reproduce r5's probe: register a hand-authored
   file adapter through the CLI with --result-schema-version 3 - it must
   pass the parser and reach seat validation.
2. A CLI test (tests/test_seats.py, test_cli_seats_add_accepts_result_schema_v3)
   covers that path, closing the gap that let a green suite miss it.
3. Bare-v2 prescriptions swept: README discover paragraph ('v2 or v3'),
   README contract-safe publication claim now explicitly v3-scoped with
   the frozen v2 inline publication named, and the onboarding skill's
   sites (approval declaration, engine-fact note, registration template,
   wrapper offer) recommend v3 with v2 accepted.
4. The docs-consistency test asserts per public document both the
   bundled-seat v3 rule and the custom-adapter v2-or-v3 rule.

Also run the full suite exactly as
   PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
from the export root and quote the result line, and name every further
release-blocking defect you can establish, not the first.

Operational reminder: performed verification carries AT MOST 16 evidence
items - consolidate related probes; breadth beyond the cap is a contract
refusal, not extra credit.

Verdicts cite your own runs, never this request. NO_PASS requires a
reproducing command per blocking finding.


Controller-Docket-Provenance:
- topology: minimum-two-agent
- controller-config-sha256: 8fa777eee4af67637128fcaf153ab8cdd1d74e66192b89922ae0f4b61f635c67
- source-ref: e0891104111552e8d4ad4803a01f3c8cdc04cd33
- review-contract: {"goal": "Establish whether the pinned v0.8.0 source tree is release-ready for the tag.", "review_contract_basis": "recorded", "review_domain": "The complete pinned export at the source ref. Gate r5 (39515) closed NO_PASS on the v3 custom-adapter path: the seats-add parser rejected --result-schema-version 3 while every engine layer and the engine's own refusal text admit it, plus three bare-v2 doc sites. All fixed at this revision: parser accepts (1,2,3), a CLI test registers a v3 adapter, README/CHANGELOG/onboarding-skill sites swept to v2-or-v3 with v3 recommended, README's private-publication claim v3-scoped. Verify those fixes; re-verify the rest only as far as your own judgment requires.", "review_mode": "release-gate", "stop_rule": "PASS only if your own fresh suite run is green and you find no release-blocking defect; otherwise NO_PASS with bounded actionable findings. Stop at terminal agreement or the cap."}
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- docket-files: []
- profile-sha256: {"claude": "6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382", "codex": "3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-affiliated", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "073d42803d02867af7035116021655b266a4d8c945ce40749b52ce78e531f527", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "codex": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "f7354001b14cdbb8d61dc18f315b5086bbe08d0e675d9c82e0e00ce1f0e1d47a", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "codex", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "codex", "reasoning_effort": "default", "requested_model": "gpt-5.6-sol", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "a651e65e7b62d33957521f4c30c00d1584f3d89cf8f88d60245d4f424965d363", "codex": "169db22734835bcf48761eef29c72c863e913f6ca11a7765ba4bcb914fc50ab3"}

## MSG-2 | 2026-08-27T23:50:11+00:00 | from: claude | type: verdict | thread: release-v080-r6 | refs: -

PASS - the pinned v0.8.0 tree is release-ready for the tag; all four r5 fixes verified adversarially, and my own fresh three-gate run is green.

## Fresh verification (all against the pinned export)
An installed `debate` in site-packages shadows the export, so every command pins `PYTHONPATH` to the export's `src/`. Gates: `ruff check --no-cache .` clean; `mypy --cache-dir=/dev/null .` strict clean across 60 source files; `pytest -q` **911 passed, 1 skipped**.

## The r5 findings, each probed by trying to break it
- **Parser accepts v3.** `src/debate/__main__.py:636` declares `choices=(1, 2, 3)`. Direct CLI invocation accepts 1/2/3 and rejects `0` and `4` with `invalid choice: '4' (choose from 1, 2, 3)`. The v3 custom-adapter path that closed r5 NO_PASS is open.
- **CLI test registers a v3 adapter.** `tests/test_seats.py::test_cli_seats_add_accepts_result_schema_v3` exists, cites the r5 finding, and asserts `seat.result_schema_version == 3` after a real `seats add`. It passes.
- **Doc sites swept.** Every surviving result-schema site admits v2-or-v3: `README.md:291,399,482`, `CHANGELOG.md:56`, `skills/debate-onboarding/SKILL.md:126,129,134,152`. I grepped for any residual bare-v2 requirement and found none. Remaining "version 2" hits (`PROTOCOL.md:97,146`, `examples/claude-code.md`, `examples/glm-kimi.md`) are *managed version 2* - a distinct concept - and are correct as written.
- **README private-publication claim is v3-scoped.** `README.md:398-407` scopes contract-safe publication to v3 and explicitly states the v2 seat keeps the frozen inlining publication. That matches `controller._published_body` (`controller.py:1737`), which branches on `CONTRACT_SAFE_RESULT_SCHEMA_VERSION` for the digest+item-count block and keeps the frozen v2 inlining branch.

## Engine-layer consistency (my own probes, not the author's claim)
v3 is admitted at every layer: registry load (`seats.py:294`), `add_seat` (`seats.py:940`), `opening.admission_problem` (v1 file adapter refused with the documented `NO_EVIDENCE_WRAPPER_REFUSAL` text, v2/v3 admitted), `_brokered_adapter` (custom adapter passes `seat.result_schema_version` through; bundled bridge pins `3`), `AdapterProfile` validation, and the `bridge` argparse. End-to-end through `controller._parse_result`: a v3 result under a v3 profile is accepted (`vstatus=performed`, `basis=seat-declared`); a v2-labelled result under a v3 profile is refused; injected `sender` is refused; `unable + PASS` is refused; `unable + NO_PASS` is accepted; a missing `verification` object is refused. Contract limits held under attack: 16-item ceiling, bool `exit_status` refused, empty command refused, empty output allowed by documented design, isolated surrogate refused, and v2's smaller limits genuinely frozen (1024 vs 65536 command scalars).

## Release mechanics
I simulated `release.yml`'s pre-flight exactly: `0.8.0` agrees across `pyproject.toml`, `debate.__version__`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `.codex-plugin/plugin.json`; the em-dash heading `## v0.8.0 - 2026-08-27` matches the workflow's `(?=[ \t]|$)` anchor and yields 14711 chars of notes. `src/debate/protocol_template.md` is byte-equal to `PROTOCOL.md`. `MANIFEST.in`'s prunes (`docs`, `examples`, `.github`, `.claude`) are consistent with the paths tests actually read from the repo root - the `docs/plans/...` strings in tests are synthetic paths inside temp repos, not reads of the shipped tree.

## Non-blocking observations for the next revision
1. The doc sweep is not test-pinned. `test_plugin_manifests` pins the skill's `--verification-capable --result-schema-version 3` string, but nothing pins README/CHANGELOG - the exact r5 class of drift could recur there unnoticed.
2. No test asserts that a hand-authored **v3** adapter's brokered profile carries `result_schema_version == 3`; `test_open`'s custom-adapter case uses v2. I confirmed the pass-through by direct probe.
3. `README.md:291` leads with "`2` (or `3`)" while the skill and `README.md:482` lead with 3 and say "v3 recommended" - cosmetic inconsistency only.

None of these blocks the tag.

## Process note
My `seats add` probe wrote into this invocation's own sealed HOME registry (`.../invocations/1-claude-1/home/.config/debate/seats.json`), not the operator's config; I reverted it with `seats remove custom/x` and confirmed the seat is absent. The pinned export is unmodified - all commands against it were read-only, with ruff and mypy caches disabled so neither could write into the tree.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 11f9ceb9bdfe4204211e126286c231eb8475eab3c6cfcc459dcb96eb64bd7696
- phase: sealed
- captured-at: 2026-08-27T23:50:11+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 1427e2a29496225c2ab62e6e8ad864121b78c113704865d7ad0a379c969e4fea
- seat-declared-item-count: 16
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: 8fa777eee4af67637128fcaf153ab8cdd1d74e66192b89922ae0f4b61f635c67
- source-ref: e0891104111552e8d4ad4803a01f3c8cdc04cd33
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: a651e65e7b62d33957521f4c30c00d1584f3d89cf8f88d60245d4f424965d363
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: d05a37dbe8f3c4ce59c4123cefda4e48be15c14926d2e51c188766377292c6a3
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: de72caca0e64cce8bf5ea732365f2efc7773db9a1ba0518fb4a07c05c3098604
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 64c19682a11c585efaf8a50c9b578b34abfe36be48a27cde93a65cb41eea8a76
- phase-telemetry-sha256: ecc6cef5579bd6ee1a05006b8fa6482e424a7c6bda68de907ae3f3ce8ae413f6
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-3 | 2026-08-27T23:50:11+00:00 | from: codex | type: verdict | thread: release-v080-r6 | refs: -

PASS — no release-blocking defect found.

Fresh isolated suite run against the pinned export completed with `911 passed, 1 skipped`. The skip is the documented timing-dependent unlocked-race probe. Five focused regressions passed, covering CLI v3 registration, documentation contracts, v3 private publication, and the bundled v3 default.

Inspection confirms parser choices `(1, 2, 3)`, matching storage and product-open admission. README, CHANGELOG, and onboarding now describe custom adapters as v2-or-v3 with v3 preferred/contract-safe; README scopes private evidence publication to v3 and separately documents frozen v2 behavior.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 11f9ceb9bdfe4204211e126286c231eb8475eab3c6cfcc459dcb96eb64bd7696
- phase: sealed
- captured-at: 2026-08-27T23:50:11+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: f07486aff0ff6fff096243dfdb7dee6e56a76f7db129d9dd17818f3c95266d0f
- seat-declared-item-count: 4
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: 8fa777eee4af67637128fcaf153ab8cdd1d74e66192b89922ae0f4b61f635c67
- source-ref: e0891104111552e8d4ad4803a01f3c8cdc04cd33
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 169db22734835bcf48761eef29c72c863e913f6ca11a7765ba4bcb914fc50ab3
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: b6cb54649d62c3826e63de1a74b564b795af068e19e2fb89b6042a3a2229f0f2
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 1e57f7369859322f1c0af5f1292c24fd47890bd26afe4ad44cb794696ff13da6
- seat-stderr-sha256: 9b729fb6a067ba53639d6de2f48027c90a06b87507e190f54e35501446af4834
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: cb44d11de9e32e50478ca4311f63956d81423e22b02beec8a825eca0c1e12fb7
- phase-telemetry-sha256: 39f670ca323ed9c205aeb68f78f790ed104fa38565f46b58f9e0df8f2e257b69
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-4 | 2026-08-27T23:50:12+00:00 | from: owner | type: close | thread: release-v080-r6 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes. Runtime size at close: 25304148 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel release-gate-v080-r6-08043 --config /home/zoltan/Projects/debate/.debate/channels/release-gate-v080-r6-08043/watcher.json

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
