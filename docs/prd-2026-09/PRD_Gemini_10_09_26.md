📄 PRD: DevBureau Slim-Core & Automações "Zero-Prompt"
Versão: 4.0.0-Draft
Autor: Product Manager (@[product-manager])
Status: Proposta Estratégica para Revisão & Roadmap
Público-alvo: Desenvolvedores, Criadores de SaaS e Usuários de Negócio operando agentes de IA

1. Visão Geral & Problema de Negócio
1.1 Declaração do Problema (Problem Statement)
O DevBureau consolidou-se como um framework de ponta para orquestração de agentes especializados (23 agentes, 78 skills, 29 workflows, 11 hooks). No entanto, o custo operacional de rodar modelos de ponta (Claude 3.7/Opus, GPT-5, Gemini 1.5 Pro) em sessões longas enfrenta dois gargalos críticos:

O Monólito de Contexto Raiz: O arquivo 

.agent/rules/DEVBUREAU.md
 e seus derivados gerados (

AGENTS.md
, 

GEMINI.md
, .claude/CLAUDE.md) acumulam ~40 KB (~9.500 a 10.000 tokens) injetados estaticamente a cada turno. Em sessões de 25 a 30 iterações, isso queima até 300.000 tokens apenas lendo as regras base, aumentando o custo por tarefa e a latência de primeira resposta (TTFT). Além disso, excede o teto recomendado de 32 KB imposto por harnesses como o OpenAI Codex CLI.
Dependência de Solicitação Manual para Rotinas Seguras: Atualmente, tarefas triviais, seguras e determinísticas (formatação de código pós-edição, checagem do teste correspondente, sanitização de logs de debug, sincronização de contadores em documentação) dependem de o usuário ou o agente lembrarem de invocar scripts como 

checklist.py
 ou 

auto_fixer.py
.
1.2 Objetivo Estratégico (Goal)
Transformar o DevBureau no framework mais enxuto, rápido, econômico e autônomo para agentes de código, implementando:

Micro-Kernel de Contexto (Slim-Core): Reduzir o custo de inicialização de ~10k para < 1.000 tokens no arquivo raiz através de Progressive Disclosure e regras Glob-Scoped.
Motor de Automação "Zero-Prompt": Estruturar automações invisíveis de baixo risco que rodam sozinhas nos momentos exatos do ciclo de vida da tarefa.
Repositório AST Map Ultracompacto: Fornecer ao agente uma visão estrutural imediata do projeto sem desperdiçar rodadas de exploração.
2. Benchmark Competitivo no GitHub (Repositórios 2025–2026)
Analisamos os repositórios mais recentes e influentes no cenário de agentic harnesses, extraindo os padrões arquiteturais de alto impacto:

Repositório / Framework	Foco Principal & Mecanismo Chave	O Que Faz de Melhor	O Que Falta / Gap no DevBureau Atual
wshobson/agents (2026)	Multi-Harness Plugin Marketplace (Claude Code, Codex, Cursor, Antigravity, OpenCode, Copilot).	Progressive Disclosure: Cada plugin (plugins/<categoria>/) é isolado. O arquivo raiz 

AGENTS.md
 tem teto estrito de 150 linhas / 500 tokens. Regras e skills só carregam sob demanda.	O DevBureau carrega todas as regras universais de uma só vez (40KB) em vez de decompor o núcleo em micro-instruções contextuais.
Aider (Aider-AI/aider)	Universal AST Repo Map & Auto-Lint Feedback Loop.	Repo Map via AST + PageRank: Resume um projeto inteiro em ~1.024 tokens. Auto-Lint pós-edição: Toda alteração roda linter automaticamente e auto-corrige antes de devolver ao usuário.	O DevBureau depende do explorer-agent ler diretórios e arquivos manualmente (gastando 10 a 20 tool calls por sessão).
affaan-m/ECC (Everything Claude Code) + AgentShield	Harness Operating System & Hooks Determinísticos.	Pre/Post-Tool Enforcement: Hooks determinísticos que bloqueiam conclusões sem teste (block-no-verify), sanitizam injeções e monitoram gasto de tokens por tarefa.	O DevBureau já tem hooks em 

.agent/scripts/hooks/
, mas eles são ativos prioritariamente no Claude Code e inexistentes em projetos derivados do usuário.
obra/superpowers	TDD Disciplinado & Fatiamento Vertical.	Vertical Slicing: Proíbe decomposição de tarefas por camadas (ex: "banco primeiro, depois front"); exige fatias ponta-a-ponta testáveis. Isolamento estrito em git worktree.	DevBureau adotou recentemente o conceito no 

