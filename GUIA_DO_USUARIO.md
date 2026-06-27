# 🚀 Como Iniciar ou Continuar Qualquer Projeto

Para iniciar ou continuar um projeto utilizando a estrutura de inteligência personalizada, a cópia da pasta `.agent` para a raiz do novo projeto é suficiente para transferir os agentes, regras e scripts. Contudo, há um passo complementar obrigatório para que a IDE (como Cursor ou Claude) passe a ler e aplicar essas regras de forma nativa.

Após copiar a pasta, execute o script de sincronização no terminal do novo projeto:
```bash
python .agent/scripts/sync_ide.py --target all
```

Esse comando cria os arquivos de configuração necessários (como `.cursorrules` ou `.clauderules`) apontando para `.agent/rules/GEMINI.md`, ativando o comportamento automático.

### 🤖 Configuração para Google Gemini (Gemini Code Assist / AI Studio / Advanced)

*   **Gemini Code Assist (VS Code ou IntelliJ):** Não é necessário executar nenhum comando específico para o Gemini Code Assist. A ferramenta analisa e indexa o contexto do workspace automaticamente. Ter a pasta `.agent` e o arquivo `GEMINI.md` na raiz do projeto é suficiente para que o assistente consulte as instruções durante o uso. Ainda assim, executar o script de sincronização é recomendado para manter o ambiente preparado caso use outras ferramentas.
*   **Google AI Studio ou Gemini Advanced (Web):** Para chats via navegador ou uso direto da API, carregue o conteúdo do arquivo [.agent/rules/GEMINI.md](./.agent/rules/GEMINI.md) na seção de **System Instructions** (Instruções do Sistema) ou anexe o arquivo no primeiro prompt da conversa.

---

## 🛤️ Roteiro: Por Onde Começar?

Escolha o seu momento atual e siga a recomendação da "Equipe Profissional":

### 1️⃣ "Ainda não tenho a pasta do projeto criada"
*   **Comando:** `/new-project`
*   **Por que:** Ele é o único comando que você usa **neste kit base**. Ele vai te dar o "mapa" e os comandos de terminal para você criar sua nova pasta e levar a inteligência para lá.

### 2️⃣ "Já estou na pasta nova, mas minha ideia ainda é vaga"
*   **Comando:** `/brainstorm`
*   **Por que:** Antes de gastar tempo criando arquivos, use o consultor. Ele vai te fazer perguntas sobre público-alvo, problema que você resolve e funcionalidades essenciais. É a fase de **concepção**.

### 3️⃣ "Minha ideia está clara, quero desenhar o sistema"
*   **Comando:** `/build-saas` (para sistemas complexos) ou `/plan` (para uma funcionalidade específica)
*   **Por que:** Aqui o Arquiteto entra em cena. Ele cria os documentos técnicos (os "mapas da obra") que descrevem como o banco de dados e as telas vão funcionar. **Não escreve código ainda.**

### 4️⃣ "Quero que o agente faça tudo sozinho (Mãos livres)"
*   **Comando:** `/ade` [descreva sua ideia aqui]
*   **Por que:** É o modo "Piloto Automático". O agente vai entender sua ideia, criar a especificação e só vai te chamar para você dar seu **"DE ACORDO"** na Fase 3 antes de começar a codar.

### 5️⃣ "Quero construir junto com o agente (Interativo)"
*   **Comando:** `/create`
*   **Por que:** Ideal para quem quer ver o processo acontecer passo a passo. O agente vai conversando com você enquanto cria as pastas e os primeiros arquivos.

---

## 🗺️ Tabela Mestre: Como Chamar a Equipe

Use esta tabela para saber quem chamar ou qual comando usar. **Lembre-se:** você pode apenas falar naturalmente em Português, e o kit escolherá o especialista certo!

