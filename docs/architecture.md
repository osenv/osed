# Architecture — The Four-Agent System

OSED is built around a single design conviction: **environmental litigation contains a large mechanical layer that is genuinely templatable, sitting beneath a thin layer of judgment that is not.** The agents own the mechanical layer. Humans own the judgment. Everything in this repository is arranged to keep that boundary sharp, because the most expensive failures happen exactly when it blurs.

## The templatable / judgment spectrum

Every task in this domain sits somewhere on a spectrum:

```
TEMPLATABLE  ───────────────────────────────────────────────  JUDGMENT
the instruments        the suit types            the gating doctrines
(notice, petition,     (deadline suit,           (standing, ripeness,
 consent decree)        unreasonable delay)        whether to sue at all)

  agents do this        agents draft,             agents surface +
                        humans verify             route to humans, full stop
```

- **Instruments** are templatable. A §505 notice has required elements; supply them correctly and the instrument is well-formed. An agent does this well.
- **Suit types** are semi-templatable. A deadline suit is nearly binary (did the agency act by the date?); an unreasonable-delay suit turns on a "how long is too long" judgment. Agents draft the structure and flag the judgment.
- **Gating doctrines** are judgment. Standing, ripeness, and "should we file" depend on specific facts, forum, strategy, and risk tolerance. Agents do **not** decide these. They surface the question with the controlling law attached and stop.

An agent that drifts leftward stays useful. An agent that drifts rightward — that starts deciding whether to sue — produces filings that get dismissed or sanctioned and damages real cases. The skills are written to resist that drift; the disclaimers and flags are the brakes.

## The four agents and how they hand off

```
        ┌──────────────────┐
        │     INTAKE       │  routes a lay problem description to candidate
        │  (front door)    │  pathways (statute / agency / instrument); never
        │                  │  decides the merits
        └────────┬─────────┘
                 │ a routed pathway (which statute/agency/instrument fits)
                 ▼
        ┌──────────────────┐
        │  GAP ANALYSIS    │  reads statute → finds missed mandatory
        │                  │  deadline → structured findings table
        └────────┬─────────┘
                 │ findings table (the factual spine)
                 ▼
        ┌──────────────────┐        ┌──────────────────────────┐
        │   DRAFTING       │◄──────►│  PRECEDENT RETRIEVAL      │
        │                  │ flags  │  controlling law for each │
        │ instrument as a  │ that   │  judgment call, by forum, │
        │ flagged DRAFT    │ need   │  with currency checked    │
        └────────┬─────────┘ law    └──────────────────────────┘
                 │ drafted instrument + attached precedent
                 ▼
        ┌──────────────────┐
        │  PLAIN-LANGUAGE  │  makes the whole package legible to the
        │                  │  non-lawyer who has to decide
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │  HUMAN ATTORNEY  │  makes every judgment call; reviews, completes,
        │                  │  verifies, signs, files. Not optional.
        └──────────────────┘
```

The handoffs are deliberate:

- **Intake → Gap Analysis.** A non-lawyer's concern is routed to the likely statute/agency/instrument. Intake identifies the *pathway*, never the *merits* — it makes no strategic call, so it stays on the mechanical side of the line.
- **Gap Analysis → Drafting.** The findings table is the factual spine of the instrument. Drafting never invents facts; it draws them from the verified table or flags them as needed.
- **Drafting ↔ Precedent Retrieval.** Wherever Drafting hits a judgment call (is the violation "ongoing"? does standing exist?), it doesn't resolve it — it requests the controlling precedent so the human reviewer sees the law and the question together.
- **Anything → Plain-Language.** Whenever the audience is a non-lawyer, Plain-Language translates without crossing into advice.
- **Everything → Human.** The terminal node is always a licensed attorney. No agent output is final.

**The conductor.** `skills/pipeline` runs this whole sequence end to end so a non-lawyer need not
chain the skills by hand: it threads each artifact into the next (findings table → draft spine;
draft flags → precedent requests) and assembles one flagged DRAFT case package with a consolidated
attorney checklist. It automates the handoffs, never the judgment — every banner, flag, and currency
check is carried forward intact, it halts rather than guess past a refusal or a merits-laden choice,
and it terminates at the human attorney. `docs/runbook.md` is the same flow for a human to drive by
hand.

## Why these four, and not more

These four cover the litigation pipeline end to end — find the problem, build the instrument, ground it in law, make it legible — while each stays cleanly on the mechanical side of one stage. Adding agents that make strategic calls (a "should we sue" agent, a "will we win" agent) would violate the core design and is explicitly out of scope.

Intake is a front door, not a fifth strategic agent: it routes a concern to one of these stages, and like the others it stays on the mechanical side — it never decides whether the law was broken or whether to sue.

## Roadmap — instruments to template next

Ordered by barrier-to-entry, lowest first, because the lowest-barrier instruments serve the open-source community model best:

1. **Administrative rulemaking petition** — done (`templates/rulemaking-petition.md`). No court, no lawyer required to file.
2. **CWA §505 Notice of Intent** — done (`templates/cwa-505-notice-of-intent.md`). The formulaic gateway to citizen suits.
3. **Clean Air Act §304 notice** — next; close cousin of §505 with its own service and content rules.
4. **Deadline complaint** — scaffold directly from a Gap Analysis findings table.
5. **Consent-decree settlement scaffold** — the negotiated, court-enforceable schedule; teaches the system to generate settlement structure, not just complaints.
6. **State environmental-rights-act claim packet** — per-state variants (PA Art. I §27, NY Green Amendment, MT, HI). High access-to-justice value; heavy Plain-Language involvement.

## Design invariants (do not regress these)

1. Every drafted instrument is a marked DRAFT requiring attorney review.
2. Every judgment call is flagged inline, never silently resolved.
3. Every cited authority passes a doctrinal-currency check or is flagged.
4. No agent invents facts; missing facts become placeholders plus flags.
5. No agent tells a user they have a case, should sue, or will win.
6. The skills refuse harassment and bad-faith filing uses.
