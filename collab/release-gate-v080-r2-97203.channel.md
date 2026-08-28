
## MSG-1 | 2026-08-27T21:51:00+00:00 | from: owner | type: review-request | thread: release-v080-r2 | refs: main@d1cd59da620c99c6b16e68ecb8e42815a0327011

Release re-gate for the v0.8.0 tag: the artifact is the pinned export at
main@d1cd59da620c99c6b16e68ecb8e42815a0327011. Prior gate release-gate-v080-06452 closed NO_PASS with six
findings (B1 ambient CLAUDE_CONFIG_DIR defeating the F19 omission; B2
CHANGELOG dated 'unreleased'; B3 stale README size claims; C1 Ox Alpha
still advertised as anonymous/zero-price post-reveal; C2 case-sensitive
credential-digest redaction; C3 README claiming result schema v2). All six
are claimed fixed at this revision.

Verify with your own fresh evidence from the export:
1. Suite: run exactly
   PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
   from the export root and quote the result line - including with an
   ambient CLAUDE_CONFIG_DIR exported, the exact condition that reddened
   the prior run.
2. Each of the six fixes: confirm the fix is real, not cosmetic
   (reproduce the original probe where one was given).
3. Version and release-document coherence: pyproject, __init__, both
   plugin manifests, CHANGELOG heading date.
4. Any NEW release-blocking defect you can establish - name every blocking
   finding, not the first.

Verdicts cite your own runs, never this request. NO_PASS requires a
reproducing command per blocking finding.


Controller-Docket-Provenance:
- topology: minimum-two-agent
- controller-config-sha256: c963f8c3adefb89618e5a87177f53c18762f50201b5afebe4554e1f106247dfa
- source-ref: d1cd59da620c99c6b16e68ecb8e42815a0327011
- review-contract: {"goal": "Establish whether the pinned v0.8.0 source tree is release-ready for the tag.", "review_contract_basis": "recorded", "review_domain": "The complete pinned export at the source ref: engine, tests, hooks, launchers, plugin manifests, README, CHANGELOG. Prior gate 06452's six findings are claimed fixed at this revision; verify the fixes rather than re-deriving them.", "review_mode": "release-gate", "stop_rule": "PASS only if your own fresh suite run is green and you find no release-blocking defect in code, manifests, or release documents; otherwise NO_PASS with bounded actionable findings. Stop at terminal agreement or the cap."}
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- docket-files: []
- profile-sha256: {"claude": "6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382", "codex": "3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-affiliated", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "073d42803d02867af7035116021655b266a4d8c945ce40749b52ce78e531f527", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "codex": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "f7354001b14cdbb8d61dc18f315b5086bbe08d0e675d9c82e0e00ce1f0e1d47a", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "codex", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "codex", "reasoning_effort": "default", "requested_model": "gpt-5.6-sol", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "0d819d86e36449192aebee03d4da2f1e5085486765c9439bb0d0ecd89fdc115e", "codex": "3be9fe48d83e917f6cb2dc68aa3501d32deddc3fb2fe84e410da22f6df13fb2f"}

## MSG-2 | 2026-08-27T22:07:37+00:00 | from: claude | type: verdict | thread: release-v080-r2 | refs: -

## Verdict

NO_PASS. The engine, manifests, packaging and test suite are release-ready on my own fresh evidence. The blocking material is confined to `CHANGELOG.md`'s `## v0.8.0` section — the exact text `release.yml` publishes verbatim as the GitHub Release body, and which ships immutably inside the sdist that a PyPI upload cannot replace for the same version. Both findings are one-edit fixes; no code change is implied.

## Blocking findings

**F1 — `CHANGELOG.md:29`: severed sentence fragment in the flagship v0.8.0 bullet.** The "Optional Ox Alpha frontier seat" bullet ends at line 28 with `general.)` and line 29 then begins mid-clause: `to attention and blocks a product open. The notice uses the binding EULA's strict ...`. Line 24-25 carries the truncated other half (`a changed revision returns onboarding attention.`). A reader cannot learn what returns to attention or what blocks a product open — and that clause describes a consent/data-policy gate, not a decorative detail. Fix: restore the single sentence (e.g. `a changed revision returns the seat to attention and blocks a product open.`) and drop the orphan.

