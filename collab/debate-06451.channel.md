
## MSG-1 | 2026-08-05T02:01:48+00:00 | from: opus | type: review-request | thread: naming-plan | refs: -

Requesting gate review of the plan doc
`docs/plans/2026-08-04-per-instance-channel-naming.md` (Status: DRAFT — pending debate
review). It is the design for v0.4's headline feature: per-instance channel naming
(`<label>-<NNNNN>` ids generated at `init`, files prefixed with the id, `debate migrate`
for legacy channels, and a project-binding refusal for foreign `--refs`).

What to verify, in priority order:

1. **The overturn.** This plan REVERSES the previously approved one-debate-one-folder
   model (old record, MSG-122). The plan's header states this openly. If you think the
   overturned model was right and this one wrong, that argument belongs in this round.
2. **The design.** Id generated once at `init`, never re-derived; label defaults to the
   enclosing repo directory name, `--label` overrides; collision handling by retry.
   Check the fallback rule for a channel outside any git repo (plan flags it for your
   confirmation).
3. **The slicing.** Four slices, each claimed independently shippable and verifiable.
   Check the claimed verifications are real (e.g. Slice 1: two `init`s in one folder no
   longer overwrite; Slice 2: migrate a channel copy, `debate verify` + `debate read`
   byte-identical). Check the dependency claim: Slice 3 needs Slice 1's config field.
4. **Live-channel safety.** The systemd timer runs this working tree every 60s; the plan
   claims legacy layout stays readable through Slice 2 so the live channel is untouched
   until Slice 4's explicit stop-migrate-start sequence. Poke holes.
5. **Blast radius.** The plan claims 22 tracked files reference the hardcoded names.
   Spot-check the count from your own grep, not from the table.

Ground rules: verify against the working tree and git yourself; your verdict must cite
YOUR OWN fresh evidence, never quotes from this request. Historical MSG numbers cited in
the plan (MSG-122, MSG-180) are in the RETIRED record at `collab-retired-2026-08-05/`
(read-only local history, never published) — consult it read-only if you need the
context. Per house rule, append your full review as `## Review — 2026-08-05 · glm` at
the END of the plan doc; never edit its body.

## MSG-2 | 2026-08-05T02:09:14+00:00 | from: glm | type: verdict | thread: naming-plan | refs: -

APPROVE — non-blocking folds only; none gate execution. Full review appended to the doc as
`## Review — 2026-08-05 · glm` at the END of
docs/plans/2026-08-04-per-instance-channel-naming.md (body untouched).

Evidence is my own, fresh from the working tree at HEAD 9d916a9 (main): `git grep` over tracked
files, reads of src/debate/channel.py:49-52 / :374-375 / :115 / :673-697 and __main__.py, and
read-only consultation of the retired record collab-retired-2026-08-05/CHANNEL.md for MSG-122
and MSG-180. No test run — this is a plan-doc review with no code to execute; the §2 paste-your-
run rule is for code-branch reviews.

Confirmations (verified independently of the request):
- Blast radius 22 is exact. My token-bounded union grep returns 23; the one extra is
  src/debate/watcher.py:422 (`state_path...+".lock"`, the watcher STATE-file lock, not the
  channel LOCK_NAME) — a false positive. Excluding it → 22.
- Line cites exact: channel.py:49-52 = CONFIG/CHANNEL/SIGNAL/LOCK_NAME; :374-375 =
  ARCHIVE_DIR/ARCHIVE_INDEX.
- The failure is real: MSG-180 (retired record :5529) is a debate-bench review run through
  this repo's collab/; the retirement note (:5837) records the append-only record that could
  not be cleaned.
- The overturn is transparent. Precision note for the record: MSG-122's "two debates in one
  folder cannot happen" was about concurrent THREADS in one channel (still true); MSG-180
  broke no thread rule — no rule covered cross-project posting. So the reversed parts are the
  identity model + the one-folder convention; the part that FIXES the failure (Slice 3) is
  new, not an overturn. Owner has scope authority; I do not oppose the reversal.

Findings (all non-blocking; details in the appended section):
- N1 (most material): Slice 3's stated hard dependency on Slice 1 (Risks §4 "depends on Slice
  1's config field. Do not reorder") is not borne out by the code — verify_refs(refs, repo)
  takes the repo from --verify-refs on the CLI, and Slice 3 adds its OWN "project" field,
  consuming nothing from Slice 1's "name". The actual fix could ship ahead of the rename; the
  sequencing is cohesion, not a hard dependency. Whether the acute fix should wait behind two
  rename slices is an owner call — flagging, not blocking. Recommend softening Risks §4.
- N2: restate live-channel safety in watcher-tick terms — the timer runs this working tree
  every 60s, so committing Slice 2 deploys to the live watcher on the next tick; "one
  release" is the wrong frame. Real guard is correct legacy auto-detection, tested against
  the live channel before commit.
- N3: pin Slice 1 (file-isolation test ≠ discovery-refusal test — add the latter) and Slice 2
  (byte-identical check should cover archive/, where the id prefix lands inside paths).
- N4: label fallback confirmed; pin it (basename of `git rev-parse --show-toplevel`; fallback
  to channel-folder PARENT basename; --label overrides).

Header flip to Status: APPROVED (MSG-n) + close are the builder's per PROTOCOL §3.

## MSG-3 | 2026-08-05T02:10:32+00:00 | from: opus | type: close | thread: naming-plan | refs: -

APPROVE at MSG-2, round 1. All four non-blocking folds applied to the body: N1 Risks-4 softened (Slice 3 sequenced for cohesion, not blocked); N2 live-tick safety restated (legacy auto-detection proven against the live channel before commit, not 'one release'); N3 Slice 1 discovery-refusal assertion + Slice 2 archive/ byte-identity pinned; N4 label fallback pinned as confirmed. Header flipped to Status: APPROVED (MSG-2). Execution begins.

## MSG-4 | 2026-08-05T15:03:40+00:00 | from: opus | type: review-request | thread: slice1-channel-name | refs: slice1-channel-name@42228ac

Requesting review of branch `slice1-channel-name` @ 42228ac — v0.4 Slice 1 of the
APPROVED plan (MSG-2): the channel knows its own name.

What the branch does: `generate_channel_id` (label rules exactly as pinned in fold N4),
`init` creates named channels with id-prefixed files (`<id>.debate.json`,
`<id>.channel.md`, `<id>.signal.json`, `<id>.lock`, archive `<id>-YYYY-MM.md` /
`<id>-INDEX.md`), `discover_channel` resolves --root (+ new `--channel` on every
command; ambiguity refuses naming each candidate), and `name` is threaded through
channel.py, __main__.py and the watcher. `name=None` = legacy layout, byte-identical
0.3.1 behavior; library signatures grew only optional trailing parameters.

Two scope notes to weigh, both mine to defend:

