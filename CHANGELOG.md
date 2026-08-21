# Changelog

Notable changes per release. Dates are the tag dates.

Every release from v0.2.0 onward went through this project's own review channel — the
record is under [`collab/`](collab/), and the message numbers cited below are entries in
it.

## v0.8.0 — unreleased

**Debate becomes an installed product inside Codex and Claude Code.** Until now the
plugin was metadata plus a reactive skill wrapped around a pip-installed CLI; setup
meant registry commands in a terminal. This release ships the engine INSIDE the native
plugin, surfaces setup automatically at session start, makes seat approval an explicit
in-UI act, and makes new product-created debates brokered (managed version 2) by
default. Plan gated on channel `plan-v080-onboarding-59142` (PASS, MSG-13).

### Added

- **Installation-driven onboarding** — a read-only, zero-model-call `SessionStart`
  hook (per-host manifests: `hooks/hooks.json` for Claude, `hooks/hooks-codex.json`
  for Codex, field-identical documents) shows a setup notice when a project is not
  ready and stays silent when it is. Headless Claude sessions
  (`CLAUDE_CODE_ENTRYPOINT=sdk-cli`, spike-attested) get one context line, never a
  banner; for Codex automation the documented lever is `DEBATE_ONBOARDING_QUIET=1`
  (no headless signal is attestable there until a hook is trusted interactively).
- **`debate onboarding status|inspect|approve`** — the product engine's JSON-first
  state machine. `inspect` scans in memory and returns a deterministic
  `candidate_revision`; `approve` verifies that revision, requires `--confirmed`, and
  writes the machine registry plus the project's committable `debate-profile.json`
  transactionally (any preparation failure leaves both prior files byte-identical).
  Detection is never approval; a previous `last_pair` is never approval; zero selected
  seats writes nothing.
- **`debate open --brokered`** — mints a managed-version-2 channel from two approved
  registry seats: full loader plus adapter-doctor validation before the first target
  write, provenance (provider, model, effort, command, authentication mode, cost mode,
  permission policy, author relationship) recorded in the channel's `.debate.json`,
  the interactive host outside both seats, the human as supervisor.
- **Native plugin artifacts** — `.codex-plugin/plugin.json`, a repo-local Codex
  marketplace (`.agents/plugins/marketplace.json`), amended Claude manifests, a
  bundled-engine launcher (`scripts/debate-plugin`) that never depends on a
  PATH-installed `debate`, and the `debate-onboarding` skill (setup + start-a-debate
  UI flows).
- **Manual bridge seats** — `debate seats add` accepts `{input_path}`/`{result_path}`
  commands (brokered bridges), alongside the v1 `{prompt}` style, and a
  `--cost-mode` declaration (subscription, api, local; default unknown).
- **Declared cost and authorship, never guessed** — every seat carries a
  `cost_mode` declaration (default "unknown" = undeclared, reported as such and
  treated as potentially metered) shown in the approval table, in
  `onboarding status`, and before any smoke spend. Declare or correct it any
  time — for catalog, derived, and manual seats alike — with
  `debate seats set-cost-mode SEAT MODE`; discovery never touches the
  declaration. `open --brokered` requires `--author-vendor` (normalized,
  validated against known vendors — a typo refuses instead of silently
  degrading), and a seat sharing the interactive author's vendor is recorded
  author-affiliated in the adapter config and channel provenance.
- **Any tool can hold a seat in a debate Debate runs itself** — a seat whose command
  takes the question text is now run through Debate's own runner, carrying the
  arguments that turn that tool's settings, plugins and session saving off while it
  reviews. Claude and Codex seats carry those arguments from the packaged catalog and
  need nothing declared; for any other tool they are declared once. Nothing waives the
  rule: a seat without them is refused in plain words, naming the two ways forward
  (declare the arguments, or record a seat command of your own). Because an ordinary
  tool never reports which model actually answered, every entry such a seat posts
  states that its model identity is declared rather than verified
  (`runtime-model-basis: declared`), which configuration folder it read
  (`configuration-home`), and where its isolation arguments came from
  (`isolation-flags`). Gated on `plan-v080-part2-63227` (PASS, MSG-38).
- **Detected launcher scripts** — `onboarding inspect` lists a launcher script found
  next to a tool Debate already knows as a candidate of its own, with its model
  unverified; `approve` refuses such a row outright and points at the declaration that
  turns it into a real seat. Detection stays evidence, never approval. Gated on
  `plan-v080-part2-63227` (PASS, MSG-38).
- **Declared capability classes and the uneven-pair warning** — a seat can say how
  capable it is (frontier or lightweight; the packaged catalog declares it for the
  tools it knows). Pairing a lightweight model against a frontier model is warned
  about and confirmed, never seated quietly: interactively it is a numbered choice,
  and where nobody can answer it is refused until `--allow-mismatched-pair` says so
  deliberately — `--yes` never answers it. Gated on `plan-v080-part2-63227`
  (PASS, MSG-38).
- **`debate seats add` declaration flags** — `--capability-class`, `--isolation-argv`,
  `--no-persistence-argv` and `--config-home VAR=dir`, so one command records
  everything a tool needs to take part. The configuration folder is validated: a
  documented or well-formed variable name, and a folder strictly inside your home
  directory. Gated on `plan-v080-part2-63227` (PASS, MSG-38).

### Changed

