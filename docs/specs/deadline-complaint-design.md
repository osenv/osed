# Deadline-Complaint Instrument — Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-05-31 · **Branch:** `deadline-complaint` (off `main`, through PR #8 / CAA §304 merged)
**Implements:** Roadmap item 4 of `docs/architecture.md` ("Deadline complaint — scaffold directly from a Gap Analysis findings table"). The **first court-filing** instrument in the library.

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant; preserves all six and draws the judgment line harder for a court filing.

## Goal

Add the federal **deadline complaint** — the citizen-suit "failure to perform a nondiscretionary
duty" pleading filed after the notice period runs — to OSED's instrument library as two
statute-concrete templates (CWA §505(a)(2) and CAA §304(a)(2)), wire them into `drafting`, and
extend the two existing deadline worked-examples with a complaint stage so the
notice → wait → complaint arc is shown end to end. This is the natural next stage after the §505 /
§304 deadline notices already shipped.

## Why this instrument is different: the court-filing escalation

Every prior instrument (rulemaking petition, §505/§304 notices) is **pre-suit**. A complaint is a
**court filing** governed by the Federal Rules of Civil Procedure (FRCP 8 — short and plain
statement of the grounds for jurisdiction, the claim, and the relief; FRCP 10 — caption/numbered
paragraphs; FRCP 11 — signature, non-frivolous). This sharpens the templatable/judgment line:

- **Standing** (injury-in-fact, causation, redressability) is *jurisdictional* and is the court's to
  decide — the template **pleads** standing elements as flagged allegations and **never asserts** that
  standing exists.
- **Subject-matter jurisdiction** (28 U.S.C. §1331 + the citizen-suit grant) and **venue** are
  flagged for counsel, not asserted as settled.
- The complaint is the **date-certain deadline-suit remedy** (compel action by a date). It must NOT
  drift into an **unreasonable-delay** claim (the TRAC "how long is too long" judgment) — that suit
  type is deliberately out of scope, kept on the judgment side of the line.

## Decisions resolved during brainstorming

1. **Paired, statute-concrete templates** (not a statute-agnostic single template; not CWA-only):
   `templates/cwa-505-deadline-complaint.md` and `templates/caa-304-deadline-complaint.md`. Matches
   how every OSED instrument is statute-concrete and the two existing deadline examples.
2. **Extend both existing examples** with a Stage 5 complaint (not minimal-fixtures-only; not new
   standalone examples) — reuses the findings-table spine and tells the true litigation arc.
3. **Scope excludes unreasonable-delay** complaints (not templatable; the agent flags and routes
   those to counsel).
