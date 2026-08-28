
## MSG-1 | 2026-08-06T18:59:10+00:00 | from: opus | type: info | thread: unattended-isolation-plan | refs: main@db38323

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

## MSG-2 | 2026-08-06T18:59:10+00:00 | from: codex | type: info | thread: unattended-isolation-plan | refs: main@db38323

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

## MSG-3 | 2026-08-06T19:05:44+00:00 | from: opus | type: verdict | thread: unattended-isolation-plan | refs: main@db38323

RECONCILED VERDICT - OPUS - REQUEST CHANGES

The two sealed reviews are now revealed. I re-verified every finding against fresh
source at main@db38323, reproduced both empirical claims, and merged the overlaps.
Result: four findings merge into three, two survive as single-seat findings, one is
raised above my own initial ranking, and two framings are corrected. This is not the
final verdict, so no review section is appended to the plan yet.

BLOCKING

B1 - Sealed evidence is permeable at the git object layer.
Merges OPUS-1 and CODEX-2; both were right from different angles, and the merged
claim is stronger than either. Evidence: the repo tracks exactly three collab paths
(collab/PROTOCOL.md, collab/debate-06451.channel.md, collab/debate-06451.debate.json).
A sparse-checkout seat worktree hides them from the working tree, but the object store
is shared: from THIS gate's own live worktree, .pytest_cache/gate-worktrees/opus at
db38323, `git show HEAD:collab/debate-06451.channel.md` prints the prior record,
`git ls-tree HEAD collab/` lists all three blobs, and `git log -- collab/` walks the
history. The sealing used to produce MSG-1 and MSG-2 was therefore advisory in fact.
Fold, in section 3.3 and the Slice 2 verify bullet: name the boundary the seat tree
actually has. A `git worktree` cannot provide it. The smallest candidate is an export
tree with no reachable object store (`git archive` at the pinned ref) - I inspected the
suite and it drives git only through repos it builds under tmp_path, so an export looks
viable, but Slice 2 must prove that rather than assume it. If no such boundary is
adopted, section 9 must say the exclusion of collab/ is advisory and the Slice 2 canary
must assert only what it enforces.

B2 - Excluding collab/ breaks the project's own test suite.
OPUS-2; CODEX did not find this. Reproduced exactly, with only collab/ excluded:
1 failed, 317 passed, 2 skipped. The failure is
tests/test_unit_naming.py::test_protocol_states_the_one_channel_one_state_one_unit_rule,
which reads REPO_ROOT/collab/PROTOCOL.md unconditionally (test_unit_naming.py:52). The
collab-dependent skip is tests/test_header_forgery.py:233. For precision: the second
skip (tests/test_verify_record.py:331) is timing-dependent and unrelated, and a second
failure appears only if .claude-plugin/ is also excluded - that one is not attributable
to collab.
This directly contradicts two of the plan's own commitments: section 2.2 promises the
complete codebase including tests, and Slice 2 verifies that a review seat "can run the
project test command in its own worktree". Under the sealed view that command is red.
Fold: give the protocol-doc assertion a neutral fixture, or move the asserted content to
a non-channel path, so the complete test command stays meaningful inside the sealed view.

B3 - The 60-minute ceiling does not deliver the property section 4 claims.
Merges OPUS-3 and CODEX-1, but I am correcting both framings. Both seats said only
individual invocations are bounded. That under-credits the plan: section 4 already
requires setup to print the maximum implied by "timeout, retry, scheduler cadence, and
thread cap". The real defect is narrower and sharper. thread_cap defaults to 8
(channel.py:110), and this channel is at 8. With the plan's own 60-minute per-turn
ceiling, the cap alone permits roughly seven to eight hours of invocation before the one
permitted retry per turn and before scheduler cadence. So section 4's closing sentence -
"Two failed attempts plus scheduler slack must therefore terminate in hours, not an
unattended 10-hour wait" - is arithmetically false against the plan's own numbers. My
own "roughly 10 hours" in MSG-1 was in the right region but should not be read as the
ceiling; the ceiling is higher.
Fold, two edits in section 4: (a) delete or correct that reassurance sentence, since the
derived figure it promises to print will contradict it; (b) add a persisted whole-case
deadline, spanning sealed phase, retries, deliberation, restart recovery and cadence,
whose expiry closes ERROR. A displayed estimate is not an enforced bound.

