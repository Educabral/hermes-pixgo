# Gmail Inbox Triage — Cron Workflow

Account: `gmail` (non‑default, `segurancabral@gmail.com`)
App password stored in `~/AppData/Local/hermes/scripts/gmail_pass.sh`

## Classification Rules

**IMPORTANTE** — notify user:
- Fatura de conta (Sabesp, SP LINK, etc.)
- Alerta de segurança (login, Google, GitHub, Facebook, Amazon, Google DMARC)
- Extrato bancário/financeiro (Nubank, Mercado Pago, etc.)
- Pagamento falhando
- Confirmação de pedido com entrega pendente
- Qualquer coisa que exija ação do usuário

**LIXO** — move to `[Gmail]/Lixeira` silently:
- Propaganda / promoção
- Newsletter / onboarding
- Aviso genérico / lembrete para terceiro
- Notificação já resolvida
- Price alerts (Perplexity Tasks, CMC Spotlight, etc.)
- Emails que o usuário já estrelou manualmente (ficam onde estão)

**When in doubt, delete.** The user prefers a clean inbox.

## Step-by-Step

1. **List envelopes in INBOX:**
   ```bash
   himalaya envelope list -a gmail --page 1 --page-size 50
   ```

2. **Identify unread** — rows with blank FLAGS column. Read them with:
   ```bash
   himalaya message read -a gmail <ID>
   ```

3. **Classify each unread:**
   - If IMPORTANTE → prepare summary for delivery
   - If LIXO → batch-delete

4. **Move LIXO to trash:**
   ```bash
   himalaya message move -a gmail "[Gmail]/Lixeira" <ID1> <ID2> ...
   ```
   Gmail folder names (Portuguese UI): `[Gmail]/Lixeira`, `[Gmail]/E-mails enviados`, `[Gmail]/Com estrela`, `[Gmail]/Rascunhos`, `[Gmail]/Spam`.

5. **Starred emails (`!`)**: Leave them alone — the user manually flagged these as keepers. Only remove if clearly stale (expired event, paid bill from >1 year ago with no unresolved issue).

6. **Deliver report**: Summarize only IMPORTANTE items. Mention if inbox ended clean.

## Pitfalls

- **`-a gmail` MUST come after the subcommand**, not before. Wrong: `himalaya -a gmail envelope list` → `error: unexpected argument '-a' found`. Correct: `himalaya envelope list -a gmail`.
- **`himalaya message delete` does not work on Gmail.** Always use `himalaya message move "[Gmail]/Lixeira" <ID>`.
- **IMAP warns** `Rectified missing text to "..."` on loading. This is harmless — ignore it.
- **Message IDs change** after moving messages. Always re-list with `envelope list` after move operations before acting on new IDs.
- **Gmail `folder.aliases.trash`** in config is often set to `[Gmail]/Trash` (English) but the actual folder is `[Gmail]/Lixeira` on Portuguese-UI accounts. Use `himalaya folder list -a gmail` to discover real names.
