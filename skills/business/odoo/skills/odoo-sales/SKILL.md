---
name: odoo-sales
description: Odoo Sales operations — manage quotations, sales orders, order lines, and products.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, sales, quotations, orders, products]
    parent_skill: odoo
---
# Odoo Sales

Manage quotations, sales orders, order lines, and salable products.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List quotations (drafts)

```
ODOO sales list-quotations --limit 20
ODOO sales list-quotations --state sent
ODOO sales list-quotations --partner-id 3
```

### List confirmed orders

```
ODOO sales list-orders --limit 20
ODOO sales list-orders --state done
```

### Get order details

```
ODOO sales get 12
```

### Create quotation

```
ODOO sales create --partner-id 3
```

### Create sales order with product lines

```
ODOO sales create --partner-id 3
ODOO model sale.order.line create '{"order_id": 8, "product_id": 32, "product_uom_qty": 10, "price_unit": 50.0}'
ODOO sales confirm 8
```

### Complete Sales Order Creation (When Product/Partner May Not Exist)

**Scenario**: Creating a sales order for a new customer with products that don't exist in the system.

**Workflow**:
1. **Check if product exists**: `ODOO sales products --limit 50`
2. **Create product if missing**: `ODOO model product.product create '{"name": "Product Name", "default_code": "CODE-001", "list_price": 50.0, "type": "consu"}'`
3. **Check if partner exists**: `ODOO contacts list --limit 20` or create partner directly
4. **Create sales order**: `ODOO sales create --partner-id [partner_id]`
5. **Add order line**: `ODOO model sale.order.line create '{"order_id": [order_id], "product_id": [product_id], "product_uom_qty": [quantity], "price_unit": [unit_price]}'`
6. **Confirm order**: `ODOO sales confirm [order_id]`
7. **Verify**: `ODOO sales get [order_id]` and `ODOO sales order-lines [order_id]`

### Rice Sales Order Pattern

**Specific to Basmati Rice Sales**: When creating sales orders for rice products, use this exact pattern:
- Product ID: 1 (Basmati Rice)
- Quantity: Use actual kg weight (e.g., 100 kg)
- Price Unit: ₹75/kg for Basmati Rice
- Order Lines: Always add via raw model: `ODOO model sale.order.line create '[{"order_id": [order_id], "product_id": 1, "product_uom_qty": [quantity], "price_unit": 75.0}]'`

### Product Creation Pattern

**For consumable products (type="consu")**:
```json
{
  "name": "Product Name",
  "default_code": "CODE-001",
  "list_price": 50.0,
  "type": "consu"
}
```

**For services (type="service")**:
```json
{
  "name": "Service Name",
  "default_code": "SVC-001",
  "list_price": 0.0,
  "type": "service"
}
```

### Partner Creation Pattern

```json
{
  "name": "Customer Name",
  "email": "customer@example.com"
}
```

### Complete Sales Order Creation (When Product/Partner May Not Exist)

**Scenario**: Creating a sales order for a new customer with products that don't exist in the system.

**Workflow**:
1. **Check if product exists**: `ODOO sales products --limit 50`
2. **Create product if missing**: `ODOO model product.product create '{"name": "Product Name", "default_code": "CODE-001", "list_price": 50.0, "type": "consu"}'`
3. **Check if partner exists**: `ODOO contacts list --limit 20` or create partner directly
4. **Create sales order**: `ODOO sales create --partner-id [partner_id]`
5. **Add order line**: `ODOO model sale.order.line create '[{"order_id": [order_id], "product_id": [product_id], "product_uom_qty": [quantity], "price_unit": [unit_price]}]'`
6. **Confirm order**: `ODOO sales confirm [order_id]`
7. **Verify**: `ODOO sales get [order_id]` and `ODOO sales order-lines [order_id]`

## Common Pitfalls

1. **Simple Command Syntax**: Use basic flags like `--name "Name"` without complex arguments. When API arguments fail, use raw model operations.
2. **Invoice Line Creation**: After creating invoice, manual addition of invoice lines via `account.move.line` model is often necessary before validation.
3. **Product Dependencies**: Ensure product exists in system before creating order lines. Use `ODOO model product.product search` to verify product availability.
4. **Partner ID Format**: Partner IDs must be integers, not strings. Use JSON array format `[ID]` for calendar events.
**Workflow**:\n1. **Check if product exists**: `ODOO sales products --limit 50`\n2. **Create product if missing**: `ODOO model product.product create '{"name": "Product Name", "default_code": "CODE-001", "list_price": 50.0, "type": "consu"}'`\n3. **Check if partner exists**: `ODOO contacts list --limit 20` or create partner directly\n4. **Create sales order**: `ODOO sales create --partner-id [partner_id]`\n5. **Add order line**: `ODOO model sale.order.line create '{"order_id": [order_id], "product_id": [product_id], "product_uom_qty": [quantity], "price_unit": [unit_price]}'`\n6. **Confirm order**: `ODOO sales confirm [order_id]`\n7. **Verify**: `ODOO sales get [order_id]` and `ODOO sales order-lines [order_id]`

### Rice Sales Order Pattern

