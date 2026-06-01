"""State-ERA orientation-packet fixtures — each packet must pass deterministically.

Mirrors test_golden_examples.py: the deterministic lane proves each per-state packet
carries its banner, law-as-of stamp, provision cite, the plain-language sections, the
no-merits closing, and (NY/HI) the developing-law marker. Judge checks are skipped here.
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

PACKETS = [
    ("drafting", "state-era-pa"),
    ("drafting", "state-era-mt"),
    ("drafting", "state-era-ny"),
    ("drafting", "state-era-hi"),
]


@pytest.mark.parametrize("skill,name", PACKETS)
def test_state_era_packet_passes_deterministic_lane(skill, name):
    fx = load_fixture(FIXTURES / skill / f"{name}.json")
    gr = grade_fixture(fx)
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]
