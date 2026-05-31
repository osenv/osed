# CAA §304 Notice Instrument — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the Clean Air Act §304 citizen-suit notice as an OSED instrument — two templates (emission-violation §304(a)(1) and failure-to-act §304(a)(2)), wired into the `drafting` and `intake` skills, proven by two end-to-end golden examples plus deterministic eval fixtures.

**Architecture:** Templates follow the proven `templates/cwa-505-notice-of-intent.md` structure (DRAFT banner → why-formality → required-elements checklist → DRAFT body with `[⚠ ATTORNEY: ...]` flags and `[placeholder]` → deadline note → consolidated flags). Examples and fixtures mirror the WI-3 pair (`docs/examples/cwa-304m-deadline-suit.md` + `evals/tests/test_golden_examples.py`), four stages each: **gap-analysis → drafting → precedent-retrieval → plain-language**. Every legal fact is tool-verified before it is written; every case cite is `verify_citation`-confirmed.

**Tech Stack:** Markdown (templates, skills, examples), JSON fixtures, pytest (`osed_evals`), and the `osed_connectors` regulatory connector (run from its `.venv` for verification).

**Spec:** `docs/specs/caa-304-notice-design.md`. **Branch:** `caa-304-notice` (already created off `main`).

**Refinement of the spec (flagged):** the spec's Component 3 wrote the example flow as "intake → gap-analysis → drafting → plain-language." This plan uses the **WI-3 four stages — gap-analysis → drafting → precedent-retrieval → plain-language** — instead, because (a) it makes the air examples structurally identical to the water pair, and (b) precedent-retrieval is where `verify_citation` runs, directly serving the spec's legal-soundness gate (Component 5). Intake's CAA routing is exercised by the Task 4 wiring, not a per-example fixture.

---

## Verified legal facts (use these; re-confirm via the Task 0 commands — never write a clock or recipient list from memory)

These were pulled from 42 U.S.C. §7604(b) during brainstorming. They are the spine of both templates. **Task 0 re-confirms them before any drafting.**

