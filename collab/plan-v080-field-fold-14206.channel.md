
## MSG-1 | 2026-08-23T23:11:46+00:00 | from: owner | type: review-request | thread: plan-v080-field-fold-1 | refs: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b

Review the supplied v0.8.0 field-fold plan against every criterion in
`var/debate/plan-v080-field-fold-14206/plan-docket.md` and the exact pinned source
export at `feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b`.

This is the plan gate. Inspect the plan and source independently. Cite your own fresh
commands and evidence. Put every blocking finding in this verdict, distinguish
observations, and return PASS only when the plan is safe and executable as written.
Do not edit the plan or any channel file.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 326926458ec6e7e3a5081c9500aab42a212703e05913fa1749192b1c7591a246
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- docket-revision-sha256: a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-field-fold-14206.debate.json", "sha256": "dec1473ac06994a2b9d94d4353a904fb71746d57aa0b214fcedf94ed14a6f598", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-v080-field-fold.md", "sha256": "e6896a7f4367a6080b2c8862206bec898bd9dc79636fd8faf5d9d0de7466fbf1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket.md", "sha256": "a365693744972cb63fa7f9fb3d5e652e414d6aa07e9c57bf69a2c1b2425e7e8b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat_adapter.py", "sha256": "5e3f30bd1d0e3dd0b2ff605bc3b4412970912744c8456f944af6128ad46e71a6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/watcher.json", "sha256": "326926458ec6e7e3a5081c9500aab42a212703e05913fa1749192b1c7591a246", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347", "opus": "8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "c792316ae0bbab8f8cff3c486b9e6e430ac003b6ae209f9e2f2e9698af8b2f12", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "72037fa63a6a1065a872135c9cf28d5d6abc4a8e978378709de661732356a3ee", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279", "opus": "a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef"}

## MSG-2 | 2026-08-23T23:20:36+00:00 | from: opus | type: verdict | thread: plan-v080-field-fold-1 | refs: -

## Verdict: NO_PASS (plan gate, exhaustive adversarial bar)

Candidate ref reviewed: `feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b`, read from the pinned export root `/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/opus` (`pwd` → that path). Plan under review: docket file `docs/plans/2026-08-23-v080-field-fold.md` at docket revision `a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9`. Docket criteria from `var/debate/plan-v080-field-fold-14206/plan-docket.md`; protocol from `collab/PROTOCOL.md`.

### Fresh commands run (read-only, project-local; nothing written, no `/tmp`)

- `pwd` → export root above.
- `ls <export>/src/debate/` → `__main__.py bridge.py channel.py controller.py delta.py onboarding.py opening.py protocol_template.md seat_catalog.py seats.py setup.py watcher.py`.
- `rg -n "pair_choices|pair_menu|def suggest|symmetric" <export>/src/debate/opening.py` → hits at 394/437/456/496; read `opening.py:456-522`.
- `rg -n "permission-mode|allowedTools|--tools|isolation|sandbox|returncode|subprocess" <export>/src/debate/bridge.py`; read `bridge.py:432-537` and `bridge.py:680-714`.
- `rg -n "var/debate|VAR_DEBATE" <export>/src/debate/` → `__main__.py:377`, `__main__.py:379`, `__main__.py:914`, `protocol_template.md:99`.
- `rg -n "exited" <export>/src/debate/controller.py -C 8` → `controller.py:1308-1309`.
- Read `controller.py:336-364`, `controller.py:741-765`, `controller.py:1005-1030`, `controller.py:1245-1317`, `controller.py:1975-2046`.
- `rg -n "thread_cap" <export>/src/debate/{channel,opening,__main__}.py` → `__main__.py:619` (`--cap` default 12), `channel.py:116`, `channel.py:422`.
- `rg -n "testpaths|\[tool.pytest|addopts" -A 6 <export>/pyproject.toml` → `testpaths = ["tests"]`, `addopts = ["--basetemp=.pytest-tmp"]`.
- `rg -n -i "four call|4 call|two call|2 call|one lap|model calls" <export>/README.md <export>/skills/debate/SKILL.md <export>/skills/debate-onboarding/SKILL.md` → only "zero model calls" during discovery; **no documented per-case call budget**.
- `rg -n -i "lap|thread cap" <export>/README.md` → `README.md:140` ("New channels record managed_version 1 and default to a 12-entry thread cap"), `README.md:230`.
- `rg -n "close" <export>/src/debate/channel.py`; read `channel.py:10-49`, `channel.py:612-656`.
- `rg -c "^\|" <export>/skills/*/SKILL.md <export>/README.md`; read `skills/debate-onboarding/SKILL.md:1-200`.
- `rg -n "retryable" <export>/src/debate/*.py` → `controller.py:75-78`, `controller.py:1271` (timeout only), `watcher.py:1005`.

### Plan claims I independently confirmed against the export

- `opening.py:472-473` — `pair_choices` returns `[]` when `suggestion is None`, and `pair_menu` (`496-515`) returns `[]` in the same case, while `suggest_pair_with_reason` (`414-434`) returns `None` whenever the wanted class has no pairable pair and there is no remembered pair. Plan §2 bullet 2 is accurate.
- `bridge.py:694-705` — `_run` calls `run_seat`, then `parse_answer`/`write_result` and `return 0` **without ever reading `completed.returncode`**; the status is only printed (`bridge.py:533`). Plan §2 bullet 4 is accurate.
- `bridge.py:444` appends only `isolation_argv + no_persistence_argv`; there is no verification/tool argument surface. Plan §2 bullet 3's code half is accurate.
- Result contract is decision + free-form body: `controller.py:33` (`RESULT_SCHEMA_VERSION = 1`), `controller.py:794-830`, and the contract published to adapters at `controller.py:1014-1025` (`required_fields` = schema_version, entry_type, body, runtime_model, decision). Plan §2 bullet 5 accurate.
- `controller.py:1308-1309` is the "adapter exited N" text the plan quotes; `controller.py:355-358` requires `runtime_root` strictly below `<repo>/var/debate`, so Slice C.1's "legacy explicit path keeps loading, other roots rejected as before" is a correct statement of current behavior; `__main__.py:377-379` really does hard-code `var/debate/...` for delta dockets.
- `controller.py:745-748` creates exactly `home/`, `build/`, `tmp/` per invocation root (`controller.py:1209`), so Slice C.5's prune scope names real directories and leaves `result.json`/`input.json`/`stdout.txt`/`stderr.txt` (`1213-1214`, `1284-1287`) in place.
- Slice D.2's supervisor `close`-typed correction uses existing authority: `channel.py:64-70` (`OPENER_TYPES` includes `close`, "one-shot close-correction idiom") and `channel.py:622-632` (supervisor exempt from opener and single-open-thread rules). No new record type is needed.
- Slice A.5's "the exact table already specified" resolves to `skills/debate-onboarding/SKILL.md:40-47`.
- Scope arithmetic in §1 is honest: 10 implemented (1,2,3,6,7,8,9,11,12,13) + 3 deferred (4,5,10) + finding 14 split = 14, with §6 non-goals matching the deferrals one-for-one. No deferred design leaks into §4.

### Blocking findings

**B1 — Slice A.4 states a per-case call budget the engine at `e5c90f6` does not enforce (docket criteria 2, 8, 9).**
Plan §4, Slice A, implementation item 4: "An ordinary review is one channel and at most the existing two-call agreement/four-call disagreement budget", and the Slice A test bullet "assert the two/four-call limits with fake seats".
Source contradiction: `controller.py:1993-2046`. On disagreement the case stays in `deliberation` and invokes **one seat per entry** until `_agreement` succeeds or `len(entries) >= thread_cap` closes NO_PASS with `thread-cap-exhausted` (`1997-2004`, `2038-2045`). There is no one-lap limit. With the product default cap of 12 (`__main__.py:619`, `channel.py:116`, `channel.py:422`, `README.md:140`), a case that starts with the review-request entry plus the two revealed sealed verdicts (3 entries) can run up to 9 further single-seat invocations: worst case ≈ **11 model calls**, not 4. "Two calls on agreement" is correct (`1707-1775`); "four on disagreement" is not an existing engine property, and `rg` over README and both SKILL files found no prior 2/4 claim to inherit.
Why blocking: the skill would quote a worst-case spend to the user that the engine will not hold to, which is precisely the "budget the engine does not own" failure in criterion 2, and the prescribed test cannot pass without an unspecified engine change (a lap cap plus a terminal rule for persistent disagreement) — a material design decision left to the implementer, contrary to criterion 8.
Smallest adequate correction: in Slice A.4 either (a) state that an `ordinary` product open records `thread_cap = 5` so the engine itself bounds the case at 2 sealed + 2 deliberation invocations before `thread-cap-exhausted`, and say so in the skill's pre-open confirmation; or (b) drop the "four-call" wording and state the real bound ("2 calls on agreement; on disagreement, one seat per entry up to the recorded thread cap"). One sentence either way; the test bullet must then assert whichever bound is chosen.

