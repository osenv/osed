# Extending OSED

OSED is built to be extended — a new instrument template, a new skill, a new state ERA packet —
without weakening the guardrails that make its output safe to hand a lawyer. The contributing guide
([`../../../CONTRIBUTING.md`](../../../CONTRIBUTING.md)) is the full reference; this page is the
orientation.

## What you can add

- **A template** (`templates/`) — the structural model is `cwa-505-notice-of-intent.md`: a DRAFT
  banner, a required-elements checklist, inline `[⚠ ATTORNEY: ...]` flags, a deadline note, and a
  consolidated attorney-flags section. Follow it; an omitted required element is how these
  instruments fail in court.
- **A skill** (`skills/`) — YAML frontmatter (`name`, `description`) plus an imperative-voice body.
  The `description` is the trigger: make it specific and explicit about what the skill will *not* do.
  Every skill includes a worked example with both good and bad behavior, where the bad example shows
  the exact boundary being crossed.

## The invariants you must not regress

Any change to a skill or template must keep the [six invariants](../concepts/the-six-invariants.md)
intact — DRAFT banners, inline flags, the currency check, no invented facts, no merits calls, and
refusal of bad-faith uses. A change that weakens one is wrong even if it makes the output look more
polished.

## The eval harness enforces it

`evals/` turns those prose guardrails into checks that can actually fail. The rule: a change to
`skills/` or `templates/` must keep `cd evals && pytest` green, and CI enforces it. Two lanes:

- **Deterministic core** (CI-safe, no secrets) — exact-string / regex / forbidden-phrase /
  section-header checks against recorded transcripts (the DRAFT banner, `[⚠ ATTORNEY: ...]`,
  `[placeholder]`, required sections).
- **`--live`** (gated; needs Claude Code auth) — runs a skill via `claude -p` and adds an LLM judge
  for negation-sensitive checks (refusal under pressure; was *every* judgment call flagged).

See [`../../../evals/README.md`](../../../evals/README.md) for the harness, fixtures, and how to add
golden transcripts.

## Plugin-safe resource convention

When a skill references a bundled resource, use the `${CLAUDE_SKILL_DIR}` convention in skill prose
so the path resolves whether OSED is run from a clone or installed as a plugin. (This is the plugin
resource root for skills — not `${CLAUDE_PLUGIN_ROOT}`.)