| Especialista / Ferramenta | O que ele faz? | Como chamar (Exemplos) |
|:---|:---|:---|
| **🎨 Designer Frontend** | Visual, cores, layout, botões | "@frontend-specialist: melhora o visual", "dark mode" |
| **⚙️ Arquiteto Backend** | Servidor, API, regras de negócio | "@backend-specialist: cria uma rota", "conecta o front" |
| **💾 Arquiteto de Banco** | Organização e estrutura de dados | "@database-architect: cria uma tabela de usuários" |
| **🔍 Detetive (Debugger)** | Conserta erros e bugs | "@debugger: o login não funciona", "erro 404" |
| **🛡️ Auditor de Segurança** | Protege o app e checa invasões | "@security-auditor: o site está seguro?", "criptografia" |
| **🚀 Autônomo (/ade)** | Faz uma tarefa completa sozinho | `/ade crie um sistema de login com Google` |
| **🏗️ Construtor (/create)** | Cria algo novo do zero | `/create dashboard de vendas` |
| **🧠 Planejador (/plan)** | Planeja antes de codar | `/plan novo sistema de pagamentos` |
| **🏥 Médico (Doctor)** | Checa se sua IA está "saudável" | `checar kit`, `diagnóstico`, `doctor` |
| **🧪 Testador** | Garante que tudo funciona (QA) | `/test`, `validar projeto`, `roteiro de testes` |

---

## 🎯 Como o Agente Funciona (Em 30 Segundos)

Pense neste kit como uma **equipe de desenvolvimento de elite** composta por 22 especialistas que trabalham para você simultaneamente. 

### Iniciar um Novo Projeto
Se você quer começar **um novo aplicativo, site ou jogo** do zero, use este comando:

| Comando | O que Faz |
|---------|-----------|
| `/new-project` | **Clone Inteligente** — Transfere toda a inteligência desta base para uma nova pasta vazia. |

---

## 📋 Comandos Rápidos (Slash Commands)

Estes são atalhos que ativam workflows prontos. Digite diretamente no chat:

### Comandos de Criação e Planejamento

| Comando | Quando Usar | O que Faz |
|---------|-------------|-----------|
| `/build-saas` | Iniciar um novo produto SaaS | Guia por 7 etapas de planejamento → gera 3 docs prontos |
| `/plan` | Planejar qualquer feature | Cria um plano detalhado SEM escrever código ainda |
| `/create` | Construir algo do zero | Planeja + constrói a aplicação completa |
| `/brainstorm` | Explorar ideias | Faz perguntas estratégicas antes de decidir |

### Comandos de Desenvolvimento

| Comando | Quando Usar | O que Faz |
|---------|-------------|-----------|
| `/enhance` | Melhorar algo existente | Evolui funcionalidade já existente |
| `/ade` | Tarefa autônoma end-to-end | Pipeline completo: discovery → spec → código → testes |
| `/debug` | Algo não funciona | Investigação sistemática do problema |
| `/test` | Verificar qualidade | Cria e roda testes automaticamente |

### Comandos de Publicação

| Comando | Quando Usar | O que Faz |
|---------|-------------|-----------|
| `/deploy` | Colocar no ar | Checklist + deploy seguro passo a passo |
| `/preview` | Ver o projeto rodando | Liga o servidor local para visualização |
| `/status` | Ver progresso geral | Mostra o estado do projeto |

### Comandos de Design e Interface

| Comando | Quando Usar | O que Faz |
|---------|-------------|-----------|
| `/ui-ux-pro-max` | Design premium | 50 estilos visuais disponíveis |

### Comandos de Saúde do Kit *(Novos!)*

| Comando | Quando Usar | O que Faz |
|---------|-------------|-----------|
| `checar kit` | Antes de qualquer trabalho importante | Diagnóstico completo do kit (22 agentes, 62 skills) |
| `verificação final` | Antes de publicar | Roda todos os testes em sequência |
| `rode todos os testes` | Após fazer mudanças | Garante que nada quebrou |

---

## 💎 Pacotes de Expansão (Novos Poderes)

Agora seu kit conta com 3 novos pacotes de inteligência estratégica importados do repositório *Awesome Skills*:

