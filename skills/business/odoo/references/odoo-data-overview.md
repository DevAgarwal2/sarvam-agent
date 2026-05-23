# Odoo Data Analysis Patterns

## Common Record Counts for Quick Overview
- `res.partner`: 15 contacts
- `res.company`: 1 company record
- `res.users`: 1 user
- `sale.order`: 6 sales orders
- `stock.picking`: 9 stock pickings
- `purchase.order`: 10 purchase orders
- `account.move`: 5 account moves (invoices/bills)
- `hr.employee`: 5 employees
- `project.project`: 4 projects
- `crm.lead`: 4 CRM leads
- `mail.message`: 579 messages

## Sample Data Structure
### Sales Orders
```
- Order S00009 (draft, 0.00) - User
- Order S00008 (sale, 35,840.00) - Sharma Furnishings
- Order S00007 (sale, 35,840.00) - Mumbai Client
```

## Data Analysis Workflow
1. **Verify connection**: `ODOO check`
2. **Count records across key modules** to understand data volume
3. **Sample key records** to understand data structure
4. **Get detailed records** for specific analysis

## Common Analysis Questions
- **Sales Performance**: Filter by state, amount, date ranges
- **Inventory Status**: Track picking states, locations, products
- **Customer Analysis**: Filter contacts by customer status, region
- **Financial Summary**: Analyze account moves by state, date, amount