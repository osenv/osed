# Worked examples

End-to-end walkthroughs of the OSED pipeline on **public matters with no client facts**. They
show how the four agents hand off to one another — Gap Analysis → Drafting ↔ Precedent Retrieval
→ Plain-Language → a human attorney (the terminal node, always).

**What these are, honestly:** curated *reference exemplars* of correct behavior — not verbatim
transcripts of a specific machine run, and not legal advice (see [`../../DISCLAIMER.md`](../../DISCLAIMER.md)).
Specific facts are shown as `[placeholder]` with an attorney flag; cited cases were confirmed to
*resolve* via the connector's `verify_citation`, which is not the same as a promise they remain
good law. Everything here is subject to the doctrinal-currency rule
([`../doctrinal-currency.md`](../doctrinal-currency.md)).

Each stage of every example is also a registered eval fixture under `evals/fixtures/`, so a skill
change that degrades the worked output is caught by the gated live lane.

- [`cwa-304m-deadline-suit.md`](cwa-304m-deadline-suit.md) — a missed mandatory deadline (CWA
  § 304(m)) taken through the deadline-suit pathway.
- [`rulemaking-petition.md`](rulemaking-petition.md) — asking an agency to act, via a rulemaking
  petition.
