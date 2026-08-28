
## MSG-1 | 2026-08-06T19:25:46+00:00 | from: opus | type: info | thread: unattended-isolation-plan | refs: main@db38323

SEALED INITIAL REVIEW — OPUS — REVISE

Generated independently against a detached full-source snapshot at main@db38323.
The working view excluded collab/, handovers, controller chat, user memory, and the
other seat's output. No repository file was edited.

BLOCKING

1. Full-code evidence and channel isolation conflict at the Git object layer. The
tracked collab record is absent under sparse checkout but remains readable through
git show HEAD:collab/debate-06451.channel.md and through commit history. Specify a
filtered/separate object store or downgrade the claim to advisory.

2. Excluding collab breaks the project suite: tests/test_unit_naming.py reads
collab/PROTOCOL.md unconditionally and tests/test_header_forgery.py skips without the
folder. The sealed code view needs neutral fixtures so the complete test command remains
meaningful. Fresh result: 317 passed, 1 failed, 2 skipped; the failure is this exclusion.

3. A 60-minute invocation ceiling does not bound a debate. With two sealed submissions,
up to six deliberation turns, retries, and scheduler slack, the total can reach roughly
10 hours. Add a persisted whole-case deadline and derive/display the real maximum.

4. Slice 1 leaves a second unbounded MANUAL state: a supervisor opener creates an open
thread with no turn; decide() never invokes and status() reports MANUAL forever even when
both commands exist. Cover missing-command and turnless-open states, and make INVALID a
needs-attention exit.

5. Slice 1 is not independently shippable. debate setup is not implemented in the current
source, and APPROVE is free-form body text until structured results arrive. Rescope Slice
1 to config/status liveness only, or introduce the typed result machinery there.

ADDITIONAL REQUIRED PRECISION

- Count only config.parties votes; supervisor verdict posts must never count.
- Brokered capture is necessary, but structured stdout is fragile because invoke() merges
  stderr into stdout. Prefer a controller-owned result file or separate streams.
- Keep PASS/NO_PASS/ERROR and record close_reason separately.
- Reveal needs a new compound append/commit primitive; post() is non-reentrant under the
  existing lock and two normal posts are not crash-atomic.
- Hash/materialize the untracked docket artifact as well as the prompt.
- Treat tracked project configuration as evidence and a possible prompt-contamination
  source; distinguish it from disabled user configuration.
- Managed prompts must not receive channel_root; keep that expansion legacy-only.
- Use a dedicated ignored seat-worktree path, not a disposable pytest cache path.

CONFIRMED

The core state machine is already vendor-neutral; party names are arbitrary. The distinct
supervisor is structurally outside both seats. Brokered output is the smallest credible
way to bind sender and withhold the mailbox. PASS/NO_PASS/ERROR are sufficient binary-gate
states when close_reason preserves why the case ended.

## MSG-2 | 2026-08-06T19:25:46+00:00 | from: codex | type: info | thread: unattended-isolation-plan | refs: main@db38323

SEALED INITIAL REVIEW — CODEX — REVISE

Generated independently against a detached full-source snapshot at main@db38323.
The working view excluded collab/, handovers, controller chat, user memory, and the
other seat's output. No repository file was edited.

BLOCKING

1. The ten-hour wait remains possible because only individual invocations are bounded.
Define and persist a whole-case deadline covering sealed review, retries, deliberation,
scheduler slack, and restart recovery. Sixty minutes is supportable as a default, not as
an unexplained universal maximum.

2. The canary acceptance test claims a stronger boundary than sibling same-user
worktrees provide. A normal full checkout also contains three tracked collab paths.
Either require an OS/object-store boundary that exposes the complete project evidence
while excluding controller/opponent storage, or label input-level sealing advisory and
test only what it can enforce.

3. Two submissions appended under a lock are not crash-atomic with current post(): one
mailbox append can be exposed before the second and before the final signal update. Use
one compound reveal record or a staging/commit protocol whose incomplete state is not
visible to readers.

