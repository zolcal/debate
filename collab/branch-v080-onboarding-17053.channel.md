
## MSG-1 | 2026-08-19T21:55:57+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-1 | refs: feature/installation-onboarding-v080@86ff063c1f3926d313f16d12772d3ef50269c6ad

Branch review request: feature/installation-onboarding-v080 at 86ff063 implements the approved v0.8.0 installation-driven onboarding plan (plan gate PASS at plan-v080-onboarding-59142 MSG-13). Nine commits; the true change set vs main is materialized in the docket as branch-v080.diff, and the approved plan doc rides in the docket (docs/plans/ is untracked by design). Verify per branch-docket.md: plan conformance, correctness of the onboarding/brokered-open/hook code on your own reading, test adequacy, no unrelated changes, and the exact full-suite pytest command. Verdicts cite your own fresh evidence from the export, never this request. Name every blocking finding establishable in your pass.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 5930541e6aa0074176e95c0a8938570b27952e27b5ca8c35aef87c1ca08813f1
- source-ref: 86ff063c1f3926d313f16d12772d3ef50269c6ad
- docket-revision-sha256: 83d2bdf1af78221e861725c6c7b98830720a7cf434adc82bbd9dc4fad197e94b
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket.md", "sha256": "7d38769288a3630a864b29175ae597faa7530e5488b5c67a79ff2fe43e1eb4c3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080.diff", "sha256": "9cf7940bd791851f4b42360e689def60745228ccc78ad61cb46860ad11948bb3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher.json", "sha256": "5930541e6aa0074176e95c0a8938570b27952e27b5ca8c35aef87c1ca08813f1", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a8385f7d027929e3c442fa37eca1083fe7cd74762742e5e0c27284aa9992ffa1", "opus": "3c8984c41ff6e00743a724361eb3f82901cfe15a281fdb618edb92905abc4597"}

## MSG-2 | 2026-08-19T22:06:59+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-1 | refs: -

## Verification run (docket criterion 5)

Command, run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/86ff063c1f3926d313f16d12772d3ef50269c6ad/opus` (confirmed by `pwd`), no prefixes/suffixes/pipes:

`python -m pytest -q`

Result: `519 passed, 1 skipped in 21.68s` — exit 0. Criterion 5 is satisfied. Criteria 1 and 3 are not, on the evidence below.

## Blocking findings

### B1. Cost mode is absent from the entire onboarding surface, so §3.2's approval table and §4.3's provenance cannot be honest

The plan's user-visible acceptance contract (§3.2) requires the approval table to contain five items, one of which is "smoke state **and cost mode** (`subscription quota`, `metered API`, or `local compute`)". §4.3 requires the brokered open to "preserve exact provider/model/effort/command, authentication mode, **cost mode**, permission policy, and author relationship in provenance". §8 requires "The UI states subscription quota, API metering, or local compute before confirmation" of smoke.

Nothing in the branch models cost mode for a seat:

- `src/debate/seats.py:34-45` — the `Seat` dataclass has `vendor, submodel, effort, commands, source, present, smoke`. No cost field.
- `src/debate/seat_catalog.py:43-54` — `CatalogEntry` has `vendor, binaries, submodels, known_efforts, invocation, submodel_argv, effort_argv, notes`. No cost field.
- `src/debate/onboarding.py:158-177` — `_candidates()` emits exactly `seat_id, vendor, submodel, effort, command, source, present, smoke, existing`. No cost mode, so `inspect --json` cannot supply one.
- `skills/debate-onboarding/SKILL.md:33-37` — the table the skill is told to present is "seat id, vendor/model identity, how the model selection is pinned (the command), present or missing, smoke state, and source". Cost mode is the one §3.2 bullet dropped.
- `skills/debate-onboarding/SKILL.md:47-48` — the skill nonetheless instructs the agent to "state the cost mode (subscription quota, metered API, or local compute) before the user decides" on smoke. Since no engine surface returns that value, the agent must invent the spend disclosure. That is the exact failure mode §8 and the project's honesty rules exist to prevent.
- `src/debate/opening.py:383` — `_brokered_adapter()` hard-codes `"cost_mode": "unknown"`, and `tests/test_onboarding_flow.py:362` pins that (`assert block["cost_mode"] == "unknown"`). I confirmed `"unknown"` is a pre-existing legal value (`src/debate/controller.py:34`, `COST_MODES = ("subscription", "api", "local", "unknown")`), so this validates — but it means §4.3's "preserve exact ... cost mode ... in provenance" records nothing about the seat. The code comment at `opening.py:365-367` is candid about this ("what the registry does not know is recorded as unknown"); the gap is that the plan required the registry to know.

Blocking under criterion 1: the diff does not implement a named element of the approved plan's acceptance contract, and the consequence lands on a user spend decision.

### B2. Non-interactive banner suppression has no host trigger established anywhere in the export; its test pins a field the branch's own hook-contract spike does not attest

Plan §4.4 requires that for "non-interactive sessions (`codex exec`, headless/automation runs) ... the setup notice is suppressed or reduced to one short context line — an unconfigured project in an automation loop must not emit a full onboarding banner on every run." §6's verification matrix lists "non-interactive suppression" as a required hook case.

The implementation has exactly two triggers:

- `hooks/session-start:45` — `quiet = os.environ.get("DEBATE_ONBOARDING_QUIET") == "1"`
- `hooks/session-start:59` — `if event.get("non_interactive") is True:`

I grepped the whole export for both names. `DEBATE_ONBOARDING_QUIET` appears only at `hooks/session-start:45` and `tests/test_session_start_hook.py:192`; nothing sets it — not `hooks/hooks.json`, not `hooks/hooks-codex.json`, not `.codex-plugin/plugin.json`, not `.agents/plugins/marketplace.json`, not `scripts/debate-plugin`. `non_interactive` appears only at `hooks/session-start:59` and `tests/test_session_start_hook.py:203`.

The branch's own Slice 1A spike record — which the plan made the first act before any hook code, and which the branch presents as verified against live `codex-cli 0.148.0` / `claude-code 2.1.235` — enumerates the host input fields at `hooks/HOOK-CONTRACT.md:12-13`: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`. `non_interactive` is not among them. `permission_mode` is documented but the hook never reads it.

So on the export's own evidence, an unconfigured project in a `codex exec` loop emits the full onboarding banner on every run — the outcome §4.4 forbids. Blocking under criterion 1.

This is also a criterion 3 test-adequacy failure. `tests/test_session_start_hook.py:200-205` (`test_non_interactive_input_field_suppresses_too`) constructs `{"cwd": ..., "non_interactive": True}` itself, so it verifies the branch's own invention rather than the host contract; `test_non_interactive_suppresses_the_banner` (:188-198) sets the env var the same way. Neither pins the plan's requirement. `CHANGELOG.md:126` states the behavior as shipped — "Non-interactive sessions get one context line, never a banner" — which nothing in the export supports.

## Criteria that DID hold on my own reading (recorded so a second pass finds nothing new here)

- **Hook read-only / zero-call / exit 0 on every path**: `hooks/session-start` returns 0 on malformed input (:51-58), missing engine (:65-72), unimportable engine (:76-83), and status failure (:88-96); the only engine call is `onboarding.status` (:89). `tests/test_session_start_hook.py:208-217` snapshots mtime+size across the whole tmp tree and asserts equality after two runs.
- **Detection is never approval; approve is revision-verified, confirmed-gated, transactional**: `onboarding.py:242-276` refuses unconfirmed, empty, duplicate, unknown, and unrunnable selections and refuses a changed `candidate_revision`; `:287-315` writes and fsyncs both temp files before the first `os.replace`, so every preparation failure leaves both priors byte-identical. Verified by `tests/test_onboarding_flow.py:176-201`, which chmods the project dir and asserts both files byte-identical plus no `.debate-*` leftovers. The residual two-phase window between the two `os.replace` calls is the unavoidable POSIX one and matches the plan's stated property.
- **Brokered open mints v2, never 1, validates before the first write**: `opening.py:492/509` use `channel.BROKERED_MANAGED_VERSION`; docket-file existence (:480-485), scratch-dir loader probe (:494-497), `managed_problem()` (:498-502) and `doctor_lines(broker)` (:503-505) all precede `channel.init_channel` (:507). `watcher.py:146` guarantees `broker is not None` for v2, so `doctor_lines` is never skipped. Byte-empty-on-refusal is pinned by `tests/test_onboarding_flow.py:280, 305, 335, 384, 404`.
- **v1 bridge-seat guard**: `opening.py:250-256` refuses `{prompt}`-less seats on the legacy path; symmetric to `_brokered_adapter`'s `{input_path}`/`{result_path}` requirement (`opening.py:369-375`). Pinned by `test_v1_open_refuses_bridge_seats`.
- **Legacy behavior preserved (criterion 4)**: `opening.py:239-240` (`if profile is not None`) and `opening.py:143-144` (`profile is None or seat_id in profile.allowlist`) keep the 0.7 missing-profile-is-unrestricted reading for the direct CLI; `onboarding.py:135-136` diverges only on the product path, and `README.md` (diff lines 259-272) states the divergence explicitly, as §4.2 requires.
- **Stub debate to typed close**: `tests/test_onboarding_flow.py:417-482` drives approve → brokered open → `broker-open` → `watch --until-close` → `status` (`phase: terminal`, `terminal_result: PASS`, `close_reason: party-vote-agreement`) → `verify`, and asserts `from: owner | type: verdict` is absent from the mailbox.
- **`.gitignore`, MANIFEST.in, version lockstep**: `.acceptance/`, `.release-acceptance/`, `.worktrees/` added (diff :94-100); `MANIFEST.in` is commented and intentional with grafts and prunes; `0.8.0` agrees across `pyproject.toml`, `src/debate/__init__.py`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, pinned by `tests/test_release_sync.py` (`.agents/plugins/marketplace.json` carries no version, so "all three plugin manifests" is met).
- **No unrelated changes**: the 24 paths in `branch-v080.diff` all fall under plan §7, plus `hooks/HOOK-CONTRACT.md` (§5 Slice 1A step 1 requires recording the spike in the branch) and `MANIFEST.in` (§7's source-manifest bullet).

## Non-blocking observations

1. **Hook manifests are not literally field-identical.** `hooks/hooks.json:5` carries `"matcher": "startup|clear|compact"`; `hooks/hooks-codex.json` omits it. The parity test (`tests/test_session_start_hook.py:229-242`) deliberately scopes itself "at the hook-entry level" and so does not see the group-level divergence, which means Codex fires on every `SessionStart` source while Claude fires on three. I read the docket's "minimal and field-identical" as aimed at the hook-entry level that the 2026-06-26 `description` incident concerned, so I am not treating this as blocking — but the divergence is real and unpinned.
2. **`debate-profile.json` lands with mode 0600.** `onboarding.py:297` uses `tempfile.mkstemp`, whose 0600 mode survives `os.replace` (:307). The plan calls this a "committable" project file; git will not care, but a shared checkout will.
3. `onboarding.py:109` reaches into the private `seats._days_between`.

## Bar

Criterion 5 passed on fresh output. Criteria 1 and 3 do not hold: B1 and B2 are elements of the approved plan's contract that the diff does not implement, and B2's suite asserts a trigger the branch invented rather than the one the plan requires. NO_PASS.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 36a7d2f76e40d4b22b1d91d675fc1bbefb8c4a5c7c6e764e5745b94089450af6
- phase: sealed
- captured-at: 2026-08-19T22:02:40+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 5930541e6aa0074176e95c0a8938570b27952e27b5ca8c35aef87c1ca08813f1
- source-ref: 86ff063c1f3926d313f16d12772d3ef50269c6ad
- source-manifest-sha256: 3c8984c41ff6e00743a724361eb3f82901cfe15a281fdb618edb92905abc4597
- docket-revision-sha256: 83d2bdf1af78221e861725c6c7b98830720a7cf434adc82bbd9dc4fad197e94b
- input-sha256: f9b65341fa578c94ef91979b90252297689cc9b6061db53c4cd6c1308ac89f01
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-3 | 2026-08-19T22:06:59+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-1 | refs: -

Fresh required verification passed: `python -m pytest -q` → `519 passed, 1 skipped in 22.19s`.

Blocking findings:
1. The per-host hook manifests are not field-identical as required by criterion 1. `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/86ff063c1f3926d313f16d12772d3ef50269c6ad/codex/hooks/hooks.json:5` adds `matcher: "startup|clear|compact"`, while `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/86ff063c1f3926d313f16d12772d3ef50269c6ad/codex/hooks/hooks-codex.json:4` omits it. The parity test checks only the nested command object, so it does not pin the stated manifest-level parity claim.
2. The product cannot supply or preserve the required cost/provenance data. `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/86ff063c1f3926d313f16d12772d3ef50269c6ad/codex/src/debate/onboarding.py:164-175` returns no cost mode for approval candidates, despite the approved plan requiring the approval UI to show it. The `Seat` model has no cost, authentication, permission, or author-relationship fields. `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/86ff063c1f3926d313f16d12772d3ef50269c6ad/codex/src/debate/opening.py:377-395` therefore fabricates `author-independent` and generic authentication/permission values and records `cost_mode: unknown`; this fails the plan requirement to preserve exact provenance and can falsely satisfy the managed topology guard.

The green test suite does not cure these plan-conformance and safety failures.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 36a7d2f76e40d4b22b1d91d675fc1bbefb8c4a5c7c6e764e5745b94089450af6
- phase: sealed
- captured-at: 2026-08-19T22:06:59+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 5930541e6aa0074176e95c0a8938570b27952e27b5ca8c35aef87c1ca08813f1
- source-ref: 86ff063c1f3926d313f16d12772d3ef50269c6ad
- source-manifest-sha256: a8385f7d027929e3c442fa37eca1083fe7cd74762742e5e0c27284aa9992ffa1
- docket-revision-sha256: 83d2bdf1af78221e861725c6c7b98830720a7cf434adc82bbd9dc4fad197e94b
- input-sha256: 09dff3039c21a85cfaae32a78f09cc063d46fc6c615765949d7c4086d67e773b
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-4 | 2026-08-19T22:06:59+00:00 | from: owner | type: close | thread: branch-v080-onboarding-1 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-5 | 2026-08-19T22:19:56+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-2 | refs: feature/installation-onboarding-v080@7354ee59c85c9bcb08036f60cb41966ad2c83b1e

Fix-report and round-2 review request (fold-delta) for feature/installation-onboarding-v080, now at 7354ee5. Round 1 closed NO_PASS (MSG-4) on: cost mode absent from the onboarding surface with fabricated brokered provenance (MSG-2 B1, MSG-3.2); unattested non-interactive suppression pinning an invented input field (MSG-2 B2); hook manifests not field-identical (MSG-3.1, MSG-2 obs 1); plus profile 0600 and a private-helper reach (MSG-2 minors). Every finding is folded: declared Seat.cost_mode through the whole surface, --author-vendor-derived author relationship, spike-attested CLAUDE_CODE_ENTRYPOINT suppression with the invented field removed, deep-equal manifests, 0644 profile, public days_between. The fold diff (86ff063..7354ee5) and the full branch diff ride in the docket; compute the true change set yourself per the fold-delta clause. Verdicts cite your own fresh evidence; round-1 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 0bd16201b09fc53bf11715c7e292cb2ae235b9d69cff1fa41dbd8a4ec5aabb35
- source-ref: 7354ee59c85c9bcb08036f60cb41966ad2c83b1e
- docket-revision-sha256: be47cb3adb11a2915fa23503cf99262b026bb70ad6523169eea016abbcd205c0
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r2.md", "sha256": "fe19914c5625e25582bd7112323c2b95ef7fb15828f460433a4f8d5c3e250242", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080.diff", "sha256": "9cf7940bd791851f4b42360e689def60745228ccc78ad61cb46860ad11948bb3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r1.diff", "sha256": "32740fd1e7b966423c914bdada767b2fa14d7081128e1ae743c2e79ecc721931", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r2.diff", "sha256": "ecda81236e445b9510803ad4888ee16f94f9d76231cd106828aae3417aa59032", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r2.json", "sha256": "0bd16201b09fc53bf11715c7e292cb2ae235b9d69cff1fa41dbd8a4ec5aabb35", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "bf847b45641d7179efe35b1525f406fe267c9fa0980c2a89678bb4561a14d92a", "opus": "b8e7f7690690119f0bbe96573e6e879e19e2dd5bd6633ed67ee16b68c9e0d292"}

## MSG-6 | 2026-08-19T22:29:41+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-2 | refs: -

NO_PASS — criterion 5 passes, but the coherence sweep and the reverse check on B1 establish two blockers, plus three supporting findings.

VERIFICATION RUN (criterion 5). From the export root, literally: `python -m pytest -q` -> `521 passed, 1 skipped in 21.86s`. No failures.

TRUE CHANGE SET (computed, not taken from the fold list). `diff --git` headers of `branch-v080.diff` vs `branch-v080-r2.diff`: identical 27-file set, so the fold added no new file. Per-file section spans locate every r1->r2 growth in exactly the 12 files of `fold-r1.diff` (CHANGELOG +10, HOOK-CONTRACT +15, hooks.json -1, session-start +7, debate-onboarding/SKILL.md +7, __main__.py +40, onboarding.py +5, opening.py +28, seats.py +114, test_onboarding.py +-0, test_onboarding_flow.py +40, test_session_start_hook.py); all other sections are byte-span identical. I read the r2 seats.py section (branch-v080-r2.diff:1551-1718) line by line: every line is accounted for by r1 (registry_payload refactor, bridge-style add_seat) plus the disclosed fold. No undisclosed edit found.

FOLDS THAT DO RESOLVE THEIR FINDING. Fold 2 (MSG-2 B2): the invented `non_interactive` input field is gone from hooks/session-start; suppression is `CLAUDE_CODE_ENTRYPOINT` sdk-cli/`sdk-` prefix plus `DEBATE_ONBOARDING_QUIET=1`, attested in HOOK-CONTRACT.md:39-52, exercised by tests/test_session_start_hook.py:201-215 (sdk-cli suppresses, "cli" keeps the banner). Fold 3 (MSG-3 finding 1): `matcher` removed from hooks/hooks.json, deep equality pinned by `test_manifests_are_field_identical_documents`. The `_days_between` -> `days_between` rename with compat alias (seats.py:1718) is consistent across onboarding.py:109 and opening.py:196.

BLOCKER 1 — the branch's own README documents a command the branch's own code now refuses. README.md:205-206 ships `debate open --brokered --root ./collab --label market-research \ --pair alpha/fake,beta/fake`. src/debate/__main__.py:634-638 now raises unconditionally when `--author-vendor` is absent: "refused: --brokered needs --author-vendor". `grep` for `author-vendor` across README.md returns nothing. That example block was added by THIS branch (branch-v080-r2.diff:260-265), and fold 1 made it a guaranteed failure without updating it, while SKILL.md:67-71 and the CHANGELOG were updated. Copy-paste of the primary product doc fails 100% of the time. Criterion 4 / sweep (c).

BLOCKER 2 — fold 1 does not actually resolve MSG-2 B1 for the seats the product creates: `cost_mode` is undeclarable on the product path. The only writers of a non-"unknown" cost_mode are `add_seat` for a BRAND-NEW manual seat (seats.py:443-459) and `add_effort_seat` inheritance (seats.py:503). Discovery (seats.py:225-242) never sets it, and `add_seat` refuses catalog seats outright (seats.py:436-440: "is a catalog seat"). There is no `seats set-cost-mode`/edit command anywhere (the full cost_mode writer set in src/debate is seats.py:110/185/458/503). So for every catalog-discovered seat — which is exactly what onboarding flow 1 seats — cost_mode is permanently "unknown" and can only be changed by hand-editing seats.json. Consequences: the approval table and `onboarding status` can only ever print "unknown", which contradicts the APPROVED plan §3.2 (docs/plans/...v0.8.0.md:153, cost mode as `subscription quota`/`metered API`/`local compute`) and §3.3 (line 169, "smoke is offered ... with exact call count and cost mode"), and makes CHANGELOG "every seat carries a declared `cost_mode`" true only vacuously. Separately, `--cost-mode` is a SILENT NO-OP on the manual-append path: __main__.py:772-775 passes it, and seats.py:434-442 returns before the cost_mode assignment when the seat already exists, with no warning. Criteria 1 and 2, and fold-check (a).

SUPPORTING 3 — `--author-vendor` is unvalidated free text (__main__.py:377-382 has no `choices` and no catalog check; opening.py:461-466 only rejects blank). Catalog vendors are "claude"/"codex" (seat_catalog.py:59,69), so a typo such as "Claude" or "claude-code" silently makes BOTH seats author-independent — the permissive direction. That satisfies controller.py:370-376 ("at least one author-independent seat"), flips `topology` to "recommended-three-agent" (controller.py:388-393), and makes a self-review eligible for the PASS rule that requires an agreeing author-independent seat. A declaration that silently degrades to the permissive outcome is weak for a fold whose stated point is "declared, never guessed". No test covers a mismatched/typo vendor.

SUPPORTING 4 — stale text in the file the fold edited: HOOK-CONTRACT.md:33 still describes the manifest schema as "`matcher` + `hooks[]` of `{type, command, timeout, async}`" after fold 3 deleted `matcher` from hooks.json and pinned its absence by deep-equality test.

SUPPORTING 5 — test-adequacy gaps (criterion 3) for claimed fold items: no test for the 0644 profile chmod (onboarding.py:308-312, fold 4 — the only 0o644 in tests is unrelated, test_controller.py:666); no test for the `seats add --cost-mode` CLI flag or its no-op append path; no test for the smoke confirmation line's cost text (seats.py:542-543); no CLI-level test for the missing `--author-vendor` refusal (test_onboarding_flow.py:398 covers only the library blank-string path).

STANDING. Criteria 1-4 areas untouched by the true change set and unimplicated by the sweep stand on my round-1 evidence (MSG-2); live-host acceptance evidence remains author-sourced and outside my vote. The findings above are all I can establish this pass.

Minimum to flip: update the README brokered example to the required form; provide a real declaration path for cost_mode on catalog/derived seats (or make `--cost-mode` refuse rather than silently ignore, and correct plan/CHANGELOG claims to the honest scope); validate `--author-vendor`; fix HOOK-CONTRACT.md:33; add the missing tests.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: a18914bfc194ba8a3ca157ad11a6808570a27534c2a1c8fcb249842607217ce0
- phase: sealed
- captured-at: 2026-08-19T22:26:09+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 0bd16201b09fc53bf11715c7e292cb2ae235b9d69cff1fa41dbd8a4ec5aabb35
- source-ref: 7354ee59c85c9bcb08036f60cb41966ad2c83b1e
- source-manifest-sha256: b8e7f7690690119f0bbe96573e6e879e19e2dd5bd6633ed67ee16b68c9e0d292
- docket-revision-sha256: be47cb3adb11a2915fa23503cf99262b026bb70ad6523169eea016abbcd205c0
- input-sha256: 73fbc32d2b0f51d67c7385dd1485582b95188e2f8da1f2cf98a19495662e8782
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-7 | 2026-08-19T22:29:41+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-2 | refs: -

Blocking B1 provenance defect: `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/7354ee59c85c9bcb08036f60cb41966ad2c83b1e/codex/src/debate/opening.py:461` accepts a whitespace-padded nonblank `author_vendor`, but `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/7354ee59c85c9bcb08036f60cb41966ad2c83b1e/codex/src/debate/opening.py:383` compares it unnormalized. Fresh reproduction: `python -B -c '... author_vendor=" alpha " ...'` produced `author-independent` for an `alpha` seat. Thus a same-vendor interactive author can create immutable adapter/channel provenance that falsely records the seat as author-independent, contrary to the docket’s B1 same-vendor rule.

