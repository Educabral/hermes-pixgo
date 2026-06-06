---
name: windows-automation
description: "Windows PC automation via git-bash: controlling processes, Notepad, browser tabs, volume, and GUI operations from the Hermes terminal tool. Covers .ps1 workaround patterns, PowerShell via bash, and process management gotchas."
version: 1.0.0
platforms: [windows]
metadata:
  hermes:
    tags: [windows, powershell, automation, gui, notepad, browser]
    related_skills: []
---

# Windows Automation via git-bash

## Context

Hermes runs on Windows via git-bash (MSYS), NOT PowerShell or cmd.exe. This means:
- Native PowerShell syntax (`Get-ChildItem`, `$env:FOO`, pipe operations) does NOT work directly in `terminal()`
- Use `powershell -Command "..."` or `powershell -File "..."` to run PowerShell
- For complex scripts, write `.ps1` files with `write_file()` then execute with `powershell -ExecutionPolicy Bypass -File`

## .ps1 Workaround Pattern (Preferred)

Complex PowerShell actions (SendKeys, WScript.Shell, COM objects) CANNOT be inlined via `powershell -Command` because bash interprets `$`, backticks, and quotes differently. **Always use this pattern:**

```
# 1. Write the .ps1 file to Desktop (or temp location)
write_file(content="""$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate('bloco de notas')
$wshell.SendKeys('texto aqui')
""", path="C:\\Users\\PC\\Desktop\\temp_script.ps1")

# 2. Execute it
terminal("powershell -ExecutionPolicy Bypass -File \"C:\\Users\\PC\\Desktop\\temp_script.ps1\"")

# 3. CLEAN UP — delete the temp file
terminal("rm \"C:\\Users\\PC\\Desktop\\temp_script.ps1\"")
```

**CRITICAL:** Always clean up temp `.ps1` files from the Desktop. The user has complained about desktop clutter before.

## Common Operations

### Notepad Automation

```powershell
$wshell = New-Object -ComObject wscript.shell
$wshell.Run('notepad.exe')
Start-Sleep -Seconds 2
$wshell.AppActivate('bloco de notas')
Start-Sleep -Seconds 1
$wshell.SendKeys('Seu texto aqui')
```

Note: AppActivate uses localized window title. In PT-BR Windows it's 'bloco de notas'.

### Close Notepad (Alt+F4)

```powershell
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate('bloco de notas')
Start-Sleep -Seconds 1
$wshell.SendKeys('%{F4}')
```

### Volume Control

Use WScript.Shell + SendKeys with virtual key codes:
- **Volume Up:** `[char]175` (send 30-50 times for max volume)
- **Volume Down:** `[char]174`
- **Mute:** `[char]173`

```powershell
$wshell = New-Object -ComObject wscript.shell
for ($i = 0; $i -lt 50; $i++) {
    $wshell.SendKeys([char]175)
    Start-Sleep -Milliseconds 50
}
```

### Kill All Browsers

