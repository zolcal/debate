# Case study: the first time the fallback fired

*This is the incident that shaped debate's design rules. It happened on the production
predecessor of this library — the same protocol, running real code-review cycles between two
agents in a private research repository. Timestamps are real. The lessons are §5 of
PROTOCOL.md and the trust-model section of the README.*

## The setup

Two agents, one repo, one human supervisor:

- **The builder**: Claude Code, running in a live terminal session, driven by the human.
- **The reviewer**: a GPT-5.5 agent (authenticated through an OpenAI Codex subscription)
  hosted on [Hermes](https://github.com/NousResearch/hermes-agent) (Nous Research's
  open-source agent harness), invoked headlessly by Hermes's cron scheduler every 3 minutes.
- **The channel**: `CHANNEL.md` + `signal.json` in the repo (the 0.3-era fixed filenames; since 0.4 the files carry a per-channel id), exactly as this library implements
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

## Epilogue — the fixes became machinery (v0.5)

The three amendments above started life as prompt text and an idiom. As of 0.5's brokered
mode, each has a harder home:

1. **Git-verified claims** stayed cultural for what an agent *says* — no tool can force a
   sentence to be true. But the surface for confident staleness shrank structurally: a
   brokered seat works inside a pinned read-only export where the reviewed commit is the
   only repository state there is — no mailbox history to repeat, no `git branch` to have
   skipped, git deliberately unreachable — and its verdict is a typed, schema-checked
   result carrying provenance hashes rather than free prose.
2. **Shared-checkout discipline** stopped being discipline. Every seat gets its own
   read-only export at a full 40-character commit, its own project-local HOME, temp and
   build paths, an allowlisted environment, and a Git ceiling. The live tree the 02:01
   session walked into no longer exists for an unattended seat to find.
3. **Corrections are entries** is unchanged, and needs to be nothing more.

The scoreboard's quieter column also got its mechanism. "The live session watches the
doorbell" was a norm nobody enforced; in brokered mode a controller owns every turn under
one absolute whole-case deadline and closes with a typed outcome — `PASS`, `NO_PASS`, or
`ERROR` with the reason recorded — instead of going silent. And the machinery adds one
protection this incident never surfaced: both seats' first positions are captured sealed
and revealed as a pair, so neither can anchor its opening judgment on the other.

Honesty about the boundary, one more time: this is strong protection against *accidental*
contamination, not a claim that a same-user process is hostile-code safe. The isolation is
advisory — read-only permissions, a clean environment, a Git ceiling, canary checks — and
a sufficiently determined same-user process could still traverse to host paths its CLI
sandbox permits. The claims above are about removing the paths an honest agent stumbles
down, which is what this incident was.

Fittingly, the machinery's first production acts were reviewing this repository itself:
the merge that shipped it and the 0.5 release you are reading about both passed through
sealed brokered cases in the repository's own channel record.
