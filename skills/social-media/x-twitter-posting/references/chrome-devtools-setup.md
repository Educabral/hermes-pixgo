# Chrome DevTools Setup for X Posting

## Detecting the WebSocket Endpoint

After starting Chrome with `--remote-debugging-port=9222 --remote-allow-origins=*`:

```bash
# Get the browser WebSocket URL (stable across sessions)
curl -s http://localhost:9222/json/version | python -c "import sys,json; print(json.load(sys.stdin)['webSocketDebuggerUrl'])"

# List all open pages/tabs with X.com URLs
curl -s http://localhost:9222/json | python -c "
import sys,json
data = json.load(sys.stdin)
for d in data:
    u = d.get('url','')
    if 'x.com' in u:
        print('ID:', d['id'])
        print('URL:', u)
        print('WS:', d.get('webSocketDebuggerUrl',''))
"
```

## Common Issues

- **"Session closed" error**: The page was closed or navigated away. Re-open `compose/post`.
- **0 pages returned by pyppeteer**: The WebSocket endpoint changed (Chrome was restarted). Re-fetch from `/json/version`.
- **Tab do X não aparece no `pages()`**: O pyppeteer às vezes não enxerga abas abertas antes da conexão. Solução: pedir pro usuário fechar e reabrir a aba do compose, ou usar `browser.newPage()` e navegar — mas isso PERDE a sessão logada.
- **Timeout no `goto()`**: Não usar `waitUntil='networkidle0'`. O X nunca fica totalmente idle. Usar `await asyncio.sleep(4)`.
- **Botão "Add" não aparece**: O React do X precisa detectar texto digitado REALMENTE (type(), paste(), ou teclado). innerHTML não funciona.
