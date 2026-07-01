# Frontend Craft Knowledge Port (open-design → DevBureau)

## Goal
Port the 4 prioritized quality gaps from `.agent/memory/frontend-design-knowledge-extraction.md` (Fase 1: anti-ai-slop cardinal sins, state coverage, accessibility legal floor, form validation lifecycle) into the DevBureau frontend/accessibility skills, rewritten in DevBureau's own vocabulary with attribution.

## Critérios de Aceite
- [x] Quando `frontend-specialist` avaliar uma tela gerada, ele deve checar os 7 pecados capitais (hex exatos, emoji-ícone, métrica inventada, filler copy) e não apenas Purple Ban/bento/glassmorphism
- [x] Quando qualquer tela buscar/transformar/aceitar dados, o agente deve cobrir os 5 estados obrigatórios (loading/empty/error/populated/edge), não só o estado populado
- [x] Quando `accessibility-specialist` avaliar tamanho de toque, ele deve citar 24×24 CSS px como piso AA (não 44×44)
- [x] Quando um formulário for revisado, o agente deve checar o timing de validação (no blur, não no keystroke) e o input state machine

## Tasks
- [x] Task 1: Adicionar "7 Cardinal Sins" (hex exatos, emoji ban, invented-metrics ban, filler-copy ban) em `.agent/skills/frontend-design/SKILL.md` seção 9 → Verify: seção existe com os 7 itens e nota de atribuição
- [x] Task 2: Criar `.agent/skills/frontend-design/state-coverage.md` (5 estados, thresholds de loading, composição de erro/empty, ARIA) + linkar no Selective Reading Rule e Reference Files → Verify: arquivo existe, é referenciado em 2 lugares do SKILL.md
- [x] Task 3: Atualizar `.agent/skills/accessibility-standards/SKILL.md` (piso legal por jurisdição, touch target 24×24 AA / 44×44 AAA, nota APCA, paridade mobile nativa) e `.agent/agents/accessibility-specialist.md` (correção do erro comum de touch target) → Verify: seções novas presentes, sem remover conteúdo existente
- [x] Task 4: Criar `.agent/skills/frontend-design/form-validation.md` (state machine, Constraint Validation API, timing, Standard Schema) + linkar no Selective Reading Rule e Reference Files → Verify: arquivo existe, é referenciado em 2 lugares do SKILL.md
- [x] Task 5: Rodar `python .agent/scripts/checklist.py .agent/skills/frontend-design` e `python -m pytest .agent/tests/ -v` → Verify: ambos sem erro/falha (303 passed)

## Done When
- [x] As 4 tasks de conteúdo estão completas com atribuição a open-design/refero_skill
- [x] Kit integrity tests passam (303 testes)
- [x] Nenhum conteúdo de skills/design-systems/plugins ou código-fonte do open-design foi copiado, só o texto das regras reescrito

## Notes
Fonte dos arquivos: shallow clone de `nexu-io/open-design` em cache de sessão anterior (`craft/anti-ai-slop.md`, `craft/state-coverage.md`, `craft/accessibility-baseline.md`, `craft/form-validation.md`). Fase 2 (laws-of-ux.md, color.md, rtl-and-bidi.md, typography-hierarchy) fica fora deste plano — só entra se o usuário pedir depois.