- The plugin bundles the engine; `pip install debate` remains the standalone
  CLI/automation distribution and does not register any host integration.
- The product path reads a MISSING `debate-profile.json` as "not approved" and offers
  setup; the direct CLI keeps the 0.7 "no file, no restriction" reading.
- `onboarding status` explains vanished binaries, failed and stale smoke, stale
  registries, and duplicate approved commands before they bite at open time.
- Uninstalling the plugin removes host integration only; registries, profiles, and
  channel records are user data and are never deleted.
- **Field-test fixes (owner acceptance pass, 2026-08-20):** the seat registry is
  written atomically and smoke results apply through a locked read-modify-write
  (two concurrent smokes no longer lose a result); smoke scratch channels live
  under the registry's own directory, never the system temp dir; `debate watch`'s
  `--interval` now defaults from a brokered config's `scheduler_interval_seconds`
  (the product open writes 5s; cron deployments pin `--interval` explicitly —
  previously the loop idled on a 180s default regardless of config);
  `watch-status` reports a brokered seat invocation as in flight while its own
  invocation age is within the largest adapter budget, instead of STALE; a
  post-open registry bookkeeping failure warns instead of crashing and orphaning
  the freshly created channel.

## v0.7.0 — 2026-08-18

**The machine's models become seats you can pick from.** Until now the pair
arguing a debate was whatever you hand-wrote into a watcher config, and a fresh
machine meant rediscovering which CLIs existed and what invocation each wanted.
This release makes the host's installed model CLIs a first-class registry, and
makes choosing the arguing pair an explicit act at the debate's birth rather
than a config file you edit later.

### Added

- **A packaged seat catalog** — what each supported vendor CLI is and how it is
  invoked, carrying only verified strings. Where a wrapper pins its model the
  catalog says so rather than guessing; a vendor whose invocation could not be
  verified on real hardware is omitted, and the omission is documented in the
  module rather than filled in with a plausible-looking command.
- **A host seat registry** at `~/.config/debate/seats.json`. `debate seats
  discover` scans the machine and merges — it never clobbers: an entry whose
  binary has gone away is marked absent rather than deleted, operator-authored
  entries are left strictly alone, and writes are screened so a credential can
  never land in the file. Each seat carries a list of endpoint options, and
  selection takes the first listed.
- **A source taxonomy that makes "who owns this entry" answerable**: `catalog`
  (discovery owns it), `derived` (an `@effort` variant the tool derived, and
  will re-derive when its base moves), `manual` (yours, untouched). Removal
  follows ownership: manual, derived and absent-catalog seats can be removed; a
  present catalog seat is refused because the next scan would only put it back.
- **`debate seats`** — `discover`, `list`, `check`, `doctor`, `smoke`, `add`,
  `remove`, with `--json` on the reporting surfaces so other tools can consume
  them. `check` exits non-zero only for a missing binary or a failed smoke;
  never-smoked is information and stale is a warning, because a freshness
  report that fails on staleness trains you to ignore it.
- **`debate open`** — the arguing pair is chosen when the debate is born.
  The previous pick is offered as the default, keyed by the enclosing repo
  rather than the channel folder, so a project remembers its own pair. Seating
  the same vendor and submodel twice is refused unless you say so explicitly —
  a monologue is always a deliberate choice, never an accident. Every path is
  validated before the first byte is written, so a refusal leaves the channel
  root empty rather than half-built, and the chosen seats are recorded in the
  channel's `.debate.json` with their exact command and smoke state.
- **A per-project `debate-profile.json` allowlist** — commit it to restrict
  which seats a given repository may seat. It fails closed: malformed, unknown
  version, unknown seat id or empty allowlist all refuse and name the offender.
- **An upgrade-triggered re-scan.** When the installed tool version moves, the
  next `seats` command re-scans and persists the new stamp — scan only, never
  an automatic smoke, because smoking costs tokens and that is your call.

### Fixed

- **Test suite hermeticity.** The suite pinned pytest's basetemp inside the
  checkout, so tests that opened channels wrote their toplevel watcher configs
  into the real working tree — and one refusal test only passed because an
  earlier run had left the very file it expected to find. Its first clean run
  planted what made later runs pass, which is why CI failed on a fresh checkout
  and local runs did not. Git discovery is now fenced to the test sandbox.
- **`seats remove --help`** described only manual seats while the code removed
  three kinds, and the subcommand had no description at all.

### Changed

- **The shipped protocol template** carries a new rule: a debate never
  constrains the size of the artifact under review, and findings, evidence and
  provenance are never compressed to fit a length. A case that argues from half
  its evidence has established nothing, whatever verdict it records.

At this tag the suite is 469 test items and `src/` is 6,818 lines. The plan and
the branch each passed this project's own review channel before merge; the
append-only, tamper-evident record is under [`collab/`](collab/).

## v0.6.0 — 2026-08-13

**Wiring the seats stops being hand-rolled.** `debate init` always scaffolded the
channel and left the hard part — watcher config, pinned prompts, the channel's
PROTOCOL.md, the scheduler — to hand-editing, which is where this project's own
expensive mistakes lived. `debate setup` moves that failure surface into the tool:
it interviews (or takes flags), derives everything derivable from the channel id,
validates through the real config loader before writing a byte, smokes the actual
seat contract on a scratch channel, and prints the scheduler units. Two review
rounds rejected it before it shipped; all six findings are folded into what you
get.

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
