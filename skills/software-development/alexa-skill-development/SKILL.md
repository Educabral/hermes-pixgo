---
name: alexa-skill-development
description: "Build, deploy, and maintain Amazon Alexa Skills with Lambda backends — interaction models, custom intents, slot types, DynamoDB persistence, and voice-first UX patterns."
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [alexa, voice, lambda, aws, skill-kit, voice-assistant]
    related_skills: []
---

# Alexa Skill Development

Build voice-first Amazon Alexa Skills from scratch: interaction models (intents, slots, utterances), Lambda backends with the Alexa Skills Kit SDK Python, DynamoDB persistence, and third-party API integration.

## When to Use

- User asks: "create a skill for Alexa", "build an Alexa skill", "Alexa skill for X"
- User wants voice commands for crypto tracking, personal finance, habit tracking, or any data collection
- User needs voice-controlled progress tracking ("Alexa, I bought X, log it")

## Architecture Overview

```
User says "Alexa, {invocation_name}, {utterance}"
         ↓
Amazon Alexa Cloud (voice recognition)
         ↓
Skill's Interaction Model (intent matching + slot extraction)
         ↓
AWS Lambda (Python + ask-sdk-core)
  ├── Intent Handlers (RegistrarCompra, ConsultarProgresso, etc.)
  ├── DynamoDB (user data persistence)
  └── External API (CoinMarketCap, etc.)
         ↓
Alexa responds via SSML/text
```

## Step 1 — Define the Invocation Name & Intents

In the Amazon Developer Console, create a custom skill with a invocation name the user will say (e.g., "missão um bitcoin").

### Standard Alexa Intents (include these):
- `AMAZON.CancelIntent` — User says "cancel", "never mind"
- `AMAZON.StopIntent` — User says "stop", "off", "exit"
- `AMAZON.HelpIntent` — User says "help", "what can you do"
- `AMAZON.FallbackIntent` — User says something unrecognized
- `AMAZON.NavigateHomeIntent` — User says "go home"

### Custom Intents — Common Patterns

**Register/Create intent:**
```
"comprei {valor} de {moeda}"
"adiciona {item} na lista"
"registra {amount} de {currency}"
```

**Query/Status intent (no slots):**
```
"qual meu progresso"
"how much do I have"
"status report"
```

**Lookup intent (optional slot):**
```
"qual o preço do {cripto}"  — slot optional, defaults to BTC
```

## Step 2 — Write the Interaction Model

The interaction model is a JSON file defining your intents, their sample utterances, and custom slot types.

### Slot Type: Custom Enum
```json
{
  "name": "CryptoCurrency",
  "values": [
    {"name": {"value": "bitcoin", "synonyms": ["btc", "bit coin"]}},
    {"name": {"value": "ethereum", "synonyms": ["eth", "ether"]}}
  ]
}
```

### Slot: AMAZON.NUMBER
Use `AMAZON.NUMBER` for numeric values (prices, amounts, counts). Add sample utterances like `"{valor} reais"`, `"{valor} dólares"`.

### Slot Confirmation
Set `"confirmationRequired": false` unless the action is destructive or irreversible.

## Step 3 — Build the Lambda Backend

### Project Structure
```
project-name/
├── lambda/
│   ├── lambda_function.py       # Main handler
│   └── requirements.txt         # ask-sdk-core, boto3
├── interaction-model/
│   └── pt-BR.json               # Language model (or en-US.json)
└── docs/
    └── README.md                # Deploy instructions
```

### Lambda Skeleton
```python
import os, json, logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "LaunchRequest"
    def handle(self, handler_input):
        speech = "Welcome! Say something like..."
        return (handler_input.response_builder
                .speak(speech).ask("How can I help?")
                .set_card(SimpleCard("Title", speech)).response)

class MyIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MyIntent")(handler_input)
    def handle(self, handler_input):
        slot_val = get_slot_value(handler_input, "slot_name")
        # ... business logic ...
        return (handler_input.response_builder
                .speak("Result").response)

# Register handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MyIntentHandler())

# Lambda entry point
lambda_handler = sb.lambda_handler()
```

### DynamoDB Integration
```python
import boto3
from decimal import Decimal

table = boto3.resource("dynamodb", region_name="us-east-1").Table("TableName")

def decimal_to_float(obj):
    if isinstance(obj, Decimal): return float(obj)
    if isinstance(obj, dict): return {k: decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, list): return [decimal_to_float(i) for i in obj]
    return obj

def get_user(user_id):
    resp = table.get_item(Key={"userId": user_id})
    return resp.get("Item")

def save_user(data):
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    table.put_item(Item=data)
```

### External API Calls
Use `urllib.request` (stdlib — no extra dependencies):
```python
import urllib.request

req = urllib.request.Request(url, headers={"X-API-Key": "..."})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())
```

