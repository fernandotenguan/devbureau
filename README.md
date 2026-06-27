# DevBureau

> A production-grade multi-agent AI framework for building software with professional quality —
> without needing to know how to code. Works across Claude Code, Cursor, Codex CLI, GitHub Copilot,
> Antigravity, Windsurf, Cline, and Roo Code.

[![Kit Version](https://img.shields.io/badge/DevBureau-v3.0.0-blue)](https://github.com/fernandotenguan/devbureau)
[![Agents](https://img.shields.io/badge/Agents-22-green)](https://github.com/fernandotenguan/devbureau)
[![Skills](https://img.shields.io/badge/Skills-62-orange)](https://github.com/fernandotenguan/devbureau)
[![Workflows](https://img.shields.io/badge/Workflows-20-red)](https://github.com/fernandotenguan/devbureau)
[![Tests](https://img.shields.io/badge/Tests-Automated-brightgreen)](https://github.com/fernandotenguan/devbureau)

> Badge links assume the repo is published as `fernandotenguan/devbureau`. Update them if the final published path differs.

---

## What's Included

| Components         | Count | Description                                                                  |
| ------------------ | ----- | ---------------------------------------------------------------------------- |
| **Agents**         | 22    | Specialist AI personas (frontend, backend, security, SRE, a11y, game dev, etc.) |
| **Skills**         | 62    | Domain-specific knowledge modules with automated scripts                     |
| **Workflows**      | 20    | Slash-command procedures including the autonomous `/ade` pipeline             |
| **Master Scripts** | 5     | `doctor.py`, `checklist.py`, `verify_all.py`, `sync_ide.py`, `auto_fixer.py` |
| **Kit Tests**      | ✅    | Automated pytest suite — runs before every commit                            |
| **Memory Layer**   | ✅    | Persistent lessons and gotchas across sessions                               |
| **Hooks**          | 2     | Git pre-commit (all IDEs) + a Claude Code `PreToolUse` hook that blocks edits to auto-generated files |
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

Validates all 22 agents, 62 skills, 20 workflows, and master scripts in seconds.

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

#### Optional: Headroom MCP (third-party, not bundled)

DevBureau's rules already say "use `mcp__headroom__*` tools if present" — but getting them present is a one-time, per-machine setup you do yourself, not something `npx devbureau init` installs:

```bash
pip install "headroom-ai[mcp]"
claude mcp add headroom --scope user -- headroom mcp serve
```

`--scope user` registers it once for every project you open in Claude Code afterward — no per-project setup, no proxy, no admin rights needed. Once connected, every agent in this kit will call `headroom_compress` on large tool outputs/file reads automatically, without you asking. If it's not installed, agents proceed normally — it's an accelerator, not a dependency.

### 🔄 Multi-IDE Sync

Export the kit configuration to Antigravity, Claude Code, Cursor, Codex CLI, GitHub Copilot, Windsurf, Cline, and Roo Code:

```bash
python .agent/scripts/sync_ide.py --target all
# or a single target: claude | cursor | codex | copilot | antigravity | windsurf | cline | roocode
```

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

## What's Included

> **Requirements:** Python 3.9+ and Git

### Option 1 — NPX CLI (Recommended, fastest)

```bash
npx devbureau init
```

This copies the `.agent/` folder into your project, runs the health check (`doctor.py`), installs the pre-commit hook, and syncs the rules to your IDE. It auto-detects which IDE/engine is already in use in the project (Claude Code, Cursor, Codex, Antigravity, Copilot, Windsurf, Cline, Roo Code) and uses that as the default instead of asking blindly — you can still pick a different one or `--target=<ide>` explicitly.

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

The kit's rules are stored in `.agent/rules/GEMINI.md`. For the AI to follow them automatically:

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

**For Windsurf, Cline, or Roo Code:**

```bash
python .agent/scripts/sync_ide.py --target windsurf   # → .windsurfrules
python .agent/scripts/sync_ide.py --target cline       # → .clinerules
python .agent/scripts/sync_ide.py --target roocode     # → .roorules
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

# Sync kit to other IDEs (Antigravity, Claude, Cursor, Codex, Copilot, Windsurf, Cline, Roo Code)
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
[GEMINI.md Rules]         ← P0: global rules, anti-hallucination, clean code
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

---

## Project Structure

```
project-root/
├── .agent/
│   ├── agents/          # 22 specialist AI personas
│   ├── skills/          # 62 knowledge modules
│   ├── workflows/       # 20 slash-command procedures
│   ├── scripts/         # master validation scripts
│   │   ├── doctor.py          # kit health check
│   │   ├── checklist.py       # priority-based audit
│   │   ├── verify_all.py      # full verification suite
│   │   ├── sync_ide.py        # multi-IDE export
│   │   ├── install_hooks.py   # git hook installer
│   │   └── hooks/
│   │       └── protect_generated_files.py  # Claude Code PreToolUse hook
│   ├── tests/
│   │   └── test_kit_integrity.py  # automated pytest suite
│   ├── memory/
│   │   ├── lessons.md   # patterns that worked well
│   │   └── gotchas.md   # common pitfalls to avoid
│   └── rules/
│       └── GEMINI.md    # master rules file (P0)
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
