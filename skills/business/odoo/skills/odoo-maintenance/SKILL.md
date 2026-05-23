---
name: odoo-maintenance
description: Odoo Maintenance operations — manage equipment, maintenance requests, and team assignments.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, maintenance, equipment, requests, repair]
    parent_skill: odoo
---
# Odoo Maintenance

Manage equipment, maintenance requests, and team assignments.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List maintenance requests

```
ODOO model maintenance.request search --limit 20 --fields name,equipment_id,user_id,maintenance_team_id,stage_id,priority,date_deadline
ODOO model maintenance.request search --domain '[["stage_id","!=",false]]' --fields name,equipment_id,stage_id,priority
```

### Get request details

```
ODOO model maintenance.request read 1 --fields name,equipment_id,description,user_id,maintenance_team_id,stage_id,priority,date_deadline,create_date,schedule_date,close_date
```

### List equipment

```
ODOO model maintenance.equipment search --limit 20 --fields name,category_id,assigned_user_id,maintenance_team_id,location,model,serial_no
ODOO model maintenance.equipment search --domain '[["category_id","!=",false]]' --fields name,category_id,location
```

### List maintenance teams

```
ODOO model maintenance.team search --fields name,person_ids,color
```

### List equipment categories

```
ODOO model maintenance.equipment.category search --fields name,color
```

### Statistics

```
ODOO model maintenance.request count --domain '[["stage_id","=",1]]'
ODOO model maintenance.equipment count
```

## Key Models

| Model | Use |
|-------|-----|
| `maintenance.request` | Maintenance requests/tickets |
| `maintenance.equipment` | Equipment/machines being maintained |
| `maintenance.team` | Maintenance teams |
| `maintenance.equipment.category` | Equipment categories |

## Request Stages

| Stage | Meaning |
|-------|---------|
| New | Request created, not yet assigned |
| In Progress | Work is being done |
| Done | Maintenance completed |
| Cancelled | Request cancelled |

## Rules

1. **Equipment links to HR**: Equipment can be assigned to an employee via `assigned_user_id` which maps to `hr.employee`.
2. **Requests have priority levels**: `0` (Low), `1` (Normal), `2` (High), `3` (Very High). Higher numbers are more urgent.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List requests
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"maintenance.request\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"stage_id\",\"priority\",\"equipment_id\"]}]},\"id\":2}"
```
