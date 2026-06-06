---
name: alexa-integration
description: "Conectar o Hermes Agent ao ecossistema Amazon Alexa (Echo Dot, dispositivos) para comando por voz — servidor webhook Flask, ngrok tunnel, e integração via IFTTT ou Alexa Routines."
version: 1.5.0
platforms: [windows]
tags:
  - alexa
  - smart-home
  - voice
  - webhook
  - ngrok
  - flask
  - ifttt
related_skills: [alexa-voice-bridge, windows-automation]
---

# Alexa + Hermes Agent Integration

## Visão Geral

Permite que o usuário fale comandos para a Amazon Alexa e o Hermes Agent execute ações (postar no X, ver e-mails, buscar notícias, etc.).

**Arquitetura:**
```
Usuário: "Alexa, disparar [comando]"
  → Alexa (Echo Dot)
  → IFTTT Applet (ou Alexa Routine + Maker Webhooks skill)
  → Webhook HTTP POST
  → ngrok tunnel (HTTPS)
  → Servidor Flask local (Windows)
  → Hermes Agent executa comando
```

## ⚠️ REGRA DE OURO — Atenção imediata ao que o usuário passa

**Quando o usuário fornecer qualquer informação diretamente (códigos SMS, instruções, comandos), PARAR IMEDIATAMENTE qualquer fluxo em andamento e usar a informação na hora.**

Isso inclui:
- Códigos de verificação (SMS, email, autenticação em duas etapas)
- URLs, IDs, tokens, senhas
- Instruções sobre como fazer algo ou o que priorizar
- Correções de tom, estilo, formato

**NUNCA:**
- Ignorar uma informação que o usuário passou e tentar um caminho alternativo (ex: o usuário passou o código SMS mas o agente tenta acessar o Gmail do usuário para encontrar o mesmo código)
- Continuar o fluxo que estava em andamento sem processar o que o usuário acabou de dizer
- Ficar repetindo a mesma pergunta se o usuário já respondeu
- Pedir confirmação de algo que o usuário já disse explicitamente

**Quando o usuário reclama** "você não vê o que eu mando" ou "preste atenção" — esse é um sinal de PRIMEIRA CLASSE. Parar tudo, revisar o que o usuário acabou de passar, e agir com base no que ele disse.

**SINAIS DE FRUSTRAÇÃO E PEDIDO DE AUTONOMIA:**

- "ja me irritei" / "ja cansei" / "nao consigo" / "voce nao consegue fazer" — **PARAR IMEDIATAMENTE** qualquer tentativa complexa e pular para o Caminho Simplificado (IFTTT Button widget pelo app). Não continuar tentando a abordagem atual.
- "faca tudo que precisar sem me perguntar" / "to trabalhando" — **NAO FAZER PERGUNTAS.** Usuário quer autonomia total. Não pedir permissão, não sugerir "quer tentar?", não perguntar "o que devo fazer agora?". Executar e reportar resultado. Se algo depender do usuário e ele não forneceu, usar a melhor alternativa disponível e reportar o que foi feito.

**Nota histórica:** O usuário @Cabral_Cripto já explicitou em 04/06/2026 que durante o horário de trabalho não quer ser perturbado com perguntas. Agente deve executar com autonomia máxima e reportar resultados depois.

## Componentes

### 1. Servidor Webhook (Flask)

Arquivo: `~/AppData/Local/hermes/alexa_bridge.py`

Endpoints:
- `GET /` — health check (retorna `{"status": "online"}`)
- `POST /alexa-webhook` — recebe comando da Alexa
- `POST /ifttt-trigger` — endpoint compatível com IFTTT Webhooks

O servidor mapeia comandos de voz para ações do Hermes:
- "postar" → posta thread no X
- "noticias" → busca Degenzone21
- "emails" → lê caixa de entrada
- "med" → responde MEDs
- "resumo" → briefing do dia
- "teste" → testa conexão

### 2. ngrok Tunnel (HTTPS público)

Necessário porque o IFTTT/Alexa Routines precisam de uma URL HTTPS pública para enviar webhooks.

```bash
pip install pyngrok
python -c "from pyngrok import ngrok; print(ngrok.connect(5000, 'http'))"
```

Resultado: URL tipo `https://xxxx.ngrok-free.dev`

### 3. IFTTT Applet (OPÇÃO A — recomendada, mas com limitações)

