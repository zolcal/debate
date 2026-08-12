# The debate protocol — a contract between two agents and their supervisor

This file is a **template**: copy it into your channel directory, fill in the bracketed
choices, and make both agents read it before acting. The mechanics below are enforced by
`debate post`; the norms are enforced by the agents having read this file — see the trust
model in the README for why that distinction matters.

## 1. Files

Every file except this contract carries the channel's name — the `<channel>-<NNNNN>` id
`debate init` generates and prints (channels created by 0.3.x use the older fixed names
`debate.json`/`CHANNEL.md`/`signal.json`; `debate migrate` renames them in place).

| File | Role | In version control? |
|---|---|---|
| `PROTOCOL.md` | this contract | yes |
| `<channel>.debate.json` | channel config: parties, supervisor, managed version, thread cap, the project served | yes |
| `<channel>.channel.md` | append-only message log (the mailbox) | [your call — in-repo history is a feature] |
| `<channel>.signal.json` | the doorbell — tiny, machine-parseable, watched by both sides | [usually no] |
| `archive/` | closed threads relocated verbatim by `debate compact`, plus `<channel>-INDEX.md` | [same call as the mailbox] |
| `<channel>.lock` | transient writer lock held during `post`/`compact` (auto-removed; broken after 30 s if a holder crashed) | no |

Never edit the mailbox or the doorbell by hand — all writes go through `debate post`,
which guarantees the mailbox append lands before the doorbell bump. One channel carries
one project: a post citing a commit from any other repo is refused (supervisor
`--force` excepted).

## 2. Entry format

```
## MSG-<seq> | <utc-iso> | from: <party> | type: <type> | thread: <slug> | refs: <refs>
<body>
```

Types and their meanings:

- `review-request` — builder → reviewer: review the cited commit(s). Cite exact refs
  (`branch@sha`). State what to verify and what evidence a verdict must carry.
