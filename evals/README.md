# osed-evals

Verifies that each OSED skill's output obeys the six design invariants
(see `../CLAUDE.md` and `../docs/architecture.md`).

## Two lanes

- **Deterministic core (CI-safe, no secrets):** grades *recorded* skill
  transcripts against exact markers — the DRAFT banner, `[⚠ ATTORNEY: ...]`
  flags, `[placeholder]`, required section headers, forbidden phrases.
  This is what guarantees "the suite can fail" (the negative control).
- **`--live` (local / secrets-enabled lane):** runs a skill multi-turn via
  `claude -p` and adds an LLM judge for semantic checks (refusal under
  pressure; was *every* judgment call flagged). Mirrors the connector's
  live-smoke vs keyed-test split.

## Run

```bash
cd evals
pip install -e '.[dev]'

# CI-safe deterministic suite:
pytest

# Everything, including live skill runs + LLM judge (needs Claude Code auth):
pytest -m 'live or not live'

# Ad-hoc run over a fixtures dir:
python -m osed_evals run --fixtures fixtures --skill drafting
python -m osed_evals run --fixtures fixtures --live
```

## CI

`.github/workflows/evals.yml` runs `pytest -q` (deterministic lane only) on any
change to `skills/`, `templates/`, or `evals/`. No secrets required: live
skill runs and the LLM judge are behind the `live` marker and are deselected.
Run them locally with `pytest -m live` (needs Claude Code auth).
