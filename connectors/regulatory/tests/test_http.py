"""The shared HTTP layer enforces a host allowlist and a timeout. The allowlist
is defense-in-depth: even if a URL is constructed wrong, the connector can only
ever talk to the government APIs it is supposed to."""

import httpx
import pytest

from osed_connectors import http
from osed_connectors.http import ALLOWED_HOSTS, DisallowedHost, get


def _ok(request):
    return httpx.Response(200, json={"ok": True})


def test_rejects_disallowed_host():
    with pytest.raises(DisallowedHost):
        get("https://evil.example.com/api", transport=httpx.MockTransport(_ok))


def test_allows_federal_register_host():
    r = get(
        "https://www.federalregister.gov/api/v1/documents.json",
        params={"per_page": 5},
        transport=httpx.MockTransport(_ok),
    )
    assert r.status_code == 200


def test_allows_ecfr_host():
    r = get(
        "https://www.ecfr.gov/api/versioner/v1/titles.json",
        transport=httpx.MockTransport(_ok),
    )
    assert r.status_code == 200


def test_non_200_is_returned_not_raised():
    """Clients decide what a 404 means (often an honest not-found); the HTTP
    layer must not raise on it."""

    def not_found(request):
        return httpx.Response(404, text="nope")

    r = get("https://www.ecfr.gov/x", transport=httpx.MockTransport(not_found))
    assert r.status_code == 404


def test_phase1_hosts_are_allowlisted():
    assert "www.federalregister.gov" in ALLOWED_HOSTS
    assert "www.ecfr.gov" in ALLOWED_HOSTS


def test_phase2_hosts_are_allowlisted():
    assert "www.govinfo.gov" in ALLOWED_HOSTS
    assert "api.regulations.gov" in ALLOWED_HOSTS


def test_custom_headers_are_sent():
    """Lets a keyed client pass X-Api-Key in a header, so the key never appears
    in the request URL (and therefore never in an envelope's source_url)."""
    seen = {}

    def handler(request):
        seen.update(request.headers)
        return httpx.Response(200, json={})

    get(
        "https://api.regulations.gov/v4/documents",
        headers={"X-Api-Key": "secret-key"},
        transport=httpx.MockTransport(handler),
    )
    assert seen.get("x-api-key") == "secret-key"


def test_courtlistener_is_allowlisted():
    # POST to the CL citation-lookup host must be permitted (added for verify_citation).
    captured = {}

    def handler(request):
        captured["url"] = str(request.url)
        captured["auth"] = request.headers.get("Authorization")
        captured["body"] = request.content.decode()
        return httpx.Response(200, json=[])

    resp = http.post(
        "https://www.courtlistener.com/api/rest/v4/citation-lookup/",
        data={"text": "467 U.S. 837"},
        headers={"Authorization": "Token secret"},
        transport=httpx.MockTransport(handler),
    )
    assert resp.status_code == 200
    assert captured["auth"] == "Token secret"
    assert "text=467" in captured["body"].replace("+", "")  # body carries the citation
    assert "courtlistener.com" in captured["url"]


def test_post_rejects_non_allowlisted_host():
    import pytest
    with pytest.raises(http.DisallowedHost):
        http.post("https://evil.example.com/x", data={"a": "b"})


def test_post_accepts_timeout_override():
    # A longer timeout is needed for the slow CL endpoint; just assert it's accepted.
    def handler(request):
        return httpx.Response(200, json=[])

    resp = http.post(
        "https://www.courtlistener.com/api/rest/v4/citation-lookup/",
        data={"text": "x"},
        timeout=60.0,
        transport=httpx.MockTransport(handler),
    )
    assert resp.status_code == 200
