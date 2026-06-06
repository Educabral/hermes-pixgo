# Voice Monkey API v3 — Session Log (04 Jun 2026)

## Flow ID 2916 ("Hermes Comando")

Created by user but WITHOUT Web Request node attached. The API confirmed:
- GET `/flow?token=TOKEN&flow=2916` → `{flowId: "568cce22-6614-4af9-961a-c1ac86f175d1", flowName: "Hermes Comando", requestRef: "2916"}`
- GET `/devices?token=TOKEN` → `{devices: [{id: "bedroom-echo-5zhh7", name: "Bedroom Echo"}]}`

## Critical discovery: API cannot configure nodes

We tried:
- POST `/flow?token=TOKEN&flow=2916&type=web_request&url=...&method=POST` → 200 flow data (same as GET) — node NOT added
- POST `/flow` with JSON body `{flow:2916, action:"add_node", ...}` → `FLOW_NOT_FOUND`
- PUT `/flow` → 405 Method Not Allowed
- POST `/flow/node` → 404
- All other endpoints → 404

**Conclusion:** API is read-only. Only web console can add actions (Web Request nodes) to flows.

## API Trigger endpoint confirmed working

`GET /trigger?device=bedroom-echo-5zhh7&token=TOKEN&flow=2916` → `{"success":true,"data":"OK"}`

Both GET and POST work. POST with body also returns OK but likely ignores body.

## Token format

UUID with hyphens: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`. NO prefix like `vm_`.

User's token: `54a40-5a2ee-c7a11-c72f5-af16c-4bc3a-e3-04ef832f-42ef-4e48-8427-670d7b85f2e2`
(Note: this has an unusual format — a short group `54a40` followed by standard UUID groups. May be a composite key.)
