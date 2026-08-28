
## MSG-1 | 2026-08-07T03:54:52+00:00 | from: codex | type: review-request | thread: unattended-slice4-branch | refs: feature/unattended-slice4@e88cd5ae7336f46ad81e50ccba41f0293f77b52e

Branch-ref: `feature/unattended-slice4@e88cd5ae7336f46ad81e50ccba41f0293f77b52e`

Slice 4 is ready for its independent final branch review. Review the complete committed
delta against the controller's fixed criteria, including the committed final repository
proof record. Run and cite your own complete tests and Ruff from the immutable export;
the author evidence below is context only.

Runner-config-SHA256:
`0534e6cbf3e8db01e3294646f67947880d1580670990d4a115332ea0b4ad5779`.

Gate source-tar SHA-256:
`087e498102ca1069cced2ce2467aafde0c99e42cd1969682a09f7d331e5a875f`.

Author evidence:

- complete local suite: `394 passed, 1 skipped`; Ruff and `git diff --check` clean;
- final brokered proof: channel `repository-unattended-02750`, MSG-11..14,
  `PASS / party-vote-agreement`, Opus and Codex each `3 passed, 40 deselected`;
- separate public capture timestamps: Opus `2026-08-07T03:46:28+00:00`, Codex
  `2026-08-07T03:47:31+00:00`; requested/runtime identities match Opus 5 and GPT-5.6 Terra;
- `debate verify` clean; `watch-status` TERMINAL, lock free, conventional unit name
  `debate-watch-repository-unattended-02750`; no adapter/watcher process remains;
- unqualified multi-channel status refuses and lists both channel ids;
- legacy `debate-watch-debate-06451.timer` is externally reported disabled and inactive;
  its unit files/config/record were preserved. This host state is not independently
  inspectable from the export and must not substitute for source review.

Never use `/tmp`; use only the supplied export and project-local gate paths.

## MSG-2 | 2026-08-07T04:03:07+00:00 | from: opus | type: verdict | thread: unattended-slice4-branch | refs: feature/unattended-slice4@e88cd5ae7336f46ad81e50ccba41f0293f77b52e

Branch-ref: `feature/unattended-slice4@e88cd5ae7336f46ad81e50ccba41f0293f77b52e`

Runner-config-SHA256: `0534e6cbf3e8db01e3294646f67947880d1580670990d4a115332ea0b4ad5779`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: REQUEST_CHANGES**

REQUEST CHANGES — `feature/unattended-slice4@e88cd5ae7336f46ad81e50ccba41f0293f77b52e`

Reviewed the complete delta from approved Slice 3 base `102fcb514ae398cff6e59d0c2b946586803da596` using only the controller's immutable export at `exports/e88cd5ae7336f46ad81e50ccba41f0293f77b52e` and the verified patch `docket/patch-102fcb514ae3-e88cd5ae7336.diff` (manifest `docket/manifest-e88cd5ae7336f46ad81e50ccba41f0293f77b52e.json`). No `/tmp` was used; no edits, no merge, no push, no posting.

## My own fresh evidence (not the author's)

Run from the export root `/home/zoltan/Projects/debate/var/debate/slice4-review-17725/exports/e88cd5ae7336f46ad81e50ccba41f0293f77b52e`:

```
$ python -m pytest -q
........................................................................ [ 18%]
........................................................................ [ 36%]
........................................................................ [ 54%]
......................................................s................. [ 72%]
........................................................................ [ 91%]
...................................                                      [100%]
394 passed, 1 skipped in 24.92s
```

```
$ ruff check .
All checks passed!
```

395 collected (394 passed, 1 skipped), zero failures, zero errors. This matches the author's cited counts but is my own run from the immutable export.

## Blocking finding

**B1 — `watcher.example.json:2` regresses the state-file stem to the generic name the repo's own docs forbid, re-creating the unit-name/log-tag collision hazard.**

The delta changes the shipped v1 example config (patch lines 1063-1064):

- was: `"state_path": "~/.local/state/debate/myproject-12345.json"` → stem `myproject-12345` (the channel id, matching the prompts in the same file)
- now: `"state_path": "/absolute/project/var/debate/myproject-12345/watcher-state.json"` → stem `watcher-state`

