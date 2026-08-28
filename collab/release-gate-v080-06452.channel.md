
## MSG-1 | 2026-08-27T21:22:43+00:00 | from: owner | type: review-request | thread: release-v080 | refs: main@15eac242782fb2e5a1d144a9a2d3a2e8778706c3

Release gate for the v0.8.0 tag. The artifact is the pinned source export at
main@15eac242782fb2e5a1d144a9a2d3a2e8778706c3 - the state that will be tagged, pushed to the public repository,
and released to PyPI. Review the tree as shipped, not its history; the 23
field findings (F7-F29 in the commit log) are context only.

Verify, each with your own fresh evidence from the export:

1. Suite: run exactly
   PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
   from the export root and quote the result line. PASS requires green.
2. Version coherence: pyproject.toml, src/debate/__init__.py,
   .claude-plugin/plugin.json and .codex-plugin/plugin.json all declare
   0.8.0.
3. README honesty: the install/uninstall instructions and the Windows
   paragraph make only claims the tree supports (hooks/hooks.json
   interpreter chain, scripts/debate-plugin plus its .cmd twin, the codex
   sandbox statement, user-data survival on uninstall).
4. Hook manifests: hooks/hooks.json and hooks/hooks-codex.json parse, match
   HOOK-CONTRACT.md, and carry no field the 2026-06-26 Codex parser
   incident class would reject.
5. Anything else release-blocking you can establish in your pass - name
   every blocking finding, not the first.

Verdicts cite your own runs, never this request. NO_PASS requires a
reproducing command per blocking finding.


Controller-Docket-Provenance:
- topology: minimum-two-agent
- controller-config-sha256: 978f1232c7f18b807a5d0e74b7fdd3b6eda06f3204eda2703f054836bb037b92
- source-ref: 15eac242782fb2e5a1d144a9a2d3a2e8778706c3
- review-contract: {"goal": "Establish whether the pinned v0.8.0 source tree is release-ready for the tag.", "review_contract_basis": "recorded", "review_domain": "The complete pinned export at the source ref: engine, tests, hooks, launchers, plugin manifests, README. The 23 field findings F7-F29 are context; the artifact under review is the current tree, not its history.", "review_mode": "release-gate", "stop_rule": "PASS only if your own fresh suite run is green and you find no release-blocking defect in code, manifests, or README claims; otherwise NO_PASS with bounded actionable findings. Stop at terminal agreement or the cap."}
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- docket-files: []
- profile-sha256: {"claude": "6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382", "codex": "3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-affiliated", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "073d42803d02867af7035116021655b266a4d8c945ce40749b52ce78e531f527", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "codex": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "f7354001b14cdbb8d61dc18f315b5086bbe08d0e675d9c82e0e00ce1f0e1d47a", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "codex", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "codex", "reasoning_effort": "default", "requested_model": "gpt-5.6-sol", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "d8f0b9811e99a96b4eb8f57acbef8eef6adb40a24e8c92e32a12162ea565f6f2", "codex": "edfd2fe55d81f61549595874f4ef1716fd9323abdfbe5026ce60b34bb1b12c1b"}

## MSG-2 | 2026-08-27T21:39:13+00:00 | from: claude | type: verdict | thread: release-v080 | refs: -

# Release gate: v0.8.0 @ 15eac242 — NO_PASS

My own fresh full-suite run was **not green**, which the stop rule makes decisive on its own. The failure is not a flake: it traces to a real gap in the code the test guards. Two in-scope documentation defects compound it. All three are bounded and cheap to fix.

## What held up (adversarial probing failed to break these)

- **Export integrity.** All 96 declared files hash-match the manifest; no missing, no mismatched, no extra files. `claude.manifest.json` itself hashes to `d8f0b9811e99a96b4eb8f57acbef8eef6adb40a24e8c92e32a12162ea565f6f2`, exactly as stated.
- **Clean-environment suite:** 910 passed, 1 skipped.
- **`ruff check .`** (0.7.1, inside the pinned `>=0.7,<0.8`): all checks passed.
- **`mypy .`** (2.3.0, inside the pinned `>=1.10.0,<2.4`), strict, whole repo: no issues in 60 source files.
- **Version lockstep** at `0.8.0` across pyproject, `debate.__version__`, and all three plugin manifests.
- **sdist completeness.** I built `debate-0.8.0.tar.gz`, extracted it, and ran the packaged tests from the extraction: 910 passed, 1 skipped. The 0.7.0 regression MANIFEST.in documents does **not** recur — I also confirmed every repo-root path the tests read (`README.md`, `CHANGELOG.md`, `PROTOCOL.md`, `pyproject.toml`, `.claude-plugin/`, `.codex-plugin/`, `hooks/`, `skills/`, `src/`) is covered by an `include`/`graft`.

## Blocking findings

### B1 — An ambient `CLAUDE_CONFIG_DIR` defeats F19, and reddens the suite

