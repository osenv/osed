# WI-6 Repo Freshness / Versioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stamp the doctrinal anchors with verified/next-review dates, add a `CHANGELOG.md` and a documented re-verification cadence, and add a deterministic check that the stamp stays present and well-formed — so the currency doc doesn't quietly rot into the failure it warns against.

**Architecture:** Pure docs plus one date-agnostic doc-structure test in the WI-1 eval harness. The stamp's canonical dates live only in `docs/doctrinal-currency.md`; other docs point to it. The test asserts the stamp exists and is well-formed (not that the law is current — out of scope).

**Tech Stack:** Markdown docs; the WI-1 `evals/` harness (`evals/.venv`, pytest). Spec: `docs/specs/wi6-repo-freshness-design.md`.

**Guardrail:** WI-6 adds no skill/connector/runtime code and changes no design invariant or skill marker — the full WI-1 eval suite stays green. The structure check proves the stamp is *present and well-formed*, never that a human re-verified the law or that a date is past due (deliberately out of scope; the cadence section says so).

**Dates used throughout:** today is `2026-05-31`; the quarterly next-review date is `2026-08-31`.

---

## File Structure

```
evals/tests/test_freshness.py     # CREATE: date-agnostic stamp structure check
docs/doctrinal-currency.md        # MODIFY: law-as-of stamps on anchors + cadence section
.github/workflows/evals.yml       # MODIFY: trigger the check when the doc changes
CHANGELOG.md                      # CREATE: Keep-a-Changelog, 0.1.0 seed entry
CONTRIBUTING.md                   # MODIFY: one-line pointer to the cadence
CLAUDE.md                         # MODIFY: pointer to the law-as-of stamp
README.md                         # MODIFY: pointer to the law-as-of stamp
```

---

## Task 1: Law-as-of stamps + the deterministic structure check (TDD)

**Files:**
- Create: `evals/tests/test_freshness.py`
- Modify: `docs/doctrinal-currency.md` (the "## Worth tracking" section)
- Modify: `.github/workflows/evals.yml`

- [ ] **Step 1: Write the failing test** — `evals/tests/test_freshness.py`:

```python
"""WI-6 doctrinal-freshness structure check.

The repo's doctrinal anchors (docs/doctrinal-currency.md, the "Worth tracking"
section) must carry a law-as-of stamp: a `Law-as-of: <date>` header and, on every
anchor bullet, a `(verified YYYY-MM-DD; re-verify by YYYY-MM-DD)` stamp.

This is date-AGNOSTIC: it proves the stamp exists and is well-formed, NOT that the
law was actually re-verified or that a date is past due (out of scope — see the
doc's re-verification cadence section).
"""

import re
from pathlib import Path

DOC = Path(__file__).resolve().parents[2] / "docs" / "doctrinal-currency.md"

_STAMP = re.compile(r"\(verified \d{4}-\d{2}-\d{2}; re-verify by \d{4}-\d{2}-\d{2}\)")


def _worth_tracking_section() -> str:
    text = DOC.read_text()
    m = re.search(r"^## Worth tracking.*?(?=^## |\Z)", text, re.M | re.S)
    assert m, "missing '## Worth tracking' section in doctrinal-currency.md"
    return m.group(0)


def test_worth_tracking_has_law_as_of_header():
    section = _worth_tracking_section()
    assert re.search(r"Law-as-of:\s*\d{4}-\d{2}-\d{2}", section), "missing 'Law-as-of: <date>' header"


def test_every_anchor_bullet_is_stamped():
    section = _worth_tracking_section()
    bullets = [ln for ln in section.splitlines() if ln.lstrip().startswith("- ")]
    assert bullets, "no anchor bullets found in '## Worth tracking'"
    unstamped = [b for b in bullets if not _STAMP.search(b)]
    assert not unstamped, f"anchor bullets missing a (verified …; re-verify by …) stamp: {unstamped}"
```

- [ ] **Step 2: Run the test to verify it FAILS** (the anchors are not yet stamped)

