# debate

**A tiny file-based protocol for two AI agents that review each other's work — with enforced
turns, an append-only audit log, and a human who can always see everything.**

Zero dependencies. Two files. One rule: nobody posts out of turn.

## The problem

Multi-agent frameworks assume one orchestrator owns all the agents in one runtime. Reality is
messier: you have Claude Code in a terminal *and* some other agent on another harness — different
vendors, different processes, maybe different machines — and you want one to **build** and the
other to **review** without you being the copy-paste courier between them.

debate is the smallest thing that solves this: the agents exchange messages through two files
in a shared directory (a git repo works beautifully — the audit log becomes history you can
diff), and a dumb watcher wakes whichever agent's turn it is. No framework, no server, no queue,
no API keys. If your agent can be invoked from a shell and can read files, it can hold up its
end of a review.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/flow-dark.svg">
    <img alt="Two agents exchange posts through a shared channel (CHANNEL.md, the append-only record, plus signal.json, the doorbell). A dumb cron watcher polls the doorbell and wakes whichever agent's turn it is with a pinned, debounced prompt. Every entry is mirrored to the human supervisor, who owns merges and is never the courier." src="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/flow-light.svg" width="840">
  </picture>
</p>

## How it works

- **`CHANNEL.md`** — the mailbox. Append-only, human-readable, git-diffable. Every message has a
  sequence number, sender, type (`review-request`, `verdict`, `fix-report`, `question`, `info`,
  `close`), a thread slug, and refs (e.g. `branch@commit`).
- **`signal.json`** — the doorbell. Five fields (`seq`, `turn`, `thread`, `last_entry`,
  `updated_at`). Watchers poll this, never the mailbox.
- **`debate post`** — the only writer, and the place the protocol is *enforced* rather than
  requested: out-of-turn posts are refused, one thread open at a time, thread caps stop runaway
  loops, and the mailbox append always lands before the doorbell bump (so a watcher firing on
  `seq` never reads a half-written entry).
- **`debate watch-once`** — one tick of a deliberately dumb watcher. Run it from cron every few
  minutes: it mirrors new entries to wherever you already look, and if it's an agent's turn on an
  open thread, invokes that agent's pinned command. No LLM runs when nothing changed.

## Quickstart

```bash
pip install debate            # or just vendor the two modules; they're stdlib-only

debate init --root ./collab --parties claude,glm --supervisor owner

# The builder opens a review thread:
debate post --root ./collab --from claude --type review-request \
    --thread feature-x --refs feature-x@abc123 --body "Please review commit abc123: ..."

# The reviewer replies (their harness invokes this after reading the thread):
debate post --root ./collab --from glm --type verdict \
    --thread feature-x --refs feature-x@abc123 --body "APPROVE — verified: 27 tests pass at abc123."

# Whoever acted last closes:
debate post --root ./collab --from claude --type close --thread feature-x --body "Merged. Closing."
```

Wire the watcher to a scheduler with a config that pins each agent's invocation:

```json
{
  "state_path": "/somewhere/outside/the/channel/watcher-state.json",
  "commands": { "claude": ["claude", "-p", "{prompt}"] },
  "prompts":  { "claude": "It is your turn on the review channel at ./collab. Read the open thread, act, post via debate, then stop." },
  "debounce_seconds": { "claude": 600 },
  "retry_seconds": 1800
}
```

```bash
debate watch-once --root ./collab --config watcher.json   # cron this every ~3 minutes
```

A party without a `commands` entry is never invoked — that's how a human-driven side works: the
human's live session answers the doorbell itself, and the watcher only covers for it when it
doesn't (see `debounce_seconds`).

## The trust model — read this before running agents unattended

Be precise about what is enforced and what is merely requested:

- **Enforced (hard):** turn order, one-open-thread, thread caps, entry format, write-then-signal
  ordering. These live in `post`; an agent that misbehaves gets refused, not warned.
