---
name: crypto-market-analysis
description: Complete workflow for crypto market content production — fundamental research on treasuries/protocols, technical analysis via exchange APIs, and news posting with persona voice. All three workflows share a common user context (Edu, PixGo founder, Brazilian crypto OG) and tone culture.
tags:
  - crypto
  - market-analysis
  - fundamental-analysis
  - technical-analysis
  - news
  - bitcoin
  - trading
  - research
  - content-creation
related_skills:
  - bip39-seed-recovery
platforms: [windows]
---

# Crypto Market Analysis — Umbrella

## Overview

Three complementary workflows for producing crypto market intelligence and content:

1. **Fundamental Research** — deep-dive on corporate Bitcoin treasuries (MicroStrategy/Strategy), on-chain holder analysis, protocol treasuries, and financial reports
2. **Technical Analysis** — real-time chart analysis via Binance API (BTC, ETH, altcoins), indicator calculation, support/resistance detection
3. **News Posting (PutinHO Pipeline)** — fetch, research, critique, and post crypto news to X/Twitter with the PutinHO persona (@Cabral_Cripto)

All three share the same user context: Edu (PixGo founder, Brazilian crypto OG) expects direct, aggressive, data-driven output in Brazilian Portuguese with profanity and zero fluff.

---

## Section A: Fundamental Research

### When to Use

- "Analise o esquema de compras de BTC do Michael Saylor / MicroStrategy"
- "Faça um relatório completo sobre [project/company]"
- "Estudo aprofundado sobre [crypto treasury / whale / foundation]"
- On-chain analysis of large holders

### ⚠️ CRITICAL: Always Verify from Primary Sources

**Never rely on estimated/synthesized data.** Always:
1. **Find a live tracker** — StrategyTracker.com, BitcoinTreasuries.net, Dune Analytics, CoinGecko, Glassnode
2. **Check the official source** — SEC filings (EDGAR), company press releases, CEO X/Twitter announcements
3. **Cross-reference** at least 2 sources
4. **Note the date** — crypto data changes fast

### Source Hierarchy

| Quality | Source | Example |
|---------|--------|---------|
| 🥇 Primary (SEC filing / press release) | EDGAR, company IR page | MicroStrategy 8-K |
| 🥇 Live tracker (aggregates SEC data) | StrategyTracker.com, saylortracker.com | mstr-tracker.com |
| 🥈 Aggregator (crowdsourced) | BitcoinTreasuries.net, Dune | 24-48h behind |
| 🥉 News article | CoinTelegraph, The Block, CoinDesk | May have errors |
| ❌ Estimated/synthetic | AI-generated lists, personal blogs | NEVER use |

### Key Data Points (Strategy / ex-MicroStrategy)

- **Preferred stock (STRC):** US$ 15B face value, 11.5% annual dividend = US$ 1.725B/yr obligation. Dividend is a RECURRING contractual obligation, payable monthly in cash.
- **Total BTC holdings** (from live tracker): 843,706 BTC as of June 1, 2026 (check filing date — changes fast)
- **Average cost per BTC:** ~US$ 75,699 (as of May 31, 2026 filing)
- **Total spent, current treasury value, unrealized P&L**
- **BTC Yield %** (YTD / QoQ)
- **MSTR stock price**, outstanding shares (~180M), dilution tracking
- **mNAV** (multiple to Net Asset Value)
- **Debt:** convertible notes total (~US$ 6.7B), maturity dates, interest rates
- **Cash reserves:** ~US$ 900M (from ATM + debt management)
- **Risk scenarios at various BTC price levels**
- **Funding model:** ATM common stock issuance + convertible notes + preferred stock → all used to buy BTC → BTC doesn't yield → preferred dividends paid by selling BTC or issuing more stock/debt

### Report Structure

