---
name: user-image-help
description: "Handle user-shared images (screenshots of errors, code, UI) when the active model has no vision capability. Systematic fallback strategies: OCR, browser workarounds, and asking the user to describe."
version: 1.0.0
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [images, screenshots, debugging, user-support, ocr, error-help]
    related_skills: [systematic-debugging, ocr-and-documents]
---

# User Image Help — Visionless Workflow

## Overview

When the user shares an image (screenshot of an error, code, UI, configuration, etc.) but the active model does NOT support vision/image_url, you need a fallback strategy. **Do not flail through multiple failing approaches.** Follow this ordered workflow.

## Symptom: Model Rejects Vision

If `browser_vision` (or any vision tool) fails with:

```
unknown variant `image_url`, expected `text`
```

The model does NOT support vision. Stop trying. Proceed with the workflow below.

If `browser_vision` fails with:

```
Gemini HTTP 400 (INVALID_ARGUMENT): API key not valid
```

The model itself doesn't support vision, but the auxiliary vision backend (Gemini) IS configured — with an invalid or missing API key. See **Phase 0: Check Vision Config** below.

## Phased Workflow

### Phase 0: Check Vision Config (NEW — do this FIRST if vision errors mention API keys)

Before trying OCR or anything else, check whether the auxiliary vision backend is properly configured. This is the #1 reason vision silently fails on Gemini+non-vision-model setups:

```python
from hermes_tools import terminal
result = terminal("cat ~/AppData/Local/hermes/config.yaml | grep -A 10 \"auxiliary:\\n  vision:\"")
# Check if api_key is empty ('') and if provider matches a configured key
```

The config flow is:
1. `auxiliary.vision.provider` determines the backend (gemini, openrouter, etc.)
2. `auxiliary.vision.model` sets the model name (e.g. gemini-2.5-flash, gemini-1.5-flash)
3. `auxiliary.vision.api_key` can be set directly in config.yaml. If empty (`''`), the system looks for `GOOGLE_API_KEY` or `GEMINI_API_KEY` in the `.env` file.

**Common failure: api_key is `''` in config.yaml AND the `.env` variable is commented out or missing.**

```bash
# Check .env
grep -i "GEMINI\|GOOGLE" ~/AppData/Local/hermes/.env
```

Fix:
```bash
# Option A: Set in .env
echo 'GOOGLE_API_KEY=your_key_here' >> ~/AppData/Local/hermes/.env

# Option B: Set in config.yaml
hermes config set auxiliary.vision.api_key your_key_here
```

After setting the key, restart the agent (`/reset` in CLI, or `/restart` in gateway).

**Also check: does the Gemini API key have vision-enabled model access?** Gemini 1.5 Flash and 2.0 Flash support vision. If the key only enables the base Gemini model (text-only), vision calls still fail.

### Phase 1: Check Available Tools First (30 seconds)

Before attempting anything:

```python
# Check what's available
import shutil
ocrtools = {
    "tesseract": shutil.which("tesseract"),
    "easyocr": shutil.which("easyocr") or __import__("pkg_resources", ...).get_distribution("easyocr"),
}
```

- **If tesseract is installed**: go to Phase 2a (local OCR)
- **If easyocr is installed**: go to Phase 2a (local OCR, better for Portuguese)
- **If neither**: go to Phase 2b (browser screenshot + browser_vision) or Phase 3 (ask user)

> **Pro tip on Windows**: `python3` often points to the MS Store redirect. Use the full path:
> ```
> C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe
> ```
> Or the venv Python at:
> ```
> /c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/python
> ```

### Phase 2a: Local OCR (fast, private)

Use `pytesseract` if tesseract is installed:

```python
from PIL import Image
import pytesseract

img = Image.open(r"C:\path\to\image.jpg")
text = pytesseract.image_to_string(img, lang="por+eng")
print(text)
```

For easyocr (better accuracy, handles Portuguese well):

```python
import easyocr
reader = easyocr.Reader(["pt", "en"])
results = reader.readtext(r"C:\path\to\image.jpg")
for bbox, text, conf in results:
    print(f"[{conf:.2f}] {text}")
```

### Phase 2b: Browser Screenshot + Vision (if model supports it)

**Only try this if you haven't already confirmed the model doesn't support vision!**

If unsure, try a quick test:

```bash
browser_vision(question="Describe this image briefly")
```

If it fails with `unknown variant 'image_url'` — model has NO vision support. Skip to Phase 3.

### Phase 2c: Local HTTP Server + Browser (WINDOWS fallback)

If the image is a JPEG/PNG on disk and you want to see it in the browser:

```python
import http.server, socketserver, os

PORT = 18767  # use a unique port

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/img':
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            fsize = os.path.getsize(r'C:\path\to\image.jpg')
            self.send_header('Content-Length', str(fsize))
            self.end_headers()
            with open(r'C:\path\to\image.jpg', 'rb') as f:
                self.copyfile(f, self.wfile)
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body style="background:#111"><img src="/img" style="max-width:100%"></body></html>')
    def log_message(self, fmt, *args): pass

httpd = socketserver.TCPServer(('0.0.0.0', PORT), Handler)
httpd.serve_forever()
```

Then navigate to `http://127.0.0.1:PORT/` in the browser tool.

**Important**: This only helps if the model supports vision (browser_vision) — it just lets you view the image. If vision is not supported, this approach also fails.

### Phase 3: Ask the User (ultimate fallback)

When OCR and vision both fail, ask the user **directly** to describe the image:

> "Infelizmente meu modelo atual não suporta visão para ler imagens. Pode me descrever o que está aparecendo nela? Ou colar o texto do erro aqui?"

**Be specific in what you need:**
- If it looks like an error: ask for the full error message text
- If it's code: ask them to paste the code
- If it's a UI: ask what they were doing when it happened

### Phase 4: Debugging After Getting Text

Once you have the error/text, load the `systematic-debugging` skill and follow its 4-phase approach:
1. Root cause investigation
2. Pattern analysis
3. Hypothesis and testing
4. Implementation

## Pitfalls

- **DO NOT** try `browser_vision` more than once to confirm no-vision. The model's API capability doesn't change between calls.
- **DO NOT** waste time building elaborate HTML viewers or local servers if you've already confirmed the model has no vision — the result is the same (vision fails).
- **DO NOT** use `data:` URIs in HTML served via `file:///` — they often exceed URI length limits in Chromium.
- **On Windows**: `python3` in git-bash may point to WindowsApps (MS Store redirect), which silently fails for anything non-trivial. Always use the explicit Python path under `Programs/Python/` or the venv Python.
- **easyocr** is heavy (~1GB download on first run) — only install if you have bandwidth.
- **pytesseract** needs `tesseract-ocr` binary installed separately (`choco install tesseract` or download from GitHub).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Model supports vision | Use `browser_vision` directly — fastest path |
| Model no vision + tesseract installed | `pytesseract.image_to_string(img, lang="por+eng")` |
| Model no vision + nothing installed | **Ask user to describe/paste the content** — don't flail |
| Image is of code/error | Ask user to paste the text directly |
| Image is of UI/design | Ask user to describe what they see |
