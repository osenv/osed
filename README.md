# OSED — Open Source Environmental Defense

## What is OSED?

OSED is a library of AI agent skills that turn proven environmental-litigation instruments into something a local actor, in any state, can run again. Those skills are modular, inspectable instruction sets, and together they draft the formal documents of environmental litigation: the citizen-suit notice letter, the rulemaking petition, the deadline complaint, the settlement scaffold.

Each skill reads the governing statute and the facts you provide, drafts a clean first version, and flags every point that calls for legal judgment. A licensed attorney then reviews the draft and decides. That handoff — OSED drafts, an attorney decides — is the whole design, and every skill enforces it. See [`DISCLAIMER.md`](DISCLAIMER.md) before anything else.

---

## Why OSED?

Suppose a government agency is required to do something under an environmental law — issue a rule, clean up a hazard, answer a formal petition — and it hasn't. Holding it to that duty starts with formal paperwork, and that paperwork is the reusable engine of the law: its structure repeats from one case to the next and from state to state, while the facts and the politics are what change. Producing each document to standard has always taken scarce lawyer hours — the resource a community group, a county commission, or a small public-interest shop is most likely to lack. OSED puts that drafting capacity within reach, so the question becomes the merits of the matter rather than the cost of a first draft.

Not technical? Everything meant for you is above [Repository layout](#repository-layout); the rest of this page covers installing the skills.

---

## The agents

Each agent is a skill. Each maps to a stage of the litigation workflow, and each is deliberately scoped to the *mechanical* side of the work.

| Agent | Skill | What it does | What it never does |
|---|---|---|---|
| **Intake** | [`skills/intake`](skills/intake) | Routes a non-lawyer's environmental concern to candidate pathways: likely statute, responsible agency, and the OSED skill to run next. | Decide whether you have a case or whether anyone broke the law. |
| **Gap Analysis** | [`skills/gap-analysis`](skills/gap-analysis) | Reads a statute, extracts mandatory duties and their deadlines, cross-references the agency's actual record, flags actionable misses. | Decide whether a miss is worth suing over. |
| **Drafting** | [`skills/drafting`](skills/drafting) | Produces the formal instrument: notice of intent, rulemaking petition, deadline complaint, settlement scaffold. | Sign, file, or assert that the instrument is ready to file. |
| **Plain-Language** | [`skills/plain-language`](skills/plain-language) | Translates a legal pathway into terms a non-lawyer can act on. | Give legal advice or predict outcomes. |
| **Precedent Retrieval** | [`skills/precedent-retrieval`](skills/precedent-retrieval) | Surfaces controlling case law for the relevant circuit so a human can judge whether a case survives. | Conclude that a case is safe to file. |
| **Pipeline** | [`skills/pipeline`](skills/pipeline) | Runs the whole sequence end to end and assembles a flagged DRAFT case package with a consolidated attorney checklist. | Resolve a flag, strip the DRAFT banner, or decide the merits. |

The agents are designed to hand off to each other: Gap Analysis finds the miss, Drafting produces the instrument, Precedent Retrieval attaches the controlling law, Plain-Language makes the whole package legible to the person who has to decide.

---

## Two principles that run through every skill

**1. The templatable / judgment line.** The instruments (decree, notice, petition) are templatable. The suit types (deadline, unreasonable delay) are semi-templatable. The gating doctrines (standing, ripeness) are judgment. Every skill keeps the agent on the mechanical side of that line and routes judgment calls — with retrieved precedent attached — to a human reviewer. An agent that blurs this line produces filings that get dismissed or sanctioned.

**2. The doctrinal-currency check.** Law changes underneath you. A strategy that assumed *Chevron* deference (overturned by *Loper Bright*, 2024) now gives backwards advice; *Seven County* (2025) narrowed NEPA review scope. Before any skill drafts on a doctrine, it runs a currency check. Confident drafting on dead law is the most expensive error this project can make. Each tracked anchor carries a law-as-of stamp (verified and next-review dates) in [`docs/doctrinal-currency.md`](docs/doctrinal-currency.md) — re-verify before relying.

---

## Repository layout

```
osed/
├── README.md                      ← you are here
├── DISCLAIMER.md                  ← read before use; not legal advice
├── CONNECTORS.md                  ← legal-data sources per agent (use / build / avoid)
├── LICENSE                        ← MIT (code) + CC BY 4.0 note (docs/templates)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── docs/
│   ├── architecture.md            ← the four-agent system, in depth
│   ├── doctrinal-currency.md      ← how to keep agents off dead law
│   ├── examples/                  ← end-to-end worked examples (public matters, no client facts)
│   └── runbook.md               ← run the pipeline by hand, with invariant checkpoints
├── skills/
│   ├── intake/SKILL.md           ← the front door: routes a lay concern to candidate pathways
│   ├── pipeline/SKILL.md        ← the conductor: runs the pipeline, assembles the package
│   ├── gap-analysis/SKILL.md
│   ├── drafting/SKILL.md
│   ├── plain-language/SKILL.md
│   └── precedent-retrieval/SKILL.md
├── templates/
│   ├── cwa-505-notice-of-intent.md
│   ├── cwa-505-deadline-complaint.md
│   ├── consent-decree-deadline.md
│   ├── state-era-pa.md
│   ├── state-era-mt.md
│   ├── state-era-ny.md
│   ├── state-era-hi.md
│   ├── caa-304-emissions-notice.md
│   ├── caa-304-failure-to-act-notice.md
│   ├── caa-304-deadline-complaint.md
│   └── rulemaking-petition.md
├── connectors/
│   └── regulatory/                ← thin wrapper over federal regulatory APIs (Gap Analysis)
└── evals/                         ← eval & red-team harness: verifies skills obey the six invariants
```

`evals/` is the verification arm of the design invariants — exact-marker checks (DRAFT banner,
attorney flags, placeholders) plus a gated live + LLM-judge lane. A change to `skills/` or
`templates/` must keep `cd evals && pytest` green (enforced by CI). See `evals/README.md`.

## Quick start

```bash
git clone <your-remote-url> osed
cd osed
# Install the skills into a Claude Skills-compatible environment, or read them directly.
```

## Status

Seed release. The two templates under `templates/` are the first worked instruments; the skills reference them. The roadmap (in `docs/architecture.md`) lists the next instruments to template, by barrier-to-entry order.

## A note on scope

OSED is built to help people *use* the law that exists to protect public health and the environment. It is not a tool for harassment, for filing instruments in bad faith, or for substituting software judgment for a lawyer's. The skills are written to refuse those uses, and contributors are expected to keep them that way.