```powershell
Get-Process -Name chrome,comet,msedge,brave,firefox,opera -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Close Specific Browser Tab (Comet Browser via Shell.Application)

The user's default browser is **Comet** (a Chromium-based browser). Use the **Shell.Application** COM object + .ps1 pattern to close specific tabs.

**Approach (use this first — it works):**

```powershell
$shell = New-Object -ComObject Shell.Application
$shell.Windows() | Where-Object { $_.LocationUrl -like '*youtube*' } | ForEach-Object { $_.Quit() }
```

**CRITICAL — git-bash compatibility:** PowerShell pipe operations with `$_` CANNOT be inlined via `powershell -Command` because bash interprets `{`, `}`, and `$` differently. **Always use a .ps1 temp file:**

```
write_file(content="""$shell = New-Object -ComObject Shell.Application
$shell.Windows() | Where-Object { $_.LocationUrl -like '*youtube*' } | ForEach-Object { $_.Quit() }
""", path="C:\\Users\\PC\\kill_tab.ps1")
terminal("powershell -ExecutionPolicy Bypass -File \"C:\\Users\\PC\\kill_tab.ps1\"")
terminal("rm \"C:\\Users\\PC\\kill_tab.ps1\"")  # cleanup
```

**Filter variations:**
- `$_.LocationUrl -like '*youtube*'` — close YouTube tabs only
- `$_.LocationUrl -match 'watch?v=4QgxXHQR5kQ'` — close a specific video
- `$_.LocationUrl -notlike '*youtube*'` — close everything except YouTube
- Omit the filter to see ALL windows: `$shell.Windows() | Select-Object LocationUrl`

**Failsafe:** If no tab matches, `ForEach-Object { $_.Quit() }` does nothing. No harm.

**CRITICAL — Shell.Application tab-close can FAIL SILENTLY:**
Shell.Application's `$_.Quit()` on a single window/tab does NOT reliably close the tab. The method may appear to succeed (exit code 0) while the browser window remains open. This happens because:
- Comet spawns many sub-processes (sometimes 20-30+ `comet.exe` processes) — `Quit()` on one Shell.Application window only closes that window's tab, leaving the browser still running with other windows/tabs
- The Shell.Application COM object may not enumerate all Comet windows

**When the user says the tab/browser "não fechou não" after Shell.Application.Quit():**
1. Verify the process state: `Get-Process "*comet*"` or `Get-Process "*perplexity*"`
2. If processes remain, ask or check: does the user want everything killed (all browser processes), or just that specific tab?
3. For "tudo fechado" (everything closed): `Get-Process "*comet*","*perplexity*" | Stop-Process -Force`
4. For "só aquela aba" (just that tab): try Shell.Application again with a more specific filter, or navigate to youtube.com and stop that page via the browser tool

**When to kill all browsers instead (user says "kill everything"):**
```
Get-Process -Name chrome,comet,msedge,brave,firefox,opera -ErrorAction SilentlyContinue | Stop-Process -Force
```

**What does NOT work:**
- `window.close()` from browser_console — browsers block it for programmatically-opened tabs
- Killing the Comet process for a single tab — kills ALL tabs

## Chrome DevTools Protocol (CDP) — Access Already-Logged-In Pages

When the Comet browser (or any Chrome-based browser) can't log into a service (e.g. Google blocks Comet as "unsafe browser"), use CDP to connect to the **user's real Chrome** running with `--remote-debugging-port=9222`.

### Key concept

The Hermes `browser_navigate` tool uses a **headless** browser — separate from the user's real Chrome. When Google blocks the headless UA for login, piggyback on the real Chrome process via CDP.

### Prerequisites

Chrome must be running with `--remote-debugging-port=9222`. Check:
```bash
netstat -ano | grep 9222
curl -s http://127.0.0.1:9222/json/version
```
→ Extract `webSocketDebuggerUrl` from the version response for browser-level operations.

### Flow: Access Gmail (or any Google service) via CDP

**Step 1 — Check existing tabs for a logged-in session:**
```bash
curl -s http://127.0.0.1:9222/json
```
Look for a target with `url` containing `mail.google.com` and `title` containing "Caixa de entrada" or "Inbox".

**Step 2 — Connect to the tab's websocket debugger:**
```python
import asyncio, json, websockets
async def main():
    ws_url = 'ws://127.0.0.1:9222/devtools/page/<TAB_ID>'
    async with websockets.connect(ws_url) as ws:
        msg = json.dumps({'id': 1, 'method': 'Runtime.evaluate',
            'params': {'expression': 'document.body.innerText.substring(0, 4000)'}
        })
        await ws.send(msg)
        resp = json.loads(await ws.recv())
        text = resp['result']['result']['value']
        print(text)
asyncio.run(main())
```

**Step 3 — Create a new tab via browser-level websocket:**
```python
async with websockets.connect(BROWSER_WS_URL) as ws:
    msg = json.dumps({'id': 1, 'method': 'Target.createTarget',
        'params': {'url': 'https://mail.google.com/mail/u/0/'}
    })
    await ws.send(msg)
    resp = json.loads(await ws.recv())
    tab_id = resp['result']['targetId']
```
Then find the tab via `/json` again to get its `webSocketDebuggerUrl`.

**Step 4 — Search and read emails in Gmail:**
```javascript
// Search
const searchInput = document.querySelector('input[name="q"]');
searchInput.value = 'ifttt';
searchInput.dispatchEvent(new Event('input', {bubbles: true}));
const enterEvent = new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13, bubbles: true});
searchInput.dispatchEvent(enterEvent);

// Click on email row
const rows = document.querySelectorAll('tr[role="checkbox"], tr.zA');
for(const row of rows) {
    if(row.innerText.includes('IFTTT') && row.innerText.includes('reset')) {
        row.click(); break;
    }
}

