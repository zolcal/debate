# Distributing `debate` as an Agent Skill — research & recommendation

**Date:** 2026-07-15 · **Author/executor:** Claude (Fable 5), deep-research workflow, 102 agents, 20 sources fetched, 25 claims adversarially verified (23 confirmed, 2 refuted).
**Revision r2 (2026-07-15):** body revised by the executor after the Codex review appended below (debate channel `collab/`, thread `skill-distribution-plan`) — slices 1–4 restructured as complete per-vendor install/test paths, dependency installation made fail-closed and consentful, attribution/transcript/one-command overclaims corrected, directory submissions turned into measured external gates.
**Question:** Is packaging `debate` as an Agent Skill (SKILL.md format) a better marketing/distribution channel than PyPI for building Zoltan's public reputation as an AI-tooling developer?

## Verdict: Hybrid — pip stays canonical, add a thin skill/plugin wrapper

Keep `pip install debate` as the versioned, canonical artifact. Add an Agent Skill + Claude Code plugin marketplace in the same GitHub repo. The skills channel provides discovery surfaces and *named-author attribution* that PyPI cannot match, while the pip package preserves the tool's cross-vendor neutrality and proper versioning. Critically, the two are complementary by design: a skill that declares the pip package as a dependency and teaches the agent the protocol is a compatible and precedented pattern (finding 2) — declared via `compatibility`, installed only with explicit user consent.

## Verified findings (all as of 2026-07-15)

### 1. Skills wrapping a CLI is the documented norm, not a hack — HIGH confidence (15-0 votes)
The format is defined by both Anthropic and the open spec as folders of *instructions, scripts, and resources*. The spec documents an optional `scripts/` directory ("The agent follows the instructions, optionally executing bundled code"); Claude Code docs say "Skills can bundle and run scripts in any language"; the anthropics/skills repo is 84% Python.
Sources: [agentskills.io/specification](https://agentskills.io/specification), [anthropics/skills](https://github.com/anthropics/skills), [Anthropic engineering post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills).

### 2. Skill + pip is compatible and precedented — HIGH confidence (6-0)
The spec's optional `compatibility` frontmatter field exists precisely to declare external requirements (spec's own examples: "Requires Python 3.14+ and uv", "Requires git, docker, jq"). Anthropic's own 11 official LSP plugins follow the plugin-wraps / user-installs-binary norm with a documented "Executable not found in $PATH" flow. The field is **declarative only** — it neither installs nor authorizes anything. Per the Codex review: a missing `debate` binary must **fail closed** with an exact install command for the *user* to approve (`pip install debate==X.Y.Z`; document `pipx` / `uv tool` for isolation too) — the skill must never trigger an implicit network/package mutation.

### 3. Agent Skills is an open cross-vendor standard — HIGH confidence (12-0)
Released by Anthropic as an open standard (agentskills.io, Apache 2.0/CC-BY); **44 client entries** verified on the spec site including OpenAI Codex, Gemini CLI, GitHub Copilot, VS Code, Cursor, JetBrains Junie, Goose, OpenCode, Roo Code, Mistral Vibe. One SKILL.md can reach both Claude Code *and* GPT-based agents.
**This amplifies debate's story rather than contradicting it**: a cross-vendor review protocol, itself shipped in the cross-vendor skill format, installable by both seats of the debate. Caveat: depth of support varies per client; Superpowers needed deliberate per-harness adapter work for its 10 harnesses.

### 4. No approval gate for self-publishing — HIGH confidence (9-0)
A skill is a filesystem package. Any GitHub repo with a `.claude-plugin/marketplace.json` becomes installable via `/plugin marketplace add zolcal/debate` — no Anthropic review, only a reserved-names anti-impersonation list.

