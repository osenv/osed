"""Deterministic tests for the `claude -p` output parser (no live call).

The array shape here is the real one observed from `claude -p --output-format
json` (system -> assistant -> rate_limit_event -> result); a single-object
shape is the older CLI contract. Both must be handled.
"""

import json

import pytest

from osed_evals.claude_cli import _extract_result


def test_extract_result_from_event_array():
    stdout = json.dumps([
        {"type": "system", "subtype": "init"},
        {"type": "assistant", "message": {}},
        {"type": "rate_limit_event"},
        {"type": "result", "subtype": "success", "result": "THE OUTPUT"},
    ])
    assert _extract_result(stdout) == "THE OUTPUT"


def test_extract_result_from_single_object():
    stdout = json.dumps({"type": "result", "result": "THE OUTPUT"})
    assert _extract_result(stdout) == "THE OUTPUT"


def test_extract_result_array_without_result_event_raises():
    stdout = json.dumps([{"type": "system"}, {"type": "assistant"}])
    with pytest.raises(RuntimeError, match="no 'result' event"):
        _extract_result(stdout)


def test_extract_result_non_json_raises_with_context():
    with pytest.raises(RuntimeError, match="not JSON"):
        _extract_result("Deprecation warning\n{not json")
