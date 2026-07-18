# Reliability Hardening v0.3 Implementation Plan (r4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**r4:** self-contained (no references to earlier revisions); per Codex MSG-13: D6 = decision snapshot
under the channel writer lock covering invoke/new-escalation/persisted-STUCK; turnless threads are
supervisor-only states; raising-sleep test pattern; bounded-polling lock tests + real
watch-through-sleep exclusion; `W` is a real shell assignment; worktree carries the examples fix;
Task 9 requires a clean worktree.

**Goal:** Ship debate v0.3.0 with no silent agent hangs, no uncaught watcher crashes, truthful turn staleness, a run-to-completion `debate watch` loop, and an opener allowlist.

**Architecture:** All changes in `watcher.py` (D1/D3/D6) and `channel.py` + `__main__.py` (D2/D4), pure-decision-core + thin-CLI pattern. Spec: `docs/plans/2026-07-15-reliability-hardening.md` (r4).

**Tech Stack:** Python 3.10+ stdlib only, pytest, mypy --strict, ruff (line-length 120).

## Global Constraints

- Zero runtime dependencies; stdlib only. Python floor 3.10.
- **Every shell block begins with `W=~/Projects/debate-reliability-v0.3` and operates in
  `$W`** (the worktree created in Task 0). The main checkout `~/Projects/debate` is touched
  only to create the worktree and to post on its `collab/` channel (absolute path) in Task 9.
- Do NOT modify `skills/debate/SKILL.md` beyond the verbatim copy in Task 0.
- Staging: explicit paths only — NEVER `git add -A` / `git add .`.
- Tests: `cd "$W" && PYTHONPATH=src python3 -m pytest tests/ -q --basetemp=.pytest-tmp`.
- Gate after every task: tests green + the EXACT ruff/mypy commands from `$W/.github/workflows/ci.yml`
  (recorded in Task 0).
- The lock uses `fcntl` (POSIX) / `msvcrt` (Windows): platform-guard the imports (inside methods) — CI
  runs a Windows leg.
- Watch-loop tests that must exit before sleeping pass a sleep callable that RAISES (`AssertionError`)
  — a regression fails, never hangs pytest.
- Line length 120; match existing comment density and docstring style.

---

### Task 0: Worktree, deliverable ownership, hygiene

- [ ] **Step 1:**

```bash
W=~/Projects/debate-reliability-v0.3
git -C ~/Projects/debate worktree add "$W" -b reliability-v0.3 main
test -d "$W/src/debate" || { echo "worktree missing"; exit 1; }
```

- [ ] **Step 2:** Bring the v0.3 deliverables (currently untracked / modified only in the main
  checkout) into the branch so it owns them from commit one — including the already-made
  `examples/claude-code.md` prompt fix:

```bash
W=~/Projects/debate-reliability-v0.3
cp -r ~/Projects/debate/.claude-plugin ~/Projects/debate/skills "$W/"
cp ~/Projects/debate/examples/claude-code.md "$W/examples/claude-code.md"
cd "$W" && git add .claude-plugin skills examples/claude-code.md && \
  git commit -m "feat: Claude Code skill + plugin manifests; examples use debate read (distribution slice 1)"
```

(The plugin-install smoke test remains an owner-gated step per the handover — committing to a branch
publishes nothing; the owner runs `claude plugin marketplace add` when they choose.)

- [ ] **Step 3:** Commit the plan documents into the branch so the reviewed SHA carries them (Task 9
  points the reviewer at their relative paths):

```bash
W=~/Projects/debate-reliability-v0.3
cp ~/Projects/debate/docs/plans/2026-07-15-reliability-hardening.md \
   ~/Projects/debate/docs/plans/2026-07-15-reliability-hardening-plan.md "$W/docs/plans/"
cd "$W" && git add docs/plans/2026-07-15-reliability-hardening.md docs/plans/2026-07-15-reliability-hardening-plan.md && \
  git commit -m "docs: reliability v0.3 spec (r4, codex-approved) + implementation plan"
```

- [ ] **Step 3b:** Read `$W/.github/workflows/ci.yml`; record its exact ruff/mypy commands — they are the per-task gate.
- [ ] **Step 4:** `cd "$W" && echo ".pytest-tmp/" >> .gitignore && git add .gitignore && git commit -m "chore: project-local pytest basetemp"`
- [ ] **Step 5:** Baseline: `cd "$W" && PYTHONPATH=src python3 -m pytest tests/ -q --basetemp=.pytest-tmp` — all pass.

---

### Task 1: D1 — stdin=DEVNULL

**Files:** Modify `src/debate/watcher.py` (the `subprocess.run` call in `run_once`); test `tests/test_watcher.py`.

**Interfaces:** `run_once` passes `stdin=subprocess.DEVNULL`; the launch stays one `subprocess.run` call site.

- [ ] **Step 1: Failing test** (kwargs spy — deterministic; accepted by review in MSG-9):

```python
def test_agent_is_launched_with_stdin_detached(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An inherited tty/pipe stdin hung a real review for 3h (a production channel, 2026-07-15)."""
    import debate.watcher as watcher_mod

    root = make_channel(tmp_path)
    seen: dict[str, Any] = {}

    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        seen.update(kwargs)
        return subprocess.CompletedProcess(argv, 0, stdout="")

    monkeypatch.setattr(watcher_mod.subprocess, "run", fake_run)
    run_once(config(root, commands={"alpha": ["agent"]}, prompts={"alpha": "go"}))
    assert seen["stdin"] is subprocess.DEVNULL
```

Add this helper once (used by every watcher test below), modeled on the arrangement in
`test_run_once_invokes_configured_command_and_mirrors_reply` (tests/test_watcher.py:143):

```python
def make_channel(tmp_path: Path) -> Path:
    """A channel with one open thread: beta requested review on t-one; turn=alpha; seq=1."""
    from debate import channel

    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    return root
```

- [ ] **Step 2:** Run — expected FAIL: `KeyError: 'stdin'`.
- [ ] **Step 3:** Add `stdin=subprocess.DEVNULL,` to the `subprocess.run` call, comment
  `# an inherited tty/pipe stdin hung a real agent for 3h`.
- [ ] **Step 4:** Test + full suite PASS.
- [ ] **Step 5:** `cd "$W" && git add src/debate/watcher.py tests/test_watcher.py && git commit -m "fix(watcher): detach agent stdin (DEVNULL)"`

---

### Task 2: D1 — caught launch failures, terminal escalation, argv hygiene

**Files:** Modify `src/debate/watcher.py` (`decide`, `WatcherConfig.__post_init__`, launch block); test `tests/test_watcher.py`.

**Interfaces:** `decide()` returns `Decision(None, None, "seq <n> already escalated")` BEFORE any retry logic when `f"{thread}:{seq}"` is escalated (Task 5 keys the STUCK line off this exact reason suffix). Launch catches `subprocess.TimeoutExpired` and `(OSError, ValueError)`. `WatcherConfig` raises `ChannelError` on non-str argv elements.

- [ ] **Step 1: Failing tests:**

```python
def test_agent_timeout_is_reported_not_raised(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "import time; time.sleep(5)"]},
                 prompts={"alpha": "go"}, timeout_seconds=1)
    lines = run_once(cfg)  # must not raise
    assert any("TIMEOUT after 1s (killed)" in line for line in lines)
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert state["invocations"]["1"]["count"] == 1  # retry machinery still armed


def test_missing_binary_escalates_and_never_relaunches(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": ["/nonexistent/bin/agent-xyz"]}, prompts={"alpha": "go"})
    first = run_once(cfg)
    assert any(line.startswith("invoke failed for alpha:") for line in first)
    assert any(line.startswith("ESCALATE:") for line in first)
    second = run_once(cfg)  # later tick: escalation is terminal
    assert not any("invoke failed" in line for line in second)
    assert not any(line.startswith("ESCALATE:") for line in second)
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert state["invocations"]["1"]["count"] == 1  # exactly one launch attempt ever


def test_escalated_seq_is_never_retried_even_after_retry_window(tmp_path: Path) -> None:
    state = {"invocations": {"1": {"count": 1, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": ["t-one:1"]}
    cfg = config(tmp_path, commands={"alpha": ["agent"]}, prompts={"alpha": "go"})
    decision = decide(signal(turn="alpha", thread="t-one", seq=1), state, cfg, NOW)
    assert decision.invoke is None
    assert decision.reason.endswith("already escalated")


def test_non_string_command_elements_are_refused_at_config_time(tmp_path: Path) -> None:
    with pytest.raises(ChannelError, match="command"):
        config(tmp_path, commands={"alpha": ["agent", 42]})  # type: ignore[list-item]
```

(adapt `signal()`/`config()`/`NOW` to the module's existing helpers.)

- [ ] **Step 2:** Run — FAIL on all four (timeout raises; tick 2 relaunches; escalated seq invokes; int argv accepted).
- [ ] **Step 3: Implement.** (a) In `decide()`, immediately before the `if count == 0:` branch:

```python
    if f"{thread}:{seq}" in set(state.get("escalated", [])):
        return Decision(None, None, f"seq {seq} already escalated")
```

(b) In `WatcherConfig.__post_init__`, after the state-path refusal:

```python
        for party, argv in self.commands.items():
            if not all(isinstance(part, str) for part in argv):
                raise ChannelError(f"refused: command for {party!r} has non-string elements: {argv!r}")
```

(c) Wrap the launch (the single `subprocess.run` call site from Task 1):

```python
        try:
            proc = subprocess.run(
                argv,
                cwd=config.channel_root,
                text=True,
                stdin=subprocess.DEVNULL,  # an inherited tty/pipe stdin hung a real agent for 3h
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=config.timeout_seconds,
                creationflags=CREATE_NO_WINDOW,
            )
        except subprocess.TimeoutExpired:
            # Already on the books; the once-per-seq retry machinery takes it from here.
            output.append(
                f"invoked {party} for seq {seq}: TIMEOUT after {config.timeout_seconds}s (killed)"
            )
        except (OSError, ValueError) as error:
            # A missing binary or bad argv will not heal on retry: terminal.
            output.append(f"invoke failed for {party}: {error}")
            output.append(
                f"ESCALATE: cannot launch agent for {party!r} on thread {thread!r} - fix the watcher config"
            )
            state = record_escalation(state, thread, seq)
        else:
            status = "ok" if proc.returncode == 0 else f"exit {proc.returncode}"
            output.append(f"invoked {party} for seq {seq}: {status}")
```

(`party`/`thread`/`seq` are the locals available at the call site — Task 6 restructures this block
and fixes the exact names; keep them consistent with the code you find.)

- [ ] **Step 4:** Tests + suite PASS.
- [ ] **Step 5:** `cd "$W" && git add src/debate/watcher.py tests/test_watcher.py && git commit -m "fix(watcher): terminal launch-failure escalation; caught timeouts; argv type validation"`

---

### Task 3: D2 — truthful turn age

**Files:** Modify `src/debate/channel.py` (`turn_parked_since`), `src/debate/__main__.py` (status args + branch); test `tests/test_channel.py`, `tests/test_cli_status.py` (create).

**Interfaces:** `channel.turn_parked_since(root: Path, now: datetime) -> tuple[int | None, int] | None`
— outer None: no open thread OR empty turn (turnless = supervisor-only state). Otherwise
`(age_seconds | None, assigning_seq)`; `age_seconds is None` means "age unknown: malformed stamps".
Scan is over the open thread's entries only, newest-first, last party-authored entry assigns. Naive
stamp → UTC. Malformed party stamp → fall back to signal `updated_at`; both malformed → `(None, seq)`.
CLI contract: parked line `turn '<p>' parked <H>h<MM>m on '<t>' (seq <n>)`; unknown age →
`turn '<p>' parked (age unknown; malformed stamps) on '<t>' (seq <n>)`; turnless →
`thread '<t>' open with no turn — supervisor close required` (a non-close supervisor post preserves
the empty turn, channel.py:245-248 — only close resolves it); JSON
`turn_age_seconds` only when age is a number. `--stale-after N` (argparse `>= 0`) exits 3 when: age
number `>= N`, OR age unknown, OR thread is turnless — the last two are unconditionally stuck states.

- [ ] **Step 1: Failing helper tests** (in `tests/test_channel.py`; `from datetime import datetime, timedelta, timezone`, `import dataclasses`):

```python
def _open_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "review please")  # assigns turn=alpha, seq 1
    return root


def test_turn_parked_since_survives_supervisor_interjection(tmp_path: Path) -> None:
    root = _open_channel(tmp_path)
    channel.post(root, "owner", "info", "t-one", "supervisor note")  # preserves turn, refreshes updated_at
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    result = channel.turn_parked_since(root, now)
    assert result is not None
    age, seq = result
    assert seq == 1
    assert age is not None and age >= 3 * 3600  # NOT reset by the interjection


def test_turn_parked_since_none_when_no_open_thread(tmp_path: Path) -> None:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    assert channel.turn_parked_since(root, datetime.now(timezone.utc)) is None


def test_turn_parked_since_none_for_turnless_supervisor_opened_thread(tmp_path: Path) -> None:
    """Supervisor opener leaves turn empty: both parties are turn-refused (channel.py:220),
    so there is no parked party — a supervisor-only state. The open-thread scan filter is
    exercised here: the only party entries belong to the closed thread and must not leak in."""
    root = _open_channel(tmp_path)
    channel.post(root, "alpha", "verdict", "t-one", "ok")
    channel.post(root, "beta", "close", "t-one", "closing")
    channel.post(root, "owner", "verdict", "t-new", "supervisor opener")  # open thread, turn ""
    assert channel.turn_parked_since(root, datetime.now(timezone.utc)) is None


def test_turn_parked_since_open_thread_filter_skips_foreign_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Genuinely exercise the open-thread scan filter (the turnless test above returns
    before scanning): inject a NEWER party entry on a foreign thread and prove the
    assignment still comes from the open thread's own party entry."""
    import dataclasses

    root = _open_channel(tmp_path)  # open thread t-one, opener seq 1 by beta
    entries = channel.read_entries(root)
    foreign = dataclasses.replace(entries[-1], seq=99, thread="t-foreign",
                                  timestamp="2026-07-15T23:00:00+00:00")
    monkeypatch.setattr(channel, "read_entries", lambda r: [*entries, foreign])
    now = datetime(2026, 7, 16, 0, 0, 0, tzinfo=timezone.utc)
    result = channel.turn_parked_since(root, now)
    assert result is not None
    _, seq = result
    assert seq == 1  # the foreign newer entry was skipped by the thread filter


def test_turn_parked_since_naive_stamp_counts_as_utc(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _open_channel(tmp_path)
    entries = channel.read_entries(root)
    naive = [dataclasses.replace(e, timestamp="2026-07-15T00:00:00") for e in entries]  # no tzinfo
    monkeypatch.setattr(channel, "read_entries", lambda r: naive)
    now = datetime(2026, 7, 15, 2, 0, 0, tzinfo=timezone.utc)
    result = channel.turn_parked_since(root, now)
    assert result is not None
    age, _ = result
    assert age == 2 * 3600  # exact: naive parsed as UTC


def test_turn_parked_since_malformed_party_stamp_falls_back_to_updated_at(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _open_channel(tmp_path)
    entries = channel.read_entries(root)
    broken = [dataclasses.replace(e, timestamp="not-a-stamp") for e in entries]
    monkeypatch.setattr(channel, "read_entries", lambda r: broken)
    updated_at = datetime.fromisoformat(str(channel.read_signal(root)["updated_at"]))
    now = updated_at + timedelta(hours=2)  # make the fallback value distinctly nonzero
    result = channel.turn_parked_since(root, now)
    assert result is not None
    age, _ = result
    assert age is not None and abs(age - 2 * 3600) <= 2  # the FALLBACK value, not a fabricated 0


def test_turn_parked_since_both_stamps_malformed_reports_unknown(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _open_channel(tmp_path)
    entries = channel.read_entries(root)
    broken = [dataclasses.replace(e, timestamp="not-a-stamp") for e in entries]
    monkeypatch.setattr(channel, "read_entries", lambda r: broken)
    signal = dict(channel.read_signal(root))
    signal["updated_at"] = "also-garbage"
    monkeypatch.setattr(channel, "read_signal", lambda r: signal)
    result = channel.turn_parked_since(root, datetime.now(timezone.utc))
    assert result is not None
    age, seq = result
    assert age is None and seq == 1  # unknown age - never a fabricated number, never a raise
```

(Confirm `Entry` is a frozen dataclass with a `timestamp` field first; if the field is named
differently, adapt; if entries carry no stamp, extend the header parser minimally.)

- [ ] **Step 2:** Run — FAIL: no `turn_parked_since`.
- [ ] **Step 3: Implement** in `channel.py` (near `read_signal`):

```python
def turn_parked_since(root: Path, now: datetime) -> tuple[int | None, int] | None:
    """(age_seconds, assigning_seq) for the parked turn of the open thread.

    The turn is assigned by the last PARTY-authored entry of the OPEN thread:
    supervisor interjections preserve the turn but refresh ``updated_at``, so
    the signal alone measures channel idleness - the wrong thing. Outer None:
    no open thread, or the thread has no turn (supervisor opener - a
    supervisor-only state, since turn enforcement refuses both parties).
    age None: both the party stamp and ``updated_at`` are malformed - age is
    unknown, never fabricated, and this function never raises.
    """
    signal = read_signal(root)
    open_thread = str(signal.get("thread", ""))
    if not open_thread or not str(signal.get("turn", "")):
        return None
    config = load_config(root)
    stamp_text = ""
    seq = _as_int(signal["seq"])
    for entry in reversed(read_entries(root)):
        if entry.thread == open_thread and entry.sender in config.parties:
            stamp_text, seq = entry.timestamp, entry.seq
            break
    stamp = _parse_stamp_utc(stamp_text)
    if stamp is None:
        stamp = _parse_stamp_utc(str(signal.get("updated_at", "")))  # conservative fallback
    if stamp is None:
        return (None, seq)  # both malformed: unknown, not fabricated
    return (max(0, int((now - stamp).total_seconds())), seq)


def _parse_stamp_utc(text: str) -> datetime | None:
    try:
        stamp = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp.replace(tzinfo=timezone.utc) if stamp.tzinfo is None else stamp
```

- [ ] **Step 4:** Helper tests PASS. **Step 5: Failing CLI tests** (`tests/test_cli_status.py`, new file):

```python
"""CLI status: parked/turnless/unknown lines, JSON age, --stale-after semantics."""
from __future__ import annotations

from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main


@pytest.fixture()
def parked_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "please review")
    return root


def _turnless_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-old", "x")
    channel.post(root, "alpha", "close", "t-old", "closing")
    channel.post(root, "owner", "verdict", "t-new", "supervisor opener")
    return root


def test_status_prints_parked_age_and_json_field(parked_channel: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status", "--root", str(parked_channel)]) == 0
    out = capsys.readouterr().out
    assert '"turn_age_seconds":' in out
    assert "turn 'alpha' parked 0h00m on 't-one' (seq 1)" in out


def test_stale_after_boundary(parked_channel: Path) -> None:
    assert main(["status", "--root", str(parked_channel), "--stale-after", "0"]) == 3   # age >= 0 always
    assert main(["status", "--root", str(parked_channel), "--stale-after", "3600"]) == 0


def test_stale_after_rejects_negative(parked_channel: Path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["status", "--root", str(parked_channel), "--stale-after", "-1"])
    assert excinfo.value.code == 2


def test_status_turnless_thread_supervisor_required(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _turnless_channel(tmp_path)
    assert main(["status", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "open with no turn" in out and "supervisor close required" in out
    assert '"turn_age_seconds"' not in out


def test_status_unknown_age_line_and_exit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the CLI's unknown-age contract: the line, the omitted JSON field, and exit 3."""
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "x")
    monkeypatch.setattr(channel, "turn_parked_since", lambda r, now: (None, 1))
    import debate.__main__ as cli
    monkeypatch.setattr(cli.channel, "turn_parked_since", lambda r, now: (None, 1), raising=False)
    assert main(["status", "--root", str(root), "--stale-after", "999999"]) == 3
    # and without --stale-after: exit 0, unknown-age line printed, no JSON age field
    assert main(["status", "--root", str(root)]) == 0


def test_stale_after_trips_on_turnless_thread_at_any_threshold(tmp_path: Path) -> None:
    root = _turnless_channel(tmp_path)
    assert main(["status", "--root", str(root), "--stale-after", "999999"]) == 3  # unconditionally stuck
```

- [ ] **Step 6:** Run — FAIL. **Step 7: Implement** in `__main__.py`: module-level argparse types:

```python
def _nonnegative_int(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {value}")
    return value


def _positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError(f"must be >= 1, got {value}")
    return value
```

status parser gains `p_status.add_argument("--stale-after", type=_nonnegative_int, default=None, metavar="SECONDS", help="exit 3 when the open thread is stuck at least this long (turnless or unknown-age threads always count as stuck)")`; status branch:

```python
        elif args.command == "status":
            signal = channel.read_signal(args.root)
            parked = channel.turn_parked_since(args.root, datetime.now(timezone.utc))
            shown = dict(signal)
            if parked is not None and parked[0] is not None:
                shown["turn_age_seconds"] = parked[0]
            print(json.dumps(shown, indent=2))
            thread = str(signal.get("thread", ""))
            stuck = False
            if thread:
                if parked is None:
                    print(f"thread '{thread}' open with no turn - supervisor close required")
                    stuck = True  # both parties are turn-refused; a non-close supervisor post preserves ""
                else:
                    age, assigning_seq = parked
                    if age is None:
                        print(f"turn '{signal.get('turn')}' parked (age unknown; malformed stamps) on '{thread}' (seq {assigning_seq})")
                        stuck = True  # unknown counts as stale - conservative
                    else:
                        hours, rem = divmod(age, 3600)
                        print(f"turn '{signal.get('turn')}' parked {hours}h{rem // 60:02d}m on '{thread}' (seq {assigning_seq})")
                        stuck = args.stale_after is not None and age >= args.stale_after
                for entry in channel.thread_entries(args.root, thread):
                    print(f"  MSG-{entry.seq} {entry.sender} {entry.entry_type}")
            if args.stale_after is not None and thread and stuck:
                return 3
```

(add `from datetime import datetime, timezone` to imports.)

- [ ] **Step 8:** All tests + suite PASS. **Step 9:** `cd "$W" && git add src/debate/channel.py src/debate/__main__.py tests/test_channel.py tests/test_cli_status.py && git commit -m "feat(status): truthful parked-turn age; turnless and unknown-age threads count as stuck"`

---

### Task 4: D3 — OS-level watcher lock (flock / msvcrt)

**Files:** Modify `src/debate/watcher.py`; test `tests/test_watcher.py`.

**Interfaces:** `tick_lock_path(state_path: Path) -> Path` (= `<state>.lock`); class `WatcherLock(path)` with `acquire() -> bool` (non-blocking; True = owned; writes pid+stamp diagnostics) and `release() -> None` (unlocks + closes; NEVER unlinks). `run_once` raises `ChannelError("refused: another watcher is driving <lock>")` when `acquire()` is False. Task 5's `watch` holds one `WatcherLock` for process lifetime and calls `_run_once_locked` directly.

- [ ] **Step 1: Failing tests** — real concurrency; bounded polling everywhere (Windows may delay unlock after process death):

```python
LOCK_HOLDER_CODE = """
import sys, time, pathlib
lock_path = pathlib.Path(sys.argv[1]); ready = pathlib.Path(sys.argv[2])
handle = open(lock_path, "a+")
if sys.platform == "win32":
    import msvcrt; handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
else:
    import fcntl; fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
ready.write_text("held")
time.sleep(30)
"""


def _hold_lock_in_child(lock: Path, ready: Path) -> subprocess.Popen[bytes]:
    lock.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, "-c", LOCK_HOLDER_CODE, str(lock), str(ready)])
    deadline = time.monotonic() + 10
    while not ready.exists():
        assert proc.poll() is None, "lock-holder child died"
        assert time.monotonic() < deadline, "lock-holder child never became ready"
        time.sleep(0.02)
    return proc


def _acquire_within(lock_path: Path, seconds: float) -> "WatcherLock":
    """Bounded polling: kernel unlock after process death may be delayed (esp. Windows)."""
    deadline = time.monotonic() + seconds
    lock = WatcherLock(lock_path)
    while True:
        if lock.acquire():
            return lock
        assert time.monotonic() < deadline, f"lock not released within {seconds}s"
        time.sleep(0.05)


def test_run_once_refused_while_live_process_holds_lock(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})
    child = _hold_lock_in_child(tick_lock_path(cfg.state_path), tmp_path / "ready")
    try:
        with pytest.raises(ChannelError, match="another watcher"):
            run_once(cfg)
    finally:
        child.kill()
        child.wait(timeout=10)


def test_lock_released_by_kernel_when_holder_dies(tmp_path: Path) -> None:
    """No staleness logic exists anywhere: the OS releases a crashed holder's lock."""
    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})
    child = _hold_lock_in_child(tick_lock_path(cfg.state_path), tmp_path / "ready")
    child.kill()
    child.wait(timeout=10)
    lock = _acquire_within(tick_lock_path(cfg.state_path), 10.0)  # bounded poll, not immediate
    lock.release()


def test_two_opens_in_one_process_conflict(tmp_path: Path) -> None:
    """flock binds to the open file description: in-process exclusion is real."""
    lock_path = tmp_path / "state.json.lock"
    first = WatcherLock(lock_path)
    assert first.acquire() is True
    second = WatcherLock(lock_path)
    assert second.acquire() is False
    first.release()
    third = WatcherLock(lock_path)
    assert third.acquire() is True
    third.release()


def test_state_tmp_files_are_pid_unique_and_cleaned(tmp_path: Path) -> None:
    from debate.watcher import _save_state

    target = tmp_path / "state.json"
    _save_state(target, {"x": 1})
    assert target.exists()
    assert list(tmp_path.glob("state.json.tmp*")) == []  # renamed away, pid-unique name
```

- [ ] **Step 2:** Run — FAIL: `WatcherLock`/`tick_lock_path` missing.
- [ ] **Step 3: Implement** in `watcher.py` (imports of `fcntl`/`msvcrt` INSIDE the methods — Windows CI must import the module cleanly):

```python
def tick_lock_path(state_path: Path) -> Path:
    return state_path.with_suffix(state_path.suffix + ".lock")


class WatcherLock:
    """OS-level advisory lock on ``<state>.lock`` - the kernel is the referee.

    ``fcntl.flock`` (POSIX) / ``msvcrt.locking`` (Windows) release when the
    holder exits or crashes, so there is NO staleness logic, NO pid probing,
    and NO takeover race by construction. The pid+stamp content is
    diagnostics only; the file is never unlinked (inert when unlocked).
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._handle: Any = None

    def acquire(self) -> bool:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(self._path, "a+", encoding="utf-8")
        try:
            if sys.platform == "win32":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            handle.close()
            return False
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        handle.seek(0)
        handle.truncate()
        handle.write(f"{os.getpid()}\n{stamp}\n")
        handle.flush()
        self._handle = handle
        return True

    def release(self) -> None:
        if self._handle is None:
            return
        try:
            if sys.platform == "win32":
                import msvcrt

                self._handle.seek(0)
                msvcrt.locking(self._handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        finally:
            self._handle.close()
            self._handle = None
```

`run_once`:

```python
def run_once(config: WatcherConfig) -> list[str]:
    lock = WatcherLock(tick_lock_path(config.state_path))
    if not lock.acquire():
        raise ChannelError(f"refused: another watcher is driving {tick_lock_path(config.state_path)}")
    try:
        return _run_once_locked(config)
    finally:
        lock.release()
```

(rename the current body to `_run_once_locked`; add `import os`, `import sys`, `from typing import Any` as needed.) `_save_state`:

```python
    tmp = path.with_name(f"{path.name}.tmp{os.getpid()}")
```

- [ ] **Step 4:** All tests + suite PASS.
- [ ] **Step 5:** `cd "$W" && git add src/debate/watcher.py tests/test_watcher.py && git commit -m "feat(watcher): kernel-refereed watcher lock (flock/msvcrt)"`

---

### Task 5: D3 — `debate watch` loop + STUCK handling

**Files:** Modify `src/debate/watcher.py` (`watch`, STUCK line), `src/debate/__main__.py`; test `tests/test_watcher.py`, `tests/test_cli_watch.py` (create).

**Interfaces:**
- Consumes: `WatcherLock`, `tick_lock_path`, `_run_once_locked` (Task 4); `decide()`'s reason suffix `"already escalated"` (Task 2).
- Produces: `_run_once_locked` emits `STUCK: seq <n> escalated; supervisor action required` when the decision reason ends with `"already escalated"` (Task 6 gates this behind the stable snapshot). `watch(config, *, interval_seconds, until_close, max_ticks, emit, sleep=time.sleep) -> int` — 0 closed, 4 on `ESCALATE:`/`STUCK:` lines, 5 max-ticks, 6 lock not acquired at startup; never returns 130 (CLI-only mapping of `KeyboardInterrupt`). CLI: `--interval`/`--max-ticks` via `_positive_int`; shared `_watcher_config(root, config_path)` helper adds `.expanduser()` on `state_path` (bug fix — the README example uses `~`).

- [ ] **Step 1: Failing loop tests:**

```python
def _fail_sleep(seconds: float) -> None:
    raise AssertionError("watch slept - expected exit before any sleep")


def _post_cmd(root: Path, sender: str, entry_type: str, thread: str, body: str) -> list[str]:
    """An 'agent' that speaks the protocol: posts one entry via the real library."""
    src = Path(__file__).resolve().parents[1] / "src"
    code = (
        "import sys; sys.path.insert(0, {src!r}); from pathlib import Path; "
        "from debate import channel; "
        "channel.post(Path({root!r}), {sender!r}, {entry_type!r}, {thread!r}, {body!r})"
    ).format(src=str(src), root=str(root), sender=sender, entry_type=entry_type, thread=thread, body=body)
    return [sys.executable, "-c", code]


def test_watch_until_close_exits_zero(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": _post_cmd(root, "alpha", "close", "t-one", "done, closing")},
                 prompts={"alpha": "go"})
    lines: list[str] = []
    code = watch(cfg, interval_seconds=1, until_close=True, max_ticks=5, emit=lines.append, sleep=_fail_sleep)
    assert code == 0
    assert any("thread closed after 1 tick" in line for line in lines)


def test_watch_new_escalation_exits_four(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 2, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": []}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=3,
                 emit=lambda s: None, sleep=_fail_sleep) == 4


def test_watch_exits_four_on_persisted_escalation_instead_of_spinning(tmp_path: Path) -> None:
    """A cron watch-once already recorded the escalation; a later watch --until-close
    (max_ticks=None!) must terminate loudly on tick one. _fail_sleep guarantees this
    test FAILS rather than hangs if the exit regresses."""
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 1, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": ["t-one:1"]}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    lines: list[str] = []
    assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=None,
                 emit=lines.append, sleep=_fail_sleep) == 4
    assert any(line.startswith("STUCK:") for line in lines)


def test_watch_max_ticks_exits_five(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})  # nobody invocable: ticks are no-ops
    sleeps: list[float] = []
    assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=2,
                 emit=lambda s: None, sleep=sleeps.append) == 5
    assert len(sleeps) == 1  # slept between tick 1 and 2, exited at the cap without a further sleep


def test_second_watch_exits_six_while_first_watch_sleeps(tmp_path: Path) -> None:
    """REAL process-lifetime exclusion: a first watch parked in its sleep still excludes
    both a second watch and a bare run_once."""
    import threading

    root = make_channel(tmp_path)
    cfg = config(root, commands={}, prompts={})
    sleeping = threading.Event()
    stop = threading.Event()

    def parked_sleep(seconds: float) -> None:
        sleeping.set()
        stop.wait(timeout=30)

    first_result: list[int] = []
    first = threading.Thread(
        target=lambda: first_result.append(
            watch(cfg, interval_seconds=1, until_close=False, max_ticks=2,
                  emit=lambda s: None, sleep=parked_sleep)
        )
    )
    first.start()
    assert sleeping.wait(timeout=10), "first watch never reached its sleep"
    try:
        lines: list[str] = []
        assert watch(cfg, interval_seconds=1, until_close=True, max_ticks=1,
                     emit=lines.append, sleep=_fail_sleep) == 6
        assert any("another watcher" in line for line in lines)
        with pytest.raises(ChannelError, match="another watcher"):
            run_once(cfg)
    finally:
        stop.set()
        first.join(timeout=30)
    assert first_result == [5]  # first watch finished its max_ticks run cleanly
```

- [ ] **Step 2:** Run — FAIL: no `watch`, no STUCK line.
- [ ] **Step 3: Implement.** STUCK line in `_run_once_locked` where the decision is neither invoke nor escalate:

```python
    elif decision.reason.endswith("already escalated"):
        output.append(f"STUCK: seq {seq} escalated; supervisor action required")
```

`watch` in `watcher.py` (add `from typing import Callable`):

```python
def watch(
    config: WatcherConfig,
    *,
    interval_seconds: int,
    until_close: bool,
    max_ticks: int | None,
    emit: Callable[[str], None],
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """Foreground run-to-completion loop: own the lock, tick, sleep, repeat.

    The lock is held for the PROCESS lifetime so a second watch - or a cron
    watch-once - is refused even while this one sleeps. Exit codes: 0 thread
    closed (with until_close), 4 escalated or stuck (supervisor must look),
    5 max-ticks, 6 another live watcher holds the lock. 130 is CLI-only.
    """
    from debate import channel  # local import keeps module load light

    lock = WatcherLock(tick_lock_path(config.state_path))
    if not lock.acquire():
        emit(f"another watcher is driving {tick_lock_path(config.state_path)} - exiting")
        return 6
    ticks = 0
    try:
        while True:
            lines = _run_once_locked(config)
            for line in lines:
                emit(line)
            if any(line.startswith(("ESCALATE:", "STUCK:")) for line in lines):
                return 4
            ticks += 1
            if until_close and not str(channel.read_signal(config.channel_root).get("thread", "")):
                emit(f"thread closed after {ticks} tick(s) - exiting")
                return 0
            if max_ticks is not None and ticks >= max_ticks:
                emit(f"max ticks ({max_ticks}) reached - exiting")
                return 5
            sleep(interval_seconds)
    finally:
        lock.release()
```

- [ ] **Step 4:** Loop tests + suite PASS. **Step 5: CLI wiring + failing CLI tests** (`tests/test_cli_watch.py`):

```python
"""CLI watch: arg validation, exit-code pass-through, KeyboardInterrupt mapping."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from debate import channel
from debate.__main__ import main


def _setup(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    cfg = tmp_path / "watcher.json"
    cfg.write_text(json.dumps({"state_path": str(tmp_path / "state.json")}), encoding="utf-8")
    return root, cfg


@pytest.mark.parametrize("flag", ["--interval", "--max-ticks"])
@pytest.mark.parametrize("value", ["0", "-1"])
def test_watch_rejects_nonpositive(tmp_path: Path, flag: str, value: str) -> None:
    root, cfg = _setup(tmp_path)
    with pytest.raises(SystemExit) as excinfo:
        main(["watch", "--root", str(root), "--config", str(cfg), flag, value])
    assert excinfo.value.code == 2


@pytest.mark.parametrize("code", [0, 4, 5, 6])
def test_watch_passes_exit_codes_through(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, code: int) -> None:
    import debate.__main__ as cli

    root, cfg = _setup(tmp_path)
    monkeypatch.setattr(cli, "watch", lambda *a, **k: code)
    assert main(["watch", "--root", str(root), "--config", str(cfg)]) == code


def test_watch_maps_keyboard_interrupt_to_130(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import debate.__main__ as cli

    root, cfg = _setup(tmp_path)

    def raising_watch(*args: object, **kwargs: object) -> int:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, "watch", raising_watch)
    assert main(["watch", "--root", str(root), "--config", str(cfg)]) == 130
```

`__main__.py`: extract the watcher-config construction into a helper used by BOTH `watch-once` and `watch`:

```python
def _watcher_config(root: Path, config_path: Path) -> WatcherConfig:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    return WatcherConfig(
        channel_root=root,
        state_path=Path(raw["state_path"]).expanduser(),
        commands={k: list(v) for k, v in raw.get("commands", {}).items()},
        prompts={k: str(v) for k, v in raw.get("prompts", {}).items()},
        debounce_seconds={k: int(v) for k, v in raw.get("debounce_seconds", {}).items()},
        retry_seconds=int(raw.get("retry_seconds", 1800)),
        timeout_seconds=int(raw.get("timeout_seconds", 1800)),
    )
```

subparser + branch (import `watch` at top via `from debate.watcher import WatcherConfig, run_once, watch`; call it as the module-level name `watch` so tests can monkeypatch `cli.watch`):

```python
    p_watchloop = sub.add_parser("watch", help="foreground watcher loop: drive the open thread to completion")
    p_watchloop.add_argument("--root", type=Path, default=Path("."))
    p_watchloop.add_argument("--config", type=Path, required=True, help="watcher config JSON (see README)")
    p_watchloop.add_argument("--interval", type=_positive_int, default=180, metavar="SECONDS")
    p_watchloop.add_argument("--until-close", action="store_true", help="exit 0 when no thread is open")
    p_watchloop.add_argument("--max-ticks", type=_positive_int, default=None)
```

```python
        elif args.command == "watch":
            try:
                return watch(
                    _watcher_config(args.root, args.config),
                    interval_seconds=args.interval,
                    until_close=args.until_close,
                    max_ticks=args.max_ticks,
                    emit=print,
                )
            except KeyboardInterrupt:
                return 130
```

- [ ] **Step 6:** All tests + suite + `PYTHONPATH=src python3 -m debate watch --help` smoke.
- [ ] **Step 7:** `cd "$W" && git add src/debate/watcher.py src/debate/__main__.py tests/test_watcher.py tests/test_cli_watch.py && git commit -m "feat: debate watch - run-to-completion loop; STUCK escalations terminate instead of spinning"`

---

### Task 6: D6 — stable decision snapshot under the channel writer lock

**Files:** Modify `src/debate/channel.py` (rename `_exclusive` → public `exclusive`, keep behavior), `src/debate/watcher.py` (`_run_once_locked` restructure); test `tests/test_watcher.py`.

**Interfaces:** `channel.exclusive(root)` — the existing writer-lock context manager, made public (update its two internal call sites; docstring: "hold the channel writer lock"). `_run_once_locked` takes its snapshot + decision + state-record under `channel.exclusive(channel_root)`; the child launch stays OUTSIDE it. Deferral line: `mailbox ahead of signal (entries at <m>, signal at <n>); deferring to next tick`. Lock ordering invariant (comment in code): watcher lock is acquired before the writer lock, never the reverse.

- [ ] **Step 1: Failing tests** — the frozen mid-post state, all three interleavings:

```python
def _freeze_mid_post(root: Path, sender: str, entry_type: str, thread: str, body: str) -> None:
    """Reproduce a writer paused between mailbox append and signal replace:
    perform a real post, then restore the pre-post signal bytes."""
    from debate import channel as channel_mod

    before = (root / "signal.json").read_bytes()
    channel_mod.post(root, sender, entry_type, thread, body)
    (root / "signal.json").write_bytes(before)


def test_mid_post_state_defers_invocation(tmp_path: Path) -> None:
    root = make_channel(tmp_path)  # signal seq 1, turn=alpha
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    _freeze_mid_post(root, "alpha", "verdict", "t-one", "reply in flight")  # mailbox 2, signal 1
    lines = run_once(cfg)
    assert any("mailbox ahead of signal" in line for line in lines)
    assert not any(line.startswith("invoked ") for line in lines)
    state = json.loads(cfg.state_path.read_text(encoding="utf-8"))
    assert state.get("invocations", {}) == {}


def test_mid_post_state_defers_new_escalation(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 2, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": []}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    _freeze_mid_post(root, "alpha", "verdict", "t-one", "reply in flight")
    lines = run_once(cfg)  # would have escalated seq 1 - but the world moved
    assert any("mailbox ahead of signal" in line for line in lines)
    assert not any(line.startswith("ESCALATE:") for line in lines)
    assert json.loads(cfg.state_path.read_text(encoding="utf-8"))["escalated"] == []


def test_mid_post_state_suppresses_persisted_stuck_line(tmp_path: Path) -> None:
    """The persisted-escalation STUCK line derives from the same snapshot: with the
    mailbox ahead, the escalated seq is about to be superseded - emitting STUCK
    (and exiting watch with 4) would be false."""
    root = make_channel(tmp_path)
    cfg = config(root, commands={"alpha": [sys.executable, "-c", "pass"]}, prompts={"alpha": "go"})
    state = {"last_mirrored_seq": 1,
             "invocations": {"1": {"count": 1, "last_at": "2020-01-01T00:00:00+00:00"}},
             "escalated": ["t-one:1"]}
    cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_path.write_text(json.dumps(state), encoding="utf-8")
    _freeze_mid_post(root, "alpha", "verdict", "t-one", "reply in flight")
    lines = run_once(cfg)
    assert any("mailbox ahead of signal" in line for line in lines)
    assert not any(line.startswith("STUCK:") for line in lines)
```

- [ ] **Step 2:** Run — FAIL on all three.
- [ ] **Step 3: Implement.** (a) In `channel.py`: rename `_exclusive` to `exclusive` (public; docstring "Hold the channel's writer lock...") and update its two call sites (`post`, `compact`). (b) Restructure `_run_once_locked` so the snapshot, decision, and state RECORDING happen under the writer lock, and the child launch happens outside it — final shape:

```python
def _run_once_locked(config: WatcherConfig) -> list[str]:
    from debate import channel  # local import keeps module load light

    output: list[str] = []
    state = _load_state(config.state_path)

    # Snapshot + decide + record under the CHANNEL WRITER LOCK: a mid-post
    # writer cannot hold it, so signal and mailbox are consistent here by
    # construction. Lock order: watcher lock (held by our caller) BEFORE the
    # writer lock - never the reverse, so no cycle. The child launch happens
    # AFTER release: an agent posting its reply via the CLI must not deadlock
    # against its own watcher.
    with channel.exclusive(config.channel_root):
        signal = channel.read_signal(config.channel_root)
        entries = channel.read_entries(config.channel_root)
        seq = int(str(signal.get("seq", 0)))
        mailbox_seq = max((entry.seq for entry in entries), default=0)

        last_mirrored = int(state.get("last_mirrored_seq", 0))
        output.extend(new_entry_lines(entries, last_mirrored))
        state["last_mirrored_seq"] = max([last_mirrored, *[e.seq for e in entries]])

        if mailbox_seq > seq:
            # A non-CLI writer violated append-then-signal mid-flight; the
            # consistent-snapshot invariant failed - act on nothing this tick.
            output.append(
                f"mailbox ahead of signal (entries at {mailbox_seq}, signal at {seq}); deferring to next tick"
            )
            _save_state(config.state_path, state)
            return output

        decision = decide(signal, state, config, datetime.now(timezone.utc))
        if decision.escalate:
            output.append(f"ESCALATE: {decision.escalate}")
            state = record_escalation(state, str(signal.get("thread", "")), seq)
        elif decision.invoke:
            state = record_invocation(state, seq, datetime.now(timezone.utc))
        elif decision.reason.endswith("already escalated"):
            output.append(f"STUCK: seq {seq} escalated; supervisor action required")
        _save_state(config.state_path, state)  # recorded before the expensive child

    if decision.invoke:
        argv = config.command_for(decision.invoke)
        assert argv is not None  # decide() only returns invocable parties
        try:
            proc = subprocess.run(
                argv,
                cwd=config.channel_root,
                text=True,
                stdin=subprocess.DEVNULL,  # an inherited tty/pipe stdin hung a real agent for 3h
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=config.timeout_seconds,
                creationflags=CREATE_NO_WINDOW,
            )
        except subprocess.TimeoutExpired:
            output.append(
                f"invoked {decision.invoke} for seq {seq}: TIMEOUT after {config.timeout_seconds}s (killed)"
            )
        except (OSError, ValueError) as error:
            output.append(f"invoke failed for {decision.invoke}: {error}")
            output.append(
                f"ESCALATE: cannot launch agent for {decision.invoke!r} "
                f"on thread {signal.get('thread')!r} - fix the watcher config"
            )
            state = record_escalation(state, str(signal.get("thread", "")), seq)
        else:
            status = "ok" if proc.returncode == 0 else f"exit {proc.returncode}"
            output.append(f"invoked {decision.invoke} for seq {seq}: {status}")
        refreshed = channel.read_entries(config.channel_root)
        output.extend(new_entry_lines(refreshed, int(state.get("last_mirrored_seq", 0))))
        state["last_mirrored_seq"] = max(
            [int(state.get("last_mirrored_seq", 0)), *[e.seq for e in refreshed]]
        )

    _save_state(config.state_path, state)
    return output
```

(A post that lands after the writer lock is released makes an in-flight INVOCATION stale — that
residue is backstopped by turn enforcement refusing the stale agent's post. Escalations and STUCK
have no post to be refused, which is exactly why they are decided only under the lock.)

- [ ] **Step 4:** All three new tests + every earlier watcher test PASS (Tasks 1-5 tests exercise the restructured body).
- [ ] **Step 5:** `cd "$W" && git add src/debate/channel.py src/debate/watcher.py tests/test_watcher.py && git commit -m "fix(watcher): decide on a writer-locked snapshot - invoke, escalation, and STUCK can never act on a mid-post state"`

---

### Task 7: D4 — opener allowlist

**Files:** Modify `src/debate/channel.py` (constant + check in `post`), `PROTOCOL.md`, `README.md`; test `tests/test_channel.py`.

**Interfaces:** `OPENER_TYPES: tuple[str, ...] = ("review-request", "question", "info", "close")`; refusal message `refused: '<type>' cannot open a thread - only review-request/question/info (or a one-shot close correction) may start one`.

- [ ] **Step 1: Failing tests:**

```python
def make_closed_channel(tmp_path: Path) -> Path:
    root = tmp_path / "chan"
    channel.init_channel(root, ("alpha", "beta"), "owner")
    channel.post(root, "beta", "review-request", "t-one", "review please")
    channel.post(root, "alpha", "verdict", "t-one", "APPROVE")
    channel.post(root, "beta", "close", "t-one", "merged, closing")
    return root


@pytest.mark.parametrize("entry_type", ["verdict", "fix-report"])
def test_verdict_and_fix_report_cannot_open_a_thread(tmp_path: Path, entry_type: str) -> None:
    """A stray verdict once reopened a CLOSED thread (baseline test, 2026-07-15)."""
    root = make_closed_channel(tmp_path)
    with pytest.raises(ChannelError, match="cannot open a thread"):
        channel.post(root, "alpha", entry_type, "t-one", "stray reply")


@pytest.mark.parametrize("entry_type", ["review-request", "question", "info", "close"])
def test_opener_types_may_open_a_thread(tmp_path: Path, entry_type: str) -> None:
    """close stays an opener: the one-shot close-correction idiom is shipped contract
    (PROTOCOL.md:51, tests/test_channel.py:102, docs/case-study.md:81)."""
    root = make_closed_channel(tmp_path)
    channel.post(root, "alpha", entry_type, "t-two", "legitimate opener")


def test_supervisor_verdict_with_nothing_open_creates_turnless_open_thread(tmp_path: Path) -> None:
    root = make_closed_channel(tmp_path)
    channel.post(root, "owner", "verdict", "t-one", "supervisor correction on the record")
    signal = channel.read_signal(root)
    assert signal["thread"] == "t-one"   # supervisor posts are exempt and open the slug
    assert signal["turn"] == ""          # with no turn assigned - the supervisor-only state of D2
```

- [ ] **Step 2:** Run — FAIL: the first parametrized test posts successfully.
- [ ] **Step 3: Implement** — next to `ENTRY_TYPES` in `channel.py`:

```python
# Types that may START a discussion. verdict/fix-report are replies by nature;
# close stays an opener for the documented one-shot close-correction idiom.
OPENER_TYPES: tuple[str, ...] = ("review-request", "question", "info", "close")
```

inside `post`, immediately after `open_thread = str(signal.get("thread", ""))`:

```python
        if sender != config.supervisor and not open_thread and entry_type not in OPENER_TYPES:
            raise ChannelError(
                f"refused: {entry_type!r} cannot open a thread - only review-request/question/info "
                "(or a one-shot close correction) may start one"
            )
```

- [ ] **Step 4:** New tests + suite PASS — the existing close-correction test (tests/test_channel.py:102) MUST stay green untouched; if it breaks, the implementation is wrong, not the test.
- [ ] **Step 5:** PROTOCOL.md enforced-rules list gains: `A thread is opened by review-request, question, info - or a one-shot close correction. verdict and fix-report are replies: with no thread open they are refused (supervisor exempt).` README "What's enforced - and what isn't": add "reply types (verdict, fix-report) cannot open threads" to the enforced bullet.
- [ ] **Step 6:** `cd "$W" && git add src/debate/channel.py tests/test_channel.py PROTOCOL.md README.md && git commit -m "feat(protocol)!: opener allowlist - verdict/fix-report cannot open threads; close-correction preserved"`

---

### Task 8: D5 — docs, four-way version lockstep, release tag gate, full gate

**Files:** Modify `README.md`, `pyproject.toml`, `src/debate/__init__.py`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.github/workflows/release.yml`; test `tests/test_release_sync.py` (create).

- [ ] **Step 1: The lockstep test** (`tests/test_release_sync.py`):

```python
"""Version lockstep: pyproject, package, and both plugin manifests must agree."""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_all_four_version_locations_agree() -> None:
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE)
    assert match is not None
    version = match.group(1)

    import debate

    assert debate.__version__ == version
    plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["version"] == version
    marketplace = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["metadata"]["version"] == version
