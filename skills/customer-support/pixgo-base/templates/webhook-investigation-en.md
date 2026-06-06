# Webhook Investigation — English Template

Use when a merchant reports not receiving webhook callbacks.

## Variation 1 (Direct)

**Eduardo Cabral / Gerente de Contas**

I checked the paymentId [ID] in our system.

Regarding the webhook issue, a few things to check:

- Make sure the webhook_url parameter was sent correctly when creating the charge
- Verify your server accepts incoming requests and responds with HTTP 200
- The webhook may have been disabled due to consecutive failures (over 50 failed attempts)
- In the PixGo panel, go to Integrations > API Keys and confirm the webhook URL is still set

If you can share the webhook_url you're using, I can investigate further on my end.

## Variation 2 (More detailed)

**Eduardo Cabral / Gerente de Contas**

Thank you for reaching out. I looked into paymentId [ID] and the charge was created successfully.

The callback may not have been delivered for one of these reasons:

1. **Automatic deactivation** — if your endpoint returned errors (timeouts, 5xx) more than 50 times, PixGo automatically disables webhook delivery. Please check in your panel under Integrations > API Keys if the webhook URL field is still filled in.

2. **Missing headers** — your server needs to receive `X-Webhook-Event`, `X-Webhook-Timestamp`, and `X-Webhook-Signature` headers

3. **HMAC validation** — the signature is generated as HMAC-SHA256 of `timestamp + "." + raw JSON payload` using your Webhook Secret

4. **Response time** — your server must respond with HTTP 200 promptly; delays count as failures

If you'd like, I can investigate further. Just let me know your configured webhook URL.

## Variation 3 (Short)

**Eduardo Cabral / Gerente de Contas**

I verified paymentId [ID] — the charge was created correctly.

Common causes for missing webhook callbacks:
- Webhook URL may have been disabled in Integrations > API Keys
- Your server may not be accepting external requests (check for HTTP 200 responses)
- The webhook was deactivated after repeated failures

Go to Integrations > API Keys in your PixGo panel to check the current status.
