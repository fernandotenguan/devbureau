📄 PRD MESTRE: DevBureau 4.0 — Slim-Core, Ciclo de Vida Resiliente & Automações Zero-Prompt
Versão: 4.0.0-Unified
Data: 10 de setembro de 2026
Baseline auditado: DevBureau v3.40.1
Autor: Engenharia de Produto & Arquitetura de Agentes (Síntese Unificada)
Status: Pronto para Execução

1. Visão Geral & Oportunidade Estratégica
O DevBureau atingiu excelência em sua base de conhecimento estruturada (23 agentes, 78 skills, 29 workflows). No entanto, o custo e o atrito operacional de operá-lo no dia a dia revelam quatro ineficiências críticas:

[ Os 4 Gargalos Operacionais do DevBureau ]
 ├── 1. O Custo Fixo de Entrada & Duplicação
 │    ├── CLAUDE.md / AGENTS.md = ~10.355 tokens
 │    └── Instrução redundante de ler DEVBUREAU.md = +9.948 tokens (Total: ~20k tokens no boot!)
 ├── 2. A "Amnésia" de Sessão Longa
 │    └── Ao compactar o contexto, o harness descarta as regras P0 e volta ao comportamento genérico
 ├── 3. "Regras em Prosa" vs. "Automações Determinísticas"
 │    └── Telemetria, auditoria de docs, lints, checagem de testes e sanitização dependem de o agente
 │        lembrar de executar, em vez de rodarem automaticamente por eventos de ciclo de vida.
 └── 4. A Camada de Automação Não Chega ao Usuário (BLOQUEADOR)
      ├── CORRIGIDO em 10/09/2026 após teste em ambiente limpo: os hooks do Claude Code JÁ chegam
      │   ao projeto derivado. sync_ide.py é distribuído dentro de .agent/ e sua função
      │   ensure_claude_protect_hook() faz o merge não destrutivo de hooks e permissões em
      │   .claude/settings.json sempre que o alvo claude é sincronizado.
      ├── O que resta de real: install_hooks.py aborta sem KIT_MASTER_RULES.md, então o
      │   .git/hooks/pre-commit nunca é instalado no projeto do usuário (verificado com git init).
      └── Resíduo menor: quem sincroniza apenas um alvo que não seja o Claude fica sem hooks
          registrados até rodar sync_ide.py com o alvo claude.
O Objetivo do PRD Unificado:
Criar um ambiente de desenvolvimento enxuto, resiliente e autônomo, onde o agente opera com menos de 6.000 tokens de contexto inicial na Onda 1, podendo cair mais se o portão de qualidade permitir, mantém suas diretrizes vivas mesmo após compactação de sessão, descobre o código em 1 comando (<1k tokens) e executa tarefas de rotina de forma segura sem intervenção manual do usuário.

2. Matriz de Síntese: Unificação das Propostas
Eixo / Desafio	Contribuição do Claude	Contribuição da Nossa Análise	Solução Unificada no PRD Final
Custo de Regras no Boot	Identificou a duplicação literal entre CLAUDE.md e DEVBUREAU.md na mesma sessão (~20k tokens).	Propôs arquitetura Progressive Disclosure e regras Glob-Scoped (à la Cursor/Copilot e wshobson/agents).	Desduplicação Imediata: Remove a ordem de ler DEVBUREAU.md no boot (economia imediata de ~10k tokens). Prepara modularização em reference/ guiada por telemetria.
Sobrevivência de Sessão	Identificou a perda de regras em sessões longas e propôs o hook PreCompact.	Focou no Task Budget e Loop Protection por tipo de requisição.	Hook PreCompact + Estado Ativo: Reinjeção determinística do Micro-Kernel P0 + estado da tarefa ao ocorrer compactação.
Descoberta de Código	Propôs ranking de custo de contexto por arquivo lido (context-hogs).	Propôs Universal AST Repo Map (<1k tokens via Python AST / Tree-sitter à la Aider).	Descoberta em 2 Frentes: O agente recebe a árvore AST compacta no início da tarefa; um hook mede quais arquivos lidos foram caros demais para guiar refatorações.
Eficácia de Regras	Placar de Aderência: Medir o que o agente de fato cumpre antes de podar regras no chute.	Foco em Self-Healing (auto-correção de 1 ciclo em erros de compilação/lint).	Medição Antes da Poda: Rastrear aderência de regras por 20 sessões para saber exatamente quais partes de DEVBUREAU.md podem ser arquivadas com segurança.
Automação do Repositório	Hooks de ciclo de vida (UserPromptSubmit, Stop, SessionEnd, bloqueio de deleção de teste).	sync_docs.py (fim das falhas no TestDocsSync) e pre-commit ativo para projetos derivados.	Arsenal Completo de 17 Automações Seguras cobrindo ciclo de vida, pre-commit e documentação.
Governança de Memória	Rotação de logs (benchmark-log.md, pattern-mining-log.md > 50KB).	Memória de preferências persistentes (supressão do Socratic Gate plan-tune).	Camada de Memória Higiênica: Rotação automática para archive/ com indexação leve via 

