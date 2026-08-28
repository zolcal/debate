
## MSG-1 | 2026-08-26T03:42:08+00:00 | from: owner | type: review-request | thread: automatic-start-branch | refs: feature/automatic-debate-start-and-sequences@85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb

# Whole-branch gate docket

Review target:
`feature/automatic-debate-start-and-sequences@85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb`

Base:
`8b74f1b65ada428bd9a5eb7f0a6583f70686ee5e`

Goal: determine whether the complete branch is safe and coherent for the automatic
Debate-start and multi-checkpoint behavior approved in
`/home/zoltan/Projects/debate/docs/plans/2026-08-25-automatic-debate-start-and-sequences.md`.

Review domain:

- the 13 changed tracked files in the exact branch commit;
- preparation JSON/human parity and deterministic pair ordering;
- current-project-only remembered defaults and open-time drift checks;
- per-choice retry-inclusive budgets and the product cap-12 rule;
- degraded post-open registry-save handling;
- installed Codex/Claude onboarding guidance and fresh sequence checkpoints;
- active documentation, hook, manifest, and release-text coherence; and
- tests for atomicity, compatibility, zero-call preparation, and sequence stops.

Acceptance criteria:

1. The reviewer independently checks out the exact branch SHA and verifies the ref.
2. Every direct product start prepares before writes or calls and presents explicit
   keep/change/cancel behavior without exposing an internal command to the owner.
3. A valid previous pair is scoped to the current project and is the explicit Enter
   default; global/cross-project pair memory is not used or written by product open.
4. Final open rejects preparation/menu/profile/seat/budget drift before writes.
5. New ordinary and release-gate product channels persist `thread_cap: 12`; there is
   no active four-review, four-launch, cap-5, or eight-launch rule.
6. Each sequence checkpoint performs fresh preparation and confirmation, pins its
   pair within the channel, and carries no authorization to the next checkpoint.
7. ERROR, NO_PASS, cap exhaustion, invalid/changed ref, cancellation, or degraded
   pair persistence stops the sequence; only explicit resume can start a later gate.
8. The reviewer runs fresh relevant tests from the checked-out source rather than
   relying only on executor evidence.

Executor verification on the exact committed content:

- full pytest: 892 passed, 1 skipped in 137.21 seconds;
- focused pytest: 166 passed in 4.91 seconds;
- Ruff: clean with `--no-cache`;
- mypy: clean for 57 source files with a project-local cache;
- `git diff --check`: clean;
- committed archive SHA-256:
  `f306f50e8379493a1160d84ea9dc3853bf3db9e8c277c8f3a1a44142a846a7b9`;
- committed plugin content-manifest SHA-256:
  `5c94e9047c58d2925bbe5a195f0eb701ed326ed1799100d29951e5663899cc76`;
- final isolated Codex and Claude zero-call smokes: PASS; and
- final three-checkpoint fake fixture: PASS with zero seat calls.

