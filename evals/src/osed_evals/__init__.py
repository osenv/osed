"""OSED eval & red-team harness.

Converts the six design invariants from prose into verified checks. The
deterministic core (models, markers, assertions, grade, report) runs in CI
with no secrets. The live path (runner, judge) is gated behind the `live`
pytest marker / the `--live` CLI flag.
"""

__version__ = "0.1.0"
