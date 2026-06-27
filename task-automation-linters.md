# Task: Implement Lint Automation and Auto-Fixing

> **Goal**: Create a unified auto-fixer that cleans and optimizes code (JS, TS, Python, HTML, CSS) automatically before task delivery.

---

## 🏗️ Implementation Plan

### Phase 1: Engine Creation (scripts)
- [ ] Create `.agent/scripts/auto_fixer.py`
    - Support for JS/TS (ESLint --fix, Prettier)
    - Support for Python (Ruff fix/format)
    - Support for HTML/CSS (Prettier)
- [ ] Ensure cross-platform compatibility (Windows/Linux)

### Phase 2: Workflow Integration
- [ ] Create `/clean` workflow in `.agent/workflows/clean.md`
- [ ] Update `/ade` and other major workflows to include a "Clean & Optimize" step at the end.

### Phase 3: Rule Enforcement
- [ ] Update `DEVBUREAU.md` (TIER 0) to mandate running `auto_fixer.py` before reporting task success.

---

## 🛠️ Proposed Solution: `auto_fixer.py`

The script will detect the technology stack and run:
1. **JavaScript/TypeScript**: `npx eslint --fix .` + `npx prettier --write .`
2. **Python**: `ruff check --fix .` + `ruff format .`
3. **HTML/CSS**: `npx prettier --write "**/*.{html,css}"`

---

## 🚦 Verification Criteria
1. Run script on a "dirty" file (mixed indentation, unused imports).
2. Verify file is automatically corrected.
3. Verify no breaking changes were introduced.
