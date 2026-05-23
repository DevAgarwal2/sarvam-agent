---
name: odoo-email-marketing
description: Odoo Email Marketing operations — manage mailing lists, campaigns, and mailings.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, email-marketing, mailings, campaigns, newsletters]
    parent_skill: odoo
---
# Odoo Email Marketing

Manage mailing lists, campaigns, and mass mailings.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

```
ODOO model mailing.mailing search --limit 20 --fields subject,state,sent_date,schedule_date,total,opened,replied,bounced
ODOO model mailing.mailing read 1 --fields subject,body_html,state,schedule_date,sent_date,total,opened,clicked,replied,bounced
ODOO model mailing.list search --limit 20 --fields name,contact_count
ODOO model mailing.contact search --limit 20 --fields name,email,list_ids
```

## Key Models

| Model | Use |
|-------|-----|
| `mailing.mailing` | Mailings/campaigns |
| `mailing.list` | Mailing lists |
| `mailing.contact` | Contact addresses |

## State Flow (mailing.mailing)

```
draft → sending → done
```

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Email Marketing
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"mailing.mailing\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["subject", "state", "total"]]}},\"id\":2}"
```
