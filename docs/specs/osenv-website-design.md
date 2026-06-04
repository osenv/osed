# osenv.org Website — Design Spec

**Date:** 2026-06-04 · **Status:** Approved (brainstorm complete) · **Next:** implementation plan
(`writing-plans`).

**Spec location note:** the `osenv` repo does not exist yet, so this founding spec lives in the
`osed` repo (matching its `docs/specs/` convention). The implementation plan's first task creates
the `osenv` repo and carries this spec over as the new project's genesis document.

---

## Goal

Build v1 of **osenv.org** — the public home for **osenv**, an umbrella organization for open-source
environmental projects — with **OSED** (Open Source Environmental Defense) as its first flagship
project. The site's primary job is to **recruit builders** for the umbrella vision: lead with the
vision (open environmental data → agents → proactive legal triggering), present OSED as living
proof, and ask visitors to build/collaborate. OSED's existing two-track guide (For communities /
For attorneys) ships inside the flagship section as the credibility proof and the path for real
users — present, but not the home page's headline.

## Decisions locked during brainstorming

| Decision | Choice |
|---|---|
| Scope of v1 | Umbrella shell **+** OSED flagship section, in one build |
| Repo & content | **New `osenv` repo**; OSED guide content single-sourced from the `osed` repo, synced at build |
| Primary job | **Recruit builders** for the vision (vision-forward home, "build with us" CTA) |
| Tech stack | **Astro + Tailwind + React islands** (Approach A) |
| Hosting | **Cloudflare Pages** (GitHub Pages = zero-cost fallback) |
| Content freshness | **Pin submodule + automated bump PR** (reproducible builds, human-in-the-loop updates) |
| Brand tone | Simple, restrained, civic; warm Flexoki paper-and-ink base |
| Palette | Flexoki, per-branch as a landscape: **earth / foliage / water** |
| Agent-era future | **Explicitly undecided** — the spec assumes nothing about it |

---

## 1. Architecture & repo structure

A new `osenv` repository; Astro + Tailwind + React islands; static output to Cloudflare Pages. The
`osed` repo is pulled in read-only as a pinned git submodule and is the single source of the OSED
guide content.

```
osenv/                          ← new repo, osenv.org
├── astro.config.mjs            ← Astro + Tailwind + MDX
├── package.json
├── src/
│   ├── layouts/                ← THIN .astro shells only (keeps a future Next migration mechanical)
│   ├── components/             ← React .tsx islands — the designed UI; claude.ai/design output lands here
│   ├── pages/
│   │   ├── index.astro         ← umbrella home (vision-forward, "build with us")
│   │   ├── about.astro         ← the umbrella vision in depth
│   │   └── projects/
│   │       ├── index.astro     ← project index (OSED + future-project slots)
│   │       └── osed/           ← OSED flagship: landing + guide
│   ├── content/
│   │   └── guide/              ← Astro content collection, written by the sync script (never hand-authored)
│   ├── data/
│   │   └── projects.ts         ← data-driven project list (adding project #2 = a data entry + folder)
│   └── styles/
├── vendor/osed/                ← git submodule of the osed repo, pinned to a commit
└── scripts/sync-guide.mjs      ← prebuild: vendor/osed/docs/guide → src/content/guide + link rewriting
```

**Three load-bearing choices:**
- **Submodule pinned to a commit** (not live-tracking) → reproducible builds; content changes only
  via a reviewable pin bump.
- **Thin `.astro`, fat `.tsx`** → all real UI is plain React, so a later Next.js migration (if the
  undecided agent-era ever demands it) is mechanical re-housing of routing/layout shells, ~1–3 days.
- **Sync script, never copy-paste** → the guide prose has exactly one home (the `osed` repo); osenv
  renders it, never re-authors it.

## 2. Sitemap & content model

Pages marked **[authored]** (new in osenv) or **[synced]** (rendered from the osed guide):

