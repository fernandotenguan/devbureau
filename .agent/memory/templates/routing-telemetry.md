# Routing Telemetry — DevBureau

> Registro de cada roteamento de agente em pedidos COMPLEX CODE / DESIGN / multi-domínio, para medir se o `intelligent-routing` está escolhendo o especialista certo, em vez de assumir que sim. Uma linha por roteamento, preenchida pelo agente no fim da interação (ver `.agent/rules/DEVBUREAU.md`, seção "INTELLIGENT AGENT ROUTING"). Mesmo formato e disciplina de `gate-telemetry.md`. Fast-Track (QUESTION/SURVEY-INTEL/SIMPLE CODE) não loga aqui. Revisão periódica: `/benchmark` ou pedido explícito do usuário ("o roteamento está acertando?").

## Como ler os dados

- **"Roteamento correto? = Não" repetido para o mesmo padrão de pedido** → a linha da Domain Overlap Detection ou do Agent Selection Matrix (`intelligent-routing/SKILL.md`) precisa de ajuste — o sinal aponta exatamente qual keyword/domínio está sendo mal mapeado.
- **"Precisou de orchestrator depois?" = Sim frequente para um domínio "solo"** → esse domínio na verdade é multi-domínio na prática e deveria entrar na tabela de Domain Overlap Detection.
- **Estado de evidência majoritariamente "Declarada"** → puxe algumas linhas antigas e reclassifique com o resultado real antes de confiar nas leituras acima (mesma ressalva de `gate-telemetry.md`).

## Estado de evidência (o que sustenta cada linha)

| Estado | Significa |
|---|---|
| **Declarada** | Só o agente escolhido foi registrado; ninguém checou depois se foi o certo. Estado inicial de toda linha nova. |
| **Confirmada** | Um resultado posterior mostrou que o agente escolhido resolveu a tarefa sem precisar trocar. |
| **Contradita** | Precisou trocar de agente, escalar para `orchestrator`, ou o usuário corrigiu a escolha — este é o sinal mais valioso: aponta onde o roteamento errou. |

Sem observação posterior concreta, a linha permanece **Declarada** indefinidamente.

## Formato de entrada (uma linha por roteamento)

| Data | Pedido (slug curto) | Agente(s) escolhido(s) | Precisou de orchestrator depois? | Roteamento correto? | Estado de evidência |
|------|---------------------|--------------------------|-----------------------------------|----------------------|----------------------|

<!-- Entradas deste projeto começam abaixo. Este arquivo nasce vazio em cada instalação nova do DevBureau. "Precisou de orchestrator depois?": a escolha solo se mostrou insuficiente e a tarefa escalou para multi-agente. "Roteamento correto?": Sim/Não/N/A (ainda não observado). "Estado de evidência": Declarada/Confirmada/Contradita — ver seção acima; atualizar a mesma linha quando houver observação posterior, sem duplicar. -->
