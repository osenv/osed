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

## Stage 5 — Deadline Complaint (after the notice period runs)

*Input:* the findings table (row 1) and the served § 505(a)(2) notice, the 60-day period having run
with no agency action. *Output:* a flagged DRAFT complaint.

```
================ DRAFT — ATTORNEY REVIEW REQUIRED ================
This is a scaffold, not a filing. A licensed attorney must review,
complete, verify, and sign under FRCP 11 before any filing.
Doctrinal-currency check: [FLAGS below]
==================================================================

IN THE UNITED STATES DISTRICT COURT FOR THE [⚠ ATTORNEY: confirm district and venue]

[placeholder — plaintiff], Plaintiff, v. [placeholder — EPA Administrator, in official
capacity], Defendant.   Civil Action No. [placeholder]

COMPLAINT FOR DECLARATORY AND INJUNCTIVE RELIEF
(Failure to perform a nondiscretionary duty — CWA § 505(a)(2); § 304(m) effluent-guidelines plan)

NATURE OF THE ACTION
1. This is a citizen suit under CWA § 505(a)(2), 33 U.S.C. § 1365(a)(2), to compel the
   Administrator to perform a nondiscretionary duty the agency missed by its statutory deadline.

JURISDICTION AND VENUE
2. This Court has jurisdiction under 28 U.S.C. § 1331 and CWA § 505(a), 33 U.S.C. § 1365(a).
   [⚠ ATTORNEY: confirm venue (e.g., 28 U.S.C. § 1391(e)) for the chosen forum.]
3. The § 505(b) notice was served on the Administrator on [placeholder — date] and the 60-day
   period has run. [⚠ ATTORNEY: confirm the notice was served per 40 C.F.R. Part 135 and the
   period has run before filing.]

PARTIES
4. Plaintiff [placeholder] is [placeholder — concrete injury-in-fact traceable to the missed plan
   and redressable by an order]. [⚠ ATTORNEY: standing (injury-in-fact, causation, redressability)
   is jurisdictional and the court's to decide — plead the elements; do not assert standing is
   established.]
5. Defendant is the Administrator of the U.S. EPA, sued in their official capacity.

STATUTORY BACKGROUND
6. CWA § 304(m)(1)(A), 33 U.S.C. § 1314(m), requires EPA to publish a biennial effluent-guidelines
   plan. [⚠ ATTORNEY: confirm the duty is nondiscretionary and the deadline computation.]

FACTUAL ALLEGATIONS
7. The last plan issued on [placeholder — date from the record]; no plan has issued in the
   [placeholder] years since. [⚠ ATTORNEY: do not allege a date the record does not support.]

CLAIM FOR RELIEF — COUNT I: Failure to Perform a Nondiscretionary Duty
8. EPA's failure to publish the biennial plan by the statutory deadline violates a nondiscretionary
   duty enforceable under § 505(a)(2).

PRAYER FOR RELIEF
WHEREFORE, Plaintiff requests that the Court: (a) declare the Administrator in violation of
§ 304(m); (b) order the Administrator to publish the plan by a date certain; (c) retain
jurisdiction to ensure compliance; (d) award costs and reasonable attorney and expert witness fees
under 33 U.S.C. § 1365(d); and (e) grant any other just relief.

Respectfully submitted,
[placeholder — counsel name, bar number (if represented), firm, address, phone, email; or pro se
filer name and address]
[⚠ ATTORNEY: signature block — responsible attorney must review and sign under FRCP 11.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[⚠ needed] Caption: proper district/division and parties
[✓] Jurisdiction (28 U.S.C. § 1331; CWA § 505(a), 33 U.S.C. § 1365(a))
[⚠ needed] Venue for the chosen forum
[⚠ needed] Standing allegations (injury, causation, redressability) — pleaded, not asserted
[⚠ needed] Notice precondition satisfied (§ 505(b) notice served on the Administrator; 60-day period run)
[⚠ needed] The nondiscretionary duty, deadline, and missed-deadline facts from the record

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: confirm jurisdiction, venue, and that standing is pleaded (not asserted) — it is the court's to decide]
- [⚠ ATTORNEY: confirm the § 505(b) notice was served on the Administrator and the 60-day period ran before filing]
- [⚠ ATTORNEY: confirm § 304(m) is a nondiscretionary duty and the deadline computation]
- [⚠ ATTORNEY: needed — party identities, the last-plan date, and the years elapsed, from the record]

DEADLINE NOTE
- The § 505(b) pre-suit notice must already be satisfied before filing; this complaint seeks an
  order compelling action by a date certain (a deadline-suit remedy), not unreasonable-delay
  relief. This software tracks no clock.
```

**Handoff → the human.** The complaint joins the package; nothing here decides standing, forum, or
whether to file — those remain for counsel.

---

## Stage 6 — Consent Decree (negotiated resolution)

*Input:* the filed § 505(a)(2) complaint (Stage 5) and the parties' decision to resolve by agreement
rather than litigate to judgment. *Output:* a flagged DRAFT consent-decree scaffold — structure only;
the parties negotiate every term.

