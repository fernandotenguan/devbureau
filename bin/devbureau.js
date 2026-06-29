#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const readline = require("readline");
const { spawnSync } = require("child_process");
const { createHash } = require("crypto");

const PACKAGE_ROOT = path.resolve(__dirname, "..");
const SOURCE_AGENT_DIR = path.join(PACKAGE_ROOT, ".agent");
const SOURCE_MCP_CONFIG = path.join(PACKAGE_ROOT, ".mcp.json");
const MANIFEST_FILENAME = ".devbureau-manifest.json";
// Sidecar, not a manifest key — uninstall()/update() both assume every manifest
// key is a real .agent/... path, so version metadata gets its own tiny file.
const VERSION_FILENAME = ".devbureau-version";

function currentPackageVersion() {
  return JSON.parse(fs.readFileSync(path.join(PACKAGE_ROOT, "package.json"), "utf8")).version;
}

function saveVersionFile(targetDir, version) {
  fs.writeFileSync(path.join(targetDir, VERSION_FILENAME), `${version}\n`, "utf8");
}

function loadVersionFile(targetDir) {
  const versionPath = path.join(targetDir, VERSION_FILENAME);
  if (!fs.existsSync(versionPath)) return null;
  try {
    return fs.readFileSync(versionPath, "utf8").trim() || null;
  } catch {
    return null;
  }
}
const IDE_TARGETS = [
  "claude", "cursor", "codex", "opencode", "copilot", "antigravity", "windsurf", "cline", "roocode", "zed", "all",
];

// Detects which AI IDE/engine is already in use in this project, by checking
// for the folder/file each one creates on its own (not files DevBureau generates).
const ENGINE_DETECTORS = {
  claude: (dir) => fs.existsSync(path.join(dir, ".claude")),
  cursor: (dir) => fs.existsSync(path.join(dir, ".cursor")) || fs.existsSync(path.join(dir, ".cursorrules")),
  codex: (dir) => fs.existsSync(path.join(dir, "AGENTS.md")),
  // OpenCode also reads root AGENTS.md (same convention as Codex CLI), but
  // it additionally creates its own .opencode/ project folder — that's the
  // only marker that distinguishes it, since AGENTS.md alone is ambiguous.
  opencode: (dir) => fs.existsSync(path.join(dir, ".opencode")),
  antigravity: (dir) => fs.existsSync(path.join(dir, ".antigravity")),
  copilot: (dir) => fs.existsSync(path.join(dir, ".github", "copilot-instructions.md")),
  windsurf: (dir) => fs.existsSync(path.join(dir, ".windsurfrules")) || fs.existsSync(path.join(dir, ".windsurf")),
  cline: (dir) => fs.existsSync(path.join(dir, ".clinerules")) || fs.existsSync(path.join(dir, ".cline")),
  roocode: (dir) => fs.existsSync(path.join(dir, ".roorules")) || fs.existsSync(path.join(dir, ".roo")),
  // Zed's own project-local settings folder — distinct from the .rules file
  // DevBureau generates, which Zed reads but doesn't create on its own.
  zed: (dir) => fs.existsSync(path.join(dir, ".zed")),
};

function detectInstalledEngines(targetDir) {
  return Object.keys(ENGINE_DETECTORS).filter((id) => ENGINE_DETECTORS[id](targetDir));
}

function findPythonCommand() {
  const candidates = process.platform === "win32" ? ["python", "py", "python3"] : ["python3", "python"];
  for (const candidate of candidates) {
    const result = spawnSync(candidate, ["--version"], { encoding: "utf8" });
    const output = `${result.stdout || ""}${result.stderr || ""}`;
    if (result.status === 0 && output.trim().startsWith("Python")) return candidate;
  }
  return null;
}

// Lists every file under dir, recursively, as POSIX-style paths relative to baseDir.
function listFilesRecursive(dir, baseDir) {
  baseDir = baseDir || dir;
  let results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const absPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(listFilesRecursive(absPath, baseDir));
    } else {
      results.push(path.relative(baseDir, absPath).split(path.sep).join("/"));
    }
  }
  return results;
}

function hashFile(absPath) {
  if (!fs.existsSync(absPath) || fs.statSync(absPath).isDirectory()) return null;
  return createHash("sha256").update(fs.readFileSync(absPath)).digest("hex");
}

