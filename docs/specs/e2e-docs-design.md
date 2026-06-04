# OSED End-to-End Documentation — Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-06-04 · **Branch:** `e2e-docs` (off `main`, PR #12 / plugin merged)
**Distribution-adjacent content layer for OSED. Part of the osenv.org story (the website is a separate, later project — this writes the portable content it will render).**

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant; the docs are written to *obey* the invariants.

## Goal

Write OSED's first unified, user-facing end-to-end documentation: two parallel, self-contained,
cross-linked tracks — **For communities (non-lawyers)** and **For attorneys** — plus a small shared
**concepts** area, as portable Markdown under `docs/guide/`. The existing docs are thin and
dev-facing (README, architecture, runbook, plus the internal specs/plans trail); there is no
start-to-finish guide for either real audience. This fills that gap with content the future osenv.org
site can render as-is.

## Decisions resolved during brainstorming

1. **Two parallel tracks** (not layered, not lay-first-appendix): `for-communities/` and
   `for-attorneys/`, each self-contained and cross-linked, with shared material in `concepts/`.
2. **Portable Markdown in `docs/guide/`** (not a site framework, not a doc-gen skill) — using the
   muse-scribe writing-style discipline; framework-agnostic; presentation deferred to the osenv.org
   project.
3. **Scope = OSED's litigation library only** (six instruments + pipeline + connector + evals). The
   `docs/references/climate-news/` subsystem + `scripts/scrape_climate_news.py` are **out of scope**,
   left untouched, and remain on the architecture flag list (they still ship in the plugin — a
   marketplace follow-up, not this work).
