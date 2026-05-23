---
name: odoo-data-recycle
description: Odoo Data Recycle operations — view and restore deleted records across the system.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, data-recycle, trash, restore, deleted-records]
    parent_skill: odoo
---
# Odoo Data Recycle

View and restore soft-deleted records across the system.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List deleted records

```
ODOO model data_recycle.record search --limit 20 --fields res_model,res_id,display_name,deleted_date,deleted_by,restored
ODOO model data_recycle.record search --domain '[["restored","=",false]]' --fields res_model,res_id,display_name,deleted_date
```

### Get deleted record details

```
ODOO model data_recycle.record read 1 --fields res_model,res_id,display_name,deleted_date,deleted_by,restored,json_data
```

### View original record data

```
ODOO model data_recycle.record read 1 --fields res_model,res_id,display_name,json_data
```

### Restore a deleted record

```
ODOO model data_recycle.record restore 1
```

### Count deleted records by model

```
ODOO model data_recycle.record count --domain '[["restored","=",false]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `data_recycle.record` | Soft-deleted records |

## Rules

1. **Not all models are tracked**: Only models configured in `data_recycle.model` are tracked for soft deletion.
2. **Restore is one-way**: Once restored, the record goes back to active status. The recycle record itself stays as a log.
3. **JSON data stores original**: `json_data` field contains the full record before deletion. Use `python3 -c "import json;print(json.dumps(json.loads(data),indent=2))"` for readable output.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List deleted records
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"data_recycle.record\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"res_model\",\"display_name\",\"deleted_date\"]}]},\"id\":2}"
```