### 1. 🧠 Estratégia e Memória
*Transforma o agente de um "codificador" em um "consultor de negócios".*
- **`agent-memory-mcp`**: Permite que o agente tenha memória persistente de longo prazo (Contexto Infinito).
- **`agent-evaluation`**: Audita a qualidade e confiabilidade de cada entrega da IA.

### 2. 📊 IA Preditiva Pro (Coração do Projeto)
*Ideal para o Radar Preditivo e análise estatística de loterias.*
- **`predictive-modeling`**: Padrões avançados para predição e séries temporais.
- **`ai-engineer`**: Refinamento de modelos neurais e algoritmos de predição.
- **`machine-learning-ops`**: Cria esteiras automáticas de re-treinamento de dados.

### 3. 💰 SaaS & Business Launcher
*Para quem quer transformar a ferramenta em um produto real.*
- **`micro-saas-launcher`**: Facilita a criação de MVPs voltados para o mercado.
- **`startup-analyst`**: Analisa métricas de negócio (CAC, LTV, Burn Rate).

---

## 🤖 Novidade: Pipeline Autônomo `/ade`

O `/ade` é o modo mais poderoso. Você descreve o que quer e o agente executa tudo sozinho, em 6 fases supervisionadas:

```
Você descreve → Discovery → Spec → ✋ Você aprova → Código → QA → ✅ Pronto
```

**Exemplos de uso:**
```
/ade adicione um sistema de notificações por email
/ade crie uma tela de dashboard com gráficos de vendas
/ade implemente login com Google na plataforma
```

> **Detalhe importante:** O pipeline vai **pausar na Fase 3** para mostrar o plano detalhado e pedir sua aprovação antes de escrever qualquer código. Isso garante que o resultado seja exatamente o que você quer.

---

## 🏗️ Cenário 1: Criar um SaaS do Zero

### Como Iniciar

```
/build-saas [descreva sua ideia em uma frase]
```

**Exemplo real:**
```
/build-saas aplicativo para personal trainers gerenciarem alunos e treinos
```

### O Que Vai Acontecer

O agente vai te guiar por **7 etapas**, fazendo **uma pergunta de cada vez**:

1. 🦁 **Discovery** — "Que problema isso resolve?", "Quem vai usar?", "Como monetizar?"
2. 📋 **Requisitos** — User stories, funcionalidades prioritárias
3. 💾 **Banco de Dados** — Estrutura dos dados (sem você precisar entender SQL)
4. ⚙️ **Backend** — Estrutura do servidor e APIs
5. 🎨 **Frontend** — Páginas, componentes, design
6. 🔒 **Segurança** — Checklist de proteção automática
7. 📄 **Documentos Finais** — 3 documentos prontos para implementar

### Dicas de Ouro

- **Use referências visuais** — "Quero algo como o dashboard do Notion" funciona muito bem
- **Seja honesto quando não souber** — O agente sugere a melhor opção
- **Não traduza para técnico** — Fale como falaria com um funcionário: "Quero que o sistema avise o cliente quando o pedido sair para entrega"

---

## 🎨 Cenário 2: Criar uma Landing Page ou Site

### Como Iniciar

```
/create landing page para [seu produto/serviço]
```

**Exemplos:**
```
/create landing page para curso online de fotografia
/create site institucional para escritório de advocacia
/create página de vendas para ebook sobre produtividade
```

### Dicas

- **Mande prints de referência** — "Quero um visual parecido com esse site: [link]"
- **Descreva o estilo** — "Moderno, escuro, com animações sutis" é suficiente
- **Liste as seções** — "Hero, benefícios, depoimentos, preço, FAQ, contato"

---

## 🐛 Cenário 3: Algo Não Funciona

### Como Iniciar

```
/debug [descreva o problema]
```

**Exemplos:**
```
/debug a página de login mostra tela branca
/debug quando clico em salvar nada acontece
/debug os dados não aparecem na tabela
```

### Dicas

- **Descreva o comportamento** — O que deveria acontecer vs o que está acontecendo
- **Diga quando começou** — "Funcionava antes, parou depois que mudamos X"
- **Mande print da tela** — Screenshots ajudam muito o diagnóstico

