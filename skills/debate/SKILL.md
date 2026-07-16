---
name: debate
description: Use when a debate review channel (CHANNEL.md, signal.json, debate.json) exists in or near the project, when a scheduler wakes you to act on one, or when the user asks to request, perform, or close a cross-vendor AI-agent code review through the debate CLI.
compatibility: Requires the debate CLI on PATH (pip install debate; Python 3.10+, zero dependencies)
---

# debate — hold your seat on a cross-vendor review channel

## Overview

`debate` coordinates two AI agents from different vendors through an append-only mailbox
(`CHANNEL.md`) and a doorbell (`signal.json`) in a shared folder. The CLI is the only writer
and it enforces the rules: turn order, one open thread at a time, message caps.

**Core principle: if it didn't happen through `debate post`, it didn't happen.**

## Preflight — every wake-up, in order

1. **CLI present?** If `debate --help` fails: **STOP — fail closed.** Report to your human:
   "debate CLI not found — install with `pip install debate` (or `pipx install debate` /
   `uv tool install debate`), then wake me again." Do not improvise an alternative: no
   editing channel files by hand, no running the package from a source checkout, no
   installing anything yourself without the user's explicit go-ahead.
2. **Read `PROTOCOL.md`** at the channel root, if present — it holds channel-specific rules.
3. **Check state:** `debate status --root <root>`. Act only if **both** hold:
   `thread` is non-empty (a discussion is open) **and** `turn` equals your party name.
   - No open thread → there is nothing to do. **Exit without posting.** After a close, the
     turn field means nothing.
   - Turn is not yours → exit without posting.
4. **Read the open thread:** `debate read --root <root>` — never the raw `CHANNEL.md`.
   Channels grow forever (real ones exceed 100 KB); your working set is the open thread.
   Use `--since <seq>` for what's new, `--thread <slug>` for history when explicitly needed.

## Act — one reply per wake-up

- Do what the latest entry asks. Verify every claim about repo state against git and fresh
  test runs directly — channel history is a record of what was said, not of what is true now.
- Post only through the CLI:
  `debate post --root <root> --from <you> --type <type> --thread <slug> --body "..."`
  Types: `review-request`, `verdict`, `fix-report`, `question`, `info`, `close`.
- `--refs` cites code, never messages: `branch@shortsha` of the commit you are talking
  about. Add `--verify-refs <repo>` so unresolvable citations are refused. Threads already
  link replies; never put `MSG-n` in refs.
- Verdicts cite your own fresh evidence: what you ran, at which commit, what the counts were.
- If the CLI refuses your post, the state changed under you — exit and let the next wake-up
  handle it. `--force` is for human supervisors, never for you.
- Then stop. One doorbell change, one reply.

## You are stateless — expect amnesia

Messages from your party name were posted by earlier sessions of you that you cannot
remember. **Not remembering a message is never evidence of spoofing or tampering.** Do not
accuse, do not "correct the record", do not ask for merges to be reverted based on missing
memory. If something on the channel looks genuinely wrong, say so in your session output for
the human supervisor — do not post about it.

## Boundaries the tool cannot enforce (they are on you)

- Never edit `CHANNEL.md`, `signal.json`, or `debate.json` by hand — corrections are new
  messages, never edits.
- No merges, no pushes to protected branches — humans merge.
- Dirty working tree that isn't yours → restrict yourself to read-only verification and
  posting; build in a separate git worktree.

## Rationalizations — all of them mean stop

| Excuse | Reality |
|---|---|
| "The channel file is small, I'll just read it" | Working set = open thread. `debate read`. Always. |
| "CLI is missing but I found the source / another way to write" | Fail closed. Enforced turn-taking IS the product; a bypass is a protocol breach even when convenient. |
| "I don't remember posting MSG-n, so it must be forged" | You are stateless. An earlier session of you posted it. |
| "Nothing is open, but the team is waiting — I'll post a status" | No open thread = done. Exit silently. |
| "refs should point at the message I'm answering" | refs = `branch@sha` of code. Replies are linked by the thread. |

## Red flags — STOP and exit

- About to Write/Edit any file inside the channel root
- About to post when `status` shows no open thread, or a turn that isn't yours
- About to install or work around a missing binary without the user's explicit approval
- About to state repo facts sourced from channel history instead of git
