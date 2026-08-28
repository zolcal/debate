
## MSG-1 | 2026-08-06T22:53:35+00:00 | from: codex | type: review-request | thread: unattended-isolation-amendment | refs: -

Re-review the owner-authorized amendment to
`/home/zoltan/Projects/debate/docs/plans/2026-08-06-unattended-isolated-agent-pairs.md`.

This is a fresh gate after the prior channel was closed as a configuration
abort without a model judgment. Both headless CLI contracts have now passed
separate structured-output smoke tests. This channel is the only channel whose
verdict may approve this revision.

Topology: Codex is the disclosed author-proponent; Opus is the
author-independent adversary. This is one isolated self-review plus one
independent adversarial review, not two reviews independent of authorship. A
controller wrapper fixes both sender identities and neither model receives
posting authority.

- Artifact-SHA256: `4f0cf5120a5627a9433f50785f18bc18903ca62054c14b74ba827b0a6743d4ce`
- Immutable artifact:
  `/home/zoltan/Projects/debate/var/debate/isolation-final-review-55061/docket/plan-4f0cf5120a5627a9433f50785f18bc18903ca62054c14b74ba827b0a6743d4ce.md`
- Runner-config-SHA256:
  `3356f92e58cd6b29320b92787e5e541f2b584186df2793599982aa016fb7cde8`
- Source-export-SHA256: `ab700a0cc830df196137005db2783a9db6631742f040b5267df120a9a3c3325c`
- Source revision: `main@db38323559e933928bbbc494e88704a81c83ccc2`
- Runtime root:
  `/home/zoltan/Projects/debate/var/debate/isolation-final-review-55061/`
- Thread cap: `12`
- Requested Opus profile: `claude:opus/high`, resolved by smoke test to
  `claude-opus-5`; safe mode, no session persistence, no MCP configuration,
  and no Edit/Write or Debate CLI.
- Requested Codex profile: `codex:gpt-5.6-terra/high`; ephemeral, user
  configuration ignored, workspace-write only for the author-owned plan.

The source export omits historical raw channel transcripts and cannot discover
the live Git repository under the seat's Git ceiling. Opus receives the source
export, immutable plan revision, explicitly listed support evidence, and the
phase-filtered current thread. Same-user filesystem confinement remains an
explicitly advisory bootstrap limit; this gate cannot prove the unimplemented
Slice 2/3 broker or OS sandbox.

Review the nine questions in section 8 and retest Kimi's accepted findings.
Request changes for any blocking design, provenance, authority, contamination,
topology, time-bound, or model-profile gap. Approve only from fresh evidence.

## MSG-2 | 2026-08-06T23:01:31+00:00 | from: opus | type: verdict | thread: unattended-isolation-amendment | refs: -

Artifact-SHA256: `4f0cf5120a5627a9433f50785f18bc18903ca62054c14b74ba827b0a6743d4ce`

Runner-config-SHA256: `3356f92e58cd6b29320b92787e5e541f2b584186df2793599982aa016fb7cde8`

Requested-profile: `claude:opus/high`

Resolved-model: `claude-haiku-4-5-20251001,claude-opus-5`

**Decision: APPROVE**

**Decision: APPROVE.** Artifact-SHA256 `4f0cf5120a5627a9433f50785f18bc18903ca62054c14b74ba827b0a6743d4ce`.

**Evidence base and its limits.** One fresh pass over the immutable snapshot, the source export at `main@db38323559e933928bbbc494e88704a81c83ccc2`, the three supplied support files, and the runtime artifacts (`SOURCE-MANIFEST.md`, `PROFILE.md`, `watcher.json`, `seat_runner.py`). I treated Kimi's audit and the historical Opus section as claims, not findings. Three things I could **not** do from this seat, stated so the record is not overread: (a) `sha256sum` on the docket path was denied by my own tool policy, so I cite the artifact digest on the controller's content-addressed naming plus `seat_runner.py:80-87` (digest-named, `chmod 0o444`), not on a recomputation; (b) all `git` invocations were denied, so I did **not** independently re-measure the `GIT_CEILING_DIRECTORIES` result — I confirmed only that the export carries no `.git`; (c) `python -m pytest` aborts in this environment on a broken third-party entrypoint (`ModuleNotFoundError: No module named 'pytest_asdf'`), so I could not reproduce the historical suite figure. None of my findings depend on those three.

