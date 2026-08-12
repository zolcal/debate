# Changelog

Notable changes per release. Dates are the tag dates.

Every release from v0.2.0 onward went through this project's own review channel — the
record is under [`collab/`](collab/), and the message numbers cited below are entries in
it.

## Unreleased

### Added

- **`debate setup`** — wires the seats of an existing channel
  (plan `2026-08-04-setup-wizard.md`, APPROVED MSG-36). One question per party on a
  first run, one Enter afterwards (a defaults cache that names which channel each
  remembered answer came from — a suggestion, never a registry); flags
  (`--command`, `--human`, `--yes`) are the interview, so non-interactive use adds
  no second input surface. Everything derivable is derived, never asked: the state
  stem, unit name and config stem are the channel id. It validates before writing
  anything — commands must resolve, and the assembled config round-trips the real
  loader so state-inside-the-channel-root refuses at setup time, not first tick —
  scaffolds the channel's `PROTOCOL.md` from a packaged template (only if absent,
  never clobbered; a test pins the copy byte-equal to the repo template), and
  refuses managed-version-2 brokered channels with a pointer at `adapter-doctor`.
- **`debate setup --smoke`** — an opt-in scratch-channel round trip per
  watcher-driven seat: a throwaway channel built with setup's own write path
  (so it carries a PROTOCOL.md), an `info` probe posted as the other party, the
  seat run with its REAL pinned prompt pointed at the scratch root, and a
  well-formed reply asserted in the scratch mailbox. One model call per seat,
  announced before it is spent; the real channel is untouched; the scratch root
  is removed either way. A pass proves the seat contract — turn-gate, read,
  post — and states plainly that it proves nothing about consistency or review
  quality.
- **`debate setup --scheduler`** — generates and PRINTS the
  `debate-watch-<channel-id>.{service,timer}` user units (stateless one-minute
  `watch-once` tick, the incident-derived naming convention enforced) or the
  cron line — never touches `systemctl`. Withheld when a requested smoke
  failed: no scheduler for a seat that cannot reply.
- Watcher prompts may address their channel as `{channel_name}` alongside
  `{channel_root}` — expanded in the same single pass. A prompt addressing by
  `--root` alone refuses on every turn the day a second channel shares the folder;
  the wizard's generated prompts carry both.

## v0.5.0 — 2026-08-07

**Seats no longer post for themselves.** The headline is managed version 2: a neutral
controller runs both reviewer seats from pinned read-only source exports, keeps each
first position sealed until both exist, reveals them as a pair, and closes the case with
a typed outcome — no self-posting, no anchoring, no silent stall. The machinery's first
production acts were gating this repository's own merge and this very release.

### Added

- Explicit managed-version 2 brokered channels (`debate init --brokered`). A neutral
  `broker-open` snapshots the case before assigning the first seat; direct party posts are
  refused and structured adapter results are posted under controller-bound identities.
- Generic adapter profiles record author relationship, provider/model/runtime identity,
  reasoning, CLI/authentication/cost/permission/settings policy and a sanitized fingerprint. At least one
  seat must be author-independent; one versus two independent seats is reported as the
  minimum two-agent versus recommended three-agent topology.
- Brokered seats run from separate read-only pinned exports with a Git ceiling and clean
  project-local environment. Gitignored docket evidence is materialized by content hash;
  runtime/case state lives below `var/debate/`, survives pytest cache clearing, and records
  source, docket, prompt, profile and controller hashes. `adapter-doctor` validates and
  reports both timing bounds and cost modes without invoking a model.
- `broker-revise` snapshots each post-fix commit/docket as a new content-addressed case
  revision, records it through a supervisor entry without changing the party turn, and
  blocks invocation on a half-recorded revision.
- Brokered cases persist `docket`, `sealed`, `reveal`, `deliberation`, and `terminal`
  phases. The two initial typed positions remain private until `commit_reveal_pair`
  publishes both with one atomic mailbox replacement; restart recovery repairs the
  doorbell without duplicating or exposing one side early. Each reveal provenance block
  records when that private initial submission was captured. Typed-close intent is also
  persisted so the recurring scheduler can repair its mailbox/signal crash boundary
  without treating unrelated record anomalies as controller traffic.
- Version 2 verdicts carry `PASS` or `NO_PASS`. Matching party votes close automatically
  (a `PASS` requires an agreeing author-independent seat), the thread cap closes
  `NO_PASS`, and adapter or whole-case deadline failure closes `ERROR` with a separate
  `close_reason`. Supervisor entries never count as votes.

### Changed

- Newly named channels are `managed_version: 1`, default to a 12-entry thread cap,
  and require watcher commands for both arbitrary party names. Existing explicit caps
  remain unchanged; configs without the managed marker remain readable as legacy/manual
  history.
- Managed missing-command and turnless-open states are `INVALID`, never healthy
  `MANUAL`; `watch-status` returns the shared needs-attention exit code. Both headless
  seats default to zero debounce in the shipped examples.
