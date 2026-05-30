# WI-2 — Currency Automation: Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-05-30 · **Branch:** `wi-2-currency-automation` (off `main`, WI-1 merged)
**Implements:** WI-2 of `docs/plans/derisking-structural-pass.md` · **Protects:** invariant 3 (doctrinal currency)

> This is a design spec, not a plan. It records the validated design and the decisions made
> during brainstorming, as input to `writing-plans`. It changes no design invariant.

## Goal

Close the gap between "we *tell* the agent to run a currency check every time" and "here is the
**tool call** that does it." Today each skill's currency step is prose-only agent judgment; no
tool is named or required. WI-2 makes the currency check **tool-backed and required**, and proves
it with an eval — for both halves of the problem:

- **Rules / regulations** — a new Federal Register tool surfaces later amendments, corrections, and
  agency-announced stays affecting a cited rule.
- **Cases / doctrines** — a new CourtListener tool verifies a citation resolves to a real case and
  returns its subsequent-history evidence (the highest-stakes half: `doctrinal-currency.md` is
  mostly about cases — *Chevron* → *Loper Bright*).

**The load-bearing principle:** every tool **feeds** the CURRENT / CHANGED / DEAD / UNVERIFIED
classification; none **makes** it. Classification stays a human/agent judgment. A tool that emitted
a "DEAD/CURRENT" verdict would invite the agent to outsource judgment — the opposite of the goal.

## Decisions resolved during brainstorming

