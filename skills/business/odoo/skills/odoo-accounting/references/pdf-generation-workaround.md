# PDF Invoice Generation Workaround

## Problem
Direct PDF generation methods like `action_get_invoice_pdf` and `action_document` are not available in the Odoo API.

## Solution
Use the portal URL method:

1. Get portal URL:
```bash
ODOO model account.move call get_portal_url --method-args '[11]'
```

2. Access URL: `http://host.docker.internal:8069/my/invoices/11?access_token=TOKEN`

3. Click "Download" button in portal interface to get PDF

## Portal URL Format
`/my/invoices/{invoice_id}?access_token={generated_token}`

## Alternative Methods
- Manual download from Odoo portal
- Use `action_send_and_print` to open send wizard
- Direct portal access for users with proper permissions