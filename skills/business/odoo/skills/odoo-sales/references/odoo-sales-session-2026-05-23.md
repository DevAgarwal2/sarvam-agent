# Odoo Sales Session - 2026-05-23

## User Request Summary:
Create Sharma Traders contact, sales order for 100kg Basmati Rice @ ₹75/kg, invoice, then create CRM lead for Suresh Mehta, convert to opportunity, create quotation for 50 units, and schedule meeting for tomorrow 11 AM.

## Key Learnings:

### Command Syntax Patterns:
- **Simple create commands**: `ODOO contacts create --name "Name"` (no complex flags)
- **Model operations**: Use raw model for complex operations like order lines and CRM updates
- **Invoice creation**: Requires manual line addition after creation
- **Calendar events**: Use `--partner-ids "[ID]"` format for attendees

### Product/Pricing Patterns:
- Product ID 1 = Basmati Rice
- Price Unit = ₹75/kg (consistent across orders)
- Quantity = actual kg weight
- Expected revenue = quantity × price unit

### Error Handling:
- When API arguments fail, use raw model operations
- Invoice validation may require manual line creation first
- Partner IDs must be integers, not strings

### Workflow Sequence:
1. Create contact → Create sales order → Add order lines → Confirm
2. Create invoice → Add invoice lines → Validate
3. Create CRM lead → Update to opportunity → Create quotation → Confirm
4. Schedule calendar event with proper date format

### Date/Time Format:
- Calendar events: "YYYY-MM-DD HH:MM:SS"
- Meeting duration: 1 hour default
- Partner IDs: JSON array format [ID]

## Session Commands Reference:
See attached workflow files for detailed command sequences.