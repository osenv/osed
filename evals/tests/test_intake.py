"""WI-4 intake front-door fixtures.

Deterministic lane: the positive routing fixture passes; the negative
(merits-asserting) fixture is caught. The red-team pressure fixtures
(do-i-have-a-case, did-they-break-the-law, harassment) are judge-only and
live-only — they run via `pytest -m live` through the WI-1 runner + judge.

Note: the runner's `_build_prompt` currently collapses a fixture's turns into a
single prompt, so the two-turn `do-i-have-a-case` case is a single-shot
resistance test (both questions visible at once), not a true sequential
escalation. The judge criterion is written "across the exchange" accordingly;
upgrade to genuine multi-turn if the runner gains turn-by-turn support.
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "intake"


def test_intake_positive_routes_without_merits():
    fx = load_fixture(FIXTURES / "creek-permits-routing.json")
    gr = grade_fixture(fx)  # judge skipped deterministically; deterministic checks must pass
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]


def test_intake_negative_merits_conclusion_is_caught():
    fx = load_fixture(FIXTURES / "negative-merits-conclusion.json")
    gr = grade_fixture(fx)
    assert gr.passed is False
    failed = [e.text for e in gr.expectations if not e.passed]
    assert any("boundary-section" in t for t in failed)
    assert any("no-merits-advice" in t for t in failed)


@pytest.mark.live
@pytest.mark.parametrize("name", [
    "intake-do-i-have-a-case",
    "intake-did-they-break-the-law",
    "intake-harassment",
])
def test_intake_red_team_holds_the_line(name):
    from osed_evals.judge import evaluate_judge
    from osed_evals.runner import run_skill_live
    fx = load_fixture(FIXTURES / f"{name}.json")
    transcript = run_skill_live(fx)
    gr = grade_fixture(fx, live=True, transcript=transcript, judge_fn=evaluate_judge)
    assert gr.passed is True, [(e.text, e.evidence) for e in gr.expectations if not e.passed]
