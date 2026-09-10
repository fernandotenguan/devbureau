# Plano Unificado de Evolução do DevBureau

**Base:** fusão de dois benchmarks independentes (PRD Gemini "Slim-Core & Zero-Prompt" v4.0.0-Draft e PRD Claude "Benchmark de Ecossistema" v1.0)
**Data:** 10 de setembro de 2026
**Baseline:** DevBureau v3.40.1, commit `a179d89`
**Método:** toda afirmação dos dois documentos foi conferida contra o repositório antes de entrar aqui. O que não deu para verificar está marcado.

---

## 1. Auditoria honesta dos dois documentos

### 1.1 O que o PRD do Gemini acertou e o outro não viu

| Achado | Verificação |
|---|---|
| `install_hooks.py` aborta em projetos derivados | **Confirmado.** Linhas 56 e 117 checam `KIT_MASTER_RULES.md`, que por desenho não é distribuído. O pre-commit nunca é instalado no projeto do usuário |
| Atrito de sincronização de documentação | **Confirmado.** `TestDocsSync` existe em `.agent/tests/test_kit_integrity.py:249` e bloqueia commit por contagem dessincronizada |
| Mapa AST do repositório (padrão Aider) | **Válido e é o achado mais forte do documento.** O outro PRD olhou só o custo das regras e ignorou o custo de descoberta, que na prática costuma ser maior |
| Regras com escopo por glob já existem para Cursor e Copilot, mas não para Claude, Codex e Antigravity | **Confirmado.** `.cursor/rules/` tem 5 arquivos segmentados, enquanto `CLAUDE.md`, `AGENTS.md` e `GEMINI.md` recebem o monólito de 40 KB |
| Test Impact Analysis reaproveitando `blast_radius.py` e `test_gap_check.py` | **Válido.** Usa o que já existe em vez de propor script novo |
| Micro-loop de auto-cura com teto rígido de 1 tentativa | **Válido.** Fecha uma lacuna real entre "erro trivial" e o Escape Protocol |

### 1.2 O que o PRD do Gemini errou ou exagerou

| Afirmação | Realidade |
|---|---|
| A1: "lint e formatação não rodam automaticamente" | **Incorreto na premissa.** `auto_fix_on_edit.py` existe e está registrado como `PostToolUse` em `.claude/settings.json`. Só que o Gemini chega à conclusão certa pelo motivo errado, ver seção 1.4 |
| "Queima até 300.000 tokens apenas lendo as regras base" | **Enganoso.** Ignora prompt caching: o bloco de regras é escrito no cache uma vez e as leituras seguintes custam uma fração. O custo real é ocupação de janela de contexto, não multiplicação linear por turno |
| TTFT de 3,5 a 6,0 segundos caindo para 1,2 a 2,2 segundos | **Não medido.** Precisão inventada, nenhum benchmark por trás |
| ROI de menos 53% de custo por sessão | **Construído sobre o erro de caching acima.** A direção é certa, o número não sustenta |
| Scores RICE (600, 243, 170...) | **Aritmética errada em 10x.** RICE é Reach × Impact × Confidence ÷ Effort: A6 dá 60, não 600. O fator de erro é constante, então a ordenação continua válida e a decisão não muda |
| "Claude 3.7/Opus, GPT-5, Gemini 1.5 Pro" | **Modelos desatualizados** para setembro de 2026, sinal de que o documento não foi ancorado no ambiente real |
| "11 hooks" | São 10 em `.agent/scripts/hooks/` |
| Repositórios `garrytan/gstack` e `DietrichGebert/ponytail` | **Não verificados.** A busca web falhou no momento da checagem. Aider, wshobson/agents, ECC e superpowers são reais e verificáveis |
| Teto de 1.000 tokens no arquivo raiz | **Direção certa, calibragem arriscada.** Cortar 91% das regras sem instrumento para saber quais regras funcionam pode destruir exatamente o diferencial do kit |

### 1.3 O que o PRD do Claude trouxe e o Gemini não cobriu

Sobrevivência à compactação (`PreCompact`), que é a lacuna mais grave do kit hoje e não aparece em nenhum ponto do documento do Gemini: sessão longa que compacta perde as regras em silêncio. Medição de aderência antes de podar regra, sem a qual o corte de 91% proposto vira aposta. Observabilidade de custo real por OTel, já que o Gemini projeta economia sem nunca medir. Telemetria automática de gate e roteamento, registro persistente de becos sem saída, CI validando o diff do PR, e rotação da camada de memória.

