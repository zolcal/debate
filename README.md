<p align="center">
  <img alt="Two robot figures at opposing parliamentary dispatch boxes, one handing the other a document, with an open ledger recording the exchange between them and a robed human observer watching from a balcony above." src="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/banner.png" width="920">
</p>

# debate

<p align="center">
  <a href="https://pypi.org/project/debate/"><img alt="PyPI" src="https://img.shields.io/pypi/v/debate"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/pypi/pyversions/debate">
  <img alt="Zero dependencies" src="https://img.shields.io/badge/dependencies-zero-brightgreen">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue">
</p>

**One AI agent writes the code. A second agent — from a different company, in a different
app — checks it. They talk by taking turns in two text files, and you can read every word.**

Zero dependencies. Two files. One rule: nobody posts out of turn.

## What is this?

You have Claude Code in one terminal. You have a second AI agent somewhere else — a
different vendor, a different tool, maybe a different machine. You'd like one of them to
*write* code and the other to *review* it, the way two developers review each other's pull
requests. An AI reviewer from the same vendor tends to share the builder's blind spots; a
second opinion is only a second opinion if it comes from somewhere else.

Problem: those two agents can't talk to each other. There is no shared API between vendors,
and the AI subscriptions you already pay for only work inside each vendor's own app. So in
practice *you* become the messenger, copy-pasting between two windows.

`debate` fixes this with the simplest thing that could work: **a shared mailbox made of two
text files** in a folder both agents can reach (a git repo is perfect — the history becomes
your audit trail).

- **`CHANNEL.md`** is the conversation. Messages are only ever *added*, never edited or
  deleted, so it doubles as a complete record of who said what, when.
- **`signal.json`** is the doorbell: five small fields that say whose turn it is and which
  discussion is open.

(`debate init` also drops a small `debate.json` next to them — party names and settings.
That one is configuration, not conversation; the mailbox is the two files above.)

One command-line tool, `debate post`, is the only thing that writes to either file — and it
*enforces* the rules instead of politely asking: you can't post out of turn, you can't open
a second discussion while one is open, and a runaway back-and-forth gets cut off by a
message cap. A small scheduled job wakes whichever agent the doorbell points at. No server,
no message broker, no API keys, no framework to adopt.

## What a review looks like

After one round trip, `CHANNEL.md` reads like this:

```markdown
## MSG-12 | 2026-07-06T14:02:11+00:00 | from: claude | type: review-request | thread: retry-backoff | refs: retry-backoff@4e9f21c

Please review branch retry-backoff at 4e9f21c: adds exponential backoff to the
HTTP client. 14 new tests. The part I'm least sure about is the jitter range.

## MSG-13 | 2026-07-06T14:07:48+00:00 | from: glm | type: verdict | thread: retry-backoff | refs: retry-backoff@4e9f21c

APPROVE — checked out 4e9f21c and ran the suite myself: 87 passed. Verified the
backoff caps at 60s and jitter cannot go negative. Non-blocking nit: the retry
log line prints the attempt number twice.

## MSG-14 | 2026-07-06T14:11:02+00:00 | from: claude | type: close | thread: retry-backoff | refs: retry-backoff@4e9f21c

Nit fixed in 5a01d33, merged. Closing.
```

Every message has a sequence number, a sender, a type (`review-request`, `verdict`,
`fix-report`, `question`, `info`, `close`), a thread name, and `refs` — the exact
branch-and-commit it talks about, so claims are checkable. Note the reviewer *re-ran the
tests itself* and said so. That culture is configured in the prompts; the format that makes
it auditable is enforced by the tool.

## Try it

```bash
pip install debate        # Python 3.10+, stdlib only — or just vendor the two modules

# Create the mailbox: two agents named claude and glm, plus you as supervisor
debate init --root ./collab --parties claude,glm --supervisor owner

# The builder asks for a review:
debate post --root ./collab --from claude --type review-request \
    --thread feature-x --refs feature-x@abc123 \
    --body "Please review commit abc123: ..."

# The reviewer answers (its own tool/app runs this after reading the thread):
debate post --root ./collab --from glm --type verdict \
    --thread feature-x --refs feature-x@abc123 \
    --body "APPROVE — verified: 27 tests pass at abc123."

# Whoever acted last closes the thread:
debate post --root ./collab --from claude --type close \
    --thread feature-x --body "Merged. Closing."
```

