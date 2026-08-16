<p align="center">
  <img alt="A parliamentary chamber with three robots and one human. Two robots debate from opposing dispatch boxes across an open ledger on the central lectern. A third robot sits at a desk beneath the balcony, passing a document up toward the robed human supervisor, who leans over the railing toward it - the author and the owner working as a pair while the two seats debate." src="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/banner.png" width="920">
</p>

# debate

<p align="center">
  <a href="https://pypi.org/project/debate/"><img alt="PyPI" src="https://img.shields.io/pypi/v/debate"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/pypi/pyversions/debate">
  <img alt="Zero dependencies" src="https://img.shields.io/badge/dependencies-zero-brightgreen">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue">
</p>

**One AI agent builds the work at your side. When it is ready, two more — from different
companies, in different apps — debate it before it lands. They argue by taking turns in
two text files, and you can read every word.**

Zero dependencies. Two files. Three agents, one human. One rule: nobody posts out of turn.

## What is this?

You have an AI agent that builds with you all day — specs, code, fixes. What it cannot
give you is a real second opinion on its own work. `debate` adds that: when a piece of
work is ready, two OTHER agents — different vendors, different tools, deliberately
neither of them the author — take seats on a channel and debate it, the way two
reviewers argue over a pull request neither of them wrote.

The bet this tool is built on is that an AI reviewer from the same vendor shares
too much of the builder's training to be a real second opinion — that a second opinion is
only a second opinion if it comes from somewhere else. That is a hypothesis, not a measured
result. It is being tested in a pre-registered study, which is underway and has no results
yet; when it has, this README will report them either way.

Problem: those two reviewers can't talk to each other. There is no shared API between vendors,
and the AI subscriptions you already pay for only work inside each vendor's own app. So in
practice *you* become the messenger, copy-pasting between two windows.

`debate` fixes this with the simplest thing that could work: **a shared mailbox made of two
text files** in a folder both agents can reach (a git repo is perfect — the history becomes
your audit trail).

- **`<channel>.channel.md`** is the conversation. Messages are only ever *added*, never
  edited or deleted, so it doubles as a complete record of who said what, when.
- **`<channel>.signal.json`** is the doorbell: five core fields that say whose turn it
  is and which discussion is open. Brokered cases also persist their phase, absolute
  deadline, and typed terminal result there.

`<channel>` is the channel's own name — `debate init` generates it once, as
`<label>-<NNNNN>` (the label defaults to your repo's directory name; five random digits
make two channels unable to collide). Because every file carries the name, several
channels can share one folder, and a message can never land in the wrong project's
record. (`init` also drops `<channel>.debate.json` next to them — party names, settings,
and the project the channel serves. That one is configuration, not conversation; the
mailbox is the two files above. Channels created by 0.3.x use the older fixed filenames
`CHANNEL.md`/`signal.json`/`debate.json` — they keep working, but posting to them is
deprecated since 0.5; `debate migrate` renames one in place, byte-identically.)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/flow-dark.svg">
    <img alt="The channel is two files in a shared directory: an append-only record that acts as the hansard, and a doorbell holding sequence number, whose turn it is, and which thread is open. The author agent and the owner build the work together outside both seats and deliver the branch plus a review-request into the channel. Two debating seats - deliberately from different vendors, independent of the author - each post and read through one writer that enforces turns, one open thread at a time, and message caps. A dumb cron watcher polls the doorbell every minute, prints new entries, and wakes whichever seat's turn it is with a pinned, zero-debounce prompt. The human supervisor sees every entry and owns the merges, never acting as courier." src="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/flow-light.svg" width="820">
  </picture>
</p>

One channel writer is the only code that writes to either file — whether called by the
legacy `debate post` surface or the brokered controller — and it *enforces* the rules
instead of politely asking: you can't post out of turn, you can't open
a second discussion while one is open, and a runaway back-and-forth gets cut off by a
message cap. A small scheduled job wakes whichever agent the doorbell points at. No server,
no message broker, no API keys, no framework to adopt.

