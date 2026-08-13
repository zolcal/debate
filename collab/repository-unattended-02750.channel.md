
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

## MSG-11 | 2026-08-07T03:44:55+00:00 | from: owner | type: review-request | thread: repository-no-op-proof-final | refs: feature/unattended-slice4@1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c

# Repository unattended no-op proof

This case proves the operating mechanism against
`feature/unattended-slice4@1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c`.
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
- controller-config-sha256: acac327886a3df3d8e70bc3e5bf3c413b33754fb12ada80260488c9463210ec4
- source-ref: 1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c
- docket-revision-sha256: 3c823210957d37b5d198e724b9dc901553aadada3406e25d06137420854384bc
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-06-unattended-isolated-agent-pairs.md", "sha256": "781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/no-op-docket.md", "sha256": "721d0fb882cf9d6fdbad92e09754b6681e1a1eac44067c707e049e798fb17ae1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/watcher.json", "sha256": "acac327886a3df3d8e70bc3e5bf3c413b33754fb12ada80260488c9463210ec4", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "79c3090aa197cf8f3848590b0354d84fef7a77b365ecf96c1dc6b420d6460361", "opus": "034f4392d50c69a6795e38458dec1fa434caec3bc66a1d8549bc3f0f82a011d9"}

## MSG-12 | 2026-08-07T03:47:31+00:00 | from: opus | type: verdict | thread: repository-no-op-proof-final | refs: -

PASS — independent inspection of the pinned export plus a fresh run of the docket command satisfies every criterion.

Command run literally from the export root `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c/opus`, with no prefix, suffix, pipe or environment diagnostic:

`python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'`

Result:
```
...                                                                      [100%]
3 passed, 40 deselected in 0.86s
```
The count of 3 is consistent with the selection: `tests/test_controller.py:755 test_sealed_pair_completes_in_either_order_without_cross_anchoring` is `@pytest.mark.parametrize("first_party", ["alice", "bob"])` (line 754), giving two cases, plus `tests/test_controller.py:952 test_recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash`. Both named tests ran and passed; nothing failed, errored, or was skipped.

Criterion 2, from the content-addressed docket copies and the pinned `README.md`:

1. Opus/Codex is local configuration, not a product default. Docket `collab/repository-unattended-02750.debate.json` records `"parties": ["opus", "codex"]`, `"managed_version": 2`, `"project": "/home/zoltan/Projects/debate"`. Docket `collab/PROTOCOL.md:3-7` states the seats are opus and codex and that "This pair is this repository's local choice, not a product default." Export `README.md:499` independently says the `repository-unattended-02750` channel "selects headless Opus/Codex only in local config".
2. Both seats are headless. `PROTOCOL.md:3-4` ("two controller-bound, headless seats"); `PROTOCOL.md:89-91` requires both adapter profiles to be commands, "A commandless seat is invalid; no turn is delegated to an interactive human session"; `README.md:417` ("both parties have headless commands").
3. The supervisor is not a vote. `debate.json` records `"supervisor": "owner"`; `PROTOCOL.md:4-5` ("owner is the human supervisor and is not a vote") and `:62-64` ("The supervisor may add context but never fills a party turn and never counts as a vote"); `README.md:219-220` ("A supervisor verdict is visible context but never a vote").
4. The recorded cap is 12. `debate.json` `"thread_cap": 12`. `PROTOCOL.md:26-30` confirms the cap is per-channel, read from `<id>.debate.json`, with 12 the new-channel default and cap exhaustion closing typed `NO_PASS` in a brokered v2 case; `README.md:106` matches.
5. Alternative model pairs remain supported. `README.md:170-176`: "The model pair is configuration, not policy… Another channel can use Opus/GLM, GLM/Kimi, or local models without a code change," and `:167-168` "The core never infers either topology from names such as Opus, Codex, GLM or Kimi." `README.md:504-507` adds the GLM+Kimi example and local open-weight seats. `PROTOCOL.md:70-74` records the recommended three-agent topology for this proof while keeping the minimum two-agent topology valid, with topology set by profile fields rather than names.

Consistent with the no-op docket, I made no edits to the read-only export, read no live channel state or parent runtime, and used no `/tmp` path.

Scope note (non-blocking): shell access to the docket directory was denied by this seat's permission mode, so I could not run `sha256sum` over the docket copies; I inspected those files through read-only file reads at the docket path given in my manifest. Independent hash re-verification of the docket is not among the docket's stated criteria, and the file contents I read satisfy criteria 1 and 2 on their own.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 97d518a29d3b63b48c46b0f1d861375d866764bbf454fb38c9fea6249be6b2df
- phase: sealed
- captured-at: 2026-08-07T03:46:28+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: acac327886a3df3d8e70bc3e5bf3c413b33754fb12ada80260488c9463210ec4
- source-ref: 1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c
- source-manifest-sha256: 034f4392d50c69a6795e38458dec1fa434caec3bc66a1d8549bc3f0f82a011d9
- docket-revision-sha256: 3c823210957d37b5d198e724b9dc901553aadada3406e25d06137420854384bc
- input-sha256: c24ef627eb6877570d52bd2d9a06c7b0b797339320e15618a91623114c521602
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-13 | 2026-08-07T03:47:31+00:00 | from: codex | type: verdict | thread: repository-no-op-proof-final | refs: -

Inspected the pinned README and content-addressed protocol/config copies (their recorded SHA-256 values matched). They confirm the local headless Opus/Codex pair, owner as non-voting supervisor, thread cap 12, and configurable alternative pairs. Fresh command: `python -m pytest -q tests/test_controller.py -k 'sealed_pair_completes_in_either_order_without_cross_anchoring or recurring_tick_repairs_typed_close_after_mailbox_before_signal_crash'` → `3 passed, 40 deselected in 0.92s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 97d518a29d3b63b48c46b0f1d861375d866764bbf454fb38c9fea6249be6b2df
- phase: sealed
- captured-at: 2026-08-07T03:47:31+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: acac327886a3df3d8e70bc3e5bf3c413b33754fb12ada80260488c9463210ec4
- source-ref: 1cf9cfbf5cd6b2f8f1efc1f4dd03ffb1c678bc0c
- source-manifest-sha256: 79c3090aa197cf8f3848590b0354d84fef7a77b365ecf96c1dc6b420d6460361
- docket-revision-sha256: 3c823210957d37b5d198e724b9dc901553aadada3406e25d06137420854384bc
- input-sha256: 53f14a93ab6ae93763ccda2201d36af59a0b39998dc130fb454a86021a26cebf
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-14 | 2026-08-07T03:47:31+00:00 | from: owner | type: close | thread: repository-no-op-proof-final | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-15 | 2026-08-07T05:43:59+00:00 | from: owner | type: review-request | thread: slice4-amendment-84b1afd | refs: feature/unattended-slice4@84b1afdbe70a47d868477889b8f5ea3e175cbfb0

Branch-gate amendment review: 6c0932c..84b1afd on feature/unattended-slice4 (PR #5). The approved Slice 4 base gained two CI-forced fix commits (strict-mypy types; Windows brokered-subprocess environment baseline). Docket file amendment-docket.md states the criteria; amendment.diff is the exact diff under review. Seats verify independently from the pinned read-only export at 84b1afd.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: bbe1cba8edd451546e8eb470f4fccb10f78935fad2ad2dccdce4d6b3b62b893a
- source-ref: 84b1afdbe70a47d868477889b8f5ea3e175cbfb0
- docket-revision-sha256: 96e6c7b0a9171afb7c904d5a29789dca75068a85704f6da72b7ea4653a6a4145
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-06-unattended-isolated-agent-pairs.md", "sha256": "781def93bc2a2ea57336c11c3e34b13fd36786375bf76533ef427038390ab6b9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/amendment-docket.md", "sha256": "f3ca457fe4f64495584eaef3c1908537d74b814a9ec072c78fa512b931d55720", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/amendment.diff", "sha256": "19ff8bf42dc6e94c76ffeb9dab2bd007f28a5e36faf77b612c8274f0e0da917c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/amendment-watcher.json", "sha256": "bbe1cba8edd451546e8eb470f4fccb10f78935fad2ad2dccdce4d6b3b62b893a", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "822fa91a56590b21bca8405ddcc5f5de6114e6e90c5627ef60f71cdda14a8211", "opus": "193b03b69d2627716d740160227b7baa00a237e8bc0b3f6d745d218312d9ba5f"}

## MSG-16 | 2026-08-07T05:47:37+00:00 | from: opus | type: verdict | thread: slice4-amendment-84b1afd | refs: -

## Verification

**Command run (exactly as docketed, in the pinned export root `.../exports/84b1afdbe70a47d868477889b8f5ea3e175cbfb0/opus`):**

`python -m pytest -q`

**Result:**

```
........................................................................ [ 18%]
........................................................................ [ 36%]
........................................................................ [ 54%]
......................................................s................. [ 72%]
........................................................................ [ 91%]
...................................                                      [100%]
394 passed, 1 skipped in 17.25s
```

Exit status clean; no prefixes, suffixes, pipes or env diagnostics were attached to the command. The suite includes the amended `test_source_export_is_complete_except_separated_state_and_git_is_unreachable`, which itself re-runs `pytest -q` inside the export under the hand-built probe env, so the amended baseline-env path is exercised, not just imported.

## Hunk-by-hunk check of `amendment.diff` against the export

All seven hunks are present in the export in their post-amendment final state; each was read in place, not just from the diff.

1. `pyproject.toml:62` — `exclude = ["^build/", "^var/"]`. Regex is anchored at the relative-path root, so it hides only the broker runtime tree; `src/` and `tests/` remain in `mypy .`'s scope. Config-only, no runtime effect.
2. `controller.py:463-465` (`_git`) — `stdout: bytes | str = proc.stdout; return stdout`. Pure annotation widening to the declared return type; identical object returned. No behavior change.
3. `controller.py:668-682` — `_WINDOWS_BASELINE_ENVIRONMENT` / `_baseline_environment()`. Returns `{}` when `os.name != "nt"`, so POSIX behavior is byte-for-byte unchanged (which is why this hunk is inert under the run above and rests on inspection). The five keys (`SYSTEMROOT`, `SYSTEMDRIVE`, `COMSPEC`, `PATHEXT`, `WINDIR`) are OS-installation paths and command-resolution settings; none is an agent/tool/user-config variable, none appears in `_RESERVED_ENV` (`controller.py:38-58`), and none can smuggle credentials, HOME-rooted config, or `GIT_CONFIG_*` policy into the subprocess. The slice-2 isolation claim holds.
4. `controller.py:683-685` (`_adapter_environment`) — baseline is seeded *first*, then `.update()` with the allowlist, then `profile.environment`, then the controller-owned block (`HOME`, `XDG_*`, `TMPDIR`/`TEMP`/`TMP`, `GIT_CEILING_DIRECTORIES`, …). Precedence among the pre-existing layers is unchanged and the baseline sits at the bottom, so it can never override a controller-owned or allowlisted value.
5. `controller.py:1280` (`_recorded_result`) — `evidence: dict[str, str | Path]` annotation only; the comprehension still stringifies every value.
6. `controller.py:1295-1298`, `1323-1326`, `1777-1780` — three `isinstance(..., dict)` guards on `sealed_submissions` / `latest_votes` replacing what was previously an incidental `TypeError` from `dict(non_mapping)`. These are fail-closed and consistent with the module's `refused: …` `ChannelError` convention; on well-formed state the code path is identical. This matches the described scope exactly — no other control flow moved.
7. `watcher.py:801-820` — hoists `broker = config.broker` and adds a redundant `and broker is not None` at the `if`. `maybe_broker_commit` already required `broker is not None` and nothing between the two statements mutates it, so the added conjunct is a narrowing aid with no reachable behavior change; `BrokerController(broker)` receives the same object as `BrokerController(config.broker)`.
8. `tests/test_controller.py:478` and `tests/test_watch_status.py:11,297-300` — the probe env gains the same baseline (needed for the nested Windows `sys.executable` launch), and the watcher config fixture is built with `json.dumps` instead of concatenation. The `json.dumps` form is strictly more correct: a Windows `tmp_path` backslash previously produced invalid JSON escapes. On POSIX both forms yield equivalent JSON, so the assertions under test are unchanged.

## Non-blocking observation

`COMSPEC` and `PATHEXT` are, strictly speaking, overridable in a Windows per-user environment block, unlike the purely machine-owned `SYSTEMROOT`/`SYSTEMDRIVE`/`WINDIR`. The values that could pass through are command-resolution settings, not agent or credential configuration, and they cannot reach `_RESERVED_ENV` territory, so I do not read this as weakening the isolation claim. Flagging it only so the record shows the distinction was considered rather than assumed.

Both docket criteria are satisfied: the command passes fresh, and every hunk is correct with no behavior change beyond the described fail-closed guards.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3a4ff37a4b4c59829fdbe8592c9e071a5f5f29b4ae2d50300e16d716e2166879
- phase: sealed
- captured-at: 2026-08-07T05:46:09+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: bbe1cba8edd451546e8eb470f4fccb10f78935fad2ad2dccdce4d6b3b62b893a
- source-ref: 84b1afdbe70a47d868477889b8f5ea3e175cbfb0
- source-manifest-sha256: 193b03b69d2627716d740160227b7baa00a237e8bc0b3f6d745d218312d9ba5f
- docket-revision-sha256: 96e6c7b0a9171afb7c904d5a29789dca75068a85704f6da72b7ea4653a6a4145
- input-sha256: be9914f09453024a263df86b37185e92417d3b3a04ef9c66b8fff5c5ccbb11fe
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-17 | 2026-08-07T05:47:37+00:00 | from: codex | type: verdict | thread: slice4-amendment-84b1afd | refs: -

Inspected every amendment hunk against the pinned export. The Windows baseline is limited to the five stated machine environment keys and is empty on POSIX; the remaining changes are typing, fail-closed malformed-state guards, and Windows-safe test fixture/probe updates. Fresh verification command: `python -m pytest -q` — result: `394 passed, 1 skipped in 18.03s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3a4ff37a4b4c59829fdbe8592c9e071a5f5f29b4ae2d50300e16d716e2166879
- phase: sealed
- captured-at: 2026-08-07T05:47:37+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: bbe1cba8edd451546e8eb470f4fccb10f78935fad2ad2dccdce4d6b3b62b893a
- source-ref: 84b1afdbe70a47d868477889b8f5ea3e175cbfb0
- source-manifest-sha256: 822fa91a56590b21bca8405ddcc5f5de6114e6e90c5627ef60f71cdda14a8211
- docket-revision-sha256: 96e6c7b0a9171afb7c904d5a29789dca75068a85704f6da72b7ea4653a6a4145
- input-sha256: bc679586e604e1553ae1daaaa3cb24e03c7452bd81e3840241722fb636b05d89
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-18 | 2026-08-07T05:47:37+00:00 | from: owner | type: close | thread: slice4-amendment-84b1afd | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-19 | 2026-08-07T07:00:22+00:00 | from: owner | type: review-request | thread: plan-v050-release | refs: main@5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae

Plan-doc gate: the v0.5.0 release plan (docs/plans/2026-08-07-v0.5.0-release.md, materialized in the docket by content hash) reviewed against main@5f3baed before any execution. Criteria in plan-v050-docket.md: staleness claims accurate, procedure matches release.yml, nothing release-blocking missing, tamper-evident/advisory language rules kept.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c
- source-ref: 5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae
- docket-revision-sha256: eec11ba2ea789da89f999a74ec04a5a57499ad81924217067917cb7bab0caf19
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-07-v0.5.0-release.md", "sha256": "f3185b1e5a6c5adf9f1a4d42fb4400992f5971366600c490642c53751763d006", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v050-docket.md", "sha256": "884ba05c235dedd301131ecedddfad28c72a6760d8ad501a01e9cab2f6d823ed", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v050-watcher.json", "sha256": "db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "0aea96b4bc8197010619a075d72c5b4385f2c4e26b2d3b86646f2bf159d6765e", "opus": "ef41959f126616d1440a0394d138ed73807a4360b397eb65fbb4ed9800731cfa"}

## MSG-20 | 2026-08-07T07:08:00+00:00 | from: opus | type: verdict | thread: plan-v050-release | refs: -

## Verification command (fresh, run literally in the pinned export root)

`python -m pytest -q tests/test_release_sync.py`

```
.                                                                        [100%]
1 passed in 0.07s
```

Run from `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae/opus` with the seat's `PYTHONPATH=src`. No prefix, suffix, pipe or diagnostics. The command passes, so criterion 3 holds — but criterion 1 does not, so the verdict is NO_PASS.

## Blocking finding — a stale public claim the plan's sweep will not catch

The repository's own record-provenance claim is stale at the pinned ref, is republished by this release, and sits outside every fix the plan lists.

- `README.md:500-503` (export): "Its record includes the repository's own end-to-end sealed/reveal/automatic-close proof. **The final proof is MSG-11..14**: independent Opus and Codex capture timestamps, one paired reveal, and automatic `PASS`…"
- `CHANGELOG.md:54-57` (export, inside `## Unreleased`): "The repository's **final brokered proof (MSG-11..14)** records separate initial-capture timestamps, atomically reveals both independently gathered positions, and closes `PASS` automatically."

By the plan's own facts, MSG-11..14 is no longer final: step 6 states "the machinery's first production act was gating this repo's own merge (**channel record MSG-15..18**)" and step 9 refers to that record chore commit "as done for MSG-15..18 today"; step 8 then opens a further brokered case whose terminal `PASS` gates this very release. Plan step 4's README work is scoped to the versions block, the 0.3.x upgrade line, the counts line, the diagram embed, and a grep-sweep for `0.3.1`, counts, and "in 0.5" — none of those terms match `MSG-11..14`. Plan step 3 restructures the `### Changed` list into Added/Changed and adds Fixed/Deprecated, but never flags this line.

Why release-blocking rather than cosmetic: the `## Unreleased` block becomes the `## v0.5.0` section verbatim, and `.github/workflows/release.yml:97-117` sources the GitHub Release body from exactly that section while `publish` (lines 55-79) uploads the README-bearing sdist/wheel to PyPI — an upload the workflow's own comment at lines 52-54 calls undoable, "only yanked". A wrong claim about the audit record is precisely the class of error this project's record machinery exists to prevent, published irreversibly. Fix: correct or drop "final" in both places and extend the step 4 sweep to `MSG-` alongside `0.3.1` / counts / "in 0.5".

## Secondary finding (not blocking on its own)

Plan step 6 promises an epilogue mapping "the three same-night amendments" to v0.5 machinery, but the three amendments in `docs/case-study.md:73-83` are (1) Git-verified claims, (2) Shared-checkout discipline, (3) Corrections are entries. The plan maps 2 and 3, silently drops 1, and adds two items that are not amendments: "the live session watches the doorbell" is from the scoreboard's what-it-got-wrong column (`docs/case-study.md:104`), and "anchoring risk" appears nowhere in the article. The epilogue as specified would misdescribe the article it appends to.

## What checked out

- **Version lockstep.** Exactly four `0.4.0` version strings exist, at exactly the lines cited in step 2: `pyproject.toml:7`, `src/debate/__init__.py:42`, `.claude-plugin/plugin.json:3`, `.claude-plugin/marketplace.json:9`. `tests/test_release_sync.py:11-23` asserts those same four and nothing else.
- **README staleness claims accurate.** The "Note on versions" block is at `README.md:96-99` exactly as cited; the due 0.5 forward reference is at `README.md:380` ("supported in 0.4 and becomes a documented deprecation in 0.5"); the counts claim is at `README.md:463-464` ("about 2,300 lines … with 320 tests"). `wc -l src/debate/*.py` totals 4943, so the plan's "~4,900 lines incl. the broker" is sound; the 395 test-item figure is explicitly deferred to a recount at commit time.
- **CHANGELOG state accurate.** `CHANGELOG.md:9-11` is `## Unreleased` over a single flat `### Changed` list, as described. The proposed heading `## v0.5.0 — 2026-08-07` matches the workflow anchor `^## v0\.5\.0(?=[ \t]|$)` at `release.yml:73` and `:106`.
- **Case-study staleness accurate.** A case-insensitive search of `docs/case-study.md` for `controller|broker|v0.5|sealed|export` returns no matches — the shipped machinery is genuinely unmentioned.
- **Diagram assets.** `docs/assets/` holds `flow-light.svg`/`flow-dark.svg` and no broker pair, so step 5 creates rather than overwrites; `flow-*.svg` untouched as stated. The embed target "Brokered managed version 2" exists at `README.md:134`.
- **Release procedure matches the shipped workflow.** `release.yml:19-35` is a 4-lane gate (ubuntu/windows × 3.10/3.12) running ruff, strict mypy and pytest; `:55-76` refuses on tag≠pyproject≠`__version__` or a missing/empty CHANGELOG section *before* build and upload; `:87-117` creates the GitHub Release from that section. Step 10's description is faithful.
- **Criterion 2 holds.** Step 3 carries the explicit rule `"tamper-evident", never "unforgeable"`, and step 6 closes with isolation as advisory, "anti-accident, not hostile-code proof". A repo-wide search finds zero occurrences of "unforgeable"; the existing language at `README.md:238-244`, `README.md:454-457`, `CHANGELOG.md:144-145` and `collab/PROTOCOL.md:113-115` is preserved, not weakened.

Isolation note: the export contains no `collab/` directory, so no live channel was read and no contamination canary was encountered; the MSG-15..18 facts above are taken from the docket and the plan document, not from the record.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: e5dc6173a7fa2a09faeb5ebe3e00659ff86188f23a3c09043b6421afa9343b9f
- phase: sealed
- captured-at: 2026-08-07T07:08:00+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c
- source-ref: 5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae
- source-manifest-sha256: ef41959f126616d1440a0394d138ed73807a4360b397eb65fbb4ed9800731cfa
- docket-revision-sha256: eec11ba2ea789da89f999a74ec04a5a57499ad81924217067917cb7bab0caf19
- input-sha256: ea0932aef3841a066b25bc16d895c01c6c3aa7fb8b9d27f3f175aa78411f3832
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-21 | 2026-08-07T07:08:00+00:00 | from: codex | type: verdict | thread: plan-v050-release | refs: -

Blocking: the plan at /home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/dockets/eec11ba2ea789da89f999a74ec04a5a57499ad81924217067917cb7bab0caf19/files/docs/plans/2026-08-07-v0.5.0-release.md starts DRAFT but defers changing it to APPROVED until step 11, after branch execution, merge, tag, and publish. The plan gate must be recorded before step 1, so this ordering permits execution of an unapproved plan. I checked the pinned /home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae/codex/README.md, CHANGELOG.md, docs/case-study.md, and .github/workflows/release.yml: the cited stale README claims and four-version lockstep are present, the workflow has the stated four-lane gate and pre-upload version/notes checks, and the plan uses tamper-evident and advisory/non-hostile-code-safe language. Fresh verification run exactly: `python -m pytest -q tests/test_release_sync.py` => `1 passed in 0.08s`.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: e5dc6173a7fa2a09faeb5ebe3e00659ff86188f23a3c09043b6421afa9343b9f
- phase: sealed
- captured-at: 2026-08-07T07:03:33+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c
- source-ref: 5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae
- source-manifest-sha256: 0aea96b4bc8197010619a075d72c5b4385f2c4e26b2d3b86646f2bf159d6765e
- docket-revision-sha256: eec11ba2ea789da89f999a74ec04a5a57499ad81924217067917cb7bab0caf19
- input-sha256: a2753c7b73f465bb12e3948aafe7b68edc80081f4c784d35157a45199b0c1491
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-22 | 2026-08-07T07:08:00+00:00 | from: owner | type: close | thread: plan-v050-release | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-23 | 2026-08-07T07:09:44+00:00 | from: owner | type: review-request | thread: plan-v050-release-r2 | refs: main@5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae

Plan-doc gate round 2: the v0.5.0 release plan with the three MSG-19..22 NO_PASS findings folded (stale MSG-11..14 'final proof' claim now a fix item + MSG- sweep; APPROVED-header flip moved to step 0 before execution; epilogue remapped to the article's actual three amendments). Docket summarizes round 1; criteria otherwise unchanged.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c
- source-ref: 5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae
- docket-revision-sha256: e3350d8d7a70babd776e1e7d131f224768cb8ba592bb0b1a3852540dddfa3ba6
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-07-v0.5.0-release.md", "sha256": "bf4b97ef37fede9f4a23cf2c86c8e9720caa171de596d695a1a86659162276e6", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v050-docket.md", "sha256": "5433193b7214e9588bf57bcd5eee821bfa436fb5291cd0a6bff9e25dde6e8ed9", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v050-watcher.json", "sha256": "db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "0aea96b4bc8197010619a075d72c5b4385f2c4e26b2d3b86646f2bf159d6765e", "opus": "ef41959f126616d1440a0394d138ed73807a4360b397eb65fbb4ed9800731cfa"}

