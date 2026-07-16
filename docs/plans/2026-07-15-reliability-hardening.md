# Reliability hardening for v0.3 — staleness, crashes, run-to-completion

**Date:** 2026-07-15 · **Owner/executor:** Claude (Fable 5) session in /home/zoltan/Projects/debate
**Status:** r4 — three Codex review rounds folded in (MSG-9, MSG-11, MSG-13). Lock = kernel advisory
lock (flock/msvcrt, no staleness logic); D6 = snapshot-under-writer-lock covering invoke, escalate,
and persisted-STUCK; turn age derived from the log with turnless threads defined as supervisor-only
states; terminal launch failures; opener allowlist preserving close-corrections; release tag gate;
worktree execution.
**Motivating incidents (same day, three parallel channels):** a `codex exec` with inherited stdin hung
3 hours producing nothing (exit 144 on kill); a hand-rolled 8-minute `timeout` nearly killed a 7-minute
review mid-flight; a turn sat parked for hours with no surface showing it; a baseline-test agent posted
a `verdict` onto a CLOSED thread and silently reopened it (channel.py permits any type to open).

## Goals
Ship v0.3.0 such that a stranger running two agents unattended gets: no silent hangs, no uncaught
crashes in the watcher, visible staleness, a one-command way to drive a review to completion, and a
protocol that refuses reply-type posts from opening threads.

## Non-goals
- No push/notification transport (polling stays the model).
- No N>2 parties.
- No changes to `skills/debate/SKILL.md` (seat-side skill; keeping it untouched avoids re-running its
  scenario test suite).
- No changes to `compact`, locks in the channel root, or CRLF/byte-fidelity behavior.

## D1 — Subprocess hardening (`src/debate/watcher.py`)
1. Child launch gains `stdin=subprocess.DEVNULL` (today stdin is inherited; safe under cron, hangs
   under live terminals/harness pipes — the 3-hour incident class).
2. `subprocess.run` wrapped:
   - `subprocess.TimeoutExpired` → output line `invoked <party> for seq <n>: TIMEOUT after <t>s (killed)`.
     The invocation was already recorded pre-launch, so the existing once-per-seq retry→escalate
     machinery handles the rest. Tick continues; final state save always runs.
   - `FileNotFoundError` / `OSError` / `ValueError` → output line `invoke failed for <party>: <error>`
     **and immediate escalation** (`record_escalation`) — a missing binary or bad argv cannot heal by
     retrying.
3. **Escalation is terminal:** `decide()` consults the escalated set BEFORE its retry logic, so an
   escalated `thread:seq` is never relaunched (today the count==1 retry path fires first — a missing
   binary would be launched again). A later-tick test proves no relaunch.
4. Argv hygiene at the source: `WatcherConfig.__post_init__` validates every `commands` element is a
   `str` (kills the `AttributeError` class in `command_for` before any launch). Nonzero exit stays
   reported as today (`exit <code>`). No tick may terminate with an unhandled exception from the
   launch path.

## D2 — Staleness surface (`src/debate/channel.py` status + `__main__.py`)
1. When a thread is open, `debate status` prints one added human line:
   `turn '<party>' parked <H>h<MM>m on '<thread>' (seq <n>)` where `<n>` is the seq of the entry that
   assigned the turn (see 2) — not the latest seq.
2. **Turn age is truthful under supervisor interjections.** The turn is assigned by the last
   *party-authored* entry (supervisor posts preserve `turn` but replace `updated_at`, so
   `now - updated_at` measures channel idleness, not parked time — the wrong thing after an
   interjection). New helper `channel.turn_parked_since(root, now) -> tuple[int | None, int] | None`
   returning `(age_seconds_or_None_when_unknown, assigning_seq)` — this exact signature, spec and
   plan agree.
   - Scan newest-first over entries **of the open thread only** — an entry from an older closed
     thread must never supply the age or seq.
   - Returns None when no thread is open **or when `turn` is empty**. A turnless open thread
     (supervisor opener) is a SUPERVISOR-ONLY state: turn enforcement (channel.py:220) refuses both
     parties when a thread is open and the turn is not theirs — an empty turn matches nobody, and a
     non-close supervisor post PRESERVES the empty turn (channel.py:245-248), so only a close resolves
     the state. `status` prints `thread '<t>' open with no turn — supervisor close required` and emits no
     `turn_age_seconds`. **`--stale-after` (any N) exits 3 on a turnless open thread** — it is
     unconditionally stuck for parties, which keeps "0 detects any open thread" literally true.
   - Timestamps: naive → treat as UTC (test with a concrete expected age); malformed party stamp →
     fall back to the signal's `updated_at` (test pins the FALLBACK value at a distinctly nonzero
     age, not ≈0); **both stamps malformed → age is unknown**: the parked line prints
     `(age unknown; malformed stamps)`, `turn_age_seconds` is omitted, and `--stale-after` exits 3
     (unknown counts as stale — conservative). No fabricated 0 anywhere; nothing raises.
   - The open-thread scan filter is defense-in-depth: append-only + one-thread-at-a-time means any
     party entry newer than the open thread's opener belongs to the open thread, so a "leak" from a
     closed thread is impossible for turned threads; the filter documents intent and guards future
     format changes. Tested via the turnless case (scan over foreign-thread entries finds nothing).