memory_recall.py
.
3. Catálogo Unificado de 17 Automações Seguras "Zero-Prompt"
Todas as automações incluídas são 100% locais, reversíveis e de baixo risco. Nenhuma automação deste catálogo faz commit sem pedido, push para servidor remoto ou exclusão destrutiva.

[ Matriz de Segurança de Automações ]
 ├── REVERSÍVEL & LOCAL   ──────► ✅ EXECUÇÃO AUTOMÁTICA SILENCIOSA (Zero-Prompt)
 ├── ESCRITA EM MEMÓRIA   ──────► ✅ ATUALIZAÇÃO DETERMINÍSTICA EM SEGUNDO PLANO
 └── REMOTO / DESTRUTIVO  ──────► 🛑 EXIGE APROVAÇÃO HUMANA (Matriz de Decisão)
#	Automação	Evento de Disparo	Ação Executada	Mecanismo de Segurança / Reversibilidade
A1	Auto-Fix & Format Pós-Edição	PostToolUse (Edit/Write)	Roda silenciosamente auto_fixer.py no arquivo alterado.	Reversível via git diff local; limpa formatações e imports nulos.
A2	Proteção de Testes Existentes	PreToolUse (Edit/Write/Bash)	Bloqueia comandos que apaguem ou comentem testes unitários para mascarar falhas.	Bloqueia a ação e exige justificativa explícita do usuário.
A3	Guarda da Branch Main	PreToolUse (Edit/Write)	Interrompe edições diretas na branch main e sugere checkout de branch de trabalho.	Protege o histórico de produção contra alterações acidentais.
A4	Varredura Atômica de Segredos	PreToolUse (Write/Edit)	Impede a escrita em disco se detectar chaves de API, JWTs ou tokens sensíveis.	Bloqueio antes de gravar no sistema de arquivos.
A5	Reinjeção Pós-Compactação	PreCompact	Reinjeta o Micro-Kernel P0 + identidade do kit + resumo da tarefa ativa.	Mantém o comportamento de alta qualidade em sessões longas.
A6	Universal AST Repo Map	Sob demanda / Início de Tarefa	repo_map.py gera o grafo de símbolos e exports do projeto em < 1.024 tokens.	Somente leitura de AST; economiza até 15 tool calls exploratórias.
A7	Telemetria Silenciosa de Gate & Roteamento	UserPromptSubmit + Stop	Classifica o prompt do usuário e registra qual agente foi usado e se houve Gate.	Grava silenciosamente em .agent/memory/; o agente não gasta tokens nisso.
A8	Recuperação de Lições Relevantes	UserPromptSubmit	Busca palavras-chave do prompt em gotchas.md e dead-ends.md e injeta aviso.	Leitura local leve; previne repetir o mesmo erro de sessões passadas.
A9	Registro de Becos Sem Saída	Stop (após falha)	Quando uma abordagem falha 3x (Loop), anota em dead-ends.md.	Evita que o mesmo comando quebrado seja tentado na próxima semana.
A10	Validação Seletiva Pré-Encerramento	Stop	Executa o teste rápido do módulo alterado antes de reportar sucesso.	Garante evidência fresca sem rodar toda a suíte de testes.
A11	Auto-Sync de Docs do Kit (sync_docs.py)	Pré-Commit / Pós-Scaffold	Recalcula contadores do disco e atualiza badges em README.md e ARCHITECTURE.md.	Execução determinística em <50ms; elimina falhas no TestDocsSync.
A12	Pre-Commit Universal em Projetos Derivados	Git Hook pre-commit	Em projetos do usuário, roda checklist.py --pre-commit no diff estagiado.	Garante que o projeto do cliente não suba com testes falhando ou segredos.
A13	Ranking de Custo de Contexto por Arquivo	PostToolUse + SessionEnd	Monitora o tamanho de payloads lidos e lista os 5 arquivos mais custosos.	Apenas medição; aponta candidatos a refatoração ou resumo.
A14	Rotação Automática de Memória	SessionEnd	Move blocos de logs com mais de 50 KB para archive/ mantendo índice de busca.	Previne inflação de tokens e poluição do repositório.
A15	Auto-Purge de Workspace (clean_workspace.py)	/finish-branch / SessionEnd	Remove __pycache__, .pytest_cache e worktrees órfãos após o merge.	Mantém o repositório limpo de artefatos efêmeros.
A16	Validação de CI sobre o diff do PR	GitHub Actions (push / pull_request)	Roda checklist.py --pre-commit, varredura de segredo e doc_drift_check.py nos arquivos do diff.	Só reporta e barra o merge; nunca altera código. Fecha a brecha de PR com segredo ou lint quebrado.
A17	Relatório local de custo por tipo de tarefa	SessionEnd (opt-in)	Lê os logs de sessão e cruza custo real com o Task Budget de session_manager.py.	Estritamente local e opt-in, sem envio externo. Substitui percentual projetado por medição.
4. Especificações Técnicas das Epics (Requisitos Funcionais)
Épico 1: Custo, Desduplicação & Sobrevivência de Sessão
E1.1: Desduplicação Imediata de Instruções Raiz
Problema: O Claude Code lê .claude/CLAUDE.md (10.355 tokens) e o texto inicial manda ler .agent/rules/DEVBUREAU.md (9.948 tokens), pagando o mesmo conteúdo duas vezes (~20k tokens) no boot.
Solução:
Alterar a regra inicial: declarar que as diretrizes do kit já estão ativas e que arquivos em .agent/rules/reference/ devem ser lidos estritamente sob demanda.
Compactar o cabeçalho gerado por 

