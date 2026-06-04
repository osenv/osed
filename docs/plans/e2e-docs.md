# OSED End-to-End Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write OSED's first user-facing end-to-end guide — two parallel tracks (For communities / For attorneys) + shared concepts — as portable Markdown under `docs/guide/`, held to OSED's own invariants by a deterministic check.

**Architecture:** Hand-authored Markdown that *links to* (never duplicates) the existing examples/runbook/templates, in the muse-scribe style (imperative, verbatim labels, audience-tuned). A pytest guard (`test_guide_docs.py`) enforces the honesty discipline (no merits-drift in the community track, the disclaimer is surfaced, intra-guide links resolve), reusing the eval harness's forbidden-phrase tuple so it's negation-safe.

**Tech Stack:** Markdown; pytest (`osed_evals`); the existing `markers.PLAIN_LANGUAGE_FORBIDDEN_ADVICE`.

**Spec:** `docs/specs/e2e-docs-design.md`. **Branch:** `e2e-docs` (created off merged `main`).

---

## Grounding sources (quote labels VERBATIM from these; link, don't duplicate)

- Premise: **"OSED drafts; a licensed attorney decides."** (`DISCLAIMER.md`, `docs/architecture.md`).
- The six invariants: `CLAUDE.md` / `docs/architecture.md` ("Design invariants").
- DRAFT banners: `DRAFT — ATTORNEY REVIEW REQUIRED` (drafting output); `DRAFT SCAFFOLD — NOT A FILING` / `… NOT FOR FILING` / `… NOT AN AGREEMENT, NOT FOR LODGING OR ENTRY` (templates).
- The inline flag form: `[⚠ ATTORNEY: ...]`.
- Plain-language closing: `it does not mean you have a case`.
- Instruments: `templates/*.md`. Worked examples: `docs/examples/*`. Pipeline: `docs/runbook.md` + `skills/pipeline/SKILL.md`. Currency: `docs/doctrinal-currency.md` + `CONNECTORS.md`. Contributing/evals: `CONTRIBUTING.md` + `evals/README.md`.

## File structure

**Create:** `evals/tests/test_guide_docs.py`; `docs/guide/README.md`; `docs/guide/concepts/{the-six-invariants,the-pathways,the-disclaimer}.md`; `docs/guide/for-communities/{start-here,is-there-a-pathway,what-each-pathway-is,what-you-can-and-cant-do,find-a-lawyer}.md`; `docs/guide/for-attorneys/{start-here,instrument-catalog,running-the-pipeline,currency-and-the-connector,extending-osed}.md`.
**Modify:** `.github/workflows/evals.yml` (add `docs/guide/**` to `paths`); `README.md` (Documentation pointer); `CHANGELOG.md`.
**No change:** any instrument/skill/template; the climate-news subsystem (out of scope, still flagged).

---

## Task 1: Validation harness + guide entry point + disclaimer page (TDD)

**Files:** Create `evals/tests/test_guide_docs.py`, `docs/guide/README.md`, `docs/guide/concepts/the-disclaimer.md`; modify `.github/workflows/evals.yml`.

- [ ] **Step 1: Write the test FIRST** — `evals/tests/test_guide_docs.py`:
```python
"""End-to-end guide docs honor OSED's invariants and don't rot.

The for-communities track must never tell a reader they have a case / should sue / will win
(the same line the plain-language and intake skills hold). The guide entry point surfaces the
disclaimer, and intra-guide relative links resolve. Reuses the plain-language forbidden tuple,
which deliberately omits "you have a case" (a negation-collision trap — the negated mandated form
"it does not mean you have a case" is allowed and expected).
"""

import re
from pathlib import Path

from osed_evals.markers import PLAIN_LANGUAGE_FORBIDDEN_ADVICE

REPO = Path(__file__).resolve().parents[2]
GUIDE = REPO / "docs" / "guide"

_LINK = re.compile(r"\]\(([^)]+)\)")


def _guide_md_files():
    return sorted(GUIDE.rglob("*.md"))


def test_guide_entry_point_exists():
    assert (GUIDE / "README.md").exists(), "docs/guide/README.md (entry point) is missing"


def test_entry_point_references_the_disclaimer():
    text = (GUIDE / "README.md").read_text()
    assert "DISCLAIMER" in text, "the guide entry point must point readers to the disclaimer"


def test_community_track_has_no_merits_drift():
    community_dir = GUIDE / "for-communities"
    offenders = {}
    for f in sorted(community_dir.rglob("*.md")) if community_dir.exists() else []:
        low = f.read_text().lower()
        hits = [p for p in PLAIN_LANGUAGE_FORBIDDEN_ADVICE if p in low]
        if hits:
            offenders[f.name] = hits
    assert not offenders, f"merits-drift phrases in community docs: {offenders}"


def test_intra_guide_relative_links_resolve():
    broken = []
    for f in _guide_md_files():
        for m in _LINK.finditer(f.read_text()):
            target = m.group(1).split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (f.parent / target).resolve().exists():
                broken.append(f"{f.relative_to(REPO)} -> {target}")
    assert not broken, f"broken relative links in docs/guide: {broken}"
```

