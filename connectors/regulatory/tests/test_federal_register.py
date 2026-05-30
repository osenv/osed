"""Federal Register client — "did the agency act, and when?"

Tests use httpx.MockTransport against the exact response shape the live API
returns (probed: zero-result responses omit the `results` key entirely; result
objects carry document_number/title/type/publication_date/html_url/pdf_url/
agencies[]/citation/effective_on)."""

import httpx

from osed_connectors.clients import federal_register as fr

FR_TWO = {
    "description": "Documents matching 'ozone' and of type Rule",
    "count": 2,
    "total_pages": 1,
    "results": [
        {
            "document_number": "2026-02822",
            "title": "Air Plan Approval; Ohio; Second Maintenance Plan for 2008 Ozone NAAQS",
            "type": "Rule",
            "publication_date": "2026-02-12",
            "html_url": "https://www.federalregister.gov/documents/2026/02/12/2026-02822/x",
            "pdf_url": "https://www.govinfo.gov/content/pkg/FR-2026-02-12/pdf/2026-02822.pdf",
            "agencies": [
                {"raw_name": "ENVIRONMENTAL PROTECTION AGENCY", "name": "Environmental Protection Agency", "id": 145}
            ],
            "citation": "91 FR 6517",
            "effective_on": "2026-03-16",
            "abstract": "EPA is approving revisions to the Ohio SIP.",
        },
        {
            "document_number": "2026-07889",
            "title": "Finding of Failure To Attain",
            "type": "Rule",
            "publication_date": "2026-04-23",
            "html_url": "https://www.federalregister.gov/documents/2026/04/23/2026-07889/y",
            "pdf_url": "https://www.govinfo.gov/content/pkg/FR-2026-04-23/pdf/2026-07889.pdf",
            "agencies": [{"name": "Environmental Protection Agency"}],
            "citation": "91 FR 21729",
            "effective_on": "2026-05-26",
            "abstract": "EPA finalizing a finding of failure to attain.",
        },
    ],
}

# Live API quirk: a zero-result response is just {description, count} — no `results`.
FR_ZERO = {"description": "Documents matching 'zzqx'", "count": 0}


def _transport(payload, status=200, sink=None):
    def handler(request):
        if sink is not None:
            sink.append(request)
        return httpx.Response(status, json=payload)

    return httpx.MockTransport(handler)


def test_search_returns_normalized_documents():
    env = fr.search_actions(term="ozone", transport=_transport(FR_TWO))
    assert env["found"] is True
    assert env["source_api"] == "federal_register"
    docs = env["result"]["documents"]
    assert len(docs) == 2
    first = docs[0]
    assert first["document_number"] == "2026-02822"
    assert first["publication_date"] == "2026-02-12"
    assert first["citation"] == "91 FR 6517"
    # agencies normalized to a flat list of display names
    assert first["agencies"] == ["Environmental Protection Agency"]
    assert env["result"]["count"] == 2


def test_zero_results_is_explicit_not_found():
    env = fr.search_actions(term="zzqx", transport=_transport(FR_ZERO))
    assert env["found"] is False
    assert env["result"] is None
    assert "0" in env["reason"]


def test_upstream_error_is_not_found_with_reason():
    env = fr.search_actions(term="ozone", transport=_transport({}, status=503))
    assert env["found"] is False
    assert "503" in env["reason"]


def test_limit_is_respected_and_avoids_per_page_1_quirk():
    sink = []
    env = fr.search_actions(term="ozone", limit=1, transport=_transport(FR_TWO, sink=sink))
    # per_page=1 is silently ignored by the live API, so the client must ask for >=5...
    per_page = int(sink[0].url.params["per_page"])
    assert per_page >= 5
    # ...and slice down to the requested limit itself.
    assert len(env["result"]["documents"]) == 1


def test_filters_map_to_federal_register_conditions():
    sink = []
    fr.search_actions(
        term="ozone",
        agency="environmental-protection-agency",
        doc_type="rule",
        published_since="2026-01-01",
        transport=_transport(FR_TWO, sink=sink),
    )
    params = sink[0].url.params
    assert params["conditions[term]"] == "ozone"
    assert params["conditions[agencies][]"] == "environmental-protection-agency"
    assert params["conditions[type][]"] == "RULE"
    assert params["conditions[publication_date][gte]"] == "2026-01-01"


def test_source_url_is_the_real_request_url():
    env = fr.search_actions(term="ozone", transport=_transport(FR_TWO))
    assert env["source_url"].startswith("https://www.federalregister.gov/api/v1/documents.json")
    assert "ozone" in env["source_url"]
