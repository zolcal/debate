# GLM 5.2 reviewer seat — reconfigure collab/ from claude/codex to kimi/glm

Date: 2026-07-17 · Owner: owner · Executor: kimi (K3) · Reviewer: glm-5.2 (via the debate channel itself)

## Goal

Retire the claude (Fable) / codex seats from this repo's collaboration channel and
re-establish it as **kimi (builder, human-driven) ↔ glm-5.2 (reviewer, watcher-driven)**,
supervisor owner. Prove the new pairing live by having GLM review **this plan** through
the debate channel as the first thread — setup and smoke test in one.

Decisions already taken (owner, 2026-07-17):

- Roles: **Kimi builds, GLM 5.2 reviews** (like-for-like seat replacement: Kimi takes
  Fable's interactive seat, GLM takes Codex's headless seat).
- History: compact the 36-message claude/codex record into `collab/archive/` (verbatim,
  tool-native), switch parties. Nothing is deleted.
- Scope: setup + one attended review round (`debate watch --until-close`). **No cron**
  entry for this repo — owner's call afterwards. Another project's debate cron (a
  different channel) stays untouched.
- `debate` CLI: already installed, 0.3.1 in conda base (`~/miniconda3/bin/debate`).
  No reinstall. Seats must resolve it via PATH (see Slice 2).

## Current state (verified 2026-07-17)

- `collab/`: parties `["claude","codex"]`, supervisor owner, cap 8; all threads closed at
  MSG-36 (`signal.json`: empty turn/thread). Untracked in git. No `archive/`, no PROTOCOL.md.
- No cron drives this channel; no `watcher.json` exists for this repo.
- `~/.local/bin/glm-agent` does **not** exist (created in a prior session, since removed).
- `debate` 0.3.1 in conda base env; NOT on the default PATH of a fresh shell (fresh shells
  land in a different conda env). Repo main = 930892e (v0.3.1 tagged, on PyPI).
- `.claude/settings.local.json` exists with stale per-session allows; no project
  `.claude/settings.json`.

## Slice 1 — Channel reconfiguration (verifiable: `debate status` shows empty mailbox, parties kimi/glm)

1. `debate compact --root collab --keep-days 0 --dry-run` → inspect plan, then for real.
   Expect: all closed threads (MSG-1..36) relocated verbatim to
   `collab/archive/CHANNEL-2026-07.md` + `collab/archive/INDEX.md`; `CHANNEL.md` back to
   header-only. If `--keep-days 0` misbehaves, fall back to `--keep-days 1` (threads are
   1–2 days old) — dry-run decides.
2. Edit `collab/debate.json`: `parties: ["kimi","glm"]`, supervisor `owner`, cap 8.
   (Config file, edited by hand is legitimate; `signal.json` already idle.)
3. Write `collab/PROTOCOL.md` from the repo template with: parties kimi (builder,
   human-driven) / glm (reviewer, watcher-driven); cap 8; verdicts MUST cite the
   reviewer's own fresh evidence (current HEAD from git + the reviewer's own checks —
   never evidence quoted from the request); reading discipline via `debate read`;
   unattended-seat constraints (read-only verification + posting + appending its dated
   review section to the reviewed doc in the main checkout; builds/tests in a separate
   worktree; never merge/push main; trust git, not channel history); reviewer appends
   `## Review — YYYY-MM-DD · glm` at the END of reviewed plan docs, never edits the body;
   amendment log v1.0 noting the seat change (claude/codex → kimi/glm, record archived).

## Slice 2 — GLM seat (verifiable: fail-closed identity check passes)

1. Create `~/.local/bin/glm-agent`, `chmod +x` (deviation from the shipped example: one
   added PATH export so the seat resolves `debate` from conda base under any scheduler):

   ```bash
   #!/bin/bash
   # GLM seat for debate: claude -p repointed at z.ai's Anthropic-compatible endpoint.
   set -euo pipefail
   . ~/.secrets   # provides GLM_API_KEY - never inline it in watcher.json
   export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
   export ANTHROPIC_AUTH_TOKEN="$GLM_API_KEY"
   export ANTHROPIC_MODEL="glm-5.2"   # override any locally pinned model
   export PATH="$HOME/miniconda3/bin:$PATH"   # debate CLI lives in conda base
   exec claude -p "$1" </dev/null
   ```

2. Fail-closed identity check (refuses, not warns):
   `glm-agent "Reply with exactly: SEAT-OK <your model name>" | grep -q "SEAT-OK glm-"`.
   If this fails (missing key, endpoint drift): STOP, report to owner — no smoke round.