```
/                                          umbrella home — vision hero, architecture story,    [authored]
                                           OSED as proof, "build with us" CTA
/about                                     umbrella vision in depth                            [authored]
/projects                                  project index (OSED + future slots)                 [authored]
/projects/osed                             OSED flagship landing — what it is, the safeguards   [authored]
                                           (invariants, "it drafts; an attorney decides"),
                                           two doors into the guide + GitHub/install links
/projects/osed/guide                       guide entry (the two doors)                          [synced: guide/README]
/projects/osed/guide/for-communities/*     5 pages                                             [synced]
/projects/osed/guide/for-attorneys/*       5 pages                                             [synced]
/projects/osed/guide/concepts/*            3 pages                                             [synced]
```

- **Authored pages** = Astro pages composed of React components; the recruiting/vision design and
  claude.ai/design output live here.
- **Synced pages** = the 13 guide files rendered through one shared layout from the content
  collection; osenv chrome (nav/footer) around the osed repo's verbatim prose.
- **Extensible umbrella** — `/projects` is driven by `src/data/projects.ts`; project #2 is a data
  entry + a folder, not a re-architecture.

**v1 scope lines (decisions, not omissions):**
- OSED's worked examples, templates, runbook, and architecture docs are **not** rendered as site
  pages — the guide links to them on GitHub (canonical source). Rendering the whole repo is a v2
  question.
- **No blog/news and no search** in v1 — neither serves the "recruit builders" job on day one; both
  are clean Astro adds later.

## 3. Content sync & link rewriting (the anti-drift mechanism)

`scripts/sync-guide.mjs` runs as a prebuild step, reading the pinned submodule and writing the
content collection:

1. **Copy** `vendor/osed/docs/guide/**/*.md` → `src/content/guide/**`, preserving structure.
2. **Rewrite links** by category:
   - **Intra-guide** (e.g. `../concepts/the-pathways.md`) → site routes
     (`/projects/osed/guide/...`).
   - **Escapes the guide** (e.g. `../../../DISCLAIMER.md`, `../../examples/...`,
     `../../../templates/...`, `../../runbook.md`) → **absolute GitHub URLs at the pinned commit**
     (`github.com/<org>/osed/blob/<sha>/<path>`). Resolves, and points at canonical source.
   - **External** (`http(s)://`, `mailto:`) → untouched.
3. **Fail the build** on any link that matches no rule or whose target is absent in the submodule.
   Silent drift is the enemy; a broken sync stops the deploy.

**Why this is safe against drift:**
- The osed repo's `test_guide_docs.py` already guarantees the source links resolve and the community
  track stays merits-clean **before** content reaches osenv.
- osenv pins a specific osed commit, so a guide edit cannot silently change the live site — a human
  bumps the pin in a reviewable PR (see freshness, §5).
- The sync is **transform-only, never author** — osenv cannot introduce prose that contradicts the
  guide because it writes none. OSED's voice ("OSED drafts; a licensed attorney decides") stays
  intact under osenv framing; the disclaimer link survives and points to the real `DISCLAIMER.md`.

## 4. Brand & palette

Simple, restrained, civic. One typographic system; warm Flexoki paper-and-ink base everywhere, so
the site reads as one thing with the two audience branches **color-coded** as a natural landscape.

**Shared base (Flexoki):** paper `#FFFCF0`, ink/black `#100F0F`, `base-50…base-950` grays for
structure. Dark mode uses Flexoki's dark equivalents (paper↔black, accent `600`↔`400`).

**Accents — earth → foliage → water** (light `600` / dark `400`):

| Branch | Accent | In nature | Light `600` | Dark `400` |
|---|---|---|---|---|
| Umbrella (home/about/projects) | Orange (terracotta/clay) | earth / soil | `#BC5215` | `#DA702C` |
| For communities | Green (olive/moss) | foliage | `#66800B` | `#879A39` |
| For attorneys | Blue (slate) | water / sky (and a nod to the Clean Water Act) | `#205EA6` | `#4385BE` |