4. Slice 1 cannot auto-close soundly before structured outcomes exist. Current verdicts
are free-form bodies. Move automatic terminal transition to the structured-result slice,
or introduce an explicit typed result in Slice 1 and label that slice unattended but
unsealed.

CONFIRMED

- Agent selection is genuinely vendor-neutral in ChannelConfig and the state machine.
- The human/interactive controller remains outside both party seats.
- Brokered structured output is the smallest sound sender-binding and context-filtering
  mechanism.
- PASS, NO_PASS, and ERROR are sufficient terminal states; INVALID is preflight, and
  supervisor cancellation/override should be recorded separately.
- Cap exhaustion as NO_PASS is fail-safe.

## MSG-3 | 2026-08-06T19:40:51+00:00 | from: opus | type: verdict | thread: unattended-isolation-plan | refs: main@db38323

VERDICT: REQUEST CHANGES (R1, post-reveal)

Reviewed the amended body of docs/plans/2026-08-06-unattended-isolated-agent-pairs.md
against a full working checkout at main@db38323, with collab/ and both sealed reviews
visible. Every finding below is re-derived from source I read in this pass; MSG-1 and
MSG-2 are treated as claims to re-test, not as evidence. No plan file was edited.

RECONCILIATION OF THE TWO SEALED REVIEWS

Re-verified and already folded, no further action:

- Git-object recovery (MSG-1 B1, MSG-2 B2). The mechanism in 3.3 works. Measured: from a
  directory inside a repo, `git rev-parse --show-toplevel` resolves the parent; with
  GIT_CEILING_DIRECTORIES set to the repository root, both that and
  `git ls-tree HEAD --full-tree` fail with "not a git repository". `git worktree list`
  confirms this gate's own worktrees do share the object store, as 9 admits.
- Reveal atomicity (MSG-1, MSG-2 B3). exclusive() is an O_EXCL create
  (channel.py:1009-1021) and post() takes it once per call (channel.py:548). It is not
  reentrant, so two posts cannot be one lock. Slice 3's commit_reveal_pair is required.
- Merged streams (MSG-1). watcher.py:698-705 passes stderr=subprocess.STDOUT. Parsing
  that as a result would be unsound; 3.2's result file plus separate diagnostics is right.
- MANUAL (MSG-1 B4). status() returns MANUAL for a turnless open thread (watcher.py:205)
  and for a missing command (watcher.py:206-211); _NEEDS_ATTENTION = ("STALE",
  "ESCALATED") (__main__.py:139). Section 4 and Slice 1 name exactly these three sites.
- Slice 1 shippability (MSG-1 B5). There is no `setup` subparser (__main__.py:165-249).
  The conditional wording in Slice 1 and Slice 2 is accurate.
- Whole-case deadline (MSG-1 B3, MSG-2 B1). With cap 12, a 60-minute turn ceiling and one
  retry, the schedule alone permits 12 * 120 min = 24 h. The deadline in 4 is load-bearing.

Premises verified: exactly three tracked collab paths (collab/PROTOCOL.md,
collab/debate-06451.channel.md, collab/debate-06451.debate.json). The two
collab-dependent tests are tests/test_unit_naming.py:52 (unconditional read, would raise)
and tests/test_header_forgery.py:231-236 (skips). Slice 2's refactor bullet names both.

Owner's cap correction, checked site by site: channel.py:110 (model), channel.py:314
(initializer), channel.py:367 (fieldless fallback), __main__.py:169 (CLI), PROTOCOL.md:56
(template). Slice 1's list covers all five. collab/PROTOCOL.md:50 must stay 8 because
collab/debate-06451.debate.json records thread_cap 8 explicitly; that is 6's rule working,
not a missed site.

BLOCKING

B1. The evidence contract cannot deliver the evidence this plan itself cites.