### 5. First-party discovery exists but the best tier is gated — HIGH confidence (6-0)
- **claude-plugins-official** (curated, Anthropic's sole discretion): auto-registered in every Claude Code install, browsable in-app (`/plugin` Discover tab) and at [claude.com/plugins](https://claude.com/plugins) **with public install counts and "Made by <name>" attribution**.
- **anthropics/claude-plugins-community** (in-app submission form routes here): automated validation + safety screening, SHA-pinned; users must add it manually.

### 6. The ecosystem is huge and the ceiling for individual reputation is real — HIGH confidence
- anthropics/skills: **161,417 stars** in ~10 months (GitHub API, live-verified).
- **Superpowers precedent** (Jesse Vincent / obra, 12-0 verified): a SKILL.md-based developer-workflow framework — comparable in kind to `debate` — hit **~255k GitHub stars in 9 months** (14th on all of GitHub) and **941,207 displayed installs** on the official marketplace, with the listing publicly crediting "Made by Jesse Vincent" and linking his personal repo. PyPI *does* attribute the author (pyproject `authors` + project URLs already name Zoltan Soos and link the repo); the defensible claim is that marketplace attribution is more prominent and coupled to discovery/install signals.

### 7. …but the long tail is modest — MEDIUM confidence (2-1)
Across the largest measurable third-party marketplace namespace (452 npm-published packages), the *top* package saw only ~1,082 downloads/month. A skill listing alone does not guarantee attention. Superpowers' traction ran through an amplification event — **Simon Willison's 2025-10-10 write-up** — and the author's pre-existing reputation. The channel is a multiplier for a tool people talk about, not a substitute for being talked about.

## Refuted / unverified — do not build on these
- ✗ (1-2) "Skills reach all four Anthropic surfaces including the claude.ai consumer directory." The consumer-surface reach of a CLI-wrapping skill is **unverified**, and claude.ai's sandbox constrains network access and pip installs. Treat the skill as reliably useful in **Claude Code / Agent SDK / other CLI harnesses only**.
- ✗ (0-3) "tonsofskills.com hosts 470 plugins / 3,677 skills." Overall saturation remains poorly quantified.

## Risks
- **Spec churn / stewardship:** Anthropic is de facto steward (formal governance undefined); Claude Code layers proprietary extensions atop the open standard. Mitigation: the pip package stays canonical; the skill is a thin, cheap-to-update wrapper.
- **Survivorship bias:** Superpowers is an extreme outlier; no data exists on the *median* skill author's outcome.
- **Install-count opacity:** claude.com/plugins methodology undocumented (events, not unique users) — cite them carefully.
- **Security optics:** a fake skill passed a directory's security screening (thehackernews.com, 2026-06). A skill that *pins* `pip install debate==X.Y.Z` and is SHA-pinned in the community marketplace reads as trustworthy; leverage debate's audit-trail ethos here.

## Recommended plan (tracer-bullet slices, r2 per Codex review)

Slices 1–3 are independently shippable end-to-end paths. Slices 4 and 6 are **external gates**
(third parties control acceptance) with explicit done-conditions; slice 5 is the amplification
event. Naming, everywhere a display name is allowed: **"Debate — cross-vendor code review"**
(the bare word `debate` is collision-prone); the package/repo name stays `debate`.

1. **Slice 1 — Claude Code path, complete on a clean clone (~1 day).** One canonical
   `skills/debate/SKILL.md` (shared body for all vendors) **plus** `.claude-plugin/plugin.json`
   **and** `.claude-plugin/marketplace.json` — a marketplace entry alone is not an installable
   plugin. Skill body reconciled with the README's actual norms (the pinned prompts in
   `examples/claude-code.md` are raw material, not 90% done — line 40 still reads `CHANNEL.md`
   directly, contradicting README:135; fixing that drift is part of this slice): read
   `PROTOCOL.md` → check **open thread AND turn** (never turn alone) → `debate read` (never the
   raw file) → act → cite evidence appropriate to the task → post **only** via the CLI, with
   `--verify-refs` when refs apply → stop. Human-only merges, no pushes, dirty-worktree → work
   in a separate worktree. Missing binary **fails closed** with the exact install command for
   the user to run/approve. Implicit invocation disabled for any posting-capable skill.
   **Done =** on a clean clone: `/plugin marketplace add` → install → invoke → smoke review
   passes, plus negative cases: out-of-turn refusal, no-open-thread, missing binary.
2. **Slice 2 — Codex path, same skill body (~half a day).** Add the native Codex manifests:
   `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json` (Codex can read a
   legacy `.claude-plugin/marketplace.json` catalog, but the Codex manifest is still required).
   No duplicated workflow body — thin vendor manifests around the one SKILL.md.
   **Done =** `codex plugin marketplace add zolcal/debate` → install → smoke review on a clean
   clone. This slice *is* the cross-vendor demo: the same skill on both seats of a real review.
