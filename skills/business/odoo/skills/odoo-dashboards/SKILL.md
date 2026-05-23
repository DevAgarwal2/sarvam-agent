---
name: odoo-dashboards
description: Odoo Dashboards — access spreadsheet dashboards and KPI data. Dashboards aggregate data from other modules.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, dashboards, spreadsheets, kpi]
    parent_skill: odoo
---
# Odoo Dashboards

Odoo dashboards are spreadsheet-powered views that aggregate KPIs from other modules. Most dashboard data comes from underlying models.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

```
ODOO model spreadsheet.dashboard search --limit 20 --fields name,group_ids
ODOO model spreadsheet.dashboard read 1 --fields name,data,group_ids
```

For actual KPI data, query the source modules directly:
- Sales KPIs → `ODOO sales statistics`
- CRM KPIs → `ODOO crm statistics`
- Inventory KPIs → `ODOO inventory statistics`
- HR KPIs → `ODOO hr statistics`
- Accounting KPIs → `ODOO accounting statistics`

## Key Models

| Model | Use |
|-------|-----|
| `spreadsheet.dashboard` | Dashboard definitions |
| `spreadsheet.dashboard.group` | Dashboard groups |

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Dashboards
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"spreadsheet.dashboard\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "dashboard_group_id"]]}},\"id\":2}"
```
