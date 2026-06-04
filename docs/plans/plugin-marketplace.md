# OSED Plugin + Marketplace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make OSED installable as a Claude Code plugin distributed via a self-hosted marketplace in this repo — six skills + templates + the doctrinal-currency doc + the regulatory MCP connector — without changing any instrument or skill behavior.

**Architecture:** Root-as-plugin (`.claude-plugin/{plugin.json,marketplace.json}` at repo root, `source: "./"`). Skill→file references migrate to the one skill-content variable that resolves at every install level — `${CLAUDE_SKILL_DIR}/../../<dir>` — so no dev-vs-installed branching. The Python connector is set up into the persistent `${CLAUDE_PLUGIN_DATA}` venv by an idempotent `SessionStart` hook (python3 only, visible on failure) and launched as an MCP server; API keys are optional `userConfig`.

**Tech Stack:** JSON manifests, a small POSIX/Windows-aware shell setup script, `hooks/hooks.json`, markdown skill edits, the `osed-connectors` FastMCP package, pytest (`osed_evals`).

**Spec:** `docs/specs/plugin-marketplace-design.md`. **Branch:** `plugin-marketplace` (created off merged `main`, already pushed).

---

## Verified mechanics (do not re-derive — confirmed against code.claude.com/docs, 2026-06-01)

