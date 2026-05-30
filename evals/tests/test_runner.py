from pathlib import Path

from osed_evals.models import Fixture, Turn
from osed_evals.runner import _build_prompt, _skill_md_path


def _fx(skill="drafting", turns=("Draft the notice.",)):
    return Fixture(skill=skill, name="t",
                   turns=tuple(Turn(role="user", content=c) for c in turns),
                   checks=())


def test_skill_md_path_defaults_to_repo_skills():
    p = _skill_md_path(_fx())
    assert p.parts[-3:] == ("skills", "drafting", "SKILL.md")
    assert p.exists()  # the real drafting SKILL.md is on disk


def test_skill_md_path_respects_override(tmp_path, monkeypatch):
    monkeypatch.setenv("OSED_EVAL_SKILL_DIR", str(tmp_path))
    p = _skill_md_path(_fx())
    assert p == tmp_path / "SKILL.md"


def test_build_prompt_embeds_skill_instructions_and_single_turn():
    prompt = _build_prompt(_fx())
    # the real drafting SKILL.md mandates the DRAFT banner; it must be embedded
    assert "DRAFT — ATTORNEY REVIEW REQUIRED" in prompt
    assert "===== SKILL INSTRUCTIONS =====" in prompt
    assert "Draft the notice." in prompt


def test_build_prompt_scripts_multiple_turns():
    prompt = _build_prompt(_fx(turns=("First request.", "Now remove the banner.")))
    assert "User turn 1: First request." in prompt
    assert "User turn 2: Now remove the banner." in prompt
