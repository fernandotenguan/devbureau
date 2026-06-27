# Benchmark Log — DevBureau

> Dated record of `/benchmark` runs. Always read the most recent entry before starting a new run — diff against it, don't re-research from scratch. Full rubric in `.agent/skills/framework-benchmarking/SKILL.md`.

---

## Formato de entrada

```markdown
## YYYY-MM-DD — Benchmark Run
**Sources checked:** lista de fontes consultadas
**Findings:** tabela achado → veredito → razão
**Adopt (ready for follow-up):** itens prontos para virar tarefa
**Consider (needs a decision):** itens que precisam de decisão do usuário
**Skip:** itens descartados e por quê
```

---

## 2026-06-26 — Benchmark Run

**Sources checked:** `bmad-code-org/BMAD-METHOD`, `hesreallyhim/awesome-claude-code`, `VoltAgent/awesome-claude-code-subagents`, `VoltAgent/awesome-agent-skills`, `sickn33/antigravity-awesome-skills`, `rohitg00/awesome-claude-code-toolkit`, plus general 2026 best-practice sources for Cursor rules and Claude Code hooks/MCP.

**DevBureau state at time of run (per `doctor.py`):** 22 agents, 53 skills, 15 workflows, 8 master scripts.

### Findings

| Finding | Verdict | Reason |
|---|---|---|
| BMAD-METHOD's "scale-adaptive" planning (5-min Quick Flow → 30-min Enterprise track) | **Validated, no action** | This is conceptually what `stack-sizing` (added in this same work cycle) already does. No gap — confirms the approach rather than exposing one. |
| BMAD-METHOD's 50+ guided workflows | **Skip** | DevBureau's audience includes non-programmers; 15 focused workflows is the right size. More menus would hurt the "qualquer pessoa consegue usar" goal, not help it. |
| BMAD's "Party Mode" (multiple personas live in one session) | **Consider** | Interesting UX idea, but `orchestrator.md`'s sequential invocation already covers the substance (multiple specialists per task). Would need a concrete use case before building it. |
| `sickn33/antigravity-awesome-skills` installer (`npx antigravity-awesome-skills --cursor --claude --antigravity`) | **Validated, no action** | Confirms the `npx devbureau init` CLI direction (built in P0) is the right shape. DevBureau's CLI is narrower (one kit, not a skill marketplace) by design. |
| `antigravity-awesome-skills` categories (data/AI, more DevOps depth) | **Consider** | Re-check on a future run whether it has new skills covering gaps DevBureau still has (e.g., deeper data-engineering coverage beyond `machine-learning-ops-ml-pipeline`). Not urgent. |
| Cursor 2026 best practice: `.cursor/rules/` directory with glob-scoped files, replacing a single monolithic `.cursorrules`/`rules.md` | **Adopt** | `sync_ide.py`'s `generate_cursor_config()` still writes one big `.cursor/rules.md`. Conditional, file-scoped loading is now the documented best practice — same modular pattern DevBureau already uses for GitHub Copilot's `.github/instructions/`. Low-risk, clear improvement. |
| Claude Code 2026 guidance: hooks are the place for deterministic enforcement (e.g., "block writes outside src/") | **Consider** | DevBureau's "Agent Boundary Enforcement" tables in `orchestrator.md` are prose only — nothing actually blocks a misrouted file write. A real hook would need careful scoping/testing against Claude Code's hook event types; flagging for a dedicated task rather than rushing it. |
| No bundled `.mcp.json` starter config | **Consider** | DevBureau has `mcp-builder` (how to build an MCP server) but ships no ready server config. Needs the user's input on which integrations matter (GitHub, filesystem, etc.) before adding one — not a unilateral decision. |
| `awesome-claude-code-toolkit`'s hook/MCP counts (20 hooks, 14 MCP configs) vs. DevBureau's 1 hook, 0 MCP configs | **Consider** | Same root issue as the two items above — hooks/MCP is DevBureau's thinnest area relative to comparable toolkits. Worth a dedicated future pass, not a single-line fix. |

