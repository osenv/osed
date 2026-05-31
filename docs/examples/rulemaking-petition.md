# Worked example — outdated effluent guideline → rulemaking-petition pathway

> Public matter, no client facts. Curated reference exemplar, not verbatim machine output, not
> legal advice. Subject to the doctrinal-currency rule. Each stage below is a registered eval
> fixture (`evals/fixtures/<skill>/rulemaking-petition*`).

**The matter.** Suppose EPA wrote an effluent guideline years ago and has not revised it under its
discretionary Clean Water Act § 304(b) authority, even though circumstances have changed. There is
no missed mandatory deadline to sue over — so the vehicle is a *petition asking the agency to act*.
This walks the pipeline from spotting that opening to a flagged petition and a lay explanation —
stopping, always, at a human attorney.

---

## Stage 1 — Gap Analysis

*Input:* the statute (CWA § 304(b)) and the rule's record. *Output:* a findings table.

```
# Gap Analysis: outdated effluent guideline — candidate for a rulemaking petition
Analyzed: [2026-05-30]  |  Doctrinal-currency check: [FLAGS — see notes]

| # | Duty / authority (cite) | Verb | Deadline (computed) | Trigger | Status | Evidence relied on | What a human must decide |
|---|---|---|---|---|---|---|---|
| 1 | CWA § 304(b) effluent-guideline review/revision | shall review and revise as appropriate | no fixed date (discretionary timing) | changed circumstances | QUALIFIED | get_current_regulation shows the guideline at [placeholder — 40 C.F.R. Part]; find_rule_changes shows no revision since [placeholder — year] | whether to petition for revision under APA § 553(e) |
| 2 | APA § 553(e) right to petition for rulemaking | the agency shall give an interested person the right to petition | n/a (no deadline) | filing a petition | CURRENT | 5 U.S.C. § 553(e) | the legal vehicle, not a duty miss |

## Notes and currency flags
- This is NOT a missed-deadline gap: § 304(b) revision timing is discretionary (QUALIFIED), so the vehicle is a petition asking the agency to act — not a § 505(a)(2) deadline suit.
- 5 U.S.C. § 553(e) verified via get_uscode_section.

## Handoff
- Instrument candidate (for Drafting agent): a rulemaking petition under APA § 553(e) asking EPA to revise the guideline.
- Candidate needing precedent before any decision (for Precedent Retrieval agent): the agency's duty to respond to a petition and the standard of review for a denial.
- ⚠️ This is a factual map, not a recommendation to sue. A licensed attorney must assess standing, ripeness, and litigation strategy before any instrument is drafted, sent, or filed.
```

**Handoff → Drafting.** The discretionary-timing duty is classified QUALIFIED, not a missed
deadline — so the instrument is a § 553(e) petition, not a deadline suit. Row 1 becomes the
petition's factual spine.

---

## Stage 2 — Drafting (with a flag that calls for precedent)

*Input:* the findings table, row 1. *Output:* a flagged DRAFT petition.

```
================ DRAFT — ATTORNEY REVIEW REQUIRED ================
This is a scaffold, not a filing. A licensed attorney in the relevant
jurisdiction must review, complete, verify, and sign before any use.
Doctrinal-currency check: [FLAGS below]
==================================================================

PETITION FOR RULEMAKING UNDER 5 U.S.C. § 553(e)
(Request to revise an effluent guideline under CWA § 304(b))

To: Administrator, U.S. EPA [⚠ ATTORNEY: confirm the correct office and docket for submission]
Petitioner: [placeholder — petitioner identity and address]

Per the Gap Analysis findings table (row 1), the effluent guideline at [placeholder]
(40 C.F.R. Part, from the record) has not been revised since [placeholder] (year
from the record), despite changed circumstances. Petitioner asks EPA to revise it.

[⚠ ATTORNEY: state the specific factual grounds for revision from the record;
confirm the requested action is within EPA's CWA § 304(b) authority.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[✓] Legal authority to petition (5 U.S.C. § 553(e)) and to act (CWA § 304(b))
[✓] The specific action requested (revise the named guideline)
[⚠ needed] Petitioner identity and interest
[⚠ needed] The factual grounds for revision (from the record)
[⚠ needed] The specific guideline citation and current text
[⚠ needed] Signature of the responsible attorney

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: needed — petitioner identity; factual grounds; exact guideline citation]
- [⚠ ATTORNEY: confirm the requested revision is within EPA's § 304(b) authority]
- [⚠ ATTORNEY: currency — 5 U.S.C. § 553(e) verified via get_uscode_section; the guideline checked via get_current_regulation and find_rule_changes; confirm in force]

DEADLINE NOTE
- A § 553(e) petition has no statutory filing deadline, but the agency must respond
  within a reasonable time, and a denial may be reviewable — facts for counsel to
  verify; this software does not track any clock.
```

