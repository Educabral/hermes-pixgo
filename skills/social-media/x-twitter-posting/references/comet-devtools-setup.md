# Setup do Comet para Automação via Chrome DevTools Protocol

## Comandos para abrir o Comet com debug remoto

```powershell
# Matar instância anterior
taskkill /F /IM comet.exe 2>$null

# Abrir com debug na porta 9222
Start-Process -FilePath "C:\Program Files\Perplexity\Comet\Application\comet.exe" `
    -ArgumentList "--remote-debugging-port=9222", "--remote-allow-origins=*"

# Abrir com URL específica (já logado)
Start-Process -FilePath "C:\Program Files\Perplexity\Comet\Application\comet.exe" `
    -ArgumentList "--remote-debugging-port=9222", "--remote-allow-origins=*", `
        "https://x.com/compose/post"
```

## Verificar conexão

```bash
# Listar todas as abas
curl -s http://localhost:9222/json | python -m json.tool

# Pegar WebSocket do Browser (para pyppeteer)
WS_URL=$(curl -s http://localhost:9222/json/version | python -c "import sys,json; print(json.load(sys.stdin)['webSocketDebuggerUrl'])")

# Pegar WebSocket de uma aba específica do X
curl -s http://localhost:9222/json | python -c "
import sys,json
data = json.load(sys.stdin)
for d in data:
    if 'x.com' in d.get('url',''):
        print(d['webSocketDebuggerUrl'])
"
```

## Instalação do pyppeteer

```bash
pip install pyppeteer
```

## Conexão básica

```python
from pyppeteer import connect

async def main():
    browser = await connect(
        browserWSEndpoint='ws://localhost:9222/devtools/browser/0ac87ecc-...'
    )
    # browser.pages() retorna as abas abertas
    # browser.newPage() cria nova aba
    ...
    await browser.disconnect()
```

## Seletores do X para postagem

| Elemento | Seletor |
|---|---|
| Textarea do tweet | `[data-testid="tweetTextarea_0"]` |
| Botão Novo Tweet (sidebar) | `[data-testid="SideNav_NewTweet_Button"]` |
| Botão Adicionar na thread | `[data-testid="addButton"]` |
| Botão Publicar | `[data-testid="tweetButtonInline"]` |

## Erros comuns e soluções

| Erro | Causa | Solução |
|---|---|---|
| `WebSocketBadStatusException: 403` | Origin não permitida | Usar `--remote-allow-origins=*` |
| `Protocol error (Runtime.callFunctionOn): Given expression does not evaluate to a function` | String JS com sintaxe inválida | Usar funções puras JS (`function(){}()`) |
| `Navigation Timeout Exceeded` | `waitUntil='networkidle0'` | Remover `waitUntil`, usar `await asyncio.sleep(4)` |
| `Session closed` / `Target closed` | Comet foi fechado | Verificar processo, reiniciar |
| `Auth_token` não descriptografa | Comet usa prefixo v20 (não v10/v11) | **Não tentar descriptografar** — usar pyppeteer conectado |
