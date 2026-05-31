"""Shared HTTP access for the connectors.

Two safeguards live here, at the boundary rather than in prose:

* a **host allowlist** — the connector can only reach the government APIs and the
  one vetted first-party legal-data API (CourtListener / Free Law Project) it is
  built for, so a malformed URL can never become an exfiltration or SSRF vector;
* a **timeout** — no tool call can hang indefinitely.

Non-2xx responses are returned, not raised: an HTTP 404 from a regulatory API is
usually a legitimate "no such record," which clients turn into an honest
not-found envelope. Redirects are not followed, so a 3xx cannot bounce a request
to a host outside the allowlist.
"""

from __future__ import annotations

from urllib.parse import urlparse

import httpx

ALLOWED_HOSTS: set[str] = {
    "www.federalregister.gov",
    "www.ecfr.gov",
    "www.govinfo.gov",
    "api.regulations.gov",
    # Vetted first-party case-law source (Free Law Project). Reached directly with
    # the user's own key in a header — not via an untrusted third-party MCP. Used
    # by the CourtListener verify_citation tool (WI-2).
    "www.courtlistener.com",
}

DEFAULT_TIMEOUT = httpx.Timeout(15.0)
_USER_AGENT = "osed-connectors/0.1 (+https://github.com/bgarakani/osed)"


class DisallowedHost(ValueError):
    """Raised when a request targets a host outside the allowlist."""


def _guard(url: str) -> None:
    host = urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise DisallowedHost(
            f"Refusing request to non-allowlisted host: {host!r}. "
            f"Allowed: {sorted(ALLOWED_HOSTS)}"
        )


def _merged_headers(headers: dict | None) -> dict:
    merged = {"User-Agent": _USER_AGENT}
    if headers:
        merged.update(headers)
    return merged


def get(
    url: str,
    *,
    params: dict | list | None = None,
    headers: dict | None = None,
    transport: httpx.BaseTransport | None = None,
) -> httpx.Response:
    """GET `url`, enforcing the host allowlist and timeout.

    `headers` are merged over the default User-Agent — used to pass an API key in
    a header (e.g. X-Api-Key) so it never appears in the request URL, and thus
    never in an envelope's `source_url`. `transport` is injectable so tests can
    supply an `httpx.MockTransport` without touching the network.
    """
    _guard(url)
    with httpx.Client(
        timeout=DEFAULT_TIMEOUT,
        transport=transport,
        follow_redirects=False,
        headers=_merged_headers(headers),
    ) as client:
        return client.get(url, params=params)


def post(
    url: str,
    *,
    data: dict | None = None,
    headers: dict | None = None,
    timeout: float | httpx.Timeout | None = None,
    transport: httpx.BaseTransport | None = None,
) -> httpx.Response:
    """POST `url` with a form body, enforcing the host allowlist and timeout.

    Like `get`, `headers` carry API keys (e.g. Authorization: Token …) so the
    secret never lands in the URL. `timeout` overrides the default for slow
    endpoints (CourtListener's citation-lookup can take ~tens of seconds).
    """
    _guard(url)
    with httpx.Client(
        timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        transport=transport,
        follow_redirects=False,
        headers=_merged_headers(headers),
    ) as client:
        return client.post(url, data=data)