3. **Slice 3 — release-sync gate (~an hour).** If the skill pins `debate==X.Y.Z`, a release
   checklist (or CI check) keeps the pin and both plugin manifest versions in lockstep with
   `pyproject.toml`. A SHA-pinned marketplace entry does not authenticate or pin the PyPI
   wheel — the pin lives in the skill instructions and is part of every release.
4. **Slice 4 — directory submissions (external gates, not shippable slices).**
   - *Claude:* submit to anthropics/claude-plugins-community (automated validation +
     safety screening, SHA-pinned). **Done =** submission packet accepted by the portal.
   - *Codex:* two tiers — the owner-hosted Git marketplace (slice 2, low gate, little native
     discovery) already works; OpenAI's public directory is a **separate gated route**:
     verified publisher identity, listing/support/privacy/terms material, starter prompts,
     five positive + three negative tests, and review. (`github.com/openai/plugins` is a
     curated examples/default-marketplace repo, not a self-publishing endpoint.) Treat as its
     own gate, entered only if slice-6 metrics justify it. **Done =** complete submission
     packet accepted by OpenAI's portal: publisher identity verified, listing/support/privacy/
     terms material filed, starter prompts included, and the five positive + three negative
     tests passing in their harness. Acceptance into the directory itself is OpenAI's decision
     and is tracked as an outcome, not a task.
   - Gemini CLI / Cursor: install notes only, per the agentskills.io client showcase.
5. **Slice 5 — the amplification event (this is where reputation actually happens).** A
   write-up — "Two rival vendors' agents reviewed each other's code for four days" — built on
   the case study's verified anchors (63 messages / 112 KB / 4 days, the stale-fact incident,
   the 137× round-trip). **Precondition:** publish a redacted, provenance-linked transcript —
   the README today has only an illustrative exchange, and the story must not promise a
   transcript it doesn't ship. Claim "one command per seat *after setup*", never one-command
   reproduction (install, init, two seats, watcher config are separate steps). Targets:
   personal blog → HN → X. **Evidence artifact (required before publication):** a
   claim-to-source matrix accompanying the write-up — one row per number used in public copy
   (63 messages / 112 KB / 4 days, 137×, any star/install counts) mapping claim → primary
   source (repo file/line or URL) → dated snapshot (checked-in copy or archive.org), so every
   public number survives link rot and later re-verification.
6. **Slice 6 — reputation as a measured experiment, not an outlier extrapolation.** The table
   below, committed to git in this document, **is the versioned threshold artifact**; day-0
   baselines are captured at skill release, measurements at day 30 and day 90 are appended to
   this doc as dated appendix entries. Values are the owner's to tune before day 0 — these are
   the committed defaults:

      **Anti-encapsulation re-denomination (2026-07-17):** for a tool whose value is
   cross-vendor neutrality, the go decision is measured in vendor-neutral signals.
   **Primary signals (drive the go):** GitHub referral stars, PyPI download lift, completed
   externally-evidenced review rounds. **Secondary evidence (reported, never decisive):**
   marketplace installs and author-profile clicks — they measure duopoly-storefront reach,
   not adoption of the idea. **Operative rule (supersedes the go line below the table):**
   Go = any two of the three PRIMARY thresholds met at day 90; marketplace installs cannot
   substitute for a primary.

   | Metric | Day-30 signal | Day-90 go threshold |
   |---|---|---|
   | Qualified installs (both marketplaces, self-reported counts where displayed) | ≥ 25 | ≥ 100 |
   | New GitHub stars with skill/marketplace referral evidence (traffic tab) | ≥ 30 | ≥ 150 |
   | PyPI downloads/month above day-0 baseline | ≥ 100 | ≥ 500 |
   | Completed review rounds by external users (issue/discussion/transcript evidence) | ≥ 1 | ≥ 3 |
   | Author-profile click-through from listings | reported | reported (no threshold) |

   **Go = any two of the three PRIMARY thresholds met at day 90** (GitHub referral stars,
   PyPI download lift, completed externally-evidenced review rounds — see the re-denomination
   note above; marketplace installs are secondary evidence and cannot substitute). Otherwise
   stop: no further promotion spend — that is the experiment's honest exit. If go: pursue the curated
   claude.com/plugins tier (Anthropic's sole discretion; the only surface with public install
   counts + "Made by Zoltan Soos" attribution). **Done for the curated gate =** nomination/
   submission package delivered to Anthropic and the response recorded in this doc; the
   listing itself is Anthropic's decision, tracked as an outcome, not a task.

