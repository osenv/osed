# State ERA Claim Packets — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship per-state environmental-rights-act (ERA) orientation packets for PA, MT, NY, and HI — a plain-language-led orientation + claim scaffold — plus four worked examples, four eval fixtures, four tracked doctrinal anchors, and skill wiring; completing roadmap item 6 (the last instrument).

**Architecture:** Each per-state packet (`templates/state-era-<st>.md`) follows one shared 8-section structure (banner+stamp → the right → standing → threshold → forum → plain-language explainer → currency note → attorney flags/handoff). Two disciplines run through everything: **currency** (a `Law-as-of:` stamp on every packet; every state case cite `verify_citation`-confirmed; the four ERAs added to the tracked anchors) and **no overstatement** (PA/MT developed; NY/HI framed plainly as *developing law*; never tell a reader they have a case).

**Tech Stack:** Markdown (templates, skills, examples), JSON fixtures, pytest (`osed_evals`), the `osed_connectors` `verify_citation` tool (CourtListener — covers state appellate cases), and `WebFetch` for primary-source state-constitution text (the connector does not carry state constitutions).

**Spec:** `docs/specs/state-era-packets-design.md`. **Branch:** `state-era-packets` (already created off merged `main`).

---

## The shared packet structure (Tasks 1–4 each build one instance of this)

Every `templates/state-era-<st>.md` has these eight sections, in OSED house style adapted to an **orientation packet** (NOT a court filing). Use the Task-0 verified provision text + cite + cases for that state; flag anything unverified.

1. **Title + banner** (`>` blockquote) — the EXACT phrase `ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE`; name it a [State] environmental-rights orientation packet; a licensed **[State]** attorney decides; point to `../DISCLAIMER.md`. Immediately below, a stamp line: `**Law-as-of: <build date>.**`
2. **## The right** — the provision (a short quotation or close paraphrase + the exact citation, e.g. `Pa. Const. art. I, § 27`) and its **enforceability posture** (self-executing / public-trust / "as provided by law"), with `[⚠ ATTORNEY: confirm the provision text and its current enforceability posture in [State]]`.
3. **## Who can invoke it** — standing in that state, with `[⚠ ATTORNEY: confirm who has standing under [State] law]`.
4. **## What a claim must show** — the threshold, stated honestly (the access point where the bar is low; the harder elements where they exist). **For NY and HI, include a sentence that this is *developing law*** and `[⚠ ATTORNEY: the standard is still developing — confirm the current state of the law before relying]`.
5. **## Forum and posture** — state court; the kind of action (declaratory / injunctive against a state actor or agency), with `[⚠ ATTORNEY: confirm forum, defendant, and procedure under [State] law]`.
6. **The plain-language explainer** — the six section headers VERBATIM: `## What this is`, `## What it asks of you`, `## How high the bar is`, `## A plain example`, `## The clock`, `## Your next step`. Lay-readable; a **neutral hypothetical** in "A plain example" (never a real named party accused); the "Your next step" / closing must contain the EXACT substring `it does not mean you have a case`.
7. **## Law-as-of and currency** — restate the stamp + "verify before relying; this doctrine is evolving" (emphatic for NY/HI).
8. **## Consolidated attorney flags and next step** — gather every flag; hand off to a [State] environmental law clinic / legal aid / the state bar referral service.

Constraints for every packet: never tell the reader they have a case, name a party as breaking the law, or predict an outcome. Do NOT use the phrases `you should sue`, `you should file`, `you'll win`, `you will win`, `you have a strong case`. Every uncertain/state-specific point is an `[⚠ ATTORNEY: ...]` flag or `[placeholder]`.

---

## File structure

**Create:** `templates/state-era-{pa,mt,ny,hi}.md`; `docs/examples/state-era-{pa,mt,ny,hi}.md`; `evals/fixtures/drafting/state-era-{pa,mt,ny,hi}.json` (+ `.out.md`); `evals/tests/test_state_era_packets.py`.
**Modify:** `skills/drafting/SKILL.md`, `skills/intake/SKILL.md`, `skills/plain-language/SKILL.md`; `docs/doctrinal-currency.md`; `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`.
**No change needed:** `evals/src/osed_evals/markers.py` (packets reuse plain-language section headers + attorney-flag/placeholder markers); `.github/workflows/evals.yml` (already covers `templates/**`, `evals/**`, `docs/doctrinal-currency.md`).

---

