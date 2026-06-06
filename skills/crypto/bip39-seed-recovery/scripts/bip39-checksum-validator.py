#!/usr/bin/env python3
"""
BIP-39 Checksum Validator

Tests all combinations of ambiguous word translations against the BIP-39 checksum.
Given a base set of fixed-word indices and variable-position options, finds the
combination that produces a valid checksum.

Usage:
    python bip39_checksum_validator.py

Modify the FIXED_INDICES and AMBIGUOUS_GROUPS at the bottom of the file for each use.
"""
import hashlib
from itertools import product

def load_wordlist(path="bip39.txt") -> list[str]:
    """Load BIP-39 English wordlist"""
    with open(path) as f:
        return [l.strip() for l in f]

def validate_checksum(indices: list[int], wordlist: list[str]) -> tuple[bool, str]:
    """
    Validate BIP-39 checksum for a 12-word seed.
    Returns (is_valid, space_joined_seed_string)
    
    12 words = 132 bits = 128 entropy + 4 checksum
    """
    bits = ''.join(f'{i:011b}' for i in indices)
    entropy_bits = bits[:128]
    checksum_bits = bits[128:132]
    
    entropy = int(entropy_bits, 2).to_bytes(16, 'big')
    h = hashlib.sha256(entropy).digest()
    expected = h[0] >> 4  # First 4 bits of SHA256
    
    valid = (expected == int(checksum_bits, 2))
    seed = ' '.join(wordlist[i] for i in indices)
    return valid, seed

def search_combinations(fixed_positions: dict[int, int], 
                        ambiguous_groups: list[tuple[int, list[int]]],
                        wordlist: list[str]) -> list[tuple[list[int], str, str]]:
    """
    fixed_positions: {index_in_seed: wordlist_index} for known words
    ambiguous_groups: [(position_in_seed, [possible_wordlist_indices]), ...]
    
    Returns list of (indices, seed_string, description) for valid checksums
    """
    # Build the list of variable options
    var_positions = [g[0] for g in ambiguous_groups]
    var_options = [g[1] for g in ambiguous_groups]
    
    results = []
    count = 0
    
    for combo in product(*var_options):
        count += 1
        indices_list = [None] * 12
        
        # Fill fixed positions
        for pos, idx in fixed_positions.items():
            indices_list[pos] = idx
        
        # Fill variable positions with this combo
        for pos, idx in zip(var_positions, combo):
            indices_list[pos] = idx
        
        valid, seed = validate_checksum(indices_list, wordlist)
        if valid:
            # Build description
            parts = []
            for pos, idx in zip(var_positions, combo):
                parts.append(f"pos{pos}={wordlist[idx]}({idx})")
            desc = ", ".join(parts)
            results.append((indices_list, seed, desc))
    
    print(f"Tested {count} combinations")
    return results

def load_wordlist_remote() -> list[str]:
    """Download wordlist from GitHub (avoids local path issues on Windows/MSYS)"""
    import urllib.request
    url = 'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt'
    resp = urllib.request.urlopen(url)
    return resp.read().decode().strip().splitlines()

if __name__ == "__main__":
    import sys
    
    # Load from local file first, fallback to remote download
    try:
        wl = load_wordlist()
    except FileNotFoundError:
        print("Local bip39.txt not found. Downloading from GitHub...")
        wl = load_wordlist_remote()
    
    i2w = {i: w for i, w in enumerate(wl)}
    w2i = {w: i for i, w in enumerate(wl)}
    
    # ═══════════════════════════════════════════════════
    # CONFIGURE THIS SECTION FOR EACH RECOVERY
    # ═══════════════════════════════════════════════════
    
    # PRO TIP: word position matters. If you don't know the original order,
    # the user needs to confirm the POSITION of ambiguous words too.
    
    # Known-fixed words: {seed_position: wordlist_index}
    # Example from session: método(1122) at pos0, clip(347) at pos1, etc.
    fixed = {
        0: 1122,    # método → method
        1: 347,     # clipe → clip
        2: 1544,    # ciência → science
        4: 1476,    # revelar → reveal
        5: 1276,    # panda → panda
        7: 1853,    # viajar → travel (or 1969:voyage)
        11: 1124,   # meia-noite → midnight
    }
    
    # Ambiguous groups: (seed_position, [possible_wordlist_indices])
    # Order matters: place MOST PROBABLE translations first (literal > synonym)
    # so the script finds the match faster and avoids timeout.
    ambiguous = [
        (3,  [2030, 795]),     # mundo → world(2030), globe(795)
        (6,  [1622, 1016, 471, 640]),  # saia → skirt, leave, depart, exit
        (8,  [1405, 950, 1099]),       # questão → question, issue, matter
        (9,  [505, 906, 1599]),        # doença → disease, illness, sick
        (10, [1631, 1668, 1627]),      # magro → slim, spare, slender
    ]
    
    # If checksum fails with current fixed words, try these alternatives for método:
    # system(1767), mode(1141), technique(1861) — uncomment below and comment out method
    # fixed[0] = 1767  # método → system
    
    # If viajar doesn't match, try voyage(1969):
    # fixed[7] = 1969  # viajar → voyage
    
    # ═══════════════════════════════════════════════════
    # RUN (with early exit on first match)
    # ═══════════════════════════════════════════════════
    
    results = search_combinations(fixed, ambiguous, wl)
    
    if results:
        print(f"\n✅ Found {len(results)} valid checksum combination(s):")
        for idx, seed, desc in results:
            print(f"\n  Seed: {seed}")
            print(f"  Mapping: {desc}")
    else:
        print("\n❌ No valid checksum found with current candidates.")
        print("  Try: different word order, wider candidates, or different fixed words.")
        print("  - método alternatives: system(1767), mode(1141), technique(1861)")
        print("  - viajar alternatives: voyage(1969)")
        print("  - Also verify word ORDER — same words, different order = different wallet")
