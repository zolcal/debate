# Session-start hook contract — Slice 1A spike record (2026-08-19)

Verified against: local `codex-cli 0.148.0` + `claude-code 2.1.235` installations, the
working user-level hook at `~/.codex/hooks/session_start.py` (wired via
`~/.codex/hooks.json`, Claude-schema manifest, accepted by Codex), the
`hooks.state` trust blocks in `~/.codex/config.toml`, and
https://learn.chatgpt.com/docs/hooks (fetched 2026-08-19; previously an untrusted
citation — now confirmed on the points below).

## Input (stdin, JSON, both hosts)

Common fields: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`,
`permission_mode`. Debate's hook uses `cwd` (project root) and tolerates any extra or
missing fields. Malformed JSON on stdin is an error path, never a crash.

## Output (stdout, JSON, both hosts)

- `systemMessage` (string): visible notice in the host UI.
- `hookSpecificOutput.additionalContext` (string): model-only context. Claude requires
  the sibling `hookEventName: "SessionStart"`; Codex tolerates it — always included.

## Environment

Codex provides `PLUGIN_ROOT`/`PLUGIN_DATA` with legacy aliases `CLAUDE_PLUGIN_ROOT`/
`CLAUDE_PLUGIN_DATA`; Claude provides `CLAUDE_PLUGIN_ROOT`. Manifest commands therefore
use `${CLAUDE_PLUGIN_ROOT}` in both dialects, and the script itself falls back to its
own resolved path when the variable is absent (direct test invocation).

## Manifests

Per-host files per the approved plan: `hooks/hooks.json` (Claude) and
`hooks/hooks-codex.json` (Codex) -- DEEP-EQUAL documents (branch-gate round-1
finding): one `SessionStart` group, no `matcher`, `hooks[]` of
`{type, command, timeout, async}`. Codex parses the Claude schema and
auto-discovers both paths, preferring `hooks-codex.json` when present (observed
with superpowers in `~/.codex/config.toml`). Current Codex docs allow a top-level `description`, but the
2026-06-26 parser incident on this workstation argues for keeping both manifests
minimal and field-identical. `timeout` is in seconds; ours is 10 (host default 600).

## Non-interactive detection (spike extension, 2026-08-19)

Empirically attested by an env/stdin dump hook in an isolated HOME:

- Claude Code headless (`claude -p`): `CLAUDE_CODE_ENTRYPOINT=sdk-cli`;
  interactive TUI: `CLAUDE_CODE_ENTRYPOINT=cli`. The hook suppresses the
  visible banner when the value is `sdk-cli` (or any `sdk-` prefix).
  The stdin event carries `session_id`, `transcript_path`, `cwd`,
  `hook_event_name`, `source` -- no interactivity field.
- Codex: an UNTRUSTED user hook is silently skipped in `codex exec`, so no
  headless signal could be attested without an interactive trust session.
  Until one is attested, `DEBATE_ONBOARDING_QUIET=1` is the documented
  automation lever for Codex (set it in the automation environment). This
  is an honest limitation, not a claim of detection.

## Trust

Codex records per-hook trust hashes under `[hooks.state]` in `config.toml`
(`<source>:<event>:<index>:<index>` → `trusted_hash`); a new or changed hook is marked
for review and does not run until the user approves it. Claude prompts on plugin
install. The acceptance flows accept these prompts, never edit around them.
