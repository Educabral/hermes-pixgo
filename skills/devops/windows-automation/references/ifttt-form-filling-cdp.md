# IFTTT Applet Form-Filling via Chrome CDP

## Problem

Creating IFTTT Applets programmatically via `browser_navigate` is unreliable because:
- The Hermes browser tool runs headless — Google blocks it for auth
- IFTTT's SPA creates/destroys form fields dynamically based on user interaction
- The "Continue" button may be disabled until all required fields are filled

## Solution

Use raw Chrome DevTools Protocol websockets via the **user's real Chrome** (running with `--remote-debugging-port=9222`) to fill IFTTT forms directly with `Runtime.evaluate`.

## Check Chrome CDP is Alive

```bash
curl -s http://127.0.0.1:9222/json/version
```

Extract `webSocketDebuggerUrl` — it **changes every Chrome restart**. Don't hardcode it.

## Create a New Tab for IFTTT

```python
import asyncio, json, websockets

async def main():
    # Connect at browser level to create a tab
    ws_url = 'ws://127.0.0.1:9222/devtools/browser/<BROWSER_ID>'  # from /json/version
    async with websockets.connect(ws_url) as ws:
        msg = json.dumps({'id': 1, 'method': 'Target.createTarget',
            'params': {'url': 'https://ifttt.com/login'}
        })
        await ws.send(msg)
        resp = json.loads(await ws.recv())
        tab_id = resp['result']['targetId']
    
    # Get the tab's page-level websocket URL via /json
    import urllib.request
    with urllib.request.urlopen('http://127.0.0.1:9222/json') as r:
        targets = json.loads(r.read())
    our_tab = next(t for t in targets if t['id'] == tab_id)
    page_ws_url = our_tab['webSocketDebuggerUrl']
    
    # Now connect at page level
    async with websockets.connect(page_ws_url) as page:
        # ... interact with page ...
```

**Key:** `Target.createTarget` does NOT return `webSocketDebuggerUrl`. Poll `/json` afterward.

## IFTTT Login Form

| Field | Selector | Value |
|-------|----------|-------|
| Email | `input#user_username` | `segurancabral@gmail.com` |
| Password | `input#user_password` | user-provided |
| Submit | `input[type="submit"].button-primary` | — |

## IFTTT Create Flow — Step by Step

### Step 1: Go to Create page
```
Page.navigate → https://ifttt.com/create
```
Wait 5 seconds for the SPA to initialize.

### Step 2: Click "Add" in "If This" section
```javascript
const btns = document.querySelectorAll('button');
for(const b of btns) {
    if(b.textContent.trim() === 'Add') { b.click(); break; }
}
```

### Step 3: Search for a service
Type "Webhooks" or "Alexa" into the search input:
```javascript
const search = document.querySelector('input[placeholder*="Search"]');
const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
nativeSetter.call(search, 'Webhooks');
search.dispatchEvent(new Event('input', {bubbles: true}));
search.dispatchEvent(new Event('change', {bubbles: true}));
```

### Step 4: Click the service link (Tree Walker Pattern — Reliable for React SPAs)

IFTTT renders service links as `<a>` tags inside complex DOM hierarchies. Use a **tree walker** to find text, then walk up to find the clickable `<a>`:

```javascript
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
let node;
while(node = walker.nextNode()) {
    if(node.textContent?.trim() === 'Webhooks') {
        let parent = node.parentElement;
        for(let i = 0; i < 5 && parent; i++) {
            if(parent.tagName === 'A') {
                parent.click();
                break;
            }
            parent = parent.parentElement;
        }
        break;
    }
}
```

This works for all IFTTT service/trigger/action selection lists.

### Step 5: Select "Receive a web request with a JSON payload"

Same tree walker pattern, searching for text `'JSON payload'`.

### Step 6: Fill Event Name

```javascript
const input = document.querySelector('input');
const ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
ns.call(input, 'alexa_comando');
input.dispatchEvent(new Event('input', {bubbles: true}));
input.dispatchEvent(new Event('change', {bubbles: true}));
```

### Step 7: Create Trigger

```javascript
document.querySelector('input[type="submit"]')?.click();
```

### Step 8: Click "Add" in "Then That" section

Same as Step 2.

### Step 9: Select "Make a web request" action

Tree walker for `'Make a web request'`.

### Step 10: Fill Action Fields

**Verified IFTTT action form field names:**