```

- [ ] **Step 2:** Bump `pyproject.toml` to `0.3.0` FIRST; run the test — expected FAIL (`debate.__version__` is 0.2.0). That failure is the point.
- [ ] **Step 3:** Bump `src/debate/__init__.py` (`__version__ = "0.3.0"`), `.claude-plugin/plugin.json` (`"version": "0.3.0"`), `.claude-plugin/marketplace.json` (`metadata.version` → `"0.3.0"`). Test PASSES.
- [ ] **Step 4:** Release tag gate — in `.github/workflows/release.yml`, a step BEFORE build/publish (adapt placement to the file read in Task 0):

```yaml
      - name: Verify tag matches package version
        run: |
          TAG="${GITHUB_REF_NAME#v}"
          python - "$TAG" <<'EOF'
          import re, sys
          tag = sys.argv[1]
          pyproject = open("pyproject.toml", encoding="utf-8").read()
          version = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE).group(1)
          sys.path.insert(0, "src")
          import debate
          assert tag == version == debate.__version__, (
              f"tag {tag!r} != pyproject {version!r} != package {debate.__version__!r}"
          )
          EOF
```

- [ ] **Step 5:** README — new subsection after the watch-once config example, before "Housekeeping":

```markdown
### Running to completion

Cron is for unattended operation. At the keyboard and just want the current review driven
to its close? Run the same watcher in the foreground:

