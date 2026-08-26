"""The fold-delta round: its protocol clauses and the docket composer.

Round 1 of a gate review establishes the criteria against the artifact. Every
round after it verifies FOLDS: the author folded round-N findings into the
artifact, and the seats must decide whether each fold resolves its finding —
which they can only do against the version they reviewed. So the PRIOR version
travels INTO the docket, and the round docket says, in the same words every
time, what the seat is to do with it.

Those words were hand-written into one docket after another until the wording
stopped changing; this module freezes them. `compose_docket` arranges what it
is given and nothing else: the author's goal, the two clauses, the prior/current
pairs, the prior verdict bodies, the author's fold list and the true diff. It
never decides that a finding is resolved -- that decision is the seat's, and an
engine that pre-answered it would be writing the verdict.
"""

from __future__ import annotations

import difflib
from collections.abc import Mapping
from dataclasses import dataclass

from debate import channel


R0_GOAL_PREFIX = "GOAL: "

R2_CLAUSE = (
    "Name EVERY blocking finding you can establish in this pass, not the first "
    "one; write the list so that a second pass by you would find nothing new. A "
    "verdict citing one blocker while others are establishable in the same pass is "
    "an incomplete verdict."
)

R3_CLAUSE = (
    "This is a fold-delta round. The change set is SCOPED to the artifact(s) under "
    "review; round scaffolding — the docket instruction sheet itself, which "
    "necessarily changes every round — is excluded by name. Compute the TRUE change "
    "set yourself by diffing the artifact against the prior version INCLUDED IN "
    "THIS DOCKET (named in the fold list header) — never trust the author's fold "
    "list as the change inventory; an artifact edit absent from the fold list is "
    "itself an unresolved finding. Then verify (a) that each fold in the true "
    "change set resolves its round-N finding, (b) the REVERSE: every round-N "
    "finding has a corresponding fold — a finding with no fold is unresolved, and "
    "(c) a coherence sweep: whether any change contradicts ANY other part of the "
    "artifact. Criteria that passed in round N stand UNLESS the true change set or "
    "the sweep implicates them — establish implicated ones on your own fresh "
    "evidence; for the rest, CITE the round-N verdict (MSG id) where your own "
    "evidence established them: standing is a citation, never an omission."
)

FOLD_LIST_HEADER_HEADING = "## Fold list header"
PRIOR_VERDICTS_HEADING = "## Prior-round verdicts (standing-by-citation input)"
FOLD_LIST_HEADING = "## Author's fold list (verify against your own diff)"
TRUE_DIFF_HEADING = "## True diff"


@dataclass(frozen=True)
class DeltaRound:
    """One round's inputs, all of them the author's own words or files.

    ``priors`` pairs each artifact under review with the version the previous
    round reviewed, both project-relative; ``prior_verdicts`` carries the
    previous round's verdict bodies under their MSG ids, because the channel
    record is not in the seats' docket and standing-by-citation needs the text.
    """

    goal: str
    fold_list: str
    priors: tuple[tuple[str, str], ...]
    prior_verdicts: tuple[tuple[str, str], ...]


def unified_diff(prior_text: str, current_text: str, *, prior_path: str, current_path: str) -> str:
    """The true change set of one artifact, labelled with the two paths."""
    return "".join(
        difflib.unified_diff(
            prior_text.splitlines(keepends=True),
            current_text.splitlines(keepends=True),
            fromfile=prior_path,
            tofile=current_path,
        )
    )


def compose_docket(round_: DeltaRound, *, diffs: Mapping[str, str]) -> str:
    """Arrange one round's inputs into the docket instruction sheet."""
    sections: list[str] = [R0_GOAL_PREFIX + round_.goal.strip(), R2_CLAUSE, R3_CLAUSE]

    header: list[str] = [FOLD_LIST_HEADER_HEADING]
    for current_path, prior_path in round_.priors:
        header.append(f"Prior version: `{prior_path}`\nCurrent version: `{current_path}`")
    sections.append("\n\n".join(header))

    verdicts: list[str] = [PRIOR_VERDICTS_HEADING]
    for entry_id, body in round_.prior_verdicts:
        # Verbatim, minus the trailing blank lines the section separator adds
        # back: what the seat reads has to be what the seat wrote.
        quoted = body.rstrip("\n")
        verdicts.append(f"### {entry_id}\n\n{quoted}")
    sections.append("\n\n".join(verdicts))

    fold_list = round_.fold_list.rstrip("\n")
    sections.append(f"{FOLD_LIST_HEADING}\n\n{fold_list}")

    blocks: list[str] = [TRUE_DIFF_HEADING]
    for current_path, _prior_path in round_.priors:
        if current_path not in diffs:
            raise channel.ChannelError(
                f"refused: no diff was computed for {current_path}; the round docket shows the "
                "true change set of every artifact under review"
            )
        body = diffs[current_path]
        if body and not body.endswith("\n"):
            body += "\n"
        blocks.append(f"### `{current_path}`\n\n```diff\n{body}```")
    sections.append("\n\n".join(blocks))

    return "\n\n".join(sections) + "\n"
