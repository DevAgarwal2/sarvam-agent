---
name: odoo-discuss
description: Odoo Discuss operations — read/send messages, manage followers, and track activities.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, discuss, messages, chat, activities, followers]
    parent_skill: odoo
---
# Odoo Discuss

Read/send messages, manage followers, and track activities across any Odoo record.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### Read messages on a record

```
ODOO discuss messages --model sale.order --res-id 12 --limit 20
ODOO discuss messages --model crm.lead --res-id 7
```

### Send a message

```
ODOO discuss send --model crm.lead --res-id 7 --body "Called the client — they want a demo next week."
```

### List followers

```
ODOO discuss followers --model sale.order --res-id 12
```

### List activities

```
ODOO discuss activities --limit 20
ODOO discuss activities --user-id 2
```

### Statistics

```
ODOO discuss statistics
```

## Output Format

### messages

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 52,
      "subject": false,
      "body": "Called the client — they want a demo next week.",
      "email_from": "$ODOO_USER",
      "author_id": [2, "$ODOO_USER"],
      "date": "2026-05-11 14:30:00",
      "model": "crm.lead",
      "res_id": 7,
      "message_type": "comment",
      "record_name": "Acme Corp Deal"
    }
  ]
}
```

### send

```json
{$ODOO_DB: true, "result": 53}
```

### followers

```json
{
  $ODOO_DB: true,
  "result": [
    {"id": 5, "partner_id": [2, "$ODOO_USER"]},
    {"id": 6, "partner_id": [3, "Acme Corp"]}
  ]
}
```

### activities

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 18,
      "activity_type_id": [1, "Email"],
      "summary": "Send proposal to Acme Corp",
      "date_deadline": "2026-05-15",
      "user_id": [2, "$ODOO_USER"],
      "res_model": "crm.lead",
      "res_id": 7,
      "res_name": "Acme Corp Deal"
    }
  ]
}
```

### statistics

```json
{$ODOO_DB: true, "result": {"messages": 450, "activities": 12}}
```

## Key Models

| Model | Use |
|-------|-----|
| `mail.message` | Messages (comments, emails, notes) |
| `mail.activity` | Activities/tasks linked to records |
| `mail.activity.type` | Activity categories (Email, Call, Meeting, To-Do) |
| `mail.followers` | Record followers |

## Message Types

| Type | Description |
|------|-------------|
| `comment` | Manual message sent via Discuss |
| `notification` | Automated notification (stage change, assignment) |
| `email` | Outbound/inbound email |

## Rules

1. **model + res_id identifies the record**: Every message is linked to a specific record via `model` (technical name) and `res_id` (ID).
2. **Sent messages create notifications**: Followers of the record are notified.
3. **Activities track to-dos**: Each user has an activity list. Activities can be scheduled with deadlines.
4. **Use raw model for message history**: `ODOO model mail.message search --domain '[["model","=","crm.lead"],["res_id","=",7]]' --limit 50 --order date asc --fields subject,body,author_id,date`

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Discuss
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"mail.message\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["subject", "body", "author_id", "date"]]}},\"id\":2}"
```
