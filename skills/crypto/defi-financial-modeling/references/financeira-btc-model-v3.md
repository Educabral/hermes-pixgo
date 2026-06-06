# Financeira BTC — Model V3 Session Reference

## Date: June 3, 2026
## BTC Price at Simulation: US$ 62,774

## The Problem (Model V1/V2)

User's original idea: neighbors give him money → he buys BTC → deposits on Aave → borrows at LTV 70% → pays neighbors' bills → keeps the BTC.

**Why it fails:**
- Borrowing at 70% LTV means getting only 70% of the value back
- Paying 100% of the bill with 70% of the collateral value = shortfall
- Debt grows faster than collateral each month
- After 12 months with 5 clients: Health Factor 0.92x (below liquidation threshold at 1.0x)
- BTC -20% crash → full liquidation

## The Solution (Model V3)

### Core Innovation: Service Fee

Instead of borrowing the ENTIRE bill amount, the model charges a 15% service fee:

- Client bill: R$ 600/month
- Client pays: R$ 690/month (R$ 600 + 15% fee)
- Cost to cover: R$ 600
- **Profit: R$ 90/month/client**

### Two-Phase Strategy

**Phase 1 (Months 1-6): Buy & Hold (zero debt)**
- Use ONLY the service fee profit to buy BTC
- No collateralization, no Aave, no borrowing
- BTC accumulates steadily with zero liquidation risk
- Building a natural BTC reserve

**Phase 2 (Months 7-12): Conservative Leverage**
- Collateralize only 20-30% of accumulated BTC
- LTV: 30% (not the Aave max of 75%)
- Target Health Factor: > 2.5x
- Borrow to buy MORE BTC, not to pay operational costs
- Keep 30-40% of initial capital in USDC as emergency reserve

### Results: 5 Clients, 12 Months

| Metric | Value |
|--------|-------|
| Monthly service fee profit | R$ 450 |
| BTC accumulated (Phase 1) | ~0.0226 BTC |
| BTC accumulated (Phase 2) | ~0.0370 BTC |
| Total debt on Aave | US$ 426 |
| Equity | US$ 1,895 (~R$ 10,800) |
| Initial capital | R$ 9,000 (3 months advance) |
| Return (BTC flat) | +20% |
| Return (BTC +50%) | +206% |
| BTC -40% stress test | ✅ Health Factor 2.78x |
| BTC -70% stress test | Liquidation threshold reached |

### Key Insight

The naive model borrows to pay bills (debt grows). The correct model uses the service fee surplus to buy BTC (assets grow). The difference between "leveraging to pay expenses" and "leveraging to buy more assets" is the difference between liquidation and wealth building.
