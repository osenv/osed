# OSED regulatory connector

A small local **MCP server** that feeds the OSED **Gap Analysis** agent verified
facts from federal regulatory sources. It does mechanical retrieval only — every
result is *evidence for a human to weigh*, never a determination. See the repo
[`DISCLAIMER.md`](../../DISCLAIMER.md) and [`CONNECTORS.md`](../../CONNECTORS.md).

- **Directory:** `connectors/regulatory/`
- **Distribution name:** `osed-connectors` · **import package:** `osed_connectors`
- **Transport:** local stdio (FastMCP). MCPB is the eventual packaging upgrade path.

## Phase 1 (this release) — keyless

The complete core deadline-suit loop, requiring **no API keys**:

| Tool | Question | Source |
|---|---|---|
| `get_current_regulation` | Does the rule exist now? | eCFR (daily-fresh) |
| `find_agency_actions` | Did the agency act, and when? | Federal Register |

**Phase 2** (not yet built) adds the bookends — GovInfo (US Code source text) and
Regulations.gov (delay timeline). Both need free keys; see [`.env.example`](.env.example).

## The tools

### `get_current_regulation(title, part, section=None)`
Current eCFR text for a CFR title/part (optionally a section). A not-found (HTTP
404) means no such codified text exists in the current edition — itself a useful
answer. `source_current_as_of` carries eCFR's own freshness date.

### `find_agency_actions(term, agency=None, doc_type=None, published_since=None, published_before=None, limit=10)`
Federal Register rules / proposed rules / notices matching `term`, newest first,
with publication and effective dates. `agency` is a Federal Register slug (e.g.
`environmental-protection-agency`); `doc_type` is `rule`, `proposed_rule`, or `notice`.

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
- **Currency applies to the duty, not just doctrine.** A regulation existing today does not confirm the underlying statutory duty is still in force; it can be amended or repealed by later statute.
- **Statutory deadline text** may live in uncodified statutory notes or public law rather than the codified US Code, and relative deadlines need the enactment date — scoped to phase 2 (GovInfo).
- **Regulations.gov comment dates** (phase 2) are raw evidence, not proof of agency action — they must never imply a "missed deadline" finding.

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

Live smoke tests hit the real Federal Register + eCFR APIs (no keys, so CI needs
no secrets). Phase-2 keyed tests will be gated behind env-var presence.
