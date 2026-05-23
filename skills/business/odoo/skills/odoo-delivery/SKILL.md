---
name: odoo-delivery
description: Odoo Delivery & Shipping operations — manage delivery methods, carriers, and shipping costs.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, delivery, shipping, carriers, logistics]
    parent_skill: odoo
---
# Odoo Delivery & Shipping

Manage delivery methods, carriers, and shipping costs. Integrated into the **Inventory** app — no standalone menu. Access delivery carriers and shipping methods from Inventory > Configuration > Delivery.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List delivery carriers

```
ODOO model delivery.carrier search --limit 20 --fields name,delivery_type,product_id,active
ODOO model delivery.carrier read 1 --fields name,delivery_type,product_id,integration_level,active,free_over,amount,tariff_id
```

### List delivery price rules

```
ODOO model delivery.price.rule search --limit 20 --fields carrier_id,list_price,variable,max_value
```

### List delivery pickings

```
ODOO model stock.picking search --domain '[["picking_type_code","=","outgoing"]]' --limit 20 --fields name,partner_id,carrier_id,state,scheduled_date,origin
ODOO model stock.picking search --domain '[["carrier_id","!=",false]]' --limit 20 --fields name,carrier_id,state,partner_id
```

### Check delivery methods for a sale order

```
ODOO model sale.order read 1 --fields name,partner_id,carrier_id,delivery_price,amount_total,shipping_weight
```

### Get delivery grids

```
ODOO model delivery.carrier get	delivery.price.rules 1
```

## Key Models

| Model | Use |
|-------|-----|
| `delivery.carrier` | Shipping carriers/methods |
| `delivery.price.rule` | Carrier pricing rules |
| `stock.picking` | Delivery transfers (outgoing) |
| `stock.package` | Packages for deliveries |
| `sale.order` | Carrier reference on orders |

## Rules

1. **Carrier is set on sale.order**: The delivery method is chosen at quotation/order level. Check `sale.order.carrier_id`.
2. **Delivery creates stock moves**: Confirming delivery creates outgoing `stock.picking` transfers. Track via Inventory.
3. **Integration levels**: Carriers can be `rate` (API rates), `rate_and_ship` (full integration), or `basic` (manual).

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List carriers
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"delivery.carrier\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"delivery_type\",\"active\"]}]},\"id\":2}"
```
