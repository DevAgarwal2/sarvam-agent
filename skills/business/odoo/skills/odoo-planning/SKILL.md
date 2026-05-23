---
name: odoo-planning
description: Odoo Planning operations — manage shifts, planning slots, and workforce scheduling.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, planning, scheduling, shifts, workforce]
    parent_skill: odoo
---
# Odoo Planning

Manage shifts, planning slots, and workforce scheduling.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

> **Note:** The Planning module (`planning`) is installed but currently marked as `uninstallable` in Odoo 19.0 (likely due to unmet dependencies). Use the generic `model` command if available, or fall back to HR Attendance/Timesheets for scheduling needs.

## Usage

### List planning slots (if available)

```
ODOO model planning.planning search --limit 20 --fields name,role_id,employee_id,start_datetime,end_datetime,state
ODOO model planning.slot search --limit 20 --fields employee_id,start_datetime,end_datetime,state
```

### Alternative: HR Attendance for scheduling

```
ODOO model hr.attendance search --limit 20 --fields employee_id,check_in,check_out,worked_hours
```

## Key Models (when available)

| Model | Use |
|-------|-----|
| `planning.slot` | Individual shift/slot assignments |
| `planning.template` | Reusable shift templates |

## Rules

1. **Fall back to HR**: If Planning models aren't accessible, use `hr.attendance` for check-in/out records or `hr_timesheet` for logged hours.
2. **Check accessibility first**: Run `ODOO model planning.slot search --limit 1` to verify the module is usable before making assumptions.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List planning
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"planning.planning\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"employee_id\",\"start_datetime\",\"end_datetime\"]}]},\"id\":2}"
```
