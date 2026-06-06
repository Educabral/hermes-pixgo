# Fluxo de Anonimato Financeiro: PIX → BTC (2026)

Pipeline completo saindo do real (PIX) e chegando ao Bitcoin anônimo na OneKey,
usando PixGo como porta de entrada, Houdini como embaralhador e Monero como
quebra de rastro definitiva.

## O Fluxo (7 estágios)

```
PIX (cliente) → PixGo → DEPIX (Liquid Network)
→ USDT (Polygon)
→ Houdini Swap (embaralha rastro entre EVM chains)
→ ETH (Arbitrum/Optimism)
→ Monero via Rubic/Cake Wallet (some o rastro de vez)
→ BTC via Cake Swap (cai na OneKey Wallet)
```

## Detalhamento por Estágio

### Estágio 1 — PIX → DEPIX (Liquid)
- Cliente paga na loja PixGo via PIX
- D+1 corrido (inclui fins de semana), valor vira DEPIX (stablecoin BRL na Liquid Network)
- DEPIX não aparece em extrato bancário, nem em Imposto de Renda, nem em consulta BC
- Saiu do sistema bancário brasileiro — primeira camada de anonimato

### Estágio 2 — DEPIX → USDT (Polygon)
- Dentro da PixGo Wallet, swap DEPIX → USDT
- Rede Polygon (taxas de centavos, liquidez instantânea)
- Dinheiro agora é dólar digital na blockchain, sem CPF vinculado

### Estágio 3 — Houdini Swap (embaralhamento na EVM)
- Manda USDT da Polygon pro Houdini Swap
- Houdini roteia por múltiplas pools, exchanges descentralizadas e contratos atômicos
- Quebra a ligação entre token de entrada e de saída
- Sai ETH limpo na Arbitrum ou Optimism
- Nenhum explorador de blockchain consegue ligar o USDT que entrou com o ETH que saiu
- **Por que Houdini antes do Monero:** adiciona uma camada de ofuscação ANTES de entrar
  na camada de privacidade definitiva. Duas camadas independentes = rastro duplamente morto.

### Estágio 4 — ETH → Monero (XMR)
- Com ETH limpo na Rabby/MetaMask, vai pra Rubic Exchange
- Swap: ETH → XMR, cai na Cake Wallet
- Monero é a única cripto verdadeiramente anônima:
  - Ring signatures (assinaturas em anel) — não dá pra saber quem assinou
  - Stealth addresses — cada transação gera endereço único e descartável
  - Confidential transactions — valores são ocultos
- O rastro MORREU aqui. Nenhum blockchain explorer funciona no Monero.
- Se até o FBI já usou Monero, é porque funciona.

### Estágio 5 — Monero → BTC (OneKey)
- Dentro da Cake Wallet, swap embutido XMR → BTC
- BTC cai limpo, sem histórico, na OneKey Wallet
- Zero KYC, zero exchange, zero selfie, zero vínculo com o PIX original
- A trilha que começou no PIX do cliente não tem mais nenhuma ligação com este BTC

## Regras Ninja (CRÍTICO)

1. **Gera endereço BTC novo pra cada transação** — nunca reutiliza
2. **Fraciona valores acima de R$ 5.000** — não chama atenção
3. **Troca XMR entre carteiras antes de gastar** — mais uma camada
4. **Nunca conta o caminho completo pra ninguém** — nem pra parceira

## Por que esta rota é superior às alternativas

| Característica | PixGo → Monero | Exchange KYC → BTC | P2P direto |
|---|---|---|---|
| Anonimato real | ✅ (3 camadas) | ❌ (entregou CPF) | ⚠️ (parcial) |
| Liquidez | ✅ Imediata | ✅ | ❌ (demora) |
| Aceita PIX | ✅ Sim | ✅ Sim | ⚠️ Depende |
| Rastro forense | ❌ Nenhum | ✅ Total | ⚠️ Parcial |
| Autocustódia | ✅ Sim | ❌ Exchange guarda | ✅ Sim |

## Referência para Posts (PutinHO Style)

Ao criar conteúdo sobre este fluxo:
- **Não usar** numeração (1/7, 2/8) — o usuário odeia
- **Não usar** separadores `---`
- Tom agressivo, críticas ao sistema financeiro, linguagem de "manual de sobrevivência"
- Cada estrofe é auto-contida (~280 chars) pois o X sem verificado corta em ~280
- Terminar com murro, não lição de moral
