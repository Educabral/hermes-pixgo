# Crypto Technical Analysis — Session Reference

## BTC/USDT 4H — Example Analysis (May 2026)

From session on 2026-05-23:

**Preço:** $75,903
**Tendência:** BAIXA (SMA20 $76,783 < SMA50 $77,314)
**RSI:** 38.2 (neutro, tendendo baixo)
**MACD:** BAIXA (hist -199.6)
**Bollinger:** Dentro das bandas (sem extremo)

**Estrutura:** Death cross no 4h. Queda de $77,780 → $74,290 com rejeição. Recuperação fraca com velas de corpo pequeno ($16-$29). Volume caindo no bounce.

**Cenário predominante:** Bearish (65%). Se perder $75,200 → $74,000 → $72k.

## ETH/USDT 4H — Example Analysis (May 2026)

**Preço:** $2,076
**Tendência:** BAIXA (SMA20 $2,106 < SMA50 $2,136)
**RSI:** 40.9 (neutro)
**MACD:** BAIXA (hist -6.4)
**Bollinger:** Dentro

**ETH caindo mais que BTC.** Queda de -14.3% da máxima vs BTC -8%. Bounce de $2,009 fraco. ETH/BTC pair caindo (dominância do Bitcoin sugando liquidez).

## Quick Reference: Indicator Settings

| Indicator | Period | Formula |
|-----------|--------|---------|
| SMA | 20, 50 | Simple average of closes |
| EMA | 12, 26 | 2/(n+1) × (price - prev EMA) + prev EMA |
| MACD | 12, 26, 9 | EMA12 - EMA26, signal = EMA9 of MACD line |
| RSI | 14 | 100 - 100/(1 + avg_gain/avg_loss), Wilder's smoothing |
| Bollinger | 20, 2 | SMA20 ± 2σ |
| Pivot detection | N/A | 2-bar lookback + 2-bar lookahead on highs/lows |

## Binance Kline Response Format

Each candle: [open_time, open, high, low, close, volume, close_time, quote_asset_vol, num_trades, taker_buy_base, taker_buy_quote, ignore]

Indices used in analysis:
- [1] open, [2] high, [3] low, [4] close, [5] volume
