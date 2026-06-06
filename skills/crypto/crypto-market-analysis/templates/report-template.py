#!/usr/bin/env python3
"""
Crypto Fundamental Research Report Generator
Copy and modify for each session.
"""

import requests

# Configuration
BTC_PRICE = ...  # Set from live data
MSTR_PRICE = ...

# Fetch from StrategyTracker (or live source)
print("=== FETCHING DATA ===")
# Use CoinMarketCap API or Yahoo Finance or scrape

# BTC data
# headers = {'X-CMC_PRO_API_KEY': '7e0b6dfcde5a4682956512cc2e65dfe8'}
# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC'
# r = requests.get(url, headers=headers)
# ...

# MSTR data
# url = 'https://query1.finance.yahoo.com/v8/finance/chart/MSTR'
# r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# ...

# Report structure
data = {
    "btc_holdings": 843738,
    "avg_cost": 75701,
    "treasury_value": 64541122381,
    "total_spent": 63871810338,
    "unrealized_pnl": 669312043,
    "btc_price": 76494.27,
    "mstr_price": 159.89,
    "sats_per_share": 219626,
    "mnav": 0.95,
}

print("=" * 60)
print("RELATÓRIO T-800")
print("=" * 60)
print()
print(f"Holdings: {data['btc_holdings']:,} BTC")
print(f"Avg Cost: ${data['avg_cost']:,}/BTC")
print(f"Treasury: ${data['treasury_value']:,.0f}")
print(f"P&L: ${data['unrealized_pnl']:+,.0f} ({(data['btc_price']/data['avg_cost']-1)*100:+.2f}%)")
print(f"MSTR: ${data['mstr_price']:.2f}")
print(f"mNAV: {data['mnav']:.2f}x")