**F2 — `CHANGELOG.md:52`: the release notes state the wrong shipped contract version.** The bullet is titled `Result schema v2 with falsifiable verification evidence`, and the string `v3` appears nowhere in `CHANGELOG.md`. But `src/debate/opening.py:1085` pins every bundled product seat to `"result_schema_version": 3`, and `README.md:398` correctly says "Every new product `verdict` uses result schema v3." The limits differ materially (v2 output 8192 scalars / 32768 bytes vs v3 32768 / 131072, per `src/debate/result_contract.py:40-57`), so an adapter author sized to the notes would size to the wrong contract. `tests/test_plugin_manifests.py:test_public_docs_name_upgrade_compatibility_and_safe_pruning` asserts `"result schema v3"` only against README+CHANGELOG *combined*, so README alone satisfies it and the CHANGELOG drift is unguarded. Fix: name v3 in the bullet, keeping v2 as the frozen legacy/custom-adapter floor.

## What I verified and could not break

- **Export integrity.** All 96 files hash-match `claude.manifest.json`; no extra, missing or altered file; `sha256` of the manifest is exactly the declared `0d819d86...`. Verification ran on a byte-identical writable copy (the export itself is read-only and untouched).
- **Fresh suite, twice.** `pytest -q` — **910 passed, 1 skipped** in the repo layout, and again **910 passed, 1 skipped** from the *extracted sdist*, which is the real test of `MANIFEST.in`'s claim that the sdist carries every file its shipped tests read (the 0.7.0 regression). The single skip is the self-declared timing-dependent race window at `tests/test_verify_record.py:331`, not a masked failure.
- **The other two CI gates.** `ruff check .` exit 0; `mypy .` strict, exit 0, 60 source files (tests included). Local ruff 0.7.1 and mypy 2.3.0 both fall inside the deliberately pinned `dev` ranges.
- **Release mechanics.** `python -m build` produces both artifacts; `protocol_template.md` is present in wheel and sdist; `PROTOCOL.md` is byte-equal to the packaged template; the sdist carries `.claude-plugin`, `.codex-plugin`, `.agents`, `hooks`, `scripts`, `skills`, `tests` and prunes `collab`/`docs`/`.github`/`.claude`/`examples` as documented.
- **Release workflow preflight, simulated.** tag `0.8.0` == pyproject == `debate.__version__`; the `## v0.8.0` anchored regex extracts a 14302-char non-empty section; 9 headings, none duplicated. So the workflow will happily publish F1 and F2 rather than catch them.
- **Manifests.** Version lockstep holds across pyproject, package, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`. `${CLAUDE_PLUGIN_ROOT}` in `hooks-codex.json` is not the bug it looks like — `HOOK-CONTRACT.md` records Codex exposing the legacy alias, and the hook falls back to its resolved path. The hook exits 0 on every path, so the `py -3 || python || python3` chain cannot double-fire on a hook error.
- **Break attempts that failed.** Double-posting refused (`not your turn (turn=b)`); unknown sender refused; a forged `## MSG-99 | ... | from: a | type: verdict` header planted inside a body refused with a precise, actionable message. Credential redaction covers the raw value and its sha256 in *both* hex cases and runs before every retention path — normal exit, timeout, and the `BaseException`/Ctrl-C path (`controller.py:1541,1566,1580-1582`). Zero third-party imports anywhere under `src/` (the "zero dependencies" claim holds by AST scan, not by trust). All relative doc links resolve except `collab/`, which the export policy excludes by design. All code fences balanced across every shipped document.

## Scope note

