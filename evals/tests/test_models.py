from osed_evals.models import Turn, Check, Fixture, Expectation, GradeResult


def test_check_defaults_and_kind():
    c = Check(id="banner", kind="contains", target="DRAFT", invariant=1)
    assert c.expect is True
    assert c.scope == "final"
    assert c.patterns == ()


def test_fixture_holds_turns_and_checks():
    fx = Fixture(
        skill="drafting",
        name="demo",
        turns=(Turn(role="user", content="Draft the notice."),),
        checks=(Check(id="banner", kind="contains", target="DRAFT"),),
        transcript="DRAFT — ATTORNEY REVIEW REQUIRED",
    )
    assert fx.turns[0].role == "user"
    assert fx.checks[0].id == "banner"
    assert fx.transcript.startswith("DRAFT")


def test_grade_result_summary_counts():
    gr = GradeResult(
        skill="drafting",
        fixture="demo",
        expectations=[
            Expectation(text="a", passed=True, evidence=""),
            Expectation(text="b", passed=False, evidence="missing"),
        ],
    )
    s = gr.summary()
    assert s == {"passed": 1, "failed": 1, "total": 2, "pass_rate": 0.5}


def test_grade_result_passed_property():
    gr = GradeResult(skill="s", fixture="f",
                     expectations=[Expectation(text="a", passed=True, evidence="")])
    assert gr.passed is True
