"""End-to-end guide docs honor OSED's invariants and don't rot.

The for-communities track must never tell a reader they have a case / should sue / will win
(the same line the plain-language and intake skills hold). The guide entry point surfaces the
disclaimer, and intra-guide relative links resolve. Reuses the plain-language forbidden tuple,
which deliberately omits "you have a case" (a negation-collision trap — the negated mandated form
"it does not mean you have a case" is allowed and expected).
"""

import re
from pathlib import Path

from osed_evals.markers import PLAIN_LANGUAGE_FORBIDDEN_ADVICE

REPO = Path(__file__).resolve().parents[2]
GUIDE = REPO / "docs" / "guide"

_LINK = re.compile(r"\]\(([^)]+)\)")


def _guide_md_files():
    return sorted(GUIDE.rglob("*.md"))


def test_guide_entry_point_exists():
    assert (GUIDE / "README.md").exists(), "docs/guide/README.md (entry point) is missing"


def test_entry_point_references_the_disclaimer():
    text = (GUIDE / "README.md").read_text()
    assert "DISCLAIMER" in text, "the guide entry point must point readers to the disclaimer"


def test_community_track_has_no_merits_drift():
    community_dir = GUIDE / "for-communities"
    offenders = {}
    for f in sorted(community_dir.rglob("*.md")) if community_dir.exists() else []:
        low = f.read_text().lower()
        hits = [p for p in PLAIN_LANGUAGE_FORBIDDEN_ADVICE if p in low]
        if hits:
            offenders[f.name] = hits
    assert not offenders, f"merits-drift phrases in community docs: {offenders}"


def test_intra_guide_relative_links_resolve():
    broken = []
    for f in _guide_md_files():
        for m in _LINK.finditer(f.read_text()):
            target = m.group(1).split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (f.parent / target).resolve().exists():
                broken.append(f"{f.relative_to(REPO)} -> {target}")
    assert not broken, f"broken relative links in docs/guide: {broken}"
