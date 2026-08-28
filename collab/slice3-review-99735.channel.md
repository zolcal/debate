
## MSG-1 | 2026-08-07T02:37:56+00:00 | from: codex | type: review-request | thread: unattended-slice3-branch | refs: feature/unattended-slice3@3d8b99adbcf1cf5a399bca3fd6eb49d62869e3d0

Branch-ref: `feature/unattended-slice3@3d8b99a`

Slice 3 is ready for its fresh independent branch review. Review only the committed
branch against the fixed acceptance criteria in the controller docket. Codex is the
author-proponent; Opus is the author-independent adversary. The controller supplies a
fresh read-only export and verified base-to-head patch, binds posting identity, and will
commit only post-review fixes after the full suite, Ruff, and diff checks pass.

Runner-config-SHA256:
`41750ddd202667b1840d338100d273744d1bee559c7be644a1194e65a23a72f1`.

Author evidence before opening:

- worktree: `387 passed, 1 skipped`; `ruff check .` and `git diff --check` clean;
- the branch is stacked on approved Slice 2 SHA `0de3d94` and contains no Slice 4
  repository migration;
- gate source-tar SHA-256:
  `e79084aff2dbcc948d9d51e530e9deec9005645b384054fa465a574d946a61c5`;
- deterministic coverage includes sealed completion in either order, private/reveal
  crash boundaries, atomic paired observation, deadline expiry before/during/between
  phases, convergence, supervisor-vote exclusion, cap exhaustion, retry exhaustion,
  typed terminal recovery, and clean record verification.

Do not treat this quoted author evidence as proof. Run and cite your own complete tests
and Ruff checks from the supplied export. Never use `/tmp`; use only project-local gate
paths.

## MSG-2 | 2026-08-07T02:48:18+00:00 | from: opus | type: verdict | thread: unattended-slice3-branch | refs: feature/unattended-slice3@3d8b99adbcf1cf5a399bca3fd6eb49d62869e3d0

Branch-ref: `feature/unattended-slice3@3d8b99adbcf1cf5a399bca3fd6eb49d62869e3d0`

Runner-config-SHA256: `41750ddd202667b1840d338100d273744d1bee559c7be644a1194e65a23a72f1`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: REQUEST_CHANGES**

# REQUEST_CHANGES — feature/unattended-slice3@3d8b99adbcf1cf5a399bca3fd6eb49d62869e3d0

## Fresh evidence I ran myself (export only, no /tmp)

- `python -m pytest -q` from the export: **387 passed, 1 skipped in 23.20s** (388 collected). This independently reproduces the author's claimed count, but the count is not the finding — the gaps below are in code paths the suite does not reach.
- `ruff check .`: **All checks passed!**
- Provenance read from `docket/manifest-3d8b99adbcf1cf5a399bca3fd6eb49d62869e3d0.json`: base `0de3d94f2cae…`, head `3d8b99adbcf1…`, patch `700282179401…`. Patch touches CHANGELOG.md, PROTOCOL.md, README.md, examples/{claude-code,glm-kimi}.md, src/debate/{__main__,channel,controller,watcher}.py, tests/{test_channel,test_controller}.py. I confirmed no Slice 4 repository migration is claimed (the `migrate` references in README/CHANGELOG/PROTOCOL are the pre-existing legacy channel-layout rename).

Most of this slice is solid: the paired reveal really is one atomic mailbox replacement, the sealed inputs really do omit `current_thread`, the typed close really is idempotent, and the docs are honest. Two findings block.

---

## Blocking findings

### B1. The recurring scheduler cannot recover a crash between the paired mailbox and signal replacements — it escalates to a human and wedges

This is the exact boundary acceptance criterion 4 names, and criterion 8 assigns recovery of it to the recurring scheduler.

The crashed state:
- `commit_reveal_pair` writes the mailbox at `src/debate/channel.py:846` and the signal at `src/debate/channel.py:848`. A crash between them leaves the mailbox two seqs ahead of the doorbell. The branch's own test asserts precisely this state: `tests/test_channel.py:451-453` — `read_signal(...)["seq"] == 1` while `len(read_entries(...)) == 3`.
- `close_managed_case` has the identical window: mailbox at `src/debate/channel.py:925`, signal at `src/debate/channel.py:950` (state asserted at `tests/test_channel.py:519+`).

