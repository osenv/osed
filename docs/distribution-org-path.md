# Distribution: the organization / API-workspace path (scoping)

**Status:** scoping — not a build plan. **Audience:** OSED maintainers + a firm/clinic/org evaluating
a managed rollout. **Companion:** `docs/skills-in-cowork.md` (individual users), `connectors/regulatory/DEPLOY.md`.

> API details below move fast and use beta headers; treat versions/parameters as "verify before
> building." Where something needs confirmation it is marked **[verify]**.

---

## The question

How does a **firm, legal clinic, or organization** put OSED in front of *many* attorneys with
**central management** — one place to update skills, manage connectors and keys, and onboard people —
rather than every attorney hand-uploading zip files?

## Why claude.ai alone doesn't answer it

Custom **skills on claude.ai are per-user**: each member uploads the zips to their own account, and
there is **no admin "push to everyone."** Connectors *can* be managed org-wide on Team/Enterprise, but
the skills can't. So claude.ai gives you decentralized skills + (optionally) centralized connectors —
fine for a handful of people, not for a managed deployment.

The **Claude API workspace** is the surface that does support central skills.

---

## The API building blocks (what makes central distribution possible)

1. **Skills API — workspace-wide skills.** Upload a custom skill once via `POST /v1/skills`
   (beta `skills-2025-10-02`); it is **private to your workspace and available to every API key in
   it**. Versioned (`skills.versions.create`), ≤ 30 MB, same name/description limits as the zips. The
   Anthropic SDK takes a folder directly (`client.beta.skills.create(files=files_from_dir("skills/intake"))`).
   → *Update once, everyone gets the new version.* This is the central-distribution primitive.
2. **Skills run via the code-execution tool.** A Messages request references them in `container.skills`
   (`{type:"custom", skill_id, version}`), with `tools=[{type:"code_execution_20250825"}]` and betas
   `code-execution-2025-08-25,skills-2025-10-02`. Up to **8 skills per request** (OSED has 6 — fits).
3. **Remote MCP connectors give the skills their tools.** The skill *sandbox* has no outbound network,
   but the Messages API can attach **remote MCP servers** via the `mcp_servers` parameter
   (beta `mcp-client-2025-11-20`, by URL, with an `authorization_token`). That's how the hosted OSED
   regulatory connector (`connectors/regulatory/DEPLOY.md`) and CourtListener feed `gap-analysis`,
   `precedent-retrieval`, and `drafting`. **[verify]** that `container.skills` + `mcp_servers` compose
   in a single Messages request (both are top-level/well-documented features; confirm the combined call).

Put together: **one Messages API call** can carry the OSED skills *and* the live legal-data tools.

---

## Reference architecture (managed)

```
Attorney ──▶ OSED app (web UI, auth)
                 │  Messages API call:
                 │   • container.skills = [the 6 workspace skills]
                 │   • tools = [code_execution]
                 │   • mcp_servers = [osed-regulatory (hosted), courtlistener]
                 ▼
            Claude API (workspace)
                 │ tool calls ─▶ remote MCP connectors ─▶ gov APIs / CourtListener
                 ▼
            DRAFT instrument  ──▶  back to the attorney in the app UI
```

The org controls every box: the app, the workspace (skills + keys), and the connectors.

---

## Two org options

| | **Option A — lightweight org** | **Option B — managed product** |
|---|---|---|
| Plan/surface | Claude **Team/Enterprise** (claude.ai) | Claude **API workspace** + a hosted app |
| Skills | each member uploads the 6 zips once (onboarding step) | uploaded **once** to the workspace via Skills API |
| Connectors | admin deploys org-wide | attached per request via `mcp_servers` |
| User experience | the normal Claude app | a purpose-built OSED UI (no Claude setup) |
| Central control | connectors yes, skills no | **full** (skills, keys, connectors, UI) |
| Build effort | **low** (deploy connectors + write onboarding) | **medium–high** (build + operate an app) |
| Who's the data controller | Anthropic + each user's workspace | **you/the org** (you host the app + connectors) |

---

## What already exists vs. what's needed

**Exists:** the six skills (portable `SKILL.md`), the `pack-skills.mjs` bundles (Option A onboarding),
the regulatory connector now hostable as remote MCP (`connectors/regulatory/` + CI image), CourtListener
as a native remote MCP.

**Needed for Option B:** (1) a small **skills-publish script** (`POST /v1/skills` for each of the six —
the Skills-API analogue of `pack-skills.mjs`); (2) a **thin app/agent** that makes the combined
Messages call and renders the DRAFT, with auth and the matter intake; (3) ops: API-key management,
the hosted connectors, logging/retention policy, cost monitoring.

---

## Privacy, safety, compliance (non-negotiable for a legal tool)

- **You become the data controller.** A hosted app + connectors sees every attorney's matter and
  queries. Define retention, access control, and tenancy *before* onboarding anyone real.
- **Skills are not ZDR-eligible** — factor that into any confidentiality commitment.
- **The safeguards must live in the app, not just the skills.** The UI has to preserve the **DRAFT**
  banner, the inline **[⚠ ATTORNEY]** flags, "OSED drafts; an attorney decides," and the no-verdict
  rule. A clean product UI must not paper over the invariants the skills enforce — re-assert them at
  the app layer (and keep `evals/` in the loop).
- **Per-tenant key isolation.** If OSED hosts for multiple firms, isolate keys/connectors per tenant so
  one firm's matters and quota never touch another's.

---

## Recommendation — phase it

- **Phase 0 (today):** individuals on Cowork via `docs/skills-in-cowork.md`. Works now.
- **Phase 1 (Option A):** for an org that wants in this quarter — Team/Enterprise, deploy the two
  connectors org-wide, ship a 10-minute onboarding that uploads the six zips. Low effort, real value.
- **Phase 2 (Option B):** when demand justifies a product — API workspace + the skills-publish script +
  a thin OSED app. This is the only path to *true* one-click-for-everyone, and the only one where OSED
  fully controls the data posture.

Start gathering the Phase-2 inputs now (a firm design partner, the data-controller/retention decision,
a cost model), because those — not the code — are the long poles.

---

## Open questions to resolve before building Option B

1. **[verify]** `container.skills` + `mcp_servers` in one Messages request — confirm the combined call
   and current beta headers (`skills-2025-10-02`, `code-execution-2025-08-25`, `mcp-client-2025-11-20`).
2. Pricing model — Claude API usage + code-execution + connector calls, per matter; who pays.
3. Whether Anthropic ships **centrally-managed skills on Enterprise claude.ai** (would shrink Option B).
4. Tenancy: single shared workspace vs. one workspace per firm.
5. The data-controller / retention / confidentiality commitment OSED is willing to make.
