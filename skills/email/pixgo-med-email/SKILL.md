---
name: pixgo-med-email
title: Resposta a MEDs (Mecanismo Especial de Devolução) — PixGo
description: Workflow e templates para responder contestações MED do Banco Central/DEPIX na plataforma PixGo. Cobre defesa contra estorno, comunicação de cancelamento, e prazos regulatórios.
tags:
  - pixgo
  - med
  - depix
  - banco-central
  - email
  - suporte
  - contestação
  - estorno
---

# Resposta a MEDs (Mecanismo Especial de Devolução) — PixGo

## Trigger

Usuário diz algo como "responde esse email", "responda a contestação", "elabore a resposta do MED", "faz o retorno do MED", "responda pro suporte", ou passa um print/texto de uma contestação MED, ou pede para monitorar/limpar a caixa de entrada da PixGo.

## Email Account

- Address: **noreply@pixgo.me** (NOT suporte@pixgo.me)
- IMAP/SMTP: Working. Account name `pixgo` in Himalaya config.
- Gmail personal: segurancabral@gmail.com — account name `gmail`.
- Switching accounts: swap `default = true` in config.toml (Himalaya Windows build has no --account flag). Cannot use `--account` or `-a` flags on this Windows build.
- Gmail sent folder: [Gmail]/Sent Mail, trash: [Gmail]/Lixeira (move, not delete)
- Hostinger folders: INBOX, INBOX.Sent, INBOX.Drafts, INBOX.Trash, INBOX.Junk (subfolders of INBOX, not flat)
- Hostinger folder aliases in config: sent="INBOX.Sent", drafts="INBOX.Drafts", trash="INBOX.Trash"
- Hostinger send works with `himalaya template send < file.txt`
- PixGo folders also include: INBOX.MED, INBOX.Erros (subfolders)

## Auto-Management (Cron)

When the user asks to automate email handling:
1. Cron runs daily at 10:00 BRT
2. Scans inbox for new/unread emails
3. Classifies: MED with docs (reply confirming), MED without docs (request documents), security/financial (alert user), spam/onboarding/newsletter (delete without asking)
4. Alert user on Telegram for anything important
5. Delete the rest silently

## Contexto

MED é um recurso do Banco Central que permite ao pagador contestar uma transação PIX. A PixGo é interface tecnológica — quem decide é a adquirente/banco emissor. O prazo de análise é **15 a 20 dias úteis**, podendo variar.

## Regras OBRIGATÓRIAS em toda resposta

1. **Prazo de análise:** SEMPRE mencionar que o prazo médio é de 15 a 20 dias úteis, podendo variar conforme fila e complexidade.
2. **Imparcialidade:** Deixar claro que a decisão final cabe à adquirente/banco emissor, e que a PixGo atua como interface tecnológica, não retendo nem liberando valores.
3. **Variação OBRIGATÓRIA:** Cada resposta deve ter estrutura e vocabulário DIFERENTES das anteriores. O usuário PEDE isso explicitamente. Variar abertura ("Olá, tudo bem?" / "Prezado(a), boa tarde." / "Prezado(a), boa noite."), organização dos parágrafos (contexto do MED antes da defesa / fatos primeiro / abertura com agradecimento), e escolha de palavras. Usar um repertório diverso de sinônimos (contestação/MED/recurso, análise/avaliação/apreciação, comprovação/evidência/registro).
4. **Tom profissional:** Corporativo, neutro, sem emoção. A defesa é baseada em FATOS — pagamento voluntário, atendimento iniciado, serviço executado.
5. **Oferecer envio de docs:** Sempre encerrar oferecendo que o usuário pode enviar prints/comprovantes adicionais para anexar ao processo.

## Template estrutural (NUNCA usar o mesmo texto, só como guia de tópicos)

### Abertura
- Agradecer/confirmar recebimento dos dados
- Informar que foi registrado para análise

### Corpo da defesa (adaptar conforme o caso)
- Pagamento foi voluntário e aprovado normalmente
- Atendimento iniciado após confirmação (via WhatsApp)
- Serviço começou a ser executado sem interrupção/negação
- Cliente abriu MED mesmo com serviço em andamento
- Concluir que não há fundamento para estorno

### Prazo e papel das instituições
- MED é regulado pelo BC, criado para coação/golpe/fraude, não cancelamento
- Pedido de rejeição protocolado
- Prazo de 15 a 20 dias úteis
- Decisão final: adquirente/banco emissor. PixGo é interface, não retém/libera valores

### Encerramento
- Oferecer envio de documentos complementares
- Disponibilidade para dúvidas

## Variações de vocabulário

| Conceito | Alternativa 1 | Alternativa 2 | Alternativa 3 |
|----------|--------------|---------------|---------------|
| MED | contestação | recurso | Mecanismo Especial de Devolução |
| análise | avaliação | apreciação | verificação |
| comprovante | evidência | registro | documentação |
| prazo | período | tempo estimado | janela |
| cliente | pagador | usuário | contratante |
| estorno | devolução | reversão | cancelamento da transação |

## Explicação do MED (OBRIGATÓRIA quando apropriado)

Incluir uma breve explicação do que é o MED em respostas onde o lojista demonstra não entender o processo:
- MED (Mecanismo Especial de Devolução) é um recurso instituído pelo Banco Central do Brasil
- Permite ao portador do cartão contestar uma transação junto à instituição financeira
- Quando um MED é aberto, passa por investigação conduzida pelos órgãos responsáveis (adquirente/banco emissor)
- A contestação é a etapa em que o estabelecimento apresenta evidências para tentar reverter o bloqueio
- O MED é destinado a casos de fraude ou transações não autorizadas — não é um "cancelamento" simples

## Cases especiais

### Gmail daily cleanup (cron)

When asked to set up automatic Gmail maintenance:
- Cron schedule: `0 10 * * *` (daily 10:00 BRT)
- Scan new/unread emails in Gmail
- Classify: security alerts (Google, Facebook, Amazon login changes), financial (extratos, payment failures, invoices), ongoing setups (onboarding emails for active integrations) → KEEP AND ALERT USER
- Trash: all marketing, newsletters, spam, onboarding already-completed, generic notifications → move to [Gmail]/Lixeira silently
- Goal: user wants inbox EMPTY of anything unnecessary. Be aggressive with deletions.
- Gmail uses `himalaya message move "[Gmail]/Lixeira" <ID>` not `himalaya message delete`
- Deliver important alerts to the user on Telegram

### Google Calendar / Drive Integration (setup pattern)

When asked to connect Google Calendar and/or Google Drive:
1. Install packages: `google-auth-oauthlib`, `google-api-python-client`, `google-auth-httplib2`
2. Create scripts under `~/AppData/Local/hermes/scripts/`:
   - `google_auth_setup.py` — runs OAuth flow, saves token.json to ~/.hermes/google/
   - `google_calendar.py` — CLI: `list [days]`, `create 'title' 'YYYY-MM-DD HH:MM' [duration]`
   - `google_drive.py` — CLI: `list [query]`, `search 'term'`
3. User must create Google Cloud Project + OAuth credentials (desktop app type) and save credentials.json to ~/.hermes/google/
4. User must authorize once via browser OAuth flow
5. After setup, scripts auto-refresh token

### Cliente diz "pode estornar" / "pode reembolsar" (MED já aberto)
Explicar que o MED já está em investigação pelos órgãos responsáveis — não é um estorno simples que a PixGo pode fazer:
- O MED já foi instaurado pelo cliente junto ao banco dele
- A análise e decisão cabem à adquirente/banco emissor — a PixGo não retém nem libera valores
- É necessário enviar documentação para contestar formalmente
- **CRÍTICO:** NUNCA sugerir "reembolso por fora" ou "fazer o estorno direto com o cliente". A resposta correta é SEMPRE que o MED precisa ser avaliado e analisado pelas instituições responsáveis (adquirente/banco emissor), independentemente de qualquer acordo entre as partes. O processo segue o fluxo regulatório do Banco Central e a decisão final cabe às instituições financeiras. A PixGo é interface tecnológica — não decide, não retém, não libera. Se o estabelecimento quiser reembolsar por conta própria, isso é um processo separado que não interfere na investigação do MED, e eles podem comunicar o fato para registro na contestação.

### Cliente cancelou o MED e fez estorno por conta própria
Mesmo com cancelamento, o processo PRECISA passar pela análise formal da adquirente/banco para dar baixa no registro e garantir conformidade. Explicar:
- O MED precisa ser validado oficialmente pelas instituições
- A análise segue o fluxo mesmo com desistência
- Relembrar prazo de 15-20 dias úteis
- Orientar manter comprovante do estorno particular como evidência

### Cliente diz que vai retirar a contestação (enviou print)
- Registrar documentação recebida
- Explicar que a retirada depende do cliente entrar em contato DIRETAMENTE com o banco emissor
- A PixGo não tem autonomia para cancelar o MED
- A análise segue até decisão da adquirente/banco
- Prazo 15-20 dias úteis

### Cliente sem contato / número de WhatsApp errado
- Solicitar documentos de tentativa de contato (prints de WhatsApp, registros)
- Sem documentação, a contestação pode ser negada pela adquirente
- Explicar que o MED passa por investigação — documentos são essenciais

### Serviço digital (bot Telegram, acesso instantâneo)
- Incluir argumentos da defesa: serviço digital de consumo instantâneo, liberado após confirmação de pagamento
- Cliente aceitou termos de uso com política de reembolso
- Não há reembolso após utilização devido à natureza digital
- Transação foi voluntária — não há fundamento para estorno

### Casos sem anexos
Solicitar documentos específicos que o lojista precisa enviar:
- Prints de tentativas de contato
- Nota fiscal/comprovante de pagamento
- Registros de que o número estava incorreto (se aplicável)
- Explicar que sem documentação a contestação fica prejudicada

## Pitfalls
- **Nunca copiar a mesma resposta duas vezes:** o usuário pediu explicitamente variação. Mudar abertura, ordem dos argumentos, e vocabulário.
- **Não omitir o prazo:** é a reclamação mais frequente — SEMPRE mencionar 15-20 dias.
- **Não se colocar como autoridade de decisão:** deixar claro que PixGo é interface, quem decide é DEPIX/BC.
- **Não julgar o comportamento do cliente:** manter neutralidade. O relato é factual, não emocional.
- **Não prometer resultado:** dizer "pedido de rejeição foi registrado para análise", nunca "vai ser rejeitado".
- **Sempre manter parágrafos: corpo do email bem organizado**, sem bloco de texto contínuo.
- **Plain text**: emails de suporte PixGo são em texto plano, sem formatação HTML/rich text.
- **"Só o texto pra copiar":** quando o Edu pedir apenas o texto (sem formatação extra, explicações ou markdown), entregar APENAS o corpo do email limpo, sem "---", sem cabeçalhos adicionais, sem instruções. Apenas o texto que ele vai copiar e colar.
