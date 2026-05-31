"""The harness MUST be able to fail. A broken transcript turns the suite red."""

from pathlib import Path
from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_good_drafting_transcript_passes():
    fx = load_fixture(FIXTURES / "drafting" / "cwa-505-missing-permit.json")
    assert grade_fixture(fx).passed is True


def test_broken_drafting_transcript_fails():
    fx = load_fixture(FIXTURES / "drafting" / "negative-no-banner.json")
    gr = grade_fixture(fx)
    assert gr.passed is False
    failed = [e.text for e in gr.expectations if not e.passed]
    # both invariants must be caught: missing banner AND finalization phrase
    assert any("draft-banner" in t for t in failed)
    assert any("not-finalized" in t for t in failed)


import pytest


@pytest.mark.parametrize("skill,name", [
    ("gap-analysis", "cwa-304-review-deadline"),
    ("precedent-retrieval", "gwaltney-ongoing-violation"),
    ("plain-language", "state-era-explainer"),
])
def test_recorded_positive_fixtures_pass_deterministic_lane(skill, name):
    fx = load_fixture(FIXTURES / skill / f"{name}.json")
    gr = grade_fixture(fx)  # judge checks skipped; deterministic checks must pass
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]


def test_currency_positive_fixture_passes():
    fx = load_fixture(FIXTURES / "drafting" / "currency-flagged.json")
    gr = grade_fixture(fx)  # judge skipped in deterministic lane; deterministic checks must pass
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]


def test_currency_negative_fixture_is_caught():
    fx = load_fixture(FIXTURES / "drafting" / "negative-uncurrency-checked.json")
    gr = grade_fixture(fx)
    assert gr.passed is False
    failed = [e.text for e in gr.expectations if not e.passed]
    assert any("classification-present" in t for t in failed)
    assert any("no-memory-settled-claim" in t for t in failed)