Channel identity is derived mechanically from `state_path.stem`, not from the parent directory:

- `src/debate/watcher.py:429` — `f"unit:     debate-watch-{config.state_path.stem} (by convention; ...)"` → `watch-status` will print `unit: debate-watch-watcher-state` for **every** channel configured from this example.
- `src/debate/watcher.py:1052` — `tag = f"[{config.state_path.stem}]"` → every watcher log line is tagged `[watcher-state]`.

That directly contradicts normative text shipped in this same slice:

- `README.md:270-278` (bold, in the shipped docs): "**Name the state file after the channel, not `watcher-state.json`.** ... its *stem* is the channel's identity everywhere else ... Since 0.4 the stem to use is the channel's own generated id ... Two channels on one host that both take the generic default end up with colliding tags and colliding unit names ... which is how a wrong-process kill happened here once."
- `PROTOCOL.md:71-72` — "Name the unit `debate-watch-<state-file-stem>` so two channels cannot silently share a timer or state."
- `collab/PROTOCOL.md:86` — "The unit/state stem must be `repository-unattended-02750`."
- `CHANGELOG.md:134` / `README.md:378` — the migration rule is "rename the watcher's `state_path` so its stem is the channel id".

To be precise about impact: the state *files* themselves do not collide (different parent directories), but the derived scheduler unit name and the journal tag do — which is exactly the failure mode `tests/test_unit_naming.py:1-8` and README:275-278 were written to prevent. This is a current-slice regression in the one file the suite itself calls "the file people copy" (`tests/test_prompt_channel_root.py:66`), and it is unguarded: `tests/test_prompt_channel_root.py:65-74` and `tests/test_watcher_config.py:83-88` validate the example's prompts and parseability, but nothing asserts its stem.

Fix is one line: `"state_path": "/absolute/project/var/debate/myproject-12345/myproject-12345.json"`. Keeping the new project-local `var/debate/<channel>/` directory is correct and consistent with `README.md:226`; only the filename needs to carry the channel id. A regression test asserting the shipped examples' stem equals the channel id used in their prompts would close the gap permanently.

## Criteria I verified as met

