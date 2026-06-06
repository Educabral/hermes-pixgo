---
name: pixgo-base
description: "Base de conhecimento completa da PixGO — API, regras de negócio, níveis, taxas, wallet, saques, troubleshooting. Baseado no blog oficial pixgo.org/blog (42 artigos). Versão Master Junho/2026."
version: 3.0.0
author: Eduardo Cabral
---

# PixGo - Base de Conhecimento Master

## Sobre a PixGo
- **Empresa:** americana (não brasileira)
- **O que faz:** transforma PIX em DEPIX (stablecoin 1:1 BRL) na Liquid Network (sidechain do Bitcoin/Blockstream)
- **Sites:** [pixgo.org](https://pixgo.org) | [Dashboard](https://pixgo.org/dashboard) | [Wallet](https://wallet.pixgo.org) | [Chamados](https://pixgo.org/chamados) | [Blog](https://pixgo.org/blog) | [Afiliados](https://pixgo.org/afiliados)
- **Suporte:** Chat Naka (botão verde canto inferior direito) — consulta status em tempo real com ID do depósito
- **PSPs regulados BCB:** Fitbank (CNPJ 13.203.354/0001-00) e PLEBANK (CNPJ 43.375.652/0001-13)
- **LGPD:** dados mascarados — só vê primeiro nome e final do CPF do pagador
- **Afiliados:** herdam nível do parent_user_id (conta principal)

## DEPIX (stablecoin)
- **Rede:** Liquid Network (sidechain Bitcoin, Blockstream)
- **Lastro:** 1 DEPIX = R$ 1,00
- **Endereços:** lq1... ou VJL...
- **Autocustódia:** seed de 12 palavras (sua, não da PixGo)
- **Transações Confidenciais:** valor oculto na blockchain
- **NÃO é:** ERC-20 (Ethereum), BEP-20 (BNB Chain), Bitcoin (bc1...), saldo bancário
- **Custódia temporária:** enquanto não cai na wallet, fica em custódia interna (proteção MED). Após cair na wallet, 100% seu.

## D+1 — Liquidação (DIA CORRIDO, não útil!)
- **Regra:** PIX hoje, DEPIX amanhã até 23:59
- D+1 = **DIA CORRIDO** (sábado, domingo, feriado contam!)
- **Não existe D+0**
- **Não tem horário fixo** (pode cair 9h, 15h ou 23:59)

**Tabela completa:**
| Pagou em → | DEPIX cai até |
|---|---|
| Segunda | Terça (23:59) |
| Terça | Quarta (23:59) |
| Quarta | Quinta (23:59) |
| Quinta | Sexta (23:59) |
| Sexta | SÁBADO (sim!) |
| Sábado | DOMINGO (sim!) |
| Domingo | Segunda |
| Véspera feriado | Feriado (sim!) |

**Por que D+1?** Custódia regulatória (BCB), janela de segurança anti-MED, processamento em lote na Liquid, compliance antilavagem.
**Se passou D+2 sem cair → investigar** (endereço Liquid, status no dashboard).

## Taxas Completas

### Entrada (PIX → DEPIX)
| Faixa | Taxa PixGo |
|---|---|
| Até R$50 | 2% + R$1,00 fixo |
| Acima de R$50 | 2% (sem fixo) |

### Envio D+1 (para wallet)
- R$0,50 fixo

### Fórmulas
- **valor > R$50:** Líquido = valor × 0,98 - 0,50
- **valor ≤ R$50:** Líquido = (valor × 0,98) - 1,00 - 0,50

### Exemplos
| Valor | Taxa | Recebe |
|---|---|---|
| R$10 | R$1,70 | R$8,30 |
| R$30 | R$2,10 | R$27,90 |
| R$50 | R$2,50 | R$47,50 |
| R$100 | R$2,50 | R$97,50 |
| R$500 | R$10,50 | R$489,50 |
| R$1.000 | R$20,50 | R$979,50 |

### Não tem
Mensalidade, taxa de cadastro, multa para sair, contrato de fidelidade, taxa para gerar QR (ilimitado).

### Taxas de saída (depois do D+1)
- CryPix/Botão Pix: taxa própria CryPix (varia)
- BRSwap: spread próprio
- Buy Crypto: ~1% spread
- Gas Station: ~R$0,50

## Limites (3 Regras Principais)

### 1. Por QR Code (seu nível)
| Nível | QR até |
|---|---|
| Iniciante | R$300 |
| Bronze | R$600 |
| Prata | R$1.000 |
| Ouro | R$1.500 |
| Pro | R$2.000 |
| Master | R$2.500 |
| Elite | R$3.000 |

### 2. R$6.000/dia por CPF pagador
- Soma todos PIX do cliente no dia
- Reseta meia-noite BRT
- Se bater, PIX é rejeitado pelo PSP
- Solução: esperar 1 dia ou usar outro CPF

### 3. 3 PIX em 30 minutos (mesmo CPF)
- Janela rolante de 30 minutos
- Regra antifraude do PSP
- Solução: esperar 30 min ou consolidar valores

### Limites extras
- **Buy Crypto Wallet:** R$500/dia acumulado (mín R$10)
- **Botão Pix Wallet:** mínimo R$100 por operação

## Níveis de Conta (7 Níveis)

**Progressão automática** (cron roda 1x/dia na madrugada — sem solicitar, sem chamado):

| Nível | Requisitos | QR até |
|---|---|---|
| Iniciante | Dia 0 | R$300 |
| Bronze | 7 dias + 1 venda | R$600 |
| Prata | 15 dias + 5 vendas | R$1.000 |
| Ouro | 30 dias + 15 vendas | R$1.500 |
| Pro | 60 dias + 50 vendas | R$2.000 |
| Master | 90 dias + 150 vendas | R$2.500 |
| Elite | 180 dias + 500 vendas | R$3.000 |

**Critérios:** tempo + vendas + volume + reputação + diversidade pagadores
**Ver nível:** /depix → botão "Nível" (modal mostra tudo)
**MED perdido (refunded):** DESCONTA do volume acumulado + CONGELA nível 30-60 dias
**MED vencido:** NÃO afeta (sobe normal)
**QRs:** ILIMITADOS por dia (só valor individual é limitado)
**Afiliados:** herdam nível do parent_user_id

### Dicas para acelerar
1. Diversificar pagadores
2. Manter regularidade
3. Zero MED/chamados contra
4. Completar cadastro
5. Configurar Minha Loja (vendas contam **DOBRADO**)
6. Não mudar dados sensíveis com frequência

**Não acelera:** pagar terceiros, auto-vendas, padrões anômalos.

### Para valores acima do nível
1. Dividir em 2 QRs
2. Esperar subir de nível
3. Usar checkout da Minha Loja

## QR Code

### Prazos de expiração
| Tipo | Prazo |
|---|---|
| DEPIX avulso (/depix) | 20 min (fixo) |
| Cobrança Loja (/loja) | 30 min (configurável 5min-24h) |
| QR via API v1 | Default 1800s (configurável, max 86400s=24h) |
| Cobrança recorrente | 1 dia útil cada ciclo |

### Se cliente pagar QR expirado
1. Banco detecta e bloqueia → sem prejuízo
2. PSP detecta e rejeita → valor volta em ~24h
3. Caso raro de processar → DEPIX cai normal

**Em TODOS os casos: cliente NÃO perde dinheiro.**

**Reemissão:** gratuita e ilimitada. O mesmo link da Loja (pixgo.org/pay/ID) reaproveita automaticamente.

**QR fixo:** QR Code estático para loja física (não expira).

## PixGo Wallet
- **URL:** https://wallet.pixgo.org
- **Redes:** Liquid + Bitcoin + 7 redes EVM
- **Autocustódia:** seed de 12 palavras (NUNCA fotografar — anotar em PAPEL, guardar em local seguro)
- **App Android disponível**
- **Senha:** mínimo 8 caracteres, maiúscula + número

### Funcionalidades
| Funcionalidade | Descrição |
|---|---|
| Botão Pix (CryPix) | DEPIX → PIX direto, mín R$100, instantâneo |
| Buy Crypto | Comprar cripto com PIX, R$500/dia, mín R$10, ~1% spread |
| Cobrar | Gerar QR direto da wallet |
| Swap interno | DEPIX → USDt-Liquid (rápido, fee baixa) |
| Swap cross-chain (BRSwap) | DEPIX → USDT em ETH/Polygon/BNB/Tron/Solana/Arbitrum/Base (mín 15 DEPIX) |
| Gas Station | Converte DEPIX/USDt em L-BTC automaticamente |
| Cartão Ether.fi | Crypto → BRL via cartão internacional |

**Tokens suportados:** DEPIX, USDt-Liquid, L-BTC, BTC, ETH, USDT (várias redes)

## Como Sacar DEPIX (4 Caminhos)

### 1. Botão Pix da Wallet
- DEPIX → PIX direto pra conta bancária
- **Mínimo:** R$100
- **Taxa:** variável (CryPix, visível antes de confirmar)
- **Chaves:** qualquer chave PIX (CPF, CNPJ, email, telefone, aleatória)
- **Passo a passo:** Wallet → Portfolio → "Pix" → Logar/criar CryPix (1x) → Informar chave → Valor → Confirmar → Instantâneo
- Funciona 24/7/365, qualquer banco BR

### 2. Swap para USDT/USDC
- **Swap interno:** DEPIX → USDt-Liquid (rápido, fee baixa)
- **Swap cross-chain (BRSwap):** DEPIX → USDT em Ethereum, Polygon, BNB Chain, Tron, Solana, Arbitrum, Base (mín 15 DEPIX)
- **Ether.fi:** Swap → USDT → recarregar Ether.fi (KYC obrigatório). Redes: ETH, Base, Arbitrum, Optimism, Solana, Tron. **POLYGON NÃO FUNCIONA (perde fundos)**

### 3. Cartão Ether.fi
- Swap → USDT → recarregar Ether.fi
- KYC obrigatório
- **POLYGON NÃO FUNCIONA** — perde fundos

### 4. Peg Out para Bitcoin
- Swap DEPIX → BTC (mainnet)
- 10-30 min confirmação
- Taxa BTC ~R$5-30

## Gas Station Liquid
- Toda transação Liquid precisa de L-BTC (gas) ~R$0,02-0,10
- Gas Station: converte DEPIX/USDt em L-BTC automaticamente
- Aparece como **banner amarelo** quando precisa
- Custo: R$0,50 a R$2,00 por uso
- **Atômico** (transação única, sem risco de perda)
- **NÃO precisa para RECEBER DEPIX** (só para enviar/trocar)
- **NÃO existe** Gas Station para Ethereum/Polygon/Tron/etc.

## Minha Loja / Checkout
- **Link personalizado:** pixgo.org/pay/SEU_ID
- Mostra seu nome e logo
- Gera QR dinamicamente
- Suporta descrição, valor, imagem
- **Configurar:** Dashboard → Minha Loja → Criar checkout
- **QR fixo:** QR Code estático para loja física (não expira)
- **Vendas contam DOBRADO** para reputação/nível

## API PixGo
- **Base:** https://pixgo.org/api/v1
- **Auth:** Header "X-API-Key: pk_..." (gerar em /minha-loja → API Keys)
- **Rate limit:** 10.000 req/24h default
- **Atenção:** toda chave é PRODUÇÃO (não tem sandbox)

### Endpoints
| Método | Rota | Descrição |
|---|---|---|
| POST | /api/v1/payment/create | Criar pagamento |
| GET | /api/v1/payment/{id} | Consultar status |
| DELETE | /api/v1/payment/{id} | Cancelar |

**POST /payment/create fields:** amount (obrig, min R$10), description, external_id, receiver_name, receiver_cpf, receiver_email, receiver_phone, webhook_url
**Response:** payment_id, qr_code, qr_image_url, expires_at

### Webhooks
4 eventos: payment.pending, payment.confirmed, payment.expired, payment.refunded
Assinatura: HMAC-SHA256 (header X-Webhook-Signature)

## Banco Acusa Conta Suspeita
Aparece "Fitbank" ou "PLEBANK" no comprovante? **NORMAL.** São PSPs regulados pelo Banco Central.

### Script para cliente
"Oi! Isso é normal. O PIX que você está pagando vai para Fitbank (ou PLEBANK), que é o PSP regulado pelo Banco Central que processa pagamentos da PixGo. É a mesma estrutura que Mercado Pago, Stone, PagSeguro usam. Pode prosseguir tranquilamente — é instituição autorizada BCB."

### Se o banco TRAVAR
1. Tentar de novo confirmando o alerta
2. Usar outro banco/conta
3. Pagar pelo internet banking (não app)
4. Ligar pro banco e desbloquear
5. Gerar novo QR (se expirou)

**Bancos que mais alertam:** Nubank, Inter, Itaú, Bradesco, BB, Caixa

### Boas práticas
- Descrição clara no QR
- Avise o cliente antes
- Use Minha Loja com sua marca
- Valores altos: fracione

## PIX Não Caiu — Diagnóstico

### Checklist (4 Passos)

**Passo 1 — Status no Dashboard**
| Status | Significado |
|---|---|
| pending | Sistema viu QR, PIX não processou (aguarde até 1h) |
| completed | PIX confirmado! Só aguardar D+1 |
| expired | QR venceu sem pagamento |
| MED | Contestação em análise |
| refunded | Estorno definitivo |

**Passo 2 — ID do Depósito**
32 caracteres hex (ex: 019c8b91-49ec-7433-a506-5b834cb45ccc)
Acha no Dashboard (ícone lupa). Útil para consultar na Naka.

**Passo 3 — Endereço Liquid**
Deve começar com lq1... ou VJL...
Precisa estar "Validado" no Perfil.
**Erro comum:** usar endereço Bitcoin (bc1) ou Ethereum (0x).

**Passo 4 — Token está lá mas não aparece**
- Seletor de rede: Liquid Network (não Bitcoin, não Ethereum)
- Refresh manual
- Aguardar 3-8 segundos de sincronização

### Casos que não vão resolver
1. Status MED ou refunded
2. QR expirado mas PIX debitado (volta em até 24h)
3. Endereço Liquid inválido

## Declarar DEPIX no IR
- DEPIX = criptoativo
- Declarar em: Bens e Direitos (Grupo 08 — Criptoativos), Código 99 (Outros criptoativos)
- Acima de R$30 mil/mês: obrigatório
- Abaixo: recomendado para evitar malha fina
- Ganho de capital: tributável se lucro > R$35 mil no mês

## Compliance e Legal
- PixGo segue regras do BCB: KYC no cadastro, monitoramento de transações, relatórios ao COAF, limites progressivos antifraude
- **Legal** usar PixGo
- **Não é para "fugir do Fisco"** — declarar no IR é obrigatório
- **CPF que abre MED fica BLOQUEADO PERMANENTEMENTE** na plataforma

## Recuperar / Excluir Conta
- **Recuperar senha:** "Esqueci senha" no login
- **Perdeu seed:** sem recuperação (autocustódia)
- **Conta inativa:** abrir chamado
- **Excluir conta:** sacar todo DEPIX antes → Perfil → opção de exclusão (irreversível)

## Glossário
| Sigla | Significado |
|---|---|
| BCB | Banco Central do Brasil |
| DEPIX | Stablecoin 1:1 Real na Liquid Network |
| D+1 | Liquidação no dia seguinte (corrido) |
| Gas | Taxa de rede (L-BTC na Liquid) |
| KYC | Know Your Customer |
| L-BTC | Bitcoin na Liquid Network |
| Liquid | Sidechain do Bitcoin (Blockstream) |
| MED | Mecanismo Especial de Devolução |
| Naka | Chatbot de suporte da PixGo |
| PSP | Provedor de Serviço de Pagamento |
| payment_id | ID interno da cobrança na PixGo |
| txid | ID da transação no PSP |
| Autocustódia | Você controla a chave privada |
| Peg-out | Saída da Liquid para Bitcoin mainnet |
| Swap | Troca entre criptoativos |
| Stablecoin | Criptomoeda atrelada a moeda fiduciária |
