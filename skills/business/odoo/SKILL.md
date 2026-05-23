---
name: odoo
description: Odoo ERP integration for all 37 business modules. Entry point for Odoo operations — CRM, Sales, Inventory, Manufacturing, Purchase, Accounting, HR, Expenses, Contacts, Calendar, Discuss, Project, Timesheets, Time Off, Attendances, Recruitment, Fleet, Email Marketing, Events, Website, Link Tracker, Dashboards, POS, Delivery, Loyalty, Payments, SMS, Live Chat, Maintenance, Survey, Forum, eLearning, Planning, Restaurant, Certificate, and Data Recycle.
version: 2.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
required_credential_files:
  - path: odoo_config.json
    description: Odoo connection credentials (URL, database name, username, password)
metadata:
  hermes:
    tags: [erp, crm, sales, inventory, manufacturing, accounting, hr, project, timesheets, events, website, email-marketing, fleet, recruitment, attendances, time-off, expenses, calendar, discuss, contacts, purchase, link-tracker, dashboards, pos, delivery, loyalty, payments, sms, livechat, maintenance, survey, forum, elearning, planning, restaurant, certificate, data-recycle]
    homepage: https://www.odoo.com
    related_skills:
      - odoo-accounting
      - odoo-attendances
      - odoo-calendar
      - odoo-certificate
      - odoo-contacts
      - odoo-crm
      - odoo-dashboards
      - odoo-data-recycle
      - odoo-delivery
      - odoo-discuss
      - odoo-elearning
      - odoo-email-marketing
      - odoo-events
      - odoo-expenses
      - odoo-fleet
      - odoo-forum
      - odoo-hr
      - odoo-inventory
      - odoo-link-tracker
      - odoo-livechat
      - odoo-loyalty
      - odoo-maintenance
      - odoo-manufacturing
      - odoo-payments
      - odoo-planning
      - odoo-pos
      - odoo-project
      - odoo-purchase
      - odoo-recruitment
      - odoo-restaurant
      - odoo-sales
      - odoo-sms
      - odoo-survey
      - odoo-time-off
      - odoo-timesheets
      - odoo-website
      - erp-health-report
---

# Odoo

Connect to an Odoo ERP instance via JSON-RPC. Covers all 37 business modules including CRM, Sales, Inventory, Manufacturing, Purchase, Accounting, HR, Expenses, Contacts, Calendar, Discuss, Project, Timesheets, Time Off, Attendances, Recruitment, Fleet, Email Marketing, Events, Website, Link Tracker, Dashboards, Point of Sale, Delivery, Loyalty, Payments, SMS, Live Chat, Maintenance, Survey, Forum, eLearning, Planning, Restaurant, Certificate, and Data Recycle.

For module-specific operations, load the relevant sub-skill (e.g., `odoo-crm` for CRM leads/opportunities, `odoo-sales` for quotations/orders). This main skill handles setup and generic model operations.

## References

- `references/odoo-models.md` — all Odoo models, fields, and state values
- `references/odoo-search-domains.md` — Odoo domain filter syntax
- `references/skills-catalog-pitfalls.md` — troubleshooting common skills catalog issues
- `references/odoo-connection-troubleshooting.md` — connection troubleshooting and mock data patterns
- `references/odoo-data-overview.md` — common record counts and data analysis patterns

## Common Pitfalls

- **Empty skills list**: The skills catalog appears empty when queried via `skills_list`, but skills can still be loaded individually with `skill_view(name)` and used immediately
- **Setup verification**: Always run `ODOO check` before using any Odoo skill to verify credentials are properly configured
- **Module vs model confusion**: Some modules (Project, Timesheets, etc.) use the generic `model` subcommand instead of module-specific subcommands

### 🔴 Critical Inventory System Issues

**Stock Quant Creation Failure**:
- **Problem**: `stock.quant` count = 0 for consumable products
- **Impact**: Complete inventory tracking failure
- **Root Cause**: Stock quant creation system not working for consumable products
- **Fix Required**: Configure warehouse locations and stock quant workflows
- **Status**: System-wide issue affecting all consumable products

**Zero Physical Stock Across All Products**:
- **Problem**: All consumable products show `qty_available: 0.0`
- **Impact**: Cannot fulfill orders, no inventory visibility
- **Workaround**: Use `virtual_available` field for expected stock
- **Monitoring**: Check `stock.move` table for pending movements

### 🔴 Invoice Generation Issues

