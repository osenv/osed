# OSED regulatory connector

A small local **MCP server** that feeds the OSED **Gap Analysis** agent verified
facts from federal regulatory sources. It does mechanical retrieval only — every
result is *evidence for a human to weigh*, never a determination. See the repo
[`DISCLAIMER.md`](../../DISCLAIMER.md) and [`CONNECTORS.md`](../../CONNECTORS.md).

- **Directory:** `connectors/regulatory/`
- **Distribution name:** `osed-connectors` · **import package:** `osed_connectors`
- **Transport:** local stdio (FastMCP). MCPB is the eventual packaging upgrade path.

## The Gap Analysis + currency loop

Six tools: four for the deadline-suit analysis and two for the doctrinal-currency
check. Four are keyless; **two need a key** — Regulations.gov and CourtListener.
GovInfo US Code text is reached via the keyless link service.

| Tool | Question | Source | Key |
|---|---|---|---|
| `get_uscode_section` | What is the statutory duty? | GovInfo (US Code) | — |
| `get_current_regulation` | Does the rule exist now? | eCFR (daily-fresh) | — |
| `find_agency_actions` | Did the agency act, and when? | Federal Register | — |
| `find_rule_changes` | Did this rule change? (currency) | Federal Register | — |
| `find_rulemaking_documents` | Delay timeline (docket/comments) | Regulations.gov v4 | ✅ |
| `verify_citation` | Does this case citation resolve? (currency) | CourtListener | ✅ |

## The tools

### `get_uscode_section(title, section)`
Current US Code section text via GovInfo's keyless link service (e.g. title=42,
section="7409"). `source_current_as_of` is the annual edition year. A non-resolving
citation is an honest not-found. See the duty/deadline caveats under Known limits.

### `get_current_regulation(title, part, section=None)`
Current eCFR text for a CFR title/part (optionally a section). A not-found (HTTP
404) means no such codified text exists in the current edition — itself a useful
answer. `source_current_as_of` carries eCFR's own freshness date.

### `find_agency_actions(term, agency=None, doc_type=None, published_since=None, published_before=None, limit=10)`
Federal Register rules / proposed rules / notices matching `term`, newest first,
with publication and effective dates. `agency` is a Federal Register slug (e.g.
`environmental-protection-agency`); `doc_type` is `rule`, `proposed_rule`, or `notice`.

### `find_rulemaking_documents(term=None, agency=None, docket_id=None, document_type=None, posted_since=None, limit=10)`
Regulations.gov documents for the docket/comment timeline, oldest-first. Provide at
least one of `term`, `agency` (e.g. `EPA`), or `docket_id`. **Requires**
`REGULATIONS_GOV_API_KEY`; without it the tool returns an explicit not-found. The
key is sent in the `X-Api-Key` header, never in a URL.

### `find_rule_changes(cfr_title, cfr_part, since=None, limit=20)`
Federal Register actions affecting a CFR citation — the "did this rule change?"
step of a currency check. Returns later amendments, corrections, and agency notices
(including agency-announced stays) for the title/part, newest first, each tagged with
a `change_kind` and a `mentions_stay_or_vacatur` flag. This is **evidence** feeding the
CURRENT/CHANGED/DEAD/UNVERIFIED classification — it does not classify the rule, and it
does **not** capture judicial vacaturs or court-ordered stays (those are case law; use
`verify_citation` / CourtListener). Keyless.

### `verify_citation(text=None, volume=None, reporter=None, page=None)`
Verifies case citation(s) against CourtListener — the case half of a currency check.
Provide either `text` containing one or more citations, or an explicit
`volume`/`reporter`/`page`. Returns evidence per citation: whether it `resolved` to a
real published case, plus case name, date, precedential status, citation count, URL,
and subsequent-history fields. It does **not** say whether a case is still good law —
CourtListener does not flag overruling (Chevron still returns Published), so the
CURRENT/CHANGED/DEAD judgment stays the attorney's. A non-resolving citation is evidence
the cite may be wrong or fabricated. **Requires** `COURTLISTENER_API_KEY`; without it the
tool returns an explicit not-found. The token is sent in the `Authorization` header
(`Token …`), never in a URL.

## Tool-boundary safeguards

Every tool returns the same **evidence envelope**:

```json
{
  "found": true,
  "source_api": "ecfr",
  "source_url": "https://www.ecfr.gov/api/versioner/v1/full/2026-05-28/title-40.xml?part=50&section=50.1",
  "retrieved_at": "2026-05-29T18:42:01.123456+00:00",
  "source_current_as_of": "2026-05-28",
  "query_echo": { "title": 40, "part": "50", "section": "50.1" },
  "result": { "...": "..." },
  "reason": null,
  "notice": "eCFR is the unofficial, daily-updated edition ..."
}
```

- **Attribution on every result** — `source_url` + `retrieved_at` (UTC), so nothing is unattributable.
- **Honest not-found** — `found: false` with a `reason`, never a silent empty guess.
- **Currency support** — `source_current_as_of` plus retrieval date feed the doctrinal-currency check.
- **Host allowlist + timeouts** — the server can only reach the government APIs it is built for; no redirect-following.
- **Untrusted by default** — returned text is data for a human to weigh, not instructions.

### Known limits (surfaced, not papered over)
- **eCFR is unofficial.** Daily-fresh, but the legally operative text is the annual GPO CFR. Results say so in `notice`.
- **Currency applies to the duty, not just doctrine.** A regulation or duty existing today does not confirm it is still in force; it can be amended or repealed by later statute.
- **Statutory deadline text** may live in uncodified statutory notes or the public law rather than the codified US Code section, and relative deadlines ("within N years of enactment") need the enactment date. `get_uscode_section` returns the codified section and flags this in `notice`; it does not resolve it.
- **Regulations.gov comment dates** are raw evidence, not proof of agency action — they must never imply a "missed deadline" finding.

## Setup

```bash
cd connectors/regulatory
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Run

```bash
.venv/bin/osed-connectors        # console script (stdio)
# or
.venv/bin/python -m osed_connectors.server
```

### Register with Claude Code

Add to your project `.mcp.json` (use the absolute path to the venv script):

```json
{
  "mcpServers": {
    "osed-connectors": {
      "command": "/absolute/path/to/osed/connectors/regulatory/.venv/bin/osed-connectors"
    }
  }
}
```

## Test

```bash
.venv/bin/pytest                 # full suite, incl. live keyless smoke tests
.venv/bin/pytest -m "not live"   # offline only (no network)
```

Keyless live smoke tests hit the real Federal Register, eCFR, and GovInfo APIs
(no secrets, so CI runs them by default). The keyed live tests are gated on their
respective env vars — `REGULATIONS_GOV_API_KEY` (Regulations.gov) and
`COURTLISTENER_API_KEY` (CourtListener) — and skip when unset:

```bash
REGULATIONS_GOV_API_KEY=DEMO_KEY .venv/bin/pytest   # runs the Regulations.gov keyed test too
COURTLISTENER_API_KEY=… .venv/bin/pytest            # runs the CourtListener keyed test too
```