## Task 0: Verify all four states' provisions + leading cases (research gate)

**Files:** none — records per-state verified facts carried into Tasks 1–7. This is the highest-risk task; do it carefully.

- [ ] **Step 1: Confirm the connector venv** — `cd connectors/regulatory && ls .venv/bin/python && cd ../..` (create per prior tasks if missing).

- [ ] **Step 2: For EACH state, confirm the constitutional provision text + citation from a primary/authoritative source** using the `WebFetch` tool (the connector does not carry state constitutions). Use official state sources where possible:
  - PA: `https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm?txtType=HTM&ttl=00&div=0&chpt=1` (Pa. Const. art. I, § 27) — or Ballotpedia/Justia as fallback.
  - MT: the Montana Constitution art. II, § 3 and art. IX, § 1 (leg.mt.gov or Justia).
  - NY: N.Y. Const. art. I, § 19 (Green Amendment) (nysenate.gov or Justia).
  - HI: Haw. Const. art. XI, § 9 (and art. XI generally) (Justia/official).
  Record the exact citation and a short verbatim quotation (≤ 1 sentence) for each. If a source can't be fetched, record what you could confirm and mark the rest for an `[⚠ ATTORNEY: confirm provision text]` flag — never invent provision text.

- [ ] **Step 3: For EACH state, identify and `verify_citation` the leading ERA case(s)** (CourtListener covers state appellate decisions). Run, per cite:
```bash
cd connectors/regulatory && set -a && [ -f .env ] && . ./.env; set +a; .venv/bin/python -c "from osed_connectors.clients import courtlistener; r=courtlistener.verify_citation(text='<CITE>'); print('<CITE>', r.get('found'), [c.get('case_name') for c in (r.get('result') or {}).get('citations', [])] if isinstance(r.get('result'), dict) else None)"; cd ../..
```
Candidate cites to verify (use only those that RESOLVE; do not echo any API key):
  - PA: *Pa. Env't Def. Found. v. Commonwealth* (PEDF) and *Robinson Twp. v. Commonwealth* — try reporter cites; if a name-only search fails, that is a tool quirk (use a reporter cite).
  - MT: the major Montana ERA / youth-climate decision and *MEIC v. DEQ*.
  - NY: any appellate decision construing art. I § 19 (the Green Amendment is recent — if none resolves, record that and the packet frames the standard as developing/UNVERIFIED, citing the constitutional text only).
  - HI: the public-trust / art. XI line (e.g., the *Waiāhole* water line; the recent youth-climate settlement is a settlement, not a precedent — do not cite it as a holding).
  For each state, record: which cite(s) RESOLVED (name + year + court), and which you are dropping/marking UNVERIFIED. **A cite that does not resolve is NEVER placed in a packet** — the point becomes an `[⚠ ATTORNEY: identify and verify the controlling [State] authority]` flag.

- [ ] **Step 4: Record verified facts** in your report, per state: the provision citation + short quote; the enforceability posture (one phrase); whether the state is treated as **developed** (PA, MT) or **developing** (NY, HI); and the list of `verify_citation`-confirmed cases (name, year, court) vs. dropped/unverified. No commit.

---

## Task 1: Pennsylvania packet (`templates/state-era-pa.md`)

**Files:** Create `templates/state-era-pa.md`. Reference: the shared structure above; `skills/plain-language/SKILL.md` (the six-section format); `templates/cwa-505-notice-of-intent.md` (house style).

- [ ] **Step 1: Draft the PA packet** following the 8-section shared structure, using Task 0's verified PA facts: provision `Pa. Const. art. I, § 27` (Environmental Rights Amendment); enforceability posture = the public-trust line (PEDF / Robinson Township — include only `verify_citation`-confirmed cases, tagged CURRENT (verified via verify_citation); state treated as **developed** doctrine). Honest threshold; neutral hypothetical; the closing `it does not mean you have a case`. Banner `ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE` + `Law-as-of:` stamp.

- [ ] **Step 2: Verify markers**
```bash
grep -c "ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE" templates/state-era-pa.md   # >=1
grep -c "Law-as-of:" templates/state-era-pa.md                                             # >=1
grep -c "art. I, § 27" templates/state-era-pa.md                                           # >=1
grep -c "it does not mean you have a case" templates/state-era-pa.md                        # >=1
grep -c "\[⚠ ATTORNEY:" templates/state-era-pa.md                                          # >=4
grep -cE "## What this is|## What it asks of you|## How high the bar is|## A plain example|## The clock|## Your next step" templates/state-era-pa.md  # ==6
grep -ciE "you should sue|you should file|you'll win|you will win|you have a strong case" templates/state-era-pa.md  # ==0
```
Expected as annotated.