My fresh run: **1 failed, 909 passed, 1 skipped**.

```
FAILED tests/test_bridge.py::test_darwin_restores_the_real_home_for_an_operator_configured_seat
  - AssertionError: assert '/home/zoltan/.claude' is None
```

Root cause in `src/debate/bridge.py:634-689`. `seat_environment` builds the seat env as `os.environ` minus exactly two names (`OUR_OWN_ENV`), then in the darwin F19 branch does an early `return environment` **without unsetting an inherited `CLAUDE_CONFIG_DIR`**. The guarantee is implemented as *never setting* the pointer, which is not the same as the pointer *being absent*.

I confirmed the behavior directly, independent of the test:

```
darwin, NO ambient CLAUDE_CONFIG_DIR -> seat sees: None                   (F19 honored)
darwin, ambient CLAUDE_CONFIG_DIR set -> seat sees: '/home/zoltan/.claude' (F19 DEFEATED)
```

Why this matters beyond test hygiene:

- `bridge` is a **public CLI subcommand** (`src/debate/__main__.py:1090,1104-1105`), so it is reachable outside the controller. On the brokered path `_adapter_environment` (`controller.py:874-906`) builds a clean env from a baseline plus an explicit allowlist, so F19 *does* hold there — I want to be fair about that scope. But an operator running `debate bridge` directly on macOS from a shell that exports `CLAUDE_CONFIG_DIR` silently gets the suffixed-Keychain namespace that F19's own comment says "hides the operator's real login" — the precise failure F19 exists to prevent.
- The exporting shell is not hypothetical: **Claude Code itself exports `CLAUDE_CONFIG_DIR`**, which is why this surfaced here at all.
- It makes the release gate non-reproducible: CI is green only because GitHub runners happen not to set the variable. That is the same class of hazard the pyproject comments pin ruff and mypy to avoid.

The sibling test one screen up (`tests/test_bridge.py:788`) does `monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)`; the darwin test does not — so the gap exists in both the test and the code.

**Fix:** in the F19 branch, `environment.pop(variable, None)` before returning (and add the matching `delenv` to the test). Consider also dropping inherited `VENDOR_CONFIG_HOME_VARS` at the top of `seat_environment`, so the seat's vendor-config state is always something the bridge decided rather than something it inherited.

### B2 — CHANGELOG marks the tagged version "unreleased"

`CHANGELOG.md:9` reads `## v0.8.0 — unreleased`, while the file header three lines above states "Dates are the tag dates." Tagging `v0.8.0` ships that CHANGELOG in the sdist and publishes it as the GitHub Release body.

I checked whether the release workflow catches this: it does not. Its regex matches the heading and finds a non-empty body, so `release.yml` gates green and publishes anyway. Since a PyPI upload cannot be undone, this needs fixing before the tag, not after. One-line fix: replace `unreleased` with the tag date.

### B3 — README size claims are stale by more than 2x

`README.md:711-712` claims the project is "about 5,500 lines including the CLI, the broker and the setup wizard, with 413 tests as of this writing."

Measured on this tree: **13,144 lines** in `src/debate/` (11,447 excluding blanks and comments — stale on any counting method) and **911 tests collected**.

This sits in the "Young … read the code before trusting it" limits section, where the numbers exist specifically so a reader can size up how much unreviewed code they are taking on. Understating that by 2.4x undercuts the section's own purpose. README claims are explicitly in the gate's scope. Refresh both numbers.

## Recommendation

B2 and B3 are text edits. B1 is a two-line code fix plus a `delenv` in the test. With those three landed and the suite re-run in an environment that exports `CLAUDE_CONFIG_DIR`, I would expect this tree to pass; everything else I tried to break held.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 1e8669e5bee291fd65f165862591c037c8c06b7e430a87a0e9668271eab6bb69
- phase: sealed
- captured-at: 2026-08-27T21:39:13+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 0b4c9d67611f370440fe3f20b2c619e0b70f51fe4eb7cff1ee0a0f9e4c229d3f
- seat-declared-item-count: 16
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-affiliated
- profile-sha256: 6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382
- controller-config-sha256: 978f1232c7f18b807a5d0e74b7fdd3b6eda06f3204eda2703f054836bb037b92
- source-ref: 15eac242782fb2e5a1d144a9a2d3a2e8778706c3
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: d8f0b9811e99a96b4eb8f57acbef8eef6adb40a24e8c92e32a12162ea565f6f2
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: 53528c9e2a2bf276bb8c8363485666d19a1fc3b255c42c9065708c8c8d49891e
- requested-model: opus
- runtime-model: opus
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CLAUDE_CONFIG_DIR)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: 0e81075cdb53e590d667c557e7a9c6ef9f74dead92d564fadfae7a4fae0aa453
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 21e5a8842778a78e00401a9a5c3922a6ab5fa47a1a45bfff775fec8a86ac5c78
- phase-telemetry-sha256: d124c4374e2b561a33f98d08a25f6ebcf787d3a8670e89025e413249ab6c0ecd
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-3 | 2026-08-27T21:39:13+00:00 | from: codex | type: verdict | thread: release-v080 | refs: -