1. **Branch:** WI-1 merged (PR #1); WI-2 starts on a fresh branch off `main`.
2. **Required currency step is tool-agnostic in spirit, concrete in naming:** skills require a
   per-authority currency signal from a verification tool (named per authority type), and flag any
   authority that could not be tool-verified. The eval checks the **output** carries classifications
   and flags — not that a specific tool was literally invoked.
3. **Federal Register tool is CFR-citation keyed** (`find_rule_changes(cfr_title, cfr_part, since)`),
   evidence-only. (Verified live: `40 CFR 423` → 22 affecting documents.)
4. **Add a thin CourtListener `verify_citation` client** (one endpoint), evidence-only. The spike
   showed citation-lookup confirms a cite resolves and returns rich metadata, but does **not** flag
   overruling (*Chevron* returns `precedential_status: "Published"`, no negative-treatment signal) —
   so it is honestly an *existence + subsequent-history evidence* tool, not an "is-it-good-law"
   oracle. This is a scoped, documented refinement of `CONNECTORS.md` ("verification ≠ retrieval";
   we are not building case-law search).

## Component 1a — `find_rule_changes` (Federal Register)

**Files:** extend `connectors/regulatory/src/osed_connectors/clients/federal_register.py`; register a
tool in `server.py`; tests in `tests/test_federal_register.py` + `tests/test_smoke_live.py`.

**Naming convention** (matches existing `search_actions` → tool `find_agency_actions`): the client
function is `search_rule_changes(...)`; the agent-facing MCP tool registered in `server.py` is
`find_rule_changes`.

**Interface:**
```python
def search_rule_changes(*, cfr_title: int | str, cfr_part: int | str,
                        since: str | None = None, limit: int = 20,
                        transport=None) -> dict  # evidence envelope
```
**Query:** `GET https://www.federalregister.gov/api/v1/documents.json` with
`conditions[cfr][title]`, `conditions[cfr][part]`, `order=newest`, optional
`conditions[publication_date][gte]=since`, reusing the existing `_FIELDS` projection and the
`per_page` floor.

**Normalization:** each document tagged with a **descriptive** `change_kind` derived from the FR
`type` — `RULE → "amendment_or_final_rule"`, `PRORULE → "proposed_change"`, `NOTICE → "notice"` —
plus `mentions_stay_or_vacatur: bool` when the title/abstract contains `stay`, `vacat`, or `remand`
(case-insensitive). These are descriptions of the evidence, not currency verdicts.

**Envelope:** standard `found`/`not_found`. `result = {cfr_citation, count, returned, changes: [...]}`.
Zero results → explicit `not_found` (no later FR action found is itself meaningful evidence, stated
honestly — not proof the rule is unchanged).

**Notice (honest-limit, baked into the envelope):**
> "Evidence of Federal Register actions affecting this CFR citation — amendments, corrections, and
> agency notices (including agency-announced stays). This is NOT a currency determination, and it
> does NOT capture **judicial** vacaturs or court-ordered stays, which are court actions found in
> case law (e.g., CourtListener), sometimes with a lagging FR notice. Classifying the rule CURRENT /
> CHANGED / DEAD / UNVERIFIED is a judgment for a licensed attorney."

## Component 1b — `verify_citation` (CourtListener)

**Files:** new `connectors/regulatory/src/osed_connectors/clients/courtlistener.py`; register a tool
in `server.py`; new `tests/test_courtlistener.py`; keyed live test gated in `tests/test_smoke_live.py`;
update `.env.example`.

**Interface:**
```python
def verify_citation(*, text: str | None = None,
                    volume: str | None = None, reporter: str | None = None, page: str | None = None,
                    transport=None) -> dict  # evidence envelope
```
Accept either free `text` containing citations, or an explicit `volume`/`reporter`/`page`.

**Endpoint (from the spike):** `POST https://www.courtlistener.com/api/rest/v4/citation-lookup/`,
auth header `Authorization: Token <COURTLISTENER_API_KEY>` (header, never URL), form field `text`
(or volume/reporter/page). Returns a list of per-citation objects:
`{citation, normalized_citations, status, error_message, clusters: [...]}`. `status == 200` means
the cite **resolved**. Each cluster carries `case_name`, `date_filed`, `precedential_status`,
`citation_count`, `absolute_url`, and history fields (`history`, `procedural_history`, `disposition`).

**Normalization:** for each citation return `{citation, resolved: bool (status==200), case_name,
date_filed, court (from cluster), precedential_status, citation_count, absolute_url,
subsequent_history: {history, procedural_history, disposition}}`. A `resolved: false` is the
hallucinated/wrong-cite signal (serves invariant 4).

**Notice (honest-limit):**
> "Confirms whether a citation resolves to a real published case and returns its metadata and
> subsequent-history fields as evidence. It does NOT determine whether the case remains good law —
> CourtListener does not flag overruling or abrogation (e.g., *Chevron* still returns as Published).
> Whether a case is CURRENT / CHANGED / DEAD is a judgment for a licensed attorney reading the
> subsequent history. A non-resolving citation is evidence the cite may be wrong or fabricated."

**Rate limit:** free tier ~5/min, 50/hr, 125/day (per `CONNECTORS.md`). Keep keyed live tests to
1–2 calls, gated behind `COURTLISTENER_API_KEY` presence. The endpoint can be slow (504s observed);
use a longer per-request timeout (≈60s) than the default 15s.

## HTTP layer changes (`http.py`)

1. **Add `post()`** mirroring `get()` (allowlist + timeout + merged headers + `follow_redirects=False`),
   accepting a form `data` body and an optional `timeout` override (CL needs ~60s).
2. **Allowlist exception — add `www.courtlistener.com`** to `ALLOWED_HOSTS`. This is a deliberate,
   reviewed addition: CourtListener (Free Law Project) is the vetted first-party case-law source
   named in `CONNECTORS.md`, the key is the user's own, and it is reached directly (not via an
   untrusted third-party MCP). Update the module docstring: the allowlist covers "the government
   APIs and the one vetted first-party legal-data API (CourtListener) the connector is built for."
3. Optionally let `get()` take a `timeout` override too, for symmetry. (YAGNI unless needed.)

## Component 2 — Tool-backed required currency step (3 skills)

