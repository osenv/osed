#!/usr/bin/env bash
# OSED: build/refresh the regulatory MCP connector venv in the persistent plugin data dir.
# Idempotent: rebuilds only when the connector version marker changes. Visible on failure.
set -u
DATA="${CLAUDE_PLUGIN_DATA:?CLAUDE_PLUGIN_DATA not set}"
ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT not set}"
VENV="$DATA/connector-venv"
SRC="$ROOT/connectors/regulatory"
MARKER="$VENV/.osed-connector-version"
WANT="$(grep -m1 '^version' "$SRC/pyproject.toml" 2>/dev/null || echo unknown)"

if [ -d "$VENV/Scripts" ]; then BIN="$VENV/Scripts"; else BIN="$VENV/bin"; fi

if [ -x "$BIN/osed-connectors" ] && [ "$(cat "$MARKER" 2>/dev/null)" = "$WANT" ]; then
  exit 0
fi

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "OSED: python3 not found — the regulatory connector is unavailable; currency checks will report UNVERIFIED. See the README 'Install as a Claude Code plugin' section." >&2
  exit 0
fi

if ! "$PY" -m venv "$VENV" >/dev/null 2>&1; then
  echo "OSED: could not create the connector venv ($VENV) — connector unavailable; currency checks will report UNVERIFIED. See README." >&2
  exit 0
fi
if [ -d "$VENV/Scripts" ]; then BIN="$VENV/Scripts"; else BIN="$VENV/bin"; fi
if ! "$BIN/python" -m pip install --quiet --upgrade pip "$SRC" >/dev/null 2>&1; then
  echo "OSED: connector install failed (pip) — connector unavailable; currency checks will report UNVERIFIED. Run 'pip install $SRC' manually or see README." >&2
  exit 0
fi
printf '%s' "$WANT" > "$MARKER"
echo "OSED: regulatory connector ready ($BIN/osed-connectors)." >&2
exit 0