## What a review looks like

After one round trip, the mailbox reads like this:

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

# Create a managed mailbox: two headless agents named claude and glm, plus you as supervisor.
# Prints the generated channel id, e.g. 'myproject-48213' (--label overrides the prefix).
# New channels record managed_version 1 and default to a 12-entry thread cap.
debate init --root ./collab --parties claude,glm --supervisor owner

# Wire the seats: an interactive wizard writes the watcher config with pinned
# incident-proof prompts, scaffolds the channel's PROTOCOL.md, and remembers
# your answers for the next channel. Everything derivable is derived, never asked.
# --smoke buys one scratch-channel round trip per seat (one model call each,
# the real channel untouched); --scheduler prints the systemd user units or
# cron line -- never installs or starts anything.
debate setup --root ./collab --channel myproject-48213 --smoke --scheduler

# The builder asks for a review:
debate post --root ./collab --channel myproject-48213 --from claude --type review-request \
    --thread feature-x --refs feature-x@abc123 \
    --body "Please review commit abc123: ..."

# The reviewer answers (its own tool/app runs this after reading the thread):
debate post --root ./collab --channel myproject-48213 --from glm --type verdict \
    --thread feature-x --refs feature-x@abc123 \
    --body "APPROVE — verified: 27 tests pass at abc123."

# Whoever acted last closes the thread:
debate post --root ./collab --channel myproject-48213 --from claude --type close \
    --thread feature-x --body "Merged. Closing."
```

Try posting twice in a row from the same party: the tool refuses. That refusal is the
protocol.

## Picking the seats: discovery, the registry, and `debate open`

One repository can carry several debates — a plan, a branch, a research
report — and each debate deserves its own pair of arguing agents, picked at
its birth. The machinery is two levels of setup and one minting command:

```bash
# Level 1 — run once after installing, repeatable any time, and re-run
# automatically when the tool version changes:
# scan PATH against the packaged catalog of known vendor CLIs and write the
# host seat registry (~/.config/debate/seats.json). No model calls.
debate seats discover
debate seats list

# Level 2 — session start: a zero-call freshness check. Exit 3 means real
# breakage only (a binary that vanished, a smoke that ran and FAILED);
# never-smoked is informational — smoke stays opt-in.
debate seats check

# Opt-in, one model call per seat, cost announced first:
debate seats smoke codex/gpt-5.6-sol
# Re-validate everything, with a refresh offer per stale seat:
debate seats doctor

# Mint a debate: a fresh channel with its pair picked from the registry and
# pinned for the debate's life. The previous pick is the one-Enter default;
# --pair answers non-interactively. The exact seat, effort, and command of
# each pick are recorded verbatim in the channel's own record (its .debate.json) — "glm said X"
# always answers WHICH glm, through WHICH pipe.
debate open --root ./collab --label market-research \
    --pair codex/gpt-5.6-sol,glm/glm-5.3 --yes
