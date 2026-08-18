# Lessons Learned — DevBureau

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
**Última recuperação:** (opcional) YYYY-MM-DD da última vez que esta entrada foi de fato consultada/aplicada — atualize via `python .agent/scripts/memory_recall.py mark lessons.md <data> <trecho-do-título>` quando recuperar a entrada
```

Confiança usa a mesma escala de `.agent/skills/confidence-scale/SKILL.md`: 🟢 Confirmado (validado em produção ou em múltiplas sessões), 🟡 Inferido (observado uma vez, ainda não re-testado), 🔴 Hipótese (ainda não comprovado, registrado para vigiar).

`Última recuperação:` é opcional e não retroativo — só entradas novas precisam trazê-lo. `python .agent/scripts/memory_recall.py stale` lista entradas antigas que nunca tiveram uma recuperação registrada, candidatas a revisão via `config-gc`.

---

<!-- Entradas deste projeto começam abaixo. Este arquivo nasce vazio em cada instalação nova do DevBureau — não herda as lições do próprio kit. -->