Stop rule: issue PASS only if the exact branch is merge-ready within this docket.
Otherwise batch all actionable findings in one verdict. Do not merge, push, tag,
install over live hosts, or publish.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 42dc5ad8784dc1be56b8487ea89563990fa7b26b9b9c44bef9e2e5ef772ecc97
- source-ref: 85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb
- review-contract: {"goal": "Determine whether the complete automatic Debate-start branch is merge-ready.", "review_contract_basis": "recorded", "review_domain": "The exact branch commit and pinned Slice D docket.", "review_mode": "release-gate", "stop_rule": "PASS only if the exact branch is merge-ready; otherwise batch actionable findings."}
- docket-revision-sha256: 035b05ffa30d994c9d7834b27377d405cf5cc80ef411f3a878d23ab66e02ef6a
- docket-files: [{"path": ".release-acceptance/automatic-debate-start/slice-d-20260825/branch-gate-docket.md", "sha256": "d18c0ce9aa1345d2de70bd04a1cb86dcf3f806da028dc28b1e9477da014a1cd0", "tracked_at_source_ref": false}]
- profile-sha256: {"claude": "eb6cf3804afe933dafdbdfa30ccc30d4b08aaeacf1d0eb76d999ebf15725bef5", "stealth": "de8d5f2a11518aa42d6a15073aae205b7530d7c985055ecf722e33fef8192c66"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "2a06fefb95b053c43a0e052d9f86dc9db761945c8094f45f92cd50285107a75d", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "4010f2053475bb73e7548583330e2ad5c3568c0816a6455b2a7319b9243fcef2"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 2, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "stealth": {"authentication_mode": "the declared credential is inherited by name only at launch; its raw value is visible to the seat process and tools but is not serialized", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "4fc020a335d1acdb93c37d23f0a9db980f3057452b12d28f7115cb52dd2c14f9", "cost_mode": "api", "credential_env": ["OPENROUTER_API_KEY"], "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "4010f2053475bb73e7548583330e2ad5c3568c0816a6455b2a7319b9243fcef2"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "OPENROUTER_API_KEY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "stealth", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "stealth", "reasoning_effort": "default", "requested_model": "ox-alpha", "result_schema_version": 2, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "02d2eafac82836a190eb76907af6c56fe788ec7d221f37fba765cd085a8d3b2b", "stealth": "7a6f924b9030b082fd2591e1f188ac6681a6983efd723ffacf62325f8050d4b0"}

## MSG-2 | 2026-08-26T04:02:26+00:00 | from: claude | type: verdict | thread: automatic-start-branch | refs: -

# Whole-branch gate: PASS

I worked adversarially: I assumed each criterion was broken and tried to break it, then accepted it only when my attempt failed. I wrote an independent 10-probe suite **outside** the export (`claude-review-work/test_adversarial_probe.py`) driving the real CLI, in addition to running the project's own tests.

## Criterion 1 - exact SHA and ref

`git rev-parse feature/automatic-debate-start-and-sequences` printed `85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb`; the branch tip equals the review target. Rather than mutate the owner's working tree with a checkout (it has uncommitted changes), I pinned the artifact read-only and **stronger**: I hashed every file in the commit tree against the export. `compared=92 mismatches=0`. The only tree entries absent from the export are the 13 live `collab/` channel files, which this pass is forbidden to read. Re-run after all testing: `export drift after review: 0`.

## Criteria 2, 4 - prepare before writes; drift rejected before writes

`open --brokered` without `--pair` now returns a read-only preparation (exit 0) instead of the old refusal-with-menu. `open_debate_brokered` **re-runs** `prepare_brokered_open` itself (opening.py:1391) before any write, so the engine never trusts the host's echo.

My probes (all passed, i.e. all breaks failed):
- `test_probe_open_without_preparation_echo_refuses`: an open with `--pair` but no echo is refused (`--preparation-revision` and `--confirmed-budget` named); targets stay byte-empty.
- `test_probe_profile_drift_refuses_with_byte_empty_targets`: I mutated `debate-profile.json` after preparation; open refused with "changed after ... prepare a fresh menu" and `_target_state(project)` was **identical** before/after - `collab/` and `.debate/` untouched.
- `test_probe_forged_budget_refuses`: `--confirmed-budget 99,99` refused with "confirmed review budget does not match"; no writes.
- `test_probe_pair_outside_prepared_menu_refuses`: a pair removed from the allowlist after preparation refused; no writes.

Keep/change/cancel is explicit in the rendered lines: "Enter keeps A + B; choose a number to change; cancel stops." with no default, "Pick one numbered pair; cancel stops." The raw invocation stays agent-side - SKILL.md marks `--brokered` an "agent-only engine fact" and keeps raw commands "behind a 'details' answer".

## Criterion 3 - current-project-only pair memory

`prepare_brokered_open` calls `remembered_pair(..., include_global=False)` (opening.py:1225) and `open_debate_brokered` writes **only** `registry.last_pair[project]` (opening.py:1697) - the legacy `open_debate` still writes the global key, but that is not the product path.

`test_probe_global_pair_memory_is_never_used_or_written`: I seeded `last_pair[""]` and `last_pair["/some/other/project"]` with a valid, admissible pair and left the current project with none. The preparation returned `default_pair: null`, `default_reason: null`, `budget_scope: "per-choice"`, every `choice.default` false, and rendered "Pick one numbered pair" with **no** "Enter keeps" line. After a successful open, both foreign keys were byte-unchanged and only the current project key was written. A second preparation then showed that pair as `default_pair` with `default_reason: "previous-project-pair"` and an "Enter keeps" line - so the valid previous pair is the explicit Enter default, scoped to this project.

## Criterion 5 - cap 12, no stale rules

`test_probe_cap_twelve_persists_and_cap_five_refuses` (parametrized `ordinary` and `release-gate`): preparation reports `thread_cap 12`, `seat_turn_ceiling 11`, `nested_launch_ceiling 22` for **both** modes; the written record persists `thread_cap: 12`, `managed_version: 2`, and `review_contract` `{thread_cap 12, seat_turn_ceiling 11, nested_launch_ceiling 22, supervisor_entries_consume_cap true}`. `--cap 5` is refused with "thread cap 12 exactly".

My own grep for `cap 5|cap-5|four (vote|review|seat|nested|launch)|eight (nested|launch)` across active `.md`/`.py`/`.json`/hook files found **no** active prose hits - only the guard tests that forbid them and legacy non-product channel fixtures. `test_active_product_text_has_one_cap_twelve_policy` enforces this over README, CHANGELOG, SKILL.md, opening.py and __main__.py, and passed.

## Criteria 6, 7 - sequence checkpoints and stops

Budgets are per-choice and retry-inclusive (`review_budget`: `launches = (cap-1) * (max(retry_limits)+1)`), computed per pair from each adapter's actual `retry_limit`, not recalculated by the host.

`test_probe_second_checkpoint_cannot_reuse_first_confirmation` is my strongest sequence probe: I opened checkpoint one, then replayed **its exact** `preparation_revision` and budget for checkpoint two. It was refused with "prepare a fresh menu" and left targets byte-empty - a prior checkpoint's confirmation carries no authorization forward. The repo's own `test_three_checkpoint_policy_stops_on_error_and_resumes_with_fresh_default` covers fresh preparation per checkpoint, three distinct channels, stop-on-ERROR, and resume-with-fresh-default.

Degraded persistence: `test_probe_degraded_registry_save_exits_three`. I made the registry directory unwritable after a successful open. The CLI printed the hints, then `DEGRADED: channel <name> exists, but its project default was not saved ... Stop this sequence; do not open a replacement channel automatically.` and returned **exit 3**, with the channel intact and exactly one record. SKILL.md Flow 3 step 4 lists NO_PASS, ERROR, cap exhaustion, changed/invalid ref, cancellation and degraded save as sequence stops, and step 5 requires fresh preparation on resume.

## Criterion 8 - fresh tests from the checked-out source

Run from the export with `PYTHONPATH=<export>/src`, `TMPDIR` and `--basetemp` inside my run folder (nothing written to /tmp; `/tmp/pytest-of-$USER` entry count: 0):

- full pytest: **892 passed, 1 skipped in 142.92s** - matches the executor's claim exactly.
- my focused selection of the 7 changed test files: **175 passed in 87.03s**. (The docket cites 166 for its focused set; mine is a different, larger selection, not a contradiction.)
- `ruff check --no-cache .`: **All checks passed!**
- `mypy .`: **Success: no issues found in 57 source files** - matches the claimed file count.
- `git diff --check 8b74f1b6 85aecec8`: clean, exit 0.
- my adversarial suite: **10 passed**.

Coherence of hook/manifest/skill/release text is guarded by `test_plugin_manifests.py` and `test_release_sync.py`, both green; the hook now routes every new channel start to `debate-onboarding`, and `skills/debate/SKILL.md` correctly defers new-debate starts to that skill, so the two skills do not contradict each other.

## Non-blocking observations (not gating, recorded for the owner)

1. `preparation_revision` covers project, mode, cap, docket bytes, seat/profile state and every choice's budget, but **not** `deliberation_input` or `author_vendor`. Changing either between prepare and open would not trip the drift check. Neither alters the menu or the budget (`retry_limit` is 1 on both adapter shapes), and `author_vendor` is separately validated at open against catalog/registry vendors, so this is outside criterion 4's enumerated drift set. Worth folding into the hash if the recorded author relationship is ever owner-confirmed.
2. I could not reproduce the executor's `committed archive SHA-256` and `committed plugin content-manifest SHA-256`: no such artifact is committed in the pinned tree (my grep for both hashes found nothing), so they are build-side evidence I cannot independently confirm. Neither appears in the eight acceptance criteria, so this does not gate the verdict - I flag it only so the claim is not read as reviewer-confirmed.

## Verdict

Every one of the eight acceptance criteria holds on my own fresh evidence, and each attempt to break criteria 2 through 7 failed. The exact branch is merge-ready within this docket. I did not merge, push, tag, install, or publish, and I made no change to the export or the repository.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 1e4f6d4dc4ad4650f0440e4854194f79f41b01c524d96a9dec2a5264b587b7ed
- phase: sealed
- captured-at: 2026-08-26T04:02:26+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "git rev-parse feature/automatic-debate-start-and-sequences", "exit_status": 0, "output": "85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb"}, {"command": "for each path in `git ls-tree -r --name-only 85aecec8` (excluding collab/): compare `git cat-file blob 85aecec8:$f | sha256sum` to `sha256sum <export>/$f`", "exit_status": 0, "output": "compared=92 mismatches=0  (re-run after all testing: 'export drift after review: 0')"}, {"command": "cd <export> && TMPDIR=<work>/tmp PYTHONPATH=<export>/src .venv/bin/python -m pytest -q -p no:cacheprovider --basetemp=<work>/tmp/full", "exit_status": 0, "output": "892 passed, 1 skipped in 142.92s (0:02:22)"}, {"command": "cd <export> && TMPDIR=<work>/tmp PYTHONPATH=<export>/src .venv/bin/python -m pytest tests/test_open.py tests/test_pairing.py tests/test_deliberation_input.py tests/test_field_batch.py tests/test_plugin_manifests.py tests/test_release_sync.py tests/test_session_start_hook.py -q -p no:cacheprovider", "exit_status": 0, "output": "175 passed in 87.03s (0:01:27)"}, {"command": "cd <export> && .venv/bin/ruff check --no-cache .", "exit_status": 0, "output": "All checks passed!"}, {"command": "cd <export> && .venv/bin/mypy --cache-dir=<work>/mypy-cache .", "exit_status": 0, "output": "Success: no issues found in 57 source files"}, {"command": "git diff --check 8b74f1b65ada428bd9a5eb7f0a6583f70686ee5e 85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb", "exit_status": 0, "output": "(no output) diff --check exit=0"}, {"command": "cd <work> && TMPDIR=<work>/tmp PYTHONPATH=<export>/src:<export>/tests .venv/bin/python -m pytest test_adversarial_probe.py -q -p no:cacheprovider", "exit_status": 0, "output": "10 passed in 1.34s -- independent probes: zero seat calls through preparation+open; global/cross-project pair memory neither offered nor written; profile drift refused with byte-empty targets; forged budget 99,99 refused; open without preparation echo refused; cap 12 persisted for ordinary and release-gate with --cap 5 refused ('thread cap 12 exactly'); degraded registry save -> exit 3 with DEGRADED + 'Stop this sequence'; pair outside prepared menu refused; stale checkpoint-one confirmation cannot open checkpoint two ('prepare a fresh menu')"}, {"command": "git diff --stat 8b74f1b65ada428bd9a5eb7f0a6583f70686ee5e 85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb", "exit_status": 0, "output": "13 files changed, 1013 insertions(+), 139 deletions(-)"}, {"command": "grep -rniE \"cap 5|cap-5|four (vote|review|seat|nested|launch)|eight (nested|launch)\" --include=*.md --include=*.py --include=*.json --include=session-start . | grep -v CHANGELOG", "exit_status": 0, "output": "only guard-test patterns (tests/test_plugin_manifests.py:102 'cap 5' not in skill; tests/test_release_sync.py:38-39 forbidden regexes) and legacy non-product thread_cap=5 fixtures; no active product prose hits"}], "status": "performed"}

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: eb6cf3804afe933dafdbdfa30ccc30d4b08aaeacf1d0eb76d999ebf15725bef5
- controller-config-sha256: 42dc5ad8784dc1be56b8487ea89563990fa7b26b9b9c44bef9e2e5ef772ecc97
- source-ref: 85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 02d2eafac82836a190eb76907af6c56fe788ec7d221f37fba765cd085a8d3b2b
- docket-revision-sha256: 035b05ffa30d994c9d7834b27377d405cf5cc80ef411f3a878d23ab66e02ef6a
- input-sha256: d033cb7df397ae5a0c2608a0b8119351f9072956080fa2e56aab88df2d750a1d
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 5e39ac1bf871e8ce3c1c969bbaecb0276e37c18cd03aacee588988519cb2d5d9
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 551f833faa3b94dec930067cb00840f211ffa237e18eba4f76aac247aa0198a7
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-3 | 2026-08-26T04:02:26+00:00 | from: stealth | type: verdict | thread: automatic-start-branch | refs: -