---

## 📈 Cenário 4: Melhorar Algo Existente

### Como Iniciar

```
/enhance [descreva a melhoria]
```

**Exemplos:**
```
/enhance adicionar modo escuro no app
/enhance melhorar performance da página de dashboard
/enhance adicionar filtro de busca na lista de clientes
```

---

## 🚢 Cenário 5: Hora de Publicar

### Como Iniciar

```
/deploy
```

O agente vai:
1. Rodar checklist de segurança automático
2. Verificar se todos os testes passam
3. Confirmar variáveis de ambiente
4. Guiar o deploy passo a passo

### Verificação Final Antes de Publicar

```
verificação final
```
ou
```
rode todos os testes
```

---

## 🏥 Cenário 6 (Novo!): Verificar a Saúde do Kit

Se algo parecer estranho com o comportamento do agente, ou antes de um trabalho importante:

```
checar kit
```
ou
```
diagnóstico do kit
```
ou
```
tudo certo?
```

O agente vai rodar `doctor.py` e confirmar que todos os 22 agentes, 62 skills e 20 workflows estão funcionando corretamente.

---

## 💡 Dicas de Comunicação com o Agente

### ✅ Jeitos BONS de Pedir

| O que quer | Como pedir |
|------------|-----------|
| Nova funcionalidade | "Quero que o usuário possa exportar relatório em PDF" |
| Mudança visual | "O botão de login precisa ficar mais visível, cor verde" |
| Correção | "Quando o usuário clica em salvar, às vezes perde os dados" |
| Melhoria | "O carregamento da página tá lento, demora uns 5 segundos" |
| Ideia vaga | "Quero algo parecido com isso: [link/print]" |
| Feature autônoma | "/ade [descreva tudo em uma frase longa]" |

### ❌ Não Precisa Dizer

| Não precisa | Por quê |
|-------------|---------|
| "Use React hooks" | O agente escolhe a melhor tecnologia |
| "Faça com TypeScript" | Já é padrão do kit |
| "Adicione validação de input" | O agente faz automaticamente |
| "Coloque tratamento de erro" | Já está nas regras |
| "Use o agente X" | O roteamento é automático |

### 🎯 A Regra de Ouro

> **Descreva o QUE você quer, não COMO fazer.**
>
> ❌ "Crie um useState com useEffect que faz fetch na API..."
> ✅ "Quero que a lista de produtos atualize automaticamente."

---

## 🔄 Fluxo Recomendado para Novos Projetos

```
1. /brainstorm          ← Explore a ideia com perguntas estratégicas
2. /build-saas          ← Planeje tudo em 7 etapas
3. /create              ← Construa o MVP
4. /enhance             ← Adicione features incrementalmente
5. /ade [feature]       ← Features complexas com pipeline autônomo
6. /debug               ← Corrija problemas
7. verificação final    ← Teste tudo antes de publicar
8. /deploy              ← Publique com segurança
```

---

## 🧠 Guia Completo: Agentes, Skills e Palavras-Chave

> Use qualquer termo abaixo — em **Português** ou **Inglês** — e o agente correto será ativado automaticamente.

### 🤖 Agentes Especialistas (20)