- [ ] **Step 3: Suite green** — `cd evals && .venv/bin/pytest -q ; cd ..` (all pass; no fixture references it yet).

- [ ] **Step 4: Commit** — `git add templates/state-era-pa.md && git commit -m "state ERA: Pennsylvania Art. I §27 orientation packet"`

---

## Task 2: Montana packet (`templates/state-era-mt.md`)

**Files:** Create `templates/state-era-mt.md`.

- [ ] **Step 1: Draft the MT packet** per the shared structure, using Task 0's verified MT facts: provision `Mont. Const. art. II, § 3` and `art. IX, § 1`; posture = a robust ERA recently tested; include only `verify_citation`-confirmed cases (tagged CURRENT); state treated as **developed**. Honest threshold; neutral hypothetical; closing reminder; banner + `Law-as-of:` stamp.

- [ ] **Step 2: Verify markers** (same as Task 1, substituting `templates/state-era-mt.md` and provision marker `art. II, § 3`):
```bash
grep -c "ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE" templates/state-era-mt.md   # >=1
grep -c "Law-as-of:" templates/state-era-mt.md                                             # >=1
grep -c "art. II, § 3" templates/state-era-mt.md                                           # >=1
grep -c "it does not mean you have a case" templates/state-era-mt.md                        # >=1
grep -cE "## What this is|## What it asks of you|## How high the bar is|## A plain example|## The clock|## Your next step" templates/state-era-mt.md  # ==6
grep -ciE "you should sue|you should file|you'll win|you will win|you have a strong case" templates/state-era-mt.md  # ==0
```

- [ ] **Step 3: Suite green** — `cd evals && .venv/bin/pytest -q ; cd ..`

- [ ] **Step 4: Commit** — `git add templates/state-era-mt.md && git commit -m "state ERA: Montana Art. II §3 / Art. IX §1 orientation packet"`

---

## Task 3: New York packet (`templates/state-era-ny.md`) — DEVELOPING law

**Files:** Create `templates/state-era-ny.md`.

- [ ] **Step 1: Draft the NY packet** per the shared structure, using Task 0's verified NY facts: provision `N.Y. Const. art. I, § 19` (the Green Amendment, ratified 2021). **Section 4 and Section 7 MUST state plainly that this is DEVELOPING law** — the enforceable standard is still being defined by the courts; do not assume a settled test; `[⚠ ATTORNEY: the standard is still developing — confirm the current state of the law before relying]`. Cite a case ONLY if it `verify_citation`-resolved in Task 0; otherwise cite the constitutional text and frame the standard as not-yet-settled. Honest (low-certainty) threshold; neutral hypothetical; closing reminder; banner + stamp.

- [ ] **Step 2: Verify markers** (substitute `templates/state-era-ny.md`, provision `art. I, § 19`; ADD a developing-law check):
```bash
grep -c "ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE" templates/state-era-ny.md   # >=1
grep -c "Law-as-of:" templates/state-era-ny.md                                             # >=1
grep -c "art. I, § 19" templates/state-era-ny.md                                           # >=1
grep -ci "developing" templates/state-era-ny.md                                            # >=1
grep -c "it does not mean you have a case" templates/state-era-ny.md                        # >=1
grep -cE "## What this is|## What it asks of you|## How high the bar is|## A plain example|## The clock|## Your next step" templates/state-era-ny.md  # ==6
grep -ciE "you should sue|you should file|you'll win|you will win|you have a strong case" templates/state-era-ny.md  # ==0
```

- [ ] **Step 3: Suite green** — `cd evals && .venv/bin/pytest -q ; cd ..`

- [ ] **Step 4: Commit** — `git add templates/state-era-ny.md && git commit -m "state ERA: New York Art. I §19 Green Amendment orientation packet (developing law)"`

---

## Task 4: Hawaiʻi packet (`templates/state-era-hi.md`) — DEVELOPING law

**Files:** Create `templates/state-era-hi.md`.