Whole-branch release-gate review of feature/automatic-debate-start-and-sequences@85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb against the Slice D branch-gate docket. Ref: the read-only snapshot carries no .git, so the pin was verified via the manifest chain — sha256sum stealth.manifest.json printed 7a6f924b9030b082fd2591e1f188ac6681a6983efd723ffacf62325f8050d4b0 (the declared manifest hash), an independent re-hash of all 92 files reported 'mismatches: NONE', and the manifest's source_ref equals the docket target 85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb. Criterion 2: prepare_brokered_open (src/debate/opening.py:1159) performs admission, adapter construction and budgets fully in memory ('creates no channel/runtime state and invokes no seat'); 'debate open --brokered' without --pair prints the numbered menu/JSON and exits before any write (__main__.py:1138-1155); brokered_preparation_lines renders 'Enter keeps A + B ... cancel stops'; skills/debate-onboarding/SKILL.md Flow 2 keeps internal flags agent-only and its plain-words rule bans internal vocabulary user-facing; pinned by tests/test_open.py::test_product_preparation_is_read_only_project_local_and_human_json_agree (registry/profile bytes unchanged, no collab/, no .debate/). Criterion 3: product preparation calls remembered_pair(..., include_global=False) (opening.py:1219-1226) and the product open writes only registry.last_pair[project] (opening.py:1697); pinned by test_product_preparation_ignores_global_and_other_project_memory; the legacy global write at opening.py:940 belongs to the non-product v1 path. Criterion 4: open_debate_brokered re-prepares and refuses preparation_revision mismatch, confirmed_budget mismatch, absent menu membership, allowlist/data-policy, seatability, identity and admission drift before channel.init_channel (opening.py:1391-1557); the CLI refuses an open lacking --preparation-revision/--confirmed-budget (__main__.py:1161); pinned by test_changed_profile_or_confirmed_budget_refuses_before_any_write (asserts no collab/ and no .debate/ created). Criterion 5: resolve_review_thread_cap forces PRODUCT_THREAD_CAP=12 for ordinary and release-gate; init_channel persists thread_cap in the channel config; a grep count scan of README.md, CHANGELOG.md, PROTOCOL.md, hooks/HOOK-CONTRACT.md, both SKILL.md files, docs/case-study.md, examples and all src modules returned 0 occurrences of four-review/four-launch/cap-5/eight-launch phrasing; test_release_sync::test_active_product_text_has_one_cap_twelve_policy pins it. Criteria 6-7: skills/debate-onboarding/SKILL.md Flow 3 requires fresh preparation plus fresh current-turn confirmation at each checkpoint, pins the pair within the channel, carries no authorization forward, and stops the sequence on terminal NO_PASS, ERROR, cap exhaustion, changed/invalid artifact ref, owner cancellation or degraded remembered-pair save, resuming only with fresh preparation; the controller closes cap exhaustion as NO_PASS/thread-cap-exhausted with TERMINAL_RESULTS=(PASS,NO_PASS,ERROR); a failed registry save exits 3 printing 'DEGRADED: channel ... exists, but its project default was not saved (...) Stop this sequence; do not open a replacement channel automatically.' (__main__.py:1230-1238), pinned by tests/test_field_batch.py (rc==3); tests/test_open.py::test_three_checkpoint_policy_stops_on_error_and_resumes_with_fresh_default proves stop-on-ERROR, explicit resume with fresh preparation, distinct per-checkpoint refs/dockets, thread_cap 12 records, and zero seat invocations. Criterion 8: site-packages contained a stale debate 0.7.0, so all runs set PYTHONPATH to <export>/src (import check printed '.../stealth/src/debate/__init__.py 0.8.0'); runs executed from a scratch dir under the run's own export folder with no cache writes into the tree (leak scan clean, scratch removed afterwards). Full pytest: '892 passed, 1 skipped in 148.52s', independently matching the executor's 892 passed, 1 skipped. Focused Slice D files (test_open, test_release_sync, test_plugin_manifests, test_onboarding*, test_session_start_hook): '142 passed in 8.46s'. Ruff 0.7.1 --no-cache: 'All checks passed!'. Strict mypy (per pyproject, cache redirected to the scratch dir because the tree is read-only): 'Success: no issues found in 57 source files'. Not independently reproducible in this sandbox and not contradicted by any finding: the executor-declared archive and plugin content-manifest SHA-256s (no recipe in-repo; content byte-pinned instead by the verified manifest), the isolated installed-host Codex/Claude smokes and fake-fixture smoke (live hosts are outside the allowed evidence domain), and 'git diff --check' (no .git in the snapshot). Verdict: merge-ready within this docket; no blocking findings.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 1e4f6d4dc4ad4650f0440e4854194f79f41b01c524d96a9dec2a5264b587b7ed
- phase: sealed
- captured-at: 2026-08-26T04:02:26+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence: {"items": [{"command": "cd <export-parent> && sha256sum stealth.manifest.json", "exit_status": 0, "output": "7a6f924b9030b082fd2591e1f188ac6681a6983efd723ffacf62325f8050d4b0  stealth.manifest.json"}, {"command": "python3 -c \"re-hash all 92 manifest entries against files\" (json.load stealth.manifest.json; hashlib.sha256 per file)", "exit_status": 0, "output": "files in manifest: 92 / mismatches: NONE / source_ref = \"85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb\""}, {"command": "PYTHONPATH=$STEALTH/src PYTHONDONTWRITEBYTECODE=1 python3 -m pytest $STEALTH/tests -q -p no:cacheprovider --basetemp=$SCRATCH/.pytest-tmp", "exit_status": 0, "output": "892 passed, 1 skipped in 148.52s (0:02:28)"}, {"command": "PYTHONPATH=$STEALTH/src PYTHONDONTWRITEBYTECODE=1 python3 -m pytest $STEALTH/tests/test_open.py $STEALTH/tests/test_release_sync.py $STEALTH/tests/test_plugin_manifests.py $STEALTH/tests/test_onboarding.py $STEALTH/tests/test_onboarding_flow.py $STEALTH/tests/test_onboarding_recovery.py $STEALTH/tests/test_session_start_hook.py -q -p no:cacheprovider", "exit_status": 0, "output": "142 passed in 8.46s"}, {"command": "ruff check --no-cache . (in $STEALTH)", "exit_status": 0, "output": "All checks passed!"}, {"command": "mypy --cache-dir=$SCRATCH/.mypy-cache . (strict, in $STEALTH)", "exit_status": 0, "output": "Success: no issues found in 57 source files"}, {"command": "grep -rniEc 'four.review|four.launch|cap.?5\\b|eight.launch' README.md CHANGELOG.md PROTOCOL.md hooks/HOOK-CONTRACT.md skills/*/SKILL.md docs/case-study.md examples/*.md src/debate/*.py", "exit_status": 0, "output": "every counted file reported 0 occurrences"}], "status": "performed"}

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: de8d5f2a11518aa42d6a15073aae205b7530d7c985055ecf722e33fef8192c66
- controller-config-sha256: 42dc5ad8784dc1be56b8487ea89563990fa7b26b9b9c44bef9e2e5ef772ecc97
- source-ref: 85aecec83bc77f9aca87b27a9e67d4dcaf19e9bb
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: 7a6f924b9030b082fd2591e1f188ac6681a6983efd723ffacf62325f8050d4b0
- docket-revision-sha256: 035b05ffa30d994c9d7834b27377d405cf5cc80ef411f3a878d23ab66e02ef6a
- input-sha256: 1f8c99c9d9d1a49e4544e814952dab2107c719bd1d0ed41f3e368998163112e8
- requested-model: ox-alpha
- runtime-model: ox-alpha
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 10c5464f9eee250345689da601b3fcaf824ca1780d6bec9a40bd7a216c737c3f
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: f67abbbcc0488b85d3eca16eacc5e2462689996895d35e10cb6867031e79d20e
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-4 | 2026-08-26T04:02:27+00:00 | from: owner | type: close | thread: automatic-start-branch | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes. Runtime size at close: 27265180 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel automatic-start-branch-gate-76079 --config /home/zoltan/Projects/debate/.debate/channels/automatic-start-branch-gate-76079/watcher.json

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
