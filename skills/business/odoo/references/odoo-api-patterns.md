# Odoo API Usage Patterns & Session Notes

## Session Discovery: Furniture Business Database
**Date**: 2026-05-22
**Database**: Odoo v19.0 (Final)
**User**: admin@example.com
**Database Name**: odoo

### Database Overview
- **Partners**: 12 (mix of companies and individuals)
- **Sales Orders**: 5 (₹107,520 total revenue)
- **Stock Operations**: 9 pickings (warehouse management)
- **Purchase Orders**: 10 (₹34,620 total)
- **Financial Records**: 5 account.move records (all posted)
- **Products**: 31 items (furniture and materials)
- **Employees**: 5 staff members
- **CRM Leads**: 4 opportunities
- **System**: 579 messages, 320 attachments

### Key API Commands Discovered
```bash
# Connection verification
python3 /opt/hermes/skills/business/odoo/scripts/setup.py --check
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py check

# Data exploration
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model res.partner search --domain '[["active","=",true]]' --limit 10 --fields name,email,phone,is_company
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model sale.order search --limit 5 --fields name,state,amount_total,order_line
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model stock.picking count
python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model product.product search --limit 5 --fields name,default_code,list_price,categ_id
```

### Troubleshooting Lessons
1. **Python Path Issue**: System has python3 but not python
   - Use: `python3` instead of `python`

2. **Script Location**: API scripts are in `/opt/hermes/skills/business/odoo/scripts/`
   - setup.py: `/opt/hermes/skills/business/odoo/scripts/setup.py`
   - odoo_api.py: `/opt/hermes/skills/business/odoo/scripts/odoo_api.py`

3. **JSON Domain Format**: Must use proper JSON syntax
   - Boolean values: `true`/`false` (lowercase)
   - String arrays: `[["active","=",true]]`
   - Domain filters require exact JSON structure

### Business Context
This appears to be an Indian furniture/woodcraft business with:
- Regular B2B transactions
- Manufacturing focus (woodcraft, furniture)
- Inventory management through stock pickings
- Financial tracking through account.move
- Employee management through HR module