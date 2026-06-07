/* ============================================================
   pack-skills.mjs — package the OSED skills as self-contained .zip
   files ready to upload to claude.ai / Claude Cowork (and the Claude
   API Skills endpoint).

   Why: a Skill uploaded to claude.ai runs in a sandbox that only sees
   ITS OWN folder. Our SKILL.md files reference sibling resources in
   this repo (templates/*.md, docs/doctrinal-currency.md), which would
   dangle once a skill leaves the repo. This script parses each SKILL.md
   for those references, VENDORS the referenced files into the skill's
   zip under the same relative path, validates the frontmatter against
   claude.ai's limits, and writes one <skill>.zip per skill into
   dist-skills/.

   Run: `node scripts/pack-skills.mjs`  (Node 18+, no dependencies)
   ============================================================ */
import {
  readFileSync, writeFileSync, mkdirSync, rmSync, cpSync, readdirSync, existsSync, statSync,
} from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join, relative } from "node:path";

// scripts/ sits at the repo root, so the repo IS the resource base.
const REPO = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = join(REPO, "skills");
const OUT = join(REPO, "dist-skills");
const STAGE = join(OUT, ".stage");

// claude.ai / API frontmatter constraints (docs: agent-skills/overview)
const NAME_RE = /^[a-z0-9-]{1,64}$/;
const RESERVED = ["anthropic", "claude"];
const DESC_MAX = 1024;

/* ---------- preconditions ---------- */
if (!existsSync(SKILLS_DIR)) {
  throw new Error(`skills/ not found at ${SKILLS_DIR} — run from the OSED repo root.`);
}
try {
  execFileSync("zip", ["-v"], { stdio: "ignore" });
} catch {
  throw new Error("`zip` CLI not found on PATH. (macOS ships it; Debian/Ubuntu: `apt-get install zip`).");
}

/* ---------- helpers ---------- */
// Minimal YAML-frontmatter read for the two fields we validate.
function frontmatter(md) {
  const m = md.match(/^---\n([\s\S]*?)\n---/);
  const block = m ? m[1] : "";
  const field = (k) => {
    const r = block.match(new RegExp(`^${k}:\\s*(.+)$`, "m"));
    return r ? r[1].trim() : "";
  };
  return { name: field("name"), description: field("description") };
}

// Expand one referenced path (which may contain a <placeholder>) to the set of
// real files in the repo. `templates/state-era-<state>.md` → every
// `templates/state-era-*.md`; `templates/<file>` → every file in templates/.
function resolveRef(ref) {
  if (!ref.includes("<")) {
    return existsSync(join(REPO, ref)) ? [ref] : [];
  }
  const star = ref.replace(/<[^>]+>/g, "*");
  const dir = dirname(star);
  const base = star.slice(dir.length + 1);
  const reStr = "^" + base.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*") + "$";
  const re = new RegExp(reStr);
  const abs = join(REPO, dir);
  if (!existsSync(abs)) return [];
  return readdirSync(abs)
    .filter((f) => re.test(f) && statSync(join(abs, f)).isFile())
    .map((f) => join(dir, f));
}

// Pull every templates/… and docs/… reference out of a SKILL.md body.
function referencedResources(md) {
  const refs = new Set();
  const re = /\b(?:templates|docs)\/[A-Za-z0-9._<>\/-]+/g;
  for (const tok of md.match(re) || []) {
    for (const f of resolveRef(tok)) refs.add(f);
  }
  return [...refs].sort();
}

/* ---------- build ---------- */
rmSync(OUT, { recursive: true, force: true });
mkdirSync(STAGE, { recursive: true });

const skills = readdirSync(SKILLS_DIR).filter((d) =>
  existsSync(join(SKILLS_DIR, d, "SKILL.md"))
);

const report = [];
let hardErrors = 0;

for (const name of skills) {
  const srcDir = join(SKILLS_DIR, name);
  const md = readFileSync(join(srcDir, "SKILL.md"), "utf8");
  const fm = frontmatter(md);
  const problems = [];

  if (!NAME_RE.test(fm.name)) problems.push(`name "${fm.name}" must match ${NAME_RE}`);
  if (RESERVED.some((w) => fm.name.toLowerCase().includes(w)))
    problems.push(`name "${fm.name}" contains a reserved word (${RESERVED.join("/")})`);
  if (fm.name !== name) problems.push(`folder "${name}" ≠ frontmatter name "${fm.name}"`);
  if (!fm.description) problems.push("description is empty");
  if (fm.description.length > DESC_MAX)
    problems.push(`description ${fm.description.length} chars > ${DESC_MAX}`);
  if (problems.length) hardErrors++;

  // stage a self-contained copy: SKILL.md + any sibling files + referenced resources
  const stageDir = join(STAGE, name);
  mkdirSync(stageDir, { recursive: true });
  for (const f of readdirSync(srcDir)) {
    cpSync(join(srcDir, f), join(stageDir, f), { recursive: true });
  }
  const bundled = referencedResources(md);
  for (const rel of bundled) {
    const dest = join(stageDir, rel);
    mkdirSync(dirname(dest), { recursive: true });
    cpSync(join(REPO, rel), dest);
  }

  const zipPath = join(OUT, `${name}.zip`);
  execFileSync("zip", ["-r", "-q", "-X", zipPath, name], { cwd: STAGE });

  report.push({ name, problems, bundled, sizeKB: Math.round(statSync(zipPath).size / 1024) });
}

rmSync(STAGE, { recursive: true, force: true });

/* ---------- manifest + console summary ---------- */
const lines = [
  "# OSED skill bundles — manifest",
  "",
  "Auto-generated by `scripts/pack-skills.mjs`. Each `.zip` is a self-contained Agent Skill",
  "(SKILL.md + the templates/docs it references) ready to upload to claude.ai / Claude Cowork.",
  "",
];
for (const r of report) {
  lines.push(`## ${r.name}.zip  (${r.sizeKB} KB)`);
  if (r.problems.length) lines.push(...r.problems.map((p) => `- ⚠️ ${p}`));
  lines.push(r.bundled.length ? "- vendored resources:" : "- vendored resources: none (self-contained prose skill)");
  for (const b of r.bundled) lines.push(`  - ${b}`);
  lines.push("");
}
writeFileSync(join(OUT, "MANIFEST.md"), lines.join("\n"));

console.log(`\nPacked ${report.length} skill(s) → ${relative(REPO, OUT)}/\n`);
for (const r of report) {
  const flag = r.problems.length ? "  ✗ " + r.problems.join("; ") : "  ✓";
  console.log(`  ${r.name}.zip  ${r.sizeKB} KB  (+${r.bundled.length} vendored)${flag}`);
}
console.log(`\nManifest: ${relative(REPO, join(OUT, "MANIFEST.md"))}`);

if (hardErrors) {
  console.error(`\n${hardErrors} skill(s) failed frontmatter validation — fix before distributing.`);
  process.exit(1);
}