| Agente | O que faz | 🇧🇷 Termos PT-BR | 🇺🇸 Termos EN |
|--------|-----------|-------------------|---------------|
| **🎨 frontend-specialist** | Design, visual, layout, componentes | "muda o visual", "deixa mais bonito", "redesign", "tá feio", "interface moderna", "mudar as cores", "dark mode", "modo escuro", "esquema de cores" | "change design", "UI component", "button", "card", "layout", "style", "CSS", "responsive" |
| **⚙️ backend-specialist** | Servidor, API, rotas, lógica | "criar rota", "conectar o front", "servidor", "rota", "API", "endpoint" | "create endpoint", "server", "route", "API", "backend", "middleware" |
| **💾 database-architect** | Banco de dados, tabelas, SQL | "banco de dados", "tabela", "estrutura dos dados", "modelar dados", "schema do banco" | "database", "schema", "table", "query", "migration", "SQL", "prisma" |
| **📱 mobile-developer** | Apps mobile (React Native, Flutter) | "app mobile", "app para celular", "tela do celular", "app nativo" | "react native", "flutter", "ios", "android", "expo", "mobile app" |
| **🔍 debugger** | Conserta erros e bugs | "não funciona", "tá quebrado", "dando erro", "travou", "tela branca", "não carrega", "bugado", "caiu" | "error", "bug", "broken", "crash", "not working", "issue", "fix" |
| **🛡️ security-auditor** | Segurança, proteção, vulnerabilidades | "tá seguro?", "pode ser hackeado?", "verificar segurança", "proteger dados", "criptografar", "auditoria de segurança", "checar vulnerabilidades" | "security", "vulnerability", "auth", "login", "password", "encrypt", "audit" |
| **🧪 test-engineer** | Testes, qualidade, validação | "testar", "tá funcionando?", "verificar qualidade", "rode os testes", "garantir que funciona", "checklist de qualidade" | "test", "coverage", "unit test", "integration", "validate", "jest", "playwright" |
| **🚀 devops-engineer** | Deploy, CI/CD, Docker, servidor | "colocar no ar", "publicar", "deploy", "servidor caiu", "mandar pra produção" | "deploy", "CI/CD", "docker", "kubernetes", "hosting", "server" |
| **⚡ performance-optimizer** | Velocidade, otimização, Core Web Vitals | "tá lento", "demora pra carregar", "pesado", "melhorar velocidade", "site devagar", "fica travando" | "slow", "optimize", "speed", "performance", "cache", "lazy load" |
| **🌐 seo-specialist** | SEO, Google, visibilidade | "aparecer no Google", "melhorar posição", "SEO", "mais visitas orgânicas", "não aparece na busca" | "SEO", "meta tags", "sitemap", "ranking", "search engine", "analytics" |
| **🏗️ orchestrator** | Coordena múltiplos agentes | "tarefa complexa", "fazer tudo", "orquestrar", "coordenar" | "orchestrate", "multi-agent", "complex task", "coordinate" |
| **📋 project-planner** | Planejamento, discovery, roadmap | "planejar", "requisitos", "ideia", "funcionalidades", "MVP" | "plan", "requirements", "discovery", "roadmap", "MVP" |
| **🎮 game-developer** | Jogos 2D, 3D, multiplayer | "criar um jogo", "fazer um game", "jogo 2D", "mecânica de jogo" | "game", "unity", "godot", "phaser", "multiplayer" |
| **📄 documentation-writer** | Documentação, README, guias | "documentar", "README", "escrever os docs", "criar documentação" | "documentation", "README", "API docs", "write docs" |
| **🔬 explorer-agent** | Analisar codebase, explorar código | "analisar código", "visão geral", "listar arquivos", "entender o projeto" | "analyze", "list files", "overview", "explore codebase" |
| **🔧 code-archaeologist** | Código legado, refatoração | "refatorar", "código antigo", "limpar código", "organizar" | "refactor", "legacy code", "clean up", "reorganize" |
| **🧪 qa-automation-engineer** | Testes E2E, pipelines de teste | "testar o app inteiro", "simular usuário", "fluxo completo" | "E2E test", "end-to-end", "playwright", "test pipeline" |
| **🕵️ penetration-tester** | Testes de intrusão, red team | "simular ataque", "pentest", "teste de invasão" | "penetration test", "red team", "attack simulation" |
| **📊 product-manager** | Requisitos, histórias de usuário, backlog | "histórias de usuário", "o que o app precisa ter", "requisitos", "quem vai usar" | "user stories", "product requirements", "MVP", "backlog" |

---

### 💎 Skills Premium Design (Novo!)

