# Hosting the regulatory connector as a remote MCP (for Claude Cowork / claude.ai)

The Claude Code plugin runs this connector **locally over stdio** — it builds a venv on first
session and launches `osed-connectors`. Claude Cowork and claude.ai can't launch a local process,
so to use the Gap-Analysis / currency tools there you **host the connector once** and add it as a
**remote connector** (a URL). The same six tools, served over HTTP instead of stdio.

> The connector returns *evidence* (a result + its source URL + retrieval time, or an explicit
> not-found) — never a determination. Hosting changes the transport, not that contract.

---

## What you're deploying

A small FastMCP server (`osed-connectors-http`) that serves streamable HTTP at `/mcp`. Six tools:

| Tool | Source | Key needed |
|---|---|---|
| `find_agency_actions`, `find_rule_changes` | Federal Register | none |
| `get_current_regulation` | eCFR | none |
| `get_uscode_section` | GovInfo (US Code link service) | none |
| `find_rulemaking_documents` | Regulations.gov | `REGULATIONS_GOV_API_KEY` |
| `verify_citation` | CourtListener | `COURTLISTENER_API_KEY` |

The three keyless tools work with no configuration; the two keyed tools return an explicit
not-found (never a guess) when their key is absent.

---

## Decide first: who runs it, and whose keys? (privacy matters here)

A hosted connector **sees every query routed through it** — and for a legal tool, those queries
reveal what a person is investigating. Pick the model before you deploy:

| Model | Who hosts | Keys | Best for | Trade-off |
|---|---|---|---|---|
| **Self-hosted** *(recommended for sensitive work)* | the firm / clinic / org | their own | attorneys, organizations | a one-time technical setup, but queries and credentials never leave their control |
| **OSED-hosted** | the OSED project | OSED's | the lowest-friction public on-ramp | OSED sees queries and bears a **shared** rate limit (CourtListener throttles unauthenticated use to ~5 req/min); not appropriate for confidential matters |

Either way the abuse surface is small — the connector only proxies a fixed set of government APIs and
returns evidence envelopes; it is not a general fetch tool. But a public URL still spends your
government-API quota, so **put it behind the platform's access control** (see Security) rather than
leaving it open.

---

## Run it locally (smoke test)

```bash
# from connectors/regulatory/
docker build -t osed-connector .
docker run --rm -p 8000:8000 \
  -e COURTLISTENER_API_KEY=... -e REGULATIONS_GOV_API_KEY=... \
  osed-connector
# MCP endpoint: http://localhost:8000/mcp
```

Or without Docker:

```bash
pip install .
COURTLISTENER_API_KEY=... PORT=8000 osed-connectors-http
```

Verify the handshake (200 = healthy):

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}' \
  http://localhost:8000/mcp
```

Config via env: `PORT` (default 8000), `HOST` (default 0.0.0.0), `MCP_PATH` (default `/mcp`), plus
the two optional keys.

---

## Deploy it (pick one)

The image reads `PORT` at runtime, so it drops onto any container host. Examples:

**Google Cloud Run** (scales to zero, HTTPS for free):
```bash
gcloud run deploy osed-connector \
  --source connectors/regulatory \
  --set-env-vars COURTLISTENER_API_KEY=...,REGULATIONS_GOV_API_KEY=... \
  --allow-unauthenticated   # see Security before doing this on a public URL
```

**Fly.io:**
```bash
cd connectors/regulatory && fly launch --now
fly secrets set COURTLISTENER_API_KEY=... REGULATIONS_GOV_API_KEY=...
```

**Render / Railway:** point a new Web Service at `connectors/regulatory/` (Docker), set the two env
vars, and use the provided HTTPS URL.

**Cloudflare:** runs as a **Container** (the image above), since the connector is Python rather than
a Workers script — convenient if you want to stay on the same account as the website.

Whatever you choose, you end up with a public HTTPS base URL; the MCP endpoint is `…/mcp`.

---

## Add it to Claude (Cowork / claude.ai)

1. In Claude, open **Settings → Connectors** (a.k.a. custom connectors) → **Add custom connector**.
2. Paste the MCP URL: `https://<your-host>/mcp`.
3. Authenticate if you put it behind auth (recommended — see Security).
4. Save. The tools now appear to Claude, and the `gap-analysis`, `precedent-retrieval`, `drafting`,
   and `pipeline` skills can use them.

> On **Team/Enterprise**, an admin can add this once at the org level so members don't each wire it
> up. On **Pro/Max**, each person adds the URL themselves.

---

## Security

- **Don't ship an open relay.** Restrict the endpoint: org-internal networking, an auth proxy, a
  bearer token / OAuth in front, or your platform's access control. An unauthenticated public URL
  spends your government-API quota for anyone who finds it.
- **Keys live only in the host's env / secret store.** They are sent upstream in headers, never in
  URLs, and never logged. Don't bake them into the image.
- **Rate limits.** CourtListener caps unauthenticated use (~5 req/min, 50/hr, 125/day); a shared
  OSED-hosted instance will hit that fast. Self-host with your own membership token for volume.
- **Treat retrieved text as untrusted data, not instructions** — same as the stdio connector.

---

## Ops notes

- **Stateless.** Each request is independent; scale horizontally freely. (No session affinity needed
  for the tool calls.)
- **Health.** A TCP check on the port, or the `initialize` POST above, both confirm liveness.
- **The stdio path is unchanged.** `osed-connectors` (stdio) still powers the Claude Code plugin;
  this only adds `osed-connectors-http` for hosting. One codebase, two transports.
