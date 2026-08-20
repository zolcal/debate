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

## Flow 1 — "set up Debate" (approval)

1. Ask the user's consent if they have not just given it ("set up Debate" IS
   consent). Then run: `<launcher> onboarding inspect --project <ABS-CWD> --json`.
2. Present the candidates as a concise table: seat id, vendor/model identity, how
   the model selection is pinned (the command), present or missing, smoke state
   AND cost mode (the `cost_mode` field: subscription quota, metered API, local
   compute, or unknown -- report "unknown" as undeclared, never guess a value),
   and source (`catalog` = discovered, `derived`, `manual` = operator-authored,
   plus "existing registry entry" where labelled). Label existing state visibly
   as existing state -- it is candidate input only. End the table with this
   footer, verbatim in spirit: "Wrappers with operator-owned pins are not
   auto-detected -- name any agent that is missing and I will register it."
3. Before asking for approval, ask ONCE: "Any other agents or wrappers I
   should know about that are not listed?" If the user names one, COLLECT its
   command and cost mode from the user -- write NOTHING yet. Both are the
   user's; never invent either. Tell them plainly which kind they are
   declaring: a `{prompt}` wrapper works on legacy version-1 channels only,
   while a debate-capable seat must be a bridge accepting BOTH `{input_path}`
   and `{result_path}` -- the brokered start-a-debate path will refuse a
   `{prompt}`-only seat, so say that BEFORE they decide, not after.
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
   never invent a cost claim). Only on an explicit yes:
   `<launcher> seats smoke <SEAT> --yes` -- run smoke commands ONE AT A TIME,
   sequentially, never in parallel (each is a spend the user authorized
   individually, and sequential runs keep the spend narrative auditable).

## Flow 2 — "start a debate"

1. Run `<launcher> onboarding status --project <ABS-CWD> --json`. If `attention`
   is not `ready`, run Flow 1 first (or the repair it names).
2. Show only currently present, project-approved seats. The user picks EXACTLY
   two. A remembered pair may be shown only as a labelled convenience default,
   never preselected on first onboarding.
3. Ask for or derive the debate subject and the review target, summarize what
   will be created (two seats, managed-v2 brokered channel, the human as
   supervisor -- this session never votes), and get the user's confirmation.
4. Run EXACTLY this form -- `--brokered` is NOT optional; plain `debate open`
   without it mints a legacy version-1 channel and is never the product path:
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
   --until-close` command.
6. Report the channel id and live status in plain language; keep the raw
   commands behind a "details" answer.

## What this skill never does

Never writes a registry or profile ahead of the user's approval answer (the
one carve-out: a wrapper the user NAMED and then SELECTED is registered as a
manual seat right before approve, disclosed, undoable via `seats remove`);
never invokes a seat model during setup; never edits channel files by hand;
never merges or publishes anything; never seats this interactive session as
a debater.