A standing correction from the review: the skill wrapper **adds no hard guarantees**. No-push,
truthful evidence, and human-only merge remain advisory model behavior wherever they live —
prompt or SKILL.md. The negative-case tests in slice 1 are the mitigation, not a fix.

## Open questions (from the research)
1. Anthropic's actual promotion criteria from community → official marketplace, and what fraction ever get promoted.
2. Whether a pip-shelling skill can run at all in claude.ai's sandbox, and whether the consumer directory accepts such skills.
3. The median (not outlier) reputation lift for a skill author.
4. ~~Whether OpenAI's Codex plugin marketplace has a lower barrier / better discovery for a cross-vendor tool, and whether both can be maintained from one repo without adapter drift.~~ **Answered by the Codex review (appended below):** owner-hosted Codex marketplace = low gate / little discovery; OpenAI public directory = verified-identity + test-suite gate; one repo serves both vendors via one SKILL.md plus thin native manifests. Whether Codex discovery beats Claude's remains unproven (no comparable traffic data).

## Source quality
Numbers from this report that get reused in public copy must first pass through the slice-5
claim-to-source matrix (claim → primary source → dated snapshot); the list below records
where claims came from, not a citable snapshot.
Primary sources live-verified 2026-07-15: agentskills.io (home + specification), anthropics/skills (+ GitHub API), code.claude.com docs (skills, discover-plugins, plugin-marketplaces), claude.com/plugins (+ /superpowers, byte-verified), obra/superpowers (+ GitHub API), anthropics/claude-plugins-official, Anthropic engineering blog. Secondary: simonwillison.net, larridin.com, secondstate.io, magarcia.io, paperclipped.de, agensi.io, HN thread 47204744, claude-code issue #31005, thehackernews.com.

## Review — 2026-07-15 · codex

**Verdict: REQUEST CHANGES — approve the hybrid direction as a measured, low-cost experiment, but do not execute the six slices as currently written.** The repository supports keeping PyPI canonical and adding a thin skill wrapper. The report establishes technical feasibility; it does not establish that the wrapper will build the author's reputation, and its rollout is not yet independently shippable or fully cross-vendor.

### Evidence checked

