"""Live end-to-end negative control: a deliberately-broken skill must fail.

Proves the FULL harness (run + grade), not just the engine, can go red.
Gated behind `live`. Run with: pytest -m live
"""

from pathlib import Path
import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture
from osed_evals.runner import run_skill_live

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
BROKEN = Path(__file__).resolve().parents[1] / "broken-variants" / "drafting-no-banner"


@pytest.mark.live
def test_broken_skill_variant_makes_suite_red(monkeypatch):
    from osed_evals.judge import evaluate_judge
    fx = load_fixture(FIXTURES / "drafting" / "cwa-505-missing-permit.json")
    # Point the runner at the broken variant via the override env var.
    monkeypatch.setenv("OSED_EVAL_SKILL_DIR", str(BROKEN))
    transcript = run_skill_live(fx)
    gr = grade_fixture(fx, live=True, transcript=transcript, judge_fn=evaluate_judge)
    assert gr.passed is False  # missing DRAFT banner must be caught
    assert any("draft-banner" in e.text and not e.passed for e in gr.expectations)
