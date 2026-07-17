# Anti-encapsulation — make a non-duopoly pairing first-class before the v0.3.0 tag

**Date:** 2026-07-16 · **Owner/executor:** Claude (Fable 5), session 64ea3310 (executor seat taken 2026-07-17 on owner's go) · **Status:** r2 — both appended reviews folded in; cwd blocker fixed upstream (v0.3.1, `2591b2c` on main); BOTH seats live-smoked on this machine (GLM: `SEAT-OK glm-4.6` via env-repointed `claude -p`; Kimi: `SEAT-OK Kimi Code` via `kimi -p`)
**Motivation:** The owner's stated priority is *not to be encapsulated into the two top US models* (Anthropic + OpenAI). The `debate` tool is already vendor-neutral at the code layer (verified: `src/debate/` has zero HTTP/API/vendor coupling; the only model contact is `watcher.py:185 subprocess.run(config.command_for(party))`, a configurable argv). v0.3 is code-complete on `main` (`35513c3`, version `0.3.0` in all four places) but **not yet tagged**. The encapsulation that remains is in three *narrative/distribution* surfaces, not the code. This plan closes them while the tag is still unpushed, so the released `v0.3.0` ships a non-duopoly-co-equal posture instead of canonizing the current Claude+GPT origin story.

## What v0.3 already settled (no work needed here — context only)

Two safety footguns that previously gated *unattended* non-duopoly runs are now fixed on `main`, which is why this plan can proceed without further tool changes:

- `be70fbb` — opener allowlist: `verdict`/`fix-report` can no longer open a thread (`OPENER_TYPES = ("review-request","question","info","close")`). Closes the closed-thread-reopen footgun a careless reviewer model could trip.
- `7945f4a` — `stdin=subprocess.DEVNULL`. Closes the inherited-stdin 3-hour hang a locally-launched agent seat could hit.

v0.3 did **not** touch the README origin story, `examples/`, or the skill-distribution reputation metric — those are this plan's entire scope.

## Goals

Ship, before the `v0.3.0` tag, a state where: a stranger reading the repo sees a non-duopoly pairing as a first-class, documented path (not a Claude+GPT project that happens to be model-agnostic under the hood); and the project's own reputation metric no longer optimizes for duopoly-storefront adoption as its primary signal.

## Non-goals

- **No code changes to `src/debate/`.** v0.3 is done; this plan is docs + config only.
- **No standing up a local-model seat in this tag.** That is the deepest sovereignty move but needs a model + harness decision and real infra; it is Slice C, deferred to a follow-up.
- **No changes to `PROTOCOL.md`, `CHANNEL.md` format, or the skill body (`skills/debate/SKILL.md`).** The skill body is model-neutral already and carries its own scenario-test contract.
- **No rewriting of the Claude/Hermes origin.** It is true provenance and load-bearing; it is *de-canonized*, not deleted.

## Decision locked for this plan

**Pairing canonized in Slice A: GLM (builder) ↔ Kimi (reviewer).** Rationale: zero new infra, unblocks the tag immediately, matches the live conversation that motivated this work, and GLM already appears in the README quickstart. The local-open-weight anchor is Slice C, staged separately. *(Open to challenge in review — see Open questions.)*

---

## Slice A — a first-class non-duopoly example + README de-canonization

End-to-end, independently shippable: a reader who wants a non-US-model pairing can follow one file from `init` to a working cron, and the README presents that path as equal to the Claude origin.

### A1. Create `examples/glm-kimi.md`

**File:** create `examples/glm-kimi.md`, mirroring the structure of `examples/claude-code.md`. Exact content to write:

````markdown
# Wiring a non-duopoly pairing: GLM + Kimi

Two seats, neither Anthropic nor OpenAI: GLM (Zhipu) as the builder, Kimi (Moonshot) as
the reviewer — coordinating through the same two-file mailbox as any other pairing. The
tool is vendor-neutral; only the `commands` and `prompts` in the watcher change.

## 0. The GLM seat: a wrapper, and why

GLM has no standalone CLI; z.ai's documented path is occupying an Anthropic-compatible
harness — Claude Code — via environment repointing. The IDE integrations on z.ai's docs
(VS Code, Kilo, Droid, …) are irrelevant here: the watcher needs exactly one thing, a
headless one-shot CLI, and `claude -p` under the GLM endpoint is that. Create
`~/.local/bin/glm-agent` (secret-free repo; key sourced at runtime):

```bash
#!/bin/bash
# GLM seat for debate: claude -p repointed at z.ai's Anthropic-compatible endpoint.
set -euo pipefail
. ~/.secrets   # provides GLM_API_KEY - never inline it in watcher.json
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="$GLM_API_KEY"
export ANTHROPIC_MODEL="glm-4.6"   # override any locally pinned model
exec claude -p "$1" </dev/null
```

**Fail-closed identity check (run once at setup, and after any `claude` upgrade):**

```bash
glm-agent "Reply with exactly: SEAT-OK <your model name>"
# must print SEAT-OK glm-...  - anything else means you are NOT on GLM: stop.
```

A GLM-native harness, if one ships, is a drop-in: replace the wrapper, keep the prompt.

## 1. The channel lives in your repo

```bash
debate init --root collab --parties glm,kimi --supervisor owner
# commit collab/debate.json and your filled-in PROTOCOL.md; gitignore collab/signal.json
```

## 2. The watcher (fallback + mirror)

`watcher.json` — GLM through the wrapper above, Kimi through its own CLI. `kimi -p` runs
one prompt non-interactively; note its prompt mode auto-approves tool calls (it cannot be
combined with `--yolo`/`--auto` and needs neither) — the pinned prompt and your repo
boundary are the safety controls, same as any unattended seat:

```json
{
  "state_path": "~/.local/state/debate/my-project.json",
  "commands": {
    "glm":  ["glm-agent", "{prompt}"],
    "kimi": ["kimi", "-p", "{prompt}"]
  },
  "prompts": {
    "glm":  "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab` — never the whole CHANNEL.md. Verify signal.json still shows an open thread AND turn=='glm' — if not, exit. Constraints: feature-branch commits only; no merges or pushes to main; verify any claim about repo state against git directly, never from channel history; if the working tree is dirty, restrict yourself to read-only verification and posting — build in a separate git worktree. Post via `debate post`, then stop.",
    "kimi": "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab`. Do what the latest entry asks. For verdicts, cite YOUR OWN fresh evidence: current HEAD and a fresh test run. Post via `debate post`, then stop."
  },
  "debounce_seconds": { "glm": 600 },
  "retry_seconds": 1800
}
```

> Agents inherit the watcher's working directory (debate >= 0.3.1), so the relative paths
> above resolve against your project root — that is why the cron below `cd`s first. A
> systemd unit or Task Scheduler job needs `WorkingDirectory` / "Start in" set the same
> way. A hung agent is bounded by `timeout_seconds` (default 1800), not by stdin tricks.

## 3. Run it

```bash
*/3 * * * *  cd /path/to/your-project && debate watch-once --root collab --config watcher.json
```

Route the tick's stdout wherever you already look.

## 4. The same lessons apply

Every clause in those prompts was paid for in production with a different pairing — they
are model-neutral. Verify repo state against git, not channel history; build in a worktree
on a dirty tree; one reply, then stop. Full incident provenance in `examples/claude-code.md`.

## Notes

- Builder/reviewer roles are arbitrary; flip them by swapping which party you drive live.
- A Mistral seat, a Qwen Code seat, or a local open-weight model behind any headless CLI
  slots in the same way: one argv, one pinned prompt.
- CLI surfaces drift. Re-run the identity check and a one-line `kimi -p "Reply OK"` after
  upgrading either tool.
````

### A2. De-canonize the README origin story

**File:** modify `README.md`. The quickstart already uses `claude,glm` (line 82) and the
sample exchange shows `from: glm` (line 59) — so the encapsulation is isolated to the
"Where this comes from" section (now at line 233 after v0.3 inserted the "Running to
completion" subsection above it). Two surgical edits, no rewrite of the provenance body:

- **Edit the section's closing paragraph** (lines 259–261). The `old_string` for the Edit
  tool is the live text, byte-exact including the OpenClaw link:
  > The same shape fits whatever pair of ecosystems you already run — Claude Code on one side;
  > Hermes, [OpenClaw](https://github.com/openclaw/openclaw), or your homegrown harness on the
  > other. If it can read files and run a shell command, it can hold up its end of a review.

  Replace with:
  > The same shape fits whatever pair of ecosystems you already run. The origin above is one
  > example, not the design: a GLM + Kimi pairing works the same way (see
  > [`examples/glm-kimi.md`](examples/glm-kimi.md) — both seats verified live), and a local
  > open-weight model can hold either seat, beholden to no vendor. If it can read files and
  > run a shell command, it can hold up its end of a review.

- **Prepend one framing sentence** to the section's opening (line 235, immediately before
  "This is not a design exercise — it's the generalization of a channel that ran…"):
  > This is the setup `debate` was extracted from — provenance, not prescription.

Keep the rest of the section (Fable 5 / GPT-5.5 / Hermes detail) verbatim.

### A3. Done conditions (Slice A)

- [ ] `examples/glm-kimi.md` exists and its `watcher.json` block parses as valid JSON
      (`python3 -c "import json,sys; json.loads(sys.stdin.read())"` against the fenced block).
- [ ] The `debate init --parties glm,kimi` command in the example is runnable against the
      installed CLI (or, if the CLI is not on PATH locally, matches the exact `init` flag
      shape documented in the README quickstart).
- [ ] The two README edits land verbatim as specified; `grep -n "examples/glm-kimi.md" README.md`
      returns the new link.
- [ ] No other README prose is changed (diff is exactly the two edits above).
- [ ] Render check: the new README paragraph reads coherently in place (no orphaned reference
      to a section that moved).
- [ ] **One real watcher-driven round** with the exact published config shapes (scratch
      channel, glm+kimi parties, `watch-once` invoking at least one seat end-to-end: read →
      act → `debate post`), plus the fail-closed identity check output recorded. JSON parsing
      alone proves nothing about cwd, provider, permission, or exit behavior (codex, MSG-23).

---

## Slice B — re-denominate the reputation metric (plan-doc edit)

The one line of the project's own plan that optimizes for duopoly-storefront adoption.
`docs/plans/2026-07-15-skill-distribution-research.md` is currently **uncommitted** and
already carries an appended Codex review — the natural moment to correct the framing.

**File:** modify `docs/plans/2026-07-15-skill-distribution-research.md`. Insert immediately
*above* the slice-6 metrics table (currently ~line 109, the line beginning "The table below,
committed to git…"):

> **Anti-encapsulation re-denomination (2026-07-17):** for a tool whose value is
> cross-vendor neutrality, the go decision is measured in vendor-neutral signals.
> **Primary signals (drive the go):** GitHub referral stars, PyPI download lift, completed
> externally-evidenced review rounds. **Secondary evidence (reported, never decisive):**
> marketplace installs and author-profile clicks — they measure duopoly-storefront reach,
> not adoption of the idea.
> **Operative rule (supersedes the line below the table):** Go = any two of the three
> PRIMARY thresholds met at day 90. Marketplace installs cannot substitute for a primary.

The table's rows and thresholds stay; only the go rule is superseded, explicitly, above it.
The appended review stays untouched.

### Done conditions (Slice B)

- [ ] The note is inserted above the table only; the table rows, the `Go = any two of the
      four` line, and the `## Review — 2026-07-15 · codex` section are unchanged.
