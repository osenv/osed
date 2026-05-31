"""The MCP server exposes exactly the two phase-1 tools and delegates to the
clients. Network behavior is covered by the client + live tests; here we only
verify wiring (registration + passthrough), so no HTTP happens."""

import asyncio

from osed_connectors import server


def test_registers_all_tools():
    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    # phase 1
    assert "find_agency_actions" in names
    assert "get_current_regulation" in names
    # phase 2
    assert "get_uscode_section" in names
    assert "find_rulemaking_documents" in names
    assert "find_rule_changes" in names


def test_find_agency_actions_delegates_to_federal_register(monkeypatch):
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return {"sentinel": "fr"}

    monkeypatch.setattr(server.fr, "search_actions", fake)
    out = server.find_agency_actions(term="ozone", agency="environmental-protection-agency", limit=2)
    assert out == {"sentinel": "fr"}
    assert captured["term"] == "ozone"
    assert captured["agency"] == "environmental-protection-agency"
    assert captured["limit"] == 2


def test_get_current_regulation_delegates_to_ecfr(monkeypatch):
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return {"sentinel": "ecfr"}

    monkeypatch.setattr(server.ecfr, "get_current_text", fake)
    out = server.get_current_regulation(title=40, part="50", section="50.1")
    assert out == {"sentinel": "ecfr"}
    assert captured == {"title": 40, "part": "50", "section": "50.1"}


def test_get_uscode_section_delegates_to_govinfo(monkeypatch):
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return {"sentinel": "govinfo"}

    monkeypatch.setattr(server.govinfo, "get_uscode_section", fake)
    out = server.get_uscode_section(title=42, section="7409")
    assert out == {"sentinel": "govinfo"}
    assert captured == {"title": 42, "section": "7409"}


def test_find_rulemaking_documents_delegates_to_regulations_gov(monkeypatch):
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return {"sentinel": "rg"}

    monkeypatch.setattr(server.rg, "find_rulemaking_documents", fake)
    out = server.find_rulemaking_documents(agency="EPA", term="ozone", limit=5)
    assert out == {"sentinel": "rg"}
    assert captured["agency"] == "EPA"
    assert captured["term"] == "ozone"
    assert captured["limit"] == 5


def test_find_rule_changes_delegates_to_federal_register(monkeypatch):
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return {"sentinel": "fr_changes"}

    monkeypatch.setattr(server.fr, "search_rule_changes", fake)
    out = server.find_rule_changes(cfr_title=40, cfr_part="423", since="2025-01-01", limit=20)
    assert out == {"sentinel": "fr_changes"}
    assert captured == {"cfr_title": 40, "cfr_part": "423", "since": "2025-01-01", "limit": 20}