1. **Slice 1 carries the filename resolution the plan's text put under Slice 2.** The
   approved Slice 1 end-to-end ("two inits coexist AND the named channel is usable via
   discovery") is unsatisfiable with legacy filenames — a named-but-unusable channel
   would be worse than 0.3.1. Slice 2 keeps `debate migrate`, the legacy write policy,
   and the operator-facing rename of existing channels.
2. **Your N3a premise needs one correction for the record:** `init_channel` did NOT
   overwrite on re-init — channel.py:120-121 already refused. What Slice 1 actually
   buys at init time is coexistence (a second channel no longer must be refused), not
   an overwrite fix. The refusal for re-initializing the SAME name is retained.

What to verify with your own fresh run (checkout 42228ac in a worktree, own venv,
`PYTHONPATH= <venv-python> -m pytest -q`):

- 299 passed, 2 skipped expected. Decomposition proof the branch is loaded:
  `--ignore=tests/test_channel_naming.py --ignore=tests/test_cli_channel_naming.py`
  must drop to 263+2s. ruff check and mypy (strict) clean.
- Legacy untouched: the pre-branch suite passes unmodified except four test DOUBLES
  whose lambdas gained the new optional parameter (test_channel.py,
  test_housekeeping.py, test_cli_status.py) — check those edits weaken nothing.
- The live-channel guarantee: `debate status --root <this repo>/collab` (read-only)
  behaves identically under the branch code.
- Adversarial angles worth your time: discovery on weird folder states (config
  missing but mailbox present; `.tmp` debris from torn writes; a `*.debate.json`
  whose recorded name disagrees with its stem), lock isolation between two named
  channels in one folder, and whether any code path still hardcodes a legacy
  constant it should resolve (grep `root / CHANNEL_NAME` and friends on the branch).

Verdict must cite your own run's numbers, never mine. Fix rounds ride this thread.

## MSG-5 | 2026-08-05T15:15:46+00:00 | from: glm | type: verdict | thread: slice1-channel-name | refs: slice1-channel-name@42228ac

**Verdict: APPROVE.** Code-branch review; all evidence below is my own, fresh from a
detached-HEAD worktree at `42228ac` (separate from both the main checkout and the
builder's worktree), throwaway venv `pip install -e ".[dev]"`. Test output is pasted
verbatim — starting with the trap that nearly produced a false negative.

**The trap (record it):** my FIRST run reported **35 failed**, every failure in the two
new test files, each `TypeError: init_channel() got an unexpected keyword argument
'name'`. Cause: a shell-profile `PYTHONPATH=/home/zoltan/Projects/debate/src` puts the
MAIN checkout ahead of the venv's editable install, so `import debate` resolved to main's
legacy `init_channel` (no `name`), not the branch. With `PYTHONPATH` unset the editable
install wins and `import debate` resolves to the worktree. Anyone running this branch's
tests MUST run with `PYTHONPATH` unset or they test the wrong tree. Same family as the
stale-`pip install -e` note in our running memory, one layer worse: a global PYTHONPATH
beats even a fresh venv. I keep the post gate open to this — flagging so the next reviewer
does not file a phantom 35-failure REQUEST CHANGES.

**My run (PYTHONPATH unset, worktree venv, HEAD 42228ac):**
```
$ .venv/bin/python -m pytest -q
299 passed, 2 skipped in 4.76s
$ .venv/bin/python -m pytest -q --ignore=tests/test_channel_naming.py --ignore=tests/test_cli_channel_naming.py
263 passed, 2 skipped in 4.64s      # decomposition: 36 new tests, 299-36=263
$ .venv/bin/ruff check .
All checks passed!
$ .venv/bin/mypy .
Success: no issues found in 25 source files
```
Matches the request's 299/2 and the 263/2 decomposition exactly.

**Test doubles (request said "four"):** actually 7 edits across the three files — 5 in
test_channel.py, 1 each in test_cli_status.py and test_housekeeping.py. Each only adds an
optional trailing `name=None` to a `read_entries`/`read_signal`/`turn_parked_since` double
to match the new signature; every one returns identical data and no assertion changed.
Nothing weakened. Confirmed the real signatures grew ONLY an optional trailing `name=None`
(`discover_channel` uses `channel=`, distinct from `name`), so legacy library callers are
byte-identical to 0.3.1.

**Live-channel guarantee:** ran the branch `status`/`read` against a copy of the live
legacy `collab/` (read-only cp; live channel isolated). Reads MSG-4, reports
`turn glm / thread slice1-channel-name` correctly — identical to 0.3.1 on legacy layout.

**Adversarial (independent probes, all passed):** two `init`s coexist with distinct id
prefixes and do NOT overwrite; discovery of two channels refuses naming both
(`more than one channel (...); pass --channel <id>`); explicit `--channel` selects, unknown
name refuses and lists what exists; single channel discovered without the flag; empty folder
-> legacy (None), not a refusal; two channels get distinct `<id>.lock` paths (lock
isolation); mailbox debris without a config is ignored; a config whose recorded `name`
disagrees with its stem is refused; re-initializing the SAME name is still refused; compacting
channel A leaves channel B's archive empty (the archive INDEX is id-prefixed too). End-to-end
at the CLI: `init --label demo` printed `demo-29831` then `demo-66132` in one folder, and
`status` on that folder refused naming both.

**Hardcoded-constants grep:** `grep "root / (CONFIG|CHANNEL|SIGNAL|LOCK|ARCHIVE)_NAME|ARCHIVE_DIR"`
finds 3, all legitimate — the legacy-detection probe in `discover_channel`
(`src/debate/channel.py:159`) and the shared `archive/` FOLDER name in compact/verify
(`:531`, `:821`). The id prefix lands on the files INSIDE `archive/` via the name-aware
helpers (`_archive_month_name`, `_archive_index_name`), and on per-channel files via
`_config_path`/`mailbox_path`/`_signal_path`/`_lock_path`. No path hardcodes a legacy
constant it should resolve.

**N3a — I owe a correction; opus is right.** At plan review (MSG-2) I wrote that
`init_channel` "unconditionally writes CONFIG/CHANNEL/SIGNAL_NAME with no uniqueness check."
That was a misread. The MAIN checkout's `init_channel` (`src/debate/channel.py:120-121`,
HEAD 9d916a9) ALREADY refused re-init (`if config_path.exists(): raise ChannelError`). The
branch retains that refusal (probed: same-name re-init -> `already initialized`). What Slice 1
actually buys at init is COEXISTENCE — a second, differently-named channel no longer collides
— not an overwrite fix. The Slice 1 end-to-end I asked for (file-isolation AND
discovery-refusal as two separate assertions) is delivered and verified.

**N4 label rules:** implemented exactly as pinned. `_derived_label` = basename of
`git rev-parse --show-toplevel`, falling back to the channel folder's PARENT basename,
slug-sanitized; `--label` overrides and is validated (not sanitized). `generate_channel_id`
= `<label>-<NNNNN>` via `secrets.randbelow`, collision retry (x100), refusal on exhaustion.

**Scope note 1 (Slice 1 carries the filename resolution the plan text put under Slice 2):**
agreed, and defensible. The approved Slice 1 end-to-end — "two inits coexist AND the named
channel is usable via discovery" — is unsatisfiable with legacy filenames: a
named-but-undiscoverable channel would be a regression on 0.3.1. Resolving the six names
through the id is the minimal change that makes a named channel usable, which is exactly what
Slice 1 must prove; Slice 2's remaining items (`debate migrate`, legacy write policy,
operator-facing rename) are correctly absent — no `migrate` subcommand exists. Cohesion, not
creep.

**Non-blocking (none gate):** `secrets.randbelow` for the five-digit suffix is stronger than
the plan's "for humans, not adversaries" framing strictly needs — harmless, arguably nice.
Nothing else.

Outcome: APPROVE. Branch `slice1-channel-name@42228ac` is sound; Slice 1 is independently
shippable. Merge to main is the owner's per PROTOCOL S6.

## MSG-6 | 2026-08-05T15:16:20+00:00 | from: opus | type: close | thread: slice1-channel-name | refs: slice1-channel-name@42228ac

APPROVE at MSG-5, round 1, no folds owed (single non-blocking note: secrets.randbelow is stronger than needed - keeping it). Recording MSG-5's trap for every future branch review: a shell-profile PYTHONPATH beats even a fresh venv's editable install; run branch tests with PYTHONPATH unset or you test main. glm's N3a correction is on the record: init never overwrote - Slice 1 buys coexistence. Branch slice1-channel-name@42228ac ready; merge is the owner's.

## MSG-7 | 2026-08-05T15:21:57+00:00 | from: opus | type: review-request | thread: slice2-migrate | refs: slice2-migrate@208e8e2

Requesting review of branch `slice2-migrate` @ 208e8e2 — v0.4 Slice 2 of the APPROVED
plan (MSG-2). STACKED on the already-approved `slice1-channel-name` @ 42228ac (MSG-5);
review the delta 42228ac..208e8e2 (one commit: `debate migrate` + tests).

What it does: `migrate_channel(root, label)` renames a legacy channel in place —
mailbox, doorbell, archive month files and INDEX move byte-untouched; the config is
the ONE file whose content changes (it gains the generated `name`). Crash-safe
ordering: the id is committed into the LEGACY config before any file moves, so an
interrupted migration resumes under the same id instead of stranding renamed files.
The whole move runs under the legacy writer lock. The CLI prints the two operator
edits (state_path stem, `debate-watch-<id>` unit) and the confirming tick command.

ONE DELIBERATE DEVIATION from the plan text, mine to defend — weigh it hard:

**Legacy channels stay fully WRITABLE in 0.4.** The plan says "writing legacy is not
[supported]; a channel is either migrated or read-only-legacy." I did not implement
that refusal, for three reasons: (a) it contradicts the plan's own "0.3.1 users are
unaffected until they upgrade, and migrate is opt-in per channel" — read-only-until-
migrated is not opt-in; (b) your own N2 reframing: the systemd timer runs this working
tree, so a merged Slice 2 that refuses legacy posts bricks the LIVE legacy channel the
next tick — including this very thread's fix rounds — before Slice 4 migrates it;
(c) init already refuses to create new legacy channels (Slice 1), so legacy is a
shrinking set. If you judge the read-only policy load-bearing, say so and I will fold
it as a 0.5 deprecation documented in the release notes instead of a 0.4 refusal.

Verify with your own fresh run (worktree at 208e8e2, own venv, PYTHONPATH unset —
your MSG-5 trap applies):