### Adopt (ready for follow-up)
1. ~~Upgrade `sync_ide.py`'s Cursor target to generate `.cursor/rules/` (multiple glob-scoped files) instead of one `.cursor/rules.md`.~~ **Done 2026-06-26** — see CHANGELOG v3.4.0. Also refactored the 4 shared rule bodies (code-quality, frontend, backend, security) into standalone functions reused by both the Copilot and Cursor targets, removing ~300 lines of duplication.

### Consider (needs a decision)
1. ~~Real hook-based enforcement (currently prose-only).~~ **Partially done 2026-06-26** — see CHANGELOG v3.5.0. Implemented for Claude Code (`protect_generated_files.py`, blocks edits to auto-generated files, not the broader agent-boundary table — that one isn't deterministically checkable, see below). Skipped for Cursor: its hook API has no pre-write blocking event yet (`afterFileEdit` is after-the-fact only).
2. ~~A starter `.mcp.json` with a small set of MCP servers.~~ **Done 2026-06-26** — see CHANGELOG v3.6.0. User chose GitHub only (remote/OAuth, no token in the file); Playwright and Postgres were offered and declined for now. `npx devbureau init` propagates it to new projects.

### New Finding (2026-06-26, surfaced while implementing #1)
The broader "Agent Boundary Enforcement" table in `orchestrator.md` (e.g. "frontend-specialist CANNOT touch test files") cannot be enforced the same way as the generated-files hook. A `PreToolUse` hook sees the file path being written, but has no reliable signal for "which persona is currently narrating" — that's a prompt-level role-play concept, not something exposed to hooks. Enforcing it deterministically would need a different mechanism (e.g. one Claude Code session per subagent with its own restricted tool permissions, rather than one session narrating multiple personas). **Verdict: Skip for now** — flagging honestly rather than building a hook that looks like enforcement but isn't.
3. Re-check `antigravity-awesome-skills` on a future run for new data/AI or DevOps skills worth importing.
4. BMAD's "Party Mode" — revisit only if a concrete multi-persona-in-one-session use case comes up.

### Skip
1. Matching BMAD's 50+ workflow count — conflicts with DevBureau's lean, non-programmer-friendly positioning.

---

## 2026-06-26 — Benchmark Run #2 (single-source deep dive, user-requested)

**Source checked:** `sandeco/reversa` (github.com/sandeco/reversa), full clone + read, not just README. arXiv paper-backed (Macedo & da Costa, May 2026). Scope: reverse-engineers legacy code into executable specs (SDD), then offers forward/migrate/price/docs pipelines on top.

**DevBureau state at time of run (per `doctor.py`):** 22 agents, 54 skills, 16 workflows, 8 master scripts.

**Scope note:** Reversa's overall product (legacy-to-spec extraction) does not match DevBureau's broader scope (build + maintain systems of any tier). Verdict on wholesale adoption: **Skip** — cherry-pick mechanisms instead, listed below.

### Findings

| Finding | Verdict | Reason |
|---|---|---|
| Confidence-scale fact marking (🟢 CONFIRMED / 🟡 INFERRED / 🔴 GAP) on every claim a "reading" agent makes about existing code | **Adopt** | Directly closes a real gap: `code-archaeologist`, `debugger`, and `security-auditor` all assert facts about code they're analyzing, with no signal for "this is verified vs. guessed." Cheap to add (a shared note in the agent files), high trust payoff, zero conflict with stack-sizing or lean-roster philosophy. |
| 13 supported IDE/engine targets (incl. Windsurf, Cline, Roo Code) vs. DevBureau's 5 | **Adopt** | `sync_ide.py`'s architecture already factors rule-bodies into shared functions — adding `.windsurfrules`/`.clinerules`/`.roorules` targets is the same pattern as Copilot/Cursor, low marginal cost, clear reach increase. |
| Installer auto-detects which IDE/engine is present (`.cursor/`, `.claude/`, CLI binaries via `which`/`where`) instead of always asking | **Adopt** | Improves UX for the non-technical persona specifically — fewer questions, smarter defaults. `bin/devbureau.js`'s `promptIdeTarget()` can pre-select a detected target instead of defaulting to "skip." |
| `reversa status` / `update` / `add-agent` / `add-engine` / `uninstall` CLI commands vs. DevBureau's `init`-only CLI | **Consider** | Real gap — DevBureau has no way to update an already-installed kit except `--force` (blunt full overwrite) or manual re-sync. Needs a design decision before building (see below), not a one-line fix. |
| SHA-256 manifest (`files-manifest.json`) that detects user-modified files and never overwrites them on update | **Consider** | Would let `devbureau update` safely pull upstream kit improvements into a project where the user customized `.agent/agents/*.md` or skills, without clobbering their edits. Philosophically in tension with the hook-based "don't edit generated files, edit the source" model already shipped (v3.5.0) — that one's about IDE-native rule files (always regenerated, never user-owned), this one's about `.agent/` source files themselves (which users *do* customize per-project). The two don't conflict, but combining them needs a clear line drawn between "always regenerated" and "yours to customize, hash-tracked." |
| Explicit `CONTINUAR` pause between every agent handoff in a pipeline, not just before starting | **Consider** | More control/trust, but adds friction — tension with `orchestrator.md`'s Phase 0 "Don't over-ask" rule and the non-technical persona's preference for low ceremony. Worth testing only inside `/ade`'s already-gated pipeline, not as a global default. |
| Pricing/effort-estimation agents on top of a finished plan (`reversa-pricing-profile/size/estimate`) | **Consider** | Strong fit for DevBureau's stated business-user audience (CLAUDE.md: "business-minded professional, not a developer") — translating a technical plan into effort/cost is exactly the kind of business-facing output this persona needs. Needs a decision on methodology (story points vs. hours vs. tier-based heuristic) and which agent owns it (`product-manager` vs. `project-planner`). |
| Migration-strategy decision skill (Strangler Fig / Big Bang / Parallel Run / Branch by Abstraction) for rebuilding legacy on a modern stack | **Consider** | DevBureau has `code-archaeologist` (reads legacy) but nothing that recommends *how* to migrate it. Relevant only if "modernize an existing system" is an actual use case for DevBureau's users, not just greenfield builds — needs that confirmed before building. |
| Durable `principles.md` (project constitution, rarely changes) with impact-report-not-auto-rewrite propagation when a principle changes | **Consider** | DevBureau's memory layer (`lessons.md`/`gotchas.md`) is reactive/learned; this is proactive/declared. Could enrich `plan-writing`, but risks duplicating `KIT_MASTER_RULES.md`'s role — needs a decision on where the line is before adding a new file type. |
| Disk-persisted pipeline state (`.reversa/state.json`, phase tracking, "physical stage detection" by inspecting artifacts on disk rather than trusting metadata) for resuming an interrupted multi-phase run | **Consider** | DevBureau's `{task-slug}.md` plan files partially serve this already (written progress survives context loss), but there's no single canonical "what phase are we in" object the orchestrator reads on resume. Worth checking whether real interrupted-session pain has come up before building a new state file. |
| Full offline HTML documentation mini-site (Three.js Code City, D3 force-directed graphs, Highcharts treemaps/sankeys, generative cover seal) | **Skip** | High build cost, niche (legacy-analysis reporting, not shipped product UI), and DevBureau's existing premium-design skills already target real product UI — building a second, parallel visualization stack for internal docs doesn't fit the lean-roster principle. |
| N8N workflow-to-spec translator agent | **Skip** | Too niche for DevBureau's general-purpose positioning unless a specific project needs n8n migration. |
| Wholesale adoption of Reversa's pipeline architecture (Discovery → Forward/Migrate/Docs/Pricing) | **Skip** | Scope mismatch — Reversa's whole product is "legacy → spec," DevBureau's scope is broader (build new + maintain existing, sized by tier). The individual mechanisms above are worth mining; the architecture as a whole is not. |

### Adopt (ready for follow-up)
1. ~~Confidence-scale fact marking (🟢/🟡/🔴) for `code-archaeologist`, `debugger`, `security-auditor` when asserting facts about analyzed code.~~ **Done 2026-06-26** — see CHANGELOG v3.7.0. New `confidence-scale` skill.
2. ~~Three new `sync_ide.py` targets: Windsurf (`.windsurfrules`), Cline (`.clinerules`), Roo Code (`.roorules`) — reusing the existing shared rule-body functions.~~ **Done 2026-06-26** — see CHANGELOG v3.7.0.
3. ~~Engine auto-detection in `bin/devbureau.js`'s `init` flow, replacing the blind IDE prompt with a smart default.~~ **Done 2026-06-26** — see CHANGELOG v3.7.0.

### Consider (needs a decision)
1. ~~`devbureau update` CLI command, backed by a SHA-256 manifest for safe partial updates.~~ **Done 2026-06-26** — see CHANGELOG v3.7.0. User confirmed this as a real need. Scoped to `.agent/` only (the hook-protected IDE-native rule files remain a separate, always-regenerated mechanism). `status` was not requested and not built — revisit if asked for separately.
2. Mid-pipeline `CONTINUAR`-style checkpoints inside `/ade` specifically (not globally). **Still open** — not part of the user's confirmed real-use-case list this round.
3. ~~Pricing/effort-estimation skill.~~ **Done 2026-06-26** — see CHANGELOG v3.7.0. User confirmed this as a real need. New `effort-estimation` skill: tier-aware day ranges, no invented pricing.
4. ~~Migration-strategy decision skill.~~ **Done 2026-06-26** — see CHANGELOG v3.7.0. User confirmed legacy modernization is an in-scope use case. New `migration-strategy` skill.
5. Durable `principles.md` with impact-report propagation. **Still open** — not part of the user's confirmed real-use-case list this round; risk of overlap with `KIT_MASTER_RULES.md` still unresolved.
6. Disk-persisted pipeline state for resuming interrupted multi-phase runs. **Still open** — not part of the user's confirmed real-use-case list this round.

### Skip
1. Full offline HTML documentation mini-site (Three.js/D3/Highcharts) — niche, high cost, duplicates premium-design's purpose for the wrong audience.
2. N8N translator agent — too niche.
3. Wholesale pipeline-architecture adoption — scope mismatch with DevBureau's broader build-and-maintain positioning.

---

## 2026-06-26 — Benchmark Run #3 (token-economy deep dive, user-requested)

**Sources checked:** `DietrichGebert/ponytail` (markdown skills/rules, 16 agent hosts) and `headroomlabs-ai/headroom` (Rust+Python runtime context-compression proxy). User asked specifically: what can make DevBureau more token-efficient without losing code quality.

**DevBureau state at time of run (per `doctor.py`):** 22 agents, 57 skills, 16 workflows.

**Key structural finding:** the two sources operate at different layers, which changes what's portable.
- Ponytail is the same architecture class as DevBureau — plain markdown skills/rules synced into the same kind of IDE hosts (Claude, Cursor, Codex, Copilot, Windsurf, Cline, Gemini, Antigravity). Its mechanisms transplant directly.
- Headroom is a network proxy/library (Rust core, Python bindings) that intercepts raw HTTP traffic to the LLM provider and compresses it (AST code compression, KV-cache alignment, cross-agent memory store, an MCP server). DevBureau ships markdown that the *host* IDE loads — it has no running process and no access to the request stream. Most of Headroom's actual mechanism cannot be replicated by a rules file; only the underlying *idea* (verbosity costs real money) transfers, not the technique.

### Findings

| Finding | Verdict | Reason |
|---|---|---|
| Ponytail's 7-rung "lazy ladder" (YAGNI → reuse existing code → stdlib → native platform feature → already-installed dependency → one-liner → minimum that works), run *after* understanding the problem, never *instead of* | **Adopt** | Directly reduces code-as-output tokens (their agentic benchmark: -54% LOC, -22% tokens, -20% cost, -27% time, 100% safety retained) without sacrificing quality — it explicitly protects trust-boundary validation, error handling, security, and accessibility, which matches DevBureau's own Code Quality Standards rather than conflicting with them. DevBureau's `clean-code` skill currently states *style* rules (naming, function size) but has no decision procedure for *whether to build something at all* or *reach for a dependency vs. stdlib* — this fills that gap. |
| Output discipline: code first, then ≤3 short lines (what was skipped, when to revisit), no essays explaining a simplification, full explanation only when explicitly asked | **Adopt** | This is the single highest-leverage lever available: output tokens cost ~5x input on Opus-class models (Headroom's own stated rationale), and DevBureau's GEMINI.md TIER 0 currently only enforces terse-output discipline inside the personal PT-BR "Gabarito" section, not as a universal, language-agnostic baseline for every agent regardless of language. Adding it at the universal level (not the personal layer) benefits every user of the published kit, not just this workspace. |
| `ponytail:` deliberate-shortcut comment convention (names the ceiling + upgrade trigger) plus a one-shot debt-ledger command that greps for the marker and reports anything with no named trigger | **Adopt** | DevBureau has no convention for marking "this is intentionally minimal, here's when to revisit" — shortcuts currently either don't get taken (over-engineering by default caution) or get taken silently (real debt with no trail). This closes that gap cheaply: a comment convention + one grep-based report skill, no new infrastructure. |
| Ponytail's `/ponytail-review` (diff-scope) and `/ponytail-audit` (repo-scope) over-engineering finder, tagged `delete:`/`stdlib:`/`native:`/`yagni:`/`shrink:`, explicitly out of scope for correctness/security (routes those to a normal review) | **Adopt** | Concrete, low-cost, clean separation of concerns from DevBureau's existing security/lint scripts — this is a complexity-only lens nothing in the current catalog provides. |
| Ponytail's `lite`/`full`/`ultra` intensity levels | **Consider** | Useful dial, but DevBureau already has a tier system (`stack-sizing`) that arguably implies the same thing — a Prototype-tier project should already default to something close to "ultra," Enterprise/Critical to something closer to "lite" (less code-golf, more explicit rigor for compliance/audit trails). Needs a decision: a separate dial, or fold laziness intensity as a property of the existing tier instead of adding a second axis. |
| Headroom's runtime context-compression proxy (AST code compression, KV-cache alignment, cross-agent memory store, MCP compress/retrieve/stats tools, "headroom learn" mining failed sessions into `CLAUDE.md` corrections) | **Skip (mechanism)** | Requires a running process intercepting the LLM request stream — a completely different product (network proxy/library) from what DevBureau is (a synced markdown ruleset consumed by the host IDE's own agent). Building this would mean DevBureau ships and maintains a Rust/Python proxy, well outside current scope and distribution model (`npx devbureau init`). The underlying *idea* (verbosity reduction matters) is already captured by the two Adopt items above without needing the infrastructure. |
| Headroom's benchmark-everything culture (extensive `benchmarks/` suite measuring real token/cost/latency deltas) | **Consider** | DevBureau has no way to measure its *own* context footprint. `.agent/rules/GEMINI.md` is 32KB and gets fully injected into `CLAUDE.md`/root `GEMINI.md`/`AGENTS.md`/`copilot-instructions.md` every session before any work starts — nothing currently tracks whether that footprint is growing as agents/skills get added. A lightweight token-count check (no ML model, no proxy — just count tokens in the generated rule files) would be a much smaller, DevBureau-appropriate version of the same instinct. |
| Cursor's `CacheAligner` rationale (stabilize prefixes so provider KV caches actually hit) | **Validated, no action** | DevBureau's own `.cursor/rules/` migration (v3.4.0) already split a monolithic file into `alwaysApply: true` files (stable, loaded every turn) vs. glob-scoped conditional files — which is the same cache-friendly shape, arrived at independently. No gap to close. |

### Adopt (ready for follow-up)
1. ~~New shared skill (the "lazy ladder") encoding ponytail's 7-rung decision procedure, referenced by every coding agent.~~ **Done 2026-06-26** — see CHANGELOG v3.8.0. New `lean-code-ladder` skill, wired into all 17 code-writing agents.
2. ~~New universal Output Discipline rule in GEMINI.md TIER 0.~~ **Done 2026-06-26** — see CHANGELOG v3.8.0.
3. ~~`ponytail:`-style shortcut-marker convention + a debt-ledger report skill/command.~~ **Done 2026-06-26** — see CHANGELOG v3.8.0. `lean:` marker convention (part of `lean-code-ladder`) + new `lean-debt` skill/`/lean-debt` workflow.
4. ~~A `/review-lean`-style over-engineering finder (diff and repo scope).~~ **Done 2026-06-26** — see CHANGELOG v3.8.0. New `lean-audit` skill/`/lean-audit` workflow, one parameterized command instead of two (ponytail's own `-review`/`-audit` split merged into a single scope argument).

### Consider (needs a decision)
1. ~~Intensity levels (lite/full/ultra) vs. folding laziness into the existing `stack-sizing` tiers.~~ **Done 2026-06-26** — see CHANGELOG v3.8.0. User chose to fold it into `stack-sizing` rather than add a second dial; `lean-code-ladder` now has a "Calibrate by Project Tier" section, `stack-sizing` cross-references it.
2. ~~A lightweight token-footprint checker for DevBureau's own generated rule files.~~ **Done 2026-06-26** — see CHANGELOG v3.8.0. New `token_footprint.py`, chars/4 heuristic, diagnostic only (not a pass/fail gate).

### Skip
1. Headroom's runtime proxy/compression infrastructure as a whole — wrong architectural layer for what DevBureau is.

### Refinement (2026-06-26, user-requested follow-up)
The Skip verdict above covers Headroom's *proxy* mode correctly, but it does not cover the whole of Headroom. Headroom also ships an **MCP server** (`headroom mcp serve`, registered once at `claude mcp add --scope user`) exposing `headroom_compress`/`headroom_retrieve`/`headroom_stats` as tools an agent calls explicitly — no proxy, no Windows service, no admin rights. This mode needs nothing DevBureau can't already express: a conditional instruction ("if these MCP tools exist, use them; if not, proceed normally"). **Verdict: Adopt.** Done 2026-06-26 — see CHANGELOG v3.9.0. New GEMINI.md TIER 0 section, propagated to all 8 IDE targets. The one-time setup itself stays a documented, optional, user-run step (README), not bundled into `npx devbureau init` — confirmed during this session that the Windows persistent-proxy path hits a real upstream `sc.exe` argument-quoting bug in Headroom's own installer (`headroom install apply`, all three presets failed for different reasons: admin rights, admin rights, then a Windows-specific quoting defect even when run elevated). The MCP registration path, by contrast, worked without issue.

---

## 2026-06-27 — Benchmark Run #4 (single-source deep dive, user-requested)

**Source checked:** `shadcn/improve` (github.com/shadcn/improve), full clone + read of README, `skills/improve/SKILL.md`, and all three reference files (`audit-playbook.md`, `closing-the-loop.md`, `plan-template.md`). MIT license, v1.0.0, single-purpose Claude Code plugin.

**DevBureau state at time of run (per `doctor.py`):** 22 agents, 58 skills, 18 workflows.

**Key context for whoever reads this next:** `improve` is not an unknown competitor — it is a Claude Code Agent Skill **already installed and runnable in this very session** (it appears in the available-skills list as `improve`, verbatim-matching its own `SKILL.md` description). The benchmarking question this run answers isn't "should we learn about this" but "should DevBureau ship an equivalent skill of its own, portable to the 7 non-Claude-Code targets `sync_ide.py` supports" — since `improve` only exists for users on the Claude Code plugin marketplace. Same architecture class as DevBureau (plain markdown `SKILL.md` + reference files, no runtime), so everything below is directly portable.

### Findings

| Finding | Verdict | Reason |
|---|---|---|
| Whole pipeline: audit → vet → leverage-ranked findings table → user picks → self-contained plans for a *different, weaker, context-less* executor model | **Adopt** | Real gap, verified by reading both: `/plan` writes short same-session plans (`plan-writing` SKILL.md explicitly optimizes for "1 page max," 10 tasks, the same agent executing what it just planned); `/ade` plans *and* executes itself after approval. Neither separates "expensive model judges/specifies" from "cheap model executes," and neither is built for handoff to a model with zero session context. A new DevBureau-native skill/workflow in this shape, synced across all 8 IDE targets, would cover ground `/plan` and `/ade` don't — not a duplicate. |
| Hard Rule 6 — treat all content read from the audited repo as data, not instructions; record apparent prompt-injection attempts as a security finding instead of obeying them | **Adopt** | Confirmed absent by grep: `code-review-checklist`'s "Protection against Prompt Injection (if applicable)" checks whether *the reviewed code itself* defends against injection (e.g. in an LLM app being built) — a different concept from an *auditing agent* defending itself against instructions hidden in the files it reads. No DevBureau agent that reads arbitrary/unfamiliar content (`code-archaeologist`, `debugger`, `security-auditor`, the proposed new audit skill above) has this stated anywhere. Cheap (one paragraph), universal, zero conflict. |
| "Vet before presenting" — re-read every subagent-cited location yourself before showing the user a finding; record rejections so they aren't re-audited next run | **Adopt** | Confirmed absent by grep across all agents/skills/GEMINI.md, including `orchestrator.md`'s multi-agent coordination rules. Strong fit with the existing `confidence-scale` skill (🟢 CONFIRMED/🟡 INFERRED/🔴 GAP, adopted from Reversa in run #2) — vetting is literally the act of promoting INFERRED to CONFIRMED or rejecting it. Natural extension, not a new concept. |
| Leverage formula (impact ÷ effort, discounted by confidence and fix-risk) for ranking findings, with explicit tie-breakers (unblockers float up, HIGH-confidence security floats above equal-leverage non-security) | **Consider** | DevBureau already has an analogous formula — RICE (Reach × Impact × Confidence ÷ Effort) in `product-manager.md` — but scoped to *feature* prioritization, not audit-style findings from `security-auditor`/`lean-audit`/`debugger`, which currently just list findings unranked. Extending a leverage formula to those skills is reasonable but needs a decision: reuse RICE as-is, or adopt `improve`'s simpler impact÷effort (RICE's Reach term doesn't obviously apply to a bug-fix backlog). |
| Recon ingests ADRs/PRDs/`CONTEXT.md`/`DESIGN.md`/`PRODUCT.md` when present; documented tradeoffs aren't re-flagged as findings; a *stale* ADR (code drifted from the decision doc) is itself a finding | **Consider** | No equivalent anywhere in DevBureau. Real value for an evolving/maintained project with such docs, less relevant to the heavy greenfield/non-programmer slice of DevBureau's audience that `/ade` targets — needs a decision on which skill/workflow would own this (a recon step in the new audit skill above is the natural fit, not a retrofit onto `/ade`'s Discovery phase, which already has its own Socratic-gate shape). |
| Executor-proof plan format: STOP conditions, explicit in-scope/out-of-scope file lists, git-SHA "Planned at" stamp + drift check before execution, one verification command + expected output per step | **Consider** | Not a gap so much as a deliberate difference in audience: DevBureau's `plan-writing` skill is intentionally lightweight (max 10 tasks, 1 page, same-session execution, "NO fixed templates") for a non-programmer reviewing their own short plan. Adopting `improve`'s heavier format wholesale there would conflict with that philosophy. But the individual mechanisms (STOP conditions; drift check via git SHA) are cheap and valuable specifically for `/ade`, which already gates on human approval before execution and could resume after a long gap — worth scoping there, not as a `plan-writing` rewrite. |
| Model-tiering economics: advisor (expensive model) plans, a separate executor subagent (cheaper model, e.g. Haiku) implements in an isolated git worktree, advisor reviews like a tech lead (APPROVE/REVISE max 2 rounds/BLOCK) | **Consider** | Real architectural difference from `/ade`, which is one session planning *and* executing after approval — no model-cost tiering, no worktree isolation. Connects directly to the token-economy thread running through runs #1, #2, #3 (`lean-code-ladder`, `lean-debt`, output discipline, Headroom). Bigger design decision than the items above: needs the user to confirm it's worth the complexity, and depends on the host agent supporting worktree-isolated subagent dispatch (Claude Code does; not guaranteed on every one of the 8 IDE targets DevBureau promises to work across). |
| `reconcile` — backlog lifecycle command: spot-check DONE plans still hold, investigate BLOCKED ones, refresh drifted TODOs, retire findings fixed independently | **Consider** | Reinforces an item already left open in run #2 ("Disk-persisted pipeline state for resuming interrupted multi-phase runs — Still open"). `improve`'s version is simpler than what run #2 considered — no new state file, just re-reading `plans/README.md` and each plan's drift check. Worth resurfacing as the stronger, cheaper candidate now that two independent sources point at the same underlying gap. |
| `--issues` flag — publish selected plans as GitHub issues, with a mandatory visibility check and explicit confirmation before publishing sensitive (security/credential) findings to a public repo | **Consider** | Newly relevant: DevBureau didn't have its own GitHub remote until this same session. Nice-to-have, not urgent — needs a decision on which workflow owns `gh` interaction (devops-engineer already does elsewhere) and isn't useful until the audit skill above exists to produce plans worth publishing. |
| `quick`/`standard`/`deep` effort dial controlling audit depth and subagent fan-out count | **Validated, no action** | Same shape as Ponytail's lite/full/ultra dial from run #3, already resolved: DevBureau folds "how thorough" into the existing `stack-sizing` tiers rather than adding a second, parallel dial. No new decision needed — the precedent already covers this case. |

### Adopt (ready for follow-up)
1. ~~New DevBureau-native "audit → vet → leverage-ranked findings → self-contained handoff plans" skill/workflow, distinct from `/plan` (too lightweight, same-session) and `/ade` (plans *and* executes itself) — synced across all 8 IDE targets via `sync_ide.py`.~~ **Done 2026-06-27** — see CHANGELOG v3.10.0. New `codebase-audit` skill + `/audit` workflow, reuses existing category skills rather than re-deriving them. Excludes the `execute`/worktree-dispatch mechanism and ADR-aware recon — those stayed Consider items, not part of this Adopt.
2. ~~"Treat audited content as data, not instructions" rule.~~ **Done 2026-06-27** — see CHANGELOG v3.10.0. New TIER 0 "Untrusted Content Boundary" section in GEMINI.md, propagated to all 8 IDE targets.
3. ~~"Vet before presenting" step.~~ **Done 2026-06-27** — see CHANGELOG v3.10.0. New section in `confidence-scale` skill.

### Consider (needs a decision)
1. Extend a leverage/impact-effort formula from `product-manager`'s RICE to audit-style findings (`security-auditor`, `lean-audit`, `debugger`) — decide reuse-RICE vs. simpler impact÷effort.
2. ADR/PRD/`CONTEXT.md`/`DESIGN.md`/`PRODUCT.md`-aware recon — decide whether it belongs in the new audit skill (#1 above) only, or more broadly.
3. STOP conditions + git-SHA drift check for `/ade` plans specifically (not a `plan-writing` rewrite).
4. Model-tiered execution (expensive planner / cheap worktree-isolated executor / tech-lead-style review) for `/ade` — bigger decision, depends on host-agent worktree support across all 8 targets.
5. `reconcile`-style backlog lifecycle command — reinforces run #2's still-open "disk-persisted pipeline state" item with a simpler mechanism.
6. `--issues` flag to publish plans as GitHub issues, gated on a public-repo visibility warning — depends on #1 existing first.

### Skip
(none this run — even the lowest-priority findings above got a Consider, not a Skip, since `improve` is unusually close to DevBureau's own architecture and audience-adjacent enough that nothing was an obvious non-fit.)