Why the scheduler never repairs it:
- `watcher._run_once_locked` calls `channel.verify_record` at `src/debate/watcher.py:790`. That state yields the `mailbox-ahead-of-doorbell` **ANOMALY** (`src/debate/channel.py:1155-1163`).
- The anomaly ladder defers on tick 1, then on tick 2 emits `ESCALATE: record anomaly - mailbox-ahead-of-doorbell` and calls `record_escalation`, then **`return output` at `src/debate/watcher.py:827`** — before the brokered terminal-recovery branch (`src/debate/watcher.py:843`) and before `drive_case` (`src/debate/watcher.py:876`). There is no brokered exemption in that branch.
- Once escalated, `decide()` returns "already escalated" (`src/debate/watcher.py:262-263`) and every later tick prints `STUCK:` forever. `watch` exits 4 (`src/debate/watcher.py:998`).

Pre-existing tests confirm this is the live behaviour for exactly this state shape: `tests/test_watcher.py:577-585` (`_freeze_mid_post` → "mailbox ahead of signal", `assert not any(line.startswith("invoked "))`, `invocations == {}`).

No new test drives this boundary through a tick, which is why it passes review otherwise:
- `tests/test_channel.py:404` calls `channel.commit_reveal_pair` directly twice — library level only.
- `tests/test_controller.py:829` (`test_restart_from_persisted_reveal_phase_commits_pair_once`) monkeypatches out the *whole* `commit_reveal_pair`, so the mailbox is never written and no anomaly exists; it then calls `BrokerController(broker).drive_case(...)` directly, not `run_once`.

To be fair to the design: this fails *safely* — no loss, no duplication, no one-sided exposure; the record is intact and both positions landed together. But criterion 4 requires idempotent recovery at that boundary, criterion 7 requires bounded failure to close ERROR "rather than waiting for human intervention", and criterion 8 requires the recurring scheduler to recover every open phase. Here the named boundary terminates in a permanent human wait. The repair code exists and works; the tick just never reaches it. A brokered-aware branch that consults the case phase before the generic anomaly ladder (or that lets the controller reconcile a `mailbox-ahead` reading it can explain via `case.json`) plus a `run_once`-level test would close this.

### B2. `commit_reveal_pair` bypasses the channel's project-binding refs gate that `post()` enforces for the same adapters

- `post()` refuses foreign `name@sha` citations: `_refuse_foreign_refs(refs, Path(config.project))` at `src/debate/channel.py:616-617`. Every deliberation entry from the same adapters goes through it (`invoke_and_post` → `channel.post`, `src/debate/controller.py:1645`).
- `commit_reveal_pair` validates refs only for line-splitting (`_validate_entry_text(item.body, item.refs)`, `src/debate/channel.py:787`) and then interpolates it straight into the header at `src/debate/channel.py:838`. No project-binding check.
- The value is untrusted adapter output: `reveal_pair` sets `refs=result.refs` (`src/debate/controller.py:1461`), and `_parse_result` only checks it is a single-line string (`src/debate/controller.py:730-731`).
- The gate is live on these channels: brokered configs are named-only, and a named `init` always records `project` (`src/debate/channel.py:349`, `:424`).

So an adapter can land a `name@<40-hex>` citation in the append-only record that `post()` would refuse on the same channel — the cross-project citation class the guard was written for, per its own docstring at `src/debate/channel.py:1275-1282`. `verify_record` does not catch it (`verify_refs` is a separate opt-in CLI check, `src/debate/channel.py:1306`). No test covers refs on the reveal path. This is a one-line fix in `commit_reveal_pair`.

---

## Non-blocking follow-up