- Skill **content** substitutes `${CLAUDE_SKILL_DIR}` (the skill's own dir; resolves at personal/project/plugin level). It does **NOT** substitute `${CLAUDE_PLUGIN_ROOT}` — that is only for MCP/hook/command **configs**.
- All OSED skills live at `skills/<name>/`, so the plugin/repo root is `${CLAUDE_SKILL_DIR}/../..`.
- MCP servers: inline `plugin.json.mcpServers` (single source of truth — use this, not a sibling `.mcp.json`). `command`/`args`/`env`/`cwd` with `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` / `${user_config.*}` substitution. Per-server approval on install.
- `${CLAUDE_PLUGIN_DATA}` = persistent dir (survives updates) the docs recommend for Python venvs.
- `userConfig` prompts for config (e.g. API keys) on enable; substitutes as `${user_config.KEY}` in mcpServers `env`.
- Hooks: `hooks/hooks.json`, `SessionStart` event supported, `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}` available in hook commands.

---

## File structure

**Create:**
- `.claude-plugin/plugin.json` — plugin manifest (name, version, mcpServers, userConfig).
- `.claude-plugin/marketplace.json` — marketplace catalog (one plugin, `source: "./"`).
- `hooks/hooks.json` — the `SessionStart` connector-setup hook.
- `scripts/setup-connector.sh` — idempotent venv builder, visible on failure, POSIX/Windows bin-path aware.

**Modify:**
- `skills/drafting/SKILL.md` — template path resolution (the "read the template" line + the example) via `${CLAUDE_SKILL_DIR}/../../templates/`; the doctrinal-currency reference.
- `skills/gap-analysis/SKILL.md`, `skills/precedent-retrieval/SKILL.md` — the doctrinal-currency reference.
- `CONTRIBUTING.md` — document the resource-reference convention once (the canonical definition).
- `evals/src/osed_evals/runner.py` — substitute `${CLAUDE_SKILL_DIR}` in the embedded prompt so the gated live lane resolves resources.
- `README.md` — "Install as a Claude Code plugin" section.
- `CHANGELOG.md` — `[Unreleased]` entry.

**No change:** any instrument/template content; `markers.py` (asserts output, not paths); `.github/workflows/evals.yml` (the path edits don't touch asserted markers; suite stays green).

**Heads-up (flagged, not in scope):** the repo already contains `scripts/scrape_climate_news.py` (undocumented, unrelated to OSED's six skills — likely early osenv open-data exploration). Root-as-plugin would copy it into users' caches. Out of scope here, but worth the maintainer deciding later whether it belongs in the published plugin (a `scripts/README.md` already exists). Do not delete it in this plan.

---

## Task 1: Document the resource-reference convention (the single canonical definition)

**Files:** Modify `CONTRIBUTING.md`.

- [ ] **Step 1: Add a "Resource references in skills (plugin-safe paths)" subsection.** Find the section of `CONTRIBUTING.md` that discusses skills/conventions (or add near the "Conventions when editing" content). Insert:
```markdown
### Resource references in skills (plugin-safe paths)

OSED ships as a Claude Code plugin, and an installed plugin is copied to a cache where a skill can
only read files inside the plugin directory. So when a skill needs a shared OSED resource (a template
or the doctrinal-currency doc), it must reference it through the one path variable that is substituted
in skill content and resolves at every install level: **`${CLAUDE_SKILL_DIR}`** (the skill's own
directory).

Every skill lives at `skills/<name>/`, so the OSED root is `${CLAUDE_SKILL_DIR}/../..`. Reference
shared resources as:
- a template → `${CLAUDE_SKILL_DIR}/../../templates/<file>`
- the currency doc → `${CLAUDE_SKILL_DIR}/../../docs/doctrinal-currency.md`

Do **not** use `${CLAUDE_PLUGIN_ROOT}` in skill body text — it is only substituted in MCP/hook/command
configs, not in `SKILL.md` prose. This convention keeps skills working identically in development and
when installed, with no environment-aware branching.
```

- [ ] **Step 2: Verify + commit**
```bash
grep -c "CLAUDE_SKILL_DIR" CONTRIBUTING.md   # >=1
cd evals && .venv/bin/pytest -q ; cd ..       # green (no behavior change)
git add CONTRIBUTING.md
git commit -m "contributing: document the \${CLAUDE_SKILL_DIR} plugin-safe resource convention"
```
Expected: grep ≥1; suite green.

---

## Task 2: Migrate `skills/drafting/SKILL.md` template references

**Files:** Modify `skills/drafting/SKILL.md`.

- [ ] **Step 1: Resolve the template path in the "read the template" instruction.** After the
"Choosing the instrument" table there is a line: `Read the relevant template file in full before
drafting. The templates encode required elements; ...`. Replace that sentence's start with a
plugin-safe path:
```markdown
Read the relevant template file in full before drafting — its path is `${CLAUDE_SKILL_DIR}/../../templates/<file>` (the `templates/` directory at the OSED root; the table lists each file by name). The templates encode required elements; omitting a required element is the single most common way these instruments fail.
```
Leave the table cells (lines ~22–29) as bare `` `templates/<file>` `` labels for readability — the resolved path is now stated once, here.

- [ ] **Step 2: Fix the example reference (line ~91).** Change `Read \`templates/cwa-505-notice-of-intent.md\`` to `Read the template at \`${CLAUDE_SKILL_DIR}/../../templates/cwa-505-notice-of-intent.md\``.

- [ ] **Step 3: Verify + commit**
```bash
grep -c "CLAUDE_SKILL_DIR}/../../templates/" skills/drafting/SKILL.md   # >=2
grep -c "DRAFT — ATTORNEY REVIEW REQUIRED\|REQUIRED-ELEMENTS CHECKLIST" skills/drafting/SKILL.md  # unchanged markers still present
cd evals && .venv/bin/pytest -q ; cd ..   # green
git add skills/drafting/SKILL.md
git commit -m "drafting skill: resolve template paths via \${CLAUDE_SKILL_DIR} (plugin-safe)"
```
Expected: first grep ≥2; suite green (the deterministic fixtures assert skill output, not these path strings).

---

## Task 3: Migrate the doctrinal-currency reference in three skills

**Files:** Modify `skills/drafting/SKILL.md`, `skills/gap-analysis/SKILL.md`, `skills/precedent-retrieval/SKILL.md`.

- [ ] **Step 1: In each of the three skills, replace the `docs/doctrinal-currency.md` reference** with the plugin-safe path plus the snapshot/update note. Each skill currently says `See \`docs/doctrinal-currency.md\`` (drafting and gap-analysis) or `See \`docs/doctrinal-currency.md\`.` mid-sentence (precedent-retrieval). Replace each occurrence of `` `docs/doctrinal-currency.md` `` with:
```
`${CLAUDE_SKILL_DIR}/../../docs/doctrinal-currency.md` (when OSED is installed as a plugin this bundled doctrinal-currency reference is a snapshot as of the installed version — run `/plugin marketplace update` to refresh it, and re-verify before relying)
```
Apply to **every** `docs/doctrinal-currency.md` occurrence in the three files (drafting has it twice in the same line; gap-analysis once; precedent-retrieval once). Keep the surrounding sentence intact.

- [ ] **Step 2: Verify + commit**
```bash
grep -rc "CLAUDE_SKILL_DIR}/../../docs/doctrinal-currency.md" skills/drafting/SKILL.md skills/gap-analysis/SKILL.md skills/precedent-retrieval/SKILL.md
grep -rc "plugin marketplace update" skills/drafting/SKILL.md skills/gap-analysis/SKILL.md skills/precedent-retrieval/SKILL.md
grep -rc "docs/doctrinal-currency.md" skills/*/SKILL.md | grep -v "CLAUDE_SKILL_DIR" || true   # no BARE refs remain
cd evals && .venv/bin/pytest -q ; cd ..
git add skills/drafting/SKILL.md skills/gap-analysis/SKILL.md skills/precedent-retrieval/SKILL.md
git commit -m "skills: resolve doctrinal-currency ref via \${CLAUDE_SKILL_DIR}; note snapshot + update on install"
```
Expected: each file's CLAUDE_SKILL_DIR count ≥1 (drafting ≥2); "plugin marketplace update" present in each; suite green.

---

## Task 4: Make the gated live-eval lane resolve `${CLAUDE_SKILL_DIR}`

**Files:** Modify `evals/src/osed_evals/runner.py`. The live runner embeds raw `SKILL.md` text into a `claude -p` prompt (it is not loaded as a registered skill), so `${CLAUDE_SKILL_DIR}` would otherwise appear literally. Substitute it with the skill's absolute directory before embedding.

- [ ] **Step 1: Substitute `${CLAUDE_SKILL_DIR}` in `_build_prompt`.** In `evals/src/osed_evals/runner.py`, the `_build_prompt` function reads `skill_md = _skill_md_path(fixture).read_text()`. Replace the path string in the embedded text. Change:
```python
def _build_prompt(fixture: Fixture) -> str:
    skill_md = _skill_md_path(fixture).read_text()
```
to:
```python
def _build_prompt(fixture: Fixture) -> str:
    skill_path = _skill_md_path(fixture)
    skill_md = skill_path.read_text()
    # Plugin skills resolve ${CLAUDE_SKILL_DIR} to the skill's own directory at runtime.
    # The live lane embeds SKILL.md as raw text (not a loaded skill), so substitute it here
    # to the skill's dir so any "${CLAUDE_SKILL_DIR}/../../<resource>" path resolves.
    skill_md = skill_md.replace("${CLAUDE_SKILL_DIR}", str(skill_path.parent))
```

- [ ] **Step 2: Add a unit test** `evals/tests/test_runner.py` (extend if it exists; else create) verifying the substitution. Because `_build_prompt` is module-internal, test via a tiny fixture:
```python
from osed_evals.models import Fixture, Turn
from osed_evals import runner


def test_build_prompt_substitutes_skill_dir(tmp_path, monkeypatch):
    skill_dir = tmp_path / "skills" / "drafting"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("read ${CLAUDE_SKILL_DIR}/../../templates/x.md")
    monkeypatch.setenv("OSED_EVAL_SKILL_DIR", str(skill_dir))
    fx = Fixture(skill="drafting", name="t", turns=[Turn(role="user", content="hi")], checks=[])
    prompt = runner._build_prompt(fx)
    assert "${CLAUDE_SKILL_DIR}" not in prompt
    assert f"{skill_dir}/../../templates/x.md" in prompt
```
(Match the actual `Fixture`/`Turn` constructor signatures in `models.py`; adjust field names if needed — read `models.py` first.)

- [ ] **Step 3: Run the test + full suite**
```bash
cd evals && .venv/bin/pytest tests/test_runner.py -q && .venv/bin/pytest -q ; cd ..
```
Expected: the new test passes; full deterministic suite green (the live lane stays gated/deselected).

- [ ] **Step 4: Commit**
```bash
git add evals/src/osed_evals/runner.py evals/tests/test_runner.py
git commit -m "evals: live runner substitutes \${CLAUDE_SKILL_DIR} so plugin-safe paths resolve"
```

---

## Task 5: Plugin + marketplace manifests

**Files:** Create `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`.

- [ ] **Step 1: Create `.claude-plugin/plugin.json`** (the MCP + userConfig land here in Task 6; this step is the base manifest):
```json
{
  "name": "osed",
  "version": "0.1.0",
  "description": "Open Source Environmental Defense — skills that draft environmental-litigation instruments (citizen-suit notices, rulemaking petitions, deadline complaints, consent-decree scaffolds, state environmental-rights orientation packets). OSED drafts; a licensed attorney decides.",
  "author": { "name": "Behrang Garakani" },
  "homepage": "https://github.com/bgarakani/osed",
  "repository": "https://github.com/bgarakani/osed",
  "license": "MIT"
}
```

- [ ] **Step 2: Create `.claude-plugin/marketplace.json`:**
```json
{
  "name": "osed",
  "owner": { "name": "Behrang Garakani" },
  "description": "OSED — open-source environmental-litigation drafting skills.",
  "plugins": [
    {
      "name": "osed",
      "source": "./",
      "description": "The six OSED skills + instrument templates + the regulatory MCP connector."
    }
  ]
}
```

- [ ] **Step 3: Validate JSON + commit**
```bash
python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('valid JSON')"
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "plugin: add OSED plugin manifest + self-hosted marketplace catalog (root-as-plugin)"
```
Expected: `valid JSON`.

---

## Task 6: Wire the regulatory MCP connector (Python-only setup hook + MCP server + keys)

**Files:** Create `scripts/setup-connector.sh`, `hooks/hooks.json`; modify `.claude-plugin/plugin.json`.

- [ ] **Step 1: Create the idempotent setup script** `scripts/setup-connector.sh` (POSIX + Windows-Git-Bash aware; visible on failure). The venv lives in the persistent data dir and is rebuilt only when the connector's version marker changes:
```bash
#!/usr/bin/env bash
# OSED: build/refresh the regulatory MCP connector venv in the persistent plugin data dir.
# Idempotent: rebuilds only when the connector version marker changes. Visible on failure.
set -u
DATA="${CLAUDE_PLUGIN_DATA:?CLAUDE_PLUGIN_DATA not set}"
ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT not set}"
VENV="$DATA/connector-venv"
SRC="$ROOT/connectors/regulatory"
MARKER="$VENV/.osed-connector-version"
WANT="$(cat "$SRC/pyproject.toml" 2>/dev/null | grep -m1 '^version' || echo unknown)"

# bin dir differs on Windows (Scripts) vs POSIX (bin)
if [ -d "$VENV/Scripts" ]; then BIN="$VENV/Scripts"; else BIN="$VENV/bin"; fi

if [ -x "$BIN/osed-connectors" ] && [ "$(cat "$MARKER" 2>/dev/null)" = "$WANT" ]; then
  exit 0   # up to date
fi

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "OSED: python3 not found — the regulatory connector is unavailable; currency checks will report UNVERIFIED. See the README 'Install as a Claude Code plugin' section." >&2
  exit 0   # do not fail the session; skills degrade safely
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
```
Make it executable: `chmod +x scripts/setup-connector.sh`.

- [ ] **Step 2: Create `hooks/hooks.json`** wiring the setup script to `SessionStart` (exec form, quoted plugin-root path):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/setup-connector.sh\"" }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: Add `mcpServers` + `userConfig` to `.claude-plugin/plugin.json`.** Add these two top-level keys (the connector launches from the data-dir venv; keys are optional). Update the file so it reads:
```json
{
  "name": "osed",
  "version": "0.1.0",
  "description": "Open Source Environmental Defense — skills that draft environmental-litigation instruments (citizen-suit notices, rulemaking petitions, deadline complaints, consent-decree scaffolds, state environmental-rights orientation packets). OSED drafts; a licensed attorney decides.",
  "author": { "name": "Behrang Garakani" },
  "homepage": "https://github.com/bgarakani/osed",
  "repository": "https://github.com/bgarakani/osed",
  "license": "MIT",
  "userConfig": {
    "courtlistener_api_key": {
      "type": "string",
      "title": "CourtListener API token",
      "description": "Optional CourtListener API token for verify_citation (case-law currency). Keyless sources work without it.",
      "sensitive": true,
      "required": false
    },
    "regulations_gov_api_key": {
      "type": "string",
      "title": "Regulations.gov API key",
      "description": "Optional Regulations.gov API key for find_rulemaking_documents. Keyless sources work without it.",
      "sensitive": true,
      "required": false
    }
  },
  "mcpServers": {
    "osed-regulatory": {
      "command": "${CLAUDE_PLUGIN_DATA}/connector-venv/bin/osed-connectors",
      "env": {
        "COURTLISTENER_API_KEY": "${user_config.courtlistener_api_key}",
        "REGULATIONS_GOV_API_KEY": "${user_config.regulations_gov_api_key}"
      }
    }
  }
}
```
> Note: the `command` uses the POSIX `bin/` path. The setup script also handles Windows `Scripts/`; if cross-platform launch is needed, the plan's validation (Task 8) records whether a Windows-specific `command` variant is required. For v1, document POSIX/macOS/Linux as supported and Windows as best-effort.

- [ ] **Step 4: Validate + commit**
```bash
python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); print('valid JSON')"
bash -n scripts/setup-connector.sh && echo "setup script parses"
python3 -c "import json; json.load(open('hooks/hooks.json')); print('hooks valid JSON')"
cd evals && .venv/bin/pytest -q ; cd ..
git add scripts/setup-connector.sh hooks/hooks.json .claude-plugin/plugin.json
git commit -m "plugin: wire osed-regulatory MCP via persistent venv (SessionStart setup hook, optional keys, visible failure)"
```
Expected: all "valid"/"parses"; suite green.

---

## Task 7: Install docs (README + CHANGELOG)

**Files:** Modify `README.md`, `CHANGELOG.md`.

- [ ] **Step 1: Add a "Install as a Claude Code plugin" section to `README.md`** (place it after "Quick start"):
```markdown
## Install as a Claude Code plugin

OSED is also a Claude Code plugin, distributed from this repo as a self-hosted marketplace:

```
/plugin marketplace add bgarakani/osed
/plugin install osed@osed
```

The six skills then appear namespaced — `/osed:intake`, `/osed:gap-analysis`, `/osed:drafting`,
`/osed:precedent-retrieval`, `/osed:plain-language`, `/osed:pipeline` — and the instrument templates
travel with them.

**Regulatory connector (tool-backed currency checks).** On first session the plugin builds a small
Python virtual environment for the `osed-regulatory` MCP server (requires `python3`). The keyless
sources — Federal Register, eCFR, GovInfo — work immediately. Two tools need free API keys, which the
plugin prompts for on enable (both optional): a CourtListener token (`verify_citation`) and a
Regulations.gov key (`find_rulemaking_documents`). Without `python3` or the keys, the skills degrade
safely — they flag authorities **UNVERIFIED** rather than guessing — and the setup step prints a
visible message so you know the connector is unavailable.

**Keeping the law current.** The bundled `docs/doctrinal-currency.md` anchors (and any dated stamps)
are a **snapshot as of the installed plugin version**. Run `/plugin marketplace update` to refresh
them, and — as the doc and every skill insist — **re-verify any authority in primary sources before
relying on it**. A stamp records that a human checked; it is never a substitute for checking.
```

- [ ] **Step 2: Add a `CHANGELOG.md` `[Unreleased]` entry:**
```markdown
### Added
- OSED is now installable as a **Claude Code plugin** via a self-hosted marketplace (`.claude-plugin/marketplace.json` + `plugin.json`): the six skills, the instrument templates, and the `osed-regulatory` MCP connector (built into a persistent Python venv by a SessionStart hook; optional CourtListener / Regulations.gov keys via plugin config). See the README "Install as a Claude Code plugin" section.

### Changed
- Skills reference shared resources (templates, the doctrinal-currency doc) via `${CLAUDE_SKILL_DIR}/../..` so the paths resolve identically in development and when installed as a plugin; the currency reference notes the bundled doc is a snapshot (run `/plugin marketplace update` + re-verify).
```

- [ ] **Step 3: Verify + commit**
```bash
grep -c "Install as a Claude Code plugin" README.md   # ==1
grep -c "plugin marketplace add bgarakani/osed" README.md   # >=1
cd evals && .venv/bin/pytest -q ; cd ..
git add README.md CHANGELOG.md
git commit -m "docs: README install-as-plugin section + CHANGELOG (currency-snapshot + keyless notes)"
```

---

## Task 8: Validation — eval suite + local install smoke test

**Files:** none (or a short `docs/plugin-smoke-test.md` recording the manual steps/outcome).

- [ ] **Step 1: Full deterministic suite green** — `cd evals && .venv/bin/pytest -q ; cd ..` (the real regression gate; expect all pass, live deselected).
- [ ] **Step 2: Local install smoke test.** From a separate Claude Code session (or document the steps if not runnable here):
  1. `/plugin marketplace add /Users/behranggarakani/GitHub/osed/.claude/worktrees/bridge-cse_01XNcdFCT7dRU5qGStX85ew1` (or the repo path)
  2. `/plugin install osed@osed`
  3. Confirm the six `osed:*` skills are listed.
  4. Confirm the `SessionStart` hook ran (the "regulatory connector ready" message) and the venv exists at `~/.claude/plugins/data/osed-osed/connector-venv/`.
  5. Confirm the `osed-regulatory` MCP server appears and answers a **keyless** call, e.g. `get_current_regulation(title=40, part="50")`.
  6. (Optional) set a CourtListener key via the plugin config and confirm `verify_citation('484 U.S. 49')` resolves.
- [ ] **Step 3: Record outcome** in `docs/plugin-smoke-test.md` (what passed; any Windows/path wrinkle found in the MCP `command`; whether a Windows `command` variant is needed). If the smoke test cannot run in this environment, document the exact maintainer steps and mark it as "to verify on a real install."
- [ ] **Step 4: Commit** (only if a doc was added):
```bash
git add docs/plugin-smoke-test.md
git commit -m "docs: record the plugin local-install smoke test (and any path wrinkles)"
```

---

## Task 9: Finish the branch

- [ ] **Step 1: Full suite** — `cd evals && .venv/bin/pytest -q ; cd ..` (green).
- [ ] **Step 2: No Claude attribution** — `git log origin/main..HEAD --format="%b" | grep -i "co-authored-by\|claude\|🤖" || echo OK`.
- [ ] **Step 3: Verify the `pipeline` namespacing** (spec Component 5): `grep -n "skill" skills/pipeline/SKILL.md | grep -iE "run the .* skill|gap-analysis|drafting|precedent|plain-language|intake"` — confirm handoffs are prose ("run the gap-analysis skill"), not a hard-coded bare invocation that would break under `osed:` namespacing. If any hard invocation exists, make it namespace-robust and commit. (Expected: prose only — a verification step.)
- [ ] **Step 4: Invoke `superpowers:finishing-a-development-branch`** and present the standard options (expected: Push and create a Pull Request; PR body carries NO Claude attribution).

---

## Self-review notes (author)

- **Spec coverage:** Component 1 (manifests) → Task 5; Component 2 (`${CLAUDE_SKILL_DIR}` abstraction) → Tasks 1–4 (convention + 3 skill migrations + live-runner); Component 3 (connector) → Task 6; Component 4 (currency snapshot) → Task 3 (skill note) + Task 7 (README note); Component 5 (install docs + pipeline check) → Task 7 + Task 9 Step 3; Component 6 (testing) → Task 8.
- **The corrected mechanism** (`${CLAUDE_SKILL_DIR}` in skill content; `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}` only in the MCP/hook configs) is applied consistently: Tasks 1–4 use `${CLAUDE_SKILL_DIR}`; Task 6 uses `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}`.
- **Eval-safety:** the deterministic suite is green at every task (it asserts skill output, not path strings). The live lane is handled by Task 4. The `markers.py` constants are untouched.
- **Concern handling baked in:** the silent-failure concern → Task 6's visible `echo …>&2` on every failure branch (degrade safely, never fail the session); the currency-snapshot concern → Task 3 skill note + Task 7 README "Keeping the law current," update+re-verify only (no external URL).
- **Name consistency:** the MCP server key (`osed-regulatory`), the venv path (`${CLAUDE_PLUGIN_DATA}/connector-venv`), and the userConfig keys (`courtlistener_api_key`, `regulations_gov_api_key`) are used identically in the hook script, plugin.json, and the README.
- **Flagged-not-actioned:** `scripts/scrape_climate_news.py` (undocumented) is left untouched; surfaced for the maintainer.
