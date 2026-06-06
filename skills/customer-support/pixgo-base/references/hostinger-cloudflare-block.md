# Hostinger Webmail — Cloudflare Block + IMAP/SMTP

## Cloudflare Challenge no Webmail

O `mail.hostinger.com` está protegido por Cloudflare com desafio "Confirme que é humano" (Turnstile/Under Attack Mode). Isso significa que:

- **Browser tool do Hermes NÃO passa** — o Cloudflare detecta automação e bloqueia mesmo após clicar no checkbox
- **A sessão do usuário no Comet/Chrome é SEPARADA** — o fato do usuário estar logado no webmail no navegador dele não ajuda a sessão do Hermes
- **Workaround:** usuário copiar o texto do email e colar aqui, OU fazer login na sessão do browser tool do Hermes

## IMAP/SMTP — Hostinger e Senha de App

Conexão IMAP/SMTP direta com a senha principal do webmail **NÃO funciona**. A Hostinger rejeita com `AUTHENTICATIONFAILED`.

**Solução:** gerar uma **senha de app** no painel Hostinger:
1. Acessar o painel da Hostinger
2. Ir em Email → Gerenciar → Configurações de segurança
3. Gerar senha de app específica para IMAP/SMTP
4. Usar essa senha no Himalaya ou outro cliente de email

**Configuração IMAP:**
- Servidor: `imap.hostinger.com`
- Porta: 993 (SSL/TLS)
- Usuário: suporte@pixgo.me
- Autenticação: Plain ou Login

**Configuração SMTP:**
- Servidor: `smtp.hostinger.com`
- Porta: 465 (SSL/TLS)
- Usuário: suporte@pixgo.me

## Himalaya CLI

Instalado em `~/.local/bin/himalaya`.
Config: `~/.config/himalaya/config.toml` (deve conter account, email, imap e smtp).
Senha: script `~/AppData/Local/hermes/scripts/pixgo_pass.sh`.
