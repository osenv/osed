"""The evidence envelope.

Every connector tool returns this shape. It is where OSED's safeguards live at
the tool boundary (see CONNECTORS.md): a result is never returned without its
source URL and the moment it was retrieved, and "not found" is always explicit
rather than a silent empty value a caller might mistake for "nothing exists."
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _utc_now_iso() -> str:
    """Current time as a timezone-aware UTC ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def found(
    *,
    source_api: str,
    source_url: str,
    result: Any,
    query_echo: dict[str, Any],
    source_current_as_of: str | None = None,
    notice: str | None = None,
) -> dict[str, Any]:
    """Build a positive-result envelope.

    `source_current_as_of` is the source's own freshness date (e.g. eCFR's
    `up_to_date_as_of`) — distinct from `retrieved_at`, which is when *we*
    fetched it. Both feed the doctrinal-currency check.
    """
    return {
        "found": True,
        "source_api": source_api,
        "source_url": source_url,
        "retrieved_at": _utc_now_iso(),
        "source_current_as_of": source_current_as_of,
        "query_echo": query_echo,
        "result": result,
        "reason": None,
        "notice": notice,
    }


def not_found(
    *,
    source_api: str,
    source_url: str,
    reason: str,
    query_echo: dict[str, Any],
    notice: str | None = None,
) -> dict[str, Any]:
    """Build an explicit not-found / no-result envelope.

    Used for genuine "no matching record" *and* upstream errors. Either way the
    caller is told plainly, with the URL that was tried — never handed a guess.
    """
    return {
        "found": False,
        "source_api": source_api,
        "source_url": source_url,
        "retrieved_at": _utc_now_iso(),
        "source_current_as_of": None,
        "query_echo": query_echo,
        "result": None,
        "reason": reason,
        "notice": notice,
    }