**Handoff ↔ Precedent Retrieval.** The question of whether and how the agency must respond — and
how a refusal is reviewed — is a legal question the draft refuses to resolve. It becomes a
precedent request.

---

## Stage 3 — Precedent Retrieval (answering the draft's flag)

*Input:* the petition's duty-to-respond question. *Output:* the controlling-law landscape.

```
# Precedent: must an agency respond to a rulemaking petition, and how is a denial reviewed?  [forum: D.C. Circuit / SCOTUS framework]
Retrieved: [2026-05-30]  |  Currency check: [FLAGS]

## Controlling authority
| Case | Court / year | Jurisdiction & weight | Holding (plain) | Current status |
|---|---|---|---|---|
| Massachusetts v. EPA | U.S. 2007 | U.S. — binding (decided under the Clean Air Act) | An agency may not decline to respond to a rulemaking petition for reasons outside the governing statute; a denial is reviewable and may be set aside if arbitrary and capricious | CURRENT (verified via verify_citation) |

## Splits / tensions
- *Massachusetts v. EPA* arose under the Clean Air Act. For a Clean Water Act effluent-guideline petition, the general right to petition rests on APA § 553(e) and review of a denial on APA § 706 (and the D.C. Circuit's application of it) — [⚠ ATTORNEY: confirm the directly applicable duty-to-respond / standard-of-review authority for a CWA petition in the chosen forum; do not rely on Massachusetts v. EPA as the sole basis outside the CAA].
- Later decisions on agency authority (e.g., the major-questions line) can bear on what an agency may do in response — [⚠ ATTORNEY: confirm the current scope of EPA's authority for the specific revision sought; verify any further cite via verify_citation].

## What the rule is (not how it applies to you)
Under the APA, an interested person may petition for rulemaking (5 U.S.C. § 553(e)); the agency must respond, and a court reviews a denial under the arbitrary-and-capricious standard. The agency has broad discretion, but not unbounded discretion to ignore a petition.

## For the human deciding
- This is the legal landscape, not a prediction. Whether a specific petition or a denial-challenge succeeds is a judgment for a licensed attorney applying the law to specific facts in the chosen forum.
- Currency flags: Massachusetts v. EPA CURRENT for the duty-to-respond / arbitrary-capricious framework; flag the major-questions context as a CHANGED-adjacent consideration, not a DEAD classification.
- Jurisdiction gaps: confirm the reviewing court and any circuit-specific gloss before relying.
```

**Handoff → the human, and → Plain-Language.** The landscape attaches to the draft for the
attorney; meanwhile the pathway is translated for the people deciding whether to pursue it.

---

## Stage 4 — Plain-Language

*Input:* the pathway. *Output:* a lay explanation.

```
## What this is
A formal way to ask a government agency to make or change a rule. The law gives any interested person the right to file this kind of request — a "petition for rulemaking."

## What it asks of you
- Name the rule you want made or changed.
- Say what you want the agency to do, and point to its authority to do it.
- Give the factual reasons the change is warranted.

## How high the bar is
Filing is open to anyone — the threshold to *ask* is low. But the agency has wide discretion in how it answers, and getting a court to overturn a refusal is a steep, separate fight. A lawyer can weigh whether it is worth the effort.

## A plain example
Imagine an agency wrote a pollution limit decades ago and never updated it, even though the technology and the science have moved on. A community group could petition the agency to revise that limit.

## The clock
A petition has no filing deadline, but the agency must answer within a reasonable time, and any later challenge to a refusal can have tight deadlines. Confirm every date with a lawyer right away — this software does not track them.

## Your next step
Talk to counsel. A local environmental law clinic or legal aid office can help you decide whether a petition fits your goal.

This explains how the law works in general. It is not advice about your situation, and it does not mean you have a case — only a lawyer who reviews your specific facts can tell you that.
```

---

## Terminal node — the human attorney

The package — findings table, flagged petition, precedent landscape, plain-language explainer —
stops here. OSED drafts; **a licensed attorney decides** whether to petition, on what grounds, in
what forum, and whether to file anything. Nothing above is a recommendation or a prediction of
success.