Run: `cd /Users/behranggarakani/GitHub/osed/.claude/worktrees/bridge-cse_01XNcdFCT7dRU5qGStX85ew1/evals && .venv/bin/pytest tests/test_freshness.py -q`
Expected: 2 failed — `missing 'Law-as-of: <date>' header` and `anchor bullets missing a (verified …; re-verify by …) stamp`.

- [ ] **Step 3: Stamp the anchors.** In `docs/doctrinal-currency.md`, replace the ENTIRE "## Worth tracking" section. The current section is:
```markdown
## Worth tracking (non-exhaustive, will go stale — verify)

This list itself is subject to the currency rule. It is a prompt to check, not a substitute for checking.

- *Loper Bright* (2024) ended Chevron deference — courts now interpret statutes themselves. Cuts for and against challengers alike.
- *Seven County* (2025) narrowed NEPA review scope.
- Major Questions Doctrine continues to constrain agency action on "major" economic/political questions.
- Standing doctrine for environmental plaintiffs remains active and contested.

Re-verify all of the above before relying on any of it.
```
Replace it with:
```markdown
## Worth tracking (non-exhaustive, will go stale — verify)

**Law-as-of: 2026-05-31.** Each anchor below carries the date it was last verified and the date it
must be re-verified by. Re-verifying means: confirm in primary sources, update both dates, and add
an entry to `CHANGELOG.md`. A stamp records that a human checked — it is never a substitute for
checking.

This list itself is subject to the currency rule. It is a prompt to check, not a substitute for checking.

- *Loper Bright* (2024) ended Chevron deference — courts now interpret statutes themselves. Cuts for and against challengers alike. (verified 2026-05-31; re-verify by 2026-08-31)
- *Seven County* (2025) narrowed NEPA review scope. (verified 2026-05-31; re-verify by 2026-08-31)
- Major Questions Doctrine continues to constrain agency action on "major" economic/political questions. (verified 2026-05-31; re-verify by 2026-08-31)
- Standing doctrine for environmental plaintiffs remains active and contested. (verified 2026-05-31; re-verify by 2026-08-31)

Re-verify all of the above before relying on any of it.
```

- [ ] **Step 4: Run the test to verify it PASSES**

Run: `cd evals && .venv/bin/pytest tests/test_freshness.py -q`
Expected: 2 passed.

- [ ] **Step 5: Extend the eval CI workflow to trigger on the doc.** In `.github/workflows/evals.yml`, change the two `paths` lines. Replace:
```yaml
  push:
    paths: ["skills/**", "templates/**", "evals/**", ".github/workflows/evals.yml"]
  pull_request:
    paths: ["skills/**", "templates/**", "evals/**"]
```
with:
```yaml
  push:
    paths: ["skills/**", "templates/**", "evals/**", "docs/doctrinal-currency.md", ".github/workflows/evals.yml"]
  pull_request:
    paths: ["skills/**", "templates/**", "evals/**", "docs/doctrinal-currency.md"]
```

- [ ] **Step 6: Run the full eval suite (unchanged elsewhere)**

Run: `cd evals && .venv/bin/pytest -q`
Expected: all pass, with 2 new freshness tests added (e.g. **61 passed, 8 deselected**).

- [ ] **Step 7: Commit**

```bash
git add evals/tests/test_freshness.py docs/doctrinal-currency.md .github/workflows/evals.yml
git commit -m "WI-6: law-as-of stamps on doctrinal anchors + deterministic structure check + CI trigger"
```
Do NOT `git add -A`; verify only the three files staged.

---

## Task 2: Re-verification cadence

**Files:**
- Modify: `docs/doctrinal-currency.md` (add a section)
- Modify: `CONTRIBUTING.md` (one-line pointer)