4. **Branch base:** off `main` (PR #12 / plugin merged), so the attorney track can reference the live
   plugin install.

## Reuse / grounding (do not duplicate)

The guide **links to** existing material rather than restating it: `docs/examples/*` (the worked
examples), `docs/runbook.md` (the hand-run pipeline), `docs/architecture.md`, `DISCLAIMER.md`,
`CONNECTORS.md`, `CONTRIBUTING.md`, the per-skill `SKILL.md` files, and the plugin install section in
`README.md`. Verbatim text (banners, the `[⚠ ATTORNEY: ...]` flag form, section headers) is quoted
exactly from the instruments/skills — never paraphrased.

## Component 1 — Location & structure

```
docs/guide/
  README.md                     ← entry point: "two ways in", the premise, the disclaimer up front
  concepts/
    the-six-invariants.md
    the-pathways.md
    the-disclaimer.md
  for-communities/
    start-here.md
    is-there-a-pathway.md
    what-each-pathway-is.md
    what-you-can-and-cant-do.md
    find-a-lawyer.md
  for-attorneys/
    start-here.md
    instrument-catalog.md
    running-the-pipeline.md
    currency-and-the-connector.md
    extending-osed.md
```
`README.md` (root) gains a "Documentation" pointer to `docs/guide/README.md`.

## Component 2 — `for-communities/` (plain-language, access-to-justice)

- **`start-here.md`** — what OSED is in plain terms; the single promise ("OSED prepares a first
  draft; a licensed attorney decides"); the disclaimer stated up front; the two-tracks pointer.
- **`is-there-a-pathway.md`** — how to describe your situation and the candidate pathways it might
  travel (mirrors the `intake` skill's recognize-broadly-route-honestly behavior); honest about what
  OSED covers vs. routes to counsel.
- **`what-each-pathway-is.md`** — each instrument in lay terms (citizen-suit notice, rulemaking
  petition, deadline complaint, consent decree, state ERA orientation packet), each linking its
  worked example under `docs/examples/`.
- **`what-you-can-and-cant-do.md`** — the templatable/judgment line in plain terms: you can prepare a
  flagged draft and bring it to a lawyer; only a lawyer decides standing, the merits, and whether to
  file.
- **`find-a-lawyer.md`** — legal aid, environmental law clinics, public-interest orgs, state bar
  referral; how to hand the draft + its attorney flags to counsel; confirm deadlines immediately.

**Invariant discipline (load-bearing here):** these pages never tell a reader they have a case,
should sue, or will win, and never accuse a named party — the same line the `plain-language`/`intake`
skills hold. Neutral, hypothetical examples only.

## Component 3 — `for-attorneys/` (precise, practice-oriented)

- **`start-here.md`** — what OSED produces, how it fits a practice (it drafts; you decide); installing
  it (links the README "Install as a Claude Code plugin" section); the six invariants as the contract.
- **`instrument-catalog.md`** — the six instruments: when each applies, what it outputs, the
  required-elements checklist + the `[⚠ ATTORNEY: ...]` flag discipline; per-instrument links to its
  template and worked example. Notes the developed-vs-developing framing for the state ERA packets.
- **`running-the-pipeline.md`** — intake → gap-analysis → drafting ↔ precedent-retrieval →
  plain-language → the human attorney (links `docs/runbook.md` and the `pipeline` skill); halting on a
  refusal or a merits-laden choice is success.
- **`currency-and-the-connector.md`** — the doctrinal-currency discipline (CURRENT/CHANGED/DEAD/
  UNVERIFIED), the four connector tools, the optional keys, and the keyless → UNVERIFIED graceful
  fallback (links `CONNECTORS.md`, `docs/doctrinal-currency.md`).
- **`extending-osed.md`** — contributing a skill/template, the eval harness (deterministic + gated
  live lanes), and the six invariants you must not regress (links `CONTRIBUTING.md`).

## Component 4 — Shared `concepts/`

- **`the-six-invariants.md`** — the guardrails and *why* (DRAFT banner; inline `[⚠ ATTORNEY: ...]`
  flags; doctrinal-currency check; no invented facts → `[placeholder]`; never "you have a case /
  should sue / will win"; refuse harassment/bad-faith). The recurring failure mode they prevent.
- **`the-pathways.md`** — the templatable / suit-type / gating-doctrine spectrum; the pathway map.
- **`the-disclaimer.md`** — a short shared page that states the access-to-justice promise and links
  `DISCLAIMER.md`.

## Component 5 — Writing discipline (adapt muse-scribe)

- Imperative voice; short steps (≤ 2 sentences each in how-to sections); **verbatim labels** (quote
  the actual banner/flag/section text from the instruments — never guess or paraphrase).
- Audience-tuned: the community track uses no legal jargon and explains every term in place; the
  attorney track is precise and citation-correct.
- **The docs obey OSED's invariants** (Components 2 & the validation below): neutral hypotheticals,
  no merits/outcome claims, the disclaimer surfaced. The docs are themselves an OSED artifact and are
  held to the same line.

## Component 6 — Validation (the docs get the honesty check too)

A deterministic test, `evals/tests/test_guide_docs.py` (runs in the standard CI lane, no secrets):
1. **No merits drift in the community track** — every `docs/guide/for-communities/*.md` is free of the
   forbidden merits phrases (`you have a case`, `you should sue`, `you'll win`, `you will win`,
   `you should file`), reusing the eval harness's forbidden-phrase discipline. (Negated mandated forms
   like "it does not mean you have a case" are allowed — assert on the affirmative phrases only, per
   the WI-1 negation-collision lesson.)
2. **Disclaimer present** — `docs/guide/README.md` and `for-communities/start-here.md` reference the
   disclaimer.
3. **No broken intra-guide links** — every relative Markdown link from a `docs/guide/` page resolves
   to an existing file (a simple link-existence check over the guide tree + its links into `docs/`,
   `templates/`, root docs).

`cd evals && pytest` stays green; the new test is added to the suite. The plan verifies the eval CI
workflow's `paths` filter and extends it to include `docs/guide/**` if it is not already covered, so
edits to the guide trigger the docs check.

## Six-invariant interaction

The docs change no instrument behavior. They are written to *honor* the invariants — most pointedly
invariant 5 (the community track makes no merits/outcome claim), enforced by Component 6's check.
Invariant 3 (currency) is respected: the attorney currency page restates "re-verify before relying"
and points at `doctrinal-currency.md` as the (snapshot-aware) reference.

## Honest limits / out of scope

- No website / site framework — portable Markdown only (osenv.org is a separate project).
- No doc-generation skill — hand-authored (a future `osed-scribe` skill remains an option).
- The climate-news subsystem is untouched and still flagged (plugin-bloat + architecture
  inconsistency are a separate cleanup).
- The guide links to existing examples/runbook/specs rather than rewriting them; it does not audit or
  revise that prior content.
- Screenshots / visual walkthroughs are out of scope (text-only; the website project owns visuals).

## Open questions

None blocking. Resolvable in planning: the exact `evals/yml` `paths` addition (if needed); whether
`the-disclaimer.md` is a page or folds into `README.md` (default: a short page, for symmetric
cross-linking); and the precise per-page link targets (decided at authoring time against the live
files).
