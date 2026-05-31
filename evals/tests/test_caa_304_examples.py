"""CAA §304 golden worked-example fixtures — each pipeline stage must pass deterministically.

Mirrors test_golden_examples.py: the deterministic lane proves the §304 exemplars are
self-consistent against the recorded transcripts. Judge checks are skipped (deterministic).
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

GOLDEN = [
    ("gap-analysis", "caa-304-failure-to-act"),
    ("drafting", "caa-304-failure-to-act-notice"),
    ("precedent-retrieval", "caa-304-failure-to-act-precedent"),
    ("plain-language", "caa-304-failure-to-act-plain"),
    ("gap-analysis", "caa-304-emissions"),
    ("drafting", "caa-304-emissions-notice"),
    ("precedent-retrieval", "caa-304-emissions-precedent"),
    ("plain-language", "caa-304-emissions-plain"),
]


@pytest.mark.parametrize("skill,name", GOLDEN)
def test_caa_304_stage_fixture_passes_deterministic_lane(skill, name):
    fx = load_fixture(FIXTURES / skill / f"{name}.json")
    gr = grade_fixture(fx)
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]
