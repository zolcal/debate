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
   escalation triggers are (a) **4 review rounds** without convergence (production's
   thread_cap-8 brake), or (b) **no-progress disagreement** — the same defect flagged in
   two consecutive rounds, or builder disputing twice without the reviewer conceding
   (ESCALATED, recorded as owner-call). Laziness can't game convergence: the execution
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
Nemotron 3 Ultra (550B) are registered as NOT local-feasible on 40 GB. Serving: Ollama
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