- Migrated this repository's active guidance to a fresh cap-12 brokered channel while
  preserving the historical Opus/GLM record. The local repository profile selects
  headless Opus/Codex without making that pair a product default; examples document the
  minimum two-agent and recommended three-agent topologies plus alternative pairs.
- Every scheduler line and watcher prompt now addresses multi-channel roots with explicit
  `--channel`; the repository protocol reads each channel's persisted cap instead of
  declaring one root-wide number. The old commandless-seat timer is retired from active
  use rather than treated as a supported managed mode.
- The repository's first end-to-end brokered proof (MSG-11..14) records separate
  initial-capture timestamps, atomically reveals both independently gathered positions,
  and closes `PASS` automatically. Failed adapter setup attempts remain in the same
  append-only record as bounded `ERROR` outcomes. The record has since grown past that
  proof: the same machinery gated this repository's own merge and this release, and
  those cases are entries in the same file.

### Deprecated

- Posting to legacy-layout channels — the 0.3.x fixed filenames
  `CHANNEL.md`/`signal.json`/`debate.json` — is deprecated as of 0.5. It still works;
  `debate migrate` renames a channel in place, byte-identically, and is the supported
  path forward. Writing *new* legacy channels has been impossible since 0.4. No removal
  date is promised.

### Fixed

- Six strict-mypy errors surfaced by the feature branch's first CI contact. The visible
  part is fail-closed handling: a malformed `sealed_submissions` or `latest_votes` case
  state now raises the standard `refused:` channel error instead of a bare `TypeError`.
- Brokered subprocesses could not start Python on Windows at all: the environment
  allowlist built the child environment from nothing, and Windows cannot initialize
  interpreter hash randomization without `SYSTEMROOT`. A machine-owned Windows baseline
  (`SYSTEMROOT`, `SYSTEMDRIVE`, `COMSPEC`, `PATHEXT`, `WINDIR`) now sits beneath the
  allowlist; the POSIX baseline stays empty, so no user configuration rides in with it.
- `mypy .` excludes the broker's gitignored `var/` runtime tree beside `build/`, for the
  same reason: duplicate-module copies that exist locally but never in CI's clean
  checkout.

## v0.4.0 — 2026-08-05

**A channel now knows its own name, and which project it serves.** The headline is that
several channels can share one folder without colliding, and a message can no longer land
in the wrong project's record. Existing 0.3.x channels keep working untouched.

### Added

- **Per-instance channel naming.** `debate init` generates an id once — `<label>-<NNNNN>`,
  the label defaulting to the enclosing repo's directory name — and stores it in the
  config. Files carry it: `<id>.channel.md`, `<id>.signal.json`, `<id>.debate.json`.
  Every command discovers the channel from `--root`; `--channel <id>` disambiguates, and a
  folder holding two channels refuses and names both rather than guessing.
- **`debate migrate`** — renames a legacy channel in place to the named layout. A pure
  rename: mailbox, doorbell and archive move byte-untouched (`debate verify` before and
  after is the acceptance test). The id is committed into the legacy config *before* any
  file moves, so an interrupted migration resumes under the same id instead of stranding
  half-renamed files, and the whole move runs under the legacy writer lock. It prints the
  two edits the operator then owes: the watcher's `state_path` stem and the scheduler unit
  name.
- **One channel carries one project.** `debate.json` gains `project`, the absolute path of
  the repo the channel serves, recorded at named `init` and at `migrate`. A post whose
  `refs` cite a `name@sha` that does not resolve in that repo is refused, naming both
  sides. This exists because of a real incident: another project's review was once
  conducted through this repo's channel — every turn-order rule passed, because no rule
  *could* object — and the interleaved record became unpublishable. `--force` stays
  supervisor-only; pre-0.4 channels carry no binding and are not gated.
- **`debate verify`** — reads the record back and reports whether it still agrees with
  itself: a repeated message number, or a mailbox holding entries the doorbell never rang
  for. Exits 0 clean, 4 when a human should look. A numbering gap is information, not a
  fault — compaction relocates whole threads.
