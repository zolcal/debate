---
name: debate-onboarding
description: Use when the Debate session-start notice offers setup, when the user says "set up Debate", or when the user asks to start a debate ("start a debate", "debate this") in a project with the Debate plugin installed. Guides seat approval and starts fully managed debates through the bundled engine; the user never types registry or environment commands.
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
- **Only the owner declares a change trivial or waives review.** Never say that
  something is too small to debate. When a plan, branch, or publishable artifact
  is ready, ask the owner whether to debate it unless they already answered.
- **Every subject gets a fresh channel.** A changed artifact being re-reviewed is
  a new subject and a new channel. Never reuse a terminal channel as if its old
  verdict had been rewritten.
- **Plain words, always.** Say *agent* for an AI tool installed on this
  machine (claude, codex, kimi, ...), and *wrapper* for a small script of the
  user's that launches one with fixed settings. Define a term the first time
  you use it. The technical names live behind a "details" answer.
  (Engine fact for YOU, never for the user's ears: user-facing text never says
  "managed version 1/2", "bridge", "brokered", "{prompt}",
  "{input_path}/{result_path}", "placeholder" or "operator-owned pins".)

## Flow 1 — "set up Debate" (approval)

1. Ask the user's consent if they have not just given it ("set up Debate" IS
   consent). Then run: `<launcher> onboarding inspect --project <ABS-CWD> --json`.
