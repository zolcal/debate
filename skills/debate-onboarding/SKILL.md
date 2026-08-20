---
name: debate-onboarding
description: Use when the Debate session-start notice offers setup, when the user says "set up Debate", or when the user asks to start a debate ("start a debate", "debate this") in a project with the Debate plugin installed. Guides seat approval and starts brokered debates through the bundled engine; the user never types registry or environment commands.
compatibility: Ships inside the Debate plugin; uses the bundled engine via the launcher path the session-start hook injects (no pip install, no PATH dependency)
---

# debate-onboarding — set up seats and start debates from inside the host UI

## The engine

The session-start hook injects `launcher: <absolute path to scripts/debate-plugin>`
into your context. EVERY engine command below runs through that launcher, never a
PATH-installed `debate`. If the launcher path is missing, run
`<plugin-root>/scripts/debate-plugin onboarding status --project <cwd> --json`
by resolving the plugin root yourself; if that fails, tell the user the plugin
install is broken and stop.

Core rules, non-negotiable:

- **Detection is evidence, not approval.** Nothing found on PATH, in an old
  registry, or in a previous project's remembered pair is ever approved silently.
- **Zero model calls** during discovery and approval. Smoke is opt-in, costed,
  defaults to "not now".
- `--confirmed` may be passed to `approve` ONLY after the user answered the
  approval question in the CURRENT turn. Never pre-answer it.
- Internal commands are implementation detail: describe outcomes to the user in
  plain language; show commands only if they ask for details.
- **Plain words, always.** User-facing text never says "managed version 1/2",
  "{prompt}", "{input_path}/{result_path}", or "operator-owned pins". Say
  instead: an *agent* is an AI tool installed on this machine (claude, codex,
  kimi, ...); a *wrapper* is a small script of the user's that launches one
  with fixed settings; a *bridge* is a small adapter a seat needs before it
  can take part in a fully managed debate. Define a term the first time you
  use it. The technical names live behind a "details" answer.

## Flow 1 — "set up Debate" (approval)

1. Ask the user's consent if they have not just given it ("set up Debate" IS
   consent). Then run: `<launcher> onboarding inspect --project <ABS-CWD> --json`.
2. Present the candidates as a concise table: seat id, vendor/model identity, how
   the model selection is pinned (the command), present or missing, smoke state
   AND cost mode (the `cost_mode` field: subscription quota, metered API, local
   compute, or unknown -- report "unknown" as undeclared, never guess a value),
   and source (`catalog` = discovered, `derived`, `manual` = operator-authored,
   plus "existing registry entry" where labelled). Label existing state visibly
   as existing state -- it is candidate input only. After the table, in plain
   language and roughly this order:
   (a) one sentence on where the list comes from: "I found these by scanning
   this machine for AI tools I recognize";
   (b) one sentence of glossary if you will use the words: what an agent and
   a wrapper are (see the plain-words rule);
   (c) ONLY IF some listed seats cannot join managed debates yet, one
   low-key sentence such as: "These seats can act as reviewers right away;
   for a fully managed debate each one first needs a small adapter (a
   'bridge') -- nothing to decide now, I'll offer to set that up when you
   start your first debate." Never lead with legacy/version terminology;
   a new user does not care which channel version anything is;
   (d) the invitation: "Personal launcher scripts can't be detected
   automatically -- is there an AI tool or script of yours that should be on
   this list but isn't? Name it and I'll add it."
