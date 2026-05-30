"""The shared HTTP layer enforces a host allowlist and a timeout. The allowlist
is defense-in-depth: even if a URL is constructed wrong, the connector can only
ever talk to the government APIs it is supposed to."""

import httpx
import pytest

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