4. **Branch base:** off `main` (PR #8 / CAA §304 merged).

## Verified-before-drafting (the currency invariant applied to our own drafting)

A Task-0 gate, mirroring the CAA work, pulls the load-bearing authorities via the connector BEFORE
any template prose is written — never from memory:

- **CWA §505 / 33 U.S.C. §1365** via `get_uscode_section`: the citizen-suit jurisdiction grant
  (§1365(a) — district-court jurisdiction), and **the §505(a)(2) notice precondition (§1365(b))**.
  This last point is load-bearing: the existing `docs/examples/cwa-304m-deadline-suit.md` asserts a
  "60-day §505(a)(2) notice"; this spec **re-confirms that against §1365(b) and corrects it in place
  if the statute does not bear it out** (a small, in-scope fix to a previously-shipped file).
- **CAA §304 / 42 U.S.C. §7604** via `get_uscode_section`: §7604(a)(2) failure-to-act track,
  §7604(a) district-court jurisdiction, the §7604(b)(2) 60-day-to-the-Administrator notice
  (already verified during the CAA work).
- Citizen-suit **fee provisions** (§1365(d) / §7604(d)) for the prayer's costs-and-fees paragraph —
  flag, do not over-assert.

Whatever cannot be tool-confirmed is written as a `[⚠ ATTORNEY: ...]` flag, never asserted.

## Component 1 — Two templates

Both follow the OSED template house style (DRAFT banner → why-the-form-matters → required-elements
checklist → DRAFT body → precondition/deadline note → consolidated attorney flags), adapted to a
federal complaint. Every authority carries a tool-backed currency flag.

**Shared structure (FRCP complaint):**
- **DRAFT banner** — court-filing variant: `DRAFT SCAFFOLD — NOT FOR FILING` (distinct from the
  notices' "NOT A FILING"); a defective complaint is dismissable; FRCP 11 review/signature required;
  points to `../DISCLAIMER.md`.
- **Why the form matters** — FRCP 8(a) short-plain-statement; standing is jurisdictional and the
  court's to decide; the 60-day (or statute-specific) notice precondition must already be satisfied.
- **Required-elements checklist** (each present or flagged):
  - Caption: court and division `[⚠ ATTORNEY: confirm proper court and venue]`; full party names;
    civil-action number `[placeholder]`.
  - **Jurisdiction**: 28 U.S.C. §1331 (federal question) + the citizen-suit grant (CWA §505 /
    33 U.S.C. §1365(a) or CAA §304 / 42 U.S.C. §7604(a)).
  - **Venue** `[⚠ ATTORNEY: confirm venue (e.g., 28 U.S.C. §1391(e) for an action against a federal
    agency/officer) for the chosen forum]`.
  - **Parties + standing**: plaintiff's standing elements pleaded as allegations
    `[⚠ ATTORNEY: standing (injury-in-fact, causation, redressability) is jurisdictional and the
    court's to decide — plead the elements; do not assert standing is established]`; defendant
    (the Administrator / agency).
  - **Notice precondition satisfied**: the required pre-suit notice was served and the period ran
    `[⚠ ATTORNEY: confirm the notice was properly served and the statutory period has run before
    filing]` (ties to the §505/§304 notice instrument).
  - The **nondiscretionary duty** + its statutory hook + the **statutory deadline** + the
    missed-deadline facts, drawn from the Gap Analysis findings table (`[placeholder]` for record
    facts; `[⚠ ATTORNEY: confirm the duty is nondiscretionary and the deadline computation]`).
  - **Count I — Failure to Perform a Nondiscretionary Duty**.
  - **Prayer for relief**: declaratory judgment that the defendant is in violation; a **mandatory
    injunction / order compelling the action by a date certain**; retention of jurisdiction; costs
    and attorney/expert fees under the statute's fee provision; any other just relief.
  - FRCP 11 signature block.
- **DRAFT body** (fenced block): CAPTION → NATURE OF THE ACTION → JURISDICTION AND VENUE → PARTIES
  → STATUTORY BACKGROUND → FACTUAL ALLEGATIONS → CLAIM FOR RELIEF (Count I) → PRAYER FOR RELIEF →
  signature block. Inline `[⚠ ATTORNEY: ...]` at every gating doctrine (standing, jurisdiction,
  venue, notice satisfaction, nondiscretionary-duty determination); `[placeholder]` for every fact.
- **Precondition / deadline note** — the pre-suit notice must already be satisfied; the complaint
  is the date-certain deadline-suit remedy; the software tracks no clock.
- **Consolidated attorney flags**.

**Per-template specifics:**
- `cwa-505-deadline-complaint.md` — CWA §505(a)(2) / 33 U.S.C. §1365(a)(2); jurisdiction §1365(a);
  fees §1365(d); the §1365(b) notice precondition (re-verified per Task 0); defendant the EPA
  Administrator for a §304(m)-type planning-duty miss.
- `caa-304-deadline-complaint.md` — CAA §304(a)(2) / 42 U.S.C. §7604(a)(2); jurisdiction §7604(a);
  fees §7604(d); the §7604(b)(2) 60-day notice precondition; defendant the EPA Administrator.

## Component 2 — Skill wiring

`skills/drafting/SKILL.md`: replace the single roadmap row
`| Sue over a clearly missed statutory deadline | Deadline complaint | (roadmap — scaffold from Gap Analysis output) |`
with two rows pointing to the templates (CWA §505(a)(2) and CAA §304(a)(2) deadline complaints). Add
one sentence to the skill body noting that complaints are **court filings** — FRCP 11 applies, and
standing/jurisdiction/venue are flagged for counsel, never asserted. (The existing "you do not
resolve standing, ripeness" guardrail already states the principle; this names the complaint case.)

## Component 3 — Extend both existing examples

Append **"Stage 5 — Deadline Complaint (after the notice period runs)"** to
`docs/examples/cwa-304m-deadline-suit.md` and `docs/examples/caa-304-failure-to-act-suit.md`, before
each file's Terminal-node paragraph. Each Stage 5:
- opens with the temporal beat ("60 days have passed; the agency has still not acted");
- drafts the complaint from the **same findings-table row** that fed the notice (spine reused);
- carries the `DRAFT — ATTORNEY REVIEW REQUIRED` banner, a `Doctrinal-currency check:` line, the
  gating-doctrine flags (standing / jurisdiction / venue), the FRCP-complaint sections, and
  `[placeholder]` facts; "180" must not appear in the CAA file.
- The Terminal-node paragraph is updated only as needed to acknowledge the complaint now in the
  package (still ending at the human attorney).

While editing `cwa-304m-deadline-suit.md`, re-verify and (if needed) correct its existing "60-day
§505(a)(2) notice" statement per Task 0.

## Component 4 — Two drafting fixtures + registration

A drafting fixture per complaint, extracted from each new Stage 5:
- `evals/fixtures/drafting/cwa-505-deadline-complaint.{json,out.md}`
- `evals/fixtures/drafting/caa-304-deadline-complaint.{json,out.md}`

Deterministic checks mirror the existing drafting fixtures — `DRAFT — ATTORNEY REVIEW REQUIRED`
banner; `Doctrinal-currency check:`; `[⚠ ATTORNEY: ...]` regex; `[placeholder]`; the
`not-finalized` forbidden list — plus a **complaint-specific** check: a regex for a
standing-or-jurisdiction `[⚠ ATTORNEY: ...]` flag; and a `judge` check that facts trace to the
findings table (no invented allegation). The CWA fixture registers in
`evals/tests/test_golden_examples.py`; the CAA fixture in `evals/tests/test_caa_304_examples.py`.
Deterministic suite **69 → 71**.

No new marker file change is required (complaints reuse the drafting markers). The eval CI `paths`
already cover `templates/**` and `evals/**`.

## Component 5 — Docs

- `docs/architecture.md`: roadmap item 4 → **done** (both template paths; note the two tracks).
- `README.md`: add both templates to the layout tree.
- `CHANGELOG.md`: `## [Unreleased]` — Added (two deadline-complaint templates; the two example Stage-5
  extensions + 2 fixtures); Changed (drafting instrument table; if the CWA notice assertion is
  corrected, note it).
- `CLAUDE.md`: one-line note (deadline complaint shipped; consent-decree scaffold is next).

## Component 6 — Legal-soundness gate

Final sweep (the WI-3-style review that caught three exemplar errors): confirm the citizen-suit
jurisdiction grants and the (a)(2) notice preconditions via `get_uscode_section`; confirm the CWA
example's notice statement is now correct; confirm both complaints **flag** standing/jurisdiction/
venue rather than asserting them; confirm the prayer seeks a **date-certain order** (deadline-suit
remedy), not unreasonable-delay relief; confirm Count I is "failure to perform a nondiscretionary
duty," not a merits/`how-long-is-too-long` theory; verify any case cite via `verify_citation`;
confirm no invented facts. `cd evals && pytest` green throughout.

## Six-invariant check

1. **DRAFT banner** — both templates ("NOT FOR FILING") and both example Stage-5 drafts. ✓
2. **Inline `[⚠ ATTORNEY]` flags** — standing, jurisdiction, venue, notice satisfaction,
   nondiscretionary-duty, deadline computation. ✓
3. **Doctrinal-currency check** — jurisdiction grants + notice preconditions tool-verified; cites
   via `verify_citation`. ✓
4. **No invented facts** — every party, date, duty, and figure is `[placeholder]` from the findings
   table. ✓
5. **No "you have a case / should sue / will win"** — the complaint pleads; it never tells the user
   the suit will succeed; standing is the court's call. ✓
6. **Refuse harassment / bad-faith** — inherited from `drafting`; a complaint is exactly where a
   bad-faith filing does harm, so the refusal posture is reaffirmed. ✓

## Honest limits / out of scope

- No new connector code, skill, or marker; this is two templates + drafting wiring + two example
  extensions + two fixtures + docs.
- Unreasonable-delay (APA §706(1) / TRAC) complaints are out of scope.
- The templates flag venue/standing/jurisdiction; they do not resolve them (by design).
- The specific public matters are the two already in the existing examples; no new matter is invented.

## Open questions

None blocking. Resolvable in planning/build: exact template filenames (`cwa-505-deadline-complaint.md`
/ `caa-304-deadline-complaint.md` as above); whether the CWA §505(a)(2) notice precondition needs a
correction (decided by the Task-0 verification); and the precise placement of Stage 5 relative to the
plain-language stage in each example (default: after Plain-Language, before Terminal node).
