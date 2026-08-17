
## MSG-1 | 2026-08-17T18:00:09+00:00 | from: owner | type: review-request | thread: branch-seat-registry-4 | refs: feature/seat-registry@a38e4819b3a84a13e366b3866235a8c4b5e6f437

REVIEW REQUEST - branch gate round 4 (fold-delta) for feature/seat-registry@a38e481, on the SUBSTITUTE codex+glm channel (owner-ruled 2026-08-17: kimi quota exhausted mid-gate; prior record seat-registry-gate-11434 MSG-82..92 carries over). GOAL: verify the declared change set (round-2 folds + tree-advisory folds + salvaged round-3 folds) resolves every prior finding and the standing criteria hold. True change set materialized as branch-fold-r4.diff. Run the full suite literally. Exhaustive enumeration applies; adversarial sealed, analytical deliberation.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 98686125b569489b19b9831549f173eb56b4d467c27ad35553a0b0be0dbbb439
- source-ref: a38e4819b3a84a13e366b3866235a8c4b5e6f437
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "f31be3a15757a0db6e66c43c80f2777bb4dd50fb7188929b15a96a0061249377", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r4.diff", "sha256": "762b44774f610dd2aac58049de9f54f731894faffb842afc056db08fbc23ffa3", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "0255baf0cad8487eb5c79826b403d66dabf61477de59b9c5948bef491e52e992", "glm": "8afe66d6b9b1d591d09e6dfa55bf3e818ed258a804540723ce320be07d2a6f63"}

## MSG-2 | 2026-08-17T18:00:17+00:00 | from: owner | type: close | thread: branch-seat-registry-4 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-3 | 2026-08-17T18:01:19+00:00 | from: owner | type: review-request | thread: branch-seat-registry-5 | refs: feature/seat-registry@a38e4819b3a84a13e366b3866235a8c4b5e6f437

REVIEW REQUEST - branch gate round 4 RERUN (the first case died on a bridge path bug under the sandboxed HOME, no votes counted) for feature/seat-registry@a38e481 on the substitute codex+glm channel. Same GOAL and docket as branch-seat-registry-4: verify the declared change set resolves every prior finding (record: seat-registry-gate-11434 MSG-82..92) and the standing criteria hold. branch-fold-r4.diff is the materialized change set. Run the full suite literally. Exhaustive enumeration applies.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 98686125b569489b19b9831549f173eb56b4d467c27ad35553a0b0be0dbbb439
- source-ref: a38e4819b3a84a13e366b3866235a8c4b5e6f437
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "f31be3a15757a0db6e66c43c80f2777bb4dd50fb7188929b15a96a0061249377", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r4.diff", "sha256": "762b44774f610dd2aac58049de9f54f731894faffb842afc056db08fbc23ffa3", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "0255baf0cad8487eb5c79826b403d66dabf61477de59b9c5948bef491e52e992", "glm": "8afe66d6b9b1d591d09e6dfa55bf3e818ed258a804540723ce320be07d2a6f63"}

## MSG-4 | 2026-08-17T18:08:38+00:00 | from: codex | type: verdict | thread: branch-seat-registry-5 | refs: -

`python -m pytest -q` run literally in the export root: `460 passed, 1 skipped in 18.66s`; however plan conformance fails on three established blockers. (1) The materialized source does not contain the docket diff’s required Kimi declared-deviation fold: `src/debate/seat_catalog.py` still says only “kimi-code CLI selects…”, while `rg -n -C 3 'DECLARED DEVIATION|kimi-agent.*forwards|binaries=("kimi"' src/debate/seat_catalog.py || true` returned only `binaries=("kimi",)`. Thus the required explanation for departing from D1’s wrapper-first seed order is absent. (2) D2’s manual-entry protection is broken: the in-memory `python - <<'PY' ... seats.discover(...)` probe returned `manual derived command after rediscovery: ['new-alpha', '{prompt}', '--effort', 'high']`, proving rediscovery overwrites a manual custom-command `@effort` seat. `src/debate/seats.py` lacks the docket diff’s required old-base-argv condition. (3) The salvaged stale-warning fold is absent: `inspect.signature(opening.pick_pair).parameters['now'].default` returned `None`, and a probe with two stale passed seats called `pick_pair` without `now` and returned `('alpha/one', 'beta/two')` without invoking confirmation. This contradicts the criterion that the clock is required and stale warnings cannot be bypassed. These are all blocking findings established in this pass.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 6a2c88af98fd7ba4525926d87ce761c7c6f4bbe5ca1978ddf5d9751daa9b98f5
- phase: sealed
- captured-at: 2026-08-17T18:08:38+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 98686125b569489b19b9831549f173eb56b4d467c27ad35553a0b0be0dbbb439
- source-ref: a38e4819b3a84a13e366b3866235a8c4b5e6f437
- source-manifest-sha256: 0255baf0cad8487eb5c79826b403d66dabf61477de59b9c5948bef491e52e992
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- input-sha256: 689ba57320a92e6903dac363fafe65c6101664b5ff781f0b2af32a94bd4dd2ec
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-5 | 2026-08-17T18:08:38+00:00 | from: glm | type: verdict | thread: branch-seat-registry-5 | refs: -

Ran in the export root (ref a38e4819b3a84a13e366b3866235a8c4b5e6f437):

1. `python -m pytest -q` -> "460 passed, 1 skipped in 18.42s". Criterion 1 (the command) passes; the blockers are in criteria 2-3 and the fold-delta rules.

2. `python -m pytest -q tests/test_open.py tests/test_seats.py --collect-only` -> "48 tests collected". Neither pinning test from the docket's materialized diff exists: no `test_discover_never_clobbers_manual_custom_effort_seat`, no `test_stale_warning_cannot_be_bypassed_without_clock`. The only diff-added test present is `test_discover_prefers_first_listed_binary` (tests/test_seats.py:406).

3. Grep over the export: `old_argv` -> zero matches anywhere; `DEVIATION|kimi-agent` in src/debate/seat_catalog.py -> zero matches.

Exhaustive blocking list (each verified against the tree and the docket's branch-fold-r4.diff, which the docket declares as the complete change-set inventory, 99f5e3b -> pinned ref, TWO commits):

B1. The artifact is NOT the declared change set. Every commit-1 hunk is present (--json on discover/check/doctor at src/debate/__main__.py:237,244,248 and the merged check/doctor block :551-563; `--cap` :282; `now=now` at the pick_pair call :511; opening.py head_resolves :77-84, stale-state logic :186-204, profile enforcement :222-229, `validate(...)` pre-write :247-261, mkdir moved after scaffold_protocol :300; seats.py smoke-record validation :75, registry_version/unreadable checks :97-114, head_resolves :275-287, slug :290-299, absent-since-discovery INFO :320-324, add_seat resolvability :383-387, slugged smoke party :503-505; setup.py ancestor-is-dir hardening :192-193; tests/test_open.py:418 match="exists"), but ALL of commit 2 is absent. The diff's `now="2026-08-17T00:00:00+00:00"` additions to the existing pick_pair tests are also absent (they pass only because the tree's `now` is optional) — the export sits between the two declared commits. Under the docket's inventory rule and fold-delta rule (a), the three salvaged round-3 codex findings have no resolving fold in the true change set.

B2. Live merge-never-clobber violation (criterion 2, registry bullet "manual entries untouched"). src/debate/seats.py:234-245: when re-discovery rewrites a catalog base's argv, EVERY seat with `effort is not None`, matching id-base, and a vendor entry with `effort_argv` gets `derived.commands[0] = argv + effort_fragment` — with no check that the seat was derived from the old base argv. A manual custom-command seat created by `seats add claude/opus@high --command "my-wrapper {prompt}"` satisfies all three conditions (add_seat stores effort="high", source="manual"), so the next discovery that moves the base binary overwrites the operator's argv. The docket's commit 2 declares exactly this fix ("manual custom-command @effort seats are never clobbered (pinned by test)"); both guard (`old_argv` prefix match) and test are missing.

B3. Live stale-warning clock bypass (criterion 2, open bullet: "stale-pass seats warn like unsmoked with pick_pair taking the clock"). src/debate/opening.py:117 declares `now: str | None = None` and :189 guards the staleness computation with `elif now is not None:` — omitting `now` skips the stale check entirely: `state` stays None, no ask, no refusal, a 105-day-old smoke pass seats silently. The salvaged round-3 finding required the clock to be REQUIRED (`now: str`, no default) and pinned by a signature test; the CLI path does pass now=now (__main__.py:511), but the required-parameter contract and its test are absent, so the finding is unresolved.

B4. The kimi catalog deviation is undeclared (commit 2 item 1). The tree's module docstring (src/debate/seat_catalog.py:16-20) documents the `-m`/config mechanics but contains no "DECLARED DEVIATION" paragraph and no mention of the `kimi-agent` wrapper forwarding only the prompt (grep: zero matches). The bare-CLI seed order therefore deviates from the plan's wrapper-first rule without the declared, verified reason.

Criterion 3 (safety) is not itself breached by the missing commit beyond B2 (the seam default is covered by the passing `test_watcher_config_seam_default_unchanged`; channel/watcher/controller law is untouched by the diff). Criterion 1 passes; criteria 2-3 and fold-delta rule (a) fail on B1-B4. Verdict: NO_PASS.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 6a2c88af98fd7ba4525926d87ce761c7c6f4bbe5ca1978ddf5d9751daa9b98f5
- phase: sealed
- captured-at: 2026-08-17T18:05:42+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 98686125b569489b19b9831549f173eb56b4d467c27ad35553a0b0be0dbbb439
- source-ref: a38e4819b3a84a13e366b3866235a8c4b5e6f437
- source-manifest-sha256: 8afe66d6b9b1d591d09e6dfa55bf3e818ed258a804540723ce320be07d2a6f63
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- input-sha256: 9218d813b2659c7172bb33418520a762f90f2f4b3aeedf45d5efe52eb906571a
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-6 | 2026-08-17T18:08:38+00:00 | from: owner | type: close | thread: branch-seat-registry-5 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-7 | 2026-08-17T18:09:20+00:00 | from: owner | type: review-request | thread: branch-seat-registry-6 | refs: feature/seat-registry@1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc

REVIEW REQUEST - branch gate round 5 for feature/seat-registry@1ced5f8. The prior case (branch-seat-registry-5, NO_PASS) caught an AUTHOR PINNING ERROR: the export was pinned between the two declared commits, so commit 2 (the salvaged round-3 folds) was absent from the reviewed tree - both seats correctly identified it. The export is now pinned at the true head containing BOTH declared commits; the docket, declared change set, and branch-fold-r4.diff are unchanged and now match the export. Same GOAL and criteria. Run the full suite literally. Exhaustive enumeration applies.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 3aee88eb8c786c37009808d60153e8b3e72a6034fdcad15254a2e67ae5b4e720
- source-ref: 1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "f31be3a15757a0db6e66c43c80f2777bb4dd50fb7188929b15a96a0061249377", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r4.diff", "sha256": "762b44774f610dd2aac58049de9f54f731894faffb842afc056db08fbc23ffa3", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "4c5693f971b959ba799addd6132e4d7348972b6717fc9c2993215a92879b92bb", "glm": "ee451a248cdac0bcbac21a614b94f271af7e36e7c3e2e2516dd98a5a3cf3b226"}

## MSG-8 | 2026-08-17T18:19:04+00:00 | from: codex | type: verdict | thread: branch-seat-registry-6 | refs: -

Fresh required verification in the export root: `python -m pytest -q` → `462 passed, 1 skipped in 18.49s`.