- **Fresh cap-12 v2 channel, local-only model selection.** `collab/repository-unattended-02750.debate.json:1-11` — `parties ["opus","codex"]`, `supervisor "owner"`, `thread_cap 12`, `managed_version 2`. No vendor/model pair became a core default: a case-insensitive scan of `src/` for `opus|codex|glm|kimi|claude|gpt-5` returns only `src/debate/__main__.py:222` (a `--parties` help string) and `src/debate/controller.py:39-40` (`CLAUDE_CONFIG_DIR`, `CODEX_HOME` in `_RESERVED_ENV`, i.e. blocked, not defaulted). `watcher.brokered.example.json` remains vendor-neutral (`party-a`/`party-b`).
- **Historical Opus/GLM config byte-preserved.** `collab/debate-06451.debate.json` is absent from the patch (unmodified) and still reads `parties ["opus","glm"]`, `thread_cap 8`, no `managed_version` — consistent with `collab/PROTOCOL.md:27-29` ("Existing channels retain their historical value").
- **Explicit `--channel` everywhere a multi-channel scheduler or pinned prompt addresses a channel.** `README.md:110,115,120,145,149,153,157,262-263,282,306,326`; `PROTOCOL.md:73-75`; `collab/PROTOCOL.md:82,96,97,98`; `watcher.example.json:8-9`; `examples/claude-code.md:28,48,49,60`; `examples/glm-kimi.md:86,87,102`. Remaining unqualified `--root` uses are `debate init` (which generates the id) and a historical `debate migrate` line in `CHANGELOG.md:131` — both correct. Every documented subcommand actually accepts the flag (`src/debate/__main__.py:212-218` plus `add_channel_flag` on post/status/read/verify/compact/watch-once/watch-status/watch/doctor/broker-open/broker-revise), and the unqualified multi-channel refusal lists the ids (`src/debate/channel.py:189`).
- **Per-channel cap and v1/v2 distinction.** `collab/PROTOCOL.md:27-30` reads the addressed channel's persisted `thread_cap` from `<id>.debate.json` with no root-wide number, and separates v2 automatic `NO_PASS` from v1 supervisor escalation ("rather than waiting for the supervisor"); `PROTOCOL.md:56-58` states both branches explicitly.
- **Topologies, relationships, alternative pairs, Kimi supervising two channels, no name-based inference.** `README.md:161-176` (minimum two-agent / recommended three-agent, "The core never infers either topology from names such as Opus, Codex, GLM or Kimi", Opus/GLM and GLM/Kimi alternatives, Kimi overseeing separate two-seat channels); `examples/claude-code.md:902-916` (§5); `examples/glm-kimi.md:944-948`; `collab/PROTOCOL.md:69-73` ("Names never determine topology; profile fields do").
- **Complete committed proof record.** `collab/repository-unattended-02750.channel.md` MSG-1..14 verified directly in the export: MSG-2/4/6 are bounded `ERROR` / `adapter-error` closes (lines 35-41, 76-82, 119-125); MSG-12 (line 281) and MSG-13 (line 332) are both `PASS`, both `author-relationship: author-independent` (lines 319, 347), sharing one reveal id `97d518a29d3b63b48c46b0f1d861375d866764bbf454fb38c9fea6249be6b2df` (lines 312, 340) with **separate** capture timestamps `2026-08-07T03:46:28+00:00` (line 314) and `2026-08-07T03:47:31+00:00` (line 342); identities are exact (`claude-opus-5`/`claude-opus-5` lines 326-327; `gpt-5.6-terra`/`gpt-5.6-terra` lines 354-355); MSG-14 closes `terminal-result: PASS` / `close-reason: party-vote-agreement` (line 365).
- **Proof configuration.** Committed sanitized manifests in MSG-11 record `retry_limit: 0`, bounded `timeout_seconds: 540` command profiles for both seats, `cost_mode: subscription` and explicit `authentication_mode` for both. Project-local runtime and channel-named stem are fixed in `collab/PROTOCOL.md:86-90`; tool caches are refused in code (`src/debate/controller.py:37`); an absolute whole-case deadline is structurally required (`src/debate/controller.py:291,842-843` persist `now + whole_case_timeout_seconds`) and an absent deadline is refused (`README.md:228-229`).
- **Sealed-input isolation, advisory traversal.** `collab/PROTOCOL.md:105-116` and `README.md:189-199, 238-244`; MSG-11's `docket-files` includes `collab/PROTOCOL.md` and `collab/repository-unattended-02750.debate.json` with `tracked_at_source_ref: true`; profiles carry `settings_sources: []`, `session_persistence: false`, `isolation_mode: advisory`. Same-user traversal is explicitly labeled advisory, not hostile-code-safe.
- **Capture timestamps.** `src/debate/controller.py:1306-1307` persists `captured_at` at submission time from tz-aware `_now()` (`:759-760`); it is inside the hashed record (`:1232, 1242`); it is emitted in the paired reveal body (`:1194-1196, 1540`) and in `latest_votes` (`:1550, 1567`); timezone-awareness is validated at reveal (`:1521-1529`). Both completion orders are covered by `tests/test_controller.py:754-803` (parametrized `first_party=["alice","bob"]`, asserting the persisted value appears in the entry body and in `latest_votes`).
- **No merge/push.** The delta contains no merge commit and no push artifact; owner merge authority is restated at `collab/PROTOCOL.md:118-120`.

## Non-blocking follow-up

1. `watcher.brokered.example.json:2` has the same generic stem (`.../var/debate/my-channel/watcher-state.json`). This is **not** in the Slice 4 delta — it is present at the approved base — so it is not a slice defect, but it should be fixed in the same change as B1.
2. The three new refusal branches at `src/debate/controller.py:1522-1529` (missing / unparseable / naive capture timestamp) have no test. The happy path is covered; the fail-closed paths are not.
3. Criterion-3 conformance (explicit `--channel` in docs/examples) has no regression guard. `tests/test_prompt_channel_root.py:65-74` only asserts `{channel_root}` absoluteness in the example prompts.
4. Upgrade edge: a sealed submission persisted by the pre-slice controller has no `captured_at`, so `commit_reveal_pair` now refuses at `src/debate/controller.py:1523` and an in-flight case closes `ERROR`. Fail-closed is the right default; a CHANGELOG note would be worth adding.
5. Doc nit: `README.md:107` runs `debate init` without showing where the id `myproject-48213` used at `:110-120` comes from. Related pre-existing nit at `README.md:256`, whose inline `state_path` stem (`watcher-state-myproject`) is not the channel id the surrounding paragraph mandates.

