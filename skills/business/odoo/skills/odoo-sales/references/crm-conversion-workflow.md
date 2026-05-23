# CRM Lead to Opportunity Conversion Workflow

## Task: Convert CRM lead to opportunity and create quotation

### Commands Used:
```bash
# Create CRM lead for Suresh Mehta Delhi Traders
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py crm create --name "Suresh Mehta Delhi Traders"

# Update lead to opportunity with revenue details
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model crm.lead write 6 '{"type": "opportunity", "expected_revenue": 37500.0, "probability": 50.0}'

# Create sales order for quotation
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py sales create --partner-id 6

# Add order line for 50 units @ ₹75/kg
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model sale.order.line create '[{"order_id": 12, "product_id": 1, "product_uom_qty": 50, "price_unit": 75.0}]'

# Confirm quotation
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py sales confirm 12
```

### Key Patterns:
- Expected revenue = quantity × price unit
- Probability = 50% for initial opportunity
- Product ID 1 = Basmati Rice
- Price Unit = ₹75/kg
- 50 units = 50 kg of Basmati Rice