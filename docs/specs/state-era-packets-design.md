# State Environmental-Rights-Act (ERA) Claim Packets — Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-06-01 · **Branch:** `state-era-packets` (off `main`, through PR #10 / consent-decree scaffold merged)
**Implements:** Roadmap item 6 of `docs/architecture.md` ("State environmental-rights-act claim packet — per-state variants (PA Art. I §27, NY Green Amendment, MT, HI). High access-to-justice value; heavy Plain-Language involvement"). The **final** instrument on the roadmap.

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant; sharpens two (currency + no-overstatement) for state constitutional law.

## Goal

Add per-state **state ERA orientation packets** for the four roadmap states (PA, MT, NY, HI): a
plain-language-led orientation + claim scaffold that gets a layperson to the point where a state
attorney can take over. Unlike the five federal instruments (notice, petition, complaint, decree),
this is **state constitutional law** — no federal statute, no EPA, no federal court — and it is the
project's most volatile, most state-variable area. The packet's value is access-to-justice: making a
state environmental right legible and actionable without first proving the whole case.

## What is different about this instrument (and the two sharpened disciplines)

1. **It is not a court filing.** It is an orientation packet: the constitutional right, who can
   invoke it, the threshold a claim must meet, the forum, a plain-language explainer, and a handoff
   to state counsel. It never drafts a state-court complaint (that is per-state procedure for a
   licensed attorney).
2. **Currency is the central hazard.** State ERA doctrine moves fast and differs sharply by state.
   Every packet carries a **`Law-as-of:` stamp**; every state-specific case citation is
   `verify_citation`-confirmed at build; and the four ERAs are added to `doctrinal-currency.md`'s
   tracked "Worth tracking" anchors (WI-6 stamp format).
3. **No overstatement.** PA Art. I §27 and MT have **developed, citable** doctrine. NY's Green
   Amendment (ratified 2021) and HI Art. XI are **less settled**. Those packets must say *"this is
   developing law"* plainly and must never imply a settled standard. The plain-language no-merits
   discipline ("name the bar honestly"; never tell a reader they have a case) is load-bearing.

## Decisions resolved during brainstorming

1. **All four states** (PA, MT, NY, HI) — full roadmap coverage.
2. **Add state-ERA anchors** to `doctrinal-currency.md`'s tracked list (stamped, CHANGELOG'd,
   freshness test green) — the volatile doctrines come under the same discipline as the federal
   anchors.
3. **4 packets + 4 worked examples + 4 fixtures** — maximal coverage; each state demonstrated end to
   end.
4. **One branch / one PR**, with the plan phased by state (shared structure → PA → MT → NY → HI →
   anchors/docs → gate) so each state is independently reviewable.
