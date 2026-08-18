# Gotchas & Armadilhas — DevBureau

> Erros comuns e como evitá-los. Consulte antes de iniciar desenvolvimento.

---

## Formato de entrada

```markdown
## YYYY-MM-DD — [Nome do Problema]
**Gatilho:** Sintoma ou contexto que deveria fazer o agente lembrar deste gotcha
**Confiança:** 🟢 Confirmado / 🟡 Inferido / 🔴 Hipótese (escala de `confidence-scale`)
**Sintoma:** O que aconteceu / como se manifesta
**Causa raiz:** Por que aconteceu
**Solução:** Como foi resolvido
**Evidência:** Onde isso foi corrigido/comprovado (commit, arquivo, teste)
**Prevenção:** Como evitar que aconteça de novo
**Última recuperação:** (opcional) YYYY-MM-DD da última vez que este gotcha foi de fato consultado antes de repetir a mesma armadilha — atualize via `python .agent/scripts/memory_recall.py mark gotchas.md <data> <trecho-do-título>`
```

Confiança usa a mesma escala de `.agent/skills/confidence-scale/SKILL.md`: 🟢 Confirmado (causa raiz reproduzida e corrigida), 🟡 Inferido (causa mais provável, não 100% reproduzida), 🔴 Hipótese (ainda não comprovado, registrado para vigiar).

`Última recuperação:` é opcional e não retroativo — só entradas novas precisam trazê-lo. `python .agent/scripts/memory_recall.py stale` lista entradas antigas nunca recuperadas.

> Registre também os becos-sem-saída: uma abordagem tentada e descartada (com o motivo) é tão valiosa quanto a causa raiz de um bug — evita que uma sessão futura perca tempo tentando de novo o mesmo caminho já provado errado.

---

<!-- Entradas deste projeto começam abaixo. Este arquivo nasce vazio em cada instalação nova do DevBureau — não herda os gotchas do próprio kit. -->
