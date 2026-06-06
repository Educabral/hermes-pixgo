---
name: comet-browser
description: Regras obrigatórias de navegação web e automação humana usando o navegador Comet
---

# Regras de Automação e Navegador (COMET)

## 1. Navegador Oficial
- O ÚNICO navegador que você está autorizado a usar para qualquer tarefa web é o **COMET**. 
- Se você for abrir links via linha de comando ou usar ferramentas de visão/automação, certifique-se de direcionar o comando para o Comet (por exemplo, `start comet "url"` no Windows, caso esteja registrado, ou use o caminho do executável do Comet se necessário).

## 2. Automação Humanizada (Pare de ser robótico)
O usuário relatou que você "engasga" muito ao fechar abas, abrir links e digitar textos, parecendo um robô desajeitado. A partir de agora, mude seu comportamento:
- **Digitação:** Ao preencher formulários ou escrever textos, não use ferramentas instáveis que erram os campos. Prefira injetar o texto de forma limpa via DOM (JavaScript) se estiver no navegador, ou use a área de transferência (`clipboard`) + atalho de colar (`Ctrl+V`) se estiver usando automação de teclado.
- **Abas e Fechamentos:** Em vez de tentar "clicar" no Xzinho minúsculo da aba (o que costuma falhar), use atalhos de teclado (ex: `Ctrl+W` ou `Ctrl+F4` para fechar a aba atual, `Ctrl+T` para nova aba) que são 100% precisos e mais humanos.
- **Precisão:** Antes de clicar, tenha CERTEZA das coordenadas. Evite "adivinhar" onde estão os botões. Use navegação por `Tab` e `Enter` quando apropriado, pois humanos usam muito o teclado para navegar mais rápido.

Lembre-se: O objetivo é fluidez. Se uma ação via mouse estiver falhando (engasgando), mude imediatamente para atalhos de teclado.

## 3. Gestão Inteligente de Abas e Recuperação de Erros
- **NUNCA crie um loop de abas:** O usuário relatou que, ao cometer um erro e receber a ordem de "fechar a aba", você acaba abrindo *outra* aba por engano, gerando um efeito cascata. Isso é inaceitável.
- **Diferencie ABRIR de FECHAR:** Quando o usuário pedir para "fechar", a ÚNICA ação permitida é pressionar o atalho `Ctrl+W` para eliminar a aba defeituosa. Sob hipótese alguma tente clicar em botões de nova aba (`+`) ou executar comandos de inicialização quando a ordem for para fechar.
- **Seja analítico:** Se você errar uma tarefa, pare. Feche a aba com `Ctrl+W`, respire (metaforicamente) e tente uma abordagem diferente na próxima aba. Não repita a mesma ação falha sucessivamente.
