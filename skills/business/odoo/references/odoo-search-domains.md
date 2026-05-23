# Odoo Domain Filter Syntax

## Basic Domain Structure

Domains are lists of tuples in Python format:
```python
[('field', 'operator', 'value')]
```

Multiple conditions are combined with AND by default:
```python
[('state', '=', 'done'), ('amount_total', '>', 1000)]
```

OR conditions use the `|` operator:
```python
[('state', '=', 'done') | ('state', '=', 'cancel')]
```

## Common Operators

### Comparison Operators
- `=` - Equal
- `!=` - Not equal
- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal

### String Operators
- `ilike` - Case insensitive contains (most common)
- `like` - Case sensitive contains
- `not ilike` - Case insensitive not contains
- `in` - In list
- `not in` - Not in list

### Date Operators
- `>` - After date
- `>=` - On or after date
- `<` - Before date
- `<=` - On or before date
- `=` - Exact date match

### Boolean Operators
- `True` - True value
- `False` - False value

## Field-Specific Domains

### Partner/Customer Domains
```python
# Active customers
[('customer', '=', True), ('active', '=', True)]

# Customers with email
[('email', 'ilike', '@example.com')]

# Companies only
[('is_company', '=', True)]

# Specific partner
[('partner_id', '=', 123)]
```

### Sales Order Domains
```python
# Draft or sent orders
[('state', 'in', ['draft', 'sent'])]

# Recent orders (last 30 days)
[('date_order', '>=', datetime.datetime.now() - datetime.timedelta(days=30))]

# High value orders
[('amount_total', '>', 1000)]

# Orders for specific customer
[('partner_id', '=', 123)]

# Orders in date range
[('date_order', '>=', '2024-01-01'), ('date_order', '<=', '2024-12-31')]
```

### Purchase Order Domains
```python
# Draft or sent purchase orders
[('state', 'in', ['draft', 'sent'])]

# Orders from specific supplier
[('partner_id', '=', 456)]

# Orders above threshold
[('amount_total', '>', 5000)]
```

### CRM Domains
```python
# Leads only
[('type', '=', 'lead')]

# Opportunities only
[('type', '=', 'opportunity')]

# High priority leads
[('priority', 'in', ['high', 'medium'])]

# Recent leads (last 7 days)
[('create_date', '>=', datetime.datetime.now() - datetime.timedelta(days=7))]
```

### Inventory Domains
```python
# Low stock products
[('qty_available', '<', 10)]

# Products in specific location
[('location_id', '=', 123)]

# Active products
[('active', '=', True)]
```

### Accounting Domains
```python
# Invoices only
[('move_type', '=', 'entry')]

# Posted invoices
[('state', '=', 'posted')]

# Invoices for specific partner
[('partner_id', '=', 123)]

# Invoices in date range
[('invoice_date', '>=', '2024-01-01'), ('invoice_date', '<=', '2024-12-31')]
```

### HR Domains
```python
# Active employees
[('active', '=', True)]

# Employees in specific department
[('department_id', '=', 456)]

# Employees with specific job
[('job_id', '=', 789)]
```

### Project Domains
```python
# Active projects
[('active', '=', True)]

# Projects with tasks
[('task_count', '>', 0)]

# Tasks in specific project
[('project_id', '=', 123)]
```

### Website Domains
```python
# Published pages
[('website_published', '=', True)]

# Pages for specific website
[('website_id', '=', 123)]

# Blog posts only
[('model', '=', 'blog.post')]
```

## Complex Domain Examples

### Multi-Condition Sales Query
```python
# High value orders from active customers in Q1 2024
[
    ('state', '=', 'done'),
    ('amount_total', '>', 1000),
    ('partner_id.active', '=', True),
    ('date_order', '>=', '2024-01-01'),
    ('date_order', '<=', '2024-03-31')
]
```

### OR Conditions
```python
# Orders that are either done or cancelled
[('state', '=', 'done') | ('state', '=', 'cancel')]

# Customers with email OR phone
[('email', 'ilike', '@'), '|', ('phone', '!=', False)]
```

### Nested OR with Parentheses
```python
# Complex OR/AND combinations
[
    ('state', '=', 'done'),
    '|',
    [
        ('state', '=', 'sent'),
        ('state', '=', 'confirmed')
    ]
]
```

## Domain Helper Functions

### Date Calculations
```python
import datetime

# Last 30 days
[('create_date', '>=', datetime.datetime.now() - datetime.timedelta(days=30))]

# Current month
[('date', '>=', datetime.datetime.now().replace(day=1))]

# Current year
[('date', '>=', datetime.datetime.now().replace(month=1, day=1))]
```

### List Filtering
```python
# Multiple values
[('state', 'in', ['draft', 'sent', 'confirmed'])]

# Exclusion
[('state', 'not in', ['cancel', 'lost')]
```

## Performance Considerations

1. **Use specific fields**: Always specify `--fields` to limit returned data
2. **Apply domains early**: Filter at database level, not in Python
3. **Index frequently used fields**: Ensure database indexes on commonly filtered fields
4. **Avoid complex OR chains**: Break into multiple queries when possible
5. **Use range queries**: Instead of multiple OR conditions for date ranges

## Common Mistakes to Avoid

1. **Wrong field names**: Always verify field names with `ODOO model <model> fields`
2. **Case sensitivity**: String operators are case-insensitive by default (`ilike`)
3. **Date format**: Use ISO format YYYY-MM-DD for dates
4. **Boolean values**: Use True/False, not 1/0 for boolean fields
5. **List syntax**: Lists must be in Python format: `['value1', 'value2']`
6. **String quoting**: Domain strings need proper quoting in shell commands

## Debugging Domains

### Test Domain Syntax
```bash
ODOO model res.partner search --domain '[(\"is_company\", \"=\", True)]' --limit 5
```

### Check Available Fields
```bash
ODOO model res.partner fields
```

### Validate Domain Logic
Use `--debug` flag for detailed error messages:
```bash
ODOO model res.partner search --domain '[(\"invalid_field\", \"=\", \"test\")]' --debug
```