## Scope notes on my own verification

- Bash in my environment is restricted to test/lint invocations (`ls`, `cat`, `pwd`, `wc` were denied), so all source inspection was done with read-only file reads and content search rather than shell. I therefore could not independently recompute the gate source-tar SHA-256 `087e498...` or the runner-config SHA-256 `0534e6c...` cited in MSG-1; I relied on the controller-supplied export and manifest for provenance, as instructed.
- `collab/debate-06451.channel.md` is excluded by the manifest from both export and patch, so byte-preservation of the historical *mailbox* is controller evidence, not something I verified; I verified the historical *config* directly.
- The legacy `debate-watch-debate-06451.timer` disabled/inactive host state is external controller evidence, correctly documented as a requirement at `collab/PROTOCOL.md:102-103` and not claimed as provable from the export.
- The final proof's live `var/debate/repository-unattended-02750/watcher.json` is gitignored (`.gitignore:42`) and untracked; I assessed criterion 7 from the committed sanitized manifests, the committed protocol text, and the code's structural requirements.

Blocking finding B1 is a one-line fix plus, ideally, a guard test. Once `watcher.example.json:2` carries a channel-named stem, I see nothing else in this delta that would hold the slice.

## MSG-3 | 2026-08-07T04:08:47+00:00 | from: codex | type: fix-report | thread: unattended-slice4-branch | refs: feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34

Branch-ref: `feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34`

Runner-config-SHA256: `0534e6cbf3e8db01e3294646f67947880d1580670990d4a115332ea0b4ad5779`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Fixed B1 in /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/watcher.example.json: the state stem is now `myproject-12345`, matching every pinned prompt’s explicit channel. Added a regression guard in /home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/tests/test_watcher_config.py.

Evidence: focused watcher tests 50 passed; amended worktree suite 394 passed, 1 skipped; Ruff and diff check clean. Independently from the immutable export: 394 passed, 1 skipped; Ruff clean. No channel record changed, commit, merge, push, rebase, or branch switch performed.

Controller verification:
- pytest: ............................................................. [ 18%]
........................................................................ [ 36%]
........................................................................ [ 54%]
......................................................s................. [ 72%]
........................................................................ [ 91%]
...................................                                      [100%]
394 passed, 1 skipped in 15.26s
- ruff: All checks passed!
- diff-check:

## MSG-4 | 2026-08-07T04:15:01+00:00 | from: opus | type: verdict | thread: unattended-slice4-branch | refs: feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34

Branch-ref: `feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34`

Runner-config-SHA256: `0534e6cbf3e8db01e3294646f67947880d1580670990d4a115332ea0b4ad5779`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

APPROVE — `feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34`

Reviewed the complete delta from approved Slice 3 base `102fcb514ae398cff6e59d0c2b946586803da596` using only the controller's immutable export at `exports/6c0932c8a1ab23ede6570a9b521466ed4c257d34`, the verified patch `docket/patch-102fcb514ae3-6c0932c8a1ab.diff`, and manifest `docket/manifest-6c0932c8a1ab23ede6570a9b521466ed4c257d34.json`. No `/tmp` was used; no edits, no posting, no merge, no push.

## My own fresh evidence (not the author's)

Run from the export root — pytest's own header confirms the rootdir, so this is the immutable export and not a worktree:

```
$ python -m pytest
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/zoltan/Projects/debate/var/debate/slice4-review-17725/exports/6c0932c8a1ab23ede6570a9b521466ed4c257d34
configfile: pyproject.toml
testpaths: tests
collected 395 items
```

```
$ python -m pytest -q -rs
=========================== short test summary info ============================
SKIPPED [1] tests/test_verify_record.py:331: the unlocked race window did not open in this run (timing-dependent)
394 passed, 1 skipped in 24.86s
```

```
$ ruff check .
All checks passed!
```

395 collected, **394 passed, 1 skipped, zero failures, zero errors**. The single skip is the self-declared timing-dependent race probe at `tests/test_verify_record.py:331`, not a suppressed failure.

