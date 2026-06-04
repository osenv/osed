# Running the pipeline

The `pipeline` skill runs the whole sequence end to end; the [runbook](../../runbook.md) is the same
flow for you to drive by hand. Either way the stages and their invariant checkpoints are identical:

1. **Intake** — routes a lay concern to candidate pathways (statute / agency / instrument). No
   merits, no named-party accusation; routes to counsel where OSED has no coverage.
2. **Gap Analysis** — reads the chosen statute, extracts mandatory deadline-bound duties, checks the
   agency record, and produces a findings table (the factual spine). Currency check present; an
   UNVERIFIED authority is never reported as a missed duty.
3. **Drafting ↔ Precedent Retrieval** — drafts the instrument as a flagged DRAFT; wherever it hits a
   judgment call it requests the controlling precedent (by forum, with currency) rather than
   resolving it. Precedent states the rule; it does not apply it to the facts.
4. **Plain-Language** — makes the assembled package legible to the non-lawyer who has to decide,
   without crossing into advice.
5. **The human attorney** — the terminal node, always. You review, resolve every checklist item,
   verify currency, sign, and file. Not optional.

## Halting is success, not failure

The pipeline is built to stop rather than guess past a judgment call:

- **A stage refuses** (intake on harassment/bad-faith; drafting on a bad-faith instrument) — stop
  and surface the refusal; do not route around it.
- **The pathway choice is the human's** (more than one plausible pathway, or the choice turns on the
  merits) — stop and let you choose.
- **A fact is missing or currency cannot be confirmed** — carry the `[placeholder]` and the flag
  forward; do not invent the fact to keep moving.

## The product

A single DRAFT case package — routing, findings, flagged draft, controlling law, plain-language
summary — plus one **consolidated attorney checklist** gathering every flag, judgment call, currency
flag, and placeholder from all stages. That checklist is the list you work through before anything
is filed. Full detail and the per-stage carry-forward table: [the runbook](../../runbook.md).
