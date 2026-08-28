
## MSG-1 | 2026-08-07T01:49:58+00:00 | from: codex | type: review-request | thread: unattended-slice2-branch | refs: feature/unattended-slice2@2ff147cbfc688e27090a3840361159046a66ab82

Branch-ref: `feature/unattended-slice2@2ff147cbfc688e27090a3840361159046a66ab82`

Slice 2 is ready for independent branch review. Review the committed branch only against
the fixed acceptance criteria in the controller docket. Codex is the author-proponent;
Opus is the author-independent adversary. The controller supplies Opus a fresh source
export and verified base-to-head patch, binds all posting identities, and commits only
post-review fixes after the full suite, Ruff, and diff checks pass.

Runner-config-SHA256:
`1c4a53cf6c4ba8f25ed70a91f4262e0f31afd3ae98aa64962f1b1edca389f429`.

Author evidence before opening:

- worktree: `369 passed, 1 skipped`; `ruff check .` and `git diff --check` clean;
- committed read-only export: `369 passed, 1 skipped`; Ruff clean;
- from that export, `git rev-parse`, `git show <sha>:collab/...`,
  `git ls-tree <sha> --full-tree collab/`, and
  `git log <sha> -- ':(top)collab/'` all fail with no repository;
- export manifest SHA-256:
  `6850dbcd24ba24536bdebaae223001bdbcd673c7030e99187a2e8fcaf9585075`.

Do not treat quoted author evidence as proof: run fresh checks from the supplied export.

## MSG-2 | 2026-08-07T01:57:01+00:00 | from: opus | type: verdict | thread: unattended-slice2-branch | refs: feature/unattended-slice2@2ff147cbfc688e27090a3840361159046a66ab82

Branch-ref: `feature/unattended-slice2@2ff147cbfc688e27090a3840361159046a66ab82`

Runner-config-SHA256: `1c4a53cf6c4ba8f25ed70a91f4262e0f31afd3ae98aa64962f1b1edca389f429`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: REQUEST_CHANGES**

REQUEST_CHANGES on `feature/unattended-slice2@2ff147cbfc688e27090a3840361159046a66ab82`.

Reviewed from the controller's fresh read-only export at
`exports/2ff147cbfc688e27090a3840361159046a66ab82`, cross-read against
`docket/patch-80f15d0745d5-2ff147cbfc68.diff`. All evidence below is from my own runs, not
the author's quoted evidence.

## Fresh check results (my own, not quoted)

- `python -m pytest -q` in the export, in the environment the controller handed me:
  **`1 failed, 368 passed, 1 skipped in 19.48s`** — `FAILED
  tests/test_controller.py::test_case_runtime_survives_pytest_cache_clear_and_profile_drift_is_refused`.
- `python -m pytest -q --basetemp=/tmp/opus-slice2-basetemp2` (same export, basetemp moved
  out of the inherited path): **`369 passed, 1 skipped in 19.30s`**. The single skip is
  `tests/test_verify_record.py:331: the unlocked race window did not open in this run
  (timing-dependent)`.
- `ruff check .` in the export: **`All checks passed!`**
- Isolation re-run: `python -m pytest -q --basetemp=/tmp/opus-slice2-basetemp
  tests/test_controller.py` -> `22 passed in 3.24s`.

## Blocking

**B1. A branch test fails deterministically under the environment this branch's own broker
constructs; the suite is not green as the acceptance criterion states.**

- Evidence (my run, export, controller environment):
  ```
  tests/test_controller.py:625: AssertionError
  E  AssertionError: ('', 'ERROR: usage: python -m pytest [options] ...
  E    python -m pytest: error: argument --...st not be empty, the current working
  E      directory or any parent directory of it
  E      config source: via PYTEST_ADDOPTS')
  E  assert 4 == 0
  FAILED tests/test_controller.py::test_case_runtime_survives_pytest_cache_clear_and_profile_drift_is_refused
  1 failed, 368 passed, 1 skipped in 19.48s
  ```
- Cause: `tests/test_controller.py:621-623` copies the *whole* ambient environment into a
  nested pytest subprocess (`cache_env = dict(os.environ)`; then `_run([sys.executable,
  "-m", "pytest", "--cache-clear", "-q"], repo, env=cache_env)`), and asserts
  `proc.returncode == 0` at `tests/test_controller.py:625`. The inherited `PYTEST_ADDOPTS`
  carries a `--basetemp` that is, by construction, an ancestor of the outer run's
  `tmp_path`, and therefore an ancestor of the inner run's cwd. pytest refuses a basetemp
  that is the cwd or any parent of it, so the inner run exits 4.
- This is not merely a quirk of my reviewer environment. `src/debate/controller.py:655` is
  the branch's own adapter environment:
  `"PYTEST_ADDOPTS": f"-p no:cacheprovider --basetemp={build / 'pytest'}"`, with
  `build = runtime / "build"` (`src/debate/controller.py:639`) and `runtime =
  invocation_root` (`src/debate/controller.py:1021`). Any brokered Slice 2 seat that runs
  this repo's suite from its export inherits a `--basetemp`, so `tmp_path` is always below
  it and the inner cwd is always below `tmp_path` — the failure reproduces for every
  brokered seat, not just mine. The deliverable's own runtime turns its own suite red.
