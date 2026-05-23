---
name: odoo-expenses
description: Odoo Expenses operations — manage employee expense claims, submission, approval, and reporting.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, expenses, reimbursements, employee-expenses]
    parent_skill: odoo
---
# Odoo Expenses

Manage employee expense claims — create, submit, approve, and refuse.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List expenses

```
ODOO expenses list --limit 20
ODOO expenses list --state draft
ODOO expenses list --state approved --employee-id 1
```

### Get expense details

```
ODOO expenses get 12
```

### Create expense

```
ODOO expenses create --name "Client lunch" --total-amount 85.50 --date "2026-05-11"
ODOO expenses create --name "Airfare" --employee-id 1 --product-id 3 --unit-amount 350 --total-amount 350 --description "Flight to conference"
```

### Submit for approval

```
ODOO expenses submit 12
```

### Approve

```
ODOO expenses approve 12
```

### Refuse

```
ODOO expenses refuse 12
```

### Statistics

```
ODOO expenses statistics
```

## Output Format

### list

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 12,
      "name": "Client lunch",
      "employee_id": [1, "John Doe"],
      "product_id": [2, "Meals"],
      "unit_amount": 85.50,
      "total_amount": 85.50,
      "date": "2026-05-11",
      "state": "draft",
      "description": "Lunch with Acme Corp"
    }
  ]
}
```

### create

```json
{$ODOO_DB: true, "result": 13}
```

### submit / approve / refuse

```json
{$ODOO_DB: true, "result": true}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {"total": 45, "draft": 10, "reported": 5, "approved": 20, "done": 10}
}
```

## Key Models

| Model | Use |
|-------|-----|
| `hr.expense` | Individual expense claims |
| `hr.expense.sheet` | Grouped expense reports |

## State Flow

```
draft → reported → approved → done
                    ↘ refused
```

## Rules

1. **Submit moves to reported**: `submit` creates an expense report and moves expenses to `reported`.
2. **Approve is final**: Once approved, expenses generate accounting entries in `done` state.
3. **Refuse is reversible**: Refused expenses go back to `draft` for editing.
4. **Employee auto-set**: If `--employee-id` is omitted, the API uses the current user's linked employee. For admin users, always specify `--employee-id` explicitly.
5. **Use raw model for reports**: `ODOO model hr.expense.sheet search --domain '[["state","=","submit"]]' --fields name,employee_id,total_amount,state`

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Expenses
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"hr.expense\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "employee_id", "total_amount", "state"]]}},\"id\":2}"
```