| Skill | O que faz | 🇧🇷 Termos PT-BR | 🇺🇸 Termos EN |
|-------|-----------|-------------------|---------------|
| **🎨 premium-design-orchestrator** | Paletas, tipografia, design de alto nível | "design premium", "site premiado", "interface imersiva", "landing page premium", "experiência imersiva", "paleta premium", "tipografia premium" | "premium design", "awwwards", "immersive experience", "premium palette", "luxury design" |
| **🔍 brand-identity-extractor** | Extrai identidade visual de sites | "extrair identidade", "clonar design", "analisar referência", "extrair paleta", "copiar essência", "capturar o visual desse site" | "extract identity", "clone design", "analyze reference", "extract palette", "copy essence" |
| **⚡ premium-tech-stack** | Animações GSAP, scroll suave, 3D | "animações premium", "GSAP", "Three.js", "scroll suave", "transições de página", "5 pilares", "experiência imersiva" | "GSAP", "ScrollTrigger", "Three.js", "smooth scroll", "page transitions", "premium animations" |

---

### 🧠 Skills de Estratégia e IA

| Skill | O que faz | 🇧🇷 Termos PT-BR | 🇺🇸 Termos EN |
|-------|-----------|-------------------|---------------|
| **💾 agent-memory-mcp** | Memória persistente do agente | "lembrar contexto", "memória do agente", "lições" | "agent memory", "context", "lessons learned" |
| **🧪 agent-evaluation** | Avaliação de qualidade da IA | "avaliar a IA", "qualidade da resposta" | "evaluate AI", "agent quality", "performance" |
| **🤖 ai-engineer** | Construção de apps com LLM/IA | "construir com IA", "agente inteligente", "LLM" | "build with AI", "LLM app", "intelligent agent" |
| **📈 startup-analyst** | Análise de métricas de startup | "CAC", "LTV", "burn rate", "métricas de negócio" | "startup metrics", "CAC", "LTV", "burn rate" |
| **🚀 micro-saas-launcher** | Lançamento de micro-SaaS | "lançar SaaS", "MVP rápido", "indie hacker" | "launch SaaS", "quick MVP", "indie hacker" |

---

### 🔧 Skills Técnicas Essenciais

| Skill | O que faz | 🇧🇷 Termos PT-BR | 🇺🇸 Termos EN |
|-------|-----------|-------------------|---------------|
| **🧹 clean-code** | Código limpo, padrões de qualidade | "código limpo", "refatorar", "melhorar código" | "clean code", "refactor", "code quality" |
| **🧪 testing-patterns** | Estratégias de teste | "testar", "verificar qualidade", "rode os testes" | "testing", "unit test", "coverage", "TDD" |
| **🔐 vulnerability-scanner** | Scanner de vulnerabilidades | "checar vulnerabilidades", "seguro?", "auditoria" | "scan vulnerabilities", "security audit", "OWASP" |
| **📋 plan-writing** | Planejamento de tarefas detalhado | "planejar feature", "quebrar em tarefas" | "plan feature", "task breakdown", "implementation plan" |
| **🏗️ app-builder** | Construção de apps do zero | "criar do zero", "construir app", "novo projeto" | "build from scratch", "create app", "new project" |
| **💾 database-design** | Design de banco de dados | "modelar o banco", "estrutura de dados", "schema" | "database design", "data model", "schema", "SQL vs NoSQL" |
| **🔌 api-patterns** | Design de APIs | "criar API", "conectar front com back", "endpoints" | "API design", "REST", "GraphQL", "endpoints" |
| **🌐 seo-fundamentals** | SEO técnico e on-page | "aparecer no Google", "SEO", "meta tags" | "SEO", "search ranking", "meta tags", "sitemap" |
| **⚡ performance-profiling** | Core Web Vitals, otimização | "tá lento", "melhorar velocidade", "otimizar" | "performance", "Core Web Vitals", "optimize", "speed" |
| **📱 mobile-design** | Design mobile-first | "design pro celular", "interface mobile" | "mobile design", "touch interaction", "app design" |
| **🎨 frontend-design** | Design thinking para web | "melhorar o visual", "cores", "tipografia" | "visual design", "colors", "typography", "layout" |
| **🚢 deployment-procedures** | Deploy seguro | "colocar no ar", "publicar", "fazer deploy" | "deploy", "go live", "release", "production" |
| **🌍 i18n-localization** | Multi-idioma, traduções | "traduzir o app", "multi-idioma", "internacionalizar" | "translate", "multi-language", "localization", "i18n" |