sync_ide.py
.
Critério de Aceite:
python .agent/scripts/token_footprint.py reporta menos de 6.000 tokens no arquivo raiz do Claude Code.
O agente não executa mais view_file em DEVBUREAU.md logo no primeiro turno da conversa.
E1.2: Hook PreCompact para Sobrevivência de Sessões Longas
Problema: Quando a conversa atinge o teto da janela de contexto e o harness executa a compactação, as regras P0 do DevBureau são resumidas ou perdidas, e o agente perde a identidade.
Solução: Criar o script .agent/scripts/hooks/reinject_on_compact.py registrado no evento PreCompact do Claude Code / Antigravity, reinjetando:
Identidade do DevBureau e protocolo de evidência fresca.
Matriz de Decisão simplificada.
Resumo do estado atual da tarefa (task-slug ativo e arquivos tocados).
Critério de Aceite:
Em uma sessão forçada a compactar, o agente continua cumprindo o protocolo de evidência fresca e a Matriz de Decisão no turno imediatamente seguinte.
Épico 2: Descoberta Estrutural & Medição de Aderência
E2.1: Universal AST Repo Map (repo_map.py)
Problema: Agentes gastam de 10 a 20 chamadas exploratórias de ferramenta (list_dir, grep_search, view_file) para entender onde estão classes e funções em novos projetos.
Solução: Desenvolver python .agent/scripts/repo_map.py que parseia a árvore sintática (AST do Python nativo e Regex/Parser leve de TypeScript/JavaScript) e imprime a topologia do projeto em um formato compacto:
plaintext
src/
├── auth/service.py: AuthService [login, verify_token, refresh]
├── api/routes.ts: [POST /login, GET /profile, DELETE /session]
└── db/models.py: User, Session, Organization
Critério de Aceite:
A saída do mapa do repositório consome menos de 1.024 tokens.
Medido em 10/09/2026: cerca de 3ms por arquivo com símbolos (58 arquivos em 179ms), o que projeta cerca de 1,5s para 500 arquivos, e não os 200ms estimados antes de existir implementação. O número original era projeção, não medição. O critério que importa continua sendo comparativo: o mapa precisa reduzir de forma comprovada as chamadas de exploração, e um segundo e meio segue muito abaixo do custo de 10 a 20 tool calls.
E2.2: Placar de Aderência de Regras (rule-adherence)
Problema: Atualmente, não se sabe quais das ~40 KB de regras são seguidas e quais são solenemente ignoradas pelo modelo. Podar sem medir arrisca a qualidade.
Solução: Hook em PostToolUse e SessionEnd que verifica conformidade com 4 regras verificáveis:
Anúncio do agente presente em tarefas complexas.
Socratic Gate disparado antes de editar código em novas features.
Evidência fresca coletada antes de declarar conclusão.
Formatação pós-edição executada. Os dados são gravados em .agent/memory/rule-adherence.jsonl e sumarizados via doctor.py --adherence.
Critério de Aceite:
Após 20 sessões de uso real, gera relatório demonstrando a porcentagem de cumprimento de cada regra. Regras com <50% de adesão tornam-se candidatas prioritárias para virar hook determinístico ou serem podadas.
Épico 3: Automação Segura de Repositório & Projetos Derivados
E3.0: Distribuição da Camada de Automação (REVISADO, NÃO É MAIS BLOQUEADOR)
Histórico da revisão: a versão anterior deste épico afirmava que nenhum hook chegava ao projeto do usuário. Um teste em diretório limpo (npx devbureau init --target=claude, sem nenhuma alteração de código) desmentiu a afirmação: o arquivo .claude/settings.json foi gerado com SessionStart 1, PreToolUse 5, PostToolUse 6 e 32 regras de permissão. O responsável é sync_ide.py, que é distribuído dentro de .agent/ e cujo ensure_claude_protect_hook() já faz merge não destrutivo com poda de hooks obsoletos. Uma implementação paralela chegou a ser escrita e foi revertida por duplicar esse mecanismo e criar duas fontes de verdade para a lista de hooks.
Problema remanescente: quem sincroniza somente um alvo que não seja o Claude não tem hooks registrados até rodar sync_ide.py com o alvo claude.
Solução: nenhuma ação de código imediata. O caso é raro e o próprio sync_ide.py o resolve quando executado. Reavaliar apenas se aparecer relato real de usuário.
Reclassificação: o único item bloqueador verificado da antiga Fase 0 é o E3.2 abaixo.
E3.1: Sincronizador Automático de Documentação (sync_docs.py)
Problema: Criar ou remover um agente, skill ou workflow exige editar 4 arquivos manualmente para evitar falhas no teste TestDocsSync do 