plan-writing
, mas ainda não possui guardrails automáticos de validação por fatia.
garrytan/gstack	Virtual Team & Anti-Fatigue Harness.	plan-tune: Memória persistente de supressão de perguntas redundantes ("pare de me perguntar X"). Self-update resiliente: Auto-upgrade com backup e rollback.	Usuários frequentes do DevBureau enfrentam fadiga do Socratic Gate em tarefas repetitivas.
DietrichGebert/ponytail	Token-Economy Ruleset ("Lazy Ladder").	Economia Extrema de Saída: Código primeiro, explicação máxima de 3 linhas. Escada de decisão: YAGNI → stdlib → dependência existente → código mínimo.	Reduz em até 40% a verbosidade do modelo, gerando economia líquida de custo de API.
Cursor Rules 2.0 (.cursor/rules/*.mdc)	Glob-Scoped Rule Injection.	Injeta regras apenas quando arquivos específicos estão em foco (ex: frontend.mdc apenas para .tsx, backend.mdc apenas para .py).	DevBureau já implementou para Cursor e Copilot no 

sync_ide.py
, mas não para Claude Code, Antigravity e Codex (onde ainda gera um monólito de 40KB).
3. Gap Analysis do DevBureau
Identificamos 5 gaps estruturais no repositório atual:

[ Gaps Estruturais Atuais no DevBureau ]
 ├── 1. Context Bloat: DEVBUREAU.md / AGENTS.md = 40 KB (~10.000 tokens) em toda chamada
 ├── 2. Falta de Mapa AST: Descoberta de código manual (10-15 tool calls exploratórias)
 ├── 3. Hooks Inativos em Projetos Derivados: install_hooks.py aborta se não houver KIT_MASTER_RULES.md
 ├── 4. Zero-Prompt Gap: Lint, formatação e verificação de testes não rodam de forma automática
 └── 5. Atrito Manual de Documentação: Sincronizar contadores de agentes/skills exige editar 4 arquivos
4. Catálogo de Automações Seguras "Zero-Prompt" (Sem Solicitação Manual)
Tarefas determinísticas que o agente deve executar de forma transparente, silenciosa e segura, sem que o usuário precise pedir:

#	Automação Segura	Gatilho de Ciclo de Vida	Ação Executada em Segundo Plano	Benefício & Segurança
A1	Auto-Fix & Format Pós-Edição	Pós-Tool Use (Edit / Write em arquivos de código)	Roda silenciosamente python .agent/scripts/auto_fixer.py <arquivo> aplicando Prettier/Ruff/Black.	100% Seguro: Erros de formatação e imports não-utilizados são limpos instantaneamente sem consumir tokens de raciocínio.
A2	Test Impact Analysis (TIA) Background	Pós-Tool Use (Edit / Write em lógica)	Usa 

blast_radius.py
 + 

test_gap_check.py
 para identificar o teste unitário exato e rodá-lo.	Zero-Break Proativo: O agente sabe em milissegundos se quebrou o teste da função modificada, sem rodar toda a suite.
A3	Checkpoints Atômicos Git (Safety Snapshots)	Pré-Execução de Tarefas Complexas (COMPLEX CODE / ADE)	Cria um snapshot local leve (git stash create ou commit em branch/worktree temporária).	Reversão Instantânea: Se o agente entrar em loop ou quebrar o app, volta ao estado anterior com 1 comando, sem risco de perda de dados.
A4	Auto-Detecção de Stack & Perfil de Execução	Início da Sessão / Primeira Ferramenta	Inspeciona package.json, pyproject.toml ou requirements.txt e gera cache .agent/cache/stack_profile.json.	Não precisa perguntar ao usuário qual é a linguagem, framework ou gerenciador de pacotes (npm vs pnpm vs uv).
A5	Auto-Sanitização de Segredos & Debug	Pre-Commit / Conclusão de Tarefa	Varredura de console.log, print() de debug e credenciais via 

security_scan.py
.	Impede que dados sensíveis ou lixo de terminal subam para repositórios remotos.
A6	Auto-Sync de Documentação do Kit (sync_docs.py)	Pré-Commit / Pós-Criação de Skill ou Agente	Recalcula contadores reais do disco e atualiza badges em README.md, README_pt-BR.md, ARCHITECTURE.md e package.json.	Elimina falhas no commit por TestDocsSync e economiza 5 minutos de edição manual de markdown.
A7	Limpeza Automática de Lixo Operacional (clean_workspace.py)	Pós-Finalização de Branch (/finish-branch)	Limpa caches temporários (__pycache__, .pytest_cache, worktrees concluídos e órfãos).	Mantém a raiz do projeto sempre limpa para usuários de negócios.
5. Requisitos do Produto (PRD Specifications)
ÉPICO 1: Arquitetura Slim-Core & Otimização Radical de Tokens
US-1.1: Micro-Kernel de Instruções Raiz
Como: Agente ou Usuário operando em qualquer harness (Claude, Codex, Antigravity, Cursor).
Quero: Que o arquivo base de instruções (AGENTS.md / GEMINI.md / CLAUDE.md) contenha apenas o Micro-Kernel (Princípios P0, Matriz de Decisão, User Profile e Roteador Dinâmico).
Para: Não desperdiçar 10.000 tokens em cada mensagem e respeitar o teto de 32 KB dos harnesses CLI.
Critérios de Aceite (Gherkin):
Dado que o script 

sync_ide.py
 é executado com --target all;
Quando os arquivos 

AGENTS.md
, 

GEMINI.md
 e .claude/CLAUDE.md forem gerados;
Então o tamanho total de cada arquivo raiz não deve exceder 1.000 tokens (ou ~150 linhas);
E detalhes operacionais extensos devem residir em .agent/rules/reference/OPERATIONS_DETAIL.md carregados sob demanda ou via skills especializadas.
US-1.2: Gerador de Mapa do Repositório Ultracompacto (repo_map.py)
Como: Agente iniciando uma análise ou tarefa complexa de código.
Quero: Um script determinístico que gere um mapa estrutural do projeto em árvore de símbolos AST (classes, funções, exportações) em menos de 1.000 tokens.
Para: Eliminar rodadas cegas de list_dir e grep_search, localizando o arquivo exato na primeira tentativa.
Critérios de Aceite (Gherkin):
Dado um projeto com múltiplos módulos Python ou TypeScript;
Quando python .agent/scripts/repo_map.py for executado;
Então a saída no terminal deve apresentar a árvore de símbolos com imports e assinaturas de funções essenciais;
E a pegada de contexto deve ser inferior a 1.024 tokens.
ÉPICO 2: Automação "Zero-Prompt" & Qualidade Contínua
US-2.1: Pre-Commit Universal para Projetos Derivados
Como: Desenvolvedor ou usuário não-programador criando um software a partir do DevBureau.
Quero: Que o pre-commit instalado por 

install_hooks.py
 execute as validações do projeto derivado (checklist.py --pre-commit), e não apenas se desligue na ausência de KIT_MASTER_RULES.md.
Para: Garantir que nenhum código quebrado, sem teste ou com vulnerabilidade de segurança seja commitado no projeto final.
Critérios de Aceite (Gherkin):
Dado um projeto gerado a partir do DevBureau (sem KIT_MASTER_RULES.md);
Quando um git commit for disparado;
Então o hook pre-commit deve rodar python .agent/scripts/checklist.py --pre-commit;
E abortar o commit caso haja segredos expostos ou testes unitários falhando.
US-2.2: Sincronizador Automático de Documentação (sync_docs.py)
Como: Mantenedor ou agente evoluindo o DevBureau.
Quero: Um comando determinístico que conte agentes, skills, workflows e scripts mestre e atualize todos os documentos oficiais simultaneamente.
Para: Nunca mais sofrer bloqueio de commit por dessincronização de contagens no teste TestDocsSync.
Critérios de Aceite (Gherkin):
Dado que uma nova skill ou agente foi adicionado em .agent/;
Quando python .agent/scripts/sync_docs.py for executado;
Então as contagens e tabelas de 

README.md
, 

README_pt-BR.md
, 

ARCHITECTURE.md
 e a versão em 

package.json
 são sincronizadas em menos de 100 milissegundos.
ÉPICO 3: Auto-Recuperação e Economia de Saída (Self-Healing Loop)
US-3.1: Micro-Loop de Auto-Cura para Erros de Sintaxe e Lint
Como: Agente implementando uma funcionalidade.
Quero: Que falhas de sintaxe, tipos óbvios ou lint acionem exatamente uma tentativa autônoma de reparo com base no erro direto do compilador/linter.
Para: Não transferir atrito trivial ao usuário e nem entrar em loops alucinatórios.
Critérios de Aceite (Gherkin):
Dado que um comando de teste ou linter falhou com um erro de import ou syntax error;
Quando o agente processar a falha;
Então ele aplica a correção cirúrgica imediatamente com base no stack trace;
E se a falha persistir na segunda tentativa, aciona o Escape Protocol imediatamente, apresentando opções claras ao usuário.
6. Arquitetura da Solução & Fluxo de Execução
mermaid
flowchart TD
    subgraph Inicialização [Início da Tarefa]
        U[Solicitação do Usuário] --> Classify[REQUEST CLASSIFIER - TIER 0]
        Classify --> Checkpoint[A3: Auto Safety Checkpoint Git]
        Classify --> Detect[A4: Auto-Detecção de Stack]
    end
    subgraph Execução Enxuta [Ciclo de Execução Slim-Core]
        Checkpoint --> SlimRules[Micro-Kernel de Regras: <1.000 tokens]
        SlimRules --> RepoMap[Aider-style AST Repo Map: ~600 tokens]
        RepoMap --> CodeChange[Edição Cirúrgica de Código]
        CodeChange --> PostHook[A1: Auto-Fixer & Linter Silencioso]
    end
    subgraph Validação Segura [Validação Zero-Prompt]
        PostHook --> TIA[A2: Test Impact Analysis - Executa Teste Alvo]
        TIA -->|Passou| SecretScan[A5: Sanitização de Segredos & Logs]
        TIA -->|Falhou| SelfHeal[US-3.1: Micro-Reparo 1x com Stack Trace]
        SelfHeal -->|Sucesso| SecretScan
        SelfHeal -->|Persistiu Falha| StopAsk[Escape Protocol: Pergunta ao Usuário]
    end
    subgraph Fechamento [Encerramento da Tarefa]
        SecretScan --> SyncDocs[A6: Auto-Sync Documentação]
        SyncDocs --> Commit[Git Commit Local Seguro]
        Commit --> Clean[A7: Auto-Purge Caches Temporários]
    end
7. Matriz de Priorização (MoSCoW & RICE)
Para guiar o roadmap de engenharia de forma pragmática, aplicamos os frameworks de priorização do Product Manager:

Feature / Requisito	MoSCoW	Reach (1-10)	Impact (1-3)	Confidence (%)	Effort (dias)	Score RICE	Justificativa de Engenharia
A6: Auto-Sync de Docs (sync_docs.py)	MUST	10	3	100%	0.5	600	Elimina imediatamente o maior atrito de commit e manutenção do kit.
A1: Auto-Fixer Pós-Edição Hook	MUST	9	3	90%	1.0	243	Garante código sempre limpo e sem formatações inconsistentes.
US-1.1: Micro-Kernel Slim-Core (sync_ide.py)	MUST	10	3	85%	1.5	170	Corta 55% dos tokens de entrada por turno; economia brutal de custos.
US-2.1: Pre-Commit em Projetos Derivados	MUST	8	3	95%	1.0	228	Protege projetos de clientes e usuários finais de quebras em produção.
US-1.2: AST Repo Map (repo_map.py)	SHOULD	8	2	80%	2.0	64	Economiza 10+ chamadas de ferramentas de leitura/grep por tarefa.
A2: Test Impact Analysis Background	SHOULD	7	2	80%	2.5	44	Feedback instantâneo do teste alterado sem onerar a suite inteira.
A3: Checkpoints Atômicos Git	COULD	6	2	75%	1.5	60	Reversão sem atrito contra alucinações e loops em código complexo.
A7: Auto-Purge de Workspace (clean_workspace.py)	COULD	6	1	90%	0.5	108	Manutenção de higiene do diretório sem necessidade de comando manual.
8. Impacto Financeiro e Operacional Estimado (ROI)
Métrica	Situação Atual (DevBureau v3.39)	Com Implementação do PRD	Ganho Projetado
Tokens de Entrada por Turno (Regras)	~9.800 tokens estáticos	~850 tokens (Micro-Kernel)	-91% no overhead de regras
Custo Médio de Tokens por Sessão (30 turnos)	~450.000 tokens de contexto	~210.000 tokens totais	-53% de custo em chamadas LLM
Latência de Resposta (TTFT)	3.5s – 6.0s (processando 10k prompt)	1.2s – 2.2s	~60% mais rápido
Tempo Gasto em Setup e Descoberta	10 a 15 tool calls (list_dir, grep)	1 tool call (repo_map.py)	90% menos turnos exploratórios
Intervenção Manual do Usuário para Checagens	Frequente (precisa pedir testes/lint/sync)	Quase zero (automações em background)	Experiência 100% autônoma e fluida
9. Próximos Passos & Recomendação de Execução
Como Product Manager, recomendo a execução do roadmap na seguinte cadência:

Fase 1 (Quick Wins - Imediato / 1 dia):
Criar o script mestre python .agent/scripts/sync_docs.py para sincronizar automaticamente badges, contagens e tabelas entre 

README.md
, 

ARCHITECTURE.md
 e 

package.json
.
Ajustar 

install_hooks.py
 para que, em projetos derivados (sem KIT_MASTER_RULES.md), ele ative o pre-commit com checklist.py --pre-commit.
Fase 2 (Slim-Core Architecture - 2 dias):
Refatorar a geração do 

sync_ide.py
 para Claude, Codex e Antigravity, separando o Micro-Kernel essencial das regras detalhadas (adotando o modelo do Cursor/Copilot de carregar regras sob demanda).
Fase 3 (Inteligência & Descoberta - 2 dias):
Desenvolver python .agent/scripts/repo_map.py com suporte a Python AST e TypeScript/JS para geração de mapa de contexto em <1k tokens.
Adicionar hook de auto-fix silencioso pós-edição de arquivos.