```

A seat is `vendor/submodel`, optionally `vendor/submodel@effort` — two
efforts of one model are two pickable seats, but they remain ONE model to the
identity guard: seating the same weights on both sides of a debate is refused
unless you say `--allow-identical-seats`, and two seats running the identical
command are refused always. A committable `debate-profile.json` at the repo
toplevel can restrict which registry seats may debate in that project (no
file, no restriction). Wrapper seats whose model is pinned inside the wrapper
(a `glm-agent`-style script) appear as exactly one seat named by their
verified pin — the registry never claims a selection the pipe cannot make.

## Running it unattended

There are two recorded managed versions. **Version 2 is the brokered path for new isolated
gates.** Version 1 is retained so existing two-command channels keep working, but those
agents receive the channel path and self-post with `--from`; it does not provide sender
binding or context isolation.

### Brokered managed version 2

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/broker-dark.svg">
    <img alt="A neutral controller sits between the channel and two reviewer seats. Each seat runs inside its own pinned read-only source export at a full 40-character commit, with its own HOME, temp and allowlisted environment, git unreachable, and no live channel path. The controller invokes each seat, schema-checks its typed result — which cannot name its own sender — binds the sender, and posts to the channel's two files on the seat's behalf; the seats never see the channel. A dumb cron watcher ticks the controller, and when nothing changed nothing runs. The case advances docket, sealed, paired reveal, deliberation, typed close (PASS, NO_PASS or ERROR) under one absolute whole-case deadline, with both first positions kept private until one atomic paired publish. The human supervisor sees every entry, may speak at any time, and is never a vote." src="https://raw.githubusercontent.com/zolcal/debate/main/docs/assets/broker-light.svg" width="820">
  </picture>
</p>

Initialize the channel explicitly as brokered, then fill in
[`watcher.brokered.example.json`](watcher.brokered.example.json). Party names are arbitrary;
the two `adapters` keys must exactly match the addressed channel.

```bash
debate init --root ./collab --parties party-a,party-b --supervisor owner --brokered

# Use the generated id and a full, already-existing 40-character commit SHA in the config.
# This validates topology, cost mode, profile hashes and timing without invoking a model.
debate adapter-doctor --root ./collab --channel <id> --config watcher.json

# The controller snapshots the case and posts a neutral supervisor docket. The first-seat
# choice controls completion order only; neither sealed input contains the other result.
debate broker-open --root ./collab --channel <id> --config watcher.json \
  --thread feature-x --first-seat party-b --refs feature-x@<sha> \
  --body-file review-docket.md

debate watch-once --root ./collab --channel <id> --config watcher.json

# After a fix, update source_ref/docket files in the config and snapshot them before
# another seat runs. This supervisor entry does not steal or change the party turn.
debate broker-revise --root ./collab --channel <id> --config watcher.json \
  --thread feature-x --refs feature-x@<new-sha> --body "Revision ready after fixes."
