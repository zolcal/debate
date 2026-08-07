# Wiring a real agent: Claude Code as one side

This is the managed two-agent shape: fresh headless Claude Code and a second
CLI-invocable agent. The interactive author/controller and human supervisor observe the
record but never fill a party turn. Nothing here is Claude-specific beyond the command line;
substitute any conforming headless harness.

## 1. The channel lives in your repo

```bash
cd your-project
debate init --root collab --parties claude,reviewer --supervisor owner
# init prints the channel id, e.g. 'myproject-48213'
# commit collab/*.debate.json and your filled-in PROTOCOL.md; gitignore collab/*.signal.json
```

## 2. Open the review through the author-proponent automation

When a branch is ready, the controller or author-proponent wrapper opens the request:

```bash
debate post --root collab --from claude --type review-request \
    --thread my-feature --refs my-feature@$(git rev-parse --short HEAD) \
    --body-file review-request.md
```

Both headless commands below drive their own turns. The interactive controller may explain
the result, and the human merges, but neither is a party fallback.

## 3. The watcher (driver + mirror)

`watcher.json` — note both agents get **pinned prompts**, composed never:

```json
{
  "state_path": "~/.local/state/debate/my-project.json",
  "commands": {
    "claude":   ["claude", "-p", "{prompt}"],
    "reviewer": ["your-agent", "--headless", "{prompt}"]
  },
  "prompts": {
    "claude":   "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab` — never the whole mailbox file. Verify `debate status --root collab` still shows an open thread AND turn=='claude' — if not, exit. Constraints: feature-branch commits only; no merges or pushes to main; verify any claim about repo state against git directly, never from channel history; if the working tree is dirty, restrict yourself to read-only verification and posting — build in a separate git worktree. Post via `debate post`, then stop.",
    "reviewer": "Review channel ./collab: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab`. Do what the latest entry asks. For verdicts, cite YOUR OWN fresh evidence: current HEAD and a fresh test run. Post via `debate post`, then stop."
  },
  "debounce_seconds": { "claude": 0, "reviewer": 0 },
  "retry_seconds": 1800
}
```

Schedule it (cron, systemd timer, Windows Task Scheduler, or your harness's own scheduler —
the production setup used Hermes's cron):

```bash
*/3 * * * *  cd /path/to/your-project && debate watch-once --root collab --config watcher.json
```

Route the tick's stdout wherever you already look — the production setup piped it to Telegram.
The `cd` matters: agents inherit the watcher's working directory, so the prompts' relative
paths (`./collab`, `PROTOCOL.md`) resolve against your project root. A systemd unit or Task
Scheduler job needs `WorkingDirectory` / "Start in" set to the same place.

## 4. The lessons baked into those prompts

The `claude` prompt above is not boilerplate — every clause was added after the old
fallback's first real firing ([case study](../docs/case-study.md)):

- *"verify any claim about repo state against git directly"* — because an unattended session
  once announced a branch was pending sign-off fifteen minutes after it had been merged.
- *"if the working tree is dirty… build in a separate git worktree"* — because a headless
  seat may still share a checkout with the controller; zero debounce is not a checkout lock.
- Zero debounce — every managed turn belongs to a fresh headless invocation; there is no
  live-session fallback that can hold the thread open.
