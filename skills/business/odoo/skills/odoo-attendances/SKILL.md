---
name: odoo-attendances
description: Odoo Attendances operations — manage employee check-ins, check-outs, and attendance records.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, attendance, check-in, check-out, hr]
    parent_skill: odoo
---
# Odoo Attendances

Manage employee attendance records, check-ins, and check-outs.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List attendance records

```
ODOO model hr.attendance search --limit 20 --fields employee_id,check_in,check_out,worked_hours
ODOO model hr.attendance search --domain '[["employee_id","=",1]]' --limit 20 --fields check_in,check_out,worked_hours
```

### Get attendance record

```
ODOO model hr.attendance read 1 --fields employee_id,check_in,check_out,worked_hours
```

### Create attendance (check-in)

```
ODOO model hr.attendance create '{"employee_id":1,"check_in":"2026-05-11 09:00:00"}'
```

### Update with check-out

```
ODOO model hr.attendance write 1 '{"check_out":"2026-05-11 17:00:00"}'
```

### Count attendance records

```
ODOO model hr.attendance count --domain '[["employee_id","=",1]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `hr.attendance` | Attendance records |

## Common Fields

**hr.attendance**: employee_id, check_in, check_out, worked_hours (auto-computed)

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Attendances
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"hr.attendance\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["employee_id", "check_in", "check_out"]]}},\"id\":2}"
```
