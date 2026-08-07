# Wiring a real agent: Claude Code as one side

This page documents the managed-version 1 compatibility shape: fresh headless Claude Code and a second
CLI-invocable agent. The interactive author/controller and human supervisor observe the
record but never fill a party turn. Nothing here is Claude-specific beyond the command line;
substitute any conforming headless harness.

For new isolated gates, use managed version 2 and the brokered profile contract in the
README. Version 1 agents receive the live channel path and self-post, so this page must not
be cited as proof of sender binding or sealed context isolation. A version 2 wrapper writes
the controller-owned result JSON and includes `decision: PASS` or `decision: NO_PASS` for
every verdict; it never calls `debate post` itself.

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
debate post --root collab --channel myproject-48213 --from claude --type review-request \
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
    "claude":   "Review channel ./collab --channel myproject-48213: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab --channel myproject-48213` — never the whole mailbox file. Verify `debate status --root collab --channel myproject-48213` still shows an open thread AND turn=='claude' — if not, exit. Constraints: feature-branch commits only; no merges or pushes to main; verify any claim about repo state against git directly, never from channel history; if the working tree is dirty, restrict yourself to read-only verification and posting — build in a separate worktree. Post via `debate post --root collab --channel myproject-48213`, then stop.",
    "reviewer": "Review channel ./collab --channel myproject-48213: it is your turn. Read PROTOCOL.md, then the open thread via `debate read --root collab --channel myproject-48213`. Do what the latest entry asks. For verdicts, cite YOUR OWN fresh evidence: current HEAD and a fresh test run, never the author's pasted evidence. Post via `debate post --root collab --channel myproject-48213`, then stop."
  },
  "debounce_seconds": { "claude": 0, "reviewer": 0 },
  "retry_seconds": 1800
}
```

Schedule it (cron, systemd timer, Windows Task Scheduler, or your harness's own scheduler —
the production setup used Hermes's cron):

```bash
*/3 * * * *  cd /path/to/your-project && debate watch-once --root collab --channel myproject-48213 --config watcher.json
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

## 5. Minimum and recommended topologies

The minimum uses two agent identities: the interactive author is also represented by a
fresh headless, `author-affiliated` seat, and the opposing seat is
`author-independent`. For example, a Codex-authored change can use a fresh headless Codex
profile plus headless Opus. The interactive session never fills the turn itself.

The recommended topology uses three agent identities: the interactive author/controller
is outside both seats and both headless profiles are `author-independent`. This
repository's current proof uses interactive GPT-5.6 Sol outside headless Opus 5
(`claude:opus/high`) and headless GPT-5.6 Terra (`codex:gpt-5.6-terra/high`). Record the
actual resolved model returned by each wrapper; an alias is a request, not proof of the
runtime identity. Fable 5 or an older Opus may be selected in a different fresh profile,
but changing model, effort, relationship, permissions or authentication opens a new case.