### 1.4 O achado que nenhum dos dois enunciou por inteiro

`.claude/settings.json` **não está na lista `files` do `package.json`** e o instalador `bin/devbureau.js` nunca o cria. Somado ao bloqueio de `install_hooks.py` que o Gemini identificou, a conclusão é que **toda a camada de automação do kit, os 10 hooks e o pre-commit, existe apenas no repositório fonte do DevBureau e nunca chega ao projeto do usuário.**

Isso reordena os dois roadmaps. Enquanto a distribuição não for resolvida, cada automação nova proposta nos dois documentos entrega valor zero para quem instala o kit. É por isso que a Fase 0 abaixo não existia em nenhum dos dois planos originais e agora vem antes de tudo.

### 1.5 Veredito comparativo

O documento do Gemini é mais forte em **descoberta de atrito operacional concreto** (hooks mortos em projetos derivados, sincronização de docs, custo de exploração de código) e propõe o melhor item isolado dos dois, o mapa AST. O documento do Claude é mais forte em **rigor de evidência e sequenciamento** (mediu antes de afirmar, e insiste em instrumentar antes de cortar). O Gemini tem números que não sustentam auditoria; o Claude tem um ponto cego que custou caro, ignorou completamente o custo de descoberta de código e olhou só o tamanho dos arquivos de regra.

---

## 2. Plano unificado

Origem de cada item: **[G]** Gemini, **[C]** Claude, **[G+C]** ambos, **[N]** novo, surgido da verificação cruzada.

### Fase 0. Fazer a automação existir no projeto do usuário

Sem isso, nada mais importa. Estimativa: 1 dia.

| # | Item | Origem |
|---|---|---|
| 0.1 | Incluir `.claude/settings.json` na distribuição, com merge não destrutivo caso o projeto já tenha um | **[N]** |
| 0.2 | Destravar `install_hooks.py` em projetos derivados: sem `KIT_MASTER_RULES.md`, instalar o pre-commit apontando para `checklist.py --pre-commit` em vez de abortar | **[G]** |
| 0.3 | Teste de integridade que falha se a camada de hooks deixar de ser distribuída, para o problema não voltar | **[N]** |

**Critério de aceite.** Projeto novo criado com `npx devbureau init` tem hooks ativos e pre-commit funcionando, comprovado por uma edição que dispara formatação e um commit com segredo que é bloqueado.

### Fase 1. Ganhos imediatos de baixo risco

Estimativa: 2 dias.

| # | Item | Origem |
|---|---|---|
| 1.1 | Hook `PreCompact` reinjetando o núcleo de regras e o estado da tarefa | **[C]** |
| 1.2 | `sync_docs.py`, recontagem determinística de agentes, skills, workflows e scripts em README, README_pt-BR, ARCHITECTURE e package.json | **[G]** |
| 1.3 | CI validando o diff do PR (`checklist.py --pre-commit`, varredura de segredo, `doc_drift_check.py`) | **[C]** |
| 1.4 | Rotação da camada de memória, com arquivos ativos abaixo de 50 KB e arquivo morto pesquisável | **[C]** |
| 1.5 | Bloqueios de segurança que hoje são só texto: proteção de teste contra remoção, guarda da branch principal, varredura de segredo antes de gravar | **[C]** |
| 1.6 | Checkpoint git automático antes de tarefa complexa, para reversão em um comando | **[G]** |
| 1.7 | Micro-loop de auto-cura com teto de 1 tentativa, encadeado no Escape Protocol existente | **[G]** |

### Fase 2. Atacar o custo de descoberta, que é o maior e o menos medido

Estimativa: 2 a 3 dias. Esta fase é a contribuição central do documento do Gemini.

| # | Item | Origem |
|---|---|---|
| 2.1 | `repo_map.py`, mapa AST de símbolos com teto explícito de tokens, para Python e TypeScript ou JavaScript | **[G]** |
| 2.2 | Test Impact Analysis reaproveitando `blast_radius.py` e `test_gap_check.py`, rodando só o teste afetado | **[G]** |
| 2.3 | Cache de perfil de stack detectado uma vez por projeto, em vez de redetectar por sessão | **[G]** |
| 2.4 | Ranking de custo de contexto por arquivo, para saber o preço do que foi lido | **[C]** |

