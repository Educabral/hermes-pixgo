# Session URLs (example — replace with live values each session)

- Flask server: http://localhost:5000 (endpoint: `/ifttt-trigger`)
- ngrok dashboard: http://127.0.0.1:4040

## IFTTT Webhook Body

```json
{"comando": "{{EventName}}"}
```

## Comandos Suportados (exemplo)

| Comando | Ação |
|---------|------|
| teste | Testa conexão |
| notícias | Busca Degenzone21 |
| e-mails | Lê caixa de entrada |
| postar thread | Posta no X |
| resumo | Briefing do dia |

## Voice Monkey Setup (Primeira Vez)

1. Skill "Voice Monkey" no app Alexa (usuário instala)
2. voicemonkey.io → Console → Sign in with Amazon
3. Login Amazon: email + senha → código SMS (usuário fornece) → colar no campo
4. Criar Monkey: nome "comando", frase "manda hermes", webhook URL do ngrok
5. Falar: "Alexa, manda hermes teste"

### Alternativa: Voice Monkey Flows (v3, recomendada sobre Monkeys)

Se o dashboard tiver opção "Flows" no menu:
- Console → Flows → New Flow
- Web Request action → URL do ngrok, POST, JSON
- Copiar frase de Custom Action gerada pelo Flow
- Alexa Routine → Custom Action → colar frase
- Não precisa do comando "Alexa, manda..." — usa Custom Action nativa

### Se o Console levar a 404

O dashboard do Voice Monkey v3 pode ter links quebrados. Caminhos diretos:
- Dashboard: app.voicemonkey.io/dashboard
- Flows: app.voicemonkey.io/app/flows (se disponível)
- API Tokens: app.voicemonkey.io/app/api-tokens (gerou chave com sucesso)
- API base: https://api.voicemonkey.io/v2/ (v2, não confirmado se ativa)

Se console web não funcionar, a skill já está ativa na conta Amazon. Usar Alexa Routines nativas com Custom Action (não HTTP Request, que não existe no Brasil).

## IFTTT Credentials (se aplicável)

- Maker Webhooks API key: armazenada em memória permanente (senha)
- Trigger URL: `https://maker.ifttt.com/trigger/{event}/json/with/key/{key}`
