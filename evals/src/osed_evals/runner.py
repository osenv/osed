"""Run an OSED skill live via `claude -p`, returning the assistant transcript.

The `claude -p` call and its output parsing live in `claude_cli.run_claude_p`.
The skill's SKILL.md is read from disk and embedded in the prompt so behavior is
driven deterministically by the instructions under test (not by runtime skill
auto-discovery). Set OSED_EVAL_SKILL_DIR to point at an alternate skill
directory (used by the live negative control).

Imported only on the `--live` path / `live` pytest marker.
"""

from __future__ import annotations

import os
from pathlib import Path

from .claude_cli import run_claude_p
from .models import Fixture

# evals/src/osed_evals/runner.py -> parents[3] is the repo root.
_REPO_ROOT = Path(__file__).resolve().parents[3]


def _skill_md_path(fixture: Fixture) -> Path:
    override = os.environ.get("OSED_EVAL_SKILL_DIR")
    if override:
        return Path(override) / "SKILL.md"
    return _REPO_ROOT / "skills" / fixture.skill / "SKILL.md"


def _build_prompt(fixture: Fixture) -> str:
    skill_md = _skill_md_path(fixture).read_text()
    user_turns = [t.content for t in fixture.turns if t.role == "user"]
    if len(user_turns) == 1:
        exchange = user_turns[0]
    else:
        exchange = (
            "Respond to this multi-turn exchange, holding the line on every "
            "design invariant at each turn:\n"
            + "\n".join(f"User turn {i + 1}: {c}" for i, c in enumerate(user_turns))
        )
    return (
        "You are acting as the following OSED skill. Follow its instructions "
        "exactly and produce its full formatted output.\n\n"
        "===== SKILL INSTRUCTIONS =====\n"
        f"{skill_md}\n"
        "===== END SKILL INSTRUCTIONS =====\n\n"
        f"{exchange}"
    )


def run_skill_live(fixture: Fixture, timeout: int = 300) -> str:
    """Drive the fixture's turns live and return the assistant output.

    A full skill run (the model produces a complete formatted instrument) can
    take a couple of minutes; the timeout is generous to avoid spurious flakes.
    """
    return run_claude_p(_build_prompt(fixture), timeout, label="claude -p (skill run)")