| Field | Selector Pattern | Value |
|-------|-----------------|-------|
| URL | `textarea[name="fields[url]"]` | `https://your-ngrok-url.ngrok-free.dev/ifttt-trigger` |
| Method | `select[name="fields[method]"]` | `'POST'` |
| Content Type | `select[name="fields[content_type]"]` | `'application/json'` |
| Body | `textarea[name="fields[body]"]` | `'{"comando":"{{EventName}}"}'` |

**VERIFIED WORKING CODE (from this session):**

```javascript
// URL
const tas = document.querySelectorAll('textarea');
for(const t of tas) {
    if(t.name === 'fields[url]') {
        t.value = 'https://badness-unafraid-antiques.ngrok-free.dev/ifttt-trigger';
        t.dispatchEvent(new Event('input', {bubbles: true}));
        t.dispatchEvent(new Event('change', {bubbles: true}));
    }
}

// Method
const ss = document.querySelectorAll('select');
ss[0].value = 'POST';
ss[0].dispatchEvent(new Event('change', {bubbles: true}));

// Content-Type
ss[1].value = 'application/json';
ss[1].dispatchEvent(new Event('change', {bubbles: true}));

// Body
for(const t of document.querySelectorAll('textarea')) {
    if(t.name === 'fields[body]') {
        t.value = '{"comando":"{{EventName}}"}';
        t.dispatchEvent(new Event('input', {bubbles: true}));
        t.dispatchEvent(new Event('change', {bubbles: true}));
    }
}
```

### Step 11: Create Action

```javascript
document.querySelector('input[type="submit"]')?.click();
```

### Step 12: Click "Continue" or "Finish"

```javascript
const btns = document.querySelectorAll('button');
for(const b of btns) {
    if(b.textContent.trim() === 'Continue') { b.click(); break; }
}
```

## IFTTT Webhooks API Key

Found at `https://ifttt.com/maker_webhooks/settings`:

- **URL:** `https://maker.ifttt.com/use/<API_KEY>`
- **Webhook trigger format:** `https://maker.ifttt.com/trigger/<EVENT_NAME>/json/with/key/<API_KEY>`

### Verified in this session:
- API Key: `l4S9mL9sss70rz8MgCOPIwQ3-_BsNc9jMGzaxlOE05E`
- Event Name: `alexa_comando`
- Trigger URL: `https://maker.ifttt.com/trigger/alexa_comando/json/with/key/l4S9mL9sss70rz8MgCOPIwQ3-_BsNc9jMGzaxlOE05E`

## Pitfalls

### ❌ "Continue" doesn't advance
If Continue is clicked but the page doesn't change, a **required field is missing or invalid**:
- URL must be a valid HTTPS URL (not empty, not placeholder)
- Method must not be "GET" if you want POST
- Body and Content-Type are required for JSON payload
- Use `Runtime.evaluate` to inspect `document.querySelectorAll('input, textarea, select')` and check each field's `value`

### ❌ Native input setter vs standard value assignment
React/SPA apps (like IFTTT) ignore standard `input.value = '...'`. Always use:
```javascript
const ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
// or for textarea:
const ns = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
ns.call(element, 'new value');
element.dispatchEvent(new Event('input', {bubbles: true}));
element.dispatchEvent(new Event('change', {bubbles: true}));
```

### ❌ Tree walker finds text, not clickable elements
The tree walker finds text nodes. You MUST walk up to a parent `<a>` or `<button>` tag before calling `.click()`. Walking more than 5 levels suggests you're in the wrong subtree.

### ❌ Upgrade popup blocks flow
IFTTT's free tier shows "Get more Applets" / "Upgrade to Pro+" popups when adding triggers/actions. Dismiss with clicking "Nevermind":
```javascript
const btns = document.querySelectorAll('button');
for(const b of btns) {
    if(b.textContent.trim() === 'Nevermind') { b.click(); break; }
}
```

### ❌ Progress lost on page reload
Navigating away from the Create page (even using `history.back()` or `location.href`) resets the SPA state — all field progress is lost. Use `Page.navigate` with the recommended_services URL to get back to a fresh state: `https://ifttt.com/create?recommended_services=maker_webhooks`

## Verification: Checking if an Applet Exists

Navigate to `https://ifttt.com/home` and check for "My Applets" section. The Applet count ("You're using 1 of 20 Applets") shows on the Create page.
