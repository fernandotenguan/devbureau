# 📜 Regras de Manutenção do DevBureau

> **MANDATÓRIO:** Este documento deve ser lido por qualquer agente de IA ao iniciar uma sessão neste repositório.

## 🎯 Missão do Projeto
Este repositório NÃO é uma aplicação final. Ele é um **Framework de Desenvolvimento Agente-Assistido**. Sua função é servir de base (molde) para que usuários não programadores criem outros sistemas com qualidade de equipe profissional.

## 🛡️ Princípios de Evolução
1.  **Simplicidade para o Usuário (P0):** Toda funcionalidade nova deve ser explicada no `GUIA_DO_USUARIO.md` em linguagem de negócios.
2.  **Estrutura "Clean" (P0):** Mantenha a separação clara entre `.agent/` (Inteligência) e `web/` (Exemplo/Painel).
3.  **Rastreabilidade de Mudanças (P1):** Sempre que adicionar uma melhoria relevante, documente no `CHANGELOG.md`.
4.  **Auto-Diagnóstico:** Qualquer script novo (`.py`) deve ser integrado ao `doctor.py` para validação automática de saúde do kit.
5.  **Zero-Break na Base:** Como este kit será copiado para outros projetos, ele deve ser extremamente estável. Nunca suba código que quebre os testes do `pytest`.
6.  **Benchmarking Contínuo (P2):** Periodicamente, rode `/benchmark` para comparar agentes/skills/workflows do kit contra coleções externas bem avaliadas (ver `.agent/skills/framework-benchmarking/`). O comando só gera recomendações em `.agent/memory/benchmark-log.md` — nenhuma mudança é aplicada automaticamente. Mais agentes/skills não é o objetivo; preencher gaps reais sem violar a filosofia de tiers (`stack-sizing`) é.
7.  **Toda Skill Nova Segue `writing-skills` (P1):** Ao criar uma skill nova (não retroativo às já existentes), a `description:` declara quando usar, não o que contém, e a instrução foi validada contra um cenário de pressão real antes de entrar no catálogo. Ver `.agent/skills/writing-skills/SKILL.md`.

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
