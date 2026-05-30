"""GovInfo client — the "statutory duty" step: retrieve US Code section text.

Addressing a section by (title, number) is done through the GovInfo **link
service** (``/link/uscode/{title}/{section}``), which 302-redirects to the
keyless content HTML for the latest annual edition and reveals the package and
granule IDs in the URL. This is more robust than the search API (whose field
queries are brittle) and needs no API key.

Important limits this tool surfaces (it does not resolve them — that is for a
lawyer): a statutory *deadline* clause may live in an **uncodified statutory
note** or the **public law** rather than the codified US Code section, and a
**relative** deadline ("within 2 years of enactment") needs the enactment date,
which the codified text may not state. And the existence of a codified duty today
does not prove it is still in force — a duty can be amended or repealed by later
statute, so the doctrinal-currency check applies to the duty itself.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse

import httpx

from .. import http
from ..envelope import found, not_found

_LINK_URL = "https://www.govinfo.gov/link/uscode/{title}/{section}"
_SOURCE_API = "govinfo"
_REDIRECTS = {301, 302, 303, 307, 308}
_EDITION_RE = re.compile(r"USCODE-(\d{4})-")

_NOTICE = (
    "US Code section text. A statutory DEADLINE may not appear here: deadline "
    "clauses often live in uncodified statutory notes or the public law, not the "
    "codified section, and a relative deadline ('within N years of enactment') "
    "needs the enactment date. The existence of a duty today does not prove it is "
    "still in force — it can be amended or repealed by later statute, so the "
    "doctrinal-currency check applies to the duty itself. Evidence for a human to "
    "weigh, not a determination."
)


class _TextExtractor(HTMLParser):
    """Collect readable text, dropping script/style and adding line breaks at
    block boundaries so the statute stays roughly legible."""

    _BREAKERS = {"br", "p", "div", "tr", "li"}
    _SKIP = {"script", "style"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skipping = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self._SKIP:
            self._skipping += 1
        elif tag in self._BREAKERS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skipping:
            self._skipping -= 1
        elif tag in self._BREAKERS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skipping:
            self.parts.append(data)


def _html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    lines = (line.strip() for line in "".join(parser.parts).splitlines())
    return "\n".join(line for line in lines if line)


def get_uscode_section(
    *,
    title: int,
    section: str,
    transport: httpx.BaseTransport | None = None,
) -> dict[str, Any]:
    """Fetch the current US Code text for a citation (e.g. title=42, section="7409").

    Returns an evidence envelope. `found` is False (with a reason) when the
    citation does not resolve or the content cannot be fetched. On success,
    `source_current_as_of` is the annual edition year.
    """
    query_echo = {"title": title, "section": section}
    link_url = _LINK_URL.format(title=title, section=section)

    try:
        link_resp = http.get(link_url, params={"link-type": "html"}, transport=transport)
    except httpx.HTTPError as exc:
        return not_found(
            source_api=_SOURCE_API,
            source_url=link_url,
            reason=f"GovInfo link request failed: {exc}",
            query_echo=query_echo,
        )

    if link_resp.status_code not in _REDIRECTS:
        return not_found(
            source_api=_SOURCE_API,
            source_url=link_url,
            reason=(
                f"GovInfo link service returned HTTP {link_resp.status_code} for "
                f"{title} U.S.C. {section} — the citation does not resolve to a "
                f"US Code section."
            ),
            query_echo=query_echo,
        )

    location = link_resp.headers.get("location")
    if not location:
        return not_found(
            source_api=_SOURCE_API,
            source_url=link_url,
            reason="GovInfo link service redirected without a Location header.",
            query_echo=query_echo,
        )

    try:
        content_resp = http.get(location, transport=transport)
    except httpx.HTTPError as exc:
        return not_found(
            source_api=_SOURCE_API,
            source_url=location,
            reason=f"GovInfo content request failed: {exc}",
            query_echo=query_echo,
        )
    if content_resp.status_code != 200:
        return not_found(
            source_api=_SOURCE_API,
            source_url=location,
            reason=f"GovInfo content endpoint returned HTTP {content_resp.status_code}.",
            query_echo=query_echo,
        )

    path_parts = urlparse(location).path.split("/")
    package_id = path_parts[path_parts.index("pkg") + 1] if "pkg" in path_parts else None
    granule_id = path_parts[-1].removesuffix(".htm") if path_parts else None
    edition_match = _EDITION_RE.search(location)
    edition = edition_match.group(1) if edition_match else None

    text = _html_to_text(content_resp.text)
    return found(
        source_api=_SOURCE_API,
        source_url=location,
        result={
            "title": title,
            "section": section,
            "citation": f"{title} U.S.C. {section}",
            "edition": edition,
            "package_id": package_id,
            "granule_id": granule_id,
            "document_url": location,
            "text": text,
            "chars": len(text),
        },
        query_echo=query_echo,
        source_current_as_of=edition,
        notice=_NOTICE,
    )
