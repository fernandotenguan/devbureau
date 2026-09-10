# PRD: Benchmark de Ecossistema e Plano de Evolução do DevBureau

**Versão:** 1.0
**Data:** 10 de setembro de 2026
**Baseline auditado:** DevBureau v3.40.1 (commit `a179d89`)
**Autor:** análise de benchmark competitivo do ecossistema open source de agentes

---

## 1. Resumo executivo

O DevBureau já está no percentil alto do ecossistema em profundidade de regras (23 agentes, 78 skills, 29 workflows, 16 scripts determinísticos), mas paga um custo fixo alto e mede pouco: cada sessão do Claude Code carrega cerca de 10.355 tokens de regras antes de qualquer trabalho, e a instrução global manda ler de novo o mesmo conteúdo em `.agent/rules/DEVBUREAU.md` (mais 9.948 tokens), o que dobra o custo de partida sem ganho de comportamento.

O segundo problema é de eficácia, não de custo: boa parte das garantias do kit (telemetria de gate, log de roteamento, registro de lições, validação seletiva antes de encerrar) depende da disciplina do modelo em seguir texto, e não de automação que executa sozinha. Os projetos líderes de 2026 resolveram exatamente isso movendo regra para hook, e o DevBureau usa apenas 3 dos 12 eventos de ciclo de vida disponíveis.

**Decisão pedida ao usuário:** aprovar a Onda 1 do roadmap (seção 8), que corta o custo de entrada de sessão e liga 6 automações seguras, sem alterar nenhuma regra de conteúdo do kit.

---

## 2. Escopo, método e suposições

### 2.1 Escopo

Avaliar projetos open source recentes e relevantes de engenharia com agentes e identificar o que o DevBureau deveria absorver em três eixos: **eficiência** (menos tokens e menos passos para o mesmo resultado), **eficácia** (a regra realmente muda o comportamento) e **custo** (previsibilidade e observabilidade do gasto). Em paralelo, mapear tarefas que hoje o usuário precisa pedir toda vez e que poderiam já vir configuradas de fábrica, desde que sejam seguras e reversíveis.

### 2.2 Método

1. Auditoria do repositório atual com medição real, não estimativa (`token_footprint.py`, inventário de arquivos, leitura de `settings.json` e do workflow de CI).
2. Levantamento do ecossistema em setembro de 2026, priorizando projetos com adoção comprovada ou mecanismo tecnicamente reaproveitável.
3. Comparação item a item contra o baseline, descartando o que o DevBureau já resolve (para não propor trabalho morto).
4. Priorização por impacto sobre esforço, com critério de aceite verificável para cada item.

### 2.3 Suposições declaradas

Como o pedido não fixou restrições, este PRD assume que: o Claude Code continua sendo o ambiente principal (as demais IDEs são alvos de sincronização, não de otimização primária); o kit permanece distribuído por npm e deve continuar funcionando em projetos derivados; nenhuma proposta pode exigir serviço pago externo obrigatório; e retrocompatibilidade das regras existentes é inegociável. Se alguma dessas premissas estiver errada, a priorização da seção 6 muda.

---

## 3. Baseline medido (fatos, não impressões)

