# OSED Claude Code Plugin + Marketplace — Design Spec

**Status:** Approved (brainstorming) · **Created:** 2026-06-01 · **Branch:** `plugin-marketplace` (off `main`, all six instruments merged through PR #11)
**Distribution layer for OSED — part of the osenv.org umbrella distribution story. No instrument or skill behavior changes.**

> Design spec, not a plan. Records the validated design as input to `writing-plans`.

## Goal

Make OSED installable as a **Claude Code plugin**, distributed through a **self-hosted marketplace**
in this same repo, so users (and, later, other osenv agents) can `/plugin install` the six skills +
their templates + the regulatory MCP connector. v1 ships full functionality, including the connector.

## Verified mechanics (confirmed against code.claude.com/docs, 2026-06-01)

- A **marketplace** is a repo with `.claude-plugin/marketplace.json` (catalog); a **plugin** is a dir
  with `.claude-plugin/plugin.json`. Both can live at this repo's root (`source: "./"`).
- **Skills auto-discover** from `skills/<name>/SKILL.md`; installed, they namespace as `osed:<name>`.
- **On install, the plugin dir is COPIED to a cache; a skill cannot read files outside its dir.** So
  every file a skill reads must be bundled and referenced via `${CLAUDE_PLUGIN_ROOT}`.
- **`${CLAUDE_PLUGIN_ROOT}`** = the (ephemeral) install dir. **`${CLAUDE_PLUGIN_DATA}`** = a
  *persistent* dir (`~/.claude/plugins/data/{id}/`) the docs explicitly recommend for "Python virtual
  environments" — it survives plugin updates.
- **MCP servers**: declared in `.mcp.json` (plugin root) or inline `plugin.json.mcpServers`, with
  `command`/`args`/`env`/`cwd` and `${...}` substitution. They go through per-server approval like a
  project `.mcp.json`.
- **`userConfig`**: a plugin can prompt for config (e.g. API keys) on enable; values substitute as
  `${user_config.KEY}` in mcpServers `env` and export as `CLAUDE_PLUGIN_OPTION_<KEY>`.
- **Hooks** (`hooks/hooks.json`) support a `SessionStart` event and `${CLAUDE_PLUGIN_ROOT}` /
  `${CLAUDE_PLUGIN_DATA}` substitution — the canonical place to set up bundled-server dependencies.

## Decisions resolved during brainstorming

1. **Root-as-plugin** (`source: "./"`) — zero file moves; `skills/`, `templates/`,
   `docs/doctrinal-currency.md`, and `connectors/` already sit together and get copied as-is, so the
   eval harness, CI paths, and the WI-3 examples keep working untouched.
2. **Connector wired in v1** — full tool-backed currency out of the box.
3. **Python-only launch** — a `${CLAUDE_PLUGIN_DATA}` venv created by a `SessionStart` setup hook
   (needs only `python3`); **not** uvx (avoids a `uv` dependency).

## Component 1 — The two manifests (root-as-plugin + self-hosted marketplace)

`.claude-plugin/plugin.json`:
- `name: "osed"`, `version: "0.1.0"`, `description`, `author`, `homepage`/`repository`, `license`.
- `mcpServers` (or a sibling `.mcp.json`) declaring the regulatory connector (Component 3).
- `userConfig` declaring two optional secret keys: `courtlistener_api_key`, `regulations_gov_api_key`.

`.claude-plugin/marketplace.json`:
- `name: "osed"` (not a reserved name; `claude-for-legal` is reserved and unusable), `owner` (the
  maintainer), one `plugins` entry: `{ name: "osed", source: "./", description, version }`.

Install path for users: `/plugin marketplace add bgarakani/osed` → `/plugin install osed@osed`. The
six skills appear as `osed:intake`, `osed:gap-analysis`, `osed:drafting`, `osed:precedent-retrieval`,
`osed:plain-language`, `osed:pipeline`.

## Component 2 — Location-robust file references (the caching fix)

Two skill→file dependencies must resolve **both** in-repo (dev / evals / the live-eval lane / the
WI-3 examples) **and** installed (cache; cwd = user's project):
- `skills/drafting/SKILL.md` → `templates/*.md` (the "Choosing the instrument" table + one example
  reference). 12 references, all in this one file.
- `skills/{drafting,gap-analysis,precedent-retrieval}/SKILL.md` → `docs/doctrinal-currency.md`.

**Fix:** because SKILL.md is instructions to a reasoning agent (not code), make each reference state
the location for both modes rather than hard-swap to a single path — e.g.: *"read the template from
`${CLAUDE_PLUGIN_ROOT}/templates/<file>` when running as an installed plugin, or `templates/<file>`
from the repo root in development."* A single shared sentence/footnote per file is enough; the
individual table cells can stay as `templates/<file>` so the table reads cleanly, with the
location note stated once near the table.

**Eval-safety:** the deterministic markers (`markers.py`) assert skill *output* (banners, flags,
section headers), not these path strings, so the suite stays green. The live-eval lane reads SKILL.md
in-repo (no `${CLAUDE_PLUGIN_ROOT}`), and the "repo root in development" half of the sentence keeps it
resolvable.

**Honest limit (architectural smell, accepted):** the skill prose becomes environment-aware. This is
a pragmatic workaround, not a clean abstraction; a future cleanup could centralize "where my data
lives." Documented, not hidden.

## Component 3 — The regulatory MCP connector (Python-only, canonical pattern)

The connector (`connectors/regulatory/`, distribution `osed-connectors`, FastMCP, console script
`osed-connectors`, `requires-python >=3.11`) ships in the plugin (already at repo root). Wiring:

- **`SessionStart` setup hook** (`hooks/hooks.json` + a small bundled `scripts/setup-connector.sh`):
  idempotent and guarded — if `${CLAUDE_PLUGIN_DATA}/venv/bin/osed-connectors` is missing, run
  `python3 -m venv "${CLAUDE_PLUGIN_DATA}/venv"` and
  `"${CLAUDE_PLUGIN_DATA}/venv/bin/pip" install "${CLAUDE_PLUGIN_ROOT}/connectors/regulatory"`. After
  first run it's a fast existence check. The venv lives in the persistent data dir, so it survives
  plugin updates (re-created only if the connector changes — guard on a version/marker file).
- **The MCP server** (in `plugin.json.mcpServers`, key `osed-regulatory`):
  `command: "${CLAUDE_PLUGIN_DATA}/venv/bin/osed-connectors"`, `env` passing the two keys from
  `userConfig` (`COURTLISTENER_API_KEY: "${user_config.courtlistener_api_key}"`, etc.).
- **Keys are optional.** The keyless sources (Federal Register, eCFR, GovInfo) work with no keys;
  `verify_citation` and `find_rulemaking_documents` return their existing explicit not-found until
  keys are set. So the connector is useful immediately; keys are an enhancement.

**Concern #2 handling — never a silent failure.** The setup script must **emit a clear, visible
message** if `python3` is missing or the venv/pip step fails (e.g. echo a one-line
`OSED: regulatory connector unavailable (python3/venv setup failed) — currency tools will report
UNVERIFIED; see README` to the hook's user-visible output). The skills already degrade safely
(authorities flagged UNVERIFIED), but the user must be told tool-backed verification is off rather
than silently assume it is on.

## Component 4 — Concern #1: the currency-doc snapshot vs. the freshness design

Root-as-plugin copies `docs/doctrinal-currency.md` into the install cache, so its `Law-as-of` stamps
(including the four volatile state-ERA anchors) **freeze at install time** and refresh only on
`/plugin marketplace update`. This weakens the WI-6 freshness guarantee for installed users. Handling
(both, belt-and-suspenders):
1. **Make it explicit in the install docs**: a prominent "Keeping the law current" note — the bundled
   doctrinal anchors are a snapshot as of the installed version; run `/plugin marketplace update`
   to refresh them, and **always re-verify before relying** (consistent with the doc's own rule and
   the skills' currency step).
2. **Add one sentence to the currency-check instruction** the three skills already carry: when running
   as an installed plugin, treat the bundled `doctrinal-currency.md` as a snapshot, prefer the live
   doc at the repo URL for the current stamp, and re-verify. (No behavior change to the invariants —
   the stamp was never authoritative; this just keeps the snapshot from being mistaken for live.)

This is the single most important correctness item; it is called out for the legal-soundness-style
review at the end.

## Component 5 — Install docs + the `pipeline` namespacing check

- **README "Install as a Claude Code plugin" section**: the two `/plugin` commands; what works
  keyless vs. with keys; how to set the two API keys (via `userConfig` prompt or environment); the
  "Keeping the law current" note (Component 4); and the visible-failure note (Component 3).
- **Concern #3 verify**: confirm the `pipeline` skill (and any skill that references another) hands
  off in prose ("run the gap-analysis skill"), not via a hard-coded bare invocation that would break
  under `osed:` namespacing. If any hard invocation exists, make it namespace-robust. (Expected: all
  handoffs are prose; this is a verification step, not an anticipated change.)

## Component 6 — Testing / validation

- `cd evals && pytest` stays green throughout (no restructure; the path-reference edits don't touch
  the asserted markers). This is the regression gate.
- **Local install smoke test** (manual, recorded in the plan): from a separate checkout/dir,
  `/plugin marketplace add <path-to-this-repo>` → `/plugin install osed@osed` → confirm (a) the six
  skills appear namespaced, (b) the `SessionStart` hook builds the venv, (c) the `osed-regulatory`
  MCP server starts and answers a **keyless** call (e.g. `get_current_regulation` for a known CFR
  part), and (d) with a key set, a keyed call works. Record the outcome; if the MCP can't be smoke-
  tested in this environment, document the exact manual steps for the maintainer.
- The connector's own keyless CI smoke tests are unaffected.

## Six-invariant interaction

Distribution changes no instrument behavior, so invariants 1–2, 4–6 are untouched. **Invariant 3
(doctrinal currency)** is the one the packaging touches — Component 4 ensures the snapshot doesn't
silently masquerade as live, and Component 3 ensures the verification tools' availability is visible.

## Honest limits / out of scope

- No publishing to any third-party plugin index; no LSP/agents/output-styles/channels.
- No bundled secrets — API keys stay user-provided (`userConfig` or env).
- The path-reference approach is a pragmatic workaround (Component 2), not an architectural cleanup.
- The connector requires `python3` on the user's machine; if absent, the connector is unavailable and
  the skills degrade to UNVERIFIED (made visible per Component 3). Windows path specifics
  (`Scripts/osed-connectors.exe` vs `bin/osed-connectors`) are a known cross-platform wrinkle the plan
  must handle in the setup script.

## Open questions

None blocking. Resolvable in planning/build: the exact `userConfig` schema field names; whether the
MCP config lives inline in `plugin.json` or a sibling `.mcp.json` (functionally equivalent — default
to `plugin.json` inline for a single source of truth); and the precise Windows-vs-POSIX venv bin path
handling in the setup script.