- [ ] `grep -n "Anti-encapsulation re-denomination" docs/plans/2026-07-15-skill-distribution-research.md`
      returns exactly one match, located above the metrics table.

---

## Slice C — the local-model anchor (DEFERRED from this tag; staged here)

The deepest sovereignty move: one seat on a local open-weight model on the owner's GPUs
(3090 Ti 24GB + 5060 Ti 16GB), so that seat can never be encapsulated by any vendor. **Not
in the v0.3.0 tag.** Recorded so it is not lost.

- [ ] Pick weights that fit 24 GB at a usable quantization (Qwen-Coder-32B / DeepSeek-Coder /
      Codestral class; exact current SOTA verified at implementation time — the line moves
      fast). Default diversity rationale: pair the local seat with a *different ecosystem's*
      cloud model (e.g. local-Qwen ↔ Kimi, or local ↔ GLM), never two sizes of one family.
- [ ] Pick a harness that exposes a non-interactive, single-reply CLI invocation (an open
      agent runner over a local llama.cpp/sglang server, or equivalent).
- [ ] Add the local-seat `commands` variant to `examples/glm-kimi.md` as a documented
      alternative (or a sibling `examples/local-seat.md`), with the model/harness left as a
      setup choice — the `commands[]` *shape* is model-agnostic and can be written now.
