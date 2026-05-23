---
name: odoo-accounting
description: Odoo Accounting operations — manage invoices, bills, journal entries, payments, and financial reports.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, accounting, invoices, bills, payments, journal]
    parent_skill: odoo
---
# Odoo Accounting

Manage customer invoices, vendor bills, journal entries, and payments.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List customer invoices

```
ODOO accounting invoices --limit 20
ODOO accounting invoices --state posted
ODOO accounting invoices --invoice-type in_invoice
```

### List vendor bills

```
ODOO accounting bills --limit 20
ODOO accounting bills --state posted
```

### Get invoice details

```
ODOO accounting get-invoice 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### Download PDF via API (Workaround)

```bash
# Get portal URL first
ODOO model account.move call get_portal_url --method-args '[11]'

# Use curl to download PDF
curl -L -o invoice.pdf "http://host.docker.internal:8069/my/invoices/11?access_token=TOKEN&download=1"
```

**Note:** Direct PDF generation methods like `action_get_invoice_pdf` and `action_document` are not available. Use the portal URL method instead.

### Create invoice with lines

```
ODOO accounting create-invoice --partner-id 23
ODOO model account.move.line create '{"move_id": 11, "product_id": 32, "quantity": 10, "price_unit": 50.0}'
ODOO accounting validate 11
```

### Complete Sales Order to Invoice Workflow

**Scenario**: Creating a sales order, confirming it, and generating an invoice in sequence.

**Workflow**:\n1. **Create sales order**: `ODOO sales create --partner-id [partner_id]`\n2. **Add order lines**: `ODOO model sale.order.line create '[{"order_id": [order_id], "product_id": [product_id], "product_uom_qty": [quantity], "price_unit": [unit_price]}]'`\n3. **Confirm sales order**: `ODOO sales confirm [order_id]`\n4. **Generate invoice**: `ODOO accounting create-invoice --partner-id [partner_id]`\n5. **Validate invoice**: `ODOO accounting validate [invoice_id]`\n6. **Verify**: Check invoice status and payment state

### Validate / post invoice

```
ODOO accounting validate 25
```

### Generate PDF invoice

```
ODOO accounting get-invoice 25
# Access portal URL for PDF download:
ODOO accounting portal-url 25
```

### List journal items

```
ODOO accounting journal-items 25
```

### List payments

```
ODOO accounting payments --limit 20
```

### Statistics

```
ODOO accounting statistics
```

### Get portal URL for PDF download

```
ODOO model account.move call get_portal_url --method-args '[invoice_id]'
```

## Output Format

### invoices / bills

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 25,
      "name": "INV/2026/00025",
      "ref": null,
      "partner_id": [3, "Acme Corp"],
      "date": "2026-05-11",
      "invoice_date": "2026-05-11",
      "state": "posted",
      "move_type": "out_invoice",
      "amount_total": 1250.0,
      "amount_untaxed": 1000.0,
      "currency_id": [1, "USD"],
      "payment_state": "not_paid"
    }
  ]
}
```

### journal-items

```json
{
  $ODOO_DB: true,
  "result": [
    {"id": 45, "name": "Product X", "account_id": [15, "200000 Product Sales"], "debit": 0.0, "credit": 1000.0, "balance": -1000.0, "date": "2026-05-11"},
    {"id": 46, "name": "", "account_id": [10, "121000 Account Receivable"], "debit": 1250.0, "credit": 0.0, "balance": 1250.0, "date": "2026-05-11"}
  ]
}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {"draft": 5, "posted": 42, "customer_invoices": 30, "vendor_bills": 12}
}
```

## Key Models

| Model | Use |
|-------|-----|
| `account.move` | Journal entries, invoices, bills |
| `account.move.line` | Journal items (debits/credits) |
| `account.payment` | Payments |
| `account.journal` | Journals (sale, purchase, bank, cash) |

## Move Types

| Type | Description |
|------|-------------|
| `out_invoice` | Customer invoice |
| `out_refund` | Customer credit note |
| `in_invoice` | Vendor bill |
| `in_refund` | Vendor credit note |
| `entry` | Miscellaneous journal entry |

## State Flow

```
draft → posted
         ↘ cancel
```

## Key Models

| Model | Use |
|-------|-----|
| `account.move` | Journal entries, invoices, bills |
| `account.move.line` | Journal items (debits/credits) |
| `account.payment` | Payments |
| `account.journal` | Journals (sale, purchase, bank, cash) |

## Move Types

| Type | Description |
|------|-------------|
| `out_invoice` | Customer invoice |
| `out_refund` | Customer credit note |
| `in_invoice` | Vendor bill |
| `in_refund` | Vendor credit note |
| `entry` | Miscellaneous journal entry |

## State Flow

```
draft → posted
         ↘ cancel
```

## Common Pitfalls

1. **Invoice Validation Issues**: Invoice validation may fail with "false" response even when data is correct. Check that all required fields are populated and invoice lines are properly linked before validation.
2. **Manual Line Creation Required**: After creating invoice, manual addition of invoice lines via `account.move.line` model is often necessary before validation.
3. **Product ID Dependencies**: Ensure product exists in system before creating invoice lines. Use `ODOO model product.product search` to verify product availability.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,$ODOO_USER,$ODOO_PASS,{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Accounting
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,$ODOO_PASS,\"account.move\",\"search_read\",[[]],{\"limit\":10,\"fields\":[[\"name\", \"partner_id\", \"amount_total\", \"state\"]]}},\"id\":2}"
```

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Accounting
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"account.move\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "partner_id", "amount_total", "state"]]}},\"id\":2}"
```