The review material states prior gate 06452's six findings are claimed fixed here but does not enumerate them, so I could not check them one by one; I verified the tree independently instead. I did find one corroborating artifact: `controller.py:922`, `# Both hexadecimal cases (release-gate finding, 2026-08-27)`, with the uppercase-digest redaction present and exercised.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: b2154ce0505e90e3575fe53f034f13a3fb87c04f797eecd3e3d357fc69aebb79
- phase: sealed
- captured-at: 2026-08-27T22:07:36+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: f1b43a3b8795f673871c898b4e5e804ba0cf6df6cf4a3356e06ab6a5b8b39201
- seat-declared-item-count: 16
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: c963f8c3adefb89618e5a87177f53c18762f50201b5afebe4554e1f106247dfa
- source-ref: d1cd59da620c99c6b16e68ecb8e42815a0327011
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 0d819d86e36449192aebee03d4da2f1e5085486765c9439bb0d0ecd89fdc115e
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: c974722804f71889395bc45a48d73ff80670a1c4002f4c31bd2765d4ffb5930c
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: d3443c0e0bda1ec594f034ae867c6aad4c7ef9b701d69982be78154dedd46589
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 2e007cfa0fae09236bbb0911df1ae44695e66205acbafa6d0bace5c362a0acc4
- phase-telemetry-sha256: a3954dfa28bab8748a8d118900516316b26b5e5b9891dc1d1cc4f45052c03b11
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-3 | 2026-08-27T22:07:37+00:00 | from: codex | type: verdict | thread: release-v080-r2 | refs: -

One release blocker remains.

**F1 — v0.8.0 release notes describe the wrong default result schema.** [CHANGELOG.md](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r2-97203/exports/d1cd59da620c99c6b16e68ecb8e42815a0327011/codex/CHANGELOG.md:52) headlines the bundled-product feature as “Result schema v2,” while [README.md](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r2-97203/exports/d1cd59da620c99c6b16e68ecb8e42815a0327011/codex/README.md:398) and [opening.py](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r2-97203/exports/d1cd59da620c99c6b16e68ecb8e42815a0327011/codex/src/debate/opening.py:1085) establish schema v3 for every new product verdict. [release.yml](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r2-97203/exports/d1cd59da620c99c6b16e68ecb8e42815a0327011/codex/.github/workflows/release.yml:95) publishes this CHANGELOG section verbatim. Amend the v0.8.0 entry to state that v3 is the product default and v2 is the frozen compatibility/manual-adapter surface; add a release-sync assertion for that distinction.

Verification otherwise passed using read-only-export-safe cache and basetemp locations: Ruff clean; strict Mypy clean across 60 files; pinned source and built sdist each produced 910 passed/1 documented timing skip; seven focused prior-gate regressions passed; ten version/plugin-manifest checks passed; and sdist/wheel construction succeeded.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: b2154ce0505e90e3575fe53f034f13a3fb87c04f797eecd3e3d357fc69aebb79
- phase: sealed
- captured-at: 2026-08-27T22:07:36+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: fdb519b0005da1d8e1b598fcf798832f13c933a114d830d03346b665f44418a7
- seat-declared-item-count: 10
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: c963f8c3adefb89618e5a87177f53c18762f50201b5afebe4554e1f106247dfa
- source-ref: d1cd59da620c99c6b16e68ecb8e42815a0327011
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 3be9fe48d83e917f6cb2dc68aa3501d32deddc3fb2fe84e410da22f6df13fb2f
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 63bc24c844b9e1ef6bd4f6ec0304a67739eba35bfb4dadcbb7bf3d77075b83d6
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 1b7fc0ecfd4cf219aed41db07511ca8d447ca18b53f1586de9edd3314736e0e1
- seat-stderr-sha256: 9a64c8d6afa55f863899ca1e40eb1a34fd8d9b0f16511651e468558cac40f54d
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 5302595e07c54474043c34a1c183c1e47b58a762321e06bde2181ca9f5acefd9
- phase-telemetry-sha256: 48b709046747ad9fa64300d72e62f796d74697b607dfc1c8c3d71c4e358d0df9
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-4 | 2026-08-27T22:07:38+00:00 | from: owner | type: close | thread: release-v080-r2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes. Runtime size at close: 73373762 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel release-gate-v080-r2-97203 --config /home/zoltan/Projects/debate/.debate/channels/release-gate-v080-r2-97203/watcher.json

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement
