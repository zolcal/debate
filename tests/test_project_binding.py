"""The channel refuses work that is not its project (v0.4 Slice 3).

``debate.json`` gains ``"project": "<abs path>"``, recorded at init (and at
migrate — a migrated channel must not be forever unbindable). ``post``
refuses a ``--refs`` citation whose ``@sha`` does not resolve in the
channel's project repo, naming both sides. This is the rule that would have
stopped the MSG-180 cross-post (a debate-bench review conducted through this
repo's channel) at the moment it happened. ``--force`` stays supervisor-only.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from debate import channel
from debate.channel import ChannelError


def _git_repo_with_commit(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "--quiet", str(path)], check=True, capture_output=True)
    # Repo-unique content: two repos with identical files, message, author
    # and commit second would produce the SAME sha, making "foreign" a lie.
    (path / "f.txt").write_text(str(path), encoding="utf-8")
    env = {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
        "PATH": "/usr/bin:/bin",
    }
    subprocess.run(["git", "-C", str(path), "add", "f.txt"], check=True, capture_output=True, env=env)
    subprocess.run(
        ["git", "-C", str(path), "commit", "-q", "-m", "c"], check=True, capture_output=True, env=env
    )
    sha = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return sha


def test_init_records_the_project_it_serves(tmp_path: Path) -> None:
    repo = tmp_path / "proj"
    _git_repo_with_commit(repo)
    root = repo / "collab"

    channel.init_channel(root, ("alice", "bob"), "owner", name="alpha-11111")

    raw = json.loads((root / "alpha-11111.debate.json").read_text(encoding="utf-8"))
    assert raw["project"] == str(repo.resolve())
    assert channel.load_config(root, name="alpha-11111").project == str(repo.resolve())


def test_legacy_init_still_records_no_project(tmp_path: Path) -> None:
    """The legacy library path stays byte-identical to 0.3.1."""
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")

    raw = json.loads((tmp_path / "debate.json").read_text(encoding="utf-8"))
    assert "project" not in raw


def test_migrate_records_the_project(tmp_path: Path) -> None:
    repo = tmp_path / "proj"
    _git_repo_with_commit(repo)
    root = repo / "collab"
    channel.init_channel(root, ("alice", "bob"), "owner")

    cid = channel.migrate_channel(root, label="alpha")

    assert channel.load_config(root, name=cid).project == str(repo.resolve())


def test_post_refuses_a_citation_from_a_foreign_repo(tmp_path: Path) -> None:
    ours = tmp_path / "ours"
    _git_repo_with_commit(ours)
    foreign_sha = _git_repo_with_commit(tmp_path / "theirs")
    root = ours / "collab"
    channel.init_channel(root, ("alice", "bob"), "owner", name="alpha-11111")

    with pytest.raises(ChannelError) as excinfo:
        channel.post(
            root,
            "alice",
            "review-request",
            "t-one",
            "review this",
            refs=f"main@{foreign_sha}",
            name="alpha-11111",
        )

    # Substring assertions rather than `pytest.raises(match=...)`, because the
    # message embeds a filesystem path and a path is not a safe regex. This was
    # written as match=... + str(path).replace("/", "."), which only sanitises
    # POSIX separators: on Windows the path arrives with backslashes, `\o` in
    # `...\ours` is an invalid escape, and every Windows CI job failed with
    # "bad escape \o" while Linux stayed green. The contract is that the refusal
    # names both sides - the offending sha and the project it does not belong to.
    message = str(excinfo.value)
    assert foreign_sha in message, message
    assert str(ours.resolve()) in message, message

    assert channel.read_entries(root, name="alpha-11111") == []  # nothing was written


def test_post_accepts_a_citation_from_its_own_project(tmp_path: Path) -> None:
    repo = tmp_path / "proj"
    sha = _git_repo_with_commit(repo)
    root = repo / "collab"
    channel.init_channel(root, ("alice", "bob"), "owner", name="alpha-11111")

    entry_id = channel.post(
        root, "alice", "review-request", "t-one", "review this", refs=f"main@{sha}", name="alpha-11111"
    )

    assert entry_id == "MSG-1"


def test_post_without_sha_citations_is_not_gated(tmp_path: Path) -> None:
    repo = tmp_path / "proj"
    _git_repo_with_commit(repo)
    root = repo / "collab"
    channel.init_channel(root, ("alice", "bob"), "owner", name="alpha-11111")

    entry_id = channel.post(
        root,
        "alice",
        "review-request",
        "t-one",
        "review the plan doc",
        refs="docs/plans/2026-08-04-per-instance-channel-naming.md",
        name="alpha-11111",
    )

    assert entry_id == "MSG-1"


def test_unbound_channel_accepts_foreign_citations(tmp_path: Path) -> None:
    """No project recorded (every pre-0.4 channel) -> no gate. Compat, not policy."""
    foreign_sha = _git_repo_with_commit(tmp_path / "theirs")
    channel.init_channel(tmp_path, ("alice", "bob"), "owner")

    entry_id = channel.post(tmp_path, "alice", "review-request", "t-one", "x", refs=f"main@{foreign_sha}")

    assert entry_id == "MSG-1"


def test_supervisor_force_bypasses_the_project_gate(tmp_path: Path) -> None:
    ours = tmp_path / "ours"
    _git_repo_with_commit(ours)
    foreign_sha = _git_repo_with_commit(tmp_path / "theirs")
    root = ours / "collab"
    channel.init_channel(root, ("alice", "bob"), "owner", name="alpha-11111")

    entry_id = channel.post(
        root,
        "owner",
        "info",
        "t-one",
        "supervisor exception",
        refs=f"main@{foreign_sha}",
        force=True,
        name="alpha-11111",
    )

    assert entry_id == "MSG-1"


def test_party_force_stays_refused(tmp_path: Path) -> None:
    ours = tmp_path / "ours"
    _git_repo_with_commit(ours)
    foreign_sha = _git_repo_with_commit(tmp_path / "theirs")
    root = ours / "collab"
    channel.init_channel(root, ("alice", "bob"), "owner", name="alpha-11111")

    with pytest.raises(ChannelError, match="supervisor-only"):
        channel.post(
            root,
            "alice",
            "review-request",
            "t-one",
            "x",
            refs=f"main@{foreign_sha}",
            force=True,
            name="alpha-11111",
        )