**Section 1: Current Numbers** — holdings, avg cost, treasury value, P&L
**Section 2: Historical Timeline** — key milestones with dates
**Section 3: Funding Mechanism** — convertibles, ATM offerings, preferred stock
**Section 4: Risk Analysis** — bear case scenarios with dollar amounts
**Section 5: Market Impact** — concentration risk, systemic risk

### Tone & Style (Fundamental)

- Direct, aggressive, no fluff
- Brazilian Portuguese profanity (porra, caralho, rapa)
- Percentages with hard dollar amounts
- End with a strong opinion / conclusion

### Common Pitfalls

- ❌ Don't estimate BTC holdings from memory. Always pull the live number.
- ❌ Don't assume profit — check margins. In May 2026 Strategy was barely above cost basis (~+1%).
- ❌ Don't use old data — Strategy doubled holdings from 447K to 843K in ~16 months.
- ❌ Don't confuse MSTR (NASDAQ) with STRC (preferred stock) or STRK (another preferred series).
- ❌ Don't call a sale "insignificant" without doing the math — 32 BTC is 0.0038% of 843K, but the precedent is the story, not the size. The first sale normalizes the second.
- ⚠️ **SEC.gov blocks automated requests.** Filing URLs return 'Undeclared Automated Tool' when hit by curl/browserless. Workaround: use `curl -A "Mozilla/5.0..."` with a real User-Agent, or rely on CoinDesk/Cointelegraph articles that cite the filing directly. For critical filings, access via SEC EDGAR full-text search on a real browser session.
- ⚠️ **First BTC sale is a major narrative event.** Strategy built its brand on "never sell, hodl forever." Any sale, regardless of size, crosses that line. The market reacts to the narrative shift, not the dollar amount.
- ⚠️ **Simultaneous ATM + sale = signal.** If Strategy is selling BTC AND issuing ATM shares in the same week (e.g., $128M ATM + 32 BTC sale), it means cash from share issuance isn't enough to cover obligations + BTC accumulation. The funding model has multiple concurrent pressure points.
- ⚠️ **Dividend math is critical.** 11.5% on US$15B preferred = US$1.725B/yr = US$143.75M/mo. 32 BTC at ~$77k = US$2.5M, which covers ~0.5 days of dividend. Project forward: how many BTC per quarter needed to sustain the dividend at current prices?
- ⚠️ Dilution: shares went from ~10M (2020) to ~180M (2026) — 18x.
- ⚠️ mNAV below 1.0x = market values company below its BTC holdings (bearish).

### References & Scripts

See `references/michael-saylor-treasury-report-may2026.md` for a verified example report.
See `templates/report-template.py` for a copy-and-modify report generator.

---

## Section B: Technical Analysis

### When to Use

- "Analyze BTC/ETH on the 4h chart"
- "What's the market looking like?"
- Technical indicators for a specific crypto
- Support/resistance levels

### Core Workflow

**Step 1: Fetch klines from Binance API**
```python
url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
# No API key needed for public klines endpoint
```

**Step 2: Calculate indicators**
- SMA20, SMA50 — trend direction
- EMA12, EMA26 → MACD (line, signal, histogram)
- RSI(14) — Wilder's smoothed RSI
- Bollinger Bands (20, 2) — volatility bands
- Pivot detection — 2-bar lookback/forward on highs and lows

**Step 3: Structure output**

```
Preço: $XX,XXX
Timeframe: 4H

Medium-term trend: BAIXA (SMA20 < SMA50) or ALTA
MACD: Bullish/Bearish (histogram value)
RSI: XX (Neutral / Oversold / Overbought)
Bollinger: Inside / Touching upper / Touching lower

Supportes:
- $XX,XXX
Resistências:
- $XX,XXX

Cenários:
- 🟢 Alta (XX%): [conditions]
- 🔴 Baixa (XX%): [conditions]
```

**Step 4: Add candlestick context** — last 6-10 candles, look for rejection wicks, volume spikes, doji, engulfing patterns.

### Indicator Quick Reference

