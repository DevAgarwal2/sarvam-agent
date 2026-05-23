# Supplier Management Notes

## Ramesh Suppliers Setup (2026-05-23)

### Process:
1. **Contact Creation**: Ramesh Suppliers as company contact
2. **Supplier Activation**: Updated with `supplier_rank: 1`
3. **Verification**: Confirmed appears in purchase orders

### Key Requirements:
- **Company type**: Use `is_company: true` for supplier entities
- **Supplier rank**: Must be `> 0` to appear in purchase orders
- **Contact details**: Email and phone recommended for vendor communication

### Common Pitfalls:
- **Individual contacts**: `is_company: false` contacts won't appear in POs
- **Missing rank**: Default `supplier_rank: 0` excludes from procurement
- **Partner verification**: Always check `ODOO contacts get <id>` after creation

### Example Commands:
```bash
# Create supplier
ODOO contacts create --name "Ramesh Suppliers" --is-company true --email "ramesh@example.com" --phone "+91-9923456789"

# Activate as supplier
ODOO model res.partner write <partner_id> '{"supplier_rank": 1}'

# Verify supplier status
ODOO contacts get <partner_id>
```