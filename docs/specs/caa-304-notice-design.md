# CAA §304 Notice Instrument — Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-05-31 · **Branch:** `caa-304-notice` (off `main`, WI-1–WI-6 merged)
**Implements:** Roadmap item 3 of `docs/architecture.md` ("Clean Air Act §304 notice — next; close cousin of §505 with its own service and content rules") — the first *expansion* instrument after the de-risking pass.

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant; preserves all six.

## Goal

Add the Clean Air Act §304 citizen-suit notice to OSED's instrument library, end to end: two
templates (the two genuinely distinct §304 notice types), wire them into the `drafting` and
`intake` skills, and prove the whole pathway with two public worked examples plus deterministic
eval fixtures. The instrument is the air analog of the already-shipped CWA §505 notice; shipping it
gives the repo a matched air/water pair for both the violation-notice and the deadline-notice
spines.

## The defining design fact (verified, not remembered)

CAA §304 (42 U.S.C. §7604) splits into distinct notice types. During brainstorming the statutory
text of **§7604(b)** was pulled from a primary source to avoid drafting from memory — and it
corrected a memory error worth recording so it cannot reappear:

- **Both** notice tracks run **60 days**, *not* 60-vs-180. (An initial recollection of a "180-day"
  failure-to-act clock was wrong; §7604(b)(2) says 60 days.) The implementer **must** re-confirm
  every period and recipient list via the connector (`get_uscode_section` for 42 U.S.C. §7604,
  `get_current_regulation` for 40 C.F.R. Part 54) **before writing any number** — never from memory.
  This is the doctrinal-currency invariant applied to our own drafting.
- The two tracks differ by **defendant and recipients**, not by clock:
  - **§304(a)(1)** — emission-standard/limitation or order violation. Defendant: the alleged
    violator (a stationary source). Notice served on the **Administrator, the State, and the alleged
    violator**. Immediate-suit exception for violations of §111 (NSPS) or §112 (HAP). A
    diligent-prosecution bar applies (EPA/State already prosecuting).
  - **§304(a)(2)** — the Administrator's failure to perform a **nondiscretionary** act or duty.
    Defendant: the **Administrator**. Notice served on the **Administrator only**. Immediate-suit
    exception for violations of §7412(i)(3)(A) or (f)(4).
