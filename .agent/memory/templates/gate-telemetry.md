# Gate Telemetry — DevBureau

> Registro de cada disparo do Socratic Gate para medir se ele melhora o entendimento de verdade, em vez de assumir que sim. Uma linha por disparo, preenchida pelo agente no fim da interação (ver `.agent/skills/brainstorming/SKILL.md`, seção "Telemetria do Gate"). Revisão periódica: `/benchmark` ou pedido explícito do usuário ("o gate está funcionando?").

## Como ler os dados

- **"Mudou o plano? = Sim" frequente** → o Gate está pagando o custo: as respostas do usuário alteraram a implementação.
- **"Mudou o plano? = Não" repetido para o mesmo tópico** → pergunta candidata a supressão em `question-preferences.md` (proponha ao usuário, não suprima sozinho).
- **"Suposição correta? = Não" repetido** → o agente está inferindo demais nesse tópico; mover de "assumir" para "perguntar".
- **Estado de evidência majoritariamente "Declarada"** → a telemetria está medindo o que o agente disse fazer, não o que de fato aconteceu; puxe algumas linhas antigas e reclassifique com o resultado real antes de confiar nas leituras acima.

## Estado de evidência (o que sustenta cada linha)

Uma linha registrada logo após o disparo só prova que a pergunta/suposição existiu, não que a resposta estava certa nem que o comportamento planejado de fato ocorreu. Classifique cada linha em um dos três estados, e reclassifique quando houver dado novo:

| Estado | Significa |
|---|---|
| **Declarada** | Só a resposta do usuário ou a suposição do agente foi registrada; ninguém checou depois se bateu com o resultado real. Estado inicial de toda linha nova. |
| **Confirmada** | Um resultado posterior (a mesma sessão, uma sessão seguinte, ou revisão do usuário) comprovou que a resposta/suposição estava certa. |
| **Contradita** | Um resultado posterior mostrou que a resposta/suposição estava errada — este é o sinal mais valioso da tabela: aponta exatamente onde o Gate (ou a inferência do agente) falhou. |

Não invente uma reclassificação: sem observação posterior concreta, a linha permanece **Declarada** indefinidamente. Isso espelha a disciplina de "configuração não é uso observado" — uma resposta registrada não é, por si só, prova de que funcionou.

## Formato de entrada (uma linha por disparo)

| Data | Pedido (slug curto) | Dimensões que faltavam | Perguntas (n) | Mudou o plano? | Suposição declarada correta? | Estado de evidência |
|------|--------------------|------------------------|---------------|----------------|------------------------------|----------------------|

<!-- Entradas deste projeto começam abaixo. Este arquivo nasce vazio em cada instalação nova do DevBureau — não herda a telemetria do próprio kit. "Mudou o plano?": a resposta do usuário alterou escopo/abordagem vs. o que seria feito sem perguntar. "Suposição correta?": preencher só quando o Gate prosseguiu com suposição declarada em vez de perguntar; N/A caso contrário. "Estado de evidência": Declarada/Confirmada/Contradita — ver seção acima; comece em Declarada e atualize a mesma linha quando houver observação posterior, sem duplicar a linha. -->
