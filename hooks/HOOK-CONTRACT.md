# Session-start hook contract — Slice 1A plus Codex first-turn fold

Verified against: local `codex-cli 0.148.0`/`0.149.1` + `claude-code 2.1.235`/`2.1.241`
installations, the
working user-level hook at `~/.codex/hooks/session_start.py` (wired via
`~/.codex/hooks.json`, Claude-schema manifest, accepted by Codex), the
`hooks.state` trust blocks in `~/.codex/config.toml`, and
https://learn.chatgpt.com/docs/hooks (rechecked 2026-08-24).

## Input (stdin, JSON, both hosts)

Common fields: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`,
`permission_mode`. Debate's hook uses `cwd` (project root) and tolerates any extra or
missing fields. Malformed JSON on stdin is an error path, never a crash.

## Output (stdout, JSON, both hosts)

- `systemMessage` (string): visible notice in the host UI.
- `hookSpecificOutput.additionalContext` (string): model-only context. Claude requires
  the sibling `hookEventName: "SessionStart"`; Codex tolerates it — always included.
- `continue: false` plus `stopReason` (Codex only): for an unready interactive Codex
  project, visibly stop the first submitted turn before inference. These fields are
  absent for Claude, ready projects, quiet/headless runs, and malformed/broken-hook
  error paths.

## Environment

Codex provides the host-specific `PLUGIN_ROOT`/`PLUGIN_DATA` variables plus legacy
aliases `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA`; Claude provides
`CLAUDE_PLUGIN_ROOT`. The hook uses the presence of `PLUGIN_ROOT` as the attested
Codex host signal. Manifest commands still use `${CLAUDE_PLUGIN_ROOT}` in both
dialects, and the script falls back to its own resolved path when the variable is
absent (direct test invocation).

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
  headless distinction is attested. `PLUGIN_ROOT` identifies Codex, not whether its
  current session is interactive. `DEBATE_ONBOARDING_QUIET=1` is therefore the
  documented automation lever for Codex and suppresses both the warning and
  interruption. Debate's managed `run-seat` bridge sets this signal automatically
  for Codex seats, including seats without an operator configuration folder. It does
  not set it for other vendors. Ordinary interactive Codex sessions do not pass
  through that bridge and retain the visible first-turn stop. This is an honest
  limitation, not a claim of automatic headless detection.

## Codex 0.149.1 lifecycle timing and interruption (2026-08-24)

Installed-host evidence showed that Codex discovers, enables, and trusts the plugin
hook but does not invoke `SessionStart` merely because a prompt-free thread opens.
The first submitted turn invokes it before inference. In an isolated installed-plugin
app-server and real TUI proof, an attention-state hook result containing one
`systemMessage`, `continue: false`, and `stopReason` produced `SessionStart (stopped)`,
an empty completed turn, zero first-turn network requests, zero model-output items,
and zero token-usage events.

Product behavior is therefore host-specific:

- Claude keeps its prompt-free next-launch warning and never receives
  `continue: false`.
- Codex prompt-free startup is silent. Its first submitted prompt is stopped only
  when onboarding reports `offer_setup`, `offer_refresh`, or `repair_required`, and
  only when `PLUGIN_ROOT` is present and quiet mode is off.
- The stopped prompt is not replayed or retained by Debate. The user must repeat it
  to continue normally or reply `set up Debate`.
- Ready projects remain silent. Malformed input, missing engine, import failure, and
  status failure warn but fail open rather than creating a prompt loop.

## Trust

Codex records per-hook trust hashes under `[hooks.state]` in `config.toml`
(`<source>:<event>:<index>:<index>` → `trusted_hash`); a new or changed hook is marked
for review and does not run until the user approves it. Claude prompts on plugin
install. The acceptance flows accept these prompts, never edit around them.
