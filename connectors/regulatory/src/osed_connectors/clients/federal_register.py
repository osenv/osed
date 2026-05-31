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


_STAY_TERMS = ("stay", "vacat", "remand")

_CHANGE_KIND = {
    "Rule": "amendment_or_final_rule",
    "Proposed Rule": "proposed_change",
    "Notice": "notice",
}

_CHANGES_NOTICE = (
    "Evidence of Federal Register actions affecting this CFR citation — amendments, "
    "corrections, and agency notices (including agency-announced stays). This is NOT a "
    "currency determination, and it does NOT capture judicial vacaturs or court-ordered "
    "stays, which are court actions found in case law (e.g. CourtListener), sometimes with "
    "a lagging FR notice. Classifying the rule CURRENT / CHANGED / DEAD / UNVERIFIED is a "
    "judgment for a licensed attorney."
)


def _tag_change(doc: dict[str, Any]) -> dict[str, Any]:
    base = _normalize(doc)
    haystack = f"{base.get('title') or ''} {base.get('abstract') or ''}".lower()
    base["change_kind"] = _CHANGE_KIND.get(base.get("type"), "other")
    base["mentions_stay_or_vacatur"] = any(t in haystack for t in _STAY_TERMS)
    return base


def search_rule_changes(
    *,
    cfr_title: int | str,
    cfr_part: int | str,
    since: str | None = None,
    limit: int = 20,
    transport: httpx.BaseTransport | None = None,
) -> dict[str, Any]:
    """Find Federal Register documents affecting a CFR citation — the "did this rule
    change?" step of a currency check.

    Returns later amendments, corrections, and agency notices (incl. agency-announced
    stays) for `cfr_title`/`cfr_part`, newest first. EVIDENCE only: it does not classify
    the rule's currency, and it does not see judicial vacaturs/stays (those are case law).
    `since` is an optional earliest publication date, "YYYY-MM-DD".
    """
    cfr_citation = f"{cfr_title} CFR {cfr_part}"
    query_echo = {"cfr_title": str(cfr_title), "cfr_part": str(cfr_part),
                  "since": since, "limit": limit}

    params: list[tuple[str, str]] = [
        ("conditions[cfr][title]", str(cfr_title)),
        ("conditions[cfr][part]", str(cfr_part)),
        ("order", "newest"),
        ("per_page", str(max(_MIN_PER_PAGE, limit))),
    ]
    for field in _FIELDS:
        params.append(("fields[]", field))
    if since:
        params.append(("conditions[publication_date][gte]", since))

    try:
        resp = http.get(_ENDPOINT, params=params, transport=transport)
    except httpx.HTTPError as exc:
        return not_found(
            source_api=_SOURCE_API, source_url=_ENDPOINT,
            reason=f"Federal Register request failed: {exc}", query_echo=query_echo,
        )

    source_url = str(resp.request.url)
    if resp.status_code != 200:
        return not_found(
            source_api=_SOURCE_API, source_url=source_url,
            reason=f"Federal Register returned HTTP {resp.status_code}.", query_echo=query_echo,
        )

    data = resp.json()
    results = data.get("results")
    if not results:
        return not_found(
            source_api=_SOURCE_API, source_url=source_url,
            reason=(f"No Federal Register actions affecting {cfr_citation} found"
                    f"{' since ' + since if since else ''} (count={data.get('count', 0)}). "
                    f"Absence of an FR action is not proof the rule is unchanged."),
            query_echo=query_echo,
        )

    changes = [_tag_change(d) for d in results[:limit]]
    return found(
        source_api=_SOURCE_API, source_url=source_url,
        result={"cfr_citation": cfr_citation, "count": data.get("count"),
                "returned": len(changes), "changes": changes},
        query_echo=query_echo, notice=_CHANGES_NOTICE,
    )