## MSG-24 | 2026-08-07T07:16:16+00:00 | from: opus | type: verdict | thread: plan-v050-release-r2 | refs: -

## Verification command (fresh, run literally in the pinned export root)

`python -m pytest -q tests/test_release_sync.py`

Result:

```
.                                                                        [100%]
1 passed in 0.07s
```

Run from `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae/opus`, no prefix/suffix/pipe/env diagnostics.

## Criterion 1 — staleness claims, procedure fidelity, release-blocking gaps

Every staleness claim the plan makes is accurate against the pinned export at the cited location:

- `README.md:96-99` — the "Note on versions" block does say "The released package on PyPI is `0.3.1`" and names `debate migrate` / `debate verify` / `debate watch-status` as main-only. Plan step 4 deletes it; correct, since the release publishes them.
- `README.md:380` — "remains supported in 0.4 and becomes a documented deprecation in 0.5". The forward reference is genuinely due, and `CHANGELOG.md:139-140` carries the matching promise, which substantiates the plan's "owed by the v0.4 notes" `### Deprecated` item (step 3).
- `README.md:463` — "about 2,300 lines including the CLI, with 320 tests". Stale as claimed; the plan recounts at commit time rather than hard-coding, which is the right handling.
- `README.md:501` — "The final proof is MSG-11..14" exists verbatim; `CHANGELOG.md:54` carries the parallel "The repository's final brokered proof (MSG-11..14)". Both are covered by the plan's explicit fix items.
- `CHANGELOG.md:9-57` — the feature list does sit under `## Unreleased` as a flat `### Changed`; the restructure/dating item is warranted.
- Version strings all still read `0.4.0` at exactly the four cited lines: `pyproject.toml:7`, `src/debate/__init__.py:42`, `.claude-plugin/plugin.json:3`, `.claude-plugin/marketplace.json:9` — the same four locations `tests/test_release_sync.py:11-23` asserts, so step 2 and the lockstep test line up exactly.
- `docs/case-study.md:73-83` — exactly three amendments at those lines (git-verified claims, shared-checkout discipline, corrections are entries), matching the epilogue's mapping.

Procedure matches `.github/workflows/release.yml` as shipped: the `gate` job is a 2 OS × 2 Python matrix = the "4-lane gate" the plan claims (`release.yml:19-35`); the preflight asserts `tag == pyproject version == debate.__version__` and requires a non-empty CHANGELOG section *before* `python -m build` and the PyPI upload (`release.yml:55-79`); `github-release` sources notes from that same section (`release.yml:87-117`). The plan's proposed heading `## v0.5.0 — 2026-08-07` satisfies the workflow's `^## <tag>(?=[ \t]|$)` anchor (`release.yml:73`, `:106`). `.github/workflows/ci.yml:14-30` confirms the PR's "4 gate lanes" with the identical ruff/mypy/pytest steps the plan replicates locally in step 7.

No release-blocking gap found. Step ordering does not strand the release: the only irreversible act (PyPI upload) sits behind a preflight that refuses on version or notes mismatch, and it is preceded by a local gauntlet, a debate branch gate requiring terminal `PASS`, and 4 green PR lanes. The MSG-numbered wording is written generically ("MSG-15 onward"), so the step 9 record chore commit landing after the merge cannot make the published text false. I checked the remaining `0.3.1` / `0.4` / `MSG-` hits across the export: `examples/glm-kimi.md:94` ("debate >= 0.3.1"), `.gitignore:16`, `README.md:273,369,498`, `docs/case-study.md:16` and the `CHANGELOG.md` v0.4.0/v0.3.1 sections are accurate historical or minimum-version statements, not stale claims; `README.md:72-83` is an illustrative transcript, not a record claim.

## Criterion 2 — recorded language rules

Kept. The plan states the rule explicitly ("Language rule: 'tamper-evident', never 'unforgeable'", step 3) and closes the epilogue with "isolation is advisory (anti-accident, not hostile-code proof)" (step 6). Nothing in the plan text — including the step 5 SVG spec — asserts unforgeability or hostile-code safety. This matches the export (`README.md:454` "tamper-evident, not tamper-proof"; `CHANGELOG.md:111`) and the docket's `collab/PROTOCOL.md:113-115` ("`isolation_mode: advisory` … contamination resistance, not hostile-code"). A repository-wide case-insensitive search for "unforgeable" returned no hits.

## Round-1 folds

(a) Resolved — both stale "final proof" sites exist exactly as the fold describes (`README.md:501`, `CHANGELOG.md:54`) and each is now a named fix item, with `MSG-` added to the sweep. (b) Resolved — step 0 flips the header to `Status: APPROVED (MSG-n)` on gate PASS and states no execution step runs before the flip; step 1 is the first execution step. (c) Resolved — the epilogue maps the three real amendments at `docs/case-study.md:73-83` and separately handles the scoreboard's "norm with no mechanism" (`docs/case-study.md:104`) and the new sealed-paired-reveal machinery, no longer calling non-amendments amendments. The separate "`close` clears the turn field" change at `docs/case-study.md:88` is correctly not counted among the three.

Non-blocking observation: `docs/assets/flow-light.svg` and `flow-dark.svg` are both 5550 bytes, consistent with the plan's "dark = color-swapped" model but worth a glance when authoring the broker pair.

Decision: PASS.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 885b7575cdf2384d3cc909ca294bad4f349db91861ff3911982dde3a187930d7
- phase: sealed
- captured-at: 2026-08-07T07:12:53+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c
- source-ref: 5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae
- source-manifest-sha256: ef41959f126616d1440a0394d138ed73807a4360b397eb65fbb4ed9800731cfa
- docket-revision-sha256: e3350d8d7a70babd776e1e7d131f224768cb8ba592bb0b1a3852540dddfa3ba6
- input-sha256: 6aad8a21d90dbfba647ad6187f04f29eb7658866c1a8e09de645ef8d3252145b
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-25 | 2026-08-07T07:16:16+00:00 | from: codex | type: verdict | thread: plan-v050-release-r2 | refs: -

Inspected the immutable plan and pinned export: README.md, CHANGELOG.md, docs/case-study.md, PROTOCOL.md, .github/workflows/release.yml, the four version sources, and tests/test_release_sync.py. The stated staleness, release preflight/gate sequence, tamper-evident wording, and advisory (not hostile-code-safe) isolation all match the export. Fresh command run exactly: `python -m pytest -q tests/test_release_sync.py` → `1 passed in 0.07s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 885b7575cdf2384d3cc909ca294bad4f349db91861ff3911982dde3a187930d7
- phase: sealed
- captured-at: 2026-08-07T07:16:16+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: db5575ff8e2dcac2cc5e5230b9519eabab5031bbbfe2626fb008365e7de9521c
- source-ref: 5f3baedc3f5be30cfb62e7837f3a1acdaf1f8dae
- source-manifest-sha256: 0aea96b4bc8197010619a075d72c5b4385f2c4e26b2d3b86646f2bf159d6765e
- docket-revision-sha256: e3350d8d7a70babd776e1e7d131f224768cb8ba592bb0b1a3852540dddfa3ba6
- input-sha256: ccd2abeca8289f8c6b535c168aa3eb813489183c2162e7b40c9fc3ebd876c11d
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-26 | 2026-08-07T07:16:16+00:00 | from: owner | type: close | thread: plan-v050-release-r2 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-27 | 2026-08-07T14:20:20+00:00 | from: owner | type: review-request | thread: release-v050-branch | refs: release/v0.5.0@89fb3aab2d386a9fbbe05675ad3b93f97e474b78

Branch gate for the v0.5.0 release: release/v0.5.0@89fb3aa, one commit past main@5f3baed, under APPROVED plan (plan-v050-release-r2 PASS, MSG-26). Docket release-v050-docket.md; release-v050.diff is the full diff. Merge and irreversible tag/PyPI publish happen only on PASS.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: fb2cc3e546118a0324b913788fdd311c5f37803bc44b7f8fa798a2445596b7cd
- source-ref: 89fb3aab2d386a9fbbe05675ad3b93f97e474b78
- docket-revision-sha256: 98b983385105021a0428cb346f79a18182da0b844f5762eb68d002e48682dd78
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-07-v0.5.0-release.md", "sha256": "9d4590e84efbb9ea38586fbf014c9784877e9f0fbfe7097339931844cd9f645b", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/release-v050-docket.md", "sha256": "35c709bb1f8e4e2ee02bcb7e2a329d23d588af72022cfe8b167701ede444163b", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/release-v050.diff", "sha256": "d545d1813f8945975b4142f1541c07cfbb92508458d78134d50ab844a9a20675", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/release-v050-watcher.json", "sha256": "fb2cc3e546118a0324b913788fdd311c5f37803bc44b7f8fa798a2445596b7cd", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "5c84620f746bb8a2a42831f043da74d5eaf761b2d760b6f9ad4f8e1071fae06f", "opus": "9713a17ba8d3a03f61cf8bf00ec00d1d43e1b470df58bdb8991aff90736b5230"}

## MSG-28 | 2026-08-07T14:27:35+00:00 | from: opus | type: verdict | thread: release-v050-branch | refs: -

## Verification command

Ran exactly `python -m pytest -q` from the export root (no prefixes, pipes or env diagnostics):

```
........................................................................ [ 18%]
........................................................................ [ 36%]
........................................................................ [ 54%]
......................................................s................. [ 72%]
........................................................................ [ 91%]
...................................                                      [100%]
394 passed, 1 skipped in 17.08s
```

## Criterion-1 checks against the pinned export

**Four version strings agree at 0.5.0.** `pyproject.toml:7` `version = "0.5.0"`; `src/debate/__init__.py:42` `__version__ = "0.5.0"`; `.claude-plugin/plugin.json:3` and `.claude-plugin/marketplace.json:9` both `"0.5.0"`. Matches all four diff hunks.

**CHANGELOG `## v0.5.0 — 2026-08-07`** is present at `CHANGELOG.md:9` with no residual `Unreleased` heading (headings run v0.5.0 → v0.4.0 → v0.3.1 → …).
- *MSG-11..14 not claimed final:* `CHANGELOG.md:63` reads "The repository's **first end-to-end** brokered proof (MSG-11..14)", and adds that the record has since grown past it. No "final proof" string survives anywhere in `CHANGELOG.md`/`README.md`.
- *Deprecation without removal date:* `CHANGELOG.md:72-76` states legacy-layout posting is "deprecated as of 0.5", still works, `debate migrate` is the supported path, "No removal date is promised."
- *Fixed items match real code:* fail-closed guards are real — `controller.py:1297` and `:1325` raise `ChannelError("refused: malformed sealed submissions state")`, and `controller.py:1779` raises `"refused: malformed deliberation votes state"` for a non-dict `latest_votes` (plus `:1268`/`:1541` for malformed submission records). Windows baseline is real — `controller.py:673` `_WINDOWS_BASELINE_ENVIRONMENT = ("SYSTEMROOT", "SYSTEMDRIVE", "COMSPEC", "PATHEXT", "WINDIR")` with `_baseline_environment()` at `:676-679` returning `{}` when `os.name != "nt"`, so the POSIX baseline is empty as claimed. The mypy exclude is real — `pyproject.toml:62` `exclude = ["^build/", "^var/"]`, commented as gitignored duplicate-module trees absent from CI.

**README changes accurate.**
- Removed versions note leaves nothing dangling: no occurrence of `0.3.1`, "Note on versions", "exist only on", "Install from source", "until the next release" or "note above" remains in `README.md`.
- Deprecation wording at `README.md:381-383` matches the CHANGELOG's (deprecated as of 0.5, still works, `debate migrate` supported path, no removal date promised).
- Counts measurable in the export: `wc -l src/debate/*.py` totals **4943** lines (channel 1404, controller 1843, watcher 1105, `__main__` 549, `__init__` 42) against README's "about 4,900 lines including the CLI and the broker"; the pytest run above is 394 passed + 1 skipped = **395** collected, against "395 tests as of this writing" (`README.md:466-467`).
- MSG-11..14 wording matches the CHANGELOG's: `README.md:504` "The first end-to-end proof is MSG-11..14".

**New SVGs and alt text honor `src/debate/controller.py`.** `docs/assets/broker-light.svg` and `broker-dark.svg` both exist (9658 bytes each — expected, since the palettes differ only in equal-width hex tokens; they are not duplicates: `#161b22` occurs 6× in the dark file and 0× in the light one). `README.md:131-136` wires the dark `srcset` to `broker-dark.svg` with `broker-light.svg` as the `img` fallback. Every alt-text/diagram claim is honored by code: full 40-character pin enforced at `controller.py:354-357`; per-seat HOME/XDG/TMPDIR/`GIT_CEILING_DIRECTORIES` at `:691-701` with `_RESERVED_ENV` at `:38-50`; seats cannot name their sender — module docstring `:7` and the `"sender" in raw` rejection at `:722`; controller-owned posting via `channel.post` under the bound seat identity; sealed paired reveal through `channel.commit_reveal_pair` (`channel.py:749-765`, one mailbox replacement with restart-safe doorbell repair) invoked at `controller.py:1575-1583`; typed close PASS/NO_PASS/ERROR with `_agreement` at `:1490-1509` — PASS additionally requires an agreeing `author-independent` seat (`:1500-1508`), matching the CHANGELOG and the seat-B caption; one absolute whole-case deadline at `:859/:863` propagated as `_case_deadline`; watcher tick at `watcher.py:3-6` "Runs from any scheduler … every 60s … No LLM runs when nothing changed", with the no-op `Decision(None, None, …)` paths at `:222-276`. Supervisor is not a vote — votes are keyed only to `self.config.profiles` (`:1492`). I found no diagram or alt-text claim the code does not honor.

**Case-study epilogue faithful.** The article's three amendments at `docs/case-study.md:73-83` (git-verified claims, shared-checkout discipline, corrections-are-entries) are the same three the epilogue picks up at `:114-127`, in order and without overclaiming — amendment 1 is explicitly said to have "stayed cultural for what an agent *says*". Isolation stays advisory and the boundary honest at `:136-141` ("strong protection against *accidental* contamination, not a claim that a same-user process is hostile-code safe … The isolation is advisory"); the epilogue makes no unforgeability claim, and `README.md:463-467` keeps the record framed as an honest log, "not as evidence against a determined forger with write access".

## Non-blocking observation

`README.md:97` still reads "or just vendor the two modules", which predates this diff and is untouched by it; with the broker the package is five modules. Outside this docket's criteria and not release-blocking, but worth a follow-up edit.

Every criterion-1 check holds and the required command passes, so this seat votes PASS.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3ca477bd5efb3d1753d43900aebfb36f69bff4ce89ae22c2a88de61a5a46719d
- phase: sealed
- captured-at: 2026-08-07T14:27:35+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: fb2cc3e546118a0324b913788fdd311c5f37803bc44b7f8fa798a2445596b7cd
- source-ref: 89fb3aab2d386a9fbbe05675ad3b93f97e474b78
- source-manifest-sha256: 9713a17ba8d3a03f61cf8bf00ec00d1d43e1b470df58bdb8991aff90736b5230
- docket-revision-sha256: 98b983385105021a0428cb346f79a18182da0b844f5762eb68d002e48682dd78
- input-sha256: f5d19b07c404a6db6d0780f5ff419c9262290aed0e54755c5e09712868d2cb2b
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-29 | 2026-08-07T14:27:35+00:00 | from: codex | type: verdict | thread: release-v050-branch | refs: -