3. Project `.claude/settings.json`, narrow allowlist for the headless seat — no blanket
   skip. Post-sanitization split: the committed file carries only the generic entries
   (`Bash(debate *)`, read-only git); the host-specific entries (absolute debate path,
   the `Edit(...docs/plans/**)` house-rule permission) live in the untracked
   `.claude/settings.local.json` — claude merges both.

   (`Edit(...docs/plans/**)` is the house rule that the reviewer appends its dated review
   section to the plan doc. Deliberately no pytest entry yet — widen when the first
   *code* review needs it, per the example's guidance.)

## Slice 3 — Watcher + commit (verifiable: idle `watch-once` tick is a no-op; commit exists)

1. Watcher config: the live `watcher.json` is host-specific (absolute paths) and stays
   **untracked** (gitignored); the repo commits a sanitized `watcher.example.json`
   instead (content below). `kimi` gets **no `commands` entry** — human-driven seats are
   never auto-started (README pattern). `glm` debounce 60 s: it is a machine-only seat,
   the 600 s human-reply window does not apply and would stall attended runs.

   ```json
   {
     "state_path": "~/.local/state/debate/debate-repo.json",
     "commands": { "glm": ["~/.local/bin/glm-agent", "{prompt}"] },
     "prompts": { "glm": "Review channel ./collab: it is your turn. Read collab/PROTOCOL.md, then the open thread via `debate read --root collab` — never the whole CHANNEL.md. Immediately before acting, verify collab/signal.json still shows a NON-EMPTY thread AND turn=='glm' — if not, exit without posting. You are the REVIEWER: check what the request cites; for verdicts cite YOUR OWN fresh evidence (current HEAD from git, your own inspection) — never evidence quoted from the request. When reviewing a plan doc, append your full review as a dated section `## Review — YYYY-MM-DD · glm` at the END of the document (never edit its body) before posting your verdict. Constraints: read-only verification, doc review-section appends, and posting in the main checkout; any build/test runs in a separate git worktree; no commits to main, no merges, no pushes; verify any claim about repo state against git directly, never from channel history. Post via `debate post --root collab`, then stop." },
     "debounce_seconds": { "glm": 60 },
     "retry_seconds": 1800,
     "timeout_seconds": 1800
   }
   ```

2. Branch `glm-reviewer-seat` off main; ONE commit: Slice 1–3 artifacts + this plan doc
   + `.gitignore` entries (`collab/signal.json`, `collab/.lock`). This resolves the
   deferred owner decision to commit `collab/`. **Git mutations are executed only after
   explicit owner confirmation at run time.**

## Slice 4 — GLM reviews this plan (the smoke round; verifiable: thread closed, verdict cites fresh evidence)

1. Kimi posts `review-request`, thread `glm-reviewer-seat-plan`, refs
   `glm-reviewer-seat@<sha>` with `--verify-refs .`: review this plan doc against the repo
   as it actually is (README guarantees, examples/glm-kimi.md, src/debate semantics for
   compact/debounce/no-commands-entry), plus the wrapper/settings/watcher artifacts in the
   commit. Verdict must cite fresh evidence; full review appended per house rules.
2. `debate watch --root collab --config watcher.json --until-close` in the foreground.
   GLM wakes through the real watcher path (wrapper → claude -p → glm-5.2), appends its
   review section, posts its verdict.
3. Debate per protocol until APPROVE or the cap escalates to the supervisor. Kimi closes.
   Success = verdict authored through the watcher path, fresh evidence cited, watcher
   exits 0, thread closed under the cap. Watcher exit 4/5/6 (stuck/launch-failure) →
   stop and diagnose, do not force.

## Slice 5 — Fold in + finalize (verifiable: review findings resolved; handover current)

1. Address GLM's review: fold accepted changes into the setup/plan as follow-up commits
   on the same branch (review sections are never edited). If GLM requests changes that
   alter Slices 1–3, apply and re-verify the affected slice gate.
2. Update `docs/HANDOVER-SESSION-2.md` (created at first milestone this session).
3. Hand to owner: merge decision, plus the standing post-switch checklist — cron or not,
   first *code* review widenings (pytest allow), and whether examples/glm-kimi.md should
   mention the conda-PATH wrapper variant (deferred; example is host-generic).

## Risks / notes

- SEAT-OK failure blocks everything → owner, not workaround.
- GLM seat writes inside the repo are bounded to `docs/plans/**` appends by allowlist;
  everything else is read-only + `debate post`. Advisory, as always — see README trust model.
- `claude -p` / z.ai endpoint drift: re-run the identity check after any `claude` upgrade.
- Old seats remain in `collab/archive/` and git history by design — "out of the picture"
  means out of the active configuration, not erased from the record.

## Review — 2026-07-17 · glm

**Verdict: APPROVE.** The setup is correct against the repo as it actually is, internally
consistent, and the end-to-end path is live-verified — I am running through it right now
(glm-5.2, woken by the watcher for seq 37). Every claim below is my own fresh evidence
(current HEAD, git, file inspection); nothing is quoted from MSG-37.

**Git / cited refs (fresh).** `git rev-parse HEAD` = `77cac3e` on `glm-reviewer-seat`;
`main` = `930892e` (tag `v0.3.1`, `origin/main`). `git merge-base --is-ancestor
930892e 77cac3e` succeeds; `git rev-list --count main..77cac3e` = 1. So the cited
relationship `glm-reviewer-seat@77cac3e` = exactly one commit over `main@930892e` is
correct. The commit adds the 10 expected artifacts: `.claude/settings.json`, `.gitignore`,
`collab/{CHANNEL.md,PROTOCOL.md,debate.json,archive/*}`, `docs/HANDOVER-SESSION-2.md`,
this plan, and `watcher.json`.

**Axis 1 — setup vs repo semantics.**
- *compact:* `src/debate/channel.py:439` makes a thread eligible when
  `(now - last_at) < keep_days*86400`; with `--keep-days 0` that bound is `< 0` → always
  false → every closed thread is eligible. Archive is named by the thread's last-entry
  month (`CHANNEL-YYYY-MM.md`) with one INDEX line per thread. Verified outcome:
  `collab/archive/INDEX.md` lists 6 closed threads summing to 36 entries;
  `collab/archive/CHANNEL-2026-07.md` holds MSG-1..MSG-36 verbatim (grep `^## MSG-` count
  = 36, first = MSG-1, last = MSG-36); `collab/CHANNEL.md` is header-only post-compact,
  its only live entry being MSG-37 (+4 lines vs HEAD = the uncommitted review-request).
  Matches the README "relocate verbatim… nothing is edited or deleted."
- *no-commands-entry ⇒ never auto-started:* `src/debate/watcher.py` `command_for()` returns
  `None` for a party with no `commands` entry and `decide()` short-circuits to
  "no command configured". `kimi` has no entry in `watcher.json`. Matches README l. 128.
- *debounce:* `decide()` reads `debounce_seconds.get(turn, 0)` and holds fire while
  `(now - updated_at) < debounce`. `glm` = 60 s — a machine seat, so the 600 s human-reply
  window does not apply. Consistent with `collab/PROTOCOL.md` §4.
- *debate.json:* `parties: ["kimi","glm"]`, supervisor `owner`, `thread_cap: 8` — matches
  PROTOCOL §3.

**Axis 2 — `watcher.json` + my own pinned prompt (runtime).**
- `~/.local/bin/glm-agent` exists, is executable (`-rwxrwxr-x`), and matches Slice 2
  verbatim — including the conda-PATH deviation
  (`export PATH="$HOME/miniconda3/bin:$PATH"`). `which debate` ⇒
  `~/miniconda3/bin/debate`; `which claude` ⇒ `~/.local/bin/claude`.
  Both exec targets resolve.
- `state_path` (`~/.local/state/debate/debate-repo.json`) is outside the channel
  root, and that separation is hard-enforced in `WatcherConfig.__post_init__`. No
  cross-channel collision: the state dir holds only `debate-repo.json` + its `.lock`, and
  a grep of `~/Projects` finds no other config referencing this path (the
  other project's channel does not share it).
- The pinned prompt's relative paths (`./collab`, `collab/PROTOCOL.md`, `--root collab`)
  resolve because the agent inherits the watcher's cwd = repo root. Live-verified: I just
  ran `debate read --root collab` and `debate status --root collab` (seq 37, turn `glm`,
  turn_age 562 s) from here successfully.
- Identity gate satisfied empirically: the seat authoring this review is glm-5.2 via the
  wrapper → z.ai endpoint → `ANTHROPIC_MODEL=glm-5.2` — exactly the path the
  `SEAT-OK glm-` check asserts.
- The `Edit(//home/.../docs/plans/**)` allowlist permitted this append — you are reading
  the proof.

**Axis 3 — `collab/PROTOCOL.md` vs the upstream template (`/PROTOCOL.md`).** Faithful fill-in
of the bracketed choices (CHANNEL.md tracked; signal.json/.lock gitignored; cap 8;
`--verify-refs .`). Two deliberate deltas, both consistent with this plan: (a) the
plan-document review house rule (§3 — a dated `## Review — … · glm` section at the END,
body untouched); (b) a tightening of §5: the watcher-driven reviewer seat is bounded to
read-only verification + appending its review section + posting, with builds/tests in a
separate worktree. The template's broader "build and commit on feature branches" is dropped
because the reviewer does not commit — the builder folds accepted changes in (Slice 5).
Amendment log is present and accurate.

**Axis 4 — risks the plan misses (non-blocking; mostly already tracked).**
- *A. The installed wrapper diverges from the shipped example.* `examples/glm-kimi.md`'s
  wrapper omits the conda-PATH export that this host requires (fresh shells land in
  a different conda env, per the plan's Current state). Slice 5 defers "whether the example should
  mention the conda-PATH variant"; until then the example is misleading for this exact
  host — a seat re-created from it would not find `debate`. Worth closing when the example
  is next touched.
- *B. Relative-path correctness hinges on the watcher's cwd = repo root.* True today
  (verified), and there is no cron yet. When the owner adds cron (deferred), the line MUST
  `cd ~/Projects/debate &&` first (README ll. 123–126 / example note) or every
  relative path in the pinned prompt silently breaks. The #1 thing to get right at the
  cron step.
- *C. No pytest allowlist yet* — deliberate for a doc review (Slice 2 / example guidance:
  widen on the first *code* review). Noted as a correct boundary, not a gap.

No blocking defects. The kimi/glm pairing is correctly wired and live-verified end-to-end.
