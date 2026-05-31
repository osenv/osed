# Worked example — CAA § 304(a)(1) emission violation → citizen-suit notice pathway

> Public matter, no client facts. Curated reference exemplar, not verbatim machine output, not
> legal advice. Subject to the doctrinal-currency rule. Each stage below is a registered eval
> fixture (`evals/fixtures/<skill>/caa-304-emissions*`).

**The matter.** Suppose a stationary source — a power plant, refinery, or cement kiln — operates
under a federally enforceable emission limit (an NSPS or NESHAP standard, or a Title V / SIP permit
limit), and the source's own continuous-monitoring records show repeated exceedances of that limit
over a period. This walks the pipeline from spotting that exceedance pattern to a flagged draft and
a lay explanation — stopping, always, at a human attorney. It is the violator-facing twin of the
CAA § 304(a)(2) failure-to-act example: not a missed agency deadline, but an ongoing emission
violation by a regulated source.

---

## Stage 1 — Gap Analysis

*Input:* the applicable emission standard (an NSPS/NESHAP or Title V / SIP permit limit) and the
source's public monitoring record. *Output:* a findings table.

```
# Gap Analysis: Clean Air Act § 304(a)(1) — emission-limit exceedances at a stationary source
Analyzed: [2026-05-31]  |  Doctrinal-currency check: [FLAGS — see notes]

| # | Standard (cite) | Limit | Exceedance record | Source | Status | Evidence relied on | What a human must decide |
|---|---|---|---|---|---|---|---|
| 1 | [placeholder — applicable emission limit: NSPS/NESHAP subpart or Title V / SIP permit limit] for [placeholder — emission unit/stack] | [placeholder — limit value/averaging period] | repeated exceedances over [placeholder — period] | [placeholder — the source's own CEMS/monitoring reports] | VIOLATION FINDING | get_current_regulation confirmed the standard exists and is in force as of retrieval; monitoring records treated as RAW DATA showing readings above the limit; verify | whether the record supports a good-faith allegation of an ongoing/recurring violation under § 304(a)(1) |
| 2 | [placeholder — second emission limit or opacity standard] | [placeholder] | scattered readings near/above limit | [placeholder — same monitoring data] | UNVERIFIED | could not confirm the readings exceed the limit after applicable averaging/exemptions, or that the standard applies to this unit | whether the standard applies to this unit and whether the readings are true exceedances after averaging |

## Notes and currency flags
- The applicable emission standard's existence and in-force status were checked via
  get_current_regulation (the codified NSPS/NESHAP text) — confirm the standard, its averaging
  period, and any startup/shutdown/malfunction provisions before relying on row 1. eCFR is
  unofficial-but-current; the legally operative text is the annual GPO CFR.
- The exceedance evidence is RAW MONITORING DATA, never assumed. A reading above a numeric limit is
  not automatically a violation until the applicable averaging time and any exemptions are applied —
  that application is held for counsel. Row 1 reports a VIOLATION FINDING only as a factual map of
  what the record shows, not a legal conclusion.
- Duty 2 is UNVERIFIED and is NOT reported as a confirmed gap: whether the standard reaches this
  unit, and whether the readings survive averaging, is unresolved and held back from the gap set.
- No "deadline" framing applies here. This track is an ongoing emission violation by a source, not a
  missed agency deadline — the status taxonomy is VIOLATION FINDING / UNVERIFIED, not MISSED — DEADLINE.

## Handoff
- Strongest emission-violation candidate (for Drafting agent): row 1 — the documented exceedances of
  the applicable limit.
- Candidate needing precedent before any decision (for Precedent Retrieval agent): whether the
  record supports a good-faith allegation of an ongoing/recurring violation, as § 304(a)(1) requires
  (the CAA ongoing-violation question).
- ⚠️ This is a factual map, not a recommendation to sue.
```

**Handoff → Drafting.** Row 1 (the documented exceedances) is the emission-violation candidate; its
cells become the draft's factual spine. The "What a human must decide" column and the precedent
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

NOTICE OF INTENT TO SUE UNDER CLEAN AIR ACT § 304(a)(1)
(Violation of an emission standard or limitation — 42 U.S.C. § 7604(a)(1))