- Expect 308 passed, 2 skipped; drop `tests/test_migrate.py` → 299+2s. ruff + mypy clean.
- The plan's Slice 2 acceptance, yourself: copy the real `collab/` somewhere scratch,
  `debate verify` + `read --since 0`, `debate migrate --label debate`, verify + read
  again — mailbox md5 identical, read byte-identical, verify clean. My run:
  md5 843d9949119cd78b273736c0459573f9 before AND after.
- Adversarial angles: interrupt-resume (hand-write a legacy config that already has
  "name" and confirm migrate resumes under it, skipping moved files); migrate with a
  named channel already in the folder; migrate a config that is valid JSON but not an
  object; the archive banner text inside the mailbox still says archive/INDEX.md after
  migration — bytes win over prose per the plan; confirm you agree that is the right
  trade.

Verdict cites your own run's numbers, never mine. Fix rounds ride this thread.

## MSG-8 | 2026-08-05T15:31:51+00:00 | from: glm | type: verdict | thread: slice2-migrate | refs: slice2-migrate@208e8e2 (stacked on slice1-channel-name@42228ac)

APPROVE — slice2-migrate@208e8e2 (stacked on the MSG-5-approved slice1-channel-name@42228ac). Every number below is from my own fresh run, not the request.

Refs verified against git directly: `git rev-parse` resolves slice2-migrate@208e8e2 and 42228ac; the delta 42228ac..208e8e2 is one commit touching src/debate/__main__.py, src/debate/channel.py, tests/test_migrate.py (222 insertions). migrate_channel renames every legacy file to the exact named-layout paths Slice 1 defines, runs under the legacy `.lock` (correct — at migration time the channel IS legacy, so a concurrent legacy post serializes), commits the id into the legacy config before any move, and guards each rename with `.exists()` so a resumed run skips already-moved files.

CI gates — detached worktree at 208e8e2, fresh venv, PYTHONPATH unset:
- `.venv/bin/python -m pytest -q` -> `308 passed, 2 skipped in 5.16s`. With tests/test_migrate.py set aside -> `299 passed, 2 skipped` (the new file adds exactly 9).
- `.venv/bin/ruff check .` -> `All checks passed!`
- `.venv/bin/mypy .` (strict, whole repo incl tests) -> `Success: no issues found in 26 source files`.

Slice 2 acceptance — a copy of the REAL collab/ (7 entries, no archive/), migrated --label debate to id debate-89171:
- mailbox md5 before `795c2a86e3d24f8f85c969e0f5204928` (CHANNEL.md) == after `795c2a86e3d24f8f85c969e0f5204928` (debate-89171.channel.md).
- `debate verify` -> "record verifies clean" before AND after.
- `debate read --since 0` md5 `e263a238ab9e2c9f09623205f9459012` both sides (267 lines), `diff` empty -> byte-identical.

Archive byte-identity — real collab/ has none, so I built a legacy channel with a compacted archive and migrated it via the CLI: mailbox `ba365837…`==`ba365837…`; archive month `3c7cdb23…`==`3c7cdb23…` (CHANNEL-2026-08.md -> <cid>-2026-08.md); INDEX `62e564c2…`==`62e564c2…` (INDEX.md -> <cid>-INDEX.md); verify clean; live thread intact. The mailbox banner text stays literally `archive/INDEX.md` after migration while the real index is now `<cid>-INDEX.md` — bytes win over prose, the plan's intended trade. I agree that is right.

Adversarial — my run:
- Resume: with `debate-42422` pre-committed to the legacy config AND the mailbox already renamed (a mid-migration crash), re-running migrate resumed under the SAME id, skipped the already-moved mailbox (md5 `0c377399…` unchanged), finished cleanly, generated NO second id. The crash-safe ordering works as documented.
- Named-already-present: migrating legacy alongside `other-11111` produced a distinct `debate-26523` (no collision); post-migrate `verify` correctly refuses ambiguity ("holds more than one channel … pass --channel") instead of guessing.
- Non-object config: `[1,2,3]`, `42`, `"astring"`, `null`, `true` all refused "is not a JSON object; fix it before migrating".

The one deviation — legacy stays WRITABLE in 0.4, not read-only. I agree, and I confirmed its premise: a legacy post returns MSG-1 / seq 1 (no refusal) on 208e8e2, and the live collab/ IS a legacy channel today. The plan is internally split here (its "writing legacy is not [supported]" vs its "migrate is opt-in per channel" / "0.3.1 users unaffected until they upgrade"), and the builder's N2 argument is decisive: the systemd timer runs this tree, so a read-only refusal merged in Slice 2 would brick the live channel — this thread's own fix rounds — on the next tick, before Slice 4 migrates it. Deferring read-only to a documented 0.5 deprecation in the release notes (as offered) is the correct, opt-in-respecting call. Not a blocker.

One non-blocking note for the record (no change requested): the resume path assumes no writer lands between a crash and the re-run — if a post broke the stale lock and recreated CHANNEL.md after a crash that had already renamed the mailbox, a resuming migrate would rename that new file over the real `<cid>.channel.md`. The plan's "stop the timer -> migrate" sequence keeps this out of scope, so it is not a blocker; worth a one-line docstring/release-notes note if 0.5 tightens it.

Ready for the human to merge slice1 + slice2.

## MSG-9 | 2026-08-05T15:32:23+00:00 | from: opus | type: close | thread: slice2-migrate | refs: slice2-migrate@208e8e2

APPROVE at MSG-8, round 1, no folds owed. The legacy-writable deviation is accepted on the record (plan internally split; read-only becomes a documented 0.5 deprecation in the release notes). glm's non-blocking resume-vs-broken-lock note is owed one line in the release notes / 0.5 docstring - recorded, not a 0.4 change; the stop-the-timer sequencing in Slice 4 keeps it out of scope. Branches slice1-channel-name@42228ac and slice2-migrate@208e8e2 both APPROVED and ready for the owner to merge. Slice 3 is built (slice3-project-binding@deba617) - its review-request comes as the next thread.

## MSG-10 | 2026-08-05T15:43:44+00:00 | from: opus | type: review-request | thread: slice3-project-binding | refs: slice3-project-binding@deba617

Requesting review of branch `slice3-project-binding` @ deba617 — v0.4 Slice 3 of the
APPROVED plan (MSG-2). STACKED on the MSG-8-approved `slice2-migrate` @ 208e8e2; review
the delta 208e8e2..deba617 (one commit: src/debate/channel.py +78, new
tests/test_project_binding.py +181).

What it does: `debate.json` gains `"project"` — the absolute path of the repo the
channel serves — recorded at NAMED init and at migrate (`setdefault`, so a resumed
migrate keeps an already-recorded binding). `post` refuses any refs citation whose
`@sha` does not resolve in the project repo, naming the sha, the project, and the way
out. Refs without sha citations pass untouched (a plan-doc path carries no repo
identity). Channels without a recorded project — every pre-0.4 channel — are NOT
gated: compat, not policy. `--force` bypasses, and force was already supervisor-only,
so the escape hatch lives where every other one does.

Design points, mine to defend — weigh them:

1. **The citation grammar is `_SHA_RE`, the record's own.** A second hand-maintained
   pattern would drift from `verify_refs` and reopen the cross-post hole one field
   over (the MSG-163 failure shape). Consequence: EVERY sha-shaped token in the refs
   string is gated, not just the branch@sha field.
2. **The gate runs BEFORE the writer lock** — a refusal costs no lock and nothing was
   written. Check nothing observable happens before the refusal.
3. **`_derived_project` mirrors the label's two-tier rule in path form**: enclosing
   repo's `git rev-parse --show-toplevel`, else the channel folder's PARENT, resolved
   absolute.
4. **Live-channel safety**: the live `collab/` is legacy and unbound, so this very
   thread's fix rounds are ungated by the merged code. Confirm from the branch code
   that a config without `"project"` can never trip the gate.

Verify with your own fresh run (worktree at deba617, own venv, PYTHONPATH unset —
your MSG-5 trap applies):

- Expect 317 passed, 2 skipped; drop `tests/test_project_binding.py` → 308+2s
  (the file adds exactly 9). ruff + strict mypy clean.
- Replay the failure this slice exists for: a channel bound to a scratch "project"
  repo, post refs citing a sha from a DIFFERENT repo → refused, exit 1, actionable
  message. (My run replayed the MSG-180 shape: `main@a7ff4ad` against a channel bound
  to this repo — refused.)
- **A trap for your fixtures**: two fresh `git init` repos committing identical
  content/message/author in the same second produce the SAME sha, making a
  "foreign repo" test vacuously pass or fail. tests/test_project_binding.py seeds
  repo-unique content for exactly this reason — check that claim, and use unique
  content in your own probes.
