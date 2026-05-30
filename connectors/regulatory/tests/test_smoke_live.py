"""Live smoke tests against the keyless government APIs.

These hit the real Federal Register and eCFR endpoints — no API keys required,
so CI can run them without secrets. Marked `live` so an offline run can skip them
with `-m "not live"`. They assert the *contract we depend on* still holds (shapes,
not specific records), and that the safeguards survive a real round-trip.
"""

import pytest

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