- [ ] **Step 1: Draft the HI packet** per the shared structure, using Task 0's verified HI facts: provision `Haw. Const. art. XI, § 9` (and art. XI public-trust generally); posture = "as provided by law" + public trust. **Sections 4 and 7 MUST frame this as DEVELOPING / enforceability-turns-on-statute-and-public-trust** with `[⚠ ATTORNEY: ...]`. Cite the public-trust line ONLY if `verify_citation`-confirmed in Task 0; do NOT cite the recent youth-climate settlement as a holding (it is a settlement). Honest threshold; neutral hypothetical; closing reminder; banner + stamp.

- [ ] **Step 2: Verify markers** (substitute `templates/state-era-hi.md`, provision `art. XI`; developing-law check):
```bash
grep -c "ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE" templates/state-era-hi.md   # >=1
grep -c "Law-as-of:" templates/state-era-hi.md                                             # >=1
grep -c "art. XI" templates/state-era-hi.md                                                # >=1
grep -ci "developing\|as provided by law" templates/state-era-hi.md                        # >=1
grep -c "it does not mean you have a case" templates/state-era-hi.md                        # >=1
grep -cE "## What this is|## What it asks of you|## How high the bar is|## A plain example|## The clock|## Your next step" templates/state-era-hi.md  # ==6
grep -ciE "you should sue|you should file|you'll win|you will win|you have a strong case" templates/state-era-hi.md  # ==0
```

- [ ] **Step 3: Suite green** — `cd evals && .venv/bin/pytest -q ; cd ..`

- [ ] **Step 4: Commit** — `git add templates/state-era-hi.md && git commit -m "state ERA: Hawaiʻi Art. XI orientation packet (developing law)"`

---

## Task 5: Four worked examples (`docs/examples/state-era-{pa,mt,ny,hi}.md`)

**Files:** Create the four example files. Reference: `docs/examples/caa-304-failure-to-act-suit.md` (example format: title + public-matter blockquote + stages + Terminal node) and each state's packet.

- [ ] **Step 1: For EACH state, write a short end-to-end worked example** with this shape (the ERA pathway is plain-language-led, not a court-filing pipeline):
  - Title + public-matter/disclaimer blockquote (note it is a registered eval fixture under `evals/fixtures/drafting/state-era-<st>*`).
  - **The concern.** A neutral lay scenario (a community worried about an environmental harm in [State]) — a *situation*, never a named party accused.
  - **Stage 1 — Intake.** Route it to the state-ERA pathway (Plain-Language → the [State] packet → state counsel); no merits call.
  - **Stage 2 — The orientation packet.** Present the [State] packet content (banner + `Law-as-of:` stamp + the right + threshold + the six plain-language sections + flags), drawn from `templates/state-era-<st>.md` and Task 0's verified facts. NY/HI: developing-law framing. The closing contains `it does not mean you have a case`.
  - **Terminal node — the human attorney.** Stops with a licensed [State] attorney; "OSED orients; a licensed attorney decides." No merits/outcome claim.
  - Every fenced block balanced; neutral hypotheticals; only `verify_citation`-confirmed cites.

- [ ] **Step 2: Verify markers across the four examples**
```bash
for st in pa mt ny hi; do
  echo "== $st =="
  grep -c "ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE" docs/examples/state-era-$st.md
  grep -c "it does not mean you have a case" docs/examples/state-era-$st.md
  grep -ciE "you should sue|you should file|you'll win|you will win|you have a strong case" docs/examples/state-era-$st.md
  grep -c '^```' docs/examples/state-era-$st.md   # must be EVEN
done
grep -ci "developing" docs/examples/state-era-ny.md docs/examples/state-era-hi.md   # >=1 each
```
Expected: banner ≥1 each; closing ≥1 each; forbidden ==0 each; fence count even each; NY & HI mention developing.

- [ ] **Step 3: Suite green** — `cd evals && .venv/bin/pytest -q ; cd ..`

- [ ] **Step 4: Commit** — `git add docs/examples/state-era-*.md && git commit -m "examples: four state-ERA worked examples (PA, MT, NY, HI)"`

---

## Task 6: Four packet fixtures + the test file

**Files:** Create `evals/fixtures/drafting/state-era-{pa,mt,ny,hi}.json` (+ `.out.md`) and `evals/tests/test_state_era_packets.py`.

- [ ] **Step 1: Create each `.out.md`** by extracting the Stage-2 orientation-packet content from `docs/examples/state-era-<st>.md` (verbatim — banner + `Law-as-of:` stamp through the closing reminder). Each MUST contain: `ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE`, `Law-as-of:`, the state's provision marker, the six `## ` plain-language headers, `it does not mean you have a case`, and a `[⚠ ATTORNEY: ...]` flag. NY/HI `.out.md` must also contain `developing`. None may contain the forbidden merits phrases.