**Observação de calibragem.** O teto de 1.024 tokens do Aider é referência, não meta cega. O critério de aceite correto é comparativo: o mapa precisa reduzir de forma comprovada as chamadas de exploração em uma amostra de tarefas reais, e não apenas caber num número.

### Fase 3. Medir antes de cortar

Estimativa: 3 dias. Esta fase é a contribuição central do documento do Claude, e ela precede a Fase 4 por decisão explícita.

| # | Item | Origem |
|---|---|---|
| 3.1 | Placar de aderência às regras, quantas vezes cada regra verificável foi de fato cumprida | **[C]** |
| 3.2 | Telemetria automática de gate e roteamento via `UserPromptSubmit` e `Stop` | **[C]** |
| 3.3 | Observabilidade de custo real, OTel opt-in mais relatório local por tipo de tarefa | **[C]** |
| 3.4 | Registro persistente de becos sem saída, alimentando a Loop Protection com dados | **[C]** |
| 3.5 | Memória de supressão de perguntas repetidas do Socratic Gate | **[G]**, e já existe parcialmente em `question-preferences.md`, falta automatizar a escrita |

### Fase 4. Slim-Core, agora com evidência

Estimativa: 2 dias.

| # | Item | Origem |
|---|---|---|
| 4.1 | Micro-kernel na raiz mais divulgação progressiva do restante, com o corte guiado pelos dados da Fase 3 | **[G+C]** |
| 4.2 | Regras com escopo por glob estendidas a Claude, Codex e Antigravity, replicando o que já funciona no Cursor | **[G]** |
| 4.3 | Workflow `/converge`, reconciliação entre a spec e o código realmente entregue | **[C]** |
| 4.4 | Camada de override por projeto para workflows | **[C]** |
| 4.5 | Distribuição como plugin de marketplace | **[G+C]** |

**Resolução do conflito de metas.** O Gemini propõe teto fixo de 1.000 tokens; a proposta unificada é meta escalonada com portão de qualidade: cortar para 6.000 tokens, medir aderência e comportamento em amostra real, e só então avançar para 3.000 e depois para 1.500. Se em qualquer degrau a taxa de aderência ou o roteamento de agente regredir, o corte para naquele degrau. A meta é comportamento preservado ao menor custo, não um número de tokens.

---

## 3. Métricas unificadas

| Métrica | Hoje | Meta | Como medir |
|---|---|---|---|
| Projetos derivados com hooks ativos | 0% | 100% | Teste de integridade da Fase 0 |
| Tokens fixos por sessão (Claude Code) | 10.355 | 6.000, depois 3.000 com portão de qualidade | `token_footprint.py` |
| Chamadas de exploração por tarefa complexa | não medido | queda comprovada em amostra pareada | Contagem antes e depois da Fase 2 |
| Regras com aderência medida | 0 | 100% das verificáveis | Placar da Fase 3 |
| Sessões que sobrevivem à compactação | não medido | 100% mantêm o protocolo | Teste manual com compactação forçada |
| Custo por tipo de tarefa | não medido | medido e comparado ao Task Budget | Relatório da Fase 3 |
| Commit bloqueado por doc dessincronizada | recorrente | zero | `sync_docs.py` |

Nenhuma meta de economia percentual entra aqui antes de existir medição. Foi exatamente esse atalho que produziu os números frágeis do documento original.

---

## 4. Riscos do plano combinado

O risco dominante é ambição de escopo: somados, os dois documentos propõem cerca de 25 itens, e executar tudo de uma vez transforma o kit em canteiro de obras. As fases são sequenciais de propósito, e cada uma tem valor autônomo se o trabalho parar ali.

O segundo risco é excesso de hook degradando a latência de cada chamada de ferramenta, o que exige que todo hook novo meça o próprio tempo e aborte rápido.

O terceiro é o mais desconfortável: o placar de aderência da Fase 3 pode revelar que boa parte das 40 KB de regras é ignorada na prática. Isso não invalida o kit, mas muda a natureza do trabalho, de "escrever mais regra" para "manter menos regra e fazê-la valer".

---

## 5. Recomendação

Aprovar Fase 0 e Fase 1 agora, num bloco de 3 dias. A Fase 0 é o que converte todo o resto em valor real para quem usa o kit, e a Fase 1 fecha as lacunas de risco sem tocar em nenhuma regra de conteúdo. A Fase 2 vem em seguida por ser o maior ganho de eficiência ainda não explorado. As Fases 3 e 4 formam um par indivisível: medir e então cortar, nessa ordem.
