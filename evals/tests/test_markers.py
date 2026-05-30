from osed_evals import markers


def test_draft_banner_core_substring():
    assert "DRAFT — ATTORNEY REVIEW REQUIRED" in markers.DRAFT_BANNER


def test_attorney_flag_regex_matches_real_flag():
    import re
    flag = "[⚠ ATTORNEY: confirm each exceedance is \"ongoing\" under Gwaltney]"
    assert re.search(markers.ATTORNEY_FLAG_REGEX, flag)


def test_attorney_flag_regex_rejects_plain_brackets():
    import re
    assert re.search(markers.ATTORNEY_FLAG_REGEX, "[placeholder]") is None


def test_finalization_phrases_are_lowercase_for_ci_matching():
    # forbidden-phrase matching is case-insensitive; store canonical lowercase
    for p in markers.DRAFTING_FORBIDDEN_FINALIZATION:
        assert p == p.lower()


def test_plain_language_sections_present():
    assert "## The clock" in markers.PLAIN_LANGUAGE_SECTIONS
    assert "## Your next step" in markers.PLAIN_LANGUAGE_SECTIONS
