---
name: odoo-link-tracker
description: Odoo Link Tracker operations — track click-through links in campaigns and communications.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, link-tracker, campaigns, urls, analytics]
    parent_skill: odoo
---
# Odoo Link Tracker

Track and analyze click-through links used in campaigns, emails, and SMS.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

```
ODOO model link.tracker search --limit 20 --fields title,url,short_url,count,campaign_id
ODOO model link.tracker read 1 --fields title,url,short_url,count,medium_id,campaign_id,source_id
ODOO model link.tracker.code search --limit 20 --fields code,link_id,clicks
ODOO model link.tracker.click search --limit 50 --fields link_id,ip,country_id,click_date
ODOO model utm.campaign search --limit 20 --fields name
```

## Key Models

| Model | Use |
|-------|-----|
| `link.tracker` | Tracked links |
| `link.tracker.code` | Short URL codes |
| `link.tracker.click` | Click records |
| `utm.campaign` | Campaign sources |
| `utm.medium` | Campaign mediums |
| `utm.source` | Campaign sources |

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Link Tracker
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"link.tracker\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["title", "url", "short_url", "count"]]}},\"id\":2}"
```
