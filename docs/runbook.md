# Runbook — running the OSED pipeline by hand

The `pipeline` skill automates these handoffs. This runbook is the same flow for a human (an
attorney or an organizer) to drive directly, and it documents what each hop carries forward and the
invariant checkpoint at each. **OSED drafts; a licensed attorney decides** — the last row is never
optional.

| # | Stage | Run | Carries IN | Produces | Invariant checkpoint |
|---|---|---|---|---|---|
| 1 | Intake | `skills/intake` | the lay concern | routed candidate pathways | no merits; no named-party accusation; routes to counsel where OSED has no coverage |
| 2 | Gap Analysis | `skills/gap-analysis` | the chosen statute | findings table (the factual spine) | currency check present; no UNVERIFIED reported as MISSED; no "you should sue" |
| 3 | Drafting | `skills/drafting` | the findings table | flagged DRAFT instrument | DRAFT banner; `[⚠ ATTORNEY: ...]` on every judgment call; `[placeholder]` for missing facts; currency field |
| 4 | Precedent Retrieval | `skills/precedent-retrieval` | each draft flag that needs law | controlling-law landscape | jurisdiction + weight + currency per case; states the rule, does not apply it to facts |
| 5 | Plain-Language | `skills/plain-language` | the assembled package | lay summary | the six sections; the closing reminder; no merits advice |
| 6 | **Human attorney** | — | the whole package | a decision | reviews, resolves every checklist item, verifies currency, signs/files. **Not optional.** |

## When to stop early (halting is success, not failure)

- **A stage refuses** (intake on harassment/bad-faith; drafting on a bad-faith instrument): stop and
  surface the refusal. Do not route around it.
- **The pathway choice is the human's** (intake returns more than one plausible pathway, or the
  choice turns on the merits): stop and let the human choose.
- **A fact is missing or currency cannot be confirmed:** carry the `[placeholder]` and the flag
  forward; do not invent the fact to keep moving.

## The package

The end product is a single DRAFT case package: routing, findings, flagged draft, controlling law,
plain-language summary, and one **consolidated attorney checklist** gathering every flag, judgment
call, currency flag, and placeholder from all stages — the list the attorney works through. It is a
scaffold for review, never a filing.
