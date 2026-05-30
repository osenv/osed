"""Thin wrapper around the `claude -p` CLI used by the live lane.

Both the skill runner and the LLM judge shell out to `claude -p`. This module
centralizes that call and — crucially — the parsing of its output, which is the
one assumption most likely to drift between CLI versions.

`claude -p --output-format json` may emit either shape:
  - a single object `{"result": "...", ...}` (older CLIs), or
  - an array of event objects ending in a `{"type": "result", "result": "..."}`
    event (current CLIs: system → assistant → ... → result).
`_extract_result` is a pure function that handles both, so it can be unit-tested
without ever invoking the CLI.

Imported only on the `--live` path / `live` pytest marker.
"""

from __future__ import annotations

import json
import os
import subprocess


def _extract_result(stdout: str) -> str:
    """Pull the final result text out of `claude -p --output-format json` output."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"claude -p stdout not JSON: {stdout[:200]!r}") from exc
    if isinstance(data, dict):
        return data.get("result", "")
    if isinstance(data, list):
        for item in reversed(data):
            if isinstance(item, dict) and item.get("type") == "result":
                return item.get("result", "")
        raise RuntimeError("claude -p output array had no 'result' event")
    raise RuntimeError(f"unexpected claude -p output type: {type(data).__name__}")


def run_claude_p(prompt: str, timeout: int, *, label: str = "claude -p") -> str:
    """Invoke `claude -p ... --output-format json` and return the result text.

    Strips CLAUDECODE so this can nest inside a Claude Code session (the guard is
    for interactive terminals; programmatic subprocess use is safe). `label`
    distinguishes runner vs. judge failures in error messages.
    """
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    proc = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json"],
        capture_output=True, text=True, env=env, timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{label} failed ({proc.returncode}): {proc.stderr[:500]}")
    return _extract_result(proc.stdout)