Inspected every hunk in the immutable release diff against the pinned export. The four version locations are 0.5.0; CHANGELOG/README deprecation, MSG-11..14, Fixed-item, diagram/alt-text, and case-study claims match the exported implementation in /home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/89fb3aab2d386a9fbbe05675ad3b93f97e474b78/codex/{CHANGELOG.md,README.md,docs/case-study.md,docs/assets/broker-light.svg,docs/assets/broker-dark.svg,src/debate/controller.py,src/debate/watcher.py,pyproject.toml}. Measured source is 4,943 lines; the test suite totals 395 items. Fresh required command run exactly: `python -m pytest -q` → `394 passed, 1 skipped in 17.64s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 3ca477bd5efb3d1753d43900aebfb36f69bff4ce89ae22c2a88de61a5a46719d
- phase: sealed
- captured-at: 2026-08-07T14:23:58+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: fb2cc3e546118a0324b913788fdd311c5f37803bc44b7f8fa798a2445596b7cd
- source-ref: 89fb3aab2d386a9fbbe05675ad3b93f97e474b78
- source-manifest-sha256: 5c84620f746bb8a2a42831f043da74d5eaf761b2d760b6f9ad4f8e1071fae06f
- docket-revision-sha256: 98b983385105021a0428cb346f79a18182da0b844f5762eb68d002e48682dd78
- input-sha256: 1af692e292d243a2536b1084d037a2651e375f5a75460e07d98c182c17127610
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-30 | 2026-08-07T14:27:35+00:00 | from: owner | type: close | thread: release-v050-branch | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-31 | 2026-08-12T18:45:21+00:00 | from: owner | type: review-request | thread: setup-wizard-slice1-branch | refs: feature/setup-wizard-slice1@196fa26d308557889f34b830d2fb0f97a9a6464d

Branch gate: feature/setup-wizard-slice1@196fa26 (PR #9), Slice 1 of the APPROVED setup-wizard plan (MSG-36, debate-06451). Docket setup-slice1-docket.md; setup-slice1.diff is the full diff. One execution delta needs the seats' explicit judgment: managed-v2 channels are REFUSED by setup (the approval predates v2). Merge only on terminal PASS + green CI.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 27ac80a3a1571bf1cc3c1299e39c96bd7088580fe058a42779da0669de5ab006
- source-ref: 196fa26d308557889f34b830d2fb0f97a9a6464d
- docket-revision-sha256: 7c9df950663bafe0e7b7df29805810f431c1d90d3ca06a0d46c1c0fc0d8f51aa
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-04-setup-wizard.md", "sha256": "da654cf17ddc4c91753d1972bebf3f8c9fc2bb248bcae597918cba8a61bb3cdd", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1-docket.md", "sha256": "f1ed4b8e87573175919b38fe0b29f5b0226b22f8bd2e394557cc621cc74b2164", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1.diff", "sha256": "9c40f8af754665055ec3ecca3ca3df93e4f053da0d4597d5ba1f1b618fd2c08d", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1-watcher.json", "sha256": "27ac80a3a1571bf1cc3c1299e39c96bd7088580fe058a42779da0669de5ab006", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "f0c48c55992e42f69e00d7ecfcf9cc8a41c3bb9acd1cb919b9efbed4ff0ec043", "opus": "9dde1cb589fe430ba0304aee1da29e6425bf4d52c92b032265a73cbe4f5aa1a3"}

## MSG-32 | 2026-08-12T18:53:21+00:00 | from: opus | type: verdict | thread: setup-wizard-slice1-branch | refs: -

## Verdict: NO_PASS — one blocking finding

### Fresh command output

Mandated command, run literally from the pinned export root (`PYTHONPATH=src` per the seat profile):

```
$ python -m pytest -q
........................................................................ [ 17%]
........................................................................ [ 35%]
........................................................................ [ 53%]
..................................................................s..... [ 70%]
........................................................................ [ 88%]
...............................................                          [100%]
406 passed, 1 skipped in 16.72s
```

The suite is green. It is not sufficient, because the suite does not exercise the case below — and one of its tests pins the defect as expected output.

Supporting command:

```
$ diff PROTOCOL.md src/debate/protocol_template.md   # exit 0, no output
$ sha256sum PROTOCOL.md src/debate/protocol_template.md
8a2085a3f5a0f3a9b0b866e54da35cbe35e41ad9d73e96272598f5fe4d01fe6d  PROTOCOL.md
8a2085a3f5a0f3a9b0b866e54da35cbe35e41ad9d73e96272598f5fe4d01fe6d  src/debate/protocol_template.md
```

Disclosure: I also attempted a supplementary `python3 -c` run to demonstrate the finding below as live output. The harness permission policy denied it (test-only Bash allowlist). That finding therefore rests on reading the pinned export, not on a fresh run; every line cited is quoted from the export and is independently checkable.

### BLOCKING — the wizard's `--human` seat writes a config the tool itself reports `INVALID`

The plan's §2.1 offers "human-driven (no `commands` entry, the documented pattern for a live seat)" as a first-class answer, and `--human PARTY` is a shipped flag (`__main__.py`, `p_setup.add_argument("--human", …)`). That description is stale for anything `debate init` creates today, in exactly the way the executor's own recorded delta is stale for managed version 2:

- `channel.init_channel` (`src/debate/channel.py:353-354`): `if name is not None and managed_version is None: managed_version = MANAGED_VERSION` — every named channel is managed version 1. The README line added by this very diff says so: "New channels record managed_version 1".
- `WatcherConfig.managed_problem()` (`src/debate/watcher.py:136-167`), whose docstring reads "Kept pure so `decide()` and `status()` share exactly one definition of validity": for `managed_version == 1`, `missing = sorted(expected - configured)` → returns `"missing adapter command for managed parties: alpha"`.
- `decide()` (`src/debate/watcher.py:225-227`): `Decision(None, f"invalid managed channel: {problem}", "invalid managed configuration")` — never invokes, escalates to the supervisor on every tick.
- `status()` (`src/debate/watcher.py:328-329`): `WatchStatus("INVALID", …)`, and `_NEEDS_ATTENTION = ("STALE", "ESCALATED", "INVALID", "ERROR")` (`src/debate/__main__.py:195`) makes `watch-status` exit nonzero.
- The PROTOCOL template this wizard scaffolds states the rule itself (`src/debate/protocol_template.md:84-86`): "A managed-version 1 compatibility channel has one command for each of its exactly two parties … A missing command or a turnless open thread is `INVALID`, exits nonzero under `watch-status`, and is never delegated to a live human."

`setup.py` nonetheless writes that config with no refusal and no warning: `validate()` checks party membership, argv resolvability, overwrite and state-dir creatability, and never consults `managed_problem()`. The §2.6 round-trip does not catch it either — `apply()` calls `load_config_fn(spec.channel_root, probe, spec.channel_name)`, and `_watcher_config` → `WatcherConfig.__post_init__` binds `managed_version=1` and `parties` from the channel record but never calls `managed_problem()`. So the object *knows* it is invalid at setup time and nobody asks.

This is a direct miss against the docket criterion "§2.6 validation precedes every write and round-trips the REAL loader", whose stated purpose in the plan is to make refusals "fire at setup time rather than at the first scheduler tick". The single most likely misconfiguration the wizard itself offers is the one that survives to the first tick.

Why the tests stayed green: `test_apply_human_driven_seat_has_no_command_entry` asserts `"alpha" not in config["commands"]` — it pins the broken output as correct. `test_end_to_end_cli_yes_flags_status_and_config_load` runs `--human beta` against a managed-v1 channel and then asserts `main(["status", …])` returns 0 — that is channel `status`, not `watch-status`. Nothing in the suite runs `watch-status` or `decide()` over a wizard-produced config.

**Named better behavior (the fix I would accept):** in `setup.validate()`/`apply()`, reuse the one existing definition of validity — after the probe round-trip, call `managed_problem()` on the returned `WatcherConfig` and refuse when it is non-`None`, with a message naming the two real options (give the party a command, or the seat cannot be human-driven on a managed channel). It is a few lines, it reuses the function whose docstring already promises to be the single definition, and it closes the gap at setup time exactly as §2.6 promises. The interview should likewise not offer "empty = human-driven" for a managed-v1 channel. Add a test asserting `watch-status` (or `managed_problem()`) is clean on the wizard's own output.

### On the execution delta you asked me to accept or reject: ACCEPTED

Refusing a `managed_version: 2` channel is the right narrowing. `WatcherConfig.__post_init__` refuses `commands` mixed with brokered profiles ("refused: do not mix direct commands with brokered adapter profiles") and `managed_problem()` returns "managed-version 2 requires two brokered adapter profiles" when `broker is None`; v2 additionally needs `runtime_root`, `source_ref`, `whole_case_timeout_seconds`, docket files and canaries (`_watcher_config`, `src/debate/__main__.py:126-160`). A v1-shaped `commands`/`prompts` config for a v2 channel would be permanently `INVALID`. Refusing with a pointer at `watcher.brokered.example.json` and `adapter-doctor` is correct, and `test_brokered_channel_is_refused_with_pointer` covers it. My blocking finding is that the *same* reasoning was not applied one version down.

### Criteria that DO hold (verified against the pinned export)

- **§2.1 split** — `interview()` does terminal I/O plus the defaults read; `apply()` does validation then file writes only. Flags are the interview (`flag_commands` pre-seeds `commands`; only `open_parties` are asked). `--yes` with neither flags nor remembered answers raises `"refused: --yes with no remembered or flag-supplied answer for …"` (`setup.py`), covered by `test_yes_without_defaults_or_flags_refuses`.
- **§2.2 derived-never-asked** — `derive_paths()`: `state_path = ~/.local/state/debate/<name>.json`, `config_path = <toplevel>/<name>.watcher.json`; toplevel is the recorded project when present, else `root.resolve().parent`, and `__main__` passes `Path(chan_config.project)`. Unit name `debate-watch-<channel_name>` in `closing_hints()` agrees with the `state_path.stem` convention since the stem is the id.
- **§2.3 writes** — config, `PROTOCOL.md` only-if-absent (`scaffold_protocol` returns `None` when `target.exists()`; thread-cap bracket filled by `.replace("[12]", f"[{thread_cap}]", 1)`, and `[12]` in §3 is genuinely the first bracketed `[12]` in the template), defaults cache carrying `"channel": spec.channel_name` with the provenance surfaced as "remembered from channel …". `.gitignore` is never written — `config_is_gitignored()` only runs `git check-ignore -q` and a hint is printed instead.
- **The repo's own `.gitignore` change** — adding `*.watcher.json` beside the existing `watcher.json` is the repo adopting its own hint. It is correct and does not shadow anything committed: `watcher.example.json` and `watcher.brokered.example.json` do not match the `*.watcher.json` suffix. Accepted.
- **§2.4 prompt clauses** — `PROMPT_TEMPLATE` carries all of: PROTOCOL.md first; `debate read` only, "never the whole mailbox"; the two-gate check ("NON-EMPTY thread AND turn=='{party}' — if either fails, exit without posting"); fresh evidence ("YOUR OWN fresh evidence … never evidence quoted from the request"); review-append-at-END ("append your review as a dated section at the END … never edit its body"); post-then-stop. Addressing is `--root {channel_root} --channel {channel_name}` on both `debate read` and `debate post`.
- **`command_for` single pass** — `src/debate/watcher.py`: `{channel_root}` then `{channel_name}` are expanded in the prompt text, and argv is walked once for `{prompt}`; argv is never re-scanned, so nothing arriving from the prompt body triggers a second expansion. A prompt without placeholders is untouched (`test_prompt_without_placeholder_is_left_untouched`).
- **Packaged template byte-equality** — proven by the `diff`/`sha256sum` above and pinned by `test_packaged_template_matches_repo_protocol`.
- **No secret reaches the written config** — the written object is exactly `state_path`, `commands`, `prompts`, `debounce_seconds`, `retry_seconds`, `timeout_seconds`; the wizard solicits no credential and Slice 1 scaffolds no wrapper.

### Non-blocking notes (fix while you are in here)

1. **Dead assertion.** `test_protocol_scaffolded_when_absent_and_never_clobbered`: `assert "[9]" in text and "[12]" not in text.split("\n\n")[0] or "[9]" in text`. By Python precedence this is `(A and B) or A`, which reduces to `A` — the "`[12]` is gone" half can never fail. Assert on the thread-cap line specifically.
2. **Probe file writes into the operator's repo before the "nothing is written" guarantee.** `apply()` writes `.<name>.watcher.json.setup-probe` into the derived toplevel to round-trip the loader; it is removed in `finally`, but a kill between write and unlink leaves a stray file that — ending in `.setup-probe`, not `.watcher.json` — is not covered by the gitignore line the tool just hinted about. `tempfile.NamedTemporaryFile` in the same directory, or validating in-memory, avoids it.
3. **`--yes` silently overwrites.** `interview()` sets `overwrite=assume_yes`, so a non-interactive re-run clobbers an existing watcher config without the §2.7 "prints what exists" step. Defensible as "yes means yes", but printing the existing path before replacing it costs one line.
4. **Inline-secret argv is written verbatim.** `--command 'seat=/path/agent --api-key sk-…'` lands unscrubbed in the config. The plan's answer is the wrapper convention (§2.5, Slice 1 does not implement it); a warning when an argv element looks like a credential would close the gap the convention is carrying alone.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 1f084a952ed7a7b9bf56a45171eaacd1351885d7d55f7b5fbed27f71ebe4fa91
- phase: sealed
- captured-at: 2026-08-12T18:50:44+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 27ac80a3a1571bf1cc3c1299e39c96bd7088580fe058a42779da0669de5ab006
- source-ref: 196fa26d308557889f34b830d2fb0f97a9a6464d
- source-manifest-sha256: 9dde1cb589fe430ba0304aee1da29e6425bf4d52c92b032265a73cbe4f5aa1a3
- docket-revision-sha256: 7c9df950663bafe0e7b7df29805810f431c1d90d3ca06a0d46c1c0fc0d8f51aa
- input-sha256: 25818eadccdbfe4f166565c8ab8b44b8d7fd3ef22dc141ffb488b3b8246141fe
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-33 | 2026-08-12T18:53:21+00:00 | from: codex | type: verdict | thread: setup-wizard-slice1-branch | refs: -

`python -m pytest -q` run in the pinned export completed: `406 passed, 1 skipped in 18.66s`. Blocking criterion §2.6 failure: inspection command `nl -ba .../src/debate/setup.py | sed -n '120,225p'` shows `validate()` creates `spec.state_path.parent` at lines 162–167, and `apply()` writes a loader probe at lines 187–193 before the real loader can reject the assembled configuration. A loader failure (including state_path-inside-channel-root) can therefore occur after writes, contrary to “validation precedes every write” / “Nothing is written until every check passes.” The same source inspection shows no secret guard: CLI input is accepted via `shlex.split` in `src/debate/__main__.py:431-438`, then persisted verbatim in `setup.py:178-185` and `196`; a `--command` argv containing a credential reaches the generated watcher config, violating the docket’s “no secret can reach the written config” criterion. Other checked items were present: `cmp -s .../PROTOCOL.md .../src/debate/protocol_template.md` returned `protocol_template_cmp_exit=0`, and watcher `command_for` expands both placeholders before prompt substitution.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 1f084a952ed7a7b9bf56a45171eaacd1351885d7d55f7b5fbed27f71ebe4fa91
- phase: sealed
- captured-at: 2026-08-12T18:53:21+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 27ac80a3a1571bf1cc3c1299e39c96bd7088580fe058a42779da0669de5ab006
- source-ref: 196fa26d308557889f34b830d2fb0f97a9a6464d
- source-manifest-sha256: f0c48c55992e42f69e00d7ecfcf9cc8a41c3bb9acd1cb919b9efbed4ff0ec043
- docket-revision-sha256: 7c9df950663bafe0e7b7df29805810f431c1d90d3ca06a0d46c1c0fc0d8f51aa
- input-sha256: 83fc4f13aea07a10919ca8d4db7cbba03f26c1b3bc47e6e2366dddb6164591de
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-34 | 2026-08-12T18:53:21+00:00 | from: owner | type: close | thread: setup-wizard-slice1-branch | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-35 | 2026-08-12T18:56:36+00:00 | from: owner | type: review-request | thread: setup-wizard-slice1-branch-r2 | refs: feature/setup-wizard-slice1@397827e4d7c8592bebe6a3c8c7e61f4014ad9fbd

Branch gate round 2: feature/setup-wizard-slice1@397827e (PR #9) with the three MSG-32/33 findings folded (managed_problem() asked at setup time; zero writes before all checks pass — scratch-dir probe; credential-shaped argv refused). Also includes the Windows argv-splitting fix (POSIX shlex ate backslashes; CI all-green at this ref). Docket updated with the round-1 summary; criteria otherwise unchanged.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 6c25a174eaeb3603ece8d014397eb044aa12f13b2ee84c77c135eddf6ee20f23
- source-ref: 397827e4d7c8592bebe6a3c8c7e61f4014ad9fbd
- docket-revision-sha256: e2d7766190286ee17baba653e2400395beb0f1f9220a965600c95e2fda3fb0ca
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-04-setup-wizard.md", "sha256": "4b35ab4ee8e0c1a34350f7e60f796e45a634719bc19ab66c4eb5aa0992c7403d", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1-docket.md", "sha256": "161db4c18e88cd15864de1965f680fd5a2cee73c5ab7cf0cfb1ce64ea7496660", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1.diff", "sha256": "54806a938b3ac3d309635e7111bd6ecab6863ebd0a2a37afee8c86276a697b9a", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1-watcher.json", "sha256": "6c25a174eaeb3603ece8d014397eb044aa12f13b2ee84c77c135eddf6ee20f23", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "39e3b950a9ba437ac055096e9c1caa1849353940baa5a0032466d9b8319dc64e", "opus": "03c83b1d73e446af0ccce069d9c2c5d4227d6e1c8ee4721c37281ea810a53b68"}

## MSG-36 | 2026-08-12T19:06:00+00:00 | from: opus | type: verdict | thread: setup-wizard-slice1-branch-r2 | refs: -

## Verdict: NO_PASS — two blocking findings

### Fresh command evidence

Ran the docket command literally, no prefixes/suffixes/pipes, cwd = the pinned export root
`.../exports/397827e4d7c8592bebe6a3c8c7e61f4014ad9fbd/opus`:

```
$ python -m pytest -q
........................................................................ [ 17%]
........................................................................ [ 35%]
........................................................................ [ 52%]
...................................................................s.... [ 70%]
........................................................................ [ 88%]
................................................                         [100%]
407 passed, 1 skipped in 17.39s
```

The command passes. The blocking findings below come from criterion-1 inspection, which the
suite does not cover. Files inspected in the export: `src/debate/setup.py`,
`src/debate/__main__.py`, `src/debate/watcher.py`, `src/debate/channel.py`, `PROTOCOL.md`,
`src/debate/protocol_template.md`, `pyproject.toml`, `tests/test_setup.py`,
`tests/test_output_is_ascii.py`, plus `setup-slice1.diff` and the plan in the docket. I made
no edits, read no live channel, and used no `/tmp`. Note on evidence limits: in this seat only
the docket command and a few `ls`-class calls were permitted, so I could not independently
print the imported `debate.__file__`; the run used the environment-supplied project-local paths
from the export root, and `git status` there reports "not a git repository" (a clean export),
with no `.pytest-tmp` residue left behind.

### F1 (blocking) — the round-1 fold is fail-open by default: `apply()` skips the real-loader
round-trip *and* the `managed_problem()` gate unless the caller opts in

`src/debate/setup.py:196-231`:

```python
def apply(spec, load_config_fn: Callable[...] | None = None) -> list[Path]:
    validate(spec)
    config = {...}
    if load_config_fn is not None:
        with tempfile.TemporaryDirectory(...) as scratch:
            ...
            loaded = load_config_fn(...)
        problem = loaded.managed_problem()
        if problem is not None:
            raise channel.ChannelError(...)
```

Both round-1 folds live inside that `if`. With the default argument, `apply(spec)` writes the
config, the state dir and the defaults cache without ever asking the real loader — so
`WatcherConfig.__post_init__`'s state-inside-the-channel-root refusal and the watcher's own
`managed_problem()` INVALID verdict are simply not consulted. Docket criterion "§2.6 validation
precedes every write and round-trips the REAL loader" holds only on the CLI path
(`__main__.py:452` passes `_watcher_config`); the pinned library entry point defaults to
skipping it.

This is not hypothetical, and it re-opens round-1 finding (1) on the exact shape that finding
named. `tests/test_setup.py:64-74` asserts `{"alpha": None, "beta": [script]}` must refuse —
but only because that test passes `load_config_fn=_watcher_config`. The same spec shape reaches
`apply(spec)` with no loader twice in this diff (`tests/test_setup.py:77-83` and `:97-103`, both
`{"beta": None}`), where the only thing preventing a written INVALID managed-v1 config is that
an *earlier* check (credential / PATH) fires first. Plan §2.1 and §5 pin `apply` as the reuse
surface for a non-terminal caller ("the interview/apply split of §2.1 is what lets that agent
reuse `apply` without a terminal") — that named future caller gets the unguarded default.

A validation module whose two strongest checks are off by default is the defect; the fix is
small: make the round-trip unconditional (default the loader to the real one via a local import,
or move the loader out of `__main__`) and keep the parameter only as a test seam. I would also
keep an assertion that `apply(spec)` with no kwargs refuses the human-driven managed-v1 spec.

### F2 (blocking) — the diff introduces the first non-ASCII operator-facing strings in the
package, against the repo's own incident-driven invariant

`tests/test_output_is_ascii.py:1-11` states the rule and the incident ("CI (windows-latest) hit
`UnicodeDecodeError: byte 0xb7` … Windows `print()` to a REDIRECTED stream uses the locale
encoding … Source comments and docstrings are unaffected"). Its AST sweep
(`test_no_string_literal_in_the_watcher_can_carry_non_ascii`, line 118) is hard-scoped to
`src/debate/watcher.py`, so it cannot see the new module.

Searching non-ASCII across `src/debate/` at the pinned ref: `controller.py` 0 hits;
`channel.py` and `watcher.py` hits are *all* in docstrings/comments — i.e. before this diff the
package had zero non-ASCII runtime string literals. This diff adds eight, in operator-facing
strings:

- `__main__.py:420` and `:425` — em dash inside the "run `debate migrate` first" and the
  managed-v2 refusals; `main` prints `str(error)` to stderr (`__main__.py:614-616`).
- `__main__.py:448` — em dash inside the interactive `input(f"{spec.config_path} exists — overwrite? [y/N] ")` prompt.
- `setup.py:169-170` — em dash and `§` in the credential refusal (round-1 fold 3's own message).
- `setup.py:228` — em dash in the `managed_problem` refusal (round-1 fold 1's own message).
- `setup.py:38, 40, 44` — em dashes in `PROMPT_TEMPLATE`. Lower severity: `json.dumps` escapes
  them, so the written config stays ASCII, and argv to the child is not locale-encoded.

U+2014 and U+00A7 both exist in cp1252, so on Windows these print *successfully* as bytes
0x97/0xA7 and the redirected log is then not valid UTF-8 — precisely the failure the test module
was written for, and precisely the messages a first-run operator reads. `debate setup` is the
onboarding command; this is the worst place to reintroduce it. Fix: plain ASCII in these strings
(`-`, "section 2.5"), and widen the AST sweep to `setup.py` and `__main__.py` so the guard stops
being file-scoped.

If the maintainers scope the ASCII rule to watcher/log output only, F2 becomes a note — F1 still
blocks on its own.

### Explicit rulings the docket asked for

- **Managed-version-2 refusal (execution delta): ACCEPTED as the right narrowing.** A v2 seat is
  an adapter profile; `WatcherConfig.__post_init__` (`watcher.py:118-125`) rejects a brokered
  config that carries `commands` at all, so a wizard emitting `commands`/`prompts` for a v2
  channel could only ever produce something the loader refuses. Refusing early at
  `__main__.py:423-428` with a pointer at `watcher.brokered.example.json` and `adapter-doctor`
  is better than writing a config that dies at load. `tests/test_setup.py:209-219` pins the
  pointer. No better behavior to name.
- **Keeping `--human`: accepted as a guided refusal, with one precision note.** `debate init`
  always records a managed version (`__main__.py:401`), so on every channel the current tool
  creates, `--human` can only ever end in the F1-guarded refusal. Its help text
  ("mark a party human-driven (no watcher command); skips its question") gives no hint of that.
  Either say "legacy/unmanaged channels only" in the help, or refuse at parse time with the same
  wording. Non-blocking.
- **The repo's own `.gitignore` hunk: accepted.** `*.watcher.json` is the repo adopting the hint
  the tool prints, and it does not swallow the committed `watcher.example.json` /
  `watcher.brokered.example.json` (neither ends in `.watcher.json`). Minor inconsistency: the
  tool's hint (`setup.py:322-323`) suggests the literal filename, while the repo adopted the glob.

### Criterion-1 checks that DO hold

- **§2.1 split.** `interview()` touches only the terminal plus the defaults cache; `apply()` does
  files only. Flags are the interview (`interview()` seeds from `flag_commands`, never asks a
  covered party), and `--yes` with neither flags nor remembered answers refuses
  (`setup.py:275-278`, pinned by `tests/test_setup.py:150-155`).
- **§2.2 derived-never-asked.** `derive_paths` (`setup.py:111-123`) makes the channel id the
  config stem and the state stem; `closing_hints` names the unit `debate-watch-<channel id>`,
  which matches `watcher.py`'s `debate-watch-<state stem>` because the state file is
  `<id>.json`. Toplevel follows the recorded project, falling back to the channel folder's
  parent — the `_derived_project` two-tier rule.
- **§2.3 writes.** Config, `PROTOCOL.md` only-if-absent (`scaffold_protocol` returns `None` when
  present, `setup.py:146-151`), defaults cache carrying `"channel": spec.channel_name`, and the
  interview shows that provenance (`setup.py:262-263`). `.gitignore` is never written — only a
  printed hint, and `config_is_gitignored` runs `git check-ignore` read-only.
- **§2.4 prompt.** All required clauses present in `PROMPT_TEMPLATE`: PROTOCOL.md first, `debate
  read` only / never the whole mailbox, the two separate gates (NON-EMPTY thread AND
  `turn=='{party}'`), fresh own evidence, review appended as a dated section at the END,
  post-then-stop, and `--root {channel_root} --channel {channel_name}` addressing.
  `command_for` (`watcher.py:190-202`) expands both channel placeholders in the prompt text and
  only then substitutes `{prompt}` into argv; argv is never re-scanned. Nit only: the two
  channel replacements are chained, so a channel_root path that literally contained
  `{channel_name}` would be expanded by the second — same class as the pre-existing ordering,
  not a regression.
- **Packaged template byte-equality.** `src/debate/protocol_template.md` matches the export's
  `PROTOCOL.md` line for line on my own read (159 lines, identical content including the
  `[12]` thread-cap bracket), `pyproject.toml` ships it as package data, and
  `tests/test_setup.py:123-124` pins it — that test is inside the 407 that passed.
- **No secret reaches the config** on the checked path: `validate` scans every argv element
  before anything is written (`setup.py:165-170`), prompts and derived keys are generated.

### Non-blocking notes worth folding

1. `tests/test_setup.py:114` is tautological: `assert "[9]" in text and "[12]" not in text.split("\n\n")[0] or "[9]" in text` collapses to `"[9]" in text`, so "the thread-cap bracket was
   *replaced*" is never actually asserted. The behavior is correct (`str.replace(..., 1)` on the
   first `[12]`, which is the thread-cap line); the test just does not pin it.
2. Test hygiene outside the temp tree. `--basetemp=.pytest-tmp` (`pyproject.toml`) puts `tmp_path`
   inside the working tree, so on a real checkout `_derived_project` resolves to the repo
   toplevel and `test_end_to_end_...` / `test_two_channels_refuse_without_channel_flag` write a
   `<id>.watcher.json` into the developer's repo root and unlink it (the tests say so and clean
   up; a mid-test failure leaves residue, now gitignored). Worse, the two-channel test does not
   monkeypatch `HOME` the way the e2e test does, so `apply` does `mkdir(parents=True)` on the
   operator's real `~/.local/state/debate/`. For a tool whose stated purpose is to stop doing
   surprising things to an operator's machine, its own suite should stay inside `tmp_path`.
3. `SECRET_PATTERN` matches the bare word `secret` in any argv element, so a wrapper path such as
   `~/.secrets/glm-agent` — the very idiom plan §2.5 recommends — is refused with no override.
   Consider anchoring on assignment-shaped tokens only, or offering an escape hatch.
4. `apply` writes the config before scaffolding `PROTOCOL.md`; a failure on the second write
   leaves a config pointing at a channel with no PROTOCOL.md.

Happy to flip to PASS on a revision that makes the loader round-trip unconditional (F1) and
returns the operator-facing strings to ASCII with the AST sweep widened past `watcher.py` (F2).

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 631550944342aae92c32b9bf053040b38ff0c7a620739d1d35dac4a332960f18
- phase: sealed
- captured-at: 2026-08-12T19:06:00+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 6c25a174eaeb3603ece8d014397eb044aa12f13b2ee84c77c135eddf6ee20f23
- source-ref: 397827e4d7c8592bebe6a3c8c7e61f4014ad9fbd
- source-manifest-sha256: 03c83b1d73e446af0ccce069d9c2c5d4227d6e1c8ee4721c37281ea810a53b68
- docket-revision-sha256: e2d7766190286ee17baba653e2400395beb0f1f9220a965600c95e2fda3fb0ca
- input-sha256: 3e27307d355215e89294e24161d9395db6550b664b0e527528eac5c34d85d5eb
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-37 | 2026-08-12T19:06:00+00:00 | from: codex | type: verdict | thread: setup-wizard-slice1-branch-r2 | refs: -

Blocking: the secret guard in `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/397827e4d7c8592bebe6a3c8c7e61f4014ad9fbd/codex/src/debate/setup.py:52-53` only matches `token`/`api-key` when followed by `=` or `:`. A normal argv such as `agent --token actual-secret` passes validation and is then written into `commands` at lines 204-207, violating the docket requirement that no secret/key-shaped credential reaches the written config. The required fresh verification command `python -m pytest -q` ran in the pinned export and returned `407 passed, 1 skipped in 19.53s`, but its passing result does not cover this credential form.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 631550944342aae92c32b9bf053040b38ff0c7a620739d1d35dac4a332960f18
- phase: sealed
- captured-at: 2026-08-12T18:59:13+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 6c25a174eaeb3603ece8d014397eb044aa12f13b2ee84c77c135eddf6ee20f23
- source-ref: 397827e4d7c8592bebe6a3c8c7e61f4014ad9fbd
- source-manifest-sha256: 39e3b950a9ba437ac055096e9c1caa1849353940baa5a0032466d9b8319dc64e
- docket-revision-sha256: e2d7766190286ee17baba653e2400395beb0f1f9220a965600c95e2fda3fb0ca
- input-sha256: 2178028d0e91c2f8ec919bfd43f1bdfc4a8abde7027882d49258592f10abe49a
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-38 | 2026-08-12T19:06:00+00:00 | from: owner | type: close | thread: setup-wizard-slice1-branch-r2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-39 | 2026-08-12T19:09:09+00:00 | from: owner | type: review-request | thread: setup-wizard-slice1-branch-r3 | refs: feature/setup-wizard-slice1@b5afcb9d93f8cfe67a7236f43307d376921c3db8

Branch gate round 3: feature/setup-wizard-slice1@b5afcb9 (PR #9). Round-2 folds: required loader (fail-open gone), ASCII runtime strings + package-wide AST sweep, flag-form credential refusal. Suite 408 passed at this ref; CI re-running. Docket carries both prior rounds' summaries.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: a3a3d4392e1e7f96365ea7620a2cafad978f5664a5d8fc62a469c82efbab4510
- source-ref: b5afcb9d93f8cfe67a7236f43307d376921c3db8
- docket-revision-sha256: f8f9a7ec711c6e1565ca09fc78d6c81a1c8076e7acc1d259ece049fe3ab19d6a
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-04-setup-wizard.md", "sha256": "316f6942bc68973e8f33af15fb10de8924146114fc3c85afb28588f3d8c617b4", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1-docket.md", "sha256": "0ff18ff1c6c68ec14e2fbe1e03164a8f4a1e1115c04940208a0af909d89f97c0", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1.diff", "sha256": "02eff5c492d485e0406ae10dae661bab5b06a02b17dffc419576dc9fe6492a50", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/setup-slice1-watcher.json", "sha256": "a3a3d4392e1e7f96365ea7620a2cafad978f5664a5d8fc62a469c82efbab4510", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "bb8a342b61b5f84e1b7b02212a2688c0879339c316776fc40f7df5fde88247b4", "opus": "ffe75711b91c191bb3815388ddc88469c7eec18d81d74a4b513f22f791bf727d"}

## MSG-40 | 2026-08-12T19:16:20+00:00 | from: opus | type: verdict | thread: setup-wizard-slice1-branch-r3 | refs: -

## Verification run

Command run literally, from `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/b5afcb9d93f8cfe67a7236f43307d376921c3db8/opus` (confirmed by `pwd`), no prefix/suffix/pipe:

`python -m pytest -q`

Result: `408 passed, 1 skipped in 16.81s` (progress dots showed a single `s` at ~70%). A post-run `ls -la` of the export root shows the same 17 entries and the same 12:09 mtimes as before the run, with no `.pytest-tmp`/`.pytest_cache` residue — the pinned source is byte-untouched.

## Criterion-1 checks against the pinned export and `setup-slice1.diff`

Read in full: `setup-slice1.diff`, `src/debate/setup.py`, `src/debate/__main__.py` (setup branch + `_watcher_config`), `src/debate/watcher.py` (`WatcherConfig`, `managed_problem`, `command_for`), `src/debate/protocol_template.md`, `PROTOCOL.md`, `tests/test_setup.py`, `tests/test_output_is_ascii.py`, `pyproject.toml`, `src/debate/channel.py` (config load / `init_channel`).

- **§2.1 interview/apply split.** `interview()` (setup.py:244) takes an injectable `ask` and does no writes; `apply()` (setup.py:197) validates then writes, its only extra I/O being a scratch `TemporaryDirectory` probe. Flags are the interview: `--command`/`--human` populate `flag_commands` in `__main__.py:429-437` and covered parties are never asked (`open_parties` filter, setup.py:261). `--yes` with a party covered by neither flags nor cache refuses (setup.py:276-279; `test_yes_without_defaults_or_flags_refuses`).
- **§2.2 derived-never-asked.** `derive_paths` (setup.py:112-124): config `<toplevel>/{name}.watcher.json`, state `~/.local/state/debate/{name}.json`; unit name `debate-watch-{channel_name}` in `closing_hints` — one id for all three, matching `debate-watch-<state stem>`. Toplevel is the channel's recorded `project` when present, else the root's parent, and `__main__.py:443` passes `chan_config.project`.
- **§2.3 writes.** Config, `PROTOCOL.md` only-if-absent (`scaffold_protocol` returns `None` when the target exists; thread-cap bracket filled by `.replace("[12]", ..., 1)` — the first `[12]` in the template is the "Thread cap:" line, the earlier brackets are `[your call …]`/`[usually no]`), and the defaults cache carrying `"channel": spec.channel_name` provenance, surfaced in the next run's prompt. The tool never edits `.gitignore`: `config_is_gitignored` only runs `git check-ignore -q` and `closing_hints` prints the line to add.
- **§2.4 prompt + engine.** `PROMPT_TEMPLATE` (setup.py:35-46) carries every incident clause: PROTOCOL.md first, `debate read` only ("never the whole mailbox"), the two-gate check ("NON-EMPTY thread AND turn=='{party}' — if either fails, exit without posting"), fresh own evidence never the request's, review-appended-as-a-dated-section-at-the-END-never-edit-the-body, post-then-stop; both `debate read` and `debate post` address `--root {channel_root} --channel {channel_name}`. `command_for` (watcher.py:197-202) chains both replacements on the prompt text in one expression and then substitutes `{prompt}` into argv in a single comprehension — argv is never re-scanned.
- **§2.6 validation before writes, real loader.** `apply` calls `validate` first (no writes there — the state dir is only `mkdir`'d at setup.py:234, after the gate), writes the probe into a `TemporaryDirectory` outside every target path, and `load_config_fn` is a **required** positional-capable parameter with no default (setup.py:197-198); `__main__.py:452` passes the real `_watcher_config`, and every `setup.apply(...)` call in `tests/test_setup.py` supplies it too. `_watcher_config` binds the channel record, so `WatcherConfig.__post_init__`'s state-inside-the-root refusal and then `managed_problem()` fire at setup time.
- **Packaged template.** `src/debate/protocol_template.md` and root `PROTOCOL.md` read identically line-for-line (159 lines each), and `test_packaged_template_matches_repo_protocol` pins byte equality via `resources.files("debate")`; it is in the passing run. `pyproject.toml:40-43` ships it as package data.
- **Secrets.** `SECRET_PATTERN` is applied per argv element in `validate` before the config dict is assembled, so a refusal happens before any config text exists; `--api-key=sk-…`, bare `--token`, `secret`, `bearer`, `password`, `credential` all trip it (`test_inlined_credential_is_refused`, `test_flag_form_credential_is_refused_too`). Generated prompts are template-derived and carry no operator input.

## Round-2 folds, verified independently

1. Loader is required — no default on `load_config_fn`; the managed gate cannot be skipped.
2. ASCII sweep widened: `tests/test_output_is_ascii.py:127-129` globs `src/debate/*.py` and calls `_sweep_one_module` on each. I confirmed `src/debate` has no subpackages (`__init__.py`, `__main__.py`, `channel.py`, `controller.py`, `setup.py`, `watcher.py`), so a non-recursive glob is in fact every module. `setup.py`'s em-dashes and `§` live only in comments/docstrings, which the sweep exempts by design.
3. Flag-form credentials refuse (see above).

Round-1 folds also hold: the `managed_problem()` refusal quotes the watcher's own words (`test_human_seat_on_managed_channel_refuses_at_setup_time` asserts `INVALID.*missing adapter command` and that the state dir does not exist afterwards); validation writes nothing.

## The two judgment calls the docket asked for

**managed-version-2 refusal: accept.** A v2 config is `adapters`/`runtime_root`/`source_ref`/`docket_files`, not `commands`/`prompts`; a wizard-written v2 config would be rejected downstream anyway (`managed_problem`: "managed-version 2 requires two brokered adapter profiles"), just later and less legibly. Refusing early at `__main__.py:423-428` with a pointer at a real artifact and a real subcommand is the right narrowing — I verified `watcher.brokered.example.json` exists at the export root and `adapter-doctor` is a genuine subcommand (`__main__.py:352` parser, `:567` dispatch), so the pointer is not aspirational.

**`.gitignore` adding `*.watcher.json`: accept.** It is the repo adopting the hint the tool prints for its own generated file. No tracked file is shadowed: a glob for `**/*.watcher.json` over the export returns nothing, and the committed samples (`watcher.example.json`, `watcher.brokered.example.json`) do not end in `.watcher.json`.

**Keeping `--human`: right, narrowly.** It is not dead: `load_config` leaves `managed_version` at `None` for records that lack the key (channel.py:410), so a named pre-0.5 channel still accepts a human seat; on managed v1 it converts what would otherwise be a bare `--yes` refusal into the watcher-worded explanation.

## Non-blocking notes (none affect this verdict)

- `--human`'s help text ("mark a party human-driven … skips its question") does not warn that on a managed-v1 channel it always ends in a refusal; one clause would save a round trip.
- `test_protocol_scaffolded_when_absent_and_never_clobbered` asserts `"[9]" in text and "[12]" not in … or "[9]" in text`, which reduces to `"[9]" in text`. The clobber half of the test is solid; the bracket half is weaker than it reads.
- `SECRET_PATTERN` is a shape guard, as its own comment says: an opaque credential with no key-ish word (or a wrapper path containing "token") is a miss/false-positive respectively. Consistent with §2.5 putting keys in wrappers, so not a gate failure.
- `apply` writes the config before scaffolding PROTOCOL.md and the cache; a failure in between leaves a config with no PROTOCOL.md. Cheap to re-run, and PROTOCOL.md is never clobbered.

Every criterion-1 check holds on my own reading and the docket command passes on my own fresh run, so: **PASS**.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 8844af6d10d35fbd844723dd68b66d261de1dec2e90590e4a19ba513fc2ec41c
- phase: sealed
- captured-at: 2026-08-12T19:13:53+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: a3a3d4392e1e7f96365ea7620a2cafad978f5664a5d8fc62a469c82efbab4510
- source-ref: b5afcb9d93f8cfe67a7236f43307d376921c3db8
- source-manifest-sha256: ffe75711b91c191bb3815388ddc88469c7eec18d81d74a4b513f22f791bf727d
- docket-revision-sha256: f8f9a7ec711c6e1565ca09fc78d6c81a1c8076e7acc1d259ece049fe3ab19d6a
- input-sha256: f4fc819dfd846734f404f5c4f1c57b2fd19e9b4b0f2fa893eddfde8b40df4d95
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-41 | 2026-08-12T19:16:20+00:00 | from: codex | type: verdict | thread: setup-wizard-slice1-branch-r3 | refs: -

Inspected the complete pinned diff and plan against the source export. Verified setup's interview/apply validation flow, channel-id-derived paths, non-clobbering PROTOCOL/defaults writes, no tool .gitignore edit, complete prompt clauses and single-pass {channel_name} expansion, required real-loader round-trip before target writes, byte-equal packaged protocol template, credential guards including --token, widened ASCII sweep, and managed-v2 refusal pointing to watcher.brokered.example.json and adapter-doctor. Exact verification command: `python -m pytest -q` Result: `408 passed, 1 skipped in 17.84s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 8844af6d10d35fbd844723dd68b66d261de1dec2e90590e4a19ba513fc2ec41c
- phase: sealed
- captured-at: 2026-08-12T19:16:20+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: a3a3d4392e1e7f96365ea7620a2cafad978f5664a5d8fc62a469c82efbab4510
- source-ref: b5afcb9d93f8cfe67a7236f43307d376921c3db8
- source-manifest-sha256: bb8a342b61b5f84e1b7b02212a2688c0879339c316776fc40f7df5fde88247b4
- docket-revision-sha256: f8f9a7ec711c6e1565ca09fc78d6c81a1c8076e7acc1d259ece049fe3ab19d6a
- input-sha256: 07adc5e010dadf26f5d8827820504ad0a833bb74132bc4bbab4dd1890343fab0
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-42 | 2026-08-12T19:16:20+00:00 | from: owner | type: close | thread: setup-wizard-slice1-branch-r3 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-43 | 2026-08-12T19:36:31+00:00 | from: owner | type: review-request | thread: setup-wizard-slices23-branch | refs: feature/setup-wizard-slices23@f8a92cc537f07e217e8f3199bb8dbf2e6bee70e1

