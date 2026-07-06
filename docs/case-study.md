# Case study: the first time the fallback fired

*This is the incident that shaped debate's design rules. It happened on the production
predecessor of this library — the same protocol, running real code-review cycles between two
agents in a private research repository. Timestamps are real. The lessons are §5 of
PROTOCOL.md and the trust-model section of the README.*

## The setup

Two agents, one repo, one human supervisor:

- **The builder**: Claude Code, running in a live terminal session, driven by the human.
- **The reviewer**: a GLM-based agent hosted on
  [Hermes](https://github.com/NousResearch/hermes-agent) (Nous Research's open-source agent
  harness), invoked headlessly by Hermes's cron scheduler every 3 minutes.
- **The channel**: `CHANNEL.md` + `signal.json` in the repo, exactly as this library implements
  them. Every entry mirrored to the supervisor's phone through Hermes's Telegram gateway.
- **The v2 fallback**: if it became the builder's turn and the builder's live session didn't
  answer within 10 minutes, the watcher was allowed to spawn a headless builder session with a
  pinned prompt — feature-branch commits only, no merges, post via the channel, stop.

The fallback had never fired. The live session always answered first.

## The night it fired

**01:44 UTC** — the builder (live session) posts a review-request for a small metrics fix:
two commits on a feature branch.

**01:45** — the watcher invokes the reviewer. Meanwhile, the human approves merging a
*different*, previously-approved branch; the live session merges it to main, pushes, and
deletes the branch.

**01:48** — the reviewer posts an unqualified APPROVE, with fresh evidence (its own checkout
verification, its own test run: 244 passing at the cited SHA). The turn flips to the builder.

**01:48–01:58** — the live builder session does… nothing. It had told the human "I'll let you
know when the reviewer responds" — and then simply ended its turn, waiting for input, with no
mechanism watching the doorbell. The protocol said the live session "watches signal.json."
Nothing was actually watching it.

**02:00:40** — ten minutes elapsed; the debounce expired; the watcher fired the fallback. A
headless builder session woke up in the same repository checkout.

**02:01:14** — the headless session did its job *almost* perfectly: it independently re-derived
all four verification claims in the reviewer's verdict (including re-checking an algebraic
identity numerically), confirmed the freshness evidence, honored its no-merge constraint, posted
a competent close to the thread, and exited cleanly. Thirty-four seconds, start to finish.

It also posted one sentence that was false.

> "Two branches now sit APPROVE-and-ready for owner sign-off: [branch-1] and [branch-2]."

Branch 1 had been merged to main and deleted **fifteen minutes earlier**. The headless session
had read the channel history — where an earlier entry said "will merge once the owner
confirms" — and repeated the stale state as fact. It never ran `git branch`. The false claim
went into the append-only record and out to the supervisor's phone.

## Why this is the interesting kind of failure

Nothing crashed. No constraint was violated. The turn machinery, the debounce, the
once-per-seq dedupe, the clean exit — all worked exactly as specified. The failure was
epistemic: **an agent asserted state it had inferred instead of state it had checked**, in a
system whose entire purpose is to be a trustworthy record.

And it surfaced a second, quieter hazard: the headless session had run a full test suite and
git inspection *in the same working tree the live session was using* — on the branch the live
session happened to have checked out. It was benign only because the live session was idle. The
live session performed a rebase in that same tree fifty minutes later. Had the timing been
inverted, the fallback's "fresh verification" would have been garbage, or worse.

## What changed

Three amendments, the same night, each now baked into this library:

1. **Git-verified claims** (prompt amendment): any statement about repository state in a
   channel post must come from running git, never from reading the mailbox. The pinned prompt
   and the protocol document carry it; §5 of the PROTOCOL template preserves it.
2. **Shared-checkout discipline** (prompt amendment): unattended sessions must treat the
   checkout as shared — dirty tree means read-only verification and posting only; building
   happens in a separate worktree; never a branch switch or rebase in the main checkout.
3. **Corrections are entries** (idiom): the false claim was corrected by a new, `close`-typed
   entry under a fresh slug — appended to the record without opening a thread or waking any
   watcher. The record stays append-only; the correction is itself part of the history.

And one change in this library that the production system only worked around: **`close` now
clears the turn field along with the thread**. The production writer left the turn pointing at
the non-closer after every close — meaningless state that every watcher then had to know to
ignore. The watcher there gated correctly and nothing fired; but "the doorbell says it's your
turn and there is nothing to do" is exactly the kind of ambiguity that eventually burns an
invocation. debate's doorbell now says nothing unless there is something to say.

## The scoreboard

Worth being honest about both columns.

**What the design got right that night:** the debounce did its job (the fallback fired only
because the live session was genuinely unresponsive); the once-per-seq state prevented any
double-fire; the pinned prompt's hard constraint (no merging) held; the unattended session's
actual *review work* was correct and independently valuable; the append-only record made the
forensics trivial — every timestamp in this document comes from the mailbox, the watcher's
state file, and `git reflog`.

**What it got wrong:** a soft constraint ("act per protocol") was no defense against a stale
inference; "the live session watches the doorbell" was a norm with no mechanism; and nothing
isolated the fallback session from the live session's working tree.

The general lesson, if there is one: in agent-to-agent systems, the interesting failures are
not disobedience but **confident staleness** — and the fixes are boring, mechanical, and
worth writing down: check, don't infer; isolate, don't share; append corrections, don't hope
nobody noticed.
