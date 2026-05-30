"""Shared HTTP access for the connectors.

Two safeguards live here, at the boundary rather than in prose:

* a **host allowlist** — the connector can only reach the government APIs it is
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
}

DEFAULT_TIMEOUT = httpx.Timeout(15.0)
_USER_AGENT = "osed-connectors/0.1 (+https://github.com/bgarakani/osed)"


class DisallowedHost(ValueError):
    """Raised when a request targets a host outside the allowlist."""


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
    host = urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise DisallowedHost(
            f"Refusing request to non-allowlisted host: {host!r}. "
            f"Allowed: {sorted(ALLOWED_HOSTS)}"
        )
    merged_headers = {"User-Agent": _USER_AGENT}
    if headers:
        merged_headers.update(headers)
    with httpx.Client(
        timeout=DEFAULT_TIMEOUT,
        transport=transport,
        follow_redirects=False,
        headers=merged_headers,
    ) as client:
        return client.get(url, params=params)