A reader always knows which branch they're in by color, but never feels they left the same site.
The umbrella's clay tone reads as the soil the projects grow from. (Yellow `#AD8301` was considered
for the umbrella but rejected: low contrast for UI text; better as a sparing highlight.)

**Fixed regardless of mockups** (so visual design can't drift from substance): the two-audience door
metaphor; the disclaimer always one click away; the six invariants presented as trust signals, not
fine print.

## 5. Build, deploy & testing

**Build pipeline (Cloudflare Pages):**
1. Checkout with `--recurse-submodules` (fetch the pinned osed content). **Required** — without it
   `vendor/osed/` is empty at build.
2. `scripts/sync-guide.mjs` — transform guide MD → content collection, rewrite links, **fail build
   on any unresolved/unmapped link**.
3. `astro build` → static output → Cloudflare Pages. `main` → production; PRs → preview URLs (handy
   for reviewing claude.ai/design components and submodule-bump PRs visually).

**Content freshness (pin + automated bump PR):** the submodule stays pinned. A scheduled CI job
(nightly fallback) and an optional **repository-dispatch from the osed repo on guide changes**
advance the submodule and open a reviewable PR against osenv ("bump osed guide to `<sha>`"). No
auto-`--remote` at build time — that would reintroduce silent drift. Updates are one-click and
reviewed; builds stay reproducible.

**Testing — proportionate to a static content site, echoing OSED's own honesty guards:**
- **Sync-script unit tests (Vitest)** — the link rewriter is the one piece of real logic: intra-guide
  → route, escape → GitHub-at-SHA, external → untouched, unknown/missing → throws.
- **Build-time link integrity** — the sync step is itself the guard (the osenv analog of
  `test_guide_docs.py`); a broken/unmapped link fails the build.
- **A11y / Lighthouse smoke** on the built home + one guide page (civic site → accessibility is
  substantive).
- **No heavy E2E in v1** — no interactive flows to drive yet.

**CI (GitHub Actions):** lint + sync-tests + `astro build` on every PR; plus the
scheduled/dispatch submodule-bump PR job.

## 6. The claude.ai/design hand-off

The user generates mockups in **claude.ai/design**; the spec carries the design brief and the loop.

**Brief (paste one screen at a time):**
- **Umbrella home** — vision hero ("open environmental data + agents, in service of the laws that
  already exist"), the architecture story as a simple diagram, OSED as living proof, a "build with
  us" CTA. Umbrella clay/earth accent.
- **OSED flagship landing** — what it is; the safeguards/invariants as a trust section; the two
  color-coded doors into the guide. Umbrella clay/earth chrome (it lives under `/projects`); the two
  door cards introduce the branch accents (green / blue).
- **Guide page template** — read-optimized layout shared by the 13 synced pages: generous type,
  clear nav between the two tracks, branch accent (green/blue), the DRAFT/disclaimer framing visible.

**Loop:** mock a screen → paste React/Tailwind back → adapt into a `.tsx` component wired to real
content. Recorded here so it isn't improvised.

## 7. Out of scope for v1 (named, so each is a decision)

Analytics, search, blog/news, i18n, rendering the non-guide repo docs, and anything agent-era. All
clean Astro adds later.

## 8. Open questions / future

- **Agent-era architecture is explicitly undecided.** No part of this spec assumes it. If osenv.org
  itself ever becomes a heavy authed app, the React components + Markdown content are already in a
  portable shape; the agent services would most likely be separate (e.g. Cloudflare Workers) that
  the site links to, not a rewrite of this site.
- **GitHub org / repo name** for `<org>` in the GitHub-at-SHA link rewriting — confirm at repo
  creation (the osed repo's current remote determines it).
- **Domain/DNS wiring** for osenv.org → Cloudflare Pages — an implementation-plan step.
