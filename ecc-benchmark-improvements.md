# ECC Benchmark — Improvements

Source: `/benchmark` run #7 (2026-06-28) against `affaan-m/ECC`. Full findings, comparison table, and verdicts in `.agent/memory/benchmark-log.md`.

## Goal

Implement the 5 **Adopt** items from the ECC benchmark run — each closes a concrete gap, none conflict with DevBureau's lean/tiered philosophy, none require a design decision beyond "yes, build it."

## Tasks

- [x] **Task 1: New hook — block `git --no-verify` / `-c core.hooksPath=`**
  Create `.agent/scripts/hooks/block_no_verify.py` — a `PreToolUse` hook on `Bash` that inspects the command string for `git ... --no-verify` (on `commit`, `push`, `merge`, `cherry-pick`, `rebase`, `am`) or `-c core.hooksPath=` and exits non-zero with a message pointing at the actual hook being bypassed. Mirror `guard_worktree_path.py`'s structure (same PreToolUse pattern, same `.claude/settings.json` registration via `sync_ide.py`'s `generate_claude_config()`). Update `protect_generated_files.py`'s sibling list only if it documents the hook roster elsewhere — check first.
  → Verify: `git commit --no-verify -m "test"` is blocked with exit code 2 and a clear message; `git commit -m "test"` (no bypass flag) is unaffected. Run `python -m pytest .agent/tests/test_kit_integrity.py -q` — must stay green.

- [x] **Task 2: New hook — advisory `console.log`/debug-statement warning**
  Create `.agent/scripts/hooks/warn_debug_statements.py` — a `PostToolUse` hook on `Edit`/`Write` for `.ts`/`.tsx`/`.js`/`.jsx` files that greps the edited file for `console.log(` and prints an advisory (never blocks), same style as `scan_injection.py`. Register in `.claude/settings.json` via `sync_ide.py`.
  → Verify: editing a `.ts` file containing `console.log("x")` prints the advisory to stderr but the edit still succeeds (exit 0). Editing a file with no `console.log` prints nothing.

- [x] **Task 3: Document AgentShield as an optional companion security scanner**
  Add a new README.md/README.pt-BR.md section (same pattern as the existing "Optional: Headroom MCP" section) explaining `npx ecc-agentshield scan` as a third-party, not-bundled, documented-only tool — what it scans (CLAUDE.md, settings.json, MCP configs, hooks, agent/skill definitions), the one-line install-free quick start, and a cross-reference from `vulnerability-scanner`'s and `security-auditor`'s SKILL.md/agent files pointing to it as an optional deeper-scan companion.
  → Verify: the section exists in both README files with the exact `npx ecc-agentshield scan` command; `vulnerability-scanner/SKILL.md` and `security-auditor.md` each contain a one-line pointer to it.

- [x] **Task 4: New "Token Optimization" README section**
  Add a section documenting concrete `~/.claude/settings.json` values: `"model": "sonnet"`, `MAX_THINKING_TOKENS=10000`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50`, `CLAUDE_CODE_SUBAGENT_MODEL=haiku`, with a one-line explanation of each and a cross-reference to `/ade`'s existing per-subtask model-tiering (CHANGELOG v3.13.0) so the two don't read as unrelated advice.
  → Verify: section exists in both README files, includes all 4 settings with their effect, links to the `/ade` model-tiering mention.

- [x] **Task 5: `npx devbureau uninstall [--dry-run]`**
  Add an `uninstall(args)` function to `bin/devbureau.js`, registered alongside `init`/`update`. Reads `.devbureau-manifest.json` (the same manifest `update` already maintains); for every file listed, removes it only if its current hash still matches the manifest (i.e., not customized by the user — reuse the existing `isCustomized` logic from `update`); reports customized files left in place; removes `.agent/` only if it ends up empty; removes the generated IDE files (`AGENTS.md`, `GEMINI.md`, `.claude/`, etc.) only via the same protected-files list `protect_generated_files.py` already tracks, so the two never drift. `--dry-run` prints the plan without deleting anything. Update `printUsage()` and README's CLI command tables.
  → Verify: run `npx devbureau init` in a scratch directory, customize one file under `.agent/`, then `npx devbureau uninstall --dry-run` (prints plan, nothing removed), then `npx devbureau uninstall` (removes unmodified files, reports the customized one, leaves it on disk). Re-run `python .agent/scripts/doctor.py` in that directory afterward — should report `.agent/` missing, not crash.

## Done When

- [x] All 5 tasks verified individually (see per-task checks above).
- [x] `python .agent/scripts/doctor.py` and `python -m pytest .agent/tests/test_kit_integrity.py -q` both pass after all changes.
- [x] `python .agent/scripts/sync_ide.py --target all` regenerates cleanly with the two new hooks registered in `.claude/settings.json`.
- [x] CHANGELOG.md gets a new dated entry summarizing all 5 items, citing this benchmark run (v3.16.0).

## Notes

**Consider items, resolved 2026-06-28** (full reasoning in `.agent/memory/benchmark-log.md`'s 2026-06-28 entry, implementation in CHANGELOG v3.17.0):
1. ~~Lightweight structured fields (trigger/confidence/evidence) for `lessons.md`/`gotchas.md`.~~ **Done** — new Gatilho/Confiança/Evidência fields, reusing `confidence-scale`'s 🟢/🟡/🔴.
2. ~~GateGuard-style fact-forcing gate.~~ **Done** — documented as an external tool (Headroom/AgentShield pattern), not built native.
3. Re-verify Cursor's current hook-event surface. **Declined for now** — revisit when Cursor becomes an active priority.
4. ~~A `skill-create`-equivalent workflow.~~ **Reframed and done** — user wanted something broader: mining engineering patterns from senior-built professional projects (not other AI kits) into DevBureau's own knowledge base. New `pattern-mining` skill + `/mine-patterns` workflow, logging to `.agent/memory/pattern-mining-log.md`, never auto-applying.
5. Component-level selective install. **Declined** — keeping the current whole-folder `init`/`update` model.
6. ~~Zed as a 9th `sync_ide.py` target.~~ **Done** — turned out to be the 10th target, not the 9th (the original count had undercounted the already-shipped OpenCode target).

**Explicitly Skipped, not revisited unless something changes:** Tkinter dashboard GUI, package-manager auto-detection, JoyCode/CodeBuddy/Qwen CLI adapters, hosted GitHub App for PR audits, wholesale catalog growth toward ECC's raw agent/skill counts.
