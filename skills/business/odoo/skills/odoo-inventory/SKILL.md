---
name: odoo-inventory
description: Odoo Inventory operations — check stock levels, manage transfers, warehouses, and products.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, inventory, stock, warehouses, transfers]
    parent_skill: odoo
---
# Odoo Inventory

Check stock levels, manage transfers/deliveries, view warehouses, and browse products.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### Check stock levels

```
ODOO inventory check-stock --product-id 5
ODOO inventory check-stock --location-id 8
ODOO inventory check-stock --product-id 5 --location-id 8
```

### List transfers

```
ODOO inventory transfers --limit 20
ODOO inventory transfers --state assigned
ODOO inventory transfers --state done
```

### Get transfer details

```
ODOO inventory get-transfer 42
```

### List move lines for a transfer

```
ODOO inventory move-lines 42
```

### List warehouses

```
ODOO inventory warehouses
```

### List products with stock info

```
ODOO inventory products --limit 30
```

### Statistics

```
ODOO inventory statistics
```

## Output Format

### check-stock

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 15,
      "product_id": [5, "Office Chair"],
      "location_id": [8, "WH/Stock"],
      "quantity": 42.0,
      "available_quantity": 42.0,
      "lot_id": false,
      "inventory_quantity": null
    }
  ]
}
```

### transfers

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 42,
      "name": "WH/OUT/00042",
      "partner_id": [3, "Acme Corp"],
      "state": "assigned",
      "scheduled_date": "2026-05-12",
      "origin": "S00012",
      "date_done": null
    }
  ]
}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {
    "stock_quants": 150,
    "transfers": {"draft": 2, "waiting": 1, "confirmed": 3, "assigned": 5, "done": 80}
  }
}
```

## Key Models

| Model | Use |
|-------|-----|
| `stock.quant` | Stock on hand per product/location |
| `stock.picking` | Transfers (delivery orders, receipts, internal) |
| `stock.move` | Individual move lines within a transfer |
| `stock.warehouse` | Warehouses |

## Transfer States

```
draft → waiting → confirmed → assigned → done
                               ↘ cancel
```

## Rules

1. **Stock can be negative**: In Odoo, stock can go negative if not configured with constraints. Negative stock means more was shipped than recorded on hand.
2. **Use model for advanced filtering**: `ODOO model stock.quant search --domain '[["quantity","<",5]]' --fields product_id,location_id,quantity`
3. **Transfers have types**: A picking's `picking_type_id` determines if it's a delivery, receipt, or internal transfer. Use `ODOO model stock.picking read 42 --fields picking_type_id` to check.
5. **Transfer completion**: When transfers show as "done" but stock quants are empty, manually set `date_done` field and process `stock.move` records with `picked = true`.

## Common Pitfalls

1. **Virtual stock only**: Purchase orders show in `virtual_available` but not `qty_available` until physical receipt
2. **Consumable restrictions**: Cannot manually create stock quants for consumable/service products
3. **Transfer processing**: Transfers may need manual `date_done` setting and move line processing
4. **Missing stock quants**: Empty stock quant results may indicate need for manual intervention
5. **Manufacturing stock sync**: After manufacturing completion, stock may not update automatically. Check:
   - Manufacturing MO state is "done"
   - Stock moves exist and are picked (`picked = true`)
   - Virtual stock may show quantity but physical stock remains 0
   - May need manual stock entry or system configuration fix

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Inventory
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"stock.quant\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["product_id", "location_id", "quantity"]]}},\"id\":2}"
```
