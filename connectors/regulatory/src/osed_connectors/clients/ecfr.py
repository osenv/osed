"""eCFR client — the "does the rule exist now?" step.

Two requests against the eCFR Versioner API:

1. ``GET /api/versioner/v1/titles.json`` — to read the title's
   ``up_to_date_as_of`` date. This is both how we address current content and the
   freshness signal we hand back for the doctrinal-currency check.
2. ``GET /api/versioner/v1/full/{date}/title-{N}.xml?part=...[&section=...]`` —
   the current codified text. A 404 here is the honest "no such codified text"
   answer to "does the rule exist now."

eCFR is the *unofficial* but daily-fresh edition; the legally operative text is
the annual GPO CFR. Results are tagged accordingly (see the notice) so a reader
never mistakes currency for official status.

XML is parsed with ``defusedxml`` rather than the stdlib parser — the response is
external data, and defusedxml is the secure-by-default choice for untrusted XML.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
from defusedxml import ElementTree as ET

from .. import http
from ..envelope import found, not_found

_TITLES_URL = "https://www.ecfr.gov/api/versioner/v1/titles.json"
_FULL_URL = "https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{title}.xml"
_SOURCE_API = "ecfr"

# Tags that carry readable regulatory prose in eCFR XML.
_TEXT_TAGS = {"HEAD", "P", "HD1", "HD2", "HD3", "FP"}

_NOTICE = (
    "eCFR is the unofficial, daily-updated edition of the CFR. It is current but "
    "not the legally operative text — that is the annual GPO Code of Federal "
    "Regulations. Confirm against the official CFR before relying. A regulation's "
    "existence today does not confirm the underlying statutory duty is still in "
    "force: a duty can be amended or repealed by later statute, so the "
    "doctrinal-currency check applies to the duty itself, not only to case law."
)


def _extract(xml_bytes: bytes) -> tuple[str | None, str, str | None]:
    """Return (heading, text, citation) from eCFR full-content XML."""
    root = ET.fromstring(xml_bytes)

    citation = None
    meta = root.attrib.get("hierarchy_metadata")
    if meta:
        try:
            citation = json.loads(meta).get("citation")
        except (ValueError, TypeError):
            citation = None

    heading = None
    chunks: list[str] = []
    for el in root.iter():
        if el.tag in _TEXT_TAGS:
            text = "".join(el.itertext()).strip()
            if not text:
                continue
            if el.tag == "HEAD" and heading is None:
                heading = text
            chunks.append(text)

    return heading, "\n".join(chunks), citation


def get_current_text(
    *,
    title: int,
    part: str,
    section: str | None = None,
    transport: httpx.BaseTransport | None = None,
) -> dict[str, Any]:
    """Fetch the current eCFR text for a CFR title/part (optionally a section).

    Returns an evidence envelope. `found` is False when the title is unknown, the
    part/section has no codified text (HTTP 404 — i.e. the rule does not exist),
    or the upstream call fails. On success, `source_current_as_of` carries eCFR's
    own freshness date.
    """
    query_echo = {"title": title, "part": part, "section": section}

    # Step 1: resolve the title's current-as-of date.
    try:
        titles_resp = http.get(_TITLES_URL, transport=transport)
    except httpx.HTTPError as exc:
        return not_found(
            source_api=_SOURCE_API,
            source_url=_TITLES_URL,
            reason=f"eCFR titles request failed: {exc}",
            query_echo=query_echo,
        )
    if titles_resp.status_code != 200:
        return not_found(
            source_api=_SOURCE_API,
            source_url=str(titles_resp.request.url),
            reason=f"eCFR titles endpoint returned HTTP {titles_resp.status_code}.",
            query_echo=query_echo,
        )

    entry = next(
        (t for t in titles_resp.json().get("titles", []) if t.get("number") == title),
        None,
    )
    if entry is None:
        return not_found(
            source_api=_SOURCE_API,
            source_url=str(titles_resp.request.url),
            reason=f"CFR title {title} not found in eCFR title list.",
            query_echo=query_echo,
        )
    as_of = entry.get("up_to_date_as_of") or entry.get("latest_issue_date")

    # Step 2: fetch the dated content.
    content_url = _FULL_URL.format(date=as_of, title=title)
    params = [("part", part)]
    if section:
        params.append(("section", section))
    try:
        content_resp = http.get(content_url, params=params, transport=transport)
    except httpx.HTTPError as exc:
        return not_found(
            source_api=_SOURCE_API,
            source_url=content_url,
            reason=f"eCFR content request failed: {exc}",
            query_echo=query_echo,
        )

    source_url = str(content_resp.request.url)
    if content_resp.status_code == 404:
        target = f"section {section}" if section else f"part {part}"
        return not_found(
            source_api=_SOURCE_API,
            source_url=source_url,
            reason=(
                f"eCFR returned HTTP 404 for title {title} {target} — no such "
                f"codified text exists in the current edition."
            ),
            query_echo=query_echo,
        )
    if content_resp.status_code != 200:
        return not_found(
            source_api=_SOURCE_API,
            source_url=source_url,
            reason=f"eCFR content endpoint returned HTTP {content_resp.status_code}.",
            query_echo=query_echo,
        )

    heading, text, citation = _extract(content_resp.content)
    return found(
        source_api=_SOURCE_API,
        source_url=source_url,
        result={
            "title": title,
            "part": part,
            "section": section,
            "citation": citation,
            "heading": heading,
            "text": text,
            "chars": len(text),
        },
        query_echo=query_echo,
        source_current_as_of=as_of,
        notice=_NOTICE,
    )
