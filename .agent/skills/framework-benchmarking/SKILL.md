---
name: framework-benchmarking
description: Process for periodically comparing DevBureau's agents/skills/workflows against well-regarded external agent-framework collections (Claude Code subagent catalogs, awesome-skills lists, BMAD-METHOD, etc.), scoring gaps, and deciding what to adopt, consider, or skip. Use when running the `/benchmark` workflow, or when evaluating whether a newly-discovered framework/skill collection is worth pulling ideas from. Triggers on "compare with other frameworks", "o que tem de novo no mercado", "vale a pena importar isso".
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# Framework Benchmarking

> **The goal is not to copy the biggest catalog — it's to find what makes DevBureau more useful without violating its own principles (tiered stack sizing, lean roster, works across every IDE).**

A bigger number of agents/skills is not automatically better. BMAD-METHOD ships 50+ workflows; DevBureau deliberately stays leaner because its audience includes non-programmers who'd drown in that many menus. Benchmarking is about finding gaps and validated decisions, not maximizing catalog size.

---

## ⚠️ Core Principle

- Never adopt something just because a bigger repo has it. Ask: does this fill a real gap, or does it duplicate/conflict with what already exists?
- Check source credibility before trusting a claim: stars, last commit date, whether it's officially maintained (Anthropic/Google/Cursor) vs. community.
- Every finding gets one of three verdicts — **Adopt**, **Consider**, **Skip** — with a one-line reason. No silent "maybe later" pile.
- This skill never auto-applies changes. It produces a report; a human (or a separate implementation task, after explicit go-ahead) decides what ships.

---

## 1. Known Sources (Watch List)

Keep this list current in `references/sources.md` — update it whenever a run discovers a new credible source. As of the last run, it covers:

| Source | What it's good for | Credibility signal (at last check) |
|---|---|---|
| `bmad-code-org/BMAD-METHOD` | Scale-adaptive planning methodology, agent persona design | Active, official org repo |
| `hesreallyhim/awesome-claude-code` | Hand-curated, broadest community signal | 36.8k+ stars, canonical list |
| `VoltAgent/awesome-claude-code-subagents` | Subagent catalog by category | 154+ agents, 10 categories |
| `VoltAgent/awesome-agent-skills` | Cross-tool skill catalog (Claude Code, Codex, Gemini CLI, Cursor, Antigravity) | 1000+ skills |
| `sickn33/antigravity-awesome-skills` | Skills + installer CLI, multi-tool (this is DevBureau's own stated import source per CHANGELOG v2.2.0) | 1,600+ skills, active installer |
| `rohitg00/awesome-claude-code-toolkit` | Breadth check: hooks, MCP configs, plugins — categories DevBureau under-covers | 135 agents, 20 hooks, 14 MCP configs |

---

## 2. Run Protocol

### Step 1: Refresh source state
For each source in the watch list, `WebSearch`/`WebFetch` to confirm it's still maintained and check what's changed since the last logged run (see `.agent/memory/benchmark-log.md` for the last run's date and findings — don't re-derive what's already known).

### Step 2: Structural comparison
Compare against DevBureau's real current state (get it from `python .agent/scripts/doctor.py`, not from memory):

| Dimension | How to check |
|---|---|
| Agent count/categories | `.agent/agents/*.md` vs. the source's agent catalog |
| Skill count/categories | `.agent/skills/*/SKILL.md` vs. the source's skill catalog |
| Multi-IDE support | `sync_ide.py`'s `TARGETS` dict vs. what the source installs to |
| Hooks | DevBureau has 1 (git pre-commit). Most toolkits ship several (lint-before-commit, block-edits-outside-src, security-scan-after-dep-change) |
| MCP configs | DevBureau has none bundled (only `mcp-builder`, which teaches building one). Toolkits often ship ready `.mcp.json` examples |
| Rules file format | Confirm DevBureau's generated format still matches current best practice for each IDE (e.g., Cursor moved from a single `.cursorrules`/`rules.md` to a `.cursor/rules/` directory with glob-scoped files) |

### Step 3: Score each gap
For every difference found, assign:

- **Adopt** — clear value, no conflict with `stack-sizing` tiers or the lean-roster philosophy, low implementation cost. Goes straight into a follow-up task.
- **Consider** — valuable but needs adaptation, a design decision, or carries some risk/cost. Needs a human decision before implementing.
- **Skip** — duplicates something DevBureau already has, conflicts with a tier philosophy (e.g., "50 workflows" for a kit aimed at non-programmers), or the source isn't credible enough to trust.

### Step 4: Log and report
Append a dated entry to `.agent/memory/benchmark-log.md` (date, sources checked, findings with verdicts). This is the persistent record so the next run starts from "what's new since X" instead of redoing everything.

---

## 3. Anti-Patterns

- Importing a skill/agent without checking it doesn't already exist under a different name (causes the kind of redundancy already found between `product-manager`/`product-owner` before they were merged).
- Treating "more agents" as inherently better — DevBureau's positioning is a lean, coherent team, not the biggest catalog.
- Re-running full research from scratch every time instead of diffing against the last logged run.
- Auto-implementing a finding without a human go-ahead — this skill produces recommendations, not commits.
