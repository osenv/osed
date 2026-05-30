"""Federal Register client — the "did the agency act, and when?" step.

Searches published rules, proposed rules, and notices. This is *evidence that an
action was published on a date*, not a determination that a duty was met or a
deadline missed — that judgment belongs to a human (see the tool notice).

Live API contract (probed):
* endpoint: https://www.federalregister.gov/api/v1/documents.json
* a zero-result response is `{description, count}` with **no** `results` key
* `per_page=1` is silently ignored and returns the default page, so we request
  at least 5 and slice client-side to the caller's limit.
"""

from __future__ import annotations

from typing import Any

import httpx

from .. import http
from ..envelope import found, not_found

_ENDPOINT = "https://www.federalregister.gov/api/v1/documents.json"
_SOURCE_API = "federal_register"

# Minimum per_page the API actually honors (per_page=1 is ignored).
_MIN_PER_PAGE = 5

# User-facing document type -> Federal Register `conditions[type][]` code.
_DOC_TYPES = {
    "rule": "RULE",
    "proposed_rule": "PRORULE",
    "notice": "NOTICE",
}

_FIELDS = [
    "document_number",
    "title",
    "type",
    "publication_date",
    "effective_on",
    "citation",
    "agencies",
    "html_url",
    "pdf_url",
    "abstract",
]

_NOTICE = (
    "Evidence that a document was published on a date — not a determination that "
    "a duty was met, missed, or timely. Whether any action satisfies a statutory "
    "deadline is a legal judgment for a licensed attorney."
)


def _normalize(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "document_number": doc.get("document_number"),
        "title": doc.get("title"),
        "type": doc.get("type"),
        "publication_date": doc.get("publication_date"),
        "effective_on": doc.get("effective_on"),
        "citation": doc.get("citation"),
        "agencies": [a.get("name") for a in doc.get("agencies", []) if a.get("name")],
        "html_url": doc.get("html_url"),
        "pdf_url": doc.get("pdf_url"),
        "abstract": doc.get("abstract"),
    }


def search_actions(
    *,
    term: str,
    agency: str | None = None,
    doc_type: str | None = None,
    published_since: str | None = None,
    published_before: str | None = None,
    limit: int = 10,
    transport: httpx.BaseTransport | None = None,
) -> dict[str, Any]:
    """Search the Federal Register for agency actions matching `term`.

    `agency` is a Federal Register agency slug (e.g. "environmental-protection-agency").
    `doc_type` is one of "rule", "proposed_rule", "notice". Dates are YYYY-MM-DD.
    Returns an evidence envelope; `found` is False (with a reason) when nothing
    matched or the upstream call failed.
    """
    query_echo = {
        "term": term,
        "agency": agency,
        "doc_type": doc_type,
        "published_since": published_since,
        "published_before": published_before,
        "limit": limit,
    }

    params: list[tuple[str, str]] = [
        ("conditions[term]", term),
        ("order", "newest"),
        ("per_page", str(max(_MIN_PER_PAGE, limit))),
    ]
    for field in _FIELDS:
        params.append(("fields[]", field))
    if agency:
        params.append(("conditions[agencies][]", agency))
    if doc_type:
        code = _DOC_TYPES.get(doc_type)
        if code is None:
            return not_found(
                source_api=_SOURCE_API,
                source_url=_ENDPOINT,
                reason=f"Unknown doc_type {doc_type!r}; expected one of {sorted(_DOC_TYPES)}.",
                query_echo=query_echo,
            )
        params.append(("conditions[type][]", code))
    if published_since:
        params.append(("conditions[publication_date][gte]", published_since))
    if published_before:
        params.append(("conditions[publication_date][lte]", published_before))

    try:
        resp = http.get(_ENDPOINT, params=params, transport=transport)
    except httpx.HTTPError as exc:
        return not_found(
            source_api=_SOURCE_API,
            source_url=_ENDPOINT,
            reason=f"Federal Register request failed: {exc}",
            query_echo=query_echo,
        )

    source_url = str(resp.request.url)

    if resp.status_code != 200:
        return not_found(
            source_api=_SOURCE_API,
            source_url=source_url,
            reason=f"Federal Register returned HTTP {resp.status_code}.",
            query_echo=query_echo,
        )

    data = resp.json()
    results = data.get("results")  # absent entirely when count == 0
    if not results:
        return not_found(
            source_api=_SOURCE_API,
            source_url=source_url,
            reason=f"No Federal Register documents matched (count={data.get('count', 0)}).",
            query_echo=query_echo,
        )

    documents = [_normalize(d) for d in results[:limit]]
    return found(
        source_api=_SOURCE_API,
        source_url=source_url,
        result={"count": data.get("count"), "returned": len(documents), "documents": documents},
        query_echo=query_echo,
        notice=_NOTICE,
    )
