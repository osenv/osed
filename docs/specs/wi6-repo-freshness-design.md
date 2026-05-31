# WI-6 — Repo Freshness / Versioning: Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-05-31 · **Branch:** `wi-6-repo-freshness` (off `main`, WI-1–WI-5 merged)
**Implements:** WI-6 of `docs/plans/derisking-structural-pass.md` · **Cross-cutting (the final item)**

> Design spec, not a plan. Records the validated design as input to `writing-plans`. Changes no
> design invariant.

## Goal

Keep the repo's own doctrinal anchors from quietly rotting into the exact failure
`docs/doctrinal-currency.md` warns against. Today its "Worth tracking" anchors (*Loper Bright*,
*Seven County*, Major Questions, standing) are a bare list with no verification date and no
next-review date. WI-6 stamps them, adds a `CHANGELOG.md`, documents a re-verification cadence, and
— applying the project's own de-risking ethos to its docs — adds a deterministic check that the
stamp is present and well-formed so it can't silently disappear.

## Decisions resolved during brainstorming

1. **Branch:** WI-1–WI-5 merged; WI-6 starts on a fresh branch off `main`.
2. **Enforcement level: docs + a deterministic structure check** (not docs-only; not a date-aware
   staleness CI). The check is date-agnostic — it asserts the stamp exists and is well-formed, never
   "is it past due" (that needs today's date and is deliberately out of scope).
3. **Single source of truth for the stamp:** the canonical verified/next-review dates live only in
   `doctrinal-currency.md`; `CLAUDE.md` and `README.md` point to it rather than carrying their own
   dates (the `markers.py` pattern — prevents date drift).
4. **Cadence: quarterly default** (next-review 3 months out) + *always before relying* + a sweep
   after the U.S. Supreme Court term ends (late June/early July).
5. **CHANGELOG: Keep-a-Changelog style**, a `0.1.0 — seed` entry organized by the de-risking pass
   (WI-1…WI-6), plus an `Unreleased` heading.

## Component 1 — "Law-as-of" stamps (`docs/doctrinal-currency.md`)

In the "## Worth tracking" section:
- A header line: **`Law-as-of: 2026-05-31.`** followed by one sentence defining re-verifying:
  confirm in primary sources, update both dates, and note the change in `CHANGELOG.md`.
- Each anchor bullet gains a trailing stamp in a fixed format:
  `... (verified 2026-05-31; re-verify by 2026-08-31).`
- The four current anchors (*Loper Bright*, *Seven County*, Major Questions, standing) each get the
  stamp. Their prose is unchanged; only the dated tag is appended.

`CLAUDE.md` (the "Doctrinal-currency check" section, which names *Loper Bright*/*Seven County*) and
`README.md` (the "doctrinal-currency check" principle) gain a one-line pointer:
*"these anchors carry a law-as-of stamp in `docs/doctrinal-currency.md` — re-verify before relying."*
They do **not** carry their own dates.

## Component 2 — `CHANGELOG.md`

A root `CHANGELOG.md`, Keep-a-Changelog format (`## [Unreleased]` then `## [0.1.0] — 2026-05-31`).
The 0.1.0 "seed" entry summarizes the de-risking pass, grouped Added/Changed, organized so each
work item is legible:
- **Added** — the eval & red-team harness (`evals/`, WI-1); the regulatory connector's currency
  tools `find_rule_changes` + `verify_citation` (WI-2); golden worked-example transcripts
  (`docs/examples/`, WI-3); the `intake` front-door skill (WI-4); the `pipeline` conductor skill +
  `docs/runbook.md` (WI-5); doctrinal-anchor law-as-of stamps, this changelog, and the
  re-verification cadence (WI-6).
- **Changed** — the four skills' currency step made tool-backed (WI-2); docs reframed around the
  six skills (intake + four core + pipeline).

Going-forward note at the top: changes to `skills/`, `templates/`, `connectors/`, `evals/`, and the
**doctrinal anchors** get a changelog entry; re-verifying an anchor updates its stamp dates and adds
an entry here.

## Component 3 — re-verification cadence (`docs/doctrinal-currency.md` + pointer)

A new "## Re-verification cadence" section in `doctrinal-currency.md`:
- **Who:** maintainers and any contributor whose change relies on or touches an anchor.
- **How often:** re-verify each anchor by its `re-verify by` date; default cadence **quarterly**;
  **always** re-verify before relying on an anchor in a real matter; and sweep the
  deference / standing / major-questions anchors **after the U.S. Supreme Court term ends**
  (late June / early July), when the most consequential shifts land.
- **The rule:** re-verifying means confirming in primary sources, then updating both stamp dates and
  adding a `CHANGELOG.md` entry. A stamp is a record that a human checked — never a substitute for
  checking.

A one-line pointer is added to `CONTRIBUTING.md` (so contributors find the cadence).

## Component 4 — the deterministic structure check (`evals/tests/test_freshness.py`)

A pytest that reads `docs/doctrinal-currency.md` from the repo root (path via `parents[...]`) and
asserts, **date-agnostically**:
1. The "## Worth tracking" section contains a `Law-as-of: <YYYY-MM-DD>` header.
2. **Every** anchor bullet in that section (lines beginning `- `) carries a stamp matching
   `\(verified \d{4}-\d{2}-\d{2}; re-verify by \d{4}-\d{2}-\d{2}\)`.

Written TDD: it fails on the current bare list (Component 1 not yet applied), and passes once the
stamps are added. It uses no secrets and no current-date logic, so it runs in the deterministic CI
lane. The eval CI workflow's `paths` filter is extended to include `docs/doctrinal-currency.md` so
editing the anchors (or removing a stamp) triggers the check.

## Testing strategy

- `test_freshness.py` runs in CI (deterministic); the full WI-1 eval suite stays green; no skill
  or marker change.
- The structure check is the verification arm of the freshness stamp — exactly as `evals/` is the
  verification arm of the six invariants.

## Honest limits / out of scope

- The structure check proves the stamp **exists and is well-formed**, NOT that the law was actually
  re-verified or that an anchor is not past due. "Did a human really check?" and "is today past the
  re-verify date?" are out of scope (the latter needs the current date and would be a separate
  advisory script/cron). The cadence section says this plainly.
- WI-6 adds no skill, connector, or runtime code — only docs, a changelog, and one doc-structure
  test (+ a CI `paths` line).
- Stamps are applied to the doctrinal anchors specifically; the worked examples and specs already
  state they are subject to the currency rule and are dated artifacts — they are not re-stamped.

## Open questions

None blocking. Minor, resolvable in planning: whether `test_freshness.py` lives under `evals/tests/`
(reuses the harness venv + CI; chosen default) or a standalone `scripts/`; and the exact
Added/Changed wording in the 0.1.0 changelog entry.
