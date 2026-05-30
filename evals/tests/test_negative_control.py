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