- Service and content rules live in **40 C.F.R. Part 54** (the CAA analog of §505's Part 135) —
  tag it for tool-verification, do not assume the part number is current.

This split is why two templates beat one: a combined file would blur the recipient list and the
defendant, the two things most likely to be gotten wrong.

## Decisions resolved during brainstorming

1. **Two templates** (not one combined, not 60-day-emissions-only): `caa-304-emissions-notice.md`
   and `caa-304-failure-to-act-notice.md`.
2. **Full scope:** templates + skill wiring + two end-to-end golden examples + eval fixtures +
   docs/freshness updates + a legal-soundness gate.
3. **Both tracks get an end-to-end golden example** (a matched air pair beside WI-3's water pair).
4. **One branch / one PR**, with the plan sequenced templates → wiring → examples → fixtures → docs
   so each stage is independently reviewable.
5. **Branch base:** off `main` (WI-1–WI-6 merged via PRs #1–#7).

## Component 1 — Two templates

Both follow the proven structure of `templates/cwa-505-notice-of-intent.md`: a DRAFT-scaffold
banner; a "why the formality matters" note; a required-elements checklist; the DRAFT body with
inline `[⚠ ATTORNEY: ...]` flags and `[placeholder]` for every missing fact; a deadline note; and a
consolidated attorney-flags section. Every authority cited (42 U.S.C. §7604, 40 C.F.R. Part 54, and
the underlying standard) carries a **tool-backed** currency-check flag — the template never asserts
a citation as current.

### `templates/caa-304-emissions-notice.md` — §304(a)(1), the §505 cousin

- **Defendant:** the alleged violator (stationary source).
- **Service list:** EPA Administrator + the State in which the violation occurs + the alleged
  violator (per 40 C.F.R. Part 54 — flag to confirm the current list and addresses).
- **Required elements:** identity of the notifying party (and counsel); identity of the alleged
  violator; the **specific emission standard, limitation, or order** alleged violated; the activity
  constituting the violation; the location (facility / emission unit / stack); the date(s) or date
  range; the **ongoing/recurring** characterization (`[⚠ ATTORNEY: ...]` — the *Gwaltney*-analog
  legal judgment, counsel's call); the **§111/§112 immediate-suit exception** note (flag — whether
  the 60-day wait is even required here is counsel's call); the **diligent-prosecution bar** note
  (flag — an ongoing EPA/State action can bar the suit); attorney signature/review block.
- **Clock:** 60 days (verify via tool).

### `templates/caa-304-failure-to-act-notice.md` — §304(a)(2), the deadline cousin

- **Defendant:** the EPA Administrator.
- **Service list:** the Administrator only (per 40 C.F.R. Part 54 — flag to confirm).
- **Required elements:** identity of the notifying party (and counsel); the **specific
  nondiscretionary duty** the Administrator failed to perform and its **statutory hook**; the
  **statutory deadline** and the date it came due; the fact of non-performance (drawn from the
  agency record, never assumed — `[placeholder]` + flag where the record isn't supplied); the
  **§7412(i)(3)(A)/(f)(4) immediate-suit exception** note (flag); attorney signature/review block.
- **Clock:** 60 days (verify via tool).
- **Feed:** this instrument is the natural consumer of a Gap Analysis findings table (the
  "did the agency act by the statutory date?" spine), exactly as the deadline complaint is.

## Component 2 — Skill wiring

- **`skills/drafting/SKILL.md`** — add two rows to the "Choosing the instrument" table:
  - CAA §304 emission-violation notice → `templates/caa-304-emissions-notice.md`
  - CAA §304 failure-to-act notice → `templates/caa-304-failure-to-act-notice.md`

  No behavior change; the existing §505 worked example and guardrails stay. (Optionally generalize
  the table's existing "Notice of Intent" row wording so it reads as a family, not CWA-only.)
- **`skills/intake/SKILL.md`** — flip the Clean Air Act row of the recognizer table from
  `counsel (a CAA instrument is on the roadmap, not yet built)` to
  `Gap Analysis → Drafting (§304 notice)`. Keep the honesty rule: note that the emissions track is
  fact-driven (may go straight to Drafting) while the failure-to-act track rides Gap Analysis.
  Update the skill's example only if needed to stay consistent (no merits change).

## Component 3 — Two golden examples + eval fixtures

Under `docs/examples/`, matched to the WI-3 water pair, each a narrative run end to end through
**intake → gap-analysis → drafting → plain-language**:

- **`caa-304-failure-to-act-suit.md`** — a public CAA §304(a)(2) nondiscretionary-duty miss (the air
  analog of the CWA §304(m) deadline example). Gap Analysis reads the statutory duty + deadline and
  checks the agency record; Drafting produces the failure-to-act notice.
- **`caa-304-emissions-notice.md`** — a public CAA §304(a)(1) emission-violation matter. Gap Analysis
  reads the applicable emission standard and the exceedance record; Drafting produces the emissions
  notice.

The specific public matters and case citations are chosen **at build time** (not pinned here) and
**every cite is verified live via `verify_citation`** before it goes in, exactly as WI-3 did
(unresolvable cites are dropped, not "fixed").

**Fixtures:** 8 per-stage golden fixtures (2 matters × 4 stages) under
`evals/fixtures/<skill>/caa-304-*`, registered in a new `evals/tests/test_caa_304_examples.py`
mirroring `test_golden_examples.py`. Deterministic marker checks only (DRAFT banner, `[⚠ ATTORNEY]`,
`[placeholder]`, required section headers, negation-collision phrases routed to `judge`/excluded
from `forbidden` per the WI-1/WI-2 lesson). These drafting-stage fixtures subsume the standalone
drafting fixture from the scope menu — no separate fixture needed.

## Component 4 — Docs / freshness updates

- **`docs/architecture.md`** — mark roadmap item 3 **done** (`templates/caa-304-emissions-notice.md`,
  `templates/caa-304-failure-to-act-notice.md`).
- **`README.md`** — add both templates to the repository-layout tree.
- **`CHANGELOG.md`** — under `## [Unreleased]`: **Added** (the two CAA §304 templates; the two golden
  examples + 8 fixtures); **Changed** (intake's CAA row, now built; drafting's instrument table).
  Per WI-6's going-forward rule that `templates/`, `skills/`, `docs/examples/`, and `evals/` changes
  get a changelog entry.
- **`CLAUDE.md`** — one-line update where the build-order / instrument coverage is described, noting
  §304 is shipped (no duplicate dates; the doctrinal stamp remains the single source of truth).

## Component 5 — Legal-soundness gate (load-bearing)

Before the branch finishes, a dedicated legal-soundness pass — the WI-3 step that caught three
exemplar errors — must:

1. Confirm **both** notice periods (60 days) and **both** recipient lists against §7604(b) via
   `get_uscode_section`; confirm **40 C.F.R. Part 54** is the operative notice regulation via
   `get_current_regulation`.
2. Confirm the failure-to-act example classifies the missed duty using gap-analysis's own status
   taxonomy correctly (the WI-3 `MISSED — DEADLINE` vs `UNREASONABLE DELAY` lesson).
3. Confirm every example citation resolves via `verify_citation`; drop any that don't.
4. Record the verified **law-as-of** date in the examples (dated artifacts, subject to the currency
   rule) — not in the doctrinal-anchor stamp, which is reserved for the tracked doctrines.

`cd evals && pytest` (deterministic lane) stays green throughout; the new test runs in CI.

## Testing strategy

- `evals/tests/test_caa_304_examples.py` runs in the deterministic CI lane (no secrets); the full
  WI-1 suite stays green. `verify_citation` runs are a **build-time** verification step, not a CI
  test (CI needs no keys), consistent with WI-3.
- Confirm the eval CI `paths` filter already covers `templates/`, `docs/examples/`, and the new
  test file; extend it if not.

## Honest limits / out of scope

- No new connector code, no new skill, no new marker. This is templates + two skills' wiring + docs
  + examples + fixtures.
- The doctrinal-anchor "Worth tracking" stamp in `docs/doctrinal-currency.md` is **not** touched —
  §304 / Part 54 are statutory/regulatory hooks the templates currency-check at use time, not
  Loper/Seven-County-class doctrines. (If the legal-soundness pass surfaces a genuinely tracked
  doctrine, that's a separate, flagged addition.)
- Specific public matters and citations for the examples are chosen and verified at build time, not
  fixed in this spec.

## Six-invariant check

1. **DRAFT banner** — both templates and both drafting fixtures carry it. ✓
2. **Inline `[⚠ ATTORNEY]` flags** — every judgment call (ongoing/recurring, immediate-suit
   eligibility, diligent-prosecution bar, recipient list, deadline computation) is flagged. ✓
3. **Doctrinal-currency check** — templates tool-verify §7604 + Part 54 + the underlying standard;
   examples verify cites via `verify_citation`. The 180→60 correction is the invariant in action. ✓
4. **No invented facts** — `[placeholder]` + flag for every dial, date, party, and duty not supplied
   from a record. ✓
5. **No "you have a case / should sue / will win"** — inherited from drafting/intake; the
   examples model routing and drafting, never a merits call. ✓
6. **Refuse harassment / bad-faith** — inherited from the wired skills; unchanged. ✓

## Open questions

None blocking. Resolvable in planning/build: the exact public matters for the two examples (chosen +
`verify_citation`-confirmed at build time); whether to generalize the drafting table's NOI row
wording; and whether the eval CI `paths` filter needs extending.
