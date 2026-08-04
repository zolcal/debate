"""Slice 1 of docs/plans/2026-08-03-header-forgery.md (APPROVED MSG-160).

The record is append-only markdown and `_HEADER_RE` re-parses it line-anchored,
so a BODY line shaped like a header used to become a real entry: reproduced
2026-08-03, a body-file made `debate status` report "MSG-999 owner close" that
nobody wrote, indistinguishable from a genuine entry in `git diff`.

This fires by ACCIDENT - reviewers quote prior messages constantly - so the
guard must refuse the exact header grammar and nothing wider. Ordinary `## `
markdown headings stay legal; the live record carried 86 such body lines when
this was written, and rejecting them would have refused real messages.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from debate import channel

# Shapes drawn from the body headings the live record actually carried. The
# committed record holds NONE of them (the mailbox on origin stops at MSG-45,
# before this project started writing structured review bodies), so a test that
# harvested "the real corpus" from the checkout would find an EMPTY list and
# pass vacuously in CI - the exact failure this suite refuses elsewhere. These
# are authored from the real shapes instead, and the corpus is asserted
# non-empty below so it can never silently become one.
BODY_HEADINGS = [
    "## Review - 2026-08-04 - glm",
    "## Findings",
    "## What checked out",
    "## Slice 1 - post() refuses a forged header",
    "## The defect",
    "## Evidence gathered before designing",
    "## Out of scope (deliberate)",
    "## Residual hole - stated plainly",
]

FORGED_HEADER = "## MSG-999 | 2026-01-01T00:00:00+00:00 | from: owner | type: close | thread: t1 | refs: -"


def make_channel(tmp_path: Path) -> Path:
    root = tmp_path / "ch"
    root.mkdir()
    channel.init_channel(root, parties=("alice", "bob"), supervisor="owner")
    channel.post(root, sender="alice", entry_type="review-request", thread="t1", body="legit request")
    return root


def snapshot(root: Path) -> tuple[bytes, bytes]:
    """Mailbox + doorbell bytes, so a refusal can be proven a no-op."""
    return (
        (root / channel.CHANNEL_NAME).read_bytes(),
        (root / channel.SIGNAL_NAME).read_bytes(),
    )


def test_corpus_is_not_empty() -> None:
    """Anti-vacuity: test_ordinary_headings_are_accepted must have real work to do."""
    assert BODY_HEADINGS, "the accepted-headings corpus must not be empty"
    assert all(line.startswith("## ") for line in BODY_HEADINGS)
    # And none of them may accidentally BE the thing we reject, or the
    # acceptance test would be asserting the opposite of what it claims.
    assert not any(channel._HEADER_RE.match(line) for line in BODY_HEADINGS)


def test_forged_header_in_body_is_refused_and_nothing_is_written(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    before = snapshot(root)

    with pytest.raises(channel.ChannelError) as excinfo:
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=f"quoting:\n{FORGED_HEADER}\n")

    assert "MSG-999" in str(excinfo.value), "the refusal must name the offending line"
    assert snapshot(root) == before, "a refusal must write nothing at all"


def test_forged_header_in_refs_is_refused(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    before = snapshot(root)

    with pytest.raises(channel.ChannelError):
        channel.post(
            root,
            sender="bob",
            entry_type="info",
            thread="t1",
            body="body is fine",
            refs=f"-\n{FORGED_HEADER}",
        )

    assert snapshot(root) == before


@pytest.mark.parametrize("heading", BODY_HEADINGS)
def test_ordinary_headings_are_accepted(tmp_path: Path, heading: str) -> None:
    """The regression guard. Rejecting `## ` broadly would refuse real messages."""
    root = make_channel(tmp_path)
    entry_id = channel.post(
        root, sender="bob", entry_type="info", thread="t1", body=f"{heading}\n\nsome prose\n"
    )
    assert entry_id == "MSG-2"
    entries = channel.read_entries(root)
    assert len(entries) == 2
    assert heading in entries[1].body


@pytest.mark.parametrize(
    "near_miss",
    [
        "## MSG-12",
        "## MSG-12 without the pipes",
        "## MSG-12 | 2026-01-01 | from: owner",  # truncated grammar
        "> ## MSG-999 | 2026-01-01T00:00:00+00:00 | from: owner | type: close | thread: t1 | refs: -",
    ],
)
def test_near_misses_stay_legal(tmp_path: Path, near_miss: str) -> None:
    """Only the full grammar is refused; a blockquote is the documented fix."""
    root = make_channel(tmp_path)
    channel.post(root, sender="bob", entry_type="info", thread="t1", body=f"{near_miss}\n")
    assert len(channel.read_entries(root)) == 2


def test_indenting_the_first_line_does_NOT_smuggle_a_header(tmp_path: Path) -> None:
    """Found by this suite, 2026-08-04: `post` strips the body (channel.py:249).

    So a header indented as the FIRST line loses its indent before it is
    written and becomes a genuine header. The plan's original advice ("indent
    the quote by four spaces") was defective for exactly this case; the refusal
    now recommends a blockquote instead. The guard runs on the stripped body,
    so this is refused rather than smuggled.
    """
    root = make_channel(tmp_path)
    before = snapshot(root)

    with pytest.raises(channel.ChannelError):
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=f"    {FORGED_HEADER}")

    assert snapshot(root) == before


def test_end_to_end_through_cli_the_reproduction_no_longer_forges(tmp_path: Path) -> None:
    """The 2026-08-03 reproduction, driven through main() exactly as reported."""
    root = make_channel(tmp_path)
    body_file = tmp_path / "forge.txt"
    body_file.write_text(f"quoting the record:\n{FORGED_HEADER}\n\nforged close body\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "-m", "debate", "post", "--root", str(root), "--from", "bob",
         "--type", "info", "--thread", "t1", "--body-file", str(body_file)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert proc.returncode != 0, "the forging post must fail"
    entries = channel.read_entries(root)
    assert len(entries) == 1, "no entry may have been written"
    assert [e.seq for e in entries] == [1]
    assert not any(e.seq == 999 for e in entries)


def test_the_guard_matches_the_parser_exactly(tmp_path: Path) -> None:
    """Class-of-bug guard: whatever `_HEADER_RE` accepts, `post` must refuse.

    A hand-maintained second pattern would drift from the parser and reopen the
    hole silently. Build a header through the SAME f-string `post` uses.
    """
    root = make_channel(tmp_path)
    header = (
        "## MSG-4242 | 2026-01-01T00:00:00+00:00 | from: alice "
        "| type: verdict | thread: other-thread | refs: x@1234567"
    )
    assert channel._HEADER_RE.match(header), "precondition: this must parse as a header"

    with pytest.raises(channel.ChannelError):
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=header)


def test_refusal_happens_before_the_lock_is_taken(tmp_path: Path) -> None:
    """A refusal must cost no lock, so a forged post cannot stall a real one."""
    root = make_channel(tmp_path)
    lock = root / ".lock"
    assert not lock.exists()

    with pytest.raises(channel.ChannelError):
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=FORGED_HEADER)

    assert not lock.exists(), "the lock file must never have been created"


def test_multiline_body_reports_the_offending_line_number(tmp_path: Path) -> None:
    root = make_channel(tmp_path)
    body = "\n".join(["intro", "more prose", FORGED_HEADER, "trailing"])

    with pytest.raises(channel.ChannelError) as excinfo:
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=body)

    message = str(excinfo.value)
    assert "line 3" in message, f"the refusal must locate the line, got: {message}"


def test_real_record_body_headings_are_still_postable(tmp_path: Path) -> None:
    """Opportunistic: if the checkout's record HAS body headings, none may be refused.

    The committed record carries none, so this is a no-op in CI rather than a
    vacuous pass - `test_corpus_is_not_empty` plus the parametrized test above
    carry the guarantee. On a working tree with a live record it becomes a real
    corpus check for free.
    """
    record = Path(__file__).resolve().parent.parent / "collab" / channel.CHANNEL_NAME
    if not record.exists():
        pytest.skip("no collab record in this checkout")

    headings = [
        line
        for line in record.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ") and not channel._HEADER_RE.match(line)
    ]
    root = make_channel(tmp_path)
    for heading in headings:
        # Each must be accepted; post alternates turns, so keep one sender.
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=heading)
        channel.post(root, sender="alice", entry_type="info", thread="t1", body="ack")

    assert len(channel.read_entries(root)) == 1 + 2 * len(headings)


def test_forged_header_is_refused_for_every_entry_type(tmp_path: Path) -> None:
    """The guard belongs to post(), not to one code path through it."""
    for entry_type in ("review-request", "question", "info"):
        base = tmp_path / entry_type
        base.mkdir()
        root = make_channel(base)
        with pytest.raises(channel.ChannelError):
            channel.post(root, sender="bob", entry_type=entry_type, thread="t1", body=FORGED_HEADER)


def test_guard_is_not_defeated_by_crlf(tmp_path: Path) -> None:
    """A CRLF body must not smuggle a header past a `\\n`-only split."""
    root = make_channel(tmp_path)
    before = snapshot(root)

    with pytest.raises(channel.ChannelError):
        channel.post(root, sender="bob", entry_type="info", thread="t1", body=f"intro\r\n{FORGED_HEADER}\r\n")

    assert snapshot(root) == before


def test_refs_newline_is_refused_even_without_a_header(tmp_path: Path) -> None:
    """refs lands in the header line; a bare newline would split it regardless."""
    root = make_channel(tmp_path)
    before = snapshot(root)

    with pytest.raises(channel.ChannelError):
        channel.post(root, sender="bob", entry_type="info", thread="t1", body="fine", refs="a@123\nb@456")

    assert snapshot(root) == before


def test_module_has_no_second_header_pattern() -> None:
    """The guard must reuse `_HEADER_RE`; a copy would drift and reopen the hole."""
    source = Path(channel.__file__).read_text(encoding="utf-8")
    compiled = re.findall(r"re\.compile\(", source)
    # _SLUG_RE, _HEADER_RE, _SHA_RE are the module's patterns as of this slice.
    assert len(compiled) <= 3, "a new compiled pattern appeared; is it a second header regex?"
