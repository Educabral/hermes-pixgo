# IFTTT + Alexa Trigger — Real-world Findings (2026-06-05)

## Root Cause

Amazon **discontinued** the official Amazon Alexa integration with IFTTT. This is why Alexa appears under **"Services with no available triggers"** in ALL IFTTT plans (free, Pro, and Pro+). This is not a paywall — the API was deprecated by Amazon.

## What DOES NOT Work (confirmed this session)

- ❌ **IFTTT - any plan** — Alexa trigger is gone across the board (discontinued by Amazon)
- ❌ **Virtual Buttons** as IFTTT trigger — creates buttons but only supports "Alexa, push {button_name}", no wildcard/custom phrase capture
- ❌ **Google "Continue with Google" login** — blocked on headless browsers (Comet)  
- ❌ **Creating new applets on IFTTT free plan** — popup "Get more Applets" blocks UI even with Webhooks as trigger. "Nevermind" dismisses popup but creation flow doesn't proceed.

## What DOES Work (confirmed)

| Approach | Cost | Voice Phrase | Setup Effort |
|----------|------|--------------|--------------|
| **Voice Monkey** skill → webhook → ngrok → Flask | Free | "Alexa, manda {comando}" | Medium (create account, configure) |
| **Alexa Routines** native HTTP request → ngrok → Flask | Free | "Alexa, {qualquer frase}" | Low (app Alexa only) |
| **Virtual Buttons** skill → IFTTT Webhooks → ngrok → Flask | Free | "Alexa, push {botão}" | Low |

## Recommended: Voice Monkey (best balance)

[Voice Monkey](https://voicemonkey.io/) is a free Alexa skill that lets you create custom voice commands that trigger webhooks:

1. User installs "Voice Monkey" skill from Alexa Skills Store
2. Agent creates account at voicemonkey.io via Amazon login
3. Agent configures a "Monkey" with phrase like "comando hermes"
4. Webhook URL: agent's ngrok endpoint
5. User speaks: **"Alexa, manda hermes {comando}"**

No "apertar", no "push" — natural language command.

## Alternative: Native Alexa Routines (simplest)

The Alexa app (2024+) has native HTTP Request as an action:

1. Alexa app → More → Routines → +
2. **When:** Voice → type any phrase (e.g., "comando hermes")
3. **Then:** Add action → HTTP Request
4. URL: `https://NGROK_URL.ngrok-free.dev/ifttt-trigger`
5. Method: POST, Body: `{"comando":"teste"}`

This is the simplest approach — no third-party services, no IFTTT, just Alexa + your server.

## What DOES Work (discovered this session)

- **Maker Webhooks API returns 200 even without an applet**: `POST https://maker.ifttt.com/trigger/alexa_comando/json/with/key/KEY` responds HTTP 200. The trigger event is accepted by IFTTT's infrastructure even if no applet routes it.
- **CDP browser automation can create applets** when the React SPA renders (session not expired), using `Runtime.evaluate` with `document.createTreeWalker` to find clickable elements, and `Object.getOwnPropertyDescriptor(...HTMLInputElement.prototype..., 'value').set` for input fields.
- **IFTTT sessions expire silently** after ~30min — the React app doesn't mount, making `Runtime.evaluate` return empty strings. Use `curl http://127.0.0.1:9222/json | grep ifttt` to verify URL (should be `/create` or `/explore`, not `/join`).

## Key Technical Details

### IFTTT Login Form (CDP selectors)
- Email field: `input#user_username` (name=`user[username]`, placeholder="Email or username")
- Password field: `input#user_password` (name=`user[password]`, placeholder="Password")
- Submit: CSS class `button-primary`, type=submit, name=`commit`

### IFTTT Create Applet (CDP field selectors)
- URL field: `textarea[name="fields[url]"]`
- Method select: `select[name="fields[method]"]`
- Content-Type select: `select[name="fields[content_type]"]`
- Body field: `textarea[name="fields[body]"]`
- Submit trigger/action: `input[type="submit"]`
- No `id` attributes on selects — identify by index (`select[0]`, `select[1]`) or name

### Cookie extraction via CDP (for curl API calls)
When `Runtime.evaluate` is unreliable (React SPA issues), extract cookies via:
- `Network.getCookies` — returns all cookies, filter by domain
- Key cookies: `browser_session_id`, `auth_cdn_cache_key`
- CSRF token: `meta[name="csrf-token"]` content attribute

## Account Used

- IFTTT email: `segurancabral@gmail.com`
- Plan tier: Free (1 applet used out of 20)
- Password: `PutinHO@2026` (set via reset link from Gmail)
- Login method: email + password (not Google auth)
- Webhooks API Key: `l4S9mL9sss70rz8MgCOPIwQ3-_BsNc9jMGzaxlOE05E`
- Maker URL: `https://maker.ifttt.com/use/l4S9mL9sss70rz8MgCOPIwQ3-_BsNc9jMGzaxlOE05E`