- [ ] Run one real attended review round on the local pairing before documenting it as
      supported. Only then promote it in the README alongside the GLM/Kimi path.
- [ ] Ship as `v0.3.1` (docs-only bump) or fold into the next feature release.

---

## Release finish (after A + B; owner's call)

- [ ] With A and B merged to `main` and the implementation review APPROVEd, require green CI
      at the exact merged commit, then tag **`v0.3.1`** (code is 0.3.1 four-way since the cwd
      fix; v0.3.0 was never tagged). The `tag==version` release gate verifies it.
- [ ] Run or explicitly waive the plugin-install smoke (HANDOVER-SESSION-1.md) before tag.
- [ ] `docs/plans/2026-07-15-skill-distribution-research.md` SHIPS with Slice B applied.
      `collab/` and the handover STAY LOCAL for this tag per the debate outcome (MSG-24) —
      final call remains the owner's.

Housekeeping (separate from the release gate, destructive — owner runs when convenient):
re-run `pip install -e /home/zoltan/Projects/debate` (the active editable install points at
the reliability worktree), then prune stale worktrees
(`debate-reliability-v0.3`, `debate-cwd-v0.3.1`, the detached `/tmp/.../pre-task2-wt`).

---

## Review & implementation flow (the debate mechanism)

This document is the executor body; reviews append below. Implementation proceeds via the
debate channel, dogfooding the tool on itself (the pattern used by the reliability-v0.3 and
skill-distribution plans):

