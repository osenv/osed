# OSED — Open Source Environmental Defense

**A library of AI agent skills that turn proven environmental-litigation instruments into something a local actor, in any state, can run again.**

---

## What this is, in plain terms

Suppose a government agency is supposed to do something under an environmental law — issue a rule, clean up a hazard, answer a formal request — and it hasn't. Holding the agency to that duty usually means hiring a litigation team, which most community groups can't afford just to get started.

OSED helps you produce a clean **first draft** of the formal documents that process uses — the notice letters, petitions, and complaints that lawyers call "instruments." You bring the facts and the goal; OSED handles the repetitive structure and **flags every spot where a human judgment call is needed**.

What OSED does **not** do: it does not give legal advice, tell you whether you have a case, or file anything. A licensed attorney must review and decide before any document leaves your hands. See [`DISCLAIMER.md`](DISCLAIMER.md).

The rest of this page explains how that works in more detail, and then how to install it. If you're not technical, you can stop reading at [Repository layout](#repository-layout) — everything before it is meant for you.

---

## The idea in one paragraph

The most replicable asset in a half-century of environmental litigation is not a marquee Supreme Court win. It is procedural machinery: the citizen-suit notice letter, the deadline suit, the administrative petition, the consent-decree scaffold. Cases that turn on singular facts and a particular political moment do not transfer. Instruments do. OSED packages that machinery as a set of [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) — modular, inspectable instruction sets — so that a community group, a county commission, or a small public-interest shop can draft a clean, well-formed legal instrument without first hiring a litigation team.

OSED drafts. A licensed attorney decides. That line is the whole design, and it is enforced in every skill. See [`DISCLAIMER.md`](DISCLAIMER.md) before anything else.

---

## The four agents

Each agent is a skill. Each maps to a stage of the litigation workflow, and each is deliberately scoped to the *mechanical* side of the work.

| Agent | Skill | What it does | What it never does |
|---|---|---|---|
| **Gap Analysis** | [`skills/gap-analysis`](skills/gap-analysis) | Reads a statute, extracts mandatory duties and their deadlines, cross-references the agency's actual record, flags actionable misses. | Decide whether a miss is worth suing over. |
| **Drafting** | [`skills/drafting`](skills/drafting) | Produces the formal instrument: notice of intent, rulemaking petition, deadline complaint, settlement scaffold. | Sign, file, or assert that the instrument is ready to file. |
| **Plain-Language** | [`skills/plain-language`](skills/plain-language) | Translates a legal pathway into terms a non-lawyer can act on. | Give legal advice or predict outcomes. |
| **Precedent Retrieval** | [`skills/precedent-retrieval`](skills/precedent-retrieval) | Surfaces controlling case law for the relevant circuit so a human can judge whether a case survives. | Conclude that a case is safe to file. |

The agents are designed to hand off to each other: Gap Analysis finds the miss, Drafting produces the instrument, Precedent Retrieval attaches the controlling law, Plain-Language makes the whole package legible to the person who has to decide.

---

## Two principles that run through every skill

**1. The templatable / judgment line.** The instruments (decree, notice, petition) are templatable. The suit types (deadline, unreasonable delay) are semi-templatable. The gating doctrines (standing, ripeness) are judgment. Every skill keeps the agent on the mechanical side of that line and routes judgment calls — with retrieved precedent attached — to a human reviewer. An agent that blurs this line produces filings that get dismissed or sanctioned.

**2. The doctrinal-currency check.** Law changes underneath you. A strategy that assumed *Chevron* deference (overturned by *Loper Bright*, 2024) now gives backwards advice; *Seven County* (2025) narrowed NEPA review scope. Before any skill drafts on a doctrine, it runs a currency check. Confident drafting on dead law is the most expensive error this project can make. See [`docs/doctrinal-currency.md`](docs/doctrinal-currency.md).

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
│   └── doctrinal-currency.md      ← how to keep agents off dead law
├── skills/
│   ├── gap-analysis/SKILL.md
│   ├── drafting/SKILL.md
│   ├── plain-language/SKILL.md
│   └── precedent-retrieval/SKILL.md
└── templates/
    ├── cwa-505-notice-of-intent.md
    └── rulemaking-petition.md
```

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
