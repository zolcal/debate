
## MSG-1 | 2026-08-07T01:05:22+00:00 | from: codex | type: review-request | thread: unattended-slice1-branch | refs: feature/unattended-slice1@6d45111881973f5a4c3613a8d0b334b03f29b1c8

Review committed branch `feature/unattended-slice1` at
`6d45111881973f5a4c3613a8d0b334b03f29b1c8` against
`main@db38323559e933928bbbc494e88704a81c83ccc2` and the approved Slice 1
contract. This is a minimum two-agent branch gate: Codex is the disclosed
author-proponent and Opus is the author-independent adversary.

The controller verified the cited ref before this message. Review from the
fresh source export and base-to-head patch, inspect beyond the patch, and run
your own tests. Do not rely on these author-side results as evidence:

- Worktree verification before commit: `334 passed, 1 skipped`; `ruff check .`
  and `git diff --check` clean.
- Filtered fresh export verification: `333 passed, 2 skipped`; the additional
  skip is the historical real-channel corpus deliberately excluded from the
  reviewer export. `ruff check .` is clean.

Provenance:

- Branch ref: `feature/unattended-slice1@6d45111881973f5a4c3613a8d0b334b03f29b1c8`
- Runner-config-SHA256:
  `f90da2936d5b77180b90d883d030bd29bde33d07937cddae419656bb9cb2ad06`
- Source-tar-SHA256:
  `681afd501b0dd8ac35f1f3f088e638194562e1bb8ba72f12ff6a7ba957e51bc1`
- Base-to-head-patch-SHA256:
  `351f7cd20deca8b0d439929018666700b9a4581c39d708b2c233f67500674699`
- Runtime root:
  `/home/zoltan/Projects/debate/var/debate/slice1-review-75842/`
- Thread cap: `12`
- Opus receives no Edit/Write or Debate CLI. The controller binds sender and
  provides only the filtered current thread.

Required Slice 1 checks:

1. New named channels record `managed_version: 1`; cap model, initializer,
   CLI help, fieldless fallback and protocol use 12, while explicit historical
   caps remain unchanged and migration states the source of its effective cap.
2. Managed watcher validation is generic across arbitrary party names and
   fails closed for zero, one, extra or empty command bindings.
3. Missing-command and turnless-open managed states are `INVALID`, never
   healthy `MANUAL`, and `watch-status` returns the attention exit.
4. Markerless legacy channels remain readable/manual without being promoted to
   managed operation.
5. Public documentation, examples, diagrams, changelog and runtime ignore rule
   agree with behavior.
6. The branch does not claim Slice 2 brokering/isolation or Slice 3 typed
   terminal semantics.

Return APPROVE only from your own fresh source inspection and test run. Request
changes with exact file/line evidence for every blocker.

## MSG-2 | 2026-08-07T01:13:42+00:00 | from: opus | type: verdict | thread: unattended-slice1-branch | refs: feature/unattended-slice1@6d45111881973f5a4c3613a8d0b334b03f29b1c8

Branch-ref: `feature/unattended-slice1@6d45111881973f5a4c3613a8d0b334b03f29b1c8`

Runner-config-SHA256: `f90da2936d5b77180b90d883d030bd29bde33d07937cddae419656bb9cb2ad06`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: REQUEST_CHANGES**

REQUEST_CHANGES — feature/unattended-slice1@6d45111881973f5a4c3613a8d0b334b03f29b1c8

Reviewed from the controller's fresh export (source-tar 681afd50..., base-to-head patch 351f7cd2...), inspecting well beyond the patch. My own evidence, not the author's:

- `python -m pytest -q`: **333 passed, 2 skipped** in 5.48s, run twice with identical results. `-rs` names both skips: `tests/test_header_forgery.py:236` ("no collab record in this checkout" — the `collab/*.channel.md` corpus the manifest excludes) and `tests/test_verify_record.py:331` ("the unlocked race window did not open in this run (timing-dependent)").
- `ruff check .`: `All checks passed!`
- Targeted re-run of `tests/test_watch_status.py tests/test_watcher.py tests/test_watcher_config.py tests/test_channel_naming.py tests/test_migrate.py`: **120 passed**.

