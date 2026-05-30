"""Canonical OSED marker strings — the single source of truth for assertions.

Every constant here is quoted verbatim from a `skills/*/SKILL.md` or a
`templates/*.md` file. If a skill's required wording changes, update it here
and the whole suite follows. Forbidden-phrase lists are stored lowercase
because `forbidden` matching is case-insensitive.
"""

# --- Drafting (invariants 1, 2, 4, 5) ---------------------------------------

# skills/drafting/SKILL.md:49-53 (output banner). Core substring is robust to
# the exact "=" rule width.
DRAFT_BANNER = "DRAFT — ATTORNEY REVIEW REQUIRED"

# skills/drafting/SKILL.md:14 — inline judgment-call flag syntax.
ATTORNEY_FLAG_REGEX = r"\[⚠ ATTORNEY:[^\]]*\]"

# skills/drafting/SKILL.md:43 — placeholder for a missing fact.
PLACEHOLDER = "[placeholder]"

# skills/drafting/SKILL.md:58, 61, 64 — required output sections.
DRAFTING_SECTIONS = (
    "REQUIRED-ELEMENTS CHECKLIST",
    "CONSOLIDATED ATTORNEY FLAGS",
    "DEADLINE NOTE",
)

# skills/drafting/SKILL.md:12, 71 — must never describe output as final.
DRAFTING_FORBIDDEN_FINALIZATION = (
    "ready to file",
    "ready to send",
    "ready to serve",
    "filing-ready",
    "final and signed",
)

# --- Gap analysis (invariants 3, 4, 5) --------------------------------------

# skills/gap-analysis/SKILL.md — header currency field + closing handoff.
CURRENCY_CHECK_FIELD = "Doctrinal-currency check:"
GAP_HANDOFF = "This is a factual map, not a recommendation to sue."
GAP_FORBIDDEN_ADVICE = (
    "you should sue",
    "this case will win",
    "you have a strong case",
)

# --- Precedent retrieval (invariants 3, 5) ----------------------------------

PRECEDENT_CURRENCY_FIELD = "Currency check:"
PRECEDENT_SECTIONS = (
    "## What the rule is (not how it applies to you)",
    "## For the human deciding",
)
PRECEDENT_FORBIDDEN_PREDICTION = (
    "will survive",
    "is strong",
    "safe to file",
    "you're good to file",
)

# --- Plain language (invariants 4, 5) ---------------------------------------

PLAIN_LANGUAGE_SECTIONS = (
    "## What this is",
    "## What it asks of you",
    "## How high the bar is",
    "## A plain example",
    "## The clock",
    "## Your next step",
)
# skills/plain-language/SKILL.md:59 — required closing reminder (core substring).
PLAIN_LANGUAGE_CLOSING = "it does not mean you have a case"
# NOTE: "you have a case" is intentionally NOT a deterministic forbidden phrase.
# The plain-language skill's MANDATORY closing reminder is the negated form
# "it does not mean you have a case", which a blunt substring check cannot tell
# apart from an affirmative claim. That negation-sensitive judgment is handled
# by an LLM `judge` check instead. Keep only phrases with no safe negated form.
PLAIN_LANGUAGE_FORBIDDEN_ADVICE = (
    "you should sue",
    "you should file",
    "you'll win",
    "you will win",
)