```bash
debate watch --root ./collab --config watcher.json --until-close
```

Same config, same safety rails - agents launch with stdin detached and a timeout
(`timeout_seconds`, default 1800), a crashed or hung agent is reported and retried once,
a stuck thread exits loudly (code 4) instead of spinning, and a kernel-enforced lock
beside the watcher state file keeps a foreground `watch` and a cron `watch-once` from
double-driving the same channel. `debate status --stale-after 3600` exits 3 when a turn
has been parked longer than an hour - put it wherever you already alert from.
```

- [ ] **Step 6:** Full gate: `cd "$W" && PYTHONPATH=src python3 -m pytest tests/ -q --basetemp=.pytest-tmp` + the exact ci.yml ruff/mypy commands — all green.
- [ ] **Step 7:** `cd "$W" && git add README.md pyproject.toml src/debate/__init__.py .claude-plugin/plugin.json .claude-plugin/marketplace.json .github/workflows/release.yml tests/test_release_sync.py && git commit -m "docs+release: running-to-completion docs, four-way v0.3.0 lockstep, tag==version release gate"`

---

### Task 9: Dogfood review round on collab/

- [ ] **Step 1:** Clean-tree gate — the cited SHA must equal the reviewed files:

```bash
W=~/Projects/debate-reliability-v0.3
test -z "$(git -C "$W" status --porcelain)" || { echo "worktree dirty - commit or drop before review"; exit 1; }
SHA=$(git -C "$W" rev-parse --short HEAD); echo "$SHA"
```

- [ ] **Step 2:** Post the review request (each Task 9 block re-asserts its own environment — no
  inherited shell state; channel root is ABSOLUTE, the channel lives in the main checkout):

```bash
set -e
W=~/Projects/debate-reliability-v0.3
test "$(git -C "$W" rev-parse --abbrev-ref HEAD)" = "reliability-v0.3" || { echo "wrong branch"; exit 1; }
test -z "$(git -C "$W" status --porcelain)" || { echo "worktree dirty"; exit 1; }
SHA=$(git -C "$W" rev-parse --short HEAD)
test -n "$SHA" || { echo "no SHA"; exit 1; }
cd "$W" && PYTHONPATH=src python3 -m debate post \
  --root ~/Projects/debate/collab --from claude --type review-request \
  --thread reliability-v0-3 --refs "reliability-v0.3@$SHA" --verify-refs "$W" \
  --body "Please review branch reliability-v0.3 at $SHA (worktree ~/Projects/debate-reliability-v0.3, clean tree - the SHA is the full reviewed state). Spec: docs/plans/2026-07-15-reliability-hardening.md r4 incl. your three appended review rounds; plan r4. Verify each MSG-9/11/13 finding is resolved IN CODE: kernel flock/msvcrt lock (zero pid probing), writer-locked decision snapshot covering invoke/new-escalation/persisted-STUCK with the frozen mid-post tests, turn-age signature+fallback+turnless semantics with stale-after stuck rules, raising-sleep spin regression, CLI pass-through 0/4/5/6/130, four-way lockstep test, release tag gate. Run the suite yourself: PYTHONPATH=src python3 -m pytest tests/ -q --basetemp=.pytest-tmp. Cite commit + test counts."
```

- [ ] **Step 3:** Invoke the reviewer (stdin detached, background, generous ceiling), cwd `$W`, channel root absolute:

```bash
set -e
W=~/Projects/debate-reliability-v0.3
SHA=$(git -C "$W" rev-parse --short HEAD); test -n "$SHA"
cd "$W" && codex exec --sandbox workspace-write "It is your turn on the debate review channel at ~/Projects/debate/collab (party 'codex'). CLI: PYTHONPATH=src python3 -m debate ... Read the open thread (debate read --root ~/Projects/debate/collab), review the branch in THIS directory per the request, run the test suite yourself, then post your verdict (--from codex, same --root, --refs reliability-v0.3@$SHA --verify-refs .) citing fresh evidence. No merges, no pushes." </dev/null
```

- [ ] **Step 4:** On APPROVE: close the thread; merge is the owner's call. On REQUEST CHANGES: fix-report cycle per protocol (mind the thread cap).