| Dimensão | Estado atual | Evidência |
|---|---|---|
| Custo fixo por sessão (Claude Code) | ~10.355 tokens | `token_footprint.py` sobre `.claude/CLAUDE.md` |
| Custo fixo duplicado | +9.948 tokens | Instrução global manda ler `.agent/rules/DEVBUREAU.md`, que é a fonte de onde `CLAUDE.md` foi gerado |
| Eventos de hook usados | 3 de 12 (PreToolUse, PostToolUse, SessionStart) | `.claude/settings.json` |
| Hooks implementados | 10 | `.agent/scripts/hooks/` |
| Agentes / skills / workflows / scripts | 23 / 78 / 29 / 16 | Inventário do `.agent/` |
| Cobertura de CI | `doctor.py` mais um arquivo de teste de integridade | `.github/workflows/kit-validation.yml` |
| Observabilidade de custo real | Inexistente | Nenhuma configuração OTel, nenhum relatório de sessão |
| Medição de aderência às regras | Inexistente | `gate-telemetry.md` e `routing-telemetry.md` dependem de escrita manual pelo modelo |
| Crescimento da camada de memória | Sem rotação | `pattern-mining-log.md` 143 KB, `benchmark-log.md` 105 KB |
| Distribuição como plugin | Ausente | Não existe `.claude-plugin/marketplace.json`, só `bin/devbureau.js` via npm |
| Higiene de skills | Boa | 78 de 78 skills com frontmatter `name` e `description` válidos |

**Leitura:** a arquitetura de conhecimento está madura. A camada de execução automática e a camada de medição estão atrasadas em relação ao estado da arte.

---

## 4. Painel comparativo do ecossistema

| Projeto | O que ele faz melhor | Aplicável ao DevBureau |
|---|---|---|
| **obra/superpowers** (framework de skills, líder de adoção) | Hook de pós compactação que reinjeta as instruções de bootstrap; ciclo obrigatório brainstorm, worktree, plano, subagente com TDD, review por agente novo, fechamento de branch | **Alto.** O hook `PreCompact` é a lacuna mais crítica: hoje, sessão longa que compacta perde as regras P0 do kit silenciosamente |
| **github/spec-kit** (v1.0.1, MIT) | Hierarquia de customização em runtime (overrides do projeto vencem presets, que vencem extensions, que vencem o core) e o comando `/converge`, que reconcilia o código real contra a spec e gera as tarefas faltantes | **Alto.** O DevBureau tem 29 workflows fixos e nenhuma camada de override por projeto, e não tem passo de reconciliação entre spec e implementação |
| **OpenSpec contra BMAD-METHOD** (benchmark Reenbit: 12 minutos contra 5,5 horas na mesma tarefa) | Prova de que gate pesado custa caro e que o peso do processo deve ser proporcional ao risco | **Confirmatório.** O Fast-Track do DEVBUREAU.md já é a resposta certa; o que falta é medir se ele está sendo usado |
| **karanb192/claude-code-hooks** (marketplace de hooks) | Catálogo pronto de hooks de segurança, custo, observabilidade e produtividade, com destaque para `dead-rules-audit` (placar de quais regras do CLAUDE.md o agente segue e quais ignora), `context-hogs` (ranking de custo de contexto por arquivo) e `dead-end-registry` (memória de abordagens que falharam) | **Muito alto.** Três mecanismos que atacam diretamente eficácia, custo e loop protection do kit |
| **ColeMurray/claude-code-otel** e o OTel nativo do Claude Code | Custo por sessão, tokens por tipo, latência por ferramenta e atribuição por modelo, tudo opt-in com duas variáveis de ambiente | **Médio alto.** Transforma otimização de custo de opinião em número |
| **ReminDB** e a família de memória em SQLite | Memória estruturada com recuperação por relevância, em vez de markdown crescendo sem limite | **Médio.** O `memory_recall.py` já é o caminho certo, falta rotação e limite de tamanho |
| **Agent OS** (Brian Casel) | Codificação de convenções da casa para o agente parar de reinventar padrões do projeto existente | **Baixo.** O DevBureau já cobre isso com agentes e skills |
| **claude-context-mode** (MCP de compressão, 315 KB para 5,4 KB) | Compressão da saída de ferramenta antes de entrar no contexto | **Baixo.** Já previsto de forma condicional via `mcp__headroom__*` |

---

## 5. Gaps identificados

Organizados por eixo. Cada gap vira uma epic na seção 6.

**Eficiência de contexto**

