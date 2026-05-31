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