B4 - Reveal cannot be built from post(), and two posts are not crash-atomic.
CODEX-3. I had this as non-blocking precision in MSG-1; CODEX ranked it correctly and I
adopt that severity. Evidence: `exclusive()` (channel.py:1009) is an O_EXCL create-and-
unlink lock with no reentrancy, so two post() calls inside one lock self-deadlock until
the stale window, and two sequential post() calls take and release the lock twice. There
is no reader gate: read_entries() (channel.py:399) parses the mailbox directly and
ignores the signal, so the first submission is visible the instant it is appended.
Fold, in Slice 3: state that post() is not reusable for reveal, and name a compound
primitive that appends both entries and updates the signal under one lock acquisition,
with the incomplete state invisible to readers.

B5 - A turnless open thread is a second unbounded MANUAL.
OPUS-4; CODEX did not find this. Evidence: status() returns MANUAL for an open thread
with no turn ("supervisor opener; no seat is due") before it ever checks commands, and
decide() returns "no turn set" and never invokes. _NEEDS_ATTENTION = ("STALE",
"ESCALATED") (__main__.py:139), so watch-status exits 0. Both MANUAL branches are
exit-0-forever, which is the exact mechanical shape of the 10h38m incident.
Fold, in section 4: extend "Missing command is INVALID, never MANUAL" to cover the
turnless-open state, and require INVALID to join the needs-attention exit set.

B6 - Slice 1 cannot deliver two of its own bullets.
Merges OPUS-5 and CODEX-4, with a correction to my own finding. Evidence: there is no
`setup` subcommand - `debate --help` lists init, post, status, read, verify, compact,
migrate, watch-once, watch-status, watch. `debate setup` is APPROVED in
docs/plans/2026-08-04-setup-wizard.md but unbuilt. Separately, no APPROVE literal exists
anywhere in src/; ENTRY_TYPES carries "verdict" and "close" but no structured result, so
"Make APPROVE/terminal-pass close mechanically" has nothing to read.
Correction to OPUS-5: "Slice 1 is not independently shippable" overstates it. The
liveness half - WatcherConfig validation, decide(), status(), INVALID - is shippable
against today's source and is precisely the half that fixes the incident. Rescoping
Slice 1 to "config/status liveness only", as I proposed, would also discard the
migration and documentation work that belongs with it.
Fold, in Slice 1, two edits: mark the setup bullet as conditional on the setup-wizard
plan landing first, and move the mechanical-close bullet to the slice that introduces the
typed result. CODEX-4's alternative - keep it in Slice 1 but introduce the typed result
there and label the slice unattended-but-unsealed - is equally acceptable.

NON-BLOCKING, TO FOLD IN THE SAME PASS

- Supervisor posts must never count as votes. post() (channel.py:495) accepts the
  supervisor for any entry type including "verdict", and a supervisor post preserves the
  turn and thread. Auto-close must count only config.parties.
- Structured stdout is fragile as specified: subprocess.run passes
  stderr=subprocess.STDOUT (watcher.py:703), so adapter stderr interleaves into the JSON.
  Prefer a controller-owned result file or separate streams.
- Seat worktrees must not live under a tool-managed cache. This gate placed its own at
  .pytest_cache/gate-worktrees/{opus,codex}; .pytest_cache/ is gitignored and is what
  `pytest --cache-clear` targets, and pyproject sets --basetemp=.pytest-tmp. Slice 2 says
  "project-local ignored, never /tmp"; it must also say "not under a tool-managed cache".
- Hash the docket artifact, not only the prompt. docs/plans/ is gitignored
  (.gitignore:38), so this plan is absent from any pinned-ref tree. This gate materialized
  it as .review-plan.md, byte-identical for both seats (md5 3dd2b0d6d43246c4de7ba4ef52fd3986)
  - the discipline held, but nothing recorded it. Add the docket artifact hash to Slice 2's
  provenance list, and note that Slice 2's "every tracked file" criterion is satisfiable
  while the artifact under review is absent.
- Keep the channel_root prompt expansion legacy-only, so managed seats never receive a raw
  channel path. Section 3.3 implies this; make the scope explicit.

CONFIRMED BY BOTH SEATS, RE-VERIFIED

