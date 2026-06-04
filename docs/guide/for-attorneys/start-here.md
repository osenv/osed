# For attorneys — start here

OSED is a drafting aid scoped to the mechanical layer of environmental litigation. It produces
flagged first drafts of well-understood instruments — citizen-suit notices, rulemaking petitions,
deadline complaints, consent-decree scaffolds, state-constitution packets — so your time starts
from a structured draft with the judgment calls already surfaced, not a blank page.

**It drafts; you decide.** Every output is a marked **DRAFT**; every judgment call is flagged
`[⚠ ATTORNEY: ...]` rather than resolved; every cited authority is currency-checked or flagged.
OSED never concludes that a client has a case, that a party is liable, or that filing is wise — it
attaches the controlling law to the question and stops.

## How it fits a practice

Run a concern through the pipeline (intake → gap analysis → drafting ↔ precedent → plain-language)
and you get a DRAFT case package with one consolidated attorney checklist — the flags, placeholders,
and currency questions gathered in one place for you to work through. You complete the judgment, the
facts, and the currency confirmation; you sign and file. See
[running the pipeline](running-the-pipeline.md).

## Install

OSED is a Claude Code plugin distributed from its own repo as a self-hosted marketplace. See the
**"Install as a Claude Code plugin"** section of the [README](../../../README.md) for the
`/plugin marketplace add` + `/plugin install` steps, the optional API keys, and the connector's
safe degradation when keys or `python3` are absent.

## The contract

The [six invariants](../concepts/the-six-invariants.md) are the contract OSED holds itself to, and
the thing you should expect every output to honor. If you find an instrument deciding a gating
doctrine — standing, ripeness, whether to sue — that is a bug; report it.

From here:

- [Instrument catalog](instrument-catalog.md) — the six instruments, when each applies, and links.
- [Running the pipeline](running-the-pipeline.md) — the end-to-end flow.
- [Currency and the connector](currency-and-the-connector.md) — keeping authorities off dead law.
- [Extending OSED](extending-osed.md) — contributing skills/templates without regressing the invariants.
