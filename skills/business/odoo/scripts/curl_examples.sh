#!/bin/bash
# Odoo JSON-RPC curl examples for all modules
# Replace URL, DB, USER, PASS with your values

URL="http://YOUR_ODOO_URL"
DB="YOUR_DB"
USER="YOUR_USER"
PASS="YOUR_PASS"

# ─── Authenticate ───
UID=$(curl -s -X POST "$URL/jsonrpc" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"common\",\"method\":\"authenticate\",\"args\":[\"$DB\",\"$USER\",\"$PASS\",{}]},\"id\":1}" | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")
echo "UID: $UID"

# ─── Generic model function ───
odoo_call() {
  curl -s -X POST "$URL/jsonrpc" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$DB\",$UID,\"$PASS\",$1,$2,$3,$4]},\"id\":$(date +%s)}"
}

echo "=== CRM - List Leads ==="
odoo_call "crm.lead" "search_read" "[[\"type\",\"=\",\"lead\"]]" "{\"limit\":5,\"fields\":[\"name\",\"email_from\",\"stage_id\",\"user_id\"]}"

echo "=== Sales - List Quotations ==="
odoo_call "sale.order" "search_read" "[[\"state\",\"=\",\"draft\"]]" "{\"limit\":5,\"fields\":[\"name\",\"partner_id\",\"amount_total\",\"state\"]}"

echo "=== Inventory - Stock Check ==="
odoo_call "stock.quant" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"product_id\",\"location_id\",\"quantity\"]}"

echo "=== Manufacturing - List MOs ==="
odoo_call "mrp.production" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"product_id\",\"state\",\"date_start\"]}"

echo "=== Purchase - List RfQs ==="
odoo_call "purchase.order" "search_read" "[[\"state\",\"=\",\"draft\"]]" "{\"limit\":5,\"fields\":[\"name\",\"partner_id\",\"amount_total\"]}"

echo "=== Accounting - Invoices ==="
odoo_call "account.move" "search_read" "[[\"move_type\",\"=\",\"out_invoice\"]]" "{\"limit\":5,\"fields\":[\"name\",\"partner_id\",\"amount_total\",\"state\"]}"

echo "=== HR - Employees ==="
odoo_call "hr.employee" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"department_id\",\"work_email\"]}"

echo "=== Expenses - List ==="
odoo_call "hr.expense" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"employee_id\",\"total_amount\",\"state\"]}"

echo "=== Contacts - List ==="
odoo_call "res.partner" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"email\",\"phone\",\"is_company\"]}"

echo "=== Calendar - Events ==="
odoo_call "calendar.event" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"start\",\"stop\",\"location\"]}"

echo "=== Discuss - Messages ==="
odoo_call "mail.message" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"subject\",\"body\",\"author_id\",\"date\"]}"

echo "=== Project - List ==="
odoo_call "project.project" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"partner_id\",\"date_start\",\"state\"]}"

echo "=== Timesheets - Entries ==="
odoo_call "account.analytic.line" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"project_id\",\"task_id\",\"unit_amount\",\"date\"]}"

echo "=== Time Off - Leaves ==="
odoo_call "hr.leave" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"employee_id\",\"date_from\",\"date_to\",\"state\"]}"

echo "=== Attendances - Records ==="
odoo_call "hr.attendance" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"employee_id\",\"check_in\",\"check_out\",\"worked_hours\"]}"

echo "=== Recruitment - Applicants ==="
odoo_call "hr.applicant" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"partner_name\",\"job_id\",\"stage_id\",\"email_from\"]}"

echo "=== Fleet - Vehicles ==="
odoo_call "fleet.vehicle" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"driver_id\",\"license_plate\",\"state\"]}"

echo "=== Email Marketing - Mailings ==="
odoo_call "mailing.mailing" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"subject\",\"state\",\"sent_date\",\"total\"]}"

echo "=== Events - List ==="
odoo_call "event.event" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"date_begin\",\"date_end\",\"seats_available\"]}"

echo "=== Website - Pages ==="
odoo_call "website.page" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"url\",\"is_published\"]}"

echo "=== Link Tracker - Links ==="
odoo_call "link.tracker" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"title\",\"url\",\"short_url\",\"count\"]}"

echo "=== Dashboards - List ==="
odoo_call "spreadsheet.dashboard" "search_read" "[[]]" "{\"limit\":5,\"fields\":[\"name\",\"dashboard_group_id\"]}"