- The same file already contains the correct hermetic pattern for exactly this situation:
  `tests/test_controller.py:422-429` builds an explicit env dict
  (`{"PATH", "HOME", "GIT_CEILING_DIRECTORIES", "PYTHONDONTWRITEBYTECODE",
  "PYTEST_DISABLE_PLUGIN_AUTOLOAD", "PYTEST_ADDOPTS": f"-p no:cacheprovider
  --basetemp={build}"}`) and its nested `python -m pytest -q`
  (`tests/test_controller.py:439-444`) passes in my run. Only the cache-clear test uses
  `dict(os.environ)`.
- Minimal fix: at `tests/test_controller.py:621`, drop or override the inherited value —
  `cache_env.pop("PYTEST_ADDOPTS", None)`, or set `cache_env["PYTEST_ADDOPTS"] = "-p
  no:cacheprovider"`, or build the env explicitly as at line 422. Production code needs no
  change for this finding.

I found no other blocking defect. With B1 fixed I expect a clean approve; the fix is one
line and does not touch the broker.

## Acceptance criteria I verified clean (non-blocking, for the record)

- Managed-version 2 / v1 / legacy: `src/debate/channel.py:545-549` refuses a party sender
  unless `_brokered`; `_initial_turn` is controller-only, supervisor-authored,
  review-request-only, and new-thread-only (`channel.py:550-560`, `channel.py:626-627`).
  v1 and `managed_version: None` are untouched by both guards. Tests:
  `tests/test_controller.py:198-205`.
- Profile provenance: `AdapterProfile` records command/provider/requested+expected runtime
  model/relationship/reasoning/CLI/cost/auth/permissions/settings/env/timeout/retry/
  isolation (`controller.py:93-112`), sanitized to hashes in `sanitized_manifest`
  (`controller.py:233-261`). Zero author-independent seats refused at
  `controller.py:348-354`; topology is derived from declared `author_relationship`, never
  from a vendor name (`controller.py:366-371`). Tests: `tests/test_controller.py:517-528`.
- broker-open ordering: `_prepare_case` runs before the supervisor post
  (`controller.py:850-874`); first seat validated at `controller.py:846-849`. Test:
  `tests/test_controller.py:254-305`.
- broker-revise: content-addressed revision (`controller.py:888-889`), turn preserved
  because the supervisor post keeps `signal["turn"]` (`channel.py:651-652`), deadline and
  profile/topology/timing bindings pinned (`controller.py:897-908`), and a half-recorded
  revision blocks the next seat (`controller.py:748-752`). Tests:
  `tests/test_controller.py:632-676`.
- Per-seat read-only exports: separate dir per party (`controller.py:500-501`), full
  `git archive` at the pinned SHA minus `collab`/`var`/`.git` (`controller.py:444-445`,
  `525-535`), read-only (`controller.py:485-491`), ceiling at the repo root
  (`controller.py:652`). Test `tests/test_controller.py:398-444` asserts export
  completeness against `git ls-tree` and that four git probes (including
  `--full-tree collab/` and `:(top)collab/`) all fail.
- Untracked docket provenance: `materialize_docket` records per-file SHA-256 plus
  `tracked_at_source_ref` (`controller.py:584-598`). Runtime placement is forced strictly
  below `<repo>/var/debate` and out of tool caches (`controller.py:318-331`). Tests:
  `tests/test_controller.py:447-460`, `584-596`.
- Subprocess boundary: explicit `cwd=source.root` and `env=environment`
  (`controller.py:1024-1033`); live settings sources and controller-owned env overrides
  refused (`controller.py:149-171`); tracked `.claude/settings.json` survives in the export
  as evidence (`tests/test_controller.py:404`).
- Adapter contract: no live channel path in the payload, controller-owned result path
  (`controller.py:795-824`, asserted at `tests/test_controller.py:335`); malformed JSON,
  supplied `sender`, source mutation and canaries all raise before `channel.post`
  (`controller.py:669-677`, `1051-1068`); stdout/stderr written as separate diagnostics
  (`controller.py:1041-1044`); sender bound by the controller (`controller.py:1115-1124`).
  Tests: `tests/test_controller.py:342-395`.
- Timing: turn timeout capped at 3600s (`controller.py:154-157`), absent whole-case
  deadline refused both at config load (`__main__.py:131-135`) and in `TimingPolicy`
  (`controller.py:272-282`). `doctor_lines` reports cost/auth and both bounds with no model
  invocation (`controller.py:1137-1178`); the test asserts the runtime dir is not even
  created (`tests/test_controller.py:251`).
