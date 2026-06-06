---
name: himalaya
description: "Himalaya CLI: IMAP/SMTP email from terminal."
version: 1.1.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Communication]
    homepage: https://github.com/pimalaya/himalaya
prerequisites:
  commands: [himalaya]
---

# Himalaya Email CLI

Himalaya is a CLI email client that lets you manage emails from the terminal using IMAP, SMTP, Notmuch, or Sendmail backends.

This skill is separate from the Hermes Email gateway adapter. The gateway
adapter lets people email the agent and uses Hermes' built-in IMAP/SMTP
adapter; this skill lets the agent operate a mailbox from terminal tools and
requires the external `himalaya` CLI.

## References

- `references/configuration.md` (config file setup + IMAP/SMTP authentication)
- `references/message-composition.md` (MML syntax for composing emails)
- `references/hostinger-smtp-imap.md` (Hostinger IMAP/SMTP server details, config template, and App Password auth troubleshooting)
- `references/pixgo-email-workflow.md` (PixGo-specific email context: Hostinger known auth issue, workflow options when IMAP fails, constraints)

## Project-Specific Workflows

- **PixGo/noreply@pixgo.me**: See `references/pixgo-email-workflow.md`. IMAP/SMTP work with stored password. The earlier `suporte@pixgo.me` guess was wrong — always use `noreply@pixgo.me`.
- **SegurancaBral Gmail**: Account `gmail` in config. Uses App Password (stored in `~/AppData/Local/hermes/scripts/gmail_pass.sh`). Daily cron clears spam, only alerts on important items. See `references/gmail-inbox-triage.md` for the complete cron workflow (classification rules, step-by-step, pitfalls).

## Prerequisites

1. Himalaya CLI installed (`himalaya --version` to verify)
2. A configuration file at `~/.config/himalaya/config.toml`
3. IMAP/SMTP credentials configured (password stored securely)

### Installation

```bash
# Pre-built binary (Linux/macOS — recommended)
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS via Homebrew
brew install himalaya

# Or via cargo (any platform with Rust)
cargo install himalaya --locked
```

## Configuration Setup

Run the interactive wizard to set up an account:

```bash
himalaya account configure
```

Or create `~/.config/himalaya/config.toml` manually:

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # or use keyring

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"

# Folder aliases (himalaya v1.2.0+ syntax). Required whenever the
# server's folder names don't match himalaya's canonical names
# (inbox/sent/drafts/trash). Gmail is the common case — see
# `references/configuration.md` for the `[Gmail]/Sent Mail` mapping.
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"
```

> **Heads up on the alias syntax.** Pre-v1.2.0 docs used a
> `[accounts.NAME.folder.alias]` sub-section (singular `alias`).
> v1.2.0 silently ignores that form — TOML parses fine, but the
> alias resolver never reads it, so every lookup falls through to
> the canonical name. On Gmail this means save-to-Sent fails *after*
> SMTP delivery succeeds, and `himalaya message send` exits non-zero.
> Any caller (agent, script, user) that retries on that exit code
> will re-run the entire send — including SMTP — producing duplicate
> emails to recipients. Always use `folder.aliases.X` (plural, dotted
> keys, directly under `[accounts.NAME]`).

## Hermes Integration Notes

- **Reading, listing, searching, moving, deleting** all work directly through the terminal tool
- **Composing/replying/forwarding** — piped input (`cat << EOF | himalaya template send`) is recommended for reliability. Interactive `$EDITOR` mode works with `pty=true` + background + process tool, but requires knowing the editor and its commands
- Use `--output json` for structured output that's easier to parse programmatically
- The `himalaya account configure` wizard requires interactive input — use PTY mode: `terminal(command="himalaya account configure", pty=true)`

## Common Operations

### List Folders

```bash
himalaya folder list
```

### List Emails

List emails in INBOX (default):

```bash
himalaya envelope list
```

List emails in a specific folder:

```bash
himalaya envelope list --folder "Sent"
```

List with pagination:

```bash
himalaya envelope list --page 1 --page-size 20
```

### Search Emails

```bash
himalaya envelope list from john@example.com subject meeting
```

### Read an Email

Read email by ID (shows plain text):

```bash
himalaya message read 42
```

Export raw MIME:

```bash
himalaya message export 42 --full
```

### Reply to an Email

To reply non-interactively from Hermes, read the original message, compose a reply, and pipe it:

```bash
# Get the reply template, edit it, and send
himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
```

Or build the reply manually:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: sender@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>

Your reply here.
EOF
```

Reply-all (interactive — needs $EDITOR, use template approach above instead):

```bash
himalaya message reply 42 --all
```

### Forward an Email

```bash
# Get forward template and pipe with modifications
himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
```

### Write a New Email

**Non-interactive (use this from Hermes)** — pipe the message via stdin:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

Or with headers flag:

```bash
himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
```

Note: `himalaya message write` without piped input opens `$EDITOR`. This works with `pty=true` + background mode, but piping is simpler and more reliable.

