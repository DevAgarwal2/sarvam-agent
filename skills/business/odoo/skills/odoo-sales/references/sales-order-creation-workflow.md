# Sales Order to Invoice Integration

## Workflow Pattern

### Step-by-Step Process
1. **Sales Order Creation**
   - Create sales order with partner
   - Add order lines with product details
   - Confirm sales order

2. **Invoice Generation**
   - Use partner ID to create invoice
   - Invoice automatically references sales order
   - Validate invoice to post

### Key Integration Points
- Sales order ID: 9 (P00014)
- Invoice ID: 12
- Partner ID: 25 (Mehta Traders Mumbai)
- Product ID: 32 (Basmati Rice)

### Common Issues
- Invoice generation requires partner ID, not sales order ID
- Sales order must be confirmed before invoice generation
- Product must exist in system before order line creation

### Success Indicators
- Sales order state: "sale"
- Invoice state: "posted"
- Payment state: "not_paid"

### Verification Commands
```bash
ODOO sales get 9
ODOO accounting get-invoice 12
ODOO accounting journal-items 12
```