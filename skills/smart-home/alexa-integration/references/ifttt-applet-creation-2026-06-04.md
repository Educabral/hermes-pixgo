# IFTTT Applet Creation — Session 2026-06-04

## Context
Usuário @Cabral_Cripto (Edu) queria conectar Alexa ao Hermes Agent via IFTTT + ngrok + Flask. Sessão focada em criar Applet Button widget → Webhooks.

## Aprendizados

### 1. Button widget NÃO respeita Body configurado
O IFTTT Webhooks ignora completamente o Body JSON configurado no Applet. O Button widget envia sempre:
```json
{"value1":"","value2":"","value3":""}
```
Independente do Content-Type ser application/json e do Body ser `{"comando":"teste"}`.

**Solução:** O Flask precisa aceitar `value1` como fallback:
```python
comando = data.get('comando') or data.get('value1') or 'teste'
```

### 2. ngrok precisa ser religado após restart
O ngrok não sobrevive a desligamentos. Sempre verificar com `curl http://localhost:4040/api/tunnels` antes de pedir teste do usuário.

### 3. Flask health check via curl é mais confiável que process log
`process(action='log')` pode mostrar stdout vazio mesmo com o Flask rodando. Usar `curl http://localhost:5000/` como health check real.

### 4. Usuário prefere instruções curtas no celular
Quando o usuário está no celular, instruções com >3 linhas são ignoradas. Preferir:
- "Aba My Applets → clica no Applet → Run"
- "Aba Widgets → adiciona widget → aperta"

### 5. Sinal de frustração = mudar de estratégia
"já me irritei com isso", "desliguei" = parar abordagem atual e pular para o caminho mais simples.

### 6. Criar Applet via app IFTTT (celular) é mais confiável que navegador
O React SPA do IFTTT no navegador headless tem vários problemas (popup de upgrade, validação silenciosa, selects que não propagam eventos). O app mobile funciona direto.