Branch gate: feature/setup-wizard-slices23@f8a92cc (PR #11) — slices 2 (--smoke: scratch-channel round trip, spend announced first, seat-contract-only claims, scratch always removed) and 3 (--scheduler: printed-never-run house-template units, withheld on smoke failure) of the APPROVED setup-wizard plan. Docket setup-slices23-docket.md; full diff enclosed. Merge only on terminal PASS + green CI.

## MSG-44 | 2026-08-12T19:44:01+00:00 | from: opus | type: verdict | thread: setup-wizard-slices23-branch | refs: -

**PASS** — every criterion-1 check holds against my own reads of the pinned export, and the mandated command passes on my fresh run.

**Fresh command and result.** Run literally from the export root (`pwd` = `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/f8a92cc537f07e217e8f3199bb8dbf2e6bee70e1/opus`), no prefix, suffix, pipe or env diagnostics:

```
python -m pytest -q
```
```
........................................................................ [ 17%]
........................................................................ [ 34%]
........................................................................ [ 52%]
........................................................................ [ 69%]
s....................................................................... [ 87%]
.....................................................                    [100%]
412 passed, 1 skipped in 17.31s
```

**Diff vs. export.** I read `setup-slices23.diff` in full and confirmed the export IS the post-slice tree: `src/debate/setup.py:302-402` (`smoke`, `scheduler_units`), `src/debate/__main__.py:267-277` (flags) and `:452-502` (setup branch), and `tests/test_setup.py:246-340` are byte-consistent with the diff hunks.

**Slice 2 (`--smoke`).**
- Opt-in only: the sole call site is `__main__.py` under `if args.smoke:`; nothing else invokes `setup_mod.smoke`.
- Scratch root carries a PROTOCOL.md: `setup.py:330-333` calls `channel.init_channel(scratch, ...)` then setup's own `scaffold_protocol(scratch, spec.thread_cap)` (`setup.py:140-153`), so R2 precision note 1's false-negative (bare `init_channel` root, whose first prompt instruction "First read {channel_root}/PROTOCOL.md" would have no target) cannot occur.
- Probe is an `info` from the other party (`other = next(p for p in spec.parties if p != party)`, `entry_type="info"`). `info` is a legal opener: `channel.py:70` `OPENER_TYPES = ("review-request", "question", "info", "close")`, enforced at `channel.py:622`; with no thread open the turn-alternation guard (`channel.py:629`) does not bind, so the probe lands and hands the turn to the seat.
- Real pinned prompt, correct expansion order: `build_prompt(party)` returns the same `PROMPT_TEMPLATE` (`setup.py:35-46`) that `apply()` writes into `prompts`. `setup.py:338-341` expands `{channel_root}` then `{channel_name}` in the prompt text, then `{prompt}` into argv parts — identical to `WatcherConfig.command_for` (`watcher.py:190-197`), whose single-pass order is pinned at MSG-122; argv is never re-scanned.
- Spend announced before the model call: `emit("smoke {party}: about to spend ONE model call ...")` at `setup.py:317-319` precedes `subprocess.run` at `:342`.
- Pass states its limits plainly: `:347-350` — "seat contract only: turn-gate, read, post; NOT consistency or review quality".
- Failures carry reason and output tail: `:355-358` reports exit code plus a 160-char stdout/stderr tail; the launch-failure branch reports the OSError/SubprocessError reason.
- Scratch removed on every path: `try/finally: shutil.rmtree(scratch, ignore_errors=True)` (`:359-360`) wraps everything after `mkdtemp`, including the `continue`.
- Real channel untouched: every write in `smoke` targets `scratch`; `spec.channel_root` is only read.

**Slice 3 (`--scheduler`).** `scheduler_units` (`setup.py:371-402`) returns strings only — no `systemctl`, no `subprocess`, no file write; `__main__.py:481-499` prints the units and prints (does not run) the install line. House template present: `Type=oneshot`, `WorkingDirectory=`, `Environment=PYTHONPATH=`, `SyslogIdentifier=debate-watch-<id>`, `ExecStart=... watch-once --root ... --channel <id> --config ...`, timer `OnUnitActiveSec=1min` / `WantedBy=timers.target`. Naming matches the house convention `debate-watch-<state-file-stem>` (`watcher.py:437`, `README.md:283`), and the stem is the channel id by `derive_paths`. No credential can reach a unit: the text is built solely from `sys.executable`, resolved paths and the channel id — seat argv is never interpolated — and `validate()`'s `SECRET_PATTERN` (`setup.py:52-54`, `:168-172`) already refuses key-shaped argv. Withholding is correct: `__main__.py:482-486` prints "scheduler output withheld: fix the failing seat first" and skips generation whenever a requested smoke failed (review fold c), exiting 4.

**Review-fold discipline.** ASCII invariant holds — the widened AST sweep over every `src/debate/*.py` module (`tests/test_output_is_ascii.py:118-156`) passed in the run above, covering the new `setup.py` and `__main__.py` literals. The required loader is unchanged: `apply(spec, load_config_fn)` still has no default (`setup.py:198-199`) and `__main__.py:465` passes `_watcher_config`. No new fail-open default: the only added defaults are `SetupSpec.supervisor="owner"`, `interview(supervisor="owner")` and `smoke`'s test seams (`scratch_base`, `emit`); the CLI always passes the channel's real `chan_config.supervisor` (`__main__.py:455`), and the default path fails closed (three-way distinctness in `init_channel`) rather than skipping a gate.

**Non-blocking observations** (neither is a docket criterion): a `subprocess.TimeoutExpired` failure carries the reason but not the captured output tail, unlike the no-reply branch; and `--smoke` on a spec with no watcher-driven seat returns an empty failure list silently (unreachable for managed channels, which `apply()` already refuses for human-driven seats).

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: bbb83b609bb98e50c67384715244ac830515bf422fb60d04d33ac703c1cbe9cb
- phase: sealed
- captured-at: 2026-08-12T19:44:01+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: c29890006a837abee77782a034db287221bfb30087ecded6ec1a27b08670be37
- source-ref: f8a92cc537f07e217e8f3199bb8dbf2e6bee70e1
- source-manifest-sha256: 114a922306a1c006718f39f949264dba250c6061d80e1e815bda78347727bc40
- docket-revision-sha256: 44f48de5f08ad0075bfef334dd93332ace1a5e836705754a958e63549892a96d
- input-sha256: 448de2bab3752df97d08e294017bf73b572d74bbef5899a0065aaf4ea61daa2d
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-45 | 2026-08-12T19:44:01+00:00 | from: codex | type: verdict | thread: setup-wizard-slices23-branch | refs: -

Verified the immutable docket, full setup-slices23.diff, approved plan, and pinned source implementations in src/debate/setup.py, src/debate/__main__.py, src/debate/watcher.py, src/debate/channel.py, and tests/test_setup.py. Slice 2 uses a protocol-scaffolded scratch channel, legal info opener, pinned-prompt single-pass expansion, pre-spend notice, cleanup, and failure reporting; Slice 3 only generates text and withholds scheduler output after smoke failure. The required loader remains mandatory and the package-wide ASCII AST sweep remains present. Fresh command run exactly: `python -m pytest -q` -> `412 passed, 1 skipped in 18.03s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: bbb83b609bb98e50c67384715244ac830515bf422fb60d04d33ac703c1cbe9cb
- phase: sealed
- captured-at: 2026-08-12T19:39:23+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: c29890006a837abee77782a034db287221bfb30087ecded6ec1a27b08670be37
- source-ref: f8a92cc537f07e217e8f3199bb8dbf2e6bee70e1
- source-manifest-sha256: b75f73ed5d1ef4167d338f7e8757f80979e916d2d4d34714b6827a291969ec4e
- docket-revision-sha256: 44f48de5f08ad0075bfef334dd93332ace1a5e836705754a958e63549892a96d
- input-sha256: 4482f16d618a50f66f2373d69a1b2cb38c8b0338f459280a01b8f39f0634ad01
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-46 | 2026-08-12T19:44:01+00:00 | from: owner | type: close | thread: setup-wizard-slices23-branch | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-47 | 2026-08-12T19:44:34+00:00 | from: owner | type: review-request | thread: setup-wizard-slices23-amendment | refs: feature/setup-wizard-slices23@72464097c679cc4aed891e0012c77cc43261386a

Amendment round: one TEST-ONLY commit past the MSG-44/45 PASS (portable python fake seats for Windows lanes + fake-seat regex fix). Full amendment diff in the docket; product code untouched; CI green at this ref. Merge only on PASS.

## MSG-48 | 2026-08-12T19:50:44+00:00 | from: opus | type: verdict | thread: setup-wizard-slices23-amendment | refs: -

PASS — amendment round, feature/setup-wizard-slices23 (export ref 72464097c679cc4aed891e0012c77cc43261386a).

## Command run (exactly as the docket specifies, no prefixes/suffixes/pipes)

`python -m pytest -q`, run in the pinned export root `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/72464097c679cc4aed891e0012c77cc43261386a/opus`.

Result (run twice, identical both times):

```
........................................................................ [ 17%]
........................................................................ [ 34%]
........................................................................ [ 52%]
........................................................................ [ 69%]
s....................................................................... [ 87%]
.....................................................                    [100%]
412 passed, 1 skipped in 17.68s
```
(second run: `412 passed, 1 skipped in 17.14s`)

## The amendment commit (setup-slices23-amendment.diff)

Verified test-only: the diff touches `tests/test_setup.py` and nothing else — no `src/`, no docs, no config. Both changes are portability fixes, and the export tree matches the diff's post-state:

- `replying_seat` (tests/test_setup.py:248-264) now returns `[sys.executable, str(script), "{prompt}"]` writing a `.py` fixture instead of a `chmod +x` `#!/bin/sh` script, so a Windows lane does not have to exec a shell script. The channel-id capture is now `re.search(r"--channel ([A-Za-z0-9-]+)", prompt)` — the character class cannot swallow the pinned prompt's backtick (the old `sed 's/.*--channel \([^ ]*\).*/\1/p'` captured any non-space run, backtick included).
- The prose/silent fixtures (tests/test_setup.py:286-299) are likewise `.py` files invoked via `sys.executable`. The failure assertions are unchanged in strength: still `len(failures) == 2`, still `"no reply landed"` in every reason, still `"sure, I will"` present (output tail proven shown), still `not list(tmp_path.glob("debate-smoke-*"))`.

The fixtures still honour the real contract — parse `--root`/`--channel` out of the pinned prompt, read the open thread from `<chan>.signal.json`, post via the real `debate post` CLI — so the pass case is not weakened into a stub.

## Criterion-1 checks against the pinned export

Slice 2 (`--smoke`), src/debate/setup.py:302-356 and src/debate/__main__.py:271, 467-472:
- Opt-in only: `--smoke` exists solely on the setup parser and is read only at `__main__.py:468` (`if args.smoke:`); nothing runs otherwise.
- Scratch root carries a PROTOCOL.md: `init_channel` + `scaffold_protocol(scratch, spec.thread_cap)` (setup.py:324-326) — setup's own write path, so a correct seat does not false-negative at its first instruction.
- Probe is an `info` from the other party: `other = next(p for p in spec.parties if p != party)` (setup.py:319), `channel.post(..., sender=other, entry_type="info", ...)` (setup.py:327). `info` is a legal opener — `OPENER_TYPES = ("review-request", "question", "info", "close")` at channel.py:70, enforced at channel.py:622.
- Real pinned prompt, correct expansion order: `build_prompt(party)` (the same function `apply` writes into the config, setup.py:209) with `{channel_root}`/`{channel_name}` replaced first, then `{prompt}` substituted into argv, argv never re-scanned (setup.py:332-335) — byte-for-byte the order of `WatcherConfig.command_for` (watcher.py:197-202).
- Spend announced before the model call: the `about to spend ONE model call` emit is at setup.py:317-318, ahead of scratch creation and `subprocess.run` (setup.py:337).
- Pass states the limit plainly: `seat contract only: turn-gate, read, post; NOT consistency or review quality` (setup.py:346-348).
- Failures carry reason and tail: `no reply landed in the scratch mailbox (exit {returncode}; output tail: {tail!r})` (setup.py:350-353).
- Scratch removed on every path: `try: ... finally: shutil.rmtree(scratch, ignore_errors=True)` (setup.py:322/354-355); the exception branch's `continue` (setup.py:342) still runs the `finally`.
- Real channel untouched: every write in `smoke` targets `scratch`; `spec.channel_root` is never written.

Slice 3 (`--scheduler`), setup.py:359-401 and __main__.py:473-489:
- Text only: `scheduler_units` returns a dict of strings and writes no file; `__main__` only `print`s. `systemctl` appears nowhere except inside the printed `install (not run for you): ...` string (__main__.py:487-488) — a repo-wide grep for `systemctl`/`subprocess.run` under `src/debate` shows no execution path from the scheduler code.
- House template honoured: `Type=oneshot`, `WorkingDirectory=`, `Environment=PYTHONPATH=`, `SyslogIdentifier=debate-watch-<id>`, `ExecStart=... watch-once --root ... --channel <id> --config ...`, timer `OnUnitActiveSec=1min` / `WantedBy=timers.target`. Naming is `debate-watch-{spec.channel_name}`, and since `derive_paths` makes the state stem the channel id (setup.py:124) this agrees with the `debate-watch-<state-stem>` convention pinned in README.md:280-287 and tests/test_unit_naming.py.
- No credential can appear in a unit: unit text is composed only of `sys.executable`, the resolved root/config/workdir/PYTHONPATH and `state_path.name`; seat argv (the only credential-adjacent field, itself guarded by `SECRET_PATTERN` at setup.py:52-54/167-172) never enters the unit.
- Withheld on a failed requested smoke: `if smoke_failed: print("scheduler output withheld: fix the failing seat first", file=sys.stderr)` (__main__.py:473-478), plus exit code 4 (__main__.py:492-493).

Review-fold discipline:
- ASCII sweep still widened and still green: `test_no_string_literal_in_the_watcher_can_carry_non_ascii` walks `src/debate/*.py` in a loop (tests/test_output_is_ascii.py:118-129), so `setup.py` is in scope; it passes in the run above.
- Loader still required: `apply(spec, load_config_fn: Callable[...])` has no default (setup.py:198-199) and `__main__` passes `_watcher_config` explicitly.
- No new fail-open default: `--smoke`/`--scheduler` are `store_true` (default off), a failed smoke both withholds the units and returns 4.

## On the two round-1 non-blocking observations — still non-blocking

- Timeout tail: `subprocess.TimeoutExpired` is a `SubprocessError`, so a timed-out seat lands in the `except (OSError, subprocess.SubprocessError)` branch (setup.py:340-341) and reports `seat command failed to run: <error>` without the captured output tail that the no-reply branch shows. The failure is still loud and named, and the timeout value is in the message; this is a diagnostic thinness on one branch, not a wrong result. Not blocking.
- Silent empty smoke: with `--smoke` and no watcher-driven seat, `driven` is empty and `smoke` returns `[]` with no output, so the run reads as a pass that tested nothing. On a managed v1 channel `apply` already refuses a human-driven seat (setup.py:227-232), which bounds the exposure to legacy/unmanaged channels, and the smoke genuinely cannot exercise a human seat. Worth a line of output in a future slice; not blocking.

Nothing else from my inspection is blocking. Both docket criteria are met: the command passes at this ref, and every criterion-1 check holds against the pinned export.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: e2829d1427b896e9955ca5c810d06359920a1c06138cb91a60611bf03f5acaf0
- phase: sealed
- captured-at: 2026-08-12T19:48:39+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 361da312b477e93533765f62cca7fb7151be58304a0d0dc27a98b4274024e433
- source-ref: 72464097c679cc4aed891e0012c77cc43261386a
- source-manifest-sha256: a25fc7f773d9d75aed2ada0e3d723b27e3c9af3c7dbf9e83a882a7f292b58f56
- docket-revision-sha256: 89c3ef9b3fd9db78a93b20b0021ce2838680a6e794b042f1efd017e34b24284f
- input-sha256: 871bf60955e41bd2cc080d742b01e926dfb239931fb5ca4cf16c77526e963fd1
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-49 | 2026-08-12T19:50:44+00:00 | from: codex | type: verdict | thread: setup-wizard-slices23-amendment | refs: -

Verified the immutable docket hashes, the full slices23 and amendment diffs, and the pinned export's `src/debate/setup.py`, `src/debate/__main__.py`, `src/debate/watcher.py`, `src/debate/channel.py`, relevant tests, README, and CHANGELOG. `channel.OPENER_TYPES` includes `info`; smoke uses the scaffold path and pinned prompt with the same placeholder order as `WatcherConfig.command_for`; scheduler generation is text-only and is withheld after a requested smoke failure; the widened package AST ASCII sweep remains present. Fresh exact verification command: `python -m pytest -q` Result: `412 passed, 1 skipped in 18.22s`. The prior timeout-tail and zero-watcher-seat smoke observations remain non-blocking for this docket's stated criteria.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: e2829d1427b896e9955ca5c810d06359920a1c06138cb91a60611bf03f5acaf0
- phase: sealed
- captured-at: 2026-08-12T19:50:44+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 361da312b477e93533765f62cca7fb7151be58304a0d0dc27a98b4274024e433
- source-ref: 72464097c679cc4aed891e0012c77cc43261386a
- source-manifest-sha256: 54add63f8a9128327f5996c6db9abd48860e170a30ade2d38a4042173413707e
- docket-revision-sha256: 89c3ef9b3fd9db78a93b20b0021ce2838680a6e794b042f1efd017e34b24284f
- input-sha256: 54ed7cd7dfb57eb5ef54e23125a0dd824c1c95bd156d03b937369c0ebb428e1c
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-50 | 2026-08-12T19:50:44+00:00 | from: owner | type: close | thread: setup-wizard-slices23-amendment | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-51 | 2026-08-12T19:57:54+00:00 | from: owner | type: close | thread: record-recovery-2026-08-12 | refs: -

RECORD RECOVERY NOTE (one-shot close-correction idiom). On 2026-08-12, after merging PR #11, the operator seat (claude dev session) ran a git file-restore against this mailbox while it held eight entries not yet committed to git, truncating MSG-43..50 from the file; the doorbell stayed at seq 50. The entries were reconstructed from the controller's persisted case state (sealed_submissions, terminal fields) and invocation results, using a pipeline FIRST validated byte-equal against the still-committed MSG-40..42, with the two review-request bodies restored verbatim from the posting session's transcript. The pre-recovery truncated file is preserved at var/debate/repository-unattended-02750/mailbox-truncated-backup-2026-08-12.md and the script at var/debate/repository-unattended-02750/recover_entries.py. The owner approved the reconstruct-and-restore path in the remote session before any write. Lesson recorded: never point git file-restore at a live channel record; commit the record chore BEFORE any git operation touching collab/.

## MSG-52 | 2026-08-12T23:09:00+00:00 | from: owner | type: review-request | thread: plan-v060-release | refs: main@77c531ab8bda807e126799535f8a8d352d91ecb5

Plan-doc gate: the v0.6.0 release plan (docs/plans/2026-08-12-v0.6.0-release.md, materialized in the docket) reviewed against main@77c531a before any execution. The release ships the completed setup wizard. Flow is the owner-approved v0.5.0 precedent including its gate folds; criteria in plan-v060-docket.md — check README's current count/version claims against the export yourself.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- docket-revision-sha256: 495ce16a403f9329e73b28b7b897c57dcba30703957a0020cb52dd09f5350a21
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-12-v0.6.0-release.md", "sha256": "2c39e778195d3a6c81f09e99c76ae710c96b3e4fd00bb233e1bbe2bad03d20d4", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-07-v0.5.0-release.md", "sha256": "8cb05b7f5395330d52b3efcde56a60270cb9b2ac30f6e54ddf907fb496aa59fa", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v060-docket.md", "sha256": "df020611ecac072d5f5ba73796a4b09ee0184ef25bbd4069041397ff0519e11c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v060-watcher.json", "sha256": "c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "d2719267b1a6ad7305decc332de5f8c6960721e1126a02a981bd7180265820ad", "opus": "8d28d22a5af95055649342b8d834504312cff34516fefbf02f72820a8ea0f50d"}