2. Present the candidates as a concise table: seat id, vendor/model identity, how
   the model selection is pinned (the command), present or missing, smoke state
   AND cost mode (the `cost_mode` field: subscription quota, metered API, local
   compute, or unknown -- report "unknown" as undeclared, never guess a value),
   and source (`catalog` = discovered, `derived`, `manual` = operator-authored,
   `unverified-wrapper` = a launcher script found next to a tool I know, plus
   "existing registry entry" where labelled). Label existing state visibly
   as existing state -- it is candidate input only. After the table, in plain
   language and roughly this order:
   If a row includes `data_policy_revision`, show its complete
   `data_policy_notice` immediately below that row and label the revision. If it
   includes `credential_env`, name the required variable but never resolve, hash,
   or print its value. For `stealth/ox-alpha`, say that it is an anonymous-provider
   limited preview for non-sensitive material, that the generic OpenRouter key is
   visible to the Ox process and potentially its tools, and that every route and
   allowance available to that key is in the blast radius. Current zero pricing is
   time-sensitive and its cost mode is API, not local or subscription.
   (a) one sentence on where the list comes from: "I found these by scanning
   this machine for AI tools I recognize";
   (b) one sentence of glossary if you will use the words: what an agent and
   a wrapper are (see the plain-words rule);
   (c) ONLY IF the table holds seats from vendors other than Claude and
   Codex, one low-key sentence such as: "Claude and Codex seats can take part in a fully managed
   debate as they are; for any other tool I first need to know how it turns
   off its settings, plugins and session saving -- I'll ask for that only if
   you pick such a seat for a debate." Never lead with legacy/version
   terminology; a new user does not care which channel version anything is;
   (d) the invitation: "Personal launcher scripts can't be detected
   automatically -- is there an AI tool or script of yours that should be on
   this list but isn't? Name it and I'll add it.";
   (e) ONLY IF the table holds rows whose source is `unverified-wrapper`:
   these are launcher scripts found sitting next to a tool Debate already
   knows. Give them the state "detected launcher script, model not verified
   -- declare to register" in the same table, and say that picking one is not
   approval on its own: it goes through the questions in step 3 first, and
   what gets approved is the seat those answers describe.
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
   fill-in-the-blank form.
   (d) "No model calls" means no AI spend -- it does NOT automatically mean
   no network: a metadata subcommand (a `<tool> models` listing, a version
   check) may contact the vendor's service. Prefer offline checks; when a
   command does phone home, say so in one honest clause ("the tool checked
   its service; no AI was called").
   (e) Settle what the seat will be able to do BEFORE they decide, with one
   numbered question: "Does this tool take extra command-line arguments?
   1 yes  2 no  3 I don't know." On answer 1, work out the arguments
   yourself and put ONE proposal to them, labelled as your inference: the
   arguments that make it ignore its own settings, plugins and hooks while
   it reviews (recorded with `--isolation-argv`), the ones that stop it
   saving a session (`--no-persistence-argv`), and, where the tool documents
   a configuration folder of its own, `--config-home VAR=dir`. On answer 2
   or 3, say plainly that the seat can still act as a reviewer in a classic
   debate. A small command of your own is a fully managed option only when you
   can make it speak the current evidence contract: it reads the request file,
   writes a version-2 answer file, and supplies either performed verification
   items (`command`, integer `exit_status`, non-empty `output`) or an `unable`
   reason with a `NO_PASS` decision. Show that result shape and the declarations
   `--verification-capable --result-schema-version 2` in the SAME approval.
   Never offer to write a wrapper that the product will then refuse or whose
   answer lacks evidence. (Engine fact for YOU: a prompt-style seat is wrapped
   when isolation, no-persistence, and verification capability are recorded;
   a hand-authored file adapter additionally needs declared result schema v2.)
4. Ask which seats to approve for THIS project, listing the user-named
   wrappers from step 3 as pending rows labelled "will be registered on
   approval". Prefer the host's structured question tool (multi-select); fall
   back to a numbered in-terminal question. Zero selections: report that
   onboarding stays incomplete, write nothing.
   For every selected seat with a data-policy revision, ask a separate explicit
   numbered acceptance only after showing the complete notice: "1 accept this exact
   revision for this project  2 do not approve this seat". Selection alone is not
   policy acceptance. On answer 2, remove that seat from the proposed allowlist.
5. Only after the user's answer: FIRST register any SELECTED pending wrappers
   -- disclosing that this writes the machine registry and is undone with
   `seats remove <SEAT>` --
   `<launcher> seats add <vendor>/<submodel> --command "<their argv>"
   --cost-mode <their answer or unknown> [--isolation-argv=<args>]
   [--no-persistence-argv=<args>] [--config-home VAR=dir]
   --verification-capable [--verification-argv=<args>]
   [--result-schema-version 2]`
   (the last three only where step 3 confirmed them; an unselected pending
   wrapper is never registered at all), then re-run inspect for the fresh
   candidate revision, then run:
   `<launcher> onboarding approve --project <ABS-CWD> --candidate-revision <rev>
   --allow <SEAT> [--allow <SEAT> ...]
   [--accept-policy <SEAT>=<DISPLAYED-REVISION> ...] --confirmed --json`
   Pass `--accept-policy` only for a seat whose exact displayed revision the user
   accepted in the current turn. A missing, stale, duplicate, or unselected
   acceptance refuses before either file is written.
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
2. Derive a concrete review brief from the user's short request and the real
   project files. It must name: subject; exact artifact/ref; goal; valid input
   domain; acceptance criteria; project-local verification commands; stop rule;
   and mode. Use `ordinary` for bounded feature/fix review. Use `release-gate`
   for branch, release, security, or other owner-designated gates. Do not invent
   criteria the artifact does not claim.
3. Ask the engine for its current numbered pair menu by running the product open
   form without `--pair` (it refuses read-only after printing the menu and
   budget). Render ONLY its admissible choices, in its stable order; never invent
   or re-rank a pair. A remembered pair is a labelled convenience, never silently
   selected. The user picks EXACTLY two. If two picks have different capability
   classes,
   (a lightweight fast model against a frontier reasoning model), say so
   plainly before confirming: seats of different weight often produce
   one-sided verdicts and cost an extra deliberation lap. The engine enforces
   this too -- an uneven pair is refused rather than seated quietly. Relay
   that refusal in plain words and ask a numbered question: "1 keep this pair
   2 pick again". Pass `--allow-mismatched-pair` ONLY after answer 1 in the
   current turn; answer 2 sends you back to step 2. (Engine fact for YOU, never
   for the user's ears: what gets created is a managed-version-2 brokered
   channel.)
4. Present one confirmation table, exactly these columns and rows:

   | Review field | Proposed value |
   |---|---|
   | Subject | ... |
   | Exact artifact | ... |
   | Mode | ordinary or release-gate |
   | Goal | ... |
   | Valid review domain | ... |
   | Acceptance criteria | ... |
   | Verification commands | ... |
   | Stop rule | ... |
   | Seats | exact pair from the engine menu |
   | Clean path | 2 vote-producing seat turns / 2 nested-seat launches |
   | Enforced maximum | engine-reported seat-turn and retry-inclusive nested-launch ceilings |

   Say in the same confirmation: this creates one NEW channel; the owner is
   supervisor and never a vote; supervisor posts consume the same entry cap;
   isolation remains advisory, not protection against hostile code; and every
   verification block is seat-declared evidence which the controller makes
   falsifiable but does not authenticate as truth. For ordinary mode the engine
   owns cap 5: at most four vote-producing seat turns and eight nested launches
   with the product retry policy. For release-gate mode its default cap 12 permits
   at most eleven seat turns and twenty-two launches. Use the exact budget the
   engine printed, including any profile-specific retry difference, rather than
   recalculating it. Ask once for confirmation before opening.
5. Run EXACTLY this form (agent-only engine fact: `--brokered` is NOT
   optional -- the plain form mints a legacy version-1 channel and is never
   the product path):
   `<launcher> open --brokered --root <ABS collab dir> --label <slug>
   --pair <a>,<b> --author-vendor <your host's catalog vendor: "claude" in
   Claude Code, "codex" in Codex> --goal <goal> --review-domain <domain>
   --stop-rule <stop> --review-mode <ordinary|release-gate>
   --docket-file <project-relative review input>
   [--docket-file ...]` (the docket files are what the seats actually read --
   always pass the review target; --author-vendor makes the recorded author
   relationship a declared fact: a seat sharing your host's vendor is recorded
   author-affiliated). Identity guards are enforced by the engine: the same seat
   twice and identical commands are refused outright; the same vendor/model at
   two efforts needs `--allow-identical-seats` -- ask the user explicitly before
   passing it, and only with a dedicated warning.
   If the engine refuses a seat because it does not know how that tool turns
   off its settings, plugins and session saving, relay the two ways forward as
   a numbered question: "1 tell me those arguments and I'll record them once
   2 let me write a version-2 review wrapper for this tool". On answer 1,
   collect isolation, persistence and verification declarations exactly as in
   Flow 1 step 3. On answer 2, show the mandatory v2 verification result shape
   and both registration declarations before writing/registering anything.
6. Print the engine's single `.debate/` ignore suggestion when it appears; never
   edit `.gitignore`. Open the docket with the `broker-open` hint (the request
   body states what to verify), then drive it with the printed `watch
   --until-close` command. Set the expectation once -- "this takes a few
   minutes of model thinking; I'll report when it closes" -- then BE QUIET:
   no polling narration, no handover edits mid-debate, one report at the
   typed close. A status showing a seat invocation in flight within its
   budget is healthy, not stuck.
7. Report the channel id, typed result, and the engine-reported runtime size in
   plain language. Mention the exact `debate runtime ...` inspection command
   once at close. Pruning is never automatic: inspect first, and run
   `debate runtime ... --prune --yes` only after explicit approval; it removes
   invocation homes/build/temp state while retaining the record, case state,
   inputs/results, streams, hashes, source manifests/exports and receipts.
   Keep other raw commands behind a "details" answer.

## Flow 3 — correct a falsified terminal finding

When fresh evidence disproves a finding in a terminal channel, do not edit or
reopen that history. Draft a supervisor `close`-typed post under a fresh correction slug.
The body must cite the original MSG number, show the exact fresh
command and output, say what was falsified, and state explicitly that the
historical verdict remains in the append-only record. Include nearby real defects
when the same check exposes them, so the correction is not self-serving. Present
the draft to the owner; post with `--from <recorded supervisor>` and
`--verify-refs` only after the owner authorizes speaking in their seat. This flow
opens no review case and wakes no model.

## What this skill never does

Never writes a registry or profile ahead of the user's approval answer (the
one carve-out: a wrapper the user NAMED and then SELECTED is registered as a
manual seat right before approve, disclosed, undoable via `seats remove`);
never invokes a seat model during setup; never edits channel files by hand;
never merges or publishes anything; never seats this interactive session as
a debater.
