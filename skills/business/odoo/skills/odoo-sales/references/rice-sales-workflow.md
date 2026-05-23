# Rice Sales Order Workflow

## Task: Create sales order for Basmati Rice

### Commands Used:
```bash
# Create contact for Sharma Traders Delhi
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py contacts create --name "Sharma Traders Delhi" --email "info@sharmatrader.com" --phone "+91-9876543210" --city "Delhi"

# Create sales order
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py sales create --partner-id 27

# Add order line for Basmati Rice (100 kg @ ₹75/kg)
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model sale.order.line create '[{"order_id": 11, "product_id": 1, "product_uom_qty": 100, "price_unit": 75.0}]'

# Confirm order
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py sales confirm 11

# Create invoice
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py accounting create-invoice --partner-id 27

# Add invoice line
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model account.move.line create '[{"move_id": 18, "product_id": 1, "quantity": 100, "price_unit": 75.0}]'

# Validate invoice
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py accounting validate 18
```

### Key Patterns:
- Product ID 1 = Basmati Rice
- Price Unit = ₹75/kg
- Quantity = actual kg weight
- Invoice lines must be added manually after creation