"""GovInfo client — "the statutory duty: pull the US Code section text."

Addresses a section via the keyless GovInfo *link service*
(/link/uscode/{title}/{section}), which 302-redirects to the keyless content
HTML and auto-selects the latest annual edition. A non-302 from the link service
(probed: HTTP 400) means the citation does not resolve -> honest not-found."""

import httpx

from osed_connectors.clients import govinfo

CONTENT_URL = (
    "https://www.govinfo.gov/content/pkg/USCODE-2024-title42/html/"
    "USCODE-2024-title42-chap85-subchapI-partA-sec7409.htm"
)

HTML = (
    "<html><head><title>U.S.C. Title 42</title></head><body>"
    "<span>United States Code, 2024 Edition</span><br/>"
    "<span>Title 42 - THE PUBLIC HEALTH AND WELFARE</span><br/>"
    "<pre>&sect; 7409. National primary and secondary ambient air quality standards\n"
    "(a) The Administrator shall publish ... shall promulgate ...</pre>"
    "</body></html>"
)


def _router(*, link_status=302, location=CONTENT_URL, content_status=200, html=HTML, sink=None):
    def handler(request):
        if sink is not None:
            sink.append(request)
        if "/link/uscode/" in request.url.path:
            if link_status in (301, 302, 303, 307, 308):
                headers = {"location": location} if location else {}
                return httpx.Response(link_status, headers=headers)
            return httpx.Response(link_status, text="bad citation")
        return httpx.Response(content_status, text=html if content_status == 200 else "nope")

    return httpx.MockTransport(handler)


def test_returns_section_text_edition_and_ids():
    env = govinfo.get_uscode_section(title=42, section="7409", transport=_router())
    assert env["found"] is True
    assert env["source_api"] == "govinfo"
    r = env["result"]
    assert "ambient air quality" in r["text"]
    assert r["citation"] == "42 U.S.C. 7409"
    assert r["edition"] == "2024"
    assert r["package_id"] == "USCODE-2024-title42"
    assert r["granule_id"] == "USCODE-2024-title42-chap85-subchapI-partA-sec7409"
    assert r["document_url"] == CONTENT_URL
    # the annual edition is the currency signal
    assert env["source_current_as_of"] == "2024"


def test_unknown_citation_is_not_found_and_skips_content_fetch():
    sink = []
    env = govinfo.get_uscode_section(title=42, section="999999", transport=_router(link_status=400, sink=sink))
    assert env["found"] is False
    assert env["result"] is None
    assert "400" in env["reason"] or "not" in env["reason"].lower()
    assert all("/content/" not in r.url.path for r in sink)


def test_redirect_without_location_is_not_found():
    env = govinfo.get_uscode_section(title=42, section="7409", transport=_router(location=None))
    assert env["found"] is False


def test_content_fetch_failure_is_not_found():
    env = govinfo.get_uscode_section(title=42, section="7409", transport=_router(content_status=404))
    assert env["found"] is False
    assert "404" in env["reason"]


def test_notice_flags_uncodified_notes_and_duty_currency():
    env = govinfo.get_uscode_section(title=42, section="7409", transport=_router())
    notice = env["notice"].lower()
    assert "uncodified" in notice or "statutory note" in notice
    assert "enactment" in notice


def test_source_url_carries_no_api_key():
    env = govinfo.get_uscode_section(title=42, section="7409", transport=_router())
    assert "api_key" not in env["source_url"]
    assert env["source_url"] == CONTENT_URL