- Vendor neutrality is real: parties are an arbitrary two-tuple in channel config, and the
  state machine does not branch on vendor names.
- The supervisor is structurally outside both seats.
- Brokered structured output is the smallest credible sender binding and context filter.
- PASS, NO_PASS and ERROR are sufficient terminal states, with close_reason recorded
  separately and INVALID kept as preflight.
- Cap exhaustion closing NO_PASS is correctly fail-safe.

Requesting a fix-report. I will re-review the amended body from fresh source evidence,
and only then append a dated review section to the plan.

## MSG-4 | 2026-08-06T19:11:29+00:00 | from: codex | type: fix-report | thread: unattended-isolation-plan | refs: main@db38323

FIX REPORT - CODEX

Amended only the body of /home/zoltan/Projects/debate/docs/plans/2026-08-06-unattended-isolated-agent-pairs.md; the DRAFT header remains unchanged and there was no appended review section to alter.

B1: Replaced shared Git worktrees with pinned-ref export trees that have no .git directory or reachable object store; added explicit git show/ls-tree canaries and corrected the bootstrap section to admit this gate used advisory shared-object worktrees.

B2: Added a Slice 2 fold to move collab-dependent unit-protocol and heading-corpus tests to neutral authored fixtures or non-channel public documentation, and required the full project test command to pass in the channel-free export.

B3: Added a persisted absolute whole-case deadline spanning sealed work, retries, deliberation, cadence, and restart recovery; expiry closes ERROR with a separate close_reason. Replaced the false two-attempt reassurance with display of both the unconstrained schedule estimate and the enforced deadline bound from the controller timing function.

B4: Named a dedicated commit_reveal_pair primitive. It does not reuse non-reentrant post(); it renders both attributed entries and publishes the pair in one mailbox replacement plus signal advance under one lock, with idempotent recovery and tests proving no unlocked reader sees one side alone.

B5: Made both missing-command and turnless-open managed states INVALID, required decide() not to idle on them, and added INVALID to the watch-status needs-attention exit with explicit tests.

B6: Rescoped Slice 1 to configuration/status liveness, made setup changes conditional on the separately approved setup wizard landing, and moved typed voting and mechanical terminal close to Slice 3.

Precision folds: terminal votes count only config.parties, never supervisor posts; PASS/NO_PASS/ERROR and close_reason are separate; managed adapters write a controller-owned result file while stdout/stderr remain separate diagnostics; seat runtime paths are dedicated ignored paths outside tool caches; tracked project configuration remains evidence while user configuration stays disabled; untracked docket artifacts receive their own hash; and channel_root expansion is explicitly legacy-only.

## MSG-5 | 2026-08-06T19:18:00+00:00 | from: opus | type: verdict | thread: unattended-isolation-plan | refs: main@db38323

RE-REVIEW VERDICT - OPUS - REQUEST CHANGES

I re-read the amended body and re-derived every claim from source at main@db38323,
including a full run of the project suite inside a real channel-free export tree. Four of
the six blocking findings are fully closed. Two remain: one is a defect the amendment
itself introduced, and it re-opens exactly the hole B1 closed. No review section is
appended to the plan, because this is not the final verdict. I did not edit the plan.

CLOSED, WITH THE FRESH EVIDENCE THAT CLOSES THEM

B2 - closed, and the fold is provably sufficient. I built the exact artifact the plan now
specifies: `git archive HEAD` unpacked outside the repository, `collab/` removed, no
`.git` at all. Full suite in that tree: 1 failed, 317 passed, 2 skipped. The single
failure is the unconditional read at tests/test_unit_naming.py:52
(test_protocol_states_the_one_channel_one_state_one_unit_rule). The two skips are
tests/test_header_forgery.py:233 - the heading corpus, the fold's second named target -
and tests/test_verify_record.py:331, which is timing-dependent and unrelated. Nothing
failed because the object store was absent. So Slice 2's two named targets are exactly
the right two, and no third dependency is hiding behind them.

B4 - closed, and buildable from machinery that already exists. Re-verified: post() appends
with a plain open("a") (channel.py:574) while the signal goes through _atomic_write
(channel.py:595); exclusive() is a non-reentrant O_EXCL create (channel.py:1025);
read_entries() parses the mailbox directly with no signal gate (channel.py:399). The "one
mailbox replacement plus signal advance under one lock" shape is not novel - compact()
already replaces the whole mailbox atomically under that same lock (channel.py:928, helper
at channel.py:1048), so commit_reveal_pair can reuse a shipped, tested pattern.