// relPaths are project-root-relative (e.g. ".agent/agents/orchestrator.md").
function buildManifest(baseDir, relPaths) {
  const manifest = {};
  for (const relPath of relPaths) {
    const hash = hashFile(path.join(baseDir, relPath));
    if (hash) manifest[relPath] = hash;
  }
  return manifest;
}

function saveManifest(targetDir, manifest) {
  fs.writeFileSync(
    path.join(targetDir, MANIFEST_FILENAME),
    JSON.stringify(manifest, null, 2) + "\n",
    "utf8"
  );
}

function loadManifest(targetDir) {
  const manifestPath = path.join(targetDir, MANIFEST_FILENAME);
  if (!fs.existsSync(manifestPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  } catch {
    return null;
  }
}

function agentRelFiles(baseDir) {
  return listFilesRecursive(path.join(baseDir, ".agent")).map((p) => path.posix.join(".agent", p));
}

function copyAgentFolder(targetDir, force) {
  const destination = path.join(targetDir, ".agent");
  if (fs.existsSync(destination) && !force) {
    throw new Error(
      `.agent/ already exists at ${destination}. Re-run with --force to overwrite.`
    );
  }
  fs.cpSync(SOURCE_AGENT_DIR, destination, { recursive: true, force: true });
  saveManifest(targetDir, buildManifest(targetDir, agentRelFiles(targetDir)));
  saveVersionFile(targetDir, currentPackageVersion());
  return destination;
}

function copyMcpConfigIfAbsent(targetDir) {
  const destination = path.join(targetDir, ".mcp.json");
  if (fs.existsSync(destination)) {
    console.log("ℹ .mcp.json already exists — leaving it untouched.");
    return;
  }
  fs.copyFileSync(SOURCE_MCP_CONFIG, destination);
  console.log(`✔ Added starter .mcp.json (GitHub MCP server, OAuth — no token needed in the file)`);
}

function runPythonScript(pythonCmd, targetDir, relativeScriptPath, extraArgs) {
  const scriptPath = path.join(targetDir, relativeScriptPath);
  const result = spawnSync(pythonCmd, [scriptPath, ...extraArgs], {
    cwd: targetDir,
    stdio: "inherit",
  });
  return result.status === 0;
}

// Splits on comma, comma+space, or plain whitespace, then validates each
// token against IDE_TARGETS. "all" short-circuits the rest since it already
// covers every target on its own.
function parseIdeTargets(rawInput) {
  const tokens = rawInput.trim().toLowerCase().split(/[,\s]+/).filter(Boolean);
  if (tokens.includes("all")) return { valid: ["all"], invalid: [] };

  const valid = [];
  const invalid = [];
  for (const token of tokens) {
    if (token === "skip") continue;
    if (!IDE_TARGETS.includes(token)) invalid.push(token);
    else if (!valid.includes(token)) valid.push(token);
  }
  return { valid, invalid };
}

function promptIdeTarget(detectedEngines) {
  if (!process.stdin.isTTY) return Promise.resolve({ valid: [], invalid: [] });

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const defaultChoice = detectedEngines.length === 1 ? detectedEngines[0] : "skip";
  const detectedHint = detectedEngines.length > 0 ? ` (detected: ${detectedEngines.join(", ")})` : "";
  const question =
    `\nWhich IDE(s) do you want to sync rules to? Separate multiple with a comma or space.${detectedHint} [${IDE_TARGETS.join(", ")}, skip] (default: ${defaultChoice}): `;

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      const trimmed = answer.trim();
      if (trimmed === "") {
        return resolve(defaultChoice === "skip" ? { valid: [], invalid: [] } : { valid: [defaultChoice], invalid: [] });
      }
      resolve(parseIdeTargets(trimmed));
    });
  });
}