## MSG-53 | 2026-08-12T23:16:38+00:00 | from: opus | type: verdict | thread: plan-v060-release | refs: -

NO_PASS — the docket command passes, but criterion 1 fails on one stale public claim the plan's step-4 sweep is not written to catch.

VERIFICATION COMMAND (run literally in the pinned export root, no prefix/suffix/pipe):
`python -m pytest -q tests/test_release_sync.py`
Result: `.                 [100%]` / `1 passed in 0.08s`.

WHAT CHECKS OUT (export at 77c531a):
- Four version strings all read 0.5.0: pyproject.toml:7, src/debate/__init__.py:42, .claude-plugin/plugin.json:3, .claude-plugin/marketplace.json:9 — and tests/test_release_sync.py:11-23 is exactly the four-way lockstep the plan's step 2 leans on.
- CHANGELOG.md:9 carries `## Unreleased` with the wizard content the plan describes: `debate setup`, `--smoke`, `--scheduler`, and the `{channel_name}` prompt expansion. src/debate/setup.py and tests/test_setup.py exist, and __main__.py:246-282 registers exactly the flags the plan and README name (`--command`, `--human`, `--yes`, `--smoke`, `--scheduler`, plus the shared `--root`/`--channel`).
- Step 8 matches .github/workflows/release.yml as shipped: the `gate` job is 2 OS x 2 Python = 4 lanes (release.yml:19-35, same matrix as ci.yml:13-30), the publish pre-flight asserts tag == pyproject == `__version__` and a non-empty `## <tag>` CHANGELOG section BEFORE `python -m build` and the PyPI upload (release.yml:55-79), and `github-release` sources notes from that same section (release.yml:87-117). The step-3 heading form `## v0.6.0 — <UTC date>` satisfies the workflow's `^## v0.6.0(?=[ \t]|$)` anchor.
- Language rules hold in the export: no occurrence of "unforgeable" in any .md, and the only "final" is "the final CLIs reported" (README.md:521); README.md:512 already says "The first end-to-end proof is MSG-11..14".
- The plan is right that the counts are stale, and it under-states by how much. My own inspection: `python -m pytest -q --collect-only` → `413 tests collected in 0.63s` (README.md:475 claims 395); `wc -l src/debate/*.py` → `5488 total` (README.md:474 claims "about 4,900 lines"). Step 4's "recount at commit time" covers this.

BLOCKING FINDING — stale public claim outside step 4's sweep:
README.md:50-51 still tells readers that the 0.3.x fixed-filename layout (`CHANNEL.md`/`signal.json`/`debate.json`) is "still fully supported; see `debate migrate`". That was made false by the release this plan builds on: CHANGELOG.md:106-111 (`### Deprecated`) says posting to those legacy-layout channels "is deprecated as of 0.5", and README.md:389-391 says the same thing in its own "Upgrading from 0.3.x" paragraph. So the README asserts full support in the intro and deprecation 340 lines later. Step 4 sweeps only "the honest numbers", `MSG-`, "in 0.5"/"as of" forward references, and wizard flags; README.md:50-51 contains none of those tokens, so the sweep as written passes over it. This ships on the PyPI project page (pyproject.toml:9 sets `readme = "README.md"`), so v0.6.0 would republish the contradiction. Fix: make line 50-51 say the legacy layout keeps working but is deprecated since 0.5, and widen step 4's sweep to support-status/`0.3.x` wording, not just counts and `MSG-`/version-forward-reference tokens.

TWO NOTES, NOT COUNTED AS BLOCKING:
1. Unverifiable-from-export context claims: the plan's "merges 0fd806b and 55a4f8c" and "gate records through MSG-51 committed" cannot be checked here — the export separates `collab/` and `.git` (there is no `collab/` directory in the export, and git is unreachable), and the docket materialized only collab/PROTOCOL.md and collab/repository-unattended-02750.debate.json, neither of which is the channel record. Everything about those merges that the export can corroborate (setup.py, its tests, the Unreleased entries) is consistent with the plan. I did not treat this as a defect of the plan, only as a limit on what I could confirm.
2. The shipped `{channel_name}` prompt placeholder (CHANGELOG.md:38-42) is absent from the README watcher-config section (README.md:264-278 shows only `{prompt}`). `{channel_root}` was never documented there either, so this is a pre-existing doc gap rather than a claim made stale by v0.6.0 — worth folding into step 4 while it is open.

Re-case after the README.md:50-51 fix and a widened step-4 sweep; everything else in the plan matches the export.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 160db9be503298d22e5985e66010a6c7ccb7fa4455dd1de6b5e0a28da1c69da3
- phase: sealed
- captured-at: 2026-08-12T23:16:38+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- source-manifest-sha256: 8d28d22a5af95055649342b8d834504312cff34516fefbf02f72820a8ea0f50d
- docket-revision-sha256: 495ce16a403f9329e73b28b7b897c57dcba30703957a0020cb52dd09f5350a21
- input-sha256: 8752e3457f46c7940e73e078d29dd84ed7e8f556c74a2162cd20f3ba64d07158
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-54 | 2026-08-12T23:16:38+00:00 | from: codex | type: verdict | thread: plan-v060-release | refs: -

PASS. Fresh verification ran exactly `python -m pytest -q tests/test_release_sync.py` in `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/77c531ab8bda807e126799535f8a8d352d91ecb5/codex` and returned `1 passed in 0.08s`. I checked `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/77c531ab8bda807e126799535f8a8d352d91ecb5/codex/CHANGELOG.md`, `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/77c531ab8bda807e126799535f8a8d352d91ecb5/codex/README.md`, the four 0.5.0 version locations, and `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/77c531ab8bda807e126799535f8a8d352d91ecb5/codex/.github/workflows/release.yml`. The plan accurately covers the Unreleased wizard work, four-way bump, four-lane release gate/pre-upload version-and-notes checks, and GitHub Release creation. README's stale 4,900-line/395-test claim is explicitly swept and recounted; its `as of 0.5` wording falls within the planned forward-reference sweep. The plan preserves tamper-evident wording and prohibits final/unforgeable release language.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 160db9be503298d22e5985e66010a6c7ccb7fa4455dd1de6b5e0a28da1c69da3
- phase: sealed
- captured-at: 2026-08-12T23:11:10+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- source-manifest-sha256: d2719267b1a6ad7305decc332de5f8c6960721e1126a02a981bd7180265820ad
- docket-revision-sha256: 495ce16a403f9329e73b28b7b897c57dcba30703957a0020cb52dd09f5350a21
- input-sha256: 7b0b15ebecbca25abdbef63ea08f8525f872ea016437c10059c870811d074d76
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-55 | 2026-08-12T23:20:31+00:00 | from: codex | type: verdict | thread: plan-v060-release | refs: -

Ran exactly `python -m pytest -q tests/test_release_sync.py` in the pinned export; result: `1 passed in 0.08s`. Blocking finding: README.md:50-51 says legacy 0.3.x fixed-filename channels are “still fully supported,” but README.md:389-391 and CHANGELOG.md:107-110 correctly say posting to them has been deprecated since 0.5 (while still working). Plan step 4 only sweeps counts, `MSG-`, “in 0.5”/“as of” references, and wizard claims, so it would not catch this contradictory public support-status claim before the README is republished to PyPI. Amend the README wording and explicitly widen step 4 to sweep legacy-layout/0.3.x support-status claims. The four 0.5.0 version locations, Unreleased wizard entries, release.yml's four-lane gate/pre-upload checks, and language rules otherwise match the export.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- source-manifest-sha256: d2719267b1a6ad7305decc332de5f8c6960721e1126a02a981bd7180265820ad
- docket-revision-sha256: 495ce16a403f9329e73b28b7b897c57dcba30703957a0020cb52dd09f5350a21
- input-sha256: 501b61f5ff50cb6686d76f4dc1be02af2bba802209cca44892d4055d3aa662f3
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-56 | 2026-08-12T23:20:31+00:00 | from: owner | type: close | thread: plan-v060-release | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-57 | 2026-08-12T23:21:17+00:00 | from: owner | type: review-request | thread: plan-v060-release-r2 | refs: main@77c531ab8bda807e126799535f8a8d352d91ecb5

Plan gate round 2: the v0.6.0 release plan with the MSG-53/55 finding folded (README:50-51 support-status fix leads step 4; sweep widened to legacy-layout support-status wording; reviewers' own counts adopted; {channel_name} doc gap folded). Docket carries the round-1 summary.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- docket-revision-sha256: d5e4847d51ba3c29dcb0186a7af0eb176cc9cbe1e71214dcec9ce80550725905
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-12-v0.6.0-release.md", "sha256": "9fffd0ae77a9da46db77847b23740090c386ab70d3f6635376d63b37d56199bc", "tracked_at_source_ref": false}, {"path": "docs/plans/2026-08-07-v0.5.0-release.md", "sha256": "8cb05b7f5395330d52b3efcde56a60270cb9b2ac30f6e54ddf907fb496aa59fa", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v060-docket.md", "sha256": "30c80e89d4b3b3b5d1d241291111b2d4e463b50ec80eecc643f717f49e21e109", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-v060-watcher.json", "sha256": "c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "d2719267b1a6ad7305decc332de5f8c6960721e1126a02a981bd7180265820ad", "opus": "8d28d22a5af95055649342b8d834504312cff34516fefbf02f72820a8ea0f50d"}

## MSG-58 | 2026-08-12T23:25:56+00:00 | from: opus | type: verdict | thread: plan-v060-release-r2 | refs: -

PASS — round-1 fold verified against the pinned export; verification command green.

VERIFICATION (run literally in the export root, no prefixes/pipes):
`python -m pytest -q tests/test_release_sync.py`
→ `.                                       [100%]` / `1 passed in 0.08s`

CRITERION 1 — claims about main's state at 77c531a:
- Four lockstep version strings all read 0.5.0: pyproject.toml:7, src/debate/__init__.py:42, .claude-plugin/plugin.json:3, .claude-plugin/marketplace.json:9. tests/test_release_sync.py:11-23 is exactly the four-location enforcement step 2 cites (it asserts marketplace["metadata"]["version"]).
- CHANGELOG.md:9 carries `## Unreleased` with the wizard content the plan describes (`debate setup`, `--smoke`, `--scheduler`, and `{channel_name}` alongside `{channel_root}`); next heading is `## v0.5.0 — 2026-08-07` (CHANGELOG.md:44). Section headings observed: Unreleased, v0.5.0, v0.4.0, v0.3.1, v0.2.0, v0.1.1, v0.1.0.
- Shipped-behavior spot checks behind those entries: src/debate/__main__.py:242-280 defines exactly `--command/--human/--yes/--smoke/--scheduler` (the `--scheduler` help says "never installs or runs them", matching the CHANGELOG and README:107-110); src/debate/watcher.py:193-200 expands `{channel_root}` and `{channel_name}` in the same single pass, so the plan's engine claim is accurate.

ROUND-1 FINDING, FOLD CONFIRMED:
- README.md:50-51 still reads "Channels created by 0.3.x use the older fixed filenames … — still fully supported; see `debate migrate`", contradicting README.md:389-391 "posting to existing ones is deprecated as of 0.5". Step 4's first bullet now names this line explicitly and requires the intro to agree with the "Upgrading from 0.3.x" paragraph and the CHANGELOG. I grepped support-status wording repo-wide: skills/debate/SKILL.md:3,12, examples/glm-kimi.md:94, PROTOCOL.md:11 and docs/case-study.md:16 mention the legacy layout only descriptively (no support-status claim), so the repo-wide bullet is adequately scoped and README:50-51 is the only contradiction.

COUNTS — I recounted rather than trusting the plan:
- `python -m pytest -q --collect-only tests` → `413 tests collected in 0.65s`
- `find src -name '*.py' | xargs wc -l` → `5488 total`
The plan's folded figures (413 tests, 5,488 src lines) match my own counts exactly, and README.md:474-475 ("about 4,900 lines … with 395 tests as of this writing") is the stale claim step 4 bullet 3 targets. Those are the only occurrences of 395/4,900 anywhere in the export.

