import json
import pytest
from osed_evals.fixtures import load_fixture, load_fixtures, FixtureError


def _write(tmp_path, name, data):
    p = tmp_path / name
    p.write_text(json.dumps(data))
    return p


def test_load_fixture_parses_turns_and_checks(tmp_path):
    p = _write(tmp_path, "f.json", {
        "skill": "drafting",
        "name": "demo",
        "turns": [{"role": "user", "content": "Draft it."}],
        "checks": [{"id": "banner", "kind": "contains",
                    "target": "DRAFT", "invariant": 1}],
        "transcript": "DRAFT here",
    })
    fx = load_fixture(p)
    assert fx.skill == "drafting"
    assert fx.turns[0].content == "Draft it."
    assert fx.checks[0].kind == "contains"
    assert fx.transcript == "DRAFT here"


def test_transcript_file_is_loaded_relative_to_fixture(tmp_path):
    (tmp_path / "demo.out.md").write_text("RECORDED OUTPUT")
    p = _write(tmp_path, "demo.json", {
        "skill": "drafting", "name": "demo",
        "turns": [{"role": "user", "content": "x"}],
        "checks": [{"id": "c", "kind": "contains", "target": "RECORDED"}],
        "transcript_file": "demo.out.md",
    })
    fx = load_fixture(p)
    assert fx.transcript == "RECORDED OUTPUT"


def test_missing_required_field_raises(tmp_path):
    p = _write(tmp_path, "bad.json", {"skill": "drafting", "name": "x"})
    with pytest.raises(FixtureError, match="turns"):
        load_fixture(p)


def test_unknown_check_kind_raises(tmp_path):
    p = _write(tmp_path, "bad.json", {
        "skill": "drafting", "name": "x",
        "turns": [{"role": "user", "content": "x"}],
        "checks": [{"id": "c", "kind": "telepathy"}],
    })
    with pytest.raises(FixtureError, match="kind"):
        load_fixture(p)


def test_load_fixtures_dir_filters_by_skill(tmp_path):
    (tmp_path / "drafting").mkdir()
    (tmp_path / "gap-analysis").mkdir()
    _write(tmp_path / "drafting", "a.json", {
        "skill": "drafting", "name": "a",
        "turns": [{"role": "user", "content": "x"}],
        "checks": [{"id": "c", "kind": "contains", "target": "x"}],
        "transcript": "x"})
    _write(tmp_path / "gap-analysis", "b.json", {
        "skill": "gap-analysis", "name": "b",
        "turns": [{"role": "user", "content": "x"}],
        "checks": [{"id": "c", "kind": "contains", "target": "x"}],
        "transcript": "x"})
    only = load_fixtures(tmp_path, skill="drafting")
    assert [f.name for f in only] == ["a"]
    assert len(load_fixtures(tmp_path)) == 2
