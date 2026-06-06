---
name: bip39-seed-recovery
description: Diagnose and recover BIP-39 seed phrases that users mis-translated, mis-typed, or wrote in a non-English language. Covers checksum validation, wordlist lookup, PT→EN translation mapping, and step-by-step user guidance.
tags:
  - bip39
  - seed-phrase
  - wallet-recovery
  - cryptocurrency
  - bitcoin
  - bip-39
related_skills:
  - crypto-market-analysis
---

# BIP-39 Seed Recovery

## When to Use

A user reports their wallet won't connect/import, and they:
- Translated their 12/24-word seed phrase from English to their native language (Portuguese, Spanish, etc.)
- Misspelled one or more words from the BIP-39 wordlist
- "Forgot" the exact words but remembers approximate translations
- Is getting "invalid mnemonic" / "checksum error" from wallet software

## Core Constraint

**BIP-39 seed phrases ONLY accept the exact 2048 English words** from the official wordlist. No translations, no variations, no other languages. The wallet's BIP-39 implementation will reject anything else.

## Workflow

### Step 1: Get the exact words the user wrote

Ask them to send **every word exactly as they wrote it** (in their language). Don't let them guess — they need to send the list.

### Step 2: Build the PT→EN candidate map

Download the BIP-39 English wordlist:
```
curl -s https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt > bip39.txt
```

For each Portuguese word the user provides, find the most likely BIP-39 English equivalent:

1. **Literal translation** — is the PT word a direct translation of an English BIP-39 word?
   - e.g. `mundo` → `world` (2030), `ciência` → `science` (1544), `revelar` → `reveal` (1476)
   - e.g. `viajar` → `travel` (1853), `meia-noite` → `midnight` (1124)

2. **Fonetic/sonority match** — words that sound similar even if meaning differs
   - e.g. `ligar` is NOT a BIP-39 word 
   - The closest BIP-39 candidates that COULD be confused: `link` (1041), `light` (1037), `bind` (179)

3. **False cognates** — words that look like English but aren't
   - e.g. `pular` ≠ `pull` (jump, not pull); `assistir` ≠ `assist` (watch, not help)

4. **Semantic drift** — user remembered the concept but not the exact word
   - e.g. `saia` could be `skirt`, `leave`, `depart`, or `exit`
   - e.g. `magro` could be `slim`, `spare`, or `slender`

### Step 3: Run checksum validation

Build and run a Python script that tests ALL combinations of the ambiguous words against the BIP-39 checksum:

```
python -c "
import hashlib
with open(r'path\to\bip39.txt') as f:
    wl = [l.strip() for l in f]
i2w = {i:w for i,w in enumerate(wl)}

# Fixos (certeza)
method=1122; clip=347; science=1544; reveal=1476; panda=1276; travel=1853; midnight=1124

# Ambiguos — substituir pelas opcoes reais
mundo_opts = [('world',2030),('globe',795)]
saia_opts = [('skirt',1622),('leave',1016),('depart',471),('exit',640)]
# ... etc

def test(indices):
    bin_str = ''.join(f'{i:011b}' for i in indices)
    entropy = int(bin_str[:128],2).to_bytes(16,'big')
    h = hashlib.sha256(entropy).digest()
    return (h[0]>>4) == int(bin_str[128:132],2)

# Loop over all combos
# ...
"
```

**Key detail about the indices**: The checksum validates the ENTROPY (first N bits), not the words themselves. For a 12-word seed: first 128 bits = entropy, last 4 bits = checksum (first 4 bits of SHA256(entropy)).

### Step 4: Interpret results

- **Checksum match found** → give the user the exact English seed. They can now import into their wallet.
- **No match** → some of your assumed translations are wrong. Widen the candidates:
  - `método` could be `system`, `mode`, or `technique` (not just `method`)
  - `viajar` could be `voyage` instead of `travel`
  - The user may have the words in the **wrong order**

### Step 5: When checksum fails completely

Escalate options to the user:

1. Try each ambiguous word ONE AT A TIME manually in the wallet (change 1 word, try import, repeat)
2. Use a tool like [SeedTool](https://seedtool.xyz/) or [BIP39 Recovery](https://bip39recovery.com/) offline
3. If they truly lost the exact words, the seed is unrecoverable — warn them this is non-custodial and nobody (including the exchange/support) can help

## Pitfalls

- **Do NOT ask for the current seed "to test"** — the user should never type their seed into any chat/client. Work with translations/fuzzy versions only.
- **Zero-width characters** — sometimes copy-paste from Telegram/whatsapp injects invisible Unicode chars. Strip them.
- **Word order matters** — same 12 words in a different order = completely different wallet. Checksum will fail.
- **Case insensitive** — BIP-39 is lowercase only. Normalize before lookup.
- **Compound words** — `meia-noite` is 1 word in Portuguese but `midnight` is 1 word in English. Fine. But `ice cream` is 2 English words.
- **python3 aliases on Windows** — `python3` in git-bash/MSYS points to the Microsoft Store stub (`WindowsApps/python3.exe`) and fails with exit code 49. ALWAYS use bare `python` on Windows. Verify with `python --version` first. Download the wordlist to a Windows path like `C:\Users\<user>\bip39.txt` and reference it with the Windows path or forward-slash MSYS path.
- **Checksum validation timeout** — testing all combinations of 5 ambiguous word groups with 3-4 options each = 3×4×3×3×3 = 324 combinations per batch × 2 variations (travel vs voyage) = 648 total. Each SHA256 calculation is fast, BUT the Python `product()` over nested loops can be slow if running in a large script. Solution: use `itertools.product()` with early `sys.exit(0)` on first match, and STDOUT-only output (no debug prints inside loops). If timeout still occurs, break into smaller batches: test the most probable translations first (literal translations, not synonyms), and only expand on failure.
- **método can map to multiple BIP-39 words** — not just `method` (1122). Also consider: `system` (1767, Portuguese: "sistema"), `mode` (1141, "modo"), `technique` (1861, "técnica"). Which word the user wrote depends on how they conceptualized the English original. If checksum fails with `method`, test the others.
- **Software wallet "Liquid/BIP-39" quirks** — Liquid-based wallets (like PixGo, Sideswap, Blockstream Green) use BIP-39 but sometimes wrap the seed in SLIP-0013/Electrum-style prefixes or use different derivation paths. The BIP-39 checksum validation validates the mnemonic itself, not the derivation—so a valid BIP-39 checksum doesn't guarantee the wallet will find funds. Still, fixing the checksum is step 1.

## References

- [BIP-39 Specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
- [Official BIP-39 English Wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt)
- 12-word seed = 128 bits entropy + 4 bits checksum = 132 bits = 12 × 11-bit indices
- 24-word seed = 256 bits entropy + 8 bits checksum = 264 bits = 24 × 11-bit indices
