"""Regulations.gov v4 client — "the delay timeline: docket and comment history."

The only keyed phase-2 source. The key is read from REGULATIONS_GOV_API_KEY (or
passed explicitly) and sent via the X-Api-Key header, so it never lands in a URL
or an envelope's source_url. Comment/posting dates are returned as raw evidence;
the tool notice forbids reading them as proof of agency action."""

import httpx

from osed_connectors.clients import regulations_gov as rg

REG_TWO = {
    "data": [
        {
            "id": "EPA-HQ-OAR-2021-0001-0001",
            "type": "documents",
            "attributes": {
                "title": "Proposed Rule X",
                "docketId": "EPA-HQ-OAR-2021-0001",
                "documentType": "Proposed Rule",
                "postedDate": "2021-03-01T05:00:00Z",
                "commentStartDate": "2021-03-01T05:00:00Z",
                "commentEndDate": "2021-05-01T03:59:59Z",
                "frDocNum": "2021-04567",
                "lastModifiedDate": "2021-03-02T00:00:00Z",
                "withdrawn": False,
            },
        },
        {
            "id": "EPA-HQ-OAR-2021-0001-0050",
            "type": "documents",
            "attributes": {
                "title": "Final Rule X",
                "docketId": "EPA-HQ-OAR-2021-0001",
                "documentType": "Rule",
                "postedDate": "2023-06-15T04:00:00Z",
                "commentStartDate": None,
                "commentEndDate": None,
                "frDocNum": "2023-12890",
                "lastModifiedDate": "2023-06-16T00:00:00Z",
                "withdrawn": False,
            },
        },
    ],
    "meta": {"totalElements": 2, "hasNextPage": False, "pageSize": 5},
}

REG_EMPTY = {"data": [], "meta": {"totalElements": 0, "hasNextPage": False}}


def _transport(payload, status=200, sink=None):
    def handler(request):
        if sink is not None:
            sink.append(request)
        return httpx.Response(status, json=payload)

    return httpx.MockTransport(handler)


def test_returns_normalized_timeline():
    env = rg.find_rulemaking_documents(
        docket_id="EPA-HQ-OAR-2021-0001", api_key="TESTKEY", transport=_transport(REG_TWO)
    )
    assert env["found"] is True
    assert env["source_api"] == "regulations_gov"
    docs = env["result"]["documents"]
    assert len(docs) == 2
    first = docs[0]
    assert first["document_type"] == "Proposed Rule"
    assert first["posted_date"] == "2021-03-01T05:00:00Z"
    assert first["comment_end_date"] == "2021-05-01T03:59:59Z"
    assert first["docket_id"] == "EPA-HQ-OAR-2021-0001"
    assert env["result"]["total"] == 2


def test_missing_key_is_explicit_not_found(monkeypatch):
    monkeypatch.delenv("REGULATIONS_GOV_API_KEY", raising=False)
    env = rg.find_rulemaking_documents(agency="EPA", transport=_transport(REG_TWO))
    assert env["found"] is False
    assert "REGULATIONS_GOV_API_KEY" in env["reason"]


def test_key_travels_in_header_not_url():
    sink = []
    env = rg.find_rulemaking_documents(
        agency="EPA", api_key="SECRET123", transport=_transport(REG_TWO, sink=sink)
    )
    req = sink[0]
    assert req.headers.get("x-api-key") == "SECRET123"
    assert "SECRET123" not in str(req.url)
    assert "api_key" not in env["source_url"]
    assert "SECRET123" not in env["source_url"]


def test_page_size_min_5_and_slices_to_limit():
    sink = []
    env = rg.find_rulemaking_documents(
        agency="EPA", limit=1, api_key="TESTKEY", transport=_transport(REG_TWO, sink=sink)
    )
    assert int(sink[0].url.params["page[size]"]) >= 5
    assert len(env["result"]["documents"]) == 1


def test_filters_map_to_v4_params():
    sink = []
    rg.find_rulemaking_documents(
        term="ozone",
        agency="EPA",
        docket_id="EPA-HQ-OAR-2021-0001",
        document_type="Rule",
        posted_since="2021-01-01",
        api_key="TESTKEY",
        transport=_transport(REG_TWO, sink=sink),
    )
    p = sink[0].url.params
    assert p["filter[searchTerm]"] == "ozone"
    assert p["filter[agencyId]"] == "EPA"
    assert p["filter[docketId]"] == "EPA-HQ-OAR-2021-0001"
    assert p["filter[documentType]"] == "Rule"
    assert p["filter[postedDate][ge]"] == "2021-01-01"


def test_zero_results_is_not_found():
    env = rg.find_rulemaking_documents(agency="EPA", api_key="TESTKEY", transport=_transport(REG_EMPTY))
    assert env["found"] is False
    assert env["result"] is None


def test_403_is_not_found_with_reason():
    env = rg.find_rulemaking_documents(
        agency="EPA", api_key="BADKEY", transport=_transport({"errors": [{"status": "403"}]}, status=403)
    )
    assert env["found"] is False
    assert "403" in env["reason"]


def test_notice_flags_comment_dates_as_not_agency_action():
    env = rg.find_rulemaking_documents(agency="EPA", api_key="TESTKEY", transport=_transport(REG_TWO))
    assert "not" in env["notice"].lower() and "agency action" in env["notice"].lower()
