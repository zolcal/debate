
## MSG-1 | 2026-08-07T03:30:25+00:00 | from: owner | type: review-request | thread: repository-no-op-proof | refs: feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa

# Repository unattended no-op proof

This case proves the operating mechanism against
`feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa`.
It does not authorize code changes.

Each seat independently must:

1. inspect `README.md`, `collab/PROTOCOL.md`, and
   `collab/repository-unattended-02750.debate.json` in its pinned source export;
2. confirm that the selected Opus/Codex pair is local configuration, both seats are
   headless, the supervisor is not a vote, the recorded cap is 12, and alternative model
   pairs remain supported; and
3. run exactly:

   `python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'`

Return `PASS` only when the command passes and the inspected files satisfy all criteria.
Cite the fresh command result in the body. Otherwise return `NO_PASS` with the blocker.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: ad6da34b4fed130f45eb00a12c17ef37369426822e0830ea2d358cc967b65066
- source-ref: e96747f89b87444ec95235f635f964df338760fa
- docket-revision-sha256: 47ca057035b384986a257022ec3c0221620e6f53c5f3d5e54495233969b20475
- docket-files: [{"path": "docs/plans/2026-08-06-unattended-isolated-agent-pairs.md", "sha256": "781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/no-op-docket.md", "sha256": "ecdf25900fe0cfb8bb1d316b54ab9b65076245864f936dc58410d36e39f95041", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "6f30f8969bb72c3192a7855c6a420933850fa0cc7b94389bf313b3eac89281bd", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "0728b4458f164c9857604402f8ddb14d4df3b4b83fba92c2d31801a80fa1c9d4", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/watcher.json", "sha256": "ad6da34b4fed130f45eb00a12c17ef37369426822e0830ea2d358cc967b65066", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "c99e7b2d982e3e85148dc90dc55e69e761f3d99af3aec045b7169db3f33050c6", "opus": "f57d3b02bb841157693532206aa27274fbcc1c07ea1b1bca26f5ad96ad1cfc61"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "9607fa0adba3cfb8a8de731ef097ffe104a50aad0b1decc4f8f4316592a150a4", "opus": "a504f4b71ae7e7a72f9798796377fa1c7722f7d5c6159115d513218a3ef57b67"}

## MSG-2 | 2026-08-07T03:30:40+00:00 | from: owner | type: close | thread: repository-no-op-proof | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-3 | 2026-08-07T03:31:21+00:00 | from: owner | type: review-request | thread: repository-no-op-proof-v2 | refs: feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa

# Repository unattended no-op proof

This case proves the operating mechanism against
`feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa`.
It does not authorize code changes.

Each seat independently must:

1. inspect `README.md`, `collab/PROTOCOL.md`, and
   `collab/repository-unattended-02750.debate.json` in its pinned source export;
2. confirm that the selected Opus/Codex pair is local configuration, both seats are
   headless, the supervisor is not a vote, the recorded cap is 12, and alternative model
   pairs remain supported; and
3. run exactly:

   `python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'`

Return `PASS` only when the command passes and the inspected files satisfy all criteria.
Cite the fresh command result in the body. Otherwise return `NO_PASS` with the blocker.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: ad6da34b4fed130f45eb00a12c17ef37369426822e0830ea2d358cc967b65066
- source-ref: e96747f89b87444ec95235f635f964df338760fa
- docket-revision-sha256: 303d2767c02312d20f3b9559710f81678758f24b123d39fdf0084caf22be8e27
- docket-files: [{"path": "docs/plans/2026-08-06-unattended-isolated-agent-pairs.md", "sha256": "781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/no-op-docket.md", "sha256": "ecdf25900fe0cfb8bb1d316b54ab9b65076245864f936dc58410d36e39f95041", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "4b2827bc2820595ebf2669219c6e591cc661e61ee86fa1da3671f957f0219c19", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "0728b4458f164c9857604402f8ddb14d4df3b4b83fba92c2d31801a80fa1c9d4", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/watcher.json", "sha256": "ad6da34b4fed130f45eb00a12c17ef37369426822e0830ea2d358cc967b65066", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "c99e7b2d982e3e85148dc90dc55e69e761f3d99af3aec045b7169db3f33050c6", "opus": "f57d3b02bb841157693532206aa27274fbcc1c07ea1b1bca26f5ad96ad1cfc61"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "9607fa0adba3cfb8a8de731ef097ffe104a50aad0b1decc4f8f4316592a150a4", "opus": "a504f4b71ae7e7a72f9798796377fa1c7722f7d5c6159115d513218a3ef57b67"}

## MSG-4 | 2026-08-07T03:34:57+00:00 | from: owner | type: close | thread: repository-no-op-proof-v2 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-5 | 2026-08-07T03:36:42+00:00 | from: owner | type: review-request | thread: repository-no-op-proof-v3 | refs: feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa

# Repository unattended no-op proof

This case proves the operating mechanism against
`feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa`.
It does not authorize code changes.

Each seat independently must:

1. inspect `README.md` in the pinned source export and the content-addressed docket copies
   of `collab/PROTOCOL.md` and `collab/repository-unattended-02750.debate.json`;
2. confirm that the selected Opus/Codex pair is local configuration, both seats are
   headless, the supervisor is not a vote, the recorded cap is 12, and alternative model
   pairs remain supported; and
3. run exactly:

   `python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'`

Run that command literally, without prefixes, suffixes, pipes or environment diagnostics.

Return `PASS` only when the command passes and the inspected files satisfy all criteria.
Cite the fresh command result in the body. Otherwise return `NO_PASS` with the blocker.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: bde7467ad748e7a41215a21f8e736ccd8af2b51388de78fbb5b4678eb65b4f4c
- source-ref: e96747f89b87444ec95235f635f964df338760fa
- docket-revision-sha256: 24ad40643a832aefaedc6e2e64f318b71ba0b142b3cde4e97529549182abb8aa
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "677a8103629c15c31a475544759a84062a801395e8b33ed169d8b38466146121", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-06-unattended-isolated-agent-pairs.md", "sha256": "781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/no-op-docket.md", "sha256": "6c934e1ebf324674f29350f2730cb48652631f9eb2ac23c0fc4402894a8293fc", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "853d0e76ccd021908b5798f1960b7c529fbf3951fd03008a939d3ec7a874879e", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/watcher.json", "sha256": "bde7467ad748e7a41215a21f8e736ccd8af2b51388de78fbb5b4678eb65b4f4c", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "9607fa0adba3cfb8a8de731ef097ffe104a50aad0b1decc4f8f4316592a150a4", "opus": "a504f4b71ae7e7a72f9798796377fa1c7722f7d5c6159115d513218a3ef57b67"}

## MSG-6 | 2026-08-07T03:38:32+00:00 | from: owner | type: close | thread: repository-no-op-proof-v3 | refs: -

Controller closed the managed case as ERROR. Reason: adapter-error. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: ERROR
- close-reason: adapter-error

## MSG-7 | 2026-08-07T03:39:08+00:00 | from: owner | type: review-request | thread: repository-no-op-proof-v4 | refs: feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa

# Repository unattended no-op proof

This case proves the operating mechanism against
`feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa`.
It does not authorize code changes.

Each seat independently must:

1. inspect `README.md` in the pinned source export and the content-addressed docket copies
   of `collab/PROTOCOL.md` and `collab/repository-unattended-02750.debate.json`;
2. confirm that the selected Opus/Codex pair is local configuration, both seats are
   headless, the supervisor is not a vote, the recorded cap is 12, and alternative model
   pairs remain supported; and
3. run exactly:

   `python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'`

Run that command literally, without prefixes, suffixes, pipes or environment diagnostics.

Return `PASS` only when the command passes and the inspected files satisfy all criteria.
Cite the fresh command result in the body. Otherwise return `NO_PASS` with the blocker.


Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: bde7467ad748e7a41215a21f8e736ccd8af2b51388de78fbb5b4678eb65b4f4c
- source-ref: e96747f89b87444ec95235f635f964df338760fa
- docket-revision-sha256: 387599b07e8caf5b713d6195069861878a7d761c11691041aac4ac32309a6557
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "677a8103629c15c31a475544759a84062a801395e8b33ed169d8b38466146121", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-06-unattended-isolated-agent-pairs.md", "sha256": "781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/no-op-docket.md", "sha256": "6c934e1ebf324674f29350f2730cb48652631f9eb2ac23c0fc4402894a8293fc", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/watcher.json", "sha256": "bde7467ad748e7a41215a21f8e736ccd8af2b51388de78fbb5b4678eb65b4f4c", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "9607fa0adba3cfb8a8de731ef097ffe104a50aad0b1decc4f8f4316592a150a4", "opus": "a504f4b71ae7e7a72f9798796377fa1c7722f7d5c6159115d513218a3ef57b67"}

## MSG-8 | 2026-08-07T03:41:33+00:00 | from: opus | type: verdict | thread: repository-no-op-proof-v4 | refs: -

PASS — every criterion in `var/debate/repository-unattended-02750/no-op-docket.md` is satisfied by my own inspection of the pinned read-only export at `feature/unattended-slice4@e96747f89b87444ec95235f635f964df338760fa` plus a fresh run of the required command. No source was edited; this case authorizes no code change.

1) Inspection — docket copies and pinned README

- `collab/repository-unattended-02750.debate.json` (docket copy): `"parties": ["opus","codex"]`, `"supervisor": "owner"`, `"thread_cap": 12`, `"managed_version": 2`, `"project": "/home/zoltan/Projects/debate"`.
- `collab/PROTOCOL.md` (docket copy) lines 3-7: the active managed channel's "two controller-bound, headless seats are **opus** and **codex**; **owner** is the human supervisor and is not a vote. This pair is this repository's local choice, not a product default." Section 3 repeats that the supervisor "never fills a party turn and never counts as a vote," and section 4 requires both adapter profiles to be commands ("A commandless seat is invalid; no turn is delegated to an interactive human session"). Section 1 states caps are per-channel and new channels default to 12, matching the persisted 12.
- Cap = 12 is corroborated in two independent docket files: the debate.json above and `var/debate/repository-unattended-02750/watcher.json`'s channel runtime config, whose `adapters.opus` and `adapters.codex` are both non-interactive `/usr/bin/python3 .../seat_adapter.py <party> {input_path} {result_path}` command profiles with `session_persistence: false`, `settings_sources: []`, and `author_relationship: author-independent` — i.e. both seats headless, consistent with the recommended three-agent topology in my seat manifest.
- Pinned export `README.md` lines 170-176: "The model pair is configuration, not policy. ... Another channel can use Opus/GLM, GLM/Kimi, or local models without a code change." Lines 494-506: the historical Opus/GLM record is retired but preserved, the fresh channel "selects headless Opus/Codex only in local config," and a GLM+Kimi pairing or a local open-weight model can hold either seat. README line 167-168 confirms the core never infers topology from model names. Alternative model pairs therefore remain supported.

2) Verification — exact command, run literally with no prefix, suffix, pipe or environment diagnostics, from the pinned export root `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/e96747f89b87444ec95235f635f964df338760fa/opus`:

