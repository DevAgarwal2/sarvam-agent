# Odoo Module Models Reference

## Core Business Models

### Sales & CRM
- `res.partner` - Customer/Supplier information
- `sale.order` - Sales orders and quotations
- `sale.order.line` - Order line items
- `crm.lead` - CRM leads and opportunities
- `crm.stage` - Pipeline stages

### Purchase & Inventory
- `purchase.order` - Purchase orders
- `purchase.order.line` - Purchase order lines
- `stock.picking` - Stock transfers
- `stock.location` - Warehouse locations
- `product.product` - Product catalog
- `product.template` - Product templates

### Accounting & Finance
- `account.move` - Invoices and credit notes
- `account.journal` - Accounting journals
- `account.account` - Chart of accounts
- `account.payment` - Payments

### Manufacturing & Production
- `mrp.production` - Production orders
- `mrp.bom` - Bills of materials
- `mrp.workcenter` - Work centers

### HR & People
- `hr.employee` - Employee records
- `hr.department` - Departments
- `hr.leave` - Leave requests
- `hr.attendance` - Check-in/check-out records

### Project & Task Management
- `project.project` - Projects
- `project.task` - Tasks
- `account.analytic.line` - Timesheets

### Website & Marketing
- `website.page` - Web pages
- `blog.post` - Blog posts
- `mailing.mailing` - Email campaigns

## Common Field Patterns

### State Fields
- `active` - Record active flag
- `state` - Workflow state (draft, confirmed, done, cancel)
- `kanban_state` - Kanban board state

### Partner Fields
- `partner_id` - Related partner/customer
- `customer` / `supplier` - Boolean flags
- `email` / `phone` - Contact information

### Date Fields
- `date` - Generic date field
- `create_date` / `write_date` - Timestamps
- `deadline` - Due date

### Selection Fields
- `type` - Record type (lead, opportunity, etc.)
- `priority` - Priority level
- `company_id` - Associated company

## Common Search Domains

### Partner Search
```python
[('is_company', '=', True)]
[('customer', '=', True)]
[('email', 'ilike', 'search_term')]
```

### Sales Orders
```python
[('state', 'in', ['draft', 'sent'])]
[('amount_total', '>', 1000)]
[('date_order', '>=', '2024-01-01')]
```

### Date Filtering
```python
[('create_date', '>=', '2024-01-01')]
[('date', '<=', '2024-12-31')]
```

### State Filtering
```python
[('state', '=', 'done')]
[('state', '!=', 'cancel')]
```

## Model-Specific Patterns

### Sale Orders
- Use `sale` module commands for domain-specific operations
- Common states: draft, sent, confirmed, done, cancel
- Key fields: amount_total, date_order, partner_id

### Purchase Orders
- Use `purchase` module commands
- Common states: draft, sent, confirmed, done, cancel
- Key fields: amount_total, date_order, partner_id

### CRM Leads
- Use `crm` module commands
- Common states: lead, opportunity
- Key fields: type, priority, stage_id

### Inventory
- Use `inventory` module commands
- Common operations: check-stock, transfers, warehouses
- Key fields: location_id, product_id, quantity

### Accounting
- Use `accounting` module commands
- Common operations: invoices, bills, journal entries
- Key fields: state, amount_total, date

### Manufacturing
- Use `manufacturing` module commands
- Common operations: production orders, BOMs, work orders
- Key fields: state, product_id, workcenter_id

### HR
- Use `hr` module commands
- Common operations: employees, departments, leave
- Key fields: active, department_id, job_id

### Project
- Use `project` module commands or `model` subcommand
- Common operations: projects, tasks, time tracking
- Key fields: state, progress, user_id

### Website
- Use `website` module commands or `model` subcommand
- Common operations: pages, blog posts, menus
- Key fields: website_published, website_published_date

## Error Handling

### Common Error Messages
- `"You cannot unlink a record that is referenced by other records"`
- `"Missing required field: <field_name>"`
- `"Invalid credentials (Failure)"`
- `"current transaction is aborted"`

### Troubleshooting Steps
1. Check if record exists with `ODOO model <model> search`
2. Verify required fields with `ODOO model <model> fields`
3. Check record dependencies before deletion
4. Verify user permissions for the operation
5. Wait for server processing to complete if needed

## Performance Tips

- Use specific field selection: `--fields name,email,phone`
- Limit result sets: `--limit 10`
- Use domain filtering instead of post-processing
- Batch operations when possible
- Avoid large data exports in single queries

## Version Compatibility

This reference assumes Odoo 15+. Some field names or model structures may vary in different versions. Always verify with `ODOO model <model> fields` for your specific version.