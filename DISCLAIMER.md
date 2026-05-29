# Disclaimer — Read This First

**OSED is a drafting aid, not a lawyer. Nothing it produces is legal advice.**

This project generates *scaffolding* for legal instruments. Scaffolding is not a filing. The distance between a well-formed draft and a document that is safe to send or file is exactly the distance this software cannot cross: it is the distance of professional legal judgment, applied to specific facts, in a specific jurisdiction, at a specific moment in the law's development.

## What this means in practice

1. **No attorney-client relationship is created** by using these skills, reading this repository, or receiving any output from it.

2. **Every output requires review by a licensed attorney** in the relevant jurisdiction before it is sent, served, or filed. The skills are written to say this themselves, in their own output. That is not boilerplate; it is the safeguard the whole system is built around.

3. **The agents do mechanical work; humans make judgment calls.** The agents are deliberately scoped to drafting and information-gathering. They are instructed to *refuse* to decide whether to sue, whether a plaintiff has standing, whether a claim is ripe, or whether filing is wise. When those questions arise, the agents surface them — with the relevant law attached — and stop. If you find an agent making one of those calls, that is a bug. Report it.

4. **The law changes, and outputs go stale.** A draft that was correct the day it was generated can be wrong a year later because a doctrine shifted. See `docs/doctrinal-currency.md`. Do not reuse old outputs without re-checking the law they rest on.

5. **Deadlines are real and unforgiving.** Many of these instruments carry statutory clocks (the 60-day citizen-suit notice period, statutes of limitations, comment windows). Missing one can extinguish a claim permanently. The software does not track your deadlines. You do, with your attorney.

6. **A defective instrument can be worse than none.** A citizen-suit notice that omits a required element can get an entire case dismissed regardless of its merits. A petition filed in bad faith can draw sanctions. The stakes of getting the mechanical part wrong are high, which is why the human review step is not optional.

## Who this is for

OSED is built for public-interest use: helping communities, advocates, and small public-interest organizations use the laws that already exist to protect health and the environment, where the barrier has been access to drafting capacity rather than the merits of the claim.

It is **not** built for, and the skills are written to refuse, use as an instrument of harassment, as a way to flood agencies or opponents with bad-faith filings, or as a substitute for the legal judgment a licensed attorney provides.

## Limitation

The contributors and maintainers of OSED provide this project "as is," without warranty of any kind, and are not liable for any outcome arising from its use. See `LICENSE`.

---

*If you take one thing from this file: build the machine that drafts; keep the human who decides.*
