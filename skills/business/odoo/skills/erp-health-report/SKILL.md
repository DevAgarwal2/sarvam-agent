---
name: erp-health-report
description: "Cross-skill workflow: Odoo ERP health audit, infographic summary, PPTX report, and email delivery via Gmail."
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
required_credential_files:
  - path: odoo_config.json
    description: Odoo connection credentials
  - path: google_token.json
    description: Google OAuth2 token (for Gmail)
metadata:
  hermes:
    tags: [erp, health-report, odoo, gmail, infographic, pptx, workflow]
    homepage: https://www.odoo.com
    related_skills: [odoo, baoyu-infographic, google-workspace, nano-pdf]
---

# ERP Health Report

Generates a comprehensive ERP health report by querying all Odoo modules, visualizing key metrics as charts and an infographic, compiling a PPTX report, and emailing it via Gmail.

## Workflow

1. **Query Odoo** — fetch counts/stats from CRM, Sales, Inventory, Manufacturing, Purchase, Accounting, HR, Expenses, Contacts (9 modules)
2. **Generate charts** — matplotlib bar charts for each module
3. **Generate infographic** — creates a structured-content prompt for baoyu-infographic image generation
4. **Compile PPTX** — report with cover slide, module summary tables, embedded charts, and KPI highlights
5. **Email via Gmail** — send the PPTX report and infographic PNG to specified recipients

## Dependencies

```bash
uv pip install python-pptx matplotlib Pillow
```

## Scripts

- `scripts/erp_health_report.py` — full orchestrator: `uv run python3 scripts/erp_health_report.py [--email recipient@example.com]`

## Quick Start

```bash
# Full run: query Odoo, generate charts, compile PPTX, email
uv run python3 scripts/erp_health_report.py --email admin@company.com

# Skip email, just generate report files
uv run python3 scripts/erp_health_report.py --skip-email

# Quiet mode (JSON output only)
uv run python3 scripts/erp_health_report.py --json

# Custom output directory
uv run python3 scripts/erp_health_report.py --output-dir ./my-reports --skip-email
```

## Output

```
report/erp-health-report-YYYYMMDD-HHMMSS/
├── data.json                  # Raw Odoo query results
├── charts/                    # matplotlib PNG charts
│   ├── crm.png
│   ├── sales.png
│   ├── inventory.png
│   ├── manufacturing.png
│   ├── purchase.png
│   ├── accounting.png
│   ├── hr.png
│   ├── expenses.png
│   └── contacts.png
├── infographic-prompt.md      # Prompt for baoyu-infographic image gen
├── ERP_Health_Report.pptx     # Full compiled report
└── summary.json               # Final summary with file paths
```

## Cross-Skill Chaining

After this skill generates the report, you can chain other skills:

```bash
# 1. Generate infographic from the prompt
# Load baoyu-infographic skill, use infographic-prompt.md as source

# 2. Convert PPTX to PDF for broader distribution
# Load nano-pdf skill

# 3. Upload to Google Drive
# Load google-workspace skill, use drive upload
```

## Rules

1. Always confirm before sending email — show recipients and attachment list
2. Odoo credentials must be configured first (`odoo setup --store`)
3. Google OAuth must be authenticated (run `google-workspace/setup.py --check`)
4. A running Odoo instance is required