1. **Review round (this plan):** post a `review-request` on `collab/` citing this file —
   `debate post --root collab --from claude --type review-request --thread anti-encapsulation
   --refs anti-encapsulation-plan@<sha> --body "..."` — and let the reviewer (codex) append
   `## Review — YYYY-MM-DD · codex`. Fold any `REQUEST CHANGES` into r2 before implementing.
2. **Implementation:** in a dedicated worktree
   (`git -C /home/zoltan/Projects/debate worktree add ../debate-anti-encap -b anti-encapsulation main`),
   not the dirty shared checkout. Stage **explicit paths only** (never `git add -A`) — the
   shared tree carries a live channel and uncommitted docs.
3. **Implementation re-review:** post a `review-request` citing the implementation
   `branch@sha`; the reviewer verifies the diff against this plan's done conditions. Merge on
   APPROVE. (For a docs-only change, a lighter read-through verdict may suffice — reviewer's
   call.)
4. **Tag** only after merge.

## Compatibility notes

- No runtime behavior change from A+B. The tag is now `v0.3.1` (the cwd fix bumped code to
  0.3.1 on main, 2026-07-17; v0.3.0 was never tagged).
- `examples/glm-kimi.md` pins both seat invocations as verified on 2026-07-17 against
  installed tools (kimi 0.20.x: `-p` headless, auto-approving, no `--yolo`/`--auto` combo;
  claude 2.1.212 + z.ai endpoint: identity check answered `SEAT-OK glm-4.6`). The example
  keeps a re-verify-after-upgrade note as drift insurance.

