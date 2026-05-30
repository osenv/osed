"""eCFR client — "does the rule exist now?"

Two-step against the live contract (probed): GET titles.json for the title's
`up_to_date_as_of` (the freshness signal), then GET the dated full-content XML.
A 404 on the content fetch is the honest "no such codified text" signal. XML is
parsed with defusedxml (untrusted-input hardening, secure-by-default)."""

import httpx

from osed_connectors.clients import ecfr

TITLES = {
    "titles": [
        {
            "number": 40,
            "name": "Protection of Environment",
            "latest_amended_on": "2026-05-27",
            "latest_issue_date": "2026-05-27",
            "up_to_date_as_of": "2026-05-28",
            "reserved": False,
        }
    ],
    "meta": {},
}

SECTION_XML = (
    b'<?xml version="1.0" encoding="UTF-8"?>\n'
    b'<DIV8 N="50.1" TYPE="SECTION" '
    b'hierarchy_metadata="{&quot;citation&quot;:&quot;40 CFR 50.1&quot;}">\n'
    b"<HEAD>\xc2\xa7 50.1 Definitions.</HEAD>\n"
    b"<P>(a) As used in this part, all terms not defined herein shall have "
    b"the meaning given them by the Act.</P>\n"
    b"<P>(b) <I>Act</I> means the Clean Air Act, as amended.</P>\n"
    b"</DIV8>\n"
)


def _router(*, titles=TITLES, xml=SECTION_XML, xml_status=200, sink=None):
    def handler(request):
        if sink is not None:
            sink.append(request)
        if request.url.path.endswith("/titles.json"):
            return httpx.Response(200, json=titles)
        if xml_status != 200:
            return httpx.Response(xml_status, text="not found")
        return httpx.Response(200, content=xml, headers={"content-type": "application/xml"})

    return httpx.MockTransport(handler)


def test_get_section_returns_text_and_currency_date():
    env = ecfr.get_current_text(title=40, part="50", section="50.1", transport=_router())
    assert env["found"] is True
    assert env["source_api"] == "ecfr"
    assert "Definitions" in env["result"]["heading"]
    assert "Clean Air Act" in env["result"]["text"]
    # the eCFR freshness date is distinct from when we fetched it
    assert env["source_current_as_of"] == "2026-05-28"
    assert env["retrieved_at"]
    assert env["result"]["section"] == "50.1"


def test_missing_part_is_not_found_the_rule_does_not_exist():
    env = ecfr.get_current_text(title=40, part="999999", transport=_router(xml_status=404))
    assert env["found"] is False
    assert env["result"] is None
    assert "404" in env["reason"]


def test_unknown_title_is_not_found_before_fetching_content():
    sink = []
    env = ecfr.get_current_text(title=99, part="1", transport=_router(sink=sink))
    assert env["found"] is False
    # should bail after the titles lookup, never request content
    assert all("/full/" not in r.url.path for r in sink)


def test_notice_flags_ecfr_as_unofficial():
    env = ecfr.get_current_text(title=40, part="50", section="50.1", transport=_router())
    assert "unofficial" in env["notice"].lower()


def test_content_url_carries_the_currency_date_and_target():
    sink = []
    ecfr.get_current_text(title=40, part="50", transport=_router(sink=sink))
    content = [r for r in sink if "/full/" in r.url.path][0]
    assert "/full/2026-05-28/title-40.xml" in content.url.path
    assert content.url.params["part"] == "50"