async function init(args) {
  const targetDir = process.cwd();
  const force = args.includes("--force");
  const explicitTargetArg = args.find((arg) => arg.startsWith("--target="));
  const pythonCmd = findPythonCommand();

  console.log("\n🏛️  DevBureau — Project Setup\n");

  if (!pythonCmd) {
    console.error(
      "✘ Python was not found (tried py/python/python3). Install Python 3.9+ and re-run."
    );
    process.exitCode = 1;
    return;
  }

  let agentDir;
  try {
    agentDir = copyAgentFolder(targetDir, force);
  } catch (error) {
    console.error(`✘ ${error.message}`);
    process.exitCode = 1;
    return;
  }
  console.log(`✔ Copied .agent/ to ${agentDir}`);

  copyMcpConfigIfAbsent(targetDir);

  const doctorOk = runPythonScript(pythonCmd, targetDir, ".agent/scripts/doctor.py", []);
  if (!doctorOk) {
    console.error("\n✘ Kit health check failed. Fix the issues above before continuing.");
    process.exitCode = 1;
    return;
  }

  const gitDir = path.join(targetDir, ".git");
  if (fs.existsSync(gitDir)) {
    runPythonScript(pythonCmd, targetDir, ".agent/scripts/install_hooks.py", []);
  } else {
    console.log("ℹ No .git/ found — skipping pre-commit hook install. Run `git init` first if you want it.");
  }

  const detectedEngines = detectInstalledEngines(targetDir);
  let ideTargets = [];
  let invalidTargets = [];
  if (explicitTargetArg) {
    ({ valid: ideTargets, invalid: invalidTargets } = parseIdeTargets(explicitTargetArg.split("=")[1] || ""));
  } else if (process.stdin.isTTY) {
    ({ valid: ideTargets, invalid: invalidTargets } = await promptIdeTarget(detectedEngines));
  } else if (detectedEngines.length === 1) {
    ideTargets = [detectedEngines[0]];
    console.log(`ℹ Detected ${ideTargets[0]} in this project — syncing automatically (non-interactive mode).`);
  }

  if (invalidTargets.length > 0) {
    console.log(`⚠ Ignoring unrecognized IDE name(s): ${invalidTargets.join(", ")}`);
  }

  if (ideTargets.length > 0) {
    for (const target of ideTargets) {
      runPythonScript(pythonCmd, targetDir, ".agent/scripts/sync_ide.py", ["--target", target]);
    }
  } else {
    console.log("ℹ Skipped IDE sync. Run `python .agent/scripts/sync_ide.py --target <ide>` whenever you're ready.");
  }

  console.log("\n✅ DevBureau is set up. Open this project in your AI assistant and start with /brainstorm or /ade.\n");
}

// Reads CHANGELOG.md from the freshly-installed package and prints the entries
// between the previously-installed version and the new one (newest first,
// capped at 5 full entries). Falls back to a one-liner if either version's
// heading can't be located (manually-edited version file, missing entry).
function printChangelogSince(previousVersion, newVersion) {
  let changelog;
  try {
    changelog = fs.readFileSync(path.join(PACKAGE_ROOT, "CHANGELOG.md"), "utf8");
  } catch {
    return;
  }

  const headerPattern = /^### \[([^\]]+)\] - .+$/gm;
  const matches = [...changelog.matchAll(headerPattern)];
  const startIdx = matches.findIndex((m) => m[1] === newVersion);
  const endIdx = matches.findIndex((m) => m[1] === previousVersion);

  if (startIdx === -1 || endIdx === -1 || endIdx <= startIdx) {
    console.log(`\nℹ Atualizado de v${previousVersion} para v${newVersion} — veja CHANGELOG.md para detalhes.`);
    return;
  }

  const entries = matches.slice(startIdx, endIdx);
  const shown = entries.slice(0, 5);

  console.log(`\n📋 Novidades desde v${previousVersion}:\n`);
  for (const m of shown) {
    const entryStart = m.index;
    const next = matches[matches.indexOf(m) + 1];
    const entryEnd = next ? next.index : changelog.length;
    console.log(changelog.slice(entryStart, entryEnd).trim());
    console.log("");
  }
  if (entries.length > shown.length) {
    console.log(`...e mais ${entries.length - shown.length} releases anteriores — veja CHANGELOG.md para o histórico completo.\n`);
  }
}

