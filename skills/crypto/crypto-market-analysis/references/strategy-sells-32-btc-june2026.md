# Strategy Sells 32 BTC — June 2026 Case Study

## Event

**Date:** June 1, 2026 (filing date for sales between May 26-31, 2026)
**Source:** SEC Form 8-K (MicroStrategy/Strategy filing CIK 0001050446)
**Article:** https://www.coindesk.com/markets/2026/06/01/strategy-sold-32-btc-for-usd2-5-million-in-late-may-filing-shows

## The Facts

| Data Point | Value |
|------------|-------|
| BTC sold | 32 BTC |
| Period | May 26-31, 2026 (6 consecutive days) |
| Average price | US$ 77,135/BTC |
| Total proceeds | ~US$ 2.5 million |
| Official reason | Fund distributions on preferred stock (STRC) |
| BTC held after sale | 843,706 BTC |
| Average cost basis | US$ 75,699/BTC |
| BTC price on filing day | ~US$ 71,900-72,000 (-2.5%) |
| First BTC sale ever? | Yes — first disclosed Bitcoin disposal |

## The Preferred Stock (STRC) Detail

- **Face value:** ~US$ 15 billion in preferred stock
- **Dividend rate:** 11.5% annually (held for 4th consecutive month per separate filing)
- **Annual obligation:** US$ 1.725 billion
- **Monthly obligation:** US$ 143.75 million
- **BTC needed to cover 1 month at $77k/BTC:** ~1,867 BTC
- **BTC needed to cover 1 year at $77k/BTC:** ~22,400 BTC
- **BTC sold this time:** 32 BTC (covers ~0.5 days of dividend)

## Simultaneous Moves in Same Filing

- Raised **US$ 128.3 million** via ATM (at-the-market common stock program)
- Allocated portion to increase cash reserves from US$ 871M to US$ 900M
- Had recently deployed US$ 1.5B to repurchase 2029 convertible notes at discount
- Total cash reserves: ~US$ 900M

## Narrative Impact

This was Strategy's FIRST EVER disclosed Bitcoin sale. The company built its entire brand on "never sell, hodl forever." Even 32 BTC (0.0038% of holdings) crosses that line:

- **The "diminutivo tranquilizador":** "Só 32 BTC", "apenas 2M" — normalizes the first sale
- **The "distinção falsa":** "Operacional vs estratégico" — same action with different label
- **The precedent:** First sale normalizes the second. In 6 months, selling 5,000 BTC/quarter could become "routine"

## The Math That Doesn't Close

Strategy has ~US$ 21.7B in total liabilities (convertible notes ~US$ 6.7B + preferred stock ~US$ 15B):
- Bitcoin generates ZERO yield
- Software business revenue is negligible vs balance sheet
- Funding model: issue stock/debt → buy BTC → BTC rises → issue more stock/debt
- At 11.5% dividend cost, BTC needs to appreciate >11.5%/yr NET of drawdowns to sustain
- If BTC goes sideways for 12-18 months, Strategy becomes a forced liquidator

## Market Reaction

- BTC dropped ~2.5% on the day (from ~73,700 to ~71,900)
- ~US$ 90M in BTC-tracked futures liquidated
- The drop reflects narrative discovery (biggest corporate holder turns seller), not the 32 BTC itself

## PutinHO Post Structure Used

1. **Open with fact** — "A Strategy vendeu Bitcoin pela primeira vez na história. 32 BTC."
2. **State the math** — dividend cost vs sale proceeds
3. **Debunk the narrative** — "32 BTC não é nada" but precedent is everything
4. **Project forward** — how many BTC/yr needed to sustain
5. **End with a punch** — "A conta do Saylor não é sua conta. Auto-custódia."

## Tools & Sources Used

- **browser_navigate** to CoinDesk homepage → found the article in "Latest Crypto News" feed
- **browser_console (JS eval)** to extract the exact article URL from HTML
- **delegate_task** with [browser] tools for Deep Researcher
- **delegate_task** with [terminal] tools for Skeptic Editor
- **SEC.gov** blocked automated access — required fallback to journalist article
- **Scripts:** post_to_x.py at ~/.hermes/scripts/post_to_x.py (MSYS path: /c/Users/PC/.hermes/scripts/post_to_x.py)
