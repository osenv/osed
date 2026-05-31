# Deadline-Complaint Instrument — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the federal deadline complaint (citizen-suit "failure to perform a nondiscretionary duty" pleading) as two statute-concrete templates (CWA §505(a)(2), CAA §304(a)(2)), wire them into `drafting`, and extend the two existing deadline worked-examples with a complaint stage proven by eval fixtures.

**Architecture:** Templates follow the OSED house style (DRAFT banner → why-the-form-matters → required-elements checklist → DRAFT body → precondition/deadline note → consolidated attorney flags), adapted to an FRCP 8/10/11 complaint. The judgment line is drawn harder: standing, jurisdiction, and venue are pleaded as flagged allegations and never asserted. Examples and fixtures mirror the existing deadline examples (`docs/examples/cwa-304m-deadline-suit.md`, `docs/examples/caa-304-failure-to-act-suit.md`) and their drafting fixtures.

**Tech Stack:** Markdown (templates, skills, examples), JSON fixtures, pytest (`osed_evals`), and the `osed_connectors` regulatory connector (run from its `.venv` for statutory verification).

**Spec:** `docs/specs/deadline-complaint-design.md`. **Branch:** `deadline-complaint` (already created off merged `main`).

---

## Verified-before-drafting facts (Task 0 re-confirms; never write a citation from memory)

- **CWA §505 / 33 U.S.C. §1365:** §1365(a) grants district-court jurisdiction over citizen suits; §1365(a)(2) is the failure-to-act track against the Administrator; **§1365(b)(2)** is the notice precondition for an (a)(2) action; §1365(d) is the costs/fees provision. The existing `cwa-304m-deadline-suit.md` asserts a "60-day §505(a)(2) notice" — Task 0 confirms this against §1365(b)(2) and corrects in place only if the statute does not bear it out.
- **CAA §304 / 42 U.S.C. §7604:** §7604(a) grants district-court jurisdiction; §7604(a)(2) is the failure-to-act track; **§7604(b)(2)** is the 60-day-to-the-Administrator notice precondition (already verified during the CAA work); §7604(d) is the costs/fees provision.
- **Defendant** in both is the **EPA Administrator**. **Standing / jurisdiction / venue are flagged, never asserted.** The prayer seeks a **date-certain order**, not unreasonable-delay relief. The "180" string must not appear in the CAA artifacts.

---

## File structure

**Create:**
- `templates/cwa-505-deadline-complaint.md` — CWA §505(a)(2) deadline complaint.
- `templates/caa-304-deadline-complaint.md` — CAA §304(a)(2) deadline complaint.
- `evals/fixtures/drafting/cwa-505-deadline-complaint.json` (+ `.out.md`).
- `evals/fixtures/drafting/caa-304-deadline-complaint.json` (+ `.out.md`).

**Modify:**
- `skills/drafting/SKILL.md` — replace the deadline-complaint roadmap row with two template rows; add a court-filing sentence.
- `docs/examples/cwa-304m-deadline-suit.md` — append Stage 5; (conditionally) correct the §505(b) notice line.
- `docs/examples/caa-304-failure-to-act-suit.md` — append Stage 5.
- `evals/tests/test_golden_examples.py` — register the CWA complaint fixture.
- `evals/tests/test_caa_304_examples.py` — register the CAA complaint fixture.
- `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md` — mark roadmap item 4 done.

**No change needed:** `evals/src/osed_evals/markers.py` (complaints reuse the drafting markers); `.github/workflows/evals.yml` (`templates/**` + `evals/**` already covered).

---

## Task 0: Verify the jurisdiction grants + notice preconditions (gate before drafting)

**Files:** none — produces verified facts carried into Tasks 1–2 and 5/7.

- [ ] **Step 1: Confirm the connector venv**

Run:
```bash
cd connectors/regulatory && ls .venv/bin/python && cd ../..
```
Expected: a path. If missing: `cd connectors/regulatory && python3 -m venv .venv && .venv/bin/pip install -e . && cd ../..`.

- [ ] **Step 2: Pull CWA §505 (33 U.S.C. §1365) and read subsections (a), (b), (d)**

Run:
```bash
cd connectors/regulatory && .venv/bin/python -c "from osed_connectors.clients import govinfo; r=govinfo.get_uscode_section(title=33, section='1365'); print(r.get('found'), r.get('source_url'), r.get('source_current_as_of')); print(str(r.get('result'))[:2000])"; cd ../..
```
Expected: `found` True. Confirm: §1365(a) district-court jurisdiction; §1365(a)(2) failure-to-act-vs-Administrator track; **§1365(b)(2)** — whether an (a)(2) action requires 60 days' notice to the Administrator (and any immediate-suit exception, e.g. for §§1316/1317(a)); §1365(d) costs/fees. **Record whether the "60-day §505(a)(2) notice" the existing example asserts is borne out.** If GovInfo returns non-text, fall back to `WebFetch` on `https://www.law.cornell.edu/uscode/text/33/1365` and read subsection (b).

