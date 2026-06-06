# Automação Hostinger Webmail via pyppeteer + Chrome CDP

## Contexto

O Hostinger Webmail (mail.hostinger.com) é um SPA React que carrega e-mails em um layout split-view. A resposta ao e-mail é feita num **iframe TinyMCE** (iframe #1). Automatizar isso requer etapas específicas.

## Pré-requisitos

- Chrome do usuário aberto com debug na porta 9222
- Usuário já logado no Hostinger Webmail
- pyppeteer instalado no venv do Hermes

## Fluxo de Resposta

### 1. Criar/Encontrar a aba do Hostinger

```python
import asyncio
from pyppeteer import connect

# Opção A: Criar nova aba no Chrome do usuário
import requests
resp = requests.put('http://127.0.0.1:9222/json/new?https://mail.hostinger.com/mailboxes/INBOX')
tab_id = resp.json()['id']

# Opção B: Encontrar aba existente
browser = await connect(browserURL='http://127.0.0.1:9222')
pages = await browser.pages()
target = None
for p in pages:
    if 'hostinger' in p.url and 'INBOX' in p.url:
        target = p
        break
```

### 2. Clicar no E-mail Desejado

Use XPath para encontrar o e-mail pelo número do pedido:

```python
await target.evaluate("""
    () => {
        const xpath = "//*[contains(text(), '019e707a')]";
        const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        if (result.singleNodeValue) result.singleNodeValue.click();
    }
""")
await asyncio.sleep(3)
```

### 3. Clicar em "Responder"

Busque pelo texto ou aria-label:

```python
await target.evaluate("""
    () => {
        const items = document.querySelectorAll('button, [role=button], span, a');
        for (let el of items) {
            let t = (el.textContent || '').trim();
            let aria = (el.getAttribute('aria-label') || '');
            if (el.offsetParent !== null && (t === 'Responder' || aria === 'Responder')) {
                el.click();
                return;
            }
        }
    }
""")
await asyncio.sleep(3)
```

### 4. Encontrar o Iframe Editor

Após clicar "Responder", o Hostinger abre um iframe TinyMCE. Identifique-o como o iframe #1 (índice 1):

```python
iframes = await target.querySelectorAll('iframe')
for i, f in enumerate(iframes):
    frame = await f.contentFrame()
    if frame:
        content = await frame.evaluate('() => document.body.innerText')
        # Iframe #1 geralmente contém "Equipe PixGo" + assinatura quando vazio
        if i == 1 or ('Equipe PixGo' in content and len(content.strip()) < 30):
            # This is the editor!
```

### 5. Injetar o Texto da Resposta

Use `innerText` no iframe (não innerHTML - TinyMCE interpreta innerText como texto puro):

```python
# Escapar quebras de linha e aspas simples
escaped = RESPONSE_TEXT.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
await frame.evaluate(f"() => {{ document.body.innerText = '{escaped}'; }}")
```

### 6. Clicar em "Enviar"

```python
await target.evaluate("""
    () => {
        const all = document.querySelectorAll('button');
        for (let el of all) {
            let t = (el.textContent || '').trim();
            if (el.offsetParent !== null && t === 'Enviar') {
                el.click();
                return;
            }
        }
    }
""")
```

### 7. Confirmar Envio

Verifique se o e-mail apareceu na lista como "Re: [assunto original]" com o remetente `noreply@pixgo.me`.

## Pitfalls

1. **Cross-origin iframe**: O iframe #0 contém o corpo do e-mail original (pode ser cross-origin). Use iframe #1.

2. **innerText vs innerHTML**: TinyMCE do Hostinger só aceita texto via `innerText`. Se usar `innerHTML` os elementos HTML aparecem como texto literal.

3. **Scroll para carregar e-mails**: A lista de e-mails carrega sob demanda. Role o container (não o window) para carregar mais:

```python
await target.evaluate("""
    () => {
        const containers = document.querySelectorAll('[class*=scroll], [class*=list]');
        for (let c of containers) {
            if (c.scrollHeight > c.clientHeight) {
                c.scrollTop = c.scrollHeight;
                return;
            }
        }
    }
""")
```

4. **Elemento em (0,0)**: Não clicar em elementos com bounding rect em (0,0) — são elementos do DOM invisíveis/offscreen.

5. **SPA routing**: O Hostinger redireciona URLs como `/mailboxes/INBOX/6955` de volta para `/mailboxes/INBOX`. A navegação é client-side.

6. **Sem visão funcional**: Se `browser_vision` estiver quebrado, a automação via navegador fica extremamente frágil. Considere Himalaya CLI como alternativa.
