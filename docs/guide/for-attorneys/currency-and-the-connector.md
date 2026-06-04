# Currency and the connector

Law changes underneath you, and an instrument drafted confidently on law that has shifted is the
most expensive kind of error — polished, authoritative-looking, and wrong (*Loper Bright* ending
Chevron deference in 2024; *Seven County* narrowing NEPA review in 2025 are the live reminders).
OSED's defense is the doctrinal-currency discipline, backed by a thin regulatory connector.

## The classification

Every statute, regulation, or doctrine an instrument relies on is classified — and OSED relies only
on **CURRENT**, flagging the rest:

- **CURRENT** — confirmed in force and not narrowed in a way that matters here.
- **CHANGED** — still exists but narrowed, amended, or stayed; explain how and whether it still
  supports the instrument.
- **DEAD** — overruled, vacated, or superseded; do not rely on it.
- **UNVERIFIED** — currency could not be confirmed from available sources.

When in doubt, flag rather than assume. "I could not confirm this is current" is always a safe
output; "this is the law" about something unchecked is never. Full discipline:
[`../../doctrinal-currency.md`](../../doctrinal-currency.md).

## The connector tools

The `osed-regulatory` MCP server feeds this check with **evidence**, never a conclusion. Each tool
returns a uniform envelope — `found`, `result`, `source_url`, `source_api`, `retrieved_at`, and a
`source_current_as_of` freshness signal; `found: false` is explicit, never an empty guess.

**Keyless (work immediately):**

- `find_agency_actions` — Federal Register: *did the agency act, and when?* (evidence a document
  published on a date, not proof a duty was met or missed).
- `find_rule_changes` — Federal Register: *did this rule change?* — later amendments, corrections,
  and agency-announced stays for a CFR title/part (does **not** capture judicial vacaturs).
- `get_current_regulation` — eCFR: *does the rule exist now?* (eCFR is the **unofficial** daily
  edition; the legally operative text is the annual GPO CFR — tagged accordingly).
- `get_uscode_section` — GovInfo: the statutory-duty text (a deadline may live in uncodified notes
  or public law, and a relative deadline needs the enactment date).

**Keyed (free API keys, both optional):**

- `verify_citation` — CourtListener: the case half of the check. Returns whether a citation resolves
  to a real published case; it does **not** flag overruling (Chevron still returns Published), so the
  CURRENT/CHANGED/DEAD judgment stays yours. Needs `COURTLISTENER_API_KEY`.
- `find_rulemaking_documents` — Regulations.gov: a docket/delay timeline. Posting and comment-period
  dates are raw evidence of activity — **never** read a comment-period close as a missed deadline.
  Needs `REGULATIONS_GOV_API_KEY`.

## Keyless degradation, and the snapshot caveat

Without the keys (or without `python3`), the skills **degrade safely** — they flag authorities
**UNVERIFIED** rather than guessing, and the setup step prints a visible message so you know the
connector is unavailable. And the bundled `docs/doctrinal-currency.md` anchors are a snapshot **as of
the installed plugin version**: run `/plugin marketplace update` to refresh them, and re-verify any
authority in primary sources before relying on it. A stamp records that a human checked; it is never
a substitute for checking. See [`../../../CONNECTORS.md`](../../../CONNECTORS.md) for the full
data-source map and the connector's known limits.
