# Missão 1 Bitcoin — Alexa Skill Reference

Full codebase and interaction model for a voice-controlled Bitcoin purchase tracker.

## Concept

User says "Alexa, acabei de comprar 500 reais de Bitcoin" and the skill:
1. Fetches current BTC price from CoinMarketCap
2. Calculates BTC amount purchased
3. Saves to DynamoDB per user
4. Reports progress toward 1 BTC goal

## Intents

| Intent | Purpose | Slots |
|---|---|---|
| `RegistrarCompraIntent` | Register a purchase | `{valor}` (AMAZON.NUMBER), `{moeda}` (CryptoCurrency) |
| `ConsultarProgressoIntent` | Check progress | None |
| `CotacaoIntent` | Get current price | `{cripto}` (CryptoCurrency, optional) |
| `ResumoMissaoIntent` | Full summary | None |
| `UltimaCompraIntent` | Last purchase | None |
| `RemoverUltimaCompraIntent` | Undo last purchase | None |

## Slot Type: CryptoCurrency

```json
{
  "name": "CryptoCurrency",
  "values": [
    {"name": {"value": "bitcoin", "synonyms": ["btc", "bit coin"]}},
    {"name": {"value": "ethereum", "synonyms": ["eth", "ether"]}},
    {"name": {"value": "solana", "synonyms": ["sol"]}},
    {"name": {"value": "cardano", "synonyms": ["ada"]}},
    {"name": {"value": "polkadot", "synonyms": ["dot"]}},
    {"name": {"value": "chainlink", "synonyms": ["link"]}},
    {"name": {"value": "avalanche", "synonyms": ["avax"]}}
  ]
}
```

## Sample Utterances (RegistrarCompraIntent)

```
acabei de comprar {valor} de {moeda}
comprei {valor} de {moeda} agora
registra compra de {valor} de {moeda}
acabei de adquirir {valor} de {moeda}
comprei {valor} em {moeda}
adiciona {valor} de {moeda} na missão
comprei mais {valor} de {moeda}
coloca {valor} de {moeda} na conta
```

## Invocation Name

`missão um bitcoin`

## User Data Structure (DynamoDB)

```json
{
  "userId": "amzn1.ask.account.xxx",
  "total_investido_brl": 1500.00,
  "total_btc_acumulado": 0.02345678,
  "preco_medio_brl": 64000.00,
  "historico_compras": [
    {
      "data": "2026-06-02T10:00:00+00:00",
      "valor_brl": 500.00,
      "btc_comprado": 0.00781234,
      "preco_btc_brl": 64000.00,
      "variacao_24h": 2.34
    }
  ],
  "ultima_atualizacao": "2026-06-02T10:00:00+00:00"
}
```

## Speech Formatting Rules

- < 0.001 BTC → "X satoshis" (multiply by 100,000,000)
- < 1 BTC → "X mili Bitcoins" (multiply by 1000)
- ≥ 1 BTC → "X Bitcoin" (4 decimal places)
- Currency → replace `.` with `,` for BRL: `f"{value:,.2f} reais"`
- Always chain `.ask()` to keep session alive (except Stop/Cancel)

## Key Implementations in lambda_function.py

### Decimal Handling
```python
def decimal_to_float(obj):
    if isinstance(obj, Decimal): return float(obj)
    if isinstance(obj, dict): return {k: decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, list): return [decimal_to_float(i) for i in obj]
    return obj
```

### CoinMarketCap Integration
```python
def get_btc_price_brl():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC&convert=BRL"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY, "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        price = data["data"]["BTC"]["quote"]["BRL"]["price"]
        change_24h = data["data"]["BTC"]["quote"]["BRL"]["percent_change_24h"]
    return float(price), float(change_24h)
```

### Session Lifecycle
- `LaunchRequest` → show welcome with current progress if returning user
- Every intent response uses `.ask()` (not `.speak()`) to keep mic open
- `StopIntent`/`CancelIntent` → close session with `.speak()` only

## Project File Structure

```
alexa-missao1btc/
├── lambda/
│   ├── lambda_function.py    # Full backend (handlers, DynamoDB, CMC API)
│   └── requirements.txt      # ask-sdk-core, boto3
├── interaction-model/
│   └── pt-BR.json            # Language model
└── docs/
    └── README.md             # Deploy instructions
```

## DynamoDB Table Setup

```bash
aws dynamodb create-table \
  --table-name Missao1BTC \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

## Lambda Environment Variables

| Variable | Value |
|---|---|
| `DYNAMODB_TABLE` | Missao1BTC |
| `CMC_API_KEY` | Your CoinMarketCap Pro API key |
| `ALEXA_SKILL_ID` | From Developer Console |