- [ ] **Step 3: Re-confirm CAA §304 (42 U.S.C. §7604) subsections (a), (b)(2), (d)**

Run:
```bash
cd connectors/regulatory && .venv/bin/python -c "from osed_connectors.clients import govinfo; r=govinfo.get_uscode_section(title=42, section='7604'); print(r.get('found')); print(str(r.get('result'))[:1600])"; cd ../..
```
Expected: `found` True; confirm §7604(a) district-court jurisdiction, §7604(a)(2) failure-to-act track, §7604(b)(2) 60-day notice to the Administrator, §7604(d) fees. (This re-confirms the CAA facts already used.)

- [ ] **Step 4: Record verified facts**

In the commit body (or carried into Task 1), record: the jurisdiction grant cite for each statute; the (a)(2) notice precondition for each (days + recipient + any immediate-suit exception); the fee-provision cite for each; and an explicit yes/no on whether the existing CWA example's 60-day §505(a)(2) assertion is correct (this drives Task 5's conditional correction).

- [ ] **Step 5: Commit (only if files changed — this task changes none)**

This task creates no files; skip the commit and carry the note into Task 1's commit body. Do NOT use `--allow-empty`.

---

## Task 1: CWA §505(a)(2) deadline-complaint template

**Files:**
- Create: `templates/cwa-505-deadline-complaint.md`
- Reference (read first): `templates/cwa-505-notice-of-intent.md` (house style), `templates/caa-304-failure-to-act-notice.md` (the failure-to-act sibling), and `docs/examples/cwa-304m-deadline-suit.md` (the matter + the §505(a)(2) notice it follows).

- [ ] **Step 1: Draft the template**

Produce a file with these six sections, modeled on the house style but adapted to a **federal complaint** (FRCP 8/10/11). Use the Task-0 verified facts; never write a citation from memory.

1. **Title + DRAFT-scaffold banner** (`>` blockquote) — use the EXACT phrase `DRAFT SCAFFOLD — NOT FOR FILING`; name it a CWA §505(a)(2) deadline complaint (failure to perform a nondiscretionary duty); a defective complaint is dismissable; **standing is jurisdictional**; FRCP 11 review/signature required before filing; point to `../DISCLAIMER.md`.
2. **"Why the form matters"** — a complaint must satisfy FRCP 8(a) (a short and plain statement of the grounds for jurisdiction, the claim, and the relief) and FRCP 11 (signed, non-frivolous); standing is jurisdictional and the court's to decide; the §505(b) pre-suit notice must already be satisfied. Include:
   `> [⚠ ATTORNEY: confirm jurisdiction (28 U.S.C. § 1331 and CWA § 505 / 33 U.S.C. § 1365(a)), venue, and that the § 505(b) notice was served and its period has run before filing.]`
3. **Required-elements checklist** (`- [ ]`; each present or flagged):
   - Caption: court and division `[⚠ ATTORNEY: confirm the proper court and venue]`; full party names; civil-action number `[placeholder]`
   - Jurisdiction: 28 U.S.C. § 1331 (federal question) + CWA § 505(a) / 33 U.S.C. § 1365(a) (citizen-suit grant)
   - Venue `[⚠ ATTORNEY: confirm venue (e.g., 28 U.S.C. § 1391(e) for an action against a federal agency/officer) for the chosen forum]`
   - Parties and **standing**: plaintiff's standing elements pleaded as allegations `[⚠ ATTORNEY: standing (injury-in-fact, causation, redressability) is jurisdictional and the court's to decide — plead the elements; do not assert standing is established]`; defendant (the EPA Administrator)
   - **Notice precondition satisfied**: the § 505(b) notice was served and its period ran `[⚠ ATTORNEY: confirm the notice was properly served and the statutory period has run before filing]`
   - The nondiscretionary duty + its statutory hook + the statutory deadline + the missed-deadline facts (from the findings table) `[⚠ ATTORNEY: confirm the duty is nondiscretionary and the deadline computation]`
   - Count I — Failure to Perform a Nondiscretionary Duty
   - Prayer for relief: declaratory judgment; a mandatory injunction/order compelling the action **by a date certain**; retention of jurisdiction; costs and attorney/expert fees under CWA § 505(d) / 33 U.S.C. § 1365(d); any other just relief
   - FRCP 11 signature block
4. **DRAFT body** (fenced ``` block): a complaint with these headed sections — `IN THE UNITED STATES DISTRICT COURT FOR THE [⚠ ATTORNEY: district]` caption with `[placeholder]` parties and `Civil Action No. [placeholder]`; `NATURE OF THE ACTION`; `JURISDICTION AND VENUE` (cite §1331 + §1365(a); venue flag); `PARTIES` (plaintiff standing-element allegations with the standing flag; defendant = Administrator); `STATUTORY BACKGROUND` (the nondiscretionary duty + §505(b) notice precondition, with the notice-satisfied flag); `FACTUAL ALLEGATIONS` (the duty, the deadline, the missed deadline — `[placeholder]` for record facts, with "do not allege unsupported dates" flag); `CLAIM FOR RELIEF — COUNT I: Failure to Perform a Nondiscretionary Duty`; `PRAYER FOR RELIEF` (the date-certain order, declaratory judgment, retention, fees under §1365(d)); a `Respectfully submitted,` signature block `[⚠ ATTORNEY: signature block — responsible attorney must review and sign under FRCP 11]`. Every gating doctrine is an inline `[⚠ ATTORNEY: ...]`; every fact is `[placeholder]`. Do NOT use the literal phrases "ready to file", "ready to serve", or "filing-ready".
5. **Precondition / deadline note** — the § 505(b) pre-suit notice must already be satisfied before filing; the complaint is the date-certain deadline-suit remedy (it seeks an order compelling action by a date, NOT unreasonable-delay relief); this software tracks no clock.
6. **Consolidated attorney flags** — gather every flag: jurisdiction/venue; standing; notice precondition; nondiscretionary-duty + deadline; fees provision; FRCP 11 review and sign.

