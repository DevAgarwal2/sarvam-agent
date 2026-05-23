---
name: odoo-sms
description: Odoo SMS operations — send SMS messages, manage SMS templates, and track delivery.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, sms, messaging, notifications]
    parent_skill: odoo
---
# Odoo SMS

Send SMS messages, manage SMS templates, and track delivery status.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List SMS messages

```
ODOO model sms.sms search --limit 20 --fields number,partner_id,body,state,date
ODOO model sms.sms search --domain '[["state","=","sent"]]' --fields number,body,date
```

### Get SMS details

```
ODOO model sms.sms read 1 --fields number,partner_id,body,state,date,failure_reason
```

### List SMS templates

```
ODOO model sms.template search --fields name,body,model_id,lang
```

### Send an SMS via API

```
ODOO model sms.api send '{"res_ids":[1],"template_id":1}'
```

### Count SMS by state

```
ODOO model sms.sms count --domain '[["state","=","error"]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `sms.sms` | Individual SMS records |
| `sms.template` | Reusable SMS templates |
| `sms.api` | SMS sending API |
| `sms.account` | SMS provider account |

## SMS States

| State | Meaning |
|-------|---------|
| `outgoing` | Queued for sending |
| `sent` | Successfully delivered |
| `error` | Delivery failed |

## Rules

1. **SMS requires a provider**: An SMS provider account must be configured (e.g., Twilio). Check `sms.account` for active providers.
2. **Templates use QWeb**: SMS templates support QWeb expressions in `body` for dynamic content.
3. **Concatenated SMS**: Long messages are automatically split into multiple segments (max 160 chars per segment).

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List SMS
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"sms.sms\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"number\",\"body\",\"state\"]}]},\"id\":2}"
```
