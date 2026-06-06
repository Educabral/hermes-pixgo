# Comet Browser Flow — YouTube 🐓🎵

## Real-world session history (confirmed working)

### Opening YouTube in Comet

The Comet executable lives at:
```
C:\Program Files\Perplexity\Comet\Application\comet.exe
```

Command to open YouTube in the user's visible Comet window:
```bash
powershell -Command "Start-Process 'C:\Program Files\Perplexity\Comet\Application\comet.exe' -ArgumentList 'https://www.youtube.com'"
```

### Searching for a video

browser_navigate loads the page, browser_type types the query, browser_press Enter submits. The search results page loads with YouTube's full UI (tabs, results, sidebar).

### Playing a video

The Hermes browser_navigate loads the YouTube video page, but the autoplay is blocked in headless/stealth mode. The player shows a "Reproduzir" button instead of auto-playing.

**To actually play:** navigate to the video URL, then click the play button (ref=e42 or similar — varies by session) via browser_click. After clicking, the button changes from "Reproduzir" to "Pausa (k)" and the progress slider starts ticking (0:02 / 0:33).

### Finding video IDs from search results

When browser_snapshot doesn't show clickable video links, use browser_console to extract them programmatically:

```javascript
// Get all video links with titles containing keywords
document.querySelectorAll('a[href*="/watch?"]').forEach(a => {
  const title = a.title || a.innerText;
  const href = a.href.split('&')[0];  // strip tracking params
  if (title.includes('Despertador') || title.includes('galo'))
    console.log({title: title.substring(0,60), href});
});
```

Then navigate directly: `browser_navigate(url="https://www.youtube.com/watch?v=VIDEO_ID")`

### Closing a specific YouTube tab

Use Shell.Application COM object via a .ps1 temp file. The PowerShell pipe with Where-Object { $_.LocationUrl } breaks if inlined in bash.

Write this .ps1:
```powershell
$shell = New-Object -ComObject Shell.Application
$shell.Windows() | Where-Object { $_.LocationUrl -like '*youtube*' } | ForEach-Object { $_.Quit() }
```

Execute:
```bash
powershell -ExecutionPolicy Bypass -File "C:\Users\PC\kill_tab.ps1"
```

Cleanup:
```bash
rm "C:\Users\PC\kill_tab.ps1"
```

### ⚠️ Shell.Application.Quit() can fail silently — kills-all fallback

If the user says "não fechou não" after the tab-close command:

1. **Check what's still running:**
   Write+execute a check script:
   ```powershell
   Get-Process "*comet*" -ErrorAction SilentlyContinue | Format-Table Id, ProcessName, MainWindowTitle
   Get-Process "*perplexity*" -ErrorAction SilentlyContinue | Format-Table Id, ProcessName, MainWindowTitle
   ```

2. **Kill all Comet + Perplexity processes** (when user wants everything closed):
   ```powershell
   Get-Process "*comet*" -ErrorAction SilentlyContinue | Stop-Process -Force
   Get-Process "*perplexity*" -ErrorAction SilentlyContinue | Stop-Process -Force
   ```

3. **Verify nothing remains:** re-run the check script — empty output = done.

**Why this happens:** Comet spawns 20-30+ sub-processes. Shell.Application's `$_.Quit()` only closes one window's tab — the browser keeps running with other windows/tabs. The only reliable way to fully kill the browser is process-level termination.

### Key gotchas
- YouTube autoplay is blocked in headless mode — always need a manual click on the play button
- The headless Hermes browser (browser_navigate) is DIFFERENT from the visible Comet on the user's desktop
- Wait for the video page to fully load (browser_navigate returns snapshot) before clicking play
- The video page snapshot shows 0:00 / 0:33 before play, then 0:02 / 0:33 after clicking play (confirms playback started)
- Finding video links: browser_console with JS DOM queries works when browser_snapshot is unresponsive
- Always clean up .ps1 temp files after use — user hates desktop clutter