test_kit_integrity.py
.
Solução: Implementar python .agent/scripts/sync_docs.py que:
Lê o disco (agents/, skills/, workflows/, scripts/).
Atualiza badges e números em 

README.md
 e 

README_pt-BR.md
.
Atualiza as contagens e a tabela estrutural em 

ARCHITECTURE.md
.
Mantém a versão coerente com 

package.json
.
Critério de Aceite:
python .agent/scripts/sync_docs.py executa em menos de 100ms e deixa o teste TestDocsSync 100% verde sem edição manual.
E3.2: Ativação Universal de Pre-Commit em Projetos Derivados
Problema: O instalador 

install_hooks.py
 hoje desliga o hook caso KIT_MASTER_RULES.md não exista (ou seja, em qualquer projeto criado pelo usuário que use o kit).
Solução: Em projetos derivados, o pre-commit deve rodar: python .agent/scripts/checklist.py --pre-commit (verificando segredos expostos, linter e testes unitários no diff).
Critério de Aceite:
Um git commit em projeto derivado é interceptado e bloqueado se houver credenciais expostas ou testes quebrados.
E3.3: Reconciliação Contínua Spec vs. Código (/converge)
Problema: Tarefas complexas criam {task-slug}.md, mas ao final da implementação é comum faltarem fatias ou critérios de aceite sem que ninguém perceba.
Solução: Criar o workflow /converge (inspirado no spec-kit do GitHub) que analisa o plano aprovado, varre o código modificado via AST/Git Diff e relata:
Fatias completamente entregues.
Fatias pendentes com indicação de arquivo e linha.
Critério de Aceite:
/converge aponta com precisão tarefas incompletas de um plano antes de fechar a branch.
5. Roadmap de Implementação em 3 Ondas
A ordem foi desenhada para gerar alívio imediato de custos e segurança imediata (Onda 1), seguida de medição baseada em fatos reais (Onda 2), para culminar na arquitetura final Slim-Core e convergência (Onda 3).

mermaid
gantt
    title Roadmap de Evolução DevBureau 4.0
    dateFormat  YYYY-MM-DD
    section Onda 1: Custo Imediato & Sobrevivência
    Distribuição da Automação (E3.0)           :crit, o1_0, 2026-09-11, 1d
    Desduplicação de Regras (E1.1)             :active, o1_1, 2026-09-11, 1d
    Hook PreCompact (E1.2)                     :active, o1_2, 2026-09-12, 1d
    Script sync_docs.py (E3.1)                 :active, o1_3, 2026-09-12, 1d
    Pre-commit para Projetos Derivados (E3.2)  :active, o1_4, 2026-09-13, 1d
    Hooks A2/A3/A4 (Proteção de Testes/Main)   :o1_5, 2026-09-13, 1d
    section Onda 2: Medição, Memória & Descoberta
    Placar de Aderência de Regras (E2.2)       :o2_1, 2026-09-14, 2d
    Universal AST Repo Map (E2.1)              :o2_2, 2026-09-15, 2d
    Registro de Becos sem Saída (A9)           :o2_3, 2026-09-16, 1d
    Rotação de Memória >50KB (A14)             :o2_4, 2026-09-17, 1d
    Ranking de Custo de Contexto (A13)         :o2_5, 2026-09-17, 1d
    Validação de CI sobre o diff (A16)         :o2_6, 2026-09-16, 1d
    Relatório de Custo por Tarefa (A17)        :o2_7, 2026-09-17, 1d
    section Onda 3: Slim-Core (abre por dados, não por data)
    Poda Escalonada do Slim-Core (ver portão)  :milestone, o3_1, 2026-09-18, 0d
    Workflow /converge (E3.3)                  :o3_2, 2026-09-20, 2d
    Camada de Overrides por Projeto            :o3_3, 2026-09-21, 2d
    Distribuição Claude Plugin Marketplace     :o3_4, 2026-09-22, 1d