- [ ] **Step 1: Add the cadence section.** In `docs/doctrinal-currency.md`, immediately AFTER the "## Worth tracking" section (after its final line `Re-verify all of the above before relying on any of it.`), insert:
```markdown

## Re-verification cadence

The "Worth tracking" anchors above carry stamps so they do not quietly rot. Keep them honest:

- **Who.** Maintainers, and any contributor whose change relies on or touches an anchor.
- **How often.** Re-verify each anchor by its `re-verify by` date; the default cadence is
  **quarterly**. **Always** re-verify before relying on an anchor in a real matter. Sweep the
  deference / standing / major-questions anchors **after the U.S. Supreme Court term ends** (late
  June / early July), when the most consequential shifts land.
- **The rule.** Re-verifying means confirming in primary sources, then updating *both* stamp dates
  on the anchor and adding an entry to `CHANGELOG.md`. The stamp records that a human checked; it is
  never a substitute for checking, and a present stamp does not mean an anchor is current — only that
  someone confirmed it on the verified date.

`evals/tests/test_freshness.py` enforces that each anchor stays stamped (it checks the stamp is
present and well-formed, not whether a date is past due).
```

- [ ] **Step 2: Add the CONTRIBUTING pointer.** Read `CONTRIBUTING.md`, find where it discusses the design invariants or the doctrinal-currency requirement, and add this sentence in that vicinity (place it where it reads naturally; if there is no obviously related spot, add it as a short bullet/line near the top of the contribution guidance):
```markdown
When your change relies on a doctrinal anchor, re-verify it and update its stamp in
`docs/doctrinal-currency.md` per the re-verification cadence there, and note the change in `CHANGELOG.md`.
```

- [ ] **Step 3: Confirm the freshness test still passes** (the new section must not break the "Worth tracking" parse)

Run: `cd /Users/behranggarakani/GitHub/osed/.claude/worktrees/bridge-cse_01XNcdFCT7dRU5qGStX85ew1/evals && .venv/bin/pytest tests/test_freshness.py -q`
Expected: 2 passed (the "## Worth tracking" section now ends at "## Re-verification cadence"; the anchor bullets are still inside it and still stamped).

- [ ] **Step 4: Commit**

```bash
git add docs/doctrinal-currency.md CONTRIBUTING.md
git commit -m "WI-6: documented re-verification cadence + CONTRIBUTING pointer"
```

---

## Task 3: CHANGELOG

**Files:**
- Create: `CHANGELOG.md`

- [ ] **Step 1: Create `CHANGELOG.md`** with EXACTLY this content:

```markdown
# Changelog

All notable changes to OSED are recorded here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Changes to `skills/`, `templates/`, `connectors/`, `evals/`, and the **doctrinal anchors** in
`docs/doctrinal-currency.md` get an entry. Re-verifying an anchor updates its stamp dates (there)
and adds an entry here.

## [Unreleased]

## [0.1.0] — 2026-05-31 — seed

The de-risking structural pass (`docs/plans/derisking-structural-pass.md`): turned OSED's prose
guardrails into verified ones and opened the lay-audience front door.

### Added
- **Eval & red-team harness** (`evals/`, WI-1) — deterministic marker checks plus a gated live +
  LLM-judge lane that verify every skill obeys the six design invariants; CI on `skills/` /
  `templates/` / `evals/` changes.
- **Currency tools** in the regulatory connector (WI-2) — `find_rule_changes` (Federal Register
  amendments / stays for a CFR citation) and `verify_citation` (CourtListener citation existence +
  subsequent history); both evidence-only.
- **Golden worked-example transcripts** (`docs/examples/`, WI-3) — two full-pipeline public-matter
  examples, each pipeline stage registered as a regression-anchor fixture.
- **Intake front-door skill** (`skills/intake`, WI-4) — routes a lay environmental concern to
  candidate pathways; never decides the merits.
- **Pipeline conductor skill** (`skills/pipeline`) and **runbook** (`docs/runbook.md`, WI-5) —
  runs the pipeline end to end and assembles a flagged DRAFT case package; automates the handoffs,
  never the judgment.
- **Repo-freshness controls** (WI-6) — law-as-of stamps on the doctrinal anchors, this changelog, a
  documented re-verification cadence, and a deterministic stamp-structure check.

### Changed
- The currency step in `gap-analysis`, `drafting`, and `precedent-retrieval` is now **tool-backed**
  (names the verification tools), not prose-only (WI-2).
- Docs reframed around the six skills (intake + four core agents + the pipeline conductor); the
  "four agents" headings retitled accordingly (WI-4, WI-5).
```

- [ ] **Step 2: Sanity-check**

