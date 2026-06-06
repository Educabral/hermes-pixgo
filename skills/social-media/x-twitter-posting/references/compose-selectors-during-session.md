# Seletores do Compose/Post — Investigação de Campo

## Contexto

Esta sessão (Jun 2026) descobriu que os seletores do X variam dependendo de COMO o usuário acessa a página de compose. O fluxo `x.com/compose/post` (URL direta) tem uma estrutura de DOM DIFERENTE do fluxo de clicar no botão "Postar" na sidebar.

## Seletores Observados no `x.com/compose/post`

| Elemento | Seletor | Funciona? |
|---|---|---|
| Textarea do tweet principal | `div[data-text="true"]` | ✅ Funciona |
| Textarea do tweet principal | `[data-testid="tweetTextarea_0"]` | ❌ NÃO encontrado no compose/post URL |
| Botão Adicionar na thread | `[data-testid="addButton"]` | ❌ NÃO encontrado no compose/post URL |
| Botão Adicionar (fotos/vídeo) | `button[aria-label="Adicionar fotos ou vídeo"]` | ⚠️ Existe mas é o botão de MÍDIA, não de thread |
| Botão Publicar | `[data-testid="tweetButton"]` | ✅ Funciona (no compose/post popup) |

## Descoberta CRÍTICA

O `x.com/compose/post` é um **popup/modal** diferente do fluxo dentro da home. Neste modal:

- **NÃO existe** `[data-testid="addButton"]` para adicionar tweets na thread
- O botão "+" que aparece é na verdade `button[aria-label="Adicionar fotos ou vídeo"]` (para anexar mídia)
- Para criar THREAD no modal compose/post, o botão correto é outro (possivelmente mostra "+" quando detecta que o texto vai ser cortado, ou aparece no overflow menu)

## Como criar threads no modal compose/post

Não foi confirmado nesta sessão. Possibilidades:
1. Clicar no botão "+" de mídia NÃO cria novo tweet na thread
2. Pode ser que o compose/post seja APENAS para posts únicos, e threads requerem o fluxo da home
3. Pode haver um botão "+" diferente que não foi detectado

## Alternativa: Usar a home com popup

Se o modal compose/post não suportar threads:
```python
# Abrir a home primeiro
await page.goto('https://x.com/home')
# Depois clicar no botão "Postar" da sidebar
post_btn = await page.querySelector('[data-testid="SideNav_NewTweet_Button"]')
await post_btn.click()  # abre o popup de compose DA HOME
# Neste popup, [data-testid="addButton"] funciona
```

## Técnica de descoberta de seletores

```python
# Para investigar qual botão "+" existe, executar no contexto do pyppeteer:
await page.evaluate('''() => {
    const btns = document.querySelectorAll('[role="button"]');
    const results = [];
    for (const btn of btns) {
        const aria = btn.getAttribute('aria-label') || '';
        const testid = btn.getAttribute('data-testid') || '';
        const text = btn.innerText?.substring(0, 30) || '';
        const html = btn.innerHTML?.substring(0, 80) || '';
        if (aria || testid) {
            results.push({aria, testid, text, html});
        }
    }
    return results;
}''')
```
