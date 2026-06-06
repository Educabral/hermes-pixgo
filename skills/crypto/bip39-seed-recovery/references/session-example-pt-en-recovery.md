# Session Example: PT→EN BIP-39 Recovery (2025-05-23)

## Original User Words (Portuguese)

método, clipe, ciência, mundo, revelar, panda, saia, viajar, questão, doença, magro, meia-noite

## Translation Candidates (each → possible BIP-39 words)

| PT | EN candidates (index:word) |
|----|---------------------------|
| método | 1122:method, 1767:system, 1141:mode, 1861:technique |
| clipe | 347:clip |
| ciência | 1544:science |
| mundo | 2030:world, 795:globe |
| revelar | 1476:reveal |
| panda | 1276:panda |
| saia | 1622:skirt, 1016:leave, 471:depart, 640:exit |
| viajar | 1853:travel, 1969:voyage |
| questão | 1405:question, 950:issue, 1099:matter |
| doença | 505:disease, 906:illness, 1599:sick |
| magro | 1631:slim, 1668:spare, 1627:slender |
| meia-noite | 1124:midnight |

## Checksum Validation Result

The FIRST combination tested matched:
- **mundo=world, saia=skirt, questão=question, doença=disease, magro=slim, viajar=travel**

However this produced `middle clock scissors worry review panel skull tray quick dish slogan milk` — which does NOT correspond to the expected semantic translations. This means some assumed translations were wrong, or the word position mapping was incorrect.

## Key Lesson

Even when checksum passes, the resulting English words may not semantically match the Portuguese. The checksum only validates the **bit-level integrity**, not the meaning. If the user gave the translated seed in a DIFFERENT order than the original, or if some words aren't literal translations, the checksum-valid seed will open a DIFFERENT wallet.

**Always verify**: ask the user if the resulting words "feel right" or match what they remember writing down originally.
