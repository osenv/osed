# Worked example — CWA § 304(m) missed deadline → deadline-suit pathway

> Public matter, no client facts. Curated reference exemplar, not verbatim machine output, not
> legal advice. Subject to the doctrinal-currency rule. Each stage below is a registered eval
> fixture (`evals/fixtures/<skill>/cwa-304m-deadline*`).

**The matter.** EPA's Clean Water Act § 304(m) requires it to publish a biennial plan for
reviewing and revising effluent guidelines. Suppose years have passed without one. This walks the
pipeline from spotting that gap to a flagged draft and a lay explanation — stopping, always, at a
human attorney.

---

## Stage 1 — Gap Analysis

*Input:* the statute (CWA § 304(m)) and EPA's public record. *Output:* a findings table.

```
# Gap Analysis: Clean Water Act § 304(m) — effluent-guidelines planning
Analyzed: [2026-05-30]  |  Doctrinal-currency check: [FLAGS — see notes]

| # | Duty (cite) | Verb | Deadline (computed) | Trigger | Status | Evidence relied on | What a human must decide |
|---|---|---|---|---|---|---|---|
| 1 | CWA § 304(m)(1)(A) biennial effluent-guidelines plan | shall publish | [placeholder — last plan date] + 2 years | prior plan publication | MISSED — DEADLINE | find_agency_actions returned no biennial plan since [placeholder — last plan date]; verify | whether the lapse supports a § 505(a)(2) claim |
| 2 | CWA § 304(m)(1)(B) annual review of categories | shall review | annual | each calendar year | UNVERIFIED | could not confirm from available sources | whether the review in fact occurred |

## Notes and currency flags
- § 304(m) text verified via get_uscode_section (33 U.S.C. § 1314(m)). The currency check targets the planning duty itself: find_agency_actions found no biennial plan in the Federal Register since [placeholder — last plan date] — confirm before relying on row 1.
- Duty 2 is UNVERIFIED and is NOT reported as a confirmed gap.

## Handoff
- Strongest deadline-suit candidate (for Drafting agent): row 1 — the missed biennial plan.
- Candidate needing precedent before any decision (for Precedent Retrieval agent): whether § 304(m) is a nondiscretionary duty enforceable under CWA § 505(a)(2).
- ⚠️ This is a factual map, not a recommendation to sue. A licensed attorney must assess standing, ripeness, and litigation strategy before any instrument is drafted, sent, or filed.
```

**Handoff → Drafting.** Row 1 (the missed biennial plan) is the deadline-suit candidate; its cells
become the draft's factual spine. The "What a human must decide" column and the precedent question
travel onward — nothing here decides whether to sue.

---

## Stage 2 — Drafting (with a flag that calls for precedent)

*Input:* the findings table, row 1. *Output:* a flagged DRAFT notice.

```
================ DRAFT — ATTORNEY REVIEW REQUIRED ================
This is a scaffold, not a filing. A licensed attorney in the relevant
jurisdiction must review, complete, verify, and sign before any use.
Doctrinal-currency check: [FLAGS below]
==================================================================

NOTICE OF INTENT TO SUE UNDER CLEAN WATER ACT § 505(a)(2)
(Failure to perform a nondiscretionary duty — § 304(m) effluent-guidelines plan)

To: Administrator, U.S. EPA [⚠ ATTORNEY: confirm current Administrator and the service addresses required by 40 C.F.R. Part 135]
From: [placeholder — notifying party identity and address]

Per the Gap Analysis findings table (row 1), EPA has not published the biennial
effluent-guidelines plan required by CWA § 304(m)(1)(A), 33 U.S.C. § 1314(m). The
last plan issued on [placeholder — date from the record]; no plan has issued in the
[placeholder] years since.

[⚠ ATTORNEY: confirm § 304(m) is a nondiscretionary duty enforceable under
§ 505(a)(2) in the chosen circuit before relying on the deadline theory — see the
precedent landscape.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[✓] Statutory basis (CWA § 505(a)(2); § 304(m), 33 U.S.C. § 1314(m))
[⚠ needed] Identity and address of the notifying party
[⚠ needed] Date the last plan issued (from the agency record)
[⚠ needed] Service on the EPA Administrator per 40 C.F.R. Part 135
[⚠ needed] Signature of the responsible attorney

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: needed — notifying-party identity; last-plan date from the record]
- [⚠ ATTORNEY: confirm § 304(m) nondiscretionary-duty enforceability under § 505(a)(2)]
- [⚠ ATTORNEY: currency — § 304(m) verified via get_uscode_section; confirm via the Federal Register (find_agency_actions) that no biennial plan has issued, and confirm the duty remains in force]

DEADLINE NOTE
- CWA § 505(b) requires 60 days' written notice before filing a § 505(a)(2) action —
  a fact for counsel to verify; this software does not track the clock.
```