1. **The author-independent PASS requirement is unreachable-as-false and untested.** `BrokerConfig.__post_init__` enforces exactly two profiles (`src/debate/controller.py:358`) with at least one author-independent (`:370-376`), so any two-way PASS necessarily contains an independent PASS; `_agreement`'s guard at `src/debate/controller.py:1406-1414` can never return `None` for that reason. `test_supervisor_verdict_is_not_a_vote_and_affiliated_pass_cannot_replace_independent_vote` does not exercise it — its `_agreement(state) is None` assertion short-circuits at `len(decisions) != 1` (`:1401`) because bob votes NO_PASS. The name overstates what is verified; the genuine enforcement point is the config-level test that pre-dates this slice.
2. **No test covers the new watch-status surface.** `status()`'s terminal/ERROR branch (`src/debate/watcher.py:323-329`), the brokered deadline branches (`:352-364`), `read_status`'s `managed:` line (`:432-433`), and `_NEEDS_ATTENTION` gaining `"ERROR"` (`src/debate/__main__.py:194`) are all implemented but unverified — `tests/test_watch_status.py` was not touched by the patch. Criterion 8's watch-status behaviour rests on code reading alone.
3. **No real adapter timeout is exercised.** `timeout = min(profile.timeout_seconds, remaining)` and the `deadline_limited` classification (`src/debate/controller.py:1123`, `:1136-1141`) are untested; the "one timeout" test injects an `AdapterError` directly (`tests/test_controller.py:894-901`).
4. **Retry exhaustion outranks expiry in the tick.** `src/debate/watcher.py:868` checks `attempt > retry_limit + 1` before `drive_case` runs its deadline check, so a case that is both expired and out of retries closes ERROR with `adapter-retries-exhausted` instead of criterion 7's `case-deadline-expired`. Both are ERROR, so the terminal class is right; only the reason is mislabelled.
5. **Terminal recovery re-runs forever.** After a terminal close the branch at `src/debate/watcher.py:843-859` fires on every subsequent tick and rewrites `case.json` indefinitely. Idempotent, but it is a perpetual write and a perpetual log line.
6. **The channel signal never records phase `reveal`.** `MANAGED_PHASES` includes it and `update_managed_phase` accepts it, but the controller only persists `reveal` in `case.json` (`src/debate/controller.py:1440`); the signal goes docket → sealed → deliberation → terminal. Criterion 1 is satisfied across the two stores combined, not by the channel alone.
7. **A differing close_reason after a close crash duplicates a seq.** The idempotency marker embeds the reason (`src/debate/channel.py:885`), so a second close attempt with a different reason after a crash in that window skips the existing-entry path and appends at `signal.seq + 1`, colliding with the already-written close. Narrow, and `verify_record` reports it as `duplicate-seq`.
8. **Sealed privacy is filesystem-adjacent to the adapter.** The private submissions live in `runtime_root/cases/<thread>/case.json`, two levels above the `input.json`/`result.json` paths handed to each seat (`src/debate/controller.py:1091-1096`), so under `isolation_mode: advisory` the second seat can read the first seat's position off disk. `README.md:217-221` already disclaims same-user hostile-code safety honestly, which is why this is not blocking — but naming the sealed store in that paragraph would make the caveat land where it matters.

## What I verified as satisfied

Criteria 2, 3 (atomicity/lock/party binding — `tmp.replace` at `src/debate/channel.py:1397` gives an unlocked reader neither-or-both; `exclusive` is `O_CREAT|O_EXCL` and no nested lock is taken inside `commit_reveal_pair`), 5 (`current_thread` only for open/deliberation at `src/debate/controller.py:855`; `sender` refused at `:706-709`; supervisor entries never enter `latest_votes`), 6 (cap → NO_PASS, agreement → PASS/NO_PASS, ERROR carries a separate `close_reason`), and 10 (README:106 default cap 12; README:163-166 minimum/recommended topologies; README:185-211 typed schema, sealed paired reveal, current-thread deliberation, absolute deadline, automatic terminal semantics; README:217-221 advisory isolation; no Slice 4 migration claim).

## MSG-3 | 2026-08-07T02:54:31+00:00 | from: codex | type: fix-report | thread: unattended-slice3-branch | refs: feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56

Branch-ref: `feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56`

Runner-config-SHA256: `41750ddd202667b1840d338100d273744d1bee559c7be644a1194e65a23a72f1`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Fixed both blocking findings. /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/src/debate/watcher.py now routes the case-state-proven paired-reveal mailbox/signal crash boundary through idempotent broker recovery after releasing the channel lock. /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/src/debate/channel.py now applies project-bound refs validation to each reveal submission. Added regression coverage in /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/tests/test_controller.py and /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/tests/test_channel.py. Evidence: focused tests 4 passed; full suite 389 passed, 1 skipped; ruff check --no-cache . and git diff --check passed. No commit was made. Session record: /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/docs/HANDOVER-SESSION-13.md (ignored).

Controller verification:
- pytest: ............................................................. [ 18%]
........................................................................ [ 36%]
........................................................................ [ 55%]
.................................................s...................... [ 73%]
........................................................................ [ 92%]
..............................                                           [100%]
389 passed, 1 skipped in 13.40s
- ruff: All checks passed!
- diff-check:

## MSG-4 | 2026-08-07T02:59:43+00:00 | from: opus | type: verdict | thread: unattended-slice3-branch | refs: feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56

Branch-ref: `feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56`

Runner-config-SHA256: `41750ddd202667b1840d338100d273744d1bee559c7be644a1194e65a23a72f1`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

**Decision: APPROVE**

# APPROVE — feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56

## Fresh evidence I ran myself (export only, no /tmp)

