---
name: odoo-timesheets
description: Odoo Timesheets operations — track time on projects and tasks.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, timesheets, time-tracking, billing]
    parent_skill: odoo
---
# Odoo Timesheets

Track time entries on projects and tasks.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List timesheet entries

```
ODOO model account.analytic.line search --limit 20 --fields name,project_id,task_id,employee_id,unit_amount,date
ODOO model account.analytic.line search --domain '[["project_id","=",1]]' --limit 20
ODOO model account.analytic.line search --domain '[["employee_id","=",1],["date",">=","2026-05-01"]]' --limit 50 --fields name,unit_amount,date,task_id
```

### Create time entry

```
ODOO model account.analytic.line create '{"name":"Development","project_id":1,"task_id":1,"unit_amount":2.5,"date":"2026-05-11"}'
```

### Count hours

```
ODOO model account.analytic.line count --domain '[["employee_id","=",1]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `account.analytic.line` | Timesheet entries (time tracked) |

## Common Fields

**account.analytic.line**: name, project_id, task_id, employee_id, unit_amount (hours), date, description, company_id

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Timesheets
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"account.analytic.line\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "project_id", "unit_amount", "date"]]}},\"id\":2}"
```