## Step 4 — Speech Best Practices

### Formatting Numbers for Speech
- Prices: `f"R$ {value:,.2f} reais"` (Alexa reads "reais" naturally)
- Small BTC: `< 0.001 → satoshis" (sat_value * 100_000_000)
- Medium BTC: `< 1 → mili Bitcoins" (value * 1000)
- Large BTC: `≥ 1 → Bitcoins" (value, 4 decimal places)

### Follow-up Prompts (skill keeps session alive)
Always chain `.ask("Anything else?")` so the user doesn't have to say "Alexa" again for the next command. Only use `.speak()` (no `.ask()`) on Stop/Cancel to close the session.

### Card Fallback
`SimpleCard("Title", "text")` shows on Alexa app/Echo Show. Essential for users who want to see numbers they can't easily remember from audio.

## Step 5 — Exception Handling

```python
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception): return True
    def handle(self, handler_input, exception):
        logger.error(f"Error: {exception}", exc_info=True)
        return handler_input.response_builder
            .speak("Sorry, something went wrong. Please try again.")
            .ask("Try again?").response
```

## Step 6 — Deploy to AWS

### DynamoDB Setup
```bash
aws dynamodb create-table \
  --table-name Missao1BTC \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### Lambda Setup
1. Create Lambda function (Python 3.12+), arm64 architecture
2. Set environment variables: `DYNAMODB_TABLE`, `CMC_API_KEY`, `ALEXA_SKILL_ID`
3. Attach IAM role with `dynamodb:GetItem`, `dynamodb:PutItem` on the table
4. Add Alexa Skills Kit trigger with your Skill ID
5. Set timeout to 10s (AI API calls may need 30s)
6. Zip and upload (or use inline editor for small scripts)

### Developer Console Setup
1. Create skill at developer.amazon.com → Alexa Skills Kit
2. Choose custom model, "Provision your own" backend
3. Paste interaction model JSON
4. Set endpoint to your Lambda ARN

### Testing
Use the "Test" tab in the Developer Console — type utterances directly or use voice with an Echo device linked to your dev account.

## Pitfalls

- **`skill_view()` before `skill_manage()`** — always load existing skills before editing to avoid overwriting recent changes
- **ASK model vs Lambda ARN mismatch** — the Skill ID in the Lambda trigger must match exactly
- **Slot values can be None** — always check `get_slot_value()` return before using
- **DynamoDB Decimals break JSON** — always use `decimal_to_float()` utility before serializing user data into speech text
- **Session persistence in memory** — DynamoDB is per-user persistence; for multi-user, key on `user_id` from `handler_input.request_envelope.context.system.user.user_id`
- **urllib vs requests** — Lambda cold starts with the stdlib `urllib` are faster; avoid `requests` unless you need complex auth
- **Timeout >= 10s** — if calling external APIs (CoinMarketCap, etc.), set Lambda timeout to at least 10s
- **Language model locale** — the interaction model JSON must match the skill's locale (`pt-BR`, `en-US`, etc.)
- **Alexa SSML limits** — keep responses under 8000 chars SSML (roughly 200-300 words) or Alexa cuts off; for long summaries, paginate with follow-up prompts
- **Do NOT use `RegistrarCompraIntent` with decimal-inclusive utterances** — `AMAZON.NUMBER` slot type handles "quinhentos" well but can misparse "quinhentos e cinquenta" in some locales. Test thoroughly.
- **The `.ask()` chain is essential** — without it, the session closes and the user must say "Alexa" again. Only use `.speak()` (no `.ask()`) on Stop/Cancel intents.
- **Card text truncation** — `SimpleCard` text is truncated on Echo Show devices after ~200 chars; for long numeric summaries, break into multiple cards or rely on speech output for the full data

## References

- `references/missao-1-btc-skill-guide.md` — Full project structure and codebase for the "Missão 1 Bitcoin" Alexa Skill (invocation name: "missão um bitcoin", intents: RegistrarCompra, Cotacao, ConsultarProgresso, ResumoMissao, UltimaCompra, RemoverUltimaCompra; DynamoDB persistence; CoinMarketCap integration)
- **Session 2026-06-02 full project** at `C:\Users\PC\Desktop\Projetos_do_Chefe\alexa-missao1btc\` — complete lambda_function.py (200+ lines), interaction model pt-BR.json, and dynamodb-setup.sh created in that session. The Lambda has 10 intent handlers, DynamoDB Decimal-to-float utilities, urllib.request for CMC API with HMAC-signable webhook-style signatures in comments, and full PT-BR speech formatting for BTC values (satoshis/mili/whole)

## Templates

- `templates/` — (none yet) reusable Lambda function skeletons, interaction models, or CloudFormation templates go here