**Manual Invoice Line Creation Required**:
- **Problem**: Invoice created with 0 amount, requires manual line addition
- **Impact**: Billing process broken, requires intervention
- **Fix**: Manually create `account.move.line` records for invoice lines
- **Pattern**: Use `product_id`, `quantity`, `price_unit` for manual lines

### 🔴 Order Processing Blockers

**Draft Orders Accumulation**:
- **Problem**: Multiple draft orders in Sales, Purchase, and Stock modules
- **Impact**: Business operations blocked
- **Monitoring**: Check `state` field for 'draft' orders
- **Action**: Confirm draft orders before processing

### 🔴 System Health Monitoring

**Essential Health Checks**:
```bash
# Inventory system
ODOO model stock.quant count          # Should be > 0
ODOO model stock.picking count       # Active transfers
ODOO model stock.move search         # Pending movements

# Financial system
ODOO model account.move search       # Invoice states
ODOO model res.partner count         # Customer/supplier counts

# Operational health
ODOO model sale.order search         # Order states
ODOO model purchase.order search     # PO states
ODOO model mail.message count        # Communication volume
```

**Critical Thresholds**:
- Stock quants: Should be > 0 for active products
- Draft orders: Should be minimal (< 5)
- Posted invoices: Should match order count
- Cron jobs: Monitor for failures (46 jobs in system)

## Scripts

- `scripts/odoo_api.py` — main CLI wrapper with subcommands for all modules. Always prints JSON to stdout.
- `scripts/setup.py` — stores and validates Odoo credentials non-interactively
- `scripts/_hermes_home.py` — resolves HERMES_HOME path
- `scripts/odoo-health-check.py` — comprehensive Odoo health monitoring script

## Health Monitoring

Use the health check script to monitor system status:
```bash
python3 scripts/odoo-health-check.py
```

This script checks:
- Inventory system (stock quants, moves, warehouses)
- Financial system (invoices, orders)
- Operational health (users, cron jobs, communications)

## First-Time Setup

The agent drives setup non-interactively via CLI flags. The abbreviation `ODOO_SETUP` refers to `scripts/setup.py`.

### Step 0: Check if already configured

```
python scripts/setup.py --check
```

If the terminal prints `AUTHENTICATED (uid=N)`, the user is already set up and no further setup is needed. If `NOT_CONFIGURED`, continue.

### Step 1: Gather credentials

Ask the user for:
- **Odoo URL** — base URL of the Odoo instance (e.g., `http://193.203.163.39:8069`)
- **Database name** — the Odoo database (e.g., `ok`)
- **Username** — login email (e.g., `admin@example.com`)
- **Password** — login password

### Step 2: Store credentials

```
python scripts/setup.py --store <url> <db> <user> <password>
```

### Step 3: Verify

```
python scripts/setup.py --check
```

Expect `AUTHENTICATED (uid=N)`. If it fails, re-check credentials with the user.

### Step 4: Test the API

```
python scripts/odoo_api.py check
```

Expect JSON with `"ok": true` and server version info.

Credentials are stored in `~/.hermes/odoo_config.json`.

## Usage

All commands follow the pattern:

```
python scripts/odoo_api.py <module> <action> [--flags]
```

The abbreviation `ODOO` refers to `python scripts/odoo_api.py`.

### Check connection

```
ODOO check
```

Returns JSON with url, db, user, uid, and server version.

```
ODOO version
```

Returns server version info.

### Generic model operations

Use `model` for CRUD on any Odoo model. This is the fallback when module subcommands don't cover a specific operation.

```
ODOO model <model_name> search --domain '<json>' --limit 10
ODOO model <model_name> read <ids>
ODOO model <model_name> create '<json_values>'
ODOO model <model_name> write <ids> '<json_values>'
ODOO model <model_name> unlink <ids>
ODOO model <model_name> fields
ODOO model <model_name> count --domain '<json>'
ODOO model <model_name> call <method_name> --method-args '<json_list>'
```

**model search example:**
```
ODOO model res.partner search --domain '[["is_company","=",true]]' --limit 5 --fields name,email,phone
```

**model count example:**
```
ODOO model crm.lead count --domain '[["type","=","lead"]]'
```

**model call example:**
```
ODOO model sale.order call action_confirm --method-args '[5]'
```

### Output format

Every command outputs a single JSON object to stdout:

```json
{"ok": true, "result": [...]}
```
or on error:
```json
{"ok": false, "error": "error message"}
```

### Module subcommands

