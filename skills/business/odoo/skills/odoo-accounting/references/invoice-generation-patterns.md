# Invoice Generation Patterns

## Quick Invoice Creation

### Basic Pattern
```bash
ODOO accounting create-invoice --partner-id [partner_id]
ODOO accounting validate [invoice_id]
```

### From Sales Order
1. Confirm sales order first
2. Generate invoice using partner ID
3. Validate invoice

### Verification
```bash
ODOO accounting get-invoice [invoice_id]
ODOO accounting journal-items [invoice_id]
ODOO accounting payments --limit 20
```

### PDF Generation
```bash
ODOO model account.move call get_portal_url --method-args '[invoice_id]'
# Use curl to download PDF
```

## Session Example Results
- Invoice ID: 12
- Partner: Mehta Traders Mumbai (ID: 25)
- Amount: ₹4,500
- Status: Generated (ready for validation)