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
```

Confiança usa a mesma escala de `.agent/skills/confidence-scale/SKILL.md`: 🟢 Confirmado (causa raiz reproduzida e corrigida), 🟡 Inferido (causa mais provável, não 100% reproduzida), 🔴 Hipótese (ainda não comprovado, registrado para vigiar).

---

## 2026-03-03 — GEMINI.md não refletia novos scripts

**Gatilho:** Agente criou um script/workflow novo mas parece "não saber" que ele existe nas sessões seguintes.
**Confiança:** 🟢 Confirmado (causa raiz reproduzida e corrigida)
**Sintoma:** Agente não invocava `doctor.py` ou `/ade` automaticamente mesmo após implementação.
**Causa raiz:** Arquivos foram criados no filesystem mas não registrados no `GEMINI.md` (Request Classifier + Scripts table + Quick Reference).
**Solução:** Atualizar as 4 seções de GEMINI.md + ARCHITECTURE.md + intelligent-routing.
**Evidência:** Reaplicado como checklist mandatório em `/ade`'s fase de Memory Registration.
**Prevenção:** Usar o `/ade` workflow para qualquer nova adição ao kit — ele inclui fase de Memory Registration.

---

## Regra Geral: ZeroDivisionError em checklist.py

**Gatilho:** `checklist.py` lançando exceção em vez de relatório, especialmente em projeto recém-iniciado.
**Confiança:** 🟢 Confirmado (causa raiz reproduzida e corrigida)
**Sintoma:** `checklist.py` falha na linha ~232 com `ZeroDivisionError`.
**Causa raiz:** Dicionário `scores` está vazio quando nenhum check retorna resultado.
**Solução:** Adicionar guard `if max_val > 0` antes de calcular percentual.
**Evidência:** Correção aplicada diretamente em `.agent/scripts/checklist.py`.
**Prevenção:** Sempre rodar `doctor.py` antes de `checklist.py` para validar que o ambiente está correto.
