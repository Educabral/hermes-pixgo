---
name: defi-financial-modeling
description: Model DeFi strategies involving BTC collateralization (Aave), multi-phase accumulation, LTV risk analysis, and simulated P&L across BTC price scenarios. Designed for Brazilian crypto users building real-world financial products.
tags:
  - defi
  - aave
  - btc
  - financial-modeling
  - risk-analysis
  - collateralization
  - simulation
platforms: [windows]
related_skills:
  - crypto-market-analysis
  - windows-automation
---

# DeFi Financial Modeling

## Overview

Model financial strategies that combine:
- Real-world cash flow (receiving payments from clients/vizinhos)
- BTC accumulation (buy & hold)
- DeFi lending protocols (Aave) for collateralized loans
- Risk analysis across BTC price scenarios

The user is Edu (Brazilian crypto OG, @Cabral_Cripto) building a "Financeira BTC" — collecting payments from neighbors to pay their utility bills, investing the service fee profit in BTC, and optionally leveraging via Aave.

## When to Use

- "Quero criar uma estratégia de..." (strategic financial planning)
- User proposes a multi-step DeFi workflow with real-world cash flows
- Modeling BTC collateralization on Aave with health factor analysis
- Any scenario involving: incoming cash → BTC buy → Aave deposit → borrow → repay

## Core Concepts to Model

### The Double-Leverage Trap

The naive strategy sounds good but fails numerically:

1. User receives R$ X from client
2. Buys BTC with all of it
3. Deposits BTC on Aave as collateral
4. Borrows USDC at LTV% to pay the client's bill
5. Keeps the BTC as "savings"

**Why it breaks:** Borrowing at LTV% means you only get LTV% of the deposit value. If you need 100% of the original amount to pay the bill, you're short every cycle. The debt grows faster than the collateral → health factor drops monthly → first BTC dip liquidates everything.

**Simulation result (naive model, 5 clients, LTV 70%):**
- Month 12: Health Factor 0.92x (below liquidation threshold)
- BTC -20%: LIQUIDAÇÃO
- Return after 12 months: -23%

### The Correct Model: Service Fee + Conservative LTV

**Phase 1 — Cash Flow (months 1-6, buy & hold only):**
- Charge 15% service fee on top of the bill value
- Example: bill=R$600 → client pays R$690 (R$90 is YOUR profit)
- Use the PROFIT (not the principal) to buy BTC
- Do NOT collateralize or borrow during this phase
- Build a BTC reserve with zero debt

**Phase 2 — Conservative Leverage (months 7+:**
- Collateralize no more than 20-30% of accumulated BTC
- Use LTV of 30% or less (NOT the Aave maximum of 75-80%)
- Target Health Factor > 2.5x (liquidation only if BTC drops 70%+)
- Borrow just to buy MORE BTC, not to pay operational costs

**Phase 3 — Scaling:**
- Reinvest service fee profits into BTC continuously
- Use the growing BTC base for periodic conservative borrows
- Maintain a USDC reserve (30-40% of capital) as emergency buffer

## Simulation Parameters

Default simulation assumptions for this user's context:

| Parameter | Value |
|-----------|-------|
| BTC Price | US$ ~62,774 (live from CoinGecko) |
| BRL/USD | 5.70 |
| Swap fee (buy BTC) | 0.5% |
| Aave LTV (safe) | 30% (not max) |
| Aave borrow APY | 6% |
| Aave supply APY (USDC) | 1.5% |
| Liquidation threshold (Aave BTC) | 85% |
| Service fee rate | 15% |
| Average bill per client | R$ 600/month |

## Simulation Script Pattern

```python
# Core simulation loop:
btc_atual = capital_inicial_btc
divida_atual = 0  # Phase 1: no debt

for mes in range(1, 13):
    entrada_usd = receita_mensal_usd
    # Buy BTC with profit only
    btc_novo = (entrada_usd * (1 - taxa_swap)) / btc_price
    btc_atual += btc_novo
    
    # Phase 2: borrow conservatively
    if mes > 6:
        novo_credito = btc_novo * btc_price * ltv_seguro
        divida_atual += valor_conta_usd  # only what's needed
        
    # Health factor check
    health = (btc_atual * btc_price * 0.85) / divida_atual if divida_atual > 0 else float('inf')
```

## Stress Test Scenarios

Always run these after modeling:

1. **BTC -20%:** Target Health Factor > 1.0x (minimum survival)
2. **BTC -40%:** Target Health Factor > 1.0x (crash survival)
3. **BTC flat (0%):** Is the model P&L positive? (business sustainability)
4. **BTC +50%:** What's the upside? (investment thesis)
5. **Worst case:** 3 months of client defaults (cash flow survival)

## Pitfalls

- ❌ **Don't use Aave max LTV (70-80%).** The liquidation health margin is razor-thin. One flash crash liquidates everything. Max safe LTV is 30% for a business holding period > 6 months.
- ❌ **Don't borrow to pay operational costs.** Borrowing to pay bills means debt grows faster than collateral. Borrow ONLY to buy more assets.
- ❌ **Don't model without a reserve.** Phase 1 MUST include a USDC/stablecoin reserve (30-40% of capital) to handle emergencies and avoid forced liquidation.
- ❌ **Don't assume BTC only goes up.** Model flat and down scenarios. If the business loses money at flat BTC, the business model is broken.
- ❌ **Don't forget swap fees.** Every BTC buy on an exchange costs 0.3-1.0% in fees. On R$ 3,000/month this is R$ 15-30/month lost.
- ❌ **Don't model clients as reliable payers.** Include a 5-10% default rate. If one neighbor doesn't pay, can you still cover the bill?

## Verification Checklist

- [ ] Model is cash-flow positive WITHOUT BTC appreciation
- [ ] Health Factor stays above 2.0x at all times
- [ ] Stress test passes at BTC -40%
- [ ] Reserve covers at least 2 months of operating costs
- [ ] Service fee covers the gap between borrowed LTV and full bill cost
- [ ] Client default scenario doesn't cascade into liquidation

## Related

See `crypto-market-analysis` for market context (BTC price, trend analysis).
See `windows-automation` for running Python simulations on this Windows machine.
