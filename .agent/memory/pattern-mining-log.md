# Pattern Mining Log — DevBureau

> Dated record of `/mine-patterns` runs. Each entry mines one reference project for generalizable engineering patterns to import into DevBureau's own knowledge base. Never auto-applied — a human decides what merges. Full methodology in `.agent/skills/pattern-mining/SKILL.md`.

---

## Formato de entrada

```markdown
## YYYY-MM-DD — [repo name/URL]

**Repo:** path or URL, stack, maturity signals observed
**Patterns found:**

| Pattern | Confidence | Where observed | Destination | Verdict |
|---|---|---|---|---|
| [pattern] | 🟢/🟡/🔴 | `file:line` or dir | lessons.md / skill/agent name | Adopt/Consider/Skip |

**Adopt (ready for follow-up):** ...
**Consider (needs a decision):** ...
**Skip:** ...
```

---

No runs logged yet — this file is populated the first time `/mine-patterns` (or the `pattern-mining` skill directly) is invoked against a reference project.
