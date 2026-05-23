---
name: odoo-events
description: Odoo Events operations — manage events, registrations, and attendees.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, events, registrations, attendees]
    parent_skill: odoo
---
# Odoo Events

Manage events, registrations, and attendees.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

```
ODOO model event.event search --limit 20 --fields name,date_begin,date_end,seats_max,seats_available,stage_id,user_id
ODOO model event.event read 1 --fields name,date_begin,date_end,seats_max,seats_available,description,address_id,user_id
ODOO model event.registration search --limit 20 --fields name,event_id,partner_id,email,phone,state
```

## Key Models

| Model | Use |
|-------|-----|
| `event.event` | Events |
| `event.registration` | Attendee registrations |
| `event.type` | Event categories |

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Events
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"event.event\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "date_begin", "date_end", "seats_available"]]}},\"id\":2}"
```