- G1. Duplicação do corpo de regras entre `CLAUDE.md` e `DEVBUREAU.md` na mesma sessão.
- G2. Ausência de reinjeção após compactação, o que faz sessões longas degradarem para comportamento genérico.
- G3. Nenhum ranking de quais arquivos mais consomem contexto durante o trabalho real.

**Eficácia**

- G4. Regras que só existem como texto e dependem de disciplina: telemetria de gate, log de roteamento, validação seletiva antes de encerrar, registro de lições.
- G5. Nenhuma medida de quais das cerca de 40 KB de regras o modelo de fato segue, o que impede podar regra morta com segurança.
- G6. Loop protection é heurística de texto, sem registro persistente de abordagens que já falharam.
- G7. Nenhum passo de reconciliação entre o que foi especificado e o que foi implementado.

**Custo e governança**

- G8. Zero observabilidade de gasto real por sessão ou por tipo de tarefa.
- G9. Camada de memória cresce sem rotação, com risco de virar custo permanente.
- G10. CI valida integridade do kit, mas não valida o diff de um PR com o próprio `checklist.py`.
- G11. Automações de segurança existem como regra escrita, não como bloqueio efetivo: proteção de testes, guarda da branch principal, varredura de segredo antes de gravar.

---

## 6. Epics propostas

### E1. Desduplicação do carregamento de regras

**Problema.** `CLAUDE.md` (10.355 tokens) é gerado a partir de `DEVBUREAU.md` (9.948 tokens) e contém o mesmo corpo, e a instrução global manda ler o segundo no início de toda sessão, pagando o conteúdo duas vezes.

**Proposta.** `CLAUDE.md` passa a ser o único ponto de carga automática e deixa de embutir o corpo inteiro: mantém o P0 essencial (classificador, gate, matriz de decisão, diretrizes de estilo) e referencia sob demanda as seções longas, que ficam em `reference/`. A instrução de ler `DEVBUREAU.md` ao iniciar é substituída por "as regras já estão carregadas, leia `reference/` apenas quando a seção for citada".

**Critério de aceite.** `token_footprint.py` reporta abaixo de 6.000 tokens para o alvo Claude Code, e uma amostra de 10 tarefas mistas não apresenta regressão de comportamento (o mesmo agente é escolhido, o gate dispara nos mesmos casos).

**Esforço.** Médio. Toca `sync_ide.py` e a organização de `.agent/rules/`.

**Risco.** Médio: cortar demais degrada aderência. Mitigado pela E2, que mede antes da poda.

### E2. Placar de aderência às regras

**Problema.** Não existe evidência sobre quais regras mudam comportamento. Sem isso, toda poda é chute e toda regra nova é aposta.

**Proposta.** Hook em `SessionStart`, `PostToolUse` e `SessionEnd` que registra, por sessão, quais regras verificáveis foram cumpridas (anúncio de agente presente, gate disparado quando o tipo exigia, `auto_fixer` executado antes de finalizar, evidência fresca antes de alegar conclusão) e grava em `.agent/memory/rule-adherence.md`. Relatório agregado via `python .agent/scripts/doctor.py --adherence`.

**Critério de aceite.** Após 20 sessões, o relatório lista as regras com taxa de cumprimento abaixo de 50%, que viram candidatas a reescrita ou remoção.

**Esforço.** Médio. **Risco.** Baixo, é observação e não bloqueio.

### E3. Sobrevivência à compactação

**Problema.** Sessão longa que compacta perde o kit e volta a se comportar como agente genérico, sem aviso.

**Proposta.** Hook `PreCompact` que reinjeta um núcleo mínimo (identidade do kit, classificador, matriz de decisão, protocolo de evidência) mais o estado da tarefa corrente, a exemplo do que o superpowers faz.

**Critério de aceite.** Sessão forçada a compactar mantém o anúncio de agente e o protocolo de evidência na tarefa seguinte.

**Esforço.** Baixo. **Risco.** Baixo.

### E4. Telemetria automática de gate e roteamento

