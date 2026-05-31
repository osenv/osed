# Worked example — CAA § 304(a)(2) missed nondiscretionary duty → failure-to-act pathway

> Public matter, no client facts. Curated reference exemplar, not verbatim machine output, not
> legal advice. Subject to the doctrinal-currency rule. Each stage below is a registered eval
> fixture (`evals/fixtures/<skill>/caa-304-failure-to-act*`).

**The matter.** Suppose the Clean Air Act requires EPA to complete a residual-risk review of a
source category by a fixed statutory deadline, and years have passed without one. This walks the
pipeline from spotting that gap to a flagged draft and a lay explanation — stopping, always, at a
human attorney. It is the air-side twin of the Clean Water Act § 304(m) deadline example: a dated,
mandatory duty the agency was supposed to perform by a date certain.

---

## Stage 1 — Gap Analysis

*Input:* the statute (CAA § 112(f)(2) duty, enforced via § 304(a)(2)) and EPA's public record.
*Output:* a findings table.

```
# Gap Analysis: Clean Air Act § 304(a)(2) — missed nondiscretionary residual-risk review
Analyzed: [2026-05-31]  |  Doctrinal-currency check: [FLAGS — see notes]

| # | Duty (cite) | Verb | Deadline (computed) | Trigger | Status | Evidence relied on | What a human must decide |
|---|---|---|---|---|---|---|---|
| 1 | CAA § 112(f)(2) residual-risk review for [placeholder — source category] (42 U.S.C. § 7412(f)(2)) | shall review | [placeholder — trigger date] + 8 years | promulgation of the § 112(d) emission standard for the category | MISSED — DEADLINE | find_agency_actions returned no residual-risk rule for the category since [placeholder — trigger date]; verify | whether the lapse supports a § 304(a)(2) failure-to-act claim |
| 2 | CAA § 112(d)(6) technology review ("review, and revise as necessary") | shall review | every 8 years | prior standard / review | UNVERIFIED | could not confirm a fixed, dated deadline or non-performance from available sources | whether this is a dated nondiscretionary duty or an undated periodic duty, and whether the review in fact occurred |

## Notes and currency flags
- § 112(f)(2) text verified via get_uscode_section (42 U.S.C. § 7412(f)(2)). The currency check
  targets the review duty itself: find_agency_actions found no residual-risk rule for
  [placeholder — source category] in the Federal Register since [placeholder — trigger date] —
  confirm before relying on row 1. The 8-year clock runs from the § 112(d) standard's promulgation
  date, so the enactment/trigger date must be pinned from the record before the deadline is computed.
- Duty 2 is UNVERIFIED and is NOT reported as a confirmed gap. A § 112(d)(6) periodic technology
  review may be an undated recurring duty (the UNREASONABLE-DELAY taxonomy) rather than a dated
  MISSED — DEADLINE duty; that classification is held back until the record fixes a date certain.

## Handoff
- Strongest failure-to-act candidate (for Drafting agent): row 1 — the missed residual-risk review.
- Candidate needing precedent before any decision (for Precedent Retrieval agent): whether the
  § 112(f)(2) review is a nondiscretionary duty enforceable under CAA § 304(a)(2) (as opposed to a
  discretionary act reviewable only as unreasonable delay).
- ⚠️ This is a factual map, not a recommendation to sue.
```

**Handoff → Drafting.** Row 1 (the missed residual-risk review) is the failure-to-act candidate;
its cells become the draft's factual spine. The "What a human must decide" column and the precedent
question travel onward — nothing here decides whether to sue.

---

## Stage 2 — Drafting (with a flag that calls for precedent)

*Input:* the findings table, row 1. *Output:* a flagged DRAFT notice.

```
================ DRAFT — ATTORNEY REVIEW REQUIRED ================
This is a scaffold, not a filing. A licensed attorney in the relevant
jurisdiction must review, complete, verify, and sign before any use.
Doctrinal-currency check: [FLAGS below]
==================================================================

NOTICE OF INTENT TO SUE UNDER CLEAN AIR ACT § 304(a)(2)
(Failure to perform a nondiscretionary duty — § 112(f)(2) residual-risk review)

To: Administrator, U.S. EPA [⚠ ATTORNEY: confirm current Administrator and the
service addresses required by 40 C.F.R. Part 54; service is on the Administrator
by certified mail, and notice is deemed given on the postmark date.]
From: [placeholder — notifying party identity and address]

Per the Gap Analysis findings table (row 1), EPA has not completed the
residual-risk review required by CAA § 112(f)(2), 42 U.S.C. § 7412(f)(2), for
[placeholder — source category]. The § 112(d) emission standard for the category
issued on [placeholder — trigger date from the record]; the 8-year review came
due on [placeholder — computed deadline], and no residual-risk rule has issued in
the [placeholder] years since.

[⚠ ATTORNEY: confirm § 112(f)(2)'s review is a nondiscretionary duty enforceable
under § 304(a)(2) — not a discretionary act reviewable only as unreasonable delay —
in the chosen circuit before relying on the deadline theory; see the precedent
landscape.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[✓] Statutory basis (CAA § 304(a)(2), 42 U.S.C. § 7604(a)(2); § 112(f)(2),
    42 U.S.C. § 7412(f)(2))
[⚠ needed] Identity and address of the notifying party
[⚠ needed] The trigger date (§ 112(d) standard's promulgation) and the computed
    deadline, from the agency record
[⚠ needed] The fact of non-performance, drawn from the agency record
[⚠ needed] Service on the EPA Administrator per 40 C.F.R. Part 54 (certified mail)
[⚠ needed] Signature of the responsible attorney

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: needed — notifying-party identity; trigger date and computed
  deadline from the record; do not allege a date the record does not support]
- [⚠ ATTORNEY: confirm § 112(f)(2) nondiscretionary-duty enforceability under
  § 304(a)(2) in the chosen circuit (nondiscretionary-duty vs. unreasonable-delay
  line)]
- [⚠ ATTORNEY: assess whether the § 7412(i)(3)(A)/(f)(4) or § 7413(a) immediate-suit
  exception applies — i.e., whether the 60-day wait is required at all for this duty]
- [⚠ ATTORNEY: currency — § 112(f)(2) verified via get_uscode_section; confirm via
  the Federal Register (find_agency_actions) that no residual-risk rule has issued,
  and confirm the duty remains in force]

DEADLINE NOTE
- CAA § 304(b)(2), 42 U.S.C. § 7604(b)(2), requires 60 days' written notice to the
  Administrator before filing a § 304(a)(2) failure-to-act action — a fact for
  counsel to verify and track; this software does not track the clock. Whether an
  immediate-suit exception applies is for counsel to assess (see flags).
```