---

### ⌨️ Comandos Slash (Atalhos Rápidos)

| Comando | 🇧🇷 Quando usar | 🇺🇸 When to use |
|---------|-----------------|-----------------|
| `/brainstorm` | Explorar uma ideia, fazer perguntas | Explore an idea, ask strategic questions |
| `/build-saas` | Planejar um SaaS completo em 7 etapas | Plan a complete SaaS in 7 steps |
| `/create` | Construir algo novo do zero | Build something new from scratch |
| `/plan` | Planejar uma feature sem codar | Plan a feature without coding |
| `/ade` | Pipeline autônomo (faz tudo sozinho) | Autonomous pipeline (does everything) |
| `/enhance` | Melhorar algo existente | Improve something existing |
| `/debug` | Investigar e corrigir um bug | Investigate and fix a bug |
| `/test` | Criar e rodar testes | Create and run tests |
| `/deploy` | Publicar em produção | Deploy to production |
| `/preview` | Ligar servidor local | Start local dev server |
| `/status` | Ver progresso do projeto | View project progress |
| `/ui-ux-pro-max` | Design premium com 50 estilos | Premium design with 50 styles |
| `/new-project` | Criar nova pasta de projeto | Create new project folder |
| `/orchestrate` | Coordenar tarefa multi-agente | Coordinate multi-agent task |

---

### 🏥 Comandos de Saúde do Kit

| Ação | 🇧🇷 Como chamar | 🇺🇸 How to call |
|------|-----------------|-----------------|
| Diagnóstico | "checar kit", "diagnóstico", "tudo certo?", "saúde do kit" | "check kit", "doctor", "kit health", "diagnostics" |
| Testes do kit | "rode os testes do kit", "verificar integridade" | "run kit tests", "verify integrity" |
| Verificação final | "verificação final", "rode todos os testes" | "final check", "run all tests" |
| Ver memória | "lições aprendidas", "o que aprendemos" | "lessons learned", "gotchas", "memory" |


---

## ❓ Perguntas Frequentes

**P: Preciso saber programar?**
R: Não. O agente programa para você. Sua função é dar a direção e aprovar as entregas.

**P: O agente vai me fazer perguntas técnicas?**
R: Não. As perguntas são estratégicas (público, funcionalidades, monetização). Decisões técnicas são automáticas.

**P: E se eu quiser mudar algo depois?**
R: Basta pedir. "Muda o esquema de cores para azul escuro" ou "Adiciona uma página de FAQ".

**P: Posso usar em qualquer tipo de projeto?**
R: Sim. O kit funciona para SaaS, landing pages, apps mobile, jogos, APIs, e muito mais.

**P: O que é `/build-saas`?**
R: É um assistente que te faz as perguntas certas em 7 etapas e gera 3 documentos prontos: especificação do backend, do frontend, e um plano de implementação com tarefas de 5-15 minutos.

**P: Qual a diferença entre `/create` e `/ade`?**
R: `/create` é interativo (o agente faz perguntas e você responde). `/ade` é autônomo (o agente faz tudo, te mostra o plano e aguarda apenas sua aprovação antes de codar).

**P: O que acontece se o agente "travar" ou ficar repetindo?**
R: O kit tem proteção automática contra loops. Se perceber que está em loop, basta dizer **"para"** ou **"cancelar"**. O agente vai encerrar a tarefa e perguntar o que você prefere fazer.

**P: Meu código fica salvo em algum lugar?**
R: Sim, no seu repositório GitHub. Cada mudança aprovada pode ser salva com `git commit`.

---

> 💡 **Lembre-se:** Você é o dono do produto. O agente é sua equipe de desenvolvimento.
> Diga o que quer alcançar — ele cuida do resto.