**B2 — the mandatory `verification` object has no stated compatibility rule for hand-authored adapters (docket criteria 4, 8, 9).**
Plan §4, Slice B.4 ("Replace the free-form-only answer contract with a bounded structured `verification` object") and §8 checklist ("Structured evidence is mandatory and labelled seat-declared") make the object required, while the only mention of the affected population is a test bullet: "…and custom-adapter compatibility".
Source contradiction: `controller.py:33` pins `RESULT_SCHEMA_VERSION = 1` and `controller.py:1014-1025` publishes `required_fields` to **every** adapter, including hand-authored `{input_path}/{result_path}` adapters, which `skills/debate-onboarding/SKILL.md:104-107` and README explicitly admit into fully managed debates without isolation flags. Making `verification` required at schema_version 1 refuses every existing custom adapter result at `_parse_result` (`controller.py:794-830`); making it optional for them defeats "mandatory". The plan never says which, so "custom-adapter compatibility" has no defined expected outcome for its own test.
Smallest adequate correction: add one sentence to Slice B.4 fixing the rule — e.g. "`verification` is required for verdict results at `RESULT_SCHEMA_VERSION 2`; `schema_version 1` results are still accepted, recorded as `verification-status: absent`, and cannot carry a PASS" — and add `controller.py:1018-1024`'s published `required_fields` list to the §5 file map so the adapter-facing contract changes with it.

### Non-blocking observations

1. Slice B.5 calls "a non-zero status … a retryable adapter failure" without distinguishing the bridge's own deterministic refusal exit 2 (`bridge.py:708-714`) from a nested-seat non-zero. Today `controller.py:1309` raises with `retryable=False` (only the timeout at `controller.py:1271` is retryable), so a blanket flip would spend a paid retry on refusals that cannot succeed. Suggest a distinct bridge exit code for "nested seat exited non-zero" and mark only that one retryable.
2. §2 asserts the installed Claude CLI documents `--permission-mode`, `--tools`, **and** `--allowedTools`; `--tools` and `--allowedTools` are redundant on their face. I did not query the host CLI from this seat, so I neither confirm nor refute it. Slice B.2 already gates cataloguing on recorded installed-help evidence — keep that gate and drop whichever flag the recorded help does not actually show, and correct §2 to say the flag set is to be confirmed rather than established.
3. Slice B.4's `status: unable` → mandatory `NO_PASS` makes PASS unreachable for any review where the seat runs no command. State explicitly that read-only inspection commands over the export (`rg`, `sed`, `wc`) count as `performed`, so `unable` stays reserved for seats that genuinely cannot execute anything.
4. Slice B.1-B.2 (old registries load with capability unknown; admission refuses without a verified/declared basis) means already-approved seats stop being admissible for product debates until re-discovery or an explicit declaration. That is the right fail-closed direction, but it is an upgrade step users will hit; Slice D should name it in the CHANGELOG/README bullet list.
5. Slice A.2 makes non-empty `goal`/`review_domain`/`stop_rule`/`review_mode` part of the brokered product open, which is a CLI-breaking change for existing scripted `open --brokered` callers. Low cost pre-release, but worth stating whether the engine requires them or only the product path does.
6. Slice C's root-collection fix is sound for the reason the plan gives: pytest's default `norecursedirs` skips dotted directories, so `.debate/` is not collected. Note that in this repository the effect is already masked by `testpaths = ["tests"]` in `pyproject.toml:52`; the failure mode is real in a *user's* project, and the test fixture should be written that way (no root `testpaths`) or it will pass vacuously.

### Criterion roll-up

1 scope/proportionality — holds. 2 review-mode contract — **fails** (B1). 3 verification capability and security — holds, with observation 2. 4 evidence contract — **fails** (B2). 5 non-zero policy — holds, with observation 1. 6 footprint/cleanup — holds, with observation 6. 7 installed workflow — holds; the correction flow uses `close`-as-opener authority that already exists. 8 execution readiness — **fails** via B1 and B2. 9 internal consistency — **fails** via B1 (Slice A.4 vs `controller.py:1993-2046`).

Two blocking findings, both correctable with a sentence each plus one added file-map entry. Everything else in the plan checked out against the pinned source. Per the fixed lifecycle, the plan stays DRAFT, the author folds these in one batch, and re-review opens a new case in this channel.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 3e972e053821d128d1e1c2f362fe472583aae5068d4e6ccefca7ad0b29ecdba0
- phase: sealed
- captured-at: 2026-08-23T23:20:36+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d
- controller-config-sha256: 326926458ec6e7e3a5081c9500aab42a212703e05913fa1749192b1c7591a246
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef
- docket-revision-sha256: a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9
- input-sha256: fc442c23b060976905ef372fb078fe962212bcdd154343ce23a78aef9d4dc673
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-3 | 2026-08-23T23:20:36+00:00 | from: codex | type: verdict | thread: plan-v080-field-fold-1 | refs: -

Candidate ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b. I inspected the pinned export at /home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/codex and the immutable plan at /home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/dockets/a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9/files/docs/plans/2026-08-23-v080-field-fold.md. `pwd` returned the pinned export; `find ... -type f -print | sort` enumerated the export and docket; `sha256sum` matched every supplied docket hash. `sed`, `rg`, and `nl -ba` were used for the cited source/plan contracts.

Blocking findings:

1. Evidence bounds are promised but not specified. Plan §4, Slice B item 4 (/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/dockets/a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9/files/docs/plans/2026-08-23-v080-field-fold.md:205-209) says command, excerpt, item-count, and total-byte limits are explicit, but gives none. Its oversize test requirement (:227-229) consequently has no acceptance boundary. The current engine has only the whole-result 1 MiB ceiling at /home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/codex/src/debate/controller.py:778-783. This fails the docket's bounded, schema-checkable, execution-ready evidence requirement: an implementer must invent the material limits. Smallest correction: state exact maxima for verification items, UTF-8 command bytes, UTF-8 output bytes, and aggregate verification bytes; state their interaction with the existing 1 MiB result ceiling and require the corresponding JSON-Schema constraints.

2. Pruning is not race-safe as specified. Plan §4, Slice C item 4 (/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/dockets/a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9/files/docs/plans/2026-08-23-v080-field-fold.md:257-266) requires only that no watcher lock/process be live; it does not require the prune operation to acquire and hold that lock through revalidation, deletion, and receipt writing. A check-then-delete can race a watcher start and remove an active invocation's `home/`, `build/`, or `tmp/`. The current contract already provides the lock primitive: /home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/codex/src/debate/watcher.py:628-685 defines `WatcherLock`, and :711-718 and :1076-1130 show regular and foreground watchers hold it while driving work. Smallest correction: require prune to take the same exact-channel `WatcherLock` non-blockingly, then re-read and validate matching config and terminal state while holding it; retain the lock until deletion and append-only receipt completion, refusing without mutation if acquisition or any validation fails.

Non-blocking observations: the candidate's existing local gates are green, but do not validate the planned changes. Fresh commands/results: `env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_ADDOPTS='--basetemp=/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/cases/plan-v080-field-fold-1/invocations/1-codex-1/pytest-basetemp' python3 -m pytest -q` returned `810 passed, 1 skipped, 1 warning in 89.22s`; `/home/zoltan/Projects/debate/.venv/bin/ruff check --no-cache .` returned `All checks passed!`; `/home/zoltan/Projects/debate/.venv/bin/mypy --cache-dir=/dev/null .` returned `Success: no issues found in 53 source files`. The pytest basetemp override was necessary to preserve the read-only export; its sole warning was an attempted, denied `.pytest_cache` write in that export.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 3e972e053821d128d1e1c2f362fe472583aae5068d4e6ccefca7ad0b29ecdba0
- phase: sealed
- captured-at: 2026-08-23T23:20:36+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347
- controller-config-sha256: 326926458ec6e7e3a5081c9500aab42a212703e05913fa1749192b1c7591a246
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279
- docket-revision-sha256: a9c38b432bc0a8f106cb37bfdf9cc6fbd2e60fcc76b02ad540e7c058b6c2daf9
- input-sha256: e7c82add8dcd62b79d3c64f22b95c0aa7709dbca8436f4877e39d83ad8355dbf
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.0
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-4 | 2026-08-23T23:20:36+00:00 | from: owner | type: close | thread: plan-v080-field-fold-1 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-5 | 2026-08-23T23:24:34+00:00 | from: owner | type: review-request | thread: plan-v080-field-fold-2 | refs: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b

Re-review the amended v0.8.0 field-fold plan. Verify the complete round-1 fold in
`var/debate/plan-v080-field-fold-14206/fold-list-r1.md` against the original
`var/debate/plan-v080-field-fold-14206/plan-round1.md`, the current plan, the full
round-1 docket, and the pinned candidate source. Follow every requirement in
`var/debate/plan-v080-field-fold-14206/plan-docket-r2.md`.

