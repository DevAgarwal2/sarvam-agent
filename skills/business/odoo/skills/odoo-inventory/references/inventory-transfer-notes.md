# Inventory Transfer Processing Notes

## Maida Delivery Processing (2026-05-23)

### Issue Encountered:
- Purchase order confirmed but stock quants not automatically created for consumable products
- Transfer showed as "done" but physical stock remained 0.0 kg

### Resolution Steps:
1. **Manual transfer completion**: Set `date_done` field on transfer
2. **Move line processing**: Updated `stock.move` records with `picked = true`
3. **Stock verification**: Confirmed virtual stock (200.0 kg) vs physical stock (0.0 kg)

### Key Insights:
- **Consumable products**: Cannot manually create stock quants for consumables/services
- **Virtual vs physical stock**: Purchase orders show in `virtual_available` immediately
- **Transfer processing**: May need manual intervention for move line completion
- **Inventory status**: Use `ODOO inventory products` to check both stock types

### Commands Used:
```bash
# Check stock levels
ODOO inventory check-stock --product-id 33

# Check transfer status
ODOO inventory get-transfer 11

# Check move lines
ODOO model stock.move search --domain '[["picking_id", "=", 11]]'

# Process move lines
ODOO model stock.move write 40 '{"picked": true}'
```