**Handoff ↔ Precedent Retrieval.** The flag *"confirm § 304(m) is a nondiscretionary duty
enforceable under § 505(a)(2)"* is a legal question the draft refuses to resolve. It becomes a
precedent request.

---

## Stage 3 — Precedent Retrieval (answering the draft's flag)

*Input:* the draft's § 505(a)(2) flag. *Output:* the controlling-law landscape.

```
# Precedent: is CWA § 304(m) enforceable as a nondiscretionary duty under § 505(a)(2)?  [forum: not yet fixed — flag]
Retrieved: [2026-05-30]  |  Currency check: [FLAGS]

## Controlling authority
| Case | Court / year | Jurisdiction & weight | Holding (plain) | Current status |
|---|---|---|---|---|
| Gwaltney of Smithfield, Ltd. v. Chesapeake Bay Found., Inc. | U.S. 1987 | U.S. — binding | Defines the structure of CWA § 505 citizen suits; § 505(a)(1) requires a good-faith allegation of an ongoing violation | CURRENT (verified via verify_citation) |

## Splits / tensions
- The § 505(a)(2) "failure to perform a nondiscretionary duty" track is distinct from the § 505(a)(1) discharge track in Gwaltney. Whether § 304(m)'s planning duty counts as "nondiscretionary" for § 505(a)(2) is the live question and may turn on circuit treatment — [⚠ ATTORNEY: identify and verify (via verify_citation) the controlling § 505(a)(2) nondiscretionary-duty precedent for the chosen forum].

## What the rule is (not how it applies to you)
CWA § 505 authorizes citizen suits on two tracks: § 505(a)(1) against ongoing violations, and § 505(a)(2) to compel EPA to perform a nondiscretionary duty. Each has its own threshold and its own notice rule.

## For the human deciding
- This is the legal landscape, not a prediction. Whether § 304(m) supports a § 505(a)(2) claim in a specific forum is a judgment for a licensed attorney applying it to specific facts.
- Currency flags: Gwaltney CURRENT; the controlling § 505(a)(2) nondiscretionary-duty case is forum-dependent and UNVERIFIED here — do not present it as settled.
- Jurisdiction gaps: forum not yet fixed; pin the circuit before relying on any application.
```

**Handoff → the human, and → Plain-Language.** The landscape attaches to the draft's flag for the
attorney; meanwhile the pathway is translated for the people who have to decide whether to pursue it.

---

## Stage 4 — Plain-Language

*Input:* the pathway. *Output:* a lay explanation.

```
## What this is
A way to make a federal agency do something the law says it "shall" do by a deadline. When an agency misses a mandatory deadline, a member of the public can sometimes ask a court to order it to act.

## What it asks of you
- Show the law sets a real, mandatory deadline (a "shall ... by" duty).
- Show the agency missed it.
- Give the agency written notice — for this kind of Clean Water Act claim, 60 days — before filing.

## How high the bar is
The deadline itself can be straightforward to show. The harder questions — whether the duty is "nondiscretionary," whether you have standing, and which court — are real barriers a lawyer must weigh.

## A plain example
Imagine a law says an agency must publish an updated pollution-control plan every two years, and several years have passed with no plan. That gap is the kind of thing this pathway is built for.

## The clock
There is a strict 60-day notice step before filing, and other deadlines may apply. Confirm every date with a lawyer right away — this software does not track them.

## Your next step
Talk to counsel. A local environmental law clinic or legal aid office can help you weigh whether this pathway fits.

This explains how the law works in general. It is not advice about your situation, and it does not mean you have a case — only a lawyer who reviews your specific facts can tell you that.
```

---

## Terminal node — the human attorney

The package — findings table, flagged draft, precedent landscape, plain-language explainer — stops
here. OSED drafts; **a licensed attorney decides** whether the duty is enforceable, whether
standing exists, which forum, and whether to send or file anything. Nothing above is a
recommendation to sue or a prediction of success.
