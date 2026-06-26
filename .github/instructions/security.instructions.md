---
applyTo: "**"
---

# Security Rules — DevBureau
> Auto-generated via sync_ide.py. Do not edit manually.

## Secrets Management

- Secrets and API keys exclusively in `.env`. NEVER hardcoded, NEVER committed to git.
- `.env.example` MUST exist with all required variables, without real values.
- Sensitive environment variables NEVER have `NEXT_PUBLIC_` prefix.
- Rotate secrets periodically. Use secret managers in production (AWS SM, GCP SM, Vault).

## Input & Output

- Validate and sanitize ALL user inputs. Use allowlists over denylists.
- Parameterized queries ONLY. NEVER concatenate user input into SQL.
- Escape output in HTML contexts to prevent XSS.
- Content Security Policy (CSP) headers on all responses.

## Authentication & Authorization

- Use established libraries (NextAuth, Passport, Firebase Auth). Never roll your own crypto.
- JWT tokens: short expiry (15min access, 7d refresh). Store refresh tokens securely.
- RBAC (Role-Based Access Control) enforced at API layer, not just UI.
- Password hashing with bcrypt or argon2. NEVER store plaintext passwords.

## Error Handling

- NEVER expose internal IDs (user_id, session_id) in browser console.
- NEVER log sensitive data in console.log (tokens, emails, passwords).
- Error messages returned to frontend NEVER expose stack traces, SQL queries, or internal structure.
- Use generic error messages for clients. Log detailed errors server-side only.

## Dependencies

- Review dependencies before adding. Check maintenance status and known vulnerabilities.
- Lock dependency versions. Use lockfiles (package-lock.json, poetry.lock).
- Run dependency audit regularly: `npm audit`, `pip-audit`, `safety check`.

## HTTPS & Transport

- HTTPS mandatory in production. Redirect HTTP to HTTPS.
- HSTS headers enabled. Secure and HttpOnly flags on cookies.
- CORS configured with explicit allowed origins. Never use `*` in production.
