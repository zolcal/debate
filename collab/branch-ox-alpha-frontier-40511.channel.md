
## MSG-1 | 2026-08-24T05:12:30+00:00 | from: owner | type: review-request | thread: branch-ox-alpha-frontier-1 | refs: feature/ox-alpha-frontier-seat@985e4e3010ac8efde0372be9a866cd2feb84a09b

Whole-branch release-gate review of
`feature/ox-alpha-frontier-seat@985e4e3010ac8efde0372be9a866cd2feb84a09b`,
based on `cc34c3459ff9d7a18e96c5200518f194f52f904e`.

Use `branch-docket.md` as the controlling acceptance contract. Inspect the complete
pinned export and materialized `branch.diff`; run the three mandated gates yourself
from that export and cite their exact final lines. The author's reported gate counts
and zero-call record are context, never your evidence.

This gate reviews the committed repository branch plus coherence with the immutable
host-launcher snapshot. It authorizes no Ox/OpenRouter inference, field case, registry
or profile mutation, push, merge, install, tag, or publication. The still-unrun owner
field pass is an explicit post-PASS boundary, not a missing branch-gate criterion.

Return `PASS` only on complete agreement that every docket criterion holds. Otherwise
return `NO_PASS` and enumerate every blocking finding you can establish in this pass.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 6d5a8fffb32746961b5fda1294686821fadfa3ee0a0a7718a643da8113841e92
- source-ref: 985e4e3010ac8efde0372be9a866cd2feb84a09b
- review-contract: {"review_contract_basis": "legacy-absent", "review_mode": "release-gate"}
- docket-revision-sha256: 55537e6d4a4ae53ee52d06adcc61e3831d30195f28a8947837cfc5a4db9ae7bf
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-ox-alpha-frontier-40511.debate.json", "sha256": "01f4021b711a0dec6ad1bd035ec54888af14a1f85d162b63d8f2f8264f77300a", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-ox-alpha-agent-and-frontier-seat.md", "sha256": "009450111e3290b465e745ed16232a6ebe40b34678f2cc8f63d3027bb7f7069e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch-docket.md", "sha256": "8d95f33f3693c17c62a6994fab42ad17e02a6085f22716721d52b2ec6ff27a3b", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch.diff", "sha256": "2a3b39d9d8338ae844768f0460e8a09ac82e48aaee81380553462ad8f92e592e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot.sh", "sha256": "0cf9cf73660bbe541b6911d5fb423db0f26536c70897cea2ec0f1a867691edf4", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot-metadata.md", "sha256": "5ff8a25b4bb31b6d6c1f3e144b79651b7034ae95b62021f96ccf7a575ef7ca06", "tracked_at_source_ref": false}, {"path": ".worktrees/ox-alpha-frontier-seat/.release-acceptance/ox-alpha/zero-call/ZERO-CALL-ACCEPTANCE.md", "sha256": "149690364c5ad79c016dc92a74f000cd93d6bb0145eadd167ce8690a61c50da8", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/seat_adapter.py", "sha256": "c83bf25044712ca0f8733738a50d6e772afd4d52ac1dd56cf158610397225222", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "3f8aef5eb7c405be8e841b72d6edb7b34e42b3b07eaabd63e9ccbd0c03ffcd59", "opus": "8d52a3a6c3f01d53ce669fe71ca9b1e5fe09b6f9c9d6137734d000135248955b"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "13df36e2c2049d853422d4f39ed26fb3dfcafaf261e72288ea48956a0d633d9f", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "f43386583f66b96f69c7e4237ad063ae1d9a08f36f2361ea7743879c0ed293df", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus exact verification Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "e5ce1e345ebca5c116e07113283fc9961580851749f93b08431ca33535f3b0ca", "opus": "e840e5d0671506a2b742ddd3a7696d862e3362db9459c6c9c7c65df498b57336"}

## MSG-2 | 2026-08-24T05:18:36+00:00 | from: owner | type: close | thread: branch-ox-alpha-frontier-1 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes. Observed failure: refused: adapter 'opus' exited 1; see /home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/cases/branch-ox-alpha-frontier-1/invocations/1-opus-1/stderr.txt

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-3 | 2026-08-24T05:19:58+00:00 | from: owner | type: review-request | thread: branch-ox-alpha-frontier-2 | refs: feature/ox-alpha-frontier-seat@985e4e3010ac8efde0372be9a866cd2feb84a09b

Fresh case retry for the same whole-branch release gate of
`feature/ox-alpha-frontier-seat@985e4e3010ac8efde0372be9a866cd2feb84a09b`.

The first case, `branch-ox-alpha-frontier-1` (MSG-1..2), closed typed `ERROR /
adapter-error` before any vote because the Opus CLI returned HTTP 529 Overloaded.
That was a reviewer-infrastructure failure, not a branch verdict. No branch, source
ref, docket criterion, or review material changed.

Use `branch-docket.md` as the controlling contract. Run all three mandated gates on
your own fresh pinned export and cite their exact final lines. The author's evidence
and the failed case are context only.

The gate harness now has zero automatic retries per seat turn. Together with the two
concurrent launches conservatively counted as spent by case 1, the cumulative
worst-case ceiling is 13 launches, below the 22-launch ceiling announced before the
gate; clean agreement is four cumulative launches. Both review seats remain
subscription-backed. Ox/OpenRouter inference remains forbidden.

Return `PASS` only on complete agreement that every docket criterion holds. Otherwise
return `NO_PASS` and enumerate every blocking finding you can establish in this pass.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: d0a434f7bbe1280e0c89527e605c32282d26bffff94e168c9c58b153cc6c86d8
- source-ref: 985e4e3010ac8efde0372be9a866cd2feb84a09b
- review-contract: {"review_contract_basis": "legacy-absent", "review_mode": "release-gate"}
- docket-revision-sha256: 55537e6d4a4ae53ee52d06adcc61e3831d30195f28a8947837cfc5a4db9ae7bf
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-ox-alpha-frontier-40511.debate.json", "sha256": "01f4021b711a0dec6ad1bd035ec54888af14a1f85d162b63d8f2f8264f77300a", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-ox-alpha-agent-and-frontier-seat.md", "sha256": "009450111e3290b465e745ed16232a6ebe40b34678f2cc8f63d3027bb7f7069e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch-docket.md", "sha256": "8d95f33f3693c17c62a6994fab42ad17e02a6085f22716721d52b2ec6ff27a3b", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch.diff", "sha256": "2a3b39d9d8338ae844768f0460e8a09ac82e48aaee81380553462ad8f92e592e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot.sh", "sha256": "0cf9cf73660bbe541b6911d5fb423db0f26536c70897cea2ec0f1a867691edf4", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot-metadata.md", "sha256": "5ff8a25b4bb31b6d6c1f3e144b79651b7034ae95b62021f96ccf7a575ef7ca06", "tracked_at_source_ref": false}, {"path": ".worktrees/ox-alpha-frontier-seat/.release-acceptance/ox-alpha/zero-call/ZERO-CALL-ACCEPTANCE.md", "sha256": "149690364c5ad79c016dc92a74f000cd93d6bb0145eadd167ce8690a61c50da8", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/seat_adapter.py", "sha256": "c83bf25044712ca0f8733738a50d6e772afd4d52ac1dd56cf158610397225222", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "e3f47c811d220642a2ce2a313b3892da6edbe0d0013413253e7d62437a4a9939", "opus": "294349759db9c996e929ef434914f55e874204eb0e7a4d4a5958ea91a635b0ef"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "13df36e2c2049d853422d4f39ed26fb3dfcafaf261e72288ea48956a0d633d9f", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "f43386583f66b96f69c7e4237ad063ae1d9a08f36f2361ea7743879c0ed293df", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus exact verification Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "e5ce1e345ebca5c116e07113283fc9961580851749f93b08431ca33535f3b0ca", "opus": "e840e5d0671506a2b742ddd3a7696d862e3362db9459c6c9c7c65df498b57336"}

## MSG-4 | 2026-08-24T05:31:46+00:00 | from: opus | type: verdict | thread: branch-ox-alpha-frontier-2 | refs: -

# Verdict: NO_PASS (one blocking item, environment-induced; no substantive finding against criteria 1-10)

All commands were run from the export root
`/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/985e4e3010ac8efde0372be9a866cd2feb84a09b/opus`.

## Versions

```
python3 --version                                  -> Python 3.12.12
/home/zoltan/Projects/debate/.venv/bin/ruff --version -> ruff 0.7.4
/home/zoltan/Projects/debate/.venv/bin/mypy --version -> mypy 2.3.0 (compiled: yes)
```

## Required commands, literal and in order

```
env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
FAILED tests/test_controller.py::test_root_pytest_does_not_collect_duplicate_tests_from_hidden_runtime
1 failed, 863 passed, 1 skipped in 103.28s (0:01:43)

/home/zoltan/Projects/debate/.venv/bin/ruff check --no-cache .
All checks passed!

/home/zoltan/Projects/debate/.venv/bin/mypy --cache-dir=/dev/null .
Success: no issues found in 57 source files
```

## BLOCKING 1 — the required pytest command is not green on my fresh run

The verdict bar is explicit ("PASS only if all three required commands pass on your own fresh run"), and it did not pass. I could not produce a green run of the literal command from the pinned read-only export by any configuration. I diagnosed the failure completely, and it is **not** a defect in this branch's code. Evidence:

1. The review harness injects a basetemp override into my shell:
```
env | grep '^PYTEST_ADDOPTS='
PYTEST_ADDOPTS=-p no:cacheprovider --basetemp=/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/cases/branch-ox-alpha-frontier-2/invocations/3-opus-1/build/pytest
```
2. That override is mandatory, because the export is read-only. Removing it collapses the suite:
```
env -u PYTHONPATH -u PYTEST_ADDOPTS PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
72 passed, 2 warnings, 793 errors in 17.13s
E  PermissionError: [Errno 13] Permission denied: '<export root>/.pytest-tmp'
```
3. `tests/test_controller.py:723-724` deliberately spawns its subprocess with `{**os.environ, ...}`, so the harness `--basetemp` propagates into a child whose cwd (`tmp_path/collection-fixture`) is *under* that basetemp. pytest's own validator then refuses. Reproduced independently, without touching the source:
```
env -u PYTHONPATH -u PYTEST_ADDOPTS PYTHONPATH=src python3 -m pytest --collect-only -q \
  --basetemp=/home/zoltan/Projects/debate tests/test_controller.py
python -m pytest: error: argument --basetemp: basetemp must not be empty, the current working directory or any parent directory of it
```
This is structural: `tmp_path` is always a descendant of `--basetemp`, so *any* basetemp override breaks this test, and a read-only export always requires one.

4. The failing test is pre-existing and untouched by this branch. `branch.diff` contains exactly one `tests/` entry:
```
1045: diff --git a/tests/test_ox_alpha.py b/tests/test_ox_alpha.py
```
`src/debate/controller.py:908` (which sets `PYTEST_ADDOPTS` for adapter children) and `src/debate/seats.py:37-42` `SANDBOX_ENV` are both outside this branch's hunks.

5. My 863 passed + 1 skipped + this 1 failure = 865 collected, exactly reconciling the author's context figure of `864 passed, 1 skipped`.

**Smallest concrete repair boundary:** make `tests/test_controller.py::test_root_pytest_does_not_collect_duplicate_tests_from_hidden_runtime` robust to an inherited `PYTEST_ADDOPTS` — e.g. add `"PYTEST_ADDOPTS": "-p no:cacheprovider"` (or pop the key) to the `environment` dict it already builds at `tests/test_controller.py:723`. That is a one-line change in a file this branch does not currently touch; it makes the branch's own declared gate command reproducible from a read-only export, which is what a release gate needs. No production code change is implied.

## Criteria 1-10: inspected, no blocking finding established

**1. True change set — satisfied.** `branch.diff` reconciles exactly to the declared inventory: 848 `+` lines minus 11 `+++` headers = **837 insertions**; 33 `-` lines minus 11 `---` headers = **22 deletions**; 11 files (`CHANGELOG.md`, `README.md`, `skills/debate-onboarding/SKILL.md`, `src/debate/{__main__,bridge,controller,onboarding,opening,seat_catalog,seats}.py`, new `tests/test_ox_alpha.py`). The exported tree matches the diff. No undeclared material change found.

**2. Standalone isolation and routing — satisfied.** `launcher-snapshot.sh`: requires only `OPENROUTER_API_KEY` (:13); `ANTHROPIC_API_KEY=""` (:32); `ANTHROPIC_BASE_URL="https://openrouter.ai/api"` exactly, with the `/v1` pitfall documented (:27-30); `CLAUDE_CONFIG_DIR=/home/zoltan/.claude-ox` (:41); Fable/Opus/Sonnet/Haiku/subagent all pinned to `claude-opus-4-8` (:36-40) which inline `modelOverrides` maps to `stealth/ox-alpha` (:59) at `--effort max` (:61). The comment at :48-51 states why the pin is inline rather than global — normal `claude` is not rerouted. Snapshot metadata records live == snapshot SHA-256 `0cf9cf73…`, mode 775, non-executable review copy. README (`+34`) and CHANGELOG (`+21`) both describe it as a *pre-existing / already installed* launcher, distinguishing it from merge-controlled code.

**3. Credential-name transport — satisfied.** `seat_catalog.py:56` `KNOWN_CREDENTIAL_ENV_VARS = frozenset({"OPENROUTER_API_KEY"})`; `seats.py:132-144` `validate_credential_env` refuses duplicates and every non-code-known name (so loader/shell-startup/Python/Git/HOME/PATH/Debate names all refuse by construction), and it is enforced at load (`seats.py:306`), save (`:385`), `add_seat` (`:899`), bridge parse (`bridge.py:310-313`), and admission (`opening.py:392-397`). Only names are serialized: `seats.py:430`, `opening.py:989/1043`, `controller.py:332`. `controller.py:246-251` hard-refuses a profile that puts a credential name into persistent `environment` additions, which is what keeps `sanitized_manifest`'s `environment_additions` hashes (`controller.py:316`) free of any value-derived digest. Value crossing is confined: `_baseline_environment()` returns `{}` on POSIX (`controller.py:846-849`), so `_adapter_environment` (`:889`) admits only allowlisted names — the Ox adapter only. Missing value refuses before launch at `controller.py:880-887` and before any channel write at `opening.py:398-403`.

**4. Failure-path redaction — satisfied.** `bridge.redact_seat_output` (`bridge.py:694-725`) and `controller._redact_credential_material` (`controller.py:914-931`) each strip both the raw value and its SHA-256, longest-match-first. Ordering is correct on every retention path I traced: bridge redacts at `_run` (`bridge.py:1011-1013`) *before* `save_seat_output` (`:1014`), before the non-zero `seat-failure.json` sidecar (`:1016-1025`, which stores only digests of already-redacted text), and before `parse_answer_with_verification` (`:1029`) — so a malformed-output refusal cannot quote an unredacted value. Controller redacts stdout, stderr *and* rewrites the result file (`controller.py:1608-1618`) before writing `stdout.txt`/`stderr.txt` (`:1621-1622`), before canary scanning (`:1628-1635`), before `failure.json` (`:1685`) and before `_parse_result` (`:1697`). Timeout (`:1586-1597`) and interrupt (`:1598-1606`) paths kill the tree and retain no stream at all. Retry re-runs over already-redacted artifacts. Replacement is targeted (exact value / exact digest only), so unrelated evidence is preserved.

**5. Compatibility — satisfied.** All three new fields are conditionally serialized and absent when unused: `seats.py:430-437`, `opening.py:989/1043`, `controller.py:332`, `onboarding.py:219-223`, `__main__.py:1443-1447`. `load_profile` defaults `data_policy_acceptances` to `{}` (`seats.py:1200`) and `onboarding.approve` omits the key entirely when empty (`onboarding.py:377-379`); `approve` is the only profile writer. Catalog refresh updates catalogued rows (`seats.py:602-604`) and derived rows (`:672-674`) while the comment and code at `:606-608/:630-631` keep manual rows untouched. Proven by `tests/test_ox_alpha.py:199-210`. The remaining 863 tests (v0.8 onboarding path included) pass.

**6. Revisioned policy consent — satisfied.** Discovery makes no model call and does not approve. `onboarding.approve` refuses a missing or stale acceptance (`onboarding.py:353-361`) and refuses acceptance supplied for an unselected/policy-free seat (`:362-371`), both *before* the temp-file/atomic-replace block at `:381-399` — so the transactional guarantee in its docstring (`:298-302`) holds. Only the revision identifier is persisted (`:379`). A changed catalog revision drives `stale_policy` -> attention (`onboarding.py:153-167`, `:176-179`) and blocks managed open (`opening.py:1123-1131`). Tested end-to-end at `tests/test_ox_alpha.py:236-284`.

**7. Honest seat semantics — satisfied.** `seat_catalog.py:124-158`: vendor `stealth` + submodel `ox-alpha` -> seat id `stealth/ox-alpha`; `capability_classes={"ox-alpha": "frontier"}`; `verification_capable=True` with explicit `verification_argv`. `opening.py:973/1023` records `provider = seat.vendor` = `stealth`, never Anthropic, while `cli_version` keeps the runner provenance separate. `cost_mode` defaults to `"unknown"` (`seats.py:71`) and discovery never upgrades it — asserted at `tests/test_ox_alpha.py:80`. No B1/LIGHT repair claim appears in the catalog notes, README, CHANGELOG, SKILL, or the zero-call record; the zero-call record states the opposite explicitly (`ZERO-CALL-ACCEPTANCE.md:53`).

**8. Privacy and blast-radius wording — satisfied.** Consistent across all five surfaces: catalog notice (`seat_catalog.py:152-157`), README (`+34..+48`), CHANGELOG (`+9..+22`), SKILL (`+60..+67`), launcher header (`:6-11`), plus `debate seats list` (`__main__.py:1470-1474`) and the adapter `authentication_mode` (`opening.py:979-984`, `:1031-1037`). Each says non-sensitive material only, that the Ox process and its tools can see the generic key, and that every route/allowance on that key is in scope. Zero pricing is labelled time-sensitive and API-backed, never subscription/local/permanent (README `+47-48`, catalog `:134`). Isolation is recorded as `"isolation_mode": "advisory"` and the wording never claims an OS-enforced secret boundary.

**9. Test quality — satisfied for the security and consent contracts.** `tests/test_ox_alpha.py` proves refusals, not happy paths: unknown name and `LD_PRELOAD` refuse (`:111-132`); the digest, not just the value, is checked absent from the adapter mapping and the sanitized manifest (`:107`, `:170`); cross-seat non-leak is asserted positively *and* negatively (`:154-155`, `:164-165`); stale-revision acceptance refuses (`:244-252`); and mutation-before-refusal is disproved by comparing full `project.rglob("*")` listings around each refusal (`:308`, `:320`, `:333`) with `load_config_fn` wired to `pytest.fail` so a channel-loader call would be caught (`:315`, `:328`). No false-negative scan or setup-bypass pattern found.

**10. Lifecycle honesty — satisfied.** `ZERO-CALL-ACCEPTANCE.md:46-53` states no inference call, no smoke, no live registry/profile change, no branch review, nothing pushed/merged/installed/tagged/published. The plan checklist leaves the field record and branch gate unchecked (`:374-375`). No code or documentation claims a field pass occurred.

## Non-blocking observations (no repair required for this gate)

1. **Short-value redaction guard.** `bridge.py:702-711` and `controller.py:918-928` skip only empty values; a pathologically short credential value would `str.replace` unrelated text, brushing criterion 4's "without hiding unrelated evidence". Real OpenRouter keys are long and empty values already refuse at `controller.py:880-887`, so this is theoretical. A minimum-length guard at the same two sites would close it.
2. **Plan Slice C coverage gap.** Slice C promised a test that a fake Ox seat "is pairable with a distinct frontier seat; it is never suggested for a LIGHT target". `tests/test_ox_alpha.py` has no pairing/suggestion test (`_other_seat`/`_open_spec` are used only for refusal cases). The contract itself is enforced by `capability_classes={"ox-alpha": "frontier"}` and asserted at `:81`, and pairing/ranking logic is unchanged by this branch, so criterion 7 still holds.
3. **Surface asymmetry.** `debate seats list` prints the credential variable name (`__main__.py:1470-1474`); the human-readable `onboarding inspect` output prints only the policy notice (`__main__.py:1102-1106`). The name is present in the JSON (`onboarding.py:219-220`) and the SKILL instructs the agent to name it, so the disclosure contract holds.
4. **Launcher does not create `.claude-ox`.** Plan Slice A said "Create only this exact directory if absent"; the snapshot has no `mkdir`. Metadata records the directory already exists at mode 700, and criterion 2 does not require creation.
5. **Handover not in the branch.** Slice D's `docs/HANDOVER-SESSION-18.md` update is not present; `docs/` at this ref contains only `assets/` and `case-study.md`, and handovers/plans are untracked at the source ref. Consistent with the declared 11-file inventory, not an undeclared change.

## Summary

The implementation is coherent, honestly documented, and satisfies every acceptance criterion I could test. ruff and mypy are clean on my own fresh run. The single blocking item is that the docket's required pytest command does not pass on my own fresh run from the pinned read-only export, and the explicit verdict bar does not let the goal override that. The cause is fully isolated to one pre-existing test's inheritance of the harness `PYTEST_ADDOPTS`, and the repair is one line in `tests/test_controller.py:723`.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 2378e31a367016502b47cf07386ad4e6c5bbb151322982696f5fe20962365b0c
- phase: sealed
- captured-at: 2026-08-24T05:31:46+00:00

Controller-Verification:
- verification-status: absent
- verification-evidence-basis: absent

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 294349759db9c996e929ef434914f55e874204eb0e7a4d4a5958ea91a635b0ef
- controller-config-sha256: d0a434f7bbe1280e0c89527e605c32282d26bffff94e168c9c58b153cc6c86d8
- source-ref: 985e4e3010ac8efde0372be9a866cd2feb84a09b
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: e840e5d0671506a2b742ddd3a7696d862e3362db9459c6c9c7c65df498b57336
- docket-revision-sha256: 55537e6d4a4ae53ee52d06adcc61e3831d30195f28a8947837cfc5a4db9ae7bf
- input-sha256: 33f8715a03ccbdd4525f06d152f2155a6196e40db1de24f98855ffa1225d7175
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: absent
- verification-evidence-basis: absent

## MSG-5 | 2026-08-24T05:31:46+00:00 | from: codex | type: verdict | thread: branch-ox-alpha-frontier-2 | refs: -

Docket integrity: `sha256sum` matched all 10 supplied docket hashes. `awk` over the materialized `branch.diff` reported `additions=837 deletions=22`; `rg '^diff --git '` reported 11 files, matching inventory.

Required verification: `env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q` reached a failure at 23% but did not complete within the executor window. The diagnostic `env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -xq` completed: `1 failed, 182 passed in 10.48s`. Failure: `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/985e4e3010ac8efde0372be9a866cd2feb84a09b/codex/tests/test_controller.py:711-733`; its nested pytest inherits `PYTEST_ADDOPTS`, which supplies an invalid `--basetemp` for the nested working directory. Clear/replace that inherited option in the nested-test environment. `/home/zoltan/Projects/debate/.venv/bin/ruff check --no-cache .` returned `All checks passed!`; `/home/zoltan/Projects/debate/.venv/bin/mypy --cache-dir=/dev/null .` returned `Success: no issues found in 57 source files`. Versions: Python 3.12.12, ruff 0.7.4, mypy 2.3.0.

Additional blocking findings:
1. Missing credential smoke preflight is absent. `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/985e4e3010ac8efde0372be9a866cd2feb84a09b/codex/src/debate/seats.py:1076-1127` calls `setup.smoke` without validating `credential_env`. Fresh probe with `OPENROUTER_API_KEY` absent printed `missing-key smoke invoked setup.smoke=True; recorded=pass`. This violates the required refusal before smoke writes/model launch. Preflight the bounded credential names before confirmation, scratch creation, smoke invocation, or smoke-status mutation.
2. Timeout can retain an unredacted credential in `result.json`. `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/985e4e3010ac8efde0372be9a866cd2feb84a09b/codex/src/debate/controller.py:1583-1606` raises directly on timeout, while redaction of `result_path` starts only at lines 1608-1618. A credential-bearing adapter can write the result then hang; its raw value/digest remains in the invocation runtime. Redact/quarantine all retained result and stream artifacts in timeout and exceptional paths before recording/raising.
3. The launcher snapshot permits route/effort escape. `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/dockets/55537e6d4a4ae53ee52d06adcc61e3831d30195f28a8947837cfc5a4db9ae7bf/files/var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot.sh:55-62` explicitly places `$@` after `--model opus --effort max` and states that user `--model` or `--effort high` still wins. That contradicts the required exact Ox/max pin. Reject/strip overrides or place/enforce the fixed settings after user arguments.
4. Onboarding inspect omits the required current-price observation. Fresh candidate probe printed `cost_mode=unknown` and a policy notice containing no `$0/M` or time-sensitive pricing. The omission is implemented at `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/985e4e3010ac8efde0372be9a866cd2feb84a09b/codex/src/debate/onboarding.py:206-224` and rendered at `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/985e4e3010ac8efde0372be9a866cd2feb84a09b/codex/src/debate/__main__.py:1092-1107`. Add a non-persistent current-price/time-sensitivity observation to inspect output while preserving `cost_mode: unknown` until owner declaration.

`tests/test_ox_alpha.py` itself passed (`7 passed in 0.68s`) but lacks coverage for the failing missing-credential smoke and timeout-retention paths.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 2378e31a367016502b47cf07386ad4e6c5bbb151322982696f5fe20962365b0c
- phase: sealed
- captured-at: 2026-08-24T05:31:46+00:00

Controller-Verification:
- verification-status: absent
- verification-evidence-basis: absent

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e3f47c811d220642a2ce2a313b3892da6edbe0d0013413253e7d62437a4a9939
- controller-config-sha256: d0a434f7bbe1280e0c89527e605c32282d26bffff94e168c9c58b153cc6c86d8
- source-ref: 985e4e3010ac8efde0372be9a866cd2feb84a09b
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: e5ce1e345ebca5c116e07113283fc9961580851749f93b08431ca33535f3b0ca
- docket-revision-sha256: 55537e6d4a4ae53ee52d06adcc61e3831d30195f28a8947837cfc5a4db9ae7bf
- input-sha256: 011083e3671410898f14ecb6786da96d8c2764e017c285a7ab63ac8de50a873c
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.0
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: absent
- verification-evidence-basis: absent

## MSG-6 | 2026-08-24T05:31:46+00:00 | from: owner | type: close | thread: branch-ox-alpha-frontier-2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-7 | 2026-08-24T05:45:25+00:00 | from: owner | type: review-request | thread: branch-ox-alpha-frontier-3 | refs: feature/ox-alpha-frontier-seat@a62b21d71102f2528da622aabfe90a84d867cd1b

Fold-delta review of `feature/ox-alpha-frontier-seat`, now at
`a62b21d71102f2528da622aabfe90a84d867cd1b` after case 2 closed NO_PASS at MSG-6.
Prior reviewed head: `985e4e3010ac8efde0372be9a866cd2feb84a09b`.

Use `branch-docket-r2.md` as the controlling round-2 contract. Independently compute
the repository and external-launcher true change sets, verify both directions between
the five prior findings and the folds, run all three mandated gates from your fresh
current export, and perform the required coherence sweep. The author's fold list and
gate counts are context, never your evidence.

No Ox/OpenRouter call or owner field pass is authorized. Return `PASS` only on complete
agreement that all five findings are resolved with no fold regression; otherwise
return `NO_PASS` with every blocking finding you can establish.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: efdf225871c997933054fc58185fff000c8d7aed7dc1fb64b28ca494f8520aa6
- source-ref: a62b21d71102f2528da622aabfe90a84d867cd1b
- review-contract: {"review_contract_basis": "legacy-absent", "review_mode": "release-gate"}
- docket-revision-sha256: bc18607430cd63589378ba90791cb518f4a510086a2df147b9cf356cd59e821d
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "dfb3950a24d38ac308632baa117e961ae9da00ed1b8aac8a48261d8cbeaeb9c6", "tracked_at_source_ref": true}, {"path": "collab/branch-ox-alpha-frontier-40511.debate.json", "sha256": "01f4021b711a0dec6ad1bd035ec54888af14a1f85d162b63d8f2f8264f77300a", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-23-ox-alpha-agent-and-frontier-seat.md", "sha256": "009450111e3290b465e745ed16232a6ebe40b34678f2cc8f63d3027bb7f7069e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch-docket.md", "sha256": "8d95f33f3693c17c62a6994fab42ad17e02a6085f22716721d52b2ec6ff27a3b", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch.diff", "sha256": "2a3b39d9d8338ae844768f0460e8a09ac82e48aaee81380553462ad8f92e592e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch-docket-r2.md", "sha256": "2d0135b4668bddff31053b29e73c6935ea5977853bae5667748004ebe0c2f887", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/fold-r1.diff", "sha256": "ebd7292779ef9d74a7802fd5ea520acb7bfcf8c8d5a8c20b35c4761a203d6d11", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/branch-r2.diff", "sha256": "59963c6be8f6a590beb45c730c488cca15cccd197326c95f412f3542fc3ffd98", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-fold-r1.diff", "sha256": "0a4ffa1ddb70fbb8b6c8ffde9fbe39ab20fd3637e70d8191b8c5d1b12b8c3a98", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot.sh", "sha256": "4654fb6a4c310637d5d61592597eec863f964ceb6bf7bfcd682d70764a3221cb", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/launcher-snapshot-metadata.md", "sha256": "a350202c025efc092e19abc727220288ceeabfb2d8aeb506f77f2845aa88430b", "tracked_at_source_ref": false}, {"path": ".worktrees/ox-alpha-frontier-seat/.release-acceptance/ox-alpha/zero-call/ZERO-CALL-ACCEPTANCE.md", "sha256": "b90afde74159c742b25fcc6b8cf10db0d32291f761421f4c709a0deee123876e", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/branch-ox-alpha-frontier-40511/seat_adapter.py", "sha256": "c83bf25044712ca0f8733738a50d6e772afd4d52ac1dd56cf158610397225222", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "e3f47c811d220642a2ce2a313b3892da6edbe0d0013413253e7d62437a4a9939", "opus": "294349759db9c996e929ef434914f55e874204eb0e7a4d4a5958ea91a635b0ef"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.149.0", "command_sha256": "13df36e2c2049d853422d4f39ed26fb3dfcafaf261e72288ea48956a0d633d9f", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.241", "command_sha256": "f43386583f66b96f69c7e4237ad063ae1d9a08f36f2361ea7743879c0ed293df", "cost_mode": "subscription", "environment_additions": {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus exact verification Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"codex": "9e70d07ef3dcaf1fe5877e84c5de1e990a2af7b82ba5cdbbff695ecfdcb40930", "opus": "7148c91b3df6eb65253b9ef74f8152238ee87938e08dd8a1da8eaf73b685f5cd"}

## MSG-8 | 2026-08-24T05:52:24+00:00 | from: opus | type: verdict | thread: branch-ox-alpha-frontier-3 | refs: -

## Mandated verification (fresh, from the pinned export root `.../exports/a62b21d71102f2528da622aabfe90a84d867cd1b/opus`)

Run literally and in docket order.

```text
env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
866 passed, 1 skipped in 107.29s (0:01:47)        [exit 0]

/home/zoltan/Projects/debate/.venv/bin/ruff check --no-cache .
All checks passed!

/home/zoltan/Projects/debate/.venv/bin/mypy --cache-dir=/dev/null .
Success: no issues found in 57 source files
```

Versions: `python3 --version` -> `Python 3.12.12`; `ruff --version` -> `ruff 0.7.4`; `mypy --version` -> `mypy 2.3.0 (compiled: yes)`.

Extra adverse-condition run, reproducing round-1 finding 1's exact trigger (inherited `PYTEST_ADDOPTS` carrying `--basetemp`):

```text
env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  PYTEST_ADDOPTS="-p no:cacheprovider --basetemp=<writable invocation tmp>/adverse-basetemp" \
  python3 -m pytest -q tests/test_controller.py::test_root_pytest_does_not_collect_duplicate_tests_from_hidden_runtime
1 passed in 0.59s
```

## True change set, computed not trusted

Bash is denied on the docket directory in this seat (`sha256sum`, `wc`, `diff`, `git hash-object` all refused), so I established the fold cryptographically from the diff artifacts themselves using Read/Grep, which is stronger than the author's stat line.

`git` blob indexes in `branch.diff` (r1) vs `branch-r2.diff` (r2) chain exactly through `fold-r1.diff`:

- CHANGELOG.md `5dccc5f..24f701f`, README.md `1ed5a86..b679aea`, `__main__.py` `38f3da4..e01a65b`, `controller.py` `cf3f974..b8496bf`, `onboarding.py` `f25a293..d781913`, `seat_catalog.py` `08e0c57..d95d492`, `seats.py` `f5e9074..81068d6`, `tests/test_ox_alpha.py` `078b7e3..b6312eb` — each r1 post-image is the fold pre-image and each fold post-image is the r2 post-image.
- `tests/test_controller.py` `ef80fe5..bd040a7`: `ef80fe5` is the frozen base blob, i.e. this file was untouched at r1 and enters the branch only through the fold. Branch inventory therefore moves 11 -> 12 files, which is consistent, not undeclared.
- Unchanged between r1 and r2: `skills/debate-onboarding/SKILL.md` (`bd12895`), `src/debate/bridge.py` (`bd66b2b`), `src/debate/opening.py` (`2a9e7b1`). I also byte-compared the SKILL.md hunks in both diffs (branch.diff:52-95 vs branch-r2.diff:60-103) — identical.

Conclusion: the true fold is exactly the 9 files in `fold-r1.diff`. No edit is absent from the author's fold list, and no listed fold is fictitious.

## Each prior finding has an effective fold

1. **Gate environment.** `tests/test_controller.py:744` sets `"PYTEST_ADDOPTS": "-p no:cacheprovider"` in the nested collection subprocess, replacing inheritance. The outer gate command is untouched, and `tests/test_controller.py:709` (the other nested-pytest test) still supplies its own explicit basetemp; `:1339` still pops the variable. Proven by both the literal gate run and the adverse-basetemp run above.
2. **Smoke preflight.** `src/debate/seats.py:1096-1104` calls `validate_credential_env` then refuses on any missing value — placed before the `ask(...)` spend confirmation (`:1105`), before `scratch_base.mkdir` (`:1116`), before `setup_module.smoke` (`:1131`) and before `seat.smoke = SmokeStatus(...)` (`:1133`). `tests/test_ox_alpha.py` `test_missing_credential_refuses_smoke_before_confirmation_or_scratch` fails the test on any `ask` or `setup.smoke` call and asserts `not scratch.exists()` and `ox.smoke is None`. Its seat comes from production `seats.discover` against the real CATALOG (`_ox_seat`, `tests/test_ox_alpha.py:33-37`), so the test does not bypass the default it claims to prove.
3. **Exceptional redaction.** `src/debate/controller.py:934-961` adds one sanitizer, called on all three exits: timeout `:1622` (before the `AdapterError` is raised), `except BaseException` `:1637`, and the normal/non-zero path `:1642` (before `stdout.txt`/`stderr.txt` are written at `:1645-1646` and before the result is folded into the canary scan at `:1653-1655`). It discards rather than preserves on symlink, non-UTF-8/unreadable, and write failure — the symlink branch also closes the write-through-symlink hazard the old `is_file()`+`write_text` shape had. `_redact_credential_material` (`:914-931`) removes both the raw value and its SHA-256, longest-first. The regression `test_timeout_redacts_a_credential_bearing_result_before_retention` uses a fake adapter that writes value+digest then sleeps past a 1s timeout, and asserts `secret not in retained`, `digest not in retained`, plus both redaction markers present. Timeout path retains no stdout/stderr at all.
4. **Launcher pin.** `launcher-snapshot.sh:59-68` rejects `--settings`, `--model`, `--fallback-model`, `--agent`, `--agents`, `--effort` and every `--name=value` form with `exit 2`, and the loop precedes `exec claude` (`:70-74`). Route invariants still hold: `OPENROUTER_API_KEY` is the only required variable (`:13`), `ANTHROPIC_API_KEY=""` (`:32`), base URL exactly `https://openrouter.ai/api` (`:30`), `CLAUDE_CONFIG_DIR=/home/zoltan/.claude-ox` (`:41`), all four alias slots plus `CLAUDE_CODE_SUBAGENT_MODEL` pinned to `claude-opus-4-8` (`:36-40`) which `modelOverrides` maps to `stealth/ox-alpha` at `--effort max`; the pin is inline `--settings`, so ordinary `claude` is not rerouted (`:47-51`). Scope note: I verified this by inspecting the immutable snapshot text, whose SHA-256 in the docket manifest (`4654fb6a...`) matches `launcher-snapshot-metadata.md`'s recorded live and snapshot hash; executing the host launcher is outside this seat's authorization, so the runtime override checks remain the metadata record's zero-inference evidence, not mine.
5. **Price observation.** `src/debate/seat_catalog.py:161-164` adds the catalog-only `price_observation` ("Observed 2026-08-23: $0/M input and output; this API-backed preview price is time-sensitive and not guaranteed."). Surfaced in JSON at `src/debate/onboarding.py:235-236` and in human inspect at `src/debate/__main__.py:1107-1108`. It is not a `Seat` field: a full-tree grep for `price_observation` returns only `seat_catalog.py`, `onboarding.py`, `__main__.py` and the test, so it cannot reach registry serialization (`seats.py:430`) or the project profile — confirmed by the exact profile equality assertion at `tests/test_ox_alpha.py:272-276`. `cost_mode` stays `unknown` from the production catalog (`tests/test_ox_alpha.py:81`). Both JSON and rendered-output assertions are present (`:235-241`).

## Coherence sweep over criteria 1-10 on the current head

- Credential transport (3): `KNOWN_CREDENTIAL_ENV_VARS` is `frozenset({"OPENROUTER_API_KEY"})` (`seat_catalog.py:56`), so arbitrary/reserved/loader/shell/Python/Git/HOME/PATH/Debate names all refuse via `validate_credential_env` (`seats.py:132-144`), enforced at registry load `:306`, save `:385`, add `:899`, opening `opening.py:392-402`, bridge `bridge.py:311` and now smoke `:1096`. The live value crosses only into the child env at `controller._adapter_environment:879-890`, which refuses missing values before any launch.
- Failure-path redaction (4): bridge redacts before `save_seat_output` (`bridge.py:1011-1014`) and the failure sidecar carries only exit status and hashes of already-redacted text (`:1016-1025`); `run_seat` keeps no clock of its own (`:632-650`), so a hung nested seat is killed by the controller, which is exactly the path fold 3 now sanitizes. Redaction is value-scoped, so unrelated evidence is untouched.
- Compatibility (5): `test_legacy_payload_stays_free_of_new_optional_fields` still asserts `credential_env`/`data_policy_*` are absent from legacy rows; fold 2 is a no-op for seats with empty `credential_env`; fold 5 adds a key only when a matching catalog entry declares one.
- Consent (6): discovery remains in-memory and non-approving (`onboarding._scan`), approve still requires `--confirmed`, an exact revision match (`onboarding.py:369-372`) and a matching candidate revision (`:339-344`); the stale-revision path still returns `offer_refresh` with `data_policy_accepted: False`.
- Seat semantics (7) and privacy wording (8): README.md:229-247, CHANGELOG.md:21-38 and SKILL.md carry non-sensitive-material, key-visible-to-process-and-tools, whole-key-blast-radius, time-sensitive `$0/M`, and `api`-not-subscription/local wording, and the new fold sentences match the code they describe. Ox is described as frontier-only and is not claimed to repair the LIGHT/B1 gap.
- Lifecycle (10): `ZERO-CALL-ACCEPTANCE.md` states no Ox/OpenRouter call, no smoke, no field case, project profile absent, nothing pushed/merged/installed/tagged/published, and that fold-delta review is pending. Nothing in the branch claims a field run occurred. Test count moves 864 -> 866, matching exactly the two new regressions.

No blocking finding established in this pass. Non-blocking observations, recorded so a later pass need not re-derive them: (a) in `controller.py:938-944`, `discard()` can raise `AdapterError` from inside the `except BaseException` handler at `:1637` if `unlink` fails, which would supersede a `KeyboardInterrupt` and makes the adjacent "The exception itself is untouched" comment slightly narrower than literal — it requires an unlinkable file in a directory the controller itself created; (b) `_candidate_revision` now hashes `price_observation` too, so a catalog price edit changes the candidate revision and forces a re-inspect before approve — conservative in criterion 6's direction, not a regression; (c) the launcher guard matches long-form options only, which covers every option named in round-1 finding 4.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 97b8ff31ad58dee9dc27cf9e77d4f0b58c500540f9a46bc82cad6cdfa119b419
- phase: sealed
- captured-at: 2026-08-24T05:52:24+00:00

Controller-Verification:
- verification-status: absent
- verification-evidence-basis: absent

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: 294349759db9c996e929ef434914f55e874204eb0e7a4d4a5958ea91a635b0ef
- controller-config-sha256: efdf225871c997933054fc58185fff000c8d7aed7dc1fb64b28ca494f8520aa6
- source-ref: a62b21d71102f2528da622aabfe90a84d867cd1b
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: 7148c91b3df6eb65253b9ef74f8152238ee87938e08dd8a1da8eaf73b685f5cd
- docket-revision-sha256: bc18607430cd63589378ba90791cb518f4a510086a2df147b9cf356cd59e821d
- input-sha256: 9fd383a0da24233ac74ccc0ace42b905967a9e3a6c10a7048ce770b61aea0ea0
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.241
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: 35f2418923f21d42011311417734c7538c7d3d08b695814f99c4907c99fef0c4
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: absent
- verification-evidence-basis: absent

## MSG-9 | 2026-08-24T05:52:24+00:00 | from: codex | type: verdict | thread: branch-ox-alpha-frontier-3 | refs: -

Fresh required gates from `/home/zoltan/Projects/debate/var/debate/branch-ox-alpha-frontier-40511/exports/a62b21d71102f2528da622aabfe90a84d867cd1b/codex`:
- `env -u PYTHONPATH PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q` → `866 passed, 1 skipped in 107.53s (0:01:47)`.
- `/home/zoltan/Projects/debate/.venv/bin/ruff check --no-cache .` → `All checks passed!`.
- `/home/zoltan/Projects/debate/.venv/bin/mypy --cache-dir=/dev/null .` → `Success: no issues found in 57 source files`.
Versions: `Python 3.12.12`; `ruff 0.7.4`; `mypy 2.3.0 (compiled: yes)`.

I verified all immutable-docket SHA-256 values. `git apply --numstat < fold-r1.diff` reports the declared 208 insertions and 16 deletions across 9 repository files; `branch-r2.diff` contains 12 current paths, coherently comprising the original 11-file branch plus the folded `tests/test_controller.py` repair. The separate launcher fold contains one path. `bash -n launcher-snapshot.sh` succeeded and `sha256sum` produced `4654fb6a4c310637d5d61592597eec863f964ceb6bf7bfcd682d70764a3221cb`, matching its immutable metadata.

The five prior blockers are effectively resolved: the nested pytest subprocess clears inherited basetemp options; smoke credential validation precedes confirmation and scratch creation; controller result sanitization runs on normal, timeout, and exceptional exits and redacts values plus SHA-256 digests; the launcher rejects route/model/settings/agent/effort overrides; and onboarding inspect exposes the catalog-only dated, API-backed, time-sensitive `$0/M` observation while leaving cost mode unknown. The source, complete current diff, fold diff, launcher fold, docs, and tests are coherent with criteria 1–10; no new blocking regression was established.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 97b8ff31ad58dee9dc27cf9e77d4f0b58c500540f9a46bc82cad6cdfa119b419
- phase: sealed
- captured-at: 2026-08-24T05:52:24+00:00

Controller-Verification:
- verification-status: absent
- verification-evidence-basis: absent

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: e3f47c811d220642a2ce2a313b3892da6edbe0d0013413253e7d62437a4a9939
- controller-config-sha256: efdf225871c997933054fc58185fff000c8d7aed7dc1fb64b28ca494f8520aa6
- source-ref: a62b21d71102f2528da622aabfe90a84d867cd1b
- review-mode: release-gate
- review-contract-basis: legacy-absent
- source-manifest-sha256: 9e70d07ef3dcaf1fe5877e84c5de1e990a2af7b82ba5cdbbff695ecfdcb40930
- docket-revision-sha256: bc18607430cd63589378ba90791cb518f4a510086a2df147b9cf356cd59e821d
- input-sha256: 728f3a3edf69aed4c469a469e0d344d1172c89e2fb7985cf3f54796c394e0b22
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.149.0
- isolation-mode: advisory
- runtime-model-basis: verified
- configuration-home: sandbox
- seat-process-exit-status: not-separate
- adapter-process-exit-status: 0
- seat-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- seat-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- adapter-stdout-sha256: a2b0385502da6a03c29313f3d1ef4a48052999241aeb0d46420e8ee782cec74a
- adapter-stderr-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- verification-status: absent
- verification-evidence-basis: absent

## MSG-10 | 2026-08-24T05:52:24+00:00 | from: owner | type: close | thread: branch-ox-alpha-frontier-3 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
