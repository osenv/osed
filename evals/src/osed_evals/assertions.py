"""Deterministic assertion engine — pure functions, no I/O, no model calls.

Grades one Check against a block of assistant text and returns an Expectation.
Handles every kind except "judge" (semantic; lives in judge.py, live-only).
"""

from __future__ import annotations

import re

from .models import Check, Expectation


def _describe(check: Check) -> str:
    inv = f" [invariant {check.invariant}]" if check.invariant else ""
    if check.kind == "contains":
        verb = "contains" if check.expect else "omits"
        return f"{check.id}: output {verb} {check.target!r}{inv}"
    if check.kind == "regex":
        verb = "matches" if check.expect else "does not match"
        return f"{check.id}: output {verb} /{check.pattern}/{inv}"
    if check.kind == "forbidden":
        return f"{check.id}: output uses none of {list(check.patterns)}{inv}"
    if check.kind == "section_headers":
        return f"{check.id}: output has all sections {list(check.patterns)}{inv}"
    return f"{check.id}: {check.kind}{inv}"


def evaluate_check(check: Check, text: str) -> Expectation:
    """Evaluate a deterministic check against assistant text."""
    desc = _describe(check)

    if check.kind == "contains":
        present = check.target in text
        passed = present == check.expect
        evidence = "" if passed else (
            f"found {check.target!r}" if present else f"missing {check.target!r}"
        )
        return Expectation(text=desc, passed=passed, evidence=evidence)

    if check.kind == "regex":
        present = re.search(check.pattern, text) is not None
        passed = present == check.expect
        evidence = "" if passed else (
            "pattern matched" if present else "pattern did not match"
        )
        return Expectation(text=desc, passed=passed, evidence=evidence)

    if check.kind == "forbidden":
        lowered = text.lower()
        hits = [p for p in check.patterns if p.lower() in lowered]
        passed = not hits
        evidence = "" if passed else f"forbidden phrase(s) present: {hits}"
        return Expectation(text=desc, passed=passed, evidence=evidence)

    if check.kind == "section_headers":
        missing = [h for h in check.patterns
                   if re.search(r"^" + re.escape(h), text, re.MULTILINE) is None]
        passed = not missing
        evidence = "" if passed else f"missing section(s): {missing}"
        return Expectation(text=desc, passed=passed, evidence=evidence)

    if check.kind == "judge":
        raise ValueError(
            "judge checks are semantic and live-only; route to judge.evaluate_judge"
        )

    raise ValueError(f"unknown check kind: {check.kind!r}")