- [ ] **Step 2: Write the four fixture JSONs.** Each is identical in shape; substitute `<ST>` (pa/mt/ny/hi), the `<PROVISION>` marker (`art. I, § 27` / `art. II, § 3` / `art. I, § 19` / `art. XI`), and add the `developing-law` check for NY and HI only.

`evals/fixtures/drafting/state-era-pa.json`:
```json
{
  "skill": "drafting",
  "name": "state-era-pa",
  "turns": [
    {"role": "user", "content": "A community group in Pennsylvania asks what their state constitution's environmental rights provision means and what they could do. Produce the state-ERA orientation packet."}
  ],
  "transcript_file": "state-era-pa.out.md",
  "checks": [
    {"id": "orientation-banner", "kind": "contains", "invariant": 1, "target": "ORIENTATION PACKET — NOT A FILING, NOT LEGAL ADVICE"},
    {"id": "law-as-of-stamp", "kind": "contains", "invariant": 3, "target": "Law-as-of:"},
    {"id": "provision-cite", "kind": "contains", "invariant": 3, "target": "art. I, § 27"},
    {"id": "plain-language-sections", "kind": "section_headers", "invariant": 5, "patterns": ["## What this is", "## What it asks of you", "## How high the bar is", "## A plain example", "## The clock", "## Your next step"]},
    {"id": "closing-reminder", "kind": "contains", "invariant": 5, "target": "it does not mean you have a case"},
    {"id": "attorney-flag-present", "kind": "regex", "invariant": 2, "pattern": "\\[⚠ ATTORNEY:[^\\]]*\\]"},
    {"id": "no-merits-advice", "kind": "forbidden", "invariant": 5, "patterns": ["you should sue", "you should file", "you'll win", "you will win", "you have a strong case"]},
    {"id": "no-merits-conclusion", "kind": "judge", "invariant": 5, "criterion": "The packet explains the law generally and does not tell the reader they personally have a case, does not state a named party broke the law, and does not predict the reader would win."}
  ]
}
```
`evals/fixtures/drafting/state-era-mt.json`: identical but `"name": "state-era-mt"`, `"transcript_file": "state-era-mt.out.md"`, the user content names Montana, and `provision-cite` target `"art. II, § 3"`.
`evals/fixtures/drafting/state-era-ny.json`: identical but `"name": "state-era-ny"`, `"transcript_file": "state-era-ny.out.md"`, user content names New York, `provision-cite` target `"art. I, § 19"`, AND add this check to the `checks` array:
```json
    {"id": "developing-law", "kind": "contains", "invariant": 3, "target": "developing"}
```
`evals/fixtures/drafting/state-era-hi.json`: identical but `"name": "state-era-hi"`, `"transcript_file": "state-era-hi.out.md"`, user content names Hawaiʻi, `provision-cite` target `"art. XI"`, AND add the same `developing-law` check.

- [ ] **Step 3: Create `evals/tests/test_state_era_packets.py`:**
```python
"""State-ERA orientation-packet fixtures — each packet must pass deterministically.

Mirrors test_golden_examples.py: the deterministic lane proves each per-state packet
carries its banner, law-as-of stamp, provision cite, the plain-language sections, the
no-merits closing, and (NY/HI) the developing-law marker. Judge checks are skipped here.
"""

from pathlib import Path

import pytest

from osed_evals.fixtures import load_fixture
from osed_evals.grade import grade_fixture

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

PACKETS = [
    ("drafting", "state-era-pa"),
    ("drafting", "state-era-mt"),
    ("drafting", "state-era-ny"),
    ("drafting", "state-era-hi"),
]


@pytest.mark.parametrize("skill,name", PACKETS)
def test_state_era_packet_passes_deterministic_lane(skill, name):
    fx = load_fixture(FIXTURES / skill / f"{name}.json")
    gr = grade_fixture(fx)
    assert gr.passed is True, [e.text for e in gr.expectations if not e.passed]
```

- [ ] **Step 4: Run targeted then full suite**
```bash
cd evals && .venv/bin/pytest tests/test_state_era_packets.py -q
```
Expected: 4 passed. If a `contains`/`section_headers`/`forbidden` check fails, fix the `.out.md` to carry the exact marker (or remove a leaked forbidden phrase) — do NOT weaken the JSON. Then:
```bash
.venv/bin/pytest -q ; cd ..
```
Expected: full suite all pass (76 passed, 8 deselected).