Portão de abertura da Onda 3 (corrige contradição de cronograma)
A poda do Slim-Core não abre por data. O critério de aceite do E2.2 exige 20 sessões reais de uso, e as datas acima somam quatro dias corridos, que não produzem esse volume. A Onda 3 abre quando o relatório de aderência acumular 20 sessões, e não em 18 de setembro. As datas do bloco acima são estimativa de duração, não gatilho.
Poda escalonada com portão de qualidade
O corte não é feito de uma vez. São três degraus, cada um com verificação antes do próximo: primeiro 6.000 tokens, depois 3.000, depois 1.500. A cada degrau, uma amostra pareada de tarefas reais é comparada contra o degrau anterior em três sinais: o agente correto continua sendo selecionado, o Socratic Gate continua disparando nos mesmos casos, e a taxa de aderência das regras verificáveis não regride. Se algum sinal piorar, o corte para naquele degrau e o degrau anterior vira o valor final. A meta é comportamento preservado ao menor custo possível, e não um número de tokens.
6. Métricas de Sucesso & KPIs
KPI / Indicador	Situação Atual (v3.40.1)	Meta com DevBureau 4.0	Impacto para o Usuário
Tokens de Boot por Sessão	~20.300 tokens (duplicado)	< 6.000 tokens na Onda 1; 3.000 e depois 1.500 apenas se o portão de qualidade permitir	Corte de ~70% no custo de inicialização já na Onda 1, medido por token_footprint.py
Amnésia de Sessão Longa	Alta (apaga regras P0 pós-compactação)	Zero (reinjeção determinística via PreCompact)	Sessões de 50+ turnos continuam disciplinadas
Tool Calls para Descoberta de Código	10 a 15 chamadas	1 chamada (repo_map.py)	Menos rodadas exploratórias no início da tarefa; o ganho é medido por contagem pareada antes e depois, sem percentual projetado
Atrito de Manutenção de Docs	Manual em 4 arquivos	1 comando (<100ms via sync_docs.py)	Zero commits travados por contagem defasada
Proteção de Projetos Derivados	Desligada de fábrica	Ativa no pre-commit	Zero segredos ou builds quebradas em produção
Regras Medidas por Evidência	0% (baseado em impressão)	100% das regras verificáveis	Eliminação de regras inúteis que só gastam tokens
Pre-Commit Ativo em Projetos Derivados	0% (install_hooks.py aborta)	100%	Único gap de distribuição confirmado por teste; os hooks do Claude Code já chegam via sync_ide.py
PR com Segredo ou Lint Quebrado	Passa no CI	Barrado (A16)	O CI deixa de validar apenas a integridade do kit e passa a proteger o código do diff
Custo Real por Tipo de Tarefa	Não medido	Medido e comparado ao Task Budget (A17)	Substitui projeção percentual por número observado
7. Próxima Ação Recomendada
Para começar de forma imediata e com risco zero de regressão, recomendo executarmos a Onda 1:

Passo 0 (revisado): a distribuição dos hooks já funciona via sync_ide.py, conforme teste em ambiente limpo. O que resta é o E3.2, destravar o install_hooks.py para instalar o pre-commit em projetos derivados. Deixou de ser bloqueador dos demais passos.
Passo 1: Criar python .agent/scripts/sync_docs.py (resolve de imediato o trabalho braçal de sincronizar README.md, ARCHITECTURE.md e package.json).
Passo 2: Atualizar a instrução raiz no sync_ide.py eliminando a leitura duplicada de DEVBUREAU.md quando CLAUDE.md já estiver ativo.
Passo 3: Criar o hook PreCompact (reinject_on_compact.py) para blindar o DevBureau contra degradação em sessões longas.
Passo 4: Configurar 

install_hooks.py
 para que projetos derivados executem checklist.py --pre-commit.