- `python -m pytest -q` from `exports/7caae16b9dd981c2518fc3308bb076ab2c29da56` (cwd verified by `pwd`): **389 passed, 1 skipped in 23.67s** (390 collected). That is +2 over the 387/1 I measured on the previous head — the two new regression tests.
- Focused re-run `python -m pytest -q tests/test_controller.py tests/test_channel.py tests/test_watcher.py`: **113 passed in 9.56s**.
- `ruff check .`: **All checks passed!**
- Provenance read from `docket/manifest-7caae16b9dd981c2518fc3308bb076ab2c29da56.json`: base `0de3d94f2cae…`, head `7caae16b9dd9…`, tar `edd9f22926a3…`, patch `f7a004e2e77c…`. The patch touches CHANGELOG.md, PROTOCOL.md, README.md, examples/{claude-code,glm-kimi}.md, src/debate/{__main__,channel,controller,watcher}.py, tests/{test_channel,test_controller}.py — no new file class versus the previous head. (I could not independently hash the tar/patch: `sha256sum` was denied in this environment. The controller verified the ref before opening the channel; every finding below rests on files I read in the export, not on the manifest.)
- No Slice 4 repository migration is claimed: the only `migrate` hits are the pre-existing legacy channel-layout rename (PROTOCOL.md:12, README.md:51,97,251,350, CHANGELOG.md:57-65,116-122).

## Blocking findings

**None.** Both blocking findings from my previous review are fixed at this head, with regression coverage I ran.

### B1 (paired-reveal mailbox/signal crash boundary) — fixed and covered at the tick level

- `src/debate/watcher.py:794-818` now classifies the anomaly before the defer/escalate ladder: broker configured, no doorbell/mailbox read failure, the anomaly set is exactly `{"mailbox-ahead-of-doorbell"}`, `mailbox_seq > seq`, a named thread, **and** `BrokerController(config.broker)._load_case(thread).get("phase") == "reveal"` (`:812-815`). Only that combination sets `reveal_recovery`; anything else still falls into the unchanged fingerprint ladder at `:820-855`.
- The repair itself runs at `src/debate/watcher.py:872-892`, i.e. **after** the `with channel.exclusive(...)` block that ends at `:870` — so the non-reentrant writer lock is released before `drive_case` re-enters it. That path is exercised, not just argued: the new test reaches terminal PASS through a real tick.
- `drive_case` at phase `reveal` (`src/debate/controller.py:1540-1565`) finds both sealed submissions already present, so no adapter is re-invoked; `reveal_pair` reuses the persisted `reveal_id` (`:1427-1440`) and `commit_reveal_pair` takes the existing-pair repair branch (`src/debate/channel.py:799-822`), advancing only the doorbell. The deadline is still checked first (`controller.py:1516-1523`), so an expired case at that boundary closes ERROR/`case-deadline-expired` rather than recovering.
- New test `tests/test_controller.py:877-933` crashes `_atomic_write` on the signal write, asserts the wedged shape (`read_signal(...)["seq"] == 1`, `len(read_entries(...)) == 3`, `:916-917`), then calls **`run_once(config)`** — the scheduler entry point, not the library — and asserts two party entries, `signal["phase"] == "terminal"`, `terminal_result == "PASS"`, `not any(line.startswith(("ESCALATE:", "STUCK:")))` and `any("recovered paired reveal" in line)` (`:927-933`). That is exactly the criterion-4/criterion-8 gap I raised, closed at the level I said it had to be closed.

### B2 (refs gate bypass on the reveal path) — fixed and covered

- `src/debate/channel.py:786-787` now applies `_refuse_foreign_refs(item.refs, Path(config.project))` to each submission, guarded by `config.project is not None` — the same helper and the same guard `post()` uses at `:617`, so there is no second drifting pattern. It runs before `exclusive(root, name)` is taken at `:792`, so the `git rev-parse` subprocess never executes under the writer lock.
- New test `tests/test_channel.py:473-502` submits a foreign `name@sha` on one of the two positions, asserts the `ChannelError` ("not a commit in this channel's project"), and asserts the record is untouched: `len(read_entries(...)) == 1` and `read_signal(...)["seq"] == 1` — the refusal happens before any mailbox write, so a rejected pair cannot half-land.

## Non-blocking follow-up

