# Using the OSED skills in Claude Cowork

This guide is for the people OSED is for — **attorneys and community members** — not developers. It
walks through getting the OSED skills working inside **Claude Cowork**, Anthropic's desktop "digital
coworker," so you can use OSED without ever touching Claude Code or a terminal.

> **The one thing to remember:** OSED *drafts*; a licensed attorney *decides*. Everything it produces
> is a marked **DRAFT** for a lawyer to review. It never tells you that you have a case or will win.

---

## What you'll have when you're done

You ask Claude, in plain English, things like *"the creek by us smells bad and the county keeps
approving permits — what can we do?"* and the OSED skills guide Claude to:

- **route** your situation to the legal pathways that might fit (intake),
- **compare** the public record to the law and look for missed deadlines (gap analysis),
- **draft** the actual instrument — a notice, petition, or comment letter (drafting),
- **check** how courts have read the authority (precedent retrieval),
- **translate** the result into plain language (plain-language),
- or run the **whole pipeline** end to end (pipeline).

---

## Before you start

1. **A paid Claude plan** — Pro, Max, Team, or Enterprise — with **code execution / file creation
   turned on**. (Free plans can't run custom skills.)
2. **The Claude desktop app**, where Cowork lives. Cowork is on all paid plans and runs on your
   computer, against your local files and folders.
3. **The OSED skill files** — six `.zip` files (next section).

---

## Step 1 — Get the OSED skill files

You need the six skill bundles:

```
intake.zip            gap-analysis.zip       drafting.zip
precedent-retrieval.zip   plain-language.zip   pipeline.zip
```

Download them from the OSED release page *(maintainers: see "Producing the bundles" at the bottom —
attach the zips to a GitHub Release so non-technical users get a plain download link)*. Each zip is a
self-contained skill: it already includes the document templates and reference notes it needs.

---

## Step 2 — Add the skills to Claude

Custom skills are added through **claude.ai settings**, and then become available to Claude —
including in Cowork — for your account.

1. Open **claude.ai → Settings → Features** (the "Skills" / "Capabilities" area).
2. Find **custom Skills** and choose **Upload Skill**.
3. Upload each `.zip` **one at a time** (one skill per file). Repeat for all six.
4. You should see all six listed: `intake`, `gap-analysis`, `drafting`, `precedent-retrieval`,
   `plain-language`, `pipeline`.

You don't "run" a skill by name; you describe your situation and Claude uses the matching skill.

> **Heads-up — skills are per-person and per-app.** On individual plans each user uploads the zips to
> their own account, and uploads don't sync between claude.ai, Cowork, the API, and Claude Code.
> (See "Which plan are you on" for teams, and `docs/distribution-org-path.md` for centralized rollout.)

---

## Step 3 — Connect the data sources (important)

A skill is a set of *instructions*; it still needs *tools* to fetch real records and verify real
citations. Two of the six work on instructions alone; four reach out to live legal data and **need
connectors**:

| Skill | Needs a data connector? | Without connectors |
|---|---|---|
| **intake** | No | ✅ Works fully — it routes, it doesn't fetch |
| **plain-language** | No | ✅ Works fully — it explains |
| **gap-analysis** | Yes — regulatory data | ⚠️ Limited: can't pull live statute/rule/docket data |
| **precedent-retrieval** | Yes — CourtListener | ⚠️ Limited: can't verify citations against real cases |
| **drafting** | Yes — both | ⚠️ Drafts, but unverified facts become flagged `[placeholders]` |
| **pipeline** | Yes — both | ⚠️ Runs, but the fetch/verify steps are limited |

So **intake** and **plain-language** give value with zero setup. To make the fetch-and-verify skills
fully real, add two connectors:

1. **CourtListener** (case law + citation verification) — available as a ready-made connector at
   `mcp.courtlistener.com`. Create a free CourtListener account, generate an API token, and add it as
   a connector in Claude. Powers **precedent-retrieval** and the citation half of **drafting**.
2. **The OSED regulatory connector** (Federal Register, eCFR, US Code, Regulations.gov). It's **hosted
   once as a remote connector**, then everyone adds it by URL — no software to run. A technical helper
   deploys it a single time (`connectors/regulatory/DEPLOY.md` walks through Cloud Run / Fly / Render /
   Cloudflare and the privacy choice of who hosts it); after that your attorneys just **add the
   connector by URL** (`https://<host>/mcp`). Powers **gap-analysis** and the statute/rule-text half of
   **drafting**.

   > **Privacy note:** a hosted connector sees the queries routed through it. For confidential matters,
   > a firm or clinic should **self-host** with its own keys (see `DEPLOY.md`) rather than route through
   > a shared public instance.

> Why not the raw Claude API for individuals? API-side skills run in a no-network sandbox, so the data
> skills can't reach Federal Register or CourtListener from the sandbox itself. Cowork/claude.ai (and,
> for orgs, the API *with remote MCP connectors*) is the right home — see `docs/distribution-org-path.md`.

---

## Step 4 — Use it

Describe your situation in your own words. Examples:

- *"Our air is bad near the refinery in [town]. Who do we complain to, and is there anything we can
  do?"* → **intake**.
- *"Walk me through whether EPA missed a mandatory deadline under [statute]."* → **gap-analysis**.
- *"Draft a Clean Water Act §505 notice of intent for this situation."* → **drafting** (a marked DRAFT
  with every judgment flagged for an attorney).
- *"Explain what a citizen-suit notice is and what it can and can't do, in plain English."* →
  **plain-language**.
- *"Take my situation through the whole process and assemble a package for my attorney."* →
  **pipeline**.

Everything comes back as a **DRAFT**. The last, non-negotiable step is always a licensed attorney.

---

## Which plan are you on? (distribution)

### Individual — Pro or Max
- Each person uploads the six zips to **their own** account (Step 2) and adds the connectors (Step 3).
- **To reach attorneys/laypeople:** give them one download (the six zips) plus this guide; pre-create a
  shared CourtListener token or a hosted OSED regulatory connector so they only paste a key.

### Organization — Team or Enterprise
- You get **central user management**, and **connectors can be administered org-wide**, so IT can
  deploy CourtListener + the OSED regulatory connector once for everyone.
- **Custom *skills* are still per-user on claude.ai** — there's no org-wide "push these six to
  everyone" button. For true centralized rollout (skills shared workspace-wide via the Skills API +
  a thin app attorneys log into), see **`docs/distribution-org-path.md`**.

---

## Limits worth naming honestly

- **OSED never decides the merits** — no "you have a case," no "you'll win," no naming a party as
  having broken the law. It identifies pathways and drafts instruments for a lawyer.
- **Deadlines are real and OSED does not track them.** Confirm any deadline with a lawyer immediately.
- **Currency.** "Resolves to a real case" ≠ "still good law." The attorney judges currency.
- **State statute text is thin** — the state environmental-rights-act pathways have the weakest data;
  expect more manual work and attorney involvement there.

---

## Producing the bundles (for maintainers)

```bash
node scripts/pack-skills.mjs      # → dist-skills/*.zip + dist-skills/MANIFEST.md
```

`scripts/pack-skills.mjs` reads each `skills/<name>/SKILL.md`, validates its frontmatter against
claude.ai's limits (name format, description ≤ 1024 chars), **vendors the `templates/` and `docs/`
files each skill references into that skill's zip** (so the bundle is self-contained once it leaves
this repo), and writes one `<name>.zip` per skill plus a `MANIFEST.md` of exactly what's in each.
Re-run whenever the skills or templates change, and attach the zips to a GitHub Release so this guide
has a stable download link to point at.
