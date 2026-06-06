---
name: windows-pc-control
description: "Controlar o PC Windows do usuário: gerenciar processos, abrir URLs no navegador padrão, controlar volume do sistema. Usa PowerShell via terminal (git-bash) ou arquivos .ps1 temporários."
version: 1.0.0
platforms: [windows]
metadata:
  hermes:
    tags: [windows, powershell, desktop, volume, browser, automation]
    related_skills: []
---

# Windows PC Control

Controle do PC do usuário via PowerShell. O terminal do Hermes roda git-bash (MSYS2), então comandos diretos com `$` no PowerShell costumam quebrar por conflito de escape. Use arquivos .ps1 temporários para scripts multi-linha.

## Abrir URL no Navegador Padrão

```powershell
powershell -Command "Start-Process 'https://www.youtube.com/results?search_query=henrique+e+juliano'"
```

Funciona via git-bash porque não tem `$` problemático.

### Comet (navegador do usuário) — caminho explícito

O Comet fica em `C:\Program Files\Perplexity\Comet\Application\comet.exe`. Se Start-Process simples não abrir no Comet:

```bash
powershell -Command "Start-Process 'C:\Program Files\Perplexity\Comet\Application\comet.exe' -ArgumentList 'https://www.youtube.com'"
```

### Fallback de Áudio — YouTube/Música

**Problema crítico (nunca esquecer):** O navegador headless do Hermes (browser_navigate) NÃO reproduz áudio. O vídeo abre na tela mas fica mudo. Não adianta tentar tocar música via browser tool — o som nunca sai.

**Solução correta (única que funciona):**
1. Fechar o navegador que está rodando (`Get-Process chrome* | Stop-Process -Force`)
2. Abrir a URL no navegador nativo com `Start-Process 'https://www.youtube.com/watch?v=VIDEO_ID'`
3. O vídeo abre no Chrome/Edge real do Windows — aí o áudio funciona de verdade

**Sequência completa para tocar música:**
```bash
# 1. Fecha o Chrome (se tiver rodando)
powershell -Command "Get-Process chrome* | Stop-Process -Force"

# 2. Abre o YouTube no navegador nativo
powershell -Command "Start-Process 'https://www.youtube.com/watch?v=VIDEO_ID'"
```

## Fechar Aba Específica no Comet (YouTube)

Use Shell.Application COM object + .ps1 para fechar uma aba específica **sem** matar o navegador inteiro:

```
write_file(content="""$shell = New-Object -ComObject Shell.Application
$shell.Windows() | Where-Object { $_.LocationUrl -like '*youtube*' } | ForEach-Object { $_.Quit() }
""", path="C:\\Users\\PC\\kill_tab.ps1")
terminal("powershell -ExecutionPolicy Bypass -File \"C:\\Users\\PC\\kill_tab.ps1\"")
terminal("rm \"C:\\Users\\PC\\kill_tab.ps1\"")  # limpeza
```

**NUNCA** tente `Where-Object { $_ }` inline via `powershell -Command` — o bash quebra com `$` e `{}`. Sempre use .ps1.

### ⚠️ Falha silenciosa: Shell.Application.Quit() pode não fechar a aba

O método `$_.Quit()` do Shell.Application **falha silenciosamente** em alguns cenários:
- O Comet cria MUITOS subprocessos (já vi 29 processos `comet.exe` + 7 `Perplexity.exe` rodando ao mesmo tempo)
- `Quit()` em uma janela `Shell.Application` fecha apenas aquela aba naquela janela — mas o navegador continua rodando com outras janelas/abas
- O COM object pode não enumerar todas as janelas do Comet

**Quando o usuário disser "não fechou não" depois do Shell.Application.Quit():**
1. Verificar: `Get-Process "*comet*"` ou `Get-Process "*perplexity*"`
2. Se ainda tiver processo rodando, perguntar se quer matar TUDO ou só aquela aba
3. Para matar tudo: `Get-Process "*comet*","*perplexity*" | Stop-Process -Force`
4. Para tentar de novo só a aba: tentar Shell.Application de novo com filtro mais específico, ou navegar até youtube.com e parar pelo browser tool

### Filtros úteis:
- `$_.LocationUrl -like '*youtube*'` — só YouTube
- `$_.LocationUrl -match 'watch?v=4QgxXHQR5kQ'` — vídeo específico
- `$_.LocationUrl -notlike '*youtube*'` — fecha tudo menos YouTube
- `$shell.Windows() | Select-Object LocationUrl` — lista todas antes de filtrar

## Fechar Processo (ex: Chrome)

```powershell
powershell -Command "Get-Process chrome* | Stop-Process -Force"
```

Para Edge: `msedge*`, Firefox: `firefox*`

## Controle de Volume do Sistema

**Problema:** PowerShell com `$i`, `for($i...)`, `$obj` quebra no git-bash porque o bash interpreta `$` como variável de shell.

**Solução SEMPRE usar arquivo .ps1 temporário:**

```bash
# Cria o script
cat > /c/Users/PC/Desktop/vol.ps1 << 'EOF'
$obj = New-Object -ComObject WScript.Shell
for ($i = 0; $i -lt 50; $i++) {
    $obj.SendKeys([char]174)  # 174 = Volume Down
    Start-Sleep -Milliseconds 30
}
EOF

# Executa
powershell.exe -File "C:\Users\PC\Desktop\vol.ps1"
```

### Teclas de Volume (Virtual-Key Codes via SendKeys)

| Ação | Código | Notas |
|---|---|---|
| Volume Up | `[char]175` | Aumenta ~2% por send |
| Volume Down | `[char]174` | Diminui ~2% por send |
| Mute/Unmute | `[char]173` | Alterna mudo |

### Calibragem de Volume

- Sistema parte de ~100% por padrão
- ~50 pressionadas de Volume Down = ~50% (50 iterações)
- Sempre incluir `Start-Sleep -Milliseconds 30` entre sends pra não perder teclas

### Pitfalls

- **NUNCA** tente PowerShell inline com `$var` no git-bash — sempre crie .ps1 e execute com `powershell.exe -File`
- **Sempre mutar e desmutar primeiro** (`[char]173` duas vezes) pra garantir que não está mudo antes de ajustar volume
- O YouTube pode estar com som mutado na aba do navegador mesmo com o volume do sistema alto — isso não dá pra controlar via PowerShell, precisa pedir pro usuário clicar no ícone de som na aba
- `WScript.Shell` precisa do `New-Object -ComObject` — não funciona se PowerShell estiver restricted mode
