---
name: odoo-purchase
description: Odoo Purchase operations — manage RFQs, purchase orders, order lines, and vendor interactions.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, purchase, rfqs, procurement, vendors]
    parent_skill: odoo
---
# Odoo Purchase

Manage requests for quotation (RFQs), purchase orders (POs), and vendor procurement.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List RFQs (drafts)

```
ODOO purchase list-rfqs --limit 20
ODOO purchase list-rfqs --partner-id 3
```

### List confirmed purchase orders

```
ODOO purchase list-orders --limit 20
ODOO purchase list-orders --state done
```

### Get PO details

```
ODOO purchase get 30
```

### Create RFQ

```
ODOO purchase create --partner-id 3
```

With lines:
```
ODOO purchase create --partner-id 3 --order-lines '[{"product_id":10,"product_qty":50,"price_unit":12.5}]'
```

### Confirm RFQ → Purchase Order

```
ODOO purchase confirm 30
```

### Cancel PO

```
ODOO purchase cancel 30
```

### List order lines

```
ODOO purchase order-lines 30
```

### Statistics

```
ODOO purchase statistics
```

## Output Format

### list-rfqs / list-orders

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 30,
      "name": "P00030",
      "partner_id": [3, "Best Supplies Ltd"],
      "date_order": "2026-05-11",
      "date_planned": "2026-05-20",
      "state": "draft",
      "amount_total": 3125.0,
      "currency_id": [1, "USD"],
      "user_id": [2, "$ODOO_USER"],
      "origin": ""
    }
  ]
}
```

### confirm / cancel

```json
{$ODOO_DB: true, "result": true}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {"draft_rfq": 3, "sent": 1, "confirmed": 8, "done": 25}
}
```

## Key Models

| Model | Use |
|-------|-----|
| `purchase.order` | RFQs and purchase orders |
| `purchase.order.line` | Individual order lines |

## State Flow

```
draft → sent → purchase → done
                   ↘ cancel
```

## Rules

1. **Confirm creates receipts**: Confirming a PO creates an incoming transfer in Inventory. Cannot reverse confirmation.
2. **Partner must be a vendor**: The partner must have `supplier_rank > 0`. Check with `ODOO contacts get <partner_id>` and update with `ODOO model res.partner write <partner_id> '{"supplier_rank": 1}'` if needed.
3. **Use raw model for line detail**: `ODOO model purchase.order read 30 --fields partner_id,date_planned,order_line,amount_total`
4. **Product creation**: If product doesn't exist, create it first with `ODOO model product.product create '{"name": "Product Name", "type": "consu", "default_code": "CODE-001"}'`
5. **Order line creation**: When `create --order-lines` fails, create PO first then add lines via `ODOO model purchase.order.line create`

## Common Pitfalls

1. **Product not found**: Always verify product exists before creating PO lines
2. **Supplier not marked**: Partners must have `supplier_rank > 0` to appear in purchase orders
3. **Order line syntax**: Complex order lines may require separate creation after PO creation
4. **Virtual vs physical stock**: Confirming PO creates virtual stock but not physical stock until transfer is processed

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Purchase
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"purchase.order\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "partner_id", "amount_total", "state"]]}},\"id\":2}"
```
