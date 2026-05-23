---
name: odoo-time-off
description: Odoo Time Off (Leave) operations — manage leave requests, allocations, and leave types.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, time-off, leave, hr, holidays]
    parent_skill: odoo
---
# Odoo Time Off

Manage employee leave requests, allocations, and leave types.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List leave requests

```
ODOO model hr.leave search --limit 20 --fields name,employee_id,holiday_status_id,date_from,date_to,state,number_of_days
ODOO model hr.leave search --domain '[["state","=","confirm"]]' --limit 20 --fields name,employee_id,date_from,date_to,number_of_days
```

### Get leave request

```
ODOO model hr.leave read 1 --fields name,employee_id,holiday_status_id,date_from,date_to,state,number_of_days,notes
```

### Create leave request

```
ODOO model hr.leave create '{"name":"Vacation","employee_id":1,"holiday_status_id":1,"date_from":"2026-06-01 00:00:00","date_to":"2026-06-05 23:59:59","request_date_from":"2026-06-01","request_date_to":"2026-06-05"}'
```

### List leave types

```
ODOO model hr.leave.type search --limit 20 --fields name,allocation_type,request_unit,validity_start,validity_stop
```

### List allocations

```
ODOO model hr.leave.allocation search --limit 20 --fields name,employee_id,holiday_status_id,number_of_days,state
```

## Key Models

| Model | Use |
|-------|-----|
| `hr.leave` | Leave requests |
| `hr.leave.type` | Leave types (vacation, sick, etc.) |
| `hr.leave.allocation` | Leave allocations |

## State Flow (hr.leave)

```
draft → confirm → validate1 → validate → refuse
```

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Time Off
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"hr.leave\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "employee_id", "date_from", "date_to", "state"]]}},\"id\":2}"
```