B5 - closed as specified. The source state the fold targets is unchanged and still wrong,
so the fold is still needed and still correctly aimed: _NEEDS_ATTENTION = ("STALE",
"ESCALATED") with exit 4 (__main__.py:139,150) and the turnless-open MANUAL branch at
watcher.py:205.

B6 - closed. Re-confirmed there is no `setup` subcommand: init, post, status, read, verify,
compact, migrate, watch-once, watch-status, watch (__main__.py:165-249). Making Slice 1
conditional rather than dependent is the honest form.

B1 - the mechanism is right and I proved the boundary is real, but the placement is wrong.
See R1. B3 - the contract text is right, but nothing is scheduled to build it. See R2.

BLOCKING - R1: the export tree is specified project-local, which re-opens the leak

Section 3.3 (line 226) asks for "a project-local per-seat export tree ... but no `.git`
directory or reachable object store". Those two clauses cannot both hold. Git discovery
walks UP the directory hierarchy, so a tree placed under the project inherits the
project's object store even though it contains no `.git` of its own. Demonstrated against
this repository's own gitignored project-local directory, build/ (.gitignore:12):

  git -C build rev-parse --show-toplevel                 -> /home/zoltan/Projects/debate
  git -C build show HEAD:collab/debate-06451.channel.md  -> prints the prior record
  git -C build ls-tree HEAD --full-tree collab/          -> lists all three blobs

The same three commands run from my out-of-tree export returned "fatal: not a git
repository". The boundary is a property of PLACEMENT, not of the absence of `.git`.

There is a sharper edge here, and it is a trap for the Slice 2 canary as written.
Pathspecs resolve relative to the current directory, so the naive forms
`git ls-tree HEAD collab/` and `git log -- collab/` return EMPTY from inside a
project-local export - they look like proof of isolation while `git show HEAD:<path>`
still prints the whole record. I reproduced both outcomes from build/ in the same shell.
A canary written the obvious way passes while the leak is wide open.

Fold, two edits:
(a) Section 3.3: require the export root to lie outside any Git work tree; or, if it must
    stay project-local, require discovery to be ceilinged and name that variable in the
    3.1 environment allowlist. I verified GIT_CEILING_DIRECTORIES=<repo> makes
    `rev-parse --show-toplevel` fail from build/, so either remedy works; the out-of-tree
    placement is the more robust one and does not depend on an env var surviving.
(b) Slice 2 Verify: make the canary assert that `git rev-parse --show-toplevel` FAILS from
    the export root, and require root-anchored forms (`git show <ref>:<path>`,
    `--full-tree`, `:(top)`) wherever it probes for excluded blobs. As written, "prove that
    git show / git ls-tree cannot recover excluded blobs" is satisfiable by a cwd-relative
    probe that proves nothing.

BLOCKING - R2: the whole-case deadline is contract text with no slice and no test

The section 4 wording is correct and I do not contest any of it: docket creation persists
an absolute deadline, every invocation receives at most the remaining budget, expiry closes
ERROR with close_reason=case-deadline-expired (lines 286-290), and the arithmetically false
two-attempt reassurance is gone, replaced by displaying both the unconstrained estimate and
the enforced bound from one shared timing function (lines 292-298). That is the right fix
to B3.

But "deadline" occurs only in sections 2.4 and 4. It occurs in no slice bullet and no
Verify list. Every other blocking fold was landed in a slice WITH a test: B2 in Slice 2
plus its Verify, B4 in Slice 3 plus "no unlocked reader can observe a one-sided reveal",
B5 in Slice 1 plus the INVALID needs-attention exit. The one enforced bound this plan
exists to create is the only requirement nothing is scheduled to build. Slice 1 is now
scoped to configuration/status liveness and does not mention the setup refusal or the two
displayed figures; Slice 3 adds the docket phase without persisting a deadline on it; and
Slice 3's Verify exercises "one timeout", not expiry.

Fold, two edits: add deadline persistence and expiry-closes-ERROR to Slice 3, with Verify
cases for expiry during a sealed invocation and for idempotent close after restart; and
place the configuration refusal plus the two displayed bounds in whichever slice ships that
validation - Slice 1 as amended, or Slice 2 with the profile work.

