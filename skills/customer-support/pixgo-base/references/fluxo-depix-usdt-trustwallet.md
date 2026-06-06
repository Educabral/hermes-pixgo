# DEPIX → USDT na Trust Wallet — Sessão 02/06/2026

## Contexto
Cliente (lojista) quer sair da PixGo e receber USDT na Trust Wallet.
Usa a PixGo Wallet (wallet.pixgo.org).

## Fluxo Completo Aprovado

1. **Recebe DEPIX** na PixGo Wallet em D+1 corrido
2. **Swap interno 1:** DEPIX → L-BTC (fração pequena, ~R$ 50)
   - L-BTC é o gás da Liquid Network, necessário para pagar taxas
   - A PixGo Wallet tem swap interno nativo — não precisa de terceiros
3. **Swap interno 2:** DEPIX → USDT (Polygon) — o restante
4. **Envia USDT** da PixGo Wallet → Trust Wallet
   - Rede: **Polygon** (NÃO ERC-20!)
5. Trust Wallet precisa de **MATIC** na Polygon para taxas futuras

## Pontos Críticos

- **L-BTC é o gargalo.** Ninguém sabe disso. Explicar primeiro com analogia (ETH na Ethereum, MATIC na Polygon)
- **Trust Wallet não suporta Liquid Network.** A ponte via Polygon é obrigatória
- **Rede errada = perda de fundos.** Sempre reforçar: Polygon, não ERC-20
- **PixGo Wallet faz tudo.** Swap interno já resolve DEPIX→L-BTC e DEPIX→USDT

## Exemplo de Explicação

"Primeiro, é importante entender que a Liquid Network exige uma pequena quantidade de L-BTC para pagar taxas — assim como a Ethereum exige ETH ou a Polygon exige MATIC. A própria PixGo Wallet permite fazer esse swap internamente: você converte uma parte pequena dos seus DEPIX em L-BTC para ter o gás. Depois, converte o restante em USDT na rede Polygon. Com o USDT em Polygon, envia direto para o endereço da Trust Wallet. Lembre de manter uma fração de MATIC na Trust Wallet para taxas futuras."