OTHER STALE-CLAIM SEARCH (docket's "count and version claims" prompt): the remaining README version references — :283 "Since 0.4", :379 "created before 0.4", :385 "Upgrading from 0.3.x", :390 "as of 0.5", :515-516 "the v0.5.0 release itself", :521 pinned CLI/profile figures — are historical statements that stay true after v0.6.0; the PyPI badge at :9 is dynamic. No file outside README/CHANGELOG hard-codes a release version except pyproject.toml:7 (covered by step 2). I found no stale public claim that step 4's sweep would miss.

WATCHER-DOC GAP: `{channel_name}` and `{channel_root}` appear nowhere in README.md (grep returned no hits, including the watcher-config section at :270-300), so the folded non-blocking item is a real pre-existing gap and step 4 bullet 5 covers it.

RELEASE PROCEDURE vs .github/workflows/release.yml as shipped: trigger `on: push: tags: ["v*"]` matches step 8's tag-push; the `gate` job is 2 OS × 2 Python = the 4 lanes the plan claims; the `publish` job's "Verify tag matches package version, and that notes exist" step runs before `python -m build`/`pypa/gh-action-pypi-publish`, i.e. it refuses on version or notes mismatch before the irreversible upload, exactly as step 8 states; `github-release` sources the body from the CHANGELOG section. Step 3's heading format `## v0.6.0 — <UTC tag date>` satisfies both jobs' `^## <tag>(?=[ \t]|$)` anchor.

LANGUAGE RULES: step 3 keeps "tamper-evident, never 'unforgeable'" and "nothing is called 'final'", consistent with README.md:467-473. Grep for `unforgeable` across README/CHANGELOG/PROTOCOL/docs/skills/.claude-plugin returned nothing; the single `final` hit is README.md:521 "the final CLIs reported a `$0.355168`", an ordinary adjective about the CLI versions, not a claim that the record is final. Step 0 flips the DRAFT header at gate-PASS before execution, per the v0.5.0 fold.

STATED LIMITATION (not blocking): the export separates `.git` and the live channel record per PROTOCOL.md §5, so I could not directly confirm merge SHAs 0fd806b / 55a4f8c or "gate records through MSG-51". Everything those claims imply that is observable in the export — the wizard surface, the ASCII/`{channel_name}` work, and the `## Unreleased` contents — checks out, and collab/repository-unattended-02750.debate.json in the docket confirms the managed-version-2 opus/codex channel with thread_cap 12 that step 6 targets.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 14942d372ee88bc563f75174e9dd7672f2d22acf3957e629b6ea885f29043515
- phase: sealed
- captured-at: 2026-08-12T23:23:59+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- source-manifest-sha256: 8d28d22a5af95055649342b8d834504312cff34516fefbf02f72820a8ea0f50d
- docket-revision-sha256: d5e4847d51ba3c29dcb0186a7af0eb176cc9cbe1e71214dcec9ce80550725905
- input-sha256: 8d92ce8fa87d6ebb34172feed2fa3294d1afe89881840b22b4547f7899565baa
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-59 | 2026-08-12T23:25:56+00:00 | from: codex | type: verdict | thread: plan-v060-release-r2 | refs: -

PASS. Fresh required command run in the pinned source export: `python -m pytest -q tests/test_release_sync.py` → `1 passed in 0.08s`. Inspected `README.md`, `CHANGELOG.md`, `.github/workflows/release.yml`, `pyproject.toml`, `src/debate/__init__.py`, both `.claude-plugin` manifests, `tests/test_release_sync.py`, and setup/watcher implementation. The four versions are 0.5.0, CHANGELOG has `## Unreleased` for the wizard, release.yml provides the four-lane gate and pre-upload version/notes check, and step 4 explicitly covers the found stale README legacy-support claim, counts, MSG/forward-reference sweep, and both watcher placeholders. Fresh collection output also reports 413 tests; `wc -l src/debate/*.py` reports 5,488 total source lines. No blocking stale public claim outside the planned sweep found; source uses tamper-evident and contains no unforgeable claim.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 14942d372ee88bc563f75174e9dd7672f2d22acf3957e629b6ea885f29043515
- phase: sealed
- captured-at: 2026-08-12T23:25:56+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: c161ec6513d4f4c78932501acfc31f0874662cc9c4234c7af7deb8efa36d028d
- source-ref: 77c531ab8bda807e126799535f8a8d352d91ecb5
- source-manifest-sha256: d2719267b1a6ad7305decc332de5f8c6960721e1126a02a981bd7180265820ad
- docket-revision-sha256: d5e4847d51ba3c29dcb0186a7af0eb176cc9cbe1e71214dcec9ce80550725905
- input-sha256: 7a831b0f14a14db73f063776f6fc51f391872dc17cb25b36c3d3bc682a379640
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-60 | 2026-08-12T23:25:56+00:00 | from: owner | type: close | thread: plan-v060-release-r2 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-61 | 2026-08-12T23:27:56+00:00 | from: owner | type: review-request | thread: release-v060-branch | refs: release/v0.6.0@c87529bf310ba169f2d3e10235de0909364c5b8e

Branch gate for v0.6.0: release/v0.6.0@c87529b under the APPROVED plan (MSG-60). Docket release-v060-docket.md; full diff enclosed. Verify the round-1 support-status fix landed and sweep for any remaining contradiction. Merge + irreversible tag/PyPI only on PASS.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: ebe630f359a970f902d58bdbd3c841bfd12d8d846200070501136c637023136f
- source-ref: c87529bf310ba169f2d3e10235de0909364c5b8e
- docket-revision-sha256: 05d3672253460d3e8faa4c421c4134b548d30015d9cfd98c18b277b9bdf62f09
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-12-v0.6.0-release.md", "sha256": "1f8189af0737dcb2ed4950c378d9794162b51b53d37b89ab1bf7ee716801efce", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/release-v060-docket.md", "sha256": "f9976ec2b61a8964518801424c0f866b76275355cae99942d6d8958dc81f9ed1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/release-v060.diff", "sha256": "e9a40ffff6a91f20861161d6b02fae11c721910b4588e3eae0105844a54f2a49", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/release-v060-watcher.json", "sha256": "ebe630f359a970f902d58bdbd3c841bfd12d8d846200070501136c637023136f", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "74a02d84cfcdb65823f849277b24202f12af689e5f41cfda65f103e58c9725ad", "opus": "3ff1a948bc7a7fca842f7a84384b0a70ca3e7946be7796a2aa40807541321714"}

## MSG-62 | 2026-08-12T23:33:57+00:00 | from: opus | type: verdict | thread: release-v060-branch | refs: -

PASS — every hunk of `release-v060.diff` verified against the pinned export at c87529b, and the required command is green.

## Verification command (run literally, no prefixes/pipes)

`python -m pytest -q`

Result:
```
........................................................................ [ 17%]
........................................................................ [ 34%]
........................................................................ [ 52%]
........................................................................ [ 69%]
s....................................................................... [ 87%]
.....................................................                    [100%]
412 passed, 1 skipped in 17.44s
```

## Criterion-1 checks

**1. Four version strings at 0.6.0, lockstep test exists.** `grep -rn "0\.6\.0\|0\.5\.0" pyproject.toml src/debate/__init__.py .claude-plugin/plugin.json .claude-plugin/marketplace.json` returns exactly four hits, all 0.6.0, no 0.5.0 residue: pyproject.toml:7, src/debate/__init__.py:42, .claude-plugin/plugin.json:3, .claude-plugin/marketplace.json:9. tests/test_release_sync.py:11 `test_all_four_version_locations_agree` reads pyproject as source of truth and asserts the package `__version__` plus both manifests against it — it covers all four locations and is inside the green run above.

**2. CHANGELOG heading vs release.yml anchor.** CHANGELOG.md:9 is `## v0.6.0 — 2026-08-13`; `## Unreleased` is gone. The publish preflight and the github-release job both use `r"^## " + re.escape(ref) + r"(?=[ \t]|$)[^\n]*\n(.*?)(?=\n## |\Z)"` (release.yml:73 and :106). For ref `v0.6.0` the character after the tag is a space, so the `[ \t]` lookahead holds, the `[^\n]*` absorbs the em-dash date, and the captured body (CHANGELOG.md:11-52, through to `## v0.5.0` at :54) is non-empty — both the "no usable section" exit and the empty-body exit are avoided.

**3. CHANGELOG entries vs shipped behavior.**
- *Wizard flags*: `--command`, `--human`, `--yes` (plus `--smoke`, `--scheduler`) are all real `p_setup` arguments at src/debate/__main__.py:249,258,266,271,277. "Everything derivable is derived" matches `derive_paths` (setup.py:113) making the config stem and state stem the channel id, and `scheduler_units` (setup.py:365) making the unit `debate-watch-<channel-id>`. "Validates before writing anything" matches `apply` (setup.py:198-242): `validate` first, then the config round-trips the real loader through a probe in a scratch dir outside every target path, and only then is a byte written. The PROTOCOL scaffold is absent-only/never-clobbered (setup.py:140-153), and tests/test_setup.py:136 pins `setup.protocol_template()` byte-equal to the repo `PROTOCOL.md`, with tests at :125-132 proving an owner-edited file is not clobbered. The managed-version-2 refusal pointing at `adapter-doctor` is covered by tests/test_setup.py:227-231. The defaults cache stores the provenance channel as a suggestion, not a registry (setup.py:94-109).
- *Smoke semantics*: setup.py:302-356 matches the entry claim for claim — throwaway channel built with setup's own write path so it carries a PROTOCOL.md (`init_channel` + `scaffold_protocol`, :324-326), an `info` probe posted as the *other* party (:319, :327-331), the seat run with its REAL pinned prompt repointed at the scratch root (:332-335), a reply asserted in the scratch mailbox (:343-345), one call per seat announced before it is spent (:317-318), and `finally: shutil.rmtree(scratch, ignore_errors=True)` (:354-355) so the scratch root goes either way. The PASS message states plainly it proves the seat contract only, "NOT consistency or review quality" (:346-348).
- *Scheduler withholding*: __main__.py:473-478 prints "scheduler output withheld: fix the failing seat first" when a requested smoke failed, and only otherwise emits units; `scheduler_units` is text-only and never touches `systemctl` (setup.py:359-401, install line printed as "not run for you" at __main__.py:487).
- *`{channel_name}` expansion*: watcher.py:193-202 expands `{channel_name}` alongside `{channel_root}` in the same single first pass.

**4. Round-1 finding fixed, and no other support-status contradiction standing.** README.md:50-52 now reads "they keep working, but posting to them is deprecated since 0.5; `debate migrate` renames one in place, byte-identically" — the "still fully supported" claim is gone. That agrees with README.md:393-399 ("deprecated as of 0.5 — it still works, `debate migrate` is the supported path forward, and no removal date is promised") and with the CHANGELOG Deprecated entry at :117-121. I swept wording, not just tokens: `grep -rn "fully supported|still supported|supported|deprecat"` over all repo `*.md` (README, CHANGELOG, PROTOCOL.md, docs/, skills/) returns only CHANGELOG.md:107,118,119,183,218 and README.md:52,398,399. The one remaining "remains fully supported" is CHANGELOG.md:183, which sits inside the historical `## v0.4.0 — 2026-08-05` section (heading at :137) and is explicitly tense-scoped "in 0.4" — a correct historical record superseded by the v0.5.0 Deprecated entry, not a standing contradiction. A dedicated `0\.3\.x|legacy|CHANNEL\.md|fully supported|still supported|deprecat` sweep of README returns only :50-52, :62, :313, :393, :397-398, all consistent.

**5. Counts verify in the export.** `wc -l src/debate/*.py src/debate/**/*.py` totals exactly **5488** (channel.py 1404, controller.py 1843, __init__.py 42, __main__.py 658, setup.py 428, watcher.py 1113). Tests: the run above collected **413** (412 passed + 1 skipped). README.md:481-483 states "about 5,500 lines ... with 413 tests" — honest rounding of 5,488 and an exact test count; the stale 4,900/395 pair is gone.

**6. Placeholder documentation matches `command_for`'s real semantics.** README.md:281-286 says both placeholders expand "in one fixed pass before `{prompt}` is substituted into the argv". watcher.py:175-202 does exactly that: `{channel_root}` and `{channel_name}` are replaced inside the prompt text in a single chained pass, then `{prompt}` is substituted into argv, and argv is never re-scanned — so the documented expansion order (placeholders first, argv substitution second) is the implemented order. `{channel_root}` → `str(self.channel_root.resolve())` matches "resolved absolute channel folder"; `{channel_name}` → the channel id matches. The generated form is real: setup.py:36-45 emits prompts carrying `--root {channel_root} --channel {channel_name}`, so "`debate setup` generates exactly that form" holds. The paragraph is placed in the README watcher-config section, directly after the config JSON block ending at :279, per the folded non-blocking note.

**7. Language rules.** Case-insensitive sweep for `unforgeable|tamper-evident|final` across all repo `*.md`: no occurrence of "unforgeable" anywhere. Both tamper-evidence claims are correctly hedged — README.md:473 "tamper-evident, not tamper-proof" with the explicit "not as evidence against a determined forger with write access", and CHANGELOG.md:189 "The record is tamper-evident." Nothing is called "final" as a status claim; the sole `final` hit is README.md:529 "the final CLIs reported a `$0.355168`", where the word means *last*, not a claim of finality.

## Non-blocking observation

The heading date `2026-08-13` (CHANGELOG.md:9) is one day ahead of the current date, and the file's preamble states "Dates are the tag dates." This is not a gate failure: the docket pins that exact heading as the expected state, release.yml's anchor matches on the tag alone and ignores everything after it on the heading line, and the tag is pushed after this gate. Worth confirming the tag actually lands on 2026-08-13 UTC so the stated tag date stays honest.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: e96c053e5496e2b2ea85d548936bf9be2dadd4d0031f282e6f6d50cf01bbf77c
- phase: sealed
- captured-at: 2026-08-12T23:33:57+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: ebe630f359a970f902d58bdbd3c841bfd12d8d846200070501136c637023136f
- source-ref: c87529bf310ba169f2d3e10235de0909364c5b8e
- source-manifest-sha256: 3ff1a948bc7a7fca842f7a84384b0a70ca3e7946be7796a2aa40807541321714
- docket-revision-sha256: 05d3672253460d3e8faa4c421c4134b548d30015d9cfd98c18b277b9bdf62f09
- input-sha256: 3584c204523947459f97ea4294f416c6663768bafac95f955e2b67aaa6d0034a
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-63 | 2026-08-12T23:33:57+00:00 | from: codex | type: verdict | thread: release-v060-branch | refs: -

Verified every release-diff hunk against the pinned export and approved plan: all four version locations are 0.6.0; the CHANGELOG v0.6.0 heading matches release.yml’s tag anchor and accurately describes setup, smoke, scheduler withholding, and placeholder expansion; legacy-layout wording is consistent; source totals 5,488 lines; and no unforgeable/final release claim remains. README placeholder documentation matches watcher.command_for’s single fixed expansion pass and order. Exact command run in the export: `python -m pytest -q` → `412 passed, 1 skipped in 18.43s` (413 collected outcomes). Verified files include /home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/c87529bf310ba169f2d3e10235de0909364c5b8e/codex/CHANGELOG.md, README.md, .github/workflows/release.yml, src/debate/watcher.py, src/debate/setup.py, pyproject.toml, src/debate/__init__.py, and tests/test_release_sync.py.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: e96c053e5496e2b2ea85d548936bf9be2dadd4d0031f282e6f6d50cf01bbf77c
- phase: sealed
- captured-at: 2026-08-12T23:30:52+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: ebe630f359a970f902d58bdbd3c841bfd12d8d846200070501136c637023136f
- source-ref: c87529bf310ba169f2d3e10235de0909364c5b8e
- source-manifest-sha256: 74a02d84cfcdb65823f849277b24202f12af689e5f41cfda65f103e58c9725ad
- docket-revision-sha256: 05d3672253460d3e8faa4c421c4134b548d30015d9cfd98c18b277b9bdf62f09
- input-sha256: 98a1f4d557ccfd82adbeb53afa0713d9efea705ae01eaa73b01c1b7fb88c9e38
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-64 | 2026-08-12T23:33:57+00:00 | from: owner | type: close | thread: release-v060-branch | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-65 | 2026-08-13T02:07:57+00:00 | from: owner | type: review-request | thread: plan-three-agent-collateral | refs: main@35be8fde86c54f49a205ac0e0aef0806bb3caf5c

Plan-doc gate: the three-agent collateral refresh (README hero copy + banner + intro flow SVG updated from the two-agent story to the shipped three-agent topology: author agent with the owner, two independent seats debating). Publishable artifacts; owner picks the banner before commit; channel stays two-seat everywhere. Criteria in plan-collateral-docket.md.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- docket-revision-sha256: 923b7cea6c7477fb37daec02d5c5ff960e01d717a8feb539650e19275c0b30f2
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-13-three-agent-collateral-refresh.md", "sha256": "83c9ef422ed94cdc39d55079963296b2171156203a529ef8c0dfe7b8cd640d51", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-collateral-docket.md", "sha256": "05282a6297d52fc0db945c4a7fa1a7e3358385c0307b489019ff152da79f1437", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-collateral-watcher.json", "sha256": "2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "a9c42d8e1c7ffaff7fcf494423d1e9e2b316aa34c8fea8fed4df4738ebf7ee6b", "opus": "4343325d3ac2e2724bca0c1a2002c0a840bf5e0043c36b8b7cc0381fe66610a6"}

## MSG-66 | 2026-08-13T02:12:04+00:00 | from: opus | type: verdict | thread: plan-three-agent-collateral | refs: -

NO_PASS — the required command passes, but criterion 1 does not hold: the plan's own sweep is scoped too narrowly, and after execution the front door would still contradict the topology section in three concrete places.

## Verification (docket criterion 2)

Command run literally from the export root `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/35be8fde86c54f49a205ac0e0aef0806bb3caf5c/opus`:

```
python -m pytest -q tests/test_output_is_ascii.py
```

Result:

```
....                                                                     [100%]
4 passed in 0.25s
```

## Criterion 1 — what holds

- **Central factual claim is correct.** Verified in the export: `README.md:14` leads "One AI agent writes the code. A second agent — from a different company, in a different app — checks it."; the banner alt at `README.md:2` describes "Two robot figures at opposing parliamentary dispatch boxes"; the intro flow alt at `README.md:57` says "A builder agent and a reviewer agent"; and `docs/assets/flow-light.svg:26,31` literally labels the two boxes "builder agent" / "reviewer agent". Against that, `README.md:174-179` states "Exactly one independent seat is the minimum two-agent topology... Two independent seats are the recommended three-agent topology, where the interactive author/controller is outside both debate seats." The front door does tell a two-agent story while the shipped recommended topology is three agents.
- **Two-seat discipline is kept.** Step 1 bullet 2 and the Non-goals ("no N-party channel claims — the channel remains a two-seat debate; the third agent is the author outside it") match `README.md:185` ("each remains a two-seat debate with its own explicit channel id"), and the minimum two-agent topology is explicitly retained as the fallback.
- **Image/diagram conventions are respected.** Owner picks the banner before commit, `banner.png` filename preserved for hotlinks, alt texts updated with the images, hand-built SVG style/palette preserved — consistent with `docs/assets/` (hand-authored `<rect>`/`<text>` primitives, no export metadata).

## Blocking findings

**1. Publishable front-door copy outside README keeps the retired two-agent claim, and is outside the plan's scope.**
- `.claude-plugin/plugin.json:4`: `"description": "Debate — cross-vendor code review: one AI agent writes the code, a second agent from a different vendor reviews it, ..."` — the retired hero sentence, near-verbatim.
- `pyproject.toml:8`: `description = "Two AI agents review each other's work through two shared text files — ..."` — this is the PyPI one-line summary shown above the README on the project page.

The plan anticipates PyPI ("PyPI's README updates at the next release") but only for the README body; the summary line and the plugin listing are not in any step, and Non-goals says "No code changes", which reads as excluding `pyproject.toml`. After execution, the PyPI page and the Claude Code plugin listing would still say one agent writes and a second checks, directly contradicting the refreshed README and `README.md:174-179`.

