# WI-3 — Golden Worked-Example Transcripts: Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-05-30 · **Branch:** `wi-3-golden-transcripts` (off `main`, WI-1 + WI-2 merged)
**Implements:** WI-3 of `docs/plans/derisking-structural-pass.md` · **Serves:** documentation + regression anchors

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant.

## Goal

Produce two complete, public, no-client-facts **worked examples** that run the full OSED pipeline
end-to-end — Gap Analysis → Drafting ↔ Precedent Retrieval → Plain-Language → human attorney —
with the **handoffs shown explicitly**. They serve two purposes at once:

1. **Documentation** — a reader sees how the four agents chain into one coherent matter.
2. **Regression anchors** — each pipeline stage is registered as an eval fixture, so the gated
   live lane catches a skill change that degrades the worked output (the WI-1 mechanism).

## Decisions resolved during brainstorming

1. **Branch:** WI-1 + WI-2 merged to `main`; WI-3 starts on a fresh branch off `main`. The skills
   therefore carry WI-2's tool-backed currency wording, which the transcripts model.
2. **Two matters, spanning both templates and both suit types:**
   - **Matter A — CWA §304(m) effluent-guideline missed deadline** → deadline-suit pathway →
     CWA §505-style notice / deadline instrument (`templates/cwa-505-notice-of-intent.md`).
   - **Matter B — rulemaking petition** → petition-to-act pathway → rulemaking petition
     (`templates/rulemaking-petition.md`).
3. **Production = hand-authored golden exemplars (Approach A)**, registered as fixtures;
   deterministic in CI, runnable in the gated live lane. Honestly labeled as *curated reference
   exemplars*, not verbatim machine output.
4. **Dual representation:** a readable narrative under `docs/examples/` + per-stage fixtures whose
   `.out.md` content is quoted in the narrative.
5. **Real, verified precedent:** precedent stages cite only cases confirmed to resolve via WI-2's
   `verify_citation`. Confirmed during design: *Massachusetts v. EPA*, 549 U.S. 497 (Matter B);
   *Gwaltney*, 484 U.S. 49 (Matter A anchor). A misremembered TRAC citation (`750 F.2d 70`) was
   caught as non-resolving and excluded — the authoring step re-runs `verify_citation` on every
   cite.

## The regression-anchor mechanism (why this is honest)

A recorded `.out.md` graded by deterministic checks does **not**, by itself, catch skill
*degradation* — the file is static, so it keeps passing if the live skill regresses. As in WI-1:
the **deterministic** lane proves the exemplar is self-consistent (and anchors the harness); the
**gated `-m live` lane** re-runs the skill on the matter's input and grades fresh output against
the same checks — that is the actual regression detector. WI-3 fixtures get both, exactly like
WI-1 fixtures.

## Components

### 1. Narrative transcripts (`docs/examples/`)

- `docs/examples/cwa-304m-deadline-suit.md`
- `docs/examples/rulemaking-petition.md`
- `docs/examples/README.md` — short index explaining what these are and the honest framing.

Each narrative shows the four stages in order with a **handoff annotation** between them, making
the chaining explicit:

- **Intake → Gap Analysis:** the statute + facts in; the findings table out.
- **Gap Analysis → Drafting:** the findings table becomes the draft's *factual spine* (the
  narrative points to which row populates which part of the instrument).
- **Drafting ↔ Precedent Retrieval:** a specific `[⚠ ATTORNEY: ...]` flag in the draft spawns a
  precedent request; the retrieved landscape flows back as attached law for that flag.
- **→ Plain-Language:** the pathway translated for a lay audience.
- **→ Human attorney (terminal node):** the package stops here; the narrative states plainly that
  the attorney decides.

Each file opens with a header: *public matter, no client facts; curated reference exemplars, not
verbatim machine output; subject to the doctrinal-currency rule (`docs/doctrinal-currency.md`).*

