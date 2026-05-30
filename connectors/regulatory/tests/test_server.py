"""The MCP server exposes exactly the two phase-1 tools and delegates to the
clients. Network behavior is covered by the client + live tests; here we only
verify wiring (registration + passthrough), so no HTTP happens."""

import asyncio

from osed_connectors import server


def test_registers_the_two_phase1_tools():
    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    assert "find_agency_actions" in names
    assert "get_current_regulation" in names


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
