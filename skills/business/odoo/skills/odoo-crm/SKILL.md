---
name: odoo-crm
description: Odoo CRM operations — manage leads, opportunities, pipeline stages, and sales activities.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, crm, leads, opportunities, sales-pipeline]
    parent_skill: odoo
---
# Odoo CRM

Manage leads, opportunities, pipeline stages, and sales activities via the Odoo `crm` subcommand.

**Prerequisite:** The `odoo` skill must be set up first. Run `python scripts/setup.py --check` from the parent `business/odoo/` directory.

## Usage

All commands use `ODOO crm <action>`. `ODOO` = `python scripts/odoo_api.py` from the `business/odoo/scripts/` directory.

### List leads

```
ODOO crm list-leads --limit 20
ODOO crm list-leads --user-id 2 --limit 10
ODOO crm list-leads --team-id 1
```

### List opportunities

```
ODOO crm list-opportunities --limit 20
ODOO crm list-opportunities --user-id 2
```

### Get a lead/opportunity

```
ODOO crm get 5
```

### Create a lead

```
ODOO crm create --name "New Lead" --partner-id 3 --email-from "contact@acme.com"
```

Create an opportunity:
```
ODOO crm create --name "Big Deal" --type opportunity --expected-revenue 50000 --probability 10
```

### Update a lead

```
ODOO crm update 7 --stage-id 3 --user-id 2
ODOO crm update 7 --priority 3
```

Bulk update multiple leads:
```
ODOO crm update "[7, 8, 9]" --values '{"stage_id": 3}'
```

### Delete a lead

```
ODOO crm delete 15
```

**Always confirm with the user before deleting.**

### List pipeline stages

```
ODOO crm stages
```

### Statistics

```
ODOO crm statistics
```

## Output Format

### list-leads / list-opportunities

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 7,
      "name": "Acme Corp Deal",
      "partner_id": [3, "Acme Corp"],
      "email_from": "contact@acme.com",
      "phone": null,
      "type": "lead",
      "stage_id": [1, "New"],
      "user_id": [2, "$ODOO_USER"],
      "team_id": [1, "Sales"],
      "priority": "2",
      "expected_revenue": 50000.0,
      "date_deadline": "2026-06-01",
      "create_date": "2026-05-11 10:00:00",
      "activity_date_deadline": "2026-05-15"
    }
  ]
}
```

### get

Same as above, single object.

### create

```json
{$ODOO_DB: true, "result": 8}
```

### update / delete

```json
{$ODOO_DB: true, "result": true}
```

### stages

```json
{
  $ODOO_DB: true,
  "result": [
    {"id": 1, "name": "New", "sequence": 1, "is_won": false, "team_id": false},
    {"id": 2, "name": "Qualified", "sequence": 2, "is_won": false, "team_id": false},
    {"id": 3, "name": "Won", "sequence": 99, "is_won": true, "team_id": false}
  ]
}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {
    "total_leads": 42,
    "leads": 15,
    "opportunities": 27
  }
}
```

## Key Models

| Model | Use |
|-------|-----|
| `crm.lead` | Leads and opportunities |
| `crm.stage` | Pipeline stages |
| `crm.team` | Sales teams |

## Common Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | char | Lead/opportunity title (required) |
| `partner_id` | many2one | Contact/company |
| `email_from` | char | Email address |
| `phone` | char | Phone number |
| `type` | selection | `lead` or `opportunity` |
| `stage_id` | many2one | Pipeline stage |
| `user_id` | many2one | Assigned salesperson |
| `team_id` | many2one | Sales team |
| `priority` | selection | `0`, `1`, `2`, `3` (3 = highest) |
| `expected_revenue` | monetary | Expected deal value |
| `probability` | float | Win probability (0-100) |
| `date_deadline` | date | Expected close date |
| `description` | text | Notes/details |

## Rules

1. **Stages are sequential**: Lower `sequence` = earlier stage. `is_won=True` = won.
2. **Type matters**: `lead` → initial unqualified; `opportunity` → qualified with revenue/probability.
3. **Use the parent skill's `model` command** for operations not covered here: `ODOO model crm.lead search --domain '[["type","=","opportunity"],["priority",">",2]]'`
4. **Confirm deletes**: Always ask before running `delete`.

## Curl Examples

Authenticate first, then query:

```bash
# Auth
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List leads
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"crm.lead\",\"search_read\",[[\"type\",\"=\",\"lead\"]],{\"limit\":10,\"fields\":[\"name\",\"email_from\",\"stage_id\",\"user_id\"]}]},\"id\":2}"

# Create lead
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"crm.lead\",\"create\",[{\"name\":\"New Lead\",\"type\":\"lead\"}]]},\"id\":2}"
```
