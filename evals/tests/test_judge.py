import pytest

from osed_evals.models import Check
from osed_evals.judge import _parse_verdict, _expectation_from_verdict


def test_parse_verdict_plain_json():
    assert _parse_verdict('{"passed": true, "evidence": "ok"}') == {
        "passed": True, "evidence": "ok"}


def test_parse_verdict_unwraps_prose_and_fences():
    raw = 'Here is my verdict:\n```json\n{"passed": false, "evidence": "nope"}\n```\n'
    assert _parse_verdict(raw) == {"passed": False, "evidence": "nope"}


def test_parse_verdict_raises_without_json():
    with pytest.raises(ValueError, match="no JSON object"):
        _parse_verdict("I could not decide.")


def test_expectation_from_verdict_builds_text_and_fields():
    c = Check(id="refused", kind="judge", invariant=5, criterion="did it refuse?")
    e = _expectation_from_verdict(c, {"passed": False, "evidence": "it predicted the outcome"})
    assert e.passed is False
    assert "refused" in e.text and "invariant 5" in e.text
    assert e.evidence == "it predicted the outcome"


def test_parse_verdict_ignores_trailing_prose_with_stray_brace():
    raw = '{"passed": true, "evidence": "ok"} Note: template was {criterion}.'
    assert _parse_verdict(raw) == {"passed": True, "evidence": "ok"}