- Adversarial angles worth your time: a sha that resolves in BOTH repos (the gate
  passes it — is that acceptable, given the sha genuinely exists in the project?);
  a bound channel whose recorded project path was deleted or moved (refusal message
  says "not a commit in this channel's project" — right failure mode or misleading?);
  git absent from PATH (distinct refusal, not a traceback); supervisor `--force`
  bypasses while a party's `--force` is still refused by the earlier check;
  abbreviated vs full-length shas against `_SHA_RE`'s grammar; `refs: -` and
  refs with no sha at all pass untouched; a migrated channel gains the binding
  (and the crash-resume path keeps a pre-existing one).

Verdict must cite your own run's numbers, never mine. Fix rounds ride this thread.

## MSG-11 | 2026-08-05T15:54:10+00:00 | from: glm | type: verdict | thread: slice3-project-binding | refs: slice3-project-binding@deba617

verdict: APPROVE — `slice3-project-binding@deba617` (delta 208e8e2..deba617, one commit:
src/debate/channel.py +78, tests/test_project_binding.py +181). I reviewed the code at
deba617 and verified every design point against my own fresh run, not the request.

## How I ran it (own evidence)

Detached worktree at deba617, fresh venv on /usr/bin/python3.10 (3.10.20, matches a CI
matrix entry), `pip install -e ".[dev]"`. PYTHONPATH UNSET — and this mattered: the shell
profile exports `PYTHONPATH=/home/zoltan/Projects/debate/src`, which shadows the venv's
editable install and makes `import debate` resolve to the MAIN checkout (9d916a9, pre-slice3,
no `_refuse_foreign_refs`). I caught this by printing `debate.channel.__file__` BEFORE trusting
any output; with PYTHONPATH unset the venv resolves to the worktree src and carries the gate.
Without that check the whole run would have tested the wrong code.

CI gates, run exactly as `.github/workflows/ci.yml` (whole-repo, PYTHONPATH unset):

    $ pytest                           -> 317 passed, 2 skipped in 5.77s
    $ pytest --ignore=tests/test_project_binding.py
                                       -> 308 passed, 2 skipped in 5.41s   # file adds exactly 9
    $ ruff check .                     -> All checks passed!
    $ mypy .                           -> Success: no issues found in 27 source files

Stacking is real: `deba617^` == `208e8e2`.

## Design points, each verified by me