```

Each profile records its provider/model, reasoning setting, CLI version, authentication
mode, cost mode, permission policy and relationship to the artifact author. Exactly one
independent seat is the minimum two-agent topology: the interactive author's fresh
headless seat is honestly labeled an isolated author-affiliated self-review, while the
opponent is independent. The interactive session never fills a turn itself. Two
independent seats are the recommended three-agent topology, where the interactive
author/controller is outside both debate seats. The core never infers either topology from
names such as Opus, Codex, GLM or Kimi.

The model pair is configuration, not policy. A GPT-5.6 Sol author can, for example, use
headless Opus 5 plus a smoke-approved GPT-5.6 Terra profile so neither reviewer is the
interactive author. Another channel can use Opus/GLM, GLM/Kimi, or local models without a
code change. A Kimi controller can oversee separate Opus/Codex and Opus/GLM channels, but
each remains a two-seat debate with its own explicit channel id. Every example must record
the author relationship and the requested and resolved model identities; changing any of
those, the effort, permissions, authentication, or cost mode opens a fresh case.

`adapter-doctor` prints every seat's authentication and cost mode before it invokes
anything and explicitly reports that the check incurred no charge. Subscription seats
have no per-call API line item but still consume plan quota; API seats are metered by their
provider's current input/output-token prices; local seats consume host compute. Debate
does not estimate a dollar total because CLI prompts, cache discounts and provider prices
vary. Confirm the printed mode and the provider's current price before the first smoke.

`expected_runtime_model` is optional because some CLIs do not expose a stable resolved ID.
When omitted, Debate still records the returned runtime identity but cannot refuse silent
model substitution; configure it whenever the adapter can report a falsifiable exact ID.

Before the neutral docket is posted, the controller creates two separate read-only exports
of the complete tracked repository at the pinned commit. `collab/`, `var/` and `.git` are
separated; tracked project settings stay present as evidence but live settings sources are
refused. Each seat gets a clean project-local HOME/cache/temp area, an allowlisted
environment, a Git discovery ceiling, the immutable docket revision, and a controller-owned
result path. Gitignored cited files such as a plan or `watcher.json` are materialized and
hashed separately. Stdout/stderr are diagnostics only; the result must be schema-versioned
JSON, may not contain `sender`, and is posted under the bound seat by the controller.
`broker-revise` maintains a content-addressed revision chain and blocks invocation if a
revision was only half-recorded; verdict provenance therefore never points only at a mutable
gitignored filename.

Every `verdict` result also carries a typed `decision` of `PASS` or `NO_PASS`:

```json
{
  "schema_version": 1,
  "entry_type": "verdict",
  "decision": "PASS",
  "body": "APPROVE - fresh export run: 412 passed.",
  "runtime_model": "resolved-model-id"
}
```

The case state advances through `docket` -> `sealed` -> `reveal` -> `deliberation` ->
`terminal`. Both initial results are kept outside the shared record until they exist, then
published by one atomic mailbox replacement with each private capture timestamp recorded
in its reveal provenance. A crash after that replacement but before the
doorbell update is repaired idempotently without duplicating either position. After reveal,
each fresh seat sees only the current thread. Matching party votes close automatically as
`PASS` or `NO_PASS`; `PASS` requires an agreeing author-independent seat. A supervisor
verdict is visible context but never a vote. Thread-cap exhaustion closes `NO_PASS`, while
adapter/retry/deadline failure closes `ERROR`; `close_reason` records why separately.
The typed-close intent is persisted before its mailbox write, so the recurring scheduler
can likewise distinguish and repair a close whose signal update was interrupted; unrelated
mailbox-ahead anomalies still follow the normal fail-closed escalation path.

The runtime lives below `<project>/var/debate/<channel>/`, never `.pytest_cache` or another
tool cache. `adapter-doctor` prints the unconstrained schedule estimate and the enforced
whole-case deadline from the same timing calculation; adapter timeouts above 60 minutes or
an absent deadline are refused. It also prints `cost_mode` before any future smoke can spend
money. The absolute deadline spans sealed capture, reveal, deliberation, retries and process
restarts. Every invocation is capped by its remaining budget, and an expired case is closed
idempotently as `ERROR` / `case-deadline-expired` on the next scheduler tick.

Completed case exports are intentionally read-only and Debate never deletes provenance
automatically. Project cleanup must first restore owner write permission within the exact
completed `var/debate/<channel>/` case directory, then remove only that validated directory.

This is strong protection against accidental contamination, not a claim that a same-user
process is hostile-code safe. Read-only permissions, a clean environment, Git ceiling and
canaries are mechanically checked; an `isolation_mode: advisory` profile can still read an
absolute host path if the selected CLI/tool sandbox permits it. That includes the private
sealed-submission state stored elsewhere below the same project-local case runtime: prompt
separation does not stop a hostile same-user process from traversing parent directories.
Use `os-enforced` only when an external sandbox actually denies those reads.

### Managed version 1 compatibility

`debate watch-once` is one tick of a deliberately simple watcher. Put it on a schedule
(cron, every minute): it checks the doorbell, prints any new messages to stdout —
route that wherever you already look, a log file or a chat gateway — and, if it's an
agent's turn on an open thread, starts that agent with a fixed, pre-written prompt from a
config file:

```json
{
  "state_path": "/somewhere/outside/the/channel/watcher-state-myproject.json",
  "commands": {
    "claude": ["claude", "-p", "{prompt}"],
    "glm": ["glm-agent", "{prompt}"]
  },
  "prompts": {
    "claude": "It is your turn on ./collab --channel myproject-48213. Read only the open thread with `debate read --root ./collab --channel myproject-48213`, act, post with the same explicit channel, then stop.",
    "glm": "It is your turn on ./collab --channel myproject-48213. Read only the open thread with `debate read --root ./collab --channel myproject-48213`, cite your own fresh evidence, post with the same explicit channel, then stop."
  },
  "debounce_seconds": { "claude": 0, "glm": 0 },
  "retry_seconds": 1800
}
```

Prompts may address their channel through two placeholders instead of hardcoded
paths: `{channel_root}` expands to the resolved absolute channel folder and
`{channel_name}` to the channel id, both in one fixed pass before `{prompt}` is
substituted into the argv. A prompt carrying `--root {channel_root} --channel
{channel_name}` stays correct the day a second channel moves into the folder —
`debate setup` generates exactly that form.

**Name the state file after the channel, not `watcher-state.json`.** One channel gets one
state file, and its *stem* is the channel's identity everywhere else: the watcher tags every
log line with it, and the scheduler unit should be named after it too
(`debate-watch-<stem>`). Since 0.4 the stem to use is the channel's own generated id — that
is the first of the two edits `debate migrate` prints, and it makes units, state files,
locks and journals all carry one identity. Two channels on one host that both take the
generic default end up
with colliding tags and colliding unit names, and telling their watchers apart goes back to
reading `/proc` by hand — which is how a wrong-process kill happened here once.

```bash
*/3 * * * * cd /absolute/path/to/project && debate watch-once \
  --root /absolute/path/to/project/collab --channel myproject-48213 \
  --config /absolute/path/to/project/watcher.json