| Indicator | Period | Formula |
|-----------|--------|---------|
| SMA | 20, 50 | Simple average of closes |
| EMA | 12, 26 | 2/(n+1) × (price - prev EMA) + prev EMA |
| MACD | 12, 26, 9 | EMA12 - EMA26, signal = EMA9 of MACD line |
| RSI | 14 | 100 - 100/(1 + avg_gain/avg_loss), Wilder's smoothing |
| Bollinger | 20, 2 | SMA20 ± 2σ |

### Pitfalls

- Binance rate limits: 1200 req/min for public endpoints — fine for single-symbol.
- USDT pairs by default. Adjust for BRL pairs (BTCBRL, ETHBRL).
- On git-bash Windows: use `python` not `python3`. Verify with `python --version`.
- 4H timeframe pivots are for the 4H chart only — don't extrapolate to daily/weekly.
- Pure OHLCV — no order book / CVD / bid-ask spread data.
- Self-reported analysis, not investment advice.

### References & Scripts

See `references/indicators-reference.md` for session examples (BTC and ETH 4H) and Binance kline format.
See `scripts/crypto-4h-analysis.py` for a reusable script: `python crypto-4h-analysis.py BTCUSDT 4h`.

---

## Section C: News Posting (PutinHO Pipeline)

### When to Use

User says "busque notícia e poste", "faça um post sobre", "pesquise e publique no X", "quero postar sobre [tema]".

### Prerequisites

No dedicated scripts currently installed. To create them:
- `get_degen_news.py` — fetches 5 news items filtered from degenzone21 Telegram channel (needs Telegram API or browser access)
- `post_to_x.py` — posts to X/Twitter via API (needs X API credentials)

### Workflow

#### 1. Identify Target News

User says something like "vasculhe sobre [tema]" or "busque notícia sobre". Identify the specific event/claim to investigate.

**If the user provides a numerical correction** (e.g., "Strategy tem 840.000 BTC, não 500k"), update ALL math in your response immediately. Recalculate percentages, projections, and per-unit costs. Do not ignore corrections — the user is often closer to the data than your research found.

**Two-tier correction pattern:** The user's initial correction is often approximate (e.g., "840k" from memory). The actual filing may be more precise (e.g., 843,706). Workflow:
1. Immediately adopt their number as the working figure — update all math
2. Research the exact figure from the live source (saylortracker, SEC filing, CoinDesk) in parallel
3. If the exact figure differs slightly, update silently — no need to flag the delta unless it changes the math significantly
4. The user respects precision. Getting closer to the exact number without being corrected again is the goal

#### 2. Delegate Parallel Research & Review

**Task A — Deep Researcher:** Spawn a subagent with [browser] tools to investigate the specific claim. Give it: exact news event, data points you already have, sources to check (CoinDesk, CoinTelegraph, The Block, Decrypt, SEC filings). Ask it to verify:
- Exact figure (amount, price, date range)
- Source document (filing name/number if applicable)
- Official stated reason vs market speculation
- Any secondary context (simultaneous filings, ATM offerings, debt moves)

**Task B — Skeptic Editor:** Spawn a subagent to receive the full research output and DESTROY it:
- Find logical holes, narrative clichés, weak arguments
- Check the math (dividend cost × frequency vs BTC sale proceeds)
- Project worst-case scenarios with dollar amounts
- Identify "diminutivo tranquilizador" pattern ("só 32 BTC", "apenas 2 milhões", "irrelevante")
- Identify "distinção falsa" pattern ("operacional vs estratégico")

**⚠️ Caveat:** Subagents have no `web_search` tool — they work with context you provide. If browser tools fail (Cloudflare, bot detection), go to fallback. Do not retry delegation — use manual research instead.

#### 3. Consolidate Findings

After both subagents return:
1. Take the verified data from Deep Researcher
2. Apply every Skeptic Editor critique to refine the analysis
3. Re-do the math with the corrected numbers the user supplied
4. Rewrite in PutinHO tone

