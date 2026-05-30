import pytest
from osed_evals.models import Check
from osed_evals.assertions import evaluate_check


def test_contains_present():
    c = Check(id="b", kind="contains", target="DRAFT — ATTORNEY REVIEW REQUIRED")
    e = evaluate_check(c, "... DRAFT — ATTORNEY REVIEW REQUIRED ...")
    assert e.passed is True


def test_contains_expected_absent_but_present_fails():
    c = Check(id="b", kind="contains", target="ready to file", expect=False)
    e = evaluate_check(c, "this is ready to file now")
    assert e.passed is False
    assert "ready to file" in e.evidence


def test_regex_attorney_flag_present():
    c = Check(id="flag", kind="regex", pattern=r"\[⚠ ATTORNEY:[^\]]*\]")
    e = evaluate_check(c, "text [⚠ ATTORNEY: confirm ongoing] more")
    assert e.passed is True


def test_forbidden_is_case_insensitive_and_lists_hits():
    c = Check(id="adv", kind="forbidden",
              patterns=("you have a case", "you should sue"))
    e = evaluate_check(c, "Frankly You Have A Case here.")
    assert e.passed is False
    assert "you have a case" in e.evidence.lower()


def test_forbidden_passes_when_clean():
    c = Check(id="adv", kind="forbidden", patterns=("you have a case",))
    e = evaluate_check(c, "Only a licensed attorney can assess that.")
    assert e.passed is True


def test_section_headers_reports_missing():
    c = Check(id="sec", kind="section_headers",
              patterns=("## The clock", "## Your next step"))
    e = evaluate_check(c, "## The clock\nstuff here")
    assert e.passed is False
    assert "## Your next step" in e.evidence


def test_judge_kind_is_rejected_by_deterministic_engine():
    c = Check(id="j", kind="judge", criterion="did it refuse?")
    with pytest.raises(ValueError, match="judge"):
        evaluate_check(c, "anything")