- [ ] **Step 2: Verify markers**

Run from the worktree root:
```bash
grep -c "DRAFT SCAFFOLD — NOT FOR FILING" templates/cwa-505-deadline-complaint.md
grep -c "\[⚠ ATTORNEY:" templates/cwa-505-deadline-complaint.md
grep -c "\[placeholder" templates/cwa-505-deadline-complaint.md
grep -c "standing" templates/cwa-505-deadline-complaint.md
grep -c "1365" templates/cwa-505-deadline-complaint.md
grep -ciE "ready to file|ready to serve|filing-ready" templates/cwa-505-deadline-complaint.md
```
Expected: banner ≥ 1; attorney-flag ≥ 6; placeholder ≥ 1; standing ≥ 2; 1365 ≥ 2; the forbidden-phrase count **= 0**.

- [ ] **Step 3: Keep the suite green**

Run: `cd evals && .venv/bin/pytest -q ; cd ..` — Expected: all pass (no fixture references this file yet).

- [ ] **Step 4: Commit**

```bash
git add templates/cwa-505-deadline-complaint.md
git commit -m "deadline complaint: CWA §505(a)(2) template (federal complaint, standing/jurisdiction flagged)"
```

---

## Task 2: CAA §304(a)(2) deadline-complaint template

**Files:**
- Create: `templates/caa-304-deadline-complaint.md`
- Reference: `templates/cwa-505-deadline-complaint.md` (the sibling just created — match it section-for-section), `templates/caa-304-failure-to-act-notice.md` (the CAA notice it follows).

- [ ] **Step 1: Draft the template**

Same six-section FRCP-complaint structure as Task 1, adapted to **CAA §304(a)(2) / 42 U.S.C. §7604**:
- Banner: `DRAFT SCAFFOLD — NOT FOR FILING`; a CAA §304(a)(2) deadline complaint.
- Jurisdiction: 28 U.S.C. § 1331 + CAA § 304(a) / 42 U.S.C. § 7604(a).
- Notice precondition: the § 304(b)(2) 60-day notice to the Administrator was served and its period ran (verified fact).
- Fees: CAA § 304(d) / 42 U.S.C. § 7604(d).
- Defendant: the EPA Administrator. Standing/jurisdiction/venue flagged, not asserted. Prayer seeks a date-certain order.
- "180" must NOT appear. Same FRCP body sections and the same don't-use-"ready to file"/"ready to serve" rule.

- [ ] **Step 2: Verify markers**

```bash
grep -c "DRAFT SCAFFOLD — NOT FOR FILING" templates/caa-304-deadline-complaint.md
grep -c "\[⚠ ATTORNEY:" templates/caa-304-deadline-complaint.md
grep -c "standing" templates/caa-304-deadline-complaint.md
grep -c "7604" templates/caa-304-deadline-complaint.md
grep -c "180" templates/caa-304-deadline-complaint.md
grep -ciE "ready to file|ready to serve|filing-ready" templates/caa-304-deadline-complaint.md
```
Expected: banner ≥ 1; attorney-flag ≥ 6; standing ≥ 2; 7604 ≥ 2; **180 = 0**; forbidden = 0.

- [ ] **Step 3: Suite green**

