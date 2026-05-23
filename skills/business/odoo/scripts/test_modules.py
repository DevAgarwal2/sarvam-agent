#!/usr/bin/env python3
"""Final verification test for all Odoo modules."""
import json, subprocess, sys
from pathlib import Path

BASE = Path(__file__).parent
PY = sys.executable
SC = [PY, str(BASE / "odoo_api.py")]
M = SC + ["model"]

def run(cmd, label, expect_ok=True):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(r.stdout) if r.stdout.strip() else {}
        ok = data.get("ok", False)
        result = data.get("result")
        status = "✓" if ok else "✗"
        print(f"  {status} {label}")
        if not ok and expect_ok:
            print(f"    Error: {data.get('error', 'unknown')}")
        return ok, result
    except Exception as e:
        print(f"  ✗ {label}: {e}")
        return False, None

tests = [
    ("Base", [
        (SC + ["check"], "connection check"),
    ]),
    ("Contacts", [
        (M + ["res.partner", "create", '{"name":"Test Contact","email":"test@hermes.dev","country_id":101}'], "create partner"),
        (M + ["res.partner", "read", "2"], "read partner"),
        (M + ["res.partner", "search", "--limit", "3"], "list partners"),
    ]),
    ("CRM", [
        (M + ["crm.lead", "create", '{"name":"Test Lead","expected_revenue":50000,"type":"opportunity"}'], "create lead"),
        (M + ["crm.lead", "search", "--limit", "3"], "list leads"),
    ]),
    ("Sales", [
        (M + ["sale.order", "create", '{"partner_id":1}'], "create quotation"),
        (M + ["sale.order", "search", "--limit", "3"], "list orders"),
    ]),
    ("Purchase", [
        (M + ["purchase.order", "create", '{"partner_id":1}'], "create RFQ"),
        (M + ["purchase.order", "search", "--limit", "3"], "list POs"),
    ]),
    ("Inventory", [
        (M + ["stock.quant", "search", "--limit", "3"], "list stock quants"),
        (M + ["stock.warehouse", "search", "--limit", "3"], "list warehouses"),
        (M + ["stock.picking", "search", "--limit", "3"], "list transfers"),
    ]),
    ("Accounting", [
        (M + ["account.move", "create", '{"move_type":"out_invoice","partner_id":1,"invoice_date":"2026-05-18"}'], "create invoice"),
        (M + ["account.move", "search", "--limit", "3"], "list moves"),
    ]),
    ("HR", [
        (M + ["hr.employee", "create", '{"name":"Test Employee","work_email":"emp@hermes.dev"}'], "create employee"),
        (M + ["hr.employee", "search", "--limit", "3"], "list employees"),
    ]),
    ("Calendar", [
        (M + ["calendar.event", "create", '{"name":"Test Event","start":"2026-05-20 09:00:00","stop":"2026-05-20 10:00:00"}'], "create event"),
        (M + ["calendar.event", "search", "--limit", "3"], "list events"),
    ]),
    ("Project", [
        (M + ["project.project", "create", '{"name":"Test Project"}'], "create project"),
        (M + ["project.task", "create", '{"name":"Test Task","project_id":1}'], "create task"),
    ]),
    ("Manufacturing", [
        (M + ["mrp.bom", "create", '{"product_tmpl_id":1,"product_qty":1.0}'], "create BOM"),
        (M + ["mrp.production", "create", '{"product_id":1,"product_qty":5,"bom_id":1}'], "create MO"),
    ]),
    ("Point of Sale", [
        (M + ["pos.config", "search", "--limit", "3"], "list POS configs"),
        (M + ["pos.order", "search", "--limit", "3"], "list POS orders"),
    ]),
    ("Delivery", [
        (M + ["delivery.carrier", "search", "--limit", "3"], "list carriers"),
    ]),
    ("Loyalty", [
        (M + ["loyalty.program", "search", "--limit", "3"], "list programs"),
    ]),
    ("Payments", [
        (M + ["payment.provider", "search", "--limit", "3"], "list providers"),
    ]),
    ("SMS", [
        (M + ["sms.sms", "search", "--limit", "3"], "list SMS"),
    ]),
    ("Live Chat", [
        (M + ["im_livechat.channel", "search", "--limit", "3"], "list channels"),
    ]),
    ("Maintenance", [
        (M + ["maintenance.equipment", "create", '{"name":"Test Equipment"}'], "create equipment"),
        (M + ["maintenance.request", "create", '{"name":"Test Request","equipment_id":1}'], "create request"),
    ]),
    ("Survey", [
        (M + ["survey.survey", "create", '{"title":"Test Survey"}'], "create survey"),
        (M + ["survey.question", "create", '{"title":"Q1?","survey_id":1,"question_type":"simple_choice"}'], "create question"),
    ]),
    ("eLearning", [
        (M + ["slide.channel", "create", '{"name":"Test Course","visibility":"public"}'], "create course"),
        (M + ["slide.slide", "create", '{"name":"Lesson 1","channel_id":1,"slide_type":"article"}'], "create slide"),
    ]),
    ("Forum", [
        (M + ["forum.forum", "create", '{"name":"Test Forum","description":"Test"}'], "create forum"),
        (M + ["forum.post", "create", '{"name":"Hello","forum_id":1,"content":"Test"}'], "create post"),
    ]),
    ("Restaurant", [
        (M + ["restaurant.floor", "create", '{"name":"Main Hall"}'], "create floor"),
        (M + ["restaurant.table", "create", '{"table_number":1,"shape":"square","floor_id":1,"seats":4}'], "create table"),
    ]),
    ("Certificate", [
        (M + ["certificate.certificate", "create", '{"name":"Test Cert","company_id":1}'], "create certificate"),
    ]),
    ("Data Recycle", [
        (M + ["data_recycle.record", "search", "--limit", "3"], "list recycled records"),
    ]),
    ("Social Media", [
        (M + ["social.post", "search", "--limit", "3"], "list posts"),
    ]),
]

passed = 0
failed = 0
for group_name, cmds in tests:
    print(f"\n{group_name}")
    for cmd, label in cmds:
        ok, _ = run(cmd, label)
        if ok: passed += 1
        else: failed += 1

total = passed + failed
print(f"\n{'='*40}")
print(f"Results: {passed}/{total} passed ({failed} failed)")
if failed == 0:
    print("✓ All modules verified!")
else:
    print(f"✗ {failed} tests failed - check errors above")