Use your own fresh diff and source inspection. Return PASS only if all original
criteria now hold and the fold introduced no new blocker. Do not edit any supplied
file or channel record.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 6909647061e64650eb0a2bb29511292734d3da072ea3826e12eb2504536ed4e1
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- docket-revision-sha256: 4d814d192ae15a27f0225926339700404b527e2fadf64ac115daae5d30432189
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-field-fold-14206.debate.json", "sha256": "dec1473ac06994a2b9d94d4353a904fb71746d57aa0b214fcedf94ed14a6f598", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-v080-field-fold.md", "sha256": "754e6ada306c1c484d21ad6acc8fd4ea452da79593539ed450857e645eabf1e2", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket.md", "sha256": "a365693744972cb63fa7f9fb3d5e652e414d6aa07e9c57bf69a2c1b2425e7e8b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat_adapter.py", "sha256": "5e3f30bd1d0e3dd0b2ff605bc3b4412970912744c8456f944af6128ad46e71a6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/watcher.json", "sha256": "6909647061e64650eb0a2bb29511292734d3da072ea3826e12eb2504536ed4e1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round1.md", "sha256": "e6896a7f4367a6080b2c8862206bec898bd9dc79636fd8faf5d9d0de7466fbf1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r1.md", "sha256": "a20f21a0d9315830212270bc34e5c187ced353b13702a6d5d923ab69955970c8", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r2.md", "sha256": "9b7b5085d7c2a65bbe11f5fb40d908eddcaa3a18185dad8a89b17b72f7cfdf88", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347", "opus": "8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "c792316ae0bbab8f8cff3c486b9e6e430ac003b6ae209f9e2f2e9698af8b2f12", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "72037fa63a6a1065a872135c9cf28d5d6abc4a8e978378709de661732356a3ee", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279", "opus": "a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef"}

## MSG-6 | 2026-08-23T23:34:33+00:00 | from: opus | type: verdict | thread: plan-v080-field-fold-2 | refs: -

## Scope of this pass

Candidate ref: `feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b`, pinned export root `.../controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/opus` (manifest `a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef`). Round-2 docket revision `4d814d192ae15a27f0225926339700404b527e2fadf64ac115daae5d30432189`.

### Commands run and results

Shell access was refused in this seat. `ls -la <export root>` succeeded once (listed `src/`, `skills/`, `tests/`, `pyproject.toml`, `PROTOCOL.md`, …); every later Bash call — `diff -u .../plan-round1.md .../docs/plans/2026-08-23-v080-field-fold.md`, `wc -l` on the two plans, and `pwd && ls src` — returned `Permission to use Bash has been denied because Claude Code is running in don't ask mode`. I therefore could **not** run the fresh `diff` the round-2 docket asks for. I substituted full reads of both artifacts (current plan, 475 lines; `plan-round1.md`, 413 lines) and compared them section by section, plus ripgrep searches against the pinned export. Stating this plainly because it is a deviation from the docket's prescribed verification; the blocking findings below do not depend on it — each rests on a direct read of the plan text against a cited source line.

Inspection commands (harness ripgrep/read tools, all read-only, all inside the pinned export or the docket revision):

- `rg -n 'jsonschema|json_schema|schema\.json|maxItems|maxLength' <export root>` → **No matches found**.
- `rg -n 'def pair_choices|def pair_menu|def suggest|symmetric' src/debate/opening.py` → hits at 149, 153, 176, 394, 437, 456, 486, 488, 496.
- `rg -n 'thread_cap|thread-cap' src/debate` → `channel.py:116,128,422,637,827`; `controller.py:1997,2038`; `__main__.py:619`; `opening.py:77`.
- `rg -n 'returncode|exit|sandbox|permission|isolation|schema|required_fields|result_schema' src/debate/bridge.py` → 18, 86, 125, 444, 533, 621, 682, 705, 714 …
- `rg -n 'profile_sha256|RESULT_SCHEMA_VERSION|required_fields' src/debate` → `controller.py:33,285,794,1018,1113`; `bridge.py:70,621,648`.
- `rg -n 'testpaths|norecursedirs|\[tool.pytest|addopts' pyproject.toml` → `51-53` (`testpaths = ["tests"]`, `addopts = ["--basetemp=.pytest-tmp"]`).
- `rg -n 'var/debate|\.debate' src` → `__main__.py:377,379,914`; `protocol_template.md:99`.
- `rg -n 'OPENER_TYPES|ENTRY_TYPES|TERMINAL_RESULTS =' src/debate/channel.py` → 64, 66, 70.
- Full reads: `src/debate/opening.py` 380-540 / 814-894 / 1020-1090, `src/debate/bridge.py` 60-140 / 415-445 / 500-715, `src/debate/controller.py` 100-290 / 336-415 / 730-840 / 1000-1060 / 1195-1320 / 1655-1780 / 1780-1905 / 1917-2046, `src/debate/channel.py` 485-495 / 600-670, `src/debate/watcher.py` 960-1030, `skills/debate-onboarding/SKILL.md` 120-190, plus all ten docket files.

## What I verified as sound

The round-1 blockers are genuinely repaired against the source, not merely asserted:

- **Five-entry ordinary cap.** `channel.thread_entries` counts every entry on the thread (`channel.py:492-493`); the request + paired reveal is 3 (`channel.py:827-829` permits it: `1 + 2 <= 5`); `drive_case` refuses to invoke at `len(entries) >= thread_cap` and closes typed `NO_PASS / thread-cap-exhausted` (`controller.py:1997-2004`, `2038-2045`); and the terminal close is exempt from the post cap because `entry_type != "close"` guards it (`channel.py:635-641`). So five entries do bound the case to two seat turns on agreement and four on persistent disagreement. `thread_cap >= 2` (`channel.py:128-129`) admits 5.
- **Prune scope is exact.** Invocation runtime really is `home/`, `build/`, `tmp/` (`controller.py:745-747`), siblings of `input.json`/`result.json`/`stdout.txt`/`stderr.txt`/`rejection.json` under `invocation_root` (`controller.py:1209-1213`, `1284-1303`), so Slice C.5's retain/delete split is exact rather than approximate. `WatcherLock` is real, non-blocking, and keyed per channel state file (`watcher.py:624-625`, `628-665`).
- **Non-zero seat processes.** `bridge._run` does ignore `completed.returncode` today (`bridge.py:694-705`), and `controller._invoke` raises before parsing any result on a non-zero adapter status (`controller.py:1308-1309`, `_parse_result` at 1312), so the Slice B.6 state machine attaches to real code. `bridge.parse_bridge_command` already exists and is already used by the controller (`controller.py:2149`), so "the profile command parses as the bundled bridge" is a mechanism that exists rather than one to be invented.
- **Supervisor correction uses existing authority.** `close` is already an opener type "for the documented one-shot close-correction idiom" (`channel.py:68-70`), and PROTOCOL.md:47 says "Corrections are new entries, never edits." Slice D.2 introduces no new rule.
- **Field claims in §2 check out.** `pair_choices` returns `[]` whenever the suggestion is `None` (`opening.py:472-473`) and `suggest_pair_with_reason` returns `None` with no wanted-class pair and no remembered pair (`opening.py:434`), so `pair_menu` is empty while admissible pairs exist (`opening.py:514-515`). `pyproject.toml:52` really does set `testpaths = ["tests"]`, which is exactly the vacuity the new Slice C fixture bullet forecloses.

## Blocking findings

**B1 — Slice B.4 assigns the evidence limits to an enforcement layer the product does not have and may not add.**
Plan §4 Slice B.4: "JSON Schema enforces shape, `maxItems`, and scalar-value `maxLength`; controller parsing enforces the UTF-8 byte limits and the aggregate." There is no JSON Schema validation anywhere in the candidate: `rg -n 'jsonschema|json_schema|schema\.json|maxItems|maxLength'` over the whole export returns **No matches found**. The bundled answer contract is prompt text (`bridge.py:120-135`) plus hand-written parsing over a closed key set (`bridge.py:86`, `parse_answer` at `613-631`) and a second hand-written pass in `controller._parse_result` (`controller.py:768-840`). `required_fields` in the immutable input (`controller.py:1018-1024`) is a descriptive list in a payload, not a validator. A schema validator cannot be introduced either: `pyproject.toml:22` is `dependencies = []` and the plan itself forbids adding one (§5, "No production dependency is added"), while the obvious dependency-free alternative — handing a schema to the vendor CLI, as this channel's own adapter does with `--json-schema`/`--output-schema` — is closed off because `seat_argv` appends only isolation and no-persistence argv (`bridge.py:435-444`) and Slice B.2 forbids "inventing extra argv" for the Codex wrapper. Round-2 docket item 4 requires that "every evidence limit has an owner, unit, enforcement layer, and boundary test"; three of the five limit classes (items, per-command scalars, per-output scalars) currently have a named owner that cannot exist, so an implementer must invent a material design decision (criteria 4, 8, 9).
*Smallest adequate correction:* say that all v2 verification limits — items, scalar values, UTF-8 bytes, and the 262,144-byte aggregate — are enforced by the bundled bridge's hand-written `parse_answer` and re-checked by `controller._parse_result`, and that any published schema document is advisory prompt material; or, if vendor-side enforcement is wanted, name `claude --json-schema` / `codex --output-schema` as argv the bridge appends and add them to the exact argv-order tests.

