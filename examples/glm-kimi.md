# Wiring a non-duopoly pairing: GLM + Kimi

Two model backends, neither Anthropic nor OpenAI: GLM (Zhipu) as the builder, Kimi
(Moonshot) as the reviewer — coordinating through the same two-file mailbox as any other
pairing. (GLM's documented harness is Claude Code; the *backend* is what escapes the
duopoly, and the identity check below proves which backend answered.) The tool is
vendor-neutral; only the `commands` and `prompts` in the watcher change.

## 0. The GLM seat: a wrapper, and why

GLM has no standalone CLI; z.ai's documented path is occupying an Anthropic-compatible
harness — Claude Code — via environment repointing. The IDE integrations on z.ai's docs
(VS Code, Kilo, Droid, …) are irrelevant here: the watcher needs exactly one thing, a
headless one-shot CLI, and `claude -p` under the GLM endpoint is that. Create
`~/.local/bin/glm-agent` (secret-free repo; key sourced at runtime):

```bash
#!/bin/bash
# GLM seat for debate: claude -p repointed at z.ai's Anthropic-compatible endpoint.
set -euo pipefail
. ~/.secrets   # provides GLM_API_KEY - never inline it in watcher.json
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="$GLM_API_KEY"
export ANTHROPIC_MODEL="glm-4.6"   # override any locally pinned model
exec claude -p "$1" </dev/null
```

Make it executable and PATH-visible for the watcher (cron inherits a minimal PATH —
use an absolute argv in `watcher.json` if unsure): `chmod +x ~/.local/bin/glm-agent`.

**Fail-closed identity check (run at setup, and after any `claude` upgrade) — it refuses,
not warns:**

```bash
glm-agent "Reply with exactly: SEAT-OK <your model name>" | grep -q "SEAT-OK glm-" \
  || { echo "REFUSED: this seat is NOT answering as GLM - fix the wrapper env"; exit 1; }
```

A GLM-native harness, if one ships, is a drop-in: replace the wrapper, keep the prompt.

## 1. The channel lives in your repo

```bash
debate init --root collab --parties glm,kimi --supervisor owner
# commit collab/debate.json and your filled-in PROTOCOL.md; gitignore collab/signal.json
```

## 2. The watcher (fallback + mirror)

`watcher.json` — GLM through the wrapper above, Kimi through its own CLI. `kimi -p` runs
one prompt non-interactively; note its prompt mode auto-approves tool calls (it cannot be
combined with `--yolo`/`--auto` and needs neither) — the pinned prompt and your repo
boundary are the safety controls, same as any unattended seat:

```json
{
  "state_path": "~/.local/state/debate/my-project.json",
  "commands": {
    "glm":  ["glm-agent", "{prompt}"],
    "kimi": ["kimi", "-p", "{prompt}"]
  },
  "prompts": {
    "glm":  "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab` — never the whole CHANNEL.md. Immediately before acting, verify collab/signal.json still shows a NON-EMPTY thread AND turn=='glm' — if not, exit without posting. Constraints: feature-branch commits only; no merges or pushes to main; verify any claim about repo state against git directly, never from channel history; if the working tree is dirty, restrict yourself to read-only verification and posting — build in a separate git worktree. Post via `debate post`, then stop.",
    "kimi": "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab`. Immediately before acting, verify collab/signal.json still shows a NON-EMPTY thread AND turn=='kimi' — if not, exit without posting. Do what the latest entry asks. For verdicts, cite YOUR OWN fresh evidence: current HEAD and a fresh test run. Post via `debate post`, then stop."
  },
  "debounce_seconds": { "glm": 600 },
  "retry_seconds": 1800
}
```

> Agents inherit the watcher's working directory (debate >= 0.3.1), so the relative paths
> above resolve against your project root — that is why the cron below `cd`s first. A
> systemd unit or Task Scheduler job needs `WorkingDirectory` / "Start in" set the same
> way. A hung agent is bounded by `timeout_seconds` (default 1800), not by stdin tricks.

## 3. Run it

```bash
*/3 * * * *  cd /path/to/your-project && debate watch-once --root collab --config watcher.json
```

Route the tick's stdout wherever you already look.

## 4. The same lessons apply

Every clause in those prompts was paid for in production with a different pairing — they
are model-neutral. Verify repo state against git, not channel history; build in a worktree
on a dirty tree; one reply, then stop. Full incident provenance in `examples/claude-code.md`.

## Notes

- Builder/reviewer roles are arbitrary; flip them by swapping which party you drive live.
- A Mistral seat, a Qwen Code seat, or a local open-weight model behind any headless CLI
  slots in the same way: one argv, one pinned prompt.
- CLI surfaces drift. Re-run the identity check and a one-line `kimi -p "Reply OK"` after
  upgrading either tool.
