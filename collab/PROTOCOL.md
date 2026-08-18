# The debate protocol — channels of the `debate` repository

Active managed channel: **`repository-unattended-02750`**. Its two controller-bound,
headless seats are **opus** and **codex**; **owner** is the human supervisor and is not a
vote. This pair is this repository's local choice, not a product default. The historical
`debate-06451` Opus/GLM config and mailbox remain append-only evidence and are retired from
active scheduling.

The mechanics below are enforced by Debate. Review quality and claims about model output
remain matters of evidence; see the trust boundary in the README.

## 1. Files and channel selection

| File | Role | In version control? |
|---|---|---|
| `PROTOCOL.md` | this shared root contract | yes |
| `<id>.debate.json` | parties, supervisor, managed version, project, thread cap | yes |
| `<id>.channel.md` | append-only channel record | yes |
| `<id>.signal.json` | doorbell, phase, deadline and terminal result | no (gitignored) |
| `archive/` | compacted closed threads | yes |
| `<id>.lock` | transient writer lock | no (gitignored) |

This root holds more than one channel. Every operational command MUST include the exact
`--channel <id>`; unqualified discovery is expected to refuse. Never edit a mailbox or
signal by hand. All writes go through Debate's writer/controller.

The thread cap is not a root-wide number. Read the addressed channel's persisted
`thread_cap` from `<id>.debate.json`. Existing channels retain their historical value;
new channels default to 12. In a brokered version-2 case, cap exhaustion closes typed
`NO_PASS` rather than waiting for the supervisor.

## 2. Entries and evidence

```
## MSG-<seq> | <utc-iso> | from: <party> | type: <type> | thread: <slug> | refs: <refs>
<body>
```

- `review-request` / neutral docket — states the artifact and fixed acceptance criteria.
- `verdict` — carries typed `PASS` or `NO_PASS`. A code-review verdict cites the reviewer's
  own fresh export run, exact command and result lines; author-pasted evidence is context,
  never proof.
- `fix-report` — identifies a new immutable revision and what changed.
- `question` / `info` — context without a vote.
- `close` — typed controller close for `PASS`, `NO_PASS`, or `ERROR`.

Refs are full `branch@sha` values written after the commit exists. Corrections are new
entries, never edits. Reviewers read only the current thread; repo claims come from the
pinned source export, not channel history.

**No invented size limits; evidence is never compressed.** The debate never constrains the
SIZE of the artifact under review. A length, word, page or section budget exists only if
the owner put one in the docket; absent that there is none, and no seat may infer one from
a seed, a brief, a template or house style. Findings, the evidence behind them and their
provenance are never trimmed, summarized away or dropped to fit a length — a case that
argues from half its evidence has established nothing, whatever verdict it records. Length
alone is never a blocking finding and compression is never a condition of approval; a seat
that judges an artifact bloated says so as a non-blocking observation and the owner
decides. Never cite a page count for a document that was never rendered.

## 3. Managed operation

`repository-unattended-02750` is managed version 2. The controller, not either model:

1. snapshots the pinned commit and immutable docket into separate read-only exports;
2. invokes both initial seats without an opponent transcript;
3. publishes both sealed positions and their private capture timestamps together under one
   writer lock;
4. supplies only the current thread during later deliberation;
5. binds each structured result to its configured sender; and
6. closes automatically as `PASS`, `NO_PASS`, or `ERROR`.

Direct party posts are refused. The supervisor may add context but never fills a party
turn and never counts as a vote. `PASS` requires agreement that includes an
author-independent seat. The whole-case deadline spans invocations, retries, process
restarts and scheduler gaps; retry exhaustion and deadline expiry close `ERROR` with a
separate `close_reason`.

The repository uses the recommended three-agent topology for its proof: the interactive
GPT-5.6 Sol author/controller is outside both seats, while headless Opus 5 and GPT-5.6
Terra are both marked author-independent. The minimum two-agent topology is also valid:
one isolated seat is author-affiliated and the other is independent. Names never determine
topology; profile fields do.

## 4. Driver and diagnosis

One recurring driver owns one channel. The production scheduler line, after the approved
branch is merged and its local profile is installed, is:

```bash
cd /home/zoltan/Projects/debate && \
  PYTHONPATH=src python -m debate watch-once --root collab --channel repository-unattended-02750 \
  --config watcher.json
```

The unit/state stem must be `repository-unattended-02750`; the watcher state and all
controller runtime stay below
`/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/`, never a tool cache.
Both adapter profiles are commands. A commandless seat is invalid; no turn is delegated to
an interactive human session.

Before enabling a scheduler, run the non-charge-bearing doctor and one bounded smoke/case.
Use explicit selection for every check:

```bash
debate adapter-doctor --root collab --channel repository-unattended-02750 --config watcher.json
debate watch-status --root collab --channel repository-unattended-02750 --config watcher.json
debate verify --root collab --channel repository-unattended-02750
```

Use either the recurring scheduler or foreground `debate watch --until-close`, never both.
The old `debate-watch-debate-06451.timer` must remain disabled after migration; its config
and record stay readable as history.

## 5. Isolation and authority

Seats can read the complete pinned codebase in their own export; `collab/`, `var/` and
`.git` are separated so live channel state and controller internals do not contaminate the
opposing judgment. Settings sources, hooks, plugins, MCPs and session persistence are off.
The export and result contract mechanically prevent ordinary source edits and sender
spoofing.

This repository records `isolation_mode: advisory`. A same-user process may still traverse
absolute host paths if its CLI sandbox allows it, including the private sealed case state
elsewhere below `var/debate/`. This is contamination resistance, not hostile-code
containment; use `os-enforced` only when an external sandbox actually denies those reads.

The human supervisor alone controls merges, publication, profile changes, scheduler
changes and scope. A profile/model/topology change opens a fresh case; it never changes a
seat mid-thread.

## Amendment log

- 2026-08-18 — v2.1: added the no-invented-size-limits rule to §2 — the artifact's size is
  the owner's business, and findings, evidence and provenance are never compressed.
- 2026-08-06 — v2.0: moved active repository review to fresh brokered channel
  `repository-unattended-02750`, selected headless Opus/Codex locally, required explicit
  channel addressing and per-channel caps, and retired the commandless Opus/GLM scheduler
  shape while preserving its append-only record.
- 2026-08-05 — v1.1: historical `debate-06451` channel started with Opus/GLM after the
  previous mixed-project record was retired.