### 2. Per-stage fixtures (8 total = 2 matters × 4 stages)

Under `evals/fixtures/<skill>/<matter>-<stage>.json` + `.out.md`, e.g.
`evals/fixtures/gap-analysis/cwa-304m-deadline.json`,
`evals/fixtures/drafting/cwa-304m-deadline-notice.json`, etc. Naming uses a shared matter prefix
(`cwa-304m-…`, `rulemaking-petition-…`) so a matter's stages are grep-able as a set.

Each fixture grades its stage's `.out.md` with that skill's **established checks** (reused from the
WI-1/WI-2 fixtures):

- gap-analysis: `Doctrinal-currency check:` field; handoff disclaimer "This is a factual map, not a
  recommendation to sue."; no-sue-advice forbidden list.
- drafting: DRAFT banner; `Doctrinal-currency check:`; `[⚠ ATTORNEY: ...]` flag regex; `[placeholder]`;
  `REQUIRED-ELEMENTS CHECKLIST` / `CONSOLIDATED ATTORNEY FLAGS` / `DEADLINE NOTE`; not-finalized
  forbidden list.
- precedent-retrieval: `Currency check:`; the two required sections; no-prediction forbidden list.
- plain-language: the six section headers; the closing reminder; no-merits-advice forbidden list.

**Plus a matter-specific handoff check** where it adds value, e.g.:
- gap → a `contains` check that the findings/handoff names the downstream stage.
- drafting → a `judge` check (gated) that the draft's factual allegations trace to the findings
  table rather than inventing facts.

The `.out.md` stage output is the same text quoted in the corresponding narrative section (mild,
accepted duplication for two matters; no generator built).

### 3. Verified precedent (dogfooding WI-2)

- **Matter B precedent stage:** *Massachusetts v. EPA*, 549 U.S. 497 (2007) — the agency's duty to
  respond to a rulemaking petition and arbitrary-capricious review of a denial. Currency note in
  the transcript: still good law; flag the major-questions / *West Virginia v. EPA* context as a
  CHANGED-adjacent consideration for counsel, not a DEAD classification.
- **Matter A precedent stage:** a verified CWA citizen-suit / nondiscretionary-duty case;
  *Gwaltney*, 484 U.S. 49 (1987) is the confirmed anchor for citizen-suit structure. Final case
  selection for the §505(a)(2) deadline standard is confirmed with `verify_citation` during
  authoring; any cite that does not resolve is excluded.

## Testing strategy

- **Deterministic (CI):** all 8 new fixtures graded green. A parametrized positive test registers
  them (extend `evals/tests/test_negative_control.py` or add `evals/tests/test_golden_examples.py`).
- **Gated live (`-m live`):** the matters' inputs are runnable through the existing live runner +
  judge; this is the regression-anchor lane (no new live infrastructure required; optionally add
  one gated end-to-end smoke per matter).
- **Regression:** the full existing WI-1 eval suite stays green; no marker or invariant changes.

## Documentation touch

- Add `docs/examples/` to the README "Repository layout" tree and a one-line pointer.
- `docs/examples/README.md` indexes the two examples and states the honest framing.

## Honest limits / out of scope

- The narratives are *exemplars of correct behavior*, not evidence the live skills currently
  produce them — the gated live lane verifies that on demand.
- Mild content duplication between each narrative and its stage `.out.md` files (accepted; no build
  step for two examples).
- No new instrument templates are created; Matter B uses the existing `rulemaking-petition.md`.
- Precedent currency is modeled honestly in-transcript (classification + flags), not asserted as a
  permanent verdict — the cases were verified to *resolve*, not blessed as eternally good law.

## Open questions

None blocking. Minor, resolvable in planning: whether the matter-specific handoff "factual-spine"
check is deterministic (a `contains` on a shared identifier between findings and draft) or a gated
judge check; and the exact §505(a)(2) deadline-standard case for Matter A (confirmed via
`verify_citation` at authoring time).