function update(args) {
  const targetDir = process.cwd();
  const force = args.includes("--force");
  const destAgentDir = path.join(targetDir, ".agent");

  console.log("\n🏛️  DevBureau — Update\n");

  if (!fs.existsSync(destAgentDir)) {
    console.error("✘ No .agent/ found in this directory. Run `npx devbureau init` first.");
    process.exitCode = 1;
    return;
  }

  const previousManifest = loadManifest(targetDir);
  if (!previousManifest && !force) {
    console.log(
      "ℹ No manifest found (installed before `update` existed, or the manifest file was removed)."
    );
    console.log(
      "  Without it, DevBureau can't tell which files in .agent/ you customized — nothing was changed."
    );
    console.log(
      "  Re-run with --force to overwrite everything anyway (this WILL discard any local edits under .agent/)."
    );
    return;
  }

  const previousVersion = loadVersionFile(targetDir);
  const newVersion = currentPackageVersion();

  const sourceRelFiles = agentRelFiles(PACKAGE_ROOT);
  const destRelFiles = agentRelFiles(targetDir);
  const newManifest = {};
  const customizedFiles = [];
  let added = 0;
  let updated = 0;
  let unchanged = 0;

  // Snapshot .agent/ before touching anything, so a failure mid-update can be
  // rolled back instead of leaving the project in a half-updated state.
  const backupDir = fs.mkdtempSync(path.join(os.tmpdir(), "devbureau-backup-"));
  fs.cpSync(destAgentDir, backupDir, { recursive: true });

  try {
    for (const relPath of sourceRelFiles) {
      const sourceAbs = path.join(PACKAGE_ROOT, relPath);
      const destAbs = path.join(targetDir, relPath);
      const sourceHash = hashFile(sourceAbs);
      const destHash = hashFile(destAbs);

      if (destHash === null) {
        fs.mkdirSync(path.dirname(destAbs), { recursive: true });
        fs.copyFileSync(sourceAbs, destAbs);
        newManifest[relPath] = sourceHash;
        added++;
        continue;
      }

      if (destHash === sourceHash) {
        newManifest[relPath] = sourceHash;
        unchanged++;
        continue;
      }

      const baselineHash = previousManifest ? previousManifest[relPath] : null;
      const isCustomized = !force && baselineHash && baselineHash !== destHash;

      if (isCustomized) {
        newManifest[relPath] = baselineHash;
        customizedFiles.push(relPath);
        continue;
      }

      fs.copyFileSync(sourceAbs, destAbs);
      newManifest[relPath] = sourceHash;
      updated++;
    }
  } catch (err) {
    console.error(`\n✘ Update falhou (${err.message}) — restaurando .agent/ ao estado anterior...`);
    fs.cpSync(backupDir, destAgentDir, { recursive: true, force: true });
    fs.rmSync(backupDir, { recursive: true, force: true });
    console.error("✔ Restaurado. Nenhuma mudança foi persistida.");
    process.exitCode = 1;
    return;
  }

  fs.rmSync(backupDir, { recursive: true, force: true });
  saveManifest(targetDir, newManifest);
  saveVersionFile(targetDir, newVersion);

  const orphaned = destRelFiles.filter((relPath) => !sourceRelFiles.includes(relPath));

  console.log(`✔ Atualizados: ${updated}`);
  console.log(`✔ Adicionados: ${added}`);
  console.log(`ℹ Sem mudança: ${unchanged}`);
  if (customizedFiles.length > 0) {
    console.log(`⚠ Customizados, não sobrescritos (${customizedFiles.length}):`);
    for (const f of customizedFiles.slice(0, 20)) console.log(`    - ${f}`);
    if (customizedFiles.length > 20) console.log(`    ... e mais ${customizedFiles.length - 20}`);
    console.log("  Revise manualmente se quiser incorporar as melhorias do kit nesses arquivos.");
    console.log("  (Re-rode com --force se quiser sobrescrever mesmo assim — perde as suas edições.)");
  }
  if (orphaned.length > 0) {
    console.log(`ℹ Presentes localmente mas não mais no kit publicado (mantidos, nada foi apagado): ${orphaned.length}`);
  }

  if (previousVersion && previousVersion !== newVersion) {
    printChangelogSince(previousVersion, newVersion);
  }

  console.log("\n✅ Update concluído. Rode `python .agent/scripts/doctor.py` para validar.\n");
}

// Generated IDE files DevBureau fully owns end-to-end (their entire content
// comes from sync_ide.py, nothing else writes to them) — mirrors
// protect_generated_files.py's PROTECTED_FILES/PROTECTED_PREFIXES. Keep the
// two lists in sync if either changes.
const GENERATED_IDE_FILES = [
  ".claude/CLAUDE.md", "AGENTS.md", "GEMINI.md",
  ".github/copilot-instructions.md", ".windsurfrules", ".clinerules", ".roorules", ".rules",
];
const GENERATED_IDE_DIRS = [".cursor/rules", ".github/instructions"];

function removeEmptyDirsRecursive(dir) {
  if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) removeEmptyDirsRecursive(path.join(dir, entry.name));
  }
  if (fs.readdirSync(dir).length === 0) fs.rmdirSync(dir);
}

