---
name: odoo-hr
description: Odoo HR operations — manage employees, departments, and organizational structure.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, hr, employees, departments, organization]
    parent_skill: odoo
---
# Odoo HR

Manage employees, departments, and organizational structure.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List employees

```
ODOO hr employees --limit 20
ODOO hr employees --department-id 2
```

### Get employee details

```
ODOO hr get-employee 1
```

### List departments

```
ODOO hr departments --limit 20
```

### Create employee

```
ODOO hr create-employee --name "Jane Smith"
```

### Statistics

```
ODOO hr statistics
```

## Output Format

### employees

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 1,
      "name": "John Doe",
      "user_id": [2, "$ODOO_USER"],
      "department_id": [2, "Engineering"],
      "job_id": [5, "Software Engineer"],
      "work_email": "john@company.com",
      "work_phone": "+1-555-0100",
      "parent_id": [1, "Manager Name"],
      "coach_id": false
    }
  ]
}
```

### departments

```json
{
  $ODOO_DB: true,
  "result": [
    {"id": 1, "name": "Management", "parent_id": false, "manager_id": [1, "CEO"]},
    {"id": 2, "name": "Engineering", "parent_id": [1, "Management"], "manager_id": [3, "CTO"]}
  ]
}
```

### statistics

```json
{$ODOO_DB: true, "result": {"employees": 25, "departments": 5}}
```

## Key Models

| Model | Use |
|-------|-----|
| `hr.employee` | Employees |
| `hr.department` | Departments |
| `hr.job` | Job positions |

## Rules

1. **Employee != User**: An employee may or may not have a linked Odoo user (`user_id`).
2. **Department hierarchy**: `parent_id` forms a tree. Use `child_of` in domains for subtree queries.
3. **Use raw model for detailed queries**: `ODOO model hr.employee search --domain '[["department_id","=",2]]' --fields name,work_email,job_id,parent_id`

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Hr
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"hr.employee\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "department_id", "work_email"]]}},\"id\":2}"
```