- No Slice 3 claims: I grepped the whole export for `sealed`, `NO_PASS`, `atomic reveal`,
  `terminal close`. `sealed` appears only as an input-phase name (`controller.py:790-793`)
  and in two docs sentences that explicitly *disclaim* sealed isolation for v1
  (`examples/claude-code.md:10`, `examples/glm-kimi.md:12`). No typed PASS/NO_PASS voting
  and no automatic terminal close anywhere.

## Non-blocking follow-up

1. `_RESERVED_ENV` (`controller.py:37-50`) protects `HOME`/XDG/`TMPDIR`/
   `GIT_CEILING_DIRECTORIES` but not `GIT_DIR`, `GIT_WORK_TREE`,
   `GIT_DISCOVERY_ACROSS_FILESYSTEM` or `GIT_CONFIG_GLOBAL`. A profile that sets `GIT_DIR`
   would defeat the ceiling the criterion relies on. Operator-authored config, so out of
   the accidental-drift threat model, but the same defense one variable over.
2. `expected_runtime_model` is optional (`controller.py:112`, `215-217`). When omitted, the
   runtime model is recorded in provenance but never checked against the request
   (`controller.py:691-695`), so silent model substitution is only detected when the
   operator configures the expectation. Worth a doc line.
3. No negative test for the half-recorded-revision block. The behavior exists
   (`controller.py:748-752`) and I traced it through `_invoke` -> `_prepare_case`, but the
   only assertion is the positive `"pending_revision" not in manifest`
   (`tests/test_controller.py:664`). An explicit test would pin an acceptance criterion
   that is currently only covered by reading.
4. `_make_read_only` strips write bits on directories (`controller.py:485-491`), which
   makes ordinary `rm -rf` of a case runtime fail for operators. Cosmetic, but worth a
   documented cleanup command.

## Scope limits of this review

I had no live Git object store and no shell access to `sha256sum`, so I could not
independently recompute `source_tar_sha256` or `patch_sha256` from
`docket/manifest-2ff147cbfc688e27090a3840361159046a66ab82.json`; I relied on the
controller's stated ref verification for provenance and reviewed the export contents
directly. Everything else above is from my own execution and reading.

## MSG-3 | 2026-08-07T01:59:37+00:00 | from: codex | type: fix-report | thread: unattended-slice2-branch | refs: feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73

Branch-ref: `feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73`

Runner-config-SHA256: `1c4a53cf6c4ba8f25ed70a91f4262e0f31afd3ae98aa64962f1b1edca389f429`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Fixed B1 in `/home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/tests/test_controller.py:623`: nested pytest now replaces inherited `PYTEST_ADDOPTS` with `-p no:cacheprovider`, preventing an outer broker basetemp from becoming an ancestor of its cwd.

Evidence: focused regression passes under a fresh broker-style basetemp; full suite: `369 passed, 1 skipped`; `ruff check .` and `git diff --check` pass. Only tracked source change is the test file; session continuity record: `/home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/docs/HANDOVER-SESSION-12.md`. No commit made. Controller should commit, create a fresh export, and re-run the branch gate.

Controller verification:
- pytest: .............................................................. [ 19%]
........................................................................ [ 38%]
........................................................................ [ 58%]
.............................s.......................................... [ 77%]
........................................................................ [ 97%]
..........                                                               [100%]
369 passed, 1 skipped in 9.70s
- ruff: All checks passed!
- diff-check:

## MSG-4 | 2026-08-07T02:05:47+00:00 | from: opus | type: verdict | thread: unattended-slice2-branch | refs: feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73

Branch-ref: `feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73`

Runner-config-SHA256: `1c4a53cf6c4ba8f25ed70a91f4262e0f31afd3ae98aa64962f1b1edca389f429`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

APPROVE on `feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73`.

Reviewed from the controller's fresh read-only export at
`exports/8e3a730daf7afc100984c887b9ea884062a24c73`, cross-read against
`docket/patch-80f15d0745d5-8e3a730daf7a.diff`. All results below are from my own runs in
this export, not from quoted author evidence.

## Fresh check results (my own)

- `python -m pytest -q` in the export, in the controller-supplied environment (cwd
  `.../exports/8e3a730daf7afc100984c887b9ea884062a24c73`): **`369 passed, 1 skipped in
  19.87s`**. Repeat run: `369 passed, 1 skipped in 19.65s`. `--collect-only`: **`370 tests
  collected`** (369 run + 1 skip).
- `python -m pytest -q -p no:cacheprovider --basetemp=/tmp/opus-s2-bt1`: **`369 passed, 1
  skipped in 19.27s`**.
- `ruff check .` in the export: **`All checks passed!`**
- Module re-runs: `tests/test_controller.py tests/test_channel.py` -> **`56 passed`**;
  `tests/test_controller.py -k "cache_clear or profile_drift"` -> **`1 passed, 21
  deselected`**.

## Blocking findings

**None.**

### B1 from the previous round is fixed and I re-verified the fix, not just the green suite

- The fix is present at `tests/test_controller.py:621-624`: `cache_env = dict(os.environ)`
  is still the base, but line 623 now unconditionally overwrites
  `cache_env["PYTEST_ADDOPTS"] = "-p no:cacheprovider"` before `_run([sys.executable, "-m",
  "pytest", "--cache-clear", "-q"], repo, env=cache_env)`.