3. JSON output gains `"turn_age_seconds": <int>` (present only when a thread is open).
4. New flag `debate status --stale-after <seconds>` (validated `>= 0`): exit code **3** when a thread
   is open and `turn_age_seconds >= N`; exit 0 otherwise. `>=` is the contract — `--stale-after 0` is
   a deterministic "any open thread" probe. Lets cron/scripts alert without JSON parsing.
5. No new state files; everything derives from the mailbox + `signal.json`. Tested: a supervisor
   interjection must NOT reset the reported age.

## D3 — `debate watch` run-to-completion loop (`watcher.py` + `__main__.py`)
1. `debate watch --root R --config C [--interval 180] [--until-close] [--max-ticks N]`.
   CLI validation: `--interval` and `--max-ticks` must be `>= 1` (zero/negative → argparse error,
   exit 2, never reaching `time.sleep`); `status --stale-after` must be `>= 0` — zero is VALID (the
   "any open thread" probe); only negatives are argparse errors.
2. Semantics: loop { `run_once()` → print lines → check exit conditions → sleep interval }. Reuses
   `run_once` verbatim — no second decision path. Lock-refused ticks (see 4) do not count as ticks.
3. Exit conditions: `--until-close` and signal shows no open thread → exit 0, message
   `thread closed after <k> tick(s) — exiting`. A tick that ESCALATEs → exit **4** (loudly stuck).
   **Persisted escalations do not spin:** when the current seq is already in the escalated set,
   `run_once` emits `STUCK: seq <n> escalated; supervisor action required` each tick, and `watch`
   exits 4 on `ESCALATE:` or `STUCK:` lines — a `watch --until-close` started AFTER a cron tick
   recorded the escalation terminates immediately instead of sleeping forever (regression test).
   `--max-ticks` reached → exit 5. Another live watcher holds the lock → exit **6**. Ctrl-C →
   exit 130 — this one is CLI-ONLY (`watch()` never returns it; the CLI maps `KeyboardInterrupt`).
   Coverage contract: `watch()`-level tests for 0/4/5/6; CLI pass-through tests for 0/4/5/6
   (monkeypatched `watch` return) and 130 (monkeypatched `watch` raising `KeyboardInterrupt`);
   argparse rejection tests for nonpositive `--interval` AND `--max-ticks`. Any watch-loop test that
   must exit before sleeping uses a sleep callable that RAISES — a regression can fail, never hang
   pytest.
