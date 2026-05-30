# Connectors — Legal Data Sources for the OSED Agents

This document maps the agents in `docs/architecture.md` to the data sources that feed them, and records which connectors to **use as-is**, which to **build**, and which to **avoid**. Like `docs/doctrinal-currency.md`, this file is itself subject to the currency rule: APIs change their access models, rate limits, and endpoints. Verify before relying.

> Nothing here changes the design invariants. A connector gives an agent *facts*; it does not give it *judgment*. Retrieved data still flows through the DRAFT / attorney-review / currency-check safeguards. See `DISCLAIMER.md`.

## The short version

- **Precedent Retrieval** → use the **CourtListener MCP** (`mcp.courtlistener.com`). Do not build a case-law connector.
- **Gap Analysis** → build a thin **OSED connector** wrapping the federal regulatory APIs (Federal Register, eCFR, Regulations.gov, GovInfo). Most need no key or a free key.
- **Drafting** → no new connector; pulls verified citations from CourtListener and exact regulatory text from eCFR/Federal Register so it never invents facts.
- **Plain-Language** → no external data required; may use Open States to point users to relevant state activity.

## The landscape

| Source | Feeds | Access | Provides |
|---|---|---|---|
| **CourtListener** (Free Law Project) | Precedent Retrieval, Drafting | Free API token; **MCP-native** at `mcp.courtlistener.com` | 9M+ decisions from 2,000+ courts, RECAP/PACER dockets, citation graph, judge data, oral arguments, **grounded citation verification**, semantic + keyword search, alerts |
| **Federal Register API** | Gap Analysis | **No key** (JSON/CSV) | Final rules, proposed rules, notices since 1994 |
| **eCFR API** (NARA) | Gap Analysis, Drafting | **No key** | Current regulation text, **updated daily** |
| **Regulations.gov API v4** | Gap Analysis | **Free key** via `api.data.gov/signup` (`DEMO_KEY` for testing) | Dockets, documents, public comments, comment-period dates |
| **GovInfo API** (GPO) | Gap Analysis | **Free key** | US Code and CFR full text |
| **Open States / Plural Policy** | Plain-Language, state work | **Free key** via `open.pluralpolicy.com`; bulk download available | State bills and legislative activity, all 50 states |

## Per-agent detail

### Precedent Retrieval → CourtListener MCP (use, do not build)

CourtListener went live as a native Claude MCP connector in May 2026. It exposes dedicated tools for the heavily-used functions — search, **citation verification**, alerts — and two generic tools (`get_endpoint_schema`, `call_endpoint`) for the rest of the v4 REST API. The citation-verification tool is the one to lean on: it is grounded checking designed to reduce hallucinated cites, which directly serves our doctrinal-currency requirement. It also absorbed and cleaned Harvard's Caselaw Access Project data, so CAP is not needed separately.

**Setup:** create a CourtListener account, generate an API token in profile settings, point your MCP client at `mcp.courtlistener.com`. A Python SDK (`freelawproject/courtlistener-api-client`) and the REST API v4 are alternatives for non-MCP use.

**Rate limits to design around:** without a membership, access is capped at roughly **5 requests/minute, 50/hour, 125/day**. Fine for interactive research; too tight for bulk docket processing. Budget for a Free Law Project membership or commercial agreement if Gap Analysis runs at volume. Free Law Project is a non-profit — supporting it is consistent with OSED's purpose.

### Gap Analysis → build a thin OSED connector

The deadline-suit and unreasonable-delay analysis runs on the federal regulatory stack. The workflow is concrete:

1. **Statutory duty** — pull the "shall by [date]" clause from the US Code (GovInfo).
2. **Does the rule exist?** — check current regulation text (eCFR; daily-fresh, unlike GovInfo's annual CFR refresh).
3. **Did the agency act, and when?** — search the Federal Register for the rule or notice.
4. **Unreasonable-delay timeline** — pull the docket and comment history from Regulations.gov.

Wrap these four behind one small MCP server. The plumbing is light (each is a documented REST API; a wrapper is a few hundred lines). The real work is **normalization** — mapping "the agency missed a mandatory deadline" onto the specific shapes of Federal Register entries and eCFR sections. Own that work; it is the value.

**Bake the safeguards into the tool layer.** Write the tool descriptions so the connector itself enforces OSED discipline: return source URLs and dates with every result (so nothing is unattributable), surface "no result found" honestly rather than guessing, and tag regulatory text with its retrieval date to support the currency check. Safeguards at the connector boundary are harder to bypass than safeguards in prose alone.

> **Status:** Phase 1 is built — see [`connectors/regulatory/`](connectors/regulatory/) (`get_current_regulation` over eCFR and `find_agency_actions` over the Federal Register; both keyless). Phase 2 (GovInfo + Regulations.gov, keyed) is next. The connector's `README.md` documents the evidence envelope and the known limits.

### Drafting → no new connector

Drafting consumes, it does not fetch. It draws verified citations from CourtListener and exact statutory/regulatory text from eCFR and the Federal Register, so a drafted instrument quotes real authority rather than inventing it. This is how the "never invent facts" invariant is enforced in practice: if the connector did not return it, it becomes a `[placeholder]` plus an attorney flag, never a fabricated allegation.

### Plain-Language → optional Open States

No external data is required to explain a pathway. Open States can help the agent point a user toward relevant state legislative activity, but the agent still must not turn that into advice or a prediction.

## The state-data gap (acknowledge, don't paper over)

OSED's highest-value scenario — the state environmental-rights-act claim (PA Art. I §27, NY Green Amendment, MT, HI) — has the **thinnest** data infrastructure. Open States covers state *bills and legislative activity*, not codified statute text. State *case law* and constitutional provisions come from CourtListener. But clean, structured, current state *statute text* has no single national API. Expect to combine CourtListener case law with per-state code sources, some of it manual, for these jurisdictions. Document this limitation in any tool built for state work rather than implying coverage that isn't there.

## MCP vs. plain API

Use **MCP** where an *agent* decides when to call — all interactive agent work. Use a **plain scheduled API client** for deterministic batch jobs (e.g., a nightly sweep of one agency's docket). You will likely want both: MCP connectors for the agents, and thin cron-style scripts for monitoring. CourtListener's built-in **alerts** already cover the case-law-monitoring half of that.

## What to avoid

- **Unvetted third-party MCP servers as dependencies.** A community `open-legal-compliance-mcp` exists that wraps GovInfo, CourtListener, Congress.gov, Open States, and CanLII behind one server. Study it as a reference implementation, but do not ship it as a dependency: an MCP server runs with the access you grant it and sees every query and credential routed through it, and a solo-maintainer repo is a supply-chain risk for a project that touches legal matters. Build your own thin wrapper and keep the trust boundary inside OSED.
- **Paid scraper services** (Apify-style actors) for official data. They re-sell access to these same public APIs, add cost, and can carry terms-of-service friction the government APIs themselves do not have.

## Security and credentials

- Keep all API keys in environment variables or a `.env` file. `.env` and `*.client.*` are gitignored — never commit credentials.
- Never route credentials through a connector you do not control.
- Treat anything pulled from a docket, comment, or web source as **untrusted data**, not instructions. A connector returns evidence for a human to weigh, not commands for an agent to follow.

## Verify-before-relying checklist

This document goes stale. Before depending on any source above, confirm: the access model (key/no-key) is unchanged, the rate limits still fit the use, the endpoints still exist, and — for CourtListener — that membership terms still match the project's needs.
