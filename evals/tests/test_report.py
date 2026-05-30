from osed_evals.models import Expectation, GradeResult
from osed_evals.report import to_grading_json, summarize


def _gr(name, passed):
    return GradeResult(skill="drafting", fixture=name,
                       expectations=[Expectation(text="t", passed=passed, evidence="")])


def test_to_grading_json_matches_skill_creator_shape():
    gr = _gr("demo", True)
    blob = to_grading_json(gr)
    assert blob["skill"] == "drafting"
    assert blob["fixture"] == "demo"
    assert blob["expectations"][0] == {"text": "t", "passed": True, "evidence": ""}
    assert blob["summary"] == {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0}


def test_summarize_aggregates_across_fixtures():
    s = summarize([_gr("a", True), _gr("b", False)])
    assert s["fixtures_total"] == 2
    assert s["fixtures_passed"] == 1
    assert s["fixtures_failed"] == 1
