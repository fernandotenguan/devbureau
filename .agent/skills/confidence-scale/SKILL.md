---
name: confidence-scale
description: Marks every factual claim an agent makes about existing code with a confidence level — CONFIRMED, INFERRED, or GAP. Use whenever an agent reads/analyzes code it did not write in this session (legacy analysis, bug investigation, security audit) and reports findings back to the user. Triggers on "analyze this codebase", "what does this code do", "is this safe", "explain this legacy system".
allowed-tools: Read, Grep, Glob
---

# Confidence Scale

> **Honesty about what you actually know beats a confident-sounding guess.** An AI reading unfamiliar code can verify some things directly and has to infer others — the user needs to know which is which before they act on it.

---

## ⚠️ Core Principle

A finding without a confidence marker is a black box of trust — the reader can't tell what was extracted from the code versus what was assumed. Mark every non-trivial claim about existing code with one of three levels. No exceptions, no silent omissions.

---

## 1. The Three Levels

| Mark | Name | Meaning | Bar to meet |
|---|---|---|---|
| 🟢 | **CONFIRMED** | Read directly from the code | Can cite `file:line` as evidence |
| 🟡 | **INFERRED** | Deduced from naming, patterns, or surrounding context | Plausible, but no direct statement in the code says so |
| 🔴 | **GAP** | Cannot be determined from the code alone | Requires the user to confirm — don't guess and present it as fact |

---

## 2. How to Apply

- Attach the mark inline, right after the claim: `O sistema usa soft delete nos clientes (campo deleted_at). 🟡` or `A função aplica 15% de desconto em pedidos acima de R$500. 🟢 (src/pricing/discount.js:47)`.
- 🟢 claims must include the file and line (or equivalent precise reference) — if you can't point to it, it's not 🟢.
- 🟡 claims should name what the inference is based on (a field name, a directory convention, a comment) so the user can judge the inference themselves.
- 🔴 claims should be collected into a short list of open questions at the end of the response, not buried inline — the user needs to act on them, not just read past them.
- When a 🔴 gets resolved by the user, treat their answer the same way you'd treat new evidence: cite it as 🟢 if they pointed to a concrete source, or 🟡 if it's their best understanding without a concrete reference.

---

## 3. When This Applies

Use this for any output where the agent is reporting facts about code it analyzed rather than code it wrote:

- `code-archaeologist` explaining what a legacy module does or why a pattern exists.
- `debugger` describing root cause once investigation is done — "the bug is caused by X" needs a confidence level, especially under intermittent/hard-to-reproduce bugs.
- `security-auditor` reporting whether a vulnerability is actually exploitable in this codebase vs. a theoretical pattern match.

Do **not** apply this to code the agent is writing in the current session — that's a design decision, not a factual claim about something pre-existing, and doesn't need a confidence mark.

---

## 4. Anti-Patterns

- Marking everything 🟢 because admitting uncertainty feels less authoritative — defeats the entire purpose.
- Burying 🔴 gaps inline instead of surfacing them as explicit questions — the user will scroll past them.
- Inventing a plausible-sounding explanation instead of marking something 🔴 — a confident wrong answer is worse than an honest gap.