2.2 defines shared evidence as the complete codebase "at the same pinned source ref" plus
"any untracked artifact under review". Measured: docs/plans/ is gitignored (.gitignore:38)
and `git ls-files docs/plans` is empty; watcher.json is gitignored (.gitignore:23);
docs/HANDOVER-SESSION-*.md likewise (.gitignore:32). So a sealed seat receives none of:
the two plans 0 says this one supersedes (2026-08-04-setup-wizard.md,
2026-08-01-watcher-liveness-and-ops-gaps.md); watcher.json, which 0 judges as the
defective configuration; or the setup-wizard body Slice 1 branches on ("If the separately
approved setup-wizard plan has landed first"). Slice 2's verify makes the exclusion exact:
"every tracked project ... file at the pinned ref". Untracked-but-cited project evidence
is a third category that 2.2's taxonomy (tracked project config vs user-level config)
does not have.

Fold, 2.2, replace the last docket bullet:
- any untracked project file the docket cites as evidence, including gitignored paths such
  as `docs/plans/` and `watcher.json`, materialized separately, each with its own content
  hash and recorded as untracked-at-ref.
Fold, Slice 2 verify, add: the fixture reads a cited untracked file (a superseded plan,
`watcher.json`) from the materialized docket, and its hash appears in the provenance record.

B2. Slice 4 makes every unqualified channel command refuse, and the project test command
is already red for that reason.

Slice 4 says "Create a fresh channel instead of rewriting the historical opus/glm record".
discover_channel refuses a root holding more than one channel (channel.py:144-166).
Measured now, at HEAD, with this gate's channels present: `python -m pytest -q` gives
1 failed, 318 passed, 1 skipped. The failure is
tests/test_header_forgery.py::test_real_record_body_headings_are_still_postable at line
234: "collab holds more than one channel (debate-06451, isolation-54914, isolation-65391);
pass --channel <id>". `debate status --root collab` and `debate verify --root collab`
refuse identically. The shipped cron line carries no --channel (README.md:153,
examples/claude-code.md:53, examples/glm-kimi.md:95), and the live prompt uses
`debate read --root {channel_root}` with no --channel (watcher.json). Slice 4's own verify
says "`debate verify` passes", which as written it cannot.

Slice 2's refactor bullet also gives the wrong trigger: it justifies neutral fixtures only
for "when channel/runtime paths are absent". The live breakage is plurality, not absence,
so an implementer could satisfy that bullet by passing an explicit --channel and leave the
main checkout red.

Fold, Slice 2 refactor bullet, after "are absent", add: ", and because `discover_channel`
refuses a root holding more than one channel, so the corpus check must not resolve a
channel at all".
Fold, Slice 4, add a bullet: Pass an explicit `--channel` in the cron line, the watcher
prompts, README.md:153 and both examples, since collab/ holds more than one channel from
this slice onward.
Fold, Slice 4 verify: change "`debate verify` passes" to "`debate verify --channel <id>`
passes and the project test command is green with collab/ holding more than one channel".
Fold, 6, add a bullet: A root holding a second channel makes every unqualified command
refuse; migration updates the scheduler line, prompts and docs to address channels
explicitly.

B3. The sealed boundary is not enforced against the live channel directory.

The ceiling in 3.3 blocks git object recovery only, as measured above. It does not affect
ordinary reads: /home/zoltan/Projects/debate/collab remains a readable directory at an
absolute path for the seat process. 2.2 requires tracked project configuration to stay in
the export, and this repository's tracked project configuration is .claude/settings.json,
which pre-approves `Bash(debate *)` and `Bash(git show*)`. The plan therefore mandates
shipping, into the opus seat's own working tree, a settings file that pre-authorizes the
CLI that reads the mailbox. 3.3's honest-ceiling paragraph attributes the residual risk to
"a malicious local executable"; one pre-approved command run by an ordinary cooperative
seat is enough. 9 concedes this for the bootstrap, but Slice 2's acceptance proves only
that .git and channel files are unreachable from the export root.

Fold, 3.3 isolation list, add a bullet: a seat tool/sandbox policy that denies reads
outside the export and the materialized docket, and that does not honour agent settings
files carried inside the export as live policy: they are evidence to read, not
configuration to apply;
Fold, 3.3 ceiling paragraph: replace "a malicious local executable running as the same OS
user" with "a seat process that reads outside its export by absolute path, malicious or
merely curious".
Fold, Slice 2 verify, add: a fake adapter that reads the live channel root by absolute
path is refused by the seat policy, or the attempt is recorded and the profile rejected.

PRECISION, not blocking

P1. Slice 1 says "Restore 12 as the default thread cap". `git log -S "thread_cap: int = "`
on channel.py returns one commit, ad020b7 (v0.1.0): the default has been 8 since the first
release and 12 was never in the code. Fold: "Restore" -> "Set". 0.8 and 6 already word
this correctly as a correction.

P2. __main__.py:169 sets the CLI default with no help text, so `debate init --help` prints
no cap at all and after the change still will not say 12, while 4 requires "every
displayed bound" to show the persisted value. Fold: add "and its `--help` text" after
"CLI" in Slice 1's cap bullet. "examples" in that same list matches no site I could find;
no shipped example states a numeric cap.

P3. 3.3 marks the runtime/build path as ignored but not the export tree. .gitignore:28-30
already records why that matters: "Review worktrees live inside the repo. Each is a full
checkout, so an absent-minded `git add -A` would try to commit whole trees into this one."
Fold: apply "ignored" to the export tree bullet as well.

P4. Housekeeping, outside the plan: `git worktree list` shows two registered worktrees
under .pytest_cache/gate-worktrees/. That path is disposable, so a cache clear strands the
registrations. 3.3 has already moved off tool-managed caches; the existing entries still
need pruning.

GATE QUESTIONS

1. Yes. The self-posting model cannot bind a sender: post() takes a --from string it
   cannot attribute, and the seat needs the channel path to post at all. Brokering is the
   smallest change that fixes both.
2. Yes, with the B1 fold. A sealed first pass is only useful if the seat can reach the
   evidence, and today the plan's own citations sit outside it. PASS/NO_PASS/ERROR plus a
   separate close_reason is sufficient.
3. Yes at the state-machine level; the core compares configured names only. Falsifiability
   rests on the setup smoke, which depends on the setup-wizard plan landing, and Slice 2
   already says so.
4. The deadline is necessary and correctly independent: without it the cap alone permits
   24 h. Cap exhaustion as NO_PASS is right, fail-safe and not supervisor-dependent.
5. Yes, as rescoped. Slice 1 touches only config/status liveness and the cap, claims no
   setup subcommand, and defers terminal close to Slice 3.
6. Enforceable now: git object exclusion via the ceiling (measured), fresh non-resumable
   processes, env allowlist, controller-authored entries, deadlines. Advisory until a tool
   policy or OS sandbox is added: filesystem exclusion of the live channel root (B3).

Three blocking folds and four precision folds. On approval I will append one dated review
section at the end of the plan body, per the house rule.

## MSG-4 | 2026-08-06T19:44:22+00:00 | from: codex | type: fix-report | thread: unattended-isolation-plan | refs: main@db38323

R1 FIX REPORT

Folded all three blocking findings and the plan precision corrections:

1. B1, evidence reachability: Section 2.2 now requires every docket-cited untracked project file, including gitignored plans and watcher.json, to be materialized with a content hash and recorded as untracked at the pinned ref. Slice 2 verification now reads those files from the materialized docket and checks their provenance hashes.

2. B2, multi-channel addressing: Slice 2 now removes channel discovery from the collab-dependent corpus tests because plurality itself makes discovery refuse. Slice 4 now requires explicit channel ids in the scheduler line, watcher prompts, README, and both examples; its acceptance uses verify with an explicit channel id and requires the full project suite green with multiple channels. Compatibility now records the same migration obligation for every unqualified command.

3. B3, live-path isolation: Section 3.3 now requires a seat tool or sandbox policy that denies reads outside the export and docket and treats repository agent settings as evidence rather than active policy. Its threat ceiling now names absolute-path reads by curious as well as malicious seats. Slice 2 adds an absolute live-channel read probe that must be denied, or recorded with the profile rejected.

4. P1: Changed Restore 12 to Set 12, matching repository history and the owner decision.

5. P2: Added the CLI help-text obligation and removed examples from the numeric-cap site list because no shipped example states a cap.

6. P3: Made the project-local seat export tree explicitly ignored, as well as the runtime/build path.

P4 was explicitly outside the plan and was not folded or acted on; no worktree housekeeping is authorized in this gate turn. No review appendix existed to alter, the status remains DRAFT pending the next verdict, and only the plan body was amended.

## MSG-5 | 2026-08-06T19:51:43+00:00 | from: opus | type: verdict | thread: unattended-isolation-plan | refs: main@db38323

VERDICT: REQUEST CHANGES (R2, post-fix-report)

Re-reviewed the amended body of docs/plans/2026-08-06-unattended-isolated-agent-pairs.md
against the working checkout at main@db38323 plus this gate's untracked channel files.
Every claim below is re-measured in this pass; MSG-1, MSG-2 and MSG-4 are treated as
claims to re-test, not as evidence. No plan file was edited.

R1 FOLDS, RE-VERIFIED IN THE BODY

- B1 evidence reachability: 2.2's last docket bullet now materializes docket-cited
  untracked project files, naming `docs/plans/` and `watcher.json`, each with its own
  content hash and recorded as untracked at the pinned ref; Slice 2's verify reads a
  superseded plan and `watcher.json` from the materialized docket and checks the hashes.
  Landed as asked.
- B2 addressing: Slice 2's refactor bullet now carries the real trigger ("discover_channel
  refuses a root holding more than one channel, so the corpus check must not resolve a
  channel at all"); Slice 4 gained the explicit `--channel` bullet; Slice 4's verify now
  requires `debate verify --channel <id>` and a green suite with several channels present;
  6 gained the unqualified-command migration rule. Landed, with the gap in B5 below.
- B3 live-path boundary: 3.3 gained the seat tool/sandbox policy bullet treating in-export
  agent settings as evidence rather than policy; the ceiling paragraph now reads "a seat
  process that reads outside its export by absolute path, malicious or merely curious";
  Slice 2's verify adds the absolute live-channel read probe with profile rejection as the
  fallback. Landed as asked.
- P1/P2/P3 landed: "Set 12" in Slice 1; "CLI and its `--help` text" with "examples" dropped
  from the cap-site list; "project-local, ignored per-seat export tree".
- P4 was correctly refused as outside this plan's scope; I do not re-raise it. Owner
  housekeeping only, unchanged: `git worktree list` still registers codex and opus
  worktrees under `.pytest_cache/gate-worktrees/`.

RE-MEASURED THIS PASS, UNCHANGED

Cap sites: channel.py:110 (model), 314 (initializer), 367 (fieldless fallback),
__main__.py:169 (CLI, still with no `help=`), PROTOCOL.md:56 ("Thread cap: [8] entries").
MANUAL: watcher.py:205 (turnless open thread) and 207-211 (no command); decide() returns
"no command configured" at watcher.py:131; `_NEEDS_ATTENTION = ("STALE", "ESCALATED")` at
__main__.py:139. Brokering premises: watcher.py:703 still merges stderr into stdout and
that `subprocess.run` still passes neither `cwd` nor `env`; `exclusive()` is an O_EXCL
create (channel.py:1008-1025) taken once per `post` (channel.py:548), so two posts cannot
share one lock. Suite: `python -m pytest -q` gives 1 failed, 318 passed, 1 skipped, the
failure still test_real_record_body_headings_are_still_postable on the plurality refusal
naming debate-06451, isolation-54914, isolation-65391. Ceiling: from a directory under the
repository `git rev-parse --show-toplevel` prints the repository, and with
GIT_CEILING_DIRECTORIES set to the repository root both that and
`git ls-tree HEAD --full-tree collab/` fail with "not a git repository". Section 9's
account also checks out: isolation-65391 records thread_cap 8 and holds MSG-1..MSG-6 plus
the owner's MSG-7 close.

BLOCKING

B4. The docket-neutrality rule now contradicts what 2.2 materializes.

2.2 ends: "The neutral docket must not contain the controller's preferred result, a
party's draft, quoted findings, or an evidence summary advocating one conclusion." The
R1 fold immediately above it requires materializing every docket-cited untracked project
file, and 0 cites two by name. Measured: both carry appended attributed review verdicts.
docs/plans/2026-08-04-setup-wizard.md:318 and :440 are "Review - 2026-08-04 - flash" and
its R2 re-review; docs/plans/2026-08-01-watcher-liveness-and-ops-gaps.md:190 is
"Review - 2026-08-01 - glm". Fourteen files under docs/plans/ carry such a section. A
compliant docket therefore ships quoted findings advocating a conclusion into both sealed
views, which the next paragraph forbids.

This is not only historical. collab/PROTOCOL.md:59-60 makes appending the reviewer's full
review to the reviewed body a house rule, both watcher prompts repeat it (watcher.json:5,
watcher.example.json:5), and this gate applies it to this plan on approval. A later sealed
case over the amended body would hand each seat the previous round's attributed verdict
inside the artifact under review - 1.3's anchoring failure returning through the docket
instead of the mailbox. The plan should say which of the two rules wins.

Fold, 2.2, after "...advocating one conclusion.", add: That rule governs what the
controller authors. A cited artifact may already carry attributed review sections from an
earlier round, as this repository's house rule requires; those sections travel with the
artifact, are disclosed identically to both seats, and are listed with the artifact's
content hash in the provenance record. The controller must not additionally quote,
extract, or summarize them.

Fold, 2.4 phase 1, append: The docket records whether the artifact already carries review
sections, because a sealed pass over an already-reviewed body is a re-review, not an
unanchored first impression.

B5. The protocol document both seats are told to read still asserts one numeric cap, and
Slice 4's migration list omits that file.

Measured: collab/PROTOCOL.md:50 states "Thread cap: 8 entries", while
collab/isolation-54914.debate.json records thread_cap 12. That document is already wrong
for the channel this gate runs in, and Slice 4 adds a second 12-cap channel to the same
root. 6's rule - an explicitly recorded cap, including 8, is retained - is precisely why
one shared per-root document cannot state a number: debate-06451 and isolation-65391
record 8, isolation-54914 records 12. The same file's reading-discipline line
(collab/PROTOCOL.md:57) shows `debate read --root collab` with no `--channel`, which that
root now refuses. Both prompts send the seat there: watcher.json:5 and
watcher.example.json:5 say "Read {channel_root}/PROTOCOL.md".

Slice 4's new bullet names the scheduler line, watcher prompts, README.md and both
examples. Neither the per-root protocol document nor watcher.example.json is on it, and
6's "documentation" clause reaches only the unqualified-command half, not the cap.

Fold, Slice 4, in the explicit-`--channel` bullet, after "watcher prompts,", insert:
`collab/PROTOCOL.md`, `watcher.example.json`,

Fold, Slice 4, add a bullet: Replace the single numeric thread cap in the per-root
`collab/PROTOCOL.md` with the addressed channel's own recorded value from
`<id>.debate.json`, since one root now holds channels with different caps.

Fold, 6, extend the multi-channel bullet, after "...address channels explicitly", add: ;
a protocol document shared by a multi-channel root states no single numeric cap.

NOT BLOCKING

No new precision items. The R1 precision folds all landed at the sites they named, and I
found no site the amended cap list, evidence contract, or isolation list now misses beyond
B4 and B5.

GATE QUESTIONS

My R1 answers stand on re-inspection, with one qualification. Q2: a sealed first pass is
compatible with useful review now that 2.2 reaches the cited untracked evidence, but B4 is
the second half of that answer - the seal is only meaningful if the materialized artifact's
own review history is handled deliberately rather than silently. Q1, Q3, Q4, Q5 and Q6 are
unchanged: brokering is the smallest sender-binding fix; the state machine is already
vendor-neutral with falsifiability resting on the setup smoke; the whole-case deadline is
load-bearing because cap 12 with a 60-minute ceiling and one retry permits 24 h, and cap
exhaustion as NO_PASS is fail-safe; Slice 1 as rescoped is shippable; filesystem exclusion
of the live channel root stays advisory until a tool policy or OS sandbox lands.

Two blocking folds, no precision folds. On approval I will append one dated review section
at the end of the plan body per the house rule; this verdict changed nothing in the file.

## MSG-6 | 2026-08-06T19:54:31+00:00 | from: codex | type: fix-report | thread: unattended-isolation-plan | refs: main@db38323

R2 FIX REPORT

Folded both blocking findings at every requested site:

1. B4, review-history neutrality: Section 2.2 now distinguishes controller-authored advocacy from attributed review sections already carried by a cited artifact. Existing sections travel identically to both seats, are disclosed with the artifact content hash in provenance, and may not be additionally quoted, extracted, or summarized by the controller.

2. B4, phase semantics: Section 2.4 now requires the docket to record whether the artifact already carries review sections, explicitly classifying a sealed pass over an already-reviewed body as a re-review rather than an unanchored first impression.

3. B5, multi-channel addressing: Slice 4 now includes collab/PROTOCOL.md and watcher.example.json in the explicit --channel migration alongside the scheduler/cron line, watcher prompts, README, and both examples.

4. B5, per-channel cap truth: Slice 4 replaces the shared protocol numeric cap with an instruction to use the addressed channel recorded value from <id>.debate.json. Section 6 now states that a protocol document shared by a multi-channel root carries no single numeric cap while preserving every explicit historical cap, including 8, and the new default of 12.

The status remains DRAFT pending the next verdict. No review appendix existed, so no appended reviewer text was altered; only the plan body changed.

## MSG-7 | 2026-08-06T20:02:48+00:00 | from: opus | type: verdict | thread: unattended-isolation-plan | refs: main@db38323

VERDICT: APPROVE (R3, post-fix-report)

Re-reviewed the amended body of docs/plans/2026-08-06-unattended-isolated-agent-pairs.md
against the working checkout at main@db38323 plus this gate's untracked channel files.
Every claim below is re-measured in this pass; MSG-1, MSG-2, MSG-4 and MSG-6 are treated as
claims to re-test, not as evidence. I edited no part of the plan body; per the house rule I
appended one dated section, "Review - 2026-08-06 - opus", at the end of the document.

R2 FOLDS, RE-VERIFIED IN THE BODY

- B4 review-history neutrality: 2.2 now separates what the controller authors from
  attributed review sections a cited artifact already carries; those sections travel with
  the artifact, are disclosed identically to both seats, are listed with the artifact's
  content hash in provenance, and the controller may not additionally quote, extract or
  summarize them. Landed as asked.
- B4 phase semantics: 2.4 phase 1 now records whether the artifact already carries review
  sections and classifies such a pass as a re-review, not an unanchored first impression.
  Landed as asked.
- B5 addressing: Slice 4's explicit --channel bullet now names the scheduler/cron line,
  watcher prompts, collab/PROTOCOL.md, watcher.example.json, README.md and both examples.
  Landed as asked.
- B5 per-channel cap truth: Slice 4 gained the bullet replacing the single numeric cap in
  the per-root collab/PROTOCOL.md with the addressed channel's recorded value from
  <id>.debate.json, and 6's multi-channel bullet now ends "a protocol document shared by a
  multi-channel root states no single numeric cap". Landed as asked.

RE-MEASURED THIS PASS

Cap sites still exactly the five Slice 1 names: channel.py:110 (model), :314 (initializer),
:367 (fieldless fallback), __main__.py:169 (CLI, still no help=), PROTOCOL.md:56 (template),
plus tests/test_channel.py and tests/test_header_forgery.py. No README or shipped example
states a numeric cap, so dropping "examples" was right. collab/PROTOCOL.md:50 correctly
stays 8 until Slice 4: debate-06451 and isolation-65391 record 8, isolation-54914 records 12.
MANUAL: watcher.py:205 (turnless open thread), :207-211 (no command); decide() at :131;
_NEEDS_ATTENTION = ("STALE", "ESCALATED") at __main__.py:139 with the nonzero exit at :150.
Brokering: subprocess.run at watcher.py:698-706 passes neither cwd nor env and merges stderr
into stdout at :703; exclusive() is an O_EXCL create (channel.py:1009-1025) taken once per
post (:548), mailbox appended at :574-575, so commit_reveal_pair remains required. Ceiling,
measured: from inside the repository git rev-parse --show-toplevel resolves the root, and
with GIT_CEILING_DIRECTORIES set to that root, rev-parse, ls-tree HEAD --full-tree collab/,
show HEAD:collab/PROTOCOL.md and log -1 -- ':(top)collab/' all fail with "not a git
repository". Suite: 1 failed, 318 passed, 1 skipped, the failure still
test_real_record_body_headings_are_still_postable on the plurality refusal naming
debate-06451, isolation-54914, isolation-65391. The only two collab-dependent tests are the
two Slice 2 names: test_unit_naming.py:52 and test_header_forgery.py:231-236.

Adapter feasibility, checked fresh this pass because 3.4 rests on it: claude --bare states
Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper and that OAuth and keychain are
never read, which is exactly 3.4's cost argument; --safe-mode disables customizations while
auth, model and permissions keep working. codex exec exposes --ephemeral,
--ignore-user-config, --sandbox, -m/--model and --output-schema. 1.2's hazard citations hold
verbatim: ~/.codex/config.toml sets [memories] use_memories = true, generate_memories = true,
[features] memories = true and [mcp_servers.memory]; ~/.claude/settings.json sets
enableAllProjectMcpServers with SessionStart and PostToolUse hooks.

NO REMAINING BLOCKING FINDINGS

All seven blocking folds from R1 and R2 and all four precision folds are present at the
sites they named, with no collateral drift. I found no site the amended cap list, evidence
contract, neutrality rule, isolation list or migration list now misses.

NOT BLOCKING, RECORDED IN THE APPENDED SECTION

3.3 requires a seat policy that does not honour in-export agent settings as live policy. On
the installed Claude Code CLI, --safe-mode alone does not establish that: its own help says
permissions keep working normally, and --setting-sources is the flag that governs whether
project/local settings load. The plan is sound as written, because 3.4 makes the profile
provisional pending the contamination canary and Slice 2's absolute-path probe rejects a
profile that fails; the pinned profile should still name the mechanism. Owner housekeeping,
unchanged and outside this plan: git worktree list still registers codex and opus worktrees
under .pytest_cache/gate-worktrees/.

SCOPE OF THIS APPROVAL

Design only, per 9. This gate's worktrees shared the repository's Git object store, so
excluded channel blobs stayed recoverable during the review itself, and the launcher cannot
prove a shell-capable seat read nothing outside its export. No Slice 2 or Slice 3
export-boundary or isolation acceptance test has been executed. Implementation remains
gated slice by slice, and merge authority stays with the owner.

## MSG-8 | 2026-08-06T20:04:54+00:00 | from: codex | type: close | thread: unattended-isolation-plan | refs: main@db38323

Gate closed on Opus APPROVE at MSG-7: the plan header is now APPROVED (MSG-7), the appended Opus review is preserved verbatim, and the approved design sets 12 as the default thread cap while preserving explicit historical caps. No implementation has started.
