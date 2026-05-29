"""The evidence envelope is the safeguard contract: every tool result carries
its source URL, a retrieval timestamp, and an honest found/not-found signal."""

from datetime import datetime, timezone

from osed_connectors.envelope import found, not_found


def test_found_envelope_carries_source_and_result():
    env = found(
        source_api="federal_register",
        source_url="https://www.federalregister.gov/api/v1/documents.json?x=1",
        result={"document_number": "2026-02822"},
        query_echo={"term": "ozone"},
    )
    assert env["found"] is True
    assert env["result"] == {"document_number": "2026-02822"}
    assert env["source_api"] == "federal_register"
    assert env["source_url"].startswith("https://www.federalregister.gov")
    assert env["query_echo"] == {"term": "ozone"}
    assert env["reason"] is None


def test_not_found_is_explicit_never_a_silent_empty():
    env = not_found(
        source_api="ecfr",
        source_url="https://www.ecfr.gov/api/versioner/v1/full/2026-05-28/title-40.xml?part=999999",
        reason="eCFR returned HTTP 404 for title 40 part 999999",
        query_echo={"title": 40, "part": "999999"},
    )
    assert env["found"] is False
    assert env["result"] is None
    assert "404" in env["reason"]
    assert env["source_url"].startswith("https://www.ecfr.gov")


def test_retrieved_at_is_timezone_aware_utc():
    env = found(
        source_api="ecfr",
        source_url="https://www.ecfr.gov/x",
        result={},
        query_echo={},
    )
    parsed = datetime.fromisoformat(env["retrieved_at"])
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == timezone.utc.utcoffset(None)


def test_source_current_as_of_supports_currency_check():
    env = found(
        source_api="ecfr",
        source_url="https://www.ecfr.gov/x",
        result={},
        query_echo={},
        source_current_as_of="2026-05-28",
    )
    assert env["source_current_as_of"] == "2026-05-28"


def test_source_current_as_of_defaults_to_none_when_unknown():
    env = found(
        source_api="federal_register",
        source_url="https://www.federalregister.gov/x",
        result={},
        query_echo={},
    )
    assert env["source_current_as_of"] is None
