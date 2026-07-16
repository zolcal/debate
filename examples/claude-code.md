# Wiring a real agent: Claude Code as one side

This is the shape the production deployment used — Claude Code as the builder, any other
CLI-invocable agent as the reviewer. Nothing here is Claude-specific beyond the command line;
substitute your harness's headless invocation.

## 1. The channel lives in your repo

```bash
cd your-project
debate init --root collab --parties claude,reviewer --supervisor owner
# commit collab/debate.json and your filled-in PROTOCOL.md; gitignore collab/signal.json
```

## 2. The live path (primary)

You work with Claude Code interactively. When a branch is ready:

```bash
debate post --root collab --from claude --type review-request \
    --thread my-feature --refs my-feature@$(git rev-parse --short HEAD) \
    --body-file review-request.md
```

Your reviewer's harness watches the doorbell (see step 3) and replies. The live session reads
the verdict and acts. The human merges.

## 3. The watcher (fallback + mirror)

`watcher.json` — note both agents get **pinned prompts**, composed never:

```json
{
  "state_path": "~/.local/state/debate/my-project.json",
  "commands": {
    "claude":   ["claude", "-p", "{prompt}"],
    "reviewer": ["your-agent", "--headless", "{prompt}"]
  },
  "prompts": {
    "claude":   "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab` — never the whole CHANNEL.md. Verify signal.json still shows an open thread AND turn=='claude' — if not, exit. Constraints: feature-branch commits only; no merges or pushes to main; verify any claim about repo state against git directly, never from channel history; if the working tree is dirty, restrict yourself to read-only verification and posting — build in a separate git worktree. Post via `debate post`, then stop.",
    "reviewer": "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab`. Do what the latest entry asks. For verdicts, cite YOUR OWN fresh evidence: current HEAD and a fresh test run. Post via `debate post`, then stop."
  },
  "debounce_seconds": { "claude": 600 },
  "retry_seconds": 1800
}
```

Schedule it (cron, systemd timer, Windows Task Scheduler, or your harness's own scheduler —
the production setup used Hermes's cron):

```bash
*/3 * * * *  cd /path/to/your-project && debate watch-once --root collab --config watcher.json
```

Route the tick's stdout wherever you already look — the production setup piped it to Telegram.

## 4. The lessons baked into those prompts

The `claude` prompt above is not boilerplate — every clause was added after the fallback's
first real firing ([case study](../docs/case-study.md)):

- *"verify any claim about repo state against git directly"* — because an unattended session
  once announced a branch was pending sign-off fifteen minutes after it had been merged.
- *"if the working tree is dirty… build in a separate git worktree"* — because the fallback
  shares a checkout with your live session, and the debounce is a heuristic, not a lock.
- The 10-minute debounce — because a live session usually answers first, and the fallback
  should behave like one.
