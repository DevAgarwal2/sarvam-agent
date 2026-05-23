# Odoo Inventory System Failure Analysis

## Critical Issue: Stock Quant Creation Failure

### Symptoms
- `stock.quant` count = 0 for all consumable products
- All products show `qty_available: 0.0`
- Stock movements exist in `stock.move` but no quants created

### Root Cause Analysis
1. **Warehouse Configuration**: Missing proper warehouse setup
2. **Location Configuration**: Stock location not properly configured
3. **Product Type Issues**: Consumable products may have special handling requirements
4. **Workflow Configuration**: Stock quant creation workflow not triggered

### Affected Products
- Maida (ID: 33) - qty_available: 0.0, virtual_available: 200.0
- Basmati Rice (ID: 32) - qty_available: 0.0, virtual_available: -10.0
- Custom Dining Chair (ID: 31) - qty_available: 0.0, virtual_available: -8.0

### Workarounds
1. **Use virtual_available**: Monitor expected stock from incoming transfers
2. **Manual quant creation**: May require direct database intervention
3. **Check warehouse setup**: Verify `stock.warehouse` and `stock.location` configuration

### Monitoring Commands
```bash
# Check stock quants
ODOO model stock.quant search --domain '[["product_id", "in", [33, 32, 31]]]'

# Check stock moves
ODOO model stock.move search --domain '[["picked", "=", false]]'

# Check warehouse configuration
ODOO model stock.warehouse search --limit 3
ODOO model stock.location search --limit 5
```

### Resolution Steps
1. Verify warehouse configuration
2. Check location usage settings
3. Test stock movement workflow
4. Consider database-level stock quant creation if needed

## Invoice Generation Issues

### Problem
- Invoice created with 0 amount
- Manual line creation required
- `account.move.line` creation needed

### Fix Pattern
```bash
# Manual line creation
ODOO model account.move.line create '{"move_id": 12, "product_id": 32, "quantity": 100.0, "price_unit": 45.0, "name": "Basmati Rice"}'
```

### Monitoring
- Check invoice states: `ODOO model account.move search --domain '[["state", "=", "draft"]]'`
- Verify posted invoices match order amounts