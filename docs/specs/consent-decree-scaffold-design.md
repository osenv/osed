# Consent-Decree Settlement Scaffold — Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-06-01 · **Branch:** `consent-decree-scaffold` (off `main`, through PR #9 / deadline complaint merged)
**Implements:** Roadmap item 5 of `docs/architecture.md` ("Consent-decree settlement scaffold — the negotiated, court-enforceable schedule; teaches the system to generate settlement structure, not just complaints").

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant; introduces a new emphasis (terms scaffolded-not-proposed) within them.

## Goal

Add the **deadline/duty-suit consent decree** — the negotiated resolution of a citizen-suit
failure-to-act case — to OSED's instrument library as one statute-agnostic template, wire it into
`drafting`, and extend the CWA §304(m) deadline example with a "Stage 6 — Consent Decree" so the full
arc (gap → notice → complaint → settlement) is shown end to end. This is the natural continuation of
the deadline complaint: instead of the court *ordering* the agency to act by a date, the parties
*agree* on a compliance schedule and the court *enters* it as an enforceable order.

## Why this instrument is different: terms scaffolded, not proposed

A consent decree is **both a contract and a court order**. It binds both parties and is enforceable
by the court. Critically, every substantive provision — the compliance-schedule dates, the fee
amount, whether liability is admitted, modification/force-majeure terms — is the product of
*negotiation between the parties and their counsel*. The agent has **no authority to set any term**.

So the templatable/judgment line reaches its strongest form yet: the scaffold supplies **structure
only**, and **every negotiated term is a `[placeholder]` carrying a `[⚠ ATTORNEY: negotiated term —
the parties and their counsel set this; the software does not propose it]` flag.** This is the
settlement analog of the complaint's "standing pleaded-not-asserted": here it is
**"terms scaffolded-not-proposed."** It is enforced mechanically by an eval check (Component 4).

Two further court-filing realities the scaffold must surface (flag, not assert):
- A government environmental consent decree is typically **lodged, published for public comment
  (e.g., 28 C.F.R. §50.7), then entered by the court** — so "drafted" ≠ "agreed" ≠ "effective."
- The court does not rubber-stamp: it enters a consent decree only on finding it **fair, reasonable,
  and consistent with the statute**. Entry is not automatic.

## Decisions resolved during brainstorming

1. **Deadline/duty-suit flavor** (not the violation-suit decree with penalties/injunctive measures;
   not a combined both-flavors scaffold). Direct continuation of the deadline complaint.
2. **Single statute-agnostic template** `templates/consent-decree-deadline.md` (not paired CWA+CAA):
   a deadline-suit decree's structure is statute-uniform — the statute appears only in the recitals —
   so one clean file avoids ~95% duplication.
3. **Extend one example** (CWA §304(m)) with a Stage 6 + one drafting fixture (not minimal; not both
   examples; not a new standalone example). One clean end-to-end demonstration of the agnostic
   template.
