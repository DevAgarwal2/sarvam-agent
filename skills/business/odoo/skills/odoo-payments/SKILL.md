---
name: odoo-payments
description: Odoo Payment Provider operations — manage payment providers, transactions, and payment methods.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, payments, payment-providers, transactions, razorpay, stripe, paypal]
    parent_skill: odoo
---
# Odoo Payment Providers

Manage payment providers, transactions, and payment methods. Integrated into the **Invoicing** and **Sales** apps — no standalone menu. Access payment providers from Invoicing > Configuration > Payment Providers.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List payment providers

```
ODOO model payment.provider search --limit 20 --fields name,code,state,is_published,company_id
ODOO model payment.provider search --domain '[["state","=","enabled"]]' --fields name,code,is_published
```

### Get payment provider details

```
ODOO model payment.provider read 1 --fields name,code,state,is_published,module_id,company_id,redirect_form_view_id
```

### List payment transactions

```
ODOO model payment.transaction search --limit 20 --fields reference,provider_id,partner_id,amount,currency_id,state,operation
ODOO model payment.transaction search --domain '[["state","!=","draft"]]' --fields reference,provider_id,amount,state
```

### Get transaction details

```
ODOO model payment.transaction read 1 --fields reference,provider_id,partner_id,amount,currency_id,state,operation,last_state_change,payment_method_id
```

### List payment methods

```
ODOO model payment.method search --fields name,code,primary_payment_method_id
ODOO model payment.method line search --domain '[["provider_id","=",1]]' --fields name,payment_method_id,provider_id
```

### List account payments

```
ODOO model account.payment search --limit 20 --fields name,partner_id,payment_type,amount,state,date
```

## Key Models

| Model | Use |
|-------|-----|
| `payment.provider` | Payment providers (Stripe, Razorpay, PayPal, etc.) |
| `payment.transaction` | Individual payment transactions |
| `payment.method` | Payment method types (card, bank, digital wallet) |
| `account.payment` | Accounting payment records |

## Provider States

| State | Meaning |
|-------|---------|
| `disabled` | Provider is not available |
| `enabled` | Provider is active and accepting payments |
| `test` | Provider is in test/sandbox mode |

## Rules

1. **Provider must be enabled**: Check `state = enabled` before processing payments through a provider.
2. **Transactions have limited retry**: Failed transactions can be retried only if `state = draft` or `state = pending`.
3. **Razorpay for India**: For India-based stores, `payment_razorpay` is installed and available for INR payments.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List payment transactions
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"payment.transaction\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"reference\",\"amount\",\"state\",\"provider_id\"]}]},\"id\":2}"
```