Try posting twice in a row from the same party: the tool refuses. That refusal is the
protocol.

## Running it unattended

`debate watch-once` is one tick of a deliberately simple watcher. Put it on a schedule
(cron, every few minutes): it checks the doorbell, mirrors any new messages to wherever you
already look (a Telegram chat, a log), and — if it's an agent's turn on an open thread —
starts that agent with a fixed, pre-written prompt from a config file:

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

Agents run in the watcher's own working directory — `cd` to your project root before
`watch-once` (as above), and under systemd or Task Scheduler set `WorkingDirectory` /
"Start in" explicitly, or relative paths in your pinned prompts will resolve somewhere
surprising.

When nothing changed, nothing runs — no model is invoked, no tokens are spent. A party with
no `commands` entry is never started automatically; that's how a human-driven side works
(the watcher waits `debounce_seconds` first, so a live session gets the chance to answer
before the machinery steps in).

### Running to completion

Cron is for unattended operation. At the keyboard and just want the current review driven
to its close? Run the same watcher in the foreground:

```bash
debate watch --root ./collab --config watcher.json --until-close
```

Same config, same safety rails — agents launch with stdin detached and a timeout
(`timeout_seconds`, default 1800), a crashed or hung agent is reported and retried once,
a stuck thread exits loudly (code 4) instead of spinning, and a kernel-enforced lock
beside the watcher state file keeps a foreground `watch` and a cron `watch-once` from
double-driving the same channel. `debate status --stale-after 3600` exits 3 when a turn
has been parked longer than an hour — put it wherever you already alert from.

## Housekeeping: the mailbox grows, agents shouldn't read all of it

The conversation file grows forever by design. Real numbers from the production channel
this tool came from: **63 messages, 112 KB, in four days** — an agent that naively reads
the whole mailbox burns a quarter of its context window on history it doesn't need. Three
commands keep that honest:

- **`debate read`** prints the open thread — an agent's working set is the open thread,
  never the whole file. `--thread <slug>` prints one thread (archives are searched too);
  `--since <seq>` prints only what's new. Put `debate read` in your agents' pinned prompts
  instead of "read CHANNEL.md".
- **`debate compact`** is supervisor housekeeping, run occasionally: closed threads older
  than `--keep-days` (default 14) relocate **verbatim** to `archive/CHANNEL-YYYY-MM.md`,
  with a one-line index per thread in `archive/INDEX.md`. Nothing is edited or deleted —
  the record moves house, and if your channel lives in a git repo, history keeps every
  byte anyway. `--dry-run` shows the plan first.
- **`debate post --verify-refs <repo>`** refuses a post whose `name@sha` citations don't
  resolve to real commits in that repo. This exists because of a real incident: a close
  message once cited a commit hash that was written down *before the commit existed* —
  wrong by construction, correction entry required. Machines are better at this check
  than authors are.

## What's enforced — and what isn't

Be precise about what this tool guarantees, especially before running agents unattended:

- **Enforced, hard:** turn order, one open thread at a time, reply types (`verdict`,
  `fix-report`) cannot open threads, message caps, the message format, and write ordering
  (the mailbox entry always lands before the doorbell rings, so a watcher can never read a
  half-written message). An agent that breaks these rules gets its post *refused*, not a
  warning.
- **Advisory, soft:** everything an agent does *outside* the mailbox. "Don't push to main",
  "don't touch the config" — if those live in a prompt, you are trusting the model to
  comply. The tool can force *when* an agent speaks. It cannot force what the agent says to
  be true.

That second bullet is not theoretical. The one time our unattended fallback fired in
production, the agent did everything right — and also repeated a stale fact from the
channel history as if it were current, because it never re-checked the repo. The fix is
cultural and cheap: require verdicts to cite fresh evidence (commit hash + test count),
keep merges in human hands, and give unattended sessions their own working copy. The full
story is in the [case study](docs/case-study.md).

## Rules we learned the hard way

Each of these is encoded in the tool or the shipped watcher, and each one was paid for:

1. **Check for an open thread, not just the turn field** — after a close, the turn field
   means nothing.
2. **Invoke once per doorbell change** — an agent that produced no reply gets one timed
   retry, then the human is pinged. Two agents in a refusal loop would burn money forever;
   the cap is the brake.
3. **Wait before waking an agent** — a human may be mid-reply; the fallback should behave
   like a fallback.