```
================ DRAFT — ATTORNEY REVIEW REQUIRED ================
This is a scaffold, not an agreement. It proposes no terms. Every term
below is for the parties and their counsel to negotiate. A consent decree
is not effective until lodged, published for public comment, and entered
by the court. Doctrinal-currency check: [FLAGS below]
==================================================================

IN THE UNITED STATES DISTRICT COURT FOR THE [⚠ ATTORNEY: confirm district]

[placeholder — plaintiff], Plaintiff, v. [placeholder — EPA Administrator, in
official capacity], Defendant.   Civil Action No. [placeholder]

[PROPOSED] CONSENT DECREE

WHEREAS, Plaintiff filed this action under CWA § 505(a)(2), 33 U.S.C. § 1365(a)(2),
alleging EPA failed to perform the nondiscretionary duty to publish the § 304(m)
biennial effluent-guidelines plan by its statutory deadline;

WHEREAS, the Parties wish to resolve this action without further litigation and
without any admission of law, fact, or liability [⚠ ATTORNEY: the no-admission
framing is a negotiated term];

NOW, THEREFORE, it is STIPULATED and AGREED by the Parties, and ORDERED, ADJUDGED,
and DECREED by the Court, as follows:

1. JURISDICTION. The Court has jurisdiction under 28 U.S.C. § 1331 and CWA § 505(a),
   33 U.S.C. § 1365(a). [⚠ ATTORNEY: confirm.]

2. DEFINITIONS. [placeholder — defined terms used in this Decree, e.g., "the Plan,"
   "Day," "Effective Date."] [⚠ ATTORNEY: the defined terms are a negotiated drafting
   choice; the software proposes none.]

3. COMPLIANCE SCHEDULE. The Administrator shall publish the § 304(m) plan by
   [placeholder — agreed date]. [⚠ ATTORNEY: negotiated term — the Parties set the
   schedule; the software does not propose dates.]

4. NO ADMISSION. This Decree is not an admission of law, fact, or liability by any
   Party. [⚠ ATTORNEY: negotiated term.]

5. REPORTING. [placeholder — agreed progress-reporting obligations.] [⚠ ATTORNEY:
   negotiated term.]

6. MODIFICATION / FORCE MAJEURE. [placeholder — agreed modification and good-cause /
   force-majeure terms.] [⚠ ATTORNEY: negotiated term.]

7. DISPUTE RESOLUTION. [placeholder — agreed dispute-resolution procedure.]
   [⚠ ATTORNEY: negotiated term.]

8. COSTS AND FEES. [placeholder — agreed costs and attorney/expert fees, or a
   reservation under 33 U.S.C. § 1365(d).] [⚠ ATTORNEY: negotiated term.]

9. PUBLIC COMMENT AND ENTRY. The Parties shall lodge this Decree and, after the
   public-comment period, move for entry. [⚠ ATTORNEY: confirm the applicable
   comment/entry procedure (e.g., 28 C.F.R. § 50.7); the Decree is not effective
   until the Court enters it after finding it fair, reasonable, and consistent with
   the statute.]

10. RETENTION OF JURISDICTION. The Court shall retain jurisdiction to enforce this
    Decree. [⚠ ATTORNEY: the scope of retention is a negotiated term.]

11. EFFECTIVE DATE / TERMINATION. [placeholder — agreed effective date and
    termination provisions.] [⚠ ATTORNEY: negotiated term.]

AGREED:
[placeholder — plaintiff's counsel: name, bar number, firm, address]
[placeholder — U.S. Department of Justice / EPA counsel for Defendant]
[⚠ ATTORNEY: signature blocks — all Parties and their counsel must review and sign.]

SO ORDERED this [placeholder — date of entry].
______________________________
United States District Judge
[⚠ ATTORNEY: the Court enters the Decree; do not present it as entered.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[⚠ needed] Caption and parties (from the complaint)
[⚠ needed] Recitals: the suit and the alleged nondiscretionary duty
[⚠ needed] Definitions — negotiated drafting choice
[⚠ needed] Compliance schedule — negotiated dates
[✓] No-admission clause (negotiated)
[✓] Retention of jurisdiction
[⚠ needed] Public-comment / entry procedure for this matter
[⚠ needed] Costs and fees — negotiated
[⚠ needed] Signatures of all Parties and counsel; Court entry

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: every term in this Decree is a negotiated term — the Parties and their counsel set the schedule, fees, no-admission framing, modification, dispute-resolution, and termination terms; the software proposes none]
- [⚠ ATTORNEY: confirm the public-comment and entry procedure (e.g., 28 C.F.R. § 50.7); the Decree is not effective until the Court enters it]
- [⚠ ATTORNEY: the Court enters a consent decree only on finding it fair, reasonable, and consistent with the statute — entry is not automatic]
- [⚠ ATTORNEY: needed — party identities, the agreed compliance date, and all negotiated terms, from the record and the negotiation]

DEADLINE NOTE
- A consent decree is lodged, published for public comment, and entered by the Court before it is
  effective; the compliance schedule and every other term are negotiated by the Parties. This
  software proposes no term and tracks no clock.
```

**Handoff → the human.** The scaffold gives the Parties a structure to negotiate within; it decides
nothing. Counsel negotiate every term and shepherd the Decree through comment and entry.

---

## Terminal node — the human attorney

The package — findings table, flagged notice, precedent landscape, plain-language explainer, the
flagged complaint, **and the consent-decree scaffold** — stops here. OSED drafts; **a licensed attorney decides** whether the duty
is enforceable, whether standing exists, which forum, and whether to send or file anything. Nothing
above is a recommendation to sue or a prediction of success.