**Problema.** `gate-telemetry.md` e `routing-telemetry.md` só são preenchidos se o modelo lembrar. É o caso clássico de tarefa determinística presa em prosa.

**Proposta.** Hook `UserPromptSubmit` classifica o pedido e registra o tipo detectado; hook `Stop` fecha a linha com o agente efetivamente usado e se o gate disparou. O modelo só complementa o julgamento qualitativo (a pergunta valeu?), que é a parte que realmente exige raciocínio.

**Critério de aceite.** 100% das interações COMPLEX CODE e DESIGN geram linha de telemetria sem intervenção do modelo.

**Esforço.** Médio. **Risco.** Baixo.

### E5. Registro de becos sem saída

**Problema.** A Loop Protection detecta repetição dentro da sessão, mas nada impede repetir na semana seguinte a abordagem que já falhou.

**Proposta.** Registrar abordagem falha (comando, erro, arquivo) em `.agent/memory/dead-ends.md`, com recuperação automática por gatilho no início da tarefa via `memory_recall.py`.

**Critério de aceite.** Repetir uma abordagem já registrada produz aviso antes da execução, com o custo estimado da tentativa anterior.

**Esforço.** Médio. **Risco.** Baixo.

### E6. Observabilidade de custo real

**Problema.** O kit fala de economia de tokens em todo lugar e nunca mede a sessão real, só o tamanho de arquivos estáticos.

**Proposta.** Opt-in de OTel documentado em uma linha de configuração, mais um `cost_report.py` local que lê os logs de sessão e produz custo por tipo de tarefa do REQUEST CLASSIFIER, cruzando com o Task Budget que já existe em `session_manager.py budget`.

**Critério de aceite.** Relatório semanal mostrando custo médio por tipo de tarefa e desvio contra o teto de tool calls.

**Esforço.** Médio. **Risco.** Baixo, estritamente opt-in e sem envio externo por padrão.

### E7. Ranking de custo de contexto por arquivo

**Problema.** A regra de Context Scoping Discipline pede leitura estreita sem nunca mostrar o preço do que foi lido.

**Proposta.** Hook `PostToolUse` que atribui o custo aproximado de cada resultado de ferramenta aos arquivos carregados e gera um ranking por sessão.

**Critério de aceite.** Ao fim da sessão, lista dos 5 arquivos mais caros; arquivos recorrentes no topo viram candidatos a divisão ou a resumo indexado.

**Esforço.** Baixo. **Risco.** Baixo.

### E8. Camada de override por projeto

**Problema.** Os 29 workflows são fixos. Projeto derivado que precisa de variação hoje edita o kit, o que quebra a atualização.

**Proposta.** Resolução em cascata inspirada no spec-kit: `.agent/overrides/` do projeto vence `.agent/workflows/` do kit, e `sync_ide.py` passa a respeitar a cascata.

**Critério de aceite.** Um projeto derivado customiza `/deploy` sem tocar em arquivo do kit e continua atualizando por npm sem conflito.

**Esforço.** Médio alto. **Risco.** Médio, exige teste de integridade novo.

### E9. Passo de convergência

**Problema.** O kit produz `{task-slug}.md` para trabalho complexo e nunca volta para conferir se o código entregue corresponde ao que foi especificado.

**Proposta.** Workflow `/converge` que compara a spec ativa contra o estado real do código e anexa as tarefas remanescentes, em vez de declarar sucesso por otimismo.

**Critério de aceite.** Rodar `/converge` sobre uma tarefa parcialmente implementada lista o que falta, com `arquivo:linha`.

**Esforço.** Médio. **Risco.** Baixo.

### E10. Rotação da camada de memória

**Problema.** `pattern-mining-log.md` com 143 KB e `benchmark-log.md` com 105 KB tendem a crescer sem teto.

**Proposta.** Política de rotação: acima de um limite, entradas antigas vão para `archive/` e permanecem pesquisáveis por `memory_recall.py`, mas saem do caminho de leitura padrão.

