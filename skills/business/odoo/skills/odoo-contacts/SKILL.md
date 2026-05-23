---
name: odoo-contacts
description: Odoo Contacts operations — manage companies, individuals, addresses, and partner data.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, contacts, partners, companies, addresses]
    parent_skill: odoo
---
# Odoo Contacts

Manage companies, individual contacts, addresses, and partner relationships.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List contacts

```
ODOO contacts list --limit 20
ODOO contacts list --is-company true
ODOO contacts list --is-company false --limit 50
```

### Search contacts

```
ODOO contacts search "Acme" --limit 10
```

### Get contact details

```
ODOO contacts get 3
```

### Create contact

```
ODOO contacts create --name "Acme Corp" --is-company true --email "info@acme.com" --phone "+1-555-0100"
ODOO contacts create --name "Jane Smith" --is-company false --email "jane@acme.com" --phone "+1-555-0101" --parent-id 3
```

### Update contact

```
ODOO contacts update 3 '{"phone": "+1-555-0200", "city": "New York"}'
```

### Delete contact

```
ODOO contacts delete 15
```

**Always confirm with the user before deleting.**

### Statistics

```
ODOO contacts statistics
```

## Output Format

### list / search

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 3,
      "name": "Acme Corp",
      "email": "info@acme.com",
      "phone": "+1-555-0100",
      "customer_rank": 1,
      "supplier_rank": 0,
      "is_company": true,
      "type": "contact",
      "street": "123 Main St",
      "city": "New York",
      "create_date": "2026-01-15"
    }
  ]
}
```

### get

```json
{
  $ODOO_DB: true,
  "result": [
    {
      "id": 3,
      "name": "Acme Corp",
      "email": "info@acme.com",
      "phone": "+1-555-0100",
      "mobile": null,
      "website": "https://acme.com",
      "is_company": true,
      "parent_id": false,
      "type": "contact",
      "street": "123 Main St",
      "street2": null,
      "city": "New York",
      "zip": "10001",
      "state_id": [12, "New York"],
      "country_id": [233, "United States"],
      "vat": null,
      "comment": null,
      "customer_rank": 1,
      "supplier_rank": 0
    }
  ]
}
```

### statistics

```json
{
  $ODOO_DB: true,
  "result": {"total": 150, "companies": 45, "individuals": 105, "customers": 30, "suppliers": 12}
}
```

## Key Models

| Model | Use |
|-------|-----|
| `res.partner` | Companies and individual contacts |
| `res.country` | Countries |
| `res.country.state` | States/provinces |

## Rules

1. **is_company matters**: `true` = company, `false` = individual. Company contacts can have child contacts (`parent_id`).
2. **customer_rank / supplier_rank**: `0` = not a customer/supplier, `1` = is one. Multi-company setups may use higher numbers.
3. **Delete cascade**: Deleting a partner may fail if linked to orders/invoices. Remove those first.
4. **Use raw model for bulk**: `ODOO model res.partner search --domain '[["customer_rank",">",0]]' --fields name,email,phone,city`
5. **Supplier setup**: For purchase orders, partners must have `supplier_rank > 0`. Create with `ODOO contacts create --is-company true` then update with `ODOO model res.partner write <partner_id> '{"supplier_rank": 1}'`.

## Common Pitfalls

1. **Supplier not marked**: Contacts created as individuals need `supplier_rank` set to appear in purchase orders
2. **Company vs individual**: Use `is_company: true` for supplier entities, `false` for individual contacts
3. **Rank values**: Higher numbers may be used in multi-company setups, but `1` is sufficient for single-company

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Contacts
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"res.partner\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "email", "phone", "is_company"]]}},\"id\":2}"
```
