# Pilot: does cross-vendor code review beat same-vendor review? (Study 1)

Date: 2026-07-17 · Owner: owner · Executor: kimi (K3) · Reviewer: glm-5.2 (via the debate channel)

**Status: PRE-REGISTERED DESIGN — published before any data exists, kill gate included.
Execution repo `~/Projects/debate-bench` stays private unless results pass the gate.**

## Pre-registered hypotheses and kill gate

**H1 (primary):** a reviewer from a *different vendor* catches ≥5 percentage points more
of a builder's defects than a reviewer from the *same vendor*, at matched false-positive
rate (confidence-thresholded ROC, recall read at FPR=10%), pooled across three model
pairs. **Kill gate:** if H1 fails (pooled delta <5pp, or direction inconsistent across
≥2 of 3 pairs), benchmarking stops — no Study 2, README stays philosophical.

**H2 (secondary, owner-directed):** the *full debate lifecycle* — review → fix →
re-review, repeated **until the two agents agree (reviewer finds zero new defects), or
the loop escalates** — catches more defects than round 1 alone, and the *useful* rounds
(run deeper, with new true defects still surfacing) are **more sustained for cross-vendor
pairs** than same-vendor pairs. Rationale: owner's production experience (single issues
needing up to 7 rounds; new logic problems surfacing after multiple rounds — e.g. the
anti-encap thread took 4 review rounds, each finding real residuals), and the
collective-delusion/echo-chamber failure mode is documented as *amplified* in homogeneous
pairs (M3MAD-Bench 2026; Choi 2025). H2 is measured and reported but does not move the
kill gate.

