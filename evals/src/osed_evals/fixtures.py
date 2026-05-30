"""Load and validate JSON fixtures into Fixture objects."""

from __future__ import annotations

import json
from pathlib import Path

from .models import Check, Fixture, Turn

VALID_KINDS = {"contains", "regex", "forbidden", "section_headers", "judge"}


class FixtureError(ValueError):
    """A fixture file is missing a required field or is malformed."""


def _require(data: dict, key: str, where: Path) -> object:
    if key not in data:
        raise FixtureError(f"{where}: missing required field {key!r}")
    return data[key]


def _parse_check(raw: dict, where: Path) -> Check:
    kind = raw.get("kind")
    if kind not in VALID_KINDS:
        raise FixtureError(f"{where}: check {raw.get('id')!r} has invalid kind {kind!r}")
    return Check(
        id=str(_require(raw, "id", where)),
        kind=kind,
        invariant=raw.get("invariant"),
        target=raw.get("target"),
        pattern=raw.get("pattern"),
        patterns=tuple(raw.get("patterns", ())),
        expect=raw.get("expect", True),
        criterion=raw.get("criterion"),
        scope=raw.get("scope", "final"),
    )


def load_fixture(path: Path) -> Fixture:
    path = Path(path)
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise FixtureError(f"{path}: invalid JSON: {exc}") from exc

    turns_raw = _require(data, "turns", path)
    checks_raw = _require(data, "checks", path)

    transcript = data.get("transcript")
    if transcript is None and "transcript_file" in data:
        transcript = (path.parent / data["transcript_file"]).read_text()

    return Fixture(
        skill=str(_require(data, "skill", path)),
        name=str(_require(data, "name", path)),
        turns=tuple(Turn(role=t.get("role", "user"), content=t["content"])
                    for t in turns_raw),
        checks=tuple(_parse_check(c, path) for c in checks_raw),
        transcript=transcript,
    )


def load_fixtures(directory: Path, skill: str | None = None) -> list[Fixture]:
    directory = Path(directory)
    fixtures = [load_fixture(p) for p in sorted(directory.rglob("*.json"))]
    if skill is not None:
        fixtures = [f for f in fixtures if f.skill == skill]
    return fixtures