To: [placeholder — alleged violator: full legal name and address; owner and
operator if different] [⚠ ATTORNEY: confirm the violator's correct legal name.]
Service copies to: Administrator, U.S. EPA; [placeholder — State] air-quality
agency. [⚠ ATTORNEY: § 304(a)(1) notice is served on all three — the alleged
violator, the EPA Administrator, AND the State. Confirm the complete current
service list and addresses per 40 C.F.R. Part 54; service is by certified mail
(or personal service on the violator); notice is deemed given on the postmark date.]
From: [placeholder — notifying party identity and address]

Per the Gap Analysis findings table (row 1), the source at [placeholder —
facility/location] has exceeded the applicable emission limit, [placeholder —
NSPS/NESHAP subpart or Title V / SIP permit limit], at [placeholder — emission
unit/stack]. The source's own monitoring records show readings above the limit
on [placeholder — verified dates/date range] of [placeholder — figure/magnitude].

[⚠ ATTORNEY: state and support the ongoing/recurring character of the violations
consistent with controlling circuit law — § 304(a)(1) requires a good-faith
allegation of an ongoing or intermittently recurring violation, not a wholly past
one. This characterization is a legal judgment for counsel, not the agent; see the
precedent landscape.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[✓] Statutory basis (CAA § 304(a)(1), 42 U.S.C. § 7604(a)(1); notice under
    § 304(b)(1), 42 U.S.C. § 7604(b)(1))
[⚠ needed] Identity and address of the notifying party
[⚠ needed] Identity of the alleged violator (owner/operator if different)
[⚠ needed] The specific emission standard, limitation, or order violated, with
    its statutory/regulatory hook
[⚠ needed] The activity, location (facility, emission unit/stack), and dates of
    the violation, drawn from the monitoring record — do not allege unsupported dates
[⚠ needed] Permit / standard identifier(s) (Title V permit number, NSPS/NESHAP subpart)
[⚠ needed] The ongoing/recurring characterization under controlling circuit law
[⚠ needed] Service on the alleged violator, the EPA Administrator, AND the State
    air agency per 40 C.F.R. Part 54 (certified mail / postmark date)
[⚠ needed] Signature of the responsible attorney

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: needed — notifying-party identity; violator's legal name; the exact
  emission limit and its statutory/regulatory basis; dates/figures from the
  monitoring record; do not allege a date or magnitude the record does not support]
- [⚠ ATTORNEY: make the ongoing/recurring-violation characterization under
  controlling circuit law — § 304(a)(1) requires a good-faith allegation of an
  ongoing or intermittently recurring violation, not wholly past conduct]
- [⚠ ATTORNEY: assess whether the immediate-suit exception applies — for violations
  of § 111 (NSPS) or § 112 (HAP) standards, and under § 7412(i)(3)(A)/(f)(4) or an
  order under § 7413(a), the 60-day wait may not be required]
- [⚠ ATTORNEY: confirm no diligent-prosecution bar — that EPA or the State has not
  commenced and is not diligently prosecuting a civil action for these violations,
  which would foreclose the citizen suit]
- [⚠ ATTORNEY: currency — the emission standard verified via get_current_regulation
  (eCFR, unofficial-but-current; the operative text is the annual GPO CFR); confirm
  the standard, averaging period, and any SSM provisions remain in force]

DEADLINE NOTE
- CAA § 304(b)(1), 42 U.S.C. § 7604(b)(1), requires 60 days' written notice — to the
  alleged violator, the EPA Administrator, and the State — before filing a § 304(a)(1)
  emission-violation action. This is a fact for counsel to verify and a clock for
  counsel to track; this software does not track it. Whether the § 111/§ 112
  immediate-suit exception removes the 60-day wait, and whether the
  diligent-prosecution bar forecloses the suit, are for counsel to assess (see flags).
```

**Handoff ↔ Precedent Retrieval.** The flag *"make the ongoing/recurring-violation
characterization under controlling circuit law"* is a legal question the draft refuses to resolve.
It becomes a precedent request.

---

## Stage 3 — Precedent Retrieval (answering the draft's flag)

*Input:* the draft's ongoing-violation flag. *Output:* the controlling-law landscape.

```
# Precedent: does § 304(a)(1) require a good-faith allegation of an ONGOING violation?  [forum: not yet fixed — flag]
Retrieved: [2026-05-31]  |  Currency check: [FLAGS]

## Controlling authority
| Case | Court / year | Jurisdiction & weight | Holding (plain) | Current status |
|---|---|---|---|---|
| Gwaltney of Smithfield, Ltd. v. Chesapeake Bay Found., Inc., 484 U.S. 49 (1987) | U.S. 1987 | U.S. — binding, but a CLEAN WATER ACT case | Under the CWA citizen-suit provision (§ 505), a citizen suit requires a good-faith allegation of a continuous or intermittent (ongoing) violation, not one wholly in the past | CURRENT (verified via verify_citation; CWA, not CAA — cross-statute caveat below) |

## What the rule is (not how it applies to you)
A citizen suit against a violator generally requires a good-faith allegation that the violation is
ongoing — continuous or intermittently recurring — rather than wholly past. Gwaltney states that
framework for the Clean Water Act's citizen-suit provision. Whether the same ongoing-violation
requirement governs a Clean Air Act § 304(a)(1) suit, and exactly how a given circuit defines
"ongoing" for repeated emission exceedances, is a distinct question: § 304(a)(1) is a different
statute with its own text and its own body of case law, and courts have not uniformly imported
Gwaltney wholesale. The threshold question is whether the documented exceedance pattern supports a
good-faith ongoing-violation allegation under the law of the chosen forum.

## For the human deciding
- This is the legal landscape, not a prediction. Whether a specific exceedance record supports a
  § 304(a)(1) ongoing-violation allegation in a specific forum is a judgment for a licensed attorney
  applying it to specific facts.
- Cross-statute caveat: Gwaltney is a CLEAN WATER ACT decision construing CWA § 505. It is cited
  here only for the GENERAL citizen-suit ongoing-violation framework. Do NOT treat it as a CAA
  holding. [⚠ ATTORNEY: identify and verify (via verify_citation) the controlling CAA § 304(a)(1)
  ongoing-violation precedent for the chosen circuit; the CAA-specific rule is UNVERIFIED here and
  must not be presented as settled.]
- Currency flags: Gwaltney CURRENT (verified via verify_citation — a confirmation the citation
  resolves to a real published case, not a promise it remains good law or that it controls under the
  CAA; read the subsequent history). The CAA ongoing-violation question is forum-dependent and
  UNVERIFIED here.
- Jurisdiction gaps: forum not yet fixed; pin the circuit before relying on any application.
```

**Handoff → the human, and → Plain-Language.** The landscape attaches to the draft's flag for the
attorney; meanwhile the pathway is translated for the people who have to decide whether to pursue it.

---

## Stage 4 — Plain-Language

*Input:* the pathway. *Output:* a lay explanation.

```
## What this is
A way for a member of the public to give formal notice that a factory, power plant, or refinery is
breaking a federal air-pollution limit. When a source emits more than its limit allows, a citizen
can sometimes sue it under the Clean Air Act — but only after sending notice first.

## What it asks of you
- Point to a specific, federally enforceable emission limit (a national standard or a permit limit).
- Show the source went over that limit — usually from the source's own monitoring records.
- Show the problem is ongoing or keeps recurring, not just a single past event.
- Give written notice — for this kind of Clean Air Act claim, 60 days — to the source, the EPA, and
  the State before filing.

## How high the bar is
Showing a reading above a limit can be the easy part. The harder questions — whether the readings
are true violations after the standard's averaging rules, whether the violation is "ongoing,"
whether an agency is already enforcing (which can block a citizen suit), whether you have standing,
and which court — are real barriers a lawyer must weigh.

## A plain example
Imagine a cement plant's own pollution monitors record dust or sulfur readings above its permit
limit, again and again, over many months. That recurring pattern is the kind of thing this pathway
is built for.

## The clock
There is a strict 60-day notice step — to the source, the EPA, and the State — before filing, and
other deadlines may apply. Confirm every date with a lawyer right away; this software does not
track them.

## Your next step
Talk to counsel. A local environmental law clinic or legal aid office can help you weigh whether
this pathway fits.

This explains how the law works in general. It is not advice about your situation,
and it does not mean you have a case — only a lawyer who reviews your specific facts can tell you that.
```

---

## Terminal node — the human attorney

The package — findings table, flagged draft, precedent landscape, plain-language explainer — stops
here. OSED drafts; **a licensed attorney decides** whether the readings are violations under the
standard's own rules, whether the violation is ongoing, whether an enforcement bar applies, whether
standing exists, which forum, and whether to send or file anything. Nothing above is a
recommendation to sue or a prediction of success.
