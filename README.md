# DevBureau

**English** · [Português](README.pt-BR.md)

> A production-grade multi-agent AI framework for building software with professional quality —
> without needing to know how to code. Works across Claude Code, Cursor, Codex CLI, OpenCode,
> GitHub Copilot, Antigravity, Windsurf, Cline, Roo Code, and Zed.

[![Kit Version](https://img.shields.io/badge/DevBureau-v3.18.0-blue)](https://github.com/fernandotenguan/devbureau)
[![Agents](https://img.shields.io/badge/Agents-22-green)](https://github.com/fernandotenguan/devbureau)
[![Skills](https://img.shields.io/badge/Skills-64-orange)](https://github.com/fernandotenguan/devbureau)
[![Workflows](https://img.shields.io/badge/Workflows-21-red)](https://github.com/fernandotenguan/devbureau)
[![Tests](https://img.shields.io/badge/Tests-Automated-brightgreen)](https://github.com/fernandotenguan/devbureau)

> Badge links assume the repo is published as `fernandotenguan/devbureau`. Update them if the final published path differs.

---

## What's Included

| Components         | Count | Description                                                                  |
| ------------------ | ----- | ---------------------------------------------------------------------------- |
| **Agents**         | 22    | Specialist AI personas (frontend, backend, security, SRE, a11y, game dev, etc.) |
| **Skills**         | 64    | Domain-specific knowledge modules with automated scripts                     |
| **Workflows**      | 21    | Slash-command procedures including the autonomous `/ade` pipeline             |
| **Master Scripts** | 9     | `doctor.py`, `checklist.py`, `verify_all.py`, `sync_ide.py`, `auto_fixer.py`, `install_hooks.py`, `session_manager.py`, `auto_preview.py`, `token_footprint.py` |
| **Kit Tests**      | ✅    | Automated pytest suite — runs before every commit                            |
| **Memory Layer**   | ✅    | Persistent lessons and gotchas across sessions                               |
| **Hooks**          | 6     | Git pre-commit (all IDEs) + 5 Claude Code hooks: block edits to auto-generated files, block writes outside the current worktree, block `git --no-verify`/hooksPath bypass, advisory prompt-injection scan on Read/WebFetch/WebSearch, advisory `console.log` warning on edited JS/TS files |
| **MCP**            | 1     | Starter `.mcp.json` with the GitHub MCP server (OAuth, no token in the file) |

---

## Features

### 🤖 Intelligent Auto-Routing

Describe what you need in plain English. The kit detects the domain and applies the right specialist automatically — no commands required.

```
You: "The login button is not working"       → @debugger
You: "Make the UI look more modern"           → @frontend-specialist
You: "Is the app safe to deploy?"             → @security-auditor
You: "check kit" / "diagnose"                 → Health check (doctor.py)
```

### 🚀 Autonomous Development Pipeline (`/ade`)

The most powerful mode. You describe a feature, the kit plans it, shows you the spec, and waits for approval before writing any code.

```
/ade add email notification system
/ade create a sales dashboard with charts
/ade implement Google OAuth login
```

**6-phase pipeline:** Discovery → Spec → ✋ Your Approval → Code → QA → Memory

### 🏥 Kit Health Diagnostics

```bash
python .agent/scripts/doctor.py
```

Validates all 22 agents, 63 skills, 20 workflows, and master scripts in seconds.

### 🔒 Automated Pre-Commit Guard

Tests run automatically before every `git commit`. If anything breaks, the commit is blocked until fixed.

### 🧠 Persistent Memory Layer

The kit remembers patterns and lessons learned across sessions, stored in `.agent/memory/`.

### 🪶 Lean Code Ladder (Token Economy, Without Cutting Quality)

Every coding agent climbs a 7-rung decision ladder before writing code — YAGNI, then reuse, then stdlib, then native platform features, then an already-installed dependency, then one line, only then the minimum that works. It never cuts validation, error handling, security, or accessibility. Deliberate shortcuts get a `lean:` comment naming the ceiling and upgrade trigger, so "later" doesn't become "never":

```bash
/lean-audit          # find over-engineering to delete in the current diff
/lean-audit repo     # same, whole codebase
/lean-debt           # harvest every lean: marker into a ledger
python .agent/scripts/token_footprint.py   # measure the kit's own context footprint
```

### 🔭 Codebase Audit & Handoff Plans (`/audit`)

A senior-advisor survey, not a builder. Audits the codebase across nine categories (bugs, security, performance, tests, tech debt, dependencies, DX, docs, and direction — what to build next), re-reads every finding itself before showing it to you (subagents over-report), ranks by leverage (impact ÷ effort), and writes self-contained plans for a *different* agent or a future session to execute. It never edits source code — the plan is the product.

```bash
/audit                  # full survey, all 9 categories
/audit quick            # cheap pass, top findings only
/audit security         # one category, deeper
/audit next             # feature/direction suggestions only
```

Distinct from `/plan` (short, same-session plan) and `/ade` (plans and executes itself after approval) — `/audit` is for "survey now, hand off the work later."

### 🧬 Pattern Mining (`/mine-patterns`)

Some of the best engineering knowledge isn't in another AI-agent kit — it's in a finished, professional-grade project someone already built well. Point this at a reference repo (yours or anyone's, local path or git URL) and it extracts generalizable engineering patterns — architecture, error handling, testing strategy, config/secrets handling, tooling choices — never the project's business logic. Every pattern gets a confidence mark and a proposed landing spot (a new `lessons.md` entry or a named skill/agent), logged to `.agent/memory/pattern-mining-log.md` for your review. Nothing gets applied automatically.

```bash
/mine-patterns ../my-other-project
/mine-patterns https://github.com/some-org/well-built-service
```

Distinct from `/benchmark`, which compares DevBureau against other AI-agent kits — `/mine-patterns` studies regular software projects for engineering wisdom.

#### Optional: Headroom MCP (third-party, not bundled)

DevBureau's rules already say "use `mcp__headroom__*` tools if present" — but getting them present is a one-time, per-machine setup you do yourself, not something `npx devbureau init` installs:

```bash
pip install "headroom-ai[mcp]"
claude mcp add headroom --scope user -- headroom mcp serve
```

`--scope user` registers it once for every project you open in Claude Code afterward — no per-project setup, no proxy, no admin rights needed. Once connected, every agent in this kit will call `headroom_compress` on large tool outputs/file reads automatically, without you asking. If it's not installed, agents proceed normally — it's an accelerator, not a dependency.

#### Optional: AgentShield (third-party, not bundled)

`security-auditor` and `vulnerability-scanner` give you prose-guided, knowledge-driven review — useful for reasoning about a specific finding, but not a substitute for a deterministic scanner with a fixed, numbered rule set. [AgentShield](https://github.com/affaan-m/agentshield) (MIT, separately maintained) fills that gap: 102 static rules across secrets detection, permission auditing, hook injection analysis, MCP server risk profiling, and agent config review, graded A–F. No install needed for a one-off scan:

```bash
npx ecc-agentshield scan
```

Add `--fix` to auto-fix safe issues, or `--opus` for a deeper three-agent adversarial pass (attacker finds exploit chains, defender evaluates protections, auditor synthesizes a prioritized risk assessment). Exit code 2 on critical findings makes it usable as a CI gate. Like Headroom, this is documented here because it's a useful companion — DevBureau doesn't bundle or maintain it.

#### Optional: GateGuard (third-party, not bundled)

The Zero-Break Deployment Protocol's evidence table (above) is prompt discipline — it asks the agent to verify before claiming success, but nothing stops a model under load from skipping it. [GateGuard](https://github.com/zunoworks/gateguard) closes that gap at the tooling layer: a `PreToolUse` hook that blocks the first Edit/Write/Bash attempt on a risky change and forces the model to present concrete investigation facts (who imports this file, what's the schema, what's the rollback plan) before letting the retry through.

```bash
pip install gateguard-ai
gateguard init
```

`gateguard init` registers its hooks in `~/.claude/settings.json` (user scope) and writes a `.gateguard.yml` config — it doesn't touch DevBureau's own project-level hooks in `.claude/settings.json`, so the two run side by side without conflict.

### 💰 Token Optimization

`/ade`'s Execution phase already tiers models per subtask (cheap model for mechanical work, most-capable for architecture decisions). These `~/.claude/settings.json` values complement that at the session level:

```json
{
  "model": "sonnet",
  "env": {
    "MAX_THINKING_TOKENS": "10000",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50",
    "CLAUDE_CODE_SUBAGENT_MODEL": "haiku"
  }
}
```

| Setting | Effect |
| --- | --- |
| `"model": "sonnet"` | Default model for the main session — handles most coding tasks at a fraction of Opus's cost. Switch to Opus only for deep architectural reasoning. |
| `MAX_THINKING_TOKENS=10000` | Caps hidden thinking-token spend per request (default is much higher). |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50` | Compacts context earlier than the default 95% — better quality in long sessions instead of waiting until the window is nearly full. |
| `CLAUDE_CODE_SUBAGENT_MODEL=haiku` | Cheap default for dispatched subagents that don't need Sonnet/Opus-level reasoning — explicit per-subtask tiering in `/ade` still overrides this where it matters. |

### 🔄 Multi-IDE Sync

Export the kit configuration to Antigravity, Claude Code, Cursor, Codex CLI, OpenCode, GitHub Copilot, Windsurf, Cline, Roo Code, and Zed:

```bash
python .agent/scripts/sync_ide.py --target all
# or a single target: claude | cursor | codex | opencode | copilot | antigravity | windsurf | cline | roocode
```

> Codex CLI and OpenCode both read the same root `AGENTS.md` file directly — there's no separate file for OpenCode, so `--target codex` and `--target opencode` produce an identical result. Both names are accepted so either is discoverable.

## 🚀 Starting a New Project

This repository is your **development brain**. To bootstrap a new project (e.g. an e-commerce site, a mobile app) using this base:

1.  **Create your new project folder.**
2.  **In your agent's chat**, type:
    ```
    /new-project
    ```
3.  The agent guides you through copying `.agent/` (the kit's "soul") and the initial setup of your new application.

---

## 📜 Maintenance Rules

If you're maintaining DevBureau itself (not just consuming it in a downstream project), always follow:
[Maintenance & Evolution Rules (KIT_MASTER_RULES.md)](./KIT_MASTER_RULES.md)

---

## Installation

> **Requirements:** Python 3.9+ and Git

### Option 1 — NPX CLI (Recommended, fastest)

```bash
npx devbureau init
```

This copies the `.agent/` folder into your project, runs the health check (`doctor.py`), installs the pre-commit hook, and syncs the rules to your IDE. It auto-detects which IDE/engine is already in use in the project (Claude Code, Cursor, Codex, OpenCode, Antigravity, Copilot, Windsurf, Cline, Roo Code, Zed) and uses that as the default instead of asking blindly — you can still pick a different one or `--target=<ide>` explicitly.

Later, when you've customized agents/skills for this project and want to pull in DevBureau's latest improvements without losing your edits:

```bash
npx devbureau update
```

This compares your `.agent/` against the installed package version using a SHA-256 manifest — files you haven't touched get updated, files you customized are left alone and listed for manual review.

### Option 2 — NPX giget (no npm package needed)

Copy only the `.agent` folder directly from the GitHub repo:

```bash
npx giget@latest github:fernandotenguan/devbureau/.agent .agent --force
```

Then install the pre-commit hook so tests run automatically:

```bash
python .agent/scripts/install_hooks.py
```

### Option 3 — Git Clone

Clone the full repository and copy `.agent` into your project:

```bash
git clone https://github.com/fernandotenguan/devbureau.git
cd devbureau
# Copy .agent/ into your own project:
xcopy .agent "C:\path\to\your-project\.agent" /E /I    # Windows
# cp -r .agent /path/to/your-project/                  # Linux/macOS
```

### Verify Installation

```bash
python .agent/scripts/doctor.py
```

Expected output: `✅ All checks passed! Kit is healthy.`

---

## Setup in VSCode (with GitHub Copilot or Gemini Code Assist)

The kit works with any AI assistant in VSCode that can read workspace files. Here's how to get the best experience:

### Step 1 — Open the Project in VSCode

```bash
code .
```

Make sure your project has the `.agent/` folder at the root level.

### Step 2 — Configure the AI to Read the Kit

The kit's rules are stored in `.agent/rules/DEVBUREAU.md`. For the AI to follow them automatically:

**For GitHub Copilot (VSCode):**

Run the sync script to generate Copilot-optimized instruction files:

```bash
python .agent/scripts/sync_ide.py --target copilot
```

This creates `.github/copilot-instructions.md` (loaded automatically in every chat) and modular files in `.github/instructions/` (loaded contextually by file type).

Verify it's working: in Copilot Chat, check that the instruction files appear in the **References** list.

**For Antigravity (Google):**

Run the sync script to generate the root-level `GEMINI.md`, which Antigravity reads as the highest-priority workspace rules file:

```bash
python .agent/scripts/sync_ide.py --target antigravity
```

**For Gemini Code Assist (VSCode):**

The `GEMINI.md` rules are loaded automatically if the file is present in the workspace.

**For Cursor:**

Run the sync script to generate Cursor-specific rules:

```bash
python .agent/scripts/sync_ide.py --target cursor
```

This creates `.cursor/rules/` — 5 glob-scoped `.mdc` files (Cursor's current Project Rules format) instead of one monolithic file, so only the relevant rules load per file type.

**For Claude Code:**

```bash
python .agent/scripts/sync_ide.py --target claude
```

This creates `.claude/CLAUDE.md`.

**For Windsurf, Cline, Roo Code, or Zed:**

```bash
python .agent/scripts/sync_ide.py --target windsurf   # → .windsurfrules
python .agent/scripts/sync_ide.py --target cline       # → .clinerules
python .agent/scripts/sync_ide.py --target roocode     # → .roorules
python .agent/scripts/sync_ide.py --target zed         # → .rules
```

These three read one flat rules file (no glob-scoped splitting), so the generated file bundles everything: agent roster, code quality, frontend, backend, and security rules.

### Step 3 — Install Recommended VSCode Extensions

For the best development experience:

| Extension                         | Purpose                            |
| --------------------------------- | ---------------------------------- |
| `esbenp.prettier-vscode`          | Code formatting                    |
| `dbaeumer.vscode-eslint`          | Linting                            |
| `ms-python.python`                | Run `.agent/scripts/*.py` directly |
| `ms-vscode.vscode-github-copilot` | AI coding assistant                |
| `github.copilot-chat`             | Chat interface for agent commands  |

### Step 4 — Run the Kit Health Check from VSCode

1. Open the integrated terminal: `` Ctrl+` ``
2. Run:

```bash
python .agent/scripts/doctor.py
```

### Step 5 — Using Slash Commands in VSCode Chat

In the Copilot chat panel, type any slash command:

```
/ade add a dark mode toggle to the app
/debug why does the form not submit
/build-saas subscription platform for freelancers
```

---

## Slash Commands Reference

| Command          | Purpose                                               |
| ---------------- | ----------------------------------------------------- |
| `/ade`           | **Autonomous pipeline** — full feature end-to-end     |
| `/audit`         | Senior-advisor survey — vetted, leverage-ranked findings, self-contained handoff plans |
| `/build-saas`    | Plan a complete SaaS in 7 guided steps                |
| `/plan`          | Create a detailed plan without writing code yet       |
| `/create`        | Scaffold a new feature or application                 |
| `/brainstorm`    | Explore options with strategic questions              |
| `/enhance`       | Improve an existing feature                           |
| `/finish-branch` | Structured close-out (merge/PR/keep/discard) once work is done |
| `/lean-audit`    | Find over-engineering to delete (diff or whole-repo scope) |
| `/lean-debt`     | Harvest `lean:` shortcut markers into a debt ledger    |
| `/mine-patterns` | Mine a reference project for engineering patterns, log Adopt/Consider/Skip recommendations (no auto-apply) |
| `/debug`         | Systematic bug investigation                          |
| `/test`          | Generate and run tests                                |
| `/deploy`        | Pre-flight checks + guided deployment                 |
| `/preview`       | Start local dev server                                |
| `/status`        | Check project progress                                |
| `/ui-ux-pro-max` | Premium UI/UX design in 50 styles                     |
| `/clean`         | **Auto-fix & optimize** code (selective path support) |
| `/orchestrate`   | Coordinate multiple agents for complex tasks          |

---

## Validation & Quality Scripts

```bash
# Kit health check (run first, always)
python .agent/scripts/doctor.py

# Auto-fix & format code (selective paths supported)
python .agent/scripts/auto_fixer.py src/   # Cleaner for a specific folder

# Full project audit (security, lint, UX, SEO)
python .agent/scripts/checklist.py .

# Full verification before deployment
python .agent/scripts/verify_all.py . --url http://localhost:3000

# Sync kit to other IDEs (Antigravity, Claude, Cursor, Codex, OpenCode, Copilot, Windsurf, Cline, Roo Code, Zed)
python .agent/scripts/sync_ide.py --target all

# Measure the kit's own context footprint (approx. tokens in generated rule files)
python .agent/scripts/token_footprint.py
```

---

## How It Works

```
User request
    │
    ▼
[DEVBUREAU.md Rules]      ← P0: global rules, anti-hallucination, clean code
    │
    ▼
[Intelligent Routing]     ← auto-detects domain from request
    │
    ▼
[Agent Selected]          ← @frontend-specialist, @debugger, @security-auditor...
    │
    ▼
[Skills Loaded]           ← domain knowledge specific to the task
    │
    ▼
[Output + Verification]   ← zero-break protocol, tests run
    │
    ▼
[Memory Updated]          ← lessons.md + gotchas.md
```

### Architecture Diagrams

<p align="center">
  <img src="docs/diagrams/devbureau-architecture.drawio.png" alt="DevBureau macro architecture: request through DEVBUREAU.md rules, intelligent routing, the four catalogs, verification, and memory" width="720" />
</p>

> Macro view: request → DEVBUREAU.md rules → intelligent routing → the 4 catalogs (agents/skills/workflows/scripts) → output verification → memory.

<p align="center">
  <img src="docs/diagrams/ade-pipeline.drawio.png" alt="The /ade 6-phase autonomous pipeline, including the Fase 3 approval gate and the Fase 5 QA retry loop" width="600" />
</p>

> The `/ade` 6-phase pipeline: Discovery → Spec → ✋ approval gate → Execution → QA (retries into `@debugger` on failure) → Memory.

Both diagrams are editable `.drawio` XML (embedded in the `.png` itself) — see [docs/diagrams/README.md](./docs/diagrams/README.md) for provenance and how to regenerate them.

---

## Project Structure

```
project-root/
├── .agent/
│   ├── agents/          # 22 specialist AI personas
│   ├── skills/          # 63 knowledge modules
│   ├── workflows/       # 20 slash-command procedures
│   ├── scripts/         # master validation scripts
│   │   ├── doctor.py          # kit health check
│   │   ├── checklist.py       # priority-based audit
│   │   ├── verify_all.py      # full verification suite
│   │   ├── sync_ide.py        # multi-IDE export
│   │   ├── install_hooks.py   # git hook installer
│   │   └── hooks/
│   │       ├── protect_generated_files.py  # blocks edits to auto-generated files
│   │       ├── guard_worktree_path.py      # blocks writes outside the worktree
│   │       └── scan_injection.py           # advisory prompt-injection scan
│   ├── tests/
│   │   └── test_kit_integrity.py  # automated pytest suite
│   ├── memory/
│   │   ├── lessons.md   # patterns that worked well
│   │   └── gotchas.md   # common pitfalls to avoid
│   └── rules/
│       └── DEVBUREAU.md # master rules file (P0)
├── .mcp.json             # starter MCP config (GitHub, OAuth)
└── README.md
```

---

## Support the Project

If this kit saves you time, consider supporting:

<p align="center">
  <img src="pix-fernando.png" alt="PIX QR Code" width="180" />
</p>

**PIX key:** `fernando.tenguan@gmail.com`

---

## License

MIT — see [LICENSE](./LICENSE)

---

> _Build smarter. Ship faster. With confidence._