4. **Watcher lock — OS-level advisory file lock; no staleness logic exists.** One lock file
   `<state_path>.lock`, locked with `fcntl.flock(LOCK_EX | LOCK_NB)` on POSIX and
   `msvcrt.locking(LK_NBLCK)` (1 byte) on Windows — both stdlib, both released by the KERNEL when the
   holder exits or crashes. This eliminates the entire failure family of r2's pid design in one move:
   no `os.kill(pid, 0)` (which on Windows TERMINATES the target rather than probing it), no stale-file
   takeover, no takeover TOCTOU (two contenders seeing the same dead owner), no ownership-safe-unlink
   bookkeeping. The lock file's CONTENT (pid + ISO stamp) is written for human diagnostics only and
   carries no semantics; the file is never unlinked (it is inert when unlocked).
   - `watch-once` holds the flock around its single `run_once`; if the lock is held it gives up
     immediately with `another watcher is driving <lock>` — the next cron tick simply retries.
   - `watch` acquires the flock ONCE at startup and holds it for the process lifetime, so the
     second-watch exit-6 contract holds even while the first watch sleeps, and a cron `watch-once`
     firing during a foreground `watch` is refused — by design.
   - `_save_state` tmp files become pid-unique (`.tmp<pid>`) — belt-and-braces against any two
     writers sharing a tmp name.
   - Lock lives beside the state file — never inside the channel root (the existing `state_path`
     inside-root refusal already guarantees the location).
   - Tests are REAL concurrency tests, not prewritten files: a live child process holding the flock
     (spawned via `sys.executable -c`, parent waits on a ready-signal file) blocks `run_once` and
     makes a second `watch` exit 6; after killing the holder, reacquisition is asserted with BOUNDED
     POLLING (Windows documents that unlock after process termination may be delayed — never assume
     immediate); two opens in one process conflict correctly (flock binds to the open file
     description). One test runs a REAL `watch` into its sleep on a background thread and proves,
     while it sleeps, that both a second `watch` (exit 6) and a `run_once` (refused) stay excluded
     for the process lifetime — then releases it deterministically.
5. **What this lock does NOT do:** it serializes watchers only, not channel writers — the
   signal-vs-entries snapshot race is handled separately (D6).

## D4 — Opener allowlist (`src/debate/channel.py` post)
1. New rule, party posts only, evaluated when **no thread is open**: `entry_type` must be in the
   allowlist `OPENER_TYPES = ("review-request", "question", "info", "close")`. `verdict` and
   `fix-report` are refused:
   `refused: 'verdict' cannot open a thread — only review-request/question/info (or a one-shot close
   correction) may start one`.
   An allowlist (not a reply-type denylist) so any future entry type fails closed.
2. **`close` stays an opener deliberately** — the one-shot close-correction idiom is shipped contract
   (PROTOCOL.md:51, pinned by tests/test_channel.py:102, used in production per docs/case-study.md:81).
   The original "block all reply types" decision was based on a wrong compatibility claim; the observed
   incident was a stray `verdict`, which this still kills. A stray `close` opens-and-closes in one
   entry — record noise, no reopened discussion.
3. Supervisor unaffected (may post any type at any time, as today). The supervisor-exemption test
   asserts the RESULTING SIGNAL, not mere success: a supervisor `verdict` with nothing open creates an
   open thread with an empty turn (channel.py:243-248 preserves `turn`, which is `""` after a close).
   `--force` semantics unchanged (supervisor-only, bypasses the one-thread rule only).
4. Docs: PROTOCOL.md gains the opener-allowlist rule; README "What's enforced — and what isn't" adds it
   to the enforced list. With `close` preserved, no existing test or documented idiom breaks; the
   verdict/fix-report refusal is still a behavior change → minor-version bump.

## D5 — Tests, docs, release
1. TDD, failing test first, one behavior per test. New tests:
   - watcher: TimeoutExpired path, launch-failure escalation AND a later-tick no-relaunch proof, stdin
     is DEVNULL (kwargs spy — deterministic; accepted by review), argv-type validation; lock (flock):
     live child holder blocks `run_once` and makes a second watch exit 6, kernel release on holder
     death asserted with bounded polling, in-process double-open conflict, real watch-through-sleep
     exclusion, pid-unique state tmp files.
   - watch loop: until-close exit 0, escalate → exit 4, persisted-STUCK → exit 4 with raising sleep,
     max-ticks → exit 5, live-lock → exit 6; CLI pass-through 0/4/5/6 + `KeyboardInterrupt` → 130;
     argparse rejection of nonpositive interval/max-ticks and negative stale-after.
   - status: parked line + `turn_age_seconds` + `--stale-after` exit 3 at the `>=` boundary;
     supervisor-interjection non-reset; turnless thread (supervisor-required line, no age, stale-after
     trips); malformed-stamp fallback pinned at a distinctly nonzero value; naive-stamp concrete age;
     both-malformed → unknown-age contract.
   - channel: verdict/fix-report refused as openers; review-request/question/info/close accepted;
     supervisor exemption asserting the resulting signal; D6: all three interleavings (invoke, new
     escalation, persisted STUCK) from the frozen mid-post state.
2. README: new "Running to completion" subsection under "Running it unattended" (watch = foreground,
   cron watch-once = unattended; same config, same rails); stdin/timeout rails documented honestly.