NO_PASS. Fresh verification is green: Ruff passed, strict mypy found no issues in 60 files, pytest completed with 910 passed and 1 skipped, and the package built successfully with the installed backend. Release blockers remain:

1. The active catalog still discovers `stealth/ox-alpha` as a frontier seat even though [seat_catalog.py:141](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/src/debate/seat_catalog.py:141) says it was revealed as priced GLM-5.3-Flash and the endpoint was retired. [README.md:260](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/README.md:260) and the release notes still advertise it as anonymous Ox Alpha at current `$0/M`. Remove it from active discovery or truthfully remap its identity, cost, and policy, then update the public text.

2. Credential-digest redaction is bypassable. Both [bridge.py:760](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/src/debate/bridge.py:760) and [controller.py:909](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/src/debate/controller.py:909) replace only lowercase `hexdigest()` output; the probe shows uppercase hexadecimal SHA-256 survives both layers despite the README and changelog promise. Redact hexadecimal digests case-insensitively and add bridge/controller/timeout regression tests.

3. The public result contract is stale. [README.md:394](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/README.md:394) says every new product verdict is schema v2, while [opening.py:1038](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/src/debate/opening.py:1038) hard-codes schema v3; v3 also publishes only an evidence digest/count rather than the README's inline example. Update the README, release notes, and compatibility explanation to describe v3 accurately.

4. The tree is not finalized for a tag: [CHANGELOG.md:9](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/CHANGELOG.md:9) still says `v0.8.0 — unreleased`, while the release preflight accepts that heading. Replace it with the tag date and make the workflow reject an `unreleased` release heading.

5. The Claude marketplace description promises two independent agents from other vendors, but the documented and enforced minimum permits one author-affiliated seat. Align [plugin.json:4](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/.claude-plugin/plugin.json:4) with the actual topology or strengthen enforcement. Also refresh or remove the volatile `5,500 lines / 413 tests` claim in [README.md:710](/home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-06452/exports/15eac242782fb2e5a1d144a9a2d3a2e8778706c3/codex/README.md:710); this export has 13,144 Python source lines and the fresh suite exercised 911 cases.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 1e8669e5bee291fd65f165862591c037c8c06b7e430a87a0e9668271eab6bb69
- phase: sealed
- captured-at: 2026-08-27T21:39:13+00:00

Controller-Verification:
- verification-status: performed
- verification-evidence-basis: seat-declared
- seat-declared-evidence-sha256: 912ffddbb9c99021ce9c4bf8cbc793035bace94f1da4162dce19be750ee55550
- seat-declared-item-count: 11
- exact-evidence: retained in the private invocation result

Controller-Provenance:
- phase: sealed
- topology: minimum-two-agent
- author-relationship: author-independent
- profile-sha256: 3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb
- controller-config-sha256: 978f1232c7f18b807a5d0e74b7fdd3b6eda06f3204eda2703f054836bb037b92
- source-ref: 15eac242782fb2e5a1d144a9a2d3a2e8778706c3
- review-mode: release-gate
- review-contract-basis: recorded
- source-manifest-sha256: edfd2fe55d81f61549595874f4ef1716fd9323abdfbe5026ce60b34bb1b12c1b
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- input-sha256: e243ed0ad9ee60c5378eef4c796706bcd4af1407067cd5aaa281d455f11a90ec
- requested-model: gpt-5.6-sol
- runtime-model: gpt-5.6-sol
- reasoning-effort: default
- cli-version: registry seat (debate 0.8.0); model identity declared by the registry
- isolation-mode: advisory
- runtime-model-basis: declared
- configuration-home: operator (CODEX_HOME)
- seat-process-exit-status: 0
- adapter-process-exit-status: 0
- seat-stdout-sha256: c73be3fb435dea68c1cd7fa768f03ac3e008e8820d4aa8c7883caa6aeb094dd2
- seat-stderr-sha256: bc8d6bed5810dee67d59a1e34d8810f5dbd8c3dd98175123639a9996f52c7555
- adapter-stdout-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stderr-sha256: 01db5bbdb2143494df4a08ac624d54f75f0b3b0f3806e3fd0ada2678bfb3e9cb
- phase-telemetry-sha256: 1ac370edb3e702e0551c1023d32c92551943b1fbb77eb1d1f806f1c0f9714a38
- verification-status: performed
- verification-evidence-basis: seat-declared
- isolation-flags: catalogued

## MSG-4 | 2026-08-27T21:39:14+00:00 | from: owner | type: close | thread: release-v080 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes. Runtime size at close: 52381094 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel release-gate-v080-06452 --config /home/zoltan/Projects/debate/.debate/channels/release-gate-v080-06452/watcher.json

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement
