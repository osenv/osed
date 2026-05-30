"""Render GradeResults to skill-creator's grading.json shape and a text report."""

from __future__ import annotations

from .models import GradeResult


def to_grading_json(result: GradeResult) -> dict:
    return {
        "skill": result.skill,
        "fixture": result.fixture,
        "expectations": [
            {"text": e.text, "passed": e.passed, "evidence": e.evidence}
            for e in result.expectations
        ],
        "summary": result.summary(),
    }


def summarize(results: list[GradeResult]) -> dict:
    passed = sum(1 for r in results if r.passed)
    return {
        "fixtures_total": len(results),
        "fixtures_passed": passed,
        "fixtures_failed": len(results) - passed,
    }


def format_text_report(results: list[GradeResult]) -> str:
    lines: list[str] = []
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        lines.append(f"[{status}] {r.skill}/{r.fixture}")
        for e in r.expectations:
            if not e.passed:
                lines.append(f"    ✗ {e.text} — {e.evidence}")
    s = summarize(results)
    lines.append(f"\n{s['fixtures_passed']}/{s['fixtures_total']} fixtures passed")
    return "\n".join(lines)
