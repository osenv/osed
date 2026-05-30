"""Live smoke tests against the keyless government APIs.

These hit the real Federal Register and eCFR endpoints — no API keys required,
so CI can run them without secrets. Marked `live` so an offline run can skip them
with `-m "not live"`. They assert the *contract we depend on* still holds (shapes,
not specific records), and that the safeguards survive a real round-trip.
"""

import pytest

from osed_connectors.clients import ecfr
from osed_connectors.clients import federal_register as fr

pytestmark = pytest.mark.live


def test_federal_register_returns_real_agency_actions():
    env = fr.search_actions(
        term="ozone",
        agency="environmental-protection-agency",
        doc_type="rule",
        limit=3,
    )
    assert env["found"] is True
    docs = env["result"]["documents"]
    assert 1 <= len(docs) <= 3
    for doc in docs:
        assert doc["publication_date"]  # the "when"
        assert doc["html_url"].startswith("https://www.federalregister.gov/")
    # safeguards survived the real round-trip
    assert env["source_url"].startswith("https://www.federalregister.gov/api/v1/documents.json")
    assert env["retrieved_at"]
    assert env["notice"]


def test_federal_register_nonsense_term_is_honest_not_found():
    env = fr.search_actions(term="zzqxnonsensequeryxyz123", limit=3)
    assert env["found"] is False
    assert env["result"] is None
    assert env["reason"]


def test_ecfr_returns_current_text_with_freshness_date():
    # 40 CFR 50.1 — definitions for the National Ambient Air Quality Standards.
    env = ecfr.get_current_text(title=40, part="50", section="50.1")
    assert env["found"] is True
    assert "Clean Air Act" in env["result"]["text"]
    # eCFR's own freshness date, distinct from retrieved_at
    assert env["source_current_as_of"]
    assert env["source_current_as_of"] != env["retrieved_at"]
    assert "unofficial" in env["notice"].lower()
    assert env["source_url"].startswith("https://www.ecfr.gov/api/versioner/v1/full/")


def test_ecfr_missing_part_is_honest_not_found():
    env = ecfr.get_current_text(title=40, part="999999")
    assert env["found"] is False
    assert env["result"] is None
    assert "404" in env["reason"]
