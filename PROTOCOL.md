# The debate protocol — a contract between two agents and their supervisor

This file is a **template**: copy it into your channel directory, fill in the bracketed
choices, and make both agents read it before acting. The mechanics below are enforced by
`debate post`; the norms are enforced by the agents having read this file — see the trust
model in the README for why that distinction matters.

## 1. Files

| File | Role | In version control? |
|---|---|---|
| `PROTOCOL.md` | this contract | yes |
| `debate.json` | channel config: parties, supervisor, thread cap | yes |
| `CHANNEL.md` | append-only message log (the mailbox) | [your call — in-repo history is a feature] |
| `signal.json` | the doorbell — tiny, machine-parseable, watched by both sides | [usually no] |

Never edit `CHANNEL.md` or `signal.json` by hand — all writes go through `debate post`,
which guarantees the mailbox append lands before the doorbell bump.

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
- **One open thread at a time.** `force` exists for supervisor-directed exceptions only.
- **Thread cap: [8] entries.** At the cap only `close` is accepted; the watcher escalates to
  the supervisor. A thread that long means the agents are looping, not converging.
- Supervisor posts never flip the turn and are accepted at any time.
- Normal lifecycle: `review-request → verdict → [fix-report → verdict …] → close`.
- Corrections to the record are NEW entries (a `close`-typed post under a fresh slug opens
  nothing and wakes nobody), never edits to old ones.

## 4. Watchers

- A scheduler runs `debate watch-once` every [3] minutes. It mirrors every new entry to
  [where your supervisor already looks], and invokes a party's pinned command only when ALL of:
  the party's turn, an open thread, past the party's debounce, and not already invoked for this
  `seq` (one timed retry after [30] minutes, then a supervisor escalation — never a loop).
- Invocation prompts are **pinned in the watcher config** — fixed strings, never composed at
  runtime.
- A live human-driven session answers its own doorbell; the watcher's trigger is the fallback.
  Recommended debounce for a human-driven party: [10] minutes.

## 5. Constraints on unattended sessions

An unattended agent session invoked by the watcher MAY: read anything, build and commit on
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