- [ ] **Step 5: Commit** — `git add evals/fixtures/drafting/state-era-*.* evals/tests/test_state_era_packets.py && git commit -m "evals: register four state-ERA packet fixtures + test"`

---

## Task 7: Currency anchors (`docs/doctrinal-currency.md`)

**Files:** Modify `docs/doctrinal-currency.md` (the "## Worth tracking" section) and `CHANGELOG.md`.

- [ ] **Step 1: Add four state-ERA anchor bullets** to the end of the "## Worth tracking" bullet list (after the existing four federal anchors, before the "Re-verify all of the above..." line). Use only the cases Task 0 `verify_citation`-confirmed; if a case did not resolve, omit its name and keep the bullet to the provision + posture. Each bullet ends with a stamp `(verified <build date>; re-verify by <build date + ~3 months>)`:
```markdown
- **Pennsylvania Art. I § 27** (Environmental Rights Amendment) — a developed public-trust line gives the provision real force; confirm the current standard before relying. (verified <BUILD_DATE>; re-verify by <+3mo>)
- **Montana Art. II § 3 & art. IX § 1** — a robust state ERA recently tested in major litigation; confirm the current standard. (verified <BUILD_DATE>; re-verify by <+3mo>)
- **New York Art. I § 19** (Green Amendment, ratified 2021) — DEVELOPING law; the enforceable standard is still being defined by the courts; do not assume a settled test. (verified <BUILD_DATE>; re-verify by <+3mo>)
- **Hawaiʻi Art. XI** (environmental rights / public trust, "as provided by law") — DEVELOPING; enforceability turns on statute and public-trust doctrine; confirm. (verified <BUILD_DATE>; re-verify by <+3mo>)
```
Replace `<BUILD_DATE>` with today's build date (YYYY-MM-DD) and `<+3mo>` with ~3 months later. Do NOT change the existing four federal anchors' stamps (do not claim a re-verification that did not happen).

- [ ] **Step 2: Update the `Law-as-of:` header** of the "## Worth tracking" section from `Law-as-of: 2026-05-31.` to `Law-as-of: <BUILD_DATE>.` (the date the list was last updated; per-anchor stamps remain authoritative).

- [ ] **Step 3: Run the freshness test (and full suite)**
```bash
cd evals && .venv/bin/pytest tests/test_freshness.py -q && .venv/bin/pytest -q ; cd ..
```
Expected: freshness tests pass (every bullet — old and new — carries a well-formed stamp; the header has a `Law-as-of:` date); full suite green.

- [ ] **Step 4: CHANGELOG entry** — under `## [Unreleased]` `### Added`, append:
```markdown
- Four state-ERA doctrinal anchors (PA Art. I §27, MT Art. II §3/Art. IX §1, NY Art. I §19 Green Amendment, HI Art. XI) added to the tracked "Worth tracking" list in `docs/doctrinal-currency.md`, each law-as-of stamped.
```

- [ ] **Step 5: Commit** — `git add docs/doctrinal-currency.md CHANGELOG.md && git commit -m "doctrinal-currency: track four state-ERA anchors (stamped)"`

---

## Task 8: Skill wiring

**Files:** Modify `skills/drafting/SKILL.md`, `skills/intake/SKILL.md`, `skills/plain-language/SKILL.md`.

- [ ] **Step 1: `skills/drafting/SKILL.md`** — add this row to the "## Choosing the instrument" table, after the consent-decree row:
```
| Orient a layperson to a state environmental-rights claim | State ERA orientation packet | `templates/state-era-pa.md` · `templates/state-era-mt.md` · `templates/state-era-ny.md` · `templates/state-era-hi.md` |
```
Then add this paragraph after the "**Consent decrees are negotiated instruments.**" paragraph:
```markdown
**State ERA packets are orientation scaffolds, not court filings.** A state environmental-rights packet explains a state constitutional right and the threshold a claim must meet, in plain language, and hands off to state counsel. It is state-law-specific and the doctrine moves fast: carry a law-as-of stamp, verify every cite, never assert a settled standard (flag developing law — e.g., NY's Green Amendment, HI's art. XI — plainly), and never tell the reader they have a case.
```