**B2 — Slice A.4 states a user-facing call budget the engine can exceed, and Slice B.6 widens the gap it ignores.**
Plan §4 Slice A.4: "agreement costs two calls and persistent disagreement closes `NO_PASS / thread-cap-exhausted` after at most four," and the same numbered item requires the skill to show the user a "worst-case call count." The cap bounds *entries*, not invocations. `retry_limit` defaults to 1 and is validated to `0 or 1` (`controller.py:130`, `179-180`, `234`), and the product writes `"retry_limit": 1` into brokered profiles it generates (`opening.py:860`); a retryable failure leaves the seq unanswered and the next watcher tick re-drives the case (`watcher.py:1004-1006`, `989-995`), re-invoking only the still-missing seat (`controller.py:1802-1821`, `1869-1872`). Worst case is therefore up to 8 billed calls, not 4. Slice B.6 makes this worse rather than better: it *adds* a retryable class (bundled-bridge exit 3) without reconciling it with Slice A.4's number. The Slice A test bullet only asserts "agreement makes two calls; persistent disagreement makes four," so the gap is not caught by the plan's own tests. Against criterion 2 (no pretending to enforce a budget the engine does not own) and criterion 9, this is a spend claim the product cannot keep — which is the exact class of field failure this fold exists to fix.
*Smallest adequate correction:* in Slice A.4 state that `thread_cap = 5` bounds published entries at five and seat turns at four, and that the worst-case call count shown before confirmation is `turns × (retry_limit + 1)`; add one test asserting the displayed worst case accounts for the retry.

**B3 — the new product-open admission rule dead-ends a remedy the installed skill still offers, and Slice D does not fold it.**
Plan §4 Slice B.5: "the new product open refuses to create such a profile" (a v1 hand-authored profile), reinforced by invariant 4's "use the v2 evidence contract." The path that creates those profiles is `opening._brokered_adapter`, which records a hand-authored file-protocol command verbatim (`opening.py:842-863`) — a first-class registered seat shape (`seats.py:746`, `bridge_style`). The installed skill actively steers users into it: on an isolation refusal it offers the numbered choice "1 tell me those arguments and I'll record them once **2 let me write a small command for this tool instead**" (`skills/debate-onboarding/SKILL.md:177-181`). After the fold, answer 2 produces a seat that can never open a new product debate, and the plan provides no way for an operator to declare that a custom wrapper speaks v2 (Slice B.5 only gives profiles a `result_schema_version` defaulting to 1, with v2 reserved for "new bundled product profiles"). Slice D.4 documents the brokered-open CLI break and the verification-capability upgrade but not this one, so the installed workflow contradicts the new admission rule (criteria 7 and 9).
*Smallest adequate correction:* in Slice B.5 or D.4, either remove/relabel remedy 2 in the skill for product opens and say so, or add an explicit operator declaration that a custom wrapper emits the v2 result contract — either way with a skill-contract test that the offered choices cannot lead to an unopenable seat.

## Non-blocking observations

1. **Two more default-12 sites than the plan names.** Slice A.4 says "the parser distinguishes an omitted cap from an explicit one," but the ordinary default must be sentinel-aware in three places, not one: `__main__.py:619` (`--cap`, `default=12`), `BrokeredOpenSpec.thread_cap = 12` (`opening.py:77`), and `channel.Config.thread_cap = 12` / `load_config`'s `int(raw.get("thread_cap", 12))` (`channel.py:116`, `422`). Naming them would remove any chance of an ordinary open silently landing at 12.
2. **Cap 5 leaves only two entries of supervisor slack before the reveal hard-fails.** `commit_reveal_pair` refuses when `count + 2 > thread_cap` (`channel.py:827-829`). At cap 5, three supervisor interjections before the sealed reveal turn the case into a raised `ChannelError` rather than a graceful close. The behaviour exists today at cap 12 with ten interjections; at 5 the margin is thin enough to deserve one named test.
3. **Keep `sanitized_manifest` byte-stable for legacy profiles.** It already emits `"result_schema_version": RESULT_SCHEMA_VERSION` from the module constant (`controller.py:285`). Slice B.5's per-profile field defaulting to 1 preserves existing hashes only if no other key is added to that dict for old profiles; otherwise every in-flight case refuses at the `profile_sha256` guard (`controller.py:1113-1116`) the moment a user upgrades mid-case. The Slice B test bullet's "without changing old entries" covers the intent — say explicitly that it covers the manifest bytes too.
4. **Claude help evidence is not checkable from the export.** §2's "A fresh local `claude --help` run on 2026-08-23 (Claude Code 2.1.241) documents `--permission-mode`, `--tools`, and `--allowedTools`" is a host fact outside the pinned source, and shell access was denied here, so I neither confirm nor dispute it. Slice B.2's gate ("only after the implementation records the exact installed-help evidence") is the right shape and keeps the catalogue honest.
5. **The compatibility boundary is exercised by this channel itself.** `watcher.json:10-16` runs a hand-authored `seat_adapter.py` against a v1 `seat-result.schema.json` (`required: schema_version, entry_type, decision, body, runtime_model`, `const: 1`), and its `runtime_root` sits below `<repo>/var/debate` as `BrokerConfig.__post_init__` demands (`controller.py:354-358`). Slice C.1 must widen that check to accept `.debate/runtime/<channel>` — `controller.py` is in the file map (§5), so this is covered, but it is the single load-bearing edit for invariant 8 and worth calling out in the file map line itself.
6. **Delta paths.** The hard-coded `var/debate` strings Slice C.2 targets are in `__main__.py:377,379,914`, not `delta.py`; both files are already in the file map, so nothing is missing — only the section text points at the wrong module.

## Decision

`NO_PASS`. Criteria 1, 3, 5, and 6 hold on my own evidence. Criterion 4 fails on B1, criterion 2 on B2, criterion 7 on B3, and criterion 9 on all three. Criterion 8 fails only through B1 (an implementer would have to invent the missing enforcement layer). The plan is close: the round-1 fold is real and verified against source, and every blocker above has a one-to-three-sentence correction that does not enlarge the selected fold.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: c920d637733edc881183be7e9d3e828bc0fa1d59a9dc06fcca4f0f90c4228a02
- phase: sealed
- captured-at: 2026-08-23T23:34:33+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d
- controller-config-sha256: 6909647061e64650eb0a2bb29511292734d3da072ea3826e12eb2504536ed4e1
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef
- docket-revision-sha256: 4d814d192ae15a27f0225926339700404b527e2fadf64ac115daae5d30432189
- input-sha256: e047b2c96d061033ac585e355cebab4b3baea2282563af2390947ea07256b3f2
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-7 | 2026-08-23T23:34:33+00:00 | from: codex | type: verdict | thread: plan-v080-field-fold-2 | refs: -

Candidate reviewed: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b. Immutable round-2 docket revision: 4d814d192ae15a27f0225926339700404b527e2fadf64ac115daae5d30432189.

Blocking finding — Slice A’s promised worst-case call bound is false once its retained retry policy is included. Plan §4 Slice A, lines 168–176, requires the skill to show the worst-case call count but says agreement is two calls and persistent disagreement is at most four. Slice B lines 250–275 expressly retains one retry for a bundled bridge status 3. The fresh command `nl -ba <docket>/docs/plans/2026-08-23-v080-field-fold.md | sed -n '158,207p;250,286p'` printed those statements. A five-entry thread caps published positions (request + two sealed verdicts + two deliberations), not seat-process launches: each of the two sealed and two permitted deliberation positions can use its one retry, so the real maximum is eight nested-seat launches. This conflicts with the current lifecycle’s retry accounting: `nl -ba <source>/src/debate/controller.py | sed -n '294,323p;1254,1311p;1992,2046p'` printed `retry_limit + 1` at lines 315–321 and the post-entry cap check at lines 2038–2045; `nl -ba <source>/src/debate/watcher.py | sed -n '975,1010p'` printed retry dispatch at lines 975–1005. Smallest correction: either disable retries for ordinary mode, or redefine the 2–4 number as published vote-producing positions and record/test the true worst-case nested-seat launch/spend bound (eight) in the confirmation and product-flow tests.

Observations — The fresh `diff -u <docket>/var/debate/plan-v080-field-fold-14206/plan-round1.md <docket>/docs/plans/2026-08-23-v080-field-fold.md; test $? -eq 1` confirmed the stated fold edits in the artifact. The v1/v2 compatibility boundary, concrete evidence limits, bundled-bridge-only status-3 rule, and lock-held pruning receipt protocol are now specified and tested at plan level. `sha256sum` over the pinned docket files matched the supplied hashes. This remaining bound/spend contradiction prevents PASS under round-2 criterion 2 and the explicit five-entry verification requirement.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: c920d637733edc881183be7e9d3e828bc0fa1d59a9dc06fcca4f0f90c4228a02
- phase: sealed
- captured-at: 2026-08-23T23:34:33+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347
- controller-config-sha256: 6909647061e64650eb0a2bb29511292734d3da072ea3826e12eb2504536ed4e1
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279
- docket-revision-sha256: 4d814d192ae15a27f0225926339700404b527e2fadf64ac115daae5d30432189
- input-sha256: bf718aa2158826cf6615a23ffdc6abe6eead4aee1cc8027fb4c1b97df7585620
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.0
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-8 | 2026-08-23T23:34:33+00:00 | from: owner | type: close | thread: plan-v080-field-fold-2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-9 | 2026-08-23T23:38:45+00:00 | from: owner | type: review-request | thread: plan-v080-field-fold-3 | refs: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b