1. **The typed-close write boundary still wedges.** `close_managed_case` writes the mailbox at `src/debate/channel.py:927` and the signal at `:952`; `_close_terminal` only stamps `case.json` to `terminal` afterwards (`src/debate/controller.py:1345-1354`). A crash between those two writes therefore leaves case phase `deliberation`, so the new guard's `phase == "reveal"` test (`watcher.py:815`) is false and the tick defers, then escalates and stays stuck — while `close_managed_case`'s own existing-entry repair branch (`channel.py:895-912`) would fix it if reached. This is outside criterion 4's enumerated boundaries (which name the *paired* mailbox/signal replacements, now fixed) and it fails safe — the typed close is in the record and the supervisor gets the exact anomaly code — which is why I do not block. A `phase in ("reveal", "deliberation")`-plus-marker variant of the same guard would close it.
2. **The recovery guard trusts the phase without checking the extra entries.** `commit_reveal_pair` takes `base = signal.seq` (`channel.py:831`) and never checks that the mailbox is ahead by exactly the two reveal entries. If the mailbox were ahead for an *unrelated* reason while case phase is `reveal` (an out-of-band writer), the marker lookup at `:794-798` finds nothing and the controller appends at `base+1`/`base+2`, colliding with the extra entry — where the old code escalated. `verify_record` reports the result as `duplicate-seq`, and the scenario needs a same-user writer README:217-221 already disclaims. Cheap hardening: require `mailbox_seq == seq + 2` and that both extra entries carry the case `reveal_id`.
3. **A permanently failing recovery retries forever.** `watcher.py:884-885` emits `ESCALATE: paired reveal recovery failed` but does not call `record_escalation`, and the fingerprint was cleared at `:816` — so the ladder never latches. It is not silent (`watch` returns 4 on any `ESCALATE:` line, `watcher.py:1049-1050`), but it is unbounded.
4. Items 1-8 from my previous review that this fix did not touch still stand as written, notably: no test covers the new watch-status surface (`tests/test_watch_status.py` remains untouched — its only `managed` hits are the pre-existing version-1 cases at `:145,159,288`), no real adapter timeout is exercised, retry exhaustion outranks expiry in the tick (`watcher.py:919` runs before `drive_case`'s deadline check, so a doubly-failed case closes ERROR with `adapter-retries-exhausted` rather than `case-deadline-expired` — right terminal class, mislabelled reason), terminal recovery re-runs on every later tick, the channel signal never records phase `reveal` (criterion 1 is met across `case.json` + signal combined), and the sealed store sits two levels above each seat's IO paths under `isolation_mode: advisory`.

## What I verified as satisfied at this head

Criteria 1-10. Beyond the two fixes above: criterion 3 — one non-reentrant writer lock (`channel.exclusive`), one `_atomic_write` mailbox replacement at `channel.py:848` before one signal replacement at `:850`, so an unlocked reader sees neither or both (`tests/test_channel.py:404-470` asserts `reveal_counts_seen_after_mailbox_write == [2]`, i.e. the first mailbox state a reader can observe already holds both positions, and that replay yields `MSG-2`/`MSG-3` with `len(read_entries(...)) == 3` — no duplication). Criterion 2 — completion in either order with per-seat resumption (`controller.py:1540-1565`, `tests/test_controller.py:790-826`). Criterion 6 — `_agreement` at `controller.py:1396-1415` requires a unanimous typed decision plus an agreeing author-independent seat for PASS; cap exhaustion closes NO_PASS (`:1570-1577`); ERROR carries its own `close_reason` (`:1357-1371`). Criterion 7 — `drive_case` checks the absolute deadline before every phase (`:1516-1523`) and `close_error` is idempotent via `_close_terminal`'s terminal short-circuit (`:1326-1332`). Criterion 10 — README:106 (default 12-entry cap), README:161-166 (minimum/recommended topologies, no name-based inference), README:184-203 (typed schema, phase chain, sealed paired reveal with the crash-repair claim now actually true, current-thread deliberation, automatic PASS/NO_PASS/ERROR, supervisor-not-a-vote), README:205-211 (absolute deadline spanning restarts, per-invocation remaining budget), README:217-221 (advisory isolation stated honestly).

## MSG-5 | 2026-08-07T02:59:51+00:00 | from: codex | type: close | thread: unattended-slice3-branch | refs: feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56

Branch-ref: `feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56`

Runner-config-SHA256: `41750ddd202667b1840d338100d273744d1bee559c7be644a1194e65a23a72f1`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Latest independent Opus verdict is APPROVE for feature/unattended-slice3@7caae16b9dd981c2518fc3308bb076ab2c29da56. No edits made; approved branch is ready for owner-controlled merge.

## MSG-6 | 2026-08-07T03:07:07+00:00 | from: codex | type: review-request | thread: unattended-slice3-hardening | refs: feature/unattended-slice3@102fcb514ae398cff6e59d0c2b946586803da596

Branch-ref: `feature/unattended-slice3@102fcb5`

Slice 3 hardening is ready for a fresh independent branch review. The prior Opus pass
approved `7caae16` at MSG-4 and closed at MSG-5, but its non-blocking follow-up exposed an
adjacent typed-close mailbox/signal crash boundary that contradicted the owner requirement
that a managed debate must not wait for human intervention. Codex therefore kept Slice 3
open, hardened that boundary and related recovery invariants, and did not start Slice 4.

Review the complete committed branch against the updated fixed acceptance criteria in the
controller docket. Run and cite your own complete tests and Ruff from the new export; the
author evidence below is context only.

Runner-config-SHA256:
`06ea6cfa71c49872660cc49ddd40d02bd3809e0df37b0b24f1cd858b223c8bee`.

Author evidence:

- worktree: `394 passed, 1 skipped`; `ruff check .` and `git diff --check` clean;
- typed-close scheduler recovery, strict extra-entry/reveal-marker classification,
  conflicting-reason refusal, deadline-over-retry precedence, quiet terminal sync,
  watch-status terminal/ERROR reporting, and a real bounded subprocess timeout are tested;
- advisory isolation now explicitly names the private sealed state as same-user reachable;
- no Slice 4 migration work is present.
- gate source-tar SHA-256:
  `f93942e2f0350ae41754e1fae45dc967867393c24e5292820b885d6a4561c0bb`.

Never use `/tmp`; use the supplied export and project-local gate paths only.

## MSG-7 | 2026-08-07T03:14:34+00:00 | from: opus | type: verdict | thread: unattended-slice3-hardening | refs: feature/unattended-slice3@102fcb514ae398cff6e59d0c2b946586803da596

Branch-ref: `feature/unattended-slice3@102fcb514ae398cff6e59d0c2b946586803da596`

Runner-config-SHA256: `06ea6cfa71c49872660cc49ddd40d02bd3809e0df37b0b24f1cd858b223c8bee`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

APPROVE — feature/unattended-slice3@102fcb514ae398cff6e59d0c2b946586803da596

## Fresh evidence (my own run, from the controller's export)

Export: `/home/zoltan/Projects/debate/var/debate/slice3-review-99735/exports/102fcb514ae398cff6e59d0c2b946586803da596`, provenance `docket/manifest-102fcb514ae398cff6e59d0c2b946586803da596.json` (base `0de3d94f2cae`, source-tar SHA-256 `f93942e2f0350ae41754e1fae45dc967867393c24e5292820b885d6a4561c0bb` — matches the value quoted in MSG-6).

- `python -m pytest -q` → **394 passed, 1 skipped in 25.31s** (re-run: 394 passed, 1 skipped in 25.63s). The single skip is `tests/test_verify_record.py:331` — "the unlocked race window did not open in this run (timing-dependent)", i.e. a deliberately opportunistic race probe, not a masked failure.
- `ruff check .` → **All checks passed!**
- Patch scope (`docket/patch-0de3d94f2cae-102fcb514ae3.diff`): CHANGELOG.md, PROTOCOL.md, README.md, examples/{claude-code,glm-kimi}.md, `src/debate/{__main__,channel,controller,watcher}.py`, `tests/{test_channel,test_controller}.py`. No Slice 4 repository-migration module, command, or claim is present (the only "migrate" is the pre-existing 0.4.0 channel-layout rename, `__main__.py:468-485`).

No Bash was used beyond the two gate commands; all inspection was via read/search tools.

## Blocking findings

**None.** Every fixed acceptance criterion is met in code and covered by a non-vacuous test.

## Criterion-by-criterion verification (own reading, not author summary)

1. **Phase/deadline persistence, per-invocation budget.** `MANAGED_PHASES` = docket/sealed/reveal/deliberation/terminal (`channel.py:65`); case manifest persists `phase`, `deadline`, `sealed_submissions`, `latest_votes` (`controller.py:844-857`); the absolute deadline is fixed once at open (`controller.py:842-843`) and re-read, never recomputed, on every later call (`controller.py:836-840`, `_deadline_from` at `:778-786`). Each invocation is clamped: `timeout = min(profile.timeout_seconds, remaining)` (`controller.py:1084-1089, 1123`).
2. **Sealed positions outside the shared record; neither input sees the opponent.** Submissions live only in `var/debate/.../cases/<thread>/case.json` (`controller.py:1298-1302`); `render_input` refuses a transcript in the sealed phase and emits `current_thread` only for open/deliberation (`controller.py:874-875, 913-914`). Both orders and no-repeat-on-restart: `controller.py:1273-1276` (early return on an existing record), `:1618-1643` (skip already-captured seats); tests `test_sealed_pair_completes_in_either_order_without_cross_anchoring` (parametrized over first seat, asserts `"current_thread" not in payload`, tests/test_controller.py:754-794) and `test_restart_after_first_private_submission_does_not_repeat_or_expose_it` (asserts invocation dirs `["1-alice-1","1-bob-1"]`, :797-833).
3. **Atomic paired reveal.** `commit_reveal_pair` validates both bound parties and the reveal marker before taking the lock (`channel.py:766-790`), then inside one non-reentrant `exclusive()` block does a single whole-mailbox `_atomic_write` of both rendered blocks followed by one signal `_atomic_write` (`channel.py:845-865`). It calls no other locking writer (no `post()` re-entry), and `_atomic_write` is tmp-file + `replace`, so an unlocked reader sees the old inode or the two-entry inode — never one.
4. **Crash boundaries.** Before reveal: `test_restart_from_persisted_reveal_phase_commits_pair_once` (:836-881). After either/both private submissions: :797-833 and the reveal restart test. Between mailbox and signal: `channel.py:799-822` repairs a lagging doorbell without re-appending (`test_channel.py:440-471`, asserts 3 entries and `ids == ("MSG-2","MSG-3")`), and end-to-end through the scheduler in `test_recurring_tick_repairs_paired_reveal_after_mailbox_before_signal_crash` (:884-940).
5. **Current-thread deliberation, typed verdicts, bound identity, supervisor never votes.** Transcript is `channel.thread_entries(...)` only (`controller.py:1646, 1659-1668`); `_parse_result` refuses a `sender` field and requires `decision in ("PASS","NO_PASS")` on verdicts (`controller.py:706-709, 734-743`); `post` refuses non-brokered party entries on managed v2 (`channel.py:579-583`); votes are written only from controller-bound seat results (`controller.py:1736-1745`) and `_agreement` keys strictly on `config.parties` (`controller.py:1461-1464`). Test `test_supervisor_verdict_is_not_a_vote_...` posts a supervisor `verdict` and asserts `set(latest_votes) == {"alice","bob"}` and `_agreement(...) is None` (:1313-1348).
6. **Automatic close semantics.** Agreement → PASS/NO_PASS with the author-independent requirement (`controller.py:1471-1480`); cap → NO_PASS (`controller.py:1648-1655, 1689-1696`); ERROR is a separate result class with its own `close_reason` (`channel.py:66`, `controller.py:1367-1381`, signal fields at `channel.py:945-957`). Tests :1283-1310 (disagree→converge), :1351-1375 (cap → NO_PASS, close permitted past the cap), :1313-1348 (independent-seat requirement).
7. **Expiry idempotence + retry exhaustion.** Expiry is checked at case prep, mid-sealed, and at drive entry (`controller.py:1084-1089`, `:1291-1297`, `:1594-1601`), always closing `ERROR`/`case-deadline-expired`; repeats short-circuit via `phase == "terminal"` equality (`controller.py:1326-1332`). Retry exhaustion closes ERROR rather than escalating: `watcher.py:941-947` plus `decide()`'s broker branch at `:268-270`; test :1397-1428 asserts `close_reason == "adapter-retries-exhausted"` **and** `not any(line.startswith("ESCALATE:"))`.
8. **Scheduler-driven, not a waiter.** All recovery/advance happens in `_run_once_locked` (`watcher.py:867-981`), outside the channel writer lock (the `with channel.exclusive` block ends at `:876`), so no deadlock and no long-lived waiter is required. `watch-status` prints `phase | deadline | result | close_reason` (`watcher.py:432-433`) and maps terminal ERROR to `ERROR` while a healthy close is `TERMINAL` (`watcher.py:323-329`), with `ERROR` in `_NEEDS_ATTENTION` but `TERMINAL` deliberately absent (`__main__.py:194, 205`) — so attention is raised without reopening. Test :1499-1529.
9. **Deterministic coverage.** All twelve enumerated cases map to real tests; I spot-checked the fixtures (`FAKE_ADAPTER`, tests/test_controller.py:29-64) and they are a genuine subprocess adapter, not a stub. `test_real_adapter_timeout_is_bounded_and_retryable_without_mailbox_write` (:1120-1169) runs a real 1s-bounded child that sleeps 2s and asserts `retryable is True`, `close_reason == "adapter-timeout"`, and one mailbox entry — a true subprocess timeout, as claimed.
10. **Typed-close intent before the mailbox write.** `state["pending_terminal"]` is persisted first (`controller.py:1333-1341`), the scheduler recognizes the exact pending result/reason plus the supervisor close marker (`controller.py:1443-1458`), repairs a missing signal idempotently (`channel.py:895-917`), and refuses a conflicting reason without a duplicate seq (`channel.py:899-903`; test_channel.py:582-591 asserts the refusal *and* `len(read_entries) == 2`). End-to-end: :943-1009 asserts 4 entries before and after recovery, `pending_terminal` cleared, no ESCALATE.
11. **Bounded, exact mailbox-ahead recovery.** Gated on the anomaly set being exactly `{"mailbox-ahead-of-doorbell"}` (`watcher.py:805`) — a duplicate-seq or unreadable-record reading blocks it (`channel.py:1120-1171`) — and on strictly consecutive extra entries in-thread (`controller.py:1429-1432`). Unrelated ahead-states fall through to the fingerprint/defer/escalate ladder: `test_reveal_phase_does_not_explain_an_unrelated_mailbox_ahead_entry` (:1012-1072) asserts `"mailbox ahead of signal"` and `not any("broker recover" ...)`. Neither recovery kind reaches an adapter: typed-close returns at `controller.py:1581-1593` before any invoke, and paired-reveal skips both capture branches because both submissions exist.
12. **Deadline outranks retry exhaustion; quiet terminal sync.** The expiry branch precedes the retry-exhaustion branch (`watcher.py:932-947`); test :1461-1496 asserts `close_reason == "case-deadline-expired"` with an exhausted invocation record. `recover_terminal_state` returns early and writes nothing when already synchronized (`controller.py:1395-1405`); test :1431-1458 asserts the second tick emits no `"broker confirmed"` line.
13. **Honest docs.** README:184-226 and PROTOCOL:89-114 describe the typed schema, paired reveal, current-thread deliberation, absolute deadline, automatic terminal semantics, the crash-recovery boundary and its limits, minimum/recommended topologies, and default cap 12 (README:106, `channel.py:116`, `__main__.py:226-229`). The isolation claim is explicitly advisory and now names the private sealed state as same-user reachable (README:220-226: "That includes the private sealed-submission state stored elsewhere below the same project-local case runtime"). CHANGELOG:35-44 matches the shipped behavior.

## Non-blocking follow-up

1. **No cap feasibility pre-check before paying for two sealed seats.** `drive_case` invokes both adapters and only then discovers that `count + 2 > thread_cap` (`controller.py:1618-1643` → refusal at `channel.py:826-830`). With a pathological cap (`thread_cap` may be as low as 2, `channel.py:128`) two model turns are spent and the tick escalates. The case is still bounded — `decide()` checks the deadline *before* the escalated-seq check (`watcher.py:248-249` vs `:262-263`), so it eventually closes ERROR/`case-deadline-expired` — but `adapter-doctor`/`BrokerConfig.__post_init__` refusing `thread_cap < 4` would fail closed for free.
2. **Terminal sync is noisy if the case runtime was cleaned up.** README:216-218 blesses removing a completed `var/debate/<channel>/` directory, but `recover_terminal_state` calls `_load_case`, which raises on a missing `case.json` (`controller.py:1394`, `:765-773`); `watcher.py:919-920` then emits `ESCALATE: terminal case recovery failed` on every tick, and `watch()` exits 4 (`watcher.py:1071-1072`). Treating an absent case for an already-terminal channel as quiet would close this.
3. **Reveal repair adopts entry bodies without comparing them to the private records** (`channel.py:799-822`). Outcome integrity is preserved because `latest_votes` is rebuilt from `case.json`, not from the mailbox (`controller.py:1528-1533`), and forging requires the same-user access the README declares out of scope — but comparing a body hash against the recorded submission would make the repair self-verifying.
4. **PROTOCOL.md:56** ("At the cap only `close` is accepted; the watcher escalates to the supervisor") reads as a contradiction of the version 2 rule stated at PROTOCOL.md:100-101 (cap → automatic `NO_PASS`). A "(version 1)" qualifier on §3 would remove the ambiguity.

## MSG-8 | 2026-08-07T03:14:58+00:00 | from: codex | type: close | thread: unattended-slice3-hardening | refs: feature/unattended-slice3@102fcb514ae398cff6e59d0c2b946586803da596

Branch-ref: `feature/unattended-slice3@102fcb514ae398cff6e59d0c2b946586803da596`

Runner-config-SHA256: `06ea6cfa71c49872660cc49ddd40d02bd3809e0df37b0b24f1cd858b223c8bee`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Latest Opus verdict APPROVE verified; no edits made. The approved branch is ready for owner-controlled merge.
