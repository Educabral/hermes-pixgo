# Gmail (segurancabral@gmail.com) — Cleanup Rules

## What to KEEP and ALERT user about

| Category | Examples | Why keep |
|----------|----------|----------|
| Security alerts | Google "senha de app criada", Amazon "alguem removeu celular", Facebook "conta adicionada", Netflix "novo aparelho" | User needs to know if someone accessed their account |
| Payment failures | Runable/X "pagamento falhou" (Stripe failed payment emails) | Payment method needs updating |
| Financial statements | Nubank extrato fundos, Mercado Pago extrato, Google Play receipt | Proof of payment / fiscal records |
| GitHub token expiry | "[GitHub] Your personal access token is about to expire" | Action needed to renew before builds break |
| GitHub OAuth changes | "[GitHub] A third-party OAuth application has been added" | Security check |
| Active onboarding/setups | ngrok welcome, Arkham trial, Voice Monkey, Threads | Setup still in progress |
| Health appointments | SISS Saude lembretes | Medical appointments |
| Invoices (contas) | Sabesp, SP LINK Internet | Bills to pay |
| Event tickets | Quintal BethaVille ingressos ⭐ | User starred them |

## What to DELETE (silently, no alert)

| Category | Examples |
|----------|----------|
| Marketing/newsletters | Privalia, Sam's Club, Mercado Livre ofertas, OLX, VAIO |
| Crypto news | CMC Spotlight, Perplexity Tasks price alerts |
| Spam/debt collection | "Acordo Certo", "Boletim Extrajudicial", "divida ativa", "QueroQuitar" |
| Completed onboarding | Arkham check-in day 3 (already onboarded), Crypix blog launch |
| Generic notifications | Netflix "saindo titulos", Spotify "politica privacidade" |
| Redeemable offers | "R$95 no clube", "ganhe dinheiro" |
| IFTTT password resets | Already completed (subsequent "password set" email exists) |
| Render build failures | Old deploy logs (already resolved) |

## Technical notes

- **Delete = move to [Gmail]/Lixeira** (Gmail doesn't support hard delete via IMAP)
- Use: `himalaya message move "[Gmail]/Lixeira" <ID1> <ID2> ...`
- Batch size: 5 IDs per command (avoids timeouts)
- Flags: `*` = seen/read, `@` = attachment, `!` = flagged/starred, `R` = replied
- Unread emails have no `*` flag in the listing
- Account switch: set `default = true` under the desired account in config.toml. No `--account` flag on this Windows Himalaya build.