- **`debate watch-status`** — read-only channel liveness. Reports whether a watcher holds
  the lock (naming the holder's pid and working directory), when the channel last ticked,
  and what it is waiting for. Exits 4 when a human should look. Run it before killing any
  `debate` process: `ps` cannot tell two channels' watchers apart.
- **`{channel_root}` placeholder** in watcher prompts, expanded to the resolved absolute
  path, so a pinned prompt addresses its channel unambiguously regardless of the agent's
  working directory.

### Changed

- The watcher's tick lock, log lines and state file all carry the channel's identity, so
  two channels on one host can no longer be confused for each other. The refusal when
  another driver holds the lock now names the competitor.
- Operator-facing watcher output is ASCII-only, so it stays readable on a Windows console.
- Writing *new* legacy-layout channels is no longer possible — `debate init` always names.
  Posting to existing legacy channels remains fully supported in 0.4.
- Documentation teaches the named layout throughout; `docs/case-study.md` keeps its
  original filenames as history, with an era marker.

### Fixed

- **The record is tamper-evident.** `post` refuses a body or `refs` that would forge an
  entry header — a hazard that fires by accident, since quoting an earlier message is
  exactly how it happens — and `refs` must survive `splitlines()` unchanged. The doorbell
  is editable too, and is now refused and survived rather than crashing the reader.
- A corrupt mailbox, doorbell, watcher state file or `watcher.json` no longer kills the
  tick with a traceback. Under a 60-second timer, one hand-edit typo used to mean a
  crash-loop.
- `pytest.raises(match=...)` in the project-binding suite built a regex out of a
  filesystem path, which is only safe on POSIX; every Windows CI job failed on the invalid
  escape while Linux stayed green.
- `release.yml`'s gate ran `ubuntu-latest` only while CI gates ubuntu + windows × 3.10 +
  3.12 — a tag could have published a package CI rejects. Both now run the same matrix.
- `mypy .` excludes `build/`, which a non-editable source install writes into the tree and
  which otherwise makes the documented command fail with "Duplicate module named debate".

### Upgrading from 0.3.x

Existing channels keep working with no action. To adopt the named layout:

```bash
debate migrate --root ./collab          # prints the new id and the two edits you owe
```

Then rename the watcher's `state_path` so its stem is the channel id, rename the scheduler
unit to `debate-watch-<id>`, and confirm one clean tick with `debate watch-status`. Stop
the scheduler for the duration: `migrate` takes the writer lock, and a post that breaks a
stale lock between a migration crash and its re-run could be renamed over.

**Deprecation notice:** writing to legacy-layout channels still works in 0.4 and becomes a
documented deprecation in 0.5.

### A note on what this does not claim

The record is tamper-**evident**, not tamper-proof. `post` refuses forged headers and
`verify` catches careless or automated tampering after the fact, but the mailbox is a plain
text file: anyone who can write to it, and who uses the next message number correctly,
produces a record that verifies clean. Detecting that would need per-entry signatures,
which this tool does not have.

## v0.3.1 — 2026-07-17

Reliability release. Published to PyPI but never given a GitHub Release at the time; this
entry backfills it.

### Added

- **`debate watch`** — a run-to-completion foreground loop, for driving the current review
  to its close at the keyboard. Same config and safety rails as `watch-once`.
- **Kernel-refereed watcher lock** (`flock`/`msvcrt`), so a foreground `watch` and a cron
  `watch-once` cannot double-drive one channel.
- **Truthful parked-turn age** and `debate status --stale-after`, exiting 3 when a turn has
  been parked too long. Turnless and unknown-age threads count as stuck.
- Claude Code skill and plugin manifests (`skills/debate/`, `.claude-plugin/`).
- `examples/glm-kimi.md` — a non-duopoly pairing with both seats verified live.

### Changed

- **Opener allowlist**: `verdict` and `fix-report` are replies by nature and can no longer
  open a thread.
- The watcher decides on a writer-locked snapshot, so invocation, escalation and STUCK can
  never act on a mid-post state.
- Agents run in the watcher's own working directory, not the channel root — set
  `WorkingDirectory` explicitly under systemd.

### Fixed

- Agent stdin is detached (`DEVNULL`); a hang no longer waits forever on input.
- Terminal launch-failure escalation and caught timeouts instead of spinning.
- A corrupted `signal.json` refuses with a clear error instead of a traceback.

## v0.2.0 — 2026-07-08

Housekeeping release: the mailbox grows forever by design, and agents should not have to
read all of it. Every feature was extracted from one week of running the protocol in
production — five review rounds, 63 messages, 112 KB of mailbox in four days — and the
release itself went through two of those rounds. The reviewer found and reproduced a
data-loss race in the first version of `compact`.

### Added

- **`debate read`** — print the open thread; `--thread <slug>` for one thread (archives
  searched too), `--since <seq>` for what is new.
- **`debate compact`** — closed threads older than `--keep-days` (default 14) relocate
  verbatim to the archive with one index line each. Nothing edited, nothing deleted;
  `--dry-run` shows the plan.
- **`debate post --verify-refs <repo>`** — refuses a post whose `name@sha` citations do not
  resolve to real commits. Born from a real incident: a close message once cited a hash
  written down *before* the commit existed.

### Fixed

- `post` and `compact` serialize on a transient lock file (a crashed holder's lock is
  broken after 30 seconds), so two simultaneous posts cannot interleave and `compact`
  cannot overwrite a concurrent post.
- True byte fidelity: CRLF mailboxes survive parsing, archiving and rewriting.

## v0.1.1 — 2026-07-06

First public release on PyPI: `pip install debate`. A tiny file-based protocol so two AI
agents — from different vendors, in different apps — can review each other's work by taking
turns in two shared text files. Zero dependencies, Python 3.10+.

## v0.1.0 — 2026-07-06

Initial tag. Superseded by v0.1.1 before wide use.
