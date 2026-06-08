# Changelog

All notable changes to OSED are recorded here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Changes to `skills/`, `templates/`, `connectors/`, `evals/`, and the **doctrinal anchors** in
`docs/doctrinal-currency.md` get an entry. Re-verifying an anchor updates its stamp dates (there)
and adds an entry here.

## [Unreleased]

## [0.2.0] — 2026-06-07

State-ERA packets, the CAA §304 / deadline-complaint / consent-decree instruments, and OSED's
distribution surfaces: the Claude Code plugin and the Cowork skill bundles (six self-contained zips,
shipped via the `v0.2.0` GitHub Release) backed by a self-hostable remote regulatory connector.

### Added
- End-to-end user guide under `docs/guide/` — parallel **For communities** and **For attorneys** tracks plus shared concepts, written to obey OSED's own invariants (a `test_guide_docs.py` check guards against merits-drift in the community track, requires the disclaimer, and verifies intra-guide links).
- Four state-ERA doctrinal anchors (PA Art. I §27, MT Art. II §3/Art. IX §1, NY Art. I §19 Green Amendment, HI Art. XI) added to the tracked "Worth tracking" list in `docs/doctrinal-currency.md`, each law-as-of stamped.
- State environmental-rights-act orientation packets for PA, MT, NY, and HI (`templates/state-era-*.md`): plain-language-led, law-as-of stamped, with NY and HI framed as developing law. Four worked examples (`docs/examples/state-era-*.md`) and four packet fixtures (`evals/tests/test_state_era_packets.py`).
- Clean Air Act §304 citizen-suit notice instrument: two templates — `templates/caa-304-emissions-notice.md` (§304(a)(1) emission violations) and `templates/caa-304-failure-to-act-notice.md` (§304(a)(2) failure to perform a nondiscretionary duty).
- Deadline-complaint instrument (the first court filing): `templates/cwa-505-deadline-complaint.md` (CWA §505(a)(2)) and `templates/caa-304-deadline-complaint.md` (CAA §304(a)(2)) — citizen-suit "failure to perform a nondiscretionary duty" complaints, with standing/jurisdiction/venue flagged for counsel.
- A "Stage 5 — Deadline Complaint" added to both deadline worked-examples (`docs/examples/cwa-304m-deadline-suit.md`, `docs/examples/caa-304-failure-to-act-suit.md`), each registered as a drafting eval fixture.
- Consent-decree settlement scaffold (`templates/consent-decree-deadline.md`): the negotiated resolution of a deadline/duty suit, statute-agnostic, with every term flagged for the parties to negotiate (the software proposes none). A "Stage 6 — Consent Decree" was added to the CWA §304(m) worked example and registered as a drafting eval fixture.
- OSED is now installable as a **Claude Code plugin** via a self-hosted marketplace (`.claude-plugin/marketplace.json` + `plugin.json`): the six skills, the instrument templates, and the `osed-regulatory` MCP connector (built into a persistent Python venv by a SessionStart hook; optional CourtListener / Regulations.gov keys via plugin config). See the README "Install as a Claude Code plugin" section.
- **Claude Cowork distribution**: `scripts/pack-skills.mjs` packs each skill into a self-contained `.zip` (vendoring the templates/docs it references) for upload to claude.ai / Cowork, with a generated `MANIFEST.md`; an end-user `docs/skills-in-cowork.md` walkthrough and `docs/distribution-org-path.md` for centralized org rollout.
- **Remote regulatory connector**: the connector now also serves streamable HTTP at `/mcp` (`osed-connectors-http`) so it can be hosted as a remote MCP for Cowork/claude.ai; CI tests and publishes a multi-arch image to GHCR (`ghcr.io/osenv/osed-connector`), and `connectors/regulatory/DEPLOY.md` covers self-hosting and the who-hosts/whose-keys privacy choice. The stdio transport (Claude Code plugin) is unchanged — one codebase, two transports.

### Changed
- `skills/drafting`, `skills/intake`, and `skills/plain-language` wire the state-ERA packets into the pathway.
- `skills/drafting` routes the two CAA §304 notice types to the new templates.
- `skills/intake` now routes Clean Air Act concerns to the built §304 pathway (previously "on the roadmap, not yet built").
- `skills/drafting` routes deadline complaints to the new templates and marks complaints as court filings.
- `skills/drafting` routes the consent-decree scaffold to its template and marks decrees as negotiated instruments.
- Skills reference shared resources (templates, the doctrinal-currency doc) via `${CLAUDE_SKILL_DIR}/../..` so the paths resolve identically in development and when installed as a plugin; the currency reference notes the bundled doc is a snapshot (run `/plugin marketplace update` + re-verify).

### Fixed
- Connector docs corrected to reflect **six** tools, not four: `CONNECTORS.md`, `CLAUDE.md`, and `connectors/regulatory/README.md` (table + tool docs) had lagged behind the WI-2 currency tools (`find_rule_changes`, `verify_citation`), and several places still said Regulations.gov was the "only keyed source" — CourtListener (`verify_citation`) is keyed too. No code change.

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
