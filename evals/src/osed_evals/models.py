"""Core data models for the eval harness.

A Fixture pairs a skill input (one or more user Turns) with a list of Checks
and, for the deterministic CI lane, a recorded `transcript` of the skill's
output. Grading produces Expectations (skill-creator's grading.json shape).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Turn:
    """One scripted message in a (possibly multi-turn) skill interaction."""
    role: str  # currently always "user"
    content: str


@dataclass(frozen=True)
class Check:
    """A single gradeable expectation about a skill's output.

    kind:
      - "contains":        `target` substring present (expect=True) or absent (expect=False)
      - "regex":           `pattern` matches (expect=True) or does not (expect=False)
      - "forbidden":       none of `patterns` appear (case-insensitive); fails if any do
      - "section_headers": every header in `patterns` is present
      - "judge":           LLM judge decides `criterion` (live only)
    scope: which assistant text to grade — "final" (last turn), "any", or "all".
    """
    id: str
    kind: str
    invariant: int | None = None
    target: str | None = None
    pattern: str | None = None
    patterns: tuple[str, ...] = ()
    expect: bool = True
    criterion: str | None = None
    scope: str = "final"

    @property
    def is_deterministic(self) -> bool:
        return self.kind != "judge"


@dataclass(frozen=True)
class Fixture:
    skill: str
    name: str
    turns: tuple[Turn, ...]
    checks: tuple[Check, ...]
    transcript: str | None = None  # recorded output for the deterministic lane


@dataclass
class Expectation:
    """Result of one check — matches skill-creator's grading.json item shape."""
    text: str
    passed: bool
    evidence: str


@dataclass
class GradeResult:
    skill: str
    fixture: str
    expectations: list[Expectation] = field(default_factory=list)

    def summary(self) -> dict:
        total = len(self.expectations)
        passed = sum(1 for e in self.expectations if e.passed)
        return {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": (passed / total) if total else 0.0,
        }

    @property
    def passed(self) -> bool:
        return all(e.passed for e in self.expectations)