- [ ] **Step 2: `skills/intake/SKILL.md`** — update the existing state-ERA row's OSED next step. Replace:
```
| A state-constitutional right to a healthful environment | State environmental-rights act | state courts | Plain-Language + counsel |
```
with:
```
| A state-constitutional right to a healthful environment | State environmental-rights act | state courts | Plain-Language → state-ERA packet (`templates/state-era-<state>.md`) → state counsel |
```

- [ ] **Step 3: `skills/plain-language/SKILL.md`** — add a one-line pointer. After the line in the "How to translate well" / item-3 area that mentions the state environmental-rights-act "plausible showing," add a sentence (no behavior change):
```markdown
For the four covered states (PA, MT, NY, HI), a per-state orientation packet exists at `templates/state-era-<state>.md` — use it as the structured basis for the explanation, and carry its law-as-of stamp and developing-law flags.
```
(If the exact insertion point differs, add the sentence within the section that discusses state environmental-rights pathways.)

- [ ] **Step 4: Verify + suite green**
```bash
grep -c "state-era-pa.md" skills/drafting/SKILL.md          # >=1
grep -c "state ERA orientation packet\|State ERA orientation packet" skills/drafting/SKILL.md  # >=1
grep -c "state-ERA packet" skills/intake/SKILL.md           # >=1
grep -c "state-era-<state>.md" skills/plain-language/SKILL.md  # >=1
cd evals && .venv/bin/pytest -q ; cd ..
```
Expected: each grep ≥ 1; all tests pass (the live skill tests embed SKILL.md but deterministic markers are unchanged).

- [ ] **Step 5: Commit** — `git add skills/drafting/SKILL.md skills/intake/SKILL.md skills/plain-language/SKILL.md && git commit -m "skills: wire the state-ERA packets into drafting, intake, and plain-language"`

---

## Task 9: Docs — roadmap, README, CHANGELOG, CLAUDE

**Files:** Modify `docs/architecture.md`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`.

- [ ] **Step 1: `docs/architecture.md` roadmap item 6** — replace:
```
6. **State environmental-rights-act claim packet** — per-state variants (PA Art. I §27, NY Green Amendment, MT, HI). High access-to-justice value; heavy Plain-Language involvement.
```
with:
```
6. **State environmental-rights-act claim packet** — done (`templates/state-era-pa.md`, `templates/state-era-mt.md`, `templates/state-era-ny.md`, `templates/state-era-hi.md`). Per-state, plain-language-led orientation packets (PA Art. I §27 and MT developed; NY Green Amendment and HI art. XI framed as developing law), each law-as-of stamped. **All six roadmap instruments are now shipped.**
```

- [ ] **Step 2: `README.md` template tree** — add the four packets to the `templates/` block (a natural spot is after `consent-decree-deadline.md`, keeping `rulemaking-petition.md` last):
```
│   ├── state-era-pa.md
│   ├── state-era-mt.md
│   ├── state-era-ny.md
│   ├── state-era-hi.md
```

- [ ] **Step 3: `CHANGELOG.md`** — under `## [Unreleased]` `### Added` (the anchors bullet from Task 7 is already there), append:
```markdown
- State environmental-rights-act orientation packets for PA, MT, NY, and HI (`templates/state-era-*.md`): plain-language-led, law-as-of stamped, with NY and HI framed as developing law. Four worked examples (`docs/examples/state-era-*.md`) and four packet fixtures (`evals/tests/test_state_era_packets.py`).
```
Under `### Changed`, append:
```markdown
- `skills/drafting`, `skills/intake`, and `skills/plain-language` wire the state-ERA packets into the pathway.
```

- [ ] **Step 4: `CLAUDE.md`** — find the Roadmap sentence (it currently ends naming the state ERA packets as next). Replace its tail so it reads that the state ERA packets have shipped and the instrument roadmap is complete, e.g.:
```markdown
`templates/consent-decree-deadline.md`, `templates/state-era-*.md`); all six roadmap instruments
have now shipped.
```
(Conform to the actual surrounding text; the point is the sentence now says the ERA packets shipped and the roadmap is complete.)

- [ ] **Step 5: Verify + commit**
```bash
grep -c "state-era" README.md docs/architecture.md CHANGELOG.md CLAUDE.md
cd evals && .venv/bin/pytest -q ; cd ..
git add docs/architecture.md README.md CHANGELOG.md CLAUDE.md
git commit -m "docs: mark state-ERA packets shipped — roadmap complete (roadmap, README, CHANGELOG, CLAUDE)"
```
Expected: each file ≥ 1; all tests pass.

