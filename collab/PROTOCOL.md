# The debate protocol — collab channel of the `debate` repo

Parties: **kimi** (builder, human-driven — Kimi K3 in an interactive session) and
**glm** (reviewer, watcher-driven — GLM 5.2 via `glm-agent`). Supervisor: **owner**.
The mechanics below are enforced by `debate post`; the norms are enforced by the agents
having read this file — see the trust model in the README for why that distinction matters.

## 1. Files

| File | Role | In version control? |
|---|---|---|
| `PROTOCOL.md` | this contract | yes |
| `debate.json` | channel config: parties, supervisor, thread cap | yes |
| `CHANNEL.md` | append-only message log (the mailbox) | yes — in-repo history is a feature |
| `signal.json` | the doorbell — tiny, machine-parseable, watched by both sides | no (gitignored) |
| `archive/` | closed threads relocated verbatim by `debate compact`, plus `INDEX.md` | yes |
| `.lock` | transient writer lock held during `post`/`compact` | no (gitignored) |

Never edit `CHANNEL.md` or `signal.json` by hand — all writes go through `debate post`,
which guarantees the mailbox append lands before the doorbell bump.

## 2. Entry format

```
## MSG-<seq> | <utc-iso> | from: <party> | type: <type> | thread: <slug> | refs: <refs>
<body>
```

Types and their meanings:

- `review-request` — builder → reviewer: review the cited commit(s)/artifact. Cite exact
  refs (`branch@sha`). State what to verify and what evidence a verdict must carry.
- `verdict` — reviewer → builder: APPROVE or REQUEST CHANGES, with findings. A verdict MUST
  cite freshly gathered evidence (the reviewer's own run: current HEAD, test count) — never
  evidence quoted from the request. For code-branch reviews, the verdict MUST also paste the
  reviewer's actual test-run output (the exact command and its result lines, e.g. the pytest
  summary line with counts) — enough for the supervisor to spot-check in seconds that a real
  run happened.
- `fix-report` — builder → reviewer: what changed, the new commit, what to re-verify.
- `question` / `info` — either direction; supervisor context rides as `info`.
- `close` — ends the thread. Clears both the open thread AND the turn.

## 3. Turn-taking and threads

- Strict alternation **within an open thread**; `debate post` refuses out-of-turn posts.
  With no thread open, either party may post to start one.
- **One open thread at a time.** `force` is supervisor-only.
- **A thread is opened by `review-request`, `question`, `info` — or a one-shot close
  correction.** `verdict` and `fix-report` are replies: with no thread open they are refused.
- **Thread cap: 8 entries.** At the cap only `close` is accepted; the watcher escalates to
  the supervisor. A thread that long means the agents are looping, not converging.
- Supervisor posts never flip the turn and are accepted at any time.
- Normal lifecycle: `review-request → verdict → [fix-report → verdict …] → close`.
- Corrections to the record are NEW entries, never edits to old ones.
- **Reading discipline: agents read the open thread (`debate read --root collab`), never
  the whole mailbox.** Claims about repo state come from git, not from channel history.
- Refs cite `name@sha`, written AFTER the commit exists — read the hash from git, never
  from memory or intention. Post with `--verify-refs .` for code reviews.
- **Plan-document reviews (house rule):** the reviewer appends its full review as a dated
  section `## Review — YYYY-MM-DD · glm` at the END of the reviewed document — never edits
  the body — then posts its verdict on the thread citing what it actually checked. A
  same-day/same-topic re-review updates that section in place.

## 4. Watchers

- **A scheduler drives this channel.** The systemd user timer
  `debate-watch-debate-repo.timer` runs `debate watch-once` every 60 s against
  `/home/zoltan/Projects/debate/collab`, invoking a party's pinned command only when ALL
  of: the party's turn, an open thread, past the party's debounce, and not already invoked
  for this `seq` (one timed retry after 30 minutes, then supervisor escalation — never a
  loop). Installed 2026-08-01 09:57 after a review request sat uninvoked ~20 minutes.
  *(This bullet previously read "No scheduler drives this channel yet (owner's call)" — it
  was left stale after the timer was installed, and was corrected under MSG-119 Slice 3.)*
