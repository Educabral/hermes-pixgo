# Voice Monkey API v3 — Endpoints

> Descobertos empiricamente via sessão real no console app.voicemonkey.io
> Token obtido em: app.voicemonkey.io/app/api-tokens

## Autenticação

Token passado como query parameter `token=` na URL.
Formato: UUID-like com hífens (ex: `54a40-5a2ee-c7a11-c72f5-...`)

## Endpoints Confirmados

### GET /devices
```
GET /devices?token={TOKEN}
```
Lista dispositivos Echo vinculados à conta.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "bedroom-echo-5zhh7",
      "name": "Bedroom Echo",
      "capability": "speakers"
    }
  ]
}
```

### GET /flow
```
GET /flow?token={TOKEN}&flow={FLOW_REF}
```
Retorna informações do flow.

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `token` | Sim | Token da API |
| `flow` | Sim | Request Ref de 4 dígitos do flow |
| `include=nodes` | Não | Tentativa de incluir nodes — NÃO funciona, retorna só metadados |

**Response:**
```json
{
  "success": true,
  "data": {
    "flowId": "568cce22-6614-4af9-961a-c1ac86f175d1",
    "flowName": "Hermes Comando",
    "requestRef": "2916"
  }
}
```

### POST /flow
```
POST /flow?token={TOKEN}&flow={FLOW_REF}&type=web_request&url=...&method=POST
```
Aceita parâmetros adicionais na query string. Retorna o mesmo que GET /flow.
**Confirmado: NÃO adiciona nodes.** O POST em /flow com query params retorna 200 com os mesmos dados do flow, mas a configuração não é persistida — o node Web Request não é adicionado. A API v3 é READ-ONLY para configuração.

### GET ou POST /trigger
```
GET /trigger?device={DEVICE_ID}&token={TOKEN}&flow={FLOW_REF}
POST /trigger?device={DEVICE_ID}&token={TOKEN}&flow={FLOW_REF}
```
Dispara a execução do flow.

**Response:**
```json
{
  "success": true,
  "data": "OK"
}
```

## Endpoints que NÃO Existem (404)
- `/flows` — lista de flows
- `/flows/{ID}` — detalhe de flow por ID
- `/flows/{ID}/nodes` — nodes de um flow
- `/flow/nodes` — operações em nodes
- `/webhooks` — webhooks
- `/endpoints` — documentação
- `/skills` — skills
- `/routines` — rotinas
- `/commands` — comandos
- `/actions` — ações
- `/triggers` — triggers
- `/utterances` — utterances
- `/monkeys` — monkeys (antigo nome dos Flows)
- `/apps` — apps
- `/config` — configuração
- `/profile` — perfil
- `/account` — conta

## Métodos HTTP Suportados
- `/flow`: GET ✅, POST ✅, PUT ❌ (405)
- `/trigger`: GET ✅, POST ✅
- `/devices`: GET ✅

## Info do Console Web
- Console: `app.voicemonkey.io`
- Login: redireciona para Amazon (2FA via SMS)
- Dashboard: `app.voicemonkey.io/dashboard`
- Flows: `app.voicemonkey.io/flows`
- API Tokens: `app.voicemonkey.io/app/api-tokens`
- Docs/Guides: site público `voicemonkey.io/guides/...` (não requer login)

## Fluxo de Configuração de Nodes (Web Request)

A adição de nodes/ações (ex: Web Request) no flow **NÃO PODE ser feita via API**. É necessário usar o console web:

1. Acessar `app.voicemonkey.io/flows` (autenticado)
2. Clicar no flow desejado
3. A tela mostra o trigger "Start" e um botão "+" para adicionar próximo nó
4. Selecionar "Web Request" da lista de ações
5. Preencher: URL, Method, Headers, Body
6. Salvar

Após configurar, a tela mostra:
- **API Trigger URL:** `https://api-v3.voicemonkey.io/trigger?device=DEVICE_ID&token=TOKEN&flow=2916`
- **Request Ref:** número de 4 dígitos (ex: 2916)
- Opções: Inbound Webhooks, Schedules, Other flows