- **Advisory (soft):** everything an agent does *outside* the mailbox. "Don't push to main",
  "don't touch config" — if you put those in an agent's pinned prompt, you are trusting the
  model to comply. In our production use this failed exactly once and exactly as theory
  predicts: an unattended agent made a **true-at-some-point but stale claim** about repository
  state because it inferred state from channel history instead of checking. The protocol can
  force *when* an agent speaks; it cannot force what the agent says to be correct.

Mitigations that earn their keep: pin prompts in config (never compose them at runtime), require
agents to cite fresh evidence (commit SHA + test count) in verdicts, gate merges on the *human*
reading the mirrored verdict, and give unattended sessions an isolated worktree instead of your
live checkout. The [case study](docs/case-study.md) walks through the real incident.

## Design rules (each one paid for in production)

1. **Gate on an open thread, not the turn field.** After a `close`, `turn` means nothing.
   debate clears both on close; the watcher checks both anyway.
2. **Once per seq.** An invocation that produced no reply gets one timed retry, then a
   supervisor escalation. Two agents in a refusal loop burn money forever; the cap is the brake.
3. **Debounce before invoking.** A human-driven session may be about to answer; the fallback
   should be a fallback.
4. **The watcher's memory lives outside the channel.** Its state file is not part of the shared
   record and never collides with a fresh clone.
5. **Supervisor posts don't take a turn.** The human can interject at any point without
   breaking the agents' alternation.
6. **The mailbox is the record.** If it didn't happen in `CHANNEL.md`, it didn't happen — and
   corrections are new entries (a `close`-typed post with a fresh slug drops a correction into
   the record without opening a thread), never edits.

## Why not just…

- **GitHub PRs + a review bot?** Works great *if* both agents live where your forge is. debate
  is forge-independent, works fully offline/local, and round-trips in seconds on a cron tick
  without webhooks or API tokens. (If you have GitHub and one vendor's bot, use them.)
- **AutoGen / LangGraph / CrewAI?** Those orchestrate agents they own, in-process. debate
  coordinates agents that *nobody* jointly owns — different vendors, different harnesses,
  different lifetimes — and leaves a human-auditable trail as a first-class artifact.
- **A message queue?** You'd be trading two greppable files and `git log` for a broker. The
  audit log *is* the point.

## Limitations, honestly

- **Two parties.** Turn alternation between exactly two named agents (plus a supervisor) is a
  feature, not a to-do: a review needs a builder and a reviewer. N-party consensus is a
  different protocol.
- **Polling.** The doorbell is designed to be cheap to poll on a minutes-scale cron. If you need
  sub-second latency, this is not your transport.
- **A tolerated race.** Two agents may open *different* new threads near-simultaneously when
  none is open. With minutes-scale polling the window is tiny, and the supervisor untangles the
  rare collision; single-writer locking would cost more than it buys.
- **Reference implementation.** Extracted from a working production setup, generalized, and
  tested — but young. Read the code; it's ~600 lines including the CLI.

## Field notes

The production predecessor ran real code-review cycles between **Claude Code** (the builder,
in a live terminal) and a GLM-based reviewer hosted on
[Hermes](https://github.com/NousResearch/hermes-agent), Nous Research's open-source agent
harness — whose cron scheduler also ran the watcher and mirrored every entry to the
supervisor's phone through its Telegram gateway. That's the intended shape: debate doesn't run
your agents; whatever harnesses you already have, do. A typical review round-tripped in about
five minutes of wall clock, most of it the reviewer independently re-running the test suite.
The one night it went sideways is [the case study](docs/case-study.md).

## The name

Parliamentary, not adversarial: structured turns, one motion on the floor at a time, and
everything said is on the record — `CHANNEL.md` is the hansard. (If you arrived from the
"AI safety via debate" literature: this is not the formal debate game with opposing advocates
before a judge — it's review correspondence with teeth.)

## License

MIT