**Handoff ↔ Precedent Retrieval.** The flag *"confirm § 112(f)(2)'s review is a nondiscretionary
duty enforceable under § 304(a)(2)"* is a legal question the draft refuses to resolve. It becomes a
precedent request.

---

## Stage 3 — Precedent Retrieval (answering the draft's flag)

*Input:* the draft's § 304(a)(2) flag. *Output:* the controlling-law landscape.

```
# Precedent: is a § 112(f)(2) review a nondiscretionary duty enforceable under § 304(a)(2)?  [forum: not yet fixed — flag]
Retrieved: [2026-05-31]  |  Currency check: [FLAGS]

## Controlling authority
| Case | Court / year | Jurisdiction & weight | Holding (plain) | Current status |
|---|---|---|---|---|
| Sierra Club v. Thomas | D.C. Cir. 1987 | D.C. Cir. — persuasive elsewhere, weighty in CAA practice | Draws the line between a § 304(a)(2) suit to compel a nondiscretionary duty owed by a date certain and an unreasonable-delay claim over a discretionary act with no statutory deadline | CURRENT (verified via verify_citation) |

## What the rule is (not how it applies to you)
CAA § 304(a)(2) authorizes a citizen suit to compel the Administrator to perform an act or duty
that is **nondiscretionary** — typically a "shall … by [a date]" duty. A duty with no statutory
deadline, or one left to the agency's discretion, generally is not reachable under § 304(a)(2);
the avenue there is an unreasonable-delay claim, which is a different theory with a different
standard. Whether a given § 112(f)(2) review falls on the nondiscretionary, date-certain side of
that line is the threshold question, and it can turn on how the controlling circuit reads the
statute.

## For the human deciding
- This is the legal landscape, not a prediction. Whether a specific § 112(f)(2) review supports a
  § 304(a)(2) claim in a specific forum is a judgment for a licensed attorney applying it to
  specific facts.
- Currency flags: Sierra Club v. Thomas CURRENT (verified via verify_citation — a confirmation the
  citation resolves, not a promise it remains good law; read the subsequent history). Whether this
  particular § 112(f)(2) duty counts as nondiscretionary for § 304(a)(2) is forum-dependent and
  UNVERIFIED here — do not present it as settled. [⚠ ATTORNEY: identify and verify (via
  verify_citation) the controlling § 304(a)(2) nondiscretionary-duty precedent for the chosen forum.]
- Jurisdiction gaps: forum not yet fixed; pin the circuit before relying on any application.
```

**Handoff → the human, and → Plain-Language.** The landscape attaches to the draft's flag for the
attorney; meanwhile the pathway is translated for the people who have to decide whether to pursue it.

---

## Stage 4 — Plain-Language

*Input:* the pathway. *Output:* a lay explanation.

```
## What this is
A way to make a federal agency do something the law says it "shall" do by a deadline. When the EPA
misses a mandatory deadline for an action the Clean Air Act commands, a member of the public can
sometimes ask a court to order it to act.

## What it asks of you
- Show the law sets a real, mandatory deadline (a "shall ... by" duty), not just something the
  agency may do whenever it chooses.
- Show the agency missed it.
- Give the EPA Administrator written notice — for this kind of Clean Air Act claim, 60 days —
  before filing.

## How high the bar is
The deadline itself can be straightforward to show. The harder questions — whether the duty is
"nondiscretionary" (a date-certain command, not a discretionary choice), whether you have standing,
and which court — are real barriers a lawyer must weigh.

## A plain example
Imagine a law says the EPA must re-examine the cancer risk from a category of factories within
eight years of setting the pollution limits for them, and many years have passed with no
re-examination. That gap is the kind of thing this pathway is built for.

## The clock
There is a strict 60-day notice step to the Administrator before filing, and other deadlines may
apply. Confirm every date with a lawyer right away — this software does not track them.

## Your next step
Talk to counsel. A local environmental law clinic or legal aid office can help you weigh whether
this pathway fits.

This explains how the law works in general. It is not advice about your situation,
and it does not mean you have a case — only a lawyer who reviews your specific facts can tell you that.
```

---

## Terminal node — the human attorney

The package — findings table, flagged draft, precedent landscape, plain-language explainer — stops
here. OSED drafts; **a licensed attorney decides** whether the duty is nondiscretionary and
enforceable, whether standing exists, which forum, and whether to send or file anything. Nothing
above is a recommendation to sue or a prediction of success.