Run: `cd evals && .venv/bin/pytest -q ; cd ..` — Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add templates/caa-304-deadline-complaint.md
git commit -m "deadline complaint: CAA §304(a)(2) template (federal complaint, standing/jurisdiction flagged)"
```

---

## Task 3: Wire the drafting skill

**Files:**
- Modify: `skills/drafting/SKILL.md`

- [ ] **Step 1: Replace the deadline-complaint roadmap row with two template rows**

In the "## Choosing the instrument" table, replace the line
`| Sue over a clearly missed statutory deadline | Deadline complaint | (roadmap — scaffold from Gap Analysis output) |`
with:
```markdown
| Sue over a clearly missed statutory deadline (CWA citizen suit) | CWA §505(a)(2) deadline complaint | `templates/cwa-505-deadline-complaint.md` |
| Sue over a clearly missed statutory deadline (CAA citizen suit) | CAA §304(a)(2) deadline complaint | `templates/caa-304-deadline-complaint.md` |
```

- [ ] **Step 2: Add a court-filing sentence to the skill body**

Immediately after the "## Choosing the instrument" table (before "## The required-elements rule"), add this paragraph:
```markdown
**Complaints are court filings.** A deadline complaint is filed in federal court under FRCP 8/10/11, so the bar is higher than a pre-suit notice: standing (injury-in-fact, causation, redressability) is jurisdictional, and subject-matter jurisdiction and venue are threshold questions. You plead these as flagged allegations — you never assert that standing exists or that the court has jurisdiction. The pre-suit notice must already be satisfied before a complaint is drafted for filing.
```

- [ ] **Step 3: Verify + suite green**

```bash
grep -c "deadline-complaint.md" skills/drafting/SKILL.md
grep -c "Complaints are court filings" skills/drafting/SKILL.md
cd evals && .venv/bin/pytest -q ; cd ..
```
Expected: first grep ≥ 2; second = 1; all tests pass (the live drafting test embeds SKILL.md but its deterministic markers are unchanged).

- [ ] **Step 4: Commit**

```bash
git add skills/drafting/SKILL.md
git commit -m "drafting: route deadline complaints to the CWA/CAA templates; mark complaints as court filings"
```

---

## Task 4: Docs — roadmap, README, CHANGELOG, CLAUDE

**Files:** `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`

- [ ] **Step 1: `docs/architecture.md` roadmap item 4**

Replace:
```markdown
4. **Deadline complaint** — scaffold directly from a Gap Analysis findings table.
```
with:
```markdown
4. **Deadline complaint** — done (`templates/cwa-505-deadline-complaint.md`, `templates/caa-304-deadline-complaint.md`). The first court filing: a citizen-suit "failure to perform a nondiscretionary duty" complaint, scaffolded from a Gap Analysis findings table after the notice period runs. Standing/jurisdiction/venue are flagged, never asserted.
```

- [ ] **Step 2: `README.md` template tree**

In the `templates/` block, add the two complaint templates so the block reads:
```
├── templates/
│   ├── cwa-505-notice-of-intent.md
│   ├── cwa-505-deadline-complaint.md
│   ├── caa-304-emissions-notice.md
│   ├── caa-304-failure-to-act-notice.md
│   ├── caa-304-deadline-complaint.md
│   └── rulemaking-petition.md
```

- [ ] **Step 3: `CHANGELOG.md` `## [Unreleased]`**