`python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'`

Result (fresh, my own run):

```
...                                                                      [100%]
3 passed, 40 deselected in 0.99s
```

Three tests ran because `test_sealed_pair_completes_in_either_order_without_cross_anchoring` is parametrized `first_party=["alice","bob"]` (tests/test_controller.py:754-755), plus `test_recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash` (tests/test_controller.py:943). Zero failures, zero errors.

Scope note: I did not independently recompute the docket sha256 digests, because Bash here is restricted to the test-only allowlist (a plain directory listing was denied); the docket does not require that check, and I read the content-addressed docket copies directly under the manifest-pinned docket root. Nothing in the inspected files or command output blocks the no-op proof.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 57830390d63953a4e1de94be8e0247433befdb044d9a504dbc9388757c86cae6
- phase: sealed

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: bde7467ad748e7a41215a21f8e736ccd8af2b51388de78fbb5b4678eb65b4f4c
- source-ref: e96747f89b87444ec95235f635f964df338760fa
- source-manifest-sha256: a504f4b71ae7e7a72f9798796377fa1c7722f7d5c6159115d513218a3ef57b67
- docket-revision-sha256: 387599b07e8caf5b713d6195069861878a7d761c11691041aac4ac32309a6557
- input-sha256: 72d4b1f636f2f1a440374910686913c8aede4a38f649581f1d6c0cb3e01f16d7
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-9 | 2026-08-07T03:41:33+00:00 | from: codex | type: verdict | thread: repository-no-op-proof-v4 | refs: -

Inspected the pinned README and immutable docket copies. They establish the local headless Opus/Codex pair, a non-voting supervisor, thread cap 12, and support for alternative pairs. Fresh command run exactly: `python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'` — result: `3 passed, 40 deselected in 0.98s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 57830390d63953a4e1de94be8e0247433befdb044d9a504dbc9388757c86cae6
- phase: sealed

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: bde7467ad748e7a41215a21f8e736ccd8af2b51388de78fbb5b4678eb65b4f4c
- source-ref: e96747f89b87444ec95235f635f964df338760fa
- source-manifest-sha256: 9607fa0adba3cfb8a8de731ef097ffe104a50aad0b1decc4f8f4316592a150a4
- docket-revision-sha256: 387599b07e8caf5b713d6195069861878a7d761c11691041aac4ac32309a6557
- input-sha256: 4b9145dc5f84468017892b1642bbea462e0636d62face6dcefb9174d4c80f3e2
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-10 | 2026-08-07T03:41:33+00:00 | from: owner | type: close | thread: repository-no-op-proof-v4 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