**Why this design (research summary, 2026-07-17):** naive "multi-agent debate > solo"
does not replicate at matched compute (Huang ICLR'24; Smit ICML'24; Choi NeurIPS'25),
but *model heterogeneity* survives every ablation (Mixture-of-Agents; ReConcile; "Stop
Overvaluing MAD"), and same-vendor/same-family reviewers inflate builder output 10–25%
(Panickssery ICML'24 + follow-ups). No published head-to-head of cross- vs same-vendor
review on code exists.

## Arms, corpus, and rounds

Per pair {A, B}: both models act as builder AND reviewer → 4 cells (A→A and B→B =
same-vendor; A→B and B→A = cross-vendor), all reviewing the SAME harvested item sets
(fully paired).

1. **Corpus — two tiers, because debate is built for hard problems (owner-directed):**
   the claim under test is not "spot the bug in a function" but *deep review*: the second
   agent reads the surrounding code, takes the fix into account, and applies additional
   reasoning — work a solo "fix this bug" loop never does. The corpus must contain
   problems where that depth is possible.
   - **Tier 1 (statistics):** each builder solves **80 problems** from a **LiveCodeBench
     2026 window** (post-cutoff for every model; mid/hard mix), one-shot, no retries.
     Function-level, scale, carries the inferential stats.
   - **Tier 2 (depth):** each builder attempts **30 real issues** from a **SWE-rebench
     2026 window** (repo-level, multi-file, post-cutoff; tests provided). Patches are
     execution-scored against the issue's FAIL_TO_PASS/PASS_TO_PASS tests in the sandbox
     (per-repo env images provided by SWE-rebench where available; otherwise skipped and
     logged). The review lifecycle on these patches genuinely requires reading repo
     context — this is the tier where H2's "rounds keep finding real things" should bite.
     Tier 2 is descriptive/qualitative (small n), Tier 1 carries significance tests.
2. **Execution scoring** in a local sandbox (venv, timeouts, basetemp inside the bench
   repo — never /tmp): failing = **buggy item** (vendor-typical bug, ground truth free),
   passing = **clean item** (FPR material). Applies to both tiers (Tier 2 uses the
   issue's own FAIL_TO_PASS/PASS_TO_PASS suites).
3. **Round 1 — static review:** Tier 1: problem + code + public tests visible, NO
   execution. Tier 2: the patch + the issue text + **read access to the repo snapshot**
   (reading is the depth we want to measure; execution is still forbidden — it collapses
   discrimination to harness competence). Strict JSON output in both:
   {verdict: PASS|FAIL, defects: [{location, category}], confidence 0..1}; one retry on
   malformed output, then scored as a miss.
4. **Rounds 2..R — the full debate lifecycle (owner-directed):** the builder receives the
   latest review verbatim and either produces a fix or *disputes* specific findings
   (structured JSON: fix | dispute with reasons); every fix is **execution re-scored**
   (objective outcome: buggy→green conversion, clean→broken rate); the reviewer then
   re-reviews the current state. The loop runs **until agreement** — reviewer returns
   zero new defects (CONVERGED) — or **escalates**, mirroring the production workflow:
   escalation triggers are (a) **4 review rounds** without convergence (the production
   maximum — thread_cap 8 admits exactly 4 verdicts in the canonical lifecycle, cf.
   MSG-28..35 in collab/archive/), or (b) **no-progress disagreement** — the same defect
   flagged in two consecutive rounds, or builder disputing twice without the reviewer
   conceding (ESCALATED, recorded as owner-call). Laziness can't game convergence: the execution
   re-score after every fix is the ground truth, and the final state after the loop
   (green / not-green) is recorded for every item regardless of the agents' agreement.
5. **Calibration arm (public dataset):** 150 **DebugBench**-Python items (GPT-4-injected
   bugs, public dataset, tests included) reviewed by all 6 reviewers under the same
   static protocol, round 1 only — no vendor-cell mapping; answers "is one reviewer just
   a uniformly stronger detector?", the main confound for H1. Injected-bug results are
   reported separately from organic results (mutation-spotting ≠ organic review).
6. Cell floors: <25 buggy items from a builder → add harder problems for that builder.

**Pairs:** (1) Fable 5 ↔ GPT-5.6 Sol — premium US, via `claude`/`codex` CLI subscriptions
(run FIRST: subscription window closes in days); (2) Kimi K3 ↔ GLM-5.2 — `kimi` CLI +
z.ai API (`GLM_API_KEY` in ~/.secrets); (3) **local pair — selection gate at S1/S2**
(owner-directed: local models and serving move fast; we take the best available at pull
time). Default: **Qwen 3.6 27B ↔ Gemma 4 31B** (both Apache-2.0, ~17–19 GB Q4 on the
3090 Ti; Qwen vendor-reports SWE-bench Verified 77.2; Gemma 4 31B has 91.5 HumanEval+
community submissions — Alibaba vs Google keeps the pair cross-vendor). Candidate list
evaluated at pull time against {fits 24 GB at Q4, ≥15 tok/s on the 3090 Ti, ≥95%
strict-JSON compliance on a 20-item smoke}: Qwen 3.6 27B, Gemma 4 31B (or 26B-A4B MoE),
NVIDIA Nemotron-3-Nano-Omni-30B-A3B, Cohere North Mini Code 30B. Hunyuan Hy3 (295B) and
Nemotron 3 Ultra (550B) are registered as NOT local-feasible on 40 GB. Local serving is
SEQUENTIAL on the 3090 Ti: each Q4 footprint (17–19 GB) exceeds the 16 GB 5060 Ti, and
two models cannot co-reside on 24 GB. Serving: Ollama
baseline; draft-model speculative decoding (DFlash-style acceleration) is ALLOWED as a
speedup — it is distribution-preserving/lossless by construction, and the serving config
is recorded in methods either way. Corrections registered: "GPT-4.6"/"GLM-6.4"/"GLM-4.2"
do not exist — pair 2 is GLM-5.2 (the production reviewer); Llama dropped (mid-tier for
coding 2026).
**Asymmetry annotation** (checked 2026-07-17; artificialanalysis.ai K3 page is JS-only,
figures from leaderboard coverage): coding strength runs Fable 5 ≈ GPT-5.6 > K3 >
GLM-5.2 (BenchLM coding 80.5 / 78.9 / 78.0 / 65.1), and Qwen 3.6 27B > Gemma 4 31B for
coding specifically — every pair has a reviewer-quality gradient, so per-cell
interpretation must separate raw reviewer strength from vendor decorrelation, which is
exactly what the calibration arm + paired design control for.

**Metrics:** per-cell recall (buggy), FPR (clean), recall@FPR=10% from confidence ROC;
paired exact McNemar per pair + pooled; bootstrap 95% CIs. Lifecycle: cumulative catch
rate by round, rounds-to-convergence distribution per vendor-type, **final pass rate
after the loop** (execution ground truth — bug caught AND fixed by agreement),
fix-conversion at convergence, break rate, escalation rate and escalation cause per
vendor-type (cross-vendor pairs are expected to escalate more on genuine disagreement,
same-vendor to converge prematurely — both are reported, not hidden). Secondary:
defect-category breakdown; manual localization spot-check 30 items/pair (no LLM judge —
it reimports the bias under test). Byproduct: solo pass rates per builder (free power
analysis for Study 2).

**Statistical analysis plan (locked pre-data — MSG-42 fold-in):**
- Primary endpoint: paired recall@FPR=10% delta (cross − same) per pair, pooled via
  **CMH stratified by pair** (discordants summed within pair, then combined). Naive
  pooling is forbidden (Simpson risk).
- Co-primary: **partial AUC over FPR∈[0,0.10]** per reviewer cell, and a **bootstrap 95%
  CI** on the pooled delta. Interpretation, pre-registered: a ≥5pp pass whose CI extends
  well below 0 reads "proceed to confirmatory Study 2", never "effect established".
- Floors: ≥25 buggy AND **≥40 clean** items per builder cell (shortfall → harder
  problems for that builder; the FPR=10% operating point must not rest on <40 items).
- **Within-pair consistency (aliasing guard):** on a single builder's bug set, same/cross
  is aliased with reviewer identity, so a delta there could be raw reviewer strength.
  H1 therefore requires BOTH builders in a pair to independently favor cross-vendor
  (direction, reported per-builder) AND the CMH-pooled ≥5pp. A pair failing both-builder
  consistency counts as inconsistent for the kill gate.
- **Calibration arm, quantitative role:** per pair, compute the pair-mates' DebugBench
  recall gap. If |gap| exceeds that pair's cross−same delta, the pair's H1 contribution
  is flagged confounded-by-strength and the pooled test is reported with and without
  flagged pairs.
- H2 endpoint ranking: **final-pass-rate-after-loop** (execution ground truth) primary;
  escalation rate secondary/descriptive (partly gameable by a reviewer refusing to
  concede a false positive).
- Rounds-2+ robustness: malformed fix/dispute JSON → one retry, then no-op and re-score;
  the item's loop ends as CAP-NOP, recorded.

## Harness

New **private** repo `~/Projects/debate-bench` (public only with passing results).
Stdlib-only Python (urllib to OpenAI-compatible endpoints: z.ai, Moonshot, Ollama).
Subscription seats via CLI wrappers in the glm-agent pattern (stdin detached, timeout,
generalized SEAT-OK identity check per seat before its run, logged). JSONL-append,
resumable per cell; pacing sleeps; raw prompts+outputs preserved. Methods records CLI
versions, dates, model aliases (subscriptions expose no seed/temperature — registered
limitation). The debate channel is NOT the transport (~5,000 calls); its role is
governance — this plan went through GLM review before execution.

## Vertical slices

- **S1 — pipeline proof (GLM-5.2 only, cheapest API):** repo scaffold + LCB window fetch
  + manifest + sandbox executor + generation runner → 80 solutions executed, sane
  pass/fail counts; then SWE-rebench window fetch + one repo-level issue attempted and
  execution-scored. *Gate: one builder end-to-end on BOTH tiers.*
- **S2 — all builders, premium first:** Fable 5, GPT-5.6 (subscription window!), K3,
  then both local models — Tier 1 (80 LCB) + Tier 2 (30 SWE-rebench issues) each.
  *Gate: 6 corpora harvested on both tiers; solo pass-rate table.*
- **S3 — review rounds + calibration:** 12 cells round 1 on both tiers, then the full
  debate lifecycle per flagged item (fix/dispute → execution re-score → re-review, until
  agreement or escalation), DebugBench calibration arm (round 1 only). *Gate: cells
  complete or logged skips; raw JSONL intact.*
- **S4 — analysis + decision:** McNemar/ROC/bootstrap, lifecycle curves + final pass
  rates, report md, kill/proceed against the registered gate. *Gate: decision written
  down, either way.*

**Budget:** ≈5,000–6,500 model calls total (1,100 generation across both tiers +
~1,800 round-1 reviews + 900 calibration + lifecycle rounds ≈ 1,200–2,700 depending on
flag/convergence rates). Tier-2 calls are repo-context-heavy (10–50× Tier-1 tokens) but
few. GLM/Kimi APIs ≈ $15–35; subscriptions $0 marginal (premium ≈ 800–1,000 calls per
seat, paced over the window — if caps bite, Tier 2 is trimmed first, pairing never
broken); local ≈ 2–4 GPU-days; wall clock ≈ 6–8 days, mostly unattended.

## Risks

- Subscription rate limits → premium first, resumable runner, pacing; partial paired
  results stand (paired analysis tolerates item-overlap restrictions).
- Contamination → LCB 2026 windows post-date all six models' cutoffs; DebugBench bugs
  post-2022 + synthetic; noted in methods.
- Reviewer tool use in CLI seats → bench dir has no allowlist (`claude -p` default-deny);
  prompts demand static review; tool-use transcript = item voided (round 1). Round-2
  fixes are execution-scored by OUR harness, not the builder's say-so.
- Multi-round echo risk is the thing H2 measures, not a confound: per-round increments
  are reported, so saturation/echo shows up as data, not noise.
- This plan itself is reviewed by GLM-5.2 via the debate channel (house rule) before S1.

## Review — 2026-07-18 · glm

**Scope.** Design review of this pre-registered pilot (Study 1), checked at
`glm-reviewer-seat@b420a8a` = HEAD (git-verified: this commit adds exactly these 164 lines,
no prior review section). I reviewed the *design*, not my own expected performance as one of
the six subjects. Fresh evidence cited below is my own — git state, host checks I ran, and my
own statistical reasoning — nothing quoted from MSG-41.

**Host checks I ran (bear on Axis 4 feasibility):**
- `~/.secrets` exports `GLM_API_KEY` (z.ai) and `KIMI_API_KEY` (Moonshot) — pair-2 API auth is ready.
- On PATH: `claude`, `codex`, `kimi`, `ollama` are installed; `glm` is not (correct — the plan
  calls GLM via the z.ai HTTP endpoint, not a CLI).
- GPUs: RTX 3090 Ti (24564 MiB) + RTX 5060 Ti (16311 MiB). **Both default local-pair models
  are ~17–19 GB at Q4, so neither fits the 16 GB card and both cannot co-reside on the 24 GB
  card** ⇒ local serving is necessarily *sequential*, one model resident at a time. The plan's
  "fits 24 GB at Q4" gate is per-model, not concurrent; see Blocking-4.

### Axis 1 — internal validity of the 4-cell paired design
**Sound in principle.** The balanced design cancels *pure reviewer strength*: averaging the two
cross cells (A→B, B→A) and two same cells (A→A, B→B), a vendor-symmetric strength difference
appears equally in both averages and washes out. The vendor-decorrelation signal is precisely
the *residual* — each reviewer doing relatively better on the *other* vendor's bugs than on
their own.

**Gap-1 (blocking, analysis-spec).** Within a *single* builder's bug set, the same/cross label
is **aliased with reviewer identity** (on A's bugs, "cross" = reviewer B, "same" = reviewer A,
so a B-stronger-than-A ordering alone produces cross > same on A's bugs). The design only
becomes identifying when **both** builders of a pair show cross > same (equivalently: the
pooled-within-pair contrast cancels the strength term). The kill gate checks direction
consistency *across the 3 pairs* but does **not** require or report within-pair both-builder
consistency. Pre-registration should lock: (a) the primary contrast is the pooled-within-pair
discordant sum (both builders, cross−same), and (b) a per-pair result is "direction-consistent"
only if both builders independently favor cross. Without this, a pair-level positive delta
driven by one strong reviewer on one builder's bugs could be misread as decorrelation.

**Gap-2 (blocking, analysis-spec).** The DebugBench calibration arm is described as answering
the strength confound, but its role in the *inferential test* is unspecified — it is currently
descriptive. Pre-reg should state the quantitative rule, e.g. "report each reviewer's DebugBench
recall@FPR=10% with CI; if a pair-mate gap exceeds the observed cross−same delta, flag the pair
as strength-confounded and down-weight it in the pooled test." As written, "controlled for" is a
claim, not an enforced procedure. (Minor caveat to record in methods: DebugBench bugs are
GPT-4-*injected*, so the calibration strength estimate is itself mildly biased toward
OpenAI-family reviewers — pair 1 sits in that family.)

**Minor.** "Vendor-typical bug" conflates *makes similar bugs* with *misses similar bugs*; the
hypothesis needs the latter. The defect-category breakdown + execution re-score partially
address this — keep them.

### Axis 2 — H1 kill gate (≥5pp at recall@FPR=10%, matched FPR)
**Threshold and matched-FPR logic are sound.** Holding FPR fixed is the correct way to compare
detectors of differing strength — it strips the "trigger-happy vs lenient" axis, so the recall
gap reflects discrimination. The effect-size gate (no p-value) is the *right* choice for an
underpowered pilot and avoids p-hacking.

**Gap-3 (blocking, robustness).** recall@FPR=10% at small clean-n is **threshold-noisy**: the
operating point is pinned by ~10% of clean items. With ~40–55 clean items/builder, that is
~4–5 items fixing the threshold — coarse and quantized, and the resulting binary table feeds
the McNemar. There is a cell floor on *buggy* items (≥25) but **none on clean items**, and
clean-n drives threshold stability. Pre-reg should: (a) add a clean-item floor (≥40 clean/builder,
or the cell is flagged low-power), and (b) make AUC (or partial-AUC over FPR∈[0,0.10]) a
**co-primary** discrimination metric — AUC integrates over all thresholds and is far more stable
at this n; keep recall@FPR=10% as the matched-FPR headline. As is, a "5.1pp pass" could be one
noisy threshold rather than a real effect.

**Minor.** The gate's "OR direction inconsistent across ≥2/3 pairs" is a good guard; tie it to
the within-pair rule from Gap-1.

### Axis 3 — lifecycle (H2): fix/dispute JSON, execution re-score, escalation
**Strongest part of the design.** Execution re-score as ground truth — and recording the final
green/not-green state *regardless of agent agreement* — is what makes the loop un-gameable for
the *outcome* metric. A reviewer that lazily returns "zero defects" to converge early still
leaves a red item red, which is exactly the premature-convergence failure H2 wants to expose:
gaming becomes signal.

**Gap-4 (non-blocking, robustness).** Malformed-JSON handling is specified for round 1 ("one
retry, then scored as a miss") but **not for rounds 2+** fix/dispute JSON. A malformed fix
should not stall the loop — pre-reg: one retry, then treat as no-op (dispute denied / fix =
no-change) and re-score. Trivial to specify now, hard to retrofit mid-run.

**Gap-5 (non-blocking, interpretation).** Escalation-rate is partly gameable / noisy: a
reviewer that refuses to concede a false positive forces escalation on a clean item, inflating
"cross-vendor escalates more." Execution re-score keeps the *outcome* clean, but the
escalation-*count* is soft. Pre-reg should rank H2 metrics: primary = final-pass-rate-after-loop
and cumulative-true-catch-by-round (both execution-grounded); escalation-rate/rcause =
secondary, interpret with care. The plan lists these but doesn't rank them.

**Minor.** "4 review rounds (production's thread_cap-8 brake)" — production's cap-8 is 8
*entries* (request+verdict+fix-report ≈ 2–3 review rounds), so 4 rounds is *more* than
production allows, not a mirror of it. The 4-round cap is fine for a pilot; just fix the
justification sentence.

### Axis 4 — feasibility against this host
**Call budget is internally consistent.** My recompute: generation 6×(80+30)≈660 (+retries);
round-1 reviews 12 cells × ~110 items ≈ 1.3–1.8k; calibration 6×150=900; lifecycle on flagged
items ≈ 1.2–2.7k ⇒ ~5–6.5k total. Matches the plan. Keys (GLM/Kimi) and CLI seats
(claude/codex/kimi/ollama) verified present above. Dual transport (urllib→OpenAI-compatible for
z.ai/Moonshot/Ollama; subprocess-CLI for claude/codex/kimi) is feasible — the seat-smoke through
the real watcher (MSG-37→38→39) already proved the stdin-detached + timeout + identity-check CLI
pattern on this host. Good reuse.

**Blocking-4 (feasibility, must state).** Local serving is **sequential on the 3090 Ti only**:
both defaults (~17–19 GB Q4) exceed the 5060 Ti's 16 GB, and two cannot co-reside on 24 GB. The
plan should say so explicitly (it currently implies both are just "on the 3090 Ti"). The 5060 Ti
is spare — it could host a smaller third candidate concurrently to cut wall-clock, or sit idle.
Wall-clock and GPU-day budget are fine under sequential serving; just don't let "fits 24 GB"
read as "both resident." (Blackwell sm_120 on the 5060 Ti: if any candidate is ever targeted
there, the ≥15 tok/s smoke must run on that card — early Q4 kernels can lag.)

**Affirm (load-bearing).** The generalized **SEAT-OK identity check per seat** is correctly
included and is what keeps pair 1 genuinely cross-vendor — bare `claude -p` defaults to the
Anthropic backend (the MSG-23 anti-encap lesson), which would silently collapse pair 1's
cross-vendor cell into same-vendor. The bench-dir-has-no-allowlist + "tool use = item voided
(round 1)" guard is the right complement. This is the single most important feasibility control;
keep it strict.

**Unverifiable from here (record as schedule risk, not design risk):** the premium subscription
window ("closes in days") and per-seat quotas. The premium-first S2 ordering + resumable runner +
"partial paired results stand" mitigation is the correct posture.

### Axis 5 — statistics: is n=80/builder Tier-1 + pooled McNemar adequate for a 5pp effect?
**Adequate for the effect-size gate; honestly underpowered for significance — which the plan
correctly does not claim.** Order-of-magnitude: ~25–40 buggy/builder (cell floor ≥25) ⇒ ~60
paired buggy items/pair ⇒ ~180 pooled across 3 pairs; discordant subset ~20–35% ⇒ ~35–60
discordants. SE of the pooled paired recall delta ≈ 3–4pp, so a true 5pp effect is ~1.3–1.5 SE
— detectable as an effect size, ~p 0.1–0.2 two-sided. That is the right calibration for a
*kill-gate pilot* deciding whether to fund a powered Study 2, and the plan frames it that way.

**Gap-6 (blocking, analysis-spec).** The pooled McNemar should be **stratified by pair**
(Cochran–Mantel–Haenszel, or sum discordants within pair then combine), not a naive pool. Pairs
differ in vendor distance and strength gradient; a naive pool can be dominated by one pair
(Simpson's paradox across pairs) and would contradict the "direction consistent across pairs"
guard. The plan already reports per-pair + pooled — good — but the pooled *test* should be CMH,
and pre-reg should lock that choice now (post-hoc pooling = researcher degrees of freedom).

**Gap-7 (blocking, analysis-spec).** Make the **bootstrap 95% CI on the pooled (cross−same)
recall@FPR=10% delta the co-primary inferential statement**, alongside the exact McNemar on the
at-threshold binary table. The McNemar's binary table inherits the threshold noise from Gap-3;
the bootstrap on the delta absorbs it and quantifies precision. Tie the gate to the CI: a pass
at 5pp with a CI spanning well below 0 should be labeled "proceed to confirmatory Study 2," not
"effect established." Pre-reg should say so explicitly so a wide-CI pass is not oversold.

### Verdict — REQUEST CHANGES
The core design is methodologically sound: balanced 4-cell cancellation of reviewer strength,
matched-FPR comparison, execution-grounded lifecycle that turns gaming into signal, and an
honest effect-size (not significance) gate appropriate to a pilot. I expect to **APPROVE after
fold-in.** The blocker is **pre-registration integrity**, not design correctness: a
pre-registration's value is locking the *analysis and decision rules* ex ante, and several
gaps above leave the primary inference under-specified (so the choices would effectively be made
after seeing data). All blockers are **doc-only edits to the executor (kimi)** — no hypothesis,
arm, corpus, or gate value changes:

- **BLOCKING (lock before S1):** Gap-1 (within-pair both-builder consistency rule), Gap-2
  (calibration arm's quantitative role in the test), Gap-3 (clean-item floor + AUC co-primary),
  Gap-6 (CMH-stratified pooled test), Gap-7 (bootstrap-CI co-primary + wide-CI-pass labeling),
  Blocking-4 (state local serving is sequential; both Q4 footprints exceed the 16 GB card).
- **NON-BLOCKING (fold if cheap):** Gap-4 (malformed fix/dispute JSON in rounds 2+), Gap-5
  (rank H2 metrics: final-pass-rate primary, escalation secondary), Axis-3 minor (fix the
  "thread_cap-8 = 4 rounds" analogy).

Procedural note: I dated this section 2026-07-18 (the actual review date), per the protocol's
"dated section" intent (attribution by when reviewed); the request suggested the doc's 2026-07-17
date. Same substance either way; flagging the one-day difference for the record.