**Critério de aceite.** Nenhum arquivo ativo de memória acima de 50 KB, com a busca continuando a encontrar entradas arquivadas.

**Esforço.** Baixo. **Risco.** Baixo.

### E11. CI que valida o diff, não só o kit

**Problema.** O CI roda `doctor.py` e um arquivo de teste. Um PR que introduz segredo, quebra lint ou some com um teste passa.

**Proposta.** Adicionar ao workflow: `checklist.py --pre-commit` sobre os arquivos do diff, varredura de segredo, e verificação de deriva de documentação com o `doc_drift_check.py` que já existe.

**Critério de aceite.** PR com segredo hardcoded ou lint quebrado falha o CI.

**Esforço.** Baixo. **Risco.** Baixo.

### E12. Distribuição como plugin do Claude Code

**Problema.** A instalação é por npm e cópia de arquivos, enquanto o ecossistema convergiu para marketplace de plugins, que resolve atualização e descoberta.

**Proposta.** Publicar um `.claude-plugin/marketplace.json` expondo skills, agentes e comandos do kit, mantendo o npm como caminho alternativo.

**Critério de aceite.** Instalação do kit em um projeto novo por comando de plugin, sem cópia manual.

**Esforço.** Médio. **Risco.** Baixo.

---

## 7. Catálogo de automações seguras de fábrica

Esta é a resposta direta a "o que o usuário não deveria precisar pedir toda vez". O critério de inclusão foi rigoroso: só entra automação **reversível, local e sem custo de aprovação**. Nada aqui publica, apaga ou gasta dinheiro.

| # | Automação | Evento | Por que é segura | Status hoje |
|---|---|---|---|---|
| A1 | Formatar e corrigir lint no arquivo editado | PostToolUse | Alteração local, revertida por git | **Já existe** (`auto_fix_on_edit.py`) |
| A2 | Bloquear `--no-verify` e comandos destrutivos | PreToolUse | Só bloqueia, nunca executa | **Já existe** (`block_no_verify.py`) |
| A3 | Varrer conteúdo lido em busca de injeção de prompt | PostToolUse | Só alerta | **Já existe** (`scan_injection.py`) |
| A4 | Reinjetar núcleo de regras após compactação | PreCompact | Só adiciona contexto | **Falta** (E3) |
| A5 | Recuperar memória relevante pelo texto do pedido | UserPromptSubmit | Leitura local, sem escrita | **Falta** |
| A6 | Registrar telemetria de gate e roteamento | UserPromptSubmit e Stop | Escreve só em `.agent/memory/` | **Falta** (E4) |
| A7 | Validação seletiva do que mudou antes de encerrar o turno | Stop | Só reporta, não corrige sozinho | **Falta** |
| A8 | Impedir apagar, renomear ou desabilitar teste durante correção | PreToolUse | Bloqueio com escape explícito do usuário | **Falta** |
| A9 | Exigir branch antes de editar na `main` | PreToolUse | Só interrompe e sugere `git checkout -b` | **Falta** |
| A10 | Varrer segredo antes de gravar arquivo | PreToolUse | Bloqueio local | **Falta** (existe script, não como hook) |
| A11 | Instalar o pre-commit do kit no primeiro uso | SessionStart | Hook de git local, removível | **Falta** (existe `install_hooks.py` manual) |
| A12 | Ranking de custo de contexto por arquivo | PostToolUse e SessionEnd | Só mede | **Falta** (E7) |
| A13 | Registrar lição e beco sem saída ao fim da sessão | SessionEnd | Escrita local em memória | **Falta** (E5) |
| A14 | Rotacionar memória ao cruzar limite de tamanho | SessionEnd | Move para `archive/`, não apaga | **Falta** (E10) |
| A15 | Checagem de deriva de documentação após feature concluída | Stop | Só reporta | **Falta** (script existe, não automatizado) |