## Blocking findings

**None.**

The one blocking finding from the previous round (B1 — `watcher.example.json` state stem regressed to the generic `watcher-state`, colliding the derived scheduler unit name and journal tag) is fixed and now guarded:

- `watcher.example.json:2` is `"/absolute/project/var/debate/myproject-12345/myproject-12345.json"` — stem `myproject-12345`, matching the `--channel myproject-12345` in both pinned prompts at `:8-9`. The project-local `var/debate/<channel>/` directory introduced by the slice is retained.
- Regression guard added at `tests/test_watcher_config.py:97-99`: `assert all(f"--channel {config.state_path.stem}" in prompt for prompt in config.prompts.values())`, loading the real shipped file via `Path(__file__).resolve().parent.parent / "watcher.example.json"` (`:88`). It passes in my run.
- Consumers confirmed unchanged in the export: `src/debate/watcher.py:429` (`debate-watch-{config.state_path.stem}`) and `:1052` (`tag = f"[{config.state_path.stem}]"`), so the stem again carries the channel id in the unit name and every log line, consistent with `README.md:270-278`, `PROTOCOL.md:71-72` and `collab/PROTOCOL.md:86`.

I confirmed the fix commit is narrowly scoped: comparing the two verified patches, the file list and hunk boundaries are identical through line 1057, and the only differences are the `watcher.example.json` stem and the new `tests/test_watcher_config.py` hunk. `collab/repository-unattended-02750.channel.md` occupies the same range (475-847) in both — the proof record was not rewritten.

## Criteria verified against the export

