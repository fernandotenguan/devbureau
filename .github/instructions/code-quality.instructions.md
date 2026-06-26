---
applyTo: "**"
---

# Code Quality Standards — DevBureau
> Auto-generated via sync_ide.py. Do not edit manually.

## Functions & Methods

- Functions MUST do ONE thing only. If you need "and" to describe it, split into two.
- Maximum 20 lines per function. Above that, extract sub-functions.
- Maximum 3 arguments per function. Above that, group into object/dataclass/Pydantic model.
- Functions MUST NOT have hidden side effects (mutating global state, modifying mutable arguments silently).
- Function names MUST be descriptive verbs: `create_subscription()`, `validate_input()`. Never `process()`, `handle()`, `do()`.

## Naming & Readability

- Names MUST reveal intent: `elapsed_time_in_days` not `d`, `is_active_subscription` not `flag`.
- Classes/models with noun names: `Subscription`, `UserProfile`. Avoid `Manager`, `Helper`, `Data`, `Info`.
- No ambiguous abbreviations: `usr`, `mgr`, `tmp`. Write in full.
- Consistent naming: if you used `get_user` in one module, don't use `fetch_user` in another without reason.

## Error Handling

- Use exceptions instead of return codes.
- NEVER return None/null to indicate error. Raise exception with clear message.
- Try/except MUST be specific: catch `ValueError`, `HTTPException`. NEVER generic `except Exception` (except in top-level catch-all).
- Domain errors MUST use custom exceptions: `SubscriptionExpiredError`, `QuotaExceededError`.

## Structure & Organization

- Law of Demeter: NEVER chain `a.get_b().get_c().do_something()`. Create direct method.
- One file, one responsibility: don't mix routes + service + schemas in the same file.
- Imports organized: stdlib > third-party > local (Python) / react > libs > components > utils (TypeScript).
- Dead code (unused functions, unused imports, commented variables) MUST be removed, not commented.

## Type Safety

- Python: type hints mandatory on all functions and variables. No generic `Any`.
- TypeScript: strict mode enabled. No `any`, no `@ts-ignore`, no `as unknown as`.

## Documentation

- Every new finished feature MUST be documented in README.md: feature name, short description, and flow.
- README MUST have a `## Features` section with updated feature list.