Blocking finding (exhaustive): manual custom-command `@effort` seats can still be clobbered on rediscovery. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc/codex/src/debate/seats.py:235-251` treats any manual derived seat whose argv merely starts with the old base argv as auto-derived, then replaces it. This contradicts the docket’s required fold that manual custom-command `@effort` seats are never clobbered.

Fresh adversarial reproduction run in the export root: `python -c 'from debate import seats; r = seats.Registry(); r, _ = seats.discover(r, which=lambda name: "/old/claude" if name == "claude" else None, now="t0"); base = r.seats["claude/opus"].commands[0]; r.seats["claude/opus@high"] = seats.Seat("claude/opus@high", "claude", "opus", "high", [base + ["--effort", "high", "--manual-wrapper-flag"]], "manual", True, None); r, diff = seats.discover(r, which=lambda name: "/new/claude" if name == "claude" else None, now="t1"); print(diff); print(r.seats["claude/opus@high"].commands[0])'` → `['~ claude/opus@high re-derived from the new base argv']` and `['/new/claude', '-p', '{prompt}', '--model', 'opus', '--effort', 'high']`; the manual `--manual-wrapper-flag` was removed.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 5fa5e650e8ed7d90962c4f2fd486452984de597fd42c2d3e8196b866c6f74f61
- phase: sealed
- captured-at: 2026-08-17T18:12:51+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 3aee88eb8c786c37009808d60153e8b3e72a6034fdcad15254a2e67ae5b4e720
- source-ref: 1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc
- source-manifest-sha256: 4c5693f971b959ba799addd6132e4d7348972b6717fc9c2993215a92879b92bb
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- input-sha256: 77c8c7c1a46ba75e0568d592ba5804432a6fd669be2464d378b2dca629311210
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-9 | 2026-08-17T18:19:04+00:00 | from: glm | type: verdict | thread: branch-seat-registry-6 | refs: -

VERDICT: PASS.

1) Fresh command (docket criterion 1), run literally in the export root (/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc/glm):
`python -m pytest -q` -> "462 passed, 1 skipped in 18.76s" (repeated literally: same, 19.48s). The one skip was identified with `python -m pytest -q -rs` -> "SKIPPED [1] tests/test_verify_record.py:331: the unlocked race window did not open in this run (timing-dependent)" — a pre-existing timing guard in verify-record law this change set does not touch; zero failures.

2) Plan conformance (criterion 2), judged against the docket-materialized plan and diff by direct tree inspection:
- catalog (D1): single-seat rule statically enforced — tests/test_seats.py:43-51 asserts empty submodel_argv -> exactly one submodel, and the data honors it (src/debate/seat_catalog.py: codex/glm/deepseek each one pin); grok's omission is documented as unverifiable in the module docstring (seat_catalog.py:30-31); the kimi bare-CLI deviation is a DECLARED deviation with its verified reason (seat_catalog.py:16-26) — round-3 finding (1) resolved.
- registry (D2/ruling 4): Seat.commands is a list of endpoint argvs; selection is first-listed everywhere I could find a consumer (seats.py:330, opening.py:79/311, seats.py:451, seats.py:515); every write is credential-screened (seats.py:148-176 screen_credentials inside save_registry, also called up front in open_debate); discovery merge-never-clobbers — absent-marked, never deleted, manual entries untouched (seats.py:228-256).
- freshness (D3/H1): check() fails ONLY on unresolvable binary or failed smoke; never-smoked and absent-since-discovery are INFO, stale is WARN (seats.py:317-347); CLI returns 3 iff fails, both --json and text paths (__main__.py:551-570); tests test_seats.py:230-274 and 363-386 pin the exit semantics; the upgrade trigger re-scans scan-only (seats.py:350-362).
- dispatch (B2): `seats` and `open` join init/migrate in the no-discovery set (__main__.py:482).
- open (D4): last-pair default keyed by the git toplevel via channel._derived_project (opening.py:52-54); --yes covers only the unsmoked/stale warning, the identity guard runs after it unconditionally (opening.py:193-205); identical SELECTED argv refused always, vendor/submodel identity only via --allow-identical-seats, effort ignored (opening.py:88-106); shared-vendor party names slugified (opening.py:234-242, pinned by test_open.py:231-256); ALL validation precedes the first write and runs through the channel_config seam on _watcher_config (opening.py:221-293; seam at __main__.py:73-77,133-134, omitted -> disk read exactly as before, pinned by test_open.py:48-56); setup.apply is never imported by opening.py (opening.py:22) and the defaults cache is byte-untouched (test_open.py:281-297); the provenance block records seat id, effort incl. null, exact command, smoke_at (opening.py:305-320). Round-3 finding (3) resolved: pick_pair's clock is a required parameter, pinned by test_open.py:495-501.
- profile (D2.5/ruling 5): committable debate-profile.json allowlist, fail-closed on malformed/version/unknown-id/empty with the offender named (seats.py:553-597), opt-in per project, picker restricted and enforced at both the pick_pair and open_debate layers (opening.py:124-127, 222-229; tests test_open.py:337-403).

3) Safety (criterion 3): the seam's default path is byte-identical (channel_config=None -> channel.load_config, __main__.py:133-134, existing watcher/config suites untouched and green); the dispatch guard changes nothing for commands outside ("init","migrate","seats","open"); branch-fold-r4.diff contains no hunks in channel.py, watcher.py, or controller.py, so channel/watcher/broker law is untouched by this change set.

4) Fold-delta (R3): (a) every prior finding I could trace has its resolving fold in the tree — round-2/D3 surface (--json on discover/check/doctor, open --cap, __main__.py:234-248,282-283,609-615), stale-pass warn with pick_pair taking the clock (opening.py:178-204), one resolvability definition head_resolves across add/check/pick (seats.py:280-292 used at seats.py:331,388 and opening.py:80,153), open composing setup.validate with the state mkdir moved to the write phase plus the ancestor-is-dir hardening (opening.py:247-261,300; setup.py:187-196), registry version/smoke-result validation and missing-vs-unreadable split (seats.py:75,99-114), slugged smoke party names (seats.py:508-510), derived @effort re-derivation (seats.py:232-250, pinned by test_seats-side test_discover_never_clobbers_manual_custom_effort_seat, test_open.py:504-526 — round-3 finding (2) resolved), absent-since-discovery INFO (seats.py:325-329), resolvable-only interactive listing (opening.py:149-154), precise catalog notes (seat_catalog.py:66), first-listed-binary preference test (test_seats.py:406-429). (b) The reverse holds: I enumerated every hunk of the materialized diff across its seven files and each traces to a declared fold in the docket's change set; I also verified the pre-states are absent from the tree (grep for "--thread-cap", "already exists; a freshly minted", the old inline resolvability branches, the old OSError->empty-registry swallow: no matches). (c) Coherence sweep found no contradiction: the new code references only existing machinery, and the full suite is green.

Exhaustive blocking list per the R2 enumeration rule: none establishable. Two sub-threshold observations, on the record and non-blocking: setup.validate keeps its own inline resolvability check rather than calling head_resolves (semantically the same is_file+X_OK rule; the docket scopes the ONE-definition claim to add/check/pick, which all literally call seats.head_resolves); and `open`'s existing-config refusal wording changed to setup.validate's ("exists...") with the test updated — the same refusal, declared under the validate-composition fold. Files checked: src/debate/{seats,opening,seat_catalog,setup,__main__,channel}.py, tests/{test_seats,test_open}.py, README.md (seats/open/profile sections present), plus the six docket files.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 5fa5e650e8ed7d90962c4f2fd486452984de597fd42c2d3e8196b866c6f74f61
- phase: sealed
- captured-at: 2026-08-17T18:19:04+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 3aee88eb8c786c37009808d60153e8b3e72a6034fdcad15254a2e67ae5b4e720
- source-ref: 1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc
- source-manifest-sha256: ee451a248cdac0bcbac21a614b94f271af7e36e7c3e2e2516dd98a5a3cf3b226
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- input-sha256: 52207d6806de95904221144b77a20021241e4e1524dfca53a57c2f18cb5161fb
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-10 | 2026-08-17T18:23:52+00:00 | from: codex | type: verdict | thread: branch-seat-registry-6 | refs: -

Fresh required command in the export root: `python -m pytest -q` → `462 passed, 1 skipped in 18.54s`.

Blocking finding (exhaustive): I retain my sealed finding after re-verification. The required round-3 fold says manual custom-command `@effort` seats are never clobbered, but `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc/codex/src/debate/seats.py:235-250` identifies a supposedly derived seat solely by old-base argv prefix, without distinguishing a manual command. Fresh public-API reproduction: `python -c 'from debate import seats; r = seats.Registry(); r, _ = seats.discover(r, which=lambda name: "/bin/echo" if name == "claude" else None, now="t0"); seats.add_seat(r, "claude/opus@high", "/bin/echo -p {prompt} --model opus --effort high --manual-wrapper-flag"); r, diff = seats.discover(r, which=lambda name: "/bin/true" if name == "claude" else None, now="t1"); print(diff); print(r.seats["claude/opus@high"].source, r.seats["claude/opus@high"].commands[0])'` → `['~ claude/opus@high re-derived from the new base argv']` and `manual ['/bin/true', '-p', '{prompt}', '--model', 'opus', '--effort', 'high']`; the manual flag is lost.

Judgment on the opposing PASS: its cited test at `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc/codex/tests/test_open.py:504-526` covers only a wholly different executable, so it does not establish the required never-clobber guarantee. The suite passing does not cure this plan-conformance failure.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 3aee88eb8c786c37009808d60153e8b3e72a6034fdcad15254a2e67ae5b4e720
- source-ref: 1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc
- source-manifest-sha256: 4c5693f971b959ba799addd6132e4d7348972b6717fc9c2993215a92879b92bb
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- input-sha256: 404fe5e5d99361603d40e64b6c85787dc8cb5d2879b07b41b70a9e9ae91fcf40
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-11 | 2026-08-17T18:30:03+00:00 | from: glm | type: verdict | thread: branch-seat-registry-6 | refs: -

VERDICT: NO_PASS. I retract my sealed PASS and adopt the opponent's blocking finding; on re-verification against fresh evidence in MY export it survives, and my own sealed evidence for "manual entries untouched" does not.

1) Fresh docket command, run literally in the export root (/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc/glm): `python -m pytest -q` -> "462 passed, 1 skipped in 20.30s". Criterion 1 holds; the suite does not cure the plan-conformance failure below.

2) Blocking finding (exhaustive; the only one establishable). The required commit-2 fold (2) — "derived-refresh re-derives ONLY seats whose argv derives from the old base — manual custom-command @effort seats are never clobbered (pinned by test)" — is violated, as is standing criterion D2 ("merge-never-clobber discovery ... manual entries untouched"). In src/debate/seats.py:236-250, when a catalog seat's base argv changes, any seat with a non-None effort whose id-base matches and whose commands[0] PREFIX-MATCHES the old base argv (seats.py:244) is overwritten wholesale: `derived.commands[0] = argv + effort_fragment`. The guard never consults the creation path; and it cannot consult `source`, because add_effort_seat itself stores derived seats as source="manual" (seats.py:460). A manual seat created via the public `seats add` path (add_seat, seats.py:365-419 — it accepts vendor/submodel@effort ids, seats.py:409-414) whose command extends the base spelling is therefore misclassified as derived and silently rewritten: its operator-authored argv tail is destroyed. Static trace, every step verified in my export: catalog claude entry (seat_catalog.py:58-67: invocation `{binary} -p {prompt}`, submodel_argv `--model {submodel}`, effort_argv `--effort {effort}`) -> `_assemble_argv` (seats.py:179-181) yields old base argv [bin, "-p", "{prompt}", "--model", "opus"]; `split_argv` is plain shlex (setup.py:75-79); so `seats.add_seat(r, "claude/opus@high", "<old-bin> -p {prompt} --model opus --effort high --manual-wrapper-flag")` passes all validation (placeholder, absolute executable head via head_resolves, secret screen) and stores commands[0] = old_argv + ["--effort", "high", "--manual-wrapper-flag"]; on rediscovery with a changed binary (or any catalog argv change), base_changed fires (seats.py:233), the prefix test at seats.py:244 matches, and commands[0] is replaced by new_base + ["--effort", "high"] — the manual tail is gone, with diff line "~ claude/opus@high re-derived from the new base argv". Materiality: the version-mismatch upgrade trigger re-runs this discover (seats.py:358-362), so every tool upgrade or PATH change re-executes it; and add_effort_seat's own refusal message directs operators to `seats add --command` for effort variants (seats.py:443-445), i.e. the tool routes operators into exactly the clobbered path. The code contradicts its own asserted invariants: the inline comment "a manual custom command is the operator's own and is never clobbered" (seats.py:241-243), discover's docstring "never touches a manual entry" (seats.py:195-196), and "the registry never clobbers an existing seat" (seats.py:433).

3) Why my sealed PASS was wrong, on the record. My sealed verdict cited the pinning test as resolving round-3 finding (2). I re-read it: tests/test_open.py:504-526 (`test_discover_never_clobbers_manual_custom_effort_seat`, fresh isolated run `python -m pytest -q tests/test_open.py::test_discover_never_clobbers_manual_custom_effort_seat tests/test_seats.py -v --no-header` -> "28 passed") creates the manual seat with a WHOLLY DIFFERENT executable (`echo-agent` vs `claude`), so the prefix test at seats.py:244 fails and the seat trivially survives. The test passes while the guarantee it names in its own assertion message ("a manual custom-command @effort seat is the operator's own") is false for any manual command sharing the base prefix. Codex's characterization of the test is accurate; their dynamic reproduction (MSG-10) matches my static trace line-for-line at the same ref.

4) Judgment calls, named explicitly. (a) I read "manual custom-command @effort seats" as the class defined by CREATION PATH (`seats add`, source="manual"), not by argv shape — the docket's own D2 clause "manual entries untouched" is unconditional and the code's comments assert the absolute guarantee. (b) I considered the narrow reading — the fold's first clause ("re-derives ONLY seats whose argv derives from the old base") is implemented literally, and derived/manual are genuinely indistinguishable by `source` — but rejected it as the verdict basis: the prefix check is strictly weaker than even the exact "base + effort_argv" derived shape, so it over-matches; the sanctioned-operand path point (2) makes the overlap realistic rather than contrived; and a fold "pinned by test" whose test silently narrows the guarantee to different-head commands does not establish the docketed guarantee. (c) Provenance note: my Bash allowlist is pytest-only — a `python -c` dynamic reproduction was denied by the harness — so the reproduction above is an exhaustive static trace of my own export's code (the opponent's dynamic run at the same ref agrees); the pytest commands cited are the ones I ran.

5) Exhaustive enumeration, remainder: fresh suite green (criterion 1); nothing in this finding implicates the other sealed citations — D1 catalog single-seat rule, D3 freshness exit semantics, B2 dispatch guard, D4 open/validation-before-write/identity-guard/--yes scope, D2.5 profile fail-closed, and the fold-delta reverse direction all stand as previously verified against the same tree; my sealed verdict's clause "discovery ... manual entries untouched (seats.py:228-256)" is RETRACTED — it is the blocker above. Blocking list: exactly one finding. Files checked this pass: src/debate/{seats,seat_catalog,setup}.py (discovery, add/derive/remove, catalog, split_argv), tests/{test_open.py:495-526, test_seats.py}, plus the docket's branch-docket.md and branch-fold-r4.diff context.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 3aee88eb8c786c37009808d60153e8b3e72a6034fdcad15254a2e67ae5b4e720
- source-ref: 1ced5f818c782fd7ed507bab8b0c1fbbad8dfbcc
- source-manifest-sha256: ee451a248cdac0bcbac21a614b94f271af7e36e7c3e2e2516dd98a5a3cf3b226
- docket-revision-sha256: 10199de0268dac4d7e2f1bec201933f36a81387c6ae32e807cae1727baef25e0
- input-sha256: f8363c636de79f1f47976bfc84433fc78a6e2847fdba56f5a02a9d0feae91c0e
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-12 | 2026-08-17T18:30:03+00:00 | from: owner | type: close | thread: branch-seat-registry-6 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-13 | 2026-08-17T18:32:59+00:00 | from: owner | type: review-request | thread: branch-seat-registry-7 | refs: feature/seat-registry@a4cb5362194cccee6b0d4726ea4f251e3db6541c

REVIEW REQUEST - branch gate round 6 (fold-delta) for feature/seat-registry@a4cb536. GOAL: verify the single fold (exact-shape derived-refresh guard, pinned by the reproduction test) resolves the round-5 converged finding; everything else stands per MSG-8/9/11 unless implicated. True change set materialized as branch-fold-r5.diff. Run the full suite literally. Exhaustive enumeration applies.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 3a554e29b32d636696c3ef7a482a6224a547725b4e7d14b94aa473d319cb84b9
- source-ref: a4cb5362194cccee6b0d4726ea4f251e3db6541c
- docket-revision-sha256: aa2acf3e40864deb7537fbbffd0a1e09c7e5089f8f219550edc6c472985ff857
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "9f412065a8529a7e05011ab15b1ca1cbd1b1a86bbcc853220e5ab5d6df4c578c", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r5.diff", "sha256": "ab7f0b4aa0f93f79b286ed6cab562f9d676fd6b0af32a0df623084c71e4a1ecc", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "4770b54e50626da854113147f62b7276f6567d839e38b08125549dd5ff9cbe1b", "glm": "d7f5a5a5ff90b0f1ed4f3a6eb4575ef7cf95694469ae7096425314155e51a670"}

## MSG-14 | 2026-08-17T18:41:51+00:00 | from: codex | type: verdict | thread: branch-seat-registry-7 | refs: -

Exhaustive blockers established:
1. The pinned export does not contain docket-required tracked file `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/a4cb5362194cccee6b0d4726ea4f251e3db6541c/codex/collab/PROTOCOL.md` (docket SHA-256 `1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e`). I ran `if test -e collab/PROTOCOL.md; then sha256sum collab/PROTOCOL.md; else printf 'MISSING collab/PROTOCOL.md\n'; fi; sha256sum PROTOCOL.md; find collab -maxdepth 1 -type f -print 2>&1 || true`; result: `MISSING collab/PROTOCOL.md`, root `PROTOCOL.md` SHA-256 `26ead49eb64bc0e17b4a2b6d50052c4ccda0a317eb556d65ab7a9cf989e3703a`, and `find: ‘collab’: No such file or directory`. Thus the complete pinned source export cannot satisfy the docket’s tracked-file binding.
2. D3 requires a version-mismatch re-scan to stamp the new registry version. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/a4cb5362194cccee6b0d4726ea4f251e3db6541c/codex/src/debate/__main__.py` saves only when `upgrade_diff` is nonempty, so a successful empty re-scan loses the new stamp. I ran `python -c 'from debate import seats; from debate.__main__ import main; registry = seats.Registry(tool_version="obsolete"); saved = []; original_catalog = seats.CATALOG; original_load = seats.load_registry; original_save = seats.save_registry; seats.CATALOG = (); seats.load_registry = lambda: registry; seats.save_registry = lambda value: saved.append(value.tool_version); rc = main(["seats", "list"]); print({"exit": rc, "tool_version_after_scan": registry.tool_version, "save_calls": saved}); seats.CATALOG = original_catalog; seats.load_registry = original_load; seats.save_registry = original_save'`; result: `{'exit': 0, 'tool_version_after_scan': '0.6.0', 'save_calls': []}`. The update exists only in memory and is not persisted, so the next invocation repeats the mismatch instead of recording the required stamp.

Required verification was also run literally in the export root: `python -m pytest -q` -> `463 passed, 1 skipped in 18.86s`. That passing suite does not cure the two blockers.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 464b876f1354d402e28d2e62a6405a541f57b4f07b5addb8c7eaecb65e332527
- phase: sealed
- captured-at: 2026-08-17T18:41:51+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 3a554e29b32d636696c3ef7a482a6224a547725b4e7d14b94aa473d319cb84b9
- source-ref: a4cb5362194cccee6b0d4726ea4f251e3db6541c
- source-manifest-sha256: 4770b54e50626da854113147f62b7276f6567d839e38b08125549dd5ff9cbe1b
- docket-revision-sha256: aa2acf3e40864deb7537fbbffd0a1e09c7e5089f8f219550edc6c472985ff857
- input-sha256: 6108d8f0cc3870a7b31b8872a3f45d6af9c31175e5f9477985347ed0721c41f0
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-15 | 2026-08-17T18:41:51+00:00 | from: glm | type: verdict | thread: branch-seat-registry-7 | refs: -