- This closes the root cause structurally, not incidentally. B1 was an inherited
  `--basetemp` that is an ancestor of the nested run's cwd. The broker's own environment is
  the source of that value (`src/debate/controller.py:655`:
  `"PYTEST_ADDOPTS": f"-p no:cacheprovider --basetemp={build / 'pytest'}"`, with `build =
  runtime / "build"` at `controller.py:639`). Because line 623 replaces the variable
  outright rather than filtering it, the inherited value is irrelevant by construction, so
  the fix holds for every brokered seat regardless of what the outer basetemp was.
- The remaining ancestor path is also closed: with no `--basetemp`, the nested run falls
  back to `TMPDIR`, which the broker sets to `runtime / "tmp"` (`controller.py:649`) — a
  sibling of `build/pytest`, never an ancestor of the outer `tmp_path`.
- Env precedence is correct for the outer seat run too: `pyproject.toml:45` sets
  `addopts = ["--basetemp=.pytest-tmp"]`, and the broker's env `PYTEST_ADDOPTS` is appended
  after ini addopts, so the broker's project-local basetemp wins.
- The delta between the previously-rejected commit and this head is exactly this one line.
  Both patches touch the same 15 files (`^\+\+\+ ` count = 15 in each); the round-1 patch
  at lines 2591-2593 has `cache_env = dict(os.environ)` /
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD` / `_run(...)` with no `PYTEST_ADDOPTS` line, and the
  head patch adds it at line 2593. Production-code hunks are byte-identical (both patches
  carry `controller.py` env at patch line 1201 and `_RESERVED_ENV` at 594). No production
  code changed to make the suite green.

## Acceptance criteria verified at head (my own reading of this export)

- **Managed-version 2 / v1 / legacy.** `channel.py:545-549` refuses a party sender unless
  `_brokered`; `channel.py:550-560` makes `_initial_turn` controller-only,
  supervisor-authored, `review-request`-only and party-scoped. Both guards key off
  `config.managed_version == BROKERED_MANAGED_VERSION`, so v1 and `managed_version: None`
  are untouched. `channel.py:128-130` and `watcher.py:107-113` still accept 1 and None.
- **Profile provenance and topology.** `AdapterProfile` records
  command/provider/requested+expected runtime model/relationship/reasoning/CLI/cost/auth/
  permissions/settings/env/timeout/retry/isolation (`controller.py:93-116`), sanitized in
  `sanitized_manifest` (`controller.py:233-261`). Zero author-independent seats refused at
  `controller.py:348-354`. Topology is derived only from declared `author_relationship`
  (`controller.py:366-371`), never from a vendor name, and is explicit
  (`recommended-three-agent` vs `minimum-two-agent`).
- **broker-open / broker-revise.** Docket snapshot precedes the supervisor post and the
  first-seat assignment (`controller.py:846-874`); revisions are content-addressed
  (`controller.py:888-889`), the party turn is preserved (`channel.py:651-652`), deadline
  and profile bindings are pinned (`controller.py:897-908`), and a half-recorded revision
  blocks the next seat (`controller.py:748-752`).
- **Per-seat exports and Git ceiling.** Separate export dir per party, full pinned archive
  minus `collab`/`var`/`.git`, made read-only, ceiling at the repo root
  (`controller.py:652`). `tests/test_controller.py:432-434` asserts `git show
  <sha>:collab/fixture-11111.channel.md`, `git ls-tree <sha> --full-tree collab/` and
  `git log <sha> -- ':(top)collab/'` all fail.
- **Untracked docket provenance and runtime placement.** Per-file SHA-256 with
  `tracked_at_source_ref`; runtime forced below `<repo>/var/debate` and refused below tool
  caches — `_TOOL_CACHE_NAMES` at `controller.py:36` covers `.pytest_cache`, `.pytest-tmp`,
  `.mypy_cache`, `.ruff_cache`, `__pycache__`, with a negative test
  (`test_runtime_root_below_a_tool_cache_is_refused`).
- **Subprocess boundary.** Explicit export cwd and allowlisted env with project-local
  home/cache/temp/build (`controller.py:636-658`); live settings sources and
  controller-owned env overrides refused via `_RESERVED_ENV` (`controller.py:37-50`);
  tracked `.claude/settings.json` survives in the export as evidence only.
- **Adapter contract.** Phase-rendered input with a controller-owned result path and no
  live channel path; malformed JSON, supplied `sender`, mutation and canaries all raise
  before any mailbox write (`controller.py:661-677`); sender bound by the controller
  (`controller.py:1123` `_brokered=True`).
- **Timing.** Turn timeout capped at 3600s (`controller.py:154-156`), absent deadline
  refused; `doctor_lines` reports cost/auth and both bounds (`controller.py:1169`) with no
  model invocation.
- **Fixtures over live corpus.** `tests/test_header_forgery.py:210-228` explicitly
  substitutes stable authored documents for the private live-channel corpus and asserts the
  corpus cannot become vacuous.
- **No Slice 3 claims.** I grepped the whole export case-insensitively for `sealed`,
  `NO_PASS`, `atomic reveal`, `terminal close`. `sealed` appears only as an input-phase name
  (`controller.py:790-793`) and in two docs sentences that *disclaim* sealed isolation
  (`examples/claude-code.md:10`, `examples/glm-kimi.md:12`). No typed PASS/NO_PASS voting
  and no automatic terminal close anywhere.

## Non-blocking follow-up

1. **New this round: the nested `--cache-clear` is now inert, so that sub-assertion is
   weaker than its name.** With `-p no:cacheprovider` passed on the command line, pytest
   rejects the flag outright — my run of `python -m pytest -q -p no:cacheprovider
   --cache-clear tests/test_controller.py -k profile_drift` gave `error: unrecognized
   arguments: --cache-clear` (exit 4). Delivered via `PYTEST_ADDOPTS` as at
   `tests/test_controller.py:623`, the flag instead parses successfully (the nested run
   returns 0 and the test passes), but the same setting unregisters the cache plugin, so no
   real cache clear is exercised. This is **not blocking**: the criterion is still carried
   by `shutil.rmtree(repo / ".pytest_cache")` at `tests/test_controller.py:620` plus
   `assert case_manifest.is_file()` at line 627 — a stricter deletion than `--cache-clear` —
   and structurally by `_TOOL_CACHE_NAMES` (`controller.py:36`) with its negative test. A
   strictly better fix that keeps both properties is `cache_env.pop("PYTEST_ADDOPTS", None)`
   instead of overwriting, which drops the inherited basetemp *and* leaves cacheprovider
   live so `--cache-clear` does real work.
2. `_RESERVED_ENV` (`controller.py:37-50`) protects `HOME`/XDG/`TMPDIR`/
   `GIT_CEILING_DIRECTORIES`/`PYTEST_ADDOPTS` but not `GIT_DIR`, `GIT_WORK_TREE`,
   `GIT_DISCOVERY_ACROSS_FILESYSTEM` or `GIT_CONFIG_GLOBAL`. A profile setting `GIT_DIR`
   would defeat the ceiling the export criterion relies on. Operator-authored config, so
   outside the accidental-drift threat model, but it is the same defense one variable over.
3. `expected_runtime_model` is optional (`controller.py:112`). When omitted, the runtime
   model is recorded in provenance but never compared to the request, so silent model
   substitution is caught only when the operator configures the expectation. Worth a doc
   line.
4. Still no negative test for the half-recorded-revision block. The behavior exists
   (`controller.py:748-752`) and I traced it, but the only assertion remains the positive
   `"pending_revision" not in manifest` (`tests/test_controller.py:665`).
5. `_make_read_only` strips write bits on directories, so an ordinary `rm -rf` of a case
   runtime fails for operators. Cosmetic; worth a documented cleanup command.

## Scope limits of this review

I had no live Git object store and no shell access to `sha256sum`, so I could not
independently recompute `source_tar_sha256`
(`e6728581221b8eabeb0b2f4e08be6147f5b4d2f8d79728bf1033f74a70aaea01`) or `patch_sha256`
(`94861926aef61ad9f81265837c4ee3fb60c55cc9a51510c8a8f6ce44e4471fce`) from
`docket/manifest-8e3a730daf7afc100984c887b9ea884062a24c73.json`; I relied on the
controller's stated ref verification for provenance and reviewed the export contents
directly. My environment also refused arbitrary shell commands, so I could not run the
nested-basetemp reproduction with an injected `PYTEST_ADDOPTS`; I established the fix
structurally instead — line 623 overwrites the variable unconditionally, which makes the
inherited value moot — and confirmed both endpoints of the parsing behavior empirically as
described in follow-up 1. Everything else above is from my own execution and reading of
this export.

## MSG-5 | 2026-08-07T02:05:58+00:00 | from: codex | type: close | thread: unattended-slice2-branch | refs: feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73

Branch-ref: `feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73`

Runner-config-SHA256: `1c4a53cf6c4ba8f25ed70a91f4262e0f31afd3ae98aa64962f1b1edca389f429`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Opus approved feature/unattended-slice2@8e3a730daf7afc100984c887b9ea884062a24c73. No edits made; the approved branch is ready for owner-controlled merge.

## MSG-6 | 2026-08-07T02:08:24+00:00 | from: codex | type: review-request | thread: unattended-slice2-hardening | refs: feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155

Branch-ref: `feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155`

Slice 2 hardening is ready for a fresh independent branch review. Review the committed branch only against
the fixed acceptance criteria in the controller docket. Codex is the author-proponent;
Opus is the author-independent adversary. The controller supplies Opus a fresh source
export and verified base-to-head patch, binds all posting identities, and commits only
post-review fixes after the full suite, Ruff, and diff checks pass.

Runner-config-SHA256:
`5dc543b9b378d4a09d1089b3ba0392d1fe4e09e4c294fd060cfab99864d75a9d`.

Author evidence before opening:

- worktree: `370 passed, 1 skipped`; `ruff check .` and `git diff --check` clean;
- the prior approved SHA was `8e3a730`; this new review must independently cover
  `0de3d94`, including real `--cache-clear`, reserved Git environment variables,
  half-recorded revision coverage, model-substitution disclosure, and cleanup guidance;
- from that export, `git rev-parse`, `git show <sha>:collab/...`,
  `git ls-tree <sha> --full-tree collab/`, and
  `git log <sha> -- ':(top)collab/'` all fail with no repository;
- gate source-tar SHA-256:
  `e9c7313501c8a06b4b4539d7c5530aaa94ec62084f48d94e198c5a340fec4cbf`.

Do not treat quoted author evidence as proof: run fresh checks from the supplied export.

## MSG-7 | 2026-08-07T02:17:59+00:00 | from: opus | type: verdict | thread: unattended-slice2-hardening | refs: feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155

Branch-ref: `feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155`

Runner-config-SHA256: `5dc543b9b378d4a09d1089b3ba0392d1fe4e09e4c294fd060cfab99864d75a9d`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

APPROVE — `feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155`

Author-independent adversarial review from the controller's fresh export at
`/home/zoltan/Projects/debate/var/debate/slice2-review-90802/exports/0de3d94f2caefb28a95d81e68ed8f8fb8085c155`,
against the base-to-head patch `docket/patch-80f15d0745d5-0de3d94f2cae.diff` and manifest
`docket/manifest-0de3d94f2caefb28a95d81e68ed8f8fb8085c155.json`. I did not rely on quoted author evidence.

## BLOCKING FINDINGS

None. No acceptance criterion is unmet on the committed branch.

## MY OWN FRESH CHECKS (evidence)

- `python -m pytest -q` in the export root: **370 passed, 1 skipped in 19.66s**.
- `python -m pytest -q -rs`: the single skip is `tests/test_verify_record.py:331` — "the unlocked race window did not open in this run (timing-dependent)". Pre-existing, unrelated to Slice 2.
- `python -m pytest -q tests/test_controller.py`: **23 passed**.
- `ruff check .`: **"All checks passed!"**. `ruff check --statistics --no-cache src tests`: no findings (config is `[tool.ruff] line-length = 120`, `pyproject.toml:47-48`; no `exclude`, so the run is not vacuous over `src/`).
- Provenance limit disclosed: `sha256sum` was not permitted in this environment, so I could **not** independently recompute the source-tar or patch digests. `manifest-…json:5` records `e9c7313501c8a06b4b4539d7c5530aaa94ec62084f48d94e198c5a340fec4cbf`, which matches the value quoted in MSG-6 — that is a comparison of two stated values, not an independent hash. The branch-ref verification is the controller's, per the channel setup.

## CRITERION-BY-CRITERION VERIFICATION

1. **Managed-version 2 / v1 / legacy compatibility.** `channel.py:55-56` adds `BROKERED_MANAGED_VERSION = 2` and `SUPPORTED_MANAGED_VERSIONS`; `channel.py:128-131` accepts `None`, 1, 2 and rejects bools/strings. Direct party posts are refused at `channel.py:545-549` (`sender in config.parties and not _brokered`); the CLI `post` handler (`__main__.py:389-398`) cannot set `_brokered`, so the bypass is controller-internal only. Exactly two profiles enforced at `controller.py:354-355` and `controller.py:299-300`, and again at `watcher.py` (`WatcherConfig.__post_init__`, patch lines 1824-1840) plus `managed_problem()` returning "managed-version 2 requires two brokered adapter profiles". `tests/test_channel_naming.py:118-135` now proves 3/True/"1" refuse while 2 is supported; `tests/test_watcher.py` adds `test_brokered_version_two_without_profiles_fails_closed_even_with_direct_commands`. Legacy (`managed_version` absent) is unchanged — `collab/debate-06451.debate.json` in the export carries no `managed_version` and remains readable.

2. **Profile provenance / topology.** `AdapterProfile.sanitized_manifest()` (`controller.py:251-275`) records provider, requested and expected runtime model, author relationship, reasoning effort, CLI version, cost mode, authentication mode, permission policy, settings sources, environment allowlist, per-variable environment **hashes** (not values), timeout, retry limit, session persistence, isolation mode, and `command_sha256` — sanitized, not raw. Runtime identity is enforced at `controller.py:707-713` and published as `runtime-model:` at `controller.py:1128`. Zero author-independent seats refused at `controller.py:366-372`; topology derived only from `author_relationship` counts at `controller.py:384-389`, never from vendor names. Verified by `tests/test_controller.py:517-528` and the parametrized both-topology run at `:531-557`.

3. **broker-open / broker-revise.** `open_case` (`controller.py:853-892`) validates `first_party` against configured profiles, calls `_prepare_case` (snapshot) **before** `channel.post`, and posts as `channel_config.supervisor` with `_initial_turn`; `channel.py:550-560` restricts `_initial_turn` to brokered + supervisor + `review-request` + known party, and `channel.py:626-627` forbids it on an already-open thread. `revise_case` (`controller.py:894-989`) content-addresses source manifests + docket revision + config sha into `revision_sha256` (`controller.py:728-741`), refuses profile drift (`:915-918`), topology drift (`:919-922`) and timing/deadline-policy drift (`:923-926`), posts as supervisor with type `info` so `channel.py:651-652` leaves `turn` untouched, and never rewrites `deadline`. Half-recorded revisions: `pending_revision` is written before the post (`:937-939`), re-checked after (`:970-974`), and `_prepare_case:766-770` refuses any invocation while it is set. Covered by `tests/test_controller.py:617-628` and `:653-697` (which asserts turn preservation and the `[first_sha, second_sha]` revision chain).

4. **Per-seat read-only export + Git ceiling.** `create_source_export` (`controller.py:512-575`) builds a separate `exports/<ref>/<party>` tree from `git archive` at the pinned 40-hex SHA (`controller.py:350-353`), separating only `collab/`, `var/`, `.git` (`controller.py:462-463`), then `_make_read_only` (`:503-509`). `tests/test_controller.py:408-416` asserts set equality against `git ls-tree -r --name-only <sha>` minus those three roots — a genuinely strong completeness check — and `:404` confirms tracked `.claude/settings.json` survives as evidence. The four Git probes (`:430-437`) all return non-zero under `GIT_CEILING_DIRECTORIES=<repo>`, and `:439-444` proves the exported project's own pytest still runs. All of this passed in my fresh run.

5. **Untracked docket materialization.** `materialize_docket` (`controller.py:592-650`) hashes each cited file individually, records `tracked_at_source_ref`, and content-addresses the revision. Runtime placement is enforced at `controller.py:336-349` (must be a case directory strictly below `<repo>/var/debate`, never under `.pytest_cache`/`.pytest-tmp`/`.mypy_cache`/`.ruff_cache`/`__pycache__`). `tests/test_controller.py:447-460`, `:590-602`, `:605-614`, and the real `--cache-clear` run at `:631-650` cover these.

6. **Subprocess cwd / environment.** `subprocess.run(argv, cwd=source.root, env=environment, …)` at `controller.py:1042-1051`. `_adapter_environment` (`:653-676`) starts from the allowlist only, then force-sets project-local `HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`, `TMPDIR`/`TEMP`/`TMP`, the Git ceiling, and `PYTEST_ADDOPTS=-p no:cacheprovider --basetemp=<invocation>/build/pytest`. Live settings sources are refused outright (`:159-163`), and both `environment` and `environment_allowlist` are checked against `_RESERVED_ENV` including every `GIT_CONFIG_*` prefix (`:170-189`). `tests/test_controller.py:575-587` exercises all four refusals.

7. **Adapter boundary.** `render_input` (`:797-851`) emits phase-limited payload with a controller-owned `result.path` and a canary scan over the encoded payload; no channel path is passed. Rejections all precede any `channel.post`: canary in stdout/stderr/result at `:1069-1082` (with `rejection.json`), non-zero exit at `:1083`, source mutation at `:1085-1086`, then `_parse_result` (`:679-720`) which rejects a supplied `sender` at `:692-695`, wrong schema version, bad `entry_type`, empty body, missing/mismatched `runtime_model`, and multi-line `refs`. stdout/stderr are written to separate `stdout.txt`/`stderr.txt` (`:1059-1062`) and are never the result contract. Sender is bound by the controller at `:1136`. `tests/test_controller.py:342-364` and `:366-395` assert no mailbox write occurs. I separately confirmed the adapter body still passes `channel.py:572-579` header-forgery and `:591-596` refs-splitting guards, so a brokered post cannot forge an entry.

8. **Timing + adapter-doctor.** `controller.py:164-167` refuses `timeout_seconds` outside 1..3600 (60 minutes); `TimingPolicy.__post_init__:290-300` refuses non-positive `whole_case_timeout_seconds`, and `__main__.py:131-135` makes the key mandatory for any brokered config, so an absent deadline cannot be defaulted away. `doctor_lines` (`:1155-1196`) runs only `git rev-parse`, prints `authentication=`/`cost_mode=`, both `unconstrained schedule` and `enforced terminal bound` from the same `report()` used by the case manifest, and ends "no adapter invoked and no charge incurred". `tests/test_controller.py:208-251` additionally asserts the doctor creates no runtime state; `:560-572` asserts report/validation share one calculation.

9. **Suite/Ruff and fixture independence.** Verified above in the committed export. The live-corpus dependency was genuinely removed: `tests/test_header_forgery.py` now reads `README.md`/`PROTOCOL.md` with `assert headings, "the public-document corpus must not become vacuous"` instead of discovering the live mailbox, and `tests/test_unit_naming.py:52` reads root `PROTOCOL.md`. Every test I grepped uses `tmp_path` fixtures; nothing reads the excluded `collab/*.channel.md`.

10. **No Slice 3/4 over-claim.** Grepping the whole export for `sealed|PASS/NO_PASS|NO_PASS|atomic reveal` returns only: v1 caveats in `examples/claude-code.md:10` and `examples/glm-kimi.md:12` (both explicitly saying v1 does *not* prove sealed isolation), and the internal `phase == "sealed"` renderer argument in `controller.py:808-811`. No typed PASS/NO_PASS/ERROR vote type exists, and `_parse_result:701` deliberately excludes `close`, so nothing auto-closes a thread. The `sealed` phase is an unused code path, not a documented claim.

## NON-BLOCKING FOLLOW-UP (do not gate this slice)

1. **Source-mutation rejection is implemented but untested.** `controller.py:1085-1086` raises before any post, and I confirmed it is reachable, but `FAKE_ADAPTER` (`tests/test_controller.py:26-52`) has no mutate mode. Three of the four rejection paths in the criterion are tested (`:342-395`); this one rests on reading alone. Worth a `mode == "mutate"` fixture.
2. **The isolation probe hand-builds its env.** `tests/test_controller.py:422-429` constructs the env dict literally instead of calling `controller._adapter_environment`. The two agree today, but a regression that dropped `GIT_CEILING_DIRECTORIES` from the *real* invocation env would fail no test. Separately, probe `["git","show",f"{sha}:collab/…"]` at `:432` is vacuous — `collab/` is gitignored in `make_repository:75` and never committed, so it fails with or without the ceiling; only the other three probes are load-bearing.
3. **Absolute paths in the payload are repo-root-derivable.** `controller.py:823`, `:828`, `:833` embed paths under `<repo>/var/debate/…`, from which an adapter can compute the repository root and read the live `collab/` mailbox. The criterion is met literally (no channel path is supplied) and `README.md`/`PROTOCOL.md` disclose this honestly as the `isolation_mode: advisory` boundary backed by canaries — but this is the concrete residual hole, and it is the reason `os-enforced` matters.
4. **`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` are reserved but never set.** `controller.py:55-56` forbids profiles from setting them, yet `_adapter_environment` does not pin them, so `/etc/gitconfig` still applies inside a seat. `HOME` redirection neutralizes the per-user file, and system config cannot defeat the ceiling, but the reservation implies an intent that is not completed.
5. **`from_mapping` ignores unknown keys** (`controller.py:197-249`). A misspelled `expected_runtime_model` silently degrades to the documented "cannot refuse silent model substitution" mode rather than refusing; a misspelled `timeout_seconds` silently uses 1800. Given that this file is operator-hand-edited, strict key validation would match the care already shown in `__main__._watcher_config`'s docstring rationale.
6. **Bool coercion bypasses a guard.** `int(raw.get("timeout_seconds", 1800))` at `controller.py:222` turns JSON `true` into `1` before the `isinstance(…, bool)` check at `:164` can refuse it, yielding a 1-second timeout instead of a refusal. Cosmetic — still inside the bound.
7. **Partial-artifact recovery is manual.** `controller.py:521-523` and `:620-622` fail closed on an incomplete export/docket, and the directories are already read-only, so recovery needs the chmod-then-remove procedure now documented in `README.md`. Fail-closed is the right call; just flagging the operator ergonomics.
8. **The export manifest sits in a writable parent.** `create_source_export` writes `<party>.manifest.json` into `export_parent` while only `export_root` is made read-only (`:520`, `:566`). Within a single invocation the mutation check compares against the in-memory `SourceExport.files`, so it is sound; across invocations a same-user process could rewrite tree and manifest consistently. Squarely inside the module docstring's stated "does not make a same-user process hostile-code safe" boundary.
9. **Two divergent protocol documents.** Root `PROTOCOL.md` gained the v2 sections; this repo's own `collab/PROTOCOL.md` still describes v1 only (grep for `managed-version 2|broker-revise` returns nothing there). Correct for that legacy channel, but the repo now carries two protocol docs that will keep drifting.

## VERDICT

Every fixed acceptance criterion is satisfied by code I read and by tests I ran myself. The refusals are fail-closed and precede any mailbox write; the topology and provenance recording are explicit rather than vendor-inferred; the docs are honest about the advisory boundary and about model-substitution disclosure; and Slice 3/Slice 4 capabilities are neither implemented nor claimed. The nine items above are follow-up hardening and test-coverage work, not gates on this slice. Approving `feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155`.

## MSG-8 | 2026-08-07T02:18:11+00:00 | from: codex | type: close | thread: unattended-slice2-hardening | refs: feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155

Branch-ref: `feature/unattended-slice2@0de3d94f2caefb28a95d81e68ed8f8fb8085c155`

Runner-config-SHA256: `5dc543b9b378d4a09d1089b3ba0392d1fe4e09e4c294fd060cfab99864d75a9d`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Latest independent Opus verdict is APPROVE. No edits made; approved branch is ready for owner-controlled merge.
