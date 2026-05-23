---
name: odoo-loyalty
description: Odoo Coupons & Loyalty operations — manage loyalty programs, coupons, and reward rules.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, loyalty, coupons, promotions, rewards, gift-cards]
    parent_skill: odoo
---
# Odoo Coupons & Loyalty

Manage loyalty programs, coupons, promotions, gift cards, and reward rules. Integrated into the **Sales** app — no standalone menu. Access loyalty programs from Sales > Products > Loyalty Programs.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List loyalty programs

```
ODOO model loyalty.program search --limit 20 --fields name,program_type,trigger,applies_on,date_to,active
ODOO model loyalty.program search --domain '[["active","=",true]]' --fields name,program_type,trigger,applies_on
```

### List coupons/cards

```
ODOO model loyalty.card search --limit 20 --fields code,partner_id,program_id,points,expiration_date,active
ODOO model loyalty.card search --domain '[["partner_id","=",3]]' --fields code,program_id,points,expiration_date
```

### List reward rules

```
ODOO model loyalty.rule search --limit 20 --fields name,program_id,minimum_amount,reward_point_amount,reward_point_mode
ODOO model loyalty.reward search --fields program_id,reward_type,discount,description,discount_line_product_id
```

### Check loyalty on sale orders

```
ODOO model sale.order read 1 --fields name,partner_id,amount_total,no_code_promo_program_ids,code_promo_program_id
ODOO model sale.order read 1 --fields name,reward_amount,reward_points,coupon_ids
```

## Key Models

| Model | Use |
|-------|-----|
| `loyalty.program` | Loyalty/coupon programs |
| `loyalty.card` | Individual customer loyalty cards |
| `loyalty.rule` | Earning rules per program |
| `loyalty.reward` | Reward definitions |
| `loyalty.coupon` | Coupon instances |

## Program Types

| Type | Use |
|------|-----|
| `promotion` | Automatic promotions (no code) |
| `promo_code` | Promo code based |
| `loyalty` | Point-based loyalty |
| `gift_card` | Gift cards |

## Rules

1. **Programs can stack or exclude**: Check `program_type` and `applies_on` to understand if multiple programs apply to the same order.
2. **Coupons expire**: Always check `expiration_date` on `loyalty.card.coupon`.
3. **Gift cards are treated as loyalty**: Gift cards use the same model with `program_type = gift_card`.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List loyalty programs
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"loyalty.program\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"program_type\",\"active\"]}]},\"id\":2}"
```
