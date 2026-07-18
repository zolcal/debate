# Handover — Session 2 (2026-07-17)

## Summary
Reconfiguring this repo's collab channel from claude/codex to **kimi (builder, human-driven)
↔ glm-5.2 (reviewer, watcher-driven)**, supervisor owner. Plan: `docs/plans/2026-07-17-glm-reviewer-seat.md`
— GLM reviews that very plan through the channel as the smoke round (owner requirement).

## Completed
- Context review: channel idle at MSG-36 (all closed); no cron for THIS repo (another project's debate cron is a different channel, untouched); `debate` 0.3.1 lives in conda **base** (`~/miniconda3/bin/debate`), NOT on fresh-shell PATH (fresh shells land in a different env).
- Plan doc written + owner-approved: `docs/plans/2026-07-17-glm-reviewer-seat.md` (5 vertical slices).
- Slice 1: `debate compact --keep-days 0` — MSG-1..36 (6 threads) verbatim to `collab/archive/CHANNEL-2026-07.md` + INDEX.md; `debate.json` parties → `["kimi","glm"]`; `collab/PROTOCOL.md` written (cap 8, fresh-evidence verdicts, house rule: reviewer appends `## Review — YYYY-MM-DD · glm` at END of plan docs).
- Slice 2: `~/.local/bin/glm-agent` recreated (example + added `export PATH="$HOME/miniconda3/bin:$PATH"` so the seat finds `debate`); **SEAT-OK glm-5.2 PASS** (fail-closed check); project `.claude/settings.json` narrow allowlist (debate CLI, read-only git, `Edit(docs/plans/**)`). Had to set `projects["~/Projects/debate"].hasTrustDialogAccepted=true` in `~/.claude.json` (claude ignores project settings in untrusted workspaces; backup at `~/.claude.json.bak-debate-20260717`).
- Slice 3 (pre-commit): `watcher.json` at repo root (glm-only command, debounce 60 s — machine-only seat; kimi has NO commands entry = never auto-started; timeout 1800); `.gitignore` += `collab/signal.json`, `collab/.lock`; idle `watch-once` tick verified silent, exit 0.

## In Progress
- Nothing. Awaiting owner only.

## Smoke round — COMPLETE (2026-07-17, thread glm-reviewer-seat-plan, MSG-37..39)
- MSG-37 review-request (kimi) → watcher woke glm-agent after 60 s debounce → **MSG-38
  APPROVE (glm-5.2)**: fresh evidence on all 4 axes (compact semantics channel.py:439,
  no-commands-entry ⇒ never auto-started, debounce, wrapper/state-path/allowlist runtime,
  PROTOCOL vs template), full review appended to the plan doc (`## Review — 2026-07-17 · glm`).
- 3 non-blocking notes: (A) example wrapper lacked the conda-PATH export → **folded at
  5e529b4**; (B) future cron line MUST `cd ~/Projects/debate &&` first
  (relative prompt paths) — carried as owner item; (C) pytest allowlist boundary confirmed
  deliberate (widen on first code review).
- MSG-39 close (kimi). Branch `glm-reviewer-seat` = 77cac3e (setup) + 5e529b4 (fold-in),
  2 commits over main@930892e.

## Sanitization (2026-07-17, pre-push)
- Owner directive: machine refs (`/home/<user>` paths, supervisor handle, other-project
  codenames) must not be public; legal name stays (LICENSE/pyproject/manifests/authors).
- Branch rewritten pre-push (unpushed commits): scrubbed tree re-committed as
  5497e11 (setup) → 28b8e1b (plan+review) → 3118e69 (redact main docs) → tip (handover).
  Old SHAs 77cac3e/5e529b4/c3737ed/ab8ae16 no longer exist; SHA-remap correction posted
  to the channel. History subset check vs main: CLEAN (no new exposure in any commit).
- `watcher.json` untracked (host paths) — sanitized `watcher.example.json` committed;
  host-specific allowlist entries moved to `.claude/settings.local.json`; .gitignore +=
  watcher.json, settings.local.json, HANDOVER-SESSION-1.md.
- Supervisor renamed to `owner` in collab/debate.json — supervisor posts now use `--from owner`.
- Main's 4 plan docs + test docstring redacted in 3118e69 (visible redaction commit;
  old blobs remain in history by owner decision — no force-push).

## Benchmark pilot — IN PROGRESS (2026-07-17)
- Owner approved a pre-registered Study-1 pilot: does cross-vendor code review beat
  same-vendor review? Plan: `docs/plans/2026-07-17-cross-vendor-review-benchmark-pilot.md`
  (committed b420a8a; GLM reviewing via channel, thread benchmark-pilot-plan, MSG-41).
- Design: H1 kill gate (cross-vs-same recall ≥5pp @ FPR=10%, pooled 3 pairs); H2 full
  debate lifecycle (agreement-or-escalation, production-mirrored); two-tier corpus
  (80 LCB-2026 + 30 SWE-rebench-2026 per builder); DebugBench calibration arm; pairs =
  Fable5↔GPT-5.6 (subscriptions, FIRST — Codex window closes in days), K3↔GLM-5.2,
  local Qwen3.6-27B↔Gemma4-31B (selection gate at pull time; spec-decoding allowed).
- Execution repo `~/Projects/debate-bench` to be created (PRIVATE until gate passes).
- Research basis (3-agent sweep, 2026-07-17): naive debate doesn't replicate at matched
  compute; heterogeneity + self-preference bias (10-25%) are the defensible ingredients;
  no published cross-vs-same-vendor code-review head-to-head exists.
- NEXT after verdict: fold in findings → S1 (harness, GLM-5.2 pipeline proof) → S2
  (premium builders first) → S3 (reviews+lifecycle) → S4 (analysis, kill/proceed).
- Owner note: marketing context — README seat-tense update + video-3 still pending;
  benchmark is the potential headline for both. Owner also flagged a "major project"
  to discuss after the push judgment (delivered: safe to push).

## Next Steps (owner)
1. Merge `glm-reviewer-seat` to main (ff) + push — the merge decision was left to you per protocol §6.
2. Cron or not for this channel; if yes: `*/3 * * * * cd ~/Projects/debate && ~/miniconda3/bin/debate watch-once --root collab --config watcher.json` (cd-first is load-bearing).
3. Still pending from Session 1: worktree pruning
   (debate-reliability-v0.3, debate-cwd-v0.3.1, debate-anti-encap); ~/.claude.json backup
   file `~/.claude.json.bak-debate-20260717` can be dropped once the trust setting sticks.
4. Widen `.claude/settings.json` (pytest etc.) when the first *code* review lands.

## Key Decisions
- Roles: Kimi builds, GLM reviews (like-for-like seat replacement).
- History compacted to archive, not deleted — "out of the picture" = out of active config.
- glm debounce 60 s (600 s human window doesn't apply to a machine-only seat).
- No cron installed by this plan — owner's call after the smoke round.
- Pre-publication sanitization: machine refs scrubbed, legal name stays, redaction commit
  over history rewrite (no force-push on a public repo).

## Files Changed
- Committed on `glm-reviewer-seat` (rewritten, 4 commits): collab/ (debate.json,
  PROTOCOL.md, archive/, CHANNEL.md), watcher.example.json, .gitignore,
  .claude/settings.json (generic), plan doc (+GLM review section), examples/glm-kimi.md
  (PATH note), redacted main plan docs + test docstring, this handover.
- Outside repo: `~/.local/bin/glm-agent` (new), `~/.claude.json` (trust flag for this
  workspace; backup `~/.claude.json.bak-debate-20260717`).
