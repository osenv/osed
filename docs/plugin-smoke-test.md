# Plugin smoke test — connector setup chain

Task 8 of the plugin-marketplace plan. This records what an automated agent *can* verify
(the regulatory-connector setup hook, end to end) and the manual `/plugin` steps a maintainer
must still run on a real Claude Code instance.

Run on 2026-06-03, branch `plugin-marketplace`.

## Automated results

### Step 1 — eval regression gate

```
cd evals && .venv/bin/pytest -q
→ 77 passed, 8 deselected
```

Green. The six invariants' deterministic checks all hold.

### Step 2 — connector SETUP HOOK, end to end

Simulated the plugin runtime env (`CLAUDE_PLUGIN_ROOT` = repo root, `CLAUDE_PLUGIN_DATA` =
a fresh `mktemp -d`) and ran `scripts/setup-connector.sh`. The hook built a fresh venv and
`pip install`ed the connector from source (`connectors/regulatory/`).

- **venv built:** yes — `connector-venv/` created in the temp data dir.
- **console script present:** yes — `connector-venv/bin/osed-connectors` exists and is executable.
- **"ready" message printed:** yes — `OSED: regulatory connector ready (.../connector-venv/bin/osed-connectors).`
- **exit code:** 0.
- **marker file:** `connector-venv/.osed-connector-version` holds `version = "0.1.0"` (the
  `WANT` line `grep`'d from `pyproject.toml`).

### Step 3 — keyless connector works

Using the freshly-built venv's python:

```
osed_connectors.clients.ecfr.get_current_text(title=40, part="50")
→ ecfr found: True | source_current_as_of: 2026-06-01
```

eCFR is keyless; the live call succeeded with network access. The result carries its
`source_current_as_of` date, as required for the currency check.

### Step 4 — idempotency

A second run of `setup-connector.sh` with the same data dir exited **0 immediately** with
**no "ready" rebuild message** — the guard at the top of the script (`[ -x "$BIN/osed-connectors" ]`
plus matching marker) short-circuits the rebuild. Temp data dir was then removed.

## Manual `/plugin` steps (maintainer must run on a real Claude Code instance)

These CANNOT be exercised by an automated/non-interactive agent — they require the interactive
Claude Code plugin runtime. Run them to finish verification:

1. `/plugin marketplace add <path-to-this-repo>` (or `/plugin marketplace add osenv/osed`
   once pushed).
2. `/plugin install osed@osed`.
3. Confirm the six `osed:*` skills are listed: `intake`, `gap-analysis`, `drafting`,
   `precedent-retrieval`, `plain-language`, `pipeline`.
4. Confirm the **SessionStart hook** ran — look for the
   `OSED: regulatory connector ready (...)` message — and that
   `~/.claude/plugins/data/osed-osed/connector-venv/` exists (the persistent data dir; path
   shape depends on the host, but the `connector-venv/` leaf is what `setup-connector.sh` builds).
5. Confirm the `osed-regulatory` MCP server appears (it requires per-server approval on first
   use) and answers a **keyless** call, e.g. `get_current_regulation(title=40, part="50")`.
6. (Optional) Set a CourtListener key via plugin config (`courtlistener_api_key`) and confirm
   `verify_citation('484 U.S. 49')` resolves. Likewise `regulations_gov_api_key` enables
   `find_rulemaking_documents`. Keyless sources work without either key.

## Wrinkles found

- **`/connector-venv/` vs spec-prose `/venv/`:** the plan spec prose refers to a `/venv/`
  directory; the implementation (both `scripts/setup-connector.sh` and the
  `mcpServers.osed-regulatory.command` in `.claude-plugin/plugin.json`) uses **`/connector-venv/`**.
  The implementation is authoritative — both the hook and the MCP server command agree on
  `connector-venv/`, so they are consistent with each other.
- **Windows path:** `setup-connector.sh` correctly handles the Windows venv layout
  (`Scripts/` instead of `bin/`) when selecting `$BIN`. However, the MCP server command in
  `plugin.json` is hardcoded to the Unix path
  `${CLAUDE_PLUGIN_DATA}/connector-venv/bin/osed-connectors`. On Windows the console script would
  live under `Scripts/`, so the MCP server launch would not find it as written. Not a blocker for
  macOS/Linux (the validated platform); flag for a future cross-platform pass if Windows support
  is in scope.
