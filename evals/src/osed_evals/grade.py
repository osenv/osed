"""Grade a Fixture into a GradeResult.

Deterministic lane (`live=False`): grades the fixture's recorded `transcript`
against all non-judge checks; judge checks are skipped. Live lane
(`live=True`): if no transcript is supplied it is produced by running the
skill (caller passes `transcript=`), and judge checks are evaluated.
"""

from __future__ import annotations

from .assertions import evaluate_check
from .models import Fixture, GradeResult


def _select_text(transcript: str, scope: str) -> str:
    # Recorded transcripts are graded whole; multi-turn scope selection is
    # applied by the live runner before calling grade_fixture (it passes the
    # already-selected text as `transcript`). For recorded single outputs the
    # whole transcript is the assistant text regardless of scope.
    return transcript


def grade_fixture(
    fixture: Fixture,
    *,
    live: bool = False,
    transcript: str | None = None,
    judge_fn=None,
) -> GradeResult:
    text = transcript if transcript is not None else fixture.transcript
    if text is None:
        raise ValueError(
            f"fixture {fixture.name!r}: no transcript to grade "
            "(supply a recorded transcript, or run with live=True)"
        )

    result = GradeResult(skill=fixture.skill, fixture=fixture.name)
    for check in fixture.checks:
        if check.is_deterministic:
            result.expectations.append(evaluate_check(check, _select_text(text, check.scope)))
        elif live:
            if judge_fn is None:
                raise ValueError("live grading of a judge check requires judge_fn")
            result.expectations.append(judge_fn(check, text))
        # else: judge check skipped in the deterministic lane
    return result