3. Version 0.3.0 in ALL FOUR places — `pyproject.toml`, `src/debate/__init__.py.__version__`,
   `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` — enforced by a new unit test
   (`tests/test_release_sync.py`) that reads all four and asserts equality, so drift fails CI forever,
   not just this release.
4. **Execution isolation:** implementation happens in a dedicated git worktree
   (`git worktree add ../debate-reliability-v0.3 -b reliability-v0.3 main`), NOT in this dirty shared
   checkout (which carries a live channel, in-flight docs, and separately-owned untracked work). The
   v0.3 deliverables that are currently untracked here — `.claude-plugin/` and `skills/` from the
   distribution slice-1 — are COPIED into the worktree and committed there as the first commit, which
   resolves their base/ownership ordering: the branch owns them from commit one. The dogfood review
   round posts to THIS checkout's `collab/` by absolute path.
5. Hygiene: every commit stages EXPLICIT paths (never `git add -A`); pytest runs with a project-local
   `--basetemp` (`.pytest-tmp/`, gitignored); the local gate mirrors CI exactly (same ruff/mypy
   commands and targets as `.github/workflows/ci.yml`).
6. **Release gate:** `.github/workflows/release.yml` currently publishes any `v*` tag unchecked. Add a
   step before build/publish that fails unless the tag equals the package version:
   `python -c` comparing `${GITHUB_REF_NAME}` (stripped of `v`) against both `pyproject.toml` version
   and `debate.__version__`. With the four-way unit test (D5.3) this closes the tag→package gap.
7. After implementation and green tests: post a `review-request` on `collab/` citing the branch@sha and
   run the codex review round before merge (dogfooding).

## D6 — Stable decision snapshot under the channel writer lock (`src/debate/watcher.py`)
`post` appends the mailbox entry BEFORE replacing the signal (channel.py:235→257), and both writers
serialize on the channel writer lock (`channel._exclusive`). The race: writer appends MSG n+1,
pauses; every watcher read returns signal seq n while the mailbox already holds n+1. Re-reading the
signal cannot catch it, and a mailbox-vs-signal comparison outside a lock still leaves a window for
escalations (which have no turn-enforcement backstop, because escalating posts nothing).

Fix — take the DECISION on a snapshot that cannot be mid-post: `_run_once_locked` wraps ONLY its
snapshot + decision + state-record step in `channel._exclusive(channel_root)` (expose it as
`channel.exclusive()` — public, documented as "hold the channel writer lock"):
1. Under the lock: read signal, read entries, defer iff `max(entry.seq) > signal.seq` (a mid-post
   writer cannot hold the lock, so under it the pair is consistent by construction — the guard is an
   invariant assertion against non-CLI writers, emitting `mailbox ahead of signal (entries at <m>,
   signal at <n>); deferring to next tick`). NOT equality: `compact` legitimately archives old
   entries, leaving the signal seq ahead of the remaining mailbox. Then run `decide()`, and if the
   decision is invoke/escalate, record it in watcher state and save.
2. Outside the lock: mirror lines, LAUNCH the child (never hold the writer lock across the child —
   an agent posting its reply through the CLI would deadlock against its own watcher), final save.
   The post-launch `OSError`/`ValueError` escalation is deliberately a GLOBAL broken-config
   escalation recorded outside the writer lock — it reports "this watcher cannot launch this
   command", a fact independent of channel state, and is distinct from the seq-local
   retry-exhaustion escalation decided under the lock in step 1.
3. The deferral applies to EVERY decision consumer — invoke, NEW escalation, and the persisted-STUCK
   line — because all three derive from the same under-lock snapshot; there is no path that acts on
   an unstable pair. A post that lands after lock release makes an in-flight invocation stale; that
   residue (invoke-only) is backstopped by turn enforcement refusing the stale agent's post.
Tests: the frozen mid-post state (real `channel.post`, then restore pre-post `signal.json` bytes)
must defer (a) an invocation, (b) a NEW escalation, and (c) suppress the STUCK line for a persisted
escalation — all three interleavings pinned. Lock-ordering note: the watcher lock is always acquired
BEFORE the channel writer lock, and the writer lock is never held while acquiring the watcher lock —
no cycle, no deadlock.

