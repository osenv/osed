"""Command-line entry point: grade a fixtures directory.

    python -m osed_evals run --fixtures fixtures [--skill drafting] [--live]

Exit code 0 if all graded fixtures pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .fixtures import load_fixtures
from .grade import grade_fixture
from .report import format_text_report, summarize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="osed_evals")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="grade a fixtures directory")
    run.add_argument("--fixtures", required=True, type=Path)
    run.add_argument("--skill", default=None)
    run.add_argument("--live", action="store_true",
                     help="run skills + LLM judge via claude -p (needs Claude Code auth)")
    args = parser.parse_args(argv)

    fixtures = load_fixtures(args.fixtures, skill=args.skill)
    results = []
    for fx in fixtures:
        if args.live:
            from .runner import run_skill_live
            from .judge import evaluate_judge
            transcript = run_skill_live(fx)
            results.append(grade_fixture(fx, live=True, transcript=transcript,
                                         judge_fn=evaluate_judge))
        else:
            if fx.transcript is None:
                continue  # live-only fixture; skip in deterministic lane
            results.append(grade_fixture(fx, live=False))

    print(format_text_report(results))
    return 0 if summarize(results)["fixtures_failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