Exact required verification run: `python -m pytest -q` -> `521 passed, 1 skipped in 22.14s`; the passing suite does not cover padded author-vendor input.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: a18914bfc194ba8a3ca157ad11a6808570a27534c2a1c8fcb249842607217ce0
- phase: sealed
- captured-at: 2026-08-19T22:29:41+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 0bd16201b09fc53bf11715c7e292cb2ae235b9d69cff1fa41dbd8a4ec5aabb35
- source-ref: 7354ee59c85c9bcb08036f60cb41966ad2c83b1e
- source-manifest-sha256: bf847b45641d7179efe35b1525f406fe267c9fa0980c2a89678bb4561a14d92a
- docket-revision-sha256: be47cb3adb11a2915fa23503cf99262b026bb70ad6523169eea016abbcd205c0
- input-sha256: 3ac50c4abafc0babf75a11a1904ba09b1e5ce315a314d26f921eaba87c5b515d
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-8 | 2026-08-19T22:29:41+00:00 | from: owner | type: close | thread: branch-v080-onboarding-2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-9 | 2026-08-19T22:35:34+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-3 | refs: feature/installation-onboarding-v080@76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83

Fix-report and round-3 review request (fold-delta) for feature/installation-onboarding-v080, now at 76f2d6c. Round 2 closed NO_PASS (MSG-8) on: the README brokered example failing against the branch's own --author-vendor refusal (MSG-6 B1); cost_mode undeclarable on the product path with a silently ignored --cost-mode append (MSG-6 B2); unvalidated author vendor degrading to the permissive reading, incl. codex's padded-input reproduction recording false author-independent provenance (MSG-6 S3, MSG-7); stale HOOK-CONTRACT schema text (S4); and five enumerated test gaps (S5). Every finding is folded: README example corrected; seats set-cost-mode for any seat plus an applying append path; normalized+validated author vendor (padded input now records author-affiliated, typos refuse pre-write); contract doc updated; all five tests added. The fold diff (7354ee5..76f2d6c) and full branch diff ride in the docket; compute the true change set yourself per the fold-delta clause. Verdicts cite your own fresh evidence; standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: fd12cc06084429fb584249f3232010842140343aa530ffbe246c6b6ccb65b388
- source-ref: 76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83
- docket-revision-sha256: b8fba3e0f25c2bb48ff466438bc82f2e0fa53a28a71dedecae3de21eb11d4e3c
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r3.md", "sha256": "3cd3dfe87b1e3ee10120e163b2646e29b6c452736372b5c02ef54092b527cec1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r2.diff", "sha256": "ecda81236e445b9510803ad4888ee16f94f9d76231cd106828aae3417aa59032", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r2.diff", "sha256": "4a9ce96ae617804f23d7c000a9d312cfbafe1188db4efbe3ea5f56229026a7ed", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r3.diff", "sha256": "b8cb023bcb202c8ffd2cc401b243a8e1e380f5d7588dc4a2516b5128c644ddd5", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r3.json", "sha256": "fd12cc06084429fb584249f3232010842140343aa530ffbe246c6b6ccb65b388", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "20eb487a13e9a112388bae0554e1a8cd19a81abe8d55c1dab2fc685fd2b2ea02", "opus": "61c67eee0ad8700e66f2922af9cc787afd3b739fc2e63fedb7127d2ba7d6e616"}

## MSG-10 | 2026-08-19T22:48:06+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-3 | refs: -

PASS — round-3 fold-delta review of feature/installation-onboarding-v080 at 76f2d6c.

## Criterion 5 — the exact command

Run from the export root `/home/zoltan/.../exports/76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83/opus`:

`python -m pytest -q`
→ `525 passed, 1 skipped in 22.91s` (exit 0).

Environment binding checked separately with `python -m pytest --pyargs debate.seats --collect-only`, which printed `rootdir: /home/zoltan/.../exports/76f2d6cc.../opus` and `configfile: pyproject.toml` — the run used the export's own config and `testpaths = ["tests"]`. Caveat, stated for the record: the sandbox denied `python -c`, `pip show` and `printenv`, so I could not print the resolved `debate.__file__`. Indirect evidence that the engine under test is this tree: `tests/test_release_sync.py:17-19` imports `debate` and asserts `__version__` equals the export's `pyproject.toml` version (0.8.0), and the fold-specific behaviours (`seats.set_cost_mode`, the `--author-vendor` known-vendor refusal) are exercised and green, which only this branch tip provides.

## True change set (computed independently, not from the author's list)

I compared the per-file blob hashes in the `index <old>..<new>` headers of `branch-v080-r2.diff` and `branch-v080-r3.diff` (both are branch-vs-main, so the new-side blob is the branch content at that round). Exactly eight files differ, and the file set is otherwise byte-identical with no additions or deletions:

- CHANGELOG.md 094aaa5→e2575d4
- README.md 2d97df8→7b7f282
- hooks/HOOK-CONTRACT.md 756d6bd→e7d17a3
- skills/debate-onboarding/SKILL.md 4466fa7→287c59b
- src/debate/__main__.py 87e680a→f4934a6
- src/debate/opening.py 9165273→28c72a0
- src/debate/seats.py 4020afb→15b9a4c
- tests/test_onboarding_flow.py 5c4c171→6ac4d62

`fold-r2.diff`'s own `index` pairs match those eight old→new blobs exactly and cover no other path, so the author's fold list is the complete change set: **no edit rides outside the declared folds**. I verified the post-images against the export files themselves rather than trusting the diff text.

## (a) Each fold resolves its round-2 finding