**Specific to Basmati Rice Sales**: When creating sales orders for rice products, use this exact pattern:
- Product ID: 1 (Basmati Rice)
- Quantity: Use actual kg weight (e.g., 100 kg)
- Price Unit: ₹75/kg for Basmati Rice
- Order Lines: Always add via raw model: `ODOO model sale.order.line create '[{"order_id": [order_id], "product_id": 1, "product_uom_qty": [quantity], "price_unit": 75.0}]'`

### Product Creation Pattern

**For consumable products (type="consu")**:\\n```json\\n{\\n  \\\"name\\\": \\\"Product Name\\\",\\n  \\\"default_code\\\": \\\"CODE-001\\\",\\n  \\\"list_price\\\": 50.0,\\n  \\\"type\\\": \\\"consu\\\"\\n}\\n```\\n\\n**For services (type="service")**:\\n```json\\n{\\n  \\\"name\\\": \\\"Service Name\\\",\\n  \\\"default_code\\\": \\\"SVC-001\\\",\\n  \\\"list_price\\\": 0.0,\\n  \\\"type\\\": \\\"service\\\"\\n}\\n```\\n\\n### Partner Creation Pattern\\n\\n```json\\n{\\n  \\\"name\\\": \\\"Customer Name\\\",\\n  \\\"email\\\": \\\"customer@example.com\\\"\\n}\\n```

### Rice Sales Order Pattern

**Specific to Basmati Rice Sales**: When creating sales orders for rice products, use this exact pattern:
- Product ID: 1 (Basmati Rice)
- Quantity: Use actual kg weight (e.g., 100 kg)
- Price Unit: ₹75/kg for Basmati Rice
- Order Lines: Always add via raw model: `ODOO model sale.order.line create '[{"order_id": [order_id], "product_id": 1, "product_uom_qty": [quantity], "price_unit": 75.0}]'`

### Product Creation Pattern

**For consumable products (type="consu")**:\\n```json\\n{\\n  \\\"name\\\": \\\"Product Name\\\",\\n  \\\"default_code\\\": \\\"CODE-001\\\",\\n  \\\"list_price\\\": 50.0,\\n  \\\"type\\\": \\\"consu\\\"\\n}\\n```\\n\\n**For services (type="service")**:\\n```json\\n{\\n  \\\"name\\\": \\\"Service Name\\\",\\n  \\\"default_code\\\": \\\"SVC-001\\\",\\n  \\\"list_price\\\": 0.0,\\n  \\\"type\\\": \\\"service\\\"\\n}\\n```\\n\\n### Partner Creation Pattern\\n\\n```json\\n{\\n  \\\"name\\\": \\\"Customer Name\\\",\\n  \\\"email\\\": \\\"customer@example.com\\\"\\n}\\n```

### Create invoice from sales order

```\nODOO accounting create-invoice --partner-id 23\nODOO model account.move.line create '{\"move_id\": 11, \"product_id\": 32, \"quantity\": 10, \"price_unit\": 50.0}'\nODOO accounting validate 11\n```

### Confirm quotation → sale order

```
ODOO sales confirm 12
```

### Cancel order

```
ODOO sales cancel 12
```

### Set state

```
ODOO sales set-state 12 sent
```

### List order lines

```
ODOO sales order-lines 12
```

### List salable products

```
ODOO sales products --limit 30
```

### Statistics

```
ODOO sales statistics
```

## Common Workflows

For detailed step-by-step examples of complete sales order creation, see `references/sales-order-creation-workflow.md`.

## Output Format

### list-quotations / list-orders

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 12,
      "name": "S00012",
      "partner_id": [3, "Acme Corp"],
      "date_order": "2026-05-11",
      "state": "draft",
      "amount_total": 1250.0,
      "amount_untaxed": 1000.0,
      "currency_id": [1, "USD"],
      "user_id": [2, "$ODOO_USER"],
      "invoice_status": "to invoice",
      "create_date": "2026-05-11 10:00:00"
    }
  ]
}
```

### confirm

```json
{$ODOO_DB: true, "result": true}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {"draft": 5, "sent": 2, "sale": 15, "done": 3}
}
```

## Key Models

| Model | Use |
|-------|-----|
| `sale.order` | Quotations and sales orders |
| `sale.order.line` | Individual order lines |
| `product.template` | Product templates (sale_$ODOO_DB=True) |

## State Flow

```
draft → sent → sale → done
                   ↘ cancel
```

## Rules

1. **Confirm is irreversible**: Once confirmed, a quotation becomes a sale order and generates procurement. Confirm with the user.
2. **Cancel only draft/sent**: Cannot cancel an order that's already `done`.
3. **Use raw model for advanced queries**: `ODOO model sale.order search --domain '[["amount_total",">",5000]]'`

## Curl Examples

```bash
# List draft quotations
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",2,\"$ODOO_PASS\",\"sale.order\",\"search_read\",[[\"state\",\"=\",\"draft\"]],{\"limit\":10,\"fields\":[\"name\",\"partner_id\",\"amount_total\",\"state\"]}]},\"id\":2}"

# Create quotation
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",2,\"$ODOO_PASS\",\"sale.order\",\"create\",[{\"partner_id\":3}]]},\"id\":2}"

# Confirm quotation
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",2,\"$ODOO_PASS\",\"sale.order\",\"action_confirm\",[1]]},\"id\":2}"
```