Criterion 1 (command): ran `python -m pytest -q` literally in the export root (cwd = .../exports/a4cb5362194cccee6b0d4726ea4f251e3db6541c/glm), no prefixes/suffixes/pipes. Result: "463 passed, 1 skipped in 19.13s". A follow-up `python -m pytest -q -rs` (diagnostic only) identifies the skip as tests/test_verify_record.py:331 "the unlocked race window did not open in this run (timing-dependent)" — a designed probabilistic skip in pre-existing lock-race machinery, untouched by this fold; zero failures.

Round-5 fold (the delta under review): src/debate/seats.py:236-253 now re-derives an @effort seat ONLY when `derived.commands[0] == old_argv + fragment` (exact equality; `if derived.commands[0] != old_argv + fragment: continue`); the old prefix match (`derived.commands[0][: len(old_argv)] == old_argv`) is gone, and grep confirms no other `[: len(` / prefix-match site exists in src/debate. The manual seat is further protected by the `existing.source == "catalog"` gate (seats.py:228) so discovery never rewrites a manual base. The materialized branch-fold-r5.diff matches the source exactly: the seats.py hunk's post-state is verbatim seats.py:236-253 and the test hunk is verbatim tests/test_open.py:529-561, which carries codex's exact reproduction (base + ["--effort","high","--manual-wrapper-flag"] preserved, commands[0][0] still the old binary, seat untouched entirely) plus the true-derivation contrast (claude/opus@low re-derived to the new binary). I attempted to break the guard (catalog effort_argv drift, multi-option derived seats, manual seats shadowing catalog ids) — every path fails safe: mismatch → never clobbered; only commands[0] is rewritten with commands[1:] preserved.

Criterion 2 (plan conformance), each probed against code plus the green suite:
- D1 catalog: single-seat rule statically enforced — tests/test_seats.py:43-51 asserts empty submodel_argv ⇒ exactly one submodel; codex/glm/deepseek entries comply (seat_catalog.py). Grok's omission is documented in the module docstring (seat_catalog.py:30-31) as unverifiable — the declared no-guessing form.
- D2/ruling 4: commands validated as one-or-more non-empty argv lists (seats.py:64-71); selection is first-listed everywhere (discover, add_effort_seat:454, smoke_seat:518, check:333, opening._seatable/open_debate:253-255); save_registry screens every argv with SECRET_PATTERN before writing (seats.py:148-176) and add_seat screens at entry (396-401); discovery marks vanished catalog seats present:false, deletes nothing, never touches manual entries (seats.py:254-259, 228; test_rediscover_marks_absent_never_deletes).
- D3/H1: check() emits FAIL only for a present seat whose head no longer resolves or a smoke that ran and failed (seats.py:334-343); absent→INFO, never-smoked→INFO, stale>30d→WARN; `__main__` returns 3 iff fails on both text and --json paths and ends with the re-discovery offer; ensure_current re-runs discover only (never smoke) on version mismatch and stamps the version (seats.py:353-365).
- B2: __main__.py:482 excludes ("init","migrate","seats","open") from channel discovery; asserted from a multi-channel CWD (test_cli_seats_discover_and_list) and a multi-channel root (test_cli_open_on_multichannel_root).
- D4: pick_pair defaults from last_pair keyed by project_key = channel._derived_project (git toplevel; H4) with global "" fallback, unseatable/out-of-allowlist defaults dropped, --yes-without-default refuses (opening.py:129-147); --yes covers the unsmoked/stale warning (195-196) but never the identity guard — same vendor/submodel refused with effort ignored, --allow-identical-seats is the only key, identical SELECTED argv refuses even with the flag, literal same seat refuses always (opening.py:88-106; test_pick_pair_identity_guard); shared-vendor party names slugify dot/effort-free (codex-gpt-5-6-sol-low/high, opening.py:57-65,234-242; test_open_debate_shared_vendor_party_names_are_slugs); ALL validation precedes the first target write and the loader round-trip goes through the `channel_config` seam on _watcher_config (__main__.py:73-77,130-134; opening.py:285-293) — three distinct forced-failure tests assert the target root stays empty; setup.apply is never called (grep: only referenced in comments) and the defaults cache is byte-untouched (test_open_debate_leaves_setup_defaults_cache_untouched; store_defaults is reachable only via setup.apply, setup.py:242); the provenance block records seat id, effort (null included), exact first-listed command, and smoke state (opening.py:305-320), round-tripped by load_config which ignores unknown keys (channel.py:385-428).
- D2.5/ruling 5: load_profile refuses malformed JSON, wrong profile_version, unknown id, and empty allowlist, each naming the file and offender (seats.py:556-600; test_load_profile_fail_closed); missing file → no restriction; picker listing, --pair, and last_pair all honor the allowlist (test_pick_pair_profile_restricts).

Criterion 3 (safety): the seam is default-compatible — channel_config defaults to None and then performs the same unconditional disk read; all seven pre-existing _watcher_config call sites (__main__.py:209,721,856,862,868,884,897) pass no fourth argument and are byte-identical in behavior; the dispatch-guard change only adds seats/open to the exclusion tuple; the fold's change set touches only seats.py's discover and test_open.py — nothing in channel/watcher/broker/setup law; the full pre-existing suite (channel, watcher, controller, setup, verify, migrate tests) passes unchanged.

Exhaustive enumeration per R2: I actively tried to break each docket claim (prefix-match residue, guard edge cases, exit-code sources, seam default path, dispatch guard, profile bypasses, cache side effects, provenance fidelity) and every attempt failed to produce a contradiction. No blocking finding is establishable in this pass; the list is empty.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 464b876f1354d402e28d2e62a6405a541f57b4f07b5addb8c7eaecb65e332527
- phase: sealed
- captured-at: 2026-08-17T18:38:12+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 3a554e29b32d636696c3ef7a482a6224a547725b4e7d14b94aa473d319cb84b9
- source-ref: a4cb5362194cccee6b0d4726ea4f251e3db6541c
- source-manifest-sha256: d7f5a5a5ff90b0f1ed4f3a6eb4575ef7cf95694469ae7096425314155e51a670
- docket-revision-sha256: aa2acf3e40864deb7537fbbffd0a1e09c7e5089f8f219550edc6c472985ff857
- input-sha256: 4df879709cc2b047e84719212905bbed8550738e860c54b8f1ec1a67c0a40b00
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-16 | 2026-08-17T18:48:38+00:00 | from: glm | type: verdict | thread: branch-seat-registry-7 | refs: -

FRESH COMMANDS (criterion 1): `python -m pytest -q` run literally in the export root (cwd .../exports/a4cb5362194cccee6b0d4726ea4f251e3db6541c/glm), no prefixes/suffixes/pipes -> "463 passed, 1 skipped in 18.77s". Diagnostic: `python -m pytest -q tests/test_seats.py -k ensure_current` -> "2 passed, 25 deselected in 0.41s". The suite is green; criterion 1 holds. Criteria 2-3 fail on one finding.

EXHAUSTIVE BLOCKING LIST (one entry; the other candidate is rejected below with the judgment calls named):

