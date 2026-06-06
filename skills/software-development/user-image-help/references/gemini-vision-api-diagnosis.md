# Gemini Vision API Key Diagnosis

## The Problem

`vision_analyze()` fails with:
```
Error analyzing image: Gemini HTTP 400 (INVALID_ARGUMENT): API key not valid
```

## Root Cause

The config.yaml has:
```yaml
auxiliary:
  vision:
    api_key: ''           # ← EMPTY
    provider: gemini
    model: gemini-2.5-flash
```

When `api_key` is empty (`''`), the system falls back to env vars. If the `.env` has the key commented out:
```
# GOOGLE_API_KEY=your_key_here
# GEMINI_API_KEY=your_key_here
```

The fallback fails silently, and the HTTP 400 is the result.

## Fix

```bash
# Option 1: Set in .env (uncomment)
sed -i 's/^# GOOGLE_API_KEY=/GOOGLE_API_KEY=/' ~/AppData/Local/hermes/.env
# Then add the actual key

# Option 2: Set in config.yaml directly
hermes config set auxiliary.vision.api_key "your_gemini_key_here"
```

## Verification

```bash
grep -E "GOOGLE_API_KEY|GEMINI_API_KEY|vision.api_key" ~/AppData/Local/hermes/.env ~/AppData/Local/hermes/config.yaml
```

## Notes

- Gemini 1.5 Flash and 2.0 Flash both support vision.
- On Windows, the `.env` path is `C:\Users\<user>\AppData\Local\hermes\.env`.
- After changing config, restart the agent: `/reset` in CLI, `/restart` in gateway.
