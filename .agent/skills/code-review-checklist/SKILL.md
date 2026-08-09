---
name: code-review-checklist
description: Use when reviewing PRs, auditing code quality, or checking for security issues — code quality, security, and best-practice guidelines.
allowed-tools: Read, Glob, Grep
---

# Code Review Checklist

## Quick Review Checklist

### Correctness
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling in place
- [ ] No obvious bugs

### Security
- [ ] Input validated and sanitized
- [ ] No SQL/NoSQL injection vulnerabilities
- [ ] No XSS or CSRF vulnerabilities
- [ ] No hardcoded secrets or sensitive credentials
- [ ] **AI-Specific:** Protection against Prompt Injection (if applicable)
- [ ] **AI-Specific:** Outputs are sanitized before being used in critical sinks

### Performance
- [ ] No N+1 queries
- [ ] No unnecessary loops
- [ ] Appropriate caching
- [ ] Bundle size impact considered

### Code Quality
- [ ] Clear naming
- [ ] DRY - no duplicate code
- [ ] SOLID principles followed
- [ ] Appropriate abstraction level

### Testing
- [ ] Unit tests for new code
- [ ] Edge cases tested
- [ ] Tests readable and maintainable

### Documentation
- [ ] Complex logic commented
- [ ] Public APIs documented
- [ ] README updated if needed

## Trilha de Auditoria (Trajectory Check)

Para tarefas marcadas como sensíveis (segurança, dados de produção, dinheiro, deploy, exclusão de dados), não avalie só se o resultado final está certo — avalie também o caminho usado para chegar lá:

- [ ] Quais arquivos/comandos/ferramentas foram usados para produzir esse resultado?
- [ ] Algum passo pulou uma checagem de segurança, apagou evidência de erro, ou silenciou um aviso só para o resultado "parecer" certo?
- [ ] Se sim → marque 🔴 BLOCKING mesmo que a saída final esteja correta. Um resultado certo por um caminho perigoso é uma falha de qualidade, não um sucesso.
- [ ] **Exemplo concreto — proteção de config:** editar/enfraquecer um arquivo de config de lint/formatter/tooling (`eslint.config.*`, `tsconfig.json`, `.flake8`, `pyproject.toml [tool.*]`, etc.) só para um check parar de reclamar, em vez de corrigir o código que ele está sinalizando, é 🔴 BLOCKING — mesmo com o lint/build "verde" no final. A trava existe para pegar o código, não para ser contornada.

### Retrospectiva de Rastreabilidade (revisão de histórico, sob pedido)

A Trilha de Auditoria acima olha UMA tarefa em andamento. Use este modo à parte quando o pedido for sobre o histórico ("os últimos commits têm rastreabilidade fraca?", "faz uma retrospectiva do repositório", `/audit` focado em processo) — não roda por padrão em toda revisão.

1. Rode `git log --oneline -30` (ou o intervalo pedido) e classifique cada commit:
   - Mensagem referencia issue/spec/`{task-slug}.md`, ou é autoexplicativa o bastante para reconstruir o "porquê"? Sem nenhum dos dois → 🟡 SUGGESTION (rastreabilidade fraca).
   - Commit mistura escopos não relacionados (ex.: fix + refactor + feature no mesmo commit) → 🟡 SUGGESTION (escopo misto, dificulta bisect/revert).
   - Commit toca arquivo sensível (`.agent/`, config de produção, schema de banco) sem menção a teste/validação na mensagem ou no PR associado → 🔴 BLOCKING.
2. Para commits sinalizados que tocam arquivos com muitos dependentes, rode `python .agent/scripts/blast_radius.py <arquivo> --diff` (`.agent/SCRIPTS_REGISTRY.md`) para confirmar se o raio de impacto real bate com o que a mensagem do commit sugere — uma mudança "pequena" com risco HIGH é ela mesma um achado.
3. Reporte como uma lista curta, mesmo vocabulário 🔴/🟡/🟢 desta skill, sem tabela nova: padrão observado, exemplos (`hash` curto + descrição), e uma sugestão de mensagem-modelo se o padrão se repetir 3+ vezes (candidato a lembrar em `.agent/memory/lessons.md`, não a virar script — julgamento de "essa mensagem conta a história certa" não é determinístico).

## AI & LLM Review Patterns (2025)

### Logic & Hallucinations
- [ ] **Chain of Thought:** Does the logic follow a verifiable path?
- [ ] **Edge Cases:** Did the AI account for empty states, timeouts, and partial failures?
- [ ] **External State:** Is the code making safe assumptions about file systems or networks?

### Prompt Engineering Review
```markdown
// ❌ Vague prompt in code
const response = await ai.generate(userInput);

// ✅ Structured & Safe prompt
const response = await ai.generate({
  system: "You are a specialized parser...",
  input: sanitize(userInput),
  schema: ResponseSchema
});
```

## Anti-Patterns to Flag

```typescript
// ❌ Magic numbers
if (status === 3) { ... }

// ✅ Named constants
if (status === Status.ACTIVE) { ... }

// ❌ Deep nesting
if (a) { if (b) { if (c) { ... } } }

// ✅ Early returns
if (!a) return;
if (!b) return;
if (!c) return;
// do work

// ❌ Long functions (100+ lines)
// ✅ Small, focused functions

// ❌ any type
const data: any = ...

// ✅ Proper types
const data: UserData = ...
```

## Review Comments Guide

```
// Blocking issues use 🔴
🔴 BLOCKING: SQL injection vulnerability here

// Important suggestions use 🟡
🟡 SUGGESTION: Consider using useMemo for performance

// Minor nits use 🟢
🟢 NIT: Prefer const over let for immutable variable

// Questions use ❓
❓ QUESTION: What happens if user is null here?
```