BLOCKER (adopted from codex MSG-14, re-verified on my own export's source; the D3 upgrade trigger does not persist the version stamp when the re-scan diff is empty). Static chain, all line numbers from my export: src/debate/__main__.py:542-545 — every non-discover `seats` subcommand calls `registry, upgrade_diff = seats.ensure_current(registry, now=now)` and then `seats.save_registry(registry)` ONLY inside `if upgrade_diff:`; src/debate/seats.py:353-365 — ensure_current returns discover() on mismatch; seats.py:260-262 — discover mutates `registry.discovered_at`/`registry.tool_version = __version__` on the returned object; diff lines are appended only for a real change (seats.py:227 new seat, 230 present-again, 253 re-derive, 259 absent-mark). So `seats list`/`check`/`doctor` on a stale registry whose catalog re-scan changes nothing (the steady state after any tool upgrade with an unchanged catalog) produce diff == [], skip save_registry, and leave the persisted `tool_version` stale — the mismatch re-scan re-fires on every subsequent invocation and the required stamp is never recorded. The `open` path has the same conditional (__main__.py:488-490) but saves unconditionally later at :530, so it does persist; the defect surface is exactly list/check/doctor. The plan is explicit that stamping is part of the trigger: docket plan copy, D3 — "on mismatch it re-runs the catalog scan FIRST (scan only — smoke is never automatic), prints the diff ..., and stamps the new version"; Slice-2 spec — "older tool_version -> discover runs, diff returned, version stamped"; interface comment — "version mismatch -> discover() + stamp"; and `tool_version` is a persisted registry-schema field whose only consumer is the load-time comparison (seats.py:363). Nothing in the suite pins persistence: test_seats.py:289-297 asserts only the in-memory stamp, and the one CLI upgrade test (tests/test_open.py:446-458) forces tool_version "0.0.1", runs `seats list --json`, and asserts only exit 0 and pure-JSON stdout — never that the file was re-saved. JUDGMENT CALL, named: one could read "stamps" as discover()'s in-memory mutation; I reject that reading because an unpersisted stamp is functionally void (the field's only reader is the next load), which would make the plan's schema field and its Slice-2 assertion vacuous. Sandbox note, reported faithfully: the docket-profile Bash allowlist is test-only, so codex's dynamic `python -c` monkeypatch repro was denied to me when I attempted it verbatim; the static chain above is conclusive on its own, the inputs codex exercised are byte-identical in my export, and their observed result (exit 0, tool_version '0.6.0' in memory, save_calls []) is exactly what this code does. This violates docket criterion 2 (D3/fold H1 plan conformance); hence NO_PASS.

REJECTED CANDIDATE (codex MSG-14 blocker 1, "docket-tracked collab/PROTOCOL.md missing from the pinned export"): the fact reproduces — my export also has no `collab/` directory (verified: `ls` of the export root lists no collab; root PROTOCOL.md is a different document, the tool's shipped template, "# The debate protocol — a contract between two debating seats..."). But the docket's pinned copy exists in the docket revision (read in full at .../dockets/aa2acf3e.../files/collab/PROTOCOL.md), and that document itself defines the export scope I must judge against: section 3 — the controller "snapshots the pinned commit and immutable docket into separate read-only exports"; section 5 — "Seats can read the complete pinned codebase in their own export; `collab/`, `var/` and `.git` are separated so live channel state and controller internals do not contaminate the opposing judgment." `tracked_at_source_ref: true` distinguishes the repo-tracked contract from controller artifacts; it does not promise reproduction inside the codebase export, and the seat brief supplies the file via the immutable docket, where I read it. JUDGMENT CALL, named: I read the export-completeness rule from the very file whose absence was alleged rather than assuming the export must mirror the docket list; on that evidence the export is complete per its documented scope and no docket criterion (command, plan conformance, safety) depends on collab/PROTOCOL.md living inside it. Blocker rejected — it does not survive re-verification.

RETRACTION of my own sealed MSG-15 claim "ensure_current re-runs discover only ... and stamps the version (seats.py:353-365)": true in memory, false on disk for list/check/doctor whenever the re-scan is clean. That sealed PASS was an incomplete sweep of the persistence path; it is withdrawn and replaced by this verdict.

RE-VERIFIED AND STANDING from the sealed sweep (spot-checked fresh against this export): the round-5 fold resolves the converged finding — seats.py:236-253 re-derives only on the exact shape (`if derived.commands[0] != old_argv + fragment: continue` at :250), no prefix-match residue exists (`rg '\[: len\('` over src/debate: no matches), the manual base is further gated by `existing.source == "catalog"` (seats.py:228), and the pinned reproduction test sits verbatim at tests/test_open.py:529-561 (base + ["--effort","high","--manual-wrapper-flag"] untouched including the old binary head; claude/opus@low re-derived to the new binary); branch-fold-r5.diff's post-state is byte-identical to both files. Dispatch fold B2 confirmed at __main__.py:482 (`("init", "migrate", "seats", "open")`). D1/D2/D4/D2.5 and safety claims were re-checked at spot-check level and are unchanged by this fold's two-file change set; the full suite passing fresh corroborates them. Nothing else establishable — the list above is exhaustive for this pass.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 3a554e29b32d636696c3ef7a482a6224a547725b4e7d14b94aa473d319cb84b9
- source-ref: a4cb5362194cccee6b0d4726ea4f251e3db6541c
- source-manifest-sha256: d7f5a5a5ff90b0f1ed4f3a6eb4575ef7cf95694469ae7096425314155e51a670
- docket-revision-sha256: aa2acf3e40864deb7537fbbffd0a1e09c7e5089f8f219550edc6c472985ff857
- input-sha256: 3d8e5785040b89630925eb5b45eddc2960efee2f97583536ff44066a50f8e99d
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-17 | 2026-08-17T18:48:38+00:00 | from: owner | type: close | thread: branch-seat-registry-7 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-18 | 2026-08-17T18:50:16+00:00 | from: owner | type: review-request | thread: branch-seat-registry-8 | refs: feature/seat-registry@2e3cc983302760884817207345b3eb7c57a00f7f

REVIEW REQUEST - branch gate round 7 (fold-delta) for feature/seat-registry@2e3cc98. GOAL: verify the single fold (upgrade stamp persists on a clean re-scan, pinned by a reload-the-file test) resolves the round-6 converged finding; everything else stands per MSG-8/9/11/14/15/16 unless implicated. True change set materialized as branch-fold-r6.diff. Run the full suite literally. Exhaustive enumeration applies.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 6b3ad60b197b292c30692b1360197bd5d7ad6b6e6599c42dd2bf869b3477645e
- source-ref: 2e3cc983302760884817207345b3eb7c57a00f7f
- docket-revision-sha256: 1bee2bbc43e0d96a3d3ee00d7ec7302f69efe729f9af8b7c30656be8b2226240
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "e34832ca3e5f7f0545da729c1b825c7dcfd1b67915ef4f2e8ea6481d765abcfa", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r6.diff", "sha256": "ad62dc44c5a45ecc9c95208dfd76b21e28796eede2ba5cb5176bd224e1efbe01", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a4933a3564957935da9e6967ed4dc4aa9c101b22f3deec01d794c118f5fea941", "glm": "de50ed1c969fe9dc45a992cf9d8c6349d1ba830e0e56a526de892ff905f07133"}

## MSG-19 | 2026-08-17T19:01:38+00:00 | from: codex | type: verdict | thread: branch-seat-registry-8 | refs: -

`python -m pytest -q` exited 0: `464 passed, 1 skipped in 19.28s`. Blocking findings:

1. Freshness is wrong for an absent catalog seat. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/seats.py:328` skips binary checking when `present` is false and emits INFO. Fresh command `python -c '...discover...discover...check...'` printed `False`, `[]`, and `['INFO glm/glm-5.3: absent since discovery (run: debate seats discover)']`: a discovery-confirmed vanished binary exits 0, contrary to D3's missing-binary failure.

2. Project-profile version loading is not fail-closed. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/seats.py:489` uses `!= 1`, so JSON boolean `true` equals Python integer `1`. Fresh command writing `{"profile_version": true, "allowlist":["x/y"]}` and calling `load_profile` printed `Profile(allowlist=('x/y',))`; malformed/non-version-1 input must refuse.

3. The implementation was not versioned for the planned 0.6→0.7 upgrade. Fresh command `grep -HnE '^version =|^__version__' pyproject.toml src/debate/__init__.py` printed `pyproject.toml:7:version = "0.6.0"` and `src/debate/__init__.py:42:__version__ = "0.6.0"`. Consequently existing 0.6.0 registry stamps do not mismatch when this registry/catalog feature ships, so its required upgrade re-scan is not triggered for this change.

4. Open provenance does not preserve smoke state verbatim. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/opening.py:301` records only `smoke_at`, omitting the smoke result. A fresh local `open_debate` probe with two passing `SmokeStatus` values printed entries containing `"smoke_at"` but no `"result"`; D4 requires the smoke state in the `.debate.json` provenance block.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 3024239d4f337602306c7a9d7d03be08ee48744c05d78cc428b096d25bf595ec
- phase: sealed
- captured-at: 2026-08-17T18:55:21+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 6b3ad60b197b292c30692b1360197bd5d7ad6b6e6599c42dd2bf869b3477645e
- source-ref: 2e3cc983302760884817207345b3eb7c57a00f7f
- source-manifest-sha256: a4933a3564957935da9e6967ed4dc4aa9c101b22f3deec01d794c118f5fea941
- docket-revision-sha256: 1bee2bbc43e0d96a3d3ee00d7ec7302f69efe729f9af8b7c30656be8b2226240
- input-sha256: 132120b3e7c5f2290ef977c8f653fac5a54d9a69c1bc6d4c4c20e0dba20cf6ef
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-20 | 2026-08-17T19:01:38+00:00 | from: glm | type: verdict | thread: branch-seat-registry-8 | refs: -

COMMAND (run literally in the export root, no prefix/suffix/pipe): `python -m pytest -q` -> "464 passed, 1 skipped in 18.63s", zero failures. The single skip is the suite's own documented probabilistic anti-vacuity test (tests/test_verify_record.py:331, "the unlocked race window did not open in this run"), pre-existing and unrelated to the fold.

ROUND-6 CONVERGED FINDING RESOLVED (the GOAL, verified on my own evidence): both dispatch sites persist the stamp even when the re-scan diff is empty -- src/debate/__main__.py:488-493 (`open`) and :546-555 (`seats`), each `if upgrade_diff or registry.tool_version != pre_version: seats.save_registry(registry)` with `pre_version` captured before `seats.ensure_current`; pinned by the reload-the-file test tests/test_open.py:564-582 (`test_upgrade_stamp_persists_on_clean_rescan`, asserts `seats.load_registry().tool_version == __version__` after a clean re-scan), which ran green in my fresh suite run. `ensure_current` re-scans scan-only (`seats.py:353-365` -> `discover`, no model calls); every `seats` entry point except `discover` (which always saves) passes through the guarded site.

CRITERION 2 (plan conformance), files checked: D1 -- single-seat rule statically enforced (tests/test_seats.py:43-51) and satisfied by the data (codex/glm/deepseek each exactly one submodel with empty `submodel_argv`, seat_catalog.py:57-112); grok's omission documented in the module docstring as unverifiable (seat_catalog.py:30-31), kimi's wrapper-first deviation declared under the correct-the-seeds mandate (seat_catalog.py:17-26). D2/ruling 4 -- commands is one-or-more argvs (`_seat_from_raw`, seats.py:63-71), selection first-listed at every consumer I could find (check :333, pick/open/smoke/add-effort all use `commands[0]`); credential screen on every write path (seats.py:136-150, add_seat :396-401, opening.py:221); merge-never-clobber (absent-marked never deleted, seats.py:254-259; operator seats untouched, pinned tests/test_seats.py:147-163 and the round-3/round-5 exact-derived-shape tests tests/test_open.py:504-561). D3/H1 -- `check` fails ONLY on unresolvable binary or failed smoke; never-smoked INFO, stale WARN, exit 0 (seats.py:320-350, CLI returns 3 iff fails, __main__.py:556-575; pinned tests/test_seats.py:230-274, 363-386). An absent-marked seat is INFO with the re-discovery offer -- consistent with the docket's necessary-condition wording ("exits 3 ONLY on...") and unseatable anyway (opening.py:68-85). Dispatch B2 -- `seats`/`open` join init/migrate in the no-discovery set (__main__.py:482). D4 -- pick_pair default keyed by `_derived_project` (git toplevel; opening.py:52-54, channel.py:254-273), global fallback and dropped unseatable/non-allowlisted defaults (opening.py:129-147); unsmoked/stale warning covered by `--yes` (opening.py:195-196), identity guard never covered by it, same vendor/submodel refused without `--allow-identical-seats` with effort ignored, identical SELECTED argv refused always (opening.py:88-106, pinned test_open.py:127-159); shared-vendor party names slugified dot-free (opening.py:57-65, 234-242, pinned test_open.py:231-256); ALL validation before the first target write through the `channel_config` seam, probe written outside the target root (opening.py:285-293; empty-root pins test_open.py:259-278, 405-443); `setup.apply` never called and the defaults cache byte-untouched (opening.py imports only validate/build_prompt/derive_paths/scaffold_protocol; pinned test_open.py:281-297); provenance block records seat id, effort incl. null, exact command, smoke state per the plan's D4 step 5 shape (opening.py:303-321). D2.5/ruling 5 -- committable profile, fail-closed on malformed/version/unknown-id/empty with the offender named, opt-in, picker restricted (seats.py:556-600, opening.py:122-127, 170-175, 222-229; pinned test_open.py:337-399).

CRITERION 3 (safety): the seam is default-compatible -- `channel_config=None` takes the identical `channel.load_config` disk path (__main__.py:130-134) and no existing caller passes it; the dispatch guard changes nothing for pre-existing commands (they still resolve a channel, __main__.py:481-483); the fold's true change set (var/debate/.../branch-fold-r6.diff) touches only the two save conditions plus the new test, and channel/watcher/broker/setup law is untouched by it; the full suite including the watcher/channel/controller corpora passed. New modules are ASCII-clean (non-ASCII exists only in exempt docstrings/templates and deliberate test fixtures).

Exhaustive sweep: no further blocking finding was establishable in this pass; the two candidate tensions I probed (absent-seat INFO vs exit 3; @effort re-derivation touching source="manual" seats) are both settled, tested law from rounds 3-5 and consistent with the docket's stated criterion text.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3024239d4f337602306c7a9d7d03be08ee48744c05d78cc428b096d25bf595ec
- phase: sealed
- captured-at: 2026-08-17T19:01:38+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 6b3ad60b197b292c30692b1360197bd5d7ad6b6e6599c42dd2bf869b3477645e
- source-ref: 2e3cc983302760884817207345b3eb7c57a00f7f
- source-manifest-sha256: de50ed1c969fe9dc45a992cf9d8c6349d1ba830e0e56a526de892ff905f07133
- docket-revision-sha256: 1bee2bbc43e0d96a3d3ee00d7ec7302f69efe729f9af8b7c30656be8b2226240
- input-sha256: a73c501f1be31f7775ddc9c20b1fa3f664c32e0b3b54816554d90338edfca3ea
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-21 | 2026-08-17T19:07:43+00:00 | from: codex | type: verdict | thread: branch-seat-registry-8 | refs: -

`python -m pytest -q` run literally in the export root passed: `464 passed, 1 skipped in 18.60s`. I adopt the opponent’s conclusion that the round-6 stamp fold itself works: `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/__main__.py:488-491` and `:546-550` persist a changed stamp, and the passing suite includes the reload test. I reject its broader PASS conclusion. All four of my sealed blockers survive fresh re-verification; none is retracted.

Blocking findings, exhaustive for this pass:

1. D3 missing-binary handling is wrong for a discovery-confirmed absent catalog seat. Exact command: `python -c '... print("cli_exit=", main(["seats", "check"]))'` (with a current-version registry containing an absent seat whose command head is `/definitely-not-installed`) printed `INFO glm/glm-5.3: absent since discovery...` and `cli_exit= 0`. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/seats.py:328-332` skips resolution for `present == false`. Judgment: D3’s required missing-binary failure includes a binary discovery has confirmed vanished; the INFO-only treatment violates it.

2. D2.5 profile loading is not fail-closed for a malformed version type. Exact command writing `{\"profile_version\": true, \"allowlist\":[\"x/y\"]}` then calling `seats.load_profile(...)` printed `Profile(allowlist=('x/y',))`. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/seats.py:577` accepts JSON `true` because `True == 1`. Judgment: boolean is not profile version 1, so it must refuse.

3. The planned 0.6→0.7 upgrade trigger cannot fire. Exact command `python -c 'from debate import __version__, seats; ...'` printed `package_version= 0.6.0` and `rescan= False diff= [] stamp= 0.6.0` for an existing `0.6.0` registry. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/pyproject.toml:7` and `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/__init__.py:42` are both `0.6.0`. Judgment: the plan expressly requires this feature’s upgrade re-scan from 0.6 to 0.7, and unchanged versioning defeats it.

4. D4 provenance does not retain smoke state verbatim. Exact `open_debate` probe with two passing `SmokeStatus(at, result)` values printed provenance entries containing only `smoke_at`, with no `result`. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/2e3cc983302760884817207345b3eb7c57a00f7f/codex/src/debate/opening.py:308-319` serializes only the timestamp. Judgment: the docket’s explicit “smoke state verbatim” criterion requires the result as well as its time.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 6b3ad60b197b292c30692b1360197bd5d7ad6b6e6599c42dd2bf869b3477645e
- source-ref: 2e3cc983302760884817207345b3eb7c57a00f7f
- source-manifest-sha256: a4933a3564957935da9e6967ed4dc4aa9c101b22f3deec01d794c118f5fea941
- docket-revision-sha256: 1bee2bbc43e0d96a3d3ee00d7ec7302f69efe729f9af8b7c30656be8b2226240
- input-sha256: 24de1f37612d3dbc519d21010ba3fc826cc7dadb7c04b62c62512a9173c80d42
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-22 | 2026-08-17T19:17:02+00:00 | from: glm | type: verdict | thread: branch-seat-registry-8 | refs: -

COMMAND (docket criterion 1, run literally in the export root): `python -m pytest -q` -> "464 passed, 1 skipped in 18.67s", zero failures (the skip is the suite's own documented probabilistic anti-vacuity test). Targeted fresh runs: `python -m pytest -q tests/test_seats.py -k "check or ensure_current or rediscover" tests/test_open.py -k "check or ensure_current or rediscover"` -> 9 passed; `python -m pytest -q tests/test_open.py::test_upgrade_stamp_persists_on_clean_rescan ...::test_open_debate_end_to_end ...::test_open_debate_shared_vendor_party_names_are_slugs ...::test_load_profile_fail_closed ...::test_pick_pair_profile_restricts ...::test_cli_seats_list_json_is_machine_readable_after_upgrade ...::test_pick_pair_absent_seat_refused` -> 7 passed. My Bash surface this pass is pytest-only, so code-level claims below rest on the pinned source read plus Python's deterministic bool/int semantics, each marked.

GOAL VERIFIED (adopting codex's agreement): branch-fold-r6.diff is exactly the two guarded saves (src/debate/__main__.py:488-493 `open`, :546-555 `seats`, each `if upgrade_diff or registry.tool_version != pre_version: seats.save_registry(registry)` with pre_version captured before ensure_current) plus the reload-the-file test (tests/test_open.py:564-582, asserts `seats.load_registry().tool_version == __version__` after a clean re-scan) — passed green above. The round-6 converged finding is resolved.

BLOCKING FINDING (adopted from the opponent after fresh re-verification; exhaustive for this pass):
1. D2.5 profile loading is not fail-closed for a non-integer profile_version. src/debate/seats.py:577 uses `raw.get("profile_version") != 1`; JSON `true` parses to Python `True` and `True == 1`, so `{"profile_version": true, "allowlist": [...]}` is ACCEPTED and returns a Profile (float `1.0` likewise). This is deterministic from the code path — no probe needed. The docket's D2.5 clause is absolute ("fail-closed loading (malformed/version/unknown-id/empty all refuse with the offender named)") and a boolean is not version 1: the one valid value is the integer 1, and fail-closed means everything else refuses. The codebase type-checks every neighboring field (seats.py:79-83 refuses non-bool `present`; seats.py:63-71 refuses malformed commands) — the version check alone leans on bool-subclasses-int, an implementation artifact, not a design choice. Judgment call, named: I classify a boolean/float version under the docket's "version" offender category, so the criterion has a hole; impact is narrow (the allowlist itself is still validated), but the docket bar is letter-level and the exhaustive rule forbids waving a establishable deviation through. Same-class twin, named for the fix but not separately blocking (no docket clause covers it): load_registry's `version != REGISTRY_VERSION` at seats.py:110 accepts `true`/`1.0` for registry_version the same way.

OPPONENT FINDINGS REJECTED (each a named judgment call, fresh evidence):
2. Absent-seat INFO vs exit 3 (their blocker 1). src/debate/seats.py:328-332 does skip binary resolution for `present == false` — fact confirmed. Judgment: I read the plan's FAIL clause ("a seat whose binary no longer resolves") as the ROT case — the registry believes the seat present and the head is gone (seats.py:333-335, pinned by test_check_missing_binary_is_fail, passed fresh). An absent-marked seat is the already-RECORDED state, not news: catalog seats are never deleted (discover deletes nothing, seats.py:254-259; `seats remove` refuses catalog seats, seats.py:473-476), so treating absent as FAIL would make exit 3 permanent on any machine that ever removed a vendor CLI, with no remedy — exactly the toll shape fold H1's rationale rejects; ruling 1 asks level 2 to "flag rot and OFFER full re-discovery", which the INFO line does verbatim ("absent since discovery (run: debate seats discover)"); and the docket's own wording is the necessary-condition form ("exits 3 ONLY on missing binary or failed smoke"), which holds — every exit-3 cause is a missing binary or failed smoke. Absent seats are unseatable at open regardless (opening.py:72-76, test_pick_pair_absent_seat_refused passed). Correction to my sealed verdict: this is a plan-reading judgment, NOT "tested law" as I sealed — no test classifies absent seats in check.
3. Version not bumped 0.6->0.7 (their blocker 3). Fact confirmed: pyproject.toml:7 and src/debate/__init__.py:42 are both "0.6.0". Judgment: the plan's Non-goals state "No release in this plan; version/CHANGELOG ride the next release plan" — the bump is expressly out of the executable scope, and the docket's criterion asks only that "the upgrade trigger re-scans on version mismatch, scan only", which is implemented (seats.py:353-365, discover is scan-only) and pinned by mismatch-fixture tests passed fresh (test_ensure_current_version_mismatch_rescans, test_cli_seats_list_json_is_machine_readable_after_upgrade, and the fold's reload test). The 0.6->0.7 mentions illustrate the mechanism across a release boundary, matching the plan's own Slice-2 fixture-based verification step.
4. Provenance omits smoke result (their blocker 4). src/debate/opening.py:305-320 records seat/effort/command/smoke_at — exactly the shape of the plan's own D4 step 5 example block (which carries `smoke_at` null or timestamp, no result field), and the docket's enumeration ("seat id, effort (null included), exact command, and smoke state verbatim") maps 1:1 onto those four fields. Judgment: the record is unambiguous because a FAILED smoke can never be seated — pick_pair refuses any non-pass smoke outright (opening.py:180-185) and the CLI routes `open` through pick_pair before minting (__main__.py:505-530) — so null means seated-untested and a timestamp means a pass at that time (staleness is computable from picked_at vs smoke_at). The opponent demands a field the materialized plan never specified; the implementation matches the plan's normative example verbatim.

SEATED-VERDICT RE-VERIFICATION: my sealed GOAL/D1-D4/S3 checks all survive fresh re-verification (catalog single-seat rule statically enforced, tests/test_seats.py:43-51; grok's omission documented as unverifiable and kimi's deviation declared under the correct-the-seeds mandate, seat_catalog.py:16-35; merge-never-clobber and credential screens, seats.py:136-176, 254-259; dispatch no-discovery set, __main__.py:482; the channel_config seam default-identical, __main__.py:130-134; identity guard and slug rules, opening.py:88-106, 57-65; profile restriction, opening.py:122-127, 170-175; provenance shape test, tests/test_open.py:199-228 — all in the green runs above). RETRACTED from my sealed verdict: its closing claim that no further blocking finding was establishable — blocker 1 above is establishable and adopted.

DECISION: NO_PASS. Criterion 1 passes and criteria 2-3 hold on my own evidence EXCEPT the D2.5 fail-closed clause (blocker 1); the fold itself is verified resolved and nothing else in the fold's change set or my sweep implicates the standing criteria. Fix: type-check the version fields (`isinstance(v, int) and not isinstance(v, bool) and v == 1`, and likewise for registry_version) with the offender still named, plus a pinning test for the `true`/`1.0` inputs at both sites.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 6b3ad60b197b292c30692b1360197bd5d7ad6b6e6599c42dd2bf869b3477645e
- source-ref: 2e3cc983302760884817207345b3eb7c57a00f7f
- source-manifest-sha256: de50ed1c969fe9dc45a992cf9d8c6349d1ba830e0e56a526de892ff905f07133
- docket-revision-sha256: 1bee2bbc43e0d96a3d3ee00d7ec7302f69efe729f9af8b7c30656be8b2226240
- input-sha256: 81560535c6abb2a384b6429f8d56d486f15d8580d807560da88850a2688aeb81
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-23 | 2026-08-17T19:17:02+00:00 | from: owner | type: close | thread: branch-seat-registry-8 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-24 | 2026-08-17T19:19:31+00:00 | from: owner | type: review-request | thread: branch-seat-registry-9 | refs: feature/seat-registry@99410da6bd8c36f3fc65a81ea47abcfb38a55afc

REVIEW REQUEST - branch gate round 8 (fold-delta) for feature/seat-registry@99410da. GOAL: verify folds C1 (absent = FAIL + removal remedy), C2 (profile_version bool guard), C4 (smoke_result in provenance) resolve their round-7 findings; judge the C3 rejection on the plan Non-goals text quoted in the docket; everything else stands per the cited record. True change set materialized as branch-fold-r7.diff. Run the full suite literally. Exhaustive enumeration applies.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 518663df1e2f04aefa7abd6f9b2adbaeacfd28ae031d24c41e97746d2c9e872d
- source-ref: 99410da6bd8c36f3fc65a81ea47abcfb38a55afc
- docket-revision-sha256: efb36a72c399621cd1c1b550c068bc85163222177f61a76f49044299e2da5b9d
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "9e0eeb76ff6e246253636be0097d87d81176817c69159b1248a3f10aacefb771", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r7.diff", "sha256": "073d7c54d104ed74d83ee5465a473114ef057e8676ac9aee99d351c6644fdb9f", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "6307aea79141e4b59c11a9ef7ebefd9e9773d02cd89927b2e2dcc10ea1df353a", "glm": "57535f44843ebcfb10709f9795f68ed224b0f00fcb3d99b7231d0dfd5a2c62e1"}

## MSG-25 | 2026-08-17T19:27:37+00:00 | from: codex | type: verdict | thread: branch-seat-registry-9 | refs: -

`python -m pytest -q` (run literally in the export root) passed: `466 passed, 1 skipped in 19.41s`. Blocking finding: registry discovery violates the standing D2 rule that manual entries remain untouched. `/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/99410da6bd8c36f3fc65a81ea47abcfb38a55afc/codex/src/debate/seats.py` creates `@effort` derivations with `source="manual"` but rewrites their selected command on re-discovery when it matches the old derived form. My fresh in-memory probe (`python - <<'PY'` calling `seats.discover`, `seats.add_effort_seat`, then `seats.discover` with a changed resolved Claude path) returned `derived_source= manual` and `manual_derived_rewritten= True /new/claude`. This contradicts the docket's required “manual entries untouched”; tests passing does not satisfy that criterion.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 294ce9aa51c2ec0c948c70b50f814b9b586021089f3a5d7f9c1bfaa204a509b9
- phase: sealed
- captured-at: 2026-08-17T19:27:37+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff
- controller-config-sha256: 518663df1e2f04aefa7abd6f9b2adbaeacfd28ae031d24c41e97746d2c9e872d
- source-ref: 99410da6bd8c36f3fc65a81ea47abcfb38a55afc
- source-manifest-sha256: 6307aea79141e4b59c11a9ef7ebefd9e9773d02cd89927b2e2dcc10ea1df353a
- docket-revision-sha256: efb36a72c399621cd1c1b550c068bc85163222177f61a76f49044299e2da5b9d
- input-sha256: d4832a5eff9f2a9fd1db93af896bdeba6e54586de04cec4d05eeddd244fd5822
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-26 | 2026-08-17T19:27:37+00:00 | from: glm | type: verdict | thread: branch-seat-registry-9 | refs: -

VERDICT: PASS.

1) Docket command, run literally in the export root (/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/99410da6bd8c36f3fc65a81ea47abcfb38a55afc/glm): `python -m pytest -q` -> "466 passed, 1 skipped in 18.85s". The two skips are pre-existing conditional skips (tests/test_watcher_config.py:90 "no example config in this checkout"; tests/test_verify_record.py:331 timing-dependent race window), not new seat-surface tests. Export integrity spot-check: sha256sum of src/debate/{seats,opening,seat_catalog,__main__,channel,setup}.py all match glm.manifest.json (e.g. seats.py b674e75790f362a957d234ceac09468327950ebbb4d0136819b471d455d285b8).

2) Round-7 folds present in the pinned export, each probed against its own text:
- C1: src/debate/seats.py:328-332 `check` FAILs absent seats ("binary missing ... debate seats remove") and seats.py:474-478 `remove_seat` refuses only PRESENT catalog seats, allowing absent-catalog cleanup; pinned by tests/test_seats.py:162-165 and 344-349. I tried to break the D3-literal rule (exit 3 = real breakage only) via never-smoked/stale paths: seats.py:338-350 keeps them INFO/WARN, and __main__.py:565/575 returns 3 only when fails is nonempty.
- C2: seats.py:579-584 rejects JSON true for profile_version (`isinstance(version_raw, bool)` guard); pinned by tests/test_open.py:585-592.
- C4: src/debate/opening.py:312-313,318-321 records smoke_at AND smoke_result verbatim; pinned by tests/test_open.py:595-609.
- C3 rejection stands on the plan: version stays 0.6.0 (src/debate/__init__.py:42, pyproject.toml:7), CHANGELOG has no 0.7.0 release, matching the plan's Non-goal "No release in this plan; version/CHANGELOG ride the next release plan"; no mismatch loop is possible since discover stamps the current __version__ (seats.py:261).

3) Plan conformance, checked by reading the materialized code: D1 single-seat rule statically enforced (tests/test_seats.py:43-51; catalog entries with empty submodel_argv carry exactly one submodel), grok's absence documented in seat_catalog.py:30-31, kimi's wrapper-order deviation declared in the module docstring under the Slice-1 correct-the-seeds mandate. D2: commands is a list of endpoint argvs, first-listed selection everywhere (seats.py:40, opening.py uses commands[0] for pick, provenance, watcher config); merge-never-clobber (seats.py:254-259 marks absent, deletes nothing, skips source!="catalog"); credential-screened writes (save_registry -> screen_credentials, seats.py:148-176; add_seat, seats.py:397-402). D3: dispatch exempt set is ("init","migrate","seats","open") (__main__.py:482) — `seats` takes no --root and never resolves a channel; upgrade trigger ensure_current is scan-only and wired into every seats subcommand and open (__main__.py:539-555, 486-493), stamp persists even on an empty diff (tests/test_open.py:564-582). D4: pick_pair defaults keyed by the git toplevel via channel._derived_project (opening.py:52-54, 131), unseatable/non-allowlisted defaults dropped, --yes with no default refuses; identity guard is effort-blind and never covered by --yes while identical SELECTED argv refuses even with --allow-identical-seats (opening.py:88-106, tests/test_open.py:127-159); shared-vendor party names slugified dot-free (opening.py:57-65, 234-242, tests/test_open.py:231-256); ALL validation precedes the first target write through the channel_config seam on _watcher_config (opening.py:285-293 probe lives in a temp dir; __main__.py:73-134 seam is default-compatible — omitted path still reads the disk, pinned by tests/test_open.py:48-71); setup.apply is never imported by opening.py and the defaults cache is byte-untouched (tests/test_open.py:281-297); provenance block carries seat id, effort incl. null, exact command, smoke state (opening.py:305-322). D2.5: fail-closed profile loading — malformed JSON, non-1 version, unknown id, empty allowlist all refuse naming the offender (seats.py:558-603, tests/test_open.py:337-362), picker restricted and --pair outside refused naming the file (tests/test_open.py:365-399).

4) Safety: the seam's default path is byte-identical (keyword defaults to None -> load_config disk read, __main__.py:133-134; pre-existing watcher/setup tests green), the dispatch guard still resolves channels for every pre-existing command, and channel/watcher/broker law is untouched by the r7 change set (branch-fold-r7.diff touches only opening.py, seats.py, and the two test files); the full pre-existing suite passing (466 total, consistent with the plan's 413 + the new seat tests) pins shipped behavior for existing commands and configs.

Files checked: docket branch-docket.md, plan, seat-result.schema.json, branch-fold-r7.diff; export src/debate/{seat_catalog,seats,opening,__main__,channel,setup,watcher,__init}.py, tests/{test_seats,test_open}.py, README.md, CHANGELOG.md, pyproject.toml, glm.manifest.json. No blocking finding establishable in this pass; the exhaustive list is empty.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 294ce9aa51c2ec0c948c70b50f814b9b586021089f3a5d7f9c1bfaa204a509b9
- phase: sealed
- captured-at: 2026-08-17T19:24:42+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 518663df1e2f04aefa7abd6f9b2adbaeacfd28ae031d24c41e97746d2c9e872d
- source-ref: 99410da6bd8c36f3fc65a81ea47abcfb38a55afc
- source-manifest-sha256: 57535f44843ebcfb10709f9795f68ed224b0f00fcb3d99b7231d0dfd5a2c62e1
- docket-revision-sha256: efb36a72c399621cd1c1b550c068bc85163222177f61a76f49044299e2da5b9d
- input-sha256: 6759a52265585e9d4f4c4a4957903f5f25abe79423c6d96423591bb4ceec2cce
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-27 | 2026-08-17T19:35:19+00:00 | from: glm | type: verdict | thread: branch-seat-registry-9 | refs: -

VERDICT: NO_PASS. I retract my sealed PASS (MSG-26): its D2 check was incomplete, and the opponent's blocking finding survives re-verification on my own evidence. Exhaustive blocking list: ONE finding.

COMMAND (docket step 1), run literally in the export root (/home/zoltan/Projects/debate/var/debate/seat-registry-gate2-91255/controller/exports/99410da6bd8c36f3fc65a81ea47abcfb38a55afc/glm): `python -m pytest -q` -> "466 passed, 1 skipped in 18.85s". The suite is green; the blocker below is a plan-conformance failure the suite does not cover.

BLOCKING FINDING (adopted from codex MSG-25 after independent re-verification): discover() rewrites the selected command of a source="manual" @effort seat, violating the docket's D2 standing criterion "merge-never-clobber discovery (absent-marked, never deleted; manual entries untouched)".
- The path, traced line-by-line in my own pinned export (branch-free, deterministic; constants read from the export): `add_effort_seat` (src/debate/seats.py:426-467) creates `vendor/submodel@effort` with source="manual" (line 464) and argv = base.commands[0] + substituted effort_argv (455-457). On re-discovery, when a catalog base seat's argv changes, the derived-rewrite loop (seats.py:236-253) replaces `derived.commands[0]` of every seat whose base id matches and whose argv is EXACTLY old-base + effort fragment — it never consults `derived.source`. A seat created by add_effort_seat satisfies the exact-match BY CONSTRUCTION, so its selected command is silently rewritten. Trace with the real claude entry (seat_catalog.py:58-67: binaries=("claude",), submodel_argv=("--model","{submodel}"), effort_argv=("--effort","{effort}"), known_efforts includes "high"): discover#1 (claude -> /old/claude) seeds claude/opus = ["/old/claude","-p","{prompt}","--model","opus"]; `seats add claude/opus@high` (__main__.py:595-596) yields ["/old/claude","-p","{prompt}","--model","opus","--effort","high"], source="manual"; discover#2 (claude -> /new/claude) rewrites it to ["/new/claude",...,"--effort","high"] with diff line "~ claude/opus@high re-derived from the new base argv", source still "manual". This is exactly codex's reported probe output (derived_source=manual, manual_derived_rewritten=True, /new/claude). Honesty note: my seat's Bash is test-only, so my ad-hoc probe heredoc was denied by the sandbox; the confirmation above is a deterministic code trace against the pinned export plus codex's executed probe, not my own execution.
- Why it blocks: the approved plan states the rule twice — D2 "Merge, never clobber" (docs/plans/2026-08-15-seat-registry-and-debate-open.md:280-283): re-discovery "never touches `source: \"manual\"` entries"; and the Slice-1 test spec (plan:544-547): "manual entries (including `@effort` derivations) untouched" — the plan names THIS category explicitly. The branchdocket.md criterion 2 restates it verbatim. The discover docstring's carve-out ("never touches a manual entry, and refreshes the derived @effort seats...", seats.py:195-197) is the code amending the plan, not the plan; this repo's own practice (grok's documented omission and kimi's DECLARED wrapper-order deviation, seat_catalog.py:16-31) shows deviations get recorded at their site under a mandate — no owner ruling or docket text sanctions this one, and the plan-demanded test does not exist (test_rediscover_marks_absent_never_deletes covers only a non-effort manual seat under a shrunk PATH, tests/test_seats.py:147-167; test_add_effort_derivation covers only creation/refusals, :318-331), which is how 466-green masks it.
- Judgment calls, named: (A) I weighed the purposive defense — the exact-match guard means only machine-derived-form entries are refreshed, never a customized command — and rejected it as the criterion: the plan's parenthetical rules on exactly this category; a hand-typed `seats add SEAT@EFFORT --command` entry that coincides with the derived form is also rewritten (add_seat and add_effort_seat seats are indistinguishable, both source="manual"), and the code comment itself concedes the exact-match cases ARE clobbered (seats.py:241-245). The plan-consistent remedy for a stale derived seat already exists: `seats check` FAILs the non-resolving head (seats.py:334-336) and the operator re-derives. (B) Scope: branch-fold-r7.diff did not add this code, but the docket's exhaustive-enumeration rule ("unless this fold's change set or your sweep implicates it") keeps standing D2 in scope. (C) Aggravation: the rewrite also fires implicitly through the upgrade trigger — ensure_current -> discover runs on every `seats`/`open` invocation after a version bump (__main__.py:489, 547) — so a tool upgrade can rewrite the operator's entry as a side effect of `seats list`, not only of an explicit re-discovery.
- Retraction of my sealed verdict: my sealed D2 evidence cited only the absent-marking loop (seats.py:254-259 marks absent, deletes nothing, skips source!="catalog") — true but incomplete; it never examined the derived-rewrite loop at seats.py:236-253. That omission is why my sealed PASS was wrong.

EVERYTHING ELSE RE-VERIFIED INTACT (no other blocker establishable): C1 — absent catalog seats FAIL in check with the removal remedy named (seats.py:329-332; exit 3 only when fails nonempty, __main__.py:565/575; never-smoked INFO / stale WARN, seats.py:338-350), remove_seat refuses only PRESENT catalog seats (seats.py:474-478); pinned by tests/test_seats.py:162-165, 344-349. C2 — the bool guard (seats.py:579-584) pinned by test_profile_version_bool_refuses (tests/test_open.py). C4 — smoke_at AND smoke_result verbatim (src/debate/opening.py:312-313, 318-321) pinned by test_open_provenance_carries_smoke_result. C3 rejection stands — version 0.6.0 (src/debate/__init__.py:42, pyproject.toml:7), no 0.7.0 release, matching the plan Non-goal (plan:767) quoted in the docket. D1 — single-seat rule statically enforced (tests/test_seats.py:43-51; codex/glm/deepseek/kimi entries carry the verified pin), grok's absence and kimi's deviation documented (seat_catalog.py:16-31). D3 — upgrade trigger scan-only, stamp persists (seats.py:354-366, __main__.py:539-555). B2 — exempt set ("init","migrate","seats","open") (__main__.py:482). D4 — identity guard effort-blind and never covered by --yes while identical SELECTED argv always refuses (opening.py:88-106); shared-vendor slugified names (opening.py:57-65, 234-242); all validation before the first write via the channel_config seam, probe in a temp dir (opening.py:285-293); no setup.apply import (opening.py:22); provenance carries seat id, effort incl. null, exact command, smoke state. D2.5 — fail-closed profile loading and restricted picker with the file named (seats.py:558-603, opening.py:170-175, 222-229). Safety — branch-fold-r7.diff touches only opening.py, seats.py (check/remove_seat/load_profile), and the two test files; the seam's default path still reads the disk (__main__.py:133-134); channel/watcher/broker law untouched; the passing pre-existing suite pins shipped behavior.

Files checked: docket branch-docket.md, plan, branch-fold-r7.diff, collab/seat-registry-gate2-91255.debate.json (no prior-round sanction of the carve-out); export src/debate/{seat_catalog,seats,opening,__main__}.py, tests/{test_seats,test_open}.py, pyproject.toml, README.md, CHANGELOG.md.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2
- controller-config-sha256: 518663df1e2f04aefa7abd6f9b2adbaeacfd28ae031d24c41e97746d2c9e872d
- source-ref: 99410da6bd8c36f3fc65a81ea47abcfb38a55afc
- source-manifest-sha256: 57535f44843ebcfb10709f9795f68ed224b0f00fcb3d99b7231d0dfd5a2c62e1
- docket-revision-sha256: efb36a72c399621cd1c1b550c068bc85163222177f61a76f49044299e2da5b9d
- input-sha256: 132a912594428367785ab69508242a95e129b3379d910517bd43d5eaabc5b954
- requested-model: glm-5.3
- runtime-model: glm-5.3
- reasoning-effort: cli-default
- cli-version: claude-code 2.1.233 (repointed at api.z.ai)
- isolation-mode: advisory

## MSG-28 | 2026-08-17T19:35:19+00:00 | from: owner | type: close | thread: branch-seat-registry-9 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-29 | 2026-08-17T19:37:28+00:00 | from: owner | type: review-request | thread: branch-seat-registry-10 | refs: feature/seat-registry@99f77b1f3080d1a6d0b2d345a9ac8d4289be168f

REVIEW REQUEST - branch gate round 9 (fold-delta) for feature/seat-registry@99f77b1. GOAL: verify the single taxonomy fold (source=derived for @effort derivations; manual absolutely untouched; derived refreshes and is removable) resolves the round-8 finding and the three-round derived-seat tension; everything else stands per the cited record. True change set materialized as branch-fold-r8.diff. Run the full suite literally. Exhaustive enumeration applies.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 1738679782ba22023b6457d8d472b26ff88a63087bc7da0d767c91d1d2bee928
- source-ref: 99f77b1f3080d1a6d0b2d345a9ac8d4289be168f
- docket-revision-sha256: 0b172c86d964b3b32ffe6facb865e3bd6b5ff0278239d5e0e7b322b9bfc69a63
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/seat-registry-gate2-91255.debate.json", "sha256": "28ece9b0eb0f5b7a722da4f38bca410dea6c2c76ea7b1eb95025db803dc56d40", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-15-seat-registry-and-debate-open.md", "sha256": "427699664af12e94cf00beea2cb22783b96dc27d991e20b90bbc74f81db580c7", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-docket.md", "sha256": "a0d107e5afdd52be1b12b6ddaa0e07a02633053ccd8e381a2a8344ddc304f56b", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/seat-registry-gate2-91255/branch-fold-r8.diff", "sha256": "4449fc0eee57e9c58b84f0724780b9c76ae13ce4d14eecd0caa12af094edb013", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "77b7e77d04521bf593e8cac9cfd8c9c31f3f5c4053926604b8c6f867ce68e6ff", "glm": "e441d4018de1bc7eaafa7fd7306f0f5edeb4f38936d7f07fbcf2ba1f85e631e2"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "091bc3bda65deab432d08f96af355ca7b5bed33f1dcb7bd2913f6b4617fd2a02", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "glm": {"authentication_mode": "z.ai key self-sourced from ~/.secrets by the child shell; never in config or argv", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.233 (repointed at api.z.ai)", "command_sha256": "0bbae649721f1584291bc1970a9c89a0a26b06d5c90b91260788241a9d5d0396", "cost_mode": "api", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "glm-5.3", "isolation_mode": "advisory", "party": "glm", "permission_policy": "read-only source export; safe mode, settings sources disabled; Read/Grep/Glob plus test-only Bash allowlist", "provider": "zhipu", "reasoning_effort": "cli-default", "requested_model": "glm-5.3", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "1e56fbc9af931067b27a8474c1a8ba07116b5ddc5c98dc88bee87e322b01d3b5", "glm": "ed31881f3aff2ca21b69267383a246f613f33b183a91cdd23866fe066d44fb92"}

## MSG-30 | 2026-08-17T19:43:57+00:00 | from: owner | type: close | thread: branch-seat-registry-10 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error
