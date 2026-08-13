---
name: plan-writing
description: Use when implementing features, refactoring, or any multi-step work that needs a written plan ({task-slug}.md) — provides task breakdown rules, acceptance criteria format, and the no-placeholders standard.
allowed-tools: Read, Glob, Grep
---

# Plan Writing

## Overview

This skill provides a framework for breaking down work into clear, actionable tasks with verification criteria.

## Task Breakdown Principles

### 1. Small, Focused Tasks

- Each task should take 2-5 minutes
- One clear outcome per task
- Independently verifiable

### 2. Clear Verification

- How do you know it's done?
- What can you check/test?
- What's the expected output?

### 3. Logical Ordering

- Dependencies identified
- Parallel work where possible
- Critical path highlighted
- **Phase X: Verification is always LAST**

### 4. Dynamic Naming in Project Root

- Plan files are saved as `{task-slug}.md` in the PROJECT ROOT
- Name derived from task (e.g., "add auth" → `auth-feature.md`)
- **NEVER** inside `.claude/`, `docs/`, or temp folders

## Vertical Slices, Not Layers

> Break work by feature slice (UI + logic + data together, testable end-to-end), never by architectural layer (all schemas, then all backend, then all UI).

Layer-first decomposition produces tasks that each finish "complete" but stay untestable until every layer for every feature has landed — a documented case: 26 tasks split by layer averaged ~20 agent rounds each, and roughly 3/4 of that work turned out to be pure rework once integration finally surfaced a mismatch nothing caught earlier.

| ❌ By layer (nothing testable until the end)               | ✅ By vertical slice (testable after each task)                   |
| ---------------------------------------------------------- | ----------------------------------------------------------------- |
| Task 1: all database schemas (login, scheduling, checkout) | Task 1: login — schema + endpoint + form, working end-to-end      |
| Task 2: all backend endpoints                              | Task 2: scheduling — schema + endpoint + form, working end-to-end |
| Task 3: all frontend screens                               | Task 3: checkout — schema + endpoint + form, working end-to-end   |

**Rule:** a task is only "done" when a human can open the app and exercise the feature it describes — not when its layer is internally complete. This is about task/ticket decomposition specifically; it doesn't change how the code itself is organized internally (routes/services/repositories layering inside a finished feature is still correct).

## Decisões, Não Código

- **Sem código no plano:** o plano registra decisões (o quê, por quê), não a implementação em si. Não copie trechos de código no `{task-slug}.md` — se o código aparece no plano, o modelo tende a colar dali na hora de implementar em vez de olhar o projeto real. Descreva o resultado esperado (endpoint, campo, comportamento), não o código que o produz.
- **Registre o que foi descartado:** quando uma alternativa foi considerada e rejeitada durante a entrevista/brainstorming, anote isso explicitamente no plano (`~~Opção X~~ descartada: motivo`) — evita que o modelo a resuggira mais tarde por não saber que já foi avaliada e recusada.

## Planning Principles (NOT Templates!)

> 🔴 **NO fixed templates. Each plan is UNIQUE to the task.**

### Principle 1: Keep It SHORT

| ❌ Wrong                    | ✅ Right              |
| --------------------------- | --------------------- |
| 50 tasks with sub-sub-tasks | 5-10 clear tasks max  |
| Every micro-step listed     | Only actionable items |
| Verbose descriptions        | One-line per task     |

> **Rule:** If plan is longer than 1 page, it's too long. Simplify.

---

### Principle 2: Be SPECIFIC, Not Generic

| ❌ Wrong             | ✅ Right                                                 |
| -------------------- | -------------------------------------------------------- |
| "Set up project"     | "Run `npx create-next-app`"                              |
| "Add authentication" | "Install next-auth, create `/api/auth/[...nextauth].ts`" |
| "Style the UI"       | "Add Tailwind classes to `Header.tsx`"                   |

> **Rule:** Each task should have a clear, verifiable outcome.

---

### Principle 3: Dynamic Content Based on Project Type

**For NEW PROJECT:**

- What tech stack? (decide first)
- What's the MVP? (minimal features)
- What's the file structure?

**For FEATURE ADDITION:**

- Which files are affected?
- What dependencies needed?
- How to verify it works?

**For BUG FIX:**

- What's the root cause?
- What file/line to change?
- How to test the fix?

---

### Principle 4: Scripts Are Project-Specific

> 🔴 **DO NOT copy-paste script commands. Choose based on project type.**

| Project Type   | Relevant Scripts                          |
| -------------- | ----------------------------------------- |
| Frontend/React | `ux_audit.py`, `accessibility_checker.py` |
| Backend/API    | `api_validator.py`, `security_scan.py`    |
| Mobile         | `mobile_audit.py`                         |
| Database       | `schema_validator.py`                     |
| Full-stack     | Mix of above based on what you touched    |

**Wrong:** Adding all scripts to every plan
**Right:** Only scripts relevant to THIS task

---

### Principle 5: Verification is Simple

| ❌ Wrong                               | ✅ Right                                      |
| -------------------------------------- | --------------------------------------------- |
| "Verify the component works correctly" | "Run `npm run dev`, click button, see toast"  |
| "Test the API"                         | "curl localhost:3000/api/users returns 200"   |
| "Check styles"                         | "Open browser, verify dark mode toggle works" |

---

## Critérios de Aceite (Contrato de Aceite)

> Todo plano precisa de um contrato de aceite em linguagem simples antes de o trabalho começar — a especificação, não o código, é a fonte da verdade sobre "o que é entregar certo".

