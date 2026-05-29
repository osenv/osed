# Contributing to OSED

Thank you for helping build this. OSED works only if the people who know the law — litigators, clinicians, advocates — shape the instruments, and the people who know the communities keep the plain-language layer honest. Contributions from both are the point.

## Before you contribute: the non-negotiables

Every contribution must preserve the design invariants from `docs/architecture.md`. A pull request that weakens any of these will be asked to revise:

1. Every drafted instrument is a marked **DRAFT** requiring attorney review.
2. Every judgment call is **flagged inline**, never silently resolved by the agent.
3. Every cited authority passes a **doctrinal-currency check** or is flagged. See `docs/doctrinal-currency.md`.
4. **No agent invents facts.** Missing facts become placeholders plus flags.
5. **No agent tells a user they have a case, should sue, or will win.**
6. The skills **refuse** harassment and bad-faith filing uses.

These exist because the cost of getting the mechanical layer wrong is high — a defective notice can sink a real case, and confident drafting on dead law misleads the people who can least afford it.

## What's especially welcome

- **New instrument templates**, following the roadmap in `docs/architecture.md` (Clean Air Act §304 notice, deadline complaint, consent-decree scaffold, state environmental-rights-act packets). Use the existing templates in `/templates` as the structural model: required-elements checklist, DRAFT banner, inline attorney flags, deadline note, consolidated flags.
- **Jurisdiction-specific knowledge** for the Precedent Retrieval skill — circuit splits, state high-court treatment, state environmental-rights-act variations.
- **Plain-language review** from people who work directly with the communities these tools are meant to serve. If a non-lawyer can't act on it, it isn't done.
- **Currency corrections** — if a doctrine referenced anywhere has shifted, that's a high-priority fix.

## How to contribute a skill or template

1. Open an issue describing the instrument or change and the legal basis for it.
2. Follow the skill format: YAML frontmatter (`name`, `description`) plus an imperative-voice body. The `description` is the trigger; make it specific and slightly "pushy" about when to use the skill, and state plainly what the skill will *not* do.
3. Include a worked example showing good behavior and bad behavior (the bad example should illustrate the boundary being crossed).
4. For templates, include the required-elements checklist and the attorney flags. Cite the governing authority and mark it for currency verification.
5. If you are not a lawyer, say so in the PR, and flag any element you're unsure carries legal weight. That's helpful, not a problem — it tells reviewers where to look.

## Review

Substantive legal content should get review from a contributor with relevant legal expertise before merge. Plain-language content should get review from someone close to the intended audience. Maintainers will route PRs accordingly. When in doubt, a contribution that flags its own uncertainty is more useful than one that hides it.

## What we won't merge

- Anything that makes an agent decide whether to sue, predict outcomes, or tell a user they have a case.
- Anything that removes or weakens the DRAFT / attorney-review safeguards.
- Anything designed to enable harassment, bad-faith filing, or use of the tools against the public-interest purpose in `DISCLAIMER.md`.

## Code of conduct

Participation is governed by `CODE_OF_CONDUCT.md`. Be the kind of collaborator you'd want on a case.