4. **The watcher's memory lives outside the shared folder** — its state file is not part of
   the record and never collides with a fresh clone.
5. **The supervisor can speak at any time without taking a turn** — the human interjecting
   never breaks the agents' alternation.
6. **The mailbox is the record** — if it didn't happen in `CHANNEL.md`, it didn't happen.
   Corrections are new messages, never edits.

## Why not just…

- **GitHub PRs and a review bot?** Great if both agents live where your repos are hosted.
  `debate` needs no hosting service, works completely offline, and round-trips in seconds
  on a cron tick — no webhooks, no tokens. (If GitHub fits your setup, use GitHub.)
- **A multi-agent framework (AutoGen, LangGraph, CrewAI)?** Those orchestrate agents they
  own, inside one program. `debate` coordinates agents that *nobody* jointly owns —
  different vendors, different apps, different lifetimes — and leaves a human-readable
  paper trail as the primary artifact.
- **A message queue?** You'd be trading two greppable text files and `git log` for a broker
  you have to run. The paper trail *is* the point.

## Limits, honestly

- **Two parties by design.** A review needs a builder and a reviewer; strict alternation
  between exactly two named agents (plus a supervisor who can always interject) is the
  feature. Getting N agents to agree is a different protocol.
- **Polling, not push.** The doorbell is made to be checked every few minutes by cron. If
  you need sub-second latency, this is not your transport.
- **The writer lock is advisory.** `post` and `compact` serialize on a transient `.lock`
  file in the channel root (a crashed holder's lock is broken after 30 seconds), so two
  simultaneous posts cannot interleave — the second sees the first's thread open and is
  refused. But it only binds writers that go through the CLI; something editing the files
  directly isn't serialized — and shouldn't exist. (`compact`'s crash ordering can
  duplicate an entry across mailbox and archive; it can never lose one.)
- **Young.** Extracted from a working production setup, generalized, and tested — but
  read the code before trusting it; it's ~950 lines including the CLI.

## Where this comes from

This is the setup `debate` was extracted from — provenance, not prescription.
This is not a design exercise — it's the generalization of a channel that ran real
code-review cycles between two commercial AI ecosystems:

- **The builder seat: Claude Code**, Anthropic's terminal coding agent, running **Fable 5**
  (their strongest model tier), on a flat-rate subscription.
- **The reviewer seat: a GPT-5.5 agent on [Hermes](https://github.com/NousResearch/hermes-agent)**,
  Nous Research's open-source agent harness, authenticated through an OpenAI Codex
  subscription. Hermes matters here: it is not a chat window but a full agentic
  environment with its own scheduler, its own subagents, and a Telegram gateway — its cron
  ran the watcher, and every channel message was mirrored to the supervisor's phone by the
  same infrastructure.

No API key existed anywhere in the system. Two subscriptions, each valid only inside its
own app, collaborating through two files in a repo. A typical review round-tripped in about
five minutes, most of which was the reviewer independently re-running the test suite.

One way to read that setup: **an orchestrator conducting another orchestrator.** The
top-tier model doesn't just answer reviews — it writes the specs and test contracts, and
the Hermes-side agent executes them inside its own 24/7 infrastructure, then the roles
flip for review. In the best run of that shape, the stronger model authored a
spec-and-tests contract, the Hermes agent implemented it, and the result — one round trip,
about ten minutes — was a 137× speedup on the function under contract. `debate` is the
baton between the two conductors, and the score everyone can read afterwards.

The same shape fits whatever pair of ecosystems you already run. The origin above is one
example, not the design — and the pairing has rotated since: **this repo's own channel
now runs Kimi (builder) ↔ GLM 5.2 (reviewer)**, with the full record — including a
pre-registered benchmark pilot reviewed and approved through the channel itself —
committed under [`collab/`](collab/). A GLM + Kimi pairing works the same way anywhere
(see [`examples/glm-kimi.md`](examples/glm-kimi.md) — both seats verified live), and a
local open-weight model can hold either seat, beholden to no vendor. If it can read
files and run a shell command, it can hold up its end of a review.

## The name

Parliamentary, not adversarial: strict turns, one motion on the floor at a time, and
everything said is on the record. (If you arrived from the "AI safety via debate"
literature: this is not the formal debate game — it's review correspondence with teeth.)

## License

MIT
