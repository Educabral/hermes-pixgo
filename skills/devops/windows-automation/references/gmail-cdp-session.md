# Gmail CDP Session — Real-world Working Pattern

## Problem

Google blocks the Comet browser (Perplexity's Chromium) during login: *"Esse navegador ou app pode não ser seguro"*. The Hermes `browser_navigate` tool runs in a headless instance which Google also doesn't trust.

## Solution

The user's real Chrome (running with `--remote-debugging-port=9222`) has an active Google session. Connect via Chrome DevTools Protocol to bypass the login entirely.

## Working Commands

### 1. Check Chrome CDP is alive

```bash
netstat -ano | grep 9222
curl -s http://127.0.0.1:9222/json/version
```

Returns `webSocketDebuggerUrl` — this CHANGES on every Chrome restart. In this session:
- Old: `ws://127.0.0.1:9222/devtools/browser/8dd30e42-b15e-4187-b7f7-b2f5c26a5892`
- New (after restart): `ws://127.0.0.1:9222/devtools/browser/0ac87ecc-8757-40b0-81dd-281164542c67`

### 2. List all open tabs (including Gmail)

```bash
curl -s http://127.0.0.1:9222/json
```

Look for: `"url": "https://mail.google.com/mail/u/0/#inbox"` and `"title": "Caixa de entrada (88) - segurancabral@gmail.com - Gmail"`

### 3. Check if the user had multiple Gmail tabs

Multiple tabs were found (likely from multiple `Target.createTarget` attempts in earlier tool calls):
- `02D04C1DA4974992C85B3887BA44A27C` → inbox (88 messages)
- `1F60B9A695E686C5F1CD6C6FBF7FB119` → inbox (same)
- `35A2713CF98018603033B5788D5F25A0` → inbox (same)
- `A5C2D855A552BFC52430238CCD60EEA2` → `RotateCookiesPage` (Google cookie refresh)

### 4. Read Gmail inbox via Python + websockets

```python
import asyncio, json, websockets

async def main():
    ws_url = 'ws://127.0.0.1:9222/devtools/page/02D04C1DA4974992C85B3887BA44A27C'
    async with websockets.connect(ws_url) as ws:
        msg = json.dumps({'id': 1, 'method': 'Runtime.evaluate',
            'params': {'expression': 'document.body.innerText.substring(0, 4000)'}
        })
        await ws.send(msg)
        resp = json.loads(await ws.recv())
        print(resp['result']['result']['value'])
asyncio.run(main())
```

### 5. Search for emails

```javascript
const searchInput = document.querySelector('input[name="q"]');
searchInput.value = 'ifttt';
searchInput.dispatchEvent(new Event('input', {bubbles: true}));
const enterEvent = new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13, bubbles: true});
searchInput.dispatchEvent(enterEvent);
```

Then wait 3-4 seconds and re-read `document.body.innerText`.

### 6. Click an email to open it

```javascript
const rows = document.querySelectorAll('tr[role="checkbox"], tr.zA');
for(const row of rows) {
    if(row.innerText.includes('IFTTT') && row.innerText.includes('reset')) {
        row.click(); break;
    }
}
```

### 7. Extract email body

```javascript
document.querySelector('.a3s.aiL')?.innerText
```

Or get all `<a>` links from the email for password reset URLs:
```javascript
document.querySelectorAll('a').forEach(a => {
    if(a.textContent.toLowerCase().includes('reset')) console.log(a.href);
});
```

## IFTTT Login Form Details

Found via CDP on the user's Chrome (logged into `segurancabral@gmail.com`):

| Field | Selector | Attributes |
|-------|----------|------------|
| Email | `input#user_username` | name=`user[username]`, placeholder="Email or username" |
| Password | `input#user_password` | name=`user[password]`, placeholder="Password" |
| Submit | `button-primary` class | type=submit, name=`commit` |

The Google "Continue with Google" button opens a popup via IFRAME and is blocked in Comet. Email/password login works directly.

## Email Found in Gmail for IFTTT

Two relevant emails at the IFTTT account `segurancabral@gmail.com`:

1. **"Reset your password"** (23:37) — contains a tracking link via `links.ifttt.com/ls/click?upn=...` wrapping `https://ifttt.com/password_resets/...`
2. **"Your password has been set"** (23:32) — confirms password was successfully set

## Pitfalls Encountered

- `pyppeteer.connect()` with `browserWSEndpoint` can timeout (300s) if the browser is busy
- `asyncio` scripts need short timeouts — use `terminal()` with timeout=20-25s, not execute_code
- The `websockets` package needs to be installed in the venv
- Gmail rows `tr.zA` and `tr[role="checkbox"]` may be empty if the page is in a loading/searching state
- `Runtime.evaluate` with complex JS that uses template literals inside nested functions is fragile with escaping — use `JSON.stringify()` in JS, not in Python
