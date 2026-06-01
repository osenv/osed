# Consent-Decree Settlement Scaffold — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the deadline/duty-suit consent decree as one statute-agnostic template (`templates/consent-decree-deadline.md`), wire it into `drafting`, and extend the CWA §304(m) deadline example with a "Stage 6 — Consent Decree" proven by a drafting eval fixture.

**Architecture:** The template follows OSED house style adapted to a consent decree (both a contract and a court order). Its defining rule: a consent decree is a negotiated agreement, so the scaffold supplies STRUCTURE ONLY — every substantive term is a `[placeholder]` carrying a `[⚠ ATTORNEY: negotiated term — the parties set this; the software does not propose it]` flag ("terms scaffolded-not-proposed"). The example/fixture mirror the existing drafting stages and add a `negotiated-term-flagged` eval check that mechanically enforces this.

**Tech Stack:** Markdown (template, skill, example), JSON fixtures, pytest (`osed_evals`), and the `osed_connectors` regulatory connector (run from its `.venv` for the one regulation check).

**Spec:** `docs/specs/consent-decree-scaffold-design.md`. **Branch:** `consent-decree-scaffold` (already created off merged `main`).

---

## Verified-before-drafting facts

- The decree itself cites the underlying suit's authorities (CWA §505(a)(2) / 33 U.S.C. §1365(a)(2), jurisdiction §1331 + §1365(a), fees §1365(d)) — already verified during the deadline-complaint work; the decree's recitals reuse them.
- The one NEW external authority is the **public-comment/entry procedure** — illustratively **28 C.F.R. §50.7** (DOJ's notice-of-proposed-consent-decree rule). The template FLAGS it ("confirm the applicable procedure") rather than asserting it. Task 0 confirms §50.7 exists/current so the illustrative reference is not wrong.
- There is **no statutory clock to compute** here — every term (schedule dates, fees, modification) is negotiated. The agent proposes none.

---

## File structure

**Create:**
- `templates/consent-decree-deadline.md` — the statute-agnostic deadline-suit consent-decree scaffold.
- `evals/fixtures/drafting/consent-decree-deadline.json` (+ `.out.md`).

**Modify:**
- `skills/drafting/SKILL.md` — replace the consent-decree roadmap row; add a "negotiated instrument" sentence.
- `docs/examples/cwa-304m-deadline-suit.md` — append Stage 6; update the Terminal node.
- `evals/tests/test_golden_examples.py` — register the consent-decree fixture.
- `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md` — mark roadmap item 5 done.

**No change needed:** `evals/src/osed_evals/markers.py` (the decree reuses the drafting markers); `.github/workflows/evals.yml` (`templates/**` + `evals/**` already covered).

---

## Task 0: Confirm the comment/entry procedure reference (light gate)

**Files:** none — produces one verified fact carried into Tasks 1 and 4.

- [ ] **Step 1: Confirm the connector venv**
```bash
cd connectors/regulatory && ls .venv/bin/python && cd ../..
```
Expected: a path. If missing: `cd connectors/regulatory && python3 -m venv .venv && .venv/bin/pip install -e . && cd ../..`.

- [ ] **Step 2: Pull 28 C.F.R. §50.7 (DOJ notice of proposed consent decrees)**
```bash
cd connectors/regulatory && .venv/bin/python -c "from osed_connectors.clients import ecfr; r=ecfr.get_current_text(title=28, part='50', section='50.7'); print(r.get('found'), r.get('source_url'), r.get('source_current_as_of')); print(str(r.get('result'))[:1200])"; cd ../..
```
Expected: `found` True; the text is DOJ's rule on publishing notice of proposed consent judgments/decrees for public comment. If `found` is False, that itself is the finding — the template then flags the comment procedure generically ("confirm the applicable procedure") WITHOUT naming §50.7 as a certainty. Record the result either way. (If the eCFR host errors, note it; do not retry endlessly — the reference is flag-grade, not asserted.)

- [ ] **Step 3: Record** in your report whether §50.7 resolved and its `source_current_as_of`. No commit (no files changed).

---

## Task 1: The consent-decree template (`templates/consent-decree-deadline.md`)

**Files:**
- Create: `templates/consent-decree-deadline.md`
- Reference (read first): `templates/cwa-505-deadline-complaint.md` (house style + the suit this settles) and `templates/cwa-505-notice-of-intent.md`.

- [ ] **Step 1: Draft the template**

Six sections, house style adapted to a consent decree:

1. **Title + DRAFT-scaffold banner** (`>` blockquote) — use the EXACT phrase `DRAFT SCAFFOLD — NOT AN AGREEMENT, NOT FOR LODGING OR ENTRY`; name it a deadline/duty-suit consent-decree scaffold; state it **proposes no terms** — every term is for the parties and their counsel to negotiate; it is not effective until lodged, published for public comment, and entered by the court; point to `../DISCLAIMER.md`.
2. **"Why the form matters"** — a consent decree is both a contract and a court order, binding both parties and enforceable by the court; the agent supplies structure only; every negotiated term is the parties' to set; the court enters it only after the public-comment process and a fairness/reasonableness/statutory-consistency review. Include:
   `> [⚠ ATTORNEY: every term in this scaffold is a negotiated term — the parties and their counsel set the schedule, fees, no-admission framing, and all other terms; the software proposes none. Confirm the applicable lodging/comment/entry procedure (e.g., 28 C.F.R. § 50.7); the decree is not effective until the court enters it.]`
3. **Required-elements checklist** (`- [ ]`; each present or flagged):
   - Caption: same court/parties as the complaint `[⚠ ATTORNEY: confirm court and parties]`
   - WHEREAS recitals: the pending suit; the alleged nondiscretionary duty; intent to resolve **without admission of law, fact, or liability** `[⚠ ATTORNEY: the no-admission framing is a negotiated term]`
   - Definitions
   - The court's jurisdiction and authority to enter the decree
   - **Compliance schedule** — agreed date(s) for the duty `[placeholder]` `[⚠ ATTORNEY: negotiated term — the parties set the schedule; the software does not propose dates]`
   - **No-admission-of-liability** clause `[⚠ ATTORNEY: negotiated term]`
   - Reporting / progress obligations `[⚠ ATTORNEY: negotiated term]`
   - Modification / good-cause extension / force-majeure `[⚠ ATTORNEY: negotiated term]`
   - Dispute-resolution procedure `[⚠ ATTORNEY: negotiated term]`
   - **Retention of jurisdiction** by the court to enforce
   - Costs and attorney/expert fees `[placeholder]` `[⚠ ATTORNEY: negotiated term]`
   - **Lodging → public comment → entry** clause `[⚠ ATTORNEY: confirm the comment/entry procedure (e.g., 28 C.F.R. § 50.7); not effective until entered]`
   - Effective date / termination `[⚠ ATTORNEY: negotiated term]`
   - Signatures of all parties and counsel; a `SO ORDERED` court-entry line
4. **DRAFT body** (fenced ``` block): the decree — caption with `[placeholder]` parties and `Civil Action No. [placeholder]`; a `[PROPOSED] CONSENT DECREE` title; `WHEREAS` recitals (the suit, the alleged duty, the no-admission intent with its flag); a `NOW, THEREFORE, it is STIPULATED ... and ORDERED ... DECREED` clause; numbered sections — `1. JURISDICTION`; `2. COMPLIANCE SCHEDULE` (`[placeholder]` date + negotiated-term flag); `3. NO ADMISSION` (negotiated-term flag); `4. REPORTING`; `5. MODIFICATION / FORCE MAJEURE`; `6. DISPUTE RESOLUTION`; `7. COSTS AND FEES`; `8. PUBLIC COMMENT AND ENTRY` (flag the procedure + not-effective-until-entered + the court's fairness review); `9. RETENTION OF JURISDICTION` (the court retains jurisdiction to enforce); `10. EFFECTIVE DATE / TERMINATION` — every substantive section a `[placeholder]` + `[⚠ ATTORNEY: negotiated term ...]`; an `AGREED:` signature area with `[placeholder]` counsel blocks for both parties and a flag; a `SO ORDERED` / `United States District Judge` entry line with `[⚠ ATTORNEY: the court enters the decree; do not present it as entered]`.
   Do NOT use the literal phrases `ready to file`, `ready to lodge`, `ready for entry`, `filing-ready`, or `final and signed`.
5. **Negotiated-terms & comment/entry note** — restates: the schedule and all terms are negotiated; the decree is lodged + published for comment + entered before it is effective; the software proposes no term and tracks no clock.
6. **Consolidated attorney flags** — every term is negotiated (the parties set them, the software proposes none); the no-admission and retention clauses; the comment/entry procedure; the court's fairness/reasonableness/statutory-consistency review; counsel review and signature; court entry.

- [ ] **Step 2: Verify markers**
```bash
grep -c "DRAFT SCAFFOLD — NOT AN AGREEMENT, NOT FOR LODGING OR ENTRY" templates/consent-decree-deadline.md
grep -c "\[⚠ ATTORNEY:" templates/consent-decree-deadline.md
grep -c "\[placeholder" templates/consent-decree-deadline.md
grep -cE "\[⚠ ATTORNEY:[^]]*negotiated[^]]*\]" templates/consent-decree-deadline.md
grep -c "RETENTION OF JURISDICTION" templates/consent-decree-deadline.md
grep -ciE "ready to file|ready to lodge|ready for entry|filing-ready|final and signed" templates/consent-decree-deadline.md
```
Expected: banner ≥ 1; attorney-flag ≥ 8; placeholder ≥ 1; negotiated-term flag ≥ 3; RETENTION OF JURISDICTION ≥ 1; forbidden **= 0**.

- [ ] **Step 3: Suite green** — `cd evals && .venv/bin/pytest -q ; cd ..` (fallback `cd evals && python -m pytest -q`). Expected: all pass.

- [ ] **Step 4: Commit**
```bash
git add templates/consent-decree-deadline.md
git commit -m "consent decree: deadline-suit settlement scaffold template (terms scaffolded-not-proposed)"
```

---

## Task 2: Wire the drafting skill

**Files:** Modify `skills/drafting/SKILL.md`.

- [ ] **Step 1: Replace the roadmap row**

Replace:
```
| Memorialize a negotiated compliance schedule | Consent-decree settlement scaffold | (roadmap) |
```
with:
```
| Memorialize a negotiated compliance schedule (settle a deadline/duty suit) | Consent-decree settlement scaffold | `templates/consent-decree-deadline.md` |
```

- [ ] **Step 2: Add a sentence to the skill body**

Immediately after the "**Complaints are court filings.**" paragraph (added during the deadline-complaint work; it sits after the "## Choosing the instrument" table), add this paragraph:
```markdown
**Consent decrees are negotiated instruments.** A consent decree is both a contract and a court order. You supply the structure and flag every term — the compliance schedule, fees, the no-admission framing, modification and dispute-resolution terms — as the parties' to negotiate; you never propose a schedule date, a fee, or an admission. And a consent decree is court-entered only after public comment, so "drafted" ≠ "agreed" ≠ "effective."
```

- [ ] **Step 3: Verify + suite green**
```bash
grep -c "consent-decree-deadline.md" skills/drafting/SKILL.md          # >=1
grep -c "Consent decrees are negotiated instruments" skills/drafting/SKILL.md   # ==1
cd evals && .venv/bin/pytest -q ; cd ..
```
Expected: first ≥ 1; second = 1; all tests pass.

- [ ] **Step 4: Commit**
```bash
git add skills/drafting/SKILL.md
git commit -m "drafting: route the consent-decree scaffold to its template; mark decrees as negotiated instruments"
```

---

## Task 3: Docs — roadmap, README, CHANGELOG, CLAUDE

**Files:** `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`.

- [ ] **Step 1: `docs/architecture.md` roadmap item 5**

Replace:
```
5. **Consent-decree settlement scaffold** — the negotiated, court-enforceable schedule; teaches the system to generate settlement structure, not just complaints.
```
with:
```
5. **Consent-decree settlement scaffold** — done (`templates/consent-decree-deadline.md`). The negotiated resolution of a deadline/duty suit: a statute-agnostic scaffold whose every term is flagged for the parties to negotiate (the software proposes none), lodged and entered by the court after public comment. The violation-suit decree (penalties/injunctive measures) remains a possible future variant.
```

- [ ] **Step 2: `README.md` template tree**

Add the template to the `templates/` block so it reads (keeping `rulemaking-petition.md` last):
```
├── templates/
│   ├── cwa-505-notice-of-intent.md
│   ├── cwa-505-deadline-complaint.md
│   ├── consent-decree-deadline.md
│   ├── caa-304-emissions-notice.md
│   ├── caa-304-failure-to-act-notice.md
│   ├── caa-304-deadline-complaint.md
│   └── rulemaking-petition.md
```
(If the existing block's order differs slightly, just add `consent-decree-deadline.md` as a new line within the `templates/` block, keeping `rulemaking-petition.md` last.)

- [ ] **Step 3: `CHANGELOG.md` `## [Unreleased]`**

Under the existing `## [Unreleased]` heading (do NOT create a second one; merge into existing `### Added` / `### Changed` if present, else create them):
```markdown
### Added
- Consent-decree settlement scaffold (`templates/consent-decree-deadline.md`): the negotiated resolution of a deadline/duty suit, statute-agnostic, with every term flagged for the parties to negotiate (the software proposes none). A "Stage 6 — Consent Decree" was added to the CWA §304(m) worked example and registered as a drafting eval fixture.

### Changed
- `skills/drafting` routes the consent-decree scaffold to its template and marks decrees as negotiated instruments.
```

- [ ] **Step 4: `CLAUDE.md` roadmap note**

Find the Roadmap sentence (updated during the deadline-complaint work). It currently ends:
```
`templates/*-deadline-complaint.md`); the consent-decree scaffold is next.
```
Replace that tail so it reads:
```
`templates/*-deadline-complaint.md`, `templates/consent-decree-deadline.md`); the state ERA packets
are next.
```
(If the exact preceding text differs, ensure the sentence now lists the consent-decree template as shipped and names the state ERA packets as next.)

- [ ] **Step 5: Verify + commit**
```bash
grep -c "consent-decree-deadline\|Consent-decree settlement scaffold" README.md docs/architecture.md CHANGELOG.md CLAUDE.md
cd evals && .venv/bin/pytest -q ; cd ..
git add docs/architecture.md README.md CHANGELOG.md CLAUDE.md
git commit -m "docs: mark consent-decree scaffold shipped (roadmap, README tree, CHANGELOG, CLAUDE)"
```
Expected: each file ≥ 1; all tests pass.

**End of Phase A — the template is shippable. Phase B adds the worked-example stage and the eval net.**

---

## Task 4: Extend the CWA example with Stage 6

**Files:** Modify `docs/examples/cwa-304m-deadline-suit.md` (Stage 5 ends ~line 238; `## Terminal node` is ~line 240; current fence count 10).
Reference: `templates/consent-decree-deadline.md`.

- [ ] **Step 1: Insert Stage 6 just BEFORE the `## Terminal node — the human attorney` section**

Insert this section (it contains ONE fenced ``` block holding the decree — open before the `==== DRAFT` banner, close after the `DEADLINE NOTE` block — exactly like Stages 2/5). The `## Stage 6` heading, the `*Input:*/*Output:*` caption, the `**Handoff → the human.**` paragraph, and the `---` rule are OUTSIDE the fence:

```
## Stage 6 — Consent Decree (negotiated resolution)

*Input:* the filed § 505(a)(2) complaint (Stage 5) and the parties' decision to resolve by agreement
rather than litigate to judgment. *Output:* a flagged DRAFT consent-decree scaffold — structure only;
the parties negotiate every term.

[OPEN FENCE]
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

2. COMPLIANCE SCHEDULE. The Administrator shall publish the § 304(m) plan by
   [placeholder — agreed date]. [⚠ ATTORNEY: negotiated term — the Parties set the
   schedule; the software does not propose dates.]

3. NO ADMISSION. This Decree is not an admission of law, fact, or liability by any
   Party. [⚠ ATTORNEY: negotiated term.]

4. REPORTING. [placeholder — agreed progress-reporting obligations.] [⚠ ATTORNEY:
   negotiated term.]

5. MODIFICATION / FORCE MAJEURE. [placeholder — agreed modification and good-cause /
   force-majeure terms.] [⚠ ATTORNEY: negotiated term.]

6. DISPUTE RESOLUTION. [placeholder — agreed dispute-resolution procedure.]
   [⚠ ATTORNEY: negotiated term.]

7. COSTS AND FEES. [placeholder — agreed costs and attorney/expert fees, or a
   reservation under 33 U.S.C. § 1365(d).] [⚠ ATTORNEY: negotiated term.]

8. PUBLIC COMMENT AND ENTRY. The Parties shall lodge this Decree and, after the
   public-comment period, move for entry. [⚠ ATTORNEY: confirm the applicable
   comment/entry procedure (e.g., 28 C.F.R. § 50.7); the Decree is not effective
   until the Court enters it after finding it fair, reasonable, and consistent with
   the statute.]

9. RETENTION OF JURISDICTION. The Court shall retain jurisdiction to enforce this
   Decree. [⚠ ATTORNEY: the scope of retention is a negotiated term.]

10. EFFECTIVE DATE / TERMINATION. [placeholder — agreed effective date and
    termination provisions.] [⚠ ATTORNEY: negotiated term.]

AGREED:
[placeholder — plaintiff's counsel: name, bar number, firm, address]
[placeholder — U.S. Department of Justice / EPA counsel for Defendant]
[⚠ ATTORNEY: signature blocks — all Parties and their counsel must review and sign.]

SO ORDERED this ___ day of __________, ____.
______________________________
United States District Judge
[⚠ ATTORNEY: the Court enters the Decree; do not present it as entered.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[⚠ needed] Caption and parties (from the complaint)
[⚠ needed] Recitals: the suit and the alleged nondiscretionary duty
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
[CLOSE FENCE]

**Handoff → the human.** The scaffold gives the Parties a structure to negotiate within; it decides
nothing. Counsel negotiate every term and shepherd the Decree through comment and entry.

---
```
(Replace `[OPEN FENCE]` / `[CLOSE FENCE]` with a real triple-backtick line each.)

- [ ] **Step 2: Update the Terminal-node paragraph** — change the package artifact list to add the decree, e.g. "... plain-language explainer, the flagged complaint, **and the consent-decree scaffold** — stops here." Keep it ending at the human attorney.

- [ ] **Step 3: Verify markers**
```bash
grep -c "Stage 6 — Consent Decree" docs/examples/cwa-304m-deadline-suit.md            # ==1
grep -c "DRAFT — ATTORNEY REVIEW REQUIRED" docs/examples/cwa-304m-deadline-suit.md     # >=3 (Stage 2, 5, 6)
grep -c "RETENTION OF JURISDICTION" docs/examples/cwa-304m-deadline-suit.md            # >=1
grep -cE "\[⚠ ATTORNEY:[^]]*negotiated[^]]*\]" docs/examples/cwa-304m-deadline-suit.md # >=3
grep -ciE "ready to file|ready to lodge|ready for entry|filing-ready|final and signed" docs/examples/cwa-304m-deadline-suit.md  # ==0
grep -c '^```' docs/examples/cwa-304m-deadline-suit.md                                 # must be EVEN (12)
```
Expected as annotated.

- [ ] **Step 4: Suite green + commit**
```bash
cd evals && .venv/bin/pytest -q ; cd ..
git add docs/examples/cwa-304m-deadline-suit.md
git commit -m "examples: add Stage 6 consent decree to the CWA §304(m) example"
```

---

## Task 5: Consent-decree fixture + register

**Files:**
- Create: `evals/fixtures/drafting/consent-decree-deadline.json` (+ `.out.md`)
- Modify: `evals/tests/test_golden_examples.py`

- [ ] **Step 1: Create the `.out.md`** by extracting the Stage-6 fenced decree content from `docs/examples/cwa-304m-deadline-suit.md` (verbatim — from the `==== DRAFT` banner through the `DEADLINE NOTE` block). It MUST contain: `DRAFT — ATTORNEY REVIEW REQUIRED`, `Doctrinal-currency check:`, a `[⚠ ATTORNEY: ...]` flag whose text contains `negotiated`, `[placeholder]`, `REQUIRED-ELEMENTS CHECKLIST`, `CONSOLIDATED ATTORNEY FLAGS`, `DEADLINE NOTE`, `RETENTION OF JURISDICTION`. It MUST NOT contain `ready to file`, `ready to lodge`, `ready for entry`, `filing-ready`, or `final and signed`.

- [ ] **Step 2: Write the fixture JSON** `evals/fixtures/drafting/consent-decree-deadline.json` EXACTLY:
```json
{
  "skill": "drafting",
  "name": "consent-decree-deadline",
  "turns": [
    {"role": "user", "content": "The parties wish to resolve the filed §505(a)(2) deadline suit by agreement rather than litigate. From the complaint and findings, scaffold a consent decree setting a compliance schedule for the court to enter."}
  ],
  "transcript_file": "consent-decree-deadline.out.md",
  "checks": [
    {"id": "draft-banner", "kind": "contains", "invariant": 1, "target": "DRAFT — ATTORNEY REVIEW REQUIRED"},
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "attorney-flag-present", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*\\]"},
    {"id": "placeholder-for-missing-fact", "kind": "contains", "invariant": 4, "target": "[placeholder]"},
    {"id": "checklist-section", "kind": "contains", "invariant": 2, "target": "REQUIRED-ELEMENTS CHECKLIST"},
    {"id": "flags-section", "kind": "contains", "invariant": 2, "target": "CONSOLIDATED ATTORNEY FLAGS"},
    {"id": "deadline-section", "kind": "contains", "invariant": 2, "target": "DEADLINE NOTE"},
    {"id": "retention-section", "kind": "contains", "invariant": 2, "target": "RETENTION OF JURISDICTION"},
    {"id": "not-finalized", "kind": "forbidden", "invariant": 5, "patterns": ["ready to file", "ready to lodge", "ready for entry", "filing-ready", "final and signed"]},
    {"id": "negotiated-term-flagged", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*negotiated[^\\]]*\\]"},
    {"id": "terms-not-proposed", "kind": "judge", "invariant": 4, "criterion": "No specific compliance-schedule date, fee amount, or other negotiated term is invented or proposed; every such term is a bracketed placeholder flagged as the parties' to negotiate."}
  ]
}
```

- [ ] **Step 3: Register in `evals/tests/test_golden_examples.py`** — add to the `GOLDEN` list, after the `("drafting", "cwa-505-deadline-complaint"),` line:
```python
    ("drafting", "consent-decree-deadline"),
```
Change nothing else.

- [ ] **Step 4: Run targeted then full suite**
```bash
cd evals && .venv/bin/pytest tests/test_golden_examples.py -q
```
Expected: passes (one more than before). If a `contains`/`regex`/`forbidden` check fails, fix the `.out.md` to carry the exact marker (or remove a leaked forbidden phrase) — do NOT weaken the JSON. Then:
```bash
.venv/bin/pytest -q ; cd ..
```
Expected: full suite all pass (72 passed, 8 deselected).

- [ ] **Step 5: Commit**
```bash
git add evals/fixtures/drafting/consent-decree-deadline.* evals/tests/test_golden_examples.py
git commit -m "evals: register consent-decree-deadline drafting fixture"
```

---

## Task 6: Legal-soundness gate

**Files:** none necessarily — may produce small fixes.

- [ ] **Step 1: Terms scaffolded-not-proposed.** Confirm the template and the Stage-6 decree propose NO term — every schedule date, fee, and admission is `[placeholder]` carrying a `[⚠ ATTORNEY: ...negotiated...]` flag, and no specific date/figure is invented.
```bash
grep -rnE "\[⚠ ATTORNEY:[^]]*negotiated[^]]*\]" templates/consent-decree-deadline.md docs/examples/cwa-304m-deadline-suit.md
```
Expected: several hits in each. Read the COMPLIANCE SCHEDULE / COSTS sections and confirm no concrete date or dollar figure was filled in.

- [ ] **Step 2: Required clauses present + flagged.** Confirm both artifacts contain a **no-admission** clause, a **retention of jurisdiction** clause, and a **lodging → public comment → entry** clause that (a) names the procedure as flag-grade ("e.g., 28 C.F.R. § 50.7"), (b) states the decree is **not effective until entered**, and (c) notes the court's **fair / reasonable / consistent with the statute** review.
```bash
grep -rin "no admission\|retention of jurisdiction\|public comment\|not effective until\|fair, reasonable" templates/consent-decree-deadline.md docs/examples/cwa-304m-deadline-suit.md
```

- [ ] **Step 3: Not presented as agreed/entered.** Confirm neither artifact states the decree is agreed, executed, or entered; the `SO ORDERED` line carries the "the court enters the decree; do not present it as entered" flag. Confirm no forbidden finalization phrase:
```bash
grep -rinE "ready to file|ready to lodge|ready for entry|filing-ready|final and signed" templates/consent-decree-deadline.md docs/examples/cwa-304m-deadline-suit.md && echo "INVESTIGATE" || echo "OK none"
```

- [ ] **Step 4: Verify any case cite** via `verify_citation` (the decree is expected to be statute/structure-based with no case cites — confirm none slipped in unverified). Re-confirm 28 C.F.R. §50.7 from Task 0 if the template names it.

- [ ] **Step 5: Full suite green.**
```bash
cd evals && .venv/bin/pytest -q ; cd ..
```
Expected: 72 passed, 8 deselected.

- [ ] **Step 6: Commit any fixes** (NO Claude attribution), or record "gate passed clean — no changes" if none.

---

## Task 7: Finish the branch

- [ ] **Step 1: Full suite one last time** — `cd evals && .venv/bin/pytest -q ; cd ..` (expect 72 passed, 8 deselected).
- [ ] **Step 2: Confirm no Claude attribution** — `git log origin/main..HEAD --format="%b" | grep -i "co-authored-by\|claude\|🤖" || echo OK`.
- [ ] **Step 3: Invoke `superpowers:finishing-a-development-branch`** and present the standard options (expected: Push and create a Pull Request; PR body carries NO Claude attribution).

---

## Self-review notes (author)

- **Spec coverage:** Component 1 → Task 1; Component 2 → Task 2; Component 3 → Task 4; Component 4 → Task 5; Component 5 → Task 3; Component 6 (legal gate) → Task 0 + Task 6.
- **The "terms scaffolded-not-proposed" invariant** is enforced both in prose and mechanically: the `negotiated-term-flagged` regex check in the fixture requires a `[⚠ ATTORNEY: …negotiated…]` flag to exist in the drafted decree, and the `terms-not-proposed` judge check guards against an invented date/figure.
- **No new marker / no CI change** — the decree reuses the drafting markers; `templates/**` and `evals/**` are already CI `paths`.
- **Type/name consistency:** the fixture `name` (`consent-decree-deadline`) matches its filename, `transcript_file`, and the `GOLDEN` tuple; the fixture adds a `retention-section` (`RETENTION OF JURISDICTION`) and a `negotiated-term-flagged` regex beyond the standard drafting set; the `negotiated` regex uses `[^\\]]*negotiated[^\\]]*` (escaped in JSON).
- **Forbidden-phrase trap:** a decree is *about* lodging/entry, so the plan forbids the literal phrases `ready to lodge`/`ready for entry`/`ready to file`/`filing-ready`/`final and signed` (grep == 0) in the template and example to keep the `not-finalized` check honest; the body uses "lodge", "move for entry", "not effective until ... enters" instead.
- **Document integrity:** Task 4 adds one fenced block; the plan verifies the `^``` ` count stays EVEN (12).
