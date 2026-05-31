"""CourtListener verify_citation — citation existence + subsequent-history evidence.

Mock the v4 citation-lookup response shape (probed live): a top-level LIST of
per-citation objects {citation, status, clusters:[{case_name, date_filed,
precedential_status, citation_count, absolute_url, history, ...}]}. status==200
means the cite resolved. Evidence-only: it never says a case is good/dead law.
"""

import httpx

from osed_connectors.clients import courtlistener as cl

CL_RESOLVED = [
    {
        "citation": "467 U.S. 837",
        "normalized_citations": ["467 U.S. 837"],
        "status": 200,
        "error_message": "",
        "clusters": [
            {
                "case_name": "Chevron U.S.A. Inc. v. NRDC",
                "date_filed": "1984-06-25",
                "precedential_status": "Published",
                "citation_count": 20624,
                "absolute_url": "/opinion/111221/chevron-u-s-a-inc-v-nrdc/",
                "history": "", "procedural_history": "", "disposition": "",
            }
        ],
    }
]

CL_UNRESOLVED = [
    {"citation": "999 U.S. 999", "normalized_citations": [], "status": 404,
     "error_message": "Citation not found", "clusters": []}
]


def _transport(payload, status=200, sink=None):
    def handler(request):
        if sink is not None:
            sink.append(request)
        return httpx.Response(status, json=payload)

    return httpx.MockTransport(handler)


def test_resolved_citation_returns_evidence():
    env = cl.verify_citation(text="Chevron, 467 U.S. 837 (1984)", api_key="t",
                             transport=_transport(CL_RESOLVED))
    assert env["found"] is True
    assert env["source_api"] == "courtlistener"
    cites = env["result"]["citations"]
    assert len(cites) == 1
    c = cites[0]
    assert c["resolved"] is True
    assert c["case_name"] == "Chevron U.S.A. Inc. v. NRDC"
    assert c["date_filed"] == "1984-06-25"
    assert c["citation_count"] == 20624
    assert c["absolute_url"] == "https://www.courtlistener.com/opinion/111221/chevron-u-s-a-inc-v-nrdc/"
    assert env["result"]["resolved_count"] == 1
    assert "good law" in env["notice"].lower()


def test_unresolved_citation_is_evidence_not_error():
    env = cl.verify_citation(text="999 U.S. 999", api_key="t", transport=_transport(CL_UNRESOLVED))
    assert env["found"] is True  # the lookup ran; non-resolution is itself evidence
    c = env["result"]["citations"][0]
    assert c["resolved"] is False
    assert env["result"]["resolved_count"] == 0


def test_key_travels_in_header_not_url():
    sink = []
    cl.verify_citation(text="467 U.S. 837", api_key="secret-token",
                       transport=_transport(CL_RESOLVED, sink=sink))
    req = sink[0]
    assert req.headers.get("Authorization") == "Token secret-token"
    assert "secret-token" not in str(req.url)


def test_missing_key_is_explicit_not_found(monkeypatch):
    monkeypatch.delenv("COURTLISTENER_API_KEY", raising=False)
    env = cl.verify_citation(text="467 U.S. 837")
    assert env["found"] is False
    assert "COURTLISTENER_API_KEY" in env["reason"]


def test_no_input_is_explicit_not_found():
    env = cl.verify_citation(api_key="t")
    assert env["found"] is False
    assert "citation" in env["reason"].lower()


def test_upstream_error_is_not_found_with_reason():
    env = cl.verify_citation(text="467 U.S. 837", api_key="t",
                             transport=_transport({}, status=500))
    assert env["found"] is False
    assert "500" in env["reason"]
