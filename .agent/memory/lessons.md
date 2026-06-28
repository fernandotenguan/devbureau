# Lessons Learned — Antigravity Kit

> Padrões identificados durante o desenvolvimento. Consulte antes de iniciar uma task complexa.

---

## Formato de entrada

```markdown
## YYYY-MM-DD — [Feature/Task Name]
**Gatilho:** Situação/palavra-chave que deveria fazer o agente lembrar deste padrão
**Confiança:** 🟢 Confirmado / 🟡 Inferido / 🔴 Hipótese (escala de `confidence-scale`)
**Padrão identificado:** O que funcionou bem (reutilizável)
**Pitfall evitado:** O que não fazer / armadilha identificada
**Evidência:** Onde isso foi comprovado (commit, sessão, teste) — o que sustenta o nível de Confiança
**Arquivos chave:** lista de arquivos relevantes
```

Confiança usa a mesma escala de `.agent/skills/confidence-scale/SKILL.md`: 🟢 Confirmado (validado em produção ou em múltiplas sessões), 🟡 Inferido (observado uma vez, ainda não re-testado), 🔴 Hipótese (ainda não comprovado, registrado para vigiar).

---

## 2026-03-03 — AIOS Integration Planning

**Gatilho:** Adicionar um novo script master, workflow ou skill ao kit.
**Confiança:** 🟢 Confirmado (princípio reaplicado em toda sessão de benchmark desde então)
**Padrão identificado:** Ao integrar novos scripts/workflows ao kit, atualizar SEMPRE os 4 arquivos de configuração do agente em sequência: DEVBUREAU.md → ARCHITECTURE.md → intelligent-routing → workflow file.
**Pitfall evitado:** Criar novos scripts sem registrá-los no DEVBUREAU.md faz o agente não saber que existem.
**Evidência:** Repetido em todas as implementações de benchmark (Runs #1–#7, ver `.agent/memory/benchmark-log.md`).
**Arquivos chave:** `.agent/rules/DEVBUREAU.md`, `.agent/ARCHITECTURE.md`, `.agent/skills/intelligent-routing/SKILL.md`

## 2026-03-06 — Premium Design Agent (Skills Locais)

**Gatilho:** Criar uma skill reutilizável e compartilhável entre projetos/equipes.
**Confiança:** 🟢 Confirmado (modelo de pasta usado por toda skill complexa do kit desde então)
**Padrão identificado:** Skills complexas devem ser organizadas em múltiplos arquivos: SKILL.md (instruções) + reference files (dados). O SKILL.md contém a tabela de referências internas com prioridade (🔴 Obrigatório / 🟡 Sob demanda). Exemplo: premium-design-orchestrator tem SKILL.md + palette-library.md + design-references.md.
**Pitfall evitado:** Skills Globais (`~/.gemini/antigravity/skills/`) NÃO são versionadas no Git. Para projetos compartilháveis, usar Skills Locais (`.agent/skills/`). A portabilidade exige que tudo relevante esteja dentro do repositório.
**Evidência:** Estrutura replicada em `framework-benchmarking`, `mobile-design`, `saas-stack-rules` e outras skills multi-arquivo.
**Arquivos chave:** `.agent/skills/premium-design-orchestrator/`, `.agent/skills/brand-identity-extractor/`, `.agent/skills/premium-tech-stack/`