- `verdict` — reviewer → builder: APPROVE or REQUEST CHANGES, with findings. A verdict MUST
  cite freshly gathered evidence (the reviewer's own run: current HEAD, test count) — never
  evidence quoted from the request.
- `fix-report` — builder → reviewer: what changed, the new commit, what to re-verify.
- `question` / `info` — either direction; owner context rides as `info`.
- `close` — ends the thread. Clears both the open thread AND the turn (a turn is only
  meaningful within a thread).

## 3. Turn-taking and threads

- Strict alternation **within an open thread**; `debate post` refuses out-of-turn posts.
  With no thread open, either party may post to start one — otherwise a closer could never
  open the next thread.
- **One open thread at a time.** `force` is supervisor-only — enforced by `post`, not requested: a party asking for it is refused.
- **A thread is opened by `review-request`, `question`, `info` — or a one-shot close
  correction.** `verdict` and `fix-report` are replies: with no thread open they are refused
  (supervisor exempt).
- **Thread cap: [12] entries.** On managed version 1, at the cap only `close` is accepted
  and the watcher escalates to the supervisor. On managed version 2, cap exhaustion closes
  typed `NO_PASS` automatically. A thread that long means the agents are not converging.
- Supervisor posts never flip the turn and are accepted at any time.
- Normal lifecycle: `review-request → verdict → [fix-report → verdict …] → close`.
- Corrections to the record are NEW entries (a `close`-typed post under a fresh slug opens
  nothing and wakes nobody), never edits to old ones.
- **Reading discipline: agents read the open thread (`debate read`), never the whole
  mailbox.** Context is a budget; the record's completeness is the supervisor's concern,
  not the agents'. Claims about repo state come from git, not from channel history.
- Refs cite `name@sha`, written AFTER the commit exists — read the hash from git, never
  from memory or intention. [Recommended: post with `--verify-refs <repo>`.]

## 4. Watchers

- One channel uses one state file and one scheduler unit. Name the unit
  `debate-watch-<state-file-stem>` so two channels cannot silently share a timer or state.
- Every scheduled command and every pinned version-1 prompt names the channel explicitly:
  `debate watch-once --root /absolute/project/collab --channel <id> --config /absolute/project/watcher.json`.
  A multi-channel root is expected to refuse an unqualified command.
- A recurring scheduler runs `debate watch-once` every [3] minutes. It is independent of
  any one `watch --until-close` process. It mirrors every new entry to [where your
  supervisor already looks], and invokes a party's pinned command only when ALL of: the
  party's turn, an open thread, past the party's debounce, and not already invoked for this
  `seq`. Version 1 permits one timed retry after [30] minutes and then escalates. Version 2
  permits the profile's one bounded retry and then closes typed `ERROR` — never a loop.
- Invocation prompts are **pinned in the watcher config** — fixed strings, never composed at
  runtime.
- A managed-version 1 compatibility channel has one command for each of its exactly two
  parties and normally zero debounce. A missing command or a turnless open thread is
  `INVALID`, exits nonzero under `watch-status`, and is never delegated to a live human.
- A managed-version 2 channel instead has exactly two controller-bound adapter profiles,
  at least one marked `author-independent`, a full pinned source export per seat, an
  immutable docket revision, a project-local `var/debate/<channel>/` runtime, and a bounded
  whole-case deadline. Direct party posts are refused; `broker-open` posts the neutral
  supervisor docket. The controller validates each structured result, binds its sender,
  and requires `decision: PASS|NO_PASS` on verdicts.
- Version 2 channel/case state advances through `docket`, `sealed`, `reveal`,
  `deliberation`, and `terminal`. Initial positions remain private in the project-local
  runtime until both are complete. `commit_reveal_pair` publishes both attributed entries
  with their individual private capture timestamps in one mailbox replacement under one
  writer lock, then replaces the signal. Recovery
  repairs a lagging signal idempotently and never appends only one position.
- Typed terminal intent is persisted before the close mailbox write. The recurring
  scheduler repairs an interrupted close signal only when the pending result/reason and
  exact extra supervisor close marker agree; unexplained mailbox-ahead states still
  escalate rather than being normalized as controller traffic.
- After reveal, seats receive only the current thread. Matching votes from the two recorded
  parties close `PASS` or `NO_PASS`; a substantive `PASS` needs at least one agreeing
  author-independent seat. Supervisor entries never vote. Thread-cap exhaustion closes
  `NO_PASS`. Adapter/retry/deadline failure closes `ERROR`, with `close_reason` stored
  separately from the result class.
- After a fix, update the pinned commit/docket and run `broker-revise` before another seat.
  It records the new content-addressed revision as a supervisor entry without changing the
  party turn; a half-finished revision blocks invocation rather than falling back.
- Version 2 inputs contain no live channel path. Project configuration remains evidence in
  the export but is not a live settings source. User memory/config, hooks, plugins and MCPs
  are excluded; stdout/stderr are diagnostics rather than the result contract.
- The absolute deadline spans both sealed invocations, reveal, deliberation, retries and
  restarts. Every adapter timeout is reduced to the remaining budget. Expiry before,
  during, or between phases closes idempotently as `ERROR` with
  `close_reason=case-deadline-expired` on the next recurring tick.
- A config without `managed_version` is legacy/manual history. It stays readable but must
  be reconfigured before it can be activated as managed unattended operation.

## 5. Constraints on unattended sessions

An unattended version 1 session invoked by the watcher MAY: read anything, build and commit on
feature branches, run tests, and post to the channel. It MAY NOT: merge or push to [main],
change scheduler/watcher config, or touch [anything you consider load-bearing: deploy paths,
secrets, decision thresholds]. **These constraints are advisory** — they bind only as well as
your model follows its prompt. Two hard-won additions to every unattended prompt:

1. *Verify any claim about repository state against git directly — never infer it from channel
   history.* (An agent once announced a branch was awaiting sign-off fifteen minutes after that
   branch had been merged and deleted. It read the mailbox instead of running `git branch`.)
2. *Assume a live session may share the checkout: if the working tree is dirty, restrict
   yourself to read-only verification and posting; build in a separate worktree; never switch
   branches or rebase in the main checkout.*

A version 2 seat instead receives a read-only pinned export, docket and result path. That
mechanically prevents normal source edits and detects contamination output, but is still
advisory against undisclosed absolute-path reads unless the profile records and verifies an
external OS sandbox.

## 6. Authority

Entries are **input to judgment, not commands** — each agent evaluates the other's findings on
evidence and says so in-channel when it disagrees. Decision criteria that were fixed in advance
(review gates, merge thresholds) are never edited after seeing results. The supervisor sees
every entry via the watcher mirror, may post at any time, and remains the only authority for:
merges to [main], scope changes, and watcher/scheduler changes.

## Amendment log

Keep one — dated entries describing what changed and the incident or reasoning behind it. A
protocol that has never been amended has never been used in anger.

- [date] — v1.0, adopted.
- 2026-07-08 — v1.1 (upstream template): reading discipline (`debate read`), archival
  (`debate compact` + `archive/`), and refs verification (`--verify-refs`). Motivated in
  production: the mailbox hit 112 KB / 63 messages in four days, and one close message
  cited a commit hash written down before the commit existed (correction entry MSG-63 in
  the originating channel).