## Out-of-scope follow-ups (tracked, not in this plan)

- A `debate doctor`-style "is my chosen party command non-interactive and exiting?" check —
  would mechanize the `kimi-cli`/local-seat verification that Slice A/C currently leave to
  the human. Already noted as out-of-scope in the v0.3 spec.
- Cross-vendor skill manifests (Codex/Gemini) — slice 2 of the distribution plan; orthogonal
  to anti-encapsulation but complementary.

## Open questions (for the reviewer / owner)

1. **Pairing choice.** GLM↔Kimi is canonized here for friction-reasons, but both are
   Chinese-ecosystem cloud models — which is *less* diverse and *less* sovereign than a
   local seat. Is GLM↔Kimi the right headline, or should Slice C (local seat) be promoted
   and GLM↔Kimi demoted to a secondary example? (Owner's sovereignty priority argues for the
   former being prominent; release-timing argues for GLM↔Kimi now.)
2. **Mistral.** If there is a European-sovereignty angle to "not the two US models", Mistral
   (open-weight, EU) is the non-US-non-China option and can also be the local seat. Worth a
   third example, or out of scope for this tag?
3. **Committing the channel.** Should `collab/` (the review transcript) ship in `v0.3.0` as
   provenance, or stay local? Affects whether this plan's own review round becomes part of
   the release record.

## Implementation evidence (2026-07-17, executor)

Slices A+B implemented on branch `anti-encapsulation` (worktree `/home/zoltan/Projects/debate-anti-encap`):

- A3 identity check (GLM seat): `env ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
  ANTHROPIC_AUTH_TOKEN=$GLM_API_KEY ANTHROPIC_MODEL=glm-4.6 claude -p "Reply with exactly:
  SEAT-OK <your model name>"` → `SEAT-OK glm-4.6` (claude 2.1.212).
- A3 headless check (Kimi seat): `kimi -p "Reply with exactly: SEAT-OK <model>"` →
  `SEAT-OK Kimi Code` (kimi 0.20.x).
- A3 real watcher-driven round — BOTH seats, full thread lifecycle (r2 fix round,
  2026-07-17): scratch project, `debate init --parties glm,kimi`; tick 1
  (`["kimi","-p","{prompt}"]`) woke the real Kimi CLI → `MSG-2 kimi verdict: APPROVE
  SEAT-SMOKE kimi`; tick 2 woke the GLM seat through the EXACT `glm-agent` wrapper script
  (chmod +x, resolved via PATH, secrets sourced inside) → `MSG-3 glm close`, thread closed,
  both watcher ticks exit 0, run from the project root with relative `--root collab` (cwd
  inheritance exercised). Fail-closed identity check ran through the same wrapper:
  `glm-agent "Reply with exactly: SEAT-OK <model>" | grep -q "SEAT-OK glm-"` → PASS
  (refuses with exit 1 on mismatch).
- A3 JSON validity: the example's fenced `watcher.json` parses (`json.loads`).
- B: operative-rule note applied above the metrics table in
  `docs/plans/2026-07-15-skill-distribution-research.md`; table and appended review untouched;
  the doc ships with the branch (resolves the on-main-vs-local contradiction).

## Review — (pending)

Reviews append below this line; the body above is edited only by the executor.

## Review — 2026-07-16 · claude (session 64ea3310, reviewer seat)