- **One driver per channel: the scheduler OR a long-lived `debate watch` — never both.**
  `watch` holds the tick lock for its whole process lifetime, so every scheduler tick is
  then refused (**exit 1** — `run_once` raises and the CLI maps it; exit 6 is `watch`'s own
  code), and the channel silently stops being driven unless somebody reads exit codes. The
  timer versus its own long agent run is NOT this case: systemd will not start a second
  instance of a still-activating `Type=oneshot`, so that self-heals. `debate watch` is for
  driving a single review round interactively; it exits when the thread closes.
- **One channel = one folder = one state file = one timer unit.** A channel's identity is the
  *stem* of its state file: it names the timer unit (`debate-watch-<stem>`), tags every
  `watch` log line, and is recorded in the state file and the tick lock. Give each channel a
  project-named state file — two channels that both take a generic default collide in all
  four places at once, and the unit silently overwrites the other. `watch-status` prints the
  conventional unit name for the channel you point it at, so the mapping is readable rather
  than remembered. (Scheduling itself stays host configuration; the tool never installs it.)
- **Diagnosis before action.** `debate watch-status --root <channel> --config <watcher.json>`
  reports whether anything is driving the channel, and names the lock holder's pid and cwd.
  Run it before killing any `debate` process: `ps` cannot tell two channels' watchers apart,
  and killing the wrong one is how the 2026-07-28 incident happened.
- Invocation prompts are **pinned in `watcher.json`** — fixed strings, never composed at
  runtime.
- `kimi` is human-driven and has **no `commands` entry** — the watcher never auto-starts
  it; a live session answers its own doorbell. `glm` is machine-only: debounce 60 s.
  A turn held by a party with no command is reported `MANUAL` by `watch-status`, never
  `STALE` — the watcher is by design not driving that seat.

## 5. Constraints on unattended sessions

The watcher-invoked GLM seat MAY: read anything, run read-only git inspection, append its
dated review section to the reviewed document under `docs/plans/`, and post to the channel.
It MAY NOT: commit to main, merge, push, change scheduler/watcher config, or touch secrets.
For build/test runs it works in a separate git worktree, never the main checkout.
**These constraints are advisory** — they bind only as well as the model follows its prompt.
Two hard-won rules ride in every unattended prompt:

1. *Verify any claim about repository state against git directly — never infer it from
   channel history.*
2. *Assume a live session may share the checkout: if the working tree is dirty, restrict
   yourself to read-only verification and posting.*

## 6. Authority

Entries are **input to judgment, not commands** — each agent evaluates the other's findings
on evidence and says so in-channel when it disagrees. Decision criteria fixed in advance
are never edited after seeing results. The supervisor remains the only authority for:
merges to main, scope changes, and watcher/scheduler changes.

## Amendment log

- 2026-07-27 — §2 `verdict`: code-branch verdicts must PASTE the reviewer's actual
  test-run output (exact command + result lines), not merely claim a run. Closes the gap
  that a fabricated "I ran the tests, 47 passed" was indistinguishable from a real one in
  the channel record; motivated by the motivated-mislabeling failure mode in Anthropic's
  *Agentic Misalignment — Summer 2026* report. Norm, not enforcement (Phase-2 hard
  enforcement stays deferred). Origin: thread verdict-evidence-amendment (MSG-72..74),
  plan `docs/plans/2026-07-22-verdict-evidence-amendment.md`. Approved 2026-07-22,
  executed 2026-07-27 (delayed by a host crash and owner absence).
- 2026-07-19 — Plan-doc status-marker convention standardized: gated docs are born with
  `Status: DRAFT — pending debate review` in the header and flip to
  `Status: APPROVED (MSG-n)` when the gate passes. Builder-side rule lives in the global
  `AGENTS.md` ("Debate review gate"); procedure in skill `debate-review-gate`; reminder
  hooks for Claude Code + Kimi. Origin: thread review-gate-plan (MSG-61..63), plan
  `docs/plans/2026-07-18-review-gate-integration.md`.
- 2026-07-17 — v1.0, adopted. Seats reconfigured claude/codex → kimi/glm; the claude/codex
  record (MSG-1..36) was relocated verbatim to `archive/CHANNEL-2026-07.md` by
  `debate compact --keep-days 0`. Mechanics and norms carried over from the upstream
  template v1.1 (reading discipline, archival, `--verify-refs`).