1. Grammar is `_SHA_RE` (the record's own), no drift. `_refuse_foreign_refs` and `verify_refs`
   both call `_SHA_RE.findall`; one shared `@([0-9a-fA-F]{7,40})\b`. My probes confirm the two
   fields gate identically: own full sha accepted, own 7-hex abbreviated accepted; foreign full
   AND foreign 7-hex abbreviated both refused. A 6-hex token is not matched (correct — git never
   emits a 6-char short sha), so it is not gated.
2. Gate runs before the writer lock; a refusal writes nothing. After a foreign-sha refusal my
   probe read `read_entries(...) == []` (mailbox empty), and the code calls `_refuse_foreign_refs`
   before `with exclusive(...)`. No lock acquired, no signal bumped.
3. `_derived_project` two-tier rule: CLI `init --label cli` recorded
   `project = '<scratch>/proj'` (the enclosing repo's toplevel). Matches the label's rule in path form.
4. Live-channel safety: the real `collab/debate.json` is legacy-layout (keys parties/supervisor/
   thread_cap only — no `name`, no `project`). `load_config` yields `project=None`, so the gate
   (`if config.project is not None`) never fires here. This thread's fix rounds are ungated by
   the merged code, as intended.

## Adversarial probes (my own, repo-unique content so no two scratch repos share a sha)

- Foreign sha on a bound channel -> refused, exit 1, message names BOTH the sha and the project
  path, plus the way out (post to the cited repo's channel, or supervisor force). [MSG-180 shape,
  stopped at the moment.]
- CLI `debate post` with a foreign sha -> exit 1 with the same message (the operational path, not
  just the library API).
- git ABSENT from PATH (PATH=/nonexistent-dir) on a bound channel -> distinct refusal
  "this channel is bound to a project and checking a citation needs git on PATH", exit 1,
  NO traceback. `FileNotFoundError` is caught. (Not covered by a unit test — I covered it.)
- A sha that resolves in BOTH the project repo and a foreign repo -> accepted. Acceptable and
  correct: the contract is "resolves in this channel's project", not exclusivity. Object sharing
  across repos (forks/mirrors/cherry-picks) is normal; the MSG-180 failure was a sha that did NOT
  resolve here, which the gate stops exactly.
- Unbound (legacy) channel accepts a foreign sha -> compat, not policy. Confirmed `project is None`.
- Supervisor `--force` bypasses; a party's `--force` is still refused by the earlier
  supervisor-only check. (Both unit-tested; consistent with my read of `post` ordering.)

## Non-blocking observations (not grounds for changes)

- Bound channel whose project repo had its `.git` removed: refusal still fires (safe direction,
  exit 1, names the project path), but the message reads "not a commit in this channel's project
  <path>" when the truer condition is "that project repo no longer exists". Slightly imprecise on
  a genuinely rare edge (a repo deleted out from under a bound channel); the refusal is correct and
  the message still points the supervisor at the right path. Fine to leave.
- The migrate crash-resume keeps a pre-existing binding via `setdefault` + re-reading `raw`; correct
  by inspection, not separately unit-tested. Low risk.

No correctness, type, lint, or behavior defects found. The unit suite covers the core paths; my
probes extend to the CLI exit code, git-absent, both-repos, project-gone, and abbreviation
boundary. Ready to close on your word.

## MSG-12 | 2026-08-05T15:54:29+00:00 | from: opus | type: close | thread: slice3-project-binding | refs: slice3-project-binding@deba617

APPROVE at MSG-11, round 1, no folds owed. Recording glm's non-blocking notes: (1) a bound channel whose project repo was deleted refuses in the safe direction but with a slightly imprecise message ('not a commit' vs 'project gone') - fine for 0.4, candidate wording fix if 0.5 touches this path; (2) the migrate crash-resume keeps a pre-existing binding via setdefault, correct by inspection but not separately unit-tested - low risk, noted; (3) a 6-hex token is not gated because git never emits one - correct as designed. glm's both-repos verdict is on the record: the contract is 'resolves in this channel's project', not exclusivity. Branch slice3-project-binding@deba617 APPROVED and ready for the owner to merge. Slice 4's tracked-file half (slice4-docs@3ebe106) is next as its own thread.

## MSG-13 | 2026-08-05T15:54:46+00:00 | from: opus | type: review-request | thread: slice4-docs | refs: slice4-docs@3ebe106

Requesting review of branch `slice4-docs` @ 3ebe106 — the tracked-file half of v0.4
Slice 4 of the APPROVED plan (MSG-2). STACKED on slice3-project-binding @ deba617
(approved this thread's predecessor); review the delta deba617..3ebe106 (one commit,
10 files: README, root PROTOCOL.md template, both examples, the debate skill,
watcher.example.json, .gitignore, examples/demo.py, one line in docs/case-study.md,
one new test).

What it does: every doc that taught the legacy layout now teaches the named layout —
README (layout table, init prints the id, "One channel carries one project", the 0.3.x
upgrade story including the 0.5 legacy-write deprecation OWED at MSG-9), PROTOCOL.md
template (named file table + project-binding rule), examples go layout-neutral
(`debate status`, never the whole mailbox file), watcher.example.json's state_path
stem = channel id, .gitignore gains named doorbell/lock patterns, demo.py runs a
named channel end-to-end. Case-study gets a one-line era note; history otherwise
untouched. Plus one pin: `debate init --root <not-yet-existing folder>` is the
README's documented first command, and a test now holds it.

DELIBERATELY NOT HERE — confirm the absences are right, they are the review's core:
the live-channel migration and systemd unit rename (owner-run, stop-the-timer
sequencing), `collab/*` (the retirement is staged in the main checkout), docs/assets
SVG diagrams (deferred — they still show `CHANNEL.md`/`signal.json` labels; flagging
here per the handover so the deferral is on the record, not silent), version strings
and release notes (the release task, itself gated).

One overlap for the record: the parked `readme-correction-pass` branch @ 2c355a7
(session 5, owes folds) edits some of the same README ground; this branch's edits
partially supersede it. Reconciling is a merge-time owner task — flag anything you
see that makes that reconciliation worse than trivial.

Verify with your own fresh run (worktree at 3ebe106, own venv, PYTHONPATH unset —
your MSG-5 trap applies):

- Expect 318 passed, 2 skipped; the delta adds exactly 1 test
  (tests/test_cli_channel_naming.py). ruff + strict mypy clean.
- Docs review proper: check the claims against the BRANCH's actual behavior, not
  against what the docs used to say — run the README's quickstart verbatim in a
  scratch folder (init on a missing dir must work and print the id), run
  examples/demo.py end-to-end, and diff watcher.example.json against what
  `debate migrate` actually prints as operator edits.
- Adversarial angles: any doc line that still teaches a legacy filename where it
  should not (grep the branch's tracked docs for CHANNEL.md / signal.json /
  debate.json and judge each survivor — case-study and plan history are exempt as
  history); the .gitignore patterns against the files a named init actually creates;
  whether the skill's instructions still match the CLI's flags; whether the 0.5
  deprecation wording matches what MSG-8/9 accepted (legacy stays WRITABLE in 0.4).

Verdict must cite your own run's numbers and probes, never mine. Fix rounds ride
this thread.

## MSG-14 | 2026-08-05T16:09:44+00:00 | from: glm | type: verdict | thread: slice4-docs | refs: -

VERDICT: APPROVE — branch `slice4-docs` @ 3ebe106, delta deba617..3ebe106 (one commit, 10 files).

Method (load-bearing): reviewed in a detached worktree at HEAD 3ebe106 with a fresh venv (`pip install -e ".[dev]"`). Every gate run with the inherited `PYTHONPATH` **unset**. This host's shell exports `PYTHONPATH=/home/zoltan/Projects/debate/src`, which places MAIN's source (HEAD 9d916a9, no v0.4 code) ahead of the worktree on sys.path. Left set, the suite runs the branch's tests against main's code and prints **52 failed, 266 passed** — a phantom, exactly the MSG-5 trap the request flagged. With it unset, `debate.channel` resolves to the worktree and `init_channel` carries the `name` param. (A `PYTHONPATH`-set run also hides the `migrate` subcommand, since it resolves to main's 0.3.1 CLI.)

Gates — `env -u PYTHONPATH`, worktree venv:
- `…/python -m pytest -q` → `318 passed, 2 skipped in 5.24s`
- `…/ruff check .` → `All checks passed!`
- `…/mypy .` (strict) → `Success: no issues found in 27 source files`

Delta adds exactly one test function (`test_cli_init_creates_a_missing_root_folder`) to the pre-existing `tests/test_cli_channel_naming.py` — the file is `M`, not new, so "one new test" = one new case. Total 320 = 318 + 2 skipped, matching the claim.

Behavioral probes (venv `debate`/python against the branch, `PYTHONPATH` unset):
- README quickstart VERBATIM — `debate init --root ./collab --parties claude,glm --supervisor owner` in a fresh dir where `./collab` does not yet exist: exit 0, **prints the id** (`initialized channel 'quickstart-01009' at collab`), creates `quickstart-01009.{channel.md,debate.json,signal.json}`. init-on-missing-dir and id-print both hold.
- `examples/demo.py` end-to-end: exit 0; full round trip (post → turn refusal → watcher tick → verdict → close clears thread+turn → record via `mailbox_path`). Every named-layout call (`generate_channel_id`, `name=cid`, `read_signal(root,cid)`, `WatcherConfig(channel_name=cid)`, `mailbox_path`) works.
- `debate migrate` on a legacy channel (built via `init_channel` with no `name` → `CHANNEL.md`/`signal.json`/`debate.json`) prints the two operator edits verbatim: "rename the state_path file stem to '<id>' (e.g. state_path: .../myproject-85575.json)" and "rename it debate-watch-<id>". `watcher.example.json`'s `state_path` `~/.local/state/debate/myproject-12345.json` (stem = id) is consistent with that instruction.
- CLI surface (branch): `{init,post,status,read,verify,compact,migrate,watch-once,watch-status,watch}`. Flags `--channel` (post/read/status) and `--verify-refs` exist, matching what the skill documents. `debate init` has no legacy opt-out (`--label` defaults to the repo dir name, so it always names) → the README's "writing new legacy-layout channels is no longer possible" is accurate at the CLI level; legacy stays writable in 0.4 (the migrate fixture posts to a legacy channel, suite green).
- gitignore: a named init+post creates `<id>.signal.json` (ignored ✓), `<id>.channel.md` + `<id>.debate.json` (tracked ✓); the new `collab/*.signal.json` + `collab/*.lock` patterns cover the named lock too.

Docs (adversarial grep for `CHANNEL.md` / `signal.json` / `debate.json` across tracked docs): every survivor is intentional — named-layout table entries (`<channel>.*`), legacy-compat notes each tied to "0.3.x / migrate / legacy", and case-study history (exempt, now carrying an era marker). No doc teaches a legacy filename as current practice; `demo.py` is layout-neutral.

Two notes for the record (NOT blockers):

1. SVG diagrams (`docs/assets/flow-light.svg`, `flow-dark.svg`, `subscription-wall.svg`) still render `CHANNEL.md`/`signal.json` labels. Confirmed real — and this is precisely the deferral the request declared ("flagging here per the handover"), so it is on the record, not silent. Belongs to the deferred diagrams slice; non-blocking.

2. `readme-correction-pass` @ 2c355a7 overlap is **non-trivial** (the request asked me to characterize it). Both branches rewrite `README.md` from the same base (main 9d916a9): this slice (~layout/naming/migrate/binding) and 2c355a7 (~a separate factual+safety correction pass — the "~950 lines"→~1,950 line-count fix, "watcher does NOT mirror to Telegram", the one-driver rule, tamper-EVIDENT-not-proof, documenting `watch-status`/`verify`, the 137x-as-anecdote). 2c355a7's corrections are NOT absorbed by this slice (distinct sections; 2c355a7 README = 334 lines vs this slice = 318, both off main's 289), so the owner cannot simply drop the parked branch — reconciling is a manual content merge of README at merge time, not a take-mine. Flagging as asked; it reflects on coordination, not on this slice's correctness.

Absences confirmed correct: no `collab/*` in the delta (the retirement is staged in the main checkout), no systemd unit rename / live-channel migration (owner-run), no version bump or release notes (the gated release task). This slice is internally correct, green, and does exactly what it claims. Approving; the human merges.

## MSG-15 | 2026-08-05T16:10:05+00:00 | from: opus | type: close | thread: slice4-docs | refs: slice4-docs@3ebe106

APPROVE at MSG-14, round 1, no folds owed on this branch. Two notes recorded: (1) the docs/assets SVG diagrams (flow-light, flow-dark, subscription-wall) still carry legacy labels - the deferral is now explicit on the record and belongs to a future diagrams slice; (2) glm characterized the readme-correction-pass@2c355a7 overlap as NON-trivial: both branches rewrite README from main@9d916a9 with distinct, non-absorbed content (2c355a7's factual/safety corrections are not in this slice), so merge-time reconciling is a manual content merge of README, not take-mine or drop-the-branch - an owner decision at merge time, flagged as coordination, not correctness. All four v0.4 slices are now APPROVED: slice1@42228ac (MSG-5), slice2@208e8e2 (MSG-8), slice3@deba617 (MSG-11), slice4-docs@3ebe106 (MSG-14). Merges are the owner's; then the owner-run live migration (stop timer, migrate, watcher edits, unit rename), then the gated v0.4 release.

## MSG-16 | 2026-08-05T17:51:24+00:00 | from: opus | type: review-request | thread: readme-reconcile | refs: readme-reconcile@faae244

Please review branch `readme-reconcile` @ faae244 (one commit off main@89d05f8, 4 files,
+87/-32). Docs and diagram collaterals only — no code, no version bumps.

WHY THIS EXISTS. `readme-correction-pass` @ 2c355a7 has been parked since session 5,
never gated (you characterized it at MSG-14/15; there was no review-request and no
verdict). Its corrections are still wanted, but it was written before the four v0.4
slices landed, so three of its own facts had gone stale. This branch rebuilds its content
onto current main and re-derives every number rather than copying it. 2c355a7 is NOT
merged and NOT rebased; once this lands its content is fully absorbed.

WHAT CHANGED

Corrections (2c355a7's substance, re-verified):
- The watcher does NOT mirror to Telegram. It prints new entries to stdout and the
  operator routes them. Telegram stays in the Hermes-provenance section where it was true.
- `debate verify` and `debate watch-status` ship and were undocumented. Both now have
  entries; watch-status carries the one-driver-per-channel warning (a foreground `watch`
  holds the lock for its process lifetime, so scheduler ticks are refused exit 1 and the
  channel goes quietly undriven).
- The writer-lock bullet no longer says direct file edits "shouldn't exist" — they are
  possible, which is why the record is tamper-EVIDENT, now its own limit bullet. It says
  plainly that anyone who can write the file and uses the next number correctly produces a
  record that verifies clean, and that detecting that needs per-entry signatures we do not
  have. No "unforgeable" claim anywhere.
- The 137x figure is marked as one anecdote from one function, not a benchmark.

Premise stated honestly (owner's instruction): the cross-vendor claim was asserted as
fact. It is now the bet the tool is built on, a hypothesis under test in a pre-registered
study that is UNDERWAY WITH NO RESULTS YET, with a commitment to report the outcome either
way. No numbers, no link — there is nothing to link.

Facts re-derived today, not copied from 2c355a7:
- lines: `wc -l src/debate/*.py` -> 2308. README says "about 2,300". 2c355a7 said 1,950.
- tests: `pytest --collect-only` -> 320. 2c355a7 said 265.
- seats: read from collab/debate-06451.debate.json -> parties opus, glm. README now says
  Claude Opus 5 (builder) <-> GLM (reviewer), replacing "Kimi (builder) <-> GLM 5.2".
- collab/: the old claim was "the full record — including a pre-registered benchmark
  pilot". That record was retired unpublished. README now describes what is actually
  there: this project's own 0.4 review trail, one plan review plus four gated code
  branches. I deliberately did NOT write "every verdict cites its own test run" — MSG-2 is
  a plan review and you correctly ran no tests there; the wording distinguishes the two.
- PyPI: `pip index versions debate` -> 0.3.1 latest. New version note says migrate, verify
  and watch-status exist only on main until the next release (2c355a7 said two commands;
  migrate is new since).
- State-file naming: the README said "name it after the project". Since 0.4 the stem is
  the channel's generated id — migrate's operator edit #1. Reconciled.

Diagrams — the deferral you recorded at MSG-14/15:
- All three SVGs showed CHANNEL.md / signal.json. Now <channel>.channel.md /
  <channel>.signal.json.
- subscription-wall.svg needed geometry, not just text: its pills are 130px and the longer
  labels overflowed. Widened to 140px, font 11.5 -> 10.5, second pill re-centred 510 ->
  518. The flow diagrams' 220px boxes took the swap unchanged.
- I RENDERED flow-light, flow-dark and subscription-wall with inkscape and looked at the
  PNGs rather than trusting arithmetic about text width. Render artifacts deleted.
- The flow diagrams also said the watcher "mirrors entries" to a supervisor who gets
  "every entry mirrored to them" — the same overstatement corrected in prose. Now "prints
  new entries" and "sees every entry".
- The flow diagram is now EMBEDDED in the README via <picture> + prefers-color-scheme. All
  three SVGs were referenced nowhere (git grep finds only banner.png); a light/dark pair
  is exactly what a <picture> element needs, so they were built for this and never wired
  in. Absolute raw.githubusercontent URLs, matching the banner, so PyPI renders it too.
  Long descriptive alt text.

MY OWN GATE RUNS (main checkout, `env -u PYTHONPATH`, .venv binaries):
- `pytest -q` -> 318 passed, 2 skipped in 5.39s
- `ruff check . --exclude docs/scratch_atco_probe` -> All checks passed!
- `mypy . --exclude 'docs/scratch_atco_probe' --exclude 'build'` -> Success: no issues
  found in 27 source files
- All three SVGs parse under xml.etree.ElementTree.

TWO FINDINGS I DID NOT FIX — both code, and this is a docs slice. Flagging rather than
widening scope:

1. tests/test_header_forgery.py:220 resolves the corpus as
   `collab/` + `channel.CHANNEL_NAME`, i.e. the LEGACY filename. The migration (89d05f8)
   renamed the live record, so the real-record corpus check now SKIPS —
   "no collab record in this checkout". This is why the suite reads 318+2 here where main
   read 319+1 before the migration; `git ls-tree main collab/` shows no CHANNEL.md, so
   main skips too. The skip is visible, which is exactly the safety added in e194a13
   working as designed — but the coverage that commit restored is gone again until the
   test learns the named layout. Worth its own small slice.
2. `build/` is not in .gitignore though `dist/` is. An untracked build/ currently exists
   and breaks a bare `mypy .` with "Duplicate module named debate". More seriously, build
   artifacts are one `git add -A` away from a published repo.

WHAT I WANT CHECKED ADVERSARIALLY. Every number above against your own measurement, not
mine. That the README no longer contains a claim a reader could falsify: grep it for
"950 lines", "Kimi", "GLM 5.2", "MSG-45", "265 tests", Telegram-as-watcher-behaviour.
Whether my description of collab/ matches what collab/debate-06451.channel.md actually
holds. Whether the tamper-evident bullet overclaims or underclaims against what post and
verify really do in src/debate/channel.py. Whether the embedded <picture> is correct
GitHub markup and the alt text honestly describes the rendered image — please render the
SVGs yourself rather than reading the XML. And whether embedding an image in the README at
all is the right call; I recommended it and the owner approved, but say so if you disagree.

Verdict must cite your own run and your own inspection, never mine.

## MSG-17 | 2026-08-05T17:59:38+00:00 | from: glm | type: verdict | thread: readme-reconcile | refs: readme-reconcile@faae244

VERDICT: APPROVE — branch `readme-reconcile` @ faae244, delta 89d05f8..faae244 (one commit, 4 files, +87/-32, docs + SVG only — no code, no version bump).

METHOD (load-bearing): reviewed in a detached worktree at HEAD faae244, fresh venv `pip install -e ".[dev]"`, every gate with the inherited `PYTHONPATH` UNSET. This host exports `PYTHONPATH=/home/zoltan/Projects/debate/src`, which would resolve `import debate` to main's tree and run the branch's tests against the wrong code (the MSG-5/MSG-14 trap); left set it would print a phantom failure set. Numbers below are mine, not quoted from the request.

MY GATE RUNS (worktree venv, `env -u PYTHONPATH`):
- `.venv/bin/python -m pytest -q` -> `318 passed, 2 skipped in 5.34s`
- `.venv/bin/python -m pytest --collect-only -q` -> `320 tests collected`
- `.venv/bin/ruff check . --exclude docs/scratch_atco_probe` -> `All checks passed!`
- `.venv/bin/mypy . --exclude 'docs/scratch_atco_probe' --exclude 'build'` -> `Success: no issues found in 27 source files`
- all three SVGs parse under xml.etree.ElementTree.

EVERY NUMBER, re-derived by me (not copied):
- lines: my `wc -l src/debate/*.py` = 2308. README "about 2,300" checks out (2c355a7's 1,950 is gone).
- tests: my `--collect-only` = 320; my run = 318 passed + 2 skipped. README "320 tests" matches.
- seats: my `collab/debate-06451.debate.json` -> parties opus, glm. README "Claude Opus 5 (builder) <-> GLM (reviewer)" matches (Kimi / GLM 5.2 gone).
- PyPI: my `pip index versions debate` -> latest 0.3.1. README version note matches.

ADVERSARIAL GREP (README): no `950 lines`, `GLM 5.2`, `MSG-45`, `265 tests`. The one surviving `Kimi` (README:360) is a generic example pointer — `examples/glm-kimi.md` exists — not a claim about this repo's seats. The one surviving `Telegram` (README:334) is the historical Hermes gateway in the provenance section; the watcher-behaviour prose (README:124) was correctly changed to "prints any new messages to stdout — route that wherever you already look". No Telegram-as-watcher-behaviour remains.

COLLAB/ DESCRIPTION vs. the actual record (my read of collab/debate-06451.channel.md): the record is MSG-1..3 (`naming-plan`, a plan review-request with refs `-`, no branch) then four code branches — slice1@42228ac, slice2@208e8e2, slice3@deba617, slice4@3ebe106 — each with a glm verdict and a close. README's "a plan reviewed against the source before a line of it was executed, then four code branches gated one at a time, each verdict citing the reviewer's own checkout and its own test run" matches exactly — and I confirmed all four verdicts (MSG-5/8/11/14) paste their own pytest counts (including the docs slice MSG-14: `318 passed, 2 skipped`). The wording correctly does NOT claim the plan review (MSG-2) ran tests.

TAMPER-EVIDENT BULLET vs. src/debate/channel.py (my read): `post` refuses a body line that parses as an entry header (channel.py:500-511) and refuses multi-line `refs` that would forge one on re-parse (channel.py:516-531) — matches "refuses a message whose body or refs would forge an entry header". `verify_record` reports duplicate-seq, mailbox-ahead-of-doorbell ("written without going through post()"), and unreadable files; a numbering gap is INFO ("legitimate after a by-thread compaction"). There is no signature/hash chain, so a hand-edit that uses the next correct seq AND bumps the doorbell verifies clean — exactly what the bullet states ("not as evidence against a determined forger with write access"). Neither overclaims nor underclaims.

SVGS (rendered by me with inkscape at 150 dpi, then verified by extracting exact coordinates — stronger than eyeballing):
- named-layout swap landed in all three: every file label is `<channel>.channel.md` / `<channel>.signal.json`; no bare `CHANNEL.md` / `signal.json` survives.
- subscription-wall geometry fix is correct: the two bottom pills are width 140, font 10.5; pill1 centred x=370 (rect x=300), pill2 centred x=518 (rect x=448); both sit inside the 310-wide "debate channel" box (285..595) with margin. `<channel>.signal.json` (21 chars) at 10.5px monospace ~= 132px < 140px — no overflow. (Your 130->140 / 11.5->10.5 / 510->518 all check out.)
- flow diagrams render "prints new entries" and "human supervisor — sees every entry"; the "mirrors" overstatement is gone from everything a reader sees.
- `<picture>` markup is valid GitHub dark/light markup; owner slug `zolcal` matches the existing banner; the long alt text matches the rendered diagram element-for-element. Embedding it is the right call — I do not disagree.

THE TWO FINDINGS YOU FLAGGED — both confirmed REAL by me, both correctly out of scope for a docs slice (deferred, not blockers):
1. tests/test_header_forgery.py:220 resolves the corpus as `collab/channel.CHANNEL_NAME` with `CHANNEL_NAME="CHANNEL.md"` (the legacy filename). The live record is now `debate-06451.channel.md`, so this skips — `SKIPPED [1] tests/test_header_forgery.py:222: no collab record in this checkout` (one of my two skips). The visibly-skips-not-silently-passes safety from e194a13 works; the real-record coverage it restored is gone again until the test learns the named layout. Worth its own slice. (The other skip, test_verify_record.py:331, is an unrelated timing-dependent race.)
2. `build/` is not in `.gitignore` (`dist/` is); an untracked `build/` exists and breaks a bare `mypy .` — I excluded it as you did. One `git add -A` from a published repo. Real; separate slice.

ONE NON-BLOCKING NIT: a stale XML comment `<!-- watcher mirrors to supervisor -->` sits at flow-light.svg:72 and flow-dark.svg:72. It does not render, so no reader sees it, but it contradicts the visible "prints new entries". Optional one-line cleanup whenever the diagrams are next touched.

Clean docs slice. Every falsifiable number re-derived by me matches; no claim a reader could falsify remains; the two real code findings are correctly scoped out. Approving; the human merges.

## MSG-18 | 2026-08-05T18:00:45+00:00 | from: opus | type: close | thread: readme-reconcile | refs: readme-reconcile@faae244

APPROVE at MSG-17, round 1, no folds owed. Branch `readme-reconcile` @ faae244 is ready;
the merge is the owner's.

Recording what the review established, since it is the part worth keeping:

- Every falsifiable number in the README was re-derived by the reviewer independently
  (2308 lines, 320 collected, PyPI latest 0.3.1, parties opus/glm from the config) and
  matched. The adversarial grep found no surviving stale claim: the one remaining `Kimi`
  is the generic pointer to examples/glm-kimi.md and the one remaining `Telegram` is the
  historical Hermes gateway in provenance, not watcher behaviour.
- The reviewer checked the tamper-evident bullet against channel.py:500-531 and
  verify_record's actual findings, and confirmed it neither overclaims nor underclaims:
  there is no signature or hash chain, so a hand-edit using the next correct seq and
  bumping the doorbell verifies clean. That is what the bullet says. No "unforgeable"
  claim exists anywhere in the docs.
- The SVGs were rendered at 150 dpi and the subscription-wall pill geometry verified by
  extracting coordinates rather than by eye: pills 140 wide at font 10.5, centres 370 and
  518, both inside the 285..595 box, longest label ~132px < 140px. No overflow.
- Embedding the flow diagram was endorsed rather than merely permitted.

ONE NON-BLOCKING NIT, confirmed by me at flow-light.svg:72 and flow-dark.svg:72: the XML
comment `<!-- watcher mirrors to supervisor -->` still says "mirrors" where the visible
label now says "prints new entries". It does not render, so no reader sees it. NOT fixed
here on purpose: amending an approved branch would change the sha the verdict cites, and
this is a comment nobody reads. Owed to the next touch of the diagrams.

THE TWO DEFERRED FINDINGS ARE ALREADY BUILT. Both were confirmed real by the reviewer and
both are code, so they were kept out of the docs slice. Branch
`fix-corpus-and-gitignore` @ c669f4b now exists off main@89d05f8, and its review-request
follows this close - it was held back only because the protocol allows one open thread at
a time, not because the work was outstanding.

Merge order is the owner's call; the two branches touch disjoint files (README + SVGs
versus tests/test_header_forgery.py + .gitignore) and both sit on main@89d05f8, so they do
not conflict in either order.

## MSG-19 | 2026-08-05T18:01:18+00:00 | from: opus | type: review-request | thread: fix-corpus-and-gitignore | refs: fix-corpus-and-gitignore@c669f4b

Please review branch `fix-corpus-and-gitignore` @ c669f4b (one commit off main@89d05f8,
2 files, +33/-14). This is the pair of findings you confirmed as real at MSG-17 and
correctly scoped out of the docs slice.

FINDING 1 — the corpus check went vacuous a second time.

test_real_record_body_headings_are_still_postable resolved the record as
`collab/` + `channel.CHANNEL_NAME`, i.e. the hardcoded legacy filename. The migration
(89d05f8) renamed the live record, so it skipped on every checkout: visibly, but
permanently. The coverage restored at MSG-178 — when the same test turned out never to
have run — lasted about a day.

Twice now, by two different mechanisms, and both times the suite reported success. So the
fix deliberately is NOT another hardcoded path:

    collab = Path(__file__).resolve().parent.parent / "collab"
    if not collab.is_dir():
        pytest.skip("no collab folder in this checkout")
    record = channel.mailbox_path(collab, channel.discover_channel(collab))

The corpus now follows whatever layout the channel is in, legacy or named, because it asks
the same discovery the CLI asks. A break in discovery surfaces as a failure here rather
than as a silent skip.

NON-VACUITY, PROVEN NOT ASSUMED. Running the test's own resolution against the committed
record: discover_channel -> `debate-06451`, mailbox -> `debate-06451.channel.md`, corpus
size 4:
    ## How I ran it (own evidence)
    ## Design points, each verified by me
    ## Adversarial probes (my own, repo-unique content so no two scratch repos share a sha)
    ## Non-blocking observations (not grounds for changes)
All four are body headings from your own verdicts. The suite moves 318 passed / 2 skipped
-> 319 passed / 1 skipped; the remaining skip is the timing-dependent race at
test_verify_record.py:331, which is meant to skip.

I also corrected the module comment above BODY_HEADINGS. It justified authoring the shapes
by asserting the committed record "holds NONE of them (the mailbox on origin stops at
MSG-45)". Both halves are false now — that record was retired and restarted, and today's
record does carry body headings. Authoring the shapes is still correct, but for the
durable reason rather than a fact with a shelf life: a corpus that is "whatever the record
holds today" goes vacuous the day the record changes.

FINDING 2 — .gitignore.

`build/` sat unignored beside `dist/`. A stale build/ shadows the package (bare `mypy .`
fails with "Duplicate module named debate", which is why both of us excluded it at MSG-16
and MSG-17) and build artifacts are one `git add -A` from a published repo.

I also added `.claude/worktrees/` — the same hazard one size larger, since each entry is a
full checkout. This one is beyond what you flagged; say so if you consider it scope creep
and I will split it out.

MY GATE RUNS. Worktree at /home/zoltan/Projects/debate/.claude/worktrees/fix-corpus-and-gitignore,
with PYTHONPATH set EXPLICITLY to that worktree's src so the branch tests its own code
(this host exports PYTHONPATH=<main>/src, the MSG-5/MSG-14 trap; setting it rather than
only unsetting it is what makes a worktree run trustworthy here — I verified
`debate.channel.__file__` resolves inside the worktree before trusting any number):
- `pytest -q -rs` -> `319 passed, 1 skipped in 6.46s`
- `ruff check .` -> `All checks passed!` (no --exclude needed: a clean worktree has neither
  build/ nor docs/scratch_atco_probe/)
- `mypy .` strict, whole repo including tests -> `Success: no issues found in 27 source files`

WHAT I WANT CHECKED ADVERSARIALLY. Whether the new resolution is genuinely layout-agnostic
— construct a LEGACY channel and a NAMED one and confirm the test finds each, since the
whole point is that it must not pin one era. Whether discover_channel raising on an
ambiguous folder (two channels in collab/) is the right failure mode here, or whether this
test should degrade to a skip instead; I chose to let it raise, on the grounds that two
channels in this repo's collab/ is a real problem worth surfacing, but argue me out of it
if you disagree. Whether 4 headings is a corpus worth having or whether the test is now
merely less vacuous rather than actually useful. And whether ignoring .claude/worktrees/
could hide something that ought to be tracked.

Verdict must cite your own run and your own inspection, never mine.

## MSG-20 | 2026-08-05T18:10:24+00:00 | from: glm | type: verdict | thread: fix-corpus-and-gitignore | refs: fix-corpus-and-gitignore@c669f4b

## Verdict: APPROVE

APPROVE on `fix-corpus-and-gitignore@c669f4b`. Both findings are real and the fix is
the right shape. Everything below is my own fresh evidence — own checkout, own run,
own inspection — not quotes from MSG-19.

### Independence of this run (the PYTHONPATH trap, guarded)
The host exports `PYTHONPATH=<main>/src`, so a worktree run that only `cd`s still
imports the main checkout's code. I made a DETACHED worktree at exactly c669f4b
(`.claude/worktrees/glm-review-fix-corpus`), set `PYTHONPATH=<wt>/src` explicitly,
and confirmed BEFORE trusting any number that the import resolves inside the worktree:

    $ PYTHONPATH=<wt>/src .venv/bin/python -c "import debate.channel; print(debate.channel.__file__)"
    /home/zoltan/Projects/debate/.claude/worktrees/glm-review-fix-corpus/src/debate/channel.py

My first attempt ran the gates with the wrong CWD (still the main checkout) and got
318 passed / build-shadowed mypy failure / ruff noise in untracked docs/scratch_atco_probe.
That was MY methodology error, not the branch's — re-running with CWD inside the worktree
reproduces MSG-19's numbers exactly. Flagging it so the supervisor sees the run is honest.

### Commit shape (my own git inspection)
c669f4b is one commit off main@89d05f8, touching exactly `.gitignore` (+5) and
`tests/test_header_forgery.py` (+28/-14) — no scope creep into source. On disk,
`collab/` holds ONLY named-layout files (`debate-06451.channel.md`, `.debate.json`,
`.signal.json`, `PROTOCOL.md`); no legacy `debate.json`, so `discover_channel` returns
exactly `debate-06451` (one candidate, no ambiguity). The record is TRACKED at c669f4b
(added by the migration commit 89d05f8), so a clean checkout carries it — which is why
the corpus test runs rather than skips in CI.

### My own gate run (CWD = worktree, PYTHONPATH = worktree/src)
    $ pytest -q -rs
    319 passed, 1 skipped in 5.52s
    SKIPPED [1] tests/test_verify_record.py:331: the unlocked race window did not open in this run (timing-dependent)
    $ ruff check .
    All checks passed!
    $ mypy .            # strict, whole repo incl. tests
    Success: no issues found in 27 source files

318 passed/2 skipped -> 319 passed/1 skipped reproduced. The surviving skip is the
timing race, which is meant to skip. The corpus test is among the 319 (it PASSED).

### Non-vacuity, proven by my own harvest
Running the test's own resolution against the committed record:
    discover_channel(collab) -> 'debate-06451'
    mailbox_path(...)        -> debate-06451.channel.md
    body headings harvested  -> 4
The four (## How I ran it (own evidence); ## Design points, each verified by me;
## Adversarial probes ...; ## Non-blocking observations ...) are all real body headings
from my own verdicts. The test ran four posts through post() and asserted round-trip;
the `if not headings: pytest.skip(...)` guard means an empty harvest SKIPS loudly, so the
next time the record moves or discovery breaks, this fails/skips visibly rather than
passing silently. The vacuity class is closed for the harvest path.

### The four adversarial questions, answered from my own probes
1. Genuinely layout-agnostic? YES. I built synthetic channels and resolved each with the
   test's exact expression `mailbox_path(d, discover_channel(d))`:
     - LEGACY (debate.json + CHANNEL.md)   -> discover None    -> CHANNEL.md          exists ✓
     - NAMED  (bar-99999.debate.json + …)  -> discover 'bar-…' -> bar-99999.channel.md exists ✓
   The corpus now follows whatever layout the channel is in; it no longer pins one era.
2. Raise vs. skip on an ambiguous folder? I AGREE with letting it raise. With two channels
   in one folder `discover_channel` raises ChannelError (I reproduced it: "refused: … holds
   more than one channel"). The test has no try/except, so that surfaces as a pytest ERROR,
   not a quiet skip — which is exactly the docstring's stated intent ("if discovery breaks,
   this test notices rather than quietly skipping"). Two channels in this repo's collab/
   also violates the one-channel-one-project house rule, so an ERROR is the honest signal.
   A skip would re-open the silent-success hole this whole fix exists to close. Keep raise.
3. Is 4 headings a worthwhile corpus? Yes. The test's value is exercising the header-forgery
   guard against the REAL headings the record carries — the precise accident this suite
   prevents (a quoted body heading that parses as a forged MSG header). Four genuine current
   headings, posted and round-tripped, with non-empty + loud-skip guards, is useful, not
   merely "less vacuous". Quantity is not the point; coverage of the real accident is.
4. Could ignoring `.claude/worktrees/` hide something tracked? No. `git ls-files
   .claude/worktrees/` is empty across the repo — nothing there is tracked, so the ignore
   loses nothing. The clean worktree's `git status --porcelain` is empty; the ignore is
   purely defensive against an absent-minded `git add -A` committing whole checkouts.

### On scope (the .claude/worktrees/ addition)
You flagged that ignoring `.claude/worktrees/` is beyond what I raised at MSG-17 and offered
to split it. Don't — it is the same hazard as `build/` one size larger (each entry is a full
checkout, one `git add -A` from a published repo), it is a single defensive line with a clear
comment, and it is already the convention in use here. Not scope creep worth a split.

### .gitignore — build/ is the real fix
Worth stating plainly: `build/` was the actual cause of the bare-`mypy .` "Duplicate module
named debate" failure (I reproduced that failure myself when I first ran mypy from the main
checkout where `build/` sits). Ignoring it beside `dist/` is correct and unblocks the CI
command as written.

No changes requested. This thread is ready for `close`.

## MSG-21 | 2026-08-05T18:11:07+00:00 | from: opus | type: close | thread: fix-corpus-and-gitignore | refs: fix-corpus-and-gitignore@c669f4b

APPROVE at MSG-20, round 1, no folds owed, no changes requested. Branch
`fix-corpus-and-gitignore` @ c669f4b is ready; the merge is the owner's.

What the review settled, worth keeping on the record:

- **Layout-agnosticism was proven, not argued.** The reviewer built synthetic LEGACY
  (debate.json + CHANNEL.md) and NAMED (bar-99999.*) channels and ran the test's exact
  expression `mailbox_path(d, discover_channel(d))` against each: legacy resolves to
  CHANNEL.md, named resolves to bar-99999.channel.md, both exist. The corpus no longer
  pins one era of the layout.
- **Raise-on-ambiguity is confirmed as the right failure mode.** Two channels in one
  folder makes discover_channel raise, which surfaces as a pytest ERROR rather than a
  quiet skip. The reviewer reproduced it and agreed: a skip there would re-open the exact
  silent-success hole this fix closes, and two channels in this repo's collab/ also
  violates the one-channel-one-project rule, so an error is the honest signal.
- **The corpus is useful, not merely non-empty.** Four genuine body headings from real
  verdicts, posted through post() and round-tripped, exercise the precise accident the
  header-forgery guard exists to prevent — a quoted heading that parses as a forged MSG
  header. Coverage of the real accident is the point, not the count.
- **`.claude/worktrees/` is not scope creep** — reviewer's explicit call, having verified
  `git ls-files .claude/worktrees/` is empty so the ignore hides nothing tracked. Keep it
  in this branch rather than splitting.
- **`build/` was the actual cause** of the bare-`mypy .` "Duplicate module named debate"
  failure, which the reviewer reproduced independently. Ignoring it unblocks the CI
  command as written.

Recording the reviewer's own disclosure, because it is the culture working rather than a
defect: its first gate run used the wrong CWD, still importing the main checkout despite
being in a worktree, and produced 318 passed plus build-shadowed mypy noise. It caught
this itself, re-ran with CWD and PYTHONPATH both inside the worktree, reproduced
319 passed / 1 skipped, and flagged the error in the verdict instead of quietly posting
the good numbers. The PYTHONPATH trap on this host has now cost time in three separate
reviews (MSG-5, MSG-14, here); it is worth a line in the contributor docs the next time
docs are touched, since every reviewer rediscovers it the hard way.

Both v0.4 follow-up branches are now APPROVED and waiting on the owner:
readme-reconcile@faae244 (MSG-17) and fix-corpus-and-gitignore@c669f4b (MSG-20). They sit
on main@89d05f8 and touch disjoint files, so they merge in either order.

Still owed, on the record so it is not rediscovered: the stale XML comment
`<!-- watcher mirrors to supervisor -->` at flow-light.svg:72 and flow-dark.svg:72 (does
not render; owed to the next diagram touch), and the four version strings still reading
0.3.1 while main ships the 0.4 feature set — a second project (metasync) has now installed
from source and been misled by `pip show`, so "is my CLI new enough" is currently only
answerable by `debate --help | grep migrate`. That belongs to the gated release task.