5. **Branch base:** off `main` (PR #10 merged).

## Component 1 — The per-state packet structure (shared)

Each per-state file `templates/state-era-<st>.md` (`pa`, `mt`, `ny`, `hi`) follows one shared
structure, in OSED house style adapted to an orientation packet:

1. **Banner** — the exact phrase `ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE`; a licensed
   **[state]** attorney decides; points to `../DISCLAIMER.md`; carries a **`Law-as-of: <date>`**
   stamp line.
2. **The right** — the constitutional provision: a short quotation or close paraphrase + the exact
   citation (e.g., `Pa. Const. art. I, § 27`), and the **enforceability posture** (self-executing /
   public-trust / "as provided by law") `[⚠ ATTORNEY: confirm the provision text and its current
   enforceability posture in [state]]`.
3. **Who can invoke it / standing** in that state `[⚠ ATTORNEY: confirm who has standing under
   [state] law]`.
4. **The threshold — what a claim must show** — stated honestly: the access point where the bar is
   low; the harder elements where they exist. NY/HI carry an explicit **"this is developing law"**
   line `[⚠ ATTORNEY: the standard is unsettled / still developing — confirm the current state of
   the law before relying]`.
5. **Forum & posture** — state court; the kind of action (declaratory / injunctive against a state
   actor or agency) `[⚠ ATTORNEY: confirm forum, defendant, and procedure under [state] law]`.
6. **Plain-language explainer** — the access-to-justice core: the six plain-language section headers
   verbatim (`## What this is`, `## What it asks of you`, `## How high the bar is`, `## A plain
   example`, `## The clock`, `## Your next step`), lay-readable, neutral hypothetical, closing with
   the mandated reminder containing `it does not mean you have a case`.
7. **Currency note** — the `Law-as-of` stamp restated + "verify before relying; this doctrine is
   evolving" (emphatic for NY/HI).
8. **Consolidated attorney flags + counsel handoff** — every state-specific judgment flagged; hand
   off to a [state] environmental law clinic / legal aid / the state bar referral service.

The packet **never** tells a reader they have a case, names a party as having broken the law, or
predicts an outcome (invariant 5); every uncertain or state-specific point is an `[⚠ ATTORNEY: ...]`
flag or a `[placeholder]` (invariants 2, 4); every authority is currency-checked (invariant 3).

## Component 2 — The four states

- `templates/state-era-pa.md` — Pennsylvania, **Pa. Const. art. I, § 27** (the public-trust /
  Environmental Rights Amendment line; developed doctrine).
- `templates/state-era-mt.md` — Montana, **Mont. Const. art. II, § 3 & art. IX, § 1** (a robust,
  recently-tested ERA).
- `templates/state-era-ny.md` — New York, **N.Y. Const. art. I, § 19** (the Green Amendment, 2021;
  **developing law** — framed as such throughout).
- `templates/state-era-hi.md` — Hawaiʻi, **Haw. Const. art. XI, § 9** ("as provided by law";
  public-trust under art. XI; **developing law** — framed as such).

Every provision quotation/citation and every case cite is verified at build (primary source /
`verify_citation`). Where a current case cannot be `verify_citation`-confirmed, the packet states the
point as `[⚠ ATTORNEY: identify and verify the controlling [state] authority]` rather than asserting
an unverified case — exactly the WI-3 lesson.

## Component 3 — Skill wiring

- **`skills/drafting/SKILL.md`** — add an instrument-table row (orient a layperson to a state
  environmental-rights claim → State ERA orientation packet → `templates/state-era-<state>.md`), and
  a one-paragraph note that ERA packets are **orientation scaffolds, not court filings**:
  plain-language-led, state-law-specific, never asserting a settled standard or that the reader has a
  case.
- **`skills/intake/SKILL.md`** — the existing state-ERA row ("A state-constitutional right to a
  healthful environment | State environmental-rights act | state courts | Plain-Language + counsel")
  updates its OSED next step to name the packet: `Plain-Language → state-ERA packet → state counsel`.
- **`skills/plain-language/SKILL.md`** — already ERA-aware; add a one-line pointer to the per-state
  packets (light touch; no behavior change).

## Component 4 — Currency anchors (`docs/doctrinal-currency.md`)

Add four state-ERA anchors to the "## Worth tracking" list, each a bullet with a WI-6-format stamp
`(verified 2026-06-01; re-verify by 2026-09-01)`:
- PA Art. I §27 — the Environmental Rights Amendment / public-trust line.
- MT Art. II §3 & art. IX §1 — the state ERA.
- NY Art. I §19 — the Green Amendment (**developing**).
- HI Art. XI — the environmental-rights / public-trust provision (**developing**).

Stamp the four new anchors with their **actual** verification date (the build date the implementer
confirms each provision in primary sources). Do **not** bump the existing four federal anchors'
verified dates — a stamp asserts a human re-verified on that date, so the federal anchors keep their
`2026-05-31` stamps unless the implementer actually re-verifies them. Update the section's
`Law-as-of:` header to the date the list was last updated (the build date), which represents "this
list last changed on," with each anchor's own stamp remaining the authoritative per-anchor record.
Add a `CHANGELOG.md` entry, and keep `evals/tests/test_freshness.py` green (it is date-agnostic: it
requires every "Worth tracking" anchor bullet to carry a well-formed
`(verified YYYY-MM-DD; re-verify by YYYY-MM-DD)` stamp — four new stamped bullets pass).

## Component 5 — Four worked examples

`docs/examples/state-era-<state>.md` for PA, MT, NY, HI. Each runs the ERA pathway end to end for a
neutral public-interest scenario: a lay concern → **Intake** routing → **Plain-Language** orientation
→ the **packet** → **state counsel**. Heavy plain-language; neutral hypotheticals (never a real
named party accused); the closing no-merits reminder; every cite `verify_citation`-confirmed; NY/HI
framed as developing. These are the access-to-justice demonstrations the roadmap calls for. Each
example ends at a `## Terminal node` that stops with the human (state) attorney.

## Component 6 — Four packet fixtures

`evals/fixtures/drafting/state-era-<state>.{json,out.md}` (extracted from each packet / its worked
example's packet stage), registered in a new `evals/tests/test_state_era_packets.py`. Deterministic
checks per packet:
- `orientation-banner` — `contains` `ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE`.
- `law-as-of-stamp` — `contains` `Law-as-of:`.
- `provision-cite` — `contains` the state's provision marker (e.g., `art. I, § 27` for PA).
- `plain-language-sections` — `section_headers` for the six `## ...` headers.
- `closing-reminder` — `contains` `it does not mean you have a case`.
- `attorney-flag-present` — `regex` `\[⚠ ATTORNEY:[^\]]*\]`.
- `no-merits-advice` — `forbidden` `["you should sue", "you should file", "you'll win", "you will win", "you have a strong case"]`.
- `no-merits-conclusion` — `judge` (skipped in the deterministic lane): the packet explains the law
  generally and does not tell the reader they personally have a case or predict they would win.
- For **NY and HI only**: `developing-law` — `contains` a marker such as `developing` (the packet
  must flag the unsettled posture).

Deterministic suite **72 → 76**.
No new `markers.py` change is required (the packets reuse the plain-language section headers and the
attorney-flag/`[placeholder]` markers); `.github/workflows/evals.yml` already covers `templates/**`,
`evals/**`, and `docs/doctrinal-currency.md`.

## Component 7 — Docs

- `docs/architecture.md`: roadmap item 6 → **done** (the four `templates/state-era-*.md`), noting the
  per-state, plain-language-led, orientation-packet nature; and a line that **all six roadmap
  instruments are now shipped**.
- `README.md`: add the four packets to the layout tree (a `state-era-*` grouping).
- `CHANGELOG.md`: `## [Unreleased]` — Added (the four ERA packets; the four worked examples + four
  fixtures; the four new doctrinal anchors); Changed (drafting/intake/plain-language wiring).
- `CLAUDE.md`: note the ERA packets shipped and the instrument roadmap is complete.

## Component 8 — Legal-soundness gate (highest scrutiny in the project)

A dedicated final sweep — the WI-3-style review, applied hardest here:
1. **Every** provision quotation/citation and **every** case cite is `verify_citation`-/primary-source-confirmed; any that do not resolve are dropped or replaced with an `[⚠ ATTORNEY: identify and
   verify ...]` flag.
2. **PA/MT are not overstated; NY/HI are explicitly framed as developing** — no settled-standard
   implication anywhere in the NY/HI packets or examples.
3. Every packet carries the `Law-as-of:` stamp; the four anchors are stamped and
   `test_freshness.py` passes.
4. No packet or example tells a reader they have a case, accuses a named party, or predicts an
   outcome (invariant 5); neutral hypotheticals only.
5. `cd evals && pytest` green throughout.

## Six-invariant check

1. **DRAFT/marked banner** — every packet carries the orientation-packet banner + law-as-of stamp. ✓
2. **Inline `[⚠ ATTORNEY]` flags** — provision posture, standing, threshold, forum, the developing-law
   posture (NY/HI). ✓
3. **Doctrinal-currency check** — law-as-of stamps; `verify_citation` on every cite; the four anchors
   tracked. The state-law volatility is the invariant's hardest test. ✓
4. **No invented facts** — `[placeholder]` / flags for anything not verified; no fabricated case or
   holding. ✓
5. **No "you have a case / should sue / will win"** — the plain-language no-merits discipline,
   enforced by the fixtures' forbidden list + judge check. ✓
6. **Refuse harassment / bad-faith** — inherited from intake/plain-language; an ERA packet aimed at
   harassing a neighbor or a developer is a refused use. ✓

## Honest limits / out of scope

- No new connector code, no new skill, no new marker. This is four templates + three skills' wiring +
  four examples + four fixtures + four currency anchors + docs.
- The packet **orients**; it does not draft a state-court complaint (per-state procedure is for a
  licensed attorney). A future variant could add a per-state complaint scaffold.
- Only the four roadmap states are covered; other states' ERAs (e.g., the several states with weaker
  or non-self-executing provisions) are out of scope.
- The packets and examples use neutral hypotheticals; no real pending matter is depicted.

## Open questions

None blocking. Resolvable in planning/build: the exact per-state provision quotations and which
specific cases are `verify_citation`-confirmed (decided at build, per state); the exact filenames
(`templates/state-era-{pa,mt,ny,hi}.md` as above); and whether the README groups the packets under a
`state-era/` visual subheading in the tree (cosmetic).
