# Google Calendar & Drive Integration Setup

## Prerequisites
- Google Cloud project with Calendar API + Drive API enabled
- OAuth 2.0 credentials (Desktop app type) → `~/.hermes/google/credentials.json`
- User email segurancabral@gmail.com added as test user
- Python packages: `google-auth-oauthlib`, `google-api-python-client`, `google-auth-httplib2`

## Scripts

Location: `~/AppData/Local/hermes/scripts/`

### google_auth_setup.py
First-run setup — user must:
1. Create project + enable APIs + create OAuth credentials in Google Cloud Console
2. Save credentials.json to `~/.hermes/google/`
3. Run the script, authorize via browser
4. Token saved to `~/.hermes/google/token.json`

### google_calendar.py
- `python google_calendar.py list [days]` — list upcoming events
- `python google_calendar.py create 'Title' '2026-06-10 14:00' [duration_min]` — create event

### google_drive.py
- `python google_drive.py list [query]` — list files
- `python google_drive.py search 'term'` — search by name

## Token refresh
The scripts auto-refresh the OAuth token if expired. Token lives at ~/.hermes/google/token.json.
If token is invalid/deleted, re-run google_auth_setup.py.
