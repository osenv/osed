"""WI-6 doctrinal-freshness structure check.

The repo's doctrinal anchors (docs/doctrinal-currency.md, the "Worth tracking"
section) must carry a law-as-of stamp: a `Law-as-of: <date>` header and, on every
anchor bullet, a `(verified YYYY-MM-DD; re-verify by YYYY-MM-DD)` stamp.

This is date-AGNOSTIC: it proves the stamp exists and is well-formed, NOT that the
law was actually re-verified or that a date is past due (out of scope — see the
doc's re-verification cadence section).
"""

import re
from pathlib import Path

DOC = Path(__file__).resolve().parents[2] / "docs" / "doctrinal-currency.md"

_STAMP = re.compile(r"\(verified \d{4}-\d{2}-\d{2}; re-verify by \d{4}-\d{2}-\d{2}\)")


def _worth_tracking_section() -> str:
    text = DOC.read_text()
    m = re.search(r"^## Worth tracking.*?(?=^## |\Z)", text, re.M | re.S)
    assert m, "missing '## Worth tracking' section in doctrinal-currency.md"
    return m.group(0)


def test_worth_tracking_has_law_as_of_header():
    section = _worth_tracking_section()
    assert re.search(r"Law-as-of:\s*\d{4}-\d{2}-\d{2}", section), "missing 'Law-as-of: <date>' header"


def test_every_anchor_bullet_is_stamped():
    section = _worth_tracking_section()
    bullets = [ln for ln in section.splitlines() if ln.lstrip().startswith("- ")]
    assert bullets, "no anchor bullets found in '## Worth tracking'"
    unstamped = [b for b in bullets if not _STAMP.search(b)]
    assert not unstamped, f"anchor bullets missing a (verified …; re-verify by …) stamp: {unstamped}"
