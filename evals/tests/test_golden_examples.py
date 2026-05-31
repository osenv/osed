"""WI-3 golden worked-example fixtures — each pipeline stage must pass deterministically.

These double as regression anchors: the deterministic lane proves the exemplar is
self-consistent; the gated `-m live` lane (via the WI-1 runner) re-runs the skill on
the same input to catch skill regression. Judge checks are skipped here (deterministic).
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

GOLDEN = [
    ("gap-analysis", "cwa-304m-deadline"),
    ("drafting", "cwa-304m-deadline-notice"),
    ("precedent-retrieval", "cwa-304m-deadline-precedent"),
    ("plain-language", "cwa-304m-deadline-plain"),
]


@pytest.mark.parametrize("skill,name", GOLDEN)
def test_golden_stage_fixture_passes_deterministic_lane(skill, name):
    fx = load_fixture(FIXTURES / skill / f"{name}.json")
    gr = grade_fixture(fx)
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]
