#!/usr/bin/env python3
"""
Crypto Technical Analysis — 4H Chart Script
Fetches Binance data and prints structured analysis.
Usage: python crypto_4h_analysis.py [SYMBOL] [INTERVAL]
Default: BTCUSDT 4h
"""
import requests, sys, json

SYMBOL = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
INTERVAL = sys.argv[2] if len(sys.argv) > 2 else "4h"
LIMIT = 150

url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit={LIMIT}"
try:
    data = requests.get(url, timeout=10).json()
except Exception as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)

if not data or isinstance(data, dict):
    print(f"Invalid response: {json.dumps(data)[:200]}")
    sys.exit(1)

closes = [float(c[4]) for c in data]
highs = [float(c[2]) for c in data]
lows = [float(c[3]) for c in data]
volumes = [float(c[5]) for c in data]
current = closes[-1]

# SMAs
sma20 = sum(closes[-20:]) / 20
sma50 = sum(closes[-50:]) / 50

# EMAs + MACD
def ema(vals, period):
    m = 2/(period+1)
    r = [sum(vals[:period])/period]
    for p in vals[period:]:
        r.append((p - r[-1])*m + r[-1])
    return r

ema12 = ema(closes, 12)[-1]
ema26 = ema(closes, 26)[-1]
macd_line = ema12 - ema26
macd_all = [ema(closes[:i+1], 12)[-1] - ema(closes[:i+1], 26)[-1] for i in range(25, len(closes))]
signal = sum(macd_all[-9:])/9 if len(macd_all) >= 9 else 0

# RSI
gains = [closes[i]-closes[i-1] for i in range(1, len(closes))]
ag = sum(max(0,g) for g in gains[-14:])/14
al = sum(abs(min(0,g)) for g in gains[-14:])/14
rsi = 100 - 100/(1+ag/al) if al != 0 else 100

# Bollinger
var = sum((c-sma20)**2 for c in closes[-20:])/20
std = var**0.5
bb_up = sma20 + 2*std
bb_dn = sma20 - 2*std

# Pivots
pivots = []
for i in range(2, len(highs)-2):
    if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]:
        pivots.append(('RES', highs[i]))
    if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]:
        pivots.append(('SUP', lows[i]))

res = sorted([p for p in pivots if p[0]=='RES'], key=lambda x: x[1])[-5:]
sup = sorted([p for p in pivots if p[0]=='SUP'], key=lambda x: x[1], reverse=True)[-5:]

# Volume
vol_24h = sum(float(d[5]) for d in data[-6:])
vol_prev = sum(float(d[5]) for d in data[-12:-6])

# Output
print(f"=== {SYMBOL} — GRÁFICO {INTERVAL} ===")
print(f"")
print(f"Preço:  ${current:,.2f}")
print(f"Máxima: ${max(highs):,.2f} | Mínima: ${min(lows):,.2f}")
print(f"")
print(f"— MÉDIAS —")
print(f"SMA 20: ${sma20:,.2f}  |  Preço: {'ACIMA 🟢' if current>sma20 else 'ABAIXO 🔴'}")
print(f"SMA 50: ${sma50:,.2f}  |  Preço: {'ACIMA 🟢' if current>sma50 else 'ABAIXO 🔴'}")
print(f"Tendência: {'ALTA (SMA20 > SMA50) 🟢' if sma20>sma50 else 'BAIXA (SMA20 < SMA50) 🔴'}")
print(f"")
print(f"— MOMENTO —")
rsi_label = 'SOBRECOMPRADO ⚠️' if rsi>70 else 'SOBREVENDIDO 🟢' if rsi<30 else 'NEUTRO'
print(f"RSI (14): {rsi:.1f} — {rsi_label}")
print(f"MACD: {macd_line:.1f} | Sinal: {signal:.1f} | Hist: {macd_line-signal:.1f}")
print(f"MACD tendência: {'ALTA 🟢' if macd_line>signal else 'BAIXA 🔴'}")
print(f"")
print(f"— BOLLINGER BANDS —")
print(f"Sup: ${bb_up:,.2f} | Méd: ${sma20:,.2f} | Inf: ${bb_dn:,.2f}")
band_pos = 'Fora (acima)' if current>bb_up else 'Fora (abaixo)' if current<bb_dn else 'Dentro'
print(f"Preço: {band_pos}")
print(f"")
print(f"— SUPORTES —")
for r in sup:
    dist = ((r[1]-current)/current)*100
    print(f"  ${r[1]:,.2f} ({dist:+.1f}%)")
print(f"— RESISTÊNCIAS —")
for r in res:
    dist = ((r[1]-current)/current)*100
    print(f"  ${r[1]:,.2f} ({dist:+.1f}%)")
print(f"")
print(f"— VOLUME —")
print(f"24h: {vol_24h:,.0f} (x{vol_24h/vol_prev:.2f} da janela anterior)")
print(f"")
print(f"— ÚLTIMAS VELAS {INTERVAL} —")
for v in data[-8:]:
    o,h,l,c = float(v[1]), float(v[2]), float(v[3]), float(v[4])
    candle = '🟢' if c>o else '🔴'
    body = abs(c-o)
    shadow_upper = h - max(c,o)
    shadow_lower = min(c,o) - l
    print(f"{candle} O={o:,.0f} H={h:,.0f} L={l:,.0f} C={c:,.0f} Body={body:,.0f} U={shadow_upper:,.0f} Lw={shadow_lower:,.0f}")