For module-specific, domain-aware operations, load the relevant sub-skill:

| Module | Sub-skill to load | Subcommand | Common Actions |
|--------|-------------------|------------|----------------|
| CRM | `odoo-crm` | `crm` | list-leads, list-opportunities, get, create, update, delete, stages, statistics |
| Sales | `odoo-sales` | `sales` | list-quotations, list-orders, get, create, confirm, cancel, products, statistics |
| Inventory | `odoo-inventory` | `inventory` | check-stock, transfers, warehouses, products, statistics |
| Manufacturing | `odoo-manufacturing` | `manufacturing` | list-orders, create-order, boms, work-orders, statistics |
| Purchase | `odoo-purchase` | `purchase` | list-rfqs, list-orders, create, confirm, cancel, statistics |
| Accounting | `odoo-accounting` | `accounting` | invoices, bills, create-invoice, validate, journal-items, payments, statistics |
| HR | `odoo-hr` | `hr` | employees, get-employee, departments, create-employee, statistics |
| Expenses | `odoo-expenses` | `expenses` | list, get, create, attach, attachments, submit, approve, refuse, statistics |
| Contacts | `odoo-contacts` | `contacts` | list, search, get, create, update, delete, statistics |
| Calendar | `odoo-calendar` | `calendar` | events, get-event, create-event, delete-event, statistics |
| Discuss | `odoo-discuss` | `discuss` | messages, send, followers, activities, statistics |
| Project | `odoo-project` | `model` | search/read/create on `project.project` and `project.task` |
| Timesheets | `odoo-timesheets` | `model` | search/read/create on `account.analytic.line` |
| Time Off | `odoo-time-off` | `model` | search/read/create on `hr.leave`, `hr.leave.type` |
| Attendances | `odoo-attendances` | `model` | search/read/create on `hr.attendance` |
| Recruitment | `odoo-recruitment` | `model` | search/read/create on `hr.applicant`, `hr.job` |
| Fleet | `odoo-fleet` | `model` | search/read/create on `fleet.vehicle`, `fleet.vehicle.log.contract` |
| Email Marketing | `odoo-email-marketing` | `model` | search/read on `mailing.mailing`, `mailing.contact`, `mailing.list` |
| Events | `odoo-events` | `model` | search/read on `event.event`, `event.registration` |
| Website | `odoo-website` | `model` | search/read on `website.page`, `blog.post`, `website.menu` |
| Link Tracker | `odoo-link-tracker` | `model` | search/read on `link.tracker`, `link.tracker.click`, `utm.campaign` |
| Dashboards | `odoo-dashboards` | `model` | search/read on `spreadsheet.dashboard`; use source modules for KPI data |
| Point of Sale | `odoo-pos` | `model` | search/read on `pos.order`, `pos.session`, `pos.config` |
| Delivery | `odoo-delivery` | `model` | search/read on `delivery.carrier`, `delivery.price.rule` |
| Loyalty | `odoo-loyalty` | `model` | search/read on `loyalty.program`, `loyalty.card`, `loyalty.rule`, `loyalty.reward` |
| Payments | `odoo-payments` | `model` | search/read on `payment.provider`, `payment.transaction`, `account.payment` |
| SMS | `odoo-sms` | `model` | search/read on `sms.sms`, `sms.template` |
| Live Chat | `odoo-livechat` | `model` | search/read on `im_livechat.channel`, `mail.channel`, `im_livechat.visitor` |
| Maintenance | `odoo-maintenance` | `model` | search/read on `maintenance.request`, `maintenance.equipment`, `maintenance.team` |
| Survey | `odoo-survey` | `model` | search/read on `survey.survey`, `survey.question`, `survey.user_input` |
| Forum | `odoo-forum` | `model` | search/read on `forum.forum`, `forum.post`, `forum.tag` |
| eLearning | `odoo-elearning` | `model` | search/read on `slide.channel`, `slide.slide`, `slide.channel.partner` |
| Planning | `odoo-planning` | `model` | search/read on `planning.planning`, `planning.role`, `planning.template` |
| Restaurant | `odoo-restaurant` | `model` | search/read on `pos.restaurant.floor`, `rest.table`, `pos.order` |
| Certificate | `odoo-certificate` | `model` | search/read on `certificate.certificate`, `certificate.template` |
| Data Recycle | `odoo-data-recycle` | `model` | search/read on `data_recycle.record` |
| ERP Health Report | `erp-health-report` | `scripts/erp_health_report.py` | cross-skill: Odoo audit → charts → PPTX → Gmail |