Upgrade the currency step in `skills/gap-analysis`, `skills/drafting`, `skills/precedent-retrieval`
from prose imperative to an explicit **required, tool-backed** step. Indicative wording (adapt to
each skill's voice and existing structure):

> **Currency check — required, tool-backed.** For every authority the output relies on, obtain a
> currency signal from a verification tool, **not from memory**:
> - **Cases / doctrines** → CourtListener `verify_citation` (does the cite resolve; subsequent
>   history) and, where connected, the CourtListener MCP.
> - **Regulations / rules** → the OSED regulatory connector: `get_current_regulation` (does the
>   text exist now) and `find_rule_changes` (later FR amendments / stays affecting the CFR citation).
> - **Statutes** → `get_uscode_section` (codified text); note uncodified deadlines may live in
>   statutory notes / public law.
>
> Classify each authority CURRENT / CHANGED / DEAD / UNVERIFIED per `docs/doctrinal-currency.md`.
> Any authority you could not verify with a tool is **UNVERIFIED → flag it**; never present an
> unchecked authority as good law on the basis of memory alone.

Add to each skill's "What you refuse to do": *"You do not present an authority as current on the
basis of memory alone; currency rests on a tool check or an explicit UNVERIFIED flag."*

**Invariant / marker preservation (critical):** these are instruction edits only. They change **no**
design invariant and **no output marker** WI-1 asserts on — the `Doctrinal-currency check: [PASS /
FLAGS]` and `Currency check:` header lines stay exactly as they are. The existing WI-1 suite must
remain green after the edits.

## Component 3 — WI-1 currency eval case

Add fixtures to `evals/` proving the behavioral requirement, following the WI-1 pattern (recorded
transcripts + checks; judge gated behind `live`):

- **Positive** (`drafting` or `gap-analysis`): cites an authority, reports a per-authority
  classification, and flags an unverifiable one → passes.
- **Negative** (recorded broken transcript): rests on an authority with **no** currency
  classification / presents unchecked law as good → suite goes **red** (the WI-1 negative-control
  pattern; reliable and deterministic, in CI).
- **Judge check** `currency-tool-backed` (gated): "Every authority the output relies on carries a
  CURRENT/CHANGED/DEAD/UNVERIFIED classification; any unverifiable authority is flagged; none is
  presented as current on memory alone."
- **Deterministic backstops:** the existing `Doctrinal-currency check:` / `Currency check:` header
  checks already in the WI-1 fixtures; optionally a `forbidden` check for blatant memory-claims is
  *not* added (too negation-sensitive — judge territory, per the WI-1 lesson).

## Testing strategy

- **Connectors:** transport-mocked unit tests for both new clients (zero-result → `not_found`;
  results → normalized + tagged; CL `status != 200` → `resolved: false`; allowlist rejection for a
  non-allowlisted host). Live smoke: `find_rule_changes` keyless (always runs, like existing FR
  smoke); `verify_citation` keyed, gated behind `COURTLISTENER_API_KEY` presence (1–2 calls).
- **Evals:** currency fixtures run deterministically in CI; the judge check is gated behind `-m live`.
- **Regression:** the full existing WI-1 eval suite and the existing connector suite must stay green.

## Security & secrets

- Keys live in `connectors/regulatory/.env` (gitignored, untracked — verified). `.env` is **not**
  present in this worktree; copy it locally from the main checkout for keyed testing (never commit).
- Add `COURTLISTENER_API_KEY` to `.env.example` (name + signup URL only, no value).
- Both keys travel in **headers** (`Authorization: Token …`, `X-Api-Key: …`), never in a URL, so
  they never land in an envelope's `source_url`.
- The allowlist addition is the only new outbound host; no third-party MCP dependency is introduced.

## Honest limits / out of scope

- **CourtListener does not detect overruling/abrogation** — `verify_citation` is existence +
  subsequent-history evidence, not a good-law verdict. Documented in the tool notice.
- **Judicial vacaturs/stays are not in the Federal Register** — `find_rule_changes` covers
  agency-published actions only. Documented in the tool notice.
- **The eval verifies output, not tool invocation** — it checks the output carries classifications
  and flags, not that a specific tool was called (markdown skills can't be made to *prove* a call).
- **The CourtListener MCP remains the richer path** when connected; `verify_citation` is the
  always-available verification primitive, not a replacement for case-law search.
- Existing connector limits carry over unchanged (eCFR unofficial; uncodified statutory notes;
  Regulations.gov comment dates are not agency-action proof).

## Open questions

None blocking. Minor, resolvable in planning: exact placement/wording of the currency step within
each skill's existing structure; which skill hosts the new eval fixtures (likely `drafting`, which
cites rules and cases).