1. **B1 (README example vs the branch's own refusals)** — `README.md:201-210` now reads `debate open --brokered ... --pair alpha/fake,beta/fake --author-vendor claude --docket-file README.md`. Checked against the CLI's actual rules: `--brokered` requires `--pair` and `--author-vendor` (`src/debate/__main__.py:873-905`); `claude` is a catalog vendor (`src/debate/seat_catalog.py:59`), so it survives the new validation; `--docket-file` is resolved as `project_path / docket_file` (`src/debate/opening.py:514-519`) and README.md exists at the project root. The example no longer refuses.
2. **B2 (cost_mode undeclarable; silent no-op append)** — `seats.set_cost_mode` (`src/debate/seats.py:467-480`) declares for any existing seat regardless of source, validating the mode and the seat id; CLI wiring at `src/debate/__main__.py:274-281` (parser, `dest` defaults `seat_id`/`cost_mode`) and `:794-798` (dispatch under `seats_sub = ...add_subparsers(dest="seats_command")`, `:233`). The append path now applies a non-unknown declaration (`seats.py:441-446`). I checked the "discovery never touches the declaration" claim on my own reading: `discover()` (`seats.py:238-278`) mutates only `present` and `commands` on existing seats and never `cost_mode`; `registry_payload` persists it (`seats.py:185`); `onboarding.approve` writes through that payload (`onboarding.py:283`), so a declaration survives re-scan and re-approval. The CHANGELOG bullet (`CHANGELOG.md:47-59`) now matches that scope, and the skill records user declarations (`skills/debate-onboarding/SKILL.md:48-49`) with the exact command the CLI accepts.
3. **MSG-7 + S3 (padded vendor / unvalidated vendor)** — `opening.py:463` normalizes the declaration (`strip().lower()`), `:475-481` validates it against catalog ∪ registry vendors (registry side also normalized) and refuses a typo, and `:382-386` compares `seat.vendor.strip().lower()` against the normalized declaration — both sides normalized, so padded ` Alpha ` records author-affiliated instead of falsely author-independent. The refusal is pre-write: it precedes `generate_channel_id`/`init_channel` (`:483`, `:541`), and the test asserts the target root stays empty (`tests/test_onboarding_flow.py:430-440`).
4. **S4 (stale HOOK-CONTRACT text)** — `hooks/HOOK-CONTRACT.md:31-35` now says DEEP-EQUAL documents, one `SessionStart` group, no `matcher`, `hooks[]` of `{type, command, timeout, async}`. That matches the shipped manifests (both blobs are literally the same object, git blob 9c45964 for `hooks/hooks.json` and `hooks/hooks-codex.json`) and the standing test `test_manifests_are_field_identical_documents` (`tests/test_session_start_hook.py:253-259`).
5. **S5 (test gaps)** — present and green: `test_padded_author_vendor_still_matches_and_typo_is_refused`, `test_cli_brokered_open_requires_author_vendor`, `test_approved_profile_is_world_readable` (asserts 0o644, matching `onboarding.py:311-313`), `test_cost_mode_declaration_paths` (creation, append-applies, set_cost_mode validation + missing seat, and `"cost mode: api"` in the smoke confirmation prompt) — `tests/test_onboarding_flow.py:409-504`.

## (b) Reverse check

Every round-2 finding named in the docket (MSG-6 B1, B2, S3, S4, S5; MSG-7 padded `author_vendor`; the MSG-8 NO_PASS close) maps to a fold in the true change set, and every hunk in the true change set maps to one of those findings. No orphan edit, no orphan finding.

## (c) Coherence sweep

- Adapter config and channel provenance cannot diverge: the `.debate.json` record copies `author_relationship`/`cost_mode` straight out of the adapter dicts (`opening.py:563-579`).
- Argparse namespaces do not collide: `seats add` uses `dest="seats_add_cost_mode"` (`__main__.py:265-271`) while `set-cost-mode` uses positional `cost_mode`; both consumed correctly at `:780-798`.
- Docs↔code: CHANGELOG, README, the onboarding skill and the CLI now state the same rules (`--author-vendor` required and validated; cost mode declarable any time; discovery non-destructive). The skill's Flow 2 tells hosts to pass `claude`/`codex`, both catalog vendors, so the new validation cannot refuse the documented product path.
- Nothing in the fold touches the hook, plugin manifests, MANIFEST.in, or the v1 open path; their round-1/round-2 criteria are unimplicated.

## Standing criteria

Criteria 1-4 outside the areas the true change set and the sweep implicate stand on my own round-2 evidence (MSG-6), where I established plan conformance, correctness, test adequacy and no-regressions apart from the findings folded here; live-host acceptance evidence remains author-sourced and outside my vote.

## Non-blocking observations (recorded, none blocks the verdict)

1. `seats.add_seat` validates `cost_mode` against `COST_MODES` only on the creation path (`seats.py:448`); the append path applies the value and returns first (`:445-447`), so a library caller passing an invalid literal to an existing manual seat writes a value `load_registry` will later refuse (`seats.py:95-99`). Unreachable from the product path (argparse `choices` constrain the CLI) and from the skill. One-line fix: hoist the `COST_MODES` check above the `existing is not None` branch.
2. The new `debate seats set-cost-mode` CLI subcommand has engine-level coverage only; the argparse wiring itself is untested. I verified it by reading (`__main__.py:233, 274-281, 794-798`), and it is correct.
3. The known-vendor validation refuses an honest declaration from a host whose vendor is in neither the catalog nor the registry (e.g. a third-party host), because a truthful unknown vendor is indistinguishable from a typo. That is the conservative reading the round-2 findings asked for, and the refusal message enumerates the known vendors, so I do not treat it as a defect — flagging it as a deliberate behavioural narrowing worth a release note if third-party hosts are expected.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 1edebf9f2284d8faa0f6c4894a32584a86933cc45a446f4dd4874689c164b64c
- phase: sealed
- captured-at: 2026-08-19T22:43:17+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: fd12cc06084429fb584249f3232010842140343aa530ffbe246c6b6ccb65b388
- source-ref: 76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83
- source-manifest-sha256: 61c67eee0ad8700e66f2922af9cc787afd3b739fc2e63fedb7127d2ba7d6e616
- docket-revision-sha256: b8fba3e0f25c2bb48ff466438bc82f2e0fa53a28a71dedecae3de21eb11d4e3c
- input-sha256: f8c9c4bb889e0fd571159ab7c6d396a1c729e1972495a14cded743db69ef378b
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-11 | 2026-08-19T22:48:06+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-3 | refs: -

`python -m pytest -q` run from the pinned export completed: `525 passed, 1 skipped in 22.71s`. Blocking coherence finding: brokered `--docket-file` preflight accepts an existing absolute path or `../` escape because `src/debate/opening.py:514-519` only checks `project_path / docket_file` is a file. The controller later rejects that same config as outside the repository in `src/debate/controller.py:611-615`, but only after `open_debate_brokered` has created the channel, runtime directory, and watcher config at `src/debate/opening.py:541-548`. This violates the approved plan's requirement that immutable docket inputs be under the project and that all validation complete before the first target write (plan §4.3, lines 304-308). `tests/test_onboarding_flow.py:525-552` covers only a missing file and an in-project file, not absolute or traversal paths, so the passing suite does not establish the required pre-write refusal.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 1edebf9f2284d8faa0f6c4894a32584a86933cc45a446f4dd4874689c164b64c
- phase: sealed
- captured-at: 2026-08-19T22:48:06+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: fd12cc06084429fb584249f3232010842140343aa530ffbe246c6b6ccb65b388
- source-ref: 76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83
- source-manifest-sha256: 20eb487a13e9a112388bae0554e1a8cd19a81abe8d55c1dab2fc685fd2b2ea02
- docket-revision-sha256: b8fba3e0f25c2bb48ff466438bc82f2e0fa53a28a71dedecae3de21eb11d4e3c
- input-sha256: 7a2eb909ece81b00a50bf7db138a4009161db24b77f3194caa4152a32729d063
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-12 | 2026-08-19T22:54:39+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-3 | refs: -

NO_PASS — round-3 deliberation on feature/installation-onboarding-v080 at 76f2d6c. This revises my sealed PASS (MSG-10): the folds are all correct, but the coherence sweep the docket asks for (clause (c)) yields one blocking defect in new brokered-open code that I did not establish in the sealed pass and have now verified on my own reading. I do not adopt MSG-11 on its word; I re-derived every element below from the export.

## Criterion 5 — the exact command

From the export root `/home/zoltan/.../exports/76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83/opus`:

`python -m pytest -q`
→ `525 passed, 1 skipped in 23.35s` (exit 0). The command passes; it does not establish the behaviour below, because no test covers it (see B3.4).

## Blocking finding

**B3 — brokered `--docket-file` preflight does not enforce "under the project"; an absolute or `../` path is accepted pre-write and refused only after the channel exists.**

1. The check is `candidate = project_path / docket_file; if not candidate.is_file(): raise` (`src/debate/opening.py:514-519`). Under documented pathlib semantics, joining an absolute right-hand operand discards the left: `Path('/proj') / '/etc/passwd'` is `/etc/passwd`. So an absolute path that exists anywhere on disk passes, and a relative `../outside.md` passes as `project/../outside.md` — there is no `resolve()` and no containment test. The refusal message asserts a property ("does not exist **under the project**") that the check does not verify. (I could not run `python -c` to demo this — the sandbox denies non-test Bash — so this rests on the code plus pathlib's specified join behaviour, which is not in doubt.)
2. Nothing upstream constrains it: the CLI only appends raw strings (`src/debate/__main__.py:376-383`, metavar `PROJECT_RELATIVE_PATH`, no validation; passed through at `:659`), and the pre-write loader probe cannot catch it — `BrokerConfig.__post_init__` checks `docket_files` only for duplicates (`src/debate/controller.py:385-386`).
3. The raw string is written into the config (`opening.py:511`) and the channel, runtime root, protocol scaffold, config and `.debate.json` are all created (`opening.py:541-582`). The containment rule is enforced only later, in `materialize_docket` (`controller.py:611-615`), which runs in `_prepare_case` (`controller.py:820-821`) — i.e. at the next product step, `broker-open`. Result: `debate open --brokered` reports success and the immediately following `broker-open` refuses `docket file ... is outside repository`, leaving a created-but-unusable channel.
4. This contradicts the approved plan §4.3: "create the adapter configuration and immutable source/docket inputs **under the project**" (plan lines 304-305, docket copy `docs/plans/2026-08-19-...md:304`), and it contradicts the branch's own stated invariant one screen up — `opening.py:532-536` refuses any config that "would be INVALID to the controller", which this config demonstrably is. Test coverage stops short of it: `tests/test_onboarding_flow.py:525-552` exercises only a missing file and an in-project file.
5. Reachability: the skill instructs hosts to pass "the review target" as `--docket-file` (`skills/debate-onboarding/SKILL.md:69-73`); it says project-relative, but nothing rejects an absolute path a user or host agent naturally supplies. No data escapes — `materialize_docket` refuses before reading — so this is a validation-ordering/plan-conformance defect, not an exfiltration vuln.
6. Fix: in the `opening.py:514` loop, refuse `Path(docket_file).is_absolute()`, then `resolve()` the candidate and require `is_relative_to(project_path.resolve())` before the existence check, plus tests for the absolute and `../` cases asserting the target root stays byte-empty.

Scope note: `opening.py:514-519` is not in this round's fold delta (`fold-r2.diff` touches those tests only to swap `author_vendor="testhost"` → `"claude"`), but it is new code on this branch versus main, and criteria 1-2 govern it. Standing is a default for unimplicated criteria, not an amnesty for a defect established in the sweep the docket mandates.

## What I re-confirm from my sealed pass (MSG-10), unchanged

- True change set, computed from the `index <old>..<new>` blob pairs of `branch-v080-r2.diff` vs `branch-v080-r3.diff`: exactly eight files (CHANGELOG.md, README.md, hooks/HOOK-CONTRACT.md, skills/debate-onboarding/SKILL.md, src/debate/__main__.py, src/debate/opening.py, src/debate/seats.py, tests/test_onboarding_flow.py), matching `fold-r2.diff` exactly — no edit rides outside the declared folds.
- (a) Each fold resolves its round-2 finding: B1 README example now satisfies the CLI's own rules (`README.md:207-209`, `__main__.py:873-905`, `seat_catalog.py:59`); B2 `seats.set_cost_mode` (`seats.py:467-480`) plus CLI wiring (`__main__.py:274-281, 794-798`) and an applying append path (`seats.py:441-447`); MSG-7/S3 normalized-and-validated `author_vendor` refusing pre-write (`opening.py:463-481`, test at `tests/test_onboarding_flow.py:430-440`); S4 HOOK-CONTRACT text matches the deep-equal matcher-free manifests (`hooks/HOOK-CONTRACT.md:31-35`); S5 all five tests present and green.
- (b) Reverse check clean: every round-2 finding maps to a fold, every fold to a finding.

## Non-blocking, recorded (none of these blocks on its own)

1. `seats.add_seat` validates `cost_mode` against `COST_MODES` only on the creation path (`seats.py:448`); the append path applies and returns first (`:441-447`), so a library caller can write a value `load_registry` later refuses (`seats.py:95-99`). Same "accept now, refuse later" shape as B3 but unreachable from the CLI (argparse `choices`) and from the skill — hence not blocking. One-line fix: hoist the check above the `existing is not None` branch.
2. `BrokerConfig`'s duplicate check compares raw strings (`controller.py:385`), so `README.md` and `./README.md` both survive and yield duplicate records in `materialize_docket`. Pre-existing; the B3 fix (normalize then compare) subsumes it.
3. `debate seats set-cost-mode` has engine-level coverage only; the argparse wiring is verified by reading (`__main__.py:233, 274-281, 794-798`) and is correct.
4. Known-vendor validation refuses a truthful declaration from a host in neither catalog nor registry — the conservative reading the round-2 findings asked for; worth a release note if third-party hosts are expected.

Criteria 1-4 outside the areas the true change set, the sweep and B3 implicate stand on my round-2 evidence (MSG-6); live-host acceptance evidence remains author-sourced and outside my vote.

Controller-Decision:
- decision: NO_PASS

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: fd12cc06084429fb584249f3232010842140343aa530ffbe246c6b6ccb65b388
- source-ref: 76f2d6cc807d1ce213b79cfd69dff3d78cb9ec83
- source-manifest-sha256: 61c67eee0ad8700e66f2922af9cc787afd3b739fc2e63fedb7127d2ba7d6e616
- docket-revision-sha256: b8fba3e0f25c2bb48ff466438bc82f2e0fa53a28a71dedecae3de21eb11d4e3c
- input-sha256: ddfad406be38b4fb22b0301c290660a03788210e5a368c772dc3d585aef156ae
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-13 | 2026-08-19T22:54:39+00:00 | from: owner | type: close | thread: branch-v080-onboarding-3 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-14 | 2026-08-19T22:57:45+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-4 | refs: feature/installation-onboarding-v080@442b094f1f52fc053f659dde321e5339be18f057

Fix-report and round-4 review request (fold-delta) for feature/installation-onboarding-v080, now at 442b094. Round 3 closed NO_PASS (MSG-13) on one blocker: --docket-file accepted absolute and ../ paths, refused by the controller only after the channel write (MSG-11); opus sealed PASS with two observations (MSG-10). All folded: pre-write refusal of absolute/traversal docket paths with byte-empty-target tests; append-path cost_mode validation hoisted; set-cost-mode CLI wiring test. The fold is 121 diff lines; fold-r3.diff and the full branch diff ride in the docket. Verdicts cite your own fresh evidence; standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 05c3387642608efd6098814ccd7148ac5fb78d7aa527319cc2021804817b12a6
- source-ref: 442b094f1f52fc053f659dde321e5339be18f057
- docket-revision-sha256: 4e292fa75a32b71d59f68904ce8182b641efd9c73713a5494afc34ea75803fe6
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r4.md", "sha256": "0c4ae3194cc480bdcd8f207786e349b4ffcd9916c8b4fba5974b252591475d85", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r3.diff", "sha256": "b8cb023bcb202c8ffd2cc401b243a8e1e380f5d7588dc4a2516b5128c644ddd5", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r3.diff", "sha256": "93b8aed81679c608f6bd5618a95037c436e5352ce35343eff7835bd99a63929f", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r4.diff", "sha256": "7ca634ce5e4b497bd405372f1bec29d518864e6e3b16ecc6c7364790b7a88c49", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r4.json", "sha256": "05c3387642608efd6098814ccd7148ac5fb78d7aa527319cc2021804817b12a6", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "4a0d3886ace280349c2f948af670fb03e56487ec355935da8ff5a1649a4f7ccf", "opus": "f74271bf07fd1ed329ce55a8c8f01368918c92f795c07196f6784e15b2082d4f"}

## MSG-15 | 2026-08-19T23:04:53+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-4 | refs: -

PASS on my own reading of the pinned export at 442b094 plus fresh command output. No blocking findings; one non-blocking accuracy note on the fold list is recorded below.

CRITERION 5 (exact command). Run literally from the export root /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/442b094f1f52fc053f659dde321e5339be18f057/opus:
  `python -m pytest -q`
Result: `528 passed, 1 skipped in 22.74s` (7 progress lines, one `s` at the 81% line; no failures, no errors).

TRUE CHANGE SET (computed by me, not taken from the fold list). The export has no .git (`git rev-parse HEAD` -> `fatal: not a git repository`), so I derived the fold delta by comparing the two branch-vs-main renderings in the docket. Grepping `^(diff --git|index |@@)` over branch-v080-r3.diff and branch-v080-r4.diff yields an IDENTICAL file inventory (24 file sections, same order) and identical `index` blob pairs for every file EXCEPT three:
- src/debate/opening.py  12462d4..28c72a0 (r3) -> 12462d4..0e13f5d (r4)
- src/debate/seats.py    9851619..15b9a4c (r3) -> 9851619..7701778 (r4)
- tests/test_onboarding_flow.py 0000000..6ac4d62 (r3) -> 0000000..c71736c (r4)
Those three post-image blobs are exactly the ones fold-r3.diff claims (28c72a0->0e13f5d, 15b9a4c->7701778, 6ac4d62->c71736c). Hunk arithmetic agrees: opening.py final hunk +237 -> +252 (net +15 = 16 added, 1 removed in the fold); test_onboarding_flow.py 620 -> 675 lines (+55, the fold's single @@ -552,6 +552,61 @@); seats.py r3's single @@ -412,7 +439,16 @@ splits into r4's @@ -404,6 +431,10 @@ (+4) and @@ -412,6 +443,11 @@ (+5), net unchanged — a move, as claimed. I also confirmed the r4 diff's post-image matches the actual export bytes for a file the fold list says was NOT touched (src/debate/__main__.py: the `set-cost-mode` subparser at __main__.py:274-281 and dispatch at __main__.py:794-798 match diff lines 737-744/949-953 verbatim), and a Glob of src/debate/*.py, tests/*.py, hooks/*, skills/** shows no file outside the diff inventory. So fold-list item 4 ("no other change") holds: the true change set is exactly those three files.

(a) EACH FOLD RESOLVES ITS FINDING.
1. MSG-11 (codex blocker, docket-file escape refused only after the channel write). opening.py:514-534 now computes `project_resolved = project_path.resolve()`, refuses `raw.is_absolute()` (:521), and refuses `(project_path / raw).resolve()` that fails `is_relative_to(project_resolved)` (:527), before the existing `is_file()` check. These land at :514-534, i.e. BEFORE the first mutation: `channel.init_channel` (:556), `scaffold_protocol` (:560), `state_path.parent.mkdir`/`runtime_root.mkdir` (:561-562), `config_path.write_text` (:563). The config dict at :503-513 is in memory only. Test test_docket_file_escapes_are_refused_pre_write (tests/test_onboarding_flow.py:555-580) drives both escape shapes and asserts `not root.exists() or list(root.iterdir()) == []` after each. The traversal case is a real exercise of the new check, not a vacuous one: the `isolated` fixture puts project at tmp_path/"project" (:58-66), and the test writes tmp_path/"outside.md", so `project/../outside.md` EXISTS and would have passed the old `is_file()` gate; only `is_relative_to` refuses it.
2. MSG-10 obs 1 (append path did not validate cost_mode). seats.py:434-437 validates `cost_mode not in COST_MODES` ahead of `existing = registry.seats.get(seat_id)` (:438) and the append branch (:439-451); the round-2 behaviour that a non-"unknown" declaration APPLIES on append (:449-450) is untouched. COST_MODES = ("subscription","api","local","unknown") (seats.py:53), so the default `cost_mode="unknown"` still passes the hoisted check — no regression for ordinary calls. Test test_add_seat_append_validates_cost_mode (tests/test_onboarding_flow.py:594-607) pins the refusal on the append path.
3. MSG-10 obs 2 (untested set-cost-mode CLI wiring). test_cli_set_cost_mode_wiring (tests/test_onboarding_flow.py:583-591) calls `main(["seats","set-cost-mode","alpha/fake","subscription"])`, asserts rc == 0 and reads the persisted registry — it exercises the argparse positionals (`seat_id`, `cost_mode`, __main__.py:278-281) and the dispatch/save at __main__.py:794-798.

(b) REVERSE CHECK. The round-3 findings the docket names are MSG-11 (codex blocker) and MSG-10's two observations, with MSG-13's NO_PASS resting on MSG-11; each has a corresponding fold in the true change set (above), and the true change set contains nothing beyond those three folds. MSG-13 closes with MSG-11.

(c) COHERENCE SWEEP. The new opening-side root is `Path(project)`, and the controller's is `repository_root=Path(channel_config.project)` (__main__.py:174) checked at controller.py:608-616 — same root, so the open-time and materialize-time rules agree; opening is strictly the tighter of the two (it also refuses absolute paths that name in-repo files, which controller.py:613 would accept), so the fold closes a hole without opening one. Symlink handling matches on both sides (`resolve()` before `is_relative_to`). Every docket path in the branch's docs and examples is project-relative (README.md:209 `--docket-file README.md`; watcher.brokered.example.json:60-63; skills/debate-onboarding/SKILL.md:71-72 says "project-relative review input"; opening.py:72 comment likewise), so nothing in the branch is invalidated by the new refusal. Empty-string / "." docket paths still fall through to the existing is_file() refusal. The seats.py hoist changes the error message precedence for an existing CATALOG seat given a bad cost_mode (now the cost_mode refusal instead of the catalog refusal); both are refusals, no behavioural regression, and the full suite passes.

CRITERIA 1-4. Criterion 4 (no regressions/unrelated changes) I establish freshly above: the true change set is three files and nothing else. Criteria 1-3 (plan conformance, correctness, test adequacy) are implicated only in the folded regions, which I read directly and verified above; for the unimplicated remainder they stand by citation to my round-3 verdict MSG-10 (opus PASS on criteria 1-4), whose observations are the ones folded here. Live-host acceptance evidence remains author-sourced and outside my vote.

NON-BLOCKING OBSERVATION (accuracy of the fold list, not of the code). Fold-list item 1 says both new checks sit "BEFORE generate_channel_id". They do not: `generate_channel_id` is called at opening.py:483 and the checks are at :514-534, after it. This does not weaken the fix, because channel.generate_channel_id (channel.py:309-329) only validates the label and globs `root` for collisions — it writes nothing — so the refusal is still strictly pre-write, as the test's byte-empty-root assertion confirms. Worth correcting in the fold narrative so a future round is not misled about where the guard sits.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 7046508e2eae6a6e6641de9bb223d46395c7da75fa9f2c1896b75df10e5472c7
- phase: sealed
- captured-at: 2026-08-19T23:02:07+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 05c3387642608efd6098814ccd7148ac5fb78d7aa527319cc2021804817b12a6
- source-ref: 442b094f1f52fc053f659dde321e5339be18f057
- source-manifest-sha256: f74271bf07fd1ed329ce55a8c8f01368918c92f795c07196f6784e15b2082d4f
- docket-revision-sha256: 4e292fa75a32b71d59f68904ce8182b641efd9c73713a5494afc34ea75803fe6
- input-sha256: 6296c8f64f6c888283df58bced1b2ef197fa696b9adc529c92151ad6b3e92fe2
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-16 | 2026-08-19T23:04:53+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-4 | refs: -

Blocking finding (MSG-11 fold): the docket explicitly requires the absolute/traversal docket-file checks before `generate_channel_id`, but `src/debate/opening.py` calls `channel.generate_channel_id(...)` at line 483 and performs those checks only from line 514. The test proves no target write, but not the required pre-generation ordering. Fresh commands/results: `python -m pytest -q` → `528 passed, 1 skipped in 22.35s`; `python -m pytest -q tests/test_onboarding_flow.py -k 'docket_file_escapes or cli_set_cost_mode_wiring or add_seat_append_validates_cost_mode'` → `3 passed, 20 deselected`; `diff -U0 .../branch-v080-r3.diff .../branch-v080-r4.diff` showed the true fold delta is limited to `opening.py`, `seats.py`, and `test_onboarding_flow.py`. The cost-mode validation and CLI test folds are present, but the unresolved MSG-11 sequencing criterion prevents PASS.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 7046508e2eae6a6e6641de9bb223d46395c7da75fa9f2c1896b75df10e5472c7
- phase: sealed
- captured-at: 2026-08-19T23:04:53+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 05c3387642608efd6098814ccd7148ac5fb78d7aa527319cc2021804817b12a6
- source-ref: 442b094f1f52fc053f659dde321e5339be18f057
- source-manifest-sha256: 4a0d3886ace280349c2f948af670fb03e56487ec355935da8ff5a1649a4f7ccf
- docket-revision-sha256: 4e292fa75a32b71d59f68904ce8182b641efd9c73713a5494afc34ea75803fe6
- input-sha256: 9bb11cdb7a9a53dce360dcd0778b9c29e597801337c082709fbc84962c4681e7
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-17 | 2026-08-19T23:10:07+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-4 | refs: -

PASS on my own reading of the pinned export at 442b094 plus fresh command output. I hold the PASS I recorded in MSG-15 and address codex's MSG-16 blocker below on fresh evidence.

CRITERION 5 (exact command). Run literally from the export root /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/442b094f1f52fc053f659dde321e5339be18f057/opus:
  `python -m pytest -q`
Result: `528 passed, 1 skipped in 22.43s` (8 progress lines, a single `s` on the 81% line; no failures, no errors).

Supplementary run (not a substitute for criterion 5), same root:
  `python -m pytest -q tests/test_onboarding_flow.py -k "docket_file_escapes or cli_set_cost_mode_wiring or add_seat_append_validates_cost_mode"`
Result: `3 passed, 20 deselected in 0.64s`.

TRUE CHANGE SET (recomputed by me this round). Grepping `^(diff --git|index )` over branch-v080-r3.diff and branch-v080-r4.diff gives an identical 24-file inventory in identical order, with identical index blob pairs everywhere except three files: src/debate/opening.py 12462d4..28c72a0 -> 12462d4..0e13f5d; src/debate/seats.py 9851619..15b9a4c -> 9851619..7701778; tests/test_onboarding_flow.py 0000000..6ac4d62 -> 0000000..c71736c. fold-r3.diff contains exactly those three sections with matching pre/post blobs (28c72a0..0e13f5d, 15b9a4c..7701778, 6ac4d62..c71736c) and four hunks total. So the true change set is those three files and nothing else; fold-list item 4 holds. codex's MSG-16 independently reports the same three-file delta.

RESPONSE TO MSG-16 (the sole cited blocker). codex reads "both BEFORE generate_channel_id" as a docket requirement. On my reading of branch-docket-r4.md that phrase appears only inside the section headed "## Author's fold list (verify against your own diff)" (branch-docket-r4.md:28-38), which the docket itself tells the seat not to take at face value ("Never trust the author's fold list as the change inventory -- an edit absent from it is itself an unresolved finding", :17-19). The binding requirements are the goal statement and the standing criteria: the goal names MSG-11 as "--docket-file accepted absolute/../ paths whose refusal landed only AFTER the channel write" (:4-5), and criteria 1-5 (:40-53) say nothing about generate_channel_id. The docket's untrust rule is aimed at edits missing from the list; here the list overstates the precision of a fold whose substance is present, which is a narrative defect, not a missing edit.

On the substance, the ordering codex flags is inert. opening.py:483 calls channel.generate_channel_id; channel.py:309-329 validates the label against _SLUG_RE, otherwise derives one, then loops globbing `root` for a free `<label>-NNNNN` and returns a string — no mkdir, no write, no mutation of any kind. Between :483 and the new checks the code only calls derive_paths (setup.py:113-125, pure path arithmetic: two `/` joins plus expanduser), computes runtime_root/state_path, builds two adapter dicts, and assembles an in-memory config dict (:495-513). The refusals at :514-534 (is_absolute at :521, resolve()+is_relative_to(project_resolved) at :526-527, then the pre-existing is_file() at :531) therefore land before every mutation: init_channel (:556), scaffold_protocol (:560), the two mkdirs (:561-562), config_path.write_text (:563). The tempfile probe at :543-545 is a scratch TemporaryDirectory and is also after the checks. test_docket_file_escapes_are_refused_pre_write (tests/test_onboarding_flow.py:555-580) drives both escape shapes and asserts `not root.exists() or list(root.iterdir()) == []` after each, which is the pre-write property MSG-11 asked for, and it is a live exercise of the new gate: the `isolated` fixture roots the project at tmp_path/"project" and the test writes tmp_path/"outside.md", so `../outside.md` resolves to an existing file that the old is_file() gate would have accepted. I record the fold-list wording as a non-blocking accuracy note (as in MSG-15), not as a blocker: no criterion is unmet and no write escapes.

(a) EACH FOLD RESOLVES ITS FINDING. 1. MSG-11: opening.py:514-534, pre-write as established above, with the byte-empty-root test. 2. MSG-10 obs 1: seats.py:434-437 validates `cost_mode not in COST_MODES` ahead of `existing = registry.seats.get(seat_id)` (:438) and the append branch (:439-451); the round-2 behaviour that a non-"unknown" declaration applies on append (:449-450) is untouched, and the default "unknown" is in COST_MODES (seats.py:53), so ordinary calls are unaffected. Pinned by test_add_seat_append_validates_cost_mode (tests/test_onboarding_flow.py:594-607). 3. MSG-10 obs 2: test_cli_set_cost_mode_wiring (:583-591) drives `main(["seats","set-cost-mode","alpha/fake","subscription"])`, asserts rc == 0 and reads the persisted registry, exercising the argparse positionals and the dispatch/save in __main__.py.

(b) REVERSE CHECK. Round-3 findings are MSG-11 and MSG-10's two observations, with MSG-13's NO_PASS resting on MSG-11; each maps to one fold in the true change set, and the change set holds nothing beyond those three. MSG-13 closes with MSG-11.

(c) COHERENCE SWEEP. Opening's root is Path(project); the controller's materialize-time check uses repository_root=Path(channel_config.project) — the same root — so the two rules agree and opening is strictly the tighter (it also refuses absolute paths naming in-repo files). Both resolve() before is_relative_to, so symlink handling matches. Every docket path in the branch's docs and examples is project-relative (README.md:209; watcher.brokered.example.json:60-63; skills/debate-onboarding/SKILL.md:71-72; opening.py:72), so nothing in-branch is invalidated. Empty-string and "." docket paths still fall through to the is_file() refusal. The seats.py hoist only changes which refusal message wins for a catalog seat given a bad cost_mode; both outcomes are refusals.

CRITERIA 1-4. Criterion 4 is established freshly above (three files, nothing else). Criteria 1-3 are implicated only in the folded regions, which I read directly this round; for the unimplicated remainder they stand by citation to my round-3 verdict MSG-10 (opus PASS on criteria 1-4). Live-host acceptance evidence remains author-sourced and outside my vote.

NO OTHER BLOCKING FINDINGS. A second pass by me over this change set would find nothing new beyond the fold-list wording note above.

Controller-Decision:
- decision: PASS

Controller-Decision:
- decision: PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 05c3387642608efd6098814ccd7148ac5fb78d7aa527319cc2021804817b12a6
- source-ref: 442b094f1f52fc053f659dde321e5339be18f057
- source-manifest-sha256: f74271bf07fd1ed329ce55a8c8f01368918c92f795c07196f6784e15b2082d4f
- docket-revision-sha256: 4e292fa75a32b71d59f68904ce8182b641efd9c73713a5494afc34ea75803fe6
- input-sha256: 28a885b903f108f7f02a42e087e4886cafabf7aa4c2cd50762d6d41232363696
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-18 | 2026-08-19T23:15:20+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-4 | refs: -

PASS. I verified the immutable docket hashes, inspected the pinned export and fold delta, and found no blocking issue.

Exact required command, run from the export root: `python -m pytest -q`
Result: `528 passed, 1 skipped in 24.55s`.

My diff of `branch-v080-r3.diff` against `branch-v080-r4.diff` establishes that the true fold delta is limited to `src/debate/opening.py`, `src/debate/seats.py`, and `tests/test_onboarding_flow.py`. The opening guard rejects absolute docket paths and resolved traversal escapes before `init_channel`, scaffolding, directory creation, or config writes; its test covers both forms and asserts the target root remains empty. The `cost_mode` validation now precedes the append branch, and the CLI wiring test persists `set-cost-mode` through `main`.

The fold-list phrase claiming these guards are before `generate_channel_id` is inaccurate: generation occurs earlier. It is not a blocking criterion because that function only validates/derives an identifier and checks for collisions; it performs no write. The stated round-3 finding was refusal after a channel write, and the fix now refuses before all mutations.

Criteria 1–3 otherwise stand by the prior PASS evidence cited as MSG-10; criterion 4 is freshly supported by the three-file true-change-set review. No other blocking findings established.

Controller-Decision:
- decision: PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 05c3387642608efd6098814ccd7148ac5fb78d7aa527319cc2021804817b12a6
- source-ref: 442b094f1f52fc053f659dde321e5339be18f057
- source-manifest-sha256: 4a0d3886ace280349c2f948af670fb03e56487ec355935da8ff5a1649a4f7ccf
- docket-revision-sha256: 4e292fa75a32b71d59f68904ce8182b641efd9c73713a5494afc34ea75803fe6
- input-sha256: 882453fd2d002b7a426214040cff277c4365491a1dee1441665b34f4d459a7b8
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-19 | 2026-08-19T23:15:20+00:00 | from: owner | type: close | thread: branch-v080-onboarding-4 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-20 | 2026-08-20T01:45:24+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-5 | refs: feature/installation-onboarding-v080@44a5028949ff613e87b1c0abdd5a76aa1035f52a

Round-5 review request (field-fold delta) for feature/installation-onboarding-v080, now at 44a5028. Round 4 closed PASS (MSG-19) at 442b094; the owner then live-tested the installed plugin in real Codex and found two defects the gates missed: a concurrent-smoke registry-write race that lost an observed PASS, and smoke scratch landing in the system temp dir. One commit folds both: atomic save_registry, a locked update_registry read-modify-write applied per observed result, config-local smoke scratch, sequential-smoke skill instruction, and regression tests reproducing the exact field interleaving. The 204-line fold diff and full branch diff ride in the docket. Verify per branch-docket-r5.md; verdicts cite your own fresh evidence; rounds 1-4 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: ab5629983061c5bceb451fd612c59a4f590b197844bdcca1894a37e84e3db606
- source-ref: 44a5028949ff613e87b1c0abdd5a76aa1035f52a
- docket-revision-sha256: 0c6d785f6c201a633c4be46cf3df65846edd1d4f73267fc63184d5831b591733
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r5.md", "sha256": "13aab0562ff91bde49a58268122e0a6b726ced8a4e5aa86f9c9996446a4941cb", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r4.diff", "sha256": "7ca634ce5e4b497bd405372f1bec29d518864e6e3b16ecc6c7364790b7a88c49", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r4.diff", "sha256": "fc7fe2b2f36c45fd43142b43e04584a732b24518eea391a94b912bd49620d47f", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r5.diff", "sha256": "549cc1ed0da908e81b928b9460b9de1ef9f5798e8cb97a132a1fbf6aca84f990", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r5.json", "sha256": "ab5629983061c5bceb451fd612c59a4f590b197844bdcca1894a37e84e3db606", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "b75ce9ecf2a01059d08b5b1296f9facc2f682772caaa24657b96d90688313d21", "opus": "ea8929a6093bce239719e0db666a2369eea3451f9015f03867f04a1ae088f3e3"}

## MSG-21 | 2026-08-20T01:55:05+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-5 | refs: -

PASS on my own inspection of the pinned export at 44a5028 plus fresh command output.

COMMAND (criterion 5), run literally from the export root /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/44a5028949ff613e87b1c0abdd5a76aa1035f52a/opus:
  `python -m pytest -q`
RESULT: `531 passed, 1 skipped in 22.92s` (exit 0).

TRUE CHANGE SET (computed by me, not taken from the author's fold list). Bash could not read the docket directory (permission denied for `diff`/`python` against the docket path), and the export carries no git history (`git status` -> "fatal: not a git repository"), so I derived 442b094 -> 44a5028 by reading branch-v080-r4.diff and branch-v080-r5.diff in full and comparing them section by section (both are renderings against the same main base, so their difference IS the fold). Findings:
- Identical file inventory in both diffs (grep of `^diff --git|^@@` over each: same 24 file sections, same order).
- Byte-identical bodies for every section except four, verified by reading r4 lines 1-3219 and r5 lines 1-3375 across paged reads (r4 1-1000, 1000-1620, 1619-1858, 1853-2874, 2874-end; r5 1-1233, 1234-1853, 1854-2553, 2554-2953, 3030-end), with the constant expected offsets (+2 after the skill, +29 after __main__, +86 after seats.py, +156 after the flow tests).
- The four differing sections are exactly: skills/debate-onboarding/SKILL.md (+3 lines), src/debate/__main__.py (smoke hunk `@@ -602,7 +777,10` -> `@@ -591,18 +766,35`), src/debate/seats.py (`@@ -169,12 +182,20` -> `@@ -169,15 +182,77`), tests/test_onboarding_flow.py (675 -> 745 lines). Their content matches fold-r4.diff line for line, and the blob hashes agree (SKILL 287c59b->8d5f068, seats 7701778->90a1e97, flow tests c71736c->1d3d60b). NO edit outside the author's fold list; the fold list is complete and honest.

FIELD DEFECT 1 (registry write race) — resolved, on my reading of the export source:
- seats.py:193-214 save_registry now writes via mkstemp+fsync+os.replace, unlinking tmp on OSError; seats.py:217-253 update_registry takes an O_EXCL lock at `<registry>.lock`, polls to a 15s deadline, then loads FRESH, mutates, saves, and unlinks the lock in `finally` (so a ChannelError from screen_credentials cannot strand it). The lock is held only for load+mutate+save, never across the model call — the minutes-long window that produced the field loss.
- __main__.py:768-791: the smoke loop passes the seat's OBSERVED result into a freshly loaded registry through update_registry and no longer calls save_registry(stale snapshot). `_apply` binds the seat id as a default arg and guards `if _seat in fresh.seats`, so a seat removed meanwhile is a no-op rather than a resurrection. `observed` is read at immediate call time, so the loop-closure trap does not bite.
- Regression coverage: tests/test_onboarding_flow.py test_concurrent_smoke_results_both_survive reproduces the interleaving (stale snapshot + concurrent locked write; both smoke results must survive — the old save would have erased beta), and test_update_registry_lock_contention_times_out pins the named refusal ("registry lock ... is held").

FIELD DEFECT 2 (/tmp scratch) — resolved: __main__.py:772 sets `scratch_base = seats.registry_path().parent / "smoke-scratch"` and passes it to smoke_seat; seats.py:625-626 creates it and setup.py:321-322 uses it as the mkdtemp `dir=` (previously `dir=None`, i.e. the system temp dir). setup.py:355-356 still rmtree's each per-run scratch in a `finally`, so nothing accumulates. test_cli_smoke_uses_config_local_scratch_and_locked_apply asserts the CLI wires a scratch base under the registry directory and that the result persists through the reload.

FOLD 3 — skills/debate-onboarding/SKILL.md:55-57 in the export instructs sequential, never-parallel smoke runs, coherent with the lock's bounded-wait-then-refuse behaviour.

COHERENCE SWEEP: no contradiction found. save_registry keeps its screen_credentials gate and its registry_payload shape (shared with onboarding.approve, so the two writers cannot drift); onboarding.approve's own transactional mkstemp+fsync+replace path and its ".debate-" leftover assertion are untouched and do not collide with the new ".seats-" temp or the "seats.json.lock" name; nothing enumerates the registry directory expecting a single file (all registry_path() uses checked); the new scratch/lock live in the user config dir, so .gitignore, MANIFEST.in and the plan's TMPDIR/basetemp confinement for release acceptance stay valid (under a scoped DEBATE_SEATS_REGISTRY the scratch is confined too). Registry files written after this change are 0600 (mkstemp mode survives os.replace) rather than umask-default; that matches the branch's own "registry stays private-by-default" comment and onboarding.approve's pre-existing behaviour, so it is a tightening, not a regression.

SCOPING JUDGEMENT (fold item 4), on the merits: leaving add/set-cost-mode/discover-save on the unlocked last-writer pattern is defensible. The atomic replace removes torn reads everywhere, and those paths' load->save windows are milliseconds, whereas the defect that actually bit had a model call inside it. Widening to update_registry would be cheap, but I could not establish it is needed, so it is not a blocker.

STANDING: criteria 1-4 are unimplicated outside the four sections above — the rest of the branch diff is byte-identical to the r4 rendering I compared here — and stand on the rounds 1-3 record closed at round 4 PASS (MSG-19). The implicated parts (registry persistence, the smoke CLI path, the skill's smoke instruction) I established on the fresh evidence cited above. Live-host acceptance evidence is author-sourced and outside my vote.

NON-BLOCKING (nothing here changes the verdict): (1) the unreleased v0.8.0 CHANGELOG section documents no line for the atomic/locked registry write or the relocated smoke scratch, both user-visible; worth one line before release. (2) A process killed mid-update leaves a stale `seats.json.lock` requiring manual removal — the refusal message says exactly that, which is honest, but a PID/mtime-based staleness note would be kinder. (3) The empty `smoke-scratch` parent directory remains after runs (per-run dirs are cleaned).

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3fc5c7499c2440f4a707daeeb014668945250e163d978c09ff3c473b7de8d116
- phase: sealed
- captured-at: 2026-08-20T01:51:31+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: ab5629983061c5bceb451fd612c59a4f590b197844bdcca1894a37e84e3db606
- source-ref: 44a5028949ff613e87b1c0abdd5a76aa1035f52a
- source-manifest-sha256: ea8929a6093bce239719e0db666a2369eea3451f9015f03867f04a1ae088f3e3
- docket-revision-sha256: 0c6d785f6c201a633c4be46cf3df65846edd1d4f73267fc63184d5831b591733
- input-sha256: 72c7a313fb30ad1a56994751f0dc6ff56a857e4f5084b6a8ea9a8dc1ae7bb53a
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-22 | 2026-08-20T01:55:05+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-5 | refs: -

PASS. Computed the r4→r5 delta by running `diff -u <docket>/branch-v080-r4.diff <docket>/branch-v080-r5.diff`; it changes only `skills/debate-onboarding/SKILL.md`, `src/debate/__main__.py`, `src/debate/seats.py`, and `tests/test_onboarding_flow.py`, matching the stated fold. Inspection confirms smoke runs are instructed sequentially; CLI smoke uses `<registry-dir>/smoke-scratch`; each observed smoke result is applied through a fresh locked registry load; and registry saves use same-directory `mkstemp`, file `fsync`, `os.replace`, and cleanup on failure. The two added regression tests cover the stale-snapshot interleaving, lock-timeout refusal, and CLI scratch/locked persistence. No contradictory or unrelated r5 change was found. Standing criteria 1–4 remain supported by the prior review record cited in the docket/plan (round-1 codex MSG-3, round-2 codex MSG-7, and round-4 PASS MSG-19). Fresh required verification run from the pinned export root: `python -m pytest -q` (executed as `cd /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/44a5028949ff613e87b1c0abdd5a76aa1035f52a/codex && python -m pytest -q`) returned `531 passed, 1 skipped in 23.34s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3fc5c7499c2440f4a707daeeb014668945250e163d978c09ff3c473b7de8d116
- phase: sealed
- captured-at: 2026-08-20T01:55:05+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: ab5629983061c5bceb451fd612c59a4f590b197844bdcca1894a37e84e3db606
- source-ref: 44a5028949ff613e87b1c0abdd5a76aa1035f52a
- source-manifest-sha256: b75ce9ecf2a01059d08b5b1296f9facc2f682772caaa24657b96d90688313d21
- docket-revision-sha256: 0c6d785f6c201a633c4be46cf3df65846edd1d4f73267fc63184d5831b591733
- input-sha256: a2106f93b620030779ccbe0bea0eaf3190a8336fb9fb16e6bcdff14103fd5575
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-23 | 2026-08-20T01:55:05+00:00 | from: owner | type: close | thread: branch-v080-onboarding-5 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-24 | 2026-08-20T02:34:55+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-6 | refs: feature/installation-onboarding-v080@2702074aaac1ae69594f4c73d31e2878ff2a4495

Round-6 review request (field-fold delta) for feature/installation-onboarding-v080, now at 2702074. Round 5 closed PASS (MSG-23); the owner's live retest then surfaced a UX finding: a user whose own wrapper has an operator-owned (env-overridable) pin sees its catalogued sibling in the approval table while their agent is silently absent. One 34-line skill-copy-only fold: table footer disclosing that operator-pinned wrappers are not auto-detected, plus an ask-once-before-approval step that registers user-named agents as manual seats with the user's declared command and cost, then re-inspects. Engine deliberately untouched; vendor-scoped sibling detection is deferred to a gated 0.8.1 plan. Verify per branch-docket-r6.md; verdicts cite your own fresh evidence; rounds 1-5 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 7f0a4857dcec213818e07d222c80e59cbc36b6ae783054acadbafbace4ba9d5b
- source-ref: 2702074aaac1ae69594f4c73d31e2878ff2a4495
- docket-revision-sha256: 5486e42fc8a17557cdfb1d85ee655bd5e9d7f1c670b6f79771d74e988d39be98
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r6.md", "sha256": "eb6a14139fdde8e05ac07f8d9d52d31ec6505de0a27b86d55d04b57c41ce8d23", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r5.diff", "sha256": "549cc1ed0da908e81b928b9460b9de1ef9f5798e8cb97a132a1fbf6aca84f990", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r5.diff", "sha256": "fdd79b6669a57e284a85c5eed7568a8b990d65bce95e1a3d8056acdfb3a9226e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r6.diff", "sha256": "16cd5801e99f391af7396d7ac22268e515d145673e2e7e841165456f7fa3fd58", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r6.json", "sha256": "7f0a4857dcec213818e07d222c80e59cbc36b6ae783054acadbafbace4ba9d5b", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "e55a29273e1101af568099a036033529906e3328777589eebf356b2acf731766", "opus": "5f93b7e297907e091e97372222bac0a6b1c6a4ef8b503e7a2a6ebbe538d6ee46"}

## MSG-25 | 2026-08-20T02:43:40+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-6 | refs: -

## Verification run (criterion 5) — PASS

Command, run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/2702074aaac1ae69594f4c73d31e2878ff2a4495/opus`:

`python -m pytest -q`

Result: `531 passed, 1 skipped in 23.11s` (exit 0). No prefixes, pipes or diagnostics were added.

## True change set (computed independently) — matches the author's fold list

I did not take the fold list as inventory. Comparing the two branch renderings in the docket:
- File inventory (`^diff --git`) is identical in `branch-v080-r5.diff` and `branch-v080-r6.diff`: the same 27 paths, same order.
- Comparing every `index`/`new file mode` line of the two branch diffs, exactly one blob hash differs: `skills/debate-onboarding/SKILL.md` `8d5f068 → 89470f3`. Every other blob pair is byte-identical (e.g. `src/debate/onboarding.py 0000000..836c6fc`, `src/debate/seats.py 12462d4..0e13f5d`, all tests) in both renderings.
- All hunks after SKILL.md shift by exactly +9 lines (r5 `skills/debate/SKILL.md` at line 672 → r6 line 681), consistent with the fold's single `@@ -36,16 +36,25 @@` (+9 net) and nothing else.
- `fold-r5.diff` carries the same `8d5f068..89470f3` pair, and the working file at `skills/debate-onboarding/SKILL.md:1-100` in the export matches the r6 rendering line for line.

So: one prose file changed, exactly as claimed; no undisclosed edit. Absence of engine changes is consistent with the declared Layer-2 deferral.

Engine-contract claims in the new copy check out on my own reading: `seats add` requires `vendor/submodel` (`src/debate/seats.py:462-465`), accepts `{prompt}` OR both `{input_path}`/`{result_path}` (`src/debate/seats.py:466-475`), takes `--cost-mode {subscription,api,local,unknown}` (`src/debate/__main__.py:267-273`); `approve` verifies and refuses on a changed `candidate_revision` (`src/debate/onboarding.py:259-267`); a manual seat does change the revision because `_candidates` enumerates all registry seats (`src/debate/onboarding.py:163-186`) and `seats add` persists via `save_registry` (`src/debate/__main__.py:792-806`). The footer claim is accurate: `discover` only resolves `CATALOG` binary names (`src/debate/seats.py:279-281`), so an operator-owned wrapper is genuinely not auto-detected.

## Blocking findings

**1. The new step 3 writes the machine registry before approval, contradicting the approved plan and the skill's own guarantees (criteria 1 and 4).**
New copy at `skills/debate-onboarding/SKILL.md:42-48` instructs, explicitly "Before asking for approval", to run `<launcher> seats add ...`. That command persists to the host registry unconditionally (`src/debate/__main__.py:805` `seats.save_registry(registry)`). This conflicts with three unamended statements:
- Approved plan §3.2, `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md:157-158`: "The user selects one or more seats. **Only then** may Debate write the machine registry and the project's committable `debate-profile.json`."
- Same file, step 4 (`skills/debate-onboarding/SKILL.md:49-51`): "Zero selections: report that onboarding stays incomplete, **write nothing**." After the fold, a user who names a wrapper and then approves nothing is left with a persisted manual seat in `~/.config/debate/seats.json`.
- Same file, `skills/debate-onboarding/SKILL.md:98`: "Never writes a registry or profile without the approve flow."

The pre-existing `seats set-cost-mode` write (step 6, line 57-58) does not set a precedent: it is post-approval, so the plan's ordering rule held through rounds 1-5. This fold is the first write ahead of selection. The plan carries an amendment history for exactly this kind of owner-authorized behavior change (plan lines 12, 16, 22, last amended for round-2 folds) and was not amended here, and the fold list does not disclose the ordering change. Remedy is copy/plan-level: carve out user-declared manual seats in the plan rule and at line 98, and have the skill disclose the write (and how to undo it via `seats remove`) before running it.

**2. Step 3 leads the user to a seat the skill's only debate path refuses (criterion 2).**
Step 3 tells the agent to register the seat with "`{prompt}` or `{input_path}`/`{result_path}`" (`skills/debate-onboarding/SKILL.md:45-46`). A `{prompt}`-only seat registers fine, is present and approvable, but Flow 2 step 4 mandates `--brokered` and calls plain `open` "never the product path" (`skills/debate-onboarding/SKILL.md:78-79`), and the brokered adapter refuses any seat without both bridge placeholders: `src/debate/opening.py:375-378` — "refused: seat ... is not brokered-capable: its command carries no {input_path}/{result_path} placeholders". So the field friction this fold targets (a user's agent silently absent) is replaced by a refusal after the user has declared, registered and approved the seat. The copy is faithful to `seats add` in isolation but incoherent with the flow it lives in; it needs to steer manual seats intended for debates to the bridge form, or warn about the v1-only outcome.

## Non-blocking observations (named so a second pass finds nothing new)

- Step 3 gives no recovery script for the refusals `add_seat` can raise — missing placeholder, unresolvable head (`src/debate/seats.py:477-481`), credential-shaped argv (`src/debate/seats.py:482-487`) — while also forbidding the agent to invent a command; an agent hitting one has no next move.
- A seat added in step 3 is labelled `existing: true` in the re-run inspect table, because `_scan` snapshots `existing_ids` from the on-disk registry before discovery (`src/debate/onboarding.py:205`). The seat the user just named is therefore presented under step 2's "existing registry entry" label. Factually true after the write, but it reads as pre-existing state.
- Test adequacy for this fold is inherently prose-level; `tests/test_plugin_manifests.py:61` only asserts the file ships. Not a defect by itself.

## Standing

The true change set is one prose file, so criteria 1-4 are implicated only where that file bears; those parts I established freshly above. The remainder of criteria 1-4 stands by citation to the round-5 PASS (MSG-23) at 44a5028, whose blob set I verified is byte-identical to this tip apart from `skills/debate-onboarding/SKILL.md`.

Verdict: NO_PASS on findings 1 and 2. Criterion 5 passed; the fold matches the true change set.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: b0da758df31b42866afd832afa37159c85fa8f72a2e828c66fe24364876b3131
- phase: sealed
- captured-at: 2026-08-20T02:40:29+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 7f0a4857dcec213818e07d222c80e59cbc36b6ae783054acadbafbace4ba9d5b
- source-ref: 2702074aaac1ae69594f4c73d31e2878ff2a4495
- source-manifest-sha256: 5f93b7e297907e091e97372222bac0a6b1c6a4ef8b503e7a2a6ebbe538d6ee46
- docket-revision-sha256: 5486e42fc8a17557cdfb1d85ee655bd5e9d7f1c670b6f79771d74e988d39be98
- input-sha256: 46e0b2eacf6cbc31b5c6af8614557253aea1b65d8c4907a6e400071ff3bc346b
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-26 | 2026-08-20T02:43:40+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-6 | refs: -

Docket hashes matched the supplied manifest. Fresh required verification from the pinned export: `python -m pytest -q` → `531 passed, 1 skipped in 25.32s`. Comparing the r5 and r6 full-branch diff index records produced exactly one change: `skills/debate-onboarding/SKILL.md` (`8d5f068` → `89470f3`), matching the fold; `git hash-object skills/debate-onboarding/SKILL.md` returned `89470f38843cb07ac9470e20beb306820de1756d`. The revised skill asks once before approval, registers only user-declared manual command/cost input, accepts both supported command placeholder forms, re-inspects after registration, and approval revalidates the candidate revision. No engine changes or coherence conflicts were found. Criteria 1–4 remain standing under the docket’s prior round-5 PASS (MSG-23).

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: b0da758df31b42866afd832afa37159c85fa8f72a2e828c66fe24364876b3131
- phase: sealed
- captured-at: 2026-08-20T02:43:40+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 7f0a4857dcec213818e07d222c80e59cbc36b6ae783054acadbafbace4ba9d5b
- source-ref: 2702074aaac1ae69594f4c73d31e2878ff2a4495
- source-manifest-sha256: e55a29273e1101af568099a036033529906e3328777589eebf356b2acf731766
- docket-revision-sha256: 5486e42fc8a17557cdfb1d85ee655bd5e9d7f1c670b6f79771d74e988d39be98
- input-sha256: 97e73252d221e197a804065916737d96085ebc409719f9f203e6d10c969ff198
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-27 | 2026-08-20T02:49:21+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-6 | refs: -

## Criterion 5 — PASS (fresh run this phase)

Command, run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/2702074aaac1ae69594f4c73d31e2878ff2a4495/opus`:

`python -m pytest -q`

Result: `531 passed, 1 skipped in 22.69s` (exit 0). No prefixes, pipes or diagnostics.

## True change set — recomputed independently; matches the fold list

Comparing every `diff --git` / `index` / `new file mode` record of `branch-v080-r5.diff` and `branch-v080-r6.diff`: identical 27-path inventory in identical order, and exactly one blob differs — `skills/debate-onboarding/SKILL.md` `0000000..8d5f068` → `0000000..89470f3`. Every other blob pair is byte-identical across the two renderings (e.g. `src/debate/onboarding.py 0000000..836c6fc`, `src/debate/opening.py 12462d4..0e13f5d`, `src/debate/seats.py 9851619..90a1e97`, all tests). `fold-r5.diff` carries the same `8d5f068..89470f3` pair and a single `@@ -36,16 +36,25 @@` hunk (+9 net); the export's working file at `skills/debate-onboarding/SKILL.md:40-48` reproduces the fold's added footer and step 3 line for line. One prose file changed, exactly as claimed; no undisclosed edit. Absence of engine changes is consistent with the declared Layer-2 deferral. (Correcting one path mislabel in my sealed pass: the `12462d4..0e13f5d` pair belongs to `opening.py`, not `seats.py`; the conclusion is unchanged.)

## Blocking findings (both re-established on fresh evidence this phase)

**1. New step 3 writes the machine registry before selection, against the approved plan's explicit ordering rule (criteria 1 and 4).**
`skills/debate-onboarding/SKILL.md:42-48` instructs the agent, explicitly "Before asking for approval", to run `<launcher> seats add ...`. That command persists to the host registry unconditionally: `src/debate/__main__.py:792-805` calls `seats.add_seat(...)` then `seats.save_registry(registry)`. The approved plan, `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md:157-158`, states: "The user selects one or more seats. **Only then** may Debate write the machine registry and the project's committable `debate-profile.json`." The same section lists "operator-authored manual seat" (line 154) as *input* to the table, not something the flow creates. The plan carries an amendment history for owner-authorized behaviour changes (lines 12, 16, 22) and was not amended; the fold list does not disclose the ordering change.

It also collides with the unamended copy in the same file: step 4's "Zero selections: report that onboarding stays incomplete, write nothing" (`skills/debate-onboarding/SKILL.md:51`) is no longer true for a user who names a wrapper and then approves nothing — they are left with a persisted manual seat in `~/.config/debate/seats.json`. (I accept the narrower reading of line 98, "Never writes a registry or profile without the approve flow", as meaning "outside Flow 1", under which step 3 is inside it; the pre-existing `seats set-cost-mode` write at step 6 supports that reading. My anchor is the plan sentence plus line 51, which the narrower reading does not rescue: `set-cost-mode` is post-selection, so this fold is the first write ahead of selection.) Remedy is copy/plan-level: carve out user-declared manual seats in the plan rule and at line 51, and have the skill disclose the write and the `seats remove` undo before running it.

**2. Step 3 steers users to a seat the skill's only debate path refuses (criterion 2, coherence sweep).**
Step 3 tells the agent to register with "`{prompt}` or `{input_path}`/`{result_path}`" (`SKILL.md:45-46`). `seats add` does accept both (`src/debate/seats.py:466-475`), so the copy is accurate in isolation. But Flow 2 step 4 mandates `--brokered` and calls plain `open` "never the product path" (`SKILL.md:78-79`), and the brokered adapter refuses any seat lacking both bridge placeholders: `src/debate/opening.py:375-381` — "refused: seat ... is not brokered-capable: its command carries no {input_path}/{result_path} placeholders". A user who declares a `{prompt}`-only wrapper therefore registers it, sees it in the re-inspected table, approves it, and is refused at debate time. The friction this fold targets (a user's agent silently absent) is replaced by a later, costlier dead end. The copy must steer manual seats intended for debates to the bridge form, or state the v1-only outcome.

## On the opposing PASS (MSG-26)

That verdict's affirmative findings I reproduce and agree with: test result, single-blob change set, ask-once-before-approval, user-declared command/cost only, re-inspect, and revision revalidation on approve (`src/debate/onboarding.py:159-186`, `211-213`; `src/debate/__main__.py:322-323`, `588-594`). Its conclusion turns on "no coherence conflicts were found", which does not engage the two artefacts above: it cites the engine's acceptance of both placeholder forms as a virtue without reaching `opening.py:375-381`, and does not address plan line 157-158 or `SKILL.md:51`. Absence of a finding is not a rebuttal of one; both are checkable against the pinned export.

## Non-blocking observations (so a second pass by me finds nothing new)

- Step 3 gives no recovery script for the refusals `add_seat` raises — missing placeholder (`seats.py:470-475`), unresolvable head (`seats.py:477-481`), credential-shaped argv (`seats.py:482-487`), invalid cost mode (`seats.py:488-491`) — while forbidding the agent to invent a command; an agent hitting one has no next move.
- A seat added in step 3 is labelled `existing: true` in the re-run table, because `_scan` snapshots `existing_ids` from the on-disk registry before discovery (`onboarding.py:205`) and `_candidates` derives the flag from it (`onboarding.py:176`). The seat the user just named is presented under step 2's "existing registry entry" label — true post-write, but it reads as pre-existing state.
- Test adequacy for this fold is inherently prose-level; `tests/test_plugin_manifests.py` only asserts the file ships. Not a defect by itself.

## Standing

The true change set is one prose file, so criteria 1-4 are implicated only where that file bears; those parts are established freshly above. The remainder stands by citation to the round-5 PASS (MSG-23) at 44a5028, whose blob set I verified byte-identical to this tip apart from `skills/debate-onboarding/SKILL.md`.

Verdict: NO_PASS on findings 1 and 2. Criterion 5 passed; the fold matches the true change set.

Controller-Decision:
- decision: NO_PASS

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 7f0a4857dcec213818e07d222c80e59cbc36b6ae783054acadbafbace4ba9d5b
- source-ref: 2702074aaac1ae69594f4c73d31e2878ff2a4495
- source-manifest-sha256: 5f93b7e297907e091e97372222bac0a6b1c6a4ef8b503e7a2a6ebbe538d6ee46
- docket-revision-sha256: 5486e42fc8a17557cdfb1d85ee655bd5e9d7f1c670b6f79771d74e988d39be98
- input-sha256: d2450b1837070038dad55cf5e6f2fb8685afb82838653f01bbee02fef5e7d5b5
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-28 | 2026-08-20T02:53:44+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-6 | refs: -

Fresh verification: `python -m pytest -q` from `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/2702074aaac1ae69594f4c73d31e2878ff2a4495/codex` completed `531 passed, 1 skipped in 22.99s` (exit 0).

The true r5→r6 delta is exactly one prose blob, `skills/debate-onboarding/SKILL.md` (`8d5f068` → `89470f3`), matching `fold-r5.diff`; no undisclosed source change was found.

Blocking findings:

1. The new Flow 1 step 3 directs `seats add` before the approval selection (`skills/debate-onboarding/SKILL.md:42-48`). That command unconditionally persists the machine registry (`src/debate/__main__.py:792-805`). This contradicts the approved plan’s explicit ordering rule that Debate may write the registry/profile only after the user selects seats (`docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md:157-158`), and makes the unchanged claim “Zero selections … write nothing” false (`skills/debate-onboarding/SKILL.md:49-51`).

2. Step 3 permits a `{prompt}`-only manual command (`skills/debate-onboarding/SKILL.md:45-46`), which `seats add` accepts (`src/debate/seats.py:466-475`), but the skill’s only product debate path mandates `open --brokered` (`skills/debate-onboarding/SKILL.md:78-79`). Brokered opening rejects any seat without both `{input_path}` and `{result_path}` (`src/debate/opening.py:375-381`). Thus a newly declared, approved `{prompt}`-only seat reaches a predictable refusal when used to start a debate. The copy must require the bridge form for debate seats or clearly limit `{prompt}` seats to legacy v1 use.

The prior-round criteria not implicated by this one-file fold stand by MSG-23; criterion 5 passed.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 7f0a4857dcec213818e07d222c80e59cbc36b6ae783054acadbafbace4ba9d5b
- source-ref: 2702074aaac1ae69594f4c73d31e2878ff2a4495
- source-manifest-sha256: e55a29273e1101af568099a036033529906e3328777589eebf356b2acf731766
- docket-revision-sha256: 5486e42fc8a17557cdfb1d85ee655bd5e9d7f1c670b6f79771d74e988d39be98
- input-sha256: 1abdd3d2612e95355c4222098e8d7c09a217b9360f2e2d58a03159ed2c92843f
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-29 | 2026-08-20T02:53:44+00:00 | from: owner | type: close | thread: branch-v080-onboarding-6 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-30 | 2026-08-20T02:57:33+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-7 | refs: feature/installation-onboarding-v080@68b6f3d6410943b545f0b46378c2ddb9f0125547

Fix-report and round-7 review request (fold-delta) for feature/installation-onboarding-v080, now at 68b6f3d. Round 6 closed NO_PASS (MSG-29) on two skill-copy findings (MSG-25): the ask-once step wrote the registry before the user's approval selection, and a {prompt}-only manual seat dead-ended at the brokered refusal after registration. One 53-line skill-only fold resolves both: collect-only step 3, pending rows in the approval question, post-selection registration of ONLY selected wrappers (disclosed, undoable), fresh re-inspect before approve, and an up-front v1-vs-bridge disclosure. The never-writes guarantee names the carve-out. Verify per branch-docket-r7.md; verdicts cite your own fresh evidence; rounds 1-6 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: ec62bf42af9ea6a9ad190653319e92fa893d106856a6e40b6fe747ef989080cc
- source-ref: 68b6f3d6410943b545f0b46378c2ddb9f0125547
- docket-revision-sha256: f118ef9d90c8ab7d89a4557f3f144ca509ded3d4368dc3d8f8fb03f282dbca8e
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r7.md", "sha256": "409d0afe63697c63b10581997b85c29d426402b8017c659498e501ee6ee07504", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r6.diff", "sha256": "16cd5801e99f391af7396d7ac22268e515d145673e2e7e841165456f7fa3fd58", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r6.diff", "sha256": "d0051449c0887fa26565b6586f3fc9db782bbd97e0d1bd36438c3c29e2ee73b9", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r7.diff", "sha256": "f327a344c504cbf34e77c6da8e8cf0439e6d7ab8acc105b0f80ab04f349943a8", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r7.json", "sha256": "ec62bf42af9ea6a9ad190653319e92fa893d106856a6e40b6fe747ef989080cc", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "384751ec11f46b945e6e3c422a26df1f5f89316a6b1141f4cbcb291fd1c69cf5", "opus": "7876e05bbe03986c5fb370fbee2ca4d1bd1dc36864f3716c2a4070bb8c5c0f58"}

## MSG-31 | 2026-08-20T03:05:35+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-7 | refs: -

## Verdict: PASS (round 7, fold-delta over 68b6f3d)

### Criterion 5 — required command
Run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/68b6f3d6410943b545f0b46378c2ddb9f0125547/opus`:

`python -m pytest -q`

Result: `531 passed, 1 skipped in 22.86s` (exit 0, no failures, no errors).

### True change set (computed, not taken from the author's fold list)
The export is not a git checkout, so I derived the delta from the two full branch diffs in the docket. Extracting every `^index ` line from `branch-v080-r6.diff` and `branch-v080-r7.diff` (Grep, all 27 entries each, same 27 `diff --git` paths in the same order) yields byte-identical post-image blob ids for 26 of 27 files; exactly one differs:

- `skills/debate-onboarding/SKILL.md`: `index 0000000..89470f3` (r6) -> `index 0000000..ee34d42` (r7)

`fold-r6.diff` declares `index 89470f3..ee34d42 100644` for that same path and nothing else. Header offsets corroborate: all `diff --git` line numbers are identical up to `skills/debate-onboarding/SKILL.md` (line 575 in both) and shift by exactly +12 afterwards (681 -> 693 … 3119 -> 3131), matching the fold's +12 net lines. So the TRUE change set is SKILL.md only, and the author's fold list is complete — no undisclosed edit. I then read the export's `skills/debate-onboarding/SKILL.md` directly: lines 42-65 and 105-112 are exactly the fold's post-image, so the shipped file is the reviewed content.

### (a) Each fold resolves its round-6 finding
1. MSG-25 finding 1 (registry write before the approval selection). Old step 3 ran `seats add` immediately on naming. New step 3 (SKILL.md:42-49) COLLECTS command and cost mode and "write NOTHING yet"; step 4 (:50-54) lists user-named wrappers as pending rows "will be registered on approval"; step 5 (:55-63) registers only SELECTED pending wrappers after the answer, discloses the registry write and its undo (`seats remove <SEAT>`), then re-runs inspect before `approve --candidate-revision`. Unselected pending wrappers are never registered (:60-61), and zero selections still writes nothing (:53-54). Resolved.
   - Engine coherence for the new ordering: `src/debate/onboarding.py:259-278` shows `approve` rescans, re-derives `_candidate_revision`, and refuses any `--allow` id absent from the registry or not present — so registering a selected wrapper *immediately before* approve, with a fresh inspect revision, is the only executable order; the skill now matches it. Plan conformance holds: the approved plan §3.2 says "The user selects one or more seats. Only then may Debate write the machine registry and the project's committable debate-profile.json" (docket copy of `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md:156-158`); the new ordering is write-after-selection, which is what the plan requires. The plan says nothing about user-named wrappers ("wrapper" does not appear in it), so the carve-out adds no plan conflict; §3.2:154 already contemplates an "operator-authored manual seat" source.
2. MSG-25 finding 2 ({prompt}-only seat dead-ends at the brokered refusal). New step 3 states, before the user decides, that a `{prompt}` wrapper serves legacy version-1 channels only and a debate-capable seat must accept BOTH `{input_path}` and `{result_path}`. This is factually exact against the engine: `src/debate/opening.py:375-381` refuses a brokered seat whose argv lacks either placeholder, and `opening.py:251-257` refuses a v1 open for a seat lacking `{prompt}`; `src/debate/seats.py:468-475` enforces the same either/or at `seats add` with a matching message. Both branches are test-covered (`tests/test_onboarding_flow.py:309 test_brokered_open_refuses_prompt_style_seats`, `:507 test_v1_open_refuses_bridge_seats`). The late refusal is now an informed choice made before declaration; the engine still legitimately supports v1 seats, so warning rather than blocking is the correct remedy. Resolved.

### (b) Reverse check — every round-6 finding has a fold
The docket records exactly two MSG-25 findings closing MSG-29 NO_PASS; folds 1 and 2 above cover both, and the true delta contains no edit outside them. No round-6 finding is unaddressed, and no fold is unaccounted for.

### (c) Coherence sweep
- Closing guarantee (SKILL.md:107-112) now reads "never writes a registry or profile ahead of the user's approval answer" with the carve-out stated explicitly; I checked every other write in the skill — `seats set-cost-mode` and `seats smoke` (step 6) both occur after approve — so the guarantee is true of the whole flow as written.
- No other branch artifact contradicts the carve-out: grep for `never writes|writes nothing|write nothing` across the export hits only `hooks/session-start:7` (hook itself: zero writes — still true, unchanged), `src/debate/onboarding.py:10,192,212` (status/inspect read-only — still true), `CHANGELOG.md:33` ("zero selected seats writes nothing" — still true per SKILL.md:53-54 and `onboarding.py:249-253`), and the skill itself. README:114-127 and :212-224 describe detection-is-not-approval, which the carve-out (user NAMED then SELECTED) does not violate.
- `seats remove` (the disclosed undo) exists and works for manual seats: `src/debate/__main__.py:283,813-814` wiring, `src/debate/seats.py:582-591` (only a PRESENT catalog seat is refused; a manual seat is removable), tested at `tests/test_seats.py:342,410`.
- Dropping the placeholder hint from step 5's `--command` template is harmless because step 3 now explains both kinds and `seats.add_seat` refuses a placeholder-less argv with an explanatory message (`seats.py:470-475`); it also refuses an unresolvable head (`seats.py:477-481`), so an unrunnable wrapper is rejected at registration rather than after a write.
- Field-defect fixes named in the docket goal are present at the tip and unchanged by this fold: locked read-modify-write of only the observed smoke result (`src/debate/__main__.py:778-788`) and scratch under the registry directory instead of the system temp dir (`__main__.py:769-772`), covered by `tests/test_onboarding_flow.py:610 test_concurrent_smoke_results_both_survive` and `:654 test_cli_smoke_uses_config_local_scratch_and_locked_apply`.

### Standing criteria
The delta is prose-only in one skill file, so criteria 1-4 are implicated only for `skills/debate-onboarding/SKILL.md`, established freshly above. For every other file the post-image blob is byte-identical to round 6, so the earlier findings stand by citation: round-4 PASS, MSG-19, as recorded in this docket's goal paragraph. Criterion 3 (test adequacy) for this fold: no code changed, and the repo's only assertion about this file is existence (`tests/test_plugin_manifests.py:54-64`); the two engine behaviors the new prose asserts are covered by the two brokered/v1 refusal tests cited above, so no new test is owed.

### Blocking findings
None. Complete list of non-blocking observations, so a second pass finds nothing new: (i) skill prose has no automated content assertion beyond file presence — pre-existing and by design; (ii) if `approve` later refuses (e.g. candidate-set race), a just-registered wrapper remains in the machine registry — disclosed in step 5 with `seats remove` as the undo, and `add_seat`'s PATH check makes the unrunnable case fail before the write; (iii) with zero pending wrappers, step 5's "re-run inspect" is a redundant read-only call — no write, no model call.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: bfea9f9a6258a8cd3c1e5f419db7750fb97782de469dc0dc387dc0826ff39ffe
- phase: sealed
- captured-at: 2026-08-20T03:03:00+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: ec62bf42af9ea6a9ad190653319e92fa893d106856a6e40b6fe747ef989080cc
- source-ref: 68b6f3d6410943b545f0b46378c2ddb9f0125547
- source-manifest-sha256: 7876e05bbe03986c5fb370fbee2ca4d1bd1dc36864f3716c2a4070bb8c5c0f58
- docket-revision-sha256: f118ef9d90c8ab7d89a4557f3f144ca509ded3d4368dc3d8f8fb03f282dbca8e
- input-sha256: 490b71876992a5279d762aa19678090a6eb07c945458af6301e35ba0f92584e5
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-32 | 2026-08-20T03:05:35+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-7 | refs: -

PASS. Fresh required verification: `python -m pytest -q` exited 0 with `531 passed, 1 skipped in 23.09s`. I compared the supplied full diffs with `diff -u branch-v080-r6.diff branch-v080-r7.diff`; its only substantive change is `skills/debate-onboarding/SKILL.md`, matching `fold-r6.diff`. The revised flow collects manual wrappers without writes, registers only selected wrappers after the approval answer, re-inspects before approval, and warns before selection that `{prompt}`-only seats are v1-only while brokered seats require both `{input_path}` and `{result_path}`. This coheres with the source bridge guard. No unrelated fold change was found; standing criteria 1-4 remain supported by the docket-recorded round-4 PASS (MSG-19).

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: bfea9f9a6258a8cd3c1e5f419db7750fb97782de469dc0dc387dc0826ff39ffe
- phase: sealed
- captured-at: 2026-08-20T03:05:35+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: ec62bf42af9ea6a9ad190653319e92fa893d106856a6e40b6fe747ef989080cc
- source-ref: 68b6f3d6410943b545f0b46378c2ddb9f0125547
- source-manifest-sha256: 384751ec11f46b945e6e3c422a26df1f5f89316a6b1141f4cbcb291fd1c69cf5
- docket-revision-sha256: f118ef9d90c8ab7d89a4557f3f144ca509ded3d4368dc3d8f8fb03f282dbca8e
- input-sha256: 01a529a150dbe8288c41c87f23e90bc9e4800edb640480ffe84877548b66590b
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-33 | 2026-08-20T03:05:35+00:00 | from: owner | type: close | thread: branch-v080-onboarding-7 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-34 | 2026-08-20T04:09:25+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-8 | refs: feature/installation-onboarding-v080@f5ed51436720ad86488abc14c4012f33d111f0ef

Round-8 review request (field-fold delta) for feature/installation-onboarding-v080, now at f5ed514. Round 7 closed PASS (MSG-33); the owner's continued live retest then surfaced a safety finding: asked to seat a new agent (grok), the host agent swept config directories to infer a model pin and printed a live OAuth token from an auth file into its transcript. One 20-line skill-copy-only fold bounds seat investigation (CLI --help and the user-pointed wrapper only; credential/auth material and config sweeps banned by name; inferences labeled UNVERIFIED and user-confirmed). Verify per branch-docket-r8.md; verdicts cite your own fresh evidence; rounds 1-7 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 06b0143bced52451d4fd1219211c60e41b05a4bbd3eaa91b46b656a9fb48773d
- source-ref: f5ed51436720ad86488abc14c4012f33d111f0ef
- docket-revision-sha256: 3805097a8b525347c21aeb1119350a910e5f5ad2e0c0b0d50bb5829b77ec9fce
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r8.md", "sha256": "49e845c462bb12b628a640d7ec9463719916ba62ca19a852212f8090bf40c60e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r7.diff", "sha256": "f327a344c504cbf34e77c6da8e8cf0439e6d7ab8acc105b0f80ab04f349943a8", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r7.diff", "sha256": "c3d80be5af11e919eb60fa0b3ac2bb37d697fd6e4d190ad347db60345fafcaf3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r8.diff", "sha256": "d870a67f33ef43476e07ae8e2b61e5c6b057c340e5cac4a5f8ecdaeaf14e0cb9", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r8.json", "sha256": "06b0143bced52451d4fd1219211c60e41b05a4bbd3eaa91b46b656a9fb48773d", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "1a199518d5e6bd1ebecd18372a55b3b3d06b862fb1dadcf6cf1652dd2ef5cead", "opus": "b07aba492f57032fa90c7f45e9fb49ee9f6d3d48ed8da9e85187a94860a0cbea"}

## MSG-35 | 2026-08-20T04:16:41+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-8 | refs: -

PASS — the single FIELD-TEST fold is the whole change set, it resolves the owner's finding, and the required command passes.

## Criterion 5 — required command

Ran literally from the export root (`pwd` = /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/f5ed51436720ad86488abc14c4012f33d111f0ef/opus), no prefixes/pipes:

`python -m pytest -q`
→ `531 passed, 1 skipped in 24.34s`

## True change set, computed independently (not from the author's fold list)

I did not take `fold-r7.diff` as the inventory. I derived the r7→r8 delta from the two branch diffs in the docket:

1. File inventory: `^diff --git` in `branch-v080-r7.diff` and `branch-v080-r8.diff` — same 27 paths, same order. Offsets are identical through line 574; from `skills/debate-onboarding/SKILL.md` onward every subsequent file header is shifted by exactly +7 (r7 693 → r8 700, … r7 3131 → r8 3138).
2. Content fingerprints: `^index ` in both diffs — all 27 pre-image/post-image blob pairs are identical except entry 15, `skills/debate-onboarding/SKILL.md`: r7 `index 0000000..ee34d42` vs r8 `index 0000000..35ee391`. Every other post-image blob (including all of `src/debate/*`, `tests/*`, hooks, manifests, README, CHANGELOG) is byte-identical between rounds, so the engine is untouched, as the fold list claims.
3. Body spot-checks: read r7 lines 1–700 vs r8 lines 1–707 (identical through 574; the SKILL.md hunk grows 112→119 lines) and the tails, r7 3113–3232 vs r8 3120–3239 — byte-identical under the +7 shift, confirming the shift is a pure insertion and not a same-length substitution elsewhere.

Conclusion: the true change set is exactly one file, `skills/debate-onboarding/SKILL.md`, +7 lines. That equals `fold-r7.diff` (`index ee34d42..35ee391`, one hunk `@@ -42,7 +42,14 @@`) and equals the author's fold list item 1. No edit is absent from the fold list.

## (a) The fold resolves the field finding

Read the export file `skills/debate-onboarding/SKILL.md` (119 lines); its step 3 (lines 45–52) now bounds investigation of a user-named agent: `--help` plus the wrapper the user points at are allowed; searching/reading credential or auth material (auth.json, tokens, keyrings, `.secrets`, session stores) is forbidden; sweeping configuration directories to infer a model pin is banned by name, with the 2026-08-20 OAuth-token incident cited as the reason; anything inferred rather than user-stated is labeled UNVERIFIED and user-confirmed before use. That is exactly the two behaviors the owner observed (config sweep to infer a pin, auth file read into the transcript), and the export content matches the r8 post-image.

## (b) Reverse check

One field finding this round, one fold, one file changed. Nothing in the fold list lacks a diff, and nothing in the diff is missing from the fold list.

## (c) Coherence sweep — no contradiction found

- Step 3 stays collect-only: the permitted acts (`--help`, reading a pointed-at script) are read-only and make no model call, so they do not disturb "write NOTHING yet", the "Zero model calls during discovery and approval" core rule, registration-after-selection in step 5, or the closing guarantees ("never writes a registry or profile ahead of the user's approval answer"; "never invokes a seat model during setup"). Running an agent CLI's `--help` is not invoking a seat model.
- Engine agrees rather than conflicts: `src/debate/seats.py:153 screen_credentials`, called from `onboarding.py:207` and `opening.py:239,426`, refuses credential-shaped seat commands; `src/debate/setup.py:50-53` carries the same guard. Nothing in the engine reads auth files or sweeps config dirs — `src/debate/seat_catalog.py` mentions `~/.codex/config.toml` only in static `notes` strings (grep for `read_text|open\(|Path\(|subprocess|run\(` in that file: no matches).
- Repo-wide `*.md` grep for `config.toml|auth.json`: the only `auth.json` mention is the new SKILL.md line itself; `config.toml` appears only in `hooks/HOOK-CONTRACT.md` about Codex hook-trust hashes, unrelated to inferring pins. No doc instructs the contrary behavior.
- Plan conformance (criterion 1): the fold reinforces the materialized approved plan's invariants — "no credential values appear in JSON, UI, logs, records, or fixtures" (plan line 528), "It never writes a registry/profile, runs discovery, invokes a seat, reads credentials" (line 238), "No automatic provider login, credential creation…" (line 597). Nothing in the plan authorizes config-sweep pin inference.

## Standing criteria

My sealed thread is empty, so I hold no prior-round MSG id of my own; I cite the closes the docket itself records: round 7 closed PASS at MSG-33 (68b6f3d) and round 4 closed PASS at MSG-19. Criteria 1–4 stand on those closes except where implicated by the true change set — the changed SKILL.md, which I established on fresh evidence above — plus the full suite re-run above as the regression check (criterion 4: no unrelated changes, proven by the 26 identical post-image blobs).

## Non-blocking observations (no finding blocks this verdict)

1. Cosmetic: the inserted text leaves SKILL.md line 52 over-long ("…confirmed by the user before use. Tell them plainly which kind they are"), breaking the file's ~72-column wrap. Prose only, no behavioral effect.
2. No test asserts the new safety clause; `tests/test_plugin_manifests.py:61` only asserts the skill file ships. That matches the branch's existing posture for skill prose (no skill-content assertions anywhere), so it is not a test-adequacy gap introduced by this fold.
3. CHANGELOG carries no entry for the guardrail. v0.8.0 is unreleased and its entries do not enumerate skill copy rules, so this is consistent, not a defect.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 726d2227777640aa7903639751a658f43748f01b4f7323975dd745e5bd8d6cc8
- phase: sealed
- captured-at: 2026-08-20T04:14:08+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 06b0143bced52451d4fd1219211c60e41b05a4bbd3eaa91b46b656a9fb48773d
- source-ref: f5ed51436720ad86488abc14c4012f33d111f0ef
- source-manifest-sha256: b07aba492f57032fa90c7f45e9fb49ee9f6d3d48ed8da9e85187a94860a0cbea
- docket-revision-sha256: 3805097a8b525347c21aeb1119350a910e5f5ad2e0c0b0d50bb5829b77ec9fce
- input-sha256: dff96baca7003c0bf331acbdffe4dcbc97690772a541845c216b588a3b2f9224
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-36 | 2026-08-20T04:16:41+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-8 | refs: -

PASS. `diff -u /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/dockets/3805097a8b525347c21aeb1119350a910e5f5ad2e0c0b0d50bb5829b77ec9fce/files/var/debate/branch-v080-onboarding-17053/branch-v080-r7.diff /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/dockets/3805097a8b525347c21aeb1119350a910e5f5ad2e0c0b0d50bb5829b77ec9fce/files/var/debate/branch-v080-onboarding-17053/branch-v080-r8.diff` reported exactly one substantive delta: the seven-line addition in `skills/debate-onboarding/SKILL.md`; it matches `fold-r7.diff`. Inspection with `sed -n '1,160p' skills/debate-onboarding/SKILL.md` confirmed the bounded investigation permits only CLI `--help` and a user-pointed wrapper, forbids auth/credential material and configuration-directory sweeps, requires inferred details to be labeled UNVERIFIED and user-confirmed, and remains coherent with collect-only step 3, post-selection registration, and the closing guarantees. No engine or unrelated branch artifact changed in this round. Standing criteria 1–4 are unimplicated and carried by the docket's round-7 PASS (MSG-33). Exact required verification: `python -m pytest -q` → `531 passed, 1 skipped in 22.98s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 726d2227777640aa7903639751a658f43748f01b4f7323975dd745e5bd8d6cc8
- phase: sealed
- captured-at: 2026-08-20T04:16:41+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 06b0143bced52451d4fd1219211c60e41b05a4bbd3eaa91b46b656a9fb48773d
- source-ref: f5ed51436720ad86488abc14c4012f33d111f0ef
- source-manifest-sha256: 1a199518d5e6bd1ebecd18372a55b3b3d06b862fb1dadcf6cf1652dd2ef5cead
- docket-revision-sha256: 3805097a8b525347c21aeb1119350a910e5f5ad2e0c0b0d50bb5829b77ec9fce
- input-sha256: 191dfca79cade0e7cccd08026c1015d6ee062263513f8439d75e0f5c37d85ca9
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-37 | 2026-08-20T04:16:41+00:00 | from: owner | type: close | thread: branch-v080-onboarding-8 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-38 | 2026-08-20T15:31:50+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-9 | refs: feature/installation-onboarding-v080@235149a0b19409b41d6e883660360fd755068151

Round-9 review request (field-fold delta) for feature/installation-onboarding-v080, now at 235149a. Round 8 closed PASS (MSG-37); the owner's retest of that build then surfaced a UX finding: the post-table onboarding copy led with protocol vocabulary (legacy version-1 channels, {prompt}-only wrappers, operator-owned pins) that a new user neither knows nor needs. One 66-line skill-copy-only fold adds a plain-words rule (agent/wrapper/bridge defined on first use; placeholders and version numbers never reach the user), restructures the post-table copy (origin, glossary, low-key bridges-later note only when relevant, then the invitation = the ask-once step), and keeps the round-6 pre-declaration warning's substance in user words with engine facts marked agent-only. Verify per branch-docket-r9.md that no gate obligation was weakened; verdicts cite your own fresh evidence; rounds 1-8 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 71d15563d9b049ded04190c7adbdbc62f18b1a74235f2fc31d659e755772bf1e
- source-ref: 235149a0b19409b41d6e883660360fd755068151
- docket-revision-sha256: 91eb4e4b4281cfbde9a249327df78b6061eca4b2e4fbc5ad7f52127a5b89e06a
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r9.md", "sha256": "92549943ca3d9b55d3fc3728f531c083e91b7840034c9a8a5de0267b79db60f1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r8.diff", "sha256": "d870a67f33ef43476e07ae8e2b61e5c6b057c340e5cac4a5f8ecdaeaf14e0cb9", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r8.diff", "sha256": "24c6e04ecca677f0432e290dc262a489975b8980774f1845574cbd8962d2e8d8", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r9.diff", "sha256": "fcf2a8361f6d6c8d47856d27e3da04d610dbdb50dc41409e6d48d7063452c5ac", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r9.json", "sha256": "71d15563d9b049ded04190c7adbdbc62f18b1a74235f2fc31d659e755772bf1e", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a22186488a0859ff49cd03ed14015730a08dbb982babc8a2b64d2e3b91bcde34", "opus": "f2bb9cd4065d54428c8ef1a5ba76dc44c9313550342bbe79a31892731c5cd81a"}

## MSG-39 | 2026-08-20T15:38:34+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-9 | refs: -

NO_PASS — criterion 5 passes and the fold's scope claim is true, but the coherence sweep (docket item (c)) establishes one blocking finding: the fold's new non-negotiable rule is contradicted by user-facing copy in the same file.

## Commands run and results

1. Criterion 5, run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/235149a0b19409b41d6e883660360fd755068151/opus` with no prefix, suffix, pipe or env diagnostics:

   `python -m pytest -q`
   → `531 passed, 1 skipped in 23.26s`

   Criterion 5 SATISFIED.

2. True change set, computed by me rather than taken from the fold list. Bash was sandbox-denied outside the export root (`diff`, `git`, `ls` and `python -c` against the docket path all returned the don't-ask-mode denial), so I compared the two branch renderings with the read tools. Grep of `^diff --git|^index |^new file mode|^deleted file mode` over `branch-v080-r8.diff` and `branch-v080-r9.diff` returns 27 identical file entries; every pre/post blob SHA pair is byte-identical between the two rounds EXCEPT:

   `skills/debate-onboarding/SKILL.md`: r8 `index 0000000..35ee391`, r9 `index 0000000..bddfa94`

   Corroborated by Grep of `^diff --git|^@@`: the SKILL.md hunk goes `@@ -0,0 +1,119 @@` → `@@ -0,0 +1,140 @@` (+21), offsets before it are identical, and every hunk after it shifts by exactly 21 lines. `fold-r8.diff` carries the header `index 35ee391..bddfa94`, matching. Reading the pinned `skills/debate-onboarding/SKILL.md` (140 lines) confirms it is the fold diff's post-state verbatim.

   Conclusion: the true change set is SKILL.md ONLY, and the author's fold list matches it. No unlisted edit. Criteria 1-4 are unimplicated outside this file and stand on the docket's recorded verdicts (round 8 PASS, MSG-37; round 4 PASS, MSG-19); note the sealed-phase thread is empty and the docketed `collab/branch-v080-onboarding-17053.debate.json` carries channel metadata only, so those MSG ids are cited as the docket records them.

## BLOCKING FINDING (1)

**F1 — the new "Plain words, always" core rule contradicts Flow 2 step 3, which instructs the agent to say a banned term to the user.**

The fold adds at `skills/debate-onboarding/SKILL.md:28-29`, under the heading "Core rules, non-negotiable" (line 18):

  "**Plain words, always.** User-facing text never says "managed version 1/2", "{prompt}", "{input_path}/{result_path}", or "operator-owned pins"."

and at line 56-57 reinforces "Never lead with legacy/version terminology; a new user does not care which channel version anything is."

But `skills/debate-onboarding/SKILL.md:112-114` (unchanged text, now governed by the new global rule) reads:

  "3. Ask for or derive the debate subject and the review target, summarize what will be created (two seats, managed-v2 brokered channel, the human as supervisor -- this session never votes), and get the user's confirmation."

The parenthetical enumerates the content of a summary delivered to the user at a confirmation prompt, and it names "managed-v2" — the exact channel-version vocabulary the new rule bans. Evidence: Grep of `managed-v2|managed v2|version-1|version 1|\{prompt\}|operator-owned pins` across the export's `skills/` returns exactly five hits — lines 28 and 29 (the rule itself), line 75 (explicitly marked agent-only), line 113, and line 116.

This is squarely the defect class the fold exists to fix: the docket's goal records the owner finding that post-table onboarding copy "led with protocol vocabulary ... that a new user neither knows nor needs." Flow 2 is the very next thing that user does — Flow 1 step 2(c) tells them "I'll offer to set that up when you start your first debate" — and the first confirmation prompt they hit there is specified to say "managed-v2 brokered channel." The fold is therefore incomplete against its own non-negotiable rule, and the file now contains two instructions an agent cannot satisfy at once.

Note the fold demonstrates the correct handling pattern elsewhere: at lines 74-77 it marks the engine facts as "(Engine fact for YOU, never for the user's ears: ...)". Line 113 receives no such marking and is not a command-selection instruction — it is a specification of what to tell the user. Nothing in the approved plan mandates the term: plan lines 183-184 require only that the agent "summarizes what it will create," lines 185-186 state the managed-version-2 channel as a system requirement rather than user copy, and lines 187-188 require reporting "in plain language" with internal detail "behind a 'details' explanation." The fix is one line and does not disturb plan conformance.

## Non-blocking observations (recorded so a second pass finds nothing new)

- `skills/debate-onboarding/SKILL.md:115-116` ("plain `debate open` without it mints a legacy version-1 channel and is never the product path") also carries version vocabulary, but it is an instruction to the agent about which command form to run, not user-facing copy, so the rule does not reach it. It is inconsistent only in that the analogous engine fact at line 75 was given an explicit agent-only marking and this one was not. Not blocking.
- "bridge" is defined at line 32 and glossed inline at 52-55, but 2(c) is conditional ("ONLY IF some listed seats cannot join managed debates yet"); when it is skipped, step 3's "bridge adapter" (line 73) is the first use. The core rule's "Define a term the first time you use it" already covers this, so it is not a separate defect.

## Obligations verified intact (no weakening found)

- Disclosure precedes the decision: line 70-74 retains the round-6 substance — "Tell them plainly, BEFORE they decide, what the seat will be able to do" — restated in user words.
- Ask-once step intact and not doubled: the invitation moves to step 2(d) (lines 58-60) and step 3 designates it explicitly ("That invitation IS the ask-once step"), still ahead of the step-4 approval ask. The naming invitation remains unconditional; only the new bridges-come-later note (2(c)) is conditional, so the r8 footer's obligation is preserved, not narrowed.
- Pending-row / post-selection registration flow untouched: steps 4-5 (lines 78-93) are outside all three fold hunks and are byte-identical to r8, including the "will be registered on approval" pending rows and the "an unselected pending wrapper is never registered at all" carve-out.
- Round-8 credential-investigation bounds untouched: lines 63-70 appear as unchanged context in `fold-r8.diff` — the bounded `--help`/named-script reading, the ban on credential and auth material and on config sweeps with the 2026-08-20 OAuth-token rationale, and the UNVERIFIED-and-confirmed requirement all survive verbatim.

PASS is withheld solely on F1. Clearing it — restating line 113's summary content in user words, or marking the term agent-only as line 75 does — with the test command still green would satisfy every docket criterion on my reading.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: b0770ae12797d5d4194518e267c5f98cc4a4b0e4174c1351ba2ccf43b7a43f1b
- phase: sealed
- captured-at: 2026-08-20T15:36:26+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 71d15563d9b049ded04190c7adbdbc62f18b1a74235f2fc31d659e755772bf1e
- source-ref: 235149a0b19409b41d6e883660360fd755068151
- source-manifest-sha256: f2bb9cd4065d54428c8ef1a5ba76dc44c9313550342bbe79a31892731c5cd81a
- docket-revision-sha256: 91eb4e4b4281cfbde9a249327df78b6061eca4b2e4fbc5ad7f52127a5b89e06a
- input-sha256: 7c64db668b77abf7d46a6702cfe4640ac1a5902dfd938f424bc0f9fcba53d10e
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-40 | 2026-08-20T15:38:34+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-9 | refs: -

PASS. Fresh required command: `python -m pytest -q` -> `531 passed, 1 skipped in 22.90s`. Coherence check `diff -u .../branch-v080-r8.diff .../branch-v080-r9.diff` yielded only the 66-line `skills/debate-onboarding/SKILL.md` fold; `git hash-object skills/debate-onboarding/SKILL.md` -> `bddfa943a65e3a5c7916ffa04413699c14b8ecf4`, matching the fold's post-image. The fold preserves the explicit before-decision capability warning, agent-only engine facts, one invitation/ask-once flow, pending-row registration only after selection, and credential-investigation ban; its added copy supplies definitions, ordered post-table guidance, and conditional bridge note. No unrelated fold change found. Criteria 1-4 remain standing after this unimplicated coherence sweep; docket records the prior round-8 PASS as MSG-37.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: b0770ae12797d5d4194518e267c5f98cc4a4b0e4174c1351ba2ccf43b7a43f1b
- phase: sealed
- captured-at: 2026-08-20T15:38:34+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 71d15563d9b049ded04190c7adbdbc62f18b1a74235f2fc31d659e755772bf1e
- source-ref: 235149a0b19409b41d6e883660360fd755068151
- source-manifest-sha256: a22186488a0859ff49cd03ed14015730a08dbb982babc8a2b64d2e3b91bcde34
- docket-revision-sha256: 91eb4e4b4281cfbde9a249327df78b6061eca4b2e4fbc5ad7f52127a5b89e06a
- input-sha256: ea11d411a2236289a2677c1ca63959e6a4e35b21d9a0e7ce97fa3b9b930ac4e1
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-41 | 2026-08-20T15:43:33+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-9 | refs: -

NO_PASS — held after deliberation. Criterion 5 passes and the fold's scope claim is true, but the docket's coherence sweep (item (c)) still establishes one blocking finding, and MSG-40 does not reach it: the codex PASS verifies that the fold *preserved* the round-6/round-8 obligations (which I agree it did) but never examines whether the fold's newly added non-negotiable rule is consistent with the copy already in the same file. That is exactly what item (c) asks.

## Commands run and results (fresh, this pass)

1. Criterion 5, run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/235149a0b19409b41d6e883660360fd755068151/opus`, no prefix, suffix, pipe, or env diagnostics:

   `python -m pytest -q`
   → `531 passed, 1 skipped in 23.15s`

   Criterion 5 SATISFIED.

2. True change set, recomputed by me this pass. Bash remains sandbox-denied outside the export root (a single `cd <docket path> && wc -l/grep` returned the don't-ask-mode denial), so I used the read tools. Grep of `^diff --git|^index ` over `branch-v080-r8.diff` and `branch-v080-r9.diff` returns the same 27 files with byte-identical blob pairs on every entry EXCEPT `skills/debate-onboarding/SKILL.md` (r8 `index 0000000..35ee391`, r9 `index 0000000..bddfa94`). `fold-r8.diff` is a single-file diff headed `index 35ee391..bddfa94`, three hunks at `@@ -25,6 +25,13 @@`, `@@ -36,11 +43,22 @@`, `@@ -49,11 +67,14 @@`. Reading the pinned `skills/debate-onboarding/SKILL.md` (140 lines) confirms it is the fold's post-state verbatim.

   Conclusion: true change set = SKILL.md ONLY; the author's fold list matches it; no unlisted edit. Criteria 1-4 are unimplicated outside this file and stand on the docket's recorded verdicts (round 8 PASS, MSG-37; round 4 PASS, MSG-19).

## BLOCKING FINDING (1) — unchanged from my sealed pass, re-established on fresh evidence

**F1 — the fold's new "Plain words, always" core rule is contradicted by Flow 2 step 3, which specifies user-facing copy containing a banned term.**

Added by the fold at `skills/debate-onboarding/SKILL.md:28-29`, under "Core rules, non-negotiable" (line 18):

  "**Plain words, always.** User-facing text never says \"managed version 1/2\", \"{prompt}\", \"{input_path}/{result_path}\", or \"operator-owned pins\"."

reinforced at lines 56-57: "Never lead with legacy/version terminology; a new user does not care which channel version anything is."

Unchanged text now governed by that global rule, `skills/debate-onboarding/SKILL.md:112-114`:

  "3. Ask for or derive the debate subject and the review target, summarize what will be created (two seats, managed-v2 brokered channel, the human as supervisor -- this session never votes), and get the user's confirmation."

The parenthetical enumerates the *content of a summary delivered to the user* at a confirmation prompt, and it names "managed-v2" — the channel-version vocabulary the new rule bans (the docket's own fold list paraphrases the rule as "user-facing text never says managed versions"). Evidence: Grep of `managed-v2|managed v2|managed version|version-1|version 1|\{prompt\}|operator-owned|\{input_path\}|\{result_path\}` across the export's `skills/` returns exactly seven hits — lines 28, 29 (the rule), 75, 76, 77 (explicitly marked agent-only), 113, and 116. The same grep over `hooks/` returns no matches.

Why blocking rather than cosmetic: this is the defect class the fold exists to remove. The docket goal records the owner finding that post-table copy "led with protocol vocabulary ... that a new user neither knows nor needs." Flow 1 step 2(c) tells that user "I'll offer to set that up when you start your first debate" (line 56); Flow 2 is the next thing they do, and the first confirmation prompt there is specified to say "managed-v2 brokered channel." The file now carries two instructions an agent cannot satisfy at once, so compliance depends on which one the reader privileges. The fold demonstrates the correct handling pattern 38 lines earlier — lines 74-77 mark the engine facts "(Engine fact for YOU, never for the user's ears: ...)". Line 113 gets no such marking and is not a command-selection instruction; it is a specification of what to say.

Nothing in the approved plan mandates the term: plan lines 183-184 require only that the agent "summarizes what it will create"; line 185-186 state the managed-version-2 channel as a system property of what Debate creates, not as user copy; lines 187-188 require plain language with internal detail "behind a 'details' explanation." The fix is one line and disturbs no plan conformance.

## Non-blocking observations (so a second pass by me finds nothing new)

- `skills/debate-onboarding/SKILL.md:115-116` ("plain `debate open` without it mints a legacy version-1 channel and is never the product path") also carries version vocabulary, but it instructs the agent which command form to run; it is not user-facing copy, so the rule does not reach it. It is inconsistent only in that the analogous engine fact at line 75 received an explicit agent-only marking and this one did not. Not blocking.
- "bridge" is defined at line 32 and glossed inline at 52-55, but 2(c) is conditional ("ONLY IF some listed seats cannot join managed debates yet"); when skipped, step 3's "bridge adapter" (line 73) is the term's first use. The core rule's "Define a term the first time you use it" already covers that, so it is not a separate defect.

## Obligations verified intact (no weakening found; concurs with MSG-40 on these)

- Disclosure precedes the decision: lines 70-74 retain the round-6 substance — "Tell them plainly, BEFORE they decide, what the seat will be able to do" — restated in user words.
- Ask-once step intact and not doubled: the invitation moves to 2(d) (lines 58-60) and step 3 designates it ("That invitation IS the ask-once step"), still ahead of the step-4 approval ask. The invitation itself stays unconditional; only the bridges-come-later note (2(c)) is conditional, so the r8 footer obligation is preserved, not narrowed.
- Pending-row / post-selection registration flow untouched: steps 4-5 (lines 78-93) fall outside all three fold hunks — "will be registered on approval" pending rows and the "an unselected pending wrapper is never registered at all" carve-out survive verbatim.
- Round-8 credential-investigation bounds untouched: lines 63-70 appear as unchanged context in `fold-r8.diff` — bounded `--help`/named-script reading, the ban on credential and auth material and on config sweeps with the 2026-08-20 OAuth-token rationale, and the UNVERIFIED-and-confirmed requirement all intact.

PASS is withheld solely on F1. Clearing it — restating line 113's summary content in user words, or marking the term agent-only as line 75 does — with `python -m pytest -q` still green would satisfy every docket criterion on my reading.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 71d15563d9b049ded04190c7adbdbc62f18b1a74235f2fc31d659e755772bf1e
- source-ref: 235149a0b19409b41d6e883660360fd755068151
- source-manifest-sha256: f2bb9cd4065d54428c8ef1a5ba76dc44c9313550342bbe79a31892731c5cd81a
- docket-revision-sha256: 91eb4e4b4281cfbde9a249327df78b6061eca4b2e4fbc5ad7f52127a5b89e06a
- input-sha256: 76493ab60b19b7d1f090333ba83231378a710bdaf6bdfe9196003a65229d9ab7
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-42 | 2026-08-20T15:48:16+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-9 | refs: -

NO_PASS — `python -m pytest -q` run from `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/235149a0b19409b41d6e883660360fd755068151/codex` completed: `531 passed, 1 skipped in 23.36s`.

Blocking finding F1: the fold adds the non-negotiable user-copy rule at `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/235149a0b19409b41d6e883660360fd755068151/codex/skills/debate-onboarding/SKILL.md:28` that user-facing text never says managed versions. Yet Flow 2 step 3 at the same file:112-114 instructs the agent to summarize to the user that it will create a “managed-v2 brokered channel.” That is user-facing version vocabulary and contradicts the new global rule; the engine-only carve-out used at lines 74-77 does not apply. The approved plan requires a plain-language summary, not that term (`/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/dockets/91eb4e4b4281cfbde9a249327df78b6061eca4b2e4fbc5ad7f52127a5b89e06a/files/docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md:183-188`).

Fresh `diff -u` of the docketed r8 and r9 branch diffs establishes the sole delta as the 66-line fold to `skills/debate-onboarding/SKILL.md`; its post-image hash is `bddfa943a65e3a5c7916ffa04413699c14b8ecf4`, matching the fold. No unlisted edit found. The remaining round-8 obligations remain intact; unimplicated criteria 1-4 stand by the docket-recorded MSG-37/MSG-19 verdicts. F1 prevents PASS.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 71d15563d9b049ded04190c7adbdbc62f18b1a74235f2fc31d659e755772bf1e
- source-ref: 235149a0b19409b41d6e883660360fd755068151
- source-manifest-sha256: a22186488a0859ff49cd03ed14015730a08dbb982babc8a2b64d2e3b91bcde34
- docket-revision-sha256: 91eb4e4b4281cfbde9a249327df78b6061eca4b2e4fbc5ad7f52127a5b89e06a
- input-sha256: ff41803dd6feabfc7d029f30f1613932e596893dbb0cbc7242ce299097fc4344
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-43 | 2026-08-20T15:48:16+00:00 | from: owner | type: close | thread: branch-v080-onboarding-9 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-44 | 2026-08-20T16:41:59+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-10 | refs: feature/installation-onboarding-v080@4f3f28d1bd1faea6ffdf3f208d820891a25be2b0

Fix-report and round-10 review request (fold-delta) for feature/installation-onboarding-v080, now at 4f3f28d. The owner completed a full live field-test pass and every finding was batched into this single change set per a new batching ruling: the round-9 F1 fix (Flow 2 speaks user words, managed-version vocabulary agent-only), locate-then-confirm seat investigation, the numbered smoke choice, tier-mismatch advisory, network-vs-spend disclosure, quiet watching, and three engine fixes (5s interactive tick, in-flight-not-stale brokered status within the adapter budget, post-open bookkeeping failures warn instead of crash-and-orphan) with a dedicated regression suite. The fold spans f5ed514..4f3f28d (three commits, 435 diff lines) materialized in the docket with the full branch diff. Verify per branch-docket-r10.md; verdicts cite your own fresh evidence; rounds 1-8 standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 9420ebb309624dc12493c29c5be8dde17b737031161e8a1c662148ae4b82ed01
- source-ref: 4f3f28d1bd1faea6ffdf3f208d820891a25be2b0
- docket-revision-sha256: 4b7fe800b25b205c5ef1b28447ecc14047226a6bd378e488bd36bde51815b9dc
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r10.md", "sha256": "83140ca34056fa4c9a6d4fd4f319be1daffb5810f8645464b83b3847416097d9", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r9.diff", "sha256": "fcf2a8361f6d6c8d47856d27e3da04d610dbdb50dc41409e6d48d7063452c5ac", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r9.diff", "sha256": "e6f8834998c4f76f5cdb2f7677b837dc1d461fef0d9142a95dbf5a123ccf42cb", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r10.diff", "sha256": "b4ab3f7717d28bbf6397bf2a3e3d0f48ccdc059d87ca7feb9a0caa12d0596c37", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r10.json", "sha256": "9420ebb309624dc12493c29c5be8dde17b737031161e8a1c662148ae4b82ed01", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "35cc9853d45cda592d33b5785df0e5a4fe9656ceed21ce3f0bfad415a3e351e9", "opus": "20b691fb8af5c6b8b05e61859d676a6861169594b91bee7e3a0b3f636e941a39"}

## MSG-45 | 2026-08-20T16:53:03+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-10 | refs: -

## Verdict: NO_PASS (2 blocking findings)

### Commands run (from the export root `/home/zoltan/.../exports/4f3f28d.../opus`)

1. `python -m pytest -q` → `536 passed, 1 skipped in 23.05s` (criterion 5 satisfied).
2. `python -m pytest -q tests/test_field_batch.py -k brokered` → `3 passed, 2 deselected in 0.44s`.
3. `python -m pytest -q tests/test_field_batch.py tests/test_watch_status.py` → `22 passed in 0.39s`.

Tooling note, stated because it bounds my evidence: Bash in this seat is confined to the export root and to `python -m pytest` invocations — `git hash-object`, `python -c`, and any read outside the export were refused by the sandbox. Findings F1/F2 below therefore rest on code reading at cited line numbers plus the pytest runs above, not on an ad-hoc interpreter probe.

### True change set (computed independently, not from the author's fold list)

Comparing the pre-/post-image blob ids in the `index` lines of `branch-v080-r9.diff` and `branch-v080-r10.diff` (both vs main) isolates exactly what moved since round 9:

- `skills/debate-onboarding/SKILL.md` bddfa94 → 5421eec
- `src/debate/__main__.py` 6b668ec → 13c52ca
- `src/debate/opening.py` 0e13f5d → 3456cda
- `src/debate/watcher.py` 6fac820 → 7cb8ce8 (absent from r9: unchanged then)
- `tests/test_field_batch.py` new, 520b5eb

All 24 other paths carry byte-identical post-image blobs in both diffs (`e2575d4` CHANGELOG, `7b7f282` README, `90a1e97` seats.py, `836c6fc` onboarding.py, etc.). So there is **no edit outside the fold list**, and criterion 4 (no unrelated changes) holds. `fold-r9.diff`'s SKILL.md pre-image `35ee391` is the round-8 blob, consistent with it spanning f5ed514→4f3f28d.

### Resolved (verified on my own reading of the export, not the diff)

- **Round-9 F1 + its non-blocking observation** — `SKILL.md:134-146`: Flow 2 step 3 summarizes in user words, and both "managed-version-2" and the `--brokered` rationale are explicitly marked agent-only engine facts. Resolved.
- **Item 2 (locate-then-confirm)** — `SKILL.md:61-93`: agent does the legwork, bounded PATH/`--help`/plain-script reads, round-8 credential and config-sweep bans restated and declared to outrank the new text, one concrete proposal per named agent with inferences labelled, "Write NOTHING yet" retained, location question only as fallback (c). Resolved.
- **Item 3 (numbered smoke choice)** — `SKILL.md:116-125`: numbers / `all (<N> calls)` / `skip` with its consequence, numeric reply is the authorization, total echoed, sequential. Resolved.
- **Item 4 (tier mismatch)** — `SKILL.md:138-143`. Resolved.
- **Item 5 (no AI spend ≠ no network)** — `SKILL.md:82-86`. Resolved.
- **Item 6 (expectation then quiet)** — `SKILL.md:159-163`. Resolved as text (but see F1, which makes its last sentence false in practice).
- **Item 9 (post-open bookkeeping)** — both open paths guarded: `__main__.py:666-678` (brokered) and `__main__.py:729-741` (plain), warn + `return 0`; `tests/test_field_batch.py:412-435` pins the warning and the single-channel outcome. Resolved.
- Criteria 1-4 are otherwise unimplicated by the true change set and stand on the round-8 PASS (MSG-37); the plan document specifies nothing about tick cadence or `watch-status` semantics, so the two engine items below are judged on correctness (criterion 2) and test adequacy (criterion 3), not plan conformance.

---

### F1 (blocking) — Item 8's DRIVING branch is unreachable during an actual in-flight seat call; the three tests pin a state that cannot occur mid-invocation

The new code is inside the `count == 0` (never-invoked) arm of `status()`:

- `watcher.py:374-391` — if the seq has **any** invocation record, `status()` returns from that arm: `INVOKED` while `age < config.retry_seconds`, else `STALE` ("…past the {retry}s retry window, so no tick is running"). The lock is never consulted there beyond the cosmetic `holder` suffix.
- `watcher.py:402-418` — the new lock-aware DRIVING return is only reached **after** that arm, i.e. only when `count == 0`.
- `watcher.py:893-902` — for a brokered channel the tick calls `record_invocation(...)` and persists state **before** the adapter child (`_save_state(config.state_path, state)  # recorded before the expensive child`); the adapter then runs at `watcher.py:951-966`. So while a seat is thinking, the state file always has `count >= 1` for that seq.
- `opening.py:513` — the brokered product open writes `"retry_seconds": 30`, loaded into `WatcherConfig.retry_seconds` at `__main__.py:193`. Seat budgets are minutes (fixture uses 1200s; `tests/test_field_batch.py:284`).

Consequence: 30 seconds into every brokered seat invocation, `watch-status` returns **STALE — "no tick is running"**, exactly the field symptom the item exists to remove, and the new branch cannot fire because the lock is only held in states where `count > 0`. `tests/test_field_batch.py:333-359` passes only because all three cases pass `{}` as the state (no invocations) — a state that is mutually exclusive with a held tick lock during a seat call. `tests/test_watch_status.py:94-113` documents the reachable arm and calls it "the commonest state of a live review", confirming the semantics I read. The tests are therefore green while the behavior is unchanged, so item 8 fails both criterion 2 and criterion 3. This also falsifies the new `SKILL.md:162-163` claim that a healthy in-flight status is what the agent will see.

Fix direction: apply the lock-plus-budget check before/inside the `count > 0` arm (measure from the invocation stamp or the lock stamp against the largest profile budget), and add a test whose state contains `{"invocations": {"<seq>": {"count": 1, "last_at": ...}}}` together with the held lock.

### F2 (blocking) — Item 7 writes a key no scheduler reads; the interactive idle it names is governed by `watch --interval`, default 180s

`opening.py:505-512` changes the brokered open to write `"scheduler_interval_seconds": 5`, with the comment that the 60s tick "made a six-message case idle for whole minutes between phases". Every consumer of that key in the tree:

- `__main__.py:168` loads it into `TimingPolicy`;
- `controller.py:289, 297, 307-314, 320-326` — the field is used **only** by `unconstrained_seconds` (a derived bound that `enforced_seconds` then clamps to `whole_case_timeout_seconds`, 3600) and by `timing.report()`, which is recorded in the case manifest and drift-checked at `controller.py:1019`.

No scheduler consults it. The cadence of the path the product actually uses is `watcher.watch()`'s `sleep(interval_seconds)` at `watcher.py:1106`, fed from `args.interval` — `__main__.py:531: p_watchloop.add_argument("--interval", type=_positive_int, default=180, ...)`. The drive hint the brokered open prints is `debate watch --root … --channel … --config … --until-close` (`opening.py:612-613`) with no `--interval`, and `SKILL.md:157-159` tells the agent to run that printed command verbatim. Repo-wide, `--interval` is set only in two tests (`tests/test_watcher_identity.py:88`, `tests/test_cli_watch.py:21`).

So after this change an interactive brokered debate still idles up to **180 seconds** between phases — worse than the 60s the commit blames. `tests/test_field_batch.py:387-409` asserts `config["scheduler_interval_seconds"] == 5`, which pins the literal write but proves nothing about cadence. Item 7 satisfies its own sentence literally while leaving the field finding it cites unfixed (criterion 2), and its test cannot detect the gap (criterion 3).

Fix direction: make the product path actually tick fast — e.g. have `watch` default `--interval` from the loaded config's `scheduler_interval_seconds`, and/or emit the interval in the `drive it:` hint — with a test that asserts the sleep interval the loop uses, not the JSON value.

### Non-blocking observations (not part of the verdict)

- `CHANGELOG.md` is byte-identical to its round-9 state (`e2575d4`), so none of the three engine behavior changes appear under v0.8.0; the section has no "Fixed" subsection, unlike v0.7.0. Worth an entry before release.
- `watcher.brokered.example.json:6` still documents `60`, and `__main__.py:168` keeps 60 as the absent-key default — consistent with "unattended channels can configure larger values", so no conflict.
- Item 9 is implemented on both open paths but pinned by a test only on the brokered one; that matches the docket's own wording, so it is not a finding.

A second pass by me over this change set would find nothing beyond F1 and F2.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 4667a3178d645c3ad63d00febff340fcded8d6155b1fc583bed1928b442a30cb
- phase: sealed
- captured-at: 2026-08-20T16:49:46+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 9420ebb309624dc12493c29c5be8dde17b737031161e8a1c662148ae4b82ed01
- source-ref: 4f3f28d1bd1faea6ffdf3f208d820891a25be2b0
- source-manifest-sha256: 20b691fb8af5c6b8b05e61859d676a6861169594b91bee7e3a0b3f636e941a39
- docket-revision-sha256: 4b7fe800b25b205c5ef1b28447ecc14047226a6bd378e488bd36bde51815b9dc
- input-sha256: e2753356da05d887a2fd295dcd56a29c1c48c5e5bb1638a517fad1c8f8831c74
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-46 | 2026-08-20T16:53:03+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-10 | refs: -

PASS. I independently compared the immutable r9/r10 branch-diff inventories: the true fold delta is exactly skills/debate-onboarding/SKILL.md, src/debate/__main__.py, src/debate/opening.py, src/debate/watcher.py, and tests/test_field_batch.py; it matches the supplied fold. Source inspection confirms all round-9 and owner-batch items 1-9, including user-facing wording, locate-then-confirm, numbered smoke authorization, tier advisory, network disclosure, quiet watching, 5-second brokered-open default, in-flight lock status, and both post-open registry-save guards. Standing criteria 1-4 are retained by round-8 PASS MSG-37; implicated behavior was rechecked. Exact required command run from the pinned export root: `python -m pytest -q` -> `536 passed, 1 skipped in 22.86s` (exit 0).

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 4667a3178d645c3ad63d00febff340fcded8d6155b1fc583bed1928b442a30cb
- phase: sealed
- captured-at: 2026-08-20T16:53:03+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 9420ebb309624dc12493c29c5be8dde17b737031161e8a1c662148ae4b82ed01
- source-ref: 4f3f28d1bd1faea6ffdf3f208d820891a25be2b0
- source-manifest-sha256: 35cc9853d45cda592d33b5785df0e5a4fe9656ceed21ce3f0bfad415a3e351e9
- docket-revision-sha256: 4b7fe800b25b205c5ef1b28447ecc14047226a6bd378e488bd36bde51815b9dc
- input-sha256: 0b9ef5e5d968d9aa15db8374979563bc17cb6e568fbef929bab531aed8525ad1
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-47 | 2026-08-20T16:58:44+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-10 | refs: -

## Deliberation verdict: NO_PASS (F1 and F2 maintained after re-verification)

### Commands run this pass (export root `/home/zoltan/.../exports/4f3f28d.../opus`)

1. `python -m pytest -q` → `536 passed, 1 skipped in 23.07s` (criterion 5 satisfied — same as MSG-45 and as codex's MSG-46 run).
2. `python -m pytest -q tests/test_field_batch.py tests/test_watch_status.py` → `22 passed in 0.72s`.

Bash in this seat remains confined to `python -m pytest` in the export root, so F1/F2 rest on code reading at the cited lines plus those runs.

### Citation correction to MSG-45

My sealed message cited `tests/test_field_batch.py:333-359`, `:387-409`, `:412-435`, `:284`. That file is 191 lines; those line numbers are wrong. The correct citations, which carry the same substance, are: the three status tests at `tests/test_field_batch.py:88-114` (all three pass `{}` as state), the interval assertion at `:142-164`, the bookkeeping test at `:167-190`, and the fixture's `timeout_seconds=1200` / `retry_seconds=30` at `:40` and `:70`. No finding changes.

### F1 (blocking, maintained) — item 8's DRIVING branch cannot fire during an ordinary in-flight seat call

Re-read of the export confirms the ordering exactly:

- `watcher.py:374-391` — if the seq has any invocation record, `status()` returns from that arm: `INVOKED` while `age < config.retry_seconds`, else `STALE` ("…past the {retry}s retry window, so no tick is running"). The lock contributes only the cosmetic `_holder_note` suffix.
- `watcher.py:402-418` — the new lock-aware DRIVING return sits after that arm, i.e. only on the `count == 0` path.
- `watcher.py:893-902` — the brokered tick calls `record_invocation(state, seq, …)` and then `_save_state(config.state_path, state)  # recorded before the expensive child`; the adapter child runs afterwards at `watcher.py:951-982`, with the tick lock held across the whole of `_run_once_locked` (`watcher.py:690-694`, released in the `finally` at `:1107-1108`). `read_status` re-reads that saved state at `watcher.py:443-444`.
- `opening.py:513` writes `"retry_seconds": 30` for the brokered product open (`__main__.py:193` loads it); seat budgets are minutes (fixture `timeout_seconds=1200`, `tests/test_field_batch.py:40`).

So 30 seconds into every brokered seat invocation the product's `watch-status` prints STALE / "no tick is running" — precisely the field symptom item 8 exists to remove — because during a live invocation `count >= 1` for that seq, and the new branch is gated on `count == 0`. The three new tests are green only because they pass `{}` (no invocations) together with a held lock, a combination that cannot occur while a seat call is in flight. `tests/test_watch_status.py:94-113` documents the arm that actually governs and calls it "the commonest state of a live review".

To be precise about reachability rather than overstate it: the new branch is reachable in the broker-recovery path, where `watcher.py:893` skips `record_invocation` for `broker_recovery is not None` and `drive_case` still runs under the lock. That narrow case is real; the ordinary seat invocation named by the item is not covered. Item 8 therefore fails criterion 2 and criterion 3, and falsifies the new `SKILL.md:162-163` claim that the agent will see a healthy in-flight status.

Fix direction unchanged: apply the lock-plus-budget check before or inside the `count > 0` arm (measure from the invocation or lock stamp against the largest profile budget), with a test whose state contains `{"invocations": {"<seq>": {"count": 1, "last_at": …}}}` plus the held lock.

### F2 (blocking, maintained) — item 7 writes a key no scheduler reads

`opening.py:505-512` writes `"scheduler_interval_seconds": 5`. Repo-wide consumers, re-checked this pass: `__main__.py:168` loads it into `TimingPolicy`; `controller.py:289, 297, 307-314, 320-326` use it only inside `unconstrained_seconds` (a budget bound that `enforced_seconds` clamps to `whole_case_timeout_seconds` = 3600) and in `timing.report()`. Nothing schedules on it.

The cadence of the path the product actually uses is `sleep(interval_seconds)` at `watcher.py:1106`, fed from `args.interval` (`__main__.py:1135`), whose default is `180` (`__main__.py:531`). The brokered open's drive hint is `debate watch --root … --channel … --config … --until-close` with no `--interval` (`opening.py:612-613`), and `SKILL.md:157-159` tells the agent to run that printed command. `--interval` is passed nowhere outside two tests (`tests/test_watcher_identity.py:88`, `tests/test_cli_watch.py:21`).

So an interactive brokered debate still idles up to 180s between phases — longer than the 60s the commit comment blames. `tests/test_field_batch.py:142-164` asserts the literal JSON value and proves nothing about cadence. Criterion 2 and criterion 3 fail for item 7.

Fix direction unchanged: default `watch --interval` from the loaded config's `scheduler_interval_seconds` and/or emit the interval in the `drive it:` hint, with a test asserting the interval the loop sleeps on.

### On codex's PASS (MSG-46)

MSG-46 reports the same suite result and the same true fold delta I computed from the r9/r10 `index` blob ids (SKILL.md, `__main__.py`, `opening.py`, `watcher.py`, new `tests/test_field_batch.py`; 24 other paths byte-identical), so criterion 4 is not in dispute. Its treatment of items 7 and 8 is presence-of-code confirmation ("5-second brokered-open default, in-flight lock status"), which both items do satisfy literally. Neither claim is contradicted by my findings; what MSG-46 does not address is whether the written key reaches a scheduler and whether the new branch is reachable in the state a live seat call produces. On the evidence above the answer to both is no, and the docket judges these two items on correctness and test adequacy, not on the presence of the literal.

### Standing and resolved items (unchanged from MSG-45)

Items 1-6 and 9 verified resolved on my own reading: `SKILL.md:134-146` (user words, agent-only engine vocabulary), `:61-93` (locate-then-confirm with the round-8 credential/config-sweep bans restated as outranking), `:116-125` (numbered smoke choice), `:138-143` (tier advisory), `:82-86` (network vs spend), `:157-163` (expectation then quiet — text resolved, but its last sentence is falsified by F1); item 9 guarded on both open paths at `__main__.py:666-681` and `:729-744`, pinned by `tests/test_field_batch.py:167-190`. Criteria 1-4 are otherwise unimplicated by the true change set and stand on the round-8 PASS (MSG-37).

Non-blocking, not part of the verdict: `CHANGELOG.md` is byte-identical to its round-9 state, so none of the three engine behavior changes are recorded under v0.8.0; `watcher.brokered.example.json:6` and the absent-key default of 60 at `__main__.py:168` remain consistent with the unattended-channel story.

A second pass by me over this change set would find nothing beyond F1 and F2.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 9420ebb309624dc12493c29c5be8dde17b737031161e8a1c662148ae4b82ed01
- source-ref: 4f3f28d1bd1faea6ffdf3f208d820891a25be2b0
- source-manifest-sha256: 20b691fb8af5c6b8b05e61859d676a6861169594b91bee7e3a0b3f636e941a39
- docket-revision-sha256: 4b7fe800b25b205c5ef1b28447ecc14047226a6bd378e488bd36bde51815b9dc
- input-sha256: 5bfb6d02ce5b7eb2b2e7edb214e7430d7eacd8362630fc1ed27671684e968f60
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-48 | 2026-08-20T17:03:26+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-10 | refs: -

Ran exactly from the pinned export root: `python -m pytest -q` → `536 passed, 1 skipped in 23.62s`.

Blocking F1 — item 8 is not correct for an ordinary in-flight brokered seat call. In `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/4f3f28d1bd1faea6ffdf3f208d820891a25be2b0/codex/src/debate/watcher.py:374`, any invocation record returns INVOKED/STALE before the new lock-aware DRIVING branch at line 406. A real brokered tick records and saves the invocation before starting the expensive adapter child (`watcher.py:893-902`, `:951-981`), while holding the tick lock (`:689-696`). With the brokered `retry_seconds` of 30 (`opening.py:513`), a seat thinking longer than 30 seconds is therefore reported STALE despite the held lock and 1200-second adapter budget. The new tests at `tests/test_field_batch.py:88-114` pass `{}` state, which omits the invocation record present in the real case. This fails correctness and test adequacy.

Blocking F2 — item 7 changes a timing/reporting key, not the interactive scheduler cadence. Brokered open writes `scheduler_interval_seconds: 5` at `src/debate/opening.py:505-513`, but the foreground product command emitted at `opening.py:612-613` supplies no interval. `debate watch` defaults `--interval` to 180 at `src/debate/__main__.py:527-533` and passes that directly to `watch()` at `:1131-1142`; `watch()` sleeps that value at `src/debate/watcher.py:1106`. The configured scheduler value is only used in `TimingPolicy`’s derived bound/report (`src/debate/controller.py:307-326`). Thus the field behavior remains up to 180 seconds idle, and `tests/test_field_batch.py:142-164` only pins the JSON literal rather than actual cadence. This fails correctness and test adequacy.

The remaining fold items appear implemented; the two findings above are the complete blocking set established in this pass.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 9420ebb309624dc12493c29c5be8dde17b737031161e8a1c662148ae4b82ed01
- source-ref: 4f3f28d1bd1faea6ffdf3f208d820891a25be2b0
- source-manifest-sha256: 35cc9853d45cda592d33b5785df0e5a4fe9656ceed21ce3f0bfad415a3e351e9
- docket-revision-sha256: 4b7fe800b25b205c5ef1b28447ecc14047226a6bd378e488bd36bde51815b9dc
- input-sha256: ec121350af979bf3411e55ad588d795555259a1b4722e177edae26320811ae43
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-49 | 2026-08-20T17:03:26+00:00 | from: owner | type: close | thread: branch-v080-onboarding-10 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-50 | 2026-08-20T17:07:12+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-11 | refs: feature/installation-onboarding-v080@df884284c4314d568c0c54f566b15df055172209

Fix-report and round-11 review request (fold-delta) for feature/installation-onboarding-v080, now at df88428. Round 10 closed NO_PASS (MSG-49) on two converged blockers, both of the same shape: the batch pinned values, not behavior. One 180-line fold resolves both: the brokered in-flight status check is a shared helper covering BOTH stale arms (the invoked-past-retry arm a live call actually reaches, with tests carrying a real invocation record plus the held lock), and the watch loop's cadence now defaults from the loaded config's scheduler_interval_seconds via _watch_interval (explicit flag wins; legacy 180s unchanged), with tests pinning the resolution. Verify per branch-docket-r11.md; verdicts cite your own fresh evidence; standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 3b5cba80fdae330427f592a9e450a10cf72298b0d55c46163ef035ca44e076b9
- source-ref: df884284c4314d568c0c54f566b15df055172209
- docket-revision-sha256: a390e122eb0a9e9ad96e23556b4e9bee1b03fa65eb52ec6db1d1fb0b2af6e60f
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r11.md", "sha256": "aa581ae521979b71a11d84e2434c04c9c57133ed797ab9676abe356fe8ab9621", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r10.diff", "sha256": "b4ab3f7717d28bbf6397bf2a3e3d0f48ccdc059d87ca7feb9a0caa12d0596c37", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r10.diff", "sha256": "572239c5f1e37a82241bc26e19ad2f9983c5089c2dc0311c881a44e74a9aee6d", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r11.diff", "sha256": "5486f3fdd9a6b8f894f42a278052b43efa63abc523c57d63a7da5eb5a04c701c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r11.json", "sha256": "3b5cba80fdae330427f592a9e450a10cf72298b0d55c46163ef035ca44e076b9", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "f7d8cdade773e31709a653f474ccf4af28329903b62d23b91a729924f1020ce1", "opus": "0082ccbd9204f6a6f6b7cc10932acfb5c97781dfc5095e793cf6faa15514e442"}

## MSG-51 | 2026-08-20T17:17:34+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-11 | refs: -

# Round 11 verdict — NO_PASS

## Criterion 5 — required command (PASSES)

Ran literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/df884284c4314d568c0c54f566b15df055172209/opus`:

`python -m pytest -q`

Result: `537 passed, 1 skipped in 25.59s` (exit 0).

## True change set (computed independently; fold list item 3 confirmed)

Bash is denied on the docket path in this seat, so I derived the delta from the two branch diffs with the file tools: I extracted every `^diff --git` and every `^@@` header from `branch-v080-r10.diff` and `branch-v080-r11.diff`. Both carry the same 29 file sections in the same order. Section start offsets are byte-identical up to `src/debate/__main__.py` (line 798 in both); thereafter the shifts are exactly +51 (`__main__.py`), +27 (`watcher.py`), +26 (`tests/test_field_batch.py`), and every downstream section (`onboarding.py`, `opening.py`, `seats.py`, `test_onboarding*.py`, `test_plugin_manifests.py`, `test_release_sync.py`, `test_session_start_hook.py`) is shifted by the constant sum +104 with identical `@@` ranges and context function names. The true change set is therefore confined to `src/debate/__main__.py`, `src/debate/watcher.py`, `tests/test_field_batch.py`. **No undisclosed edit; the author's fold list is complete as an inventory.**

Reverse check — every batch item has a corresponding fold: in-flight status (`watcher.py:377-435`), snappy interactive tick (`opening.py:512` + now wired), orphan guard (`__main__.py:691-699` and `:754-762`, test at `test_field_batch.py:193-216`). All present.

## MSG-45 F2 — RESOLVED

Verified in the export, not the diff: `_watch_interval` at `__main__.py:201-215`; flag default `None` with resolution named in help at `:549-551`; wiring at `:1153-1157`; `sleep(interval_seconds)` is the loop cadence at `watcher.py:1119`. `interval` has exactly one consumer (`__main__.py:1157`), so no stale 180 reader survives. The brokered open hint (`opening.py:612-613`) carries no `--interval`, so the printed command now genuinely ticks at the config's 5s. I also checked the risk that moving `_watcher_config` out of the inner `try` lost error handling: that `try` catches only `KeyboardInterrupt` (`:1165`) and the outer `except channel.ChannelError` (`:1167`) still wraps it — no regression.

## BLOCKING FINDING 1 — MSG-45 F1's fold uses a signal that does not measure invocation time on the very path F2 names

`_in_flight()` (`watcher.py:383-399`) decides "seat invocation in flight" from `now - lock.stamp` against the largest seat budget. `lock.stamp` is written **once, at lock acquisition**, and never refreshed: `WatcherLock.acquire()` stamps at `watcher.py:649-656`, and the class has only `acquire`/`release` (`:633-676`) — no refresh. That proxy is valid only for `run_once()` (`:702-709`), which acquires and releases per tick, i.e. the cron `watch-once` path. The foreground `watch()` loop acquires once at `:1100-1101` and holds it for the process lifetime (its own docstring, `:1078`: "The lock is held for the PROCESS lifetime … even while this one sleeps"), releasing only in `finally` at `:1120-1121`. On that path `held_for` is **watcher process uptime**, not invocation age.

That path is precisely the one F2's fold is about ("the interactive product path idled on this loop's own default", `__main__.py:206-208`) and the one the brokered open hint prints (`opening.py:612-613`). With the shipped product values — per-seat `timeout_seconds: 1200` (`opening.py:403`), `retry_seconds: 30` (`opening.py:513`) — extending `_in_flight()` to the invoked-past-retry arm (`watcher.py:411-413`) yields, for a channel driven by `debate watch`:

- **0–1200s of watcher uptime:** every past-retry seq reads `DRIVING` with a factually false detail — "brokered seat invocation in flight: tick lock held by pid N for 900s of the 1200s seat budget" — when the seat was invoked 30s ago and nothing is in flight. A seat whose adapter died silently is masked for up to 20 minutes.
- **>1200s of watcher uptime:** the same healthy, actively-driving watcher flips to `STALE` — "past the 30s retry window, **so no tick is running**" (`:414-418`) — while a tick demonstrably is running. This is the original field complaint reintroduced on a 20-minute fuse.

The invoked arm already computes the correct quantity: `age = now - record["last_at"]` (`:405`), the true invocation age. Testing that against the seat budget would be correct on both deployments and independent of lock acquisition time.

The new test cannot detect this. `test_brokered_in_flight_covers_the_invoked_past_retry_arm` (`tests/test_field_batch.py:101-116`) hand-builds a `LockState` with a 3-minute-old stamp alongside a 2.5-minute-old `last_at`; both readings of `held_for` agree there, so the test passes under either semantics and pins neither. No test exercises `_in_flight()` against a lock held longer than one invocation.

This is not a pre-existing issue standing from round 10: r10 applied the check only to the uninvoked arm; this fold moves it onto the arm a live foreground watcher occupies most of the time, which is what makes the mismatch operative.

## FINDING 2 — non-blocking: the F2 CLI wiring is unpinned

`test_field_batch.py:186-190` pins `_watch_interval` against a genuinely loaded brokered config (good — that is behavior, not a JSON value), but nothing pins that `main()` passes the resolved value to `watch()`. `tests/test_cli_watch.py:30-36` stubs `watch` with `lambda *a, **k: code`, which swallows any kwarg, so reverting `:1157` to `interval_seconds=args.interval` would leave the suite green. I rate this non-blocking because such a revert fails loudly at `sleep(None)` rather than silently, unlike the defect MSG-49 named — but given that round-10 NO_PASS was exactly "pinned values rather than behavior", a five-line test asserting `interval_seconds == 5` from a stubbed `main(["watch", ...])` on a brokered config closes it.

## FINDING 3 — non-blocking: CHANGELOG silent on the field-batch engine fixes

The v0.8.0 section (`CHANGELOG.md:9-67`) documents no entry for the three field-batch fixes or for the changed `--interval` default. The plan's CHANGELOG requirement (plan lines 456-457, 566-567) is satisfied by the section's existence, the omission predates this fold and was unchanged across r10/r11, and no `.md` in the tree mentions `interval` (checked), so nothing is left factually stale. Recording the user-visible `--interval` default change under "Changed" before release is a housekeeping item, not a gate.

## Standing criteria

Criteria 1-4 were not otherwise implicated by the true change set or the sweep and stand by citation as passed in rounds 1-8, except criterion 2 (correctness) and criterion 3 (test adequacy), which the change set implicates and which I establish above on fresh evidence: criterion 2 fails on Finding 1.

## Bar

The required command passes and the reverse check passes, but criterion 2 does not hold: the fold closing MSG-45 F1 does not resolve the finding for the deployment its companion fold identifies as the product path. NO_PASS.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 86f578496423e90f914bdd737dc7f0bfdec9f2fe78c5e4bca31f306d938540ba
- phase: sealed
- captured-at: 2026-08-20T17:14:25+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 3b5cba80fdae330427f592a9e450a10cf72298b0d55c46163ef035ca44e076b9
- source-ref: df884284c4314d568c0c54f566b15df055172209
- source-manifest-sha256: 0082ccbd9204f6a6f6b7cc10932acfb5c97781dfc5095e793cf6faa15514e442
- docket-revision-sha256: a390e122eb0a9e9ad96e23556b4e9bee1b03fa65eb52ec6db1d1fb0b2af6e60f
- input-sha256: ee769cb14efecb77b522e494e4b1cf1d18e7bc3f8a7aac3800c88cbdbe7b78f7
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-52 | 2026-08-20T17:17:34+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-11 | refs: -

PASS. Docket hashes matched. True fold delta is limited to `src/debate/__main__.py`, `src/debate/watcher.py`, and `tests/test_field_batch.py` (`r10 files: 29`, `r11 files: 29`; no unique files). `git apply --reverse --check .../branch-v080-r11.diff` exited 0 against the pinned export. The shared in-flight helper now covers both stale arms, including invoked-past-retry (MSG-45 F1); watch parses `--interval` as None and resolves brokered config cadence before calling the loop (MSG-45 F2). The prior bookkeeping/orphan guard remains covered. Fresh required verification, run literally from the export root: `python -m pytest -q` -> `537 passed, 1 skipped in 23.35s` (exit 0). No blocking finding established. Plan approval is recorded as MSG-13; unimplicated standing criteria remain standing.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 86f578496423e90f914bdd737dc7f0bfdec9f2fe78c5e4bca31f306d938540ba
- phase: sealed
- captured-at: 2026-08-20T17:17:34+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 3b5cba80fdae330427f592a9e450a10cf72298b0d55c46163ef035ca44e076b9
- source-ref: df884284c4314d568c0c54f566b15df055172209
- source-manifest-sha256: f7d8cdade773e31709a653f474ccf4af28329903b62d23b91a729924f1020ce1
- docket-revision-sha256: a390e122eb0a9e9ad96e23556b4e9bee1b03fa65eb52ec6db1d1fb0b2af6e60f
- input-sha256: 3bfdb755c18161b9887f0d9d2b18040f9146b2e75d6b748a566aa6fada325305
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-53 | 2026-08-20T17:23:17+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-11 | refs: -

# Round 11 deliberation — NO_PASS (position unchanged)

## Criterion 5 — required command (PASSES)

Run literally from my export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/df884284c4314d568c0c54f566b15df055172209/opus`:

`python -m pytest -q`

Result: `537 passed, 1 skipped in 23.36s` (exit 0).

## True change set — agreed

Re-confirmed this pass: `fold-r10.diff` carries exactly three sections (`src/debate/__main__.py`, `src/debate/watcher.py`, `tests/test_field_batch.py`), which matches the delta I derived independently in MSG-51 from the `^diff --git`/`^@@` structure of `branch-v080-r10.diff` vs `branch-v080-r11.diff` (29 sections each, same order, constant downstream shift +104 with identical hunk ranges). Codex's independent check (file counts plus `git apply --reverse --check`, MSG-52) reaches the same set. No undisclosed edit; the fold list is a complete inventory. Reverse check passes: every batch item has a fold (in-flight `watcher.py:377-435`; interval resolution `__main__.py:201-215` + `:1157`; orphan guard `__main__.py:691-699`, `:754-762`, test at `test_field_batch.py:193-216`).

MSG-45 F2 is resolved (`_watch_interval` at `__main__.py:201-215`, flag default `None` at `:549`, sole consumer at `:1157`, loop cadence `watcher.py:1119`).

## BLOCKING FINDING 1 (stands) — the F1 fold measures lock age, not invocation age, on the path F2 names as the product path

Codex's PASS states that "the shared in-flight helper now covers both stale arms" (MSG-52). That is true as a structural statement and is not the point in dispute: the dispute is what the helper measures. MSG-52 offers no evidence on that question, so nothing rebuts the following, all re-verified in the export this pass:

- `_in_flight()` (`watcher.py:383-399`) derives `held_for` from `lock.stamp` alone.
- `lock.stamp` is written once, in `WatcherLock.acquire()` (`watcher.py:649-656`). The class has only `acquire`/`release` (`:633-676`); a full grep of `watcher.py` for lock/stamp writes shows no refresh anywhere. So `held_for` = age of the lock acquisition, never age of the current invocation.
- That proxy is sound only where acquire/release brackets one invocation — `run_once()` (`:702-709`), i.e. the cron `watch-once` line. The foreground loop acquires once at `:1100-1101` and holds to process exit (`finally` at `:1120-1121`); its own docstring says so (`:1078`: "The lock is held for the PROCESS lifetime … even while this one sleeps"). On that path `held_for` is watcher **uptime**.
- That is the path the fold's companion names as the product path (`__main__.py:206-208`: "the interactive product path idled on this loop's own default") and the path the brokered open hint prints (`opening.py:612-613`: `debate watch … --until-close`).

With the shipped brokered values — `timeout_seconds: 1200` (`opening.py:403`), `retry_seconds: 30` (`opening.py:513`), `scheduler_interval_seconds: 5` (`opening.py:512`) — routing the invoked-past-retry arm (`watcher.py:411-413`) through this helper gives, for a channel driven by `debate watch`:

- **watcher uptime < 1200s:** every past-retry seq reads `DRIVING` with a factually false detail — "brokered seat invocation in flight: tick lock held by pid N for 900s of the 1200s seat budget" — when the invocation is 30s old. A seat whose adapter died silently is masked for up to 20 minutes.
- **watcher uptime > 1200s** (ordinary for `--until-close` on a multi-round case): `_in_flight()` returns `None` and the same healthy, actively-invoking watcher reports `STALE` — "past the 30s retry window, **so no tick is running**" (`:414-418`) — while a tick demonstrably is running. That is the original field complaint reintroduced, on a 20-minute fuse, on the arm a live invocation actually occupies. The trailing holder note (`_holder_note`, `:566-573`) makes the line self-contradictory rather than correct.

The correct quantity is already in hand three lines above: `age = now - record["last_at"]` (`:405`) is the true invocation age and is right on both deployments, independent of when the lock was taken.

The new test cannot see this. `test_brokered_in_flight_covers_the_invoked_past_retry_arm` (`tests/test_field_batch.py:101-116`) builds a lock stamped 11:57:00 next to `last_at` 11:57:30 at `NOW` 12:00 — the two readings agree, so the test passes under either semantics and pins neither. No test exercises `_in_flight()` with a lock held across more than one invocation.

This is not a pre-existing issue standing from earlier rounds: r10 applied the check only to the uninvoked arm; this fold is what puts it on the arm a live foreground watcher occupies. Criterion 2 (correctness) therefore fails, and MSG-45 F1 is not resolved for the deployment the fold's own companion calls the product path.

## FINDING 2 — non-blocking: F2's CLI wiring is unpinned

`test_field_batch.py:186-190` pins `_watch_interval` against a genuinely loaded brokered config, but nothing pins that `main()` hands the resolved value to `watch()`. Re-checked this pass: `tests/test_cli_watch.py:35` stubs `watch` with `lambda *a, **k: code`, swallowing kwargs, and the only other `--interval` user (`tests/test_watcher_identity.py:88`) passes `30` explicitly. Reverting `:1157` to `interval_seconds=args.interval` leaves the suite green. Non-blocking because such a revert fails loudly at `sleep(None)`; a five-line test asserting `interval_seconds == 5` from a stubbed `main(["watch", …])` on a brokered config would close it, and given that MSG-49 was exactly "pinned values, not behavior", it is worth adding.

## FINDING 3 — non-blocking: CHANGELOG silent on the field-batch fixes

The v0.8.0 section (`CHANGELOG.md:9-67`) has no entry for the three field-batch fixes or for the user-visible `--interval` default change. The plan's CHANGELOG requirement is met by the section's existence, the omission predates this fold and is unchanged across r10/r11, and no `.md` in the tree mentions `interval`, so nothing is left factually stale. Housekeeping before release, not a gate.

## Standing criteria

Criteria 1 and 4 are unimplicated by the true change set or the sweep and stand by citation as passed in rounds 1-8. Criteria 2 and 3 are implicated and established above on my own fresh evidence: criterion 2 fails on Finding 1. A second pass by me over this change set would find nothing further.

## Bar

The required command passes, the change set is fully disclosed, and F2 is resolved — but criterion 2 does not hold. NO_PASS.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: 3b5cba80fdae330427f592a9e450a10cf72298b0d55c46163ef035ca44e076b9
- source-ref: df884284c4314d568c0c54f566b15df055172209
- source-manifest-sha256: 0082ccbd9204f6a6f6b7cc10932acfb5c97781dfc5095e793cf6faa15514e442
- docket-revision-sha256: a390e122eb0a9e9ad96e23556b4e9bee1b03fa65eb52ec6db1d1fb0b2af6e60f
- input-sha256: 02ed61cc29da1226f93a93692fde0b30f9c869b2b5f9431025d1ea58eb7ca98c
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-54 | 2026-08-20T17:29:40+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-11 | refs: -

Required verification run exactly from the pinned export root: `python -m pytest -q` → `537 passed, 1 skipped in 23.20s` (exit 0).

Blocking finding — MSG-45 F1 remains incorrect on the foreground `watch` path. The true r10→r11 delta is limited to `src/debate/__main__.py`, `src/debate/watcher.py`, and `tests/test_field_batch.py`; it matches the fold inventory. In `watcher.status()`, the new shared `_in_flight()` decides against `now - lock.stamp`, but `watch()` acquires that lock once for the process lifetime. Thus its value is watcher uptime, not the current invocation age (`record['last_at']`). After a foreground watcher has run longer than the 1200s seat budget, a current invocation 60s old and past the 30s retry window reports `STALE` / “so no tick is running” while the watcher is actively executing that invocation. I reproduced that status result with the shipped timing values. Conversely, before 1200s of watcher uptime, an old failed invocation is masked as in-flight. The new test stamps the lock and invocation near each other, so it cannot detect this deployment-path mismatch.

Criterion 2 therefore fails; the shared helper’s structural coverage of both stale arms does not resolve F1 behaviorally.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: 3b5cba80fdae330427f592a9e450a10cf72298b0d55c46163ef035ca44e076b9
- source-ref: df884284c4314d568c0c54f566b15df055172209
- source-manifest-sha256: f7d8cdade773e31709a653f474ccf4af28329903b62d23b91a729924f1020ce1
- docket-revision-sha256: a390e122eb0a9e9ad96e23556b4e9bee1b03fa65eb52ec6db1d1fb0b2af6e60f
- input-sha256: bed937797340e06f0486c7782a70ee7bbbd888e861773a5273e4eeb036868e7e
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-55 | 2026-08-20T17:29:40+00:00 | from: owner | type: close | thread: branch-v080-onboarding-11 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-56 | 2026-08-20T17:32:46+00:00 | from: owner | type: review-request | thread: branch-v080-onboarding-12 | refs: feature/installation-onboarding-v080@36852335ff92d8c97db83721bfa8e99741ed1cfe

Fix-report and round-12 review request (fold-delta) for feature/installation-onboarding-v080, now at 3685233. Round 11 closed NO_PASS (MSG-55) on one blocker: the in-flight check measured the lock stamp, which the foreground watch loop holds for its whole uptime -- masking dead adapters within the budget and re-tripping the false STALE past it. The 151-line fold (plus a one-line mypy fixup) makes _in_flight take the arm-local age (invocation last_at / doorbell posted_at) against the largest adapter budget, with discriminating tests for BOTH failure directions (hours-old lock + fresh invocation = DRIVING; fresh lock + budget-exceeded invocation = STALE); the CLI interval wiring is pinned at main() level; the CHANGELOG documents the field fixes and the --interval default change. Verify per branch-docket-r12.md; verdicts cite your own fresh evidence; standing criteria may be cited by MSG id where unimplicated.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: f362a0fb337009423de3e0de33f2e9ca875af50c27856db97b19fa905abb266d
- source-ref: 36852335ff92d8c97db83721bfa8e99741ed1cfe
- docket-revision-sha256: 4a27978b59ae38e2843ccf6843bc3d1d4f96c551f46e54272be2e48d77df16c4
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-v080-onboarding-17053.debate.json", "sha256": "dae728a6222fe2783f252da5fa203b30d42617b2ed84a481bbb8ae21d7a70315", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md", "sha256": "13edd74f3eb0b4e65715b44ac2c7ac50b419b32d54ac031428e9e8bea8ae03d3", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-docket-r12.md", "sha256": "7d2cc418d88e9c6131c1cd428bc74bf9abcccc98d9b62a1e8dbf2bd262c44ea1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r11.diff", "sha256": "5486f3fdd9a6b8f894f42a278052b43efa63abc523c57d63a7da5eb5a04c701c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/fold-r11.diff", "sha256": "ceaa3815f7ead60a4ba018b4fe27852113fa0310419abfe40eaf1881afbd9ad0", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/branch-v080-r12.diff", "sha256": "845849bd0bde61203cca0964ce70582dd7968847bc5bad67877d4c8ca9b2cf65", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/branch-v080-onboarding-17053/watcher-r12.json", "sha256": "f362a0fb337009423de3e0de33f2e9ca875af50c27856db97b19fa905abb266d", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe", "opus": "63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.148.0", "command_sha256": "6ee55fd4f4c4078496f7c1ae22073e4976d49f47b94d6e61628763617ad4948f", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.235", "command_sha256": "98b041d5d38c184a2a3033db1158f9edcf624932953e8953277d89283967ee64", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "bfe9fd37eb36eb384b7637629c9f1b8255920684fcee2182cd029d68bc8090f3", "opus": "55e8f8dbd9195abb86f1b80f61551342ea11dfe48d65ac6a017e9cfc9b3f07df"}

## MSG-57 | 2026-08-20T17:41:30+00:00 | from: opus | type: verdict | thread: branch-v080-onboarding-12 | refs: -

# Round-12 verdict: PASS

## Criterion 5 — required command

Run literally from the export root `/home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/exports/36852335ff92d8c97db83721bfa8e99741ed1cfe/opus`:

`python -m pytest -q`

Result: `538 passed, 1 skipped in 23.29s` (exit 0). No prefixes, suffixes, pipes or environment diagnostics.

## True change set (computed independently, not taken from the fold list)

`git` is denied to Bash in this seat, so I differenced the two pinned branch renderings myself: extracted every `diff --git` header and every `@@` hunk header from `branch-v080-r11.diff` and `branch-v080-r12.diff`. Both list the identical 29 files, and every hunk header is byte-identical except:

- `CHANGELOG.md`: `@@ -6,6 +6,66 @@` → `@@ -6,6 +6,77 @@` (+11)
- `src/debate/watcher.py`: `@@ -374,6 +374,30 @@` → `@@ -374,6 +374,31 @@` (+1); the two downstream hunks shift `+24→+25`, `+26→+27`
- `tests/test_field_batch.py`: `@@ -0,0 +1,216 @@` → `@@ -0,0 +1,256 @@` (+40)

Every file after `tests/test_field_batch.py` shifts by exactly +52 = 11+1+40 (`2344→2396`, `2549→2601`, `3300→3352`, `3478→3530`, `3548→3600`, `3558→3610`), which pins that no other file changed size, and the three deltas match `fold-r11.diff` exactly. **The true change set is those three files — no edit absent from the author's fold list.** The disclosed "one-line mypy fixup" falls inside them (the quoted `monkeypatch: "pytest.MonkeyPatch"` annotation in the new CLI test); nothing lands outside the artifact under review.

## (a) Each fold resolves its finding — verified against export source, not the diff

**1. MSG-51 blocker (lock stamp).** `src/debate/watcher.py:383-400`: `_in_flight(age_seconds, measured_from)` no longer parses `lock.stamp`; a grep for `held_for` across the whole export returns zero hits. It still requires `lock.held`, then compares the caller's arm-local age to `max(profile.timeout_seconds ...)`. Call sites pass the correct arm: `watcher.py:412` passes `age = now - last_at` (invocation stamp), `watcher.py:430` passes `age = now - posted_at` (doorbell).

I confirmed the finding's premise directly: `watcher.py:1101-1108` shows `watch()` acquiring the lock once *outside* the loop and then ticking, so lock age really is watcher uptime — consulting it was the defect, and the arm-local age is the right measure.

The tests at `tests/test_field_batch.py:101-127` are genuinely discriminating; I traced both against the code and against the pre-fold code:
- hours-old lock (08:00, NOW 12:00) + 150s-old invocation → `150 <= 1200` → DRIVING. Pre-fold: `held_for = 14400 > 1200` → STALE, so this assertion **fails** without the fold.
- 10s-old lock (11:59:50) + 1800s-old invocation → `1800 > 1200` → STALE. Pre-fold: `held_for = 10 <= 1200` → DRIVING, i.e. a dead adapter masked, so this assertion **fails** without the fold.

Both failure directions the finding named are pinned.

**2. MSG-51 NB-2 (unpinned CLI interval wiring).** `__main__.py:201-215` `_watch_interval`, consumed at `__main__.py:1157` as `interval_seconds=_watch_interval(args.interval, watch_config)`. `tests/test_field_batch.py:130-156` stubs `cli.watch` and asserts `captured["interval_seconds"] == 5` with `--interval` absent — so `args.interval` is `None`, and a revert to `args.interval` yields `None != 5` and fails. `tests/test_field_batch.py:226-230` additionally exercises `_watch_interval` against a really-loaded config (`==5` default, `==42` explicit-flag override), so both the resolution rule and the CLI wiring are covered.

**3. MSG-51 NB-3 (CHANGELOG).** `CHANGELOG.md:68-78` documents all five field-batch engine fixes (atomic registry write + locked read-modify-write smoke results; scratch channels off the system temp dir; `--interval` config default; in-flight-not-STALE `watch-status`; post-open bookkeeping warn-not-crash) and calls out the user-visible `--interval` default change explicitly.

## (b) Reverse check

The in-flight/STALE lineage that the round-9 finding opened is still folded and unweakened: `tests/test_field_batch.py:88-98` (original uninvoked-arm case) still passes on its own merits under the new code — doorbell age 240s vs 120s debounce+grace and the 1200s budget → DRIVING with `"1200s"` in the detail. Round-10 MSG-45 F1 (both stale arms) and F2 (the JSON value must drive the loop cadence) remain pinned at `:101` and `:223-230`. No batch item above lacks a corresponding fold.

Stated assumption: the docket names a "round-9 finding" that no docket file describes, and the supplied record `collab/branch-v080-onboarding-17053.debate.json` contains only channel configuration (parties, supervisor, thread_cap, project, managed_version) with no message history, so I cannot resolve its MSG text from sealed materials. I read it as the in-flight/STALE lineage the goal paragraph tracks, which is resolved and still pinned as above; under the docket's rule that the goal-serving reading prevails, this does not block.

## (c) Coherence sweep

- No leftover `held_for` or lock-stamp read anywhere in the export.
- The reworded DRIVING detail is asserted on by no other test; `skills/debate-onboarding/SKILL.md:162` ("a seat invocation in flight within its budget is healthy, not stuck") stays coherent with the new message.
- No hardcoded 180s `--interval` default survives in README or docs; the parser help at `__main__.py:549-551` states the config-driven default, and `tests/test_cli_watch.py:21-27` only pins non-positive rejection, so there is no stale default assertion.
- The plan `docs/plans/2026-08-19-installation-driven-agent-onboarding-v0.8.0.md` has zero hits for `scheduler_interval|watch-status|in flight|STALE|interval`, so this fold touches nothing plan-scoped; criterion 1 is unimplicated and stands.

## Standing criteria

Criteria 1-4 from the round-1 docket stand for everything the true change set does not implicate, per the docket's standing clause; live-host/field evidence remains author-sourced and outside my vote — I verified the code responses only. The implicated parts (correctness, test adequacy and no-regression on the three changed files) are established on the fresh evidence above rather than by citation. Prior-round findings are cited as the docket names them: MSG-45 (round-10 F1/F2, also carried in source comments at `watcher.py:379` and `test_field_batch.py:102,223`), MSG-51 and MSG-55 (round-11).

## Blocking findings

None. I found no blocker establishable in this pass.

## Non-blocking observations

1. `tests/test_field_batch.py:159` `test_brokered_lock_past_seat_budget_is_stale` now misnames its mechanism: the lock stamp is no longer consulted, and what the case actually exercises is doorbell age (1800s) past the 1200s budget. It passes and still pins real behavior; only the name is stale.
2. `budget = max(profile.timeout_seconds for ...)` over `config.broker.profiles.values()` would raise `ValueError` on an empty profiles map. Pre-existing and untouched by this fold, and unreachable through `BrokerConfig`'s two-profile construction.
3. On the uninvoked arm a held lock reads DRIVING for any doorbell age within the largest budget (up to 1200s), even when no invocation is actually running. It is bounded by the budget, flips to STALE past it, and is unchanged in kind from the round-10-accepted design — a diagnosis delay, not a masked dead adapter.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 2b988b8becae987465ed9aae6261e3e45a6e8d750487ac60e4df6a1c824fbbb9
- phase: sealed
- captured-at: 2026-08-20T17:38:24+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 63af823ffa7cd7aadee8a4274251910788fe2531d1f49f5e28cd987b6b9786eb
- controller-config-sha256: f362a0fb337009423de3e0de33f2e9ca875af50c27856db97b19fa905abb266d
- source-ref: 36852335ff92d8c97db83721bfa8e99741ed1cfe
- source-manifest-sha256: 55e8f8dbd9195abb86f1b80f61551342ea11dfe48d65ac6a017e9cfc9b3f07df
- docket-revision-sha256: 4a27978b59ae38e2843ccf6843bc3d1d4f96c551f46e54272be2e48d77df16c4
- input-sha256: 1badfb65cf853949935b9416161b0dd59f1814953330bb4a4dad75e6ce50d32e
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.235
- isolation-mode: advisory

## MSG-58 | 2026-08-20T17:41:30+00:00 | from: codex | type: verdict | thread: branch-v080-onboarding-12 | refs: -

Verified the complete export inventory and true fold: `git apply --reverse --check /home/zoltan/Projects/debate/var/debate/branch-v080-onboarding-17053/controller/dockets/4a27978b59ae38e2843ccf6843bc3d1d4f96c551f46e54272be2e48d77df16c4/files/var/debate/branch-v080-onboarding-17053/branch-v080-r12.diff` and the corresponding `fold-r11.diff` both exited 0 with no output. The true fold is limited to CHANGELOG, watcher status logic, and regression tests. It resolves MSG-51: arm-local invocation/posted age—not lock age—governs in-flight status; both discriminating directions are tested; CLI passes the resolved config interval; and the v0.8.0 changelog records all five field fixes. Coherence sweep found no regression. Required fresh command, run literally from the export root: `python -m pytest -q` → `538 passed, 1 skipped in 23.43s`. Focused relevant suite also passed: `python -m pytest -q tests/test_field_batch.py tests/test_cli_watch.py tests/test_watcher.py` → `53 passed in 2.70s`. Standing plan approval is cited in the immutable plan as MSG-13; the prior blocking branch outcome is MSG-55.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 2b988b8becae987465ed9aae6261e3e45a6e8d750487ac60e4df6a1c824fbbb9
- phase: sealed
- captured-at: 2026-08-20T17:41:30+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: d37718de4e30dea0e8814b0a2aee970871745cd6edd243b2fcb9b80d31899cbe
- controller-config-sha256: f362a0fb337009423de3e0de33f2e9ca875af50c27856db97b19fa905abb266d
- source-ref: 36852335ff92d8c97db83721bfa8e99741ed1cfe
- source-manifest-sha256: bfe9fd37eb36eb384b7637629c9f1b8255920684fcee2182cd029d68bc8090f3
- docket-revision-sha256: 4a27978b59ae38e2843ccf6843bc3d1d4f96c551f46e54272be2e48d77df16c4
- input-sha256: 49055754d69cb819a5a84b26f427ca305122bcce507f6ee61cc9c0a21a59b1f4
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.148.0
- isolation-mode: advisory

## MSG-59 | 2026-08-20T17:41:30+00:00 | from: owner | type: close | thread: branch-v080-onboarding-12 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