Re-review the twice-amended v0.8.0 field-fold plan. Verify the complete round-2
fold in `var/debate/plan-v080-field-fold-14206/fold-list-r2.md` against the
immutable `var/debate/plan-v080-field-fold-14206/plan-round2.md`, the current plan,
the full original docket, and the pinned candidate source. Follow every requirement
in `var/debate/plan-v080-field-fold-14206/plan-docket-r3.md`.

Use your own fresh diff and source inspection. Return PASS only if all nine original
criteria now hold and neither fold introduced a new blocker. Do not edit any supplied
file or channel record.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- docket-revision-sha256: 8ecee4a12569a44d531f70fe3c2998e3472df0f329483a008e47382c7ad9f6f3
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-field-fold-14206.debate.json", "sha256": "dec1473ac06994a2b9d94d4353a904fb71746d57aa0b214fcedf94ed14a6f598", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-v080-field-fold.md", "sha256": "d9b05e4096bb23a1f1f3f026022a6d88b9a2a4e2f14031e74b1a878ad70dd05a", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket.md", "sha256": "a365693744972cb63fa7f9fb3d5e652e414d6aa07e9c57bf69a2c1b2425e7e8b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat_adapter.py", "sha256": "5e3f30bd1d0e3dd0b2ff605bc3b4412970912744c8456f944af6128ad46e71a6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/watcher.json", "sha256": "a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round1.md", "sha256": "e6896a7f4367a6080b2c8862206bec898bd9dc79636fd8faf5d9d0de7466fbf1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r1.md", "sha256": "a20f21a0d9315830212270bc34e5c187ced353b13702a6d5d923ab69955970c8", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r2.md", "sha256": "9b7b5085d7c2a65bbe11f5fb40d908eddcaa3a18185dad8a89b17b72f7cfdf88", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round2.md", "sha256": "754e6ada306c1c484d21ad6acc8fd4ea452da79593539ed450857e645eabf1e2", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r2.md", "sha256": "f7bb8dc7a103e0c4a0f16f945dcbdbfb2343c421cd78b60936075a34c0990706", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r3.md", "sha256": "a9bb754f6d04026da50d78924173d43ef94ceb5ab526102a8f60735452d1f075", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347", "opus": "8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "c792316ae0bbab8f8cff3c486b9e6e430ac003b6ae209f9e2f2e9698af8b2f12", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "72037fa63a6a1065a872135c9cf28d5d6abc4a8e978378709de661732356a3ee", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279", "opus": "a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef"}

## MSG-10 | 2026-08-23T23:41:49+00:00 | from: owner | type: close | thread: plan-v080-field-fold-3 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-11 | 2026-08-23T23:42:42+00:00 | from: owner | type: review-request | thread: plan-v080-field-fold-3-retry1 | refs: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b

Re-review the twice-amended v0.8.0 field-fold plan. Verify the complete round-2
fold in `var/debate/plan-v080-field-fold-14206/fold-list-r2.md` against the
immutable `var/debate/plan-v080-field-fold-14206/plan-round2.md`, the current plan,
the full original docket, and the pinned candidate source. Follow every requirement
in `var/debate/plan-v080-field-fold-14206/plan-docket-r3.md`.

Use your own fresh diff and source inspection. Return PASS only if all nine original
criteria now hold and neither fold introduced a new blocker. Do not edit any supplied
file or channel record.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- docket-revision-sha256: 8ecee4a12569a44d531f70fe3c2998e3472df0f329483a008e47382c7ad9f6f3
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-field-fold-14206.debate.json", "sha256": "dec1473ac06994a2b9d94d4353a904fb71746d57aa0b214fcedf94ed14a6f598", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-v080-field-fold.md", "sha256": "d9b05e4096bb23a1f1f3f026022a6d88b9a2a4e2f14031e74b1a878ad70dd05a", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket.md", "sha256": "a365693744972cb63fa7f9fb3d5e652e414d6aa07e9c57bf69a2c1b2425e7e8b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat_adapter.py", "sha256": "5e3f30bd1d0e3dd0b2ff605bc3b4412970912744c8456f944af6128ad46e71a6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/watcher.json", "sha256": "a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round1.md", "sha256": "e6896a7f4367a6080b2c8862206bec898bd9dc79636fd8faf5d9d0de7466fbf1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r1.md", "sha256": "a20f21a0d9315830212270bc34e5c187ced353b13702a6d5d923ab69955970c8", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r2.md", "sha256": "9b7b5085d7c2a65bbe11f5fb40d908eddcaa3a18185dad8a89b17b72f7cfdf88", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round2.md", "sha256": "754e6ada306c1c484d21ad6acc8fd4ea452da79593539ed450857e645eabf1e2", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r2.md", "sha256": "f7bb8dc7a103e0c4a0f16f945dcbdbfb2343c421cd78b60936075a34c0990706", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r3.md", "sha256": "a9bb754f6d04026da50d78924173d43ef94ceb5ab526102a8f60735452d1f075", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347", "opus": "8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "c792316ae0bbab8f8cff3c486b9e6e430ac003b6ae209f9e2f2e9698af8b2f12", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "72037fa63a6a1065a872135c9cf28d5d6abc4a8e978378709de661732356a3ee", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279", "opus": "a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef"}

## MSG-12 | 2026-08-23T23:45:51+00:00 | from: owner | type: close | thread: plan-v080-field-fold-3-retry1 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-13 | 2026-08-23T23:46:15+00:00 | from: owner | type: review-request | thread: plan-v080-field-fold-3-retry2 | refs: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b

Re-review the twice-amended v0.8.0 field-fold plan. Verify the complete round-2
fold in `var/debate/plan-v080-field-fold-14206/fold-list-r2.md` against the
immutable `var/debate/plan-v080-field-fold-14206/plan-round2.md`, the current plan,
the full original docket, and the pinned candidate source. Follow every requirement
in `var/debate/plan-v080-field-fold-14206/plan-docket-r3.md`.

Use your own fresh diff and source inspection. Return PASS only if all nine original
criteria now hold and neither fold introduced a new blocker. Do not edit any supplied
file or channel record.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- docket-revision-sha256: 8ecee4a12569a44d531f70fe3c2998e3472df0f329483a008e47382c7ad9f6f3
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-field-fold-14206.debate.json", "sha256": "dec1473ac06994a2b9d94d4353a904fb71746d57aa0b214fcedf94ed14a6f598", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-v080-field-fold.md", "sha256": "d9b05e4096bb23a1f1f3f026022a6d88b9a2a4e2f14031e74b1a878ad70dd05a", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket.md", "sha256": "a365693744972cb63fa7f9fb3d5e652e414d6aa07e9c57bf69a2c1b2425e7e8b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat_adapter.py", "sha256": "5e3f30bd1d0e3dd0b2ff605bc3b4412970912744c8456f944af6128ad46e71a6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/watcher.json", "sha256": "a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round1.md", "sha256": "e6896a7f4367a6080b2c8862206bec898bd9dc79636fd8faf5d9d0de7466fbf1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r1.md", "sha256": "a20f21a0d9315830212270bc34e5c187ced353b13702a6d5d923ab69955970c8", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r2.md", "sha256": "9b7b5085d7c2a65bbe11f5fb40d908eddcaa3a18185dad8a89b17b72f7cfdf88", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round2.md", "sha256": "754e6ada306c1c484d21ad6acc8fd4ea452da79593539ed450857e645eabf1e2", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r2.md", "sha256": "f7bb8dc7a103e0c4a0f16f945dcbdbfb2343c421cd78b60936075a34c0990706", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r3.md", "sha256": "a9bb754f6d04026da50d78924173d43ef94ceb5ab526102a8f60735452d1f075", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347", "opus": "8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "c792316ae0bbab8f8cff3c486b9e6e430ac003b6ae209f9e2f2e9698af8b2f12", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "72037fa63a6a1065a872135c9cf28d5d6abc4a8e978378709de661732356a3ee", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279", "opus": "a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef"}

## MSG-14 | 2026-08-23T23:56:21+00:00 | from: opus | type: verdict | thread: plan-v080-field-fold-3-retry2 | refs: -

## Scope of this pass

Candidate ref: `feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b`
(pinned export root `/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/opus`, manifest `a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef`).
Round-3 docket revision `8ecee4a12569a44d531f70fe3c2998e3472df0f329483a008e47382c7ad9f6f3`.