Escreva cada critério como uma frase "Quando [situação], o sistema deve [resultado esperado]". Isso é a versão em linguagem acessível do formato Given/When/Then (Gherkin/BDD) usado em Spec-Driven Development.

| ❌ Vago (não é um critério de aceite) | ✅ Contrato de aceite                                                                               |
| ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| "Login deve funcionar"                | "Quando o cliente digitar e-mail e senha corretos, o sistema deve abrir o painel em até 2 segundos" |
| "Tratar erro de pagamento"            | "Quando o pagamento for recusado, o sistema deve mostrar o motivo da recusa e não cobrar o cliente" |

Um critério sem "quando/deve" testável conta como placeholder (ver seção "No Placeholders") e reprova o plano.

## Nota Técnica: YAML para Dados Estruturados

Quando o plano precisar descrever dados estruturados (schema de config, contrato de API, modelo de dados), use um bloco YAML em vez de JSON dentro do plano — o agente processa YAML com mais precisão e menor custo de tokens. Texto corrido continua em Markdown normalmente; isso vale só para blocos de dados estruturados.

## Plan Structure (Flexible, Not Fixed!)

```
# [Task Name]

## Goal
One sentence: What are we building/fixing?

## Critérios de Aceite
- [ ] Quando [situação], o sistema deve [resultado esperado]
- [ ] Quando [situação], o sistema deve [resultado esperado]

## Tasks
- [ ] Task 1: [Specific action] → Verify: [How to check]
- [ ] Task 2: [Specific action] → Verify: [How to check]
- [ ] Task 3: [Specific action] → Verify: [How to check]

## Done When
- [ ] [Main success criteria]

## Notes
[Any important considerations — only if truly needed]
```

> **That's it.** No phases, no sub-sections unless truly needed.
> Keep it minimal. Add complexity only when required.

---

## No Placeholders

A plan with these is a plan failure, regardless of how short it is — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases" (name the actual check)
- "Similar to Task N" (repeat the actual content — a reader may hit tasks out of order)
- A verification step without a command and expected output

## Self-Review (Before Calling the Plan Done)

After writing the plan, check it against the original request with fresh eyes — this is a checklist you run yourself, not a separate pass:

1. **Coverage**: can you point to a task for every part of what was asked? List any gaps.
2. **Placeholder scan**: search the plan for the patterns above. Fix them inline.
3. **Consistency**: do names/paths used in later tasks match what earlier tasks defined? A function called `clearLayers()` in Task 2 but `clearFullLayers()` in Task 4 is a bug in the plan itself.

Fix issues inline as you find them — no need to re-run the whole review after a fix.

## Segunda Opinião (Opcional, planos de alto risco)

O Self-Review acima é o mesmo agente que escreveu o plano relendo o próprio raciocínio — não pega o próprio ponto cego. Para planos de risco real, use um segundo agente independente antes de apresentar o plano para aprovação do usuário.

**Quando disparar** (qualquer um destes, não todos):

- Classificado como COMPLEX CODE ou DESIGN pelo REQUEST_CLASSIFIER (DEVBUREAU.md) **e** toca 3+ arquivos.
- Algum passo do plano cai em "PERGUNTE"/"EXIGIR + TRADUÇÃO" na Matriz de Decisão (ação irreversível, produção, dados de cliente).
- `blast_radius.py` aponta risco HIGH em algum arquivo-alvo do plano (`.agent/SCRIPTS_REGISTRY.md`).
- O usuário pede explicitamente uma segunda opinião.

Fora desses casos, pule esta seção — não é gate obrigatório para planos simples; rodar sem necessidade é o mesmo desperdício de tokens que o Triple Gate do `loop-forge` evita para loops.

**Como rodar:**

1. Termine de escrever `{task-slug}.md` primeiro. O revisor nunca vê o seu raciocínio, só o artefato final e o pedido original do usuário (mesma disciplina do `triangulate-spec-review` do better-harness: contexto bruto, não a conclusão).
2. Dispare via `Agent` tool com `subagent_type: "Plan"` (esse tipo já não tem acesso a Edit/Write — a garantia de "revisor não edita" fica estrutural, não só uma instrução que pode ser ignorada) e `run_in_background: false` (o resultado bloqueia o próximo passo, não pode rodar em paralelo silenciosamente).
3. Prompt do revisor: cole o conteúdo de `{task-slug}.md` e o pedido original do usuário; peça achados classificados com o mesmo vocabulário do `code-review-checklist` (🔴 BLOCKING / 🟡 SUGGESTION / 🟢 NIT) aplicado ao PLANO, não a código — lacunas de entendimento do objetivo, limites de escopo não declarados, passo irreversível sem rollback, verificação sem comando concreto.
4. **Normalize:** corrija todo 🔴 BLOCKING antes de prosseguir. 🟡 SUGGESTION é opcional — aplique se barato, senão anote e siga. 🟢 NIT é ignorado por padrão.
5. O revisor nunca edita o plano nem o código — só a Plan/general-purpose agent que escreveu o plano aplica as correções, depois de comparar os achados.
6. Isso é uma camada adicional ao Socratic Gate, não um substituto: mesmo com zero 🔴 BLOCKING, o plano ainda espera a aprovação do usuário antes da implementação (DEVBUREAU.md, "Alignment de Workspace").

## Best Practices (Quick Reference)

1. **Start with goal** - What are we building/fixing?
2. **Max 10 tasks** - If more, break into multiple plans
3. **Each task verifiable** - Clear "done" criteria
4. **Project-specific** - No copy-paste templates
5. **Update as you go** - Mark `[x]` when complete

---

## When to Use

- New project from scratch
- Adding a feature
- Fixing a bug (if complex)
- Refactoring multiple files
