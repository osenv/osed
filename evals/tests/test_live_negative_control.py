"""Live end-to-end negative control: a deliberately-broken skill must be caught.

Proves the FULL live harness (run + grade) — not just the engine — catches a
skill whose output violates an invariant. Gated behind `live`; run with
`pytest -m live`.

IMPORTANT caveat (empirically observed): a capable model is robust enough to
"self-heal" a tampered SKILL.md — e.g. the broken drafting variant explicitly
says "Do NOT add any DRAFT banner", yet the model often re-adds the banner from
its strong drafting priors. So we cannot assert that a *specific* injected
defect (the banner) disappears. Instead: if the broken variant happens to
produce fully-compliant output this run, we SKIP (a finding about model
resilience, not a harness bug); when it does produce a violation, we assert the
harness caught it. The authoritative, deterministic "the suite can fail"
guarantee lives in `test_negative_control.py` (recorded broken transcript).
"""

from pathlib import Path
import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture
from osed_evals.runner import run_skill_live

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
BROKEN = Path(__file__).resolve().parents[1] / "broken-variants" / "drafting-no-banner"


@pytest.mark.live
def test_broken_skill_variant_is_caught_when_output_is_broken(monkeypatch):
    from osed_evals.judge import evaluate_judge
    fx = load_fixture(FIXTURES / "drafting" / "cwa-505-missing-permit.json")
    # Point the runner at the broken variant via the override env var.
    monkeypatch.setenv("OSED_EVAL_SKILL_DIR", str(BROKEN))
    transcript = run_skill_live(fx)
    gr = grade_fixture(fx, live=True, transcript=transcript, judge_fn=evaluate_judge)

    if gr.passed:
        pytest.skip(
            "broken variant self-healed to fully-compliant output (model resisted "
            "the tampered instructions); deterministic negative control is authoritative"
        )
    # The broken skill produced an invariant violation and the live harness caught it.
    failed = [e.text for e in gr.expectations if not e.passed]
    assert failed