### Move/Copy Emails

Move to folder:

```bash
himalaya message move 42 "Archive"
```

Copy to folder:

```bash
himalaya message copy 42 "Important"
```

### Delete an Email

**Does not work on Gmail** — the internal `move to Trash` fails with "No fold" because the alias resolution for delete is broken. Use the move workaround instead:

```bash
# Gmail: move to lixeira/trash instead of delete
himalaya message move "[Gmail]/Lixeira" 42 43 44
```

For non-Gmail IMAP servers where `delete` works:

```bash
himalaya message delete 42
```

### Manage Flags

Add flag (positional syntax — no `--flag` flag):

```bash
# Add star (flagged) to an email
himalaya flag add 42 flagged -f INBOX
```

Add flag to multiple emails:

```bash
himalaya flag add 42 43 44 flagged -f INBOX
```

Remove flag:

```bash
himalaya flag remove 42 flagged -f INBOX
```

Note: `-f INBOX` specifies the source folder (required if not default). The flag name is positional (`flagged` for starred, `seen` for read).

## Multiple Accounts

List accounts:

```bash
himalaya account list
```

Use the default account (no flag needed):

```bash
himalaya envelope list
```

Use a specific (non-default) account — `-a` flag MUST go AFTER the subcommand, NOT before:

```bash
himalaya envelope list -a gmail
himalaya message read -a gmail 42
himalaya folder list -a gmail
himalaya message move -a gmail "[Gmail]/Lixeira" 42 43
```

⚠ **CRITICAL — `-a` position matters.** Placing `-a` before the subcommand (e.g. `himalaya -a gmail envelope list`) fails with `error: unexpected argument '-a' found`. Always place `--account NAME` / `-a NAME` immediately after the subcommand name.

## Attachments

Save attachments from a message:

```bash
himalaya attachment download 42
```

Save to specific directory:

```bash
himalaya attachment download 42 --dir ~/Downloads
```

## Output Formats

Most commands support `--output` for structured output:

```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

## Debugging

Enable debug logging:

```bash
RUST_LOG=debug himalaya envelope list
```

Full trace with backtrace:

```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## Understanding the FLAGS Column

When listing envelopes, the FLAGS column tells you message state:

| Symbol | Meaning                    |
|--------|----------------------------|
| (blank)| **Unread** — not yet seen  |
| `*`    | **Seen** — already read    |
| `!`    | **Flagged/Starred** by user|
| `R`    | **Replied** to             |
| `@`    | **Attachment** present     |

Multiple flags combine (e.g., `!R` = starred and replied, `*R` = read and replied).

This is critical for inbox triage cron jobs: unread = no flags at all, seen = `*`, manually important = `!`.

## Tips

- Use `himalaya --help` or `himalaya <command> --help` for detailed usage.
- Message IDs are relative to the current folder; re-list after folder changes.
- For composing rich emails with attachments, use MML syntax (see `references/message-composition.md`).
- Store passwords securely using `pass`, system keyring, or a command that outputs the password.

## Gmail-Specific Notes

- **Gmail folder names are in Portuguese** when the account UI is in Portuguese: `[Gmail]/Lixeira` for Trash, `[Gmail]/E-mails enviados` for Sent, `[Gmail]/Com estrela` for Starred. Use `himalaya folder list` to discover actual folder names.
- **`himalaya message delete <ID>` does not work on Gmail** — it tries to move to the Trash alias but fails with "No fold" because the alias mapping doesn't resolve for delete internally. Use `himalaya message move "[Gmail]/Lixeira" <ID1> <ID2> ...` instead.
- **Senha de app Google**: user must go to `https://myaccount.google.com/apppasswords` (requires 2FA enabled). The standard Gmail password does NOT work with IMAP/SMTP clients.
- **Gmail sent folder alias**: use `folder.aliases.sent = "[Gmail]/E-mails enviados"` — the English `[Gmail]/Sent Mail` may not exist if the UI is in Portuguese. Use `folder.aliases.trash = "[Gmail]/Lixeira"` and `folder.aliases.drafts = "[Gmail]/Rascunhos"`.
- **Price alerts / crypto newsletters / promo emails**: identify by sender pattern (CMC Spotlight, Perplexity Tasks, Privalia, Sam's Club, OLX, Acordo Certo, Boletim Extrajudicial). These are safe to batch-delete.
- **IMAP port 993 TLS** and **SMTP port 465 TLS** are standard for Gmail. No STARTTLS needed.
- **Batch cleanup pattern**: list all envelopes first with `himalaya envelope list --page 1 --page-size 50`, identify which to keep, compute the diff, then batch-move to Lixeira in groups of 5-10 IDs: `himalaya message move "[Gmail]/Lixeira" <id1> <id2> ...`. Work in batches of 5 for reliability.
- **Flag/star emails**: use `himalaya flag add <id> flagged -f INBOX` (positional syntax, no `--flag` flag). Verify with `himalaya envelope list -f INBOX` (starred emails show `!` in FLAGS column).