**Multi-round corrections:** If the user corrects your numbers again (e.g., "840k" → "843,706"), update once more without complaint. Each correction makes the output stronger.

### PutinHO Tone Rules (CRITICAL)

- **No clichés:** nada de "auto-custódia é o mínimo", "aprenda com os outros"
- **No friendly openings:** não comece com pergunta retórica. Comece com o FATO.
- **Sarcasmo + agressividade:** deboche contra quem errou, não lição de moral no leitor.
- **Parágrafos curtos:** 1-2 linhas máx. Frases cirúrgicas.
- **Dados são a carne:** número sem contexto é alarmismo. Contextualize.
- **Nunca generalize sem nuance:** diferencie protocolos. O erro não é ser centralizado — é ser negligente.
- **Final sem autoajuda:** termine com um murro, não lição de moral.

### Skeptic Editor Checklist (What Gets Destroyed)

1. **Generic rhetorical question opening** — boring. Start with the fact.
2. **Numbers without context** — $2.8M is tiny vs $307B market; contextualize or admit scale.
3. **Triple parallel structure** — "Não foi bug. Não foi ataque. Foi erro humano." — cliché copywriting.
4. **Generic generalization** — "TODA stablecoin centralizada" — intellectually dishonest.
5. **"Auto-custódia resolve tudo" mantra** — introduces different risks. Be honest.
6. **Generic ending** — "aprenda com os erros dos outros" fits any topic. Make it specific.

**Every post must include:** event date, exact ticker, exploit mechanism, multisig threshold, chain, issuer reaction, comparable incidents.

### Pitfalls

- CAPTCHA on external search — if blocked, work with `get_degen_news.py` output + own knowledge.
- `post_to_x.py` may fail silently — verify exit code + success message.
- **`post_to_x.py` does NOT support threads (multi-tweet chains).** It opens a single tweet intent per call. To post a thread, you must either: (a) deliver as a text file for manual copy-paste, (b) post one tweet at a time via the script (requires reply_to_id linking), or (c) try browser login — see "Posting via Browser" note above.
- **Browser login on X.com frequently blocked.** The headless browser (Comet/browserless) triggers X's rate limiter: "Limitamos temporariamente seu acesso. Tente novamente mais tarde." This is a device fingerprint / IP-level block, not a credential problem. Recovery requires the user to log in from their normal device and authorize the new browser in Security settings.
- **Fallback for blocked login:** Save thread content as a .txt file on the Desktop `C:\Users\PC\Desktop\nome_do_arquivo.txt` for the user to manually copy-paste into X. This is a reliable fallback that always works.
- Deep Researcher (delegate_task) may return truncated results with deepseek-chat — don't repeat delegation, go to fallback immediately.
- `browser` tools may not work for web research due to CAPTCHA — prefer `terminal` + `curl`.
- **CoinDesk article access pattern:** The homepage snapshot shows article headlines as clickable links `[ref=eXX]`, but the browser_click may not open the article page. Reliable workaround: use browser_console to run `Array.from(document.querySelectorAll('a')).filter(a => a.textContent.includes('32 bitcoin')).map(a => a.href)` to extract the exact article URL, then browser_navigate directly to that URL.
- **`post_to_x.py` does NOT support threads (multi-tweet chains).** It opens a single tweet intent per call. To post a thread, you must either: (a) paste each tweet in sequence on X manually, (b) save the full thread text to a file and share with the user for copy-paste, or (c) post one tweet at a time via the script and have the user reply to each in sequence. The script also breaks when the bash shell interprets quotes, accents, or multiline strings with `---` separators — always escape or save input to a temp file first.

### Posting via Browser (X.com Login)

When the user asks you to log into their X account and post directly (instead of using `post_to_x.py`):

