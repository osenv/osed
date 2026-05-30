"""Live red-team: the precedent skill must hold the line under multi-turn pressure.

Gated behind `live`. Run with: pytest -m live
Exercises fixtures/red-team/precedent-hypothetical-win.json — the
"hypothetically would I win" escalation that invariant 5 forbids answering.
"""

from pathlib import Path
import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture
from osed_evals.runner import run_skill_live

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.mark.live
def test_precedent_refuses_hypothetical_win():
    from osed_evals.judge import evaluate_judge
    fx = load_fixture(FIXTURES / "red-team" / "precedent-hypothetical-win.json")
    transcript = run_skill_live(fx)
    gr = grade_fixture(fx, live=True, transcript=transcript, judge_fn=evaluate_judge)
    assert gr.passed is True, [
        (e.text, e.evidence) for e in gr.expectations if not e.passed
    ]
