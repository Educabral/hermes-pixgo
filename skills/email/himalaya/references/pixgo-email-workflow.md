# PixGo Email Workflow — noreply@pixgo.me

## Account Context

- Email: **noreply@pixgo.me** (NOT suporte@pixgo.me — that one exists but this is the operational inbox)
- Display name: Eduardo Cabral
- Hosting: Hostinger (webmail, IMAP, SMTP)
- IMAP/SMTP servers: imap.hostinger.com:993 (TLS), smtp.hostinger.com:465 (TLS)
- Password stored in: `~/AppData/Local/hermes/scripts/pixgo_pass.sh` (`3Npw0]FGX68$`)

## Status

**IMAP/SMTP WORKS** with the stored password. No App Password needed.

The previous assumption that IMAP was blocked (`AUTHENTICATIONFAILED`) was because we tried the wrong email (`suporte@pixgo.me`). The email `noreply@pixgo.me` authenticates fine with the same credentials.

## Himalaya Config

Account name in config.toml: `pixgo`
The user also has a personal Gmail (`segurancabral@gmail.com`) as account `gmail`.

Since Himalaya v1.2.0 doesn't support the `--account` flag on Windows, switching between accounts requires editing `default = true` in config.toml:
- Set `[accounts.pixgo] default = true` + remove default from gmail → work on PixGo inbox
- Set `[accounts.gmail] default = true` + remove default from pixgo → work on Gmail inbox

## Response Style for MED Emails

- **Professional tone**, no emojis, no markdown formatting
- **Sign**: Eduardo Cabral / Gerente de Contas
- **Vary vocabulary** between consecutive replies to the same client
- **Never ask** the client for proof of shipment or invoices
- Key points to include when explaining MED:
  - MED (Mecanismo Especial de Devolução) is a Central Bank of Brazil instrument
  - It allows cardholders to dispute transactions with their financial institution
  - PixGo is a **technological interface** between the merchant and acquirers — sends documentation, but analysis/decision is the acquirer's responsibility
  - When a MED is cancelled by the client: the investigation still runs independently, 15-20 business days for return
  - Investigation is independent of agreements between parties

## Email Classification for Auto-Management

When monitoring the PixGo inbox, classify incoming emails as:

1. **MED Contestation with documents** (anexos included): Respond confirming receipt, docs registered, forwarded for analysis, 15-20 business day timeline
2. **MED Contestation without documents**: Request specific documents (proof of contact, screenshots, invoice)
3. **Client says they cancelled the MED / want refund**: Explain the process still needs investigation, 15-20 days for return
4. **Support tickets / protocol updates**: Forward to user as summary
5. **Anything unusual**: Alert the user on Telegram with a summary