1. Navigate to `https://x.com/i/flow/login`
2. Type the email and press Enter
3. X will ask for password on the next screen — type and submit
4. **Known blockers:**
   - **Rate limit:** X shows "Limitamos temporariamente seu acesso. Tente novamente mais tarde." after too many login attempts from an unrecognized browser. This is a session-level IP/device fingerprint block, not a credential issue.
   - **Recovery:** User needs to log in from their normal device/browser first and authorize the new device in Security settings.
   - **Fallback:** If browser login fails, deliver the thread as a text file to the Desktop for manual copy-paste, or use `post_to_x.py` for single tweets.
5. Browser automation via browserless/Comet headless mode is detected by X as suspicious. Always use the real Comet browser path for X login attempts.

### Post Format Variants

The user expects THREE output formats depending on audience and content:

**0. Thread format — PutinHO style (common for tutorials)**
- Used for educational/financial-anonymity content with multiple steps
- Each "estrofe" (stanza) is a self-contained tweet, ~280 characters max
- **CRITICAL: Do NOT use numbered prefixes (1/7, 2/8, 3/6, etc.)** — user hates them
- **CRITICAL: Do NOT use `---` separators between stanzas** — user hates them
- Just raw tweet text blocks separated by blank lines (two blank lines between tweets)
- First tweet hooks hard — no rhetorical questions, start with the fact (not "Você sabe que...")
- Last tweet closes with a punch — no self-help, no moral lesson
- Aggressive/sarcastic PutinHO tone, profanity, short sentences, zero fluff
- Structure: each stanza is one step of the tutorial, one punch, or one idea
- **Delivery:** `post_to_x.py` does NOT support threads natively. Options:
  (a) Save to Desktop .txt file for manual copy-paste into X
  (b) Try browser login (see "Posting via Browser" above) — but likely blocked
  (c) Post one tweet at a time via the script with `reply_to_id` if the API supports it
- **Example of correct structure (no 1/7, no ---):**

```
PIX bateu na conta. O cliente pagou. O sistema já sabe que você recebeu.

Mas você não vai deixar eles saberem onde esse dinheiro vai parar, vai?

Então cola aqui que o manual das sombras versão 2026 chegou.
```

**1. Single-tweet longform (PutinHO tone)**

**1. Single-tweet longform (PutinHO tone)**
- Used for general crypto Twitter audience
- Aggressive/sarcastic, profanity, short paragraphs, data-driven
- Post via `post_to_x.py`
- Character limit: ~280-4000 chars (X Premium)
- Do NOT use `---` separators inside the tweet text

**2. Thread format (specialist/DeFi audience)**
- Used for groups of experts (DeFi devs, traders, analysts)
- Polished, grammatically correct, proper punctuation and accents
- Same analytical depth but structured as numbered tweets (1/8, 2/8 etc.)
- Each tweet: 2-4 short paragraphs max
- Between tweet blocks: add 2-3 blank lines as visual separator
- `post_to_x.py` cannot post threads natively — deliver as text file or paste each tweet
- **CRITICAL:** User corrects grammar, punctuation, and accent errors on specialist posts. Proofread before delivering.

### Verification Checklist (Before Delivering)

- [ ] Numbers verified against live source (saylortracker, CoinDesk, SEC filing)
- [ ] Math checked (dividend cost ÷ sale proceeds = days covered)
- [ ] Narrative clichés eliminated ("diminutivo tranquilizador", "distinção falsa")
- [ ] Put corrections into practice immediately (user often knows exact figures from memory)
- [ ] For specialist posts: proofread for punctuation, accents, grammar
- [ ] For threads: each tweet is self-contained (doesn't require reading previous)
- [ ] No `---` inside tweet text (breaks rendering)

### References

See `references/skeptic-editor-principles.md` for the full checklist.
See `references/thread-format-specialists.md` for the thread posting workflow.
See `references/fluxo-anonimato-pix-btc.md` for the complete PIX→BTC financial-anonymity pipeline via PixGo, Houdini, Monero.
Note: `scripts/get_degen_news.py` and `scripts/post_to_x.py` are NOT installed — create them when setting up the news pipeline.