**2. `README.md:463-465` survives the sweep and contradicts the topology section.** "**Two parties by design.** A review needs a builder and a reviewer; strict alternation between exactly two named agents (plus a supervisor who can always interject) is the feature." Under the recommended three-agent topology neither seat is the builder — both are author-independent. Step 1 scopes the sweep to "README/PROTOCOL **intro** wording", and this bullet is in "Limits, honestly", so it is not covered. It needs rewording to the two-*seat* framing (which preserves the bullet's actual anti-N-party point) or the front door and `README.md:174-179` still disagree.

**3. The PROTOCOL sweep collides with the "no code changes" non-goal.** `tests/test_setup.py:135-136` asserts `setup.protocol_template() == (REPO / "PROTOCOL.md").read_text(...)`, byte-locking `PROTOCOL.md` to `src/debate/protocol_template.md` (both open "a contract between two agents and their supervisor"). Any PROTOCOL intro rewording required by step 1 must edit the packaged template in lockstep, which the plan forbids under "no code changes". Step 4's full-suite run would catch it, but the plan as written specifies two mutually exclusive things.

## Non-blocking

Step 3 underspecifies the SVG relayout: `docs/assets/flow-light.svg:1` is a fixed `width="880" height="430" viewBox="0 0 880 430"` canvas with the builder box at `x="40"`, the channel at `x="310"` (w=260) and the reviewer at `x="640"` (w=200) — there is no horizontal room for a third box plus the owner without widening the viewBox or relaying out, and `README.md:57` pins `width="820"`. Worth naming the target canvas so light/dark stay identical in geometry.

Re-run recommendation: add the `pyproject.toml` summary and `.claude-plugin/plugin.json` description to step 1, extend the sweep beyond "intro" to at least `README.md:463`, and reconcile the PROTOCOL sweep with `src/debate/protocol_template.md`.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 0eaf5849e8d4651cd6b4950c8670c631f7e923c0ad428607e47248c0ca130a84
- phase: sealed
- captured-at: 2026-08-13T02:10:46+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: 4343325d3ac2e2724bca0c1a2002c0a840bf5e0043c36b8b7cc0381fe66610a6
- docket-revision-sha256: 923b7cea6c7477fb37daec02d5c5ff960e01d717a8feb539650e19275c0b30f2
- input-sha256: 37621f216b492bf027e4dbd96100d713d8236474951b8afdbed6557edd2e713e
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-67 | 2026-08-13T02:12:04+00:00 | from: codex | type: verdict | thread: plan-three-agent-collateral | refs: -

Inspected the pinned export README and flow SVGs plus the immutable docket. The README front door currently presents two agents, while its brokered section explicitly documents the recommended three-agent topology with the author/controller outside two seats; the plan correctly reconciles this while retaining the two-seat channel and minimum topology. Its banner/SVG steps preserve filenames, require owner selection before commit, update alt text, and preserve the hand-built SVG convention. Fresh verification: `python -m pytest -q tests/test_output_is_ascii.py` => `4 passed in 0.28s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: 0eaf5849e8d4651cd6b4950c8670c631f7e923c0ad428607e47248c0ca130a84
- phase: sealed
- captured-at: 2026-08-13T02:12:04+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: a9c42d8e1c7ffaff7fcf494423d1e9e2b316aa34c8fea8fed4df4738ebf7ee6b
- docket-revision-sha256: 923b7cea6c7477fb37daec02d5c5ff960e01d717a8feb539650e19275c0b30f2
- input-sha256: 34cb63adf887e8bfd7d632e70c9f0dca2cdaf5069523f7946001faf31252f30d
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-68 | 2026-08-13T02:16:31+00:00 | from: opus | type: verdict | thread: plan-three-agent-collateral | refs: -

NO_PASS — holding my position after re-reading the export against the opposing PASS. The required command passes; criterion 1 bullet 3 still fails, and the opposing verdict does not address the specific lines that fail it.

## Verification (docket criterion 2)

Command run literally from the export root `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/35be8fde86c54f49a205ac0e0aef0806bb3caf5c/opus`:

```
python -m pytest -q tests/test_output_is_ascii.py
```

Result:

```
....                                                                     [100%]
4 passed in 5.16s
```

## Where I agree with the PASS seat

Re-verified in the export and unchanged from my sealed read: the plan's central factual claim is right (`README.md:14` "One AI agent writes the code. A second agent — from a different company, in a different app — checks it."; banner alt at `README.md:2`; intro flow alt at `README.md:57` "A builder agent and a reviewer agent"; `docs/assets/flow-light.svg:26,31` labels "builder agent"/"reviewer agent" — versus `README.md:174-179` documenting the recommended three-agent topology with the author/controller outside both seats). Two-seat discipline holds (plan step 1 bullet 2 + Non-goals vs `README.md:185` "each remains a two-seat debate with its own explicit channel id"), the minimum two-agent topology is retained, and the image/diagram steps match repo convention (owner picks before commit, `banner.png` filename preserved, alt text updated with images, hand-built SVG primitives preserved). Those three sub-criteria are not in dispute.

## Blocking — criterion 1, bullet 3 ("anything missing that would leave the front door and the topology section contradicting each other after execution")

**1. `README.md:463-465` survives the plan's sweep and directly contradicts `README.md:174-179`.** Verbatim at the pinned ref:

> - **Two parties by design.** A review needs a builder and a reviewer; strict alternation between exactly two named agents (plus a supervisor who can always interject) is the feature.

Under the recommended three-agent topology neither seat is the builder — both are author-independent, which is exactly what `README.md:174-179` says. Plan step 1 bullet 3 scopes the sweep to "README/PROTOCOL **intro** wording"; this bullet is in "Limits, honestly", so it is not covered by any step. This is the same README page — the front door — and after execution it would still assert the retired framing. The fix is small (reframe to two *seats*, which preserves the bullet's real anti-N-party point) but it is not in the plan. The PASS verdict asserts the plan "correctly reconciles" the front door without reaching this line; I could not reconcile that assertion with the text.

**2. Publishable one-line descriptions outside README keep the retired claim and are excluded by the plan's own Non-goals.**
- `.claude-plugin/plugin.json:4`: `"description": "Debate — cross-vendor code review: one AI agent writes the code, a second agent from a different vendor reviews it, ..."` — the retired hero sentence near-verbatim, and this is the text shown in the plugin listing.
- `pyproject.toml:8`: `description = "Two AI agents review each other's work through two shared text files — ..."` — the PyPI summary rendered above the README on the project page.

Plan step 5 anticipates PyPI but only for the README body ("PyPI's README updates at the next release"); neither string appears in any step, and "No code changes" reads as excluding `pyproject.toml`. Post-execution the PyPI page would carry a two-agent summary directly above a three-agent README. I weight this below finding 1 (it is adjacent collateral rather than the README front door proper), but it is the same contradiction the plan exists to remove, and it is cheap to fold into step 1.

## Downgraded from my sealed verdict — non-blocking

My sealed finding 3 (PROTOCOL sweep vs "no code changes") is weaker than I first stated. `tests/test_setup.py:135-136` does byte-lock `PROTOCOL.md` to `src/debate/protocol_template.md`, so any PROTOCOL intro edit must touch `src/` in lockstep against the "No code changes" non-goal. But sweeping the actual text, `PROTOCOL.md:1` ("a contract between two agents and their supervisor") and the `builder → reviewer` message-type names at lines 37-42 describe channel mechanics and message roles, which remain accurate for a two-seat channel. So the sweep can legitimately conclude "no PROTOCOL change needed"; the plan is under-specified here, not self-contradictory. Flagging the byte-lock so execution does not discover it late.

Also non-blocking: step 3 does not name the target canvas. `docs/assets/flow-light.svg:1` is fixed at `width="880" height="430" viewBox="0 0 880 430"` with boxes at `x="40"`, `x="310"` (w=260) and `x="640"` (w=200) — no horizontal room for a third box plus the owner without widening or relaying out, and `README.md:57` pins `width="820"`. Name the canvas so light and dark stay geometrically identical.

## To clear this

Add `README.md:463` (extend the sweep past "intro" to the whole README) and the `pyproject.toml` / `.claude-plugin/plugin.json` descriptions to step 1, and state the SVG target canvas. Criterion 2 already passes and the other three sub-criteria of criterion 1 already hold.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: 4343325d3ac2e2724bca0c1a2002c0a840bf5e0043c36b8b7cc0381fe66610a6
- docket-revision-sha256: 923b7cea6c7477fb37daec02d5c5ff960e01d717a8feb539650e19275c0b30f2
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: 4343325d3ac2e2724bca0c1a2002c0a840bf5e0043c36b8b7cc0381fe66610a6
- docket-revision-sha256: 923b7cea6c7477fb37daec02d5c5ff960e01d717a8feb539650e19275c0b30f2
- input-sha256: fa49b9566e127f78b18b7749822edc27ce34f2d2858cb5fdc7e7cbb07e6dc032
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-69 | 2026-08-13T02:21:03+00:00 | from: codex | type: verdict | thread: plan-three-agent-collateral | refs: -

`python -m pytest -q tests/test_output_is_ascii.py` passed: `4 passed in 0.22s`.

The central claim is correct: README.md:14-15, :2, :57, and flow-light.svg:26/31 tell a builder/reviewer two-agent story, while README.md:174-179 specifies the recommended three-agent topology with the author/controller outside two independent seats. The plan preserves two-seat channel mechanics, the fallback topology, banner selection/filenames/alt text, and hand-built SVGs.

Blocking: step 1 limits its sweep to README/PROTOCOL “intro wording.” README.md:463-465 would remain: “A review needs a builder and a reviewer” with two named agents. That conflicts with the recommended topology, where the two channel seats are independent and the builder/author is outside them. The plan must explicitly sweep and reframe this full-README claim to the two-seat channel model.

Also missing from the public collateral sweep are pyproject.toml:8 and .claude-plugin/plugin.json:4, whose package/plugin descriptions retain the retired two-agent framing. Updating only the README would leave those published entry points inconsistent with its three-agent topology section.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: a9c42d8e1c7ffaff7fcf494423d1e9e2b316aa34c8fea8fed4df4738ebf7ee6b
- docket-revision-sha256: 923b7cea6c7477fb37daec02d5c5ff960e01d717a8feb539650e19275c0b30f2
- input-sha256: 175e0754e912e10e9909a58cee01b492260c82a1603e6ca23881c844d4384c07
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-70 | 2026-08-13T02:21:03+00:00 | from: owner | type: close | thread: plan-three-agent-collateral | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-71 | 2026-08-13T04:40:30+00:00 | from: owner | type: review-request | thread: plan-three-agent-collateral-r2 | refs: main@35be8fde86c54f49a205ac0e0aef0806bb3caf5c

Plan gate round 2: the collateral refresh with all three MSG-66..69 findings folded (entry-point strings in scope; full-README sweep incl. the Limits bullet reframed to two seats; PROTOCOL/template lockstep honored; non-goal wording fixed). Docket carries the round-1 summary.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- docket-revision-sha256: 6ab590813c1c7a0f38e08dc26f0ec937e5eaf881f0ad8aaaea85fcf409e807ca
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-13-three-agent-collateral-refresh.md", "sha256": "3ab9e9b7efb7be4af0318e763701130dd69fdbd84b4d16905df2c41c498508f5", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-collateral-docket.md", "sha256": "02ecee936ad914e72be9ee11b9b1fc0bdf0c1ac434b952037c3989a106a8d2ba", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/plan-collateral-watcher.json", "sha256": "2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "a9c42d8e1c7ffaff7fcf494423d1e9e2b316aa34c8fea8fed4df4738ebf7ee6b", "opus": "4343325d3ac2e2724bca0c1a2002c0a840bf5e0043c36b8b7cc0381fe66610a6"}

## MSG-72 | 2026-08-13T04:44:31+00:00 | from: opus | type: verdict | thread: plan-three-agent-collateral-r2 | refs: -

PASS — the round-1 folds hold and the plan's central claim is correct against my own reads of the pinned export.

VERIFICATION COMMAND (run literally, no prefixes/pipes, from the export root):
`python -m pytest -q tests/test_output_is_ascii.py`
Result: `....                                                                     [100%]` / `4 passed in 0.22s`.

CRITERION 1 — central factual claim: CONFIRMED.
- Front door tells a two-agent story: README.md:14-15 hero ("One AI agent writes the code. A second agent - from a different company, in a different app - checks it"); README.md:2 banner alt text ("Two robot figures at opposing parliamentary dispatch boxes..."); README.md:57 intro flow alt text ("A builder agent and a reviewer agent - deliberately from different vendors - each post and read...").
- Shipped topology is three agents with the author outside both seats: README.md:174-179 ("Exactly one independent seat is the minimum two-agent topology... Two independent seats are the recommended three-agent topology, where the interactive author/controller is outside both debate seats"), backed in code/tests by src/debate/controller.py:393 and tests/test_controller.py:578-591 ("recommended-three-agent" for two author-independent seats). The contradiction the plan names is real.

TWO-SEAT ACCURACY / MINIMUM TOPOLOGY: preserved. Plan step 1 bullet 2 keeps "a channel seats exactly two debating parties; the author is OUTSIDE both seats" and keeps the minimum two-agent topology documented as the fallback; the non-goals restate "no N-party channel claims - the channel remains a two-seat debate". That matches README.md:185 ("each remains a two-seat debate with its own explicit channel id") and the Limits bullet's anti-N-party point at README.md:463-465, which the plan reframes to two *seats* rather than deleting.

ROUND-1 FOLDS, each checked against the export:
- (F1) Published entry-point strings are now in scope and do carry the retired sentence: pyproject.toml:8 description ("Two AI agents review each other's work...", the PyPI summary) and .claude-plugin/plugin.json:4 ("one AI agent writes the code, a second agent from a different vendor reviews it"). .claude-plugin/marketplace.json's two description strings ("through two shared text files", "hold your seat on a debate review channel") carry no retired claim, so naming the file is harmless over-coverage, not an error.
- (F2) The "Limits, honestly" bullet at README.md:463 ("A review needs a builder and a reviewer") is explicitly named, and the sweep is now FULL-README rather than intro-scoped - needed, because the same flavor also sits at README.md:23 ("the way two developers review each other's pull requests") and README.md:30 ("those two agents can't talk to each other"), both of which the widened sweep covers.
- (F3) The byte-lock is real: tests/test_setup.py:135-136 `test_packaged_template_matches_repo_protocol` asserts `setup.protocol_template() == (REPO / "PROTOCOL.md").read_text(...)`, and PROTOCOL.md:1 is byte-identical in the packaged src/debate/protocol_template.md:1. Plan step 1 requires lockstep edits, and the non-goal now reads "No behavior or code-logic changes" with metadata strings and the PROTOCOL/template lockstep declared IN scope - the round-1 contradiction is gone.

MY OWN SWEEP for anything left contradicting the topology section after execution: I found no blocking gap. Residual "two agent" mentions outside the plan's enumerated scope remain accurate under the three-agent topology and do not contradict README.md:174-179: skills/debate/SKILL.md:11 ("coordinates two AI agents from different vendors" - describes the two seats, not the author); PROTOCOL.md:1 title ("a contract between two agents and their supervisor" - the two seats); docs/case-study.md:4-10 (a historical incident account of a real two-agent run); src/debate/__init__.py:1 docstring. Two non-blocking notes for execution: __init__.py:1's "two AI agents that review each other's work" carries the same mutual-review framing the plan retires from the PyPI summary and is cheap to align while touching metadata; and the GitHub repo "About" blurb is not in the export, so if it mirrors the hero sentence it needs the same edit in repo settings (step 5 mentions the repo page updating on merge but not that field).

IMAGE/DIAGRAM STEPS vs repo conventions: consistent. docs/assets/ holds banner.png, social-preview.png, flow-light.svg, flow-dark.svg, broker-light.svg, broker-dark.svg; step 2 replaces files in place (filenames stay, hotlinks keep resolving) and requires OWNER PICKS before anything is committed, with the social preview regenerated to match. flow-light.svg is hand-authored markup (inline `<marker>` defs, section comments, GitHub palette #f6f8fa/#d0d7de/#57606a/#8250df), and step 3 preserves that style and palette. Alt texts are updated with the images (step 1 close, step 3), which is required since the <picture> block carries its alt only on the <img> at README.md:57. Leaving the broker pair as is checks out: its alt text (README.md:143) already describes a controller plus two seats and makes no author-in-seat claim.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: b5a71fab7eab3194e36828247cd1dfb2df5dfdc35c32cd483c569439e24c348e
- phase: sealed
- captured-at: 2026-08-13T04:44:31+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: 4343325d3ac2e2724bca0c1a2002c0a840bf5e0043c36b8b7cc0381fe66610a6
- docket-revision-sha256: 6ab590813c1c7a0f38e08dc26f0ec937e5eaf881f0ad8aaaea85fcf409e807ca
- input-sha256: ef6916f0e3b92442eaa06c31887a83cfd5d1120662c79a33a11fc1bd31c4c66c
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-73 | 2026-08-13T04:44:31+00:00 | from: codex | type: verdict | thread: plan-three-agent-collateral-r2 | refs: -

PASS. Fresh export inspection confirms README.md front door currently presents a two-agent story (hero alt text, lead, and intro-flow alt text), while its brokered section explicitly defines the recommended three-agent topology as an interactive author/controller outside two independent seats and preserves the minimum two-agent topology. The plan explicitly sweeps the full README (including Limits), keeps the channel two-seat, updates both flow SVGs and all relevant alt text, retains owner selection before raster-asset commit and stable filenames, and includes the previously omitted PyPI/plugin descriptions plus PROTOCOL.md and src/debate/protocol_template.md lockstep. I also confirmed the existing protocol/template are byte-identical. Exact verification run: `python -m pytest -q tests/test_output_is_ascii.py` -> `4 passed in 0.21s`.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: b5a71fab7eab3194e36828247cd1dfb2df5dfdc35c32cd483c569439e24c348e
- phase: sealed
- captured-at: 2026-08-13T04:42:15+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 2b46bc56bd0799fdcbe4104f12fefaa19f66ea065e8926b0f16d03a1afc6a40d
- source-ref: 35be8fde86c54f49a205ac0e0aef0806bb3caf5c
- source-manifest-sha256: a9c42d8e1c7ffaff7fcf494423d1e9e2b316aa34c8fea8fed4df4738ebf7ee6b
- docket-revision-sha256: 6ab590813c1c7a0f38e08dc26f0ec937e5eaf881f0ad8aaaea85fcf409e807ca
- input-sha256: 5ffb4f23f1d49f19d737f64d4f51dd18dcf32b15d04f0f788c94e4c63170c5c2
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-74 | 2026-08-13T04:44:31+00:00 | from: owner | type: close | thread: plan-three-agent-collateral-r2 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement

## MSG-75 | 2026-08-13T05:23:19+00:00 | from: owner | type: review-request | thread: collateral-branch | refs: feature/three-agent-collateral@acbae9a89b6a59f17a1555e88b136dd6c2e8811a

Branch gate: feature/three-agent-collateral@acbae9a under the APPROVED plan (MSG-74). Publishable front-door refresh to the three-agent story; docket collateral-branch-docket.md; sweep for any surviving two-agent claim yourself. Merge on PASS + green CI.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: a0e5780dbfe3e0a9a514f999d81e219675c247fd03add6998856317a56d270c8
- source-ref: acbae9a89b6a59f17a1555e88b136dd6c2e8811a
- docket-revision-sha256: d6e92601890233ae2db3cde9e43e9e174f21beec6d660a9ec3c26cbcc228d861
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-13-three-agent-collateral-refresh.md", "sha256": "8e3face1c2572247dbabb29521549a743b3b4d06d2615fbd45fac33da88c2dda", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral-branch-docket.md", "sha256": "512e6838811eca276316316bc3300aa6446092fc913e4540b65b45df5bbab8f7", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral.diff", "sha256": "b60be542016e264d6b18543abc45ede30d7b1661e4bf2ea0ad716ff722304f5f", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral-branch-watcher.json", "sha256": "a0e5780dbfe3e0a9a514f999d81e219675c247fd03add6998856317a56d270c8", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "9fe4e296cb80ce1aab9a3aa43498d167d58e6c4d1fa7b7aeaf75ebb5dceebe60", "opus": "e815f9ad1ac04052686bd245869d6dbdfbc4504165353af055ef01b5e9dc34b6"}

## MSG-76 | 2026-08-13T05:30:38+00:00 | from: opus | type: verdict | thread: collateral-branch | refs: -

NO_PASS on `feature/three-agent-collateral@acbae9a`. The mandated command passes; two criterion-1 checks do not.

## Mandated command — PASS

Run literally from the export root `.../exports/acbae9a89b6a59f17a1555e88b136dd6c2e8811a/opus`:

```
python -m pytest -q
```

Result: `412 passed, 1 skipped in 17.71s` (fresh run, no prefixes/pipes). This matches the README's "413 tests as of this writing" (412 + 1 skipped collected).

## Blocking finding 1 — both flow SVGs: the new author unit overlaps the watcher box

Criterion: "the updated flow SVGs keep the hand-built style"; plan step 4 requires "both SVGs render in light and dark". The existing diagram is laid out with no overlapping elements. The new author+owner unit breaks that in **both** variants, at identical coordinates.

`docs/assets/flow-light.svg:53` (and `flow-dark.svg:53`) — watcher box occupies x∈[330,550], y∈[270,340]:
```
<rect x="330" y="270" width="220" height="70" rx="10" fill="#fbf7ff" stroke="#8250df" stroke-width="1.5"/>
```

`docs/assets/flow-light.svg:84` (and `flow-dark.svg:84`):
```
<text x="330" y="330" text-anchor="middle" font-size="11.5" fill="#bc4c00">delivers the branch +</text>
```
`text-anchor="middle"` centers the string's advance width on x=330, so roughly half of a ~120px string (x≈330→390) lies inside the watcher rect's x-range, with baseline y=330 inside its y-range [270,340]. Because this `<text>` is declared after the watcher `<rect>`, it paints **on top of** the watcher's fill. Line 85 (`review-request`, baseline y=345) clips the rect's bottom edge with its ascenders.

`docs/assets/flow-light.svg:83` (and `flow-dark.svg:83`):
```
<path d="M 260 380 C 330 380 350 260 385 224" .../>
```
Evaluating this cubic: it crosses x=330 at y≈326 (t≈0.45) and exits the rect's top edge y=270 at x≈358 (t≈0.72). So the orange arrow traverses the watcher box interior for roughly a quarter of its length, painted over the box.

Honest scoping: this seat's shell is restricted to a narrow allowlist — `inkscape --query-all` and `python3 -c` were both denied — so I could not produce a rasterized render. The finding is derived from the exact coordinates quoted above, and the `text-anchor="middle"` overlap is unarguable from the numbers alone regardless of exact glyph metrics.

## Blocking finding 2 — the retired two-agent sentence survives in the shipped package

Criterion: "nothing anywhere still tells the retired builder/reviewer two-agent story — sweep yourself, do not trust the diff's coverage."

`src/debate/__init__.py:1`:
```
"""debate — a tiny file-based protocol for two AI agents that review each other's work.
```
This is verbatim the retired story the branch deliberately removed from `pyproject.toml` ("Two AI agents review each other's work through two shared text files"). Under the recommended topology the two seats do not review *each other's* work — they debate a third agent's work, which is precisely the contradiction round-1 finding (1) was folded to eliminate. It is the top-level docstring of the shipped package (`pydoc debate` / `help(debate)`), not code logic, so editing it sits inside the plan's non-goals. It is not surfaced by `debate --help` (`src/debate/__main__.py:209` uses that module's own docstring, which is clean), which is why it is a sweep miss rather than a headline error — but it is exactly what the docket told me not to trust the diff for.

## Non-blocking note

`.claude-plugin/marketplace.json` is untouched by the diff although plan step 1 names it among the entry-point strings to update. Its current text ("cross-vendor AI code review through two shared text files"; "hold your seat on a debate review channel") is topology-neutral and carries no agent count, so it does not contradict the new story. Flagging it only because the plan named it explicitly; I do not treat it as blocking.

## Checks that PASS

- **PROTOCOL lockstep** — `cmp PROTOCOL.md src/debate/protocol_template.md` → byte-equal; both `sha256 26ead49eb64bc0e17b4a2b6d50052c4ccda0a317eb556d65ab7a9cf989e3703a`. The intro edit ("two agents"→"two debating seats", "both agents read it"→"both seats read it") is wording-only; no semantic change to the message-type contract.
- **Hero images** — `file docs/assets/banner.png docs/assets/social-preview.png` → `1584 x 672` and `1344 x 672`. The social preview is exactly 2:1 and, on visual inspection, a centered crop of the banner (120px off each side).
- **Banner alt text vs. the actual image** — I viewed `docs/assets/banner.png`. It shows three robots and one human: two at opposing dispatch boxes across an open ledger on a central lectern, a third at a desk beneath the balcony extending a purple document upward, and a robed human leaning over the balcony railing toward it. `README.md:2`'s alt text describes exactly that composition, matching the plan's chosen composition.
- **Flow alt text vs. the SVG labels** — `README.md:61` ("The author agent and the owner build the work together outside both seats and deliver the branch plus a review-request into the channel. Two debating seats … independent of the author") matches the SVG's `author agent + owner` / `build the work together, outside both seats` / `delivers the branch + review-request` / `seat A - debater` / `independent of the author`.
- **Dark palette map** — the new `arrowAuthor` marker and author unit use `#bc4c00`/`#f0883e` (light/dark) with fills `#fff8f0`/`#2b1a12`, consistent with the existing Primer pairings in the file (`#8250df`/`#a371f7`, `#1a7f37`/`#3fb950`, `#57606a`/`#8b949e`, and the supervisor strip's `#f0f7f0`/`#12261a`).
- **Two-seat and topology claims** — README ~178-186 keeps "Exactly one independent seat is the minimum two-agent topology", "Two independent seats are the recommended three-agent topology, where the interactive author/controller is outside both debate seats", and "each remains a two-seat debate". The reframed "Limits, honestly" bullet preserves the anti-N-party point ("Getting N agents to agree is a different protocol"). No N-party claim anywhere.
- **Language rules** — `README.md:478` says "tamper-evident, not tamper-proof"; no occurrence of "unforgeable" anywhere in the export. The only `final` hits are `README.md:534` ("the final CLIs reported"), `tests/test_watcher_identity.py:78` and a `release.yml` comment — none claims a verdict or record is final.
- **Remaining builder/reviewer hits are legitimate** — `PROTOCOL.md`/`protocol_template.md:37-42` use builder/reviewer as message-type role names (PROTOCOL semantic changes are a plan non-goal); `docs/case-study.md`, `examples/`, and README "Where this comes from" are explicitly labeled historical provenance ("provenance, not prescription") describing a past run, not the current topology.

Fix findings 1 and 2 and I expect this to clear on the next pass; nothing else in the diff blocks.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 0564563474cf20d8ef5f27318c5c600e6259edcbd023c6c4ff3f9dca2b57c97c
- phase: sealed
- captured-at: 2026-08-13T05:28:52+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: a0e5780dbfe3e0a9a514f999d81e219675c247fd03add6998856317a56d270c8
- source-ref: acbae9a89b6a59f17a1555e88b136dd6c2e8811a
- source-manifest-sha256: e815f9ad1ac04052686bd245869d6dbdfbc4504165353af055ef01b5e9dc34b6
- docket-revision-sha256: d6e92601890233ae2db3cde9e43e9e174f21beec6d660a9ec3c26cbcc228d861
- input-sha256: 81d81a81539bb336f362c068d91fd6e9d51f14458e9b572e8e57e11fc53e39a9
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-77 | 2026-08-13T05:30:38+00:00 | from: codex | type: verdict | thread: collateral-branch | refs: -

`python -m pytest -q` completed successfully: `412 passed, 1 skipped in 18.44s`. However, the required full topology sweep fails: the retired builder/reviewer two-agent story remains in `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/acbae9a89b6a59f17a1555e88b136dd6c2e8811a/codex/skills/debate/SKILL.md:11`, `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/acbae9a89b6a59f17a1555e88b136dd6c2e8811a/codex/src/debate/__init__.py:1`, `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/acbae9a89b6a59f17a1555e88b136dd6c2e8811a/codex/examples/glm-kimi.md:4-5`, and the case-study. The sweep command `rg -n -i --glob '!*.png' --glob '!*.pyc' 'two AI agents|two agents|builder agent|reviewer agent|\bthe builder\b|\bthe reviewer\b|one AI agent writes|a second agent|writes the code|checks it|review each other' .` reported those results. It also showed the literal prohibited wording in `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/acbae9a89b6a59f17a1555e88b136dd6c2e8811a/codex/README.md:534` (`the final CLIs`). The protocol/template byte-lock and image dimensions do hold (`cmp -s PROTOCOL.md src/debate/protocol_template.md` returned `0`; banner is 1584x672 and social preview 1344x672), but not every docket criterion is satisfied.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: 0564563474cf20d8ef5f27318c5c600e6259edcbd023c6c4ff3f9dca2b57c97c
- phase: sealed
- captured-at: 2026-08-13T05:30:38+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: a0e5780dbfe3e0a9a514f999d81e219675c247fd03add6998856317a56d270c8
- source-ref: acbae9a89b6a59f17a1555e88b136dd6c2e8811a
- source-manifest-sha256: 9fe4e296cb80ce1aab9a3aa43498d167d58e6c4d1fa7b7aeaf75ebb5dceebe60
- docket-revision-sha256: d6e92601890233ae2db3cde9e43e9e174f21beec6d660a9ec3c26cbcc228d861
- input-sha256: c5e86e074250b317a040513e22778cc253bfa34db196bf462048d6d00c1cf062
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-78 | 2026-08-13T05:30:38+00:00 | from: owner | type: close | thread: collateral-branch | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-79 | 2026-08-13T05:33:42+00:00 | from: owner | type: review-request | thread: collateral-branch-r2 | refs: feature/three-agent-collateral@b2ce2a2e01dd005d2b929834c0520f2a5bdff127

Branch gate round 2: feature/three-agent-collateral@b2ce2a2 with all MSG-76/77 findings folded (SVG geometry re-routed; package docstring, plugin SKILL, glm-kimi framing, case-study era marker, 'final CLIs' rewording). Sweep again yourselves. Merge on PASS + green CI.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07
- source-ref: b2ce2a2e01dd005d2b929834c0520f2a5bdff127
- docket-revision-sha256: 846feb52f97987e52456ceda9dfd4f80a93b9ec76cab6b0963ef8bb0a1ff4cdc
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-13-three-agent-collateral-refresh.md", "sha256": "8e3face1c2572247dbabb29521549a743b3b4d06d2615fbd45fac33da88c2dda", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral-branch-docket.md", "sha256": "64f750311dc35ec32e74c99cb967dabb9f42ba85d993a41ef1d5ea521cf37c36", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral.diff", "sha256": "ba96bad85bd57b165a46107f22e62831acb65e445f962261703a55de7b9e3971", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral-branch-watcher.json", "sha256": "b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "fa05f9cf4c508aac7cc45c89fa92c1bd1de7b8be96a9cc8854f5c495b3471276", "opus": "ca2e85618b2d46aac0fa5af7b4037f7ee19a7633d0bc6a9a75fca96f45c9157f"}

## MSG-80 | 2026-08-13T05:41:56+00:00 | from: opus | type: verdict | thread: collateral-branch-r2 | refs: -

APPROVE — fresh export run at b2ce2a2, own inspection of the pinned read-only export plus the docket's exact command.

COMMAND (run literally, no prefix/suffix/pipe, cwd = export root):
`python -m pytest -q` → `412 passed, 1 skipped in 17.35s` (consistent with README:488's "413 tests as of this writing"; the byte-equality test in tests/test_setup.py is inside that green run).

CRITERION-1 CHECKS (each verified against the export, not the diff):

1. Lockstep/no-semantic-change. `sha256sum PROTOCOL.md src/debate/protocol_template.md` → both `26ead49eb64bc0e17b4a2b6d50052c4ccda0a317eb556d65ab7a9cf989e3703a`; `diff -q` printed nothing (BYTE_EQUAL). The only edit is the intro (title "two agents"→"two debating seats"; "make both agents read it"→"make both seats read it"). Section 2's `review-request`/`verdict`/`fix-report` role vocabulary (PROTOCOL.md:37-42) is untouched, so the protocol's semantics are unchanged, matching the plan's non-goal.

2. Three-agent story accurate everywhere. Hero (README.md:14-18), intro (22-26), flow alt (61), brokered topology paragraph (178-183: "Exactly one independent seat is the minimum two-agent topology … Two independent seats are the recommended three-agent topology, where the interactive author/controller is outside both debate seats"), Limits bullet (467-470), pyproject.toml:8, .claude-plugin/plugin.json description, skills/debate/SKILL.md:11-13, src/debate/__init__.py:1, examples/claude-code.md:82-88 (both topologies documented). Channel stays two-SEAT in every claim (README.md:189 "each remains a two-seat debate"; 467 "Two seats by design"; 470 keeps the anti-N-party point). glm-kimi is framed as the two-agent MINIMUM topology (examples/glm-kimi.md:3-7). marketplace.json is topology-neutral, as the round-1 ruling allows.

3. Independent sweep (not trusting the diff): grepped the whole export for `builder|reviewer agent|two agents|second agent|one AI agent|writes the code|checks it|review each other`. Remaining hits are all legitimately historical or role-name-only: docs/case-study.md (now era-marked at :5), README.md:490-522 "Where this comes from" (explicit past-tense provenance), CHANGELOG.md:287 (0.1.0 release note), examples/demo.py (party names of a scripted mechanics demo), PROTOCOL message kinds (per non-goal). No live front-door text still tells the retired builder/reviewer two-agent story.

4. SVG folds — coordinates recomputed myself. Both variants are 880x510 with an `arrowAuthor` marker and a bottom-left author+owner box at (40,360,220x76). Author arrow `M 260 396 C 290 396 285 260 380 226`: evaluating the cubic, at y=340 (watcher top edge is y=270, box x=330..550, y=270..340) x≈305; at t=0.5 y≈323.8/x≈295.6; at y≈270 (t≈0.735) x≈323 — the curve's maximum x while inside the watcher's y-band is ≈323 < 330, so the arrow clears the watcher box on the left and terminates at (380,226), just under the channel box (bottom y=220). Labels at x=262,y=310/325 (~x 206-318 at 11.5px) are likewise left of x=330 and clear of the "wakes whoever's turn it is" text at y=268/283. "prints new entries" was moved to x=497,y=370 to clear the author box. Hand-built style preserved (same rect/rx/stroke-width/font idiom). Dark palette map is consistent with the existing pairs (#bc4c00→#f0883e stroke, #fff8f0→#2b1a12 fill, alongside #8250df→#a371f7 and #1a7f37→#3fb950). Box labels ("author agent + owner", "build the work together, outside both seats", "delivers the branch + review-request") match README.md:61's alt text.

5. Raster assets. `file docs/assets/banner.png docs/assets/social-preview.png` → `PNG image data, 1584 x 672` and `PNG image data, 1344 x 672`; social-preview is exactly 2:1 at the banner's own height, i.e. a 120px-per-side centered crop (the author robot's chair, at x≈1500 in the banner, is cut at the social preview's right edge — consistent with that crop). Viewed both images: three robots + one robed human; two robots at opposing dispatch boxes leaning toward each other across an open ledger on the central lectern; a third robot seated at a desk beneath the balcony raising a purple document up toward the owner, who leans over the railing reaching down. README.md:2's alt text describes exactly that composition, and it matches the plan's chosen composition.

6. Language rules. No "unforgeable" anywhere; README.md:478 and CHANGELOG.md:222 say tamper-evident/not tamper-proof. "the final CLIs" is reworded to "at case close the CLIs reported" (README.md:534). Remaining `final` hits are .github/workflows/release.yml:71 (a pre-release tag word) and tests/test_watcher_identity.py:78 ("final output") — neither is a finality claim.

NON-BLOCKING NITS (no fix required for this gate):
- docs/case-study.md:5-6 — the era marker is correct, but the parenthetical "(the epilogue records how these roles evolved)" overpromises: the Epilogue (:113-146) records how the three amendments became v0.5 machinery and uses seat language, yet never states the author-outside-both-seats/three-agent evolution.
- docs/assets/subscription-wall.svg:20,33 still read "Fable 5 / Opus — the builder" and "reviewer agent"; grepping the export for `subscription-wall` returns no matches, so the asset is unreferenced by any doc and tells no reader the retired story.
- README.md:117 "# The builder asks for a review:" in the version-1 quickstart is builder-flavored, though it is the retained two-party path and does not contradict the topology section.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: f3f9147f39300512c4167014153cae110a7c1c47b58077fb023a93b2df0f3490
- phase: sealed
- captured-at: 2026-08-13T05:41:56+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07
- source-ref: b2ce2a2e01dd005d2b929834c0520f2a5bdff127
- source-manifest-sha256: ca2e85618b2d46aac0fa5af7b4037f7ee19a7633d0bc6a9a75fca96f45c9157f
- docket-revision-sha256: 846feb52f97987e52456ceda9dfd4f80a93b9ec76cab6b0963ef8bb0a1ff4cdc
- input-sha256: 9781fcf794ca8af862f7e8367ccc19e44a8577e1643ac9ea664a4cfb3933bf25
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-81 | 2026-08-13T05:41:56+00:00 | from: codex | type: verdict | thread: collateral-branch-r2 | refs: -

Blocking finding: `rg -n -i -C 1 'builder agent|reviewer agent|one AI agent writes|two AI agents review each other|a builder and a reviewer' README.md PROTOCOL.md docs examples skills .claude-plugin pyproject.toml src/debate --glob '!*.png'` returned `docs/assets/subscription-wall.svg:20` `Fable 5 / Opus — the builder` and `:33` `reviewer agent` (with its builder-to-channel-to-reviewer flow). This source asset has no historical/minimum-topology qualifier, so the retired builder/reviewer two-agent story still appears in the export, failing the docket's everywhere sweep criterion. Fresh required verification was run exactly as `python -m pytest -q`; result: `412 passed, 1 skipped in 18.09s` (exit 0). Other checked collateral was sound: `cmp -s PROTOCOL.md src/debate/protocol_template.md` returned 0; banner/social existed at 1584x672 and 1344x672, and centered-crop comparison returned 0.

Controller-Decision:
- decision: NO_PASS

Controller-Sealed-Reveal:
- reveal-id: f3f9147f39300512c4167014153cae110a7c1c47b58077fb023a93b2df0f3490
- phase: sealed
- captured-at: 2026-08-13T05:36:39+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07
- source-ref: b2ce2a2e01dd005d2b929834c0520f2a5bdff127
- source-manifest-sha256: fa05f9cf4c508aac7cc45c89fa92c1bd1de7b8be96a9cc8854f5c495b3471276
- docket-revision-sha256: 846feb52f97987e52456ceda9dfd4f80a93b9ec76cab6b0963ef8bb0a1ff4cdc
- input-sha256: c0090dd415eca9c13369064f0f767e7dfe73593b4251a4a2947f2d335c3f4729
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-82 | 2026-08-13T05:46:42+00:00 | from: codex | type: verdict | thread: collateral-branch-r2 | refs: -

Blocking finding: the full-export sweep found an unqualified retired builder/reviewer story in `docs/assets/subscription-wall.svg`: line 20 says `Fable 5 / Opus — the builder` and line 33 says `reviewer agent`. This is a shipped source asset and has neither a historical-era nor minimum-topology qualifier, so it violates the docket requirement that nothing anywhere still tell that story. I ran the required command exactly, `python -m pytest -q`, from the export root; it passed: `412 passed, 1 skipped in 17.96s`. The test result cannot satisfy the separate everywhere-sweep criterion.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07
- source-ref: b2ce2a2e01dd005d2b929834c0520f2a5bdff127
- source-manifest-sha256: fa05f9cf4c508aac7cc45c89fa92c1bd1de7b8be96a9cc8854f5c495b3471276
- docket-revision-sha256: 846feb52f97987e52456ceda9dfd4f80a93b9ec76cab6b0963ef8bb0a1ff4cdc
- input-sha256: 9f1c10cbb76576d08db209135a426ed05e6c80c71fa45e5930f7d804ce76e895
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-83 | 2026-08-13T05:52:36+00:00 | from: opus | type: verdict | thread: collateral-branch-r2 | refs: -

NO_PASS — I revise my sealed PASS (MSG-80). My own re-sweep confirms codex's finding, and on re-reading the docket I no longer think the mitigation I applied there survives scrutiny.

COMMAND (run literally, no prefix/suffix/pipe, cwd = export root):
`python -m pytest -q` → `412 passed, 1 skipped in 17.19s` (exit 0). The command criterion is met; it does not speak to the criterion-1 sweep.

BLOCKING FINDING — `docs/assets/subscription-wall.svg` still tells the retired builder/reviewer two-agent story, unqualified:
- :20 `<text …>Fable 5 / Opus — the builder</text>`
- :33 `<text …>reviewer agent</text>` (:34 `GLM-based`)
- :80 `<!-- document flow: builder down to channel, channel up to reviewer -->`, realized as the two arrows at :81/:83.
These are rendered visible labels, not source comments, and the diagram's whole composition is one builder agent on the left, one reviewer agent on the right, channel between. Criterion 1 says "nothing anywhere still tells the retired builder/reviewer two-agent story — sweep yourself, do not trust the diff's coverage."

Why I no longer treat this as a nit. In MSG-80 I discounted it because nothing references the file (I re-confirmed: grepping the export for `subscription-wall` returns zero hits — as it does for `bridge.png`). That imports a reader-facing qualifier the docket did not write, and it is inconsistent with how the same story is handled elsewhere in this very branch: `docs/case-study.md:3-7` was era-marked ("in the era before the three-agent topology") precisely because :13-14 name "The builder"/"The reviewer" as Claude Code and a Hermes-hosted GPT-5.5 seat. `subscription-wall.svg` depicts that identical era and pairing and carries no marker of any kind. Applied consistently, the rule that forced the case-study marker forces one here. It is also a shipped artifact under `docs/assets/` resolving at the same public raw URL pattern the README uses for `banner.png`, so "unreferenced in-repo" is not "unpublished". Fix is small: era-mark the diagram or relabel the two boxes as seats (glm-kimi.md:4-5 shows the accepted alternative — builder/reviewer role names are fine when framed as the two-agent MINIMUM topology).

CRITERIA THAT DO HOLD (re-verified this pass at the pinned export):
- Flow SVG folds: `docs/assets/flow-light.svg` rendered labels are correct — :29 "seat A - debater"/:30 "independent of the author", :34 "seat B - debater", :80-82 "author agent + owner / build the work together, / outside both seats", :84-85 "delivers the branch + review-request", matching README.md:61's alt text. I recomputed the author cubic `M 260 396 C 290 396 285 260 380 226` myself: within the watcher box's y-band (270..340) its maximum x is ≈323 (t≈0.735) versus the box's left edge x=330 — at y=340 x≈289, at t=0.5 (y≈323.8) x≈295.6 — so it clears the watcher on the left and terminates at (380,226) just under the channel box (bottom y=220). Labels at x=262 y=310/325 are likewise left of x=330 and clear of the "wakes whoever's turn it is" text at y=268/283; "prints new entries" moved to x=497,y=370 clears the author box. Hand-built style and the dark palette map (#bc4c00→#f0883e, #fff8f0→#2b1a12) are consistent with the existing pairs.
- Three-agent story accurate at every front-door claim: README.md:14-18, 22-26, 61, 178-183, 467-470; pyproject.toml:8; .claude-plugin/plugin.json; skills/debate/SKILL.md:11-13; src/debate/__init__.py:1; examples/claude-code.md:82-88. Channel stays two-SEAT everywhere (README.md:189, 467-470); glm-kimi.md:3-7 is framed as the two-agent minimum.
- PROTOCOL lockstep and the rest of the sweep: verified at this ref in MSG-80 (`sha256sum PROTOCOL.md src/debate/protocol_template.md` → both `26ead49eb64bc0e17b4a2b6d50052c4ccda0a317eb556d65ab7a9cf989e3703a`, `diff -q` silent); the byte-equality test in tests/test_setup.py is inside today's green run, and codex independently got `cmp -s` = 0. Section 2's role vocabulary (PROTOCOL.md:37-42) is untouched per the non-goal. Language rules hold: no "unforgeable"; README.md:534 reads "at case close the CLIs reported".
- Banner/social preview: composition and 1584x672 / 1344x672 with the centered 2:1 crop were verified by me at this identical pinned manifest (MSG-80) and independently re-confirmed by codex (MSG-81); the export bytes are unchanged, so I did not re-shell for `file` this pass.

NON-BLOCKING NITS (do not gate; fold if convenient with the blocking fix):
- flow-light.svg:27,32,37,43 and flow-dark.svg (same lines) still carry structural comments `builder (left)` / `reviewer (right)` / `builder <-> channel`. Non-rendered, and these are in-scope edited files — worth renaming to seat A/B for consistency, but no reader sees them.
- docs/case-study.md:5-6 — the parenthetical "(the epilogue records how these roles evolved)" overpromises: the Epilogue (:113-146) covers the three amendments becoming v0.5 machinery, never the author-outside-both-seats evolution.
- README.md:117/122 "# The builder asks for a review:" / "# The reviewer answers" in the version-1 quickstart is builder-flavored, but it is the retained two-party path and does not contradict the topology section.

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07
- source-ref: b2ce2a2e01dd005d2b929834c0520f2a5bdff127
- source-manifest-sha256: ca2e85618b2d46aac0fa5af7b4037f7ee19a7633d0bc6a9a75fca96f45c9157f
- docket-revision-sha256: 846feb52f97987e52456ceda9dfd4f80a93b9ec76cab6b0963ef8bb0a1ff4cdc
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

Controller-Decision:
- decision: NO_PASS

Controller-Provenance:
- phase: deliberation
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: b4e677ca97da1bbf998dac5738cce2179f830e2e054ab8c8e7e23ffd6cb8bf07
- source-ref: b2ce2a2e01dd005d2b929834c0520f2a5bdff127
- source-manifest-sha256: ca2e85618b2d46aac0fa5af7b4037f7ee19a7633d0bc6a9a75fca96f45c9157f
- docket-revision-sha256: 846feb52f97987e52456ceda9dfd4f80a93b9ec76cab6b0963ef8bb0a1ff4cdc
- input-sha256: e1308b3a814a454c19a0f195b8a310ea229255c8338841322cf021efc25a1895
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-84 | 2026-08-13T05:52:36+00:00 | from: owner | type: close | thread: collateral-branch-r2 | refs: -

Controller closed the managed case as NO_PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: NO_PASS
- close-reason: party-vote-agreement

## MSG-85 | 2026-08-13T05:54:29+00:00 | from: owner | type: review-request | thread: collateral-branch-r3 | refs: feature/three-agent-collateral@7f51a2300a71bfdb746492c595ad2b1d8506970d

Branch gate round 3: feature/three-agent-collateral@7f51a23 — the subscription-wall.svg finding folded (seat labels + era caption). Full re-sweep welcome. Merge on PASS + green CI.

Controller-Docket-Provenance:
- topology: recommended-three-agent
- controller-config-sha256: 157b3af90c8e98a19febdbe126e0d5a185c48ab58bc76a959841327739f3294a
- source-ref: 7f51a2300a71bfdb746492c595ad2b1d8506970d
- docket-revision-sha256: 5b9392962805ed87db9b57d7741cad5df5bd2d48654c4cb649204ceedc3bb412
- docket-files: [{"path": "collab/PROTOCOL.md", "sha256": "1c463546c33c98648e3225ac5107a01bdece1cf04c46e001aca120188d9e665e", "tracked_at_source_ref": true}, {"path": "collab/repository-unattended-02750.debate.json", "sha256": "e6dc6ecd4e7e0b67f3fe318492c883a65786b97717efe334a1d0f5ad0272bbb2", "tracked_at_source_ref": true}, {"path": "docs/plans/2026-08-13-three-agent-collateral-refresh.md", "sha256": "8e3face1c2572247dbabb29521549a743b3b4d06d2615fbd45fac33da88c2dda", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral-branch-docket.md", "sha256": "f5889096ed231465b6b5c4d84c03c1c4e897c5045c76f710633c993d60292e56", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral.diff", "sha256": "6ba89ad9b58e0717400ecc56964ec0fb555dcf9041ed3c534a5f096760288f9b", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat-result.schema.json", "sha256": "0f03c5e1f0be74c320750c3c2baf5a5a14c39622e34babe8c0b30781578161b1", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/seat_adapter.py", "sha256": "059023723e14c448598515c21dcff9c4acbc844f711edb36667fa48b8064543c", "tracked_at_source_ref": false}, {"path": "var/debate/repository-unattended-02750/collateral-branch-watcher.json", "sha256": "157b3af90c8e98a19febdbe126e0d5a185c48ab58bc76a959841327739f3294a", "tracked_at_source_ref": false}]
- profile-sha256: {"codex": "dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706", "opus": "fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215"}
- sanitized-profile-manifests: {"codex": {"authentication_mode": "Codex subscription OAuth state exposed only to the local wrapper; user config and rules ignored", "author_relationship": "author-independent", "cli_version": "codex-cli 0.146.1", "command_sha256": "ffbf7832ae53855f2de3a7aebb968a791e2b32403ec81bc58fe389d4756ae3bb", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "gpt-5.6-terra", "isolation_mode": "advisory", "party": "codex", "permission_policy": "read-only source export at filesystem layer; workspace-write sandbox limited to controller invocation output/build path", "provider": "openai", "reasoning_effort": "high", "requested_model": "gpt-5.6-terra", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}, "opus": {"authentication_mode": "subscription OAuth state exposed only to the local wrapper; safe mode and settings sources disabled", "author_relationship": "author-independent", "cli_version": "claude-code 2.1.223", "command_sha256": "6e8cf0800354f4a0dfe04684b92f41cfa1cb90a78be45fb63ebffb26b2d352c3", "cost_mode": "subscription", "environment_additions": {"PYTHONPATH": "25a6634263c1b1f6fc4697a04e2b9904ea4b042a89af59dc93ec1f5d44848a26"}, "environment_allowlist": ["PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"], "expected_runtime_model": "claude-opus-5", "isolation_mode": "advisory", "party": "opus", "permission_policy": "read-only source export; result path controller-owned; Read/Grep/Glob plus test-only Bash allowlist", "provider": "anthropic", "reasoning_effort": "high", "requested_model": "claude-opus-5", "result_schema_version": 1, "retry_limit": 0, "schema_version": 1, "session_persistence": false, "settings_sources": [], "timeout_seconds": 540}}
- source-manifest-sha256: {"codex": "33cdc9415385a414485db7da8c75861a05afc1e3bd4fb582a41ca6451e9dd201", "opus": "27e0ecdbc345b43c02b9b07236b8fcc7dd96d2c1187e56e0c873d96baf6d5e1b"}

## MSG-86 | 2026-08-13T06:01:31+00:00 | from: opus | type: verdict | thread: collateral-branch-r3 | refs: -

PASS on `feature/three-agent-collateral@7f51a23`.

## 2. Mandated command (run literally, in the export root)

`python -m pytest -q`

```
........................................................................ [ 17%]
........................................................................ [ 34%]
........................................................................ [ 52%]
........................................................................ [ 69%]
s....................................................................... [ 87%]
.....................................................                    [100%]
412 passed, 1 skipped in 17.59s
```

413 collected matches README.md:488 ("413 tests as of this writing").

## 1. Criterion checks (own sweep, not the diff's coverage)

**Three-agent story everywhere.** Hero README.md:14-18 ("One AI agent builds the work at your side... two more... debate it"; "Three agents, one human"); intro README.md:22-26; flow alt README.md:61; Limits bullet README.md:467-470; pyproject.toml:8; .claude-plugin/plugin.json description; skills/debate/SKILL.md:11-13; src/debate/__init__.py:1. marketplace.json (read in full, 20 lines) carries no topology claim at all — "hold your seat on a debate review channel" — so the round-1 non-blocking ruling still holds on its face.

**Independent sweep for the retired story.** `grep -rn -i "two agents\|two AI agents\|second agent\|a builder and a reviewer\|writes the code"` over md/toml/json/py/svg (tests excluded) returns exactly three hits, all correct: README.md:438 (two agents in a refusal loop = the two seats), docs/case-study.md:11 (inside the era-marked incident), src/debate/setup.py:4 ("makes two agents actually argue" = the two debating seats). A broader case-insensitive sweep for builder|reviewer shows the remainder are party names in CLI examples (examples/claude-code.md:18, examples/demo.py), message-type roles in PROTOCOL (`review-request` builder → reviewer), CHANGELOG history, and the era-marked origin section README.md:490-537.

**Two SEATS / minimum topology / author outside.** README.md:189 "each remains a two-seat debate"; README.md:177-183 states the minimum two-agent topology (one independent seat, author-affiliated self-review honestly labeled) and the recommended three-agent topology with the author/controller outside both seats; examples/glm-kimi.md:5-7 now frames GLM/Kimi as the two-agent minimum with a pointer to the recommended topology; examples/claude-code.md:3-6 already says the interactive author/controller never fills a party turn.

**PROTOCOL lockstep.** `cmp PROTOCOL.md src/debate/protocol_template.md` → IDENTICAL (exit 0). The edit is title + "both agents"→"both seats" only; §5, message types and mechanics are untouched — wording-only.

**Round-1 SVG fold, coordinates verified myself.** In both variants the author path is `M 260 396 C 290 396 285 260 380 226` against a watcher rect of x 330-550, y 270-340. Evaluating the cubic: t=0.70 → (317.9, 277.7); t=0.75 → (325.4, 266.9); the curve crosses y=270 at t≈0.736, x≈323 — left of the x=330 edge — and x(t) is monotonically increasing, so it never enters the watcher box. Labels centered at x=262, font-size 11.5, span roughly x 207-317, also clear of x=330. Author box (40,360,220x76) clears the watcher box and the supervisor strip (y=460). Canvas grown 430→510 in width/height and viewBox together.

**SVG style/palette.** Hand-built style preserved (same rect/text idiom, new `arrowAuthor` marker mirroring the existing two). Dark uses #f0883e stroke on #2b1a12 fill with #e6edf3/#8b949e text; light uses #bc4c00 on #fff8f0 with #1f2328/#57606a — the same light/dark pairing pattern as the existing purple (#8250df/#fbf7ff vs #a371f7/#1c1830) and green (#1a7f37/#f0f7f0 vs #3fb950/#12261a). Box labels ("author agent + owner", "build the work together, outside both seats", "delivers the branch + review-request") match the README flow alt text.

**Round-2 fold (subscription-wall.svg).** Read in full: line 20 "Fable 5 / Opus — the builder seat", line 33 "reviewer seat", and the era caption at line 86, y=490, inside the 880x500 viewBox and clear of the channel box (bottom y=470). It points at README's "Where this comes from" (README.md:490), which exists and opens "provenance, not prescription".

**Language rules.** `grep -i "unforgeable|tamper-evident"` → only README.md:478 "tamper-evident, not tamper-proof" and CHANGELOG.md:189; no "unforgeable" anywhere. README.md:534 now reads "at case close the CLIs reported"; every remaining "final" hit is Python `finally`, a test docstring, or a CI comment.

**Hero images.** Both PNGs exist in the export and render. banner.png matches the plan's chosen composition and the README alt text: two robots opposed across an open ledger on the central lectern, a third robot at a desk beneath the balcony holding the purple document up toward the robed human, who leans over the railing and reaches down. social-preview.png is visibly the same scene as a centered 2:1 crop (both edges trimmed symmetrically; rendered ~1338x669 against the banner's ~1568x670).

Scope note: I could not run a byte-level PNG header probe — `python -c` for the IHDR dimensions was denied by the sandbox, as were `ls` and the docket-root listing. Existence, rendering and aspect ratio are verified visually through the image reader rather than from IHDR bytes; no other criterion depended on a denied command.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: bfae952d4ac641f78fd81fd9c5ee63740a50dbc6078d56a2b23a4d04c838680a
- phase: sealed
- captured-at: 2026-08-13T05:58:28+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: fd2633ee8e875b63af8e4b9e1edf265f494b5b15375c877ce893967ab6907215
- controller-config-sha256: 157b3af90c8e98a19febdbe126e0d5a185c48ab58bc76a959841327739f3294a
- source-ref: 7f51a2300a71bfdb746492c595ad2b1d8506970d
- source-manifest-sha256: 27e0ecdbc345b43c02b9b07236b8fcc7dd96d2c1187e56e0c873d96baf6d5e1b
- docket-revision-sha256: 5b9392962805ed87db9b57d7741cad5df5bd2d48654c4cb649204ceedc3bb412
- input-sha256: a7cb5c3c6a2b06f35fb212da7f54c8deabbfb7ee02b00256b453a48bd7eaa5bf
- requested-model: claude-opus-5
- runtime-model: claude-opus-5
- reasoning-effort: high
- cli-version: claude-code 2.1.223
- isolation-mode: advisory

## MSG-87 | 2026-08-13T06:01:31+00:00 | from: codex | type: verdict | thread: collateral-branch-r3 | refs: -

PASS. Fresh exact verification: `python -m pytest -q` → `412 passed, 1 skipped in 18.34s`. `patch -p1 --dry-run -R < .../collateral.diff` checked every listed text hunk against the export successfully. `cmp -s PROTOCOL.md src/debate/protocol_template.md` returned 0; the flow SVGs show both independent debating seats and the author+owner unit outside the watcher, with matching light/dark palette mappings. Sweep found no `unforgeable` claim or retired unqualified topology story; historical two-seat material is explicitly era/minimum-topology framed. `identify` confirmed `/home/zoltan/Projects/debate/var/debate/repository-unattended-02750/controller/exports/7f51a2300a71bfdb746492c595ad2b1d8506970d/codex/docs/assets/banner.png` is 1584x672 and `social-preview.png` is 1344x672; visual inspection matches the README alt text and required centered 2:1 crop.

Controller-Decision:
- decision: PASS

Controller-Sealed-Reveal:
- reveal-id: bfae952d4ac641f78fd81fd9c5ee63740a50dbc6078d56a2b23a4d04c838680a
- phase: sealed
- captured-at: 2026-08-13T06:01:31+00:00

Controller-Provenance:
- phase: sealed
- topology: recommended-three-agent
- author-relationship: author-independent
- profile-sha256: dcff3412dd23ff7f63be7d40c305bdcf7b96a10d78785ea6af1131c3d8308706
- controller-config-sha256: 157b3af90c8e98a19febdbe126e0d5a185c48ab58bc76a959841327739f3294a
- source-ref: 7f51a2300a71bfdb746492c595ad2b1d8506970d
- source-manifest-sha256: 33cdc9415385a414485db7da8c75861a05afc1e3bd4fb582a41ca6451e9dd201
- docket-revision-sha256: 5b9392962805ed87db9b57d7741cad5df5bd2d48654c4cb649204ceedc3bb412
- input-sha256: 7e0d41dd841ae333dd0f40dc25493ae6c70231e94de38026c835c2d2d0bc589f
- requested-model: gpt-5.6-terra
- runtime-model: gpt-5.6-terra
- reasoning-effort: high
- cli-version: codex-cli 0.146.1
- isolation-mode: advisory

## MSG-88 | 2026-08-13T06:01:31+00:00 | from: owner | type: close | thread: collateral-branch-r3 | refs: -

Controller closed the managed case as PASS. Reason: party-vote-agreement. Supervisor messages were not counted as party votes.

Controller-Terminal:
- terminal-result: PASS
- close-reason: party-vote-agreement
