# Novidades do DevBureau

[English](RELEASE_NOTES.md) · **Português**

O que muda para você a cada versão, em linguagem simples. O `npx devbureau update` mostra estas notas desde a versão que você tinha instalada.

---

### [3.42.0] - 2026-09-24
- **Proteções no Mac e no Linux:** as verificações automáticas agora funcionam nos três sistemas. No Mac, antes, elas ficavam desligadas sem nenhum aviso. A instalação também passou a funcionar no Windows com a instalação padrão do Python.
- **Guia do usuário renovado:** instalação atualizada, uma seção sobre o que o kit protege sozinho e outra sobre como atualizar ou remover. O guia agora vem junto no pacote e está linkado no topo do README.
- **Revisões de código mais rigorosas:** cada problema apontado vem com o cenário concreto em que ele falha. Se não houver cenário, vira pergunta, não alarme.
- **O agente não desfaz o que não é dele:** mudanças e arquivos que você (ou outra sessão) está fazendo nunca são revertidos ou apagados. Depois de instalar dependências, ele confere se algo mudou sem querer.
- **Menos alarme falso em segurança:** as revisões ignoram casos comprovadamente inofensivos, mas continuam cobrando o que importa para quem vende SaaS, como limite de tentativas em login e pagamento.
- **Sites menos parecidos entre si:** quando você não define estilo, cores ou layout, o especialista de design sorteia entre opções curadas em vez de repetir sempre a mesma escolha. Textos que você entrega entram exatamente como você escreveu.
- **Pacote mais limpo:** arquivos internos de manutenção do kit deixaram de ir junto na instalação. Se a sua versão anterior os trouxe para o projeto, esta atualização os remove, desde que você não os tenha alterado.

### [3.41.0] - 2026-09-10
- **Novas travas automáticas:** o kit bloqueia o agente se ele tentar gravar uma senha ou chave de acesso num arquivo, apagar ou desativar um teste para ele "passar", ou editar direto a versão principal de um projeto compartilhado.
- **Regras não se perdem em conversas longas:** quando a ferramenta resume o histórico, o kit reinsere as regras essenciais.
- **Becos sem saída ficam registrados:** uma abordagem que falhou é anotada para não ser tentada de novo na semana seguinte.
- **Correções importantes:** a sincronização automática no início de cada sessão voltou a funcionar, e a checagem de segurança passou a barrar de verdade os problemas críticos, que antes eram só relatados.

### [3.40.1] - 2026-08-17
- **Memória própria por projeto:** cada projeto novo começa com a memória vazia. Antes, ele herdava as anotações internas do próprio kit.

### [3.40.0] - 2026-08-17
- **Busca na memória por assunto:** o agente encontra lições e erros já registrados antes de repeti-los.
- **Avisos de qualidade:** código alterado sem teste correspondente e documentação que aponta para arquivos que não existem mais passam a ser sinalizados.
- **Risco medido, não adivinhado:** antes de uma mudança sensível, o kit mede quantas partes do projeto dependem daquele arquivo.
- **Dados brasileiros protegidos:** a checagem de dados pessoais reconhece CNPJ, RG e CEP, além de CPF e telefone.

### [3.39.0] - 2026-08-13
- **Planos que evitam retrabalho:** tarefas são divididas por funcionalidade completa e testável, nunca "todo o banco primeiro, depois toda a tela".
- **Dois olhares nas mudanças de risco:** uma revisão confere se o que foi feito bate com o pedido, e outra, independente, confere a qualidade do código.
- **Veja antes de atualizar:** `npx devbureau update --dry-run` mostra o que mudaria, sem alterar nada.

### [3.38.0] - 2026-08-11
- **Respostas mais diretas:** perguntas simples e correções pequenas são atendidas na hora, sem rodada de perguntas.
- **Regras mais enxutas:** o conjunto carregado em toda conversa ficou menor, o que reduz custo sem afrouxar as travas de segurança.

### [3.36.1] - 2026-08-09
- **Segunda opinião em planos de risco:** um revisor independente lê o plano antes da execução.
- **Mapa de impacto:** o kit mostra quais arquivos seriam afetados por uma mudança.

### [3.36.0] - 2026-07-13
- **Plano aprovado roda sem interrupções:** depois que você aprova, o agente executa sem pedir permissão a cada passo, mas continua perguntando antes de publicar ou apagar qualquer coisa.
- **Design com especialista obrigatório:** o agente não mexe no visual sem ler antes as regras do especialista de design.
- **Efeitos de passar o mouse:** nova coleção de efeitos para botões, cartões e links.