4. **Branch base:** off `main` (PR #9 merged).

## Component 1 — The template (`templates/consent-decree-deadline.md`)

Statute-agnostic scaffold for the negotiated resolution of a citizen-suit failure-to-act case,
in OSED house style (DRAFT banner → why-the-form-matters → required-elements checklist → DRAFT body
→ negotiated-terms/comment-entry note → consolidated attorney flags).

- **DRAFT banner** — settlement variant: the exact phrase `DRAFT SCAFFOLD — NOT AN AGREEMENT, NOT FOR
  LODGING OR ENTRY`. It is not agreed, not signed, not effective until lodged, published for comment,
  and entered by the court; FRCP / Rule 11 and the parties' counsel govern; points to
  `../DISCLAIMER.md`.
- **Why the form matters** — a consent decree binds both parties and becomes an enforceable court
  order; the agent supplies structure only; every negotiated term is the parties' to set; the court
  enters it only after the public-comment process and a fairness/reasonableness/statutory-consistency
  review.
- **Required-elements checklist** (each present or flagged):
  - Caption: same court/parties as the complaint `[⚠ ATTORNEY: confirm court and parties]`
  - WHEREAS recitals: the pending suit; the alleged nondiscretionary duty; the parties' intent to
    resolve **without admission of liability or fact** `[⚠ ATTORNEY: the no-admission framing is a
    negotiated term]`
  - Definitions
  - The court's jurisdiction and authority to enter the decree
  - The **compliance schedule** — agreed date(s) for the agency to perform the duty `[placeholder]`
    `[⚠ ATTORNEY: negotiated term — the parties set the schedule; the software does not propose dates]`
  - **No-admission-of-liability** clause (negotiated)
  - Reporting / progress obligations (negotiated)
  - Modification / good-cause extension / force-majeure (negotiated)
  - Dispute-resolution procedure (negotiated)
  - **Retention of jurisdiction** by the court to enforce the decree
  - Costs and attorney/expert fees `[placeholder]` `[⚠ ATTORNEY: negotiated term]`
  - **Lodging → public comment → entry** clause `[⚠ ATTORNEY: confirm the applicable comment/entry
    procedure for this matter, e.g., 28 C.F.R. §50.7; the decree is not effective until entered]`
  - Effective date / termination provisions (negotiated)
  - Signatures of all parties and their counsel; a `SO ORDERED` court-entry line
- **DRAFT body** (fenced block): the decree — caption; `WHEREAS` recitals; numbered sections
  (Jurisdiction; Definitions; Compliance Schedule; No Admission; Reporting; Modification/Force
  Majeure; Dispute Resolution; Retention of Jurisdiction; Costs and Fees; Public Comment and Entry;
  Effective Date/Termination); signature blocks for both parties + counsel; the `SO ORDERED` /
  entry line for the court. **Every substantive term is `[placeholder]` and carries the
  `[⚠ ATTORNEY: negotiated term — the parties and their counsel set this; the software does not
  propose it]` flag.** No invented dates, figures, or terms.
- **Negotiated-terms & comment/entry note** — restates: the schedule and all terms are negotiated;
  the decree is lodged + published for comment + entered before it is effective; the software tracks
  no clock and proposes no terms.
- **Consolidated attorney flags** — every negotiated term; the no-admission and retention clauses;
  the comment/entry procedure; the court's fairness review; counsel review and signature.

## Component 2 — Skill wiring

`skills/drafting/SKILL.md`: replace the table row
`| Memorialize a negotiated compliance schedule | Consent-decree settlement scaffold | (roadmap) |`
with a row pointing to `templates/consent-decree-deadline.md`. Add one sentence to the skill body:
consent decrees are **negotiated instruments** — the agent supplies structure and flags every term
as the parties' to negotiate, never proposing a schedule date, fee, or admission; and a consent
decree is court-entered only after public comment, so "drafted" ≠ "agreed" ≠ "effective."

## Component 3 — Extend the CWA example with Stage 6

Append **"Stage 6 — Consent Decree (negotiated resolution)"** to
`docs/examples/cwa-304m-deadline-suit.md`, after Stage 5 (the complaint) and before the Terminal
node. Framed: rather than litigate the filed complaint to judgment, the parties negotiate; this
scaffolds the agreement they would lodge for the court to enter. Drafted as the settlement of the
§304(m) suit, with the `DRAFT — ATTORNEY REVIEW REQUIRED` banner, a `Doctrinal-currency check:`
line, the consent-decree sections, every term a `[placeholder]` carrying the negotiated-term flag,
the no-admission / retention-of-jurisdiction / comment-and-entry clauses, and the
`REQUIRED-ELEMENTS CHECKLIST` / `CONSOLIDATED ATTORNEY FLAGS` / `DEADLINE NOTE` output sections. The
fenced-block count must stay even (document integrity). The Terminal-node paragraph is updated to
include the decree, still ending at the human attorney (who negotiates the terms and shepherds
entry).

## Component 4 — Drafting fixture

`evals/fixtures/drafting/consent-decree-deadline.{json,out.md}`, extracted from Stage 6, registered
in `evals/tests/test_golden_examples.py` (the CWA example's test). Deterministic checks mirror the
drafting set — `DRAFT — ATTORNEY REVIEW REQUIRED` banner; `Doctrinal-currency check:`;
`[⚠ ATTORNEY: ...]` regex; `[placeholder]`; `REQUIRED-ELEMENTS CHECKLIST`; `CONSOLIDATED ATTORNEY
FLAGS`; `DEADLINE NOTE`; a `not-finalized` forbidden list extended with decree-specific phrases
(`ready for entry`, `ready to lodge`, `final and binding`, plus the standard `ready to file` /
`final and signed`) — **plus a consent-decree-specific `negotiated-term-flagged` regex check**
(`\[⚠ ATTORNEY:[^\]]*negotiated[^\]]*\]`) that mechanically enforces "terms scaffolded-not-proposed,"
and a `judge` check that no specific schedule date or fee figure is invented (all are placeholders).
Deterministic suite **71 → 72**.

No new marker file change is required; the eval CI `paths` already cover `templates/**` and
`evals/**`.

## Component 5 — Docs

- `docs/architecture.md`: roadmap item 5 → **done** (`templates/consent-decree-deadline.md`), noting
  the deadline-suit flavor and that the violation-suit decree remains a possible future variant.
- `README.md`: add the template to the layout tree.
- `CHANGELOG.md`: `## [Unreleased]` — Added (the consent-decree template; the CWA example Stage-6
  extension + fixture); Changed (drafting instrument table).
- `CLAUDE.md`: one-line note (consent-decree scaffold shipped; state ERA packets are next).

## Component 6 — Legal-soundness gate

Final sweep: confirm the decree **proposes no terms** (every schedule date / fee / admission is
`[placeholder]` + a negotiated-term flag); confirm the **no-admission**, **retention-of-jurisdiction**,
and **lodging → comment → entry** clauses are present and flagged (the comment procedure, e.g.,
28 C.F.R. §50.7, flagged not asserted); confirm the decree is framed as **not effective until
entered** and notes the court's **fairness / reasonableness / statutory-consistency** review;
confirm no forbidden finalization phrase; verify any case cite via `verify_citation`; confirm no
invented facts. `cd evals && pytest` green throughout.

## Six-invariant check

1. **DRAFT banner** — template ("NOT AN AGREEMENT, NOT FOR LODGING OR ENTRY") and the example Stage-6
   draft. ✓
2. **Inline `[⚠ ATTORNEY]` flags** — every negotiated term, the no-admission/retention/comment-entry
   clauses, the court's fairness review. ✓
3. **Doctrinal-currency check** — the comment/entry procedure and any cite are tool-/flag-verified;
   the court's entry standard is flagged. ✓
4. **No invented facts** — every schedule date, fee, party, and term is `[placeholder]`; the agent
   proposes nothing. ✓
5. **No "you have a case / should sue / will win"** — a settlement scaffold makes no merits or
   outcome claim; it does not say the decree will be entered or the terms are favorable. ✓
6. **Refuse harassment / bad-faith** — inherited from `drafting`; a sham or collusive settlement is a
   bad-faith use the skill refuses. ✓

## Honest limits / out of scope

- No new connector code, skill, or marker; this is one template + drafting wiring + one example
  extension + one fixture + docs.
- The **violation-suit** consent decree (private violator; civil penalties; injunctive measures;
  stipulated penalties) is out of scope — a possible future variant noted in the roadmap.
- The template flags the comment/entry procedure and the court's entry standard; it does not resolve
  them (by design), and it proposes no negotiated term.
- The worked example uses the existing CWA §304(m) public matter; no new matter is invented.

## Open questions

None blocking. Resolvable in planning/build: the exact template filename
(`consent-decree-deadline.md` as above); the precise set of decree sections to enumerate in the body
(the Component-1 list is the default); and the exact decree-specific phrases added to the fixture's
`not-finalized` forbidden list.
