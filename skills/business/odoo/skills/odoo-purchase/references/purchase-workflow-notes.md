# Purchase Order Workflow Notes

## Ramesh Suppliers Maida Purchase (2026-05-23)

### Workflow Steps:
1. **Create supplier contact**: Ramesh Suppliers (ID: 24)
   - Created with `contacts create --is-company true`
   - Updated with `supplier_rank: 1`

2. **Create product**: Maida (ID: 33)
   - Product type: consu (consumable)
   - Default code: MAIDA-001
   - Unit price: ₹40/kg

3. **Create purchase order**: P00014
   - Partner: Ramesh Suppliers (ID: 24)
   - Product: Maida - 200 kg
   - Total: ₹8,000

4. **Order line creation**:
   - Initial `create --order-lines` failed with "unhashable type"
   - Fixed by creating PO first, then adding lines via model

5. **Confirm PO**: Created incoming transfer WH/IN/00007
   - Transfer processed but stock quants not auto-created for consumables

### Key Learnings:
- **Order line syntax**: Complex order lines may require separate creation after PO creation
- **Supplier setup**: Contacts must have `supplier_rank > 0` for purchase orders
- **Product creation**: Always verify product exists before creating PO lines
- **Stock behavior**: Virtual stock appears immediately, physical stock requires manual processing for consumables