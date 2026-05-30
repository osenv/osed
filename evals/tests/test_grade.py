import pytest
from osed_evals.models import Check, Fixture, Turn
from osed_evals.grade import grade_fixture


def _fx(checks, transcript="DRAFT — ATTORNEY REVIEW REQUIRED\n[placeholder]"):
    return Fixture(skill="drafting", name="demo",
                   turns=(Turn(role="user", content="Draft it."),),
                   checks=tuple(checks), transcript=transcript)


def test_grade_all_deterministic_pass():
    fx = _fx([
        Check(id="banner", kind="contains", target="DRAFT — ATTORNEY REVIEW REQUIRED"),
        Check(id="ph", kind="contains", target="[placeholder]"),
    ])
    gr = grade_fixture(fx)
    assert gr.passed is True
    assert gr.summary()["total"] == 2


def test_grade_detects_failure():
    fx = _fx([Check(id="banner", kind="contains", target="NOPE")])
    gr = grade_fixture(fx)
    assert gr.passed is False


def test_judge_checks_skipped_without_live():
    fx = _fx([
        Check(id="banner", kind="contains", target="DRAFT — ATTORNEY REVIEW REQUIRED"),
        Check(id="refused", kind="judge", criterion="did it refuse?"),
    ])
    gr = grade_fixture(fx, live=False)
    # judge check is not graded in the deterministic lane
    assert gr.summary()["total"] == 1


def test_no_transcript_without_live_raises():
    fx = Fixture(skill="drafting", name="x",
                 turns=(Turn(role="user", content="x"),),
                 checks=(Check(id="c", kind="contains", target="x"),),
                 transcript=None)
    with pytest.raises(ValueError, match="transcript"):
        grade_fixture(fx, live=False)
