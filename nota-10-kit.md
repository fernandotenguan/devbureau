# Plano — Rumo à Nota 10 do Kit (v3.26.0)

> Objetivo: fechar as três lacunas de maior alavancagem identificadas na análise de 2026-07-03
> (benchmark-log runs #1–#8 + medição ao vivo do token_footprint.py), sem sair da arquitetura
> markdown-estática atual.

## Contexto medido (antes)

- `DEVBUREAU.md`: 49.615 chars ≈ **12.403 tokens**, injetado integralmente em Claude/Gemini/Codex
  (~13.3k tokens por sessão) — acima do alerta de 10k em 4 targets.
- 66 skills, zero teste comportamental sobre o estoque existente (decisão de 2026-06-27: TDD só
  para skills novas).
- Único Consider aberto já julgado valioso pelo usuário (CHANGELOG v3.20.0): `skillify`.

## Fases

### Fase 1 — Dieta de contexto (maior alavancagem)
- [ ] Deduplicar: "Validação Seletiva" aparece 2x (EFICIÊNCIA §2 + TIER 0) → manter 1.
- [ ] Mover detalhe verboso para `.agent/rules/reference/OPERATIONS_DETAIL.md` (lido sob demanda),
      mantendo no core a regra + ponteiro: tabela de 15 scripts (já duplica SCRIPTS_REGISTRY.md),
      comandos completos de validação seletiva (já em test-strategy-by-change-type.md),
      Code Quality Standards TIER 1 (detalhe já vive em clean-code), Gemini Mode Mapping
      (→ behavioral-modes), Quick Reference expandido.
- [ ] NÃO tocar: Socratic Gate, Matriz de Decisão, Gabarito de Conduta (pedidos pessoais do
      usuário), Anti-Hallucination core, Zero-Break core, strings exigidas pelos testes
      ("TIER 0", "SOCRATIC GATE", "/ade", >5KB).
- [ ] Alvo: core ≤ ~9k tokens (meta honesta; medir, não projetar).
- [ ] `sync_ide.py --target all` + `token_footprint.py` (antes/depois) + `pytest .agent/tests/`.

### Fase 2 — Skill `skillify`
- [ ] Criar `.agent/skills/skillify/SKILL.md` (metodologia writing-skills: description = quando
      usar; confirmação explícita antes de salvar qualquer artefato).
- [ ] Registrar gatilhos EN/PT-BR no REQUEST CLASSIFIER ou Quick Reference (forma enxuta).

### Fase 3 — Skill Re-Audit piloto (3 skills)
- [ ] Auditar `clean-code`, `plan-writing`, `intelligent-routing` contra: regra de description
      trigger-shaped (writing-skills), tamanho/staleness, sobreposição com outras skills,
      diff conceitual vs. melhores equivalentes públicos já minerados (superpowers/gstack/ECC).
- [ ] Aplicar correções baratas (descriptions, cortes de redundância); registrar veredito por
      skill como "Skill Re-Audit #1" no benchmark-log.md (novo tipo de run, reutilizável).

### Fase 4 — Verificação final
- [ ] `pytest .agent/tests/ -v` (deve manter 100%), `doctor.py`, `token_footprint.py` final.
- [ ] CHANGELOG v3.26.0 + bump de versão + commit local (sem push — Matriz de Decisão).

## Fora de escopo (deliberado)
- Runtime/daemon próprio, marketplace nativo, retrofit TDD das 66 skills (decisões anteriores
  do usuário permanecem válidas; re-audit piloto é a exceção escopada de 3 skills).