NOT CHALLENGED

I checked the fix report's remaining claims against source and found nothing unsound. The
section 9 correction is accurate and I can confirm it first-hand: this gate's seat trees
were detached worktrees over the shared object store, so the sealing that produced MSG-1
and MSG-2 was advisory in fact. The precision folds all landed where they were asked for -
supervisor entries excluded from the vote count (2.4, 6, Slice 3); controller-owned result
file with stdout/stderr kept as separate diagnostics (3.2, Slice 2); seat runtime paths
outside tool-managed caches (3.3, Slice 2); the docket artifact hashed separately (2.2,
3.3, Slice 2); channel_root expansion explicitly legacy-only (3.3); tracked project
configuration retained as evidence while user configuration stays disabled (2.2, Slice 2
Verify).

Non-blocking observation: Slice 1 now avoids depending on `setup`, but Slice 2 and section
4 still assume it exists (setup smoke, cost-mode print, configuration refusal). That
dependency is defensible, since the setup wizard is separately approved, but it should be
stated as plainly there as Slice 1 now states its own.

Requesting one more fix-report. Both remaining folds are small and exact, and neither
requires rethinking the design. When the amended body carries them, I will re-verify from
source and append my dated review section to the plan with the final verdict.

## MSG-6 | 2026-08-06T19:21:32+00:00 | from: codex | type: fix-report | thread: unattended-isolation-plan | refs: main@db38323

FIX REPORT - CODEX - ROUND 2

Amended only the body of /home/zoltan/Projects/debate/docs/plans/2026-08-06-unattended-isolated-agent-pairs.md. The DRAFT header remains unchanged, and no appended review section existed to alter.

R1 placement and environment fold: kept the seat export project-local but made the boundary explicit and enforceable under the stated operating constraints. Section 3.1 now requires the Git-discovery ceiling in the adapter environment allowlist. Section 3.3 and Slice 2 require every controller-owned seat process to receive GIT_CEILING_DIRECTORIES set to the enclosing repository root, so a child export with no local .git cannot discover the parent object store. The text now explicitly rejects both shared-object worktrees and unceilinged directories that merely lack their own .git.

R1 verification fold: Slice 2 now requires git rev-parse --show-toplevel to fail from the export root. Excluded-blob canaries must use root-anchored probes, specifically git show <ref>:<path>, git ls-tree <ref> --full-tree collab/, and git log <ref> -- :(top)collab/, so a cwd-relative empty result cannot masquerade as isolation. Fresh local reproduction confirmed the leak from /home/zoltan/Projects/debate/build and confirmed that GIT_CEILING_DIRECTORIES=/home/zoltan/Projects/debate blocks discovery there.

R2 implementation fold: Slice 3 now persists the absolute whole-case deadline in docket phase state, caps every adapter invocation at the remaining budget, and closes ERROR with close_reason=case-deadline-expired when expiry occurs before, during, or between phases. Crash and scheduler restart recovery must apply that close idempotently.

R2 verification fold: Slice 3 now includes expiry during a sealed invocation and idempotent expiry-close after controller restart, in addition to the existing timeout and write-boundary recovery cases.

R2 configuration/reporting fold: Slice 2 now schedules managed timing validation to refuse a per-turn timeout above 60 minutes or an absent/unbounded whole-case deadline, and to report both the unconstrained schedule estimate and enforced deadline bound from the shared controller timing function. Its Verify block checks the refusals and both displayed values against that function.

Setup dependency precision: Slice 2 now states, as Slice 1 already did, that setup-facing profile, smoke, and timing-report work depends on the separately approved setup-wizard plan landing first; until then the adapter config loader/profile doctor exposes the same validation without claiming an implemented setup subcommand.

## MSG-7 | 2026-08-06T19:25:15+00:00 | from: owner | type: close | thread: unattended-isolation-plan | refs: main@db38323

ABORTED CONFIGURATION — no debate verdict. This bootstrap gate was initialized with thread_cap=8, contrary to the owner's intended default of 12. It was stopped after MSG-6 before the next reviewer response. The plan now records the corrected default, and review continues only in a fresh Opus/Codex channel configured with thread_cap=12.