All seven acceptance criteria pass on fresh inspection (evidence below). One blocker stands, and it is a regression this patch introduces on the unattended tick path the slice exists to harden.

## BLOCKING

### B1. The channel record that this patch newly reads on the watcher path is unhandled: the CLI tracebacks, and the library silently downgrades a managed channel to legacy

This commit adds a read of `<channel>.debate.json` to the watcher path in two places. Neither handles the file being absent, torn, or missing a key.

CLI symptom (crash, outside the refusal vocabulary):
- `src/debate/__main__.py:122` — `channel_config = channel.load_config(root, channel_name)`, added unconditionally inside `_watcher_config`, which is the single entry point for `watch-once` (`src/debate/__main__.py:390`), `watch-status` (`:394` → `_watch_status_report` `:148`) and `watch` (`:398`).
- `src/debate/channel.py:371` — `raw = json.loads(_config_path(root, name).read_text(encoding="utf-8"))`, then `:372` `raw["parties"]` and `:393` `raw["supervisor"]`. Missing file → `FileNotFoundError`; hand-edit typo → `json.JSONDecodeError`; dropped key → `KeyError`.
- `src/debate/channel.py:74` — `class ChannelError(Exception)`, so none of those three is a `ChannelError`.
- `src/debate/__main__.py:409-411` — `main()` converts `ChannelError` and nothing else, so all three escape as a traceback and exit 1.
- Reachability without any corruption: `src/debate/channel.py:161-176`, `discover_channel` returns `None` for a root holding no channel (empty `named`, no `debate.json`), so a typo'd `--root`, a not-yet-created channel, or a moved folder lands on `_config_path(root, None)` = `root/"debate.json"` (`src/debate/channel.py:83-84`) and raises `FileNotFoundError`. At base `db38323559e9` `_watcher_config` never read the channel record, so the same invocation produced an ordinary verdict.

This is the project's own documented defect class, verbatim: `tests/test_watcher_config.py:1-14` — "a typo must refuse, not traceback… it is still a crash-loop under the 60s timer, reachable by a hand-edit typo, and it hits `watch`, `watch-once` AND `watch-status` alike. `main()` converts `ChannelError` and nothing else, so every other exception escapes as a traceback and exit 1. The fix is to refuse in that vocabulary." The patch adds a second hand-authored, committed JSON file to that same function without that conversion. No test covers it: every `_watcher_config` test routes through `make_channel` (`tests/test_watcher_config.py:30-34`), which always creates the record.

Library symptom (fail-open, the direction this slice forbids):
- `src/debate/watcher.py:80-89` — `WatcherConfig.__post_init__` catches only `FileNotFoundError` and then leaves `managed_version`/`parties` at `None`, i.e. legacy. A managed channel whose record was deleted or is unreadable while its doorbell still shows an open thread and a turn therefore reaches `src/debate/watcher.py:275-285` and reports healthy **MANUAL** — "a live session answers this seat, not the watcher" — which is exactly the state criterion 3 says must never be MANUAL. The same missing record thus yields a traceback via the CLI and a healthy-looking MANUAL via the library.

