# 📚 DevBureau - Guia Completo do Usuário

> **Bem-vindo!** Este guia mostra como usar o DevBureau do zero. Se você é novo aqui, comece pelo **[Passo 1](#início-rápido)**.

---

## 📑 Sumário (Clique para ir direto)

1. [Início Rápido](#início-rápido) — Configure em 2 minutos
2. [O Que é DevBureau?](#o-que-é-devbureau) — Entenda a base
3. [Seus Primeiros Passos](#seus-primeiros-passos) — Escolha seu caminho
4. [Como Usar (Por Tarefa)](#como-usar-por-tarefa) — Exemplos práticos
5. [Todos os Comandos](#todos-os-comandos) — Referência rápida
6. [Especialistas Disponíveis](#especialistas-disponíveis) — Quem faz o quê
7. [Perguntas Frequentes](#perguntas-frequentes)
8. [Configurações Avançadas](#configurações-avançadas)

---

## Início Rápido

### ⚡ Configure em 2 Minutos

Você baixou o DevBureau? Ótimo! Agora execute **UM COMANDO** para ativar tudo:

```bash
python .agent/scripts/sync_ide.py --target all
```

**Pronto!** Sua IDE (Cursor, Claude, VS Code) agora entende os poderes do DevBureau automaticamente.

### ✅ Verificar se Funcionou

Para confirmar que tudo está operacional:

```bash
checar kit
```

ou

```bash
python .agent/scripts/doctor.py
```

Se vir mensagens verdes com "✅ OK", significa que os **agentes e skills estão prontos**. Você está pronto para começar!

---

## O Que é DevBureau?

### 🤖 A Ideia Simples

Imagine que você tem uma **equipe de especialistas** que trabalham para você:

- 🎨 Designer frontend (visual, cores, layout)
- ⚙️ Engenheiro backend (servidor, API, lógica)
- 💾 Arquiteto de banco de dados (organização de dados)
- 🧪 Testador (verifica qualidade)
- 🛡️ Especialista de segurança
- 🚀 Especialista de deploy
- ...e muitos outros

**Você nunca precisa fazer nada sozinho.** Você descreve o que quer, eles fazem.

### 💡 Como Funciona

```
Você: "Quero um sistema de login com Google"
              ↓
DevBureau analisa e pensa: "Preciso de backend? Frontend? Segurança?"
              ↓
Especialistas relevantes trabalham juntos
              ↓
Você aprova o plano
              ↓
Código pronto
              ↓
Você publica
```

---

## Seus Primeiros Passos

### Escolha Seu Momento Atual

Qual é sua situação? Clique abaixo:

#### 1️⃣ Não Tenho a Pasta do Projeto Criada Ainda

**Situação:** Tenho uma ideia, mas ainda não criei a pasta do projeto.

**Comando:**

```
/new-project
```

**O que acontece:**

- DevBureau cria uma nova pasta com toda a inteligência
- Você recebe um "mapa" com os primeiros passos
- Pronto para usar em 30 segundos

---

#### 2️⃣ Tenho a Pasta, Mas Minha Ideia é Vaga

**Situação:** Criei a pasta, mas ainda não sei exatamente o que construir.

**Comando:**

```
/brainstorm
```

**O que acontece:**

- DevBureau faz 5-7 perguntas estratégicas
- Você responde simples (público-alvo, problema que resolve, principais funcionalidades)
- Ao final: ideia clara e estruturada
- Tempo: ~10 minutos

**Exemplo de conversa:**

```
DevBureau: Quem vai usar isso?
Você: Personal trainers que querem gerenciar alunos

DevBureau: Qual é o maior problema deles hoje?
Você: Não conseguem ver o progresso de todos os alunos em um único lugar

DevBureau: Qual é a funcionalidade mais importante?
Você: Um dashboard que mostra todos os alunos e o progresso de cada um
```

---

#### 3️⃣ Ideia Clara, Quero Desenhar o Sistema

**Situação:** Tenho a ideia clara. Quero saber como fazer antes de codar.

**Comando:**

```
/build-saas [descreva sua ideia em uma frase]
```

**Exemplo:**

```
/build-saas aplicativo para personal trainers gerenciarem alunos, treinos e evolução física
```

**O que acontece:**

- DevBureau guia você por **7 etapas** de planejamento
- Você responde uma pergunta por vez (não são técnicas, são simples)
- Ao final: **3 documentos prontos** para implementar
- Você VÊ tudo antes de uma linha de código ser escrita

**As 7 Etapas:**

1. **Discovery** — Quem usa? Qual problema resolve?
2. **Requisitos** — Quais funcionalidades principais?
3. **Banco de Dados** — Qual é a estrutura dos dados?
4. **Backend** — Qual é a estrutura do servidor?
5. **Frontend** — Quais são as telas e componentes?
6. **Segurança** — Como proteger os dados?
7. **Documentação** — Gera os 3 documentos finais

**Tempo total:** ~30-45 minutos

---

#### 4️⃣ Quero Que Tudo Seja Automático (Mãos Livres)

**Situação:** Não quero responder perguntas. Quero que o agente faça tudo sozinho.

**Comando:**

```
/ade [descreva sua ideia com detalhes]
```

**Exemplo:**

```
/ade Crie um aplicativo para personal trainers gerenciarem alunos e treinos. Preciso de:
- Dashboard com lista de alunos
- Histórico de treinos por aluno
- Evolução de peso
- Login com Google
- Interface responsiva para mobile e desktop
```

**O que acontece (Pipeline Autônomo):**

```
1. Discovery — DevBureau entende sua ideia
2. Spec — Cria o plano detalhado
3. ⏸️  VOCÊ APROVA (antes de codar)
4. Código — Implementa tudo automaticamente
5. Testes — Verifica se funciona
6. ✅ Pronto para usar
```

**Vantagem:** Você só aprova UMA VEZ, e o agente faz tudo. Tempo: ~2-4 horas.

---

#### 5️⃣ Quero Construir Junto, Passo a Passo

**Situação:** Quero ver o processo acontecer. Quero aprender ou acompanhar de perto.

**Comando:**

```
/create [descreva o que quer]
```

**Exemplo:**

```
/create dashboard para personal trainers com lista de alunos e histórico de treinos
```

**O que acontece:**

- DevBureau conversa com você enquanto cria os arquivos
- Você aprova cada etapa
- Aprende o que está sendo feito
- Tempo: ~3-5 horas

---

### Qual Escolher?

| Sua Situação       | Comando        | Tempo     | Para Quem                  |
| ------------------ | -------------- | --------- | -------------------------- |
| Sem projeto criado | `/new-project` | 30 seg    | Quem está começando        |
| Ideia vaga         | `/brainstorm`  | 10 min    | Quem quer clareza antes    |
| Ideia clara        | `/build-saas`  | 30-45 min | Quem quer ver o plano      |
| Quer automático    | `/ade`         | 2-4 horas | Quem quer resultado rápido |
| Quer aprender      | `/create`      | 3-5 horas | Quem gosta de acompanhar   |

---

## Como Usar (Por Tarefa)

### 🎯 Você Quer Fazer Isso? Clique Aqui

#### Criar um Sistema Novo (SaaS, App, Site)

**Você diz:** Quero criar um aplicativo de agenda para salões de beleza

**Você usa:** `/build-saas` ou `/ade` ou `/create`

**Passo a passo:**

1. Escolha um dos comandos acima (veja "Seus Primeiros Passos")
2. Descreva sua ideia
3. Responda as perguntas (simples, sem técnica)
4. Aprove o plano
5. Código é gerado automaticamente

**Exemplo completo:**

```
/build-saas Sistema de agendamento para salões de beleza com gerenciamento de clientes, serviços e horários
```

---

#### Adicionar uma Funcionalidade Nova

**Você diz:** Quero adicionar um sistema de notificações por email quando alguém marca um horário

**Você usa:** `/ade [descreva a funcionalidade]`

**Exemplo:**

```
/ade Adicione um sistema de notificações por email quando um cliente marca um horário.
O email deve conter: nome do serviço, horário, profissional responsável.
Também envie um lembrete 1 dia antes do agendamento.
```

**O que você recebe:**

- Plano detalhado (você aprova)
- Código implementado
- Testes passando
- Pronto para usar

---

#### Consertar um Bug (Algo Não Funciona)

**Você diz:** O login não funciona quando uso Chrome

**Você usa:** `/debug [descreva o problema]`

**Exemplo:**

```
/debug O botão de login não funciona no Chrome. Funciona perfeitamente no Firefox.
Quando clico, a tela fica branca e nada acontece. Comecei a ter esse problema
depois que atualizei as dependências.
```

**O que acontece:**

1. Especialista investiga
2. Encontra a causa
3. Corrige
4. Testa
5. Pronto

---

#### Melhorar Algo Que Já Existe

**Você diz:** O design da landing page ficou velho. Quero algo mais moderno.

**Você usa:** `/enhance [descreva a melhoria]`

**Exemplos:**

```
/enhance Deixe o design da landing page mais moderno. Adicione:
- Animações suaves
- Paleta de cores mais moderna (azul + branco + laranja)
- Cards com sombra
- Fonte maior nos títulos
```

ou

```
/enhance Melhoramos a performance do dashboard. Estava demorando 5 segundos para carregar.
Preciso reduzir para menos de 2 segundos.
```

---

#### Testar Qualidade

**Você diz:** Antes de publicar, quero ter certeza que tudo funciona

**Você usa:**

```
verificação final
```

ou

```
rode todos os testes
```

**O que acontece:**

1. ✅ Segurança — Sem vulnerabilidades?
2. ✅ Linter — Código limpo?
3. ✅ Tipos — TypeScript correto?
4. ✅ Testes — Tudo passa?
5. ✅ Performance — Lighthouse OK?
6. ✅ UX — Interface responsiva?

Se tudo passar, você recebe um "✅ Pronto para publicar"

---

#### Publicar em Produção

**Você diz:** Pronto! Quero colocar no ar.

**Você usa:**

```
/deploy
```

**O que acontece:**

1. Checklist automático de segurança
2. Verifica se todos os testes passam
3. Confirma variáveis de ambiente
4. Guia você passo a passo no deploy
5. Publica com segurança

---

#### Ver o App Rodando

**Você diz:** Quero ver meu app funcionando agora

**Você usa:**

```
/preview
```

**O que acontece:**

- Servidor local liga automaticamente
- Abre seu navegador
- Você vê o app rodando em tempo real
- Pode testar, clicar, preencher formulários

---

#### Ver Progresso do Projeto

**Você diz:** Como está o progresso? Quanto falta?

**Você usa:**

```
/status
```

**O que você vê:**

- ✅ Funcionalidades prontas
- 🔄 Em progresso
- ⏳ Planejado
- Porcentagem de conclusão

---

### 🤖 Ativar um Especialista Específico

Além dos comandos rápidos, você pode ativar um especialista específico escrevendo `@nome`:

**Como usar:**

```
@frontend-specialist: melhora o design dessa página, deixa mais moderna

@backend-specialist: cria uma rota para salvar dados de clientes

@security-auditor: verifica se o app está seguro

@database-architect: cria a tabela de usuários com os campos certos
```

**Todos os especialistas disponíveis:**

| Especialista                 | Usa quando...                        | Comando                   |
| ---------------------------- | ------------------------------------ | ------------------------- |
| 🎨 Designer Frontend         | Quer melhorar visual, cores, layout  | `@frontend-specialist`    |
| ⚙️ Engenheiro Backend        | Quer criar API, servidor, rotas      | `@backend-specialist`     |
| 💾 Arquiteto de Banco        | Quer estruturar dados, criar tabelas | `@database-architect`     |
| 📱 Dev Mobile                | Quer criar app iOS/Android           | `@mobile-developer`       |
| 🔍 Debugger                  | Tem um bug, quer consertar           | `@debugger`               |
| 🛡️ Auditor de Segurança      | Quer verificar se está seguro        | `@security-auditor`       |
| 🧪 Testador                  | Quer testar e garantir qualidade     | `@test-engineer`          |
| 🚀 DevOps                    | Quer fazer deploy ou infraestrutura  | `@devops-engineer`        |
| ⚡ Otimizador de Performance | Quer deixar mais rápido              | `@performance-optimizer`  |
| 🌐 Especialista SEO          | Quer aparecer no Google              | `@seo-specialist`         |
| 📋 Planejador                | Quer planejar tarefas                | `@project-planner`        |
| 🎮 Dev de Games              | Quer criar um jogo                   | `@game-developer`         |
| 📄 Documentador              | Quer documentar o projeto            | `@documentation-writer`   |
| 🔬 Explorador                | Quer analisar o codebase             | `@explorer-agent`         |
| 🔧 Arqueólogo de Código      | Tem código antigo, quer refatorar    | `@code-archaeologist`     |
| 🧪 QA Automation             | Quer testes automáticos              | `@qa-automation-engineer` |
| 🕵️ Pentester                 | Quer testar segurança (ataques)      | `@penetration-tester`     |
| 🤖 Orquestrador              | Quer múltiplos especialistas         | `@orchestrator`           |
| 📊 Product Manager           | Quer pensar em requisitos            | `@product-manager`        |
| 📚 Content Creator           | Quer criar conteúdo/posts            | `@content-creator`        |
| ♿ Especialista Acessibilidade | Quer o app usável por todos (WCAG)  | `@accessibility-specialist` |
| 🔌 Designer de API           | Quer desenhar o contrato da API      | `@api-designer`           |
| 👨‍💼 SRE Engineer              | Quer observabilidade e monitoramento | `@sre-engineer`           |

---

## Todos os Comandos

### 📋 Referência Completa

#### Comandos de Criação e Planejamento

| Comando        | O que faz                                       | Exemplo                         |
| -------------- | ----------------------------------------------- | ------------------------------- |
| `/new-project` | Cria uma nova pasta com o kit completo          | `/new-project`                  |
| `/brainstorm`  | Faz perguntas estratégicas para clarear a ideia | `/brainstorm`                   |
| `/build-saas`  | Planeja um SaaS em 7 etapas                     | `/build-saas app de delivery`   |
| `/plan`        | Planeja uma funcionalidade sem codar            | `/plan sistema de pagamentos`   |
| `/create`      | Cria algo do zero, passo a passo                | `/create landing page`          |
| `/ade`         | Pipeline autônomo (faz tudo sozinho)            | `/ade crie um login com Google` |

#### Comandos de Desenvolvimento

| Comando    | O que faz                   | Exemplo                                |
| ---------- | --------------------------- | -------------------------------------- |
| `/enhance` | Melhora algo existente      | `/enhance deixe o design mais moderno` |
| `/debug`   | Encontra e corrige bugs     | `/debug o login não funciona`          |
| `/test`    | Cria e roda testes          | `/test`                                |
| `/preview` | Abre o servidor local       | `/preview`                             |
| `/status`  | Mostra progresso do projeto | `/status`                              |

#### Comandos de Deploy e Publicação

| Comando                | O que faz                              |
| ---------------------- | -------------------------------------- |
| `/deploy`              | Checklist de segurança e publica       |
| `verificação final`    | Roda todos os testes antes de publicar |
| `rode todos os testes` | Executa suite de testes                |

#### Comandos de Saúde do Kit

| Comando       | O que faz                                     |
| ------------- | --------------------------------------------- |
| `checar kit`  | Diagnóstico completo (todos os agentes, skills e workflows) |
| `diagnóstico` | Mesmo que acima                               |
| `tudo certo?` | Verifica integridade                          |

#### Comando Premium Design

| Comando          | O que faz                          | Tempo     |
| ---------------- | ---------------------------------- | --------- |
| `/ui-ux-pro-max` | 50 estilos visuais premium prontos | 2-3 horas |

---

## Especialistas Disponíveis

### 🎨 Design (Frontend + Mobile)

#### **Frontend Specialist** — Designer Web

- **Quando usar:** Visual, cores, layout, botões, responsividade
- **Exemplos:** "melhora o visual", "dark mode", "deixa mais moderno"
- **Comando:** `@frontend-specialist`

#### **Mobile Developer** — Dev de Apps

- **Quando usar:** App iOS, Android, React Native, Flutter
- **Exemplos:** "cria um app mobile", "interface para celular"
- **Comando:** `@mobile-developer`

---

### ⚙️ Backend (Servidores e Lógica)

#### **Backend Specialist** — Engenheiro de Servidor

- **Quando usar:** API, rotas, servidor, autenticação, lógica de negócio
- **Exemplos:** "cria uma rota", "conecta frontend com backend"
- **Comando:** `@backend-specialist`

#### **Database Architect** — Especialista de Banco de Dados

- **Quando usar:** Estrutura de dados, tabelas, SQL, migrations
- **Exemplos:** "modelar dados", "criar tabela de usuários"
- **Comando:** `@database-architect`

---

### 🛡️ Qualidade e Segurança

#### **Security Auditor** — Auditor de Segurança

- **Quando usar:** Vulnerabilidades, criptografia, proteção de dados
- **Exemplos:** "o site está seguro?", "verificar vulnerabilidades"
- **Comando:** `@security-auditor`

#### **Test Engineer** — Testador

- **Quando usar:** Testes, cobertura, validação de qualidade
- **Exemplos:** "testar", "verificar qualidade"
- **Comando:** `@test-engineer`

#### **Debugger** — Especialista em Bugs

- **Quando usar:** Algo não funciona, erro, bug, tela branca
- **Exemplos:** "não funciona", "tá quebrado", "erro 404"
- **Comando:** `@debugger`

---

### 🚀 Deploy e Performance

#### **DevOps Engineer** — Especialista de Infraestrutura

- **Quando usar:** Deploy, CI/CD, Docker, servidor, publicação
- **Exemplos:** "colocar no ar", "fazer deploy", "servidor caiu"
- **Comando:** `@devops-engineer`

#### **Performance Optimizer** — Otimizador de Velocidade

- **Quando usar:** Site lento, otimização, cache, bundle grande
- **Exemplos:** "tá lento", "melhorar velocidade", "Core Web Vitals"
- **Comando:** `@performance-optimizer`

---

### 📊 Estratégia e Conteúdo

#### **Project Planner** — Planejador de Projetos

- **Quando usar:** Planejamento, requisitos, descoberta, roadmap
- **Exemplos:** "planejar", "quais são os requisitos?"
- **Comando:** `@project-planner`

#### **Product Manager** — Gerente de Produto

- **Quando usar:** Histórias de usuário, requisitos, backlog
- **Exemplos:** "histórias de usuário", "requisitos do app"
- **Comando:** `@product-manager`

#### **Content Creator** — Criador de Conteúdo

- **Quando usar:** Posts, carrosséis, conteúdo para redes sociais
- **Exemplos:** "cria um post", "design de carousel"
- **Comando:** `@content-creator`

---

### 🔬 Análise e Especialidades

#### **Orchestrator** — Orquestrador

- **Quando usar:** Tarefa complexa que envolve múltiplos especialistas
- **Exemplos:** "tarefa complexa", "fazer tudo"
- **Comando:** `@orchestrator`

#### **Explorer Agent** — Explorador de Codebase

- **Quando usar:** Analisar código, entender projeto, listar arquivos
- **Exemplos:** "analisar código", "visão geral do projeto"
- **Comando:** `@explorer-agent`

#### **Code Archaeologist** — Arqueólogo de Código

- **Quando usar:** Refatorar código antigo, limpar código, reorganizar
- **Exemplos:** "refatorar", "código antigo", "limpar código"
- **Comando:** `@code-archaeologist`

---

### 📖 Documentação e Específicas

#### **Documentation Writer** — Documentador

- **Quando usar:** README, documentação, guias, API docs
- **Exemplos:** "documentar", "escrever README"
- **Comando:** `@documentation-writer`

#### **SEO Specialist** — Especialista em SEO

- **Quando usar:** Aparecer no Google, rankings, visibilidade
- **Exemplos:** "aparecer no Google", "melhorar SEO"
- **Comando:** `@seo-specialist`

#### **QA Automation Engineer** — Testador de E2E

- **Quando usar:** Testes automáticos, Playwright, pipelines de teste
- **Exemplos:** "testar o app inteiro", "E2E test"
- **Comando:** `@qa-automation-engineer`

---

### 🎮 Especializações Adicionais

#### **Game Developer** — Dev de Games

- **Quando usar:** Criar jogos 2D, 3D, multiplayer
- **Exemplos:** "criar um jogo", "mecânica de jogo"
- **Comando:** `@game-developer`

#### **Penetration Tester** — Testador de Segurança

- **Quando usar:** Teste de invasão, red team, pentest
- **Exemplos:** "simular ataque", "teste de invasão"
- **Comando:** `@penetration-tester`

---

## Perguntas Frequentes

### ❓ Dúvidas Comuns

#### P: Preciso saber programar para usar DevBureau?

**R:** Não. O kit programa para você. Sua função é descrever o que quer e aprovar o resultado.

#### P: O agente vai me fazer perguntas técnicas?

**R:** Não. As perguntas são estratégicas (público-alvo, funcionalidades, monetização). Decisões técnicas são automáticas.

#### P: E se eu quiser mudar algo depois?

**R:** Basta pedir naturalmente. "Muda o esquema de cores para azul" ou "Adiciona uma página de FAQ".

#### P: Posso usar em qualquer tipo de projeto?

**R:** Sim. Funciona para SaaS, landing pages, apps mobile, jogos, APIs, e-commerce, e muito mais.

#### P: Qual a diferença entre `/build-saas`, `/create` e `/ade`?

**R:**

- **`/build-saas`** — Planeja em 7 etapas, você responde perguntas. Melhor para entender tudo antes de codar.
- **`/create`** — Cria passo a passo, conversando com você. Melhor se quer aprender.
- **`/ade`** — Faz tudo autônomo, você aprova UMA VEZ. Melhor se quer velocidade.

#### P: O agente pode ficar em loop (repetindo)?

**R:** Sim, mas o kit tem proteção. Se perceber, basta dizer "para", "cancela" ou "reset". O agente vai parar.

#### P: Como faço backup do meu código?

**R:** Tudo é salvo em Git. Cada mudança pode ser salva com `git commit`. Seu código está protegido.

#### P: Quanto custa?

**R:** DevBureau é gratuito. Você usa sua conta Claude (Cursor, claude.ai, ou extensão IDE).

#### P: Posso deletar algo com segurança?

**R:** Tudo é versionado em Git. Se deletar algo, pode recuperar com `git revert` ou `git restore`.

#### P: Qual é o tamanho máximo de projeto que posso fazer?

**R:** Sem limite. DevBureau funciona de MVPs a aplicações complexas com milhões de usuários.

#### P: O que é uma "Skill"?

**R:** Uma skill é um superpoder. Exemplos: "humanizer" (remove cara de IA do texto), "content-creator" (cria posts para redes sociais).

#### P: O que é um "Squad"?

**R:** Um squad é uma equipe especializada para um processo específico. Exemplo: "squad de content production" para criar posts, imagens, emails automaticamente.

---

## Configurações Avançadas

### 🔓 Plano Aprovado = Trabalho Sem Interrupções (Claude Code)

Quando você aprova um plano, o agente executa do início ao fim **sem pedir permissão a cada passo** para as ações seguras do dia a dia: editar código, criar arquivos, rodar testes, fazer commits locais e instalar dependências do projeto. Isso vem configurado de fábrica (o `sync_ide.py` grava as pré-aprovações em `.claude/settings.json` de todo projeto que usa o kit).

O agente **ainda vai parar e perguntar** antes de qualquer ação que publica ou destrói algo: enviar código para o repositório remoto (`git push`), apagar arquivos, descartar mudanças de forma irreversível ou qualquer ação de produção. Esse é o freio de segurança da Matriz de Decisão do kit, e recomendamos não removê-lo.

Suas próprias regras vencem: se você já configurou permissões no `.claude/settings.json`, o kit só acrescenta as dele, nunca sobrescreve as suas. Para revisar ou ajustar, use o comando `/permissions` dentro do Claude Code.

---

### 🔧 Para Usuários Experientes

#### Configurar Seu IDE (VSCode, Cursor, JetBrains)

Já executou o comando de setup?

```bash
python .agent/scripts/sync_ide.py --target all
```

Se não, execute agora. Isso cria:

- `.cursorrules` — Regras para Cursor
- `.clauderules` — Regras para Claude
- Configurações automáticas para seu IDE

---

#### Usar DevBureau com Google Gemini

Se você usa **Gemini Code Assist** (VS Code ou IntelliJ):

- Não precisa executar nenhum comando especial
- O Gemini analisa a pasta `.agent/` automaticamente
- Ainda assim, executar `sync_ide.py` é recomendado

Se você usa **Google AI Studio ou Gemini Advanced** (web):

1. Abra [.agent/rules/DEVBUREAU.md](./.agent/rules/DEVBUREAU.md)
2. Copie todo o conteúdo
3. Cole na seção de "System Instructions" do seu chat
4. Pronto!

---

#### Ler os Detalhes Técnicos

Para usuários que querem entender a arquitetura:

**Leia nesta ordem:**

1. `.agent/ARCHITECTURE.md` — Visão geral de agentes e skills
2. `.agent/rules/DEVBUREAU.md` — Todas as regras detalhadas
3. `.agent/SCRIPTS_REGISTRY.md` — Lista de todos os scripts disponíveis

---

#### Criar uma Skill Personalizada

Se você quer criar um novo superpoder:

```bash
/skillify
```

Isso guia você para criar sua própria skill reutilizável.

---

#### Criar um Squad (Equipe Especializada)

Se você quer montar uma equipe para um processo específico:

```
/squad [descreva o processo]
```

**Exemplo:**

```
/squad Criar um sistema automático que:
1. Pesquisa notícias sobre marketing
2. Seleciona as 5 melhores
3. Cria posts para Instagram
4. Cria posts para LinkedIn
5. Publica automaticamente
```

DevBureau cria uma pasta `squads/marketing-automation/` com todo o setup.

---

#### Verificar Integridade do Kit

Se algo parecer errado:

```bash
python .agent/scripts/doctor.py
```

Isso verifica:

- ✅ Todos os agentes estão prontos?
- ✅ Todas as skills funcionam?
- ✅ Scripts estão configurados?
- ✅ Dependências OK?

---

### 📚 Leitura Recomendada Adicional

Se você quer aprender mais:

| Interesse               | Arquivo                      |
| ----------------------- | ---------------------------- |
| Guia de Skills          | `.agent/skills/*/SKILL.md`   |
| Documentação de Agentes | `.agent/agents/*/[nome].md`  |
| Registro de Scripts     | `.agent/SCRIPTS_REGISTRY.md` |
| Arquitetura do Kit      | `.agent/ARCHITECTURE.md`     |
| Todas as Regras         | `.agent/rules/DEVBUREAU.md`  |

---

## 🚀 Próximos Passos

### Comece Agora!

1. **Execute o setup:**

    ```bash
    python .agent/scripts/sync_ide.py --target all
    ```

2. **Verifique:**

    ```bash
    checar kit
    ```

3. **Escolha seu caminho** (volta ao início):
    - Ideia vaga → `/brainstorm`
    - Ideia clara → `/build-saas`
    - Quer rápido → `/ade`
    - Quer aprender → `/create`

4. **Aproveite os especialistas** mencionando `@nome` quando precisar

---

## 📞 Precisa de Ajuda?

### Para Erros ou Dúvidas

1. **Tente primeiro:** `checar kit` (diagnóstico automático)
2. **Se não resolver:** Procure no **[Perguntas Frequentes](#perguntas-frequentes)** acima
3. **Se ainda não resolver:** Abra uma issue ou procure a documentação em `.agent/rules/DEVBUREAU.md`

---

> **Parabéns!** Você agora sabe como usar DevBureau.
>
> Lembre-se: **Você é o dono do produto. DevBureau é sua equipe de desenvolvimento.**
>
> 🎉 Bom trabalho!
