---
name: odoo-restaurant
description: Odoo Restaurant operations — manage restaurant floors, tables, and POS restaurant orders.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, restaurant, dining, tables, pos]
    parent_skill: odoo
---
# Odoo Restaurant

Manage restaurant floors, tables, and POS restaurant orders.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List restaurant floors

```
ODOO model pos.restaurant.floor search --fields name,pos_config_ids,table_ids,background_color
ODOO model pos.restaurant.floor read 1 --fields name,table_ids,background_color,pos_config_ids
```

### List tables

```
ODOO model rest.table search --limit 20 --fields name,floor_id,seats,width,height,pos_x,pos_y,active,shape
ODOO model rest.table search --domain '[["floor_id","=",1]]' --fields name,seats,active,shape
```

### Get table details

```
ODOO model rest.table read 1 --fields name,floor_id,seats,width,height,pos_x,pos_y,active,shape,color
```

### List POS orders for restaurant

```
ODOO model pos.order search --domain '[["table_id","!=",false]]' --limit 20 --fields name,table_id,amount_total,state,date_order,user_id
ODOO model pos.order search --domain '[["table_id","=",1]]' --fields name,amount_total,state
```

## Key Models

| Model | Use |
|-------|-----|
| `restaurant.floor` | Restaurant floor layouts |
| `restaurant.table` | Individual tables on floors |
| `pos.order` | POS orders (with `table_id` set) |

## Key Fields

**restaurant.table**: `table_number` (required, integer), `floor_id`, `seats`, `shape` (square/round), `width`, `height`, `position_h`, `position_v`

## Rules

1. **Tables belong to floors**: Each `restaurant.table` has a `floor_id` referencing its floor. Tables are positioned via `position_h`/`position_v`.
2. **Orders link to tables**: POS restaurant orders have `table_id` set to track which table ordered.
3. **Floor has POS configs**: `pos_config_ids` on a floor determines which POS configurations serve that floor.
4. **Tables use `table_number` not `name`**: The table's display name is derived from `table_number` and `floor_id`.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List tables
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"restaurant.table\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"table_number\",\"floor_id\",\"seats\",\"shape\"]}]},\"id\":2}"
```
