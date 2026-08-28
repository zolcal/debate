
## MSG-1 | 2026-08-27T22:11:38+00:00 | from: owner | type: review-request | thread: release-v080-r3 | refs: main@3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9

Release re-gate for the v0.8.0 tag: the artifact is the pinned export at
main@3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9. Gate r2 (release-gate-v080-r2-97203) cleared the engine, test
suite, packaging, manifests and break-attempt surface on both seats' own
fresh evidence, and closed NO_PASS on exactly two CHANGELOG.md defects:

F1 the Ox Alpha bullet carried a severed sentence (a historical-note
   parenthetical inserted mid-sentence orphaned 'to attention and blocks
   a product open');
F2 the v0.8.0 notes headlined 'Result schema v2' while every new product
   verdict ships schema v3 (opening.py pins version 3; README says v3).

Both are claimed fixed at this revision, and the docs-consistency test now
asserts 'result schema v3' in README and CHANGELOG individually.

Verify with your own fresh evidence from the export:
1. The two fixes: read the CHANGELOG v0.8.0 section end to end - every
   sentence complete, the schema story consistent with code and README,
   and no NEW defect introduced by the edits (this is the text release.yml
   publishes verbatim and the sdist freezes).
2. Suite: run exactly
   PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q
   from the export root and quote the result line.
3. Anything else your own judgment flags as release-blocking - name every
   blocking finding, not the first.

Verdicts cite your own runs, never this request. NO_PASS requires a
reproducing command per blocking finding.


Controller-Docket-Provenance:
- topology: minimum-two-agent
- controller-config-sha256: 58b52432a80426c2f06ec72808ad2c48ad17f06eb07b0bd4d0bb18c31281cbea
- source-ref: 3ed2b847c882b9ce6a93a72dd3e46aa66e2dc9e9
- review-contract: {"goal": "Establish whether the pinned v0.8.0 source tree is release-ready for the tag.", "review_contract_basis": "recorded", "review_domain": "The complete pinned export at the source ref. Gate r2 (97203) cleared code, tests, packaging and manifests and blocked only on two CHANGELOG defects (severed Ox sentence; schema v2 headline vs shipped v3); both are claimed fixed at this revision. Verify the two fixes and the release documents; re-verify the rest only as far as your own judgment requires.", "review_mode": "release-gate", "stop_rule": "PASS only if your own fresh suite run is green and you find no release-blocking defect; otherwise NO_PASS with bounded actionable findings. Stop at terminal agreement or the cap."}
- docket-revision-sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
- docket-files: []
- profile-sha256: {"claude": "6af59ffa6836068be28da4ff1da1497ee538f2b4299df24f46681a7ef165f382", "codex": "3f80295895c14b09b3cfcac382e09020ba0577ac4f6b6c9e4dbfb0b9874fdcfb"}
- sanitized-profile-manifests: {"claude": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-affiliated", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "073d42803d02867af7035116021655b266a4d8c945ce40749b52ce78e531f527", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "claude", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "claude", "reasoning_effort": "default", "requested_model": "opus", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}, "codex": {"authentication_mode": "the tool authenticates itself through its own configuration folder; Debate handles no credentials", "author_relationship": "author-independent", "cli_version": "registry seat (debate 0.8.0); model identity declared by the registry", "command_sha256": "f7354001b14cdbb8d61dc18f315b5086bbe08d0e675d9c82e0e00ce1f0e1d47a", "cost_mode": "subscription", "environment_additions": {"DEBATE_BRIDGE_REAL_HOME": "95bf93cd6ea0a43c135976131340c3be6404ddfe172d04e9154cd5eb9af3b8ec", "PYTHONPATH": "cfea1a5c2411b7fe3c24f918e516f0567e8263ee7a1bfdd4f57a5de90d23fec0"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": null, "isolation_mode": "advisory", "party": "codex", "permission_policy": "controller-bound invocation from a pinned read-only source export; the tool's own settings, plugins and session saving are turned off", "provider": "codex", "reasoning_effort": "default", "requested_model": "gpt-5.6-sol", "result_schema_version": 3, "retry_limit": 1, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 1200}}
- source-manifest-sha256: {"claude": "a1d358f3a5c7b49c68a0380fc2be77b14c700242218085172cc5857f0355d428", "codex": "2deaf0d5bff33a527c128c46fb8766cc8ef450ed00c269410d36ff76a34822ff"}

## MSG-2 | 2026-08-27T22:25:32+00:00 | from: owner | type: close | thread: release-v080-r3 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes. Observed failure: refused: adapter 'claude' exited 2; see /home/zoltan/Projects/debate/.debate/runtime/release-gate-v080-r3-67604/cases/release-v080-r3/invocations/1-claude-1/stderr.txt Runtime size at close: 68412780 logical bytes. Inspect retained and regenerable state with: debate runtime --root /home/zoltan/Projects/debate/collab --channel release-gate-v080-r3-67604 --config /home/zoltan/Projects/debate/.debate/channels/release-gate-v080-r3-67604/watcher.json

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error
