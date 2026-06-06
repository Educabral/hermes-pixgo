# Hostinger IMAP/SMTP — Config for Himalaya CLI

## Server Details

| Service | Host | Port | Encryption |
|---------|------|------|------------|
| IMAP | `imap.hostinger.com` | 993 | TLS |
| SMTP | `smtp.hostinger.com` | 465 | TLS |

## Himalaya Config Template

```toml
[accounts.pixgo]
email = "suporte@pixgo.me"
display-name = "Eduardo Cabral"
default = true

backend.type = "imap"
backend.host = "imap.hostinger.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "suporte@pixgo.me"
backend.auth.type = "password"
backend.auth.cmd = "bash ~/AppData/Local/hermes/scripts/pixgo_pass.sh"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.hostinger.com"
message.send.backend.port = 465
message.send.backend.encryption.type = "tls"
message.send.backend.login = "suporte@pixgo.me"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "bash ~/AppData/Local/hermes/scripts/pixgo_pass.sh"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"
```

## Password Script Pattern

Create a shell script that prints the password to stdout (no newline):

```bash
#!/bin/bash
echo -n "PASSWORD_HERE"
```

Save to `~/AppData/Local/hermes/scripts/pixgo_pass.sh` and reference it in the config as `bash ~/AppData/Local/hermes/scripts/pixgo_pass.sh`.

**Important:** The `$` character at end of password must be inside single quotes in the script: `echo -n 'PASSWORD$'` — otherwise bash interprets `$` as variable expansion.

## Authentication Troubleshooting

- **"Authentication failed"** despite correct password in webmail: Hostinger may require an **App Password** for IMAP/SMTP access. Standard webmail password may not work.
- Generate App Password via Hostinger hPanel → Email → App Passwords (if available).
- Alternatively, the password may simply be wrong — verify in the Hostinger webmail login.