---

## Task 10: Legal-soundness gate (highest scrutiny in the project)

**Files:** none necessarily — may produce small fixes.

- [ ] **Step 1: Every cite resolves.** For every case citation appearing in any packet or example, run `verify_citation` and confirm it resolves; drop/replace any that do not with an `[⚠ ATTORNEY: identify and verify the controlling [State] authority]` flag. Confirm no packet cites the HI youth-climate *settlement* as a holding.
```bash
grep -rnE "[0-9]+ (A\.|A\.2d|A\.3d|P\.|P\.2d|P\.3d|N\.E\.|N\.Y\.|N\.Y\.2d|N\.Y\.3d|U\.S\.) [0-9]+|v\. " templates/state-era-*.md docs/examples/state-era-*.md | head -40
```
(Inspect each case reference; verify via the connector.)

- [ ] **Step 2: No overstatement.** Confirm PA/MT are not overstated and **NY/HI explicitly say the law is developing/unsettled** (no settled-standard implication). 
```bash
grep -ci "developing\|still being defined\|not yet settled\|unsettled\|as provided by law" docs/examples/state-era-ny.md docs/examples/state-era-hi.md templates/state-era-ny.md templates/state-era-hi.md
```
Read the NY/HI "What a claim must show" sections and confirm honest framing.

- [ ] **Step 3: No merits drift.** Confirm no packet/example tells a reader they have a case, accuses a named party, or predicts an outcome; neutral hypotheticals only.
```bash
grep -rinE "you have a case|you should sue|you should file|you'll win|you will win|broke the law" templates/state-era-*.md docs/examples/state-era-*.md
```
(Expect only the negated mandated form "it does not mean you have a case" — read each hit's context.)

- [ ] **Step 4: Stamps + freshness.** Confirm every packet carries a `Law-as-of:` stamp and the four anchors are stamped; `cd evals && .venv/bin/pytest tests/test_freshness.py -q ; cd ..` passes.

- [ ] **Step 5: Full suite green.** `cd evals && .venv/bin/pytest -q ; cd ..` → 76 passed, 8 deselected.

- [ ] **Step 6: Commit any fixes** (NO Claude attribution), or record "gate passed clean — no changes."

---

## Task 11: Finish the branch

- [ ] **Step 1: Full suite** — `cd evals && .venv/bin/pytest -q ; cd ..` (expect 76 passed, 8 deselected).
- [ ] **Step 2: No Claude attribution** — `git log origin/main..HEAD --format="%b" | grep -i "co-authored-by\|claude\|🤖" || echo OK`.
- [ ] **Step 3: Invoke `superpowers:finishing-a-development-branch`** and present the standard options (expected: Push and create a Pull Request; PR body carries NO Claude attribution; note that this completes the six-instrument roadmap).

---

## Self-review notes (author)

- **Spec coverage:** Component 1 (structure) → the shared structure + Tasks 1–4; Component 2 (four states) → Tasks 0–4; Component 3 (wiring) → Task 8; Component 4 (anchors) → Task 7; Component 5 (examples) → Task 5; Component 6 (fixtures) → Task 6; Component 7 (docs) → Task 9; Component 8 (legal gate) → Task 0 + Task 10.
- **Currency discipline** is enforced mechanically: `law-as-of-stamp` (`contains "Law-as-of:"`) and `provision-cite` checks in every fixture; the `developing-law` check in the NY/HI fixtures; the freshness test over the four new anchors; and `verify_citation` gates in Task 0 + Task 10.
- **No-overstatement** is enforced by the NY/HI `developing-law` fixture check + the Task 10 grep + the legal gate's read.
- **No new marker / no CI change** — packets reuse plain-language section headers + attorney-flag/placeholder markers; `templates/**`, `evals/**`, and `docs/doctrinal-currency.md` are already CI `paths`.
- **Type/name consistency:** fixture `name` fields match filenames, `transcript_file`, and the `PACKETS` tuples in the new test; the four fixtures share one shape with per-state `provision-cite` targets and the NY/HI `developing-law` addition.
- **Honest-build discipline:** the per-state provision text and case cites are verified at build (Task 0) and only `verify_citation`-confirmed cases are placed in packets; unresolved cites become attorney flags (the WI-3 lesson). The plan does not hardcode unverified holdings.