Method note: shell invocations whose arguments named the docket root were refused by this
seat's permission mode (`Permission to use Bash has been denied ... running in don't ask mode`),
so no shell `diff` of round 2 against the current plan was possible. I instead read
`plan-round2.md` (475 lines) and `docs/plans/2026-08-23-v080-field-fold.md` (512 lines) in
full with the read-only file reader and compared them passage by passage; all shell commands
below were run inside the pinned read-only export.

### Round-2 → current changes I located, and independent source verification

Changed passages: header lines 7–14; Slice A.4 and the Slice A test list; Slice B.4 (schema
enforcement ownership); Slice B.5 (`result_schema_version` on registry seats + profiles,
`--result-schema-version 2`, manifest-byte preservation) and two Slice B test bullets;
Slice C.1 (one added sentence on `BrokerConfig`); Slice D.4 and the first Slice D test bullet.
Nothing else differs. Verified against source, not against `fold-list-r2.md`:

- `rg -n "thread_cap|retry_limit" src/debate` → `channel.py:637` refuses a non-`close` entry at
  `count >= thread_cap`; `channel.py:827` refuses a paired reveal at `count + 2 > thread_cap`;
  `controller.py:1997/2038` close typed `NO_PASS / thread-cap-exhausted`. Cap 5 therefore yields
  request + 2 sealed + 2 deliberation = 4 vote-producing turns; cap 12 yields 11. `controller.py:130`
  (`retry_limit: int = 1`), `:179` (must be 0 or 1) and `opening.py:860,911` (`"retry_limit": 1`)
  confirm 4×2 = 8 and 11×2 = 22. `controller.py:1766–1774` closes on agreement straight after the
  reveal, so "clean agreement launches two processes" is exact; `_capture_sealed_positions`
  (`controller.py:1785+`) recaptures only missing seats, so retries stay inside the ceiling.
  Cap sites: `__main__.py:619` (`--cap ... default=12`), `opening.py:46,77`, `channel.py:116,336,422`.
- Pre-reveal spend: `controller.py:1971–1992` invokes the sealed pair with no room check, and the
  refusal lands at `channel.py:827` after both processes have run. The fold's pre-invocation
  two-slot check is the right shape (`count + 2 <= cap`).
- `rg -n "dependencies|jsonschema" pyproject.toml` → `dependencies = []`; `bridge.py:613 parse_answer`
  and `controller.py:770–830 _parse_result` are two independent handwritten validators, and
  `controller.py:782` is the separate 1 MiB ceiling. The advisory-schema wording holds.
- `rg -n "result_schema_version" src/debate/controller.py` → `:285` already emits
  `"result_schema_version": RESULT_SCHEMA_VERSION` inside `sanitized_manifest()` with
  `RESULT_SCHEMA_VERSION = 1` (`controller.py:33`), so a per-profile field defaulting to 1
  genuinely leaves legacy `profile_sha256` bytes unchanged.
- `opening.py:280–281` admits any `{input_path}`/`{result_path}` seat unconditionally, and
  `skills/debate-onboarding/SKILL.md:103–106,180` offers "let me write a small command for this
  tool instead" — the dead-end the Slice D.4 fold closes. `bridge.py:243 SUBCOMMAND = "run-seat"`
  and `opening.py:925 bridge.parse_bridge_command(...)` make the status-3 retry gate executable.
- `controller.py:351–364` is the `BrokerConfig` root check the fold says it widens (it pins
  `repo/var/debate` and rejects tool-cache nesting); `watcher.py:628–668` is a non-blocking,
  channel-stamped `WatcherLock`; `pyproject.toml:52` is `testpaths = ["tests"]`;
  `opening.py:472–473` is the empty-menu defect. All plan claims match.

## Blocking finding (1)

**B1 — the `.debate/` runtime move is not carried into the source-export separation rule.**

Plan section: §4 Slice C item 1 (current plan lines 320–325) and the §8 checklist line
"New runtime/config live under `.debate/`". Slice C enumerates every other path site it touches —
`BrokerConfig` admission, delta paths, the ignore hint, root pytest collection, prune — and
`grep` of the plan for `exclusion|_is_separated|separated|source export` returns only lines 87 and
342, neither of which is about export separation.

Source contract it conflicts with, from
`pwd; rg -n "_is_separated|exclusion_policy" src/debate/controller.py; rg -n "expected_root = " src/debate/controller.py; rg -n "^var/" .gitignore`:

```
/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/opus
509:def _is_separated(path: PurePosixPath) -> bool:
597:                if _is_separated(relative):
610:        "exclusion_policy": ["collab/", "var/", ".git/"],
354:        expected_root = (repo / "var" / "debate").resolve()
51:var/
```

`controller.py:509-510` is `return path.parts[0] in ("collab", "var", ".git")`, applied at
`:597` while unpacking `git archive` into each party's read-only export. It is the engine-side
guarantee behind the invariant this repo states in `.gitignore:49-51` — "Managed Debate
controller/runtime state and source exports are operational, project-local, and **never part of
a source or review export**" — and it is a second layer that holds even when a project's
`.gitignore` does not. After the fold, product runtime lives at `<project>/.debate/runtime/<channel>/`,
which `_is_separated` does not cover, and Slice C.3 deliberately declines to write `.gitignore`
("Debate does not edit `.gitignore` automatically"), leaving only a printed suggestion. A user who
commits `.debate/` — the population this release targets — then has every subsequent brokered open
copy prior cases' `input.json`, `result.json`, seat stdout/stderr and 140 MiB-class invocation homes
into two per-party exports (`create_source_export`, `_tree_files`, `_make_read_only` all walk it),
and hands prior verdicts to both seats as pinned review material, which PROTOCOL.md §2 defines as
the source of repo claims. That is a product-path regression of a safety property the candidate
enforces today for `var/`, and it contradicts plan invariant 8 and the §2 rationale about cache size.

Smallest adequate correction: one sentence in Slice C item 1 requiring `.debate` to join
`("collab", "var", ".git")` in `_is_separated` (`controller.py:509-510`) and the recorded
`exclusion_policy` (`controller.py:604-610`), plus one Slice C golden test that a committed
`.debate/` tree is excluded from the per-party export and named in `excluded`.

## Non-blocking observations

1. **Deliberation-phase spend race remains.** `controller.py:1995-2018` checks room before a
   deliberation launch, but `channel.py:635-641` can still refuse after the seat has run if a
   supervisor interjects between check and post. The fold fixes only the sealed pre-reveal case;
   cap 5 makes the deliberation window likelier. Worth one sentence, not a blocker.
2. **Ordinary cap 5 has zero supervisor headroom in the clean path.** Slice A.4 requires the skill
   to display the retry-inclusive launch ceiling but not that supervisor context entries consume the
   same five slots and can force `NO_PASS / thread-cap-exhausted` before either seat runs. The typed
   `NO_PASS` itself is protocol-consistent (docket `collab/PROTOCOL.md:29-30`).
3. **Who computes the ceiling.** Slice A.4 assigns the launch-ceiling computation to the controller,
   but the single pre-open confirmation is rendered by the skill before any controller run. Naming
   the surface (skill-side derivation vs `TimingPolicy.report()`, `controller.py:327`) would remove
   the ambiguity.
4. **`retry_limit` is per-party.** `controller.py:130,234` gives each profile its own limit, so
   "seat turns times `(retry_limit + 1)`" should say the maximum across the two profiles.
5. **Declared-v2 wrapper needs the shape, not just the flag.** Slice D.4 requires the skill to show
   the `--result-schema-version 2` declaration in the same approval, but not to show the v2
   `verification` contract the wrapper must emit; without it the seat is openable yet fails closed at
   `controller.py:794` on first use.

## Criteria status

Criteria 1, 2, 3, 4, 5, 7, 8 hold on the evidence above; criterion 9 holds for every passage I
re-derived. Criterion 6 fails on B1 alone. Decision: `NO_PASS`.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 9802a6cd4d7015bf83a4c532bd125ce2a579fb92950d986971fd426e20bd0b6c
- phase: sealed
- captured-at: 2026-08-23T23:56:21+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d
- controller-config-sha256: a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef
- docket-revision-sha256: 8ecee4a12569a44d531f70fe3c2998e3472df0f329483a008e47382c7ad9f6f3
- input-sha256: 1d3e11efc76467d877a831b0b64c470877a048a66d0a65588543d7fb27b52c5f
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-15 | 2026-08-23T23:56:21+00:00 | from: codex | type: verdict | thread: plan-v080-field-fold-3-retry2 | refs: -

Candidate: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b. Immutable round-3 docket revision: a9bb754f6d04026da50d78924173d43ef94ceb5ab526102a8f60735452d1f075 (fresh sha256sum matched).

Blocker:
- Plan §4 Slice A, lines 187-189 promises that a two-entry pre-reveal room check prevents spend before a cap failure. This is not race-safe against the stated supervisor interjection: the pinned watcher explicitly releases the channel writer lock before child launch (src/debate/watcher.py:790-795), then controller.py:1971-1982 invokes the sealed pair. The existing cap check is only at paired reveal after both invocations (src/debate/channel.py:826-830). An interjection can therefore consume a slot after the proposed check but before/while the pair runs, producing the same post-spend cap failure. Smallest adequate correction: specify an atomic slot-reservation/interlock that remains effective through reveal (without blocking required result handling), and add a concurrent interjection-race test proving neither seat launches when reservation cannot be obtained.

Fresh read-only command and result: `cd /home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/codex && nl -ba src/debate/watcher.py | sed -n '785,797p' && nl -ba src/debate/controller.py | sed -n '1958,1992p' && nl -ba src/debate/channel.py | sed -n '818,833p'`; it showed the lock is released before child launch, sealed invocation follows, and `count + 2` is checked only during reveal. I also ran `diff -u .../plan-round2.md .../docs/plans/2026-08-23-v080-field-fold.md`; it confirmed the pre-reveal claim is a round-3 amendment.

Observations: the pinned source sets both brokered profiles to `retry_limit: 1` (src/debate/opening.py:860,911), supporting the stated 8/22 process-launch ceilings; the plan's dependency-free v2 validation, v1 manifest preservation, declared-v2 wrapper admission, and explicit BrokerConfig runtime-root widening are otherwise coherent.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 9802a6cd4d7015bf83a4c532bd125ce2a579fb92950d986971fd426e20bd0b6c
- phase: sealed
- captured-at: 2026-08-23T23:56:21+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347
- controller-config-sha256: a651233538f0106924178d01a33713ff912f034d630fa493cdb5a75d6eddf234
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279
- docket-revision-sha256: 8ecee4a12569a44d531f70fe3c2998e3472df0f329483a008e47382c7ad9f6f3
- input-sha256: 875e2a6deec6d4d4eed987a62e0fa5ca030f7d0a76433683cdf3e5368438e583
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.0
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-16 | 2026-08-23T23:56:21+00:00 | from: owner | type: close | thread: plan-v080-field-fold-3-retry2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-17 | 2026-08-23T23:58:40+00:00 | from: owner | type: review-request | thread: plan-v080-field-fold-4 | refs: feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b

Re-review the thrice-amended v0.8.0 field-fold plan. Verify the complete round-3
fold in `var/debate/plan-v080-field-fold-14206/fold-list-r3.md` against the
immutable `var/debate/plan-v080-field-fold-14206/plan-round3.md`, the current plan,
the original docket, and the pinned candidate source. Follow every requirement in
`var/debate/plan-v080-field-fold-14206/plan-docket-r4.md`.

Use your own fresh diff and source inspection. Return PASS only if all nine original
criteria now hold and none of the three folds introduced a new blocker. Do not edit
any supplied file or channel record.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: cd179eb914997b99a0a05bbc2db0e255ec91bba4d90277038f80c5b1e2302207
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- docket-revision-sha256: 4f4bd27adc26cdef039f29d52aadfd5c876d17c2dc6ba4bd436534cdecf4da53
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/plan-v080-field-fold-14206.debate.json", "sha256": "dec1473ac06994a2b9d94d4353a904fb71746d57aa0b214fcedf94ed14a6f598", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-v080-field-fold.md", "sha256": "5d0c799f21eac9b92ac166c2add694103276bcac101c04d114d949e123145182", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket.md", "sha256": "a365693744972cb63fa7f9fb3d5e652e414d6aa07e9c57bf69a2c1b2425e7e8b", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/seat_adapter.py", "sha256": "5e3f30bd1d0e3dd0b2ff605bc3b4412970912744c8456f944af6128ad46e71a6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/watcher.json", "sha256": "cd179eb914997b99a0a05bbc2db0e255ec91bba4d90277038f80c5b1e2302207", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round1.md", "sha256": "e6896a7f4367a6080b2c8862206bec898bd9dc79636fd8faf5d9d0de7466fbf1", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r1.md", "sha256": "a20f21a0d9315830212270bc34e5c187ced353b13702a6d5d923ab69955970c8", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r2.md", "sha256": "9b7b5085d7c2a65bbe11f5fb40d908eddcaa3a18185dad8a89b17b72f7cfdf88", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round2.md", "sha256": "754e6ada306c1c484d21ad6acc8fd4ea452da79593539ed450857e645eabf1e2", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r2.md", "sha256": "f7bb8dc7a103e0c4a0f16f945dcbdbfb2343c421cd78b60936075a34c0990706", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r3.md", "sha256": "a9bb754f6d04026da50d78924173d43ef94ceb5ab526102a8f60735452d1f075", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-round3.md", "sha256": "d9b05e4096bb23a1f1f3f026022a6d88b9a2a4e2f14031e74b1a878ad70dd05a", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/fold-list-r3.md", "sha256": "9307d70ef4379c79ce69e56667fec68e2462122025b6196cf6462bf1c70167c6", "tracked_at_source_ref": false}, {"path": "var/debate/plan-v080-field-fold-14206/plan-docket-r4.md", "sha256": "485c92629dcd0cb95f8d72db7149f622a32b42313a5c067cd429381d8294dfa7", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347", "opus": "8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "c792316ae0bbab8f8cff3c486b9e6e430ac003b6ae209f9e2f2e9698af8b2f12", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "72037fa63a6a1065a872135c9cf28d5d6abc4a8e978378709de661732356a3ee", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279", "opus": "a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef"}

## MSG-18 | 2026-08-24T00:05:41+00:00 | from: opus | type: verdict | thread: plan-v080-field-fold-4 | refs: -

## Verdict: PASS

Candidate ref: `feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b`; round-4 docket revision `4f4bd27adc26cdef039f29d52aadfd5c876d17c2dc6ba4bd436534cdecf4da53`; source export manifest `a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef`.

### Commands run (read-only, from the pinned export)

- `pwd` → `/home/zoltan/Projects/debate/var/debate/plan-v080-field-fold-14206/controller/exports/e5c90f6f1ee6e87c76817e0890e6071d9312782b/opus`
- `rg -n "_is_separated|exclusion_policy" src/debate/*.py` → `controller.py:509 def _is_separated`, `510: return path.parts[0] in ("collab", "var", ".git")`, `610: "exclusion_policy": ["collab/", "var/", ".git/"]`
- `rg -n "thread_cap|retry_limit" src/debate/*.py` → `channel.py:116 thread_cap: int = 12`, `channel.py:637 if count >= config.thread_cap`, `channel.py:827 if count + 2 > config.thread_cap`, `controller.py:179-180 retry_limit ... must be 0 or 1`, `controller.py:1997/2038 thread-cap-exhausted`, `__main__.py:619 --cap ... default=12`, `seats.py:932 thread_cap=12`
- `rg -n "class WatcherLock|release|acquire" src/debate/watcher.py` → `628 class WatcherLock`, `642 def acquire`, `654 fcntl.flock(..., LOCK_EX | LOCK_NB)`, `711-718 run_once` holds it around `_run_once_locked`
- `rg -n "RESULT_SCHEMA_VERSION|result_schema_version" src/debate/` → `bridge.py:70 = 1`, `controller.py:33 = 1`, `controller.py:285 "result_schema_version": RESULT_SCHEMA_VERSION` inside `sanitized_manifest`
- `rg -n "1 << 20|1048576|MiB|MAX_RESULT|max_bytes" src/debate/controller.py src/debate/bridge.py` → `controller.py:782-783` 1 MiB whole-result limit; `bridge.py:517` 1 MiB output cap
- `rg -n "testpaths|norecursedirs" pyproject.toml` → `52:testpaths = ["tests"]`; `rg -n "dependencies" pyproject.toml` → `22: dependencies = []`
- `rg -n "var/debate|delta-docket" src/debate/delta.py` → no match (`rg -c "" src/debate/delta.py` → 120); `rg -n "var/debate" src/debate/*.py` → `__main__.py:377,379,914`
- `rg -n "def pair_choices|def pair_menu|def suggest" src/debate/opening.py`, then `Read opening.py:394-522`, `bridge.py:420-444/500-537/605-715`, `controller.py:260-380/495-622/770-830/1230-1318/1975-2046`, `channel.py:610-669/805-830`, `seat_catalog.py:84-117`

### Docket round-4 criteria, established on that output

1. **Committed `.debate/` excluded from both party exports and recorded.** `create_source_export` (controller.py:590-611) filters every `git archive` member through `_is_separated` and records `excluded` plus a literal `exclusion_policy` list. `git archive` carries tracked files, so a committed `.debate/` tree is exactly what today leaks; Slice C.1 adds `.debate/` to both the predicate and the policy, and the Slice C test requires absence from both party exports plus presence under `excluded`, with `collab/`/`var/`/`.git/` separation byte-stable. Matches source; smallest possible change.
2. **Preflight is not a reservation; no writer lock across model execution.** `_run_once_locked` takes `channel.exclusive(...)` only for snapshot/decide/record and states at watcher.py:790-795 that "the child launch happens AFTER release". Slice A.4 now says exactly that ("deliberately not a reservation: the watcher releases the channel writer lock during model execution"). The impossible reservation claim of round 3 (plan-round3.md:187-190) is gone.
3. **Insufficient room spends nothing; a post-preflight race is fail-closed.** Source shows both race sites: `channel.post` refuses at cap (channel.py:637) and `reveal_pair` refuses at `count + 2 > thread_cap` (channel.py:827) — i.e. after spend. The fold's rule (retain controller-owned results/diagnostics, publish no verdict, spend no retry, append an exempt typed `NO_PASS / thread-cap-race`, count the launch inside the advertised ceiling) is implementable as written: `close` entries are cap-exempt (channel.py:635 `entry_type != "close"`) and `close_reason` is free-form single-line (channel.py:884), so no protocol rule is widened. The Slice A tests cover both the already-insufficient and the raced sealed/deliberation cases.
4. **One shared budget helper, unequal retries, supervisor consumption.** Arithmetic checks out against the engine: cap 5 → 1 request + 2 sealed + 2 deliberation = 4 vote-producing turns (controller.py:1997 pre-check, 2038 post-check), ceiling 4 × (max retry_limit 1 + 1) = 8; cap 12 → 11 turns and 22 launches; `retry_limit` is constrained to 0 or 1 (controller.py:179), so the maximum is conservative by construction. The cap check applies to supervisor posts too (channel.py:635 has no sender exemption), which is why the confirmation must say so — the plan now does. Menu-time retry values exist (opening.py:860/911 write `retry_limit: 1`), so one pure helper can serve both the read-only menu and open validation.
5. **v2 wrapper remedy explains the shape it must emit.** Slice D.4 now requires the approval to show "both the mandatory v2 `verification` result shape and the v2/verification declarations", and the Slice D test requires every offered remedy to explain the mandatory result shape. That closes the "openable but predictably invalid wrapper" gap.

### Round-1/round-2 repairs reconfirmed after the fold

- Legacy-adapter compatibility is now literally true of the source: `sanitized_manifest` already emits `result_schema_version` (controller.py:285), so an old profile keeps value 1 and its `profile_sha256` (controller.py:289) is byte-stable while new bundled profiles emit 2 — the in-flight guard at controller.py:1113 cannot trip.
- Dependency-free enforcement is consistent with `dependencies = []` (pyproject.toml:22); the handwritten validators exist on both sides (`bridge.parse_answer` at bridge.py:613 with a closed `ANSWER_KEYS` set at bridge.py:86; `controller._parse_result` at controller.py:770-830), and the separate 1 MiB outer ceiling is real (controller.py:782).
- Non-zero policy: `bridge._run` (bridge.py:680-705) ignores `completed.returncode` and returns 0 after writing a verdict — the plan's §2 evidence is accurate, and the status-3/sidecar split sits cleanly beside the existing exit-2 refusal path (bridge.py:708-714) and the controller's non-zero refusal (controller.py:1308-1309).
- Prune safety: `WatcherLock` is exact-channel and non-blocking (`LOCK_NB`, watcher.py:654) and records the served channel root, so Slice C.4's "acquire non-blockingly, revalidate under the lock, hold through receipt" needs no second lock protocol.
- Path/footprint: the `BrokerConfig` runtime-root admission check is real and root-anchored (controller.py:351-364), so Slice C.1's "widens, does not bypass" is accurate; `testpaths = ["tests"]` exists, which is exactly why the Slice C fixture must forbid it.
- Menu bug and mode split: `pair_choices` returns `[]` whenever `suggestion is None` (opening.py:472-473) and `pair_menu` returns `[]` with it (opening.py:514-515) — the field failure reproduces from source. The stances are discrete constants (`ADVERSARIAL_STANCE`/`ANALYTICAL_STANCE`, bridge.py:94-108), so "goldens differ only in the contract block and the mode-selected stance" is achievable, and configs without the field loading as `release-gate` matches `channel.py:422` defaulting behavior (no silent lowering).
- Scope, honesty and boundary language hold: `isolation_mode` is `advisory` in source (controller.py:42/132), findings 4/5/10 and the adaptive half of 14 stay deferred (§6), and §7.7 keeps push/merge/publish with the owner.

### Blocking findings

None.

### Non-blocking observations

1. **Claude argv combination is documented, not yet proven.** The catalogued isolation argv already contains `--safe-mode` (seat_catalog.py:96-99) and `seat_argv` appends flags positionally (bridge.py:444). Whether `--safe-mode` coexists with `--permission-mode dontAsk` / `--tools Read,Grep,Glob,Bash` is not established by help text alone. §7.4's project-local probe is the right check, but §8 permits it to "explicitly remain unrun" — if the owner declines that spend, the central Slice B outcome ships catalogued-but-unexercised. Suggested (non-blocking) tightening: make the two fold-specific real-seat checks a release precondition rather than a recordable non-result.
2. **"Five-entry bound" wording.** The typed close is appended beyond the cap by design (channel.py:635). The plan calls it "the exempt typed ... close" elsewhere, so the intent is clear, but §Slice A.4's "never the four seat-turn/five-entry bound" reads as if no sixth entry can exist.
3. **Duplicate ceiling arithmetic.** `TimingPolicy.unconstrained_seconds` (controller.py:313-321) already computes `thread_cap × max-over-profiles(timeout × (retry_limit + 1) …)`. The new launch-ceiling helper repeats that shape; saying which one owns the retry-inclusive arithmetic would prevent the two drifting apart.
4. **File map breadth.** The hard-coded delta paths are in `__main__.py:377/379/914` only; `src/debate/delta.py` carries no `var/debate` literal (120 lines, no match). Both files are listed, so nothing is missing — `delta.py` may simply not need to change.

The complete plan is safe, proportionate, internally consistent with the pinned source and the supplied protocol, and executable without inventing material design decisions.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: d1674949dd8f1f51b7309565a38525d139a517ac05d47ace8fa92c3933406bb8
- phase: sealed
- captured-at: 2026-08-24T00:05:41+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 8b8b2519c5f9e22d6c271c3b613ad30e33ab60f94fb780c87123990c297f142d
- controller-config-sha256: cd179eb914997b99a0a05bbc2db0e255ec91bba4d90277038f80c5b1e2302207
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a774a214f0a2ddb5c429f74b621775004a2b9169fc4fb1a924a6b23d783a96ef
- docket-revision-sha256: 4f4bd27adc26cdef039f29d52aadfd5c876d17c2dc6ba4bd436534cdecf4da53
- input-sha256: 97ac0e61b9ecac33f2f84602186f4a42a6890a256a0bc6e0c0f02454d5452a02
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-19 | 2026-08-24T00:05:41+00:00 | from: codex | type: verdict | thread: plan-v080-field-fold-4 | refs: -

PASS for candidate `feature/installation-onboarding-v080@e5c90f6f1ee6e87c76817e0890e6071d9312782b` against immutable docket revision `4f4bd27adc26cdef039f29d52aadfd5c876d17c2dc6ba4bd436534cdecf4da53`.

Fresh evidence: `diff -u .../plan-round3.md .../docs/plans/2026-08-23-v080-field-fold.md` showed the round-3 fold adds `.debate/` export exclusion/manifest tests, one shared max-retry budget helper, explicit non-reserving preflight/race behavior for sealed and deliberation turns, supervisor-cap disclosure, and the mandatory v2 wrapper result shape. `sha256sum` over all 16 docket files matched every supplied SHA-256. `sed`/`rg` inspection of the pinned export confirmed the relevant current contracts: `controller.py` `_is_separated` currently excludes `collab/`, `var/`, `.git/`; `commit_reveal_pair` enforces paired capacity; `watcher.py` releases the channel writer lock before invoking; and `channel.py` permits typed managed closes at the cap.

No blockers. Plan §4A(4) correctly treats preflight as non-reserving, spends nothing when room is already insufficient, and specifies retained diagnostics/no vote/no retry plus typed `NO_PASS/thread-cap-race` for the post-preflight race. Its shared helper and conservative maximum per-party retry formula cover menu disclosure and actual opening, including unequal retries and supervisor entries. Plan §4B(4-6) keeps v2 enforcement dependency-free and independently rechecked, preserves v1 compatibility, and makes the custom-wrapper remedy executable. Plan §4C(1,4-5) closes the committed-hidden-state export gap and retains the exact-channel lock/prune safeguards. The round-1/2 compatibility, process-exit, evidence, path, collection, and installed-workflow repairs remain coherent with the protocol and pinned source.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: d1674949dd8f1f51b7309565a38525d139a517ac05d47ace8fa92c3933406bb8
- phase: sealed
- captured-at: 2026-08-24T00:05:41+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: b5fee4edf0fa6da032ebda1c27bb42a06d46c0ed14dde2f02c2643bcfe5cc347
- controller-config-sha256: cd179eb914997b99a0a05bbc2db0e255ec91bba4d90277038f80c5b1e2302207
- source-ref: e5c90f6f1ee6e87c76817e0890e6071d9312782b
- source-manifest-sha256: a933959b70d7c58c2de382fdca1945da173554b5d4cf80afabcbd88a43c6b279
- docket-revision-sha256: 4f4bd27adc26cdef039f29d52aadfd5c876d17c2dc6ba4bd436534cdecf4da53
- input-sha256: cdd7745e49b8bbedeaaf27d902fa6dc7cea8bd192cbbe94caf8f2a4393ede6ce
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.0
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox

## MSG-20 | 2026-08-24T00:05:41+00:00 | from: owner | type: close | thread: plan-v080-field-fold-4 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