I reviewed this plan against `main@bcb402c`, [README.md](~/Projects/debate/README.md:76), [examples/claude-code.md](~/Projects/debate/examples/claude-code.md:1), and [pyproject.toml](~/Projects/debate/pyproject.toml:5), plus the current [Agent Skills specification](https://agentskills.io/specification), [Claude plugin-marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces), [Codex skills documentation](https://developers.openai.com/codex/skills), [Codex plugin packaging documentation](https://developers.openai.com/codex/plugins/build), [Codex public-submission requirements](https://developers.openai.com/codex/submit-plugins), and the [openai/plugins repository](https://github.com/openai/plugins). The checkout currently contains none of `skills/`, `.claude-plugin/`, `.codex-plugin/`, or `.agents/plugins/`. I did not treat the report's agent vote counts as independent corroboration, and its headline ecosystem metrics are not needed to reach the verdict below.

### Blocking corrections

1. **The first two slices are out of order and omit required artifacts.** Slice 1 cannot verify `/plugin marketplace add` before Slice 2 creates a marketplace. A Claude plugin also needs `.claude-plugin/plugin.json`, not only `.claude-plugin/marketplace.json`; adding a marketplace is distinct from installing and invoking its plugin. Make the first tracer bullet a complete clean-clone path: shared skill, required manifest and catalog, install, invocation, missing-binary behavior, and a smoke review. A second end-to-end bullet can add the other vendor rather than calling a non-installable skill folder shipped.

2. **The proposed skill source is stale in a material way.** [examples/claude-code.md:40](~/Projects/debate/examples/claude-code.md:40) tells Claude to read `CHANNEL.md` directly, while [README.md:135](~/Projects/debate/README.md:135) explicitly says pinned prompts should use `debate read`. The skill must also check that a thread is open, not only `signal.json.turn` ([README.md:170](~/Projects/debate/README.md:170)); read `PROTOCOL.md`; write only through the CLI; use `--verify-refs` when refs apply; preserve human-only merge/no-push and dirty-worktree boundaries; and request evidence appropriate to the task rather than always demanding a test count. The example is useful raw material, but “already 90%” hides reconciliation and negative-case work.

3. **`compatibility` declares a prerequisite; it neither installs nor authorizes one.** The wrapper is compatible with a pip-installed CLI, but “sanctioned combination” overstates the cited specification. A missing `debate` executable should fail closed with an exact user-approved install command, not cause an agent to make an implicit network/package mutation. For a CLI, document isolated `pipx` or `uv tool` installation as well as pip. If the skill pins `debate==0.2.0`, add a release gate that keeps the pin and both plugin versions synchronized with [pyproject.toml:7](~/Projects/debate/pyproject.toml:7); a SHA-pinned marketplace entry does not authenticate or pin the PyPI wheel.

4. **The Codex lane is feasible, but Slice 4 is not the lane.** Codex supports the open `SKILL.md` format, yet repo-local discovery uses `.agents/skills`, and installable distribution uses a plugin with `.codex-plugin/plugin.json`. A Codex marketplace normally uses `.agents/plugins/marketplace.json`; Codex can also read a legacy-compatible `.claude-plugin/marketplace.json` catalog, but that does not remove the Codex manifest requirement. One repository and one canonical `skills/debate/SKILL.md` can therefore serve both vendors with thin, tested vendor manifests—no duplicated workflow body is necessary.

5. **`github.com/openai/plugins` is real, but it is a curated examples/default-marketplace repository, not the adapter or a self-publishing endpoint.** Codex has two distribution tiers that should replace open question 4: an owner-hosted Git marketplace (`codex plugin marketplace add zolcal/debate`) has a low gate but little native discovery; a skills-only plugin can now be submitted to OpenAI's public directory, but requires verified publisher identity, listing/support/privacy/terms material, starter prompts, five positive and three negative tests, and review. Better discovery than Claude's directory is unproven because no comparable traffic or install data was established. Add the native Codex package and smoke test before “install notes,” and treat public submission as a separate external gate.

6. **The reputation conclusion needs an experiment, not an outlier extrapolation.** The report itself concedes survivorship bias and no median-author outcome. Superpowers is an existence proof, not a forecast for a small alpha CLI. Define 30/90-day baselines and go/no-go thresholds—qualified installs, GitHub referral traffic/stars, PyPI downloads, successful first review, and author-profile click-through—before spending effort on community/curated submissions. Agent vote counts are not independent evidence; preserve a claim-to-source matrix or dated snapshots for numbers used in public copy.

### Overclaims and missing risks

- PyPI attribution is not absent: [pyproject.toml:12](~/Projects/debate/pyproject.toml:12) names Zoltan Soos and its project URLs link the repository, issues, and case study. The defensible claim is that marketplace attribution may be more prominent and coupled to discovery/install signals.
- The Slice 5 evidence anchors are real: four days / 63 messages / 112 KB at [README.md:130](~/Projects/debate/README.md:130), the stale-fact incident at [README.md:163](~/Projects/debate/README.md:163), and the role flip / 137× result at [README.md:234](~/Projects/debate/README.md:234). But the checked files contain only an illustrative exchange, not the promised full transcript, and the case is not reproducible “in one command”: installation, channel initialization, two seats, watcher configuration, and scheduling are separate steps. Publish a redacted, provenance-linked transcript or change the copy; claim at most one-command seat invocation after setup.
- Skills do not strengthen the CLI's hard guarantees. No-push, truthful evidence, and human-only merge remain advisory model behavior ([README.md:150](~/Projects/debate/README.md:150)). Disable implicit invocation for any skill capable of posting, and test refusal/no-thread/out-of-turn/missing-binary cases.
- Community and curated acceptance are controlled by third parties, so Slices 3 and 6 are gates, not independently shippable outcomes. Define “submission packet accepted by the portal” as completion, with a traction threshold and stop condition for further promotion work.
- `debate` is a generic, collision-prone search term and can be confused with formal AI-safety debate despite the repository's clarification at [README.md:246](~/Projects/debate/README.md:246). Test a descriptive marketplace display name such as “Debate — cross-vendor code review” while keeping the package name stable.

**Approval conditions:** rewrite Slices 1–4 as complete Claude and Codex install/test paths sharing one skill body; make dependency installation explicit and consentful; add release synchronization and negative tests; correct the attribution, transcript, and one-command language; and turn later directory submissions into measured external gates. With those changes, the hybrid recommendation is sound and proportionate to this repository.