- [ ] **Step 2: Run it — expect failure** (no `docs/guide/` yet):
```bash
cd evals && .venv/bin/pytest tests/test_guide_docs.py -q ; cd ..
```
Expected: FAILS on `test_guide_entry_point_exists` (the guide doesn't exist yet).

- [ ] **Step 3: Create `docs/guide/concepts/the-disclaimer.md`** — a short page (≈10–15 lines): OSED's access-to-justice promise in one paragraph; the premise verbatim **"OSED drafts; a licensed attorney decides."**; then a line linking the full disclaimer: `See the full disclaimer: [../../../DISCLAIMER.md](../../../DISCLAIMER.md).` (Confirm the relative depth: `docs/guide/concepts/` → repo root is `../../../`.)

- [ ] **Step 4: Create `docs/guide/README.md`** — the entry point (≈30–50 lines): a one-paragraph "What OSED is" (it turns proven environmental-litigation instruments into something a local actor can run again; **it drafts, an attorney decides**); a prominent **"Read this first"** line linking the disclaimer page `[concepts/the-disclaimer.md](concepts/the-disclaimer.md)` AND the root `[../../DISCLAIMER.md](../../DISCLAIMER.md)` (so the word `DISCLAIMER` appears for the test); a **"Two ways in"** section linking `[For communities](for-communities/start-here.md)` and `[For attorneys](for-attorneys/start-here.md)`; a "Shared concepts" list linking the three `concepts/` pages. NOTE: the links to `for-communities/start-here.md` etc. must resolve — so EITHER create empty-but-valid stub files for the four not-yet-written entry points in this task, OR defer those links until the pages exist. **Chosen approach:** in this task, link only to files that exist now (`concepts/the-disclaimer.md`, `../../DISCLAIMER.md`); add the track links in Task 5 once the track pages exist. Keep Task-1 README links resolvable.

- [ ] **Step 5: Extend the CI `paths`** in `.github/workflows/evals.yml` — add `"docs/guide/**"` to BOTH the `push.paths` and `pull_request.paths` arrays (so guide-only edits trigger the docs check). The push line becomes:
```yaml
    paths: ["skills/**", "templates/**", "evals/**", "docs/doctrinal-currency.md", "docs/guide/**", ".github/workflows/evals.yml"]
```
and the pull_request line:
```yaml
    paths: ["skills/**", "templates/**", "evals/**", "docs/doctrinal-currency.md", "docs/guide/**"]
```

- [ ] **Step 6: Run the test — expect pass; then the full suite**
```bash
cd evals && .venv/bin/pytest tests/test_guide_docs.py -q && .venv/bin/pytest -q ; cd ..
```
Expected: the 4 guide tests pass (entry exists; references disclaimer; community dir empty → vacuous; links resolve); full suite green (e.g. 81 passed).

- [ ] **Step 7: Commit**
```bash
git add evals/tests/test_guide_docs.py docs/guide/README.md docs/guide/concepts/the-disclaimer.md .github/workflows/evals.yml
git commit -m "docs(guide): scaffold the end-to-end guide entry point + the honesty/link check"
```

---

## Task 2: Shared `concepts/` pages

**Files:** Create `docs/guide/concepts/the-six-invariants.md`, `docs/guide/concepts/the-pathways.md`. Reference: `docs/architecture.md`, `CLAUDE.md` (the invariants), `DISCLAIMER.md`.

- [ ] **Step 1: `the-six-invariants.md`** — list the six invariants verbatim in spirit, each with one plain sentence of *why* and the failure mode it prevents:
  1. Every drafted instrument is a marked **DRAFT** requiring attorney review (the visible banner).
  2. Every judgment call is **flagged inline** (`[⚠ ATTORNEY: ...]`), never silently resolved.
  3. Every cited authority passes a **doctrinal-currency check** or is flagged (link `the-pathways.md` and, for attorneys, `../for-attorneys/currency-and-the-connector.md`).
  4. **No agent invents facts** — missing facts become `[placeholder]` + a flag.
  5. **No agent tells a user they have a case, should sue, or will win.**
  6. Skills **refuse** harassment and bad-faith filing uses.
  End with the recurring failure mode these prevent (a confident, authoritative-looking instrument that is wrong). Link `[../../architecture.md](../../architecture.md)`.

- [ ] **Step 2: `the-pathways.md`** — the templatable / suit-type / gating-doctrine spectrum in plain terms: instruments (templatable) → suit types (semi) → gating doctrines (standing/ripeness/whether-to-sue = judgment, human-only). A short table mapping a concern → likely pathway → the OSED instrument (CWA/CAA citizen-suit notice; rulemaking petition; deadline complaint; consent decree; state ERA packet). Link the relevant `../for-communities/what-each-pathway-is.md` and `../for-attorneys/instrument-catalog.md`. Link `[../../architecture.md](../../architecture.md)`.

- [ ] **Step 2.5: Update `concepts/`-internal links only to existing files** (the-disclaimer exists; the two for-* targets will exist after Tasks 3–4 — to keep the link test green NOW, link those forward targets only if they exist; otherwise reference them by name without a relative link, and add the links in Task 5). Simplest: in Tasks 2–4, only add a relative link when its target file already exists; otherwise name the page in prose. Task 5 does a final cross-link pass.

- [ ] **Step 3: Suite green + commit**
```bash
cd evals && .venv/bin/pytest tests/test_guide_docs.py -q && .venv/bin/pytest -q ; cd ..
git add docs/guide/concepts/the-six-invariants.md docs/guide/concepts/the-pathways.md
git commit -m "docs(guide): shared concepts — the six invariants and the pathways"
```
Expected: link test green (no link to a missing file); suite green.

---

## Task 3: `for-communities/` track (5 pages)

**Files:** Create the five `docs/guide/for-communities/*.md`. Reference: `skills/intake/SKILL.md`, `skills/plain-language/SKILL.md`, `docs/examples/*`, `DISCLAIMER.md`. **Discipline (enforced by the test): no `you should sue` / `you should file` / `you'll win` / `you will win`. Neutral hypotheticals only. Never accuse a named party.**

- [ ] **Step 1: `start-here.md`** — what OSED is in plain terms; the one promise (**"OSED prepares a first draft; a licensed attorney decides."**); the disclaimer surfaced (link `../concepts/the-disclaimer.md`); pointer to `is-there-a-pathway.md`. The closing reminder may use the negated form "it does not mean you have a case."
- [ ] **Step 2: `is-there-a-pathway.md`** — how to describe your situation as a *situation* (not a violation); the candidate pathways it might travel (mirror the intake skill's table — water/air/waste/species/NEPA/rulemaking/state-ERA), honest about covered vs. counsel-only; route to a lawyer. No merits call.
- [ ] **Step 3: `what-each-pathway-is.md`** — each instrument in lay terms with a one-line "what it is / when it fits," each linking its worked example: citizen-suit notice → `../../examples/cwa-304m-deadline-suit.md`; rulemaking petition → `../../examples/rulemaking-petition.md`; deadline complaint → (the Stage-5 in `../../examples/cwa-304m-deadline-suit.md`); consent decree → (Stage-6 there); state ERA → `../../examples/state-era-pa.md` (+ name MT/NY/HI). Verify each link target exists.
- [ ] **Step 4: `what-you-can-and-cant-do.md`** — the templatable/judgment line in plain terms: you can prepare a flagged draft and bring it to a lawyer; only a lawyer decides standing, the merits, the forum, and whether to file. Link `../concepts/the-pathways.md`.
- [ ] **Step 5: `find-a-lawyer.md`** — legal aid, environmental law clinics, public-interest orgs, state bar referral; bring the draft + its `[⚠ ATTORNEY: ...]` flags to counsel; confirm any deadline immediately (the software tracks no clock).

- [ ] **Step 6: Verify discipline + links + suite**
```bash
grep -rinE "you should sue|you should file|you'll win|you will win" docs/guide/for-communities/ && echo "INVESTIGATE" || echo "OK: no merits phrases"
cd evals && .venv/bin/pytest tests/test_guide_docs.py -q && .venv/bin/pytest -q ; cd ..
git add docs/guide/for-communities/
git commit -m "docs(guide): the For-communities track (5 pages)"
```
Expected: no merits phrases; the guide test's merits + link checks pass; suite green.

---

## Task 4: `for-attorneys/` track (5 pages)

**Files:** Create the five `docs/guide/for-attorneys/*.md`. Reference: `templates/*.md`, `docs/runbook.md`, `skills/*/SKILL.md`, `CONNECTORS.md`, `docs/doctrinal-currency.md`, `CONTRIBUTING.md`, `README.md` (plugin install), `evals/README.md`.

- [ ] **Step 1: `start-here.md`** — what OSED produces and how it fits a practice (it drafts; you decide); how to install it (link the README section `[../../../README.md](../../../README.md)` "Install as a Claude Code plugin"); the six invariants as the contract (link `../concepts/the-six-invariants.md`).
- [ ] **Step 2: `instrument-catalog.md`** — a table of the six instruments: when each applies, what it outputs, and its template + worked-example links: `templates/cwa-505-notice-of-intent.md`, `templates/caa-304-emissions-notice.md`, `templates/caa-304-failure-to-act-notice.md`, `templates/rulemaking-petition.md`, `templates/cwa-505-deadline-complaint.md`, `templates/caa-304-deadline-complaint.md`, `templates/consent-decree-deadline.md`, `templates/state-era-{pa,mt,ny,hi}.md` (link via `../../../templates/<file>`). Note the required-elements + `[⚠ ATTORNEY: ...]` flag discipline, and the developed-vs-developing framing for NY/HI ERA packets. Verify each template link resolves.
- [ ] **Step 3: `running-the-pipeline.md`** — intake → gap-analysis → drafting ↔ precedent-retrieval → plain-language → the human attorney; halting on a refusal or a merits-laden choice is success; link `[../../runbook.md](../../runbook.md)`.
- [ ] **Step 4: `currency-and-the-connector.md`** — the CURRENT/CHANGED/DEAD/UNVERIFIED discipline; the four connector tools; optional keys; keyless → UNVERIFIED graceful fallback; the bundled-doc-is-a-snapshot note (run `/plugin marketplace update` + re-verify). Link `[../../../CONNECTORS.md](../../../CONNECTORS.md)` and `[../../doctrinal-currency.md](../../doctrinal-currency.md)`.
- [ ] **Step 5: `extending-osed.md`** — contributing a skill/template; the eval harness (deterministic + gated live lanes); the invariants you must not regress; the `${CLAUDE_SKILL_DIR}` plugin-safe resource convention. Link `[../../../CONTRIBUTING.md](../../../CONTRIBUTING.md)` and `[../../../evals/README.md](../../../evals/README.md)` (verify it exists; if not, link `evals/` dir or omit).

- [ ] **Step 6: Verify links + suite**
```bash
cd evals && .venv/bin/pytest tests/test_guide_docs.py -q && .venv/bin/pytest -q ; cd ..
git add docs/guide/for-attorneys/
git commit -m "docs(guide): the For-attorneys track (5 pages)"
```
Expected: link test green (all template/doc links resolve); suite green.

---

## Task 5: Cross-link pass + root README pointer + CHANGELOG

**Files:** Modify `docs/guide/README.md`, `docs/guide/concepts/*.md` (forward links), `README.md`, `CHANGELOG.md`.

- [ ] **Step 1: Complete the cross-links** now that all pages exist: in `docs/guide/README.md`, add the "Two ways in" links `[For communities](for-communities/start-here.md)` and `[For attorneys](for-attorneys/start-here.md)`, and the three `concepts/` links. In the `concepts/` pages, add any forward links to `../for-communities/*` / `../for-attorneys/*` that were deferred in Task 2.
- [ ] **Step 2: Root `README.md` "Documentation" pointer** — add a short section after "Repository layout" (or near the top):
```markdown
## Documentation

A full end-to-end guide lives in [`docs/guide/`](docs/guide/README.md) — two tracks, **[For communities](docs/guide/for-communities/start-here.md)** and **[For attorneys](docs/guide/for-attorneys/start-here.md)**, plus shared [concepts](docs/guide/concepts/the-six-invariants.md). OSED drafts; a licensed attorney decides.
```
- [ ] **Step 3: `CHANGELOG.md` `[Unreleased]` → Added:**
```markdown
- End-to-end user guide under `docs/guide/` — parallel **For communities** and **For attorneys** tracks plus shared concepts, written to obey OSED's own invariants (a `test_guide_docs.py` check guards against merits-drift in the community track, requires the disclaimer, and verifies intra-guide links).
```
- [ ] **Step 4: Verify + suite**
```bash
grep -c "docs/guide" README.md   # >=1
cd evals && .venv/bin/pytest tests/test_guide_docs.py -q && .venv/bin/pytest -q ; cd ..
git add docs/guide/README.md docs/guide/concepts/ README.md CHANGELOG.md
git commit -m "docs(guide): complete cross-links + root README pointer + CHANGELOG"
```
Expected: README grep ≥1; ALL guide links resolve (now that every page exists); suite green.

---

## Task 6: Final review + finish

- [ ] **Step 1: Full guide consistency pass** — re-run the guide test and the full suite:
```bash
cd evals && .venv/bin/pytest -q ; cd ..
```
Expected: all green (the guide tests + the rest).
- [ ] **Step 2: Invariant spot-check (the docs honor the invariants):**
```bash
grep -rinE "you have a case|you should sue|broke the law|you will win|you'll win" docs/guide/ | grep -viE "does not mean you have a case|never (tell|say)|do not (tell|say)|without (telling|saying)" || echo "OK: only negated/instructional forms"
```
Read any hit's context — only negated/explanatory forms (e.g. "it does not mean you have a case", or the attorneys page describing what the skill refuses to say) are acceptable.
- [ ] **Step 3: No Claude attribution** — `git log origin/main..HEAD --format="%b" | grep -i "co-authored-by\|claude\|🤖" || echo OK`.
- [ ] **Step 4: Invoke `superpowers:finishing-a-development-branch`** and present the standard options (expected: Push and create a Pull Request; PR body carries NO Claude attribution).

---

## Self-review notes (author)

- **Spec coverage:** Component 1 (location) → Task 1; Component 2 (communities) → Task 3; Component 3 (attorneys) → Task 4; Component 4 (concepts) → Tasks 1–2; Component 5 (writing discipline) → applied across Tasks 2–4; Component 6 (validation) → Task 1 (test + CI paths) + the per-task greps.
- **TDD:** Task 1 writes the test first (red), then the scaffold makes it green; later tasks keep it green as pages are added.
- **Negation-safety:** the merits check reuses `markers.PLAIN_LANGUAGE_FORBIDDEN_ADVICE`, which omits "you have a case" — so the community track's legitimate "it does not mean you have a case" closing does not false-positive (the WI-1 lesson).
- **Link-rot avoidance:** the link test resolves every relative link; the plan defers forward-links until targets exist (Task 5 cross-link pass) to keep the test green at every commit.
- **No new instrument/skill behavior; the climate-news subsystem is untouched and remains flagged.**
- **Eval-safety:** the only `evals/` change is the new `test_guide_docs.py` + the CI `paths` line; no existing fixture/marker is touched.