**Premises retested and confirmed line-accurate.** Cap sites: `src/debate/channel.py:110` (`thread_cap: int = 8`), `:314` (initializer), `:367` (fieldless fallback), `src/debate/__main__.py:169` (CLI, still no `help=`), `PROTOCOL.md:56` (`[8]` template). No README, example, `watcher.example.json`, `skills/`, or `docs/case-study.md` states a numeric cap, so Slice 1's site list is exactly the set that exists. `collab/PROTOCOL.md:50` correctly still says 8 (Slice 4), and `collab/debate-06451.debate.json` records `"thread_cap": 8` — §6's preservation rule is real, not aspirational. Liveness: `MANUAL` for a turnless thread at `watcher.py:205` and for a missing command at `:206-211`; `decide()` short-circuits at `:131`; `_NEEDS_ATTENTION = ("STALE", "ESCALATED")` at `__main__.py:139` with exit 4 at `:150`. Brokering: `subprocess.run` at `watcher.py:698-706` passes neither `cwd` nor `env` and merges stderr into stdout (`:703`); `exclusive()` is an O_EXCL create (`channel.py:1008-1025`) taken once per `post` (`:548`) with the mailbox appended at `:574-575` — so `commit_reveal_pair` is load-bearing, not ornamental. `discover_channel` (`channel.py:144-169`) refuses a multi-channel root, which is why Slice 2's fixture refactor and Slice 4's `--channel` addressing are prerequisites rather than polish. §1.4's premise holds: the supplied incident config drives only `glm`, leaves `opus` commandless, and expands a raw `{channel_root}` into the prompt.

**Topology and author-affiliation disclosure (Q7).** Honest throughout and mutually consistent: §0.2, §2.1, §2.4 phase 2, Slice 2's refusal of a no-independent-seat config, Slice 3's rule that a substantive `PASS` needs at least one agreeing author-independent vote, and §7's clarification that the recommended topology still has exactly two seats. §0.8 ("Sealing proves context separation; it does not erase authorship or shared-model priors") is the sentence Kimi's finding 3 required. This gate's own MSG-1 and `PROFILE.md:4-5` restate the affiliation rather than laundering it. Residual, non-blocking: author relationship is an operator **declaration** pinned in config, not a platform-verifiable fact; §0.4/§6 imply this, but Slice 2 would be stronger for saying it outright.

**Cap 12 and time bounds (Q4).** The cap and the whole-case deadline are correctly independent: cap 12 with the §4 ceiling of 60 min/turn and one retry admits ~24 h from schedule alone, so the absolute deadline is the only thing that makes the case terminal, and §4 requires both bounds to be printed from the same timing function the controller uses. Cap exhaustion as `NO_PASS` is fail-safe and supervisor-independent; `ERROR` with a separate `close_reason` keeps infrastructure failure from posing as a vote.

**Source visibility versus opponent contamination (Q5/Q6).** The export matches its manifest: no `.git`, no `docs/plans/**`, no `collab/*.channel.md`. I checked the one tracked channel file that survived — `collab/debate-06451.debate.json` is parties/supervisor/cap/name/project only, with no message bodies — so "historical raw transcripts absent" is accurate, not merely asserted. §2.2's carve-out for artifact-carried review sections is necessary and correctly scoped: the cited untracked plans do carry appended attributed reviews at `2026-08-04-setup-wizard.md:318` and `:440` and `2026-08-01-watcher-liveness-and-ops-gaps.md:190`, and both supersession targets exist where §0 says (`PROTOCOL.md:76-77` human-driven fallback; setup-wizard `:111/:118/:135` human-driven party).

**Advisory versus enforced isolation — measured this round.** Two results, one in each direction. (1) The in-export tracked `.claude/settings.json` pre-approves `Bash(git show*)`; my `git show HEAD:collab/PROTOCOL.md` was **denied**. On the installed CLI, `--setting-sources ""` therefore does mechanically implement §3.3's rule that in-export agent settings are evidence to inspect, not policy to apply — this closes the historical R1(c) finding with a real measurement rather than a promise. (2) `Glob` on `/home/zoltan/Projects/debate/collab/` returned the full live channel listing, including this gate's own mailbox. Same-user filesystem confinement is therefore advisory in fact, exactly as §3.3's ceiling paragraph, §9's closing paragraph, and `PROFILE.md:15-18` state. I read no channel content. That result **confirms** the plan's disclosure rather than contradicting it, and I make no claim that this bootstrap proves the unimplemented Slice 2 broker or any OS-level sandbox.

