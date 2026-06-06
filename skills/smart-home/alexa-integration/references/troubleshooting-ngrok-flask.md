# Troubleshooting ngrok + Flask + IFTTT

## Checklist rápido antes de pedir pro usuário testar

SEMPRE verificar esses 3 pontos ANTES de pedir pro usuário apertar qualquer botão no IFTTT:

```bash
# 1. Flask respondendo?
curl -s http://localhost:5000/
# Esperado: {"servico":"Hermes Agent - Alexa Bridge","status":"online","versao":"1.0.0"}

# 2. ngrok ativo?
curl -s http://localhost:4040/api/tunnels | python -c "import sys,json; d=json.load(sys.stdin); print(d['tunnels'][0]['public_url'])"
# Esperado: https://SEU_DOMINIO.ngrok-free.dev

# 3. Teste o caminho completo pelo ngrok
curl -s -X POST "https://SEU_DOMINIO.ngrok-free.dev/ifttt-trigger" \
  -H "Content-Type: application/json" \
  -d '{"value1":"teste","value2":"","value3":""}'
# Esperado: {"comando":"teste","status":"ok"}
```

Se algum desses falhar, o usuário vai apertar o botão e nada vai acontecer — gerando frustração.

## Caso 1: Flask offline

Sintoma: `curl http://localhost:5000/` falha ou retorna erro.

Causa: Processo morreu (crash, janela fechada, restart do PC).

Solução:
```bash
# Matar processos antigos na porta 5000
powershell -Command "Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"

# Subir novo
cd /c/Users/PC/AppData/Local/Temp && python alexa_bridge.py &
sleep 2
curl -s http://localhost:5000/
```

## Caso 2: ngrok offline

Sintoma: `curl http://localhost:4040/` falha.

Solução:
```bash
ngrok http 5000 --domain SEU_DOMINIO.ngrok-free.dev &
sleep 3
curl -s http://localhost:4040/api/tunnels | python -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"
```

## Caso 3: IFTTT disparou mas não chegou

Sintoma: Usuário apertou o botão, `curl localhost:5000/` responde, ngrok ativo, mas nenhum POST chegou.

Causas possíveis:
1. **Widget não foi adicionado na tela:** O Applet foi criado mas o botão físico do widget não foi adicionado na aba Widgets do app IFTTT. Pedir pro usuário: app IFTTT → aba Widgets → adicionar o widget do Applet.
2. **Applet usa trigger diferente:** Verificar se o Applet realmente tem Button widget como trigger e Webhooks como action.
3. **IFTTT usa formato value1/value2/value3:** O Webhooks do IFTTT Button widget envia `{"value1":"","value2":"","value3":""}` mesmo que o Body configurado seja outro. O `alexa_bridge.py` já trata isso extraindo comando de `value1`.
4. **IFTTT não encontrou o endpoint:** Testar o ngrok manualmente (checklist #3). Se o curl direto funciona, o problema é no IFTTT.
5. **Usuário apertou no lugar errado:** Pedir pra ir em My Applets → clicar no Applet → "Run"

## Caso 4: Flask subiu mas não loga requisições

Sintoma: O Flask responde a `curl localhost:5000/` mas `process(action='log')` mostra output vazio.

Isso acontece quando o Flask foi reiniciado em background (novo session_id) e o session_id antigo não existe mais. Usar `process(action='list')` para ver os processos ativos, depois `process(action='log', session_id=NOVO_ID)`.

Alternativa: testar direto com curl invés de depender do log.