function uninstall(args) {
  const targetDir = process.cwd();
  const dryRun = args.includes("--dry-run");
  const destAgentDir = path.join(targetDir, ".agent");
  const verb = dryRun ? "Would remove" : "Removed";

  console.log(`\n🏛️  DevBureau — Uninstall${dryRun ? " [DRY-RUN]" : ""}\n`);

  if (!fs.existsSync(destAgentDir)) {
    console.error("✘ No .agent/ found in this directory — nothing to uninstall.");
    process.exitCode = 1;
    return;
  }

  const manifest = loadManifest(targetDir);
  if (!manifest) {
    console.log(
      "ℹ No manifest found (installed before `update` existed, or the manifest file was removed)."
    );
    console.log(
      "  Without it, DevBureau can't tell which files under .agent/ you customized. Nothing was removed."
    );
    console.log("  Remove .agent/ manually if you're sure, or run `update` first to rebuild a manifest.");
    return;
  }

  let removed = 0;
  const customized = [];

  for (const relPath of Object.keys(manifest)) {
    const absPath = path.join(targetDir, relPath);
    const currentHash = hashFile(absPath);
    if (currentHash === null) continue; // already gone
    if (currentHash !== manifest[relPath]) {
      customized.push(relPath);
      continue;
    }
    if (!dryRun) fs.rmSync(absPath, { force: true });
    removed++;
  }

  if (!dryRun) removeEmptyDirsRecursive(destAgentDir);

  let ideFilesRemoved = 0;
  for (const rel of GENERATED_IDE_FILES) {
    const abs = path.join(targetDir, rel);
    if (fs.existsSync(abs)) {
      if (!dryRun) fs.rmSync(abs, { force: true });
      ideFilesRemoved++;
    }
  }
  for (const rel of GENERATED_IDE_DIRS) {
    const abs = path.join(targetDir, rel);
    if (fs.existsSync(abs)) {
      if (!dryRun) fs.rmSync(abs, { recursive: true, force: true });
      ideFilesRemoved++;
    }
  }

  const manifestPath = path.join(targetDir, MANIFEST_FILENAME);
  if (!dryRun && fs.existsSync(manifestPath) && customized.length === 0) {
    fs.rmSync(manifestPath, { force: true });
  }
  const versionPath = path.join(targetDir, VERSION_FILENAME);
  if (!dryRun && fs.existsSync(versionPath) && customized.length === 0) {
    fs.rmSync(versionPath, { force: true });
  }

  console.log(`✔ ${verb}: ${removed} file(s) under .agent/`);
  console.log(`✔ ${verb}: ${ideFilesRemoved} generated IDE file(s)/folder(s)`);
  if (customized.length > 0) {
    console.log(`⚠ Left in place (customized, ${customized.length}):`);
    for (const f of customized.slice(0, 20)) console.log(`    - ${f}`);
    if (customized.length > 20) console.log(`    ... and ${customized.length - 20} more`);
    console.log("  (Re-run with --force on `update` first if you want these overwritten, then uninstall.)");
  }
  console.log(
    "ℹ Not touched: .mcp.json (can't verify if you customized it), .claude/settings.json " +
    "(merged file — only the hook entries are DevBureau's), and the git pre-commit hook " +
    "(.git/hooks/pre-commit). Remove these manually if you want them gone too."
  );

  console.log(
    dryRun
      ? "\nℹ Dry run only — nothing was removed. Re-run without --dry-run to apply.\n"
      : "\n✅ Uninstall complete.\n"
  );
}

function printUsage() {
  console.log(`
DevBureau CLI

Usage:
  npx devbureau init [--force] [--target=<${IDE_TARGETS.join("|")}>]
  npx devbureau update [--force]
  npx devbureau uninstall [--dry-run]

Commands:
  init        Copy .agent/ and a starter .mcp.json into the current directory,
              run the health check, install the pre-commit hook, and optionally
              sync IDE rules.
  update      Pull the latest .agent/ from the installed DevBureau version into
              this project. Files you customized are detected (via a SHA-256
              manifest) and never overwritten unless you pass --force.
  uninstall   Remove everything DevBureau installed (.agent/ files matching the
              manifest, generated IDE files). Customized files are left in
              place and reported. --dry-run shows the plan without deleting
              anything. .mcp.json, .claude/settings.json, and the git
              pre-commit hook are never touched automatically.
`);
}

async function main() {
  const [command, ...args] = process.argv.slice(2);

  if (!command || command === "init") {
    await init(args);
    return;
  }

  if (command === "update") {
    update(args);
    return;
  }

  if (command === "uninstall") {
    uninstall(args);
    return;
  }

  printUsage();
  process.exitCode = command === "--help" || command === "-h" ? 0 : 1;
}

main();
