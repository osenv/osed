"""WI-5 pipeline (orchestration) fixtures.

Deterministic lane: the assembled positive package passes every invariant marker
across stages; the negative (bypassed-invariants) package is caught. The red-team
pressure fixtures (skip-the-draft, will-i-win) are judge-only and live-only — they
run via `pytest -m live` through the WI-1 runner + judge.

Note: the runner collapses a fixture's turns into a single prompt, so the two-turn
skip-the-draft case is a single-shot resistance test, not a sequential escalation.
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "pipeline"


def test_pipeline_positive_package_preserves_invariants():
    fx = load_fixture(FIXTURES / "cwa-304m-package.json")
    gr = grade_fixture(fx)  # judge skipped deterministically; deterministic checks must pass
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]


def test_pipeline_negative_bypassed_invariants_is_caught():
    fx = load_fixture(FIXTURES / "negative-bypassed-invariants.json")
    gr = grade_fixture(fx)
    assert gr.passed is False
    failed = [e.text for e in gr.expectations if not e.passed]
    assert any("package-banner" in t for t in failed)
    assert any("consolidated-checklist" in t for t in failed)
    assert any("no-merits" in t for t in failed)


@pytest.mark.live
@pytest.mark.parametrize("name", ["pipeline-skip-the-draft", "pipeline-will-i-win"])
def test_pipeline_red_team_holds_the_line(name):
    from osed_evals.judge import evaluate_judge
    from osed_evals.runner import run_skill_live
    fx = load_fixture(FIXTURES / f"{name}.json")
    transcript = run_skill_live(fx)
    gr = grade_fixture(fx, live=True, transcript=transcript, judge_fn=evaluate_judge)
    assert gr.passed is True, [(e.text, e.evidence) for e in gr.expectations if not e.passed]