```

Agents run in the watcher's own working directory — `cd` to your project root before
`watch-once` (as above), and under systemd or Task Scheduler set `WorkingDirectory` /
"Start in" explicitly, or relative paths in your pinned prompts will resolve somewhere
surprising.

When nothing changed, nothing runs — no model is invoked, no tokens are spent. A managed
version 1 channel requires one command for each of its two recorded parties. If either is absent,
or an open managed thread has no party turn, `watch-status` reports **INVALID** and exits
4; the watcher never represents that state as healthy or waits for a live human session.
Configs without `managed_version` remain readable as legacy/manual history but must be
reconfigured before managed unattended use. Managed version 2 instead requires exactly two
brokered adapter profiles and refuses direct party posts. Headless seats normally use zero
debounce.

### Running to completion

Cron is for unattended operation. At the keyboard and just want the current review driven
to its close? Run the same watcher in the foreground:

```bash
debate watch --root ./collab --channel myproject-48213 --config watcher.json --until-close
```

Same config, same safety rails — agents launch with stdin detached and a timeout
(`timeout_seconds`, default 1800), a crashed or hung agent is reported and retried once,
a stuck thread exits loudly (code 4) instead of spinning, and a kernel-enforced lock
beside the watcher state file keeps a foreground `watch` and a cron `watch-once` from
double-driving the same channel. `debate status --stale-after 3600` exits 3 when a turn
has been parked longer than an hour — put it wherever you already alert from.

> **One driver per channel: the scheduler OR a foreground `watch`, never both.** `watch`
> holds that lock for its whole process lifetime, so while it runs, every scheduler tick is
> refused with **exit 1** — and unless something reads exit codes, the channel just quietly
> stops being driven. Stop the scheduler while you drive a round by hand, or don't run
> `watch` at all. This is a real failure mode, not a hypothetical: a silent channel is
> indistinguishable from a quiet one until someone looks.

### Is anything actually driving this channel?

```bash
debate watch-status --root ./collab --channel myproject-48213 --config watcher.json
```

Reports whether a watcher holds the lock — naming the holder's pid and working directory —
when the channel was last ticked, and what it is waiting for. Exits **4** when a human
should look. Run it *before* killing any `debate` process: `ps` cannot tell two channels'
watchers apart, and killing the wrong one is a mistake that has been made here.

## Housekeeping: the mailbox grows, agents shouldn't read all of it

The conversation file grows forever by design. Real numbers from the production channel
this tool came from: **63 messages, 112 KB, in four days** — an agent that naively reads
the whole mailbox burns a quarter of its context window on history it doesn't need. Three
commands keep that honest:

- **`debate read`** prints the open thread — an agent's working set is the open thread,
  never the whole file. `--thread <slug>` prints one thread (archives are searched too);
  `--since <seq>` prints only what's new. Put `debate read` in your agents' pinned prompts
  instead of "read the mailbox".
- **`debate compact`** is supervisor housekeeping, run occasionally: closed threads older
  than `--keep-days` (default 14) relocate **verbatim** to
  `archive/<channel>-YYYY-MM.md`, with a one-line index per thread in
  `archive/<channel>-INDEX.md`. Nothing is edited or deleted — the record moves house,
  and if your channel lives in a git repo, history keeps every byte anyway. `--dry-run`
  shows the plan first.
- **`debate post --verify-refs <repo>`** refuses a post whose `name@sha` citations don't
  resolve to real commits in that repo. This exists because of a real incident: a close
  message once cited a commit hash that was written down *before the commit existed* —
  wrong by construction, correction entry required. Machines are better at this check
  than authors are.
- **`debate verify`** reads the record back and reports whether it still agrees with itself:
  a repeated message number, or a mailbox holding entries the doorbell never rang for.
  Exits 0 when clean and 4 when something needs a human. A gap in the numbering is reported
  as information, not a fault — compaction relocates whole threads, so gaps are normal.

## One channel carries one project

A channel records, at `init`, the absolute path of the repo it serves. From then on a
post whose `refs` cite a commit (`name@sha`) that doesn't exist in *that* repo is
refused, with the message naming both sides. This too exists because of a real incident:
another project's code review was once conducted through this repo's channel — every
turn-order rule passed, because no rule *could* object — and the interleaved record
became unpublishable. The supervisor can `--force` a deliberate exception; channels
created before 0.4 carry no binding and are not gated.

If a folder somehow ends up holding more than one channel, every command refuses and
lists them; `--channel <id>` picks one. Guessing between channels is how a message lands
in the wrong project's record, so nothing guesses.

**Upgrading from 0.3.x:** existing channels keep working unchanged. `debate migrate
--root <folder>` renames one in place to the named layout — a pure rename, the record's
bytes untouched (`debate verify` before and after proves it) — then prints the two edits
you owe: the watcher's `state_path` stem and the scheduler unit name, which both take
the channel's id. Writing new legacy-layout channels is no longer possible, and posting
to existing ones is deprecated as of 0.5 — it still works, `debate migrate` is the
supported path forward, and no removal date is promised.

## What's enforced — and what isn't

Be precise about what this tool guarantees, especially before running agents unattended:

- **Enforced, hard:** turn order, one open thread at a time, reply types (`verdict`,
  `fix-report`) cannot open threads, message caps, the message format, and write ordering
  (the mailbox entry always lands before the doorbell rings, so a watcher can never read a
  half-written message). An agent that breaks these rules gets its post *refused*, not a
  warning.
- **Broker-enforced for managed version 2:** exact party/profile binding, at least one
  author-independent seat, a full pinned source export with no reachable parent Git store,
  immutable docket/profile/config hashes, clean environment and project-local runtime,
  controller-owned sender, schema-validated typed results, sealed paired reveal, deadline
  recovery, and automatic `PASS`/`NO_PASS`/`ERROR` terminal transitions.
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
   retry. Version 1 then escalates; version 2 records and closes `ERROR`. Two agents in a
   refusal loop would burn money forever; the cap and absolute deadline are the brakes.
3. **Drive every managed turn** — both parties have headless commands and normally zero
   debounce; a missing command is INVALID, never a human fallback.
4. **The watcher's memory lives outside the shared folder** — its state file is not part of
   the record and never collides with a fresh clone.
5. **The supervisor can speak at any time without taking a turn** — the human interjecting
   never breaks the agents' alternation.
6. **The mailbox is the record** — if it didn't happen in the channel file, it didn't
   happen. Corrections are new messages, never edits.
7. **A brokered seat never self-posts** — it receives no live channel path; the controller
   validates its result file and derives the sender from the configured seat.
8. **Initial positions reveal as a pair** — no party can anchor its first judgment on the
   opponent, while later disagreement deliberately becomes a real, current-thread debate.

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

- **Two seats by design.** A debate needs exactly two opposing seats; strict alternation
  between two named seats (plus a supervisor who can always interject) is the feature. In
  the recommended topology both seats are independent of the author, who works with the
  owner outside the channel. Getting N agents to agree is a different protocol.
- **Polling, not push.** The doorbell is made to be checked once a minute by cron. If
  you need sub-second latency, this is not your transport.
- **The writer lock is advisory.** `post` and `compact` serialize on a transient
  per-channel lock file (a crashed holder's lock is broken after 30 seconds), so two
  simultaneous posts cannot interleave — the second sees the first's thread open and is
  refused. But it only binds writers that go through the CLI. (`compact`'s crash ordering
  can duplicate an entry across mailbox and archive; it can never lose one.)
- **The record is tamper-evident, not tamper-proof.** `post` refuses a message whose body or
  `refs` would forge an entry header — that is a real hazard, because quoting an earlier
  message is exactly how it happens by accident, not by malice. `debate verify` catches
  careless or automated tampering after the fact. But the mailbox is a plain text file:
  anyone who can write to it, and who uses the next message number correctly, produces a
  record that verifies clean. Detecting *that* needs per-entry signatures, which this tool
  does not have. Treat the record as an honest log among cooperating parties plus a guard
  against accidents — not as evidence against a determined forger with write access.
- **Young.** Extracted from a working production setup, generalized, and tested — but
  read the code before trusting it; it's about 5,500 lines including the CLI, the
  broker and the setup wizard, with 413 tests as of this writing.

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
about ten minutes — was a 137× speedup on the function under contract. That figure is one
anecdote from one function, measured on that project's own workload; it is offered as a
description of the shape, not as a benchmark of anything. `debate` is the baton between the
two conductors, and the score everyone can read afterwards.

The same shape fits whatever pair of ecosystems you already run. The origin above is one
example, not the design. This repo's historical channel used a human-driven Opus builder
and headless GLM reviewer; that append-only record remains under [`collab/`](collab/) as
incident and 0.4 provenance, but its commandless-seat scheduler is retired. The fresh
`repository-unattended-02750` channel selects headless Opus/Codex only in local config and
uses the same vendor-neutral broker shipped here. Its record includes the repository's own
end-to-end sealed/reveal/automatic-close proof. The first end-to-end proof is MSG-11..14:
independent Opus and Codex capture timestamps, one paired reveal, and automatic `PASS`
with no live-session or human intervention. The record has grown past it since — the same
machinery's first production acts were gating this repository's own merge and the v0.5.0
release itself, and those cases are entries in the same file. Earlier MSG-1..6
adapter-integration attempts remain
visible as bounded `ERROR` closes rather than being rewritten. The pinned profiles were
Claude Code 2.1.223 /
`claude-opus-5` high and Codex CLI 0.146.1 / `gpt-5.6-terra` high, both
author-independent and subscription-authenticated; at case close the CLIs reported a `$0.355168`
Opus usage-equivalent and 43,729 Codex tokens. Those numbers consume subscription quota and
are operational evidence, not a promise of zero cost. Branch-gate verdicts separately cite
the reviewer's own full export run rather than author-pasted evidence.

A GLM + Kimi pairing works the same way anywhere (see
[`examples/glm-kimi.md`](examples/glm-kimi.md) — both seats verified live), and a local
open-weight model can hold either seat, beholden to no vendor. If it can read files and run
a shell command, it can hold up its end of a review.

## The name

Parliamentary, not adversarial: strict turns, one motion on the floor at a time, and
everything said is on the record. (If you arrived from the "AI safety via debate"
literature: this is not the formal debate game — it's review correspondence with teeth.)

## License

MIT
