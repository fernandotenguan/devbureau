# Benchmark Run #10: Adopt items

Source: `/benchmark` run #10 against `asgeirtj/system_prompts_leaks` (2026-09-24). Mechanisms are rewritten in the kit's own words; no vendor text is copied.

## Goal

Close the five gaps the run confirmed by grep, without adding a skill, agent, workflow or script, and with the smallest possible growth of the always-loaded P0 file.

## Tasks

- [x] 1. `code-review-checklist`: add four bug-hunting angles (removed behavior, callers, altitude, citable convention) and require a concrete failure scenario per finding. → Verify: section present, no duplicate of "Revisão em Dois Eixos", test suite green.
- [x] 2. `DEVBUREAU.md` Surgical Changes: one row for "not yours, don't undo" plus collateral check after installers/generators. → Verify: `sync_ide.py` regenerates targets, integrity manifest regenerated.
- [x] 3. `DEVBUREAU.md` Zero-Break evidence table: one row for an independent oracle. → Verify: same as task 2, P0 growth measured with `token_footprint.py`.
- [x] 4. `security-auditor`: curated false-positive precedents, adapted to a SaaS audience (DoS, rate limiting and audit-log exclusions deliberately not imported). → Verify: section present, consistent with the 🟢🟡🔴 confidence rule.
- [x] 5. `frontend-specialist`: draw style, palette and layout with a real random source from the kit's existing curated lists; user-supplied copy goes in verbatim. → Verify: lists referenced exist, no new script.
- [x] 6. Maintainer changelog (local only, gitignored) under Unreleased; mark items done in the local benchmark log. → Verify: `doctor.py` 10/10, `pytest .agent/tests/` green, `doc_drift_check.py` clean.

## Out of scope

The nine Consider items from the same run (need a user decision). Version bump (release step).

## Assumptions

- Work happens on `feat/benchmark-run10-adopt`, not on the waves 1-2 branch.
- Local commit is automatic; push waits for the user.
