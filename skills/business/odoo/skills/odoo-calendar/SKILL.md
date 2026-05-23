---
name: odoo-calendar
description: Odoo Calendar operations — manage events, meetings, and attendee tracking.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, calendar, events, meetings, scheduling]
    parent_skill: odoo
---
# Odoo Calendar

Manage events, meetings, and attendee tracking.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List events

```
ODOO calendar events --limit 20
ODOO calendar events --start-date "2026-05-01" --end-date "2026-05-31"
ODOO calendar events --user-id 2
```

### Get event details

```
ODOO calendar get-event 10
```

### Create event

```
ODOO calendar create-event --name "Team Meeting" --start "2026-05-15 10:00:00" --stop "2026-05-15 11:00:00" --location "Room 4B"
```

With attendees:
```
ODOO calendar create-event --name "Client Call" --start "2026-05-16 14:00:00" --stop "2026-05-16 14:30:00" --partner-ids "[3,5]" --description "Project status update"
```

### Delete event

```
ODOO calendar delete-event 10
```

**Always confirm with the user before deleting.**

### Statistics

```
ODOO calendar statistics
```

## Output Format

### events

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 10,
      "name": "Team Meeting",
      "start": "2026-05-15 10:00:00",
      "stop": "2026-05-15 11:00:00",
      "allday": false,
      "duration": 1.0,
      "location": "Room 4B",
      "description": "",
      "user_id": [2, "$ODOO_USER"],
      "create_date": "2026-05-11"
    }
  ]
}
```

### create-event

```json
{$ODOO_DB: true, "result": 11}
```

### statistics

```json
{$ODOO_DB: true, "result": {"total_events": 120, "upcoming": 15}}
```

## Key Models

| Model | Use |
|-------|-----|
| `calendar.event` | Events and meetings |
| `calendar.attendee` | Attendee responses |

## Common Pitfalls

1. **Datetime Format**: Use exact format `YYYY-MM-DD HH:MM:SS` (Odoo server timezone). For full-day events, use `--allday` flag.
2. **Partner ID Format**: Partner IDs must be passed as JSON array format `"[ID]"` not as separate arguments.
3. **Date Filtering**: Use `--start-date` for `start >=` and `--end-date` for `stop <=` comparisons.
4. **Attendee Management**: Use raw model for attendee details: `ODOO model calendar.attendee search --domain '[["event_id","=",10]]' --fields partner_id,state`

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Calendar
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"calendar.event\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "start", "stop", "location"]]}},\"id\":2}"
```