// Read email body
document.querySelector('.a3s.aiL')?.innerText
```

### ⚠️ CDP gotchas

- **Browser WS endpoint changes on Chrome restart.** Always check `/json/version` fresh each session.
- **`Target.createTarget` does NOT return a `webSocketDebuggerUrl`.** Poll `/json` afterward.
- **`/json/new?<url>` is deprecated** — returns 405. Use `Target.createTarget` over WebSocket.
- **Page needs time to load** — add `await asyncio.sleep(3-5)` after navigation.
- **Gmail DOM is complex** — `querySelector('tr.zA')` works for email rows but only after search.

**Detection:** The browser tool Hermes uses (browser_navigate) often runs in a HEADLESS browser, NOT the user's visible Comet window. They are SEPARATE things. YouTube audio only works in the visible Comet, not the headless one.

### Open URL in Comet Browser

The user's default browser is **Comet** (Perplexity Comet, Chromium-based). Two approaches:

**Try first (simpler):**
```powershell
Start-Process 'https://example.com'
```
This opens in the default browser. Works if Comet is registered as the default handler.

**Fallback explicit path (when simpler fails):**
```powershell
Start-Process 'C:\Program Files\Perplexity\Comet\Application\comet.exe' -ArgumentList 'https://example.com'
```

**Discovery:** If Comet's path is unknown, search with:
```
find /c/Program\ Files/ -name "Comet*" 2>/dev/null
find /c/ -maxdepth 3 -name "*comet*" -type f 2>/dev/null | head -10
```
Typical found path: `C:\Program Files\Perplexity\Comet\Application\comet.exe`

**CRITICAL — YouTube audio:**
YouTube does NOT play audio in headless browser sessions. Always open YouTube via `Start-Process` in the real visible Comet when the user wants to hear audio.

## Pitfalls

### ❌ Do NOT inline SendKeys/Script via -Command
```powershell
# WRONG — bash breaks $ variables and quotes
powershell -Command "$wshell = New-Object ..."
```
Always use the `write_file` + `-File` pattern instead.

### ❌ Do NOT close the whole browser when user says "close tab"
Confirm with the user before killing all browser processes. Ask which browser and whether they want just one tab or everything killed.

### ❌ Do NOT leave temp files on Desktop
The user explicitly complained about desktop clutter from temp scripts. Always clean up with `rm` after execution.

### ❌ Do NOT use PowerShell built-in pipe filtering with `$_` in inline -Command
Operations like `Where-Object { $_ }` break in bash. Use the .ps1 file pattern for anything non-trivial.

### 🐞 git-bash `$_` Quirk — Bash Interprets `$_` as `C:\\Users\\PC`

When running `powershell -Command` from git-bash, the `$_` variable inside PowerShell pipeline expressions gets **intercepted by bash** and expanded to the current user's home path (e.g., `C:\\Users\\PC`). This produces errors like:

```
ForEach-Object { C:\\Users\\PC.Quit() }
                     ~
Uma expressão era esperada após '('.
```

**This affects ALL PowerShell inline commands with `$_` in pipeline blocks**, not just Shell.Application patterns.

**Workaround:** Always use the `.ps1` file pattern (write_file + powershell -File) for any command containing `$_`, `$_.Property`, or `ForEach-Object { ... }`. Do NOT attempt to escape `$_` with backticks or single quotes — it doesn't work reliably.

**Exception:** Simple `Select-Object` or `Format-Table` calls without `{ }` blocks sometimes work if the `$_` is absent. But when in doubt, write the `.ps1` file.

### 🐞 git-bash `=` Quirk — Bash Interprets `=` After Key as Redirect

When running commands with `=` in values (e.g. API keys, tokens), MSYS bash interprets `=value` after certain tokens as a **redirection operator**, eating part of the string:

```bash
# WRONG — bash eats everything after = in the value
hermes config set auxiliary.vision.api_key "AIzaSy...OlhI"
# Result: api_key: AIzaSy...OlhI  (truncated at =)
```

This happens because MSYS converts `=DQoG...` to a Windows path-like string and the `hermes config set` CLI receives truncated input. This affects:
- `hermes config set` with `=` in the value
- `curl -d '{"key":"value"}'` with `=` in JSON values
- Any command line where `=` follows certain patterns

**Workaround — use Python to wrap the command:**

```bash
python -c "import os; os.system('hermes config set auxiliary.vision.api_key AIzaSy...OlhI')"
```

Python's `os.system()` doesn't go through MSYS path translation, so the `=` sign survives intact.

**Alternative — write a .py helper script** (when the command is complex):
1. Write a small Python script with `write_file()`
2. Run it with `python /path/to/script.py`
3. Clean up

**Pro tip for API keys:** When a key contains `=` followed by alphanumerics, ALWAYS use the Python wrapper to avoid MSYS shell mangling. Verify with `grep -n 'api_key:' /path/to/config.yaml` after setting.

- **Use the explicit Comet path** when `Start-Process 'https://...'` fails (Comet not registered as default handler). Command: `powershell -Command "Start-Process 'C:\Program Files\Perplexity\Comet\Application\comet.exe' -ArgumentList 'URL'"`
  YouTube doesn't play audio in headless browser sessions. Always open via `Start-Process` in the real browser if the user wants to hear it.

## Volume Calibration

Based on real-world testing on this Windows machine:
- **~50 `[char]175` sends** (with 50ms delay) brings volume from 0 to ~100%
- **~25 `[char]174` sends** (with 30ms delay) brings volume from 100% down to ~50%
- Each send = roughly 2% volume change
- Start from a known baseline (mute first, then unmute with `[char]173`) for consistent results
- Always include `Start-Sleep -Milliseconds 50` between sends to avoid key-press loss

## Relationship with `windows-pc-control`

There are TWO Windows automation skills that overlap:
- **`windows-automation`** (devops/) — more comprehensive, covers SendKeys, process management, .ps1 patterns, browser handling, Notepad, YouTube audio, volume calibration
- **`windows-pc-control`** (productivity/) — Portuguese-medium skill with similar content

**Prefer `windows-automation`** for any new work — it's richer and covers more edge cases. The `windows-pc-control` skill is a PT-BR parallel version. When patching, update both if the change affects core patterns; update just this one for English-medium additions.

After running any automation:
1. Visually confirm the action happened (user will tell you if it didn't)
2. Clean up temp files
3. Don't assume `CloseMainWindow()` worked — check with `Get-Process` if unsure
