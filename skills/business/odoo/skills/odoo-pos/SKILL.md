---
name: odoo-pos
description: Odoo Point of Sale operations — manage POS orders, sessions, and configurations.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, pos, point-of-sale, retail, orders]
    parent_skill: odoo
---
# Odoo Point of Sale

Manage POS orders, sessions, and configurations.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List POS orders

```
ODOO model pos.order search --limit 20 --fields name,partner_id,amount_total,state,date_order,user_id,session_id
ODOO model pos.order search --domain '[["state","=","paid"]]' --limit 20 --fields name,amount_total,date_order
```

### Get POS order details

```
ODOO model pos.order read 1 --fields name,partner_id,lines,amount_total,amount_paid,amount_tax,state,date_order,user_id,session_id
```

### List POS sessions

```
ODOO model pos.session search --limit 20 --fields name,config_id,user_id,state,start_at,stop_at
ODOO model pos.session search --domain '[["state","=","opened"]]' --fields name,config_id,user_id,start_at
```

### List POS configurations

```
ODOO model pos.config search --limit 20 --fields name,company_id,picking_type_id,invoice_journal_id
```

### List POS order lines

```
ODOO model pos.order.line search --domain '[["order_id","=",1]]' --fields product_id,qty,price_unit,price_subtotal
```

### List POS payments

```
ODOO model pos.payment search --domain '[["pos_order_id","=",1]]' --fields payment_method_id,amount,name
```

### Statistics

```
ODOO model pos.order count --domain '[["state","=","paid"]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `pos.order` | POS orders |
| `pos.order.line` | POS order lines |
| `pos.session` | POS sessions (opened/closed) |
| `pos.config` | POS shop configuration |
| `pos.payment` | POS payments per order |
| `pos.payment.method` | Payment methods (cash, card, etc.) |

## Rules

1. **Sessions must be opened first**: POS orders can only be created in an opened session. Check session state before creating orders.
2. **Orders cannot be modified after payment**: Once an order is `paid` or `done`, it becomes read-only. Use refunds for corrections.
3. **Use Inventory for stock movements**: POS order fulfillment creates stock moves. Check `stock.picking` linked to the POS session for inventory impact.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List POS orders
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"pos.order\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"amount_total\",\"state\"]}]},\"id\":2}"
```