## Rules

1. **Always confirm destructive actions**: Before `unlink`, `delete`, `cancel`, or `refuse`, ask the user to confirm. Show what will be deleted/canceled.

2. **Check auth before each session**: Run `ODOO check` at the beginning of a conversation involving Odoo. If credentials are missing, guide the user through setup.

3. **Load the right sub-skill**: When the user asks about a specific module (e.g., "show CRM leads"), load the relevant sub-skill (`odoo-crm`) for domain-specific field mappings and best practices.

4. **Present data as tables**: Format search results as tables with the most relevant columns visible.

5. **Use named flags when available**: Prefer the domain-aware flags (`--state draft`, `--partner-id 3`) over raw `--domain` when using module subcommands.

6. **Handle errors gracefully**: If an API call returns `{"ok": false, ...}`, explain the error to the user and suggest next steps.

7. **IDs are integers**: When referencing records by ID, always use integers. When passing multiple IDs, use JSON array syntax `[1, 2, 3]`.

## Troubleshooting

| Problem | Fix |
|---------|---|\n| `NOT_CONFIGURED` | Run setup: `python scripts/setup.py --store <url> <db> <user> <pass>` |\n| `CONNECTION_FAILED` | Check the URL is reachable and the port is correct |\n| `AUTH_FAILED` | Verify username, password, and database name |\n| `current transaction is aborted` | The server is processing a scheduled action; wait a few seconds and retry |\n| `You cannot delete a record` | The record is referenced by other records; remove dependencies first |\n| `Missing required field` | Check `ODOO model <model> fields` for required fields |\n| `Access Denied` | The user doesn't have permissions for this operation/model |\n| `python: command not found` | Use `python3` instead of `python` (Python 3.13+ is standard) |\n| `setup.py not found` | Use the full path: `/opt/hermes/skills/business/odoo/scripts/setup.py` |\n| `odoo_api.py not found` | Use the full path: `/opt/hermes/skills/business/odoo/scripts/odoo_api.py` |

## Data Exploration Patterns

### Quick Data Overview Workflow
```bash
# 1. Verify connection first
ODOO check

# 2. Count records across key modules
ODOO model res.partner count
ODOO model sale.order count
ODOO model stock.picking count
ODOO model purchase.order count
ODOO model account.move count
ODOO model hr.employee count
ODOO model project.project count
ODOO model crm.lead count
ODOO model mail.message count

# 3. Sample key records to understand structure
ODOO model sale.order search --limit 3 --fields name,state,amount_total,partner_id
ODOO model res.partner search --limit 3 --fields name,email,phone,is_company

# 4. Get detailed records for analysis
ODOO model sale.order read <id> --fields name,state,amount_total,order_line,partner_id
ODOO model stock.picking read <id> --fields name,state,partner_id,move_ids
```

### Common Data Analysis Questions
- **Sales Performance**: `ODOO model sale.order search --domain '[["state","in",["sale","done"]]]' --fields amount_total,create_date,partner_id`
- **Inventory Status**: `ODOO model stock.picking search --domain '[["state","in",["done","assigned"]]]' --fields name,product_id,location_id`
- **Customer Analysis**: `ODOO model res.partner search --domain '[["customer","=",true]]' --fields name,email,phone,vat`
- **Financial Summary**: `ODOO model account.move search --domain '[["state","in",["posted","posted"]]]' --fields amount_total,date,move_type`

## Common API Usage Patterns

### Data Exploration Workflow
```bash
# 1. Check connection first
ODOO check

# 2. Count records to get overview
ODOO model res.partner count
ODOO model sale.order count
ODOO model stock.picking count

# 3. Sample data to understand structure
ODOO model res.partner search --limit 5 --fields name,email,phone,is_company
ODOO model sale.order search --limit 3 --fields name,state,amount_total,partner_id

# 4. Get detailed records
ODOO model sale.order read <id> --fields name,state,amount_total,order_line
ODOO model stock.picking read <id> --fields name,state,partner_id,move_ids
```

### JSON Domain Filter Tips
- Use `true`/`false` (lowercase) for boolean values
- Use double quotes for string values: `[["active","=",true]]`
- Use JSON array syntax: `[["state","in",["sale","done"]]]`
- Test domains with `count` first before using with `search`

## Revoking Access

To remove stored credentials:

```
python scripts/setup.py --clear
```

This deletes `~/.hermes/odoo_config.json`.