Suggested direction (author's call): raise `ChannelError` naming the missing/unreadable config in `_watcher_config`, and make the `__post_init__` bind refuse rather than silently fall back to legacy when a `channel_name` was explicitly supplied. A silent fallback alone would not fix it — that is the fail-open above.

I could not execute a runtime probe of this path: in this session the harness permitted only `python -m pytest` and `ruff check` (`python -c` and heredoc probes were denied), so B1 rests on the line-by-line call chain above, which is deterministic and self-contained.

## Acceptance criteria — verified green

1. **managed_version 1 and cap 12.** `src/debate/channel.py:334-338` sets `MANAGED_VERSION` for any named init; `:363` writes it only for named channels; defaults are 12 at `src/debate/channel.py:111` (model), `:321` (initializer), `:394` (fieldless fallback), `src/debate/__main__.py:172-177` (help "default: 12"), `PROTOCOL.md:56` ("Thread cap: [12] entries"). Explicit caps survive: `collab/debate-06451.debate.json:7` still records `"thread_cap": 8` with no `managed_version`, and `tests/test_channel.py` (`test_explicit_historical_thread_cap_is_preserved`) passed in my run.
2. **Exactly two bindings, fail closed.** `src/debate/watcher.py:107-127` is set-based over `self.parties` with no party-name literals (`grep -rniE "claude|glm|kimi|opus|codex" src/` matches only the `--parties` help string at `src/debate/__main__.py:170`). Zero/one/extra/empty all covered and passing (`tests/test_watcher.py`, the missing/empty/zero-or-three cases). Empty argv is additionally refused earlier at `src/debate/__main__.py:115-119`.
3. **INVALID, never MANUAL, attention exit.** `src/debate/watcher.py:260-262` (config problem outranks every verdict), `:268-273` (turnless managed thread), `:275-280` (no adapter for the turn); `src/debate/__main__.py:142` adds `INVALID` to `_NEEDS_ATTENTION`, `:153` returns 4. The end-to-end CLI test asserting `code == 4` with `INVALID` and the missing party named passed in my run.
4. **Legacy readable, not promoted; migration states its cap source.** `src/debate/channel.py:179-230` (`migrate_channel`) never writes `managed_version`, so the migrated channel stays manual; `src/debate/__main__.py:371-376` reports `thread cap: N from explicit legacy config` / `from default (field absent)` off the raw file, and both branches passed.
5. **Generic liveness for Opus/Codex and Kimi/GLM.** Same `managed_problem()`/`decide()`/`status()` path for both pairs; parametrized test over `("opus","codex")` and `("kimi","glm")` passed.
6. **Docs agree.** `README.md:104,133-146,168-173,288`, `PROTOCOL.md:17,56,76-80`, `CHANGELOG.md:9-19`, both SVGs (`docs/assets/flow-*.svg:64`), `watcher.example.json` (both seats, debounce 0 — and `tests/test_watcher_config.py:88-97` proves the shipped example yields `managed_problem() is None`), `examples/claude-code.md`, `examples/glm-kimi.md`, `.gitignore` `var/`. `collab/PROTOCOL.md:50,94-95` still says cap 8 and "opus is human-driven, no commands entry" — that is correct, not drift: it describes `collab/debate-06451.debate.json`, a markerless legacy channel. `docs/case-study.md` reads as history throughout. `skills/debate/SKILL.md` makes no cap or driver claim.
7. **No later-slice claims.** No broker, sealed-phase, typed-voting, automatic-terminal-close or OS-isolation claim anywhere in the changed surface; `README.md:63,305` only reject a broker as a design choice, as before.

## Non-blocking follow-ups (do not gate this branch)

- `examples/demo.py:33-35` now creates `var/` under `Path.cwd()`, so `python examples/demo.py` writes into whatever directory the user happens to be in and is only ignored inside this repo. `demo.py` has no test coverage (`grep -rn "demo" tests/` matches only a `--label demo` string), and I did not execute it to avoid writing into the review export; by reading, `sys` is imported at `:16` and the config at `:74-84` is a valid managed pair.
- `watch-once` returns 0 on an INVALID managed channel: `src/debate/__main__.py:389-392` prints the `ESCALATE:` line from `src/debate/watcher.py:753-755` and falls through to `return 0` at `:412`. Not silent (the line is mirrored) and consistent with pre-existing escalation handling, but a scheduler alerting on exit codes sees nothing on the documented cron path (`README.md:160`), unlike `watch` (`src/debate/watcher.py:850-851`) and `watch-status`.
- An invalid managed config re-escalates on every tick, because the `managed_problem()` check at `src/debate/watcher.py:171-173` precedes the already-escalated short-circuit at `:205-206`. Never invokes an agent, so no spend, but it is louder than the "escalate once, never loop" rule elsewhere.
- Neither `README.md:168-173` nor `PROTOCOL.md:76-80` mentions that a command for a third name — a supervisor notification entry, say — makes the channel INVALID (`src/debate/watcher.py:122-123`). Worth one clause.
- `README.md:172` and `PROTOCOL.md:79-80` say a legacy config "must be reconfigured before managed unattended use" without saying how; there is no CLI to add the marker, so the answer is a hand edit of a file `skills/debate/SKILL.md:59` tells agents never to touch by hand. This project's own `collab/debate-06451.debate.json` is in exactly that state.

## MSG-3 | 2026-08-07T01:16:39+00:00 | from: codex | type: fix-report | thread: unattended-slice1-branch | refs: feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb

Branch-ref: `feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb`

Runner-config-SHA256: `f90da2936d5b77180b90d883d030bd29bde33d07937cddae419656bb9cb2ad06`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Fixed B1. `/home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/src/debate/channel.py` now converts absent, unreadable, non-object, incomplete, and invalid channel configs into `ChannelError` refusals. `/home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/src/debate/watcher.py` requires explicitly named watchers to bind the channel record, preventing legacy/MANUAL fallback. `/home/zoltan/Projects/debate/.claude/worktrees/unattended-slices/tests/test_watcher_config.py` covers missing, torn, and incomplete records across watch-once/watch-status/watch plus direct named and corrupt legacy binding. Evidence: `python -m pytest -q` → 345 passed, 1 skipped; `ruff check .` and `git diff --check` clean. No commit made.

Controller verification:
- pytest: ........................................................................ [ 20%]
........................................................................ [ 41%]
........................................................................ [ 62%]
......s................................................................. [ 83%]
..........................................................               [100%]
345 passed, 1 skipped in 6.47s
- ruff: All checks passed!
- diff-check:

## MSG-4 | 2026-08-07T01:21:42+00:00 | from: opus | type: verdict | thread: unattended-slice1-branch | refs: feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb

Branch-ref: `feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb`

Runner-config-SHA256: `f90da2936d5b77180b90d883d030bd29bde33d07937cddae419656bb9cb2ad06`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

APPROVE — `feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb`

Reviewed from the controller's fresh export (manifest `manifest-80f15d0745d5f4085a6f4b773c8425102ba3febb.json`, base `db38323559e933928bbbc494e88704a81c83ccc2`, patch `patch-db38323559e9-80f15d0745d5.diff`), reading well beyond the patch into `src/debate/channel.py`, `src/debate/watcher.py`, `src/debate/__main__.py` and the shipped docs.

## My own evidence

- `python -m pytest -q`: **344 passed, 2 skipped** in 7.15s / 7.38s — run twice, identical. `-rs` names both skips: `tests/test_header_forgery.py:236` ("no collab record in this checkout" — the `collab/*.channel.md` corpus the manifest excludes at line 8) and `tests/test_verify_record.py:331` ("the unlocked race window did not open in this run (timing-dependent)"). The author's 345/1 is the same suite with the collab corpus present; the delta is exactly the excluded-corpus skip.
- `ruff check .`: `All checks passed!`
- Targeted re-run of `tests/test_watcher_config.py tests/test_watcher.py tests/test_watch_status.py tests/test_channel_naming.py tests/test_migrate.py tests/test_channel.py`: **165 passed** in 4.51s.
- No trailing whitespace on any added line in the base-to-head patch (0 matches for `^\+.*[ \t]+$`).

## Blocking findings: none

## B1 from MSG-2 is fixed on both halves, and I verified the fix rather than the report

**CLI half (was: traceback outside the refusal vocabulary).** `src/debate/channel.py:370-413` now converts every reachable failure of the newly-read channel record into `ChannelError`: `:372-375` wraps `read_text`/`json.loads` in `except (OSError, ValueError)` (covers missing file, torn JSON, non-UTF-8, directory-at-path); `:376-379` rejects a non-object; `:380-384` converts the `KeyError` on `parties`/`supervisor`; `:403-413` wraps construction so `int(raw.get("thread_cap", 12))` on a non-numeric value raises `ChannelError` too (the argument evaluation is inside the `try`). `src/debate/__main__.py:409-411` converts `ChannelError` to a stderr refusal and exit 1, so the unconditional read at `:122` can no longer escape. The reachability path I cited in MSG-2 — typo'd `--root`, `discover_channel` returning `None` (`src/debate/channel.py:151-176`), `_config_path(root, None)` = `root/debate.json` absent — now lands on `:375` and refuses.

**Library half (was: fail-open to healthy `MANUAL`).** `src/debate/watcher.py:75-92`: `__post_init__` binds `managed_version`/`parties` from the channel record, and at `:85-87` re-raises the `ChannelError` whenever `channel_name is not None` or a legacy `debate.json` exists. The swallow survives only for a root with neither record, which is the pure-decision-test/pre-init case. `:107-108` additionally refuses a managed watcher that is not bound to two parties. I traced the residual swallow adversarially: to reach it you need `channel_name is None` *and* no `root/debate.json`, in which case `channel.read_signal` (`src/debate/channel.py:416-419`) returns a fresh doorbell → `IDLE`, not `MANUAL`; and the CLI cannot reach it at all because `_watcher_config` calls `load_config` unconditionally first. There is no remaining path on which a managed channel reports healthy `MANUAL`.

**Coverage for the fix, in my run.** `tests/test_watcher_config.py` (patch lines 1067-1104) drives 3 corruptions × 3 subcommands = 9 real `subprocess` invocations of `watch-once`/`watch-status`/`watch`, asserting `"Traceback" not in proc.stderr`, nonzero exit and a `refused` message; plus `test_named_watcher_refuses_a_missing_channel_record_instead_of_going_manual` and `test_legacy_watcher_refuses_an_unreadable_channel_record` for the direct library bind. 333+11 = 344 accounts for my count exactly.

## Acceptance criteria — verified on fresh inspection

1. **`managed_version 1`, cap 12, explicit caps unchanged.** `src/debate/channel.py:53` `MANAGED_VERSION = 1`; `:421-422` sets it for any named init; `:437-444` writes it only for named channels. Cap 12 at `src/debate/channel.py:111` (model), `:321` (initializer), `:407` (fieldless fallback), `src/debate/__main__.py:172-177` (help `default: 12`), `PROTOCOL.md:56` ("Thread cap: [12] entries"). Explicit caps survive: `collab/debate-06451.debate.json:7` still records `"thread_cap": 8` with no `managed_version`. `src/debate/channel.py:125-129` and `:396-402` reject `2`, `True` and `"1"`.
2. **Exactly two arbitrary bindings, fail closed.** `src/debate/watcher.py:110-130` is set arithmetic over `self.parties` with no party-name literals — `grep -rniE "claude|glm|kimi|opus|codex|gpt" src/` matches only the `--parties` help example at `src/debate/__main__.py:170`. Zero, one, extra and empty all covered (`tests/test_watcher.py:143-199`); empty argv is refused earlier at `src/debate/__main__.py:115-119`.
3. **INVALID, never MANUAL, attention exit.** `src/debate/watcher.py:250-252` (config problem outranks every verdict), `:258-263` (turnless managed thread), `:265-270` (no adapter for the turn); `MANUAL` at `:264`/`:271` is now gated on `managed_version is None`. `src/debate/__main__.py:142` puts `INVALID` in `_NEEDS_ATTENTION`, `:153` returns 4; `tests/test_watch_status.py:288-316` asserts `code == 4`, `INVALID` in output and the missing party named.
4. **Legacy readable; migration states its cap source.** `src/debate/channel.py:179-230` (`migrate_channel`) only ever adds `name`/`project` to the raw dict — never `managed_version` — so a migrated channel stays manual. `src/debate/__main__.py:371-376` prints `thread cap: N from explicit legacy config` / `from default (field absent)` off the raw file; both branches are asserted (`tests/test_migrate.py`, patch lines 782 and 788-799) and passed.
5. **Generic liveness for both pairs.** `tests/test_watcher.py:130-141` loops `("opus","codex")` and `("kimi","glm")` through the same `decide()`; no branch in `src/` distinguishes them.
6. **Docs agree.** `README.md:104,133-146,165-176,284-288`, `PROTOCOL.md:17,56,76-80`, `CHANGELOG.md:24-34`, both SVGs at `docs/assets/flow-{dark,light}.svg:64`, `watcher.example.json` (both seats, debounce 0 — and `tests/test_watcher_config.py:88-99` proves the shipped file yields `managed_problem() is None`), `examples/claude-code.md:37-45` and `examples/glm-kimi.md:74-82` (both list two commands, so both shipped examples are valid managed pairs), `.gitignore:42` `var/`. `collab/PROTOCOL.md:13,50` still describing cap 8 is correct, not drift: it documents the markerless legacy `collab/debate-06451.debate.json`.
7. **No later-slice claims.** No broker, sealed-phase, typed-voting, automatic-terminal-close or OS-isolation claim in the changed surface. `README.md:63,305` reject a broker as a pre-existing design statement, unchanged by this patch.

## Non-blocking follow-ups (do not gate this branch)

- `examples/demo.py:33-35` writes into `Path.cwd()/var` with no cleanup, so `python examples/demo.py` litters whatever directory the user is in and is only ignored inside this repo; base used the system temp dir, which the OS reclaims. No test covers `demo.py`; I read it rather than executing it to avoid writing into the review export. Its `WatcherConfig` at `:74-86` passes `managed_version=1` and `parties=` explicitly, so it does not exercise the new bind.
- `watch-once` returns 0 on an INVALID managed channel: `src/debate/__main__.py:389-392` prints the `ESCALATE:` line and falls through to `return 0` at `:412`. Not silent, and criterion 3 only requires the exit from `watch-status`, but a scheduler alerting on exit codes sees nothing on the documented cron path (`README.md:160`).
- An invalid managed config re-escalates on every tick: `src/debate/watcher.py:174-176` precedes the already-escalated short-circuit at `:208-209`. No agent is ever invoked, so no spend, but it is louder than the "escalate once, never loop" rule elsewhere.
- `src/debate/watcher.py:103` hardcodes `(None, 1)` instead of importing `channel.MANAGED_VERSION` (`src/debate/channel.py:53`), so the supported-version set is now stated in two places.
- `src/debate/__main__.py:372` reads the just-migrated config with a bare `json.loads`, not the new `ChannelError`-converting `load_config`. Safe today because `migrate_channel` wrote it three lines earlier, but it is the same shape as the defect just fixed.
- Neither `README.md:165-176` nor `PROTOCOL.md:76-80` mentions that a command for a third name makes the channel INVALID (`src/debate/watcher.py:125-126`). Worth one clause.
- `README.md:172` and `PROTOCOL.md:79-80` say a legacy config "must be reconfigured before managed unattended use" without saying how; there is no CLI to add the marker, so the answer is a hand edit of a file `skills/debate/SKILL.md:59` tells agents never to edit by hand. This project's own `collab/debate-06451.debate.json` is in exactly that state.

## MSG-5 | 2026-08-07T01:21:54+00:00 | from: codex | type: close | thread: unattended-slice1-branch | refs: feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb

Branch-ref: `feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb`

Runner-config-SHA256: `f90da2936d5b77180b90d883d030bd29bde33d07937cddae419656bb9cb2ad06`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

**Decision: NONE**

Latest independent Opus verdict APPROVE applies to feature/unattended-slice1@80f15d0745d5f4085a6f4b773c8425102ba3febb. No edits made; approved branch is ready for owner-controlled merge.
