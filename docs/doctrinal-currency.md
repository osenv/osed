# Doctrinal Currency — Keeping Agents Off Dead Law

Every OSED skill runs a "doctrinal-currency check" before it relies on a statute, regulation, or doctrine. This document explains what that check is, why it is load-bearing, and how to perform it.

## The lesson, stated once

Law changes underneath you, and an agent that drafts confidently on law that has changed produces the most expensive kind of error: a polished, authoritative-looking instrument that is wrong. *Chevron v. NRDC* (1984) was the most-cited administrative-law decision in the country for forty years. The Supreme Court overturned it in *Loper Bright Enterprises v. Raimondo* (2024). A strategy memo, a brief template, or an agent instruction written before 2024 that assumes courts will defer to an agency's reasonable statutory interpretation now gives **backwards advice**. Similarly, *Seven County Infrastructure Coalition v. Eagle County* (2025) narrowed the scope of NEPA environmental-review challenges. These are not edge cases; they are recent, central shifts.

The takeaway is not "memorize these two cases." It is structural: **an agent must never assume the doctrine it learned is the doctrine in force.** Verify currency, every time, before relying.

## What can make an authority stale

- **Overruled / abrogated** — a higher court reversed the precedent (Chevron → Loper Bright).
- **Vacated** — a court struck down the rule the instrument relies on.
- **Superseded by statute** — Congress or a legislature changed the underlying law.
- **Narrowed** — the rule still stands but covers less than it did (Seven County and NEPA scope).
- **Stayed** — the rule is paused pending litigation, so it may not currently be in force.
- **Amended** — the regulation's text or deadline changed.

Any of these can turn a correct draft into a wrong one without changing a word of the draft.

## The check, in four steps

1. **List every authority the output relies on** — each statute section, regulation, and case that the instrument's validity depends on.

2. **Verify each is still in force** as of the date of the work. Use current primary sources: the U.S. Code and CFR (or state equivalents) for statutes and rules; the Federal Register for recent rule changes, stays, and vacaturs; and current case law (including subsequent history) for doctrines. For a fast-moving area, recent news of a Supreme Court or circuit decision can be the first signal that something moved — confirm it in primary sources.

3. **Classify each authority:**
   - **CURRENT** — confirmed in force and not narrowed in a way that matters here.
   - **CHANGED** — still exists but narrowed, amended, or stayed; explain how and assess whether it still supports the instrument.
   - **DEAD** — overruled, vacated, or superseded; do not rely on it.
   - **UNVERIFIED** — currency could not be confirmed from available sources.

4. **Act on the classification.** Rely only on CURRENT authority. For CHANGED, adjust the instrument and flag it. For DEAD, remove it and find a live basis or flag that none was found. For UNVERIFIED, **flag it rather than presenting it as good law** — never launder uncertainty into apparent confidence.

## How this shows up in each skill

- **Gap Analysis** confirms a duty is still live before reporting it as a gap; a repealed duty is not a gap.
- **Drafting** currency-checks every cited authority before resting the instrument on it; failures become attorney flags.
- **Precedent Retrieval** labels every case with its current status and refuses to present a doctrine it could not currency-check as settled.
- **Plain-Language** does not assert a pathway exists without confirming the underlying law still does.

## A standing reminder for the agents

When in doubt, the honest move is to flag, not to assume. "I could not confirm this authority is current — a licensed attorney must verify before relying on it" is always a safe and correct output. "This is the law" about something you did not check is the one move that is never safe.

## Worth tracking (non-exhaustive, will go stale — verify)

**Law-as-of: 2026-06-01.** Each anchor below carries the date it was last verified and the date it
must be re-verified by. Re-verifying means: confirm in primary sources, update both dates, and add
an entry to `CHANGELOG.md`. A stamp records that a human checked — it is never a substitute for
checking.

This list itself is subject to the currency rule. It is a prompt to check, not a substitute for checking.

- *Loper Bright* (2024) ended Chevron deference — courts now interpret statutes themselves. Cuts for and against challengers alike. (verified 2026-05-31; re-verify by 2026-08-31)
- *Seven County* (2025) narrowed NEPA review scope. (verified 2026-05-31; re-verify by 2026-08-31)
- Major Questions Doctrine continues to constrain agency action on "major" economic/political questions. (verified 2026-05-31; re-verify by 2026-08-31)
- Standing doctrine for environmental plaintiffs remains active and contested. (verified 2026-05-31; re-verify by 2026-08-31)
- **Pennsylvania Art. I § 27** (Environmental Rights Amendment) — a developed public-trust line (PEDF v. Commonwealth, 161 A.3d 911 (Pa. 2017); Robinson Twp. v. Commonwealth, 83 A.3d 901 (Pa. 2013)) gives the provision real force; confirm the current standard before relying. (verified 2026-06-01; re-verify by 2026-09-01)
- **Montana Art. II § 3 & art. IX § 1** — a robust state ERA: a self-executing fundamental right (MEIC v. DEQ, 988 P.2d 1236 (Mont. 1999)) recently applied in major litigation (Held v. State, 560 P.3d 1235 (Mont. 2024)); confirm the current standard. (verified 2026-06-01; re-verify by 2026-09-01)
- **New York Art. I § 19** (Green Amendment, ratified 2021) — DEVELOPING law; the enforceable standard is still being defined by the courts and no controlling appellate test is settled; do not assume a settled standard. (verified 2026-06-01; re-verify by 2026-09-01)
- **Hawaiʻi Art. XI** (environmental rights "as provided by law"; public-trust doctrine, In re Water Use Permit Applications (Waiāhole), 9 P.3d 409 (Haw. 2000)) — the § 9 individual right is DEVELOPING and statute-dependent; the public-trust line is more established; confirm. (verified 2026-06-01; re-verify by 2026-09-01)

Re-verify all of the above before relying on any of it.

## Re-verification cadence

The "Worth tracking" anchors above carry stamps so they do not quietly rot. Keep them honest:

- **Who.** Maintainers, and any contributor whose change relies on or touches an anchor.
- **How often.** Re-verify each anchor by its `re-verify by` date; the default cadence is
  **quarterly**. **Always** re-verify before relying on an anchor in a real matter. Sweep the
  deference / standing / major-questions anchors **after the U.S. Supreme Court term ends** (late
  June / early July), when the most consequential shifts land.
- **The rule.** Re-verifying means confirming in primary sources, then updating *both* stamp dates
  on the anchor and adding an entry to `CHANGELOG.md`. The stamp records that a human checked; it is
  never a substitute for checking, and a present stamp does not mean an anchor is current — only that
  someone confirmed it on the verified date.

`evals/tests/test_freshness.py` enforces that each anchor stays stamped (it checks the stamp is
present and well-formed, not whether a date is past due).
