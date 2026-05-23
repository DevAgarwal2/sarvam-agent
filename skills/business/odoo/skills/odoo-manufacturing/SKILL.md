---
name: odoo-manufacturing
description: Odoo Manufacturing (MRP) operations — manage production orders, BOMs, work orders, and production status.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, manufacturing, mrp, boms, production, work-orders]
    parent_skill: odoo
---
# Odoo Manufacturing

Manage manufacturing orders (MOs), bills of materials (BOMs), and work orders.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List manufacturing orders

```
ODOO manufacturing list-orders --limit 20
ODOO manufacturing list-orders --state draft
ODOO manufacturing list-orders --state progress
```

### Get MO details

```
ODOO manufacturing get-order 55
```

### Create manufacturing order

```
ODOO manufacturing create-order --product-id 5 --qty 10
ODOO manufacturing create-order --product-id 5 --qty 5 --bom-id 3
```

### Confirm MO

```
ODOO manufacturing confirm 55
```

### Plan MO (set qty producing)

```
ODOO manufacturing set-qty-producing 55
```

### List BOMs

```
ODOO manufacturing boms --limit 30
```

### Get BOM details

```
ODOO manufacturing get-bom 3
```

### List BOM lines (components)

```
ODOO manufacturing bom-lines 3
```

### List work orders for an MO

```
ODOO manufacturing work-orders 55
```

### Statistics

```
ODOO manufacturing statistics
```

## Output Format

### list-orders

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 55,
      "name": "WH/MO/00055",
      "product_id": [5, "Office Chair"],
      "product_qty": 10.0,
      "bom_id": [3, "Office Chair BOM"],
      "state": "confirmed",
      "date_planned_start": "2026-05-12",
      "date_planned_finished": "2026-05-14",
      "user_id": [2, "$ODOO_USER"],
      "origin": "S00012"
    }
  ]
}
```

### boms

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 3,
      "product_tmpl_id": [5, "Office Chair"],
      "code": null,
      "product_qty": 1.0,
      "type": "normal"
    }
  ]
}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {
    "production_orders": {"draft": 3, "confirmed": 2, "in_progress": 5, "done": 20},
    "boms": 8
  }
}
```

## Key Models

| Model | Use |
|-------|-----|
| `mrp.production` | Manufacturing orders |
| `mrp.bom` | Bills of materials |
| `mrp.bom.line` | BOM components |
| `mrp.workorder` | Work orders within an MO |
| `mrp.workcenter` | Work centers/machines |

## MO State Flow

```
draft → confirmed → progress → done
                   ↘ cancel
```

## Rules

1. **BOM is required to confirm**: Use `--bom-id` when creating if the product has multiple BOMs.
2. **Confirm generates movements**: Confirming an MO creates raw material movements. Canceling unreverses them.
3. **Work orders show progress**: Once planned, work orders are created. Check `work-orders` for detailed progress.
4. **Use raw model for BOM cost analysis**: `ODOO model mrp.bom read 3 --fields product_qty,bom_line_ids,product_tmpl_id`

## Common Pitfalls

1. **Manufacturing complete but stock not updated**: After setting MO state to "done", stock quants may not be created automatically. Manual intervention required:
   - Check `stock.quant` for the product
   - If empty, verify `stock.move` records exist and are picked
   - May need to process `stock.move` records with `picked = true`
   - **CRITICAL**: Always verify both `qty_available` (physical) and `virtual_available` (expected) stock levels
2. **Consumable products**: Manufacturing consumable products may not create stock quants automatically
3. **Virtual stock vs physical stock**: MO completion may only update `virtual_available`, not `qty_available`
4. **Missing stock update**: Always verify stock levels after MO completion using `ODOO inventory check-stock --product-id PRODUCT_ID`
5. **Stock quant creation failure**: If `stock.quant` count is 0 for all products, the entire inventory tracking system is broken and requires immediate attention

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Manufacturing
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"mrp.production\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "product_id", "state", "date_start"]]}},\"id\":2}"
```