3. That invitation IS the ask-once step. When the user names an agent, the
   LEGWORK IS YOURS -- the user never composes a command template or fills
   in a form. LOCATE-THEN-CONFIRM:
   (a) Locate the named tool yourself: PATH lookups (`command -v`) of names
   that plausibly match what the user said (the tool's own name and
   `<vendor>*agent`-style wrapper names), run the located CLI's own
   `--help`, and read a located executable IF it is a plain script. The
   round-8 bans stand verbatim and outrank everything here: NEVER read or
   search credential or auth material (auth.json, tokens, keyrings,
   `.secrets`, session stores), and NEVER sweep configuration directories
   to infer a model pin (a config sweep on 2026-08-20 printed a live OAuth
   token into a transcript; that class of action is banned).
   (b) Present ONE concrete proposal per named agent -- the seat id and the
   exact command you propose to record, with anything inferred labelled as
   your inference -- and ask only for what you genuinely could not
   determine (usually who pays: "who pays when this runs -- a subscription,
   a metered API, or your own machine?"). The user confirms or corrects in
   a word. Write NOTHING yet.
   (c) Only when nothing locatable matches do you ask the user where the
   tool lives -- one plain question, never a format specification, never a
   placeholder syntax.
   (d) "No model calls" means no AI spend -- it does NOT automatically mean
   no network: a metadata subcommand (a `<tool> models` listing, a version
   check) may contact the vendor's service. Prefer offline checks; when a
   command does phone home, say so in one honest clause ("the tool checked
   its service; no AI was called").
   Tell them plainly, BEFORE they decide, what the seat will be able to do
   -- in user words, not placeholders: "as it stands this can act as a
   reviewer, but it can't join a fully managed debate until it gets a
   bridge adapter; I can help with that when you start one." (Engine fact
   for YOU, never for the user's ears: a {prompt}-style command is
   v1-watcher-only, and the brokered open refuses any seat without both
   {input_path} and {result_path}.)
4. Ask which seats to approve for THIS project, listing the user-named
   wrappers from step 3 as pending rows labelled "will be registered on
   approval". Prefer the host's structured question tool (multi-select); fall
   back to a numbered in-terminal question. Zero selections: report that
   onboarding stays incomplete, write nothing.
5. Only after the user's answer: FIRST register any SELECTED pending wrappers
   -- disclosing that this writes the machine registry and is undone with
   `seats remove <SEAT>` --
   `<launcher> seats add <vendor>/<submodel> --command "<their argv>"
   --cost-mode <their answer or unknown>`
   (an unselected pending wrapper is never registered at all), then re-run
   inspect for the fresh candidate revision, then run:
   `<launcher> onboarding approve --project <ABS-CWD> --candidate-revision <rev>
   --allow <SEAT> [--allow <SEAT> ...] --confirmed --json`
   A "candidate set changed" refusal means the machine changed under you:
   re-run inspect and re-ask.
6. If the user declares a seat's cost mode ("claude is on my subscription"),
   record it: `<launcher> seats set-cost-mode <SEAT> <subscription|api|local>`.
   Report the resulting state in plain language. THEN offer smoke, default "not
   now": exactly one model call per selected seat; state each seat's RECORDED
   `cost_mode` before the user decides ("unknown" means the operator never
   declared it -- say exactly that and treat the spend as potentially metered;
   never invent a cost claim). The offer is a NUMBERED CHOICE, mirroring the
   approval table -- list the approved seats with their cost, then exactly
   one syntax line: "Reply with numbers to smoke-test (e.g. `1 3 8`), `all`
   (<N> calls), or `skip` -- skipping costs nothing; a broken seat would then
   only surface at first real use." The numeric reply in the current turn IS
   the spend authorization for exactly those seats; echo the total back
   ("that's 3 calls -- running now") before starting. Then
   `<launcher> seats smoke <SEAT> --yes` -- ONE AT A TIME, sequentially,
   never in parallel (each is a spend the user authorized individually, and
   sequential runs keep the spend narrative auditable).

## Flow 2 — "start a debate"

1. Run `<launcher> onboarding status --project <ABS-CWD> --json`. If `attention`
   is not `ready`, run Flow 1 first (or the repair it names).
2. Show only currently present, project-approved seats. The user picks EXACTLY
   two. A remembered pair may be shown only as a labelled convenience default,
   never preselected on first onboarding.
3. Ask for or derive the debate subject and the review target, summarize what
   will be created in user words -- "your two chosen seats will independently
   review it, argue if they disagree, and every word lands in a permanent
   record; you are the supervisor, and I never vote" -- and get the user's
   confirmation. If the two picks are clearly different capability classes
   (a lightweight fast model against a frontier reasoning model), say so
   plainly before confirming: mismatched seats often produce one-sided
   verdicts and cost an extra deliberation lap. (Engine fact for YOU, never
   for the user's ears: what gets created is a managed-version-2 brokered
   channel.)
4. Run EXACTLY this form (agent-only engine fact: `--brokered` is NOT
   optional -- the plain form mints a legacy version-1 channel and is never
   the product path):
   `<launcher> open --brokered --root <ABS collab dir> --label <slug>
   --pair <a>,<b> --author-vendor <your host's catalog vendor: "claude" in
   Claude Code, "codex" in Codex> --docket-file <project-relative review input>
   [--docket-file ...]` (the docket files are what the seats actually read --
   always pass the review target; --author-vendor makes the recorded author
   relationship a declared fact: a seat sharing your host's vendor is recorded
   author-affiliated). Identity guards are enforced by the engine: the same seat
   twice and identical commands are refused outright; the same vendor/model at
   two efforts needs `--allow-identical-seats` -- ask the user explicitly before
   passing it, and only with a dedicated warning.
5. Open the docket with the `broker-open` hint the engine prints (the request
   body states what to verify), then drive it with the printed `watch
   --until-close` command. Set the expectation once -- "this takes a few
   minutes of model thinking; I'll report when it closes" -- then BE QUIET:
   no polling narration, no handover edits mid-debate, one report at the
   typed close. A status showing a seat invocation in flight within its
   budget is healthy, not stuck.
6. Report the channel id and live status in plain language; keep the raw
   commands behind a "details" answer.

## What this skill never does

Never writes a registry or profile ahead of the user's approval answer (the
one carve-out: a wrapper the user NAMED and then SELECTED is registered as a
manual seat right before approve, disclosed, undoable via `seats remove`);
never invokes a seat model during setup; never edits channel files by hand;
never merges or publishes anything; never seats this interactive session as
a debater.
