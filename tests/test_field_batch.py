"""Regression tests for the owner's field-test batch (2026-08-20).

Three engine fixes from live product testing: the interactive scheduler
default, the in-flight (not stale) brokered status, and the
post-open bookkeeping crash that orphaned a channel.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from debate import opening, seats
from debate.__main__ import _watcher_config, main
from debate.controller import AdapterProfile, BrokerConfig, TimingPolicy
from debate.watcher import LockState, WatcherConfig, status

NOW = datetime(2026, 8, 20, 12, 0, 0, tzinfo=timezone.utc)


def _profile(party: str) -> AdapterProfile:
    return AdapterProfile(
        party=party,
        command=(sys.executable, "bridge.py", "{input_path}", "{result_path}"),
        provider=f"vendor-{party}",
        requested_model=f"{party}-model",
        author_relationship="author-independent",
        reasoning_effort="high",
        cli_version="fixture-1",
        cost_mode="local",
        authentication_mode="local-process",
        permission_policy="read-only-source; result-file-only",
        settings_sources=(),
        environment_allowlist=("PATH",),
        timeout_seconds=1200,
        retry_limit=1,
    )


def _brokered_config(tmp_path: Path) -> WatcherConfig:
    profiles = {"alpha": _profile("alpha"), "beta": _profile("beta")}
    timing = TimingPolicy(
        thread_cap=12,
        scheduler_interval_seconds=5,
        retry_seconds=30,
        whole_case_timeout_seconds=3600,
        profiles=(profiles["alpha"], profiles["beta"]),
    )
    broker = BrokerConfig(
        repository_root=tmp_path,
        runtime_root=tmp_path / "var" / "debate" / "case-1",
        source_ref="0" * 40,
        profiles=profiles,
        timing=timing,
        config_sha256="0" * 64,
        docket_files=(),
        contamination_canaries={},
    )
    return WatcherConfig(
        channel_root=tmp_path / "collab",
        state_path=tmp_path / "var" / "debate" / "case-1" / "state.json",
        commands={},
        prompts={},
        debounce_seconds={},
        retry_seconds=30,
        channel_name="case-channel-1",
        managed_version=2,
        parties=("alpha", "beta"),
        broker=broker,
    )


def _signal(updated_at: str) -> dict[str, Any]:
    return {
        "seq": 3,
        "turn": "alpha",
        "thread": "case-1",
        "updated_at": updated_at,
        "deadline": "2026-08-20T13:00:00+00:00",
    }


def test_brokered_in_flight_seat_is_driving_not_stale(tmp_path: Path) -> None:
    """Field finding: watch-status cried STALE while a seat legitimately
    thought for minutes under the held tick lock (uninvoked arm)."""
    config = _brokered_config(tmp_path)
    held = LockState(
        held=True, pid=4242, stamp="2026-08-20T11:57:00+00:00", cwd="/x", channel="/y"
    )
    verdict = status(_signal("2026-08-20T11:56:00+00:00"), {}, config, NOW, held)
    assert verdict.verdict == "DRIVING"
    assert "in flight" in verdict.detail
    assert "1200s" in verdict.detail


def test_brokered_in_flight_covers_the_invoked_past_retry_arm(tmp_path: Path) -> None:
    """Round-10/11 gate findings (MSG-45 F1, MSG-51 F1): a LIVE invocation
    reaches the invoked-past-retry arm, and in-flight-ness is measured from
    the INVOCATION stamp -- never the lock stamp, which a long-lived
    foreground watcher holds for its whole uptime."""
    config = _brokered_config(tmp_path)
    # The discriminating case: the watcher has held the lock for HOURS
    # (uptime), but the invocation is 150s old -- must be DRIVING.
    long_lived = LockState(
        held=True, pid=4242, stamp="2026-08-20T08:00:00+00:00", cwd="/x", channel="/y"
    )
    state = {"invocations": {"3": {"count": 1, "last_at": "2026-08-20T11:57:30+00:00"}}}
    verdict = status(_signal("2026-08-20T11:56:00+00:00"), state, config, NOW, long_lived)
    assert verdict.verdict == "DRIVING"
    assert "in flight" in verdict.detail
    # The mirror case: lock freshly acquired, but the invocation is OLDER
    # than the seat budget -- a dead adapter must read STALE, not be masked.
    fresh_lock = LockState(
        held=True, pid=4242, stamp="2026-08-20T11:59:50+00:00", cwd="/x", channel="/y"
    )
    dead = {"invocations": {"3": {"count": 1, "last_at": "2026-08-20T11:30:00+00:00"}}}
    masked = status(_signal("2026-08-20T11:20:00+00:00"), dead, config, NOW, fresh_lock)
    assert masked.verdict == "STALE"
    # Same live state with a FREE lock: genuinely stale.
    free = LockState(held=False, pid=None, stamp="", cwd=None)
    stale = status(_signal("2026-08-20T11:56:00+00:00"), state, config, NOW, free)
    assert stale.verdict == "STALE"


def test_cli_watch_passes_the_resolved_interval(tmp_path: Path, monkeypatch: "pytest.MonkeyPatch") -> None:
    """Round-11 finding 2 (non-blocking): pin that main() hands watch() the
    RESOLVED interval, so a revert to args.interval fails this test."""
    import debate.__main__ as cli

    captured: dict[str, object] = {}

    def fake_watch(config: object, **kwargs: object) -> int:
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(cli, "watch", fake_watch)

    def fake_config(*args: object, **kwargs: object) -> object:
        class _Cfg:
            class broker:
                class timing:
                    scheduler_interval_seconds = 5
        return _Cfg()

    monkeypatch.setattr(cli, "_watcher_config", fake_config)
    from debate import channel as channel_module

    monkeypatch.setattr(channel_module, "discover_channel", lambda *a, **k: "chan-1")
    rc = cli.main(["watch", "--root", str(tmp_path), "--config", str(tmp_path / "w.json"), "--max-ticks", "1"])
    assert rc == 0
    assert captured["interval_seconds"] == 5


def test_brokered_lock_past_seat_budget_is_stale(tmp_path: Path) -> None:
    config = _brokered_config(tmp_path)
    ancient = LockState(
        held=True, pid=4242, stamp="2026-08-20T11:35:00+00:00", cwd="/x", channel="/y"
    )
    verdict = status(_signal("2026-08-20T11:30:00+00:00"), {}, config, NOW, ancient)
    assert verdict.verdict == "STALE"


def test_brokered_free_lock_past_grace_is_stale(tmp_path: Path) -> None:
    config = _brokered_config(tmp_path)
    free = LockState(held=False, pid=None, stamp="", cwd=None)
    verdict = status(_signal("2026-08-20T11:56:00+00:00"), {}, config, NOW, free)
    assert verdict.verdict == "STALE"


# --- interactive scheduler default + orphan guard --------------------------


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    registry = tmp_path / "config" / "seats.json"
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("DEBATE_SEATS_REGISTRY", str(registry))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    return registry, project


def _prepare_project(registry: Path, project: Path, tmp_path: Path) -> None:
    from test_onboarding_flow import (  # reuse the proven fixtures
        _approve_all,
        _brokered_registry,
        _git_project,
    )

    _brokered_registry(registry, tmp_path)
    _git_project(project)
    _approve_all(project)


def test_interactive_open_defaults_to_a_snappy_tick(
    isolated: tuple[Path, Path], tmp_path: Path
) -> None:
    """Field finding: the 60s cron tick made a six-message debate idle for
    minutes; the interactive product default is seconds."""
    import subprocess

    registry, project = isolated
    _prepare_project(registry, project, tmp_path)
    head = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    result = opening.open_debate_brokered(
        opening.BrokeredOpenSpec(
            root=project / "collab", label="stub", pair=("alpha/fake", "beta/fake"),
            source_ref=head, author_vendor="claude",
        ),
        seats.load_registry(), load_config_fn=_watcher_config,
        now="2026-08-20T12:00:00+00:00", tool_version="test",
    )
    config = json.loads(result.config_path.read_text(encoding="utf-8"))
    assert config["scheduler_interval_seconds"] == 5
    # Round-10 gate finding (MSG-45 F2): the JSON value alone drives nothing.
    # The watch loop's cadence must DEFAULT from it: this is the behavior the
    # field finding was about.
    from debate.__main__ import _watch_interval, _watcher_config as load_config

    loaded = load_config(project / "collab", result.config_path, result.channel_name)
    assert _watch_interval(None, loaded) == 5      # config-driven default
    assert _watch_interval(42, loaded) == 42       # explicit flag wins


def test_open_survives_post_creation_bookkeeping_failure(
    isolated: tuple[Path, Path], tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """Field finding: a sandboxed registry write crashed the CLI AFTER a
    successful open, stranding an orphaned channel on retry. The channel is
    usable; last_pair is a convenience -- warn, never crash."""
    registry, project = isolated
    _prepare_project(registry, project, tmp_path)

    def refuse(_registry: seats.Registry) -> Path:
        raise OSError(30, "Read-only file system")

    monkeypatch.setattr(seats, "save_registry", refuse)
    rc = main([
        "open", "--brokered", "--root", str(project / "collab"),
        "--label", "stub", "--pair", "alpha/fake,beta/fake",
        "--author-vendor", "claude",
    ])
    captured = capsys.readouterr()
    assert rc == 0
    assert "bookkeeping failed" in captured.out
    channels = list((project / "collab").glob("*.debate.json"))
    assert len(channels) == 1  # created once, usable, no crash


# --- final wave follow-up: what a fully managed channel says about itself ----


def test_a_fully_managed_channel_reports_itself_in_plain_words(tmp_path: Path) -> None:
    """`debate watch-status` prints exactly what `read_status` returns, and its
    verdict comes from `status`; a tick's own reasons come from `decide`. None
    of them may speak the engine's private words. The forbidden list is
    IMPORTED from the plain-words law so the two can never drift.
    """
    from debate.watcher import decide, read_status
    from test_plain_words import FORBIDDEN, _is_literal_token

    config = _brokered_config(tmp_path)
    config.channel_root.mkdir(parents=True, exist_ok=True)
    signal_path = config.channel_root / f"{config.channel_name}.signal.json"

    free = LockState(held=False, pid=None, stamp="", cwd=None)
    held = LockState(
        held=True, pid=4242, stamp="2026-08-20T11:57:00+00:00", cwd="/x", channel="/y"
    )
    no_deadline = {key: value for key, value in _signal("2026-08-20T11:59:00+00:00").items()
                   if key != "deadline"}
    expired = {**_signal("2026-08-20T11:00:00+00:00"), "deadline": "2026-08-20T11:30:00+00:00"}
    in_flight = _signal("2026-08-20T11:56:00+00:00")

    spoken: list[str] = []
    verdicts: list[str] = []
    for signal, lock in ((no_deadline, free), (expired, free), (in_flight, held)):
        verdict = status(signal, {}, config, NOW, lock)
        verdicts.append(verdict.verdict)
        spoken.append(f"{verdict.verdict}: {verdict.detail}")
        decision = decide(signal, {}, config, NOW)
        spoken.extend(
            str(part) for part in (decision.invoke, decision.escalate, decision.reason) if part
        )
        # And the same states through the command's own reader.
        signal_path.write_text(json.dumps(signal), encoding="utf-8")
        lines, reported = read_status(config, NOW)
        spoken.extend(lines)
        spoken.append(f"{reported.verdict}: {reported.detail}")

    # Proof the three branches this covers were actually reached.
    assert verdicts == ["INVALID", "STALE", "DRIVING"], verdicts

    offences = [
        f"{word!r} in {text!r}"
        for text in spoken
        for word, pattern in FORBIDDEN
        for match in pattern.finditer(text)
        if not _is_literal_token(text, match.start(), match.end())
    ]
    assert not offences, "\n".join(offences)