Under the existing `## [Unreleased]` heading add:
```markdown
### Added
- Deadline-complaint instrument (the first court filing): `templates/cwa-505-deadline-complaint.md` (CWA §505(a)(2)) and `templates/caa-304-deadline-complaint.md` (CAA §304(a)(2)) — citizen-suit "failure to perform a nondiscretionary duty" complaints, with standing/jurisdiction/venue flagged for counsel.
- A "Stage 5 — Deadline Complaint" added to both deadline worked-examples (`docs/examples/cwa-304m-deadline-suit.md`, `docs/examples/caa-304-failure-to-act-suit.md`), each registered as a drafting eval fixture.

### Changed
- `skills/drafting` routes deadline complaints to the new templates and marks complaints as court filings.
```
(If Task 5 corrects the CWA example's notice statement, add a line under Changed noting it.)

- [ ] **Step 4: `CLAUDE.md` roadmap note**

Update the Roadmap sentence's parenthetical/tail to note the deadline complaint shipped and the consent-decree scaffold is next. Find the sentence added during the CAA work:
```markdown
§304 notice has shipped as two templates (`templates/caa-304-*.md`); the deadline complaint is next.
```
Replace its tail so it reads:
```markdown
§304 notice and the deadline complaint have shipped as templates (`templates/caa-304-*.md`,
`templates/*-deadline-complaint.md`); the consent-decree scaffold is next.
```

- [ ] **Step 5: Verify + commit**

```bash
grep -c "deadline-complaint\|deadline complaint" README.md docs/architecture.md CHANGELOG.md CLAUDE.md
cd evals && .venv/bin/pytest -q ; cd ..
git add docs/architecture.md README.md CHANGELOG.md CLAUDE.md
git commit -m "docs: mark deadline complaint shipped (roadmap, README tree, CHANGELOG, CLAUDE)"
```
Expected: each file ≥ 1; all tests pass.

**End of Phase A — both templates shippable. Phase B adds the worked-example stages and the eval net.**

---

## Task 5: Extend the CWA example with Stage 5 (+ conditional notice correction)

**Files:**
- Modify: `docs/examples/cwa-304m-deadline-suit.md`
- Reference: `templates/cwa-505-deadline-complaint.md`; the file's own Stage 1 findings table (the spine) and Stage 2 notice.

- [ ] **Step 1: (Conditional) correct the §505(b) notice statement**

Per Task 0, if §1365(b)(2) does NOT support the existing line 83 (`CWA § 505(b) requires 60 days' written notice before filing a § 505(a)(2) action`), correct it to match the statute and note the correction for the CHANGELOG. If Task 0 confirmed it (the likely outcome — §1365(b)(2) parallels CAA §7604(b)(2)), leave it unchanged and record "confirmed correct."

- [ ] **Step 2: Append Stage 5 before the Terminal node (currently line ~153, `## Terminal node — the human attorney`)**

Insert a new section just before `## Terminal node`:
```markdown
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
3. The § 505(b) notice was served on [placeholder — date] and the statutory period has run.
   [⚠ ATTORNEY: confirm the notice was properly served and the period has run before filing.]

PARTIES
4. Plaintiff [placeholder] is [placeholder — standing allegations: concrete injury, traceable to
   the missed plan, redressable by an order]. [⚠ ATTORNEY: standing (injury-in-fact, causation,
   redressability) is jurisdictional and the court's to decide — plead the elements; do not assert
   standing is established.]
5. Defendant is the Administrator of the U.S. EPA, sued in [placeholder — official capacity].

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
§ 304(m); (b) order the Administrator to publish the plan by a date certain; (c) retain jurisdiction
to ensure compliance; (d) award costs and fees under 33 U.S.C. § 1365(d); and (e) grant any other
just relief.

Respectfully submitted,
[⚠ ATTORNEY: signature block — responsible attorney must review and sign under FRCP 11.]

------------------------------------------------------------------
REQUIRED-ELEMENTS CHECKLIST
[⚠ needed] Caption: proper district/division and parties
[✓] Jurisdiction (28 U.S.C. § 1331; CWA § 505(a), 33 U.S.C. § 1365(a))
[⚠ needed] Venue for the chosen forum
[⚠ needed] Standing allegations (injury, causation, redressability) — pleaded, not asserted
[⚠ needed] Notice precondition satisfied (§ 505(b) notice served; period run)
[⚠ needed] The nondiscretionary duty, deadline, and missed-deadline facts from the record

CONSOLIDATED ATTORNEY FLAGS
- [⚠ ATTORNEY: confirm jurisdiction, venue, and that standing is pleaded (not asserted) — it is the court's to decide]
- [⚠ ATTORNEY: confirm the § 505(b) notice was served and the period ran before filing]
- [⚠ ATTORNEY: confirm § 304(m) is a nondiscretionary duty and the deadline computation]
- [⚠ ATTORNEY: needed — party identities, the last-plan date, and the years elapsed, from the record]

DEADLINE NOTE
- The § 505(b) pre-suit notice must already be satisfied before filing; this complaint seeks an
  order compelling action by a date certain (a deadline-suit remedy), not unreasonable-delay
  relief. This software tracks no clock.
```

**Handoff → the human.** The complaint joins the package; nothing here decides standing, forum, or
whether to file — those remain for counsel.

```
(Note the nested fences: the outer Stage-5 section contains one fenced ``` block holding the whole complaint, exactly like Stages 2–4 in this file.)

- [ ] **Step 3: Update the Terminal-node paragraph** to acknowledge the complaint now in the package (e.g., "findings table, flagged notice, precedent landscape, plain-language explainer, **and the flagged complaint**"). Keep it ending at the human attorney.

- [ ] **Step 4: Verify markers**

```bash
grep -c "Stage 5 — Deadline Complaint" docs/examples/cwa-304m-deadline-suit.md
grep -c "DRAFT — ATTORNEY REVIEW REQUIRED" docs/examples/cwa-304m-deadline-suit.md
grep -c "COUNT I" docs/examples/cwa-304m-deadline-suit.md
grep -cE "\[⚠ ATTORNEY:[^]]*standing[^]]*\]" docs/examples/cwa-304m-deadline-suit.md
grep -ciE "ready to file|ready to serve|filing-ready" docs/examples/cwa-304m-deadline-suit.md
```
Expected: Stage 5 = 1; banner ≥ 2 (Stage 2 notice + Stage 5 complaint); COUNT I ≥ 1; standing-flag ≥ 1; forbidden = 0.

- [ ] **Step 5: Suite green + commit**

```bash
cd evals && .venv/bin/pytest -q ; cd ..
git add docs/examples/cwa-304m-deadline-suit.md
git commit -m "examples: add Stage 5 deadline complaint to the CWA §304(m) example"
```

---

## Task 6: CWA complaint fixture + register

**Files:**
- Create: `evals/fixtures/drafting/cwa-505-deadline-complaint.json` (+ `.out.md`)
- Modify: `evals/tests/test_golden_examples.py`

- [ ] **Step 1: Create the `.out.md` from the Stage-5 complaint block**

Extract the fenced complaint content of the new Stage 5 in `docs/examples/cwa-304m-deadline-suit.md` into `evals/fixtures/drafting/cwa-505-deadline-complaint.out.md` (verbatim, the same extraction pattern as the other drafting `.out.md` files). It must carry: `DRAFT — ATTORNEY REVIEW REQUIRED`, `Doctrinal-currency check:`, a `[⚠ ATTORNEY: ...]` flag containing the word `standing`, `[placeholder]`, `REQUIRED-ELEMENTS CHECKLIST`, `CONSOLIDATED ATTORNEY FLAGS`, `DEADLINE NOTE`, and `COUNT I`. It must NOT contain `ready to file`, `ready to serve`, `filing-ready`, `ready to send`, or `final and signed`.

- [ ] **Step 2: Write the fixture JSON**

`evals/fixtures/drafting/cwa-505-deadline-complaint.json`:
```json
{
  "skill": "drafting",
  "name": "cwa-505-deadline-complaint",
  "turns": [
    {"role": "user", "content": "The §505(b) notice period has run with no agency action. From the Gap Analysis findings table (CWA 304(m) missed biennial plan, row 1), draft the §505(a)(2) deadline complaint."}
  ],
  "transcript_file": "cwa-505-deadline-complaint.out.md",
  "checks": [
    {"id": "draft-banner", "kind": "contains", "invariant": 1, "target": "DRAFT — ATTORNEY REVIEW REQUIRED"},
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "attorney-flag-present", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*\\]"},
    {"id": "placeholder-for-missing-fact", "kind": "contains", "invariant": 4, "target": "[placeholder]"},
    {"id": "checklist-section", "kind": "contains", "invariant": 2, "target": "REQUIRED-ELEMENTS CHECKLIST"},
    {"id": "flags-section", "kind": "contains", "invariant": 2, "target": "CONSOLIDATED ATTORNEY FLAGS"},
    {"id": "deadline-section", "kind": "contains", "invariant": 2, "target": "DEADLINE NOTE"},
    {"id": "count-section", "kind": "contains", "invariant": 2, "target": "COUNT I"},
    {"id": "not-finalized", "kind": "forbidden", "invariant": 5, "patterns": ["ready to file", "ready to send", "ready to serve", "filing-ready", "final and signed"]},
    {"id": "standing-flagged", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*standing[^\\]]*\\]"},
    {"id": "facts-trace-to-findings", "kind": "judge", "invariant": 4, "criterion": "The complaint's factual allegations trace to the Gap Analysis findings table or are bracketed placeholders/flags; no specific date, party, or figure is invented."}
  ]
}
```

- [ ] **Step 3: Register in `evals/tests/test_golden_examples.py`**

Add this tuple to the `GOLDEN` list (after the `("plain-language", "cwa-304m-deadline-plain")` line):
```python
    ("drafting", "cwa-505-deadline-complaint"),
```

- [ ] **Step 4: Run targeted then full suite**

```bash
cd evals && .venv/bin/pytest tests/test_golden_examples.py -q
```
Expected: passes (count +1). If a `contains`/`regex`/`forbidden` check fails, fix the `.out.md` to carry the exact marker (or remove a leaked forbidden phrase) — do NOT weaken the JSON. Then:
```bash
.venv/bin/pytest -q ; cd ..
```
Expected: full suite all pass (70).

- [ ] **Step 5: Commit**

```bash
git add evals/fixtures/drafting/cwa-505-deadline-complaint.* evals/tests/test_golden_examples.py
git commit -m "evals: register CWA §505(a)(2) deadline-complaint drafting fixture"
```

---

## Task 7: Extend the CAA example with Stage 5

**Files:**
- Modify: `docs/examples/caa-304-failure-to-act-suit.md`
- Reference: `templates/caa-304-deadline-complaint.md`; the file's Stage 1 findings table and Stage 2 notice.

- [ ] **Step 1: Append Stage 5 before the Terminal node (currently line ~200)**

Insert, mirroring Task 5's Stage 5 but for **CAA §304(a)(2)**: jurisdiction `28 U.S.C. § 1331` + `CAA § 304(a) / 42 U.S.C. § 7604(a)`; the § 304(b)(2) 60-day notice precondition; fees under `42 U.S.C. § 7604(d)`; the duty is the § 112(f)(2) residual-risk review (the matter this file already uses); defendant the Administrator. Same banner, the standing `[⚠ ATTORNEY: ...]` flag, `COUNT I`, `REQUIRED-ELEMENTS CHECKLIST`, `CONSOLIDATED ATTORNEY FLAGS`, `DEADLINE NOTE`, and `[placeholder]` facts. The string "180" must NOT appear; do NOT use "ready to file"/"ready to serve"/"filing-ready". The PRAYER seeks an order compelling the review by a date certain (not unreasonable-delay relief).

- [ ] **Step 2: Update the Terminal-node paragraph** to acknowledge the complaint now in the package; keep it ending at the human attorney.

- [ ] **Step 3: Verify markers**

```bash
grep -c "Stage 5 — Deadline Complaint" docs/examples/caa-304-failure-to-act-suit.md
grep -c "DRAFT — ATTORNEY REVIEW REQUIRED" docs/examples/caa-304-failure-to-act-suit.md
grep -c "COUNT I" docs/examples/caa-304-failure-to-act-suit.md
grep -cE "\[⚠ ATTORNEY:[^]]*standing[^]]*\]" docs/examples/caa-304-failure-to-act-suit.md
grep -c "180" docs/examples/caa-304-failure-to-act-suit.md
grep -ciE "ready to file|ready to serve|filing-ready" docs/examples/caa-304-failure-to-act-suit.md
```
Expected: Stage 5 = 1; banner ≥ 2; COUNT I ≥ 1; standing-flag ≥ 1; **180 = 0**; forbidden = 0.

- [ ] **Step 4: Suite green + commit**

```bash
cd evals && .venv/bin/pytest -q ; cd ..
git add docs/examples/caa-304-failure-to-act-suit.md
git commit -m "examples: add Stage 5 deadline complaint to the CAA §304(a)(2) example"
```

---

## Task 8: CAA complaint fixture + register

**Files:**
- Create: `evals/fixtures/drafting/caa-304-deadline-complaint.json` (+ `.out.md`)
- Modify: `evals/tests/test_caa_304_examples.py`

- [ ] **Step 1: Create the `.out.md`** from the Stage-5 complaint block in `docs/examples/caa-304-failure-to-act-suit.md` (verbatim extraction). Must carry the same markers as Task 6 Step 1 (banner, `Doctrinal-currency check:`, a `standing` attorney flag, `[placeholder]`, the three sections, `COUNT I`) and must NOT contain `180` or any forbidden finalization phrase.

- [ ] **Step 2: Write the fixture JSON**

`evals/fixtures/drafting/caa-304-deadline-complaint.json`:
```json
{
  "skill": "drafting",
  "name": "caa-304-deadline-complaint",
  "turns": [
    {"role": "user", "content": "The §304(b)(2) 60-day notice period has run with no agency action. From the Gap Analysis findings (CAA §304(a)(2) missed §112(f)(2) review, row 1), draft the §304(a)(2) deadline complaint."}
  ],
  "transcript_file": "caa-304-deadline-complaint.out.md",
  "checks": [
    {"id": "draft-banner", "kind": "contains", "invariant": 1, "target": "DRAFT — ATTORNEY REVIEW REQUIRED"},
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "attorney-flag-present", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*\\]"},
    {"id": "placeholder-for-missing-fact", "kind": "contains", "invariant": 4, "target": "[placeholder]"},
    {"id": "checklist-section", "kind": "contains", "invariant": 2, "target": "REQUIRED-ELEMENTS CHECKLIST"},
    {"id": "flags-section", "kind": "contains", "invariant": 2, "target": "CONSOLIDATED ATTORNEY FLAGS"},
    {"id": "deadline-section", "kind": "contains", "invariant": 2, "target": "DEADLINE NOTE"},
    {"id": "count-section", "kind": "contains", "invariant": 2, "target": "COUNT I"},
    {"id": "not-finalized", "kind": "forbidden", "invariant": 5, "patterns": ["ready to file", "ready to send", "ready to serve", "filing-ready", "final and signed"]},
    {"id": "standing-flagged", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*standing[^\\]]*\\]"},
    {"id": "facts-trace-to-findings", "kind": "judge", "invariant": 4, "criterion": "The complaint's factual allegations trace to the Gap Analysis findings or are bracketed placeholders/flags; no specific date, party, or figure is invented."}
  ]
}
```

- [ ] **Step 3: Register in `evals/tests/test_caa_304_examples.py`**

Add to the `GOLDEN` list (after the `("plain-language", "caa-304-failure-to-act-plain")` line):
```python
    ("drafting", "caa-304-deadline-complaint"),
```

- [ ] **Step 4: Run targeted then full suite**

```bash
cd evals && .venv/bin/pytest tests/test_caa_304_examples.py -q
```
Expected: passes (count +1). Fix the `.out.md` (never the JSON) if a deterministic check fails. Then:
```bash
.venv/bin/pytest -q ; cd ..
```
Expected: full suite all pass (71).

- [ ] **Step 5: Commit**

```bash
git add evals/fixtures/drafting/caa-304-deadline-complaint.* evals/tests/test_caa_304_examples.py
git commit -m "evals: register CAA §304(a)(2) deadline-complaint drafting fixture"
```

---

## Task 9: Legal-soundness gate

**Files:** none necessarily — the WI-3-style review; may produce small fixes.

- [ ] **Step 1: Re-confirm jurisdiction + notice preconditions** (re-run Task 0 Steps 2–3). Confirm both templates and both Stage-5 complaints cite §1331 + the citizen-suit grant, flag venue, and state the (a)(2) notice precondition correctly. Confirm the CWA example's §505(b) notice statement is now correct.

- [ ] **Step 2: Standing/jurisdiction are pleaded, not asserted.** Read each complaint's PARTIES/JURISDICTION sections; confirm standing is pleaded with a `[⚠ ATTORNEY: ...]` flag and never asserted as established; confirm jurisdiction/venue carry flags.
```bash
grep -rnE "\[⚠ ATTORNEY:[^]]*standing[^]]*\]" templates/*-deadline-complaint.md docs/examples/cwa-304m-deadline-suit.md docs/examples/caa-304-failure-to-act-suit.md
```
Expected: at least one standing flag in each of the four artifacts.

- [ ] **Step 3: Deadline-suit remedy, not unreasonable-delay.** Confirm each PRAYER seeks a date-certain order and Count I is "failure to perform a nondiscretionary duty"; confirm no artifact frames the claim as an unreasonable-delay / TRAC theory.
```bash
grep -rinE "unreasonable delay|how long is too long|TRAC" templates/*-deadline-complaint.md && echo "INVESTIGATE" || echo "OK: no unreasonable-delay framing"
grep -rn "180" templates/caa-304-deadline-complaint.md docs/examples/caa-304-failure-to-act-suit.md && echo "INVESTIGATE 180" || echo "OK: no 180"
```

- [ ] **Step 4: Verify any case cite via `verify_citation`** (if any appear in the new content); drop/replace any that do not resolve. Confirm no invented facts (every party/date/figure is `[placeholder]`).

- [ ] **Step 5: Full suite green.**
```bash
cd evals && .venv/bin/pytest -q ; cd ..
```
Expected: 71 passed, 8 deselected.

- [ ] **Step 6: Commit any fixes** (NO Claude attribution), or record "gate passed clean — no changes" if none.

---

## Task 10: Finish the branch

- [ ] **Step 1: Full suite one last time** — `cd evals && .venv/bin/pytest -q ; cd ..` (expect 71 passed, 8 deselected).
- [ ] **Step 2: Confirm no Claude attribution** — `git log origin/main..HEAD --format="%b" | grep -i "co-authored-by\|claude\|🤖" || echo OK`.
- [ ] **Step 3: Invoke `superpowers:finishing-a-development-branch`** and present the standard options (expected choice: Push and create a Pull Request; PR body carries NO Claude attribution).

---

## Self-review notes (author)

- **Spec coverage:** Component 1 → Tasks 1–2; Component 2 → Task 3; Component 3 → Tasks 5, 7; Component 4 → Tasks 6, 8; Component 5 → Task 4; Component 6 (legal gate) → Task 0 + Task 9. The §505(b) re-verification → Task 0 + Task 5 Step 1. The "180" guard → Tasks 2, 7, 9 (`grep` expecting 0).
- **No new marker / no CI change** — complaints reuse the drafting markers; `templates/**` and `evals/**` are already CI `paths`.
- **Type/name consistency:** fixture `name` fields match filenames and the `GOLDEN` tuples; `transcript_file` matches each `.out.md`; both complaint fixtures add a `count-section` (`COUNT I`) and a `standing-flagged` regex check beyond the standard drafting set; the `standing` regex uses `[^\\]]*standing[^\\]]*` (escaped in JSON).
- **Court-filing posture** is enforced both in prose (Task 3 paragraph) and mechanically (the `standing-flagged` regex check in both fixtures requires a standing flag to exist in the drafted complaint).
- **Forbidden-phrase trap:** a complaint is *about* filing/serving, so the plan explicitly forbids the literal phrases `ready to file`/`ready to serve`/`filing-ready` in templates and examples (grep == 0) to keep the `not-finalized` check honest.