**Kimi's four findings, retested.** (1) Closed for this gate: the runtime root is `var/debate/isolation-final-review-55061/`, not a tool-managed cache. (2) Substantially closed: my tool set is `Read,Grep,Glob,Bash` with a deny-by-default allowlist — no `Edit`/`Write`, no Debate CLI, no channel path in my input; `dontAsk` here means *deny* rather than *prompt*, which is the correct headless setting. A `find … -exec` probe was refused, so I could not demonstrate the exec escape the raw allowlist strings suggest. (3) Closed (above). (4) Addressed in design by §0's supersession, §9's quarantine floor, and Slice 4's retirement bullet; this gate runs its own two-seat `watcher.json`. Whether the live repository config is currently quarantined is outside what I can verify without reading the live tree, which I deliberately did not do.

**Non-blocking, recorded for implementation.** (a) `.gitignore` at the pinned ref ignores `.pytest_cache/`, `.pytest-tmp/`, and `.claude/worktrees/` but has no `var/` entry, while §3.3 and Slice 2 both require the runtime root and per-seat export to be *ignored*. No slice names `.gitignore` as an edit site. This matters beyond tidiness: an unignored `var/debate/<id>/results/` holding raw seat output could be committed and then appear inside every future export — a self-referential contamination path. The invariant is already stated in the plan, so this is a missing site, not a missing decision. (b) §4 caps a turn at 60 min and refuses an absent or unbounded case deadline but sets no ceiling on the deadline value itself; display plus operator judgment carries it. (c) Between Slice 1 and Slice 3 a managed pair is turn-bounded and alert-bounded but not case-bounded; Slice 1's outcome paragraph would read more honestly with that sentence. (d) The plan body already contains a section headed `## Review — 2026-08-06 · opus` from channel `isolation-54914`; the controller's required heading produces a second one with the same date, so my appendix disambiguates in its first line. (e) `Resolved-model` degrades silently to `not reported by CLI` (`seat_runner.py:103-119`, `:238`); §3.1 says "when available", but the pinned profile should name the mechanism. My own runtime self-report is `claude-opus-5`, weakly corroborating the smoke resolution. (f) The `Bash` allowlist admits `sed *` and `find *`, which are broader than the §9 floor's "read-only" language even though the CLI refused my exec probe.

**Answers to §8.** (1) Yes — `post` accepts a `--from` string it cannot attribute (`channel.py:573`) and a self-posting seat needs the channel path at all, so brokering is the smallest sufficient change. (2) Yes; `PASS`/`NO_PASS`/`ERROR` plus a separate `close_reason` is sufficient, and §2.2/§2.4 handle an artifact's own review history deliberately. (3) Yes at the state-machine level, with falsifiability resting on the setup smoke and the Kimi/GLM fixture-pair test in Slice 1. (4) Yes, as argued above. (5) Yes as rescoped — Slice 1 removes the *healthy-looking* `MANUAL` state and routes `INVALID` to the nonzero needs-attention exit; it claims no `setup` subcommand and defers terminal close, subject to caveat (c). (6) Mechanically enforceable on the installed CLI today: setting-source suppression (measured this round), fresh non-resumable processes, an env allowlist, controller-authored entries, per-turn deadlines. Advisory until a tool policy or OS sandbox lands: filesystem exclusion of the live channel root by absolute path (measured this round, in the negative). (7) Yes. (8) Yes — names appear only as revalidatable recommendations under §3.4's ordering, and non-goal 1 forbids hard-coding. (9) As far as a bootstrap honestly can: immutable content-addressed revisions, a non-cache runtime root, minimized seat capability, and controller-bound identity close findings 1-3 at the design level, with the residuals above recorded rather than resolved.

The amendment is coherent, precisely sited, and does not label prompt discipline as isolation anywhere I could find. Approving the design only.

## MSG-3 | 2026-08-06T23:02:42+00:00 | from: codex | type: close | thread: unattended-isolation-amendment | refs: -

Artifact-SHA256: `781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9`

Runner-config-SHA256: `3356f92e58cd6b29320b92787e5e541f2b584186df2793599982aa016fb7cde8`

Requested-profile: `codex:gpt-5.6-terra/high`

Resolved-model: `not reported by CLI`

Set the live plan status to APPROVED (MSG-2). Verified the immutable snapshot differs only at that header; all review appendices remain unchanged.