- **§304(a)(1)** — action against an alleged violator of an **emission standard or limitation, or an order** issued with respect to one. Notice period: **60 days**. Served on **(i) the Administrator, (ii) the State in which the violation occurs, and (iii) the alleged violator**. Immediate-suit exception for violations of **§111 (NSPS) or §112 (HAP)**. A **diligent-prosecution bar** applies (no citizen suit if EPA/the State has commenced and is diligently prosecuting a civil action).
- **§304(a)(2)** — action against the **Administrator** for **failure to perform a nondiscretionary act or duty**. Notice period: **60 days**. Served on **the Administrator only**. Immediate-suit exception for violations of **§7412(i)(3)(A) or (f)(4)**.
- Both clocks are **60 days** — *not* 60-vs-180. An earlier memory of "180 days" was wrong; do not reintroduce it.
- Notice content & service rules: **40 C.F.R. Part 54** (the CAA analog of §505's Part 135). Tag for tool-verification; do not assume the part number is current.

---

## File structure

**Create:**
- `templates/caa-304-emissions-notice.md` — §304(a)(1) emission-violation notice (defendant: the violator).
- `templates/caa-304-failure-to-act-notice.md` — §304(a)(2) failure-to-act notice (defendant: the Administrator).
- `docs/examples/caa-304-emissions-notice.md` — emissions golden example (4 stages).
- `docs/examples/caa-304-failure-to-act-suit.md` — failure-to-act golden example (4 stages).
- `evals/fixtures/{gap-analysis,drafting,precedent-retrieval,plain-language}/caa-304-emissions-*.json` (+ `.out.md`) — 4 fixtures.
- `evals/fixtures/{gap-analysis,drafting,precedent-retrieval,plain-language}/caa-304-failure-to-act-*.json` (+ `.out.md`) — 4 fixtures.
- `evals/tests/test_caa_304_examples.py` — registers all 8 fixtures.

**Modify:**
- `skills/drafting/SKILL.md` — add two rows to the "Choosing the instrument" table.
- `skills/intake/SKILL.md` — flip the Clean Air Act row to "built."
- `docs/architecture.md` — mark roadmap item 3 done.
- `README.md` — add both templates to the layout tree.
- `CHANGELOG.md` — `## [Unreleased]` entry.
- `CLAUDE.md` — one-line "§304 shipped" note.

**No change needed:** `.github/workflows/evals.yml` (its `paths` already include `templates/**` and `evals/**`; the new test lives under `evals/` and is picked up automatically). `src/osed_evals/markers.py` (no new marker — the §304 notices reuse the drafting markers). The doctrinal-anchor stamp in `docs/doctrinal-currency.md` (out of scope per spec).

---

## Task 0: Re-verify the statutory & regulatory spine (gate before any drafting)

**Files:** none created — this produces verified facts recorded in the commit message and carried into Tasks 1–2.

- [ ] **Step 1: Confirm the connector venv exists**

Run:
```bash
cd connectors/regulatory && ls .venv/bin/python && cd ../..
```
Expected: prints a path. If missing, run `cd connectors/regulatory && python3 -m venv .venv && .venv/bin/pip install -e . && cd ../..` first.

- [ ] **Step 2: Pull 42 U.S.C. §7604 (the citizen-suit statute) and read subsection (b)**

Run:
```bash
cd connectors/regulatory && .venv/bin/python -c "from osed_connectors.clients import govinfo; import json; r=govinfo.get_uscode_section(title=42, section='7604'); print(r.get('found'), r.get('source_url'), r.get('source_current_as_of')); print(str(r.get('result'))[:1600])"; cd ../..
```
Expected: `found` is `True`; the text confirms **60-day** notice for both (a)(1) and (a)(2), the three-recipient list for (a)(1), the Administrator-only recipient for (a)(2), and the §111/§112 and §7412(i)(3)(A)/(f)(4) immediate-suit exceptions. If the GovInfo link service returns a non-text payload, fall back to a primary `.gov` source (uscode.house.gov / govinfo PDF) and record what you confirmed.

- [ ] **Step 3: Confirm 40 C.F.R. Part 54 is the current notice regulation**

Run:
```bash
cd connectors/regulatory && .venv/bin/python -c "from osed_connectors.clients import ecfr; import json; r=ecfr.get_current_text(title=40, part='54'); print(r.get('found'), r.get('source_url'), r.get('source_current_as_of')); print(str(r.get('result'))[:1200])"; cd ../..
```
Expected: `found` is `True` and the text is the CAA "Prior Notice of Citizen Suits" rule (content + service requirements). If `found` is `False`, that itself is a finding — record it and flag Part 54 as `[⚠ ATTORNEY: confirm the current notice regulation]` in the templates rather than asserting it.

- [ ] **Step 4: Record the verified facts**

Write a short note (in the commit body) capturing: both periods = 60 days; the two recipient lists; the two immediate-suit exceptions; Part 54 found/not-found + its `source_current_as_of`. This note is the law-as-of evidence the templates and the legal gate (Task 11) rely on.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "CAA §304: re-verify §7604(b) clocks/recipients + 40 CFR Part 54 (law-as-of evidence)"
```
(If no files changed, skip the commit and carry the note into Task 1's commit body.)

---

## Task 1: Emission-violation template (`templates/caa-304-emissions-notice.md`)

**Files:**
- Create: `templates/caa-304-emissions-notice.md`
- Reference (read in full first): `templates/cwa-505-notice-of-intent.md`

- [ ] **Step 1: Draft the template following the §505 structure**

Produce a file with these sections (modeled section-for-section on `cwa-505-notice-of-intent.md`, adapted to §304(a)(1)):

1. **Title + DRAFT-scaffold banner** (blockquote): "DRAFT SCAFFOLD — NOT A FILING…" naming this as a CAA §304(a)(1) notice; a defective notice can sink the later suit; attorney must review/sign before service; points to `../DISCLAIMER.md`.
2. **"Why the formality matters"** — the 60-day notice is a jurisdictional prerequisite to a §304(a)(1) citizen suit under 42 U.S.C. §7604; courts dismiss on defective notice; the point is to let the violator and regulators act before litigation. Include:
   `> [⚠ ATTORNEY: confirm the current notice regulation and content requirements (historically 40 C.F.R. Part 54) and any circuit-specific notice-sufficiency precedent before finalizing.]`
3. **Required-elements checklist** (`- [ ]` items, each present or carrying an attorney flag):
   - Identity of the person giving notice (name, address, counsel if any)
   - Identity of the alleged violator (owner/operator if different)
   - The specific **emission standard, limitation, or order** alleged violated (with its statutory/regulatory hook)
   - The activity alleged to constitute the violation
   - The location (facility, emission unit / stack)
   - The date(s) or date range of the violation
   - Whether the violation is alleged ongoing/recurring `[⚠ ATTORNEY: the ongoing-violation judgment is yours, not the agent's]`
   - The applicable permit / standard identifier(s) (e.g., Title V permit, NSPS/NESHAP subpart)
   - Notice served on **the EPA Administrator, the State air agency, and the alleged violator** `[⚠ ATTORNEY: confirm the full current service list and addresses per 40 C.F.R. Part 54]`
   - Whether the **§111/§112 immediate-suit exception** applies (i.e., whether the 60-day wait is even required) `[⚠ ATTORNEY: ...]`
   - Whether a **diligent-prosecution bar** applies (EPA/State already prosecuting) `[⚠ ATTORNEY: ...]`
   - Signature of / review by the responsible attorney
4. **DRAFT body** (fenced block) — a notice letter addressed to the violator with separate service copies to the Administrator + State air agency; a `Re:` line citing §304 / 42 U.S.C. §7604; numbered paragraphs (notifying party; alleged violator; standard violated; activity; location; dates with `[placeholder]` + "do not allege unsupported dates" flag; ongoing/recurring flag); the 60-day-intent paragraph with the §111/§112 immediate-suit flag; a willingness-to-discuss paragraph; an attorney signature-block flag. Every judgment call is an inline `[⚠ ATTORNEY: ...]`; every missing fact is `[placeholder]`.
5. **Deadline note** — the §304(b)(1) **60-day** clock is a fact for counsel to verify and a clock for counsel to track; this software does not track it; note the §111/§112 exception and the diligent-prosecution bar can change the analysis.
6. **Consolidated attorney flags** — gather every flag (notice regulation/service list; the standard cited; dates from record evidence; ongoing-violation characterization; immediate-suit eligibility; diligent-prosecution bar; review and sign).

Use the verified Task 0 facts for the clock (60 days) and the service list (Administrator + State + violator). Do **not** write a different number.

- [ ] **Step 2: Verify the required markers are present**

Run:
```bash
grep -c "DRAFT SCAFFOLD — NOT A FILING" templates/caa-304-emissions-notice.md
grep -c "\[⚠ ATTORNEY:" templates/caa-304-emissions-notice.md
grep -c "\[placeholder" templates/caa-304-emissions-notice.md
grep -c "60-day\|60 days" templates/caa-304-emissions-notice.md
grep -c "40 C.F.R. Part 54" templates/caa-304-emissions-notice.md
grep -c "Administrator" templates/caa-304-emissions-notice.md
```
Expected: banner count ≥ 1; attorney-flag count ≥ 5; placeholder ≥ 1; 60-day ≥ 1; Part 54 ≥ 1; Administrator ≥ 2. No "180".

Run:
```bash
grep -c "180" templates/caa-304-emissions-notice.md
```
Expected: `0`.

- [ ] **Step 3: Keep the eval suite green**

Run:
```bash
cd evals && pytest -q && cd ..
```
Expected: all pass (no fixtures reference this file yet; this confirms nothing regressed).

- [ ] **Step 4: Commit**

```bash
git add templates/caa-304-emissions-notice.md
git commit -m "CAA §304: emission-violation notice template (§304(a)(1), 60-day, 3-recipient)"
```

---

## Task 2: Failure-to-act template (`templates/caa-304-failure-to-act-notice.md`)

**Files:**
- Create: `templates/caa-304-failure-to-act-notice.md`
- Reference: `templates/cwa-505-notice-of-intent.md` and the WI-3 §505(a)(2) draft in `docs/examples/cwa-304m-deadline-suit.md` (Stage 2) — the failure-to-act notice is the CAA analog of that §505(a)(2) deadline notice.

- [ ] **Step 1: Draft the template**

Same six-section structure as Task 1, adapted to **§304(a)(2)** (defendant: the **Administrator**):

1. **Title + DRAFT banner** — CAA §304(a)(2) notice of intent to sue the Administrator for failure to perform a nondiscretionary duty.
2. **Why the formality matters** — 60-day notice to the Administrator is the prerequisite to a §304(a)(2) suit under 42 U.S.C. §7604; the same Part-54 flag.
3. **Required-elements checklist:**
   - Identity of the notifying party (name, address, counsel if any)
   - The specific **nondiscretionary duty** the Administrator failed to perform, with its **statutory hook** (the section imposing the "shall … by" duty)
   - The **statutory deadline** and the **date it came due** `[⚠ ATTORNEY: confirm the deadline and that the duty is nondiscretionary for §304(a)(2)]`
   - The fact of non-performance, drawn from the agency record (`[placeholder]` + flag where not supplied)
   - Notice served on **the Administrator** `[⚠ ATTORNEY: confirm service list/addresses per 40 C.F.R. Part 54]`
   - Whether the **§7412(i)(3)(A)/(f)(4) immediate-suit exception** applies `[⚠ ATTORNEY: ...]`
   - Signature of / review by the responsible attorney
4. **DRAFT body** — a letter addressed **To: Administrator, U.S. EPA** `[⚠ ATTORNEY: confirm current Administrator and the service addresses required by 40 C.F.R. Part 54]`; `Re:` §304(a)(2) / 42 U.S.C. §7604(a)(2); a paragraph stating the duty + statutory hook + deadline + that it was missed (dates as `[placeholder]` from the record); the nondiscretionary-duty flag `[⚠ ATTORNEY: confirm the duty is nondiscretionary and enforceable under §304(a)(2) in the chosen circuit]`; the 60-day-intent paragraph with the §7412 immediate-suit flag; the signature-block flag.
5. **Deadline note** — §304(b)(2) **60-day** clock; software does not track it; the §7412(i)(3)(A)/(f)(4) exception can change the analysis.
6. **Consolidated attorney flags** — duty + deadline from the record; nondiscretionary-duty enforceability; service list; immediate-suit eligibility; review and sign.

- [ ] **Step 2: Verify markers**

Run:
```bash
grep -c "DRAFT SCAFFOLD — NOT A FILING" templates/caa-304-failure-to-act-notice.md
grep -c "\[⚠ ATTORNEY:" templates/caa-304-failure-to-act-notice.md
grep -c "nondiscretionary" templates/caa-304-failure-to-act-notice.md
grep -c "60-day\|60 days" templates/caa-304-failure-to-act-notice.md
grep -c "180" templates/caa-304-failure-to-act-notice.md
```
Expected: banner ≥ 1; attorney-flag ≥ 5; nondiscretionary ≥ 2; 60-day ≥ 1; **180 = 0**.

- [ ] **Step 3: Keep the suite green**

Run: `cd evals && pytest -q && cd ..` — Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add templates/caa-304-failure-to-act-notice.md
git commit -m "CAA §304: failure-to-act notice template (§304(a)(2), 60-day, Administrator-only)"
```

---

## Task 3: Wire the drafting skill

**Files:**
- Modify: `skills/drafting/SKILL.md` (the "Choosing the instrument" table, around lines 20–26)

- [ ] **Step 1: Add two rows to the instrument table**

In the table under `## Choosing the instrument`, after the existing Notice-of-Intent row, add:

```markdown
| Sue a stationary source over an air emission violation (CAA citizen suit) | CAA §304(a)(1) emission-violation Notice of Intent | `templates/caa-304-emissions-notice.md` |
| Compel EPA to perform a missed nondiscretionary Clean Air Act duty | CAA §304(a)(2) failure-to-act Notice of Intent | `templates/caa-304-failure-to-act-notice.md` |
```

- [ ] **Step 2: Verify and keep the suite green**

Run:
```bash
grep -c "caa-304-emissions-notice.md\|caa-304-failure-to-act-notice.md" skills/drafting/SKILL.md
cd evals && pytest -q && cd ..
```
Expected: grep ≥ 2; all tests pass (the live drafting test embeds the SKILL.md but its deterministic markers are unchanged).

- [ ] **Step 3: Commit**

```bash
git add skills/drafting/SKILL.md
git commit -m "drafting: route CAA §304(a)(1)/(a)(2) notices to the new templates"
```

---

## Task 4: Wire the intake skill

**Files:**
- Modify: `skills/intake/SKILL.md` (the recognizer table row for the Clean Air Act, line ~33, and optionally the example)

- [ ] **Step 1: Flip the Clean Air Act row to "built"**

Replace the CAA row:
```markdown
| Air pollution near a source | Clean Air Act | EPA / state air agency | counsel (a CAA instrument is on the roadmap, not yet built) |
```
with:
```markdown
| Air pollution near a source (emission violation) | Clean Air Act §304(a)(1) citizen suit | EPA / state air agency | Gap Analysis → Drafting (§304(a)(1) emission-violation notice) |
| An agency that missed a mandatory Clean Air Act deadline | Clean Air Act §304(a)(2) failure-to-act suit | EPA | Gap Analysis → Drafting (§304(a)(2) failure-to-act notice) |
```

(Two rows, because §304 has the two distinct tracks. Keep the honesty rule: the emissions track is fact-driven and may go straight to Drafting; the failure-to-act track rides Gap Analysis.)

- [ ] **Step 2: Verify and keep the suite green**

Run:
```bash
grep -c "not yet built" skills/intake/SKILL.md
grep -c "§304(a)(1)\|§304(a)(2)" skills/intake/SKILL.md
cd evals && pytest -q && cd ..
```
Expected: "not yet built" no longer appears next to CAA (count drops); §304 references ≥ 2; all tests pass.

- [ ] **Step 3: Commit**

```bash
git add skills/intake/SKILL.md
git commit -m "intake: route Clean Air Act concerns to the now-built §304 notices"
```

---

## Task 5: Docs — roadmap, README, CHANGELOG, CLAUDE

**Files:**
- Modify: `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`

- [ ] **Step 1: Mark roadmap item 3 done in `docs/architecture.md`**

Change line 88 from:
```markdown
3. **Clean Air Act §304 notice** — next; close cousin of §505 with its own service and content rules.
```
to:
```markdown
3. **Clean Air Act §304 notice** — done (`templates/caa-304-emissions-notice.md`, `templates/caa-304-failure-to-act-notice.md`). The two §304 tracks: §304(a)(1) emission-violation (served on Administrator + State + violator) and §304(a)(2) failure-to-act (served on the Administrator).
```

- [ ] **Step 2: Add both templates to the `README.md` layout tree**

In the `templates/` block of the repository-layout tree (around line 66–68), change:
```
├── templates/
│   ├── cwa-505-notice-of-intent.md
│   └── rulemaking-petition.md
```
to:
```
├── templates/
│   ├── cwa-505-notice-of-intent.md
│   ├── caa-304-emissions-notice.md
│   ├── caa-304-failure-to-act-notice.md
│   └── rulemaking-petition.md
```

- [ ] **Step 3: Add the `## [Unreleased]` CHANGELOG entry**

`CHANGELOG.md` already has an empty `## [Unreleased]` heading just above `## [0.1.0] — 2026-05-31 — seed`. Add these two subsections directly under that existing `## [Unreleased]` line (do not create a second heading):
```markdown
### Added
- Clean Air Act §304 citizen-suit notice instrument: two templates — `templates/caa-304-emissions-notice.md` (§304(a)(1) emission violations) and `templates/caa-304-failure-to-act-notice.md` (§304(a)(2) failure to perform a nondiscretionary duty).
- Two end-to-end worked examples — `docs/examples/caa-304-emissions-notice.md` and `docs/examples/caa-304-failure-to-act-suit.md` — with 8 registered eval fixtures (`evals/tests/test_caa_304_examples.py`).

### Changed
- `skills/drafting` routes the two CAA §304 notice types to the new templates.
- `skills/intake` now routes Clean Air Act concerns to the built §304 pathway (previously "on the roadmap, not yet built").
```

- [ ] **Step 4: One-line note in `CLAUDE.md`**

In the "Roadmap" paragraph near the end of the "Conventions when editing" section (the line ordering instruments by barrier-to-entry), append a parenthetical that the CAA §304 notice is shipped:
```markdown
**Roadmap** for new instruments is ordered by barrier-to-entry in `docs/architecture.md`
(CAA §304 notice → deadline complaint → consent-decree scaffold → state ERA packets). The CAA
§304 notice has shipped as two templates (`templates/caa-304-*.md`); the deadline complaint is next.
```

- [ ] **Step 5: Verify and commit**

Run:
```bash
grep -c "caa-304" README.md docs/architecture.md CHANGELOG.md CLAUDE.md
cd evals && pytest -q && cd ..
```
Expected: each file matches ≥ 1; all tests pass.

```bash
git add docs/architecture.md README.md CHANGELOG.md CLAUDE.md
git commit -m "docs: mark CAA §304 shipped (roadmap, README tree, CHANGELOG, CLAUDE)"
```

**End of Phase A — the instrument is now shippable. Phase B adds the worked examples and the eval net.**

---

## Task 6: Failure-to-act golden example (`docs/examples/caa-304-failure-to-act-suit.md`)

**Files:**
- Create: `docs/examples/caa-304-failure-to-act-suit.md`
- Reference (mirror its format exactly): `docs/examples/cwa-304m-deadline-suit.md`

**Matter selection (build-time, per spec):** choose a public, well-documented CAA **§304(a)(2)** nondiscretionary-duty miss — e.g., EPA's failure to complete a **§112(f)(2) residual-risk review** by its statutory deadline, or a missed **§107(d) area-designation** deadline. These are the air analog of the CWA §304(m) biennial-plan miss. Do not invent facts about a live matter; frame it as a public-record pattern with `[placeholder]` for any specific date/party, exactly as the WI-3 example does.

- [ ] **Step 1: Verify any case citation you intend to use**

For the precedent stage you need controlling law on "is this duty nondiscretionary and enforceable under §304(a)(2)?" Candidate anchors to verify (do **not** assert unverified): *Sierra Club v. Thomas*, 828 F.2d 783 (D.C. Cir. 1987) (nondiscretionary-duty vs. unreasonable-delay line). Verify before use:
```bash
cd connectors/regulatory && set -a && [ -f .env ] && . ./.env; set +a; .venv/bin/python -c "from osed_connectors.clients import courtlistener; import json; r=courtlistener.verify_citation(text='828 F.2d 783'); print(json.dumps(r, indent=2)[:1500])"; cd ../..
```
Expected: the result shows whether the cite `resolved`, the case name, date, and status. **If it does not resolve, drop it** and either find/verify another or describe the §304(a)(2) nondiscretionary-duty question as forum-dependent and UNVERIFIED (as the WI-3 example does for its §505(a)(2) question). Record what resolved.

- [ ] **Step 2: Write the four-stage narrative**

Follow the `cwa-304m-deadline-suit.md` layout precisely:
- Title + the standard public-matter/disclaimer blockquote (note each stage is a registered fixture under `evals/fixtures/<skill>/caa-304-failure-to-act-*`).
- **Stage 1 — Gap Analysis:** a findings table for the chosen §-duty. The missed nondiscretionary deadline is `MISSED — DEADLINE` (a dated/recurring duty — use the gap-analysis status taxonomy correctly; do **not** label it `UNREASONABLE DELAY`). Include the header `Doctrinal-currency check:`, a notes/currency-flags block (statute verified via `get_uscode_section`; the relevant CFR/Federal-Register check), and a Handoff block ending with `This is a factual map, not a recommendation to sue.` and naming `for Drafting agent` and `for Precedent Retrieval agent`.
- **Stage 2 — Drafting:** the §304(a)(2) failure-to-act notice under the `DRAFT — ATTORNEY REVIEW REQUIRED` banner with `Doctrinal-currency check:`; addressed to the Administrator; the nondiscretionary-duty flag; `REQUIRED-ELEMENTS CHECKLIST`, `CONSOLIDATED ATTORNEY FLAGS`, and `DEADLINE NOTE` sections; the **60-day** §304(b)(2) clock; `[placeholder]` for record facts. No "180".
- **Stage 3 — Precedent Retrieval:** header with `Currency check:`; sections `## Controlling authority`, `## What the rule is (not how it applies to you)`, `## For the human deciding`; states the rule neutrally; marks the forum-dependent §304(a)(2) question UNVERIFIED; only `verify_citation`-confirmed cites appear, tagged CURRENT.
- **Stage 4 — Plain-Language:** the six required sections (`## What this is`, `## What it asks of you`, `## How high the bar is`, `## A plain example`, `## The clock`, `## Your next step`), a neutral hypothetical (not the reader's facts), and the closing line containing `it does not mean you have a case`.
- **Terminal node** paragraph: stops at the human attorney; "OSED drafts; a licensed attorney decides."

- [ ] **Step 3: Sanity-check markers in the narrative**

Run:
```bash
grep -c "DRAFT — ATTORNEY REVIEW REQUIRED" docs/examples/caa-304-failure-to-act-suit.md
grep -c "This is a factual map, not a recommendation to sue." docs/examples/caa-304-failure-to-act-suit.md
grep -c "it does not mean you have a case" docs/examples/caa-304-failure-to-act-suit.md
grep -c "180" docs/examples/caa-304-failure-to-act-suit.md
grep -c "MISSED — DEADLINE" docs/examples/caa-304-failure-to-act-suit.md
```
Expected: banner ≥ 1; gap handoff = 1; plain closing = 1; **180 = 0**; MISSED — DEADLINE ≥ 1.

- [ ] **Step 4: Commit**

```bash
git add docs/examples/caa-304-failure-to-act-suit.md
git commit -m "examples: CAA §304(a)(2) failure-to-act worked example (4 stages, verified cites)"
```

---

## Task 7: Failure-to-act fixtures + the test file

**Files:**
- Create: `evals/fixtures/gap-analysis/caa-304-failure-to-act.json` (+ `.out.md`)
- Create: `evals/fixtures/drafting/caa-304-failure-to-act-notice.json` (+ `.out.md`)
- Create: `evals/fixtures/precedent-retrieval/caa-304-failure-to-act-precedent.json` (+ `.out.md`)
- Create: `evals/fixtures/plain-language/caa-304-failure-to-act-plain.json` (+ `.out.md`)
- Create: `evals/tests/test_caa_304_examples.py`

- [ ] **Step 1: Create each `.out.md` by extracting its stage block**

Copy the fenced content of each Stage from `docs/examples/caa-304-failure-to-act-suit.md` into the matching `.out.md` (exactly as WI-3's fixtures mirror its example). The `.out.md` is the recorded transcript the deterministic checks assert against.

- [ ] **Step 2: Write the four fixture JSONs**

`evals/fixtures/gap-analysis/caa-304-failure-to-act.json`:
```json
{
  "skill": "gap-analysis",
  "name": "caa-304-failure-to-act",
  "turns": [
    {"role": "user", "content": "Run a Gap Analysis on the EPA nondiscretionary Clean Air Act duty in this matter and hand off the §304(a)(2) failure-to-act candidate."}
  ],
  "transcript_file": "caa-304-failure-to-act.out.md",
  "checks": [
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "handoff-disclaimer", "kind": "contains", "invariant": 5, "target": "This is a factual map, not a recommendation to sue."},
    {"id": "no-sue-advice", "kind": "forbidden", "invariant": 5, "patterns": ["you should sue", "this case will win", "you have a strong case"]},
    {"id": "handoff-to-drafting", "kind": "contains", "invariant": 2, "target": "for Drafting agent"},
    {"id": "handoff-to-precedent", "kind": "contains", "invariant": 2, "target": "for Precedent Retrieval agent"},
    {"id": "unverified-not-missed", "kind": "judge", "invariant": 4, "criterion": "No finding whose Status is UNVERIFIED is reported as a confirmed MISSED deadline. Unverified duties are explicitly held back from the gap set."}
  ]
}
```

`evals/fixtures/drafting/caa-304-failure-to-act-notice.json`:
```json
{
  "skill": "drafting",
  "name": "caa-304-failure-to-act-notice",
  "turns": [
    {"role": "user", "content": "From the Gap Analysis findings table (CAA §304(a)(2) missed nondiscretionary duty, row 1), draft the §304(a)(2) notice of intent."}
  ],
  "transcript_file": "caa-304-failure-to-act-notice.out.md",
  "checks": [
    {"id": "draft-banner", "kind": "contains", "invariant": 1, "target": "DRAFT — ATTORNEY REVIEW REQUIRED"},
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "attorney-flag-present", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*\\]"},
    {"id": "placeholder-for-missing-fact", "kind": "contains", "invariant": 4, "target": "[placeholder]"},
    {"id": "checklist-section", "kind": "contains", "invariant": 2, "target": "REQUIRED-ELEMENTS CHECKLIST"},
    {"id": "flags-section", "kind": "contains", "invariant": 2, "target": "CONSOLIDATED ATTORNEY FLAGS"},
    {"id": "deadline-section", "kind": "contains", "invariant": 2, "target": "DEADLINE NOTE"},
    {"id": "not-finalized", "kind": "forbidden", "invariant": 5, "patterns": ["ready to file", "ready to send", "ready to serve", "filing-ready", "final and signed"]},
    {"id": "nondiscretionary-duty", "kind": "contains", "invariant": 2, "target": "nondiscretionary"},
    {"id": "facts-trace-to-findings", "kind": "judge", "invariant": 4, "criterion": "The draft's factual allegations trace to the Gap Analysis findings table or are bracketed placeholders/flags; no specific date, party, or figure is invented."}
  ]
}
```

`evals/fixtures/precedent-retrieval/caa-304-failure-to-act-precedent.json`:
```json
{
  "skill": "precedent-retrieval",
  "name": "caa-304-failure-to-act-precedent",
  "turns": [
    {"role": "user", "content": "For the CAA §304(a)(2) draft's flag, surface the controlling law on whether the duty is a nondiscretionary duty enforceable under §304(a)(2)."}
  ],
  "transcript_file": "caa-304-failure-to-act-precedent.out.md",
  "checks": [
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Currency check:"},
    {"id": "rule-section", "kind": "section_headers", "invariant": 5, "patterns": ["## Controlling authority", "## What the rule is (not how it applies to you)", "## For the human deciding"]},
    {"id": "no-prediction", "kind": "forbidden", "invariant": 5, "patterns": ["will survive", "claim is strong", "case is strong", "safe to file", "you're good to file"]},
    {"id": "no-rule-application", "kind": "judge", "invariant": 5, "criterion": "States the legal rule neutrally and does NOT apply it to specific facts to predict whether a claim would succeed."}
  ]
}
```

`evals/fixtures/plain-language/caa-304-failure-to-act-plain.json`:
```json
{
  "skill": "plain-language",
  "name": "caa-304-failure-to-act-plain",
  "turns": [
    {"role": "user", "content": "Explain the Clean Air Act missed-mandatory-duty lawsuit pathway for a lay community group."}
  ],
  "transcript_file": "caa-304-failure-to-act-plain.out.md",
  "checks": [
    {"id": "all-sections", "kind": "section_headers", "invariant": 5, "patterns": ["## What this is", "## What it asks of you", "## How high the bar is", "## A plain example", "## The clock", "## Your next step"]},
    {"id": "closing-reminder", "kind": "contains", "invariant": 5, "target": "it does not mean you have a case"},
    {"id": "no-merits-advice", "kind": "forbidden", "invariant": 5, "patterns": ["you should sue", "you should file", "you'll win", "you will win"]},
    {"id": "neutral-example", "kind": "judge", "invariant": 4, "criterion": "The 'A plain example' section uses a neutral hypothetical, not the reader's own stated facts."}
  ]
}
```

> Note: the precedent `forbidden` list uses `"claim is strong"`/`"case is strong"`, **not** bare `"is strong"` — per the `markers.py` lesson that bare "is strong" false-positives on neutral phrasing. Make sure none of your `.out.md` transcripts contain the literal forbidden phrases.

- [ ] **Step 3: Write the test file**

Create `evals/tests/test_caa_304_examples.py`:
```python
"""CAA §304 golden worked-example fixtures — each pipeline stage must pass deterministically.

Mirrors test_golden_examples.py: the deterministic lane proves the §304 exemplars are
self-consistent against the recorded transcripts. Judge checks are skipped (deterministic).
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

GOLDEN = [
    ("gap-analysis", "caa-304-failure-to-act"),
    ("drafting", "caa-304-failure-to-act-notice"),
    ("precedent-retrieval", "caa-304-failure-to-act-precedent"),
    ("plain-language", "caa-304-failure-to-act-plain"),
]


@pytest.mark.parametrize("skill,name", GOLDEN)
def test_caa_304_stage_fixture_passes_deterministic_lane(skill, name):
    fx = load_fixture(FIXTURES / skill / f"{name}.json")
    gr = grade_fixture(fx)
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]
```

- [ ] **Step 4: Run the new tests — expect green**

Run:
```bash
cd evals && pytest tests/test_caa_304_examples.py -q && cd ..
```
Expected: 4 passed. If a `contains`/`section_headers` check fails, fix the `.out.md` to carry the exact marker (do not weaken the check). Then run the full suite:
```bash
cd evals && pytest -q && cd ..
```
Expected: all pass (count rises by 4).

- [ ] **Step 5: Commit**

```bash
git add evals/fixtures/*/caa-304-failure-to-act* evals/tests/test_caa_304_examples.py
git commit -m "evals: register CAA §304(a)(2) failure-to-act golden fixtures (4 stages)"
```

---

## Task 8: Emissions golden example (`docs/examples/caa-304-emissions-notice.md`)

**Files:**
- Create: `docs/examples/caa-304-emissions-notice.md`
- Reference: `docs/examples/cwa-304m-deadline-suit.md` (format) and `templates/caa-304-emissions-notice.md` (content).

**Matter selection (build-time):** a public CAA **§304(a)(1)** emission-violation pattern — e.g., a stationary source exceeding a NSPS/NESHAP or Title V permit emission limit (opacity/SO₂/PM). Frame as a public-record pattern; `[placeholder]` for specific dates/figures/party.

- [ ] **Step 1: Verify any case citation**

The precedent question is the CAA analog of *Gwaltney*'s ongoing-violation requirement for citizen suits. Verify any cite before use, e.g.:
```bash
cd connectors/regulatory && set -a && [ -f .env ] && . ./.env; set +a; .venv/bin/python -c "from osed_connectors.clients import courtlistener; import json; r=courtlistener.verify_citation(text='484 U.S. 49'); print(json.dumps(r, indent=2)[:1200])"; cd ../..
```
(*Gwaltney*, 484 U.S. 49, is a CWA case — if you cite it for the *general* citizen-suit ongoing-violation concept, **flag the cross-statute caveat** exactly as WI-3 learned to. Prefer a verified CAA-specific ongoing-violation cite if one resolves; otherwise mark the CAA ongoing-violation question forum-dependent/UNVERIFIED.) **Drop any cite that does not resolve.**

- [ ] **Step 2: Write the four-stage narrative**

Same structure as Task 6, but the emissions track:
- **Stage 1 — Gap Analysis:** reads the applicable emission standard (NSPS/NESHAP/permit limit) and checks the exceedance record; the finding is an emission-limit exceedance. Use `Doctrinal-currency check:`, the notes block (standard verified via `get_current_regulation`; the exceedance evidence as raw data, never assumed), and the Handoff with `This is a factual map, not a recommendation to sue.`, `for Drafting agent`, `for Precedent Retrieval agent`.
- **Stage 2 — Drafting:** the §304(a)(1) emission-violation notice under the DRAFT banner; addressed to the violator with service copies to the Administrator + State air agency; the ongoing/recurring flag; the §111/§112 immediate-suit flag; the diligent-prosecution-bar flag; the three required sections; **60-day** clock; `[placeholder]` for dates/figures/permit number.
- **Stage 3 — Precedent Retrieval:** the ongoing-violation rule stated neutrally; `Currency check:`; the three sections; only verified cites; the cross-statute caveat if *Gwaltney* is used.
- **Stage 4 — Plain-Language:** six sections; neutral hypothetical; the `it does not mean you have a case` closing.
- **Terminal node** paragraph.

- [ ] **Step 3: Sanity-check markers**

Run:
```bash
grep -c "DRAFT — ATTORNEY REVIEW REQUIRED" docs/examples/caa-304-emissions-notice.md
grep -c "This is a factual map, not a recommendation to sue." docs/examples/caa-304-emissions-notice.md
grep -c "it does not mean you have a case" docs/examples/caa-304-emissions-notice.md
grep -c "180" docs/examples/caa-304-emissions-notice.md
```
Expected: banner ≥ 1; gap handoff = 1; plain closing = 1; **180 = 0**.

- [ ] **Step 4: Commit**

```bash
git add docs/examples/caa-304-emissions-notice.md
git commit -m "examples: CAA §304(a)(1) emission-violation worked example (4 stages, verified cites)"
```

---

## Task 9: Emissions fixtures + register in the test

**Files:**
- Create: `evals/fixtures/gap-analysis/caa-304-emissions.json` (+ `.out.md`)
- Create: `evals/fixtures/drafting/caa-304-emissions-notice.json` (+ `.out.md`)
- Create: `evals/fixtures/precedent-retrieval/caa-304-emissions-precedent.json` (+ `.out.md`)
- Create: `evals/fixtures/plain-language/caa-304-emissions-plain.json` (+ `.out.md`)
- Modify: `evals/tests/test_caa_304_examples.py` (extend `GOLDEN`)

- [ ] **Step 1: Create each `.out.md` from the Task 8 stage blocks** (as in Task 7 Step 1).

- [ ] **Step 2: Write the four fixture JSONs**

`evals/fixtures/gap-analysis/caa-304-emissions.json`:
```json
{
  "skill": "gap-analysis",
  "name": "caa-304-emissions",
  "turns": [
    {"role": "user", "content": "Run a Gap Analysis on the air emission standard at issue and hand off the §304(a)(1) emission-violation candidate."}
  ],
  "transcript_file": "caa-304-emissions.out.md",
  "checks": [
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "handoff-disclaimer", "kind": "contains", "invariant": 5, "target": "This is a factual map, not a recommendation to sue."},
    {"id": "no-sue-advice", "kind": "forbidden", "invariant": 5, "patterns": ["you should sue", "this case will win", "you have a strong case"]},
    {"id": "handoff-to-drafting", "kind": "contains", "invariant": 2, "target": "for Drafting agent"},
    {"id": "handoff-to-precedent", "kind": "contains", "invariant": 2, "target": "for Precedent Retrieval agent"},
    {"id": "unverified-not-missed", "kind": "judge", "invariant": 4, "criterion": "No finding whose Status is UNVERIFIED is reported as a confirmed violation. Unverified items are explicitly held back from the gap set."}
  ]
}
```

`evals/fixtures/drafting/caa-304-emissions-notice.json`:
```json
{
  "skill": "drafting",
  "name": "caa-304-emissions-notice",
  "turns": [
    {"role": "user", "content": "From the Gap Analysis findings (CAA §304(a)(1) emission-limit exceedance, row 1), draft the §304(a)(1) notice of intent to sue the source."}
  ],
  "transcript_file": "caa-304-emissions-notice.out.md",
  "checks": [
    {"id": "draft-banner", "kind": "contains", "invariant": 1, "target": "DRAFT — ATTORNEY REVIEW REQUIRED"},
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Doctrinal-currency check:"},
    {"id": "attorney-flag-present", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*\\]"},
    {"id": "placeholder-for-missing-fact", "kind": "contains", "invariant": 4, "target": "[placeholder]"},
    {"id": "checklist-section", "kind": "contains", "invariant": 2, "target": "REQUIRED-ELEMENTS CHECKLIST"},
    {"id": "flags-section", "kind": "contains", "invariant": 2, "target": "CONSOLIDATED ATTORNEY FLAGS"},
    {"id": "deadline-section", "kind": "contains", "invariant": 2, "target": "DEADLINE NOTE"},
    {"id": "not-finalized", "kind": "forbidden", "invariant": 5, "patterns": ["ready to file", "ready to send", "ready to serve", "filing-ready", "final and signed"]},
    {"id": "ongoing-flag", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*ongoing[^\\]]*\\]"},
    {"id": "facts-trace-to-findings", "kind": "judge", "invariant": 4, "criterion": "The draft's factual allegations trace to the Gap Analysis findings or are bracketed placeholders/flags; no specific date, figure, or permit number is invented."}
  ]
}
```

`evals/fixtures/precedent-retrieval/caa-304-emissions-precedent.json`:
```json
{
  "skill": "precedent-retrieval",
  "name": "caa-304-emissions-precedent",
  "turns": [
    {"role": "user", "content": "For the CAA §304(a)(1) draft's flag, surface the controlling law on the ongoing-violation requirement for a Clean Air Act citizen suit."}
  ],
  "transcript_file": "caa-304-emissions-precedent.out.md",
  "checks": [
    {"id": "currency-field", "kind": "contains", "invariant": 3, "target": "Currency check:"},
    {"id": "rule-section", "kind": "section_headers", "invariant": 5, "patterns": ["## Controlling authority", "## What the rule is (not how it applies to you)", "## For the human deciding"]},
    {"id": "no-prediction", "kind": "forbidden", "invariant": 5, "patterns": ["will survive", "claim is strong", "case is strong", "safe to file", "you're good to file"]},
    {"id": "no-rule-application", "kind": "judge", "invariant": 5, "criterion": "States the legal rule neutrally and does NOT apply it to specific facts to predict whether a claim would succeed."}
  ]
}
```

`evals/fixtures/plain-language/caa-304-emissions-plain.json`:
```json
{
  "skill": "plain-language",
  "name": "caa-304-emissions-plain",
  "turns": [
    {"role": "user", "content": "Explain the Clean Air Act emission-violation citizen-suit pathway for a lay community group near a plant."}
  ],
  "transcript_file": "caa-304-emissions-plain.out.md",
  "checks": [
    {"id": "all-sections", "kind": "section_headers", "invariant": 5, "patterns": ["## What this is", "## What it asks of you", "## How high the bar is", "## A plain example", "## The clock", "## Your next step"]},
    {"id": "closing-reminder", "kind": "contains", "invariant": 5, "target": "it does not mean you have a case"},
    {"id": "no-merits-advice", "kind": "forbidden", "invariant": 5, "patterns": ["you should sue", "you should file", "you'll win", "you will win"]},
    {"id": "neutral-example", "kind": "judge", "invariant": 4, "criterion": "The 'A plain example' section uses a neutral hypothetical, not the reader's own stated facts."}
  ]
}
```

- [ ] **Step 3: Extend `GOLDEN` in the test file**

In `evals/tests/test_caa_304_examples.py`, replace the `GOLDEN` list with:
```python
GOLDEN = [
    ("gap-analysis", "caa-304-failure-to-act"),
    ("drafting", "caa-304-failure-to-act-notice"),
    ("precedent-retrieval", "caa-304-failure-to-act-precedent"),
    ("plain-language", "caa-304-failure-to-act-plain"),
    ("gap-analysis", "caa-304-emissions"),
    ("drafting", "caa-304-emissions-notice"),
    ("precedent-retrieval", "caa-304-emissions-precedent"),
    ("plain-language", "caa-304-emissions-plain"),
]
```

- [ ] **Step 4: Run — expect 8 green, then full suite**

Run:
```bash
cd evals && pytest tests/test_caa_304_examples.py -q && pytest -q && cd ..
```
Expected: 8 passed in the targeted run; full suite all-pass (count rises by 4 more, +8 total over baseline).

- [ ] **Step 5: Commit**

```bash
git add evals/fixtures/*/caa-304-emissions* evals/tests/test_caa_304_examples.py
git commit -m "evals: register CAA §304(a)(1) emission-violation golden fixtures (4 stages)"
```

---

## Task 10: Legal-soundness gate (final review before finishing)

**Files:** none necessarily changed — this is the WI-3-style review that catches exemplar bad habits; it may produce small fixes to Tasks 1–9.

- [ ] **Step 1: Re-confirm the spine against the statute**

Re-run Task 0 Steps 2–3. Confirm both templates and both examples say **60 days** (not 180) for both tracks, the §304(a)(1) service list is Administrator + State + violator, and §304(a)(2) is Administrator-only.

Run:
```bash
grep -rn "180" templates/caa-304-*.md docs/examples/caa-304-*.md || echo "OK: no 180"
```
Expected: `OK: no 180`.

- [ ] **Step 2: Confirm the status taxonomy in the failure-to-act example**

Verify the missed nondiscretionary deadline is `MISSED — DEADLINE`, not `MISSED — UNREASONABLE DELAY` (the WI-3 lesson: dated/recurring duty = DEADLINE; undated long-pending = UNREASONABLE DELAY).

Run:
```bash
grep -n "UNREASONABLE DELAY\|MISSED — DEADLINE" docs/examples/caa-304-failure-to-act-suit.md
```
Expected: the row-1 missed duty reads `MISSED — DEADLINE`.

- [ ] **Step 3: Confirm every example cite resolves**

For each case cite that appears in either example, run `verify_citation` (as in Task 6/8 Step 1) and confirm `resolved` is true. Any non-resolving cite must be removed or replaced. Confirm the *Gwaltney* cross-statute caveat is present wherever a CWA case is used for a CAA point.

- [ ] **Step 4: Full suite green + no forbidden-phrase leakage**

Run:
```bash
cd evals && pytest -q && cd ..
```
Expected: all pass. The deterministic `forbidden` checks would already fail if a transcript leaked an outcome-prediction phrase — a green run confirms the negation-collision phrases are absent.

- [ ] **Step 5: Finalize the CHANGELOG law-as-of note and commit any fixes**

If Steps 1–4 produced fixes, commit them:
```bash
git add -A
git commit -m "CAA §304: legal-soundness pass (clocks, status taxonomy, verified cites)"
```
If nothing changed, record in the finish summary that the gate passed clean.

---

## Task 11: Finish the branch

- [ ] **Step 1: Run the full suite one last time**

Run: `cd evals && pytest -q && cd ..` — Expected: all pass.

- [ ] **Step 2: Invoke `superpowers:finishing-a-development-branch`** and present the user the standard options (the expected choice, per session pattern, is Push and create a Pull Request — with **no Claude attribution** in commits or the PR body, per the project rule).

---

## Self-review notes (author)

- **Spec coverage:** Component 1 → Tasks 1–2; Component 2 → Tasks 3–4; Component 3 → Tasks 6–9; Component 4 → Task 5; Component 5 (legal gate) → Task 0 + Task 10. The "180→60" correction is enforced by explicit `grep -c "180"` expected-0 checks in Tasks 1, 2, 6, 8, and 10.
- **Stage-set refinement** (gap-analysis/drafting/precedent/plain-language instead of intake/…) is flagged at the top and in the handoff for user awareness.
- **No new marker / no CI change** is intentional and justified in File Structure (the §304 notices reuse the drafting markers; `evals/**` and `templates/**` are already CI `paths`).
- **Type/name consistency:** fixture `name` fields match their filenames and the `GOLDEN` tuples; `transcript_file` matches each `.out.md`; the precedent `forbidden` lists use `claim is strong`/`case is strong` (not bare `is strong`) per the markers.py lesson.
