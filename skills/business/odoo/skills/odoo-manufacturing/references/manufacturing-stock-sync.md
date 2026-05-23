# Manufacturing Stock Sync Issues

## Session: 2026-05-23
### Problem Identified
- Manufacturing Order completed successfully
- Stock quants not created automatically
- `qty_available`: 0.0 (physical stock)
- `virtual_available`: 500.0 (expected stock)

### Root Cause
Consumable products in Odoo 19.0 may not create stock quants automatically after MO completion.

### Resolution Steps
1. Check `stock.move` records exist for the product
2. Verify `picked = true` status on stock moves
3. Manual stock quant creation may be required
4. Verify both physical and virtual stock levels

### Verification Commands
```bash
# Check stock quants
ODOO model stock.quant search --domain '[["product_id", "=", PRODUCT_ID]]'

# Check stock moves
ODOO model stock.move search --domain '[["picking_id", "=", PICKING_ID]]'

# Verify stock levels
ODOO inventory check-stock --product-id PRODUCT_ID
```

### Status
- **Issue**: Stock quant creation system not working for consumables
- **Impact**: Cannot track physical inventory
- **Workaround**: Manual stock entry required
- **Priority**: HIGH - Affects all manufacturing operations