**⚠️ LIMITAÇÃO CRÍTICA — MESMO NO PLANO PAGO:** "Amazon Alexa" aparece como "Services with no available triggers" no IFTTT, mesmo em contas Pro comuns. A Alexa como trigger só está disponível em contas **Pro+** (~$7/mês) ou via **serviços de terceiros** como "Alexa Voice Monkey", "Alexa Actions by mkZense", "Virtual Buttons" — que têm triggers próprios mas NÃO oferecem "Say a specific phrase" com captura de wildcard.

**Solução real:** Usar **Alexa Routines nativas** (OPÇÃO B abaixo) ou skill "Voice Monkey" que cria comandos de voz na Alexa e dispara webhooks.

**Se o trigger Alexa estiver disponível (verificar em ifttt.com/create → clicar "If This" → pesquisar "Alexa"):**
- IF: Alexa → "Say a specific phrase" → `disparar {{comando}}`
- THEN: Webhooks → "Make a web request"
  - URL: `https://xxxx.ngrok-free.dev/ifttt-trigger`
  - Method: POST
  - Content-Type: application/json
  - Body: `{ "command": "{{comando}}" }`

### 4. Alexa Routines + Maker Webhooks (OPÇÃO B — grátis, recomendada)

Quando o IFTTT grátis não suporta Alexa:
1. Abrir app Alexa no celular
2. Mais → Rotinas → + (criar nova)
3. Quando: Voz → digitar frase (ex: "disparar {comando}")
4. Ação: Adicionar skill → pesquisar "Maker Webhooks" ou "HTTP Request" (skills gratuitas que permitem enviar webhooks)
5. Configurar com a URL do ngrok
6. Salvar

Alternativa: skill "Virtual Buttons" ou "Webhook" na loja de skills Alexa.

## ⚠️ Amazon descontinuou Alexa como trigger do IFTTT (CONFIRMADO)

A integração oficial da Amazon Alexa com IFTTT **foi descontinuada pela Amazon em 2024/2025**. Por isso a Alexa aparece como "serviço sem gatilhos" no IFTTT — só é possível usar a Alexa como **destino da ação**, nunca como disparador (trigger). Isso afeta **TODOS os planos do IFTTT**, inclusive Pro+.

**Conclusão:** Não perder tempo pesquisando ou testando Alexa como trigger no IFTTT. A rota funcional é:
- Voice Monkey (skill Alexa) → webhook próprio → ngrok → Flask → Hermes
- Ou Alexa Routines nativas com HTTP Request (se disponível na região)

### Caminhos Reais que Funcionam

| Abordagem | Custo | Frase de Voz | Complexidade |
|-----------|-------|--------------|--------------|
| **Voice Monkey** (skill Alexa) → Webhook → ngrok → Flask | Grátis | "Alexa, manda {comando}" | Média |
| **Alexa Routines nativas** → HTTP Request → ngrok → Flask | Grátis | "Alexa, {qualquer frase}" | Baixa |
| **Virtual Buttons** (skill Alexa) → IFTTT Webhooks → ngrok → Flask | Grátis | "Alexa, push {botão}" | Baixa |

### Opção Recomendada: Voice Monkey (login com Amazon + 2FA)

[Voice Monkey](https://voicemonkey.io/) é uma skill gratuita da Alexa que permite criar comandos de voz personalizados que disparam webhooks HTTP.

**Setup:**

1. Usuário instala skill "Voice Monkey" no app Alexa
2. Navegar para voicemonkey.io → clicar Console → "Sign in with your Amazon account"
3. **Login Amazon com 2FA:** O login redireciona para a Amazon e pede verificação em duas etapas:
   - Inserir email/senha da Amazon
   - Amazon envia código OTP por SMS para o celular do usuário
   - **O usuário precisa fornecer o código SMS** — o agente NÃO deve tentar acessar o Gmail do usuário para encontrar o código. Se o código não funcionar, pedir um novo código SMS.
4. Após login, criar um "Monkey" (comando virtual):
   - Nome do Monkey: ex: "comando"
   - Frase de ativação: ex: "manda hermes" (assim o usuário fala "Alexa, manda hermes comando")
   - Webhook URL: `https://SEU_NGROK.ngrok-free.dev/ifttt-trigger`
   - Method: POST, Content-Type: application/json
   - Body: `{"command":"{{MonkeyName}}"}`
5. Pronto! Comando natural: **"Alexa, manda hermes teste"**

**⚠️ Atenção com códigos fornecidos pelo usuário:**
Quando o usuário diz que passou um código SMS ou informação, USAR IMEDIATAMENTE. Não tentar caminhos alternativos (acessar Gmail, verificar outro email) — o usuário já forneceu o que precisa.

**⚠️ Códigos SMS expiram rápido:**
Códigos de verificação da Amazon expiram em ~5 minutos. Se o usuário passar um código e ele não funcionar, pedir um **novo código SMS** imediatamente — não tentar reusar códigos antigos ou acessar o email do usuário.

**⚠️ Página vazia após 2FA do Amazon:**
Após inserir o código SMS de verificação da Amazon, o navegador headless (browserbase/Comet) frequentemente fica com snapshot vazio ("empty page"). Isso não significa erro — o redirecionamento ocorreu, mas a página de destino pode ser SPA React. Tentar navegar para URLs conhecidas (`/app/dashboard`) ou voltar para `voicemonkey.io/` e clicar em "Console" novamente para verificar se o login foi bem-sucedido.

**⚠️ Skill já ativada via Alexa app = login parcial:**
O usuário pode ativar a skill "Voice Monkey" diretamente no app Alexa do celular, sem passar pelo console web. Quando isso acontece:
1. A skill está funcional na Alexa, mas o console web (`voicemonkey.io`) ainda requer login Amazon separado
2. Tentar logar no console web dá acesso à configuração avançada (criar Monkeys customizados)
3. Mas mesmo sem o console, a skill funciona com as configurações padrão
4. **Solução pragmática:** se o console web não conseguir logar (2FA looping, página vazia), a skill já está ativa e o próximo passo é usar **Alexa Routines nativas** para criar comandos de voz personalizados que chamam webhooks HTTP — isso não depende do console Voice Monkey

### Opção Alternativa: Alexa Routines Nativas

O app Alexa (iOS/Android) tem suporte nativo a HTTP requests desde 2024, **mas apenas na Alexa americana/inglesa**. Na **Alexa brasileira (idioma português)**, a ação "HTTP Request" ou "Enviar requisição HTTP" **NÃO existe** nas Rotinas. Confirmado empiricamente.

**⚠️ Importante:** Antes de tentar configurar, verificar se a opção existe no app Alexa do usuário. Se não existir (caso do Brasil), as Opções funcionais são:
- **Voice Monkey** (skill grátis) → "Custom Action" na Alexa Routine → webhook (recomendado)
- Virtual Buttons (skill grátis) + IFTTT

### Caminho Funcional: Voice Monkey Flows (recomendado quando HTTP Request nativo não existe)

Documentado no guia oficial: https://voicemonkey.io/guides/how-to-make-an-http-request-from-an-alexa-routine

**Fluxo de 3 passos:**

1. **Criar um Flow no console Voice Monkey:**
   - Console → Flows → New Flow
   - Nome descritivo (ex: "Hermes Comando")
   - Adicionar ação **Web Request**
   - URL: `https://SEU_NGROK.ngrok-free.dev/ifttt-trigger`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body: `{"comando":"{{utterance}}"}`

2. **Copiar a frase de Custom Action** que o Flow gera (ou anotar o **Request Ref** de 4 dígitos)

3. **Criar Alexa Routine:**
   - App Alexa → Mais → Rotinas → + (nova rotina)
   - **Quando:** Voz → digitar frase de gatilho (ex: "manda hermes")
   - **Ação:** Adicionar → **Custom Action** → colar a frase do Flow
   - Salvar

**Comando natural:** "Alexa, manda hermes" (ou a frase que escolheu)

#### Voice Monkey API v3 — Endpoints Conhecidos

A API v3 tem endpoints limitados. Endpoints confirmados funcionais:

| Endpoint | Método | Exemplo | Funcionalidade |
|----------|--------|---------|----------------|
| `/devices?token=TOKEN` | GET | Lista dispositivos Echo vinculados | Funciona ✅ |
| `/flow?token=TOKEN&flow=FLOW_REF` | GET | Retorna informações do flow (flowId, flowName, requestRef) | Funciona ✅ |
| `/flow?token=TOKEN&flow=FLOW_REF&include=nodes` | GET | Mesmo sem nodes — não lista nodes mesmo com `include=nodes` | Funciona mas sem nodes ❌ |
| `/flow?token=TOKEN` | POST | Adicionar parâmetros via query string — **confirmado que retorna 200 com dados do flow, mas NÃO confirma se nodes foram adicionados.** O POST em `/flow` com query params retorna o flow data normal, sem evidência de que a configuração foi aplicada. | ✅ Response 200 mas não confirma node adicionado |
| `/flow?token=TOKEN` | POST + body JSON | `{"flow":2916,"action":"add_node","node_type":"web_request"}` | ❌ `FLOW_NOT_FOUND` |
| `/flow?token=TOKEN` | PUT | Qualquer body | ❌ 405 Method Not Allowed |
| `/trigger?device=DEVICE_ID&token=TOKEN&flow=FLOW_REF` | GET/POST | Dispara o flow | ✅ Response `{"success":true,"data":"OK"}` |
| `/flow/node?token=TOKEN` | POST | Tentativa de adicionar node | ❌ 404 |
| Qualquer outro endpoint | GET/POST | 404 | ❌ |

**Conclusão sobre a API v3:** A API é **read-only para configuração**. GET funciona para ler devices e flow info. POST em `/flow` com query params não adiciona nodes — apenas o console web pode configurar ações nos flows. A API só serve para: listar devices, ler flow info, e **triggerar execution**.

┼ A API é read-only para configuração: GET funciona para ler devices e flow info. POST em /flow com query params NAO adiciona nodes — retorna 200 com dados do flow mas a configuracao nao e persistida. Apenas o console web pode adicionar nodes de acao (Web Request) aos flows. A API so serve para: listar devices, ler flow info, e triggerar execution.

**Token format:** UUID-like com hifens: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX (grupo de caracteres separados por hifen, sem prefixo como vm)

**Trigger URL para disparar flow por API:**
```
https://api-v3.voicemonkey.io/trigger?device=DEVICE_ID&token=SEU_TOKEN&flow=FLOW_REF
```
Onde `DEVICE_ID` é o ID do Echo (ex: `bedroom-echo-5zhh7`), `TOKEN` é o token da API, e `FLOW_REF` é o número de 4 dígitos.

**⚠️ Limitação crítica da API v3:** Não é possível adicionar ou configurar nodes/ações via API. O node Web Request precisa ser adicionado manualmente no console web. A API só permite: listar devices, ver info do flow, e **triggerar** o flow. Configuração de ações (URL, method, body, headers) é exclusivamente via console web.

#### Criando Flow com Web Request — Guia Visual para o Usuário

Quando o usuário estiver no console `app.voicemonkey.io/flows` após criar um Flow:

1. **Após criar o Flow com um nome** (ex: "Hermes Comando"), a tela mostra o **Trigger Methods** (API Trigger URL + Request Ref)
2. O usuário precisa **adicionar uma Ação** (node) ao Flow — procurar por um botão de "+" ou "Add Node" ou "Add Action"
3. Na lista de ações, procurar **"Web Request"**
4. Preencher: URL, Method (POST), Headers (Content-Type: application/json), Body
5. Salvar

**Se o usuário não entender a interface ou se irritar com a complexidade, sugerir o Caminho Simplificado abaixo.**

#### Caminho Simplificado (Usuário Não-Técnico)

Se o usuário não conseguir configurar o Flow manualmente (interface confusa, se irritou):

1. **Já instalar a skill "Voice Monkey" na Alexa** — pelo app Alexa no celular: Skills → buscar "Voice Monkey" → Ativar
2. **Criar Alexa Routine** com ação **Custom Action**:
   - App Alexa → Mais → Rotinas → + (nova rotina)
   - Quando: Voz — "manda hermes [comando]"
   - Ação: Adicionar → **Custom Action**
   - Na frase, usar o Request Ref de 4 dígitos do flow criado
   - Salvar
3. **Testar direto** — o usuário fala "Alexa, manda hermes teste" e a skill responde

**Fallback final — IFTTT + Button widget (mais simples, MAS NAO CONFIRMADO FUNCIONAL):**
1. Usuario abre app IFTTT no celular
2. Cria Applet: **Button widget** (trigger) → **Webhooks > Make a web request** (action)
3. URL: URL do ngrok, Method: POST, Content-Type: application/json, Body: `{"comando":"teste"}`
4. Aperta o botao no widget do IFTTT
5. ⚠️ RESULTADO EMPIRICO: **O Applet aparece como "Connected" mas o webhook NAO E ENVIADO para a URL configurada.** O ngrok/Flask nao recebe requisicao alguma vinda do IFTTT. O body customizado (`{"comando":"teste"}`) nunca chega ao servidor.

**Causas provaveis (nao isoladas):**
- O servico "Button widget" precisa ser **conectado/ativado separadamente** no IFTTT (aba Explore → Button widget → Connect) antes de funcionar como trigger
- O formato de body customizado e ignorado pelo trigger Button widget — ele so enviaria `{"value1":"...","value2":"...","value3":"..."}` se enviasse algo
- O webhook pode ser disparado apenas quando o widget e **adicionado fisicamente na aba Widgets do app** e apertado, nao quando o Applet e run pela aba My Applets

**Solucao alternativa que funciona independentemente:** API Maker Webhooks direta:
```
curl -X POST "https://maker.ifttt.com/trigger/hermes_comando/with/key/SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"value1":"teste"}'
```
Retorna `Congratulations! You've fired the hermes_comando event` — funciona mesmo sem Applet.

**⚠️ "Nao encontrei o botao/Applet" apos criar:** Se o usuario criou o Applet mas nao acha o botao para apertar:
   - Abrir app IFTTT → aba **My Applets** (inferior, icone de grade quadrada)
   - Clicar no Applet recem-criado
   - Dentro dele, deve ter botao **"Run"** ou **"Check now"**
   - Alternativa: aba **Widgets** (inferior, ícone de widget/grid) → adicionar o widget manualmente
   - Se ainda não achar, pedir pro usuário usar a **aba "My Applets" → clicar no Applet → Run**

**⚠️ IFTTT Button widget envia formato value1/value2/value3 (CONFIRMADO POR TESTE):** O Webhooks do IFTTT não envia `{"comando":"teste"}` como configurado — ele ignora o Body configurado e envia o payload padrão do Button widget: `{"value1":"","value2":"","value3":""}`. O servidor Flask PRECISA tratar esse formato como fallback (ver template `alexa-bridge-server.py` que já faz isso), extraindo comando de `value1` se `comando` não existir.

**⚠️ ngrok não sobrevive a restart/desligamento:** O ngrok cai quando o processo morre. **SEMPRE verificar infraestrutura ANTES de pedir pro usuário testar ou apertar qualquer botão.** Protocolo obrigatório:
1. `curl http://localhost:4040/api/tunnels` — ngrok online?
2. `curl http://localhost:5000/` — Flask respondendo?
3. Se ngrok offline: religar com `ngrok http 5000 --domain DOMINIO_EXISTENTE`
4. Se Flask offline: matar processos antigos na porta 5000 via PowerShell, reiniciar
5. Só depois pedir pro usuário testar. Caso contrário o usuário aperta o botão e nada acontece, gerando frustração.

**Preferência do usuário: autonomia total durante trabalho:** O usuário explicitamente pediu "faça tudo que precisar sem me pedir ajuda pois estou trabalhando agora". Quando isso for dito:
- NÃO fazer perguntas, mesmo opcionais
- NÃO pedir permissão para ações
- NÃO sugerir "quer tentar?" ou "o que devo fazer agora?"
- Executar com autonomia máxima e reportar resultados depois
- Se algo depender do usuário e ele não forneceu, usar a melhor alternativa disponível

**Health check:** Usar `curl http://localhost:5000/` em vez de depender do stdout do processo Flask.

**Nota:** O guia oficial é para Voice Monkey v2 e pode estar parcialmente desatualizado para v3. O console web atual (v3) tem dashboard diferente — se links levarem a 404, acessar `app.voicemonkey.io/flows` diretamente ou pedir pro usuário criar manualmente no dashboard.

### Opção Alternativa: Virtual Buttons + IFTTT (se já tiver IFTTT configurado)

1. Instalar skill "Virtual Buttons" na Alexa (gratuita)
2. Criar botão "comando" na skill
3. No IFTTT: Webhooks trigger (Receive a web request) + Webhooks action (Make a web request para ngrok)
4. Falar: **"Alexa, push comando"** — não precisa de "apertar" se o cliente criar o botão com o nome que preferir

### O que NÃO funciona mais
- ❌ IFTTT Applet com Alexa como trigger (descontinuado pela Amazon em TODOS os planos)
- ❌ Virtual Buttons como trigger do IFTTT não permite frases customizadas — só "Alexa, push {nome_do_botão}"

## Setup Completo (Primeira Vez)

### 1. Instalar dependências

```bash
pip install flask pyngrok requests
```

### 2. Criar servidor

O servidor está em `~/AppData/Local/hermes/alexa_bridge.py` — contém:
- Servidor Flask na porta 5000
- Mapeamento de comandos para ações
- Log de comandos recebidos

### 3. Iniciar servidor + ngrok

```bash
# Terminal 1: servidor Flask
cd ~/AppData/Local/hermes && python alexa_bridge.py

# Terminal 2: ngrok tunnel
python -c "from pyngrok import ngrok; print(ngrok.connect(5000, 'http'))"
```

A URL pública gerada pelo ngrok expira a cada sessão — é necessário reiniciar o ngrok sempre que reiniciar o computador.

### 4. Expor comandos para o usuário

O usuário precisa saber quais frases funcionam. Exemplos:

| Falar pra Alexa | Ação |
|----------------|------|
| "Alexa, disparar teste" | Testa conexão |
| "Alexa, disparar notícias" | Busca Degenzone21 |
| "Alexa, disparar e-mails" | Lê caixa de entrada |
| "Alexa, disparar postar" | Posta no X |

## Falha Comum: Popup de Upgrade do IFTTT Grátis ao Criar Applet

### O Problema

No **plano grátis do IFTTT** (limite de 3 applets, usuário pode ter 1 já criado), ao tentar criar um novo Applet via navegador, mesmo com Webhooks pré-selecionado, um popup **"Get more Applets"** aparece bloqueando o fluxo:

```
Get more Applets
IFTTT Pro+ is billed at $107.88 per year...
Nevermind | Upgrade to Pro+
```

Clicar em **"Nevermind"** fecha o popup, mas o fluxo de criação não avança — a escolha de trigger/ação fica travada. Esse popup reaparece em cada tentativa de navegar para `/create`.

### Solução 1: Usar a API Maker Webhooks Direta (funciona sem Applet)

Mesmo sem Applet criado, a API do IFTTT Maker Webhooks **responde 200** para triggers diretos:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  "https://maker.ifttt.com/trigger/alexa_comando/json/with/key/l4S9mL9sss70rz8MgCOPIwQ3-_BsNc9jMGzaxlOE05E"
# Retorna 200
```

A URL de trigger direto é:
```
https://maker.ifttt.com/trigger/{event}/json/with/key/{SUA_CHAVE}
```

Isso significa que a infraestrutura já está funcional mesmo sem Applet visível — o trigger funciona. O Applet só é necessário para **rotear** o trigger para uma ação específica (ex: chamar o ngrok). Mas como a API já aceita o trigger, o próximo passo é criar o Applet (ver Solução 2 ou 3).

### Solução 2: Criar Applet via CDP (Chrome real do usuário)

**⚠️ IMPORTANTE — SINAL DE FRUSTRAÇÃO DO USUÁRIO:** Se o usuário diz "ja me irritei", "ja cansei", "nao consigo" ou qualquer expressão de frustração com Voice Monkey ou IFTTT, PARAR IMEDIATAMENTE e pular para o Caminho Simplificado (Solução 3 ou Fallback IFTTT Button widget). Usuário frustrado não quer mais configuração — quer algo que funcione AGORA.

Quando o Chrome real do usuário está aberto com `--remote-debugging-port=9222` e a sessão do IFTTT ainda está ativa, o fluxo de criação via **websocket CDP** funciona, mas requer atenção:

**Checklist de verificação:**
```bash
# Verificar se a sessão IFTTT está ativa
curl -s http://127.0.0.1:9222/json | grep -i ifttt
# Se mostrar URL com /explore ou /create, sessão OK
# Se mostrar /join ou /login, sessão expirou
```

**Criação passo a passo (via browser headless/CDP):**

1. Navegar para `https://ifttt.com/create`
2. Clicar **Add** no "If This" (o botão está em um `<generic>` com ref que pode variar)
3. Buscar por **"Button widget"** (não "Webhooks" como trigger — Button widget é o trigger mais simples que funciona)
4. Clicar no resultado "Button widget"
5. Na tela "Choose a trigger", selecionar a primeira opção (Button press)
6. Clicar **Add** no "Then That"
7. Buscar por **"Webhooks"**
8. Clicar "Webhooks" → "Make a web request"
9. Preencher campos:

| Campo | Técnica de preenchimento no React SPA |
|-------|---------------------------------------|
| URL | `input[name*="url"]` — usar `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(el, url)` + `el.dispatchEvent(new Event('input', {bubbles:true}))` |
| Method | `document.querySelectorAll('select')[0].value = 'POST'; select.dispatchEvent(new Event('change', {bubbles:true}))` |
| Content-Type | `document.querySelectorAll('select')[1].value = 'application/json'; select.dispatchEvent(new Event('change', {bubbles:true}))` |
| Body | `textarea[name*="body"]` — `Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(el, body)` + `el.dispatchEvent(new Event('input', {bubbles:true}))` |

10. Clicar **Create action** — buscar com `[...document.querySelectorAll('button')].find(b => b.textContent.trim() == 'Create action')`
11. Se o clique não funcionar (página não muda), verificar no console JS se há erros de validação ocultos
12. Se ainda assim travar, pedir pro usuário fazer manualmente (~2 min via app IFTTT no celular)

**⚠️ Limitações do CDP com IFTTT (React SPA):**

- O `Runtime.evaluate` pode falhar silenciosamente em páginas React SPA que usam `cross-origin-isolated` ou CSP restritivo. Se `document.body.innerText` retornar vazio mesmo após 5s de espera, a página não montou.
- **Sessão expirada:** IFTTT invalida sessões após ~30min de inatividade. Quando expira, o React não monta e o CDP evaluate retorna vazio. Recarregar a página ou relogar via `https://ifttt.com/login`.
- **Clicar em elementos:** O IFTTT Renderiza cards como `<a>` tags com textContent visível. Usar `document.createTreeWalker` para encontrar o nó de texto e subir 5 níveis no parentElement procurando `<a>`.
- **Selects não têm `id`:** Os selects de Method e Content-Type não têm atributo `id`. Identificar por index (`select[0]`, `select[1]`) ou por `name`.
- **Textareas do formulário Web Request se confundem entre navegações:** O IFTTT React re-renderiza o formulário quando o clique no botão "Create action" falha por validação. O conteúdo do campo Body pode aparecer no campo "Additional Headers" e vice-versa. Estratégia: usar `document.querySelectorAll('textarea')` e indexar por posição (0=URL, 1=Headers, 2=Body) — re-preenche tudo antes de cada tentativa de clique.
- **Eventos de change em select não propagam para o React state:** `select.value = 'POST'` + `select.dispatchEvent(new Event('change', {bubbles: true}))` nem sempre acorda o React. Tentar `Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set.call(select, 'POST')` + `select.dispatchEvent(new Event('change', {bubbles: true}))`.
- **Botão "Create action" via CDP pode parar de responder:** Após clicar e a página re-renderizar com os mesmos campos (incluindo lista de ingredientes do trigger), o React desabilitou silenciosamente o botão — o `dispatchEvent(new MouseEvent('click'))` retorna `false` (preventDefault foi chamado). Nesse caso, parar de tentar e pular para o caminho alternativo: usuário fazer via app mobile (~2 min) ou usar API Maker Webhooks direta.

**Reset de senha (conta criada via Google):**
Se a sessão expirou e precisa relogar mas a conta foi criada via "Continue with Google", Google bloqueia o Comet/headless browser. Solução:
1. Navegar para `https://ifttt.com/login`
2. Clicar **"Forgot your password?"**
3. Digitar o email Gmail
4. Dizer ao usuário para verificar o Gmail (no celular ou no Chrome real) e clicar no link de reset
5. Usuário cria nova senha
6. Logar com email + senha (não botão do Google) — campos:
   - Email: `input#user_username`
   - Senha: `input#user_password`
   - Submit: `input[type="submit"]`

### Solução 3: Pedir pro usuário fazer manualmente (~2 minutos)

Quando as soluções automáticas falham (sessão expirada sem acesso ao Gmail, React não renderizando), pedir pro usuário:
1. Abrir `https://ifttt.com/create` no Chrome (onde já está logado no Google)
2. If This → Add → Webhooks → "Receive a web request with a JSON payload"
3. Event Name: `alexa_comando` → Create trigger
4. Then That → Add → Webhooks → "Make a web request"
5. Preencher URL, Method POST, Content-Type JSON, Body `{"comando":"{{EventName}}"}`
6. Create action → Continue → Save

### Extrair Chave da API Maker Webhooks

```bash
# Via CDP: navegar para https://ifttt.com/maker_webhooks/settings
# A chave aparece no campo "URL": https://maker.ifttt.com/use/SUA_CHAVE_AQUI
```

Trigger URL direto: `https://maker.ifttt.com/trigger/{event}/json/with/key/{key}`

### Fluxo Alternativo: Virtual Buttons (Alexa skill) + IFTTT Webhooks

Se o IFTTT grátis não permite criar Applets com Alexa trigger:
1. Usuário instala skill **"Virtual Buttons"** na Alexa
2. Cria botão "teste" na skill
3. No IFTTT: Webhooks trigger (Receive a web request) + Webhooks action (Make a web request para o ngrok)
4. Usuário fala: "Alexa, push teste" → Virtual Buttons → envia webhook para o IFTTT → IFTTT encaminha para ngrok → Flask → Hermes

## ⚠️ Nota de Consolidação

Esta skill (`alexa-integration`) e a skill `alexa-voice-bridge` (smart-home/) cobrem o mesmo território em português e inglês, respectivamente. Esta versão PT-BR é mais completa. `alexa-voice-bridge` foi **absorvida** aqui — templates e referências migrados.

## Pitfalls

- **ngrok URL muda a cada reinicialização** do ngrok — a URL pública expira. Precisa gerar nova URL e atualizar no IFTTT/Routines.
- **Plano grátis IFTTT bloqueia criação de Applets com popup de upgrade.** Mesmo com Webhooks pré-selecionado, o popup "Get more Applets" aparece ao tentar criar. A API Maker (`/trigger/{event}/json/with/key/{key}`) funciona independentemente — retorna 200 mesmo sem Applet configurado.
- **CDP + React SPA = frágil.** O IFTTT é uma SPA React que não renderiza confiavelmente via CDP websocket evaluate. `Runtime.evaluate` pode retornar vazio mesmo com a página carregada. Preferir extrair cookies via `Network.getCookies` e fazer chamadas curl com esses cookies, OU pedir pro usuário fazer manualmente.
- **Sessão IFTTT expira silenciosamente** após ~30min de inatividade. Sintoma: CDP evaluate retorna vazio, curl em `/json` mostra URL `/join`. Solução: relogar via formulário de login (não Google).
- **Google bloqueia Comet/headless.** Contas IFTTT criadas via Google não podem relogar no Comet. Fazer reset de senha via "Forgot password?" e logar com email+senha.
- **Sempre usar informação que o usuário passa na hora.** Se o usuário diz "recebi o código XXXX" ou "preste atenção no que te passei" — PARAR qualquer fluxo, revisar o que ele passou, e agir imediatamente. **Nunca** ignorar a informação do usuário e tentar um caminho alternativo.
- **ngrok free tier:** 40 conexões/minuto, túnel expira após ~2h de inatividade, URL muda a cada restart.
- **Firewall Windows:** porta 5000 pode estar bloqueada. O Flask roda em `0.0.0.0` (acessível na rede local), mas o ngrok contorna firewalls externos.
- **Python environment:** o Flask e pyngrok precisam estar no mesmo Python que executa o servidor. Verificar com `python -c "import flask; print('ok')"`.
- **Voice Monkey + Amazon 2FA:** O login do Voice Monkey redireciona para a Amazon, que exige verificação em duas etapas. O fluxo típico: email/senha → Amazon envia SMS OTP → usuário passa o código SMS. **Não tentar acessar o Gmail do usuário para achar o código** — pedir o código SMS e usar imediatamente quando o usuário fornecer. Códigos expiram em ~5 minutos; se falhar, pedir código NOVO.
- **Skill Voice Monkey pode ser instalada diretamente no app Alexa** (sem web console). O usuário faz "Skills → buscar Voice Monkey → Ativar". Nesse caso a skill funciona mas o console web ainda requer login separado. Se o console web não conseguir logar, a skill já está operacional — usar com Alexa Routines nativas.
- **Snapshot vazio "empty page" após Amazon 2FA é normal** — o redirecionamento ocorreu. Tentar navegar diretamente para `voicemonkey.io/` e clicar "Console" novamente, ou verificar login por navegação para sub-URLs.
- **Voice Monkey comando padrão abre música:** Quando o usuário fala "Alexa, pedir pro Voice Monkey" sem configuração personalizada, a skill responde com áudio/música padrão. Para evitar isso, criar Monkeys personalizados no console web. Se o console não estiver acessível, usar a skill apenas como trigger em Alexa Routines nativas.
- **Voice Monkey UI v3 é confusa para usuários não-técnicos:** O dashboard v3 reorganizou "Monkeys" como "Flows", e a interface do Flow editor mostra o trigger "Start" sem indicar claramente como adicionar ações. Usuários podem ficar perdidos. Estratégia: guiar passo a passo via texto curto (usuário no celular) OU pular para o caminho simplificado (IFTTT Button widget) que é mais direto.
- **"Ja me irritei" = mudar de estrategia imediatamente:** Quando o usuario diz que se irritou com Voice Monkey ou IFTTT, NAO continuar tentando. Pular para o caminho mais simples disponivel. Usuario frustrado nao quer mais configuracao, quer algo que funcione AGORA.
- **ngrok/Flask pode estar offline quando o usuario aperta o botao:** SEMPRE verificar a infraestrutura ANTES de pedir pro usuario testar. Protocolo: (1) `curl http://localhost:4040/api/tunnels` — ngrok rodando? (2) `curl http://localhost:5000/` — Flask respondendo? (3) Soh pedir pro usuario apertar o botao se ambos estiverem OK.
- **IFTTT Button widget emite webhook mas ngrok nao recebe:** Mesmo com `curl -X POST` no ngrok funcionando perfeitamente, o IFTTT Button widget pode estar disparando mas o webhook nunca chega ao servidor. O Applet fica "Connected" mas nao entrega. Suspeita: o servico Button widget precisa ser ativado/conectado separadamente no IFTTT antes de funcionar como trigger.
