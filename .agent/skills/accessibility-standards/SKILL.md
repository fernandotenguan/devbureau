---
name: accessibility-standards
description: WCAG 2.1/2.2 compliance principles — semantic HTML, ARIA roles, keyboard navigation, color contrast, screen reader testing, and automated a11y tooling (axe, pa11y, Lighthouse). Use when auditing or building accessible UI, or when a legal/compliance requirement (ADA, EN 301 549, LBI/eMAG) applies. Triggers on "acessibilidade", "leitor de tela", "contraste", "WCAG", "ARIA", "navegação por teclado".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Accessibility Standards

> **If it's not accessible, it's broken — not "broken for some users," just broken.**

---

## ⚠️ Core Principle

- Semantic HTML first. ARIA is a patch for when semantic HTML genuinely can't express the interaction — not a default.
- WCAG **AA** is the practical bar for almost everything (it's what ADA lawsuits, EU's EN 301 549, and Brazil's LBI/eMAG for public-sector sites reference). AAA is for content explicitly aimed at users with disabilities.
- Accessibility is sized by audience and legal exposure, not by project tier the way infra is — a one-page Prototype aimed at the public still needs basic semantic HTML and alt text.

---

## 1. WCAG Levels — When Each Applies

| Level | Bar | Typical Requirement Source |
|---|---|---|
| **A** | Minimum, often legally insufficient alone | Rarely the target alone |
| **AA** | Practical default for almost everything public-facing | ADA (US), EN 301 549 (EU), LBI/eMAG (BR public sector) |
| **AAA** | Enhanced, for content/audiences that need it | Government services for disability-focused orgs, specific contracts |

Default to **AA** unless told otherwise.

---

## 2. Semantic HTML Checklist (do this before reaching for ARIA)

- [ ] Headings in order (`h1` → `h2` → `h3`, no skipped levels)
- [ ] `<button>` for actions, `<a href>` for navigation — never a `<div onClick>`
- [ ] `<label>` associated with every form input
- [ ] Landmark elements (`<nav>`, `<main>`, `<header>`, `<footer>`)
- [ ] Images have meaningful `alt` text (or `alt=""` if purely decorative)

---

## 3. ARIA — Only When Semantic HTML Can't Do It

| Need | Use |
|---|---|
| Custom dropdown/combobox | `role="combobox"` + `aria-expanded`, `aria-controls` |
| Live region (toast, status update) | `aria-live="polite"` (or `"assertive"` only for urgent errors) |
| Icon-only button | `aria-label` describing the action, not the icon |
| Modal dialog | `role="dialog"` + `aria-modal="true"` + focus trap + restore focus on close |

> First rule of ARIA: no ARIA is better than wrong ARIA. An incorrect `role` lies to screen reader users.

---

## 4. Keyboard Navigation

- Every interactive element reachable via `Tab`, operable via `Enter`/`Space`.
- Visible focus indicator — never `outline: none` without a replacement.
- Logical tab order matching visual order.
- No keyboard traps (a modal must let `Esc` or `Tab` cycling out).

---

## 5. Color & Contrast

| Text Type | Minimum Ratio (AA) |
|---|---|
| Normal text | 4.5:1 |
| Large text (18pt+/14pt bold+) | 3:1 |
| UI components/icons | 3:1 |

- Never use color alone to convey meaning (error state needs an icon/text too, not just red).

---

## 6. Testing Approach

| Layer | Tool | Catches |
|---|---|---|
| **Automated, CI** | `axe-core`, `pa11y`, Lighthouse a11y audit | ~30-40% of issues: missing labels, contrast, ARIA misuse |
| **Manual, keyboard-only** | Unplug the mouse, navigate the whole flow | Tab order, focus traps, hidden interactive elements |
| **Manual, screen reader** | NVDA (Windows, free), VoiceOver (Mac) | Announcement clarity, redundant/missing context |

Automated tools are a floor, not a finish line — they cannot judge whether an `alt` text is actually meaningful.

---

## ❌ Anti-Patterns

- `<div onClick>` instead of `<button>`.
- Decorative icon fonts read aloud as gibberish by screen readers (missing `aria-hidden="true"`).
- Placeholder text used as the only label.
- Auto-playing media with no pause control.
- Fixing only what the automated scanner flags and calling it "accessible."