Run: `cd /Users/behranggarakani/GitHub/osed/.claude/worktrees/bridge-cse_01XNcdFCT7dRU5qGStX85ew1 && grep -c "0.1.0\|### Added\|### Changed\|Unreleased" CHANGELOG.md`
Expected: a non-zero count (4 — all headings present).

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "WI-6: add CHANGELOG.md (0.1.0 seed — the de-risking pass)"
```

---

## Task 4: Pointers from CLAUDE.md and README

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`

> Single source of truth: these files point to the stamp; they do not carry their own dates.

- [ ] **Step 1: `CLAUDE.md`.** In the "## Doctrinal-currency check" section, find the sentence that ends the paragraph about the anchors — it currently reads:
```
Note anchors that may already be stale: *Loper Bright* (2024) ended Chevron deference;
*Seven County* (2025) narrowed NEPA review scope. Re-verify even these before relying.
```
Replace it with:
```
Note anchors that may already be stale: *Loper Bright* (2024) ended Chevron deference;
*Seven County* (2025) narrowed NEPA review scope. These anchors carry a **law-as-of stamp** in
`docs/doctrinal-currency.md` (verified + next-review dates, enforced by `evals/tests/test_freshness.py`);
re-verify them on the cadence documented there before relying.
```

- [ ] **Step 2: `README.md`.** In the "## Two principles that run through every skill" section, principle 2 ("The doctrinal-currency check") ends with `See [`docs/doctrinal-currency.md`](docs/doctrinal-currency.md).` Replace that trailing sentence with:
```
Each tracked anchor carries a law-as-of stamp (verified and next-review dates) in [`docs/doctrinal-currency.md`](docs/doctrinal-currency.md) — re-verify before relying.
```

- [ ] **Step 3: Confirm the eval suite still green** (these edits touch no fixture or the anchor stamps)

Run: `cd /Users/behranggarakani/GitHub/osed/.claude/worktrees/bridge-cse_01XNcdFCT7dRU5qGStX85ew1/evals && .venv/bin/pytest -q`
Expected: same as Task 1 Step 6 (e.g. **61 passed, 8 deselected**). All pass.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "WI-6: point CLAUDE.md + README to the doctrinal law-as-of stamp (single source of truth)"
```

---

## Self-Review (completed by plan author)

**Spec coverage vs `docs/specs/wi6-repo-freshness-design.md`:**
- ✅ Component 1 law-as-of stamps on the anchors + CLAUDE.md/README pointers (no duplicate dates) → Task 1 (stamps) + Task 4 (pointers).
- ✅ Component 2 `CHANGELOG.md` (Keep-a-Changelog, 0.1.0 seed by work item) → Task 3.
- ✅ Component 3 re-verification cadence (who / quarterly + before-relying + post-SCOTUS-term / the rule) + CONTRIBUTING pointer → Task 2.
- ✅ Component 4 deterministic structure check (date-agnostic, TDD) + CI `paths` extension → Task 1.
- ✅ Honest limit (stamp present/well-formed ≠ law current / not past due) → stated in the test docstring, the cadence section, and the CHANGELOG note.

**Placeholder scan:** none — every doc block and the test are authored in full; the one piece of latitude (where the CONTRIBUTING pointer lands) is bounded by "read it and place it near the invariants/currency guidance, else near the top," with the freshness test re-run afterward to confirm nothing broke.

**Consistency:** the stamp format `(verified 2026-05-31; re-verify by 2026-08-31)` exactly matches the test regex `\(verified \d{4}-\d{2}-\d{2}; re-verify by \d{4}-\d{2}-\d{2}\)`; the `Law-as-of: 2026-05-31` header matches `Law-as-of:\s*\d{4}-\d{2}-\d{2}`. `test_freshness.py` path `parents[2]` = repo root → `docs/doctrinal-currency.md`. The cadence section is added AFTER "## Worth tracking", so the section-parse regex still captures the stamped bullets (re-verified in Task 2 Step 3).

**Known limits preserved:** no skill/connector/runtime code; the structure check is date-agnostic; the doctrinal anchors are the only stamped docs (specs/examples are dated artifacts, already noted as subject to the currency rule).
