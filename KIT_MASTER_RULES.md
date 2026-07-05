# 📜 Regras de Manutenção do DevBureau

> **MANDATÓRIO:** Este documento deve ser lido por qualquer agente de IA antes de modificar a estrutura do kit (agents, skills, workflows, scripts). A referência que garante essa leitura está em `.agent/rules/DEVBUREAU.md` (seção "Eficiência Operacional"), propagada a todas as IDEs via `sync_ide.py`.

## 🎯 Missão do Projeto
Este repositório NÃO é uma aplicação final. Ele é um **Framework de Desenvolvimento Agente-Assistido**. Sua função é servir de base (molde) para que usuários não programadores criem outros sistemas com qualidade de equipe profissional.

## 🛡️ Princípios de Evolução
1.  **Simplicidade para o Usuário (P0):** Toda funcionalidade nova deve ser explicada no `GUIA_DO_USUARIO.md` em linguagem de negócios.
2.  **Estrutura "Clean" (P0):** Mantenha a separação clara entre `.agent/` (Inteligência) e `web/` (Exemplo/Painel).
3.  **Rastreabilidade de Mudanças (P1):** Sempre que adicionar uma melhoria relevante, documente no `CHANGELOG.md`.
4.  **Auto-Diagnóstico (escopo do doctor):** O `doctor.py` valida apenas os scripts essenciais à saúde estrutural do kit (`checklist.py` e `verify_all.py` obrigatórios; `doctor.py` e `sync_ide.py` opcionais) — não todos os scripts. Script novo entra primeiro no `.agent/SCRIPTS_REGISTRY.md` (Protocolo Script-First) e só é adicionado ao `doctor.py` se a ausência dele quebrar o funcionamento do kit. O `doctor.py` é leve (checagens de arquivo, <1s) e roda automaticamente só no pre-commit; fora isso, apenas sob demanda ("checar kit", `/ade`, `/new-project`).
5.  **Sincronização de Documentos (P0):** Sempre que um agent, skill, workflow ou script mestre for adicionado ou removido, atualize NO MESMO COMMIT: `.agent/ARCHITECTURE.md` (tabelas e contagens), os badges e contagens de `README.md` e `README_pt-BR.md` (sempre na versão mais nova do `package.json`), e `GUIA_DO_USUARIO.md`/`USER_GUIDE.md` se a mudança for visível ao usuário. O teste `TestDocsSync` em `.agent/tests/test_kit_integrity.py` compara esses números com o disco e **bloqueia o commit** se estiverem defasados.
6.  **Zero-Break na Base:** Como este kit será copiado para outros projetos, ele deve ser extremamente estável. Nunca suba código que quebre os testes do `pytest`.
7.  **Benchmarking Contínuo (P2):** Periodicamente, rode `/benchmark` para comparar agentes/skills/workflows do kit contra coleções externas bem avaliadas (ver `.agent/skills/framework-benchmarking/`). O comando só gera recomendações em `.agent/memory/benchmark-log.md` — nenhuma mudança é aplicada automaticamente. Mais agentes/skills não é o objetivo; preencher gaps reais sem violar a filosofia de tiers (`stack-sizing`) é.
8.  **Toda Skill Nova Segue `writing-skills` (P1):** Ao criar uma skill nova (não retroativo às já existentes), a `description:` declara quando usar, não o que contém, e a instrução foi validada contra um cenário de pressão real antes de entrar no catálogo. Ver `.agent/skills/writing-skills/SKILL.md`.

## 👥 Conceito de Equipe Profissional
Sempre que o usuário interagir, trate os agentes como uma equipe:
- **Product Manager**: Analisa o `/ade` e o `/build-saas`.
- **Tech Lead**: Valida a arquitetura em `.agent/ARCHITECTURE.md`.
- **QA Engineer**: Roda o `checklist.py` e os testes.
- **Frontend/Backend Specialists**: Executam o código seguindo padrões SOLID.

## 🚀 Como Atualizar Corretamente
1.  **Analisar**: Entenda o impacto da mudança em novos projetos que usarão esta base.
2.  **Implementar**: Código limpo, com tipagem (Type Hints em Python, TS no Front).
3.  **Documentar**: Atualize `README.md` ou `GUIA_DO_USUARIO.md`.
4.  **Validar**: Rodar `python .agent/scripts/doctor.py` e garantir 100% de aprovação.