## Compatibility notes
- D4 refuses party-authored `verdict`/`fix-report` posts when nothing is open — previously accepted,
  never documented as legitimate, and the source of a real incident. The documented close-correction
  idiom is explicitly preserved (D4.2). This is the only protocol-visible change.
- `watch-once` behavior changes: crash-free launch failures (D1), terminal escalations (D1.3),
  watcher lock (D3.4 — a tick may now be refused while a foreground `watch` runs; cron retries),
  snapshot re-check (D6 — a tick may defer an invocation by one tick under concurrent writes).
- Watcher config file format: unchanged (no new required keys). `state_path` now honors `~` expansion
  (bug fix; the README's own example was broken without it).

## Out-of-scope follow-ups (tracked, not in v0.3)
- `debate doctor` (environment self-check: binary on PATH, config sanity, lock status).
- Windows CI leg (CREATE_NO_WINDOW path is untested today).
- Codex-side plugin manifests (slice 2 of the distribution plan).

## Review — (pending)
Reviews append below this line; the body above is edited only by the executor.

## Review — 2026-07-15 · codex

**Verdict: REQUEST CHANGES.**

I reviewed both this spec and the implementation plan against `main@bcb402c4bfa4fa9f7e1838225c5f386ba6e3c833`, including the current implementations of [watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:1), [channel.py](/home/zoltan/Projects/debate/src/debate/channel.py:1), [__main__.py](/home/zoltan/Projects/debate/src/debate/__main__.py:1), all three current test modules, the public protocol/README/case study, and the CI/release workflows. The current source anchors in Tasks 1–3 and 6 are substantially accurate, and `stdin=subprocess.DEVNULL` is the right direct mitigation for the inherited-stdin incident. The kwargs-spy in Task 1 is an acceptable deterministic unit regression for that exact subprocess contract; a pipe/FD behavioral test would be stronger but is not required for approval. I did not run tests because this is a pre-implementation plan review and the requested mutation boundary permits only this append and the channel post.

1. **BLOCKER — the proposed lock expires during a healthy tick and cannot enforce single-watch ownership.** The plan holds `_locked` around all of `run_once`, including the child process, but breaks the lock after 30 seconds ([implementation plan](/home/zoltan/Projects/debate/docs/plans/2026-07-15-reliability-hardening-plan.md:330)); the real default child timeout is 1,800 seconds ([watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:56)). The channel lock's 30-second rule is explicitly safe only because its protected work takes milliseconds ([channel.py](/home/zoltan/Projects/debate/src/debate/channel.py:51)). A contender can therefore unlink a live watcher lock, and the old holder's unconditional cleanup can then unlink the contender's replacement lock; concurrent saves also share one `.tmp` name ([watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:223)). Separately, a transient per-tick lock is absent while `watch` sleeps, so a second foreground `watch` can acquire it successfully and coexist forever rather than reach exit 6. Redesign ownership/staleness for the full invocation duration (including ownership-safe release), and distinguish process-lifetime foreground-watch ownership from per-tick `watch-once` exclusion if D3.5 remains a contract. Tests must use concurrent holders and cover a live holder beyond the stale threshold, successor-safe cleanup, two foreground watchers, and foreground-watch versus cron-tick exclusion—not only precreated lock files.

2. **HIGH — D2 measures last channel activity, not how long the current party turn has been parked.** A supervisor post deliberately preserves `turn` ([channel.py](/home/zoltan/Projects/debate/src/debate/channel.py:245)) but every post replaces `updated_at` and advances `seq` ([channel.py](/home/zoltan/Projects/debate/src/debate/channel.py:257)); the preserved-turn behavior is already pinned by [test_channel.py](/home/zoltan/Projects/debate/tests/test_channel.py:113). Thus a supervisor interjection resets a three-hour parked turn to zero and makes the displayed seq identify the interjection rather than the turn assignment. That does not close the motivating incident. Add explicit turn-assignment time/seq state or derive it reliably from the log, and test a supervisor interjection. Also handle naive/unparseable timestamps without allowing `now - stamp` to raise.

3. **HIGH — the launch-failure path does not implement its claimed terminal escalation.** Task 2 records one invocation and an escalation on `OSError`, but the real `decide()` retries every `count == 1` record after `retry_seconds` before consulting the escalated set ([watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:114)). A missing binary will therefore be launched again despite “cannot heal by retrying.” Add a later-tick assertion proving no relaunch, and change the state/decision logic accordingly. The broader “no unhandled exception from the launch path” claim also needs either narrowing or config validation: `command_for()` calls `.replace()` on unvalidated command elements before the proposed `try` ([watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:68)), and malformed argv can raise `AttributeError`/`ValueError`, not only `OSError`.

4. **BLOCKER — D4's compatibility analysis is contradicted by the shipped contract.** Party-authored one-shot `close` corrections under a fresh slug are deliberate behavior in [PROTOCOL.md](/home/zoltan/Projects/debate/PROTOCOL.md:51), [test_channel.py](/home/zoltan/Projects/debate/tests/test_channel.py:102), and the production [case study](/home/zoltan/Projects/debate/docs/case-study.md:81). Task 6 would reject that behavior, while line 601 incorrectly predicts no existing test and this spec calls all affected posts “protocol-nonsense.” Decide explicitly whether to preserve the correction idiom (possibly make it supervisor-only) or retire it; if retiring it, name the break honestly and update every contradictory test/document. Implement the spec's opener allowlist rather than a reply denylist so future entry types fail closed. The supervisor-exemption test must assert the resulting signal: today a supervisor `verdict` with nothing open creates an open thread with an empty turn ([channel.py](/home/zoltan/Projects/debate/src/debate/channel.py:243)), not merely “succeeds.”

5. **HIGH — the public contracts and planned tests are not yet aligned.** The spec says stale means `age > N`, while the plan deliberately implements `>=` and admits the spec remains unchanged ([implementation plan](/home/zoltan/Projects/debate/docs/plans/2026-07-15-reliability-hardening-plan.md:663)). `>=` is reasonable and makes zero a useful “any open thread” probe, but it must be the same documented contract and tested at a controlled boundary. The spec promises PID plus timestamp in the lock; the plan writes only PID. The spec's close message counts invocations; the plan counts every loop iteration, including no-ops and lock refusals, and reports ticks. Task 5 advertises exits 0/4/5/6 plus CLI 130 but supplies tests only for 0/4/5 ([implementation plan](/home/zoltan/Projects/debate/docs/plans/2026-07-15-reliability-hardening-plan.md:403)); add exit-6, actual CLI wiring/return-code, and `KeyboardInterrupt -> 130` tests. Do not count a refused lock acquisition as a completed tick. Validate nonnegative stale thresholds and positive interval/max-ticks values so negative input cannot reach `time.sleep` and crash.

6. **HIGH — the release and execution gates are incomplete and unsafe in this checkout.** Task 7 bumps three version locations but leaves `debate.__version__` hard-coded at `0.2.0` ([__init__.py](/home/zoltan/Projects/debate/src/debate/__init__.py:42)), and neither the plan nor [release.yml](/home/zoltan/Projects/debate/.github/workflows/release.yml:9) adds an automated manifest/package/tag synchronization check. Its final local gate is narrower than CI, which runs Ruff and strict mypy over the whole repository, including tests ([ci.yml](/home/zoltan/Projects/debate/.github/workflows/ci.yml:27)). The checkout is already dirty/untracked (`examples/claude-code.md`, `.claude-plugin/`, `collab/`, the handover/plans, and `skills/`), yet every task uses `git add -A`; that can sweep unrelated work and the live channel into commits. Replace all staging with explicit absolute paths, reconcile the intended branch/worktree boundary before Task 0, and run pytest with a project-local base-temp path rather than its default `/tmp` location.

7. **HIGH — the proposed tick lock does not close the channel snapshot race.** `run_once` reads `signal.json` before reading entries and later decides from that first signal ([watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:169)); `post` appends the mailbox entry before replacing the signal ([channel.py](/home/zoltan/Projects/debate/src/debate/channel.py:235)). A concurrent reply can therefore be mirrored while the watcher still invokes the old party/seq. The watcher lock serializes watchers only, not channel writers. Add a stable-snapshot check (for example, re-read and compare the signal before deciding/recording) and a deterministic race test; do not hold `channel._exclusive` across the child, because a child posting its reply would deadlock.

Approval requires resolving the two lock contracts, making turn age truthful, preventing retries after terminal launch failure, making the D4 compatibility decision explicit, aligning every exit/message/boundary contract with tests, completing version/release synchronization, and replacing dirty-tree-wide staging. The five feature directions are otherwise proportionate to the incidents.
