---
name: pixgo-med-responses
description: "Respostas profissionais para contestações de MED (Mecanismo Especial de Devolução) da PixGo. Regras de tom, estrutura, e templates para cada cenário."
version: 1.1.0
author: edu
tags: [pixgo, med, chargeback, customer-support, portuguese]
---

# PixGo MED Responses

## Context

Edu (user) is Account Manager at PixGo, handling MED chargeback disputes for merchants. Responses are sent via email from `suporte@pixgo.me` (Hostinger) or `segurancabral@gmail.com`. He prefers the agent to write the full email body ready-to-copy, no extra explanation.

## Critical Rules

- **Assinar sempre**: `Atenciosamente,` + blank line + `Eduardo Cabral` + `Gerente de Contas`
- **Sem emojis, sem markdown, sem negrito/itálico** — email puro, texto corrido
- **Português formal mas direto**, sem rodeios
- **Variar vocabulário entre respostas consecutivas** — não repetir a mesma abertura/fechamento/explicação
- **Nunca pedir comprovantes ao lojista** (não cobrar nota fiscal, prints, etc.)
- **Anexos já recebidos** → resposta confirmando recebimento e encaminhamento
- **Sem anexos** → avisar que precisa de documentação, mas sem exigir
- **Cliente retirou MED mas valor não voltou** → explicar que mesmo cancelado passa por investigação formal da adquirente/banco, processo independente, O MED segue um fluxo regulado pelo Banco Central e a confirmação oficial precisa ser processada internamente
- **Cliente desistiu do produto** → orientar que reembolso por vontade do cliente é feito diretamente entre as partes, MED segue com documentação
- **Número errado / sem contato, SEM anexos** → explicar que o MED precisa passar por investigação dos órgãos responsáveis (adquirente e banco emissor), e sem documentação a chance de reverter é reduzida
- **Número errado / sem contato, COM anexos** → confirmar recebimento e explicar que a análise depende da investigação dos órgãos responsáveis
- **Formato de entrega**: fornecer APENAS o texto do email, sem explicação extra antes/depois — o usuário copia e cola direto. Apenas a resposta nua.

## Standard Explanations to Include

### O que é o MED
O MED (Mecanismo Especial de Devolução) é um recurso instituído pelo Banco Central do Brasil que permite ao portador do cartão contestar uma transação junto à sua instituição financeira. Quando o MED é aberto, ele passa por uma investigação conduzida pelos órgãos responsáveis — adquirente e banco emissor — que avaliam as evidências apresentadas por ambas as partes antes de decidir.

### Papel da PixGo
A PixGo atua como interface tecnológica entre o estabelecimento e as instituições financeiras — realizamos o envio da documentação, mas a análise e decisão final sobre o MED são de responsabilidade exclusiva da adquirente ou banco envolvido. A investigação independe de acordos entre as partes.

### Cancelamento/Desistência
Mesmo quando o cliente retira a contestação junto ao banco emissor, o processo ainda precisa passar pela investigação e validação formal dos órgãos responsáveis (adquirente e banco emissor). O MED segue um fluxo regulado pelo Banco Central e a confirmação oficial do cancelamento precisa ser processada internamente antes do valor ser liberado e creditado de volta. Essa investigação independe de acordos entre as partes.

### Prazo
O prazo estimado de retorno é de 15 a 20 dias úteis, podendo variar conforme a instituição financeira envolvida.

## Templates

### Template A: Anexos recebidos, confirmar recebimento
Prezado(a),

Os documentos do pedido [ID] foram recebidos e registrados para contestação do MED.

O MED (Mecanismo Especial de Devolução) é um recurso instituído pelo Banco Central do Brasil que permite ao portador do cartão contestar uma transação junto à sua instituição financeira.

A PixGo atua como interface tecnológica entre o estabelecimento e as instituições financeiras — realizamos o envio da documentação, mas a análise e decisão final sobre o MED são de responsabilidade exclusiva da adquirente ou banco envolvido.

O prazo estimado de retorno é de 15 a 20 dias úteis.

Atenciosamente,
Eduardo Cabral
Gerente de Contas

### Template B: Cliente retirou, valor não voltou
Prezado(a),

Recebemos sua mensagem referente ao MED da transação [ID].

Entendemos a situação. Mesmo quando o cliente retira a contestação junto ao banco emissor, o processo ainda precisa passar pela investigação e validação dos órgãos responsáveis — adquirente e instituição financeira. O MED segue um fluxo regulado pelo Banco Central, e a confirmação oficial do cancelamento precisa ser processada internamente antes do valor ser liberado.

A PixGo atua como interface tecnológica entre o estabelecimento e as instituições financeiras. O trâmite de retorno depende do processamento interno de cada adquirente.

O prazo médio é de 15 a 20 dias úteis. Caso ultrapasse sem retorno, podemos abrir uma investigação complementar.

Atenciosamente,
Eduardo Cabral
Gerente de Contas

### Template C: Cliente não quis produto / desistência
Prezado(a),

Recebemos sua solicitação referente ao MED da transação [ID].

Para este caso, é importante apresentar documentação que comprove que o cliente não quis mais o produto, como prints da conversa.

Vale esclarecer que o reembolso por vontade do cliente deve ser tratado diretamente entre o estabelecimento e o comprador. Caso optem por realizar o reembolso por fora, nos informe para registrarmos que o valor já foi devolvido.

Aguardamos seu retorno com os documentos para darmos prosseguimento.

Atenciosamente,
Eduardo Cabral
Gerente de Contas

### Template D: Número errado / sem contato, SEM anexos
Prezado(a),

Recebemos sua mensagem referente ao MED da transação [ID].

Informamos que o MED (Mecanismo Especial de Devolução) é um instrumento do Banco Central que, uma vez aberto, passa por uma investigação conduzida pelos órgãos responsáveis — adquirente e banco emissor — que avaliam as evidências antes de decidir pela procedência ou não da contestação. Esse processo de investigação independe de acordos entre as partes.

Para darmos andamento, é necessário o envio de documentos que comprovem a tentativa de contato com o cliente, como prints de WhatsApp ou registros de que o número informado estava incorreto. Sem documentação, a possibilidade de reverter o MED é reduzida.

O prazo médio de retorno da análise é de 15 a 20 dias úteis.

Atenciosamente,
Eduardo Cabral
Gerente de Contas

### Template E: Número errado / sem contato, COM anexos
Prezado(a),

Recebemos os documentos referentes ao MED da transação [ID].

Os materiais foram registrados e seguem para análise. Esclarecemos que o MED (Mecanismo Especial de Devolução) é regulado pelo Banco Central e, uma vez aberto, passa por investigação dos órgãos responsáveis — adquirente e banco emissor — que avaliam as evidências de ambas as partes. Essa investigação independe de acordos entre o estabelecimento e o cliente.

A PixGo atua como interface tecnológica entre o estabelecimento e as instituições financeiras. A análise e decisão final cabem exclusivamente à adquirente.

O prazo estimado de retorno é de 15 a 20 dias úteis.

Atenciosamente,
Eduardo Cabral
Gerente de Contas

## References
- `references/med-vocabulary.md` — variants pool: rotate through different phrasings for abertura, explicação do MED, papel da PixGo, prazo, cancelamento, e fechamento. Prevents repetitive-sounding responses.