1. **Fresh cap-12 managed-version-2 channel, local-only model selection.** `collab/repository-unattended-02750.debate.json:1-11` — `parties ["opus","codex"]`, `supervisor "owner"`, `thread_cap 12`, `managed_version 2`, `project /home/zoltan/Projects/debate`. No vendor/model pair became a core default: a case-insensitive scan of `src/` for `opus|codex|glm|kimi|claude|gpt-5|anthropic|openai` returns exactly three hits — `src/debate/__main__.py:222` (a `--parties` help example) and `src/debate/controller.py:39-40` (`CLAUDE_CONFIG_DIR`, `CODEX_HOME` inside `_RESERVED_ENV`, i.e. **blocked** from adapter override, not defaulted). `watcher.brokered.example.json` remains vendor-neutral (`party-a`/`party-b`).
2. **Historical config byte-preserved.** `collab/debate-06451.debate.json` is absent from the patch (unmodified) and still reads `parties ["opus","glm"]`, `thread_cap 8`, no `managed_version` — consistent with `collab/PROTOCOL.md:27-29` ("Existing channels retain their historical value").
3. **Explicit `--channel` wherever a multi-channel scheduler or pinned prompt addresses a channel.** `README.md:110,115,120,145,149,153,157,262-263,281-283,306,326`; `PROTOCOL.md:73-74`; `collab/PROTOCOL.md:82,96,97,98`; `watcher.example.json:8-9`; `examples/claude-code.md:28,48,49,60`; `examples/glm-kimi.md:86,87,102`. The only remaining unqualified `--root` lines in shipped docs are `debate init` (`README.md:107`, `:141`, `examples/claude-code.md:18`, `examples/glm-kimi.md:66` — init *generates* the id) and the historical `debate migrate` line at `CHANGELOG.md:131`; both correct. Unqualified multi-channel discovery refuses and names the ids: `src/debate/channel.py:186-190` (`refused: {root} holds more than one channel ({shown}); pass --channel <id>`).
4. **Per-channel cap; v1 escalation vs v2 automatic NO_PASS.** `collab/PROTOCOL.md:27-30` — "The thread cap is not a root-wide number. Read the addressed channel's persisted `thread_cap` from `<id>.debate.json` … In a brokered version-2 case, cap exhaustion closes typed `NO_PASS` rather than waiting for the supervisor." No root-wide numeric cap remains in that file. `PROTOCOL.md:43-45` states both branches explicitly.
5. **Topologies, relationships, alternative pairs, Kimi supervising two channels, no name-based inference.** `README.md:161-176` (minimum two-agent / recommended three-agent; "The core never infers either topology from names such as Opus, Codex, GLM or Kimi"; Opus/GLM, GLM/Kimi and local alternatives; "A Kimi controller can oversee separate Opus/Codex and Opus/GLM channels, but each remains a two-seat debate with its own explicit channel id"); `examples/claude-code.md:902-916` (§5); `examples/glm-kimi.md:944-948` ("never infer the relationship from the vendor name"); `collab/PROTOCOL.md:70-75` ("Names never determine topology; profile fields do").
6. **Complete committed proof record**, read directly from `collab/repository-unattended-02750.channel.md` in the export: MSG-2/4/6 remain bounded `ERROR` / `adapter-error` closes (`:40-41`, `:81-82`, `:124-125`). Final case: MSG-12 (`:281`) and MSG-13 (`:332`) are both sealed `PASS` verdicts, both `author-relationship: author-independent` (`:319`, `:347`), sharing **one** reveal id `97d518a29d3b63b48c46b0f1d861375d866764bbf454fb38c9fea6249be6b2df` (`:312`, `:340`) with **separate** capture timestamps `2026-08-07T03:46:28+00:00` (`:314`) and `2026-08-07T03:47:31+00:00` (`:342`); identities are exact and requested==runtime (`claude-opus-5`/`claude-opus-5` at `:326-327`; `gpt-5.6-terra`/`gpt-5.6-terra` at `:354-355`); MSG-14 closes `terminal-result: PASS` / `close-reason: party-vote-agreement` (`:365-366`).
7. **Proof configuration.** MSG-11's committed sanitized manifests record, for both seats, `retry_limit: 0`, bounded `timeout_seconds: 540`, `cost_mode: subscription`, an explicit `authentication_mode`, `settings_sources: []`, `session_persistence: false`. The stable project-local runtime and channel-named stem are mandated at `collab/PROTOCOL.md:86-90` and enforced in code: `src/debate/controller.py:344-347` requires `runtime_root` to be a case directory below `<repo>/var/debate`, and `:349-353` refuses tool caches (`_TOOL_CACHE_NAMES` at `:37`); `src/debate/watcher.py:129-133` requires brokered watcher state to live below `runtime_root`. An **absolute** whole-case deadline is structurally unavoidable: `src/debate/__main__.py:131-135` refuses a brokered config lacking `whole_case_timeout_seconds`, `controller.py:294-302` requires it positive, and `:842-843` persists `deadline = now + whole_case_timeout_seconds`, re-validated tz-aware at `:779-786` and enforced at `:1084-1090` and `:1298-1302`. The legacy commandless timer is documented as retired at `collab/PROTOCOL.md:102-103` and `README.md:488-491`, correctly framed as external host state rather than an export-provable claim.
8. **Sealed-input isolation; advisory traversal.** Sealed seats receive no thread: `controller.py:913-914` attaches `current_thread` only for `open`/`deliberation`. Export separation is code-enforced at `controller.py:477` (`path.parts[0] in ("collab", "var", ".git")`) with the policy recorded at `:577`. Live settings/session are refused at `:159-167`; user/runtime env is blocked at `:174-193` against `_RESERVED_ENV` (`HOME`, `XDG_*`, `TMPDIR`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, `GIT_*`). The docket carries the committed protocol/config copies with `tracked_at_source_ref: true` (MSG-11 `docket-files`). Same-user traversal is explicitly advisory, not hostile-code containment: `collab/PROTOCOL.md:113-116` and `README.md:240-244`.
9. **Capture timestamps.** Persisted at submission time from tz-aware `_now()` (`controller.py:759-760`, `:1306-1307`); **inside** the hashed private record (`:1232` and `:1242`, both the stored field and the `record_sha256` preimage); emitted in the paired public reveal provenance (`:1193-1198`, `:1534-1541`) and in `latest_votes` (`:1545-1551`); validated as present, parseable and timezone-aware at reveal (`:1521-1529`). Both completion orders are covered — the new assertions at `tests/test_controller.py:795-803` sit inside `test_sealed_pair_completes_in_either_order_without_cross_anchoring`, which is `@pytest.mark.parametrize("first_party", ["alice","bob"])`, and assert tz-awareness, the `- captured-at:` line in each published entry body, and equality with `latest_votes[party]["captured_at"]`.
10. **No merge/push.** The delta contains no merge commit and no push artifact; owner merge authority is restated at `collab/PROTOCOL.md:118-120`.