**Verdict: REQUEST CHANGES — direction right, scope right, but the headline example has two
correctness gaps that would make a stranger's first non-duopoly run fail or silently not be
non-duopoly at all.** Verified against `main@35513c3` and the machine this repo lives on.

**Confirmed accurate:** code-layer neutrality claim (only model contact is the configurable
argv at `watcher.py` subprocess.run); commits `be70fbb`/`7945f4a` and their described effects
are on main; A2's `old_string` is byte-exact at README:259–261; quickstart is `claude,glm` at
README:82; the "Where this comes from" section starts at README:233; the stale-worktree list
matches `git worktree list` (incl. the detached `/tmp/.../pre-task2-wt`).

**Blocking corrections:**
1. **The Kimi argv is wrong, and it need not be deferred.** `kimi` is installed HERE (Node CLI,
   v-something via nvm): headless is `kimi -p/--prompt <prompt>` ("run one prompt
   non-interactively and print the response"), and an agent that must execute `debate post`
   non-interactively will also need its approval mode set (`-y/--yolo` or `--auto`). A1's
   `"kimi": ["kimi", "{prompt}"]` treats the prompt as a positional command and will not run
   headless. Pin `["kimi", "-p", "{prompt}"]` (+ approval flag, verified once locally) now;
   keep the setup-time note only as drift insurance.
2. **The GLM seat, as written, is Anthropic wearing a GLM name tag.** `"glm": ["claude", "-p",
   "{prompt}"]` runs whatever backend the local `claude` is configured for — by default,
   Anthropic. The "Notes on the GLM seat" hints at this but the config block does not do it.
   The example must make the backend explicit or the flagship anti-encapsulation example
   defaults to the duopoly: either an env-wrapped argv
   (`["env", "ANTHROPIC_BASE_URL=<glm-endpoint>", "ANTHROPIC_AUTH_TOKEN=...", "claude", "-p",
   "{prompt}"]`-shape, secrets sourced not inlined) or a stated prerequisite line ("your
   `claude` must be pointed at a GLM backend; verify with …") plus a one-line verification
   command. Without one of these, done-condition A3 passes while the goal fails.

**Non-blocking:**
3. Slice B anchor: the quoted line sits nearer ~105 than ~109 in the current file — matching
   on the quoted string (as specified) is robust; the number is cosmetic.
4. The flow's suggested refs `anti-encapsulation-plan@<sha>` cannot resolve while this doc is
   uncommitted — use `main@35513c3` with an "uncommitted working-tree file" note (the
   convention used by both prior plan reviews), or commit the doc first.
5. Open question 1: recommend keeping GLM↔Kimi as the headline for this tag (release timing)
   — but A2's replacement text already name-drops the local seat; that is the right level of
   Slice-C promotion for now. Open question 2 (Mistral): out of scope for this tag; one
   sentence in `examples/glm-kimi.md`'s notes ("a Mistral or local open-weight seat slots in
   the same way") would cover the gap at zero cost. Open question 3: recommend shipping
   `collab/` in the tag (gitignoring `signal.json`) — it is the strongest provenance artifact
   the project has.
6. Slice C's "pair the local seat with a different ecosystem's cloud model" rationale is good
   and worth one sentence in the README edit too, eventually — not this tag.

## Review — 2026-07-16 · codex

**Verdict: REQUEST CHANGES — the anti-encapsulation direction is worth shipping before the
tag, but the proposed flagship example is not runnable as written, Slice B does not make its
stated metric change operative, and the release finish has unresolved contradictions.**

### Evidence checked

I reviewed the full plan and the appended Claude review against `main@35513c3`, the recent
commit history through `c046bbf`, `7945f4a`, `be70fbb`, `109cd92`, and `35513c3`, and the live
working tree. I checked [README.md](/home/zoltan/Projects/debate/README.md:1),
[examples/claude-code.md](/home/zoltan/Projects/debate/examples/claude-code.md:1), the current
[skill-distribution plan](/home/zoltan/Projects/debate/docs/plans/2026-07-15-skill-distribution-research.md:1),
[watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:44), the release workflow and
version-lock test, and [HANDOVER-SESSION-1.md](/home/zoltan/Projects/debate/docs/HANDOVER-SESSION-1.md:1).
I also ran the installed `kimi` 0.20.1 and Claude Code 2.1.211 help/auth/config checks and
read-only CLI parser/path probes. No test suite was run because this is a plan review and the
task forbids writes other than this append.

### Independent ruling on the Claude findings

1. **AGREE that the Kimi argv is blocking; DISAGREE that an approval flag should be added.**
   The installed help defines `-p, --prompt <prompt>` as the one-prompt non-interactive mode,
   and `kimi noop` exits `unknown command 'noop'`; therefore `["kimi", "{prompt}"]` is wrong.
   But both suggested fixes in the Claude review are invalid on the installed version:
   `kimi --prompt noop --yolo` exits `Cannot combine --prompt with --yolo`, and the equivalent
   `--auto` command exits `Cannot combine --prompt with --auto`. Prompt mode itself creates or
   forces an `auto`-permission session and installs a headless approval handler. Pin exactly
   `["kimi", "-p", "{prompt}"]` (plus an optional explicit model), and document that prompt
   mode auto-approves tool calls, making the fixed prompt and workspace boundary the safety
   controls. Do not tell readers to add `-y` or `--auto`.

2. **AGREE with the GLM-backend diagnosis, with a narrower remediation.** Bare `claude -p`
   could drive GLM on a host already repointed to a compatible endpoint, but this example
   neither establishes nor verifies that prerequisite. On this machine `claude auth status`
   reports `claude.ai` / `firstParty` / `max`, the user configuration pins
   `claude-fable-5[1m]`, neither user nor project settings supplies backend environment keys,
   and the process has no `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, or
   `ANTHROPIC_API_KEY`. The configured `GLM_API_KEY` is not consumed by bare Claude Code.
   Moreover, the watcher performs literal argv replacement and `subprocess.run(...,
   shell=False)` with the inherited environment
   ([watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:74),
   [watcher.py](/home/zoltan/Projects/debate/src/debate/watcher.py:283)); `$GLM_API_KEY` in JSON
   would not expand. Use a dedicated wrapper/settings profile or watcher-service environment
   that sources the credential outside `watcher.json`, sets the GLM endpoint and a supported
   model mapping, and overrides the inherited Fable selection. Add a fail-closed setup check
   plus one attended identity smoke before calling the seat GLM-backed. Never inline the key
   in the example.

### Additional blocking corrections

3. **The example inherits a watcher working-directory bug that neither prior review finding
   catches.** The child starts with `cwd=config.channel_root`, so the documented cron command
   with `--root collab` launches both agents *inside* `/home/zoltan/Projects/debate/collab`.
   From there A1's `PROTOCOL.md`, `./collab`, and `debate read --root collab` resolve to the
   wrong places; there is no `collab/PROTOCOL.md`. I reproduced the consequence read-only:
   from the channel directory, `debate read --root collab` prints `no open thread`, while
   `debate read --root .` returns MSG-22. Either launch through a wrapper that restores the
   project root, or explicitly configure/add the parent workspace and rewrite the prompts to
   use `../PROTOCOL.md`, channel root `.`, and repo root `..`. A3 must include one real
   watcher-driven round with the exact published config; JSON parsing and `init --help` cannot
   catch cwd, provider, permission, or exit behavior. Also narrow line 78's claim: DEVNULL
   does not prove an interactive child cannot hang; `timeout_seconds` is the actual bound.

4. **Slice B does not currently re-denominate anything.** The source table has one
   thresholded marketplace-install row, not "two marketplace-install rows"
   ([skill-distribution plan](/home/zoltan/Projects/debate/docs/plans/2026-07-15-skill-distribution-research.md:104)).
   Its existing `Go = any two of the four` rule already makes marketplace installs alone
   insufficient. Adding a contradictory interpretive note while requiring the table and its
   operative rule to remain unchanged is not a measurable policy change. The direction is
   reasonable if the project distinguishes **cross-vendor adoption** from **storefront
   reputation reach**: keep marketplace installs/profile clicks as secondary reach evidence,
   but count GitHub referral stars, PyPI lift, and completed externally evidenced review
   rounds as the vendor-neutral primary signals. If marketplace data truly must not drive the
   go decision, rewrite the operative rule explicitly (for example, require two of those
   three primary thresholds); otherwise drop the claim that this slice changes the decision.

5. **A2's edit anchors are accurate, but its new claims are not yet accurate.** The opening
   anchor and old closing paragraph match [README.md](/home/zoltan/Projects/debate/README.md:233)
   through line 261, and the relative example link is correct. Change "GLM and Kimi pair just
   as well" to a claim supported by the completed watcher smoke. Change "a local open-weight
   model can hold either seat with no vendor in the path at all": one local seat paired with
   a cloud seat still has a vendor in the path. Say that a local model removes the hosted-model
   dependency from *that seat*, or reserve "no vendor ... at all" for two local seats. Also
   describe the headline as two non-US **model backends**, because one proposed harness is
   still Anthropic's Claude Code application.

6. **The pre-tag checklist is incomplete and internally inconsistent.** It requires A+B on
   `main` and then separately allows the untracked Slice-B target document not to ship. Decide
   which is true: commit that document with B, or remove B from the tag gate. The current
   handover also leaves the Claude plugin marketplace/install/invoke smoke unresolved
   ([HANDOVER-SESSION-1.md](/home/zoltan/Projects/debate/docs/HANDOVER-SESSION-1.md:18),
   [HANDOVER-SESSION-1.md](/home/zoltan/Projects/debate/docs/HANDOVER-SESSION-1.md:50)); run it
   before the tag or record an explicit waiver. Require green CI at the exact implementation
   commit and the GLM/Kimi watcher smoke before tagging. Version mechanics themselves are
   sound: all four locations are `0.3.0`, the lockstep test and tag/package gate exist, and
   `git tag --list` shows no `v0.3.0` yet. Worktree pruning is separate destructive
   housekeeping, not a release gate.

### Open questions

1. **Keep GLM↔Kimi as the v0.3 headline only after the exact end-to-end smoke.** It is a
   useful cloud-vendor-diversity example and can ship now; it is not sovereignty. Keep the
   local seat prominent as the next evidence-backed slice, but do not promote an unchosen,
   untested model/harness over the runnable example.
2. **Mistral is out of scope for v0.3.** Evaluate it as a Slice-C candidate using then-current
   model, license, fit, and harness evidence. I DISAGREE with adding an untested Mistral
   name-drop to A1 merely because it costs one sentence; that creates a third unsupported path.
3. **Do not ship raw `collab/` in v0.3; I DISAGREE with the Claude recommendation here.** The
   current 44 KB operational mailbox contains local absolute paths, the current review is
   still open, and `collab/signal.json` is not presently ignored. It is useful internal
   dogfooding evidence, not yet a self-contained public provenance artifact. After all reviews
   close, publish a curated/redacted, immutable transcript with a claim-to-source map as the
   distribution plan already requires; keep the live mailbox local for this tag. If the owner
   nevertheless chooses raw inclusion, add and verify the exact `signal.json` ignore before
   staging explicit paths.

**Approval conditions:** correct the Kimi command without forbidden permission flags; make
the GLM routing and identity check explicit without embedding secrets; repair the watcher cwd
contract and prove the exact example in a real round; make Slice B's rule operative and
internally accurate; tighten A2's claims; and resolve the pre-tag artifact/smoke decisions.
