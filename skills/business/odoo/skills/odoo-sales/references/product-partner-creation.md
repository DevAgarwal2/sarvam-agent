# Odoo Product & Partner Creation

## Common Product Creation Pattern
```bash
python3 scripts/odoo_api.py model product.product create '{"name": "Product Name", "default_code": "CODE-001", "list_price": 50.0, "type": "consu"}'
```

## Common Partner Creation Pattern
```bash
python3 scripts/odoo_api.py model res.partner create '{"name": "Customer Name", "email": "customer@example.com"}'
```

## Notes
- Product codes should be unique (e.g., RICE-001)
- Use "consu" type for consumable products
- Partner creation optional if customer already exists