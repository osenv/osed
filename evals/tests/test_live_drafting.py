"""Live integration: actually run the drafting skill and grade real output.

Gated behind the `live` marker (deselected by default). Requires Claude Code
auth in the environment. Run with: pytest -m live
"""

from pathlib import Path
import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture
from osed_evals.runner import run_skill_live

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.mark.live
def test_drafting_skill_obeys_invariants_live():
    from osed_evals.judge import evaluate_judge  # imported here: judge module is Task 11
    fx = load_fixture(FIXTURES / "drafting" / "cwa-505-missing-permit.json")
    transcript = run_skill_live(fx)
    gr = grade_fixture(fx, live=True, transcript=transcript, judge_fn=evaluate_judge)
    assert gr.passed is True, [
        (e.text, e.evidence) for e in gr.expectations if not e.passed
    ]