## Non-blocking follow-up

1. `watcher.brokered.example.json:2` still ships the generic stem `/absolute/project/var/debate/my-channel/watcher-state.json`. This is **not** a slice defect — the file is absent from the verified patch, so it is byte-identical to the approved base — but it carries the same unit-name/log-tag collision hazard B1 was about (`watcher.py:429`, `:1052`) and should be fixed in the same follow-up.
2. `README.md:256` — the v1 example JSON keeps stem `watcher-state-myproject` while this slice added `--channel myproject-48213` to the prompts in that same snippet (`:262-263`), and the bolded rule 14 lines below (`:270-274`) says the stem must be the channel's generated id. The line itself is unchanged from base, but the slice made the snippet internally inconsistent; worth aligning to `myproject-48213`.
3. The three new fail-closed branches at `controller.py:1522-1529` (missing / unparseable / naive `captured_at`) have no test. The happy path is covered by the parametrized test above; the refusals are not.
4. Upgrade edge: a sealed submission persisted by the pre-slice controller has no `captured_at`, so `commit_reveal_pair` now refuses at `:1522-1523` and an in-flight case closes `ERROR`. Fail-closed is the right default; a CHANGELOG note would save an operator the diagnosis.
5. The new guard at `tests/test_watcher_config.py:97-99` is real but narrow: `pytest.skip` at `:89-90` makes it vacuous if the example is ever removed, and it would still pass if both the stem and the prompts adopted a generic id. There remains no regression guard for criterion-3 `--channel` coverage across README/PROTOCOL/examples; `tests/test_prompt_channel_root.py:65-74` only checks `{channel_root}` absoluteness.
6. `skills/debate/SKILL.md:25,30,39` shows unqualified `--root` commands with a conditional note at `:30` ("If the folder holds more than one channel, every command needs `--channel <id>`"). Unchanged in this delta and outside the artifact set criterion 3 names; consider making the examples explicit for consistency.

## Scope notes on my own verification

- Bash in my environment is restricted to test/lint invocations (compound and general shell commands were denied), so all source inspection was done with read-only file reads and content search. I therefore could not independently recompute the manifest's `source_tar_sha256` `f98a7445…` or the runner-config SHA-256 `0534e6c…`; I relied on the controller-supplied export and manifest for provenance, as instructed. (MSG-1's cited tar hash `087e498…` is for the earlier head `e88cd5ae…`; the manifest for this head lists a different tar, which is expected.)
- `collab/debate-06451.channel.md` is excluded by the manifest from both export and patch, so byte-preservation of the historical *mailbox* is controller evidence, not something I verified. I verified the historical *config* directly and confirmed it is untouched by the patch. The export's `collab/` contains exactly `PROTOCOL.md`, `debate-06451.debate.json`, `repository-unattended-02750.channel.md`, `repository-unattended-02750.debate.json`.
- The `debate-watch-debate-06451.timer` disabled/inactive host state is external controller evidence; the repository documents it as a requirement (`collab/PROTOCOL.md:102-103`) and does not claim to prove it.
- The final proof pins `1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c`, not this head. That is consistent with the criteria — the docket states "It does not authorize code changes" and proves the operating mechanism, and no criterion requires the proof to be pinned at the head commit.
- The live `var/debate/repository-unattended-02750/watcher.json` is gitignored and untracked, so criterion 7 was assessed from the committed sanitized manifests in MSG-11, the committed protocol text, and the code's structural refusals cited above.

Verified fresh from the immutable export: 394 passed, 1 skipped, Ruff clean, prior blocker fixed and guarded. Nothing in this delta holds the slice.

## MSG-5 | 2026-08-07T04:15:12+00:00 | from: codex | type: close | thread: unattended-slice4-branch | refs: feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34

Branch-ref: `feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34`

Runner-config-SHA256: `0534e6cbf3e8db01e3294646f67947880d1580670990d4a115332ea0b4ad5779`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Latest independent Opus verdict approved feature/unattended-slice4@6c0932c8a1ab23ede6570a9b521466ed4c257d34. No edits made; approved branch is ready for owner-controlled merge.