**Regra de governança para o catálogo:** toda automação nova precisa declarar o evento, o que escreve, e como o usuário desliga. Automação que não pode ser desligada em uma linha não entra.

### Explicitamente fora do escopo automático

Commit automático sem pedido, push, deploy, alteração de segredo, e qualquer escrita fora de `.agent/memory/` e dos arquivos que o usuário pediu para mudar. Isso preserva a Matriz de Decisão que já está no DEVBUREAU.md, e o motivo é simples: automação que publica transforma erro de agente em incidente de produção.

---

## 8. Roadmap

**Onda 1, custo e sobrevivência (impacto imediato, risco baixo).** E3 (PreCompact), E7 (custo de contexto), E10 (rotação de memória), E11 (CI sobre o diff), mais as automações A4, A5, A7, A8, A9 e A10. Resultado esperado: sessões longas param de degradar, o CI passa a proteger o diff, e as garantias de segurança viram bloqueio em vez de texto.

**Onda 2, medição antes da poda.** E2 (placar de aderência), E4 (telemetria automática), E6 (custo real), E5 (becos sem saída). Resultado esperado: dados suficientes para decidir o que cortar em `DEVBUREAU.md` sem chute.

**Onda 3, estrutura.** E1 (desduplicação de regras, agora guiada pelos dados da Onda 2), E9 (`/converge`), E8 (overrides por projeto), E12 (plugin).

A ordem é deliberada: **E1 vem depois de E2**, porque cortar 4.000 tokens de regra sem saber quais regras funcionam é economia que pode custar qualidade.

---

## 9. Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Tokens fixos por sessão (Claude Code) | 10.355 | abaixo de 6.000 |
| Eventos de hook cobertos | 3 de 12 | 7 de 12 |
| Interações COMPLEX CODE com telemetria registrada | indeterminado, provavelmente baixo | acima de 95% |
| Regras com aderência medida | 0 | 100% das regras verificáveis |
| Maior arquivo ativo de memória | 143 KB | abaixo de 50 KB |
| PR que passa no CI com segredo ou lint quebrado | possível | impossível |
| Custo médio por tipo de tarefa | não medido | medido e comparado ao Task Budget |

---

## 10. Riscos e não objetivos

**Riscos.** Excesso de hook degrada a latência de cada chamada de ferramenta, então cada hook novo precisa medir seu próprio tempo de execução e abortar rápido. Bloqueio mal calibrado trava o trabalho, então A8, A9 e A10 nascem com escape explícito documentado. E o risco mais sutil: medir aderência pode revelar que parte substancial das regras é ignorada, o que é desconfortável, mas é exatamente a informação que justifica o projeto.

**Não objetivos.** Não é objetivo adotar BMAD, spec-kit ou superpowers como framework, a proposta é absorver mecanismos específicos e comprovados. Não é objetivo adicionar dependência paga. Não é objetivo reescrever agentes ou skills, cuja qualidade a auditoria confirmou.

---

## 11. Fontes

- [obra/superpowers](https://github.com/obra/superpowers/)
- [github/spec-kit](https://github.com/github/spec-kit)
- [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)
- [ColeMurray/claude-code-otel](https://github.com/ColeMurray/claude-code-otel)
- [radimsem/remindb](https://github.com/radimsem/remindb)
- [BMAD vs Spec Kit vs OpenSpec, comparativo 2026](https://medium.com/@reenbit/bmad-vs-spec-kit-vs-openspec-choosing-your-spec-driven-ai-framework-in-2026-a6996b3ebb8d)
- [2026 AI Specification Frameworks Compared](https://docs.bswen.com/blog/2026-08-07-ai-spec-frameworks-compared/)
- [Claude Code Hooks, padrões de produção 2026](https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns)
- [Monitoring Claude Code with OpenTelemetry](https://www.dash0.com/guides/monitoring-claude-code-opentelemetry)
- [Anthropic, enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)
