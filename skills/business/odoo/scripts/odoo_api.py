#!/usr/bin/env python3
"""
Odoo API CLI for Hermes skills.
Provides module-specific subcommands covering CRM, Sales, Inventory,
Manufacturing, Purchase, Accounting, HR, Expenses, Contacts, Calendar,
and Discuss. All output is JSON to stdout.

Usage:
    python odoo_api.py check
    python odoo_api.py version
    python odoo_api.py model <name> search '<domain>' --limit 10
    python odoo_api.py crm list-leads --limit 10
    python odoo_api.py sales list-quotations --state draft
    python odoo_api.py inventory check-stock --product-id 5
    python odoo_api.py contacts list --limit 20
"""
import argparse
import http.cookiejar
import json
import os
import sys
import urllib.request
from _hermes_home import get_hermes_home

CONFIG_FILE = "odoo_config.json"


def _load_config():
    cp = get_hermes_home() / CONFIG_FILE
    if not cp.exists():
        print(json.dumps({"ok": False, "error": f"No config found at {cp}. Run: python setup.py --store <url> <db> <user> <pass>"}))
        sys.exit(1)
    return json.loads(cp.read_text())


def _print_json(data):
    print(json.dumps(data, default=str, ensure_ascii=False))


def _jsonrpc(config, service, method, *args):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {"service": service, "method": method, "args": args},
        "id": 1,
    }
    try:
        req = urllib.request.Request(
            f"{config['url']}/jsonrpc",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read())
        if data.get("error"):
            err = data["error"]
            msg = err.get("data", {}).get("message", str(err)) if isinstance(err, dict) else str(err)
            return {"ok": False, "error": msg}
        return {"ok": True, "result": data["result"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _authenticate(config):
    result = _jsonrpc(config, "common", "authenticate",
                      config["db"], config["user"], config["password"], {})
    if not result["ok"]:
        _print_json(result)
        sys.exit(1)
    return config["db"], result["result"], config["password"]


def _session(config):
    """Authenticate and return (uid, cookie-enabled opener)."""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    db, uid, pw = _authenticate(config)
    payload = json.dumps({
        "jsonrpc": "2.0", "method": "call",
        "params": {"service": "common", "method": "authenticate",
                    "args": [db, config["user"], pw, {}]},
        "id": 1,
    })
    req = urllib.request.Request(
        f"{config['url']}/jsonrpc",
        data=payload.encode(),
        headers={"Content-Type": "application/json"},
    )
    opener.open(req, timeout=10)
    return uid, opener


def _download_invoice_pdf(config, invoice_id, output_path=None):
    """Download invoice PDF using session cookie. Returns path to PDF."""
    uid, opener = _session(config)
    pdf_url = f"{config['url']}/report/pdf/account.report_invoice/{invoice_id}"
    resp = opener.open(pdf_url, timeout=15)
    pdf_data = resp.read()
    if not output_path:
        output_path = f"/tmp/invoice_{invoice_id}.pdf"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(pdf_data)
    return output_path, len(pdf_data)


def _execute(config, model, method, *args, **kwargs):
    db, uid, pw = _authenticate(config)
    kw = kwargs.get("kw", {})
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, method, args, kw)


# ── Generic model operations ──────────────────────────────────────────────

def _model_search(db, uid, pw, config, model, domain, limit=50, offset=0, fields=None, order=""):
    domain_args = [list(domain)]
    kw = {"limit": limit, "offset": offset, "order": order}
    if fields:
        kw["fields"] = fields.split(",") if isinstance(fields, str) else fields
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "search_read", domain_args, kw)


def _model_read(db, uid, pw, config, model, ids, fields=None):
    kw = {}
    if fields:
        kw["fields"] = fields.split(",") if isinstance(fields, str) else fields
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "read", [ids], kw)


def _model_create(db, uid, pw, config, model, values):
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "create", [values])


def _model_write(db, uid, pw, config, model, ids, values):
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "write", [ids, values])


def _model_unlink(db, uid, pw, config, model, ids):
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "unlink", [ids])


def _model_count(db, uid, pw, config, model, domain):
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "search_count", [list(domain)])


def _model_fields(db, uid, pw, config, model):
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, "fields_get", [], {})


def _model_call(db, uid, pw, config, model, method, *method_args):
    return _jsonrpc(config, "object", "execute_kw", db, uid, pw, model, method, list(method_args), {})


# ── Check connection ──────────────────────────────────────────────────────

def cmd_check(config):
    result = _jsonrpc(config, "common", "authenticate",
                      config["db"], config["user"], config["password"], {})
    if not result["ok"]:
        _print_json(result)
        return
    uid = result["result"]
    ver = _jsonrpc(config, "common", "version")
    _print_json({
        "ok": True,
        "url": config["url"],
        "db": config["db"],
        "user": config["user"],
        "uid": uid,
        "version": ver.get("result", {}) if ver.get("ok") else "unknown",
    })


def cmd_version(config):
    result = _jsonrpc(config, "common", "version")
    if result["ok"]:
        _print_json({"ok": True, **result["result"]})
    else:
        _print_json(result)


# ── Model command ─────────────────────────────────────────────────────────

def cmd_model(args, config):
    db, uid, pw = _authenticate(config)
    action = args.model_action
    model = args.model_name

    if action == "search":
        domain = json.loads(args.domain) if args.domain else []
        r = _model_search(db, uid, pw, config, model, domain, args.limit, args.offset, args.fields, args.order)
    elif action == "read":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        r = _model_read(db, uid, pw, config, model, ids, args.fields)
    elif action == "create":
        values = json.loads(args.values)
        r = _model_create(db, uid, pw, config, model, values)
    elif action == "write":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        values = json.loads(args.values)
        r = _model_write(db, uid, pw, config, model, ids, values)
    elif action == "unlink":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        r = _model_unlink(db, uid, pw, config, model, ids)
    elif action == "fields":
        r = _model_fields(db, uid, pw, config, model)
    elif action == "count":
        domain = json.loads(args.domain) if args.domain else []
        r = _model_count(db, uid, pw, config, model, domain)
    elif action == "call":
        method_name = args.method_name
        method_args = json.loads(args.method_args) if args.method_args else []
        r = _model_call(db, uid, pw, config, model, method_name, *method_args)
    else:
        r = {"ok": False, "error": f"Unknown model action: {action}"}

    _print_json(r)


# ── CRM ───────────────────────────────────────────────────────────────────

def _crm_parse_values(args):
    vals = {}
    if args.values:
        vals = json.loads(args.values)
    for field in ["name", "email_from", "phone", "description", "type", "priority", "expected_revenue", "date_deadline", "probability"]:
        key = field.replace("_", "-")
        if hasattr(args, key) and getattr(args, key) is not None:
            vals[field] = getattr(args, key)
    if hasattr(args, "partner_id") and args.partner_id is not None:
        vals["partner_id"] = args.partner_id
    if hasattr(args, "stage_id") and args.stage_id is not None:
        vals["stage_id"] = args.stage_id
    if hasattr(args, "user_id") and args.user_id is not None:
        vals["user_id"] = args.user_id
    if hasattr(args, "team_id") and args.team_id is not None:
        vals["team_id"] = args.team_id
    return vals


def cmd_crm(args, config):
    db, uid, pw = _authenticate(config)
    action = args.crm_action
    fields = "name,partner_id,email_from,phone,type,stage_id,user_id,team_id,priority,expected_revenue,date_deadline,create_date,activity_date_deadline"

    if action == "list-leads":
        domain = [["type", "=", "lead"]]
        if hasattr(args, "user_id") and args.user_id:
            domain.append(["user_id", "=", args.user_id])
        if hasattr(args, "team_id") and args.team_id:
            domain.append(["team_id", "=", args.team_id])
        r = _model_search(db, uid, pw, config, "crm.lead", domain, args.limit, args.offset, fields, args.order)
        _print_json(r)
    elif action == "list-opportunities":
        domain = [["type", "=", "opportunity"]]
        if hasattr(args, "user_id") and args.user_id:
            domain.append(["user_id", "=", args.user_id])
        if hasattr(args, "team_id") and args.team_id:
            domain.append(["team_id", "=", args.team_id])
        r = _model_search(db, uid, pw, config, "crm.lead", domain, args.limit, args.offset, fields, args.order)
        _print_json(r)
    elif action == "get":
        r = _model_read(db, uid, pw, config, "crm.lead", [args.id], fields)
        _print_json(r)
    elif action == "create":
        vals = _crm_parse_values(args)
        if not vals.get("type"):
            vals["type"] = args.entity_type if hasattr(args, "entity_type") else "lead"
        r = _model_create(db, uid, pw, config, "crm.lead", vals)
        _print_json(r)
    elif action == "update":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        vals = _crm_parse_values(args)
        r = _model_write(db, uid, pw, config, "crm.lead", ids, vals)
        _print_json(r)
    elif action == "delete":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        r = _model_unlink(db, uid, pw, config, "crm.lead", ids)
        _print_json(r)
    elif action == "stages":
        r = _model_search(db, uid, pw, config, "crm.stage", [], args.limit, 0, "name,sequence,is_won,team_id", "sequence")
        _print_json(r)
    elif action == "statistics":
        total = _model_count(db, uid, pw, config, "crm.lead", [])
        leads = _model_count(db, uid, pw, config, "crm.lead", [["type", "=", "lead"]])
        opps = _model_count(db, uid, pw, config, "crm.lead", [["type", "=", "opportunity"]])
        _print_json({"ok": True, "result": {"total_leads": total.get("result"), "leads": leads.get("result"), "opportunities": opps.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown CRM action: {action}"})


# ── Sales ─────────────────────────────────────────────────────────────────

SALE_ORDER_FIELDS = "name,partner_id,date_order,state,amount_total,amount_untaxed,currency_id,user_id,team_id,invoice_status,create_date"


def cmd_sales(args, config):
    db, uid, pw = _authenticate(config)
    action = args.sales_action

    if action in ("list-quotations", "list-orders"):
        domain = [["state", "=", action.replace("list-", "")]]
        if hasattr(args, "state") and args.state:
            domain = [["state", "=", args.state]]
        if hasattr(args, "partner_id") and args.partner_id:
            domain.append(["partner_id", "=", args.partner_id])
        r = _model_search(db, uid, pw, config, "sale.order", domain, args.limit, args.offset, SALE_ORDER_FIELDS, "id desc")
        _print_json(r)
    elif action == "get":
        r = _model_read(db, uid, pw, config, "sale.order", [args.id], SALE_ORDER_FIELDS)
        _print_json(r)
    elif action == "create":
        vals = {"partner_id": args.partner_id}
        if hasattr(args, "date") and args.date:
            vals["date_order"] = args.date
        if hasattr(args, "order_lines") and args.order_lines:
            vals["order_line"] = json.loads(args.order_lines)
        if hasattr(args, "user_id") and args.user_id:
            vals["user_id"] = args.user_id
        r = _model_create(db, uid, pw, config, "sale.order", vals)
        _print_json(r)
    elif action == "confirm":
        r = _model_call(db, uid, pw, config, "sale.order", "action_confirm", [args.id])
        _print_json(r)
    elif action == "cancel":
        r = _model_call(db, uid, pw, config, "sale.order", "action_cancel", [args.id])
        _print_json(r)
    elif action == "set-state":
        vals = {"state": args.state}
        r = _model_write(db, uid, pw, config, "sale.order", [args.id], vals)
        _print_json(r)
    elif action == "order-lines":
        domain = [["order_id", "=", args.id]]
        r = _model_search(db, uid, pw, config, "sale.order.line", domain, args.limit, 0, "product_id,name,product_uom_qty,price_unit,price_subtotal", "sequence")
        _print_json(r)
    elif action == "products":
        domain = [["sale_ok", "=", True]]
        r = _model_search(db, uid, pw, config, "product.template", domain, args.limit, 0, "name,list_price,default_code,type,uom_id,qty_available")
        _print_json(r)
    elif action == "statistics":
        draft = _model_count(db, uid, pw, config, "sale.order", [["state", "=", "draft"]])
        sent = _model_count(db, uid, pw, config, "sale.order", [["state", "=", "sent"]])
        sale = _model_count(db, uid, pw, config, "sale.order", [["state", "=", "sale"]])
        done = _model_count(db, uid, pw, config, "sale.order", [["state", "=", "done"]])
        _print_json({"ok": True, "result": {"draft": draft.get("result"), "sent": sent.get("result"), "sale": sale.get("result"), "done": done.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown Sales action: {action}"})


# ── Inventory ─────────────────────────────────────────────────────────────

def cmd_inventory(args, config):
    db, uid, pw = _authenticate(config)
    action = args.inventory_action

    if action == "check-stock":
        domain = []
        if hasattr(args, "product_id") and args.product_id:
            domain.append(["product_id", "=", args.product_id])
        if hasattr(args, "location_id") and args.location_id:
            domain.append(["location_id", "=", args.location_id])
        r = _model_search(db, uid, pw, config, "stock.quant", domain, args.limit, 0,
                          "product_id,location_id,quantity,available_quantity,lot_id,inventory_quantity")
        _print_json(r)
    elif action == "transfers":
        domain = []
        if hasattr(args, "state") and args.state:
            domain.append(["state", "=", args.state])
        r = _model_search(db, uid, pw, config, "stock.picking", domain, args.limit, 0,
                          "name,partner_id,picking_type_id,state,scheduled_date,origin,date_done")
        _print_json(r)
    elif action == "get-transfer":
        r = _model_read(db, uid, pw, config, "stock.picking", [args.id],
                        "name,partner_id,picking_type_id,state,scheduled_date,origin,move_line_ids,date_done")
        _print_json(r)
    elif action == "move-lines":
        r = _model_search(db, uid, pw, config, "stock.move", [["picking_id", "=", args.picking_id]], args.limit, 0,
                          "product_id,product_uom_qty,quantity,state,name,location_id,location_dest_id")
        _print_json(r)
    elif action == "warehouses":
        r = _model_search(db, uid, pw, config, "stock.warehouse", [], args.limit, 0,
                          "name,code,partner_id,lot_stock_id")
        _print_json(r)
    elif action == "products":
        domain = []
        r = _model_search(db, uid, pw, config, "product.product", domain, args.limit, 0,
                          "name,default_code,type,qty_available,virtual_available,uom_id,lst_price")
        _print_json(r)
    elif action == "create-quant":
        vals = {"product_id": args.product_id, "location_id": args.location_id, "inventory_quantity": args.quantity}
        r = _model_create(db, uid, pw, config, "stock.quant", vals)
        _print_json(r)
    elif action == "adjust-stock":
        vals = {"inventory_quantity": args.quantity}
        r = _model_write(db, uid, pw, config, "stock.quant", [args.id], vals)
        _print_json(r)
    elif action == "create-transfer":
        vals = {
            "picking_type_id": args.picking_type_id,
            "location_id": args.src_location_id,
            "location_dest_id": args.dest_location_id,
        }
        if hasattr(args, "partner_id") and args.partner_id:
            vals["partner_id"] = args.partner_id
        r = _model_create(db, uid, pw, config, "stock.picking", vals)
        _print_json(r)
    elif action == "add-move":
        vals = {
            "product_id": args.product_id,
            "product_uom_qty": args.quantity,
            "location_id": args.src_location_id,
            "location_dest_id": args.dest_location_id,
            "picking_id": args.picking_id,
            "name": args.product_id,
        }
        r = _model_create(db, uid, pw, config, "stock.move", vals)
        _print_json(r)
    elif action == "validate-transfer":
        result = _model_call(db, uid, pw, config, "stock.picking", "button_validate", [args.id])
        # Odoo 19 returns SMS confirmation wizard — validation already done
        if result.get("ok") and isinstance(result.get("result"), dict) and result["result"].get("res_model") == "confirm.stock.sms":
            _print_json({"ok": True, "result": {"validated": True, "transfer_id": args.id, "note": "SMS wizard skipped, transfer processed"}})
        else:
            _print_json(result)
    elif action == "mark-done":
        result = _model_call(db, uid, pw, config, "stock.picking", "button_validate", [args.id])
        if result.get("ok") and isinstance(result.get("result"), dict) and result["result"].get("res_model") == "confirm.stock.sms":
            _print_json({"ok": True, "result": {"validated": True, "transfer_id": args.id, "note": "Transfer marked done"}})
        else:
            _print_json(result)
    elif action == "create-warehouse":
        vals = {"name": args.name, "code": args.code}
        r = _model_create(db, uid, pw, config, "stock.warehouse", vals)
        _print_json(r)
    elif action == "create-location":
        vals = {"name": args.name, "location_id": args.parent_location_id}
        if hasattr(args, "usage") and args.usage:
            vals["usage"] = args.usage
        r = _model_create(db, uid, pw, config, "stock.location", vals)
        _print_json(r)
    elif action == "locations":
        r = _model_search(db, uid, pw, config, "stock.location", [], args.limit, 0,
                          "name,complete_name,location_id,usage")
        _print_json(r)
    elif action == "statistics":
        total_quants = _model_count(db, uid, pw, config, "stock.quant", [])
        draft = _model_count(db, uid, pw, config, "stock.picking", [["state", "=", "draft"]])
        waiting = _model_count(db, uid, pw, config, "stock.picking", [["state", "=", "waiting"]])
        confirmed = _model_count(db, uid, pw, config, "stock.picking", [["state", "=", "confirmed"]])
        assigned = _model_count(db, uid, pw, config, "stock.picking", [["state", "=", "assigned"]])
        done = _model_count(db, uid, pw, config, "stock.picking", [["state", "=", "done"]])
        _print_json({"ok": True, "result": {
            "stock_quants": total_quants.get("result"),
            "transfers": {"draft": draft.get("result"), "waiting": waiting.get("result"),
                          "confirmed": confirmed.get("result"), "assigned": assigned.get("result"),
                          "done": done.get("result")}
        }})
    else:
        _print_json({"ok": False, "error": f"Unknown Inventory action: {action}"})


# ── Manufacturing ─────────────────────────────────────────────────────────

MRP_FIELDS = "name,product_id,product_qty,bom_id,state,date_start,date_finished,user_id,origin"


def cmd_manufacturing(args, config):
    db, uid, pw = _authenticate(config)
    action = args.mfg_action

    if action == "list-orders":
        domain = []
        if hasattr(args, "state") and args.state:
            domain.append(["state", "=", args.state])
        r = _model_search(db, uid, pw, config, "mrp.production", domain, args.limit, 0, MRP_FIELDS, "id desc")
        _print_json(r)
    elif action == "get-order":
        r = _model_read(db, uid, pw, config, "mrp.production", [args.id],
                        "name,product_id,product_qty,bom_id,state,date_start,date_finished,user_id,origin,move_raw_ids,workorder_ids")
        _print_json(r)
    elif action == "create-order":
        vals = {"product_id": args.product_id, "product_qty": args.qty}
        if hasattr(args, "bom_id") and args.bom_id:
            vals["bom_id"] = args.bom_id
        r = _model_create(db, uid, pw, config, "mrp.production", vals)
        _print_json(r)
    elif action == "confirm":
        r = _model_call(db, uid, pw, config, "mrp.production", "action_confirm", [args.id])
        _print_json(r)
    elif action == "set-qty-producing":
        r = _model_call(db, uid, pw, config, "mrp.production", "button_plan", [args.id])
        _print_json(r)
    elif action == "boms":
        r = _model_search(db, uid, pw, config, "mrp.bom", [], args.limit, 0, "product_tmpl_id,code,product_qty,bom_line_ids,type")
        _print_json(r)
    elif action == "get-bom":
        r = _model_read(db, uid, pw, config, "mrp.bom", [args.id],
                        "product_tmpl_id,code,product_qty,type,bom_line_ids")
        _print_json(r)
    elif action == "bom-lines":
        r = _model_search(db, uid, pw, config, "mrp.bom.line", [["bom_id", "=", args.bom_id]], args.limit, 0,
                          "product_id,product_qty,product_uom_id,sequence")
        _print_json(r)
    elif action == "work-orders":
        r = _model_search(db, uid, pw, config, "mrp.workorder", [["production_id", "=", args.production_id]], args.limit, 0,
                          "name,workcenter_id,state,duration_expected,duration,date_start,date_finished")
        _print_json(r)
    elif action == "statistics":
        draft = _model_count(db, uid, pw, config, "mrp.production", [["state", "=", "draft"]])
        confirmed = _model_count(db, uid, pw, config, "mrp.production", [["state", "=", "confirmed"]])
        progress = _model_count(db, uid, pw, config, "mrp.production", [["state", "=", "progress"]])
        done = _model_count(db, uid, pw, config, "mrp.production", [["state", "=", "done"]])
        boms = _model_count(db, uid, pw, config, "mrp.bom", [])
        _print_json({"ok": True, "result": {
            "production_orders": {"draft": draft.get("result"), "confirmed": confirmed.get("result"),
                                  "in_progress": progress.get("result"), "done": done.get("result")},
            "boms": boms.get("result")
        }})
    else:
        _print_json({"ok": False, "error": f"Unknown Manufacturing action: {action}"})


# ── Purchase ──────────────────────────────────────────────────────────────

PURCHASE_FIELDS = "name,partner_id,date_order,date_planned,state,amount_total,currency_id,user_id,origin"


def cmd_purchase(args, config):
    db, uid, pw = _authenticate(config)
    action = args.purchase_action

    if action in ("list-rfqs", "list-orders"):
        state = "draft" if action == "list-rfqs" else "purchase"
        if hasattr(args, "state") and args.state:
            state = args.state
        domain = [["state", "=", state]]
        if hasattr(args, "partner_id") and args.partner_id:
            domain.append(["partner_id", "=", args.partner_id])
        r = _model_search(db, uid, pw, config, "purchase.order", domain, args.limit, 0, PURCHASE_FIELDS, "id desc")
        _print_json(r)
    elif action == "get":
        r = _model_read(db, uid, pw, config, "purchase.order", [args.id],
                        "name,partner_id,date_order,date_planned,state,amount_total,currency_id,user_id,origin,order_line")
        _print_json(r)
    elif action == "create":
        vals = {"partner_id": args.partner_id}
        if hasattr(args, "order_lines") and args.order_lines:
            vals["order_line"] = json.loads(args.order_lines)
        if hasattr(args, "date") and args.date:
            vals["date_order"] = args.date
        r = _model_create(db, uid, pw, config, "purchase.order", vals)
        _print_json(r)
    elif action == "confirm":
        r = _model_call(db, uid, pw, config, "purchase.order", "button_confirm", [args.id])
        _print_json(r)
    elif action == "cancel":
        r = _model_call(db, uid, pw, config, "purchase.order", "button_cancel", [args.id])
        _print_json(r)
    elif action == "order-lines":
        r = _model_search(db, uid, pw, config, "purchase.order.line", [["order_id", "=", args.id]], args.limit, 0,
                          "product_id,name,product_qty,price_unit,price_subtotal,date_planned")
        _print_json(r)
    elif action == "statistics":
        draft = _model_count(db, uid, pw, config, "purchase.order", [["state", "=", "draft"]])
        sent = _model_count(db, uid, pw, config, "purchase.order", [["state", "=", "sent"]])
        purchase = _model_count(db, uid, pw, config, "purchase.order", [["state", "=", "purchase"]])
        done = _model_count(db, uid, pw, config, "purchase.order", [["state", "=", "done"]])
        _print_json({"ok": True, "result": {"draft_rfq": draft.get("result"), "sent": sent.get("result"),
                                            "confirmed": purchase.get("result"), "done": done.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown Purchase action: {action}"})


# ── Accounting ────────────────────────────────────────────────────────────

ACCOUNT_MOVE_FIELDS = "name,ref,partner_id,date,invoice_date,state,move_type,amount_total,amount_untaxed,currency_id,journal_id,payment_state"


def cmd_accounting(args, config):
    db, uid, pw = _authenticate(config)
    action = args.acct_action

    if action == "invoices":
        domain = [["move_type", "=", args.invoice_type]]
        if hasattr(args, "state") and args.state:
            domain.append(["state", "=", args.state])
        r = _model_search(db, uid, pw, config, "account.move", domain, args.limit, 0, ACCOUNT_MOVE_FIELDS, "id desc")
        _print_json(r)
    elif action == "bills":
        domain = [["move_type", "=", "in_invoice"]]
        if hasattr(args, "state") and args.state:
            domain.append(["state", "=", args.state])
        r = _model_search(db, uid, pw, config, "account.move", domain, args.limit, 0, ACCOUNT_MOVE_FIELDS, "id desc")
        _print_json(r)
    elif action == "get-invoice":
        r = _model_read(db, uid, pw, config, "account.move", [args.id],
                        "name,ref,partner_id,date,invoice_date,invoice_date_due,state,move_type,amount_total,amount_untaxed,currency_id,journal_id,payment_state,invoice_line_ids")
        _print_json(r)
    elif action == "create-invoice":
        vals = {"partner_id": args.partner_id, "move_type": args.move_type}
        if hasattr(args, "date") and args.date:
            vals["invoice_date"] = args.date
        if hasattr(args, "lines") and args.lines:
            line_dicts = json.loads(args.lines)
            vals["invoice_line_ids"] = [(0, 0, line) for line in line_dicts]
        r = _model_create(db, uid, pw, config, "account.move", vals)
        _print_json(r)
    elif action == "validate":
        r = _model_call(db, uid, pw, config, "account.move", "action_post", [args.id])
        _print_json(r)
    elif action == "journal-items":
        domain = [["move_id", "=", args.move_id]]
        r = _model_search(db, uid, pw, config, "account.move.line", domain, args.limit, 0,
                          "name,account_id,debit,credit,balance,date,partner_id")
        _print_json(r)
    elif action == "payments":
        r = _model_search(db, uid, pw, config, "account.payment", [], args.limit, 0,
                          "name,payment_type,partner_id,amount,date,state,journal_id")
        _print_json(r)
    elif action == "statistics":
        drafts = _model_count(db, uid, pw, config, "account.move", [["state", "=", "draft"]])
        posted = _model_count(db, uid, pw, config, "account.move", [["state", "=", "posted"]])
        out_inv = _model_count(db, uid, pw, config, "account.move", [["move_type", "=", "out_invoice"]])
        in_inv = _model_count(db, uid, pw, config, "account.move", [["move_type", "=", "in_invoice"]])
        _print_json({"ok": True, "result": {
            "draft": drafts.get("result"), "posted": posted.get("result"),
            "customer_invoices": out_inv.get("result"), "vendor_bills": in_inv.get("result")
        }})
    elif action == "download-pdf":
        path, size = _download_invoice_pdf(config, args.id, getattr(args, "output", None))
        _print_json({"ok": True, "result": {"invoice_id": args.id, "file": path, "size_bytes": size}})
    else:
        _print_json({"ok": False, "error": f"Unknown Accounting action: {action}"})


# ── HR ────────────────────────────────────────────────────────────────────

HR_EMPLOYEE_FIELDS = "name,user_id,department_id,job_id,work_email,work_phone,parent_id,coach_id,marital,gender"


def cmd_hr(args, config):
    db, uid, pw = _authenticate(config)
    action = args.hr_action

    if action == "employees":
        domain = []
        if hasattr(args, "department_id") and args.department_id:
            domain.append(["department_id", "=", args.department_id])
        r = _model_search(db, uid, pw, config, "hr.employee", domain, args.limit, 0, HR_EMPLOYEE_FIELDS)
        _print_json(r)
    elif action == "get-employee":
        r = _model_read(db, uid, pw, config, "hr.employee", [args.id],
                        "name,user_id,department_id,job_id,work_email,work_phone,parent_id,coach_id,address_id,marital,gender,birthday")
        _print_json(r)
    elif action == "departments":
        r = _model_search(db, uid, pw, config, "hr.department", [], args.limit, 0,
                          "name,parent_id,manager_id,member_ids,company_id")
        _print_json(r)
    elif action == "create-employee":
        vals = {"name": args.name}
        r = _model_create(db, uid, pw, config, "hr.employee", vals)
        _print_json(r)
    elif action == "statistics":
        total = _model_count(db, uid, pw, config, "hr.employee", [])
        depts = _model_count(db, uid, pw, config, "hr.department", [])
        _print_json({"ok": True, "result": {"employees": total.get("result"), "departments": depts.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown HR action: {action}"})


# ── Expenses ──────────────────────────────────────────────────────────────

EXPENSE_FIELDS = "name,employee_id,product_id,price_unit,total_amount,quantity,date,state,description"


def cmd_expenses(args, config):
    db, uid, pw = _authenticate(config)
    action = args.expense_action

    if action == "list":
        domain = []
        if hasattr(args, "state") and args.state:
            domain.append(["state", "=", args.state])
        if hasattr(args, "employee_id") and args.employee_id:
            domain.append(["employee_id", "=", args.employee_id])
        r = _model_search(db, uid, pw, config, "hr.expense", domain, args.limit, 0, EXPENSE_FIELDS)
        _print_json(r)
    elif action == "get":
        r = _model_read(db, uid, pw, config, "hr.expense", [args.id], EXPENSE_FIELDS)
        _print_json(r)
    elif action == "create":
        vals = {"name": args.name}
        for f in ["employee_id", "product_id", "total_amount", "date", "description"]:
            if hasattr(args, f) and getattr(args, f) is not None:
                vals[f] = getattr(args, f)
        if hasattr(args, "price_unit") and args.price_unit is not None:
            vals["price_unit"] = args.price_unit
        if hasattr(args, "quantity") and args.quantity is not None:
            vals["quantity"] = args.quantity
        r = _model_create(db, uid, pw, config, "hr.expense", vals)
        _print_json(r)
    elif action == "attach":
        attachment = {
            "name": getattr(args, "filename", "receipt"),
            "type": "binary",
            "res_model": "hr.expense",
            "res_id": args.expense_id,
            "datas": args.data,
            "mimetype": getattr(args, "mimetype", "application/octet-stream"),
        }
        r = _model_create(db, uid, pw, config, "ir.attachment", attachment)
        _print_json(r)
    elif action == "attachments":
        r = _model_search(db, uid, pw, config, "ir.attachment",
                          [["res_model", "=", "hr.expense"], ["res_id", "=", args.expense_id]],
                          args.limit, 0, "name,mimetype,file_size,create_date")
        _print_json(r)
    elif action == "submit":
        r = _model_call(db, uid, pw, config, "hr.expense", "action_submit_expenses", [args.id])
        _print_json(r)
    elif action == "approve":
        r = _model_call(db, uid, pw, config, "hr.expense", "action_approve_duplicates", [args.id])
        _print_json(r)
    elif action == "refuse":
        r = _model_call(db, uid, pw, config, "hr.expense", "action_refuse_expenses", [args.id])
        _print_json(r)
    elif action == "statistics":
        total = _model_count(db, uid, pw, config, "hr.expense", [])
        draft = _model_count(db, uid, pw, config, "hr.expense", [["state", "=", "draft"]])
        reported = _model_count(db, uid, pw, config, "hr.expense", [["state", "=", "reported"]])
        approved = _model_count(db, uid, pw, config, "hr.expense", [["state", "=", "approved"]])
        done = _model_count(db, uid, pw, config, "hr.expense", [["state", "=", "done"]])
        _print_json({"ok": True, "result": {"total": total.get("result"), "draft": draft.get("result"),
                                            "reported": reported.get("result"),
                                            "approved": approved.get("result"), "done": done.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown Expenses action: {action}"})


# ── Contacts ──────────────────────────────────────────────────────────────

PARTNER_FIELDS = "name,email,phone,mobile,website,customer_rank,supplier_rank,is_company,parent_id,type,street,city,country_id,create_date"


def cmd_contacts(args, config):
    db, uid, pw = _authenticate(config)
    action = args.contact_action

    if action == "list":
        domain = []
        if hasattr(args, "is_company") and args.is_company is not None:
            domain.append(["is_company", "=", args.is_company])
        r = _model_search(db, uid, pw, config, "res.partner", domain, args.limit, args.offset, PARTNER_FIELDS, args.order)
        _print_json(r)
    elif action == "search":
        r = _model_search(db, uid, pw, config, "res.partner",
                          [["name", "ilike", args.query]], args.limit, 0, PARTNER_FIELDS)
        _print_json(r)
    elif action == "get":
        r = _model_read(db, uid, pw, config, "res.partner", [args.id],
                        "name,email,phone,mobile,website,is_company,parent_id,type,street,street2,city,zip,state_id,country_id,vat,comment,customer_rank,supplier_rank,create_date")
        _print_json(r)
    elif action == "create":
        vals = {"name": args.name}
        for field in ["email", "phone", "mobile", "website", "street", "city", "zip", "country_id"]:
            if hasattr(args, field) and getattr(args, field) is not None:
                vals[field] = getattr(args, field)
        if hasattr(args, "is_company") and args.is_company is not None:
            vals["is_company"] = args.is_company
        if hasattr(args, "parent_id") and args.parent_id:
            vals["parent_id"] = args.parent_id
        r = _model_create(db, uid, pw, config, "res.partner", vals)
        _print_json(r)
    elif action == "update":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        vals = json.loads(args.values)
        r = _model_write(db, uid, pw, config, "res.partner", ids, vals)
        _print_json(r)
    elif action == "delete":
        ids = json.loads(args.ids) if args.ids.startswith("[") else [int(args.ids)]
        r = _model_unlink(db, uid, pw, config, "res.partner", ids)
        _print_json(r)
    elif action == "statistics":
        total = _model_count(db, uid, pw, config, "res.partner", [])
        companies = _model_count(db, uid, pw, config, "res.partner", [["is_company", "=", True]])
        individuals = _model_count(db, uid, pw, config, "res.partner", [["is_company", "=", False]])
        customers = _model_count(db, uid, pw, config, "res.partner", [["customer_rank", ">", 0]])
        suppliers = _model_count(db, uid, pw, config, "res.partner", [["supplier_rank", ">", 0]])
        _print_json({"ok": True, "result": {"total": total.get("result"), "companies": companies.get("result"),
                                            "individuals": individuals.get("result"),
                                            "customers": customers.get("result"), "suppliers": suppliers.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown Contacts action: {action}"})


# ── Calendar ──────────────────────────────────────────────────────────────

CALENDAR_FIELDS = "name,start,stop,allday,duration,location,description,user_id,create_date"


def cmd_calendar(args, config):
    db, uid, pw = _authenticate(config)
    action = args.cal_action

    if action == "events":
        domain = []
        if hasattr(args, "start_date") and args.start_date:
            domain.append(["start", ">=", args.start_date])
        if hasattr(args, "end_date") and args.end_date:
            domain.append(["stop", "<=", args.end_date])
        if hasattr(args, "user_id") and args.user_id:
            domain.append(["user_id", "=", args.user_id])
        r = _model_search(db, uid, pw, config, "calendar.event", domain, args.limit, 0, CALENDAR_FIELDS, "start asc")
        _print_json(r)
    elif action == "get-event":
        r = _model_read(db, uid, pw, config, "calendar.event", [args.id],
                        "name,start,stop,allday,duration,location,description,user_id,partner_ids,attendee_ids,create_date")
        _print_json(r)
    elif action == "create-event":
        vals = {"name": args.name, "start": args.start, "stop": args.stop}
        if hasattr(args, "description") and args.description:
            vals["description"] = args.description
        if hasattr(args, "location") and args.location:
            vals["location"] = args.location
        if hasattr(args, "allday") and args.allday:
            vals["allday"] = True
        if hasattr(args, "partner_ids") and args.partner_ids:
            vals["partner_ids"] = json.loads(args.partner_ids)
        if hasattr(args, "user_id") and args.user_id:
            vals["user_id"] = args.user_id
        r = _model_create(db, uid, pw, config, "calendar.event", vals)
        _print_json(r)
    elif action == "delete-event":
        r = _model_unlink(db, uid, pw, config, "calendar.event", [args.id])
        _print_json(r)
    elif action == "statistics":
        total = _model_count(db, uid, pw, config, "calendar.event", [])
        upcoming = _model_count(db, uid, pw, config, "calendar.event", [["start", ">=", "now"]])
        _print_json({"ok": True, "result": {"total_events": total.get("result"), "upcoming": upcoming.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown Calendar action: {action}"})


# ── Discuss ───────────────────────────────────────────────────────────────

MESSAGE_FIELDS = "subject,body,email_from,author_id,date,model,res_id,message_type,record_name"


def cmd_discuss(args, config):
    db, uid, pw = _authenticate(config)
    action = args.discuss_action

    if action == "messages":
        domain = []
        if hasattr(args, "model") and args.model:
            domain.append(["model", "=", args.model])
        if hasattr(args, "res_id") and args.res_id:
            domain.append(["res_id", "=", args.res_id])
        r = _model_search(db, uid, pw, config, "mail.message", domain, args.limit, 0, MESSAGE_FIELDS, "date desc")
        _print_json(r)
    elif action == "send":
        vals = {
            "model": args.model,
            "res_id": args.res_id,
            "body": args.body,
            "message_type": "comment",
            "subtype_xmlid": "mail.mt_comment",
        }
        r = _model_create(db, uid, pw, config, "mail.message", vals)
        _print_json(r)
    elif action == "followers":
        r = _model_search(db, uid, pw, config, "mail.followers",
                          [["res_model", "=", args.model], ["res_id", "=", args.res_id]], args.limit, 0,
                          "partner_id,display_name,email")
        _print_json(r)
    elif action == "activities":
        domain = []
        if hasattr(args, "user_id") and args.user_id:
            domain.append(["user_id", "=", args.user_id])
        r = _model_search(db, uid, pw, config, "mail.activity", domain, args.limit, 0,
                          "activity_type_id,summary,date_deadline,user_id,res_model,res_id,res_name")
        _print_json(r)
    elif action == "statistics":
        total = _model_count(db, uid, pw, config, "mail.message", [])
        activities = _model_count(db, uid, pw, config, "mail.activity", [])
        _print_json({"ok": True, "result": {"messages": total.get("result"), "activities": activities.get("result")}})
    else:
        _print_json({"ok": False, "error": f"Unknown Discuss action: {action}"})


# ── CLI setup ─────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(description="Odoo API CLI for Hermes skills")
    sub = parser.add_subparsers(dest="command", help="Module or action")

    # --- check ---
    sub.add_parser("check", help="Verify Odoo connection and credentials")
    sub.add_parser("version", help="Show Odoo server version")

    # --- model (generic) ---
    model_p = sub.add_parser("model", help="Generic model CRUD operations")
    model_p.add_argument("model_name", help="Odoo model technical name (e.g. crm.lead)")
    model_subs = model_p.add_subparsers(dest="model_action")

    p = model_subs.add_parser("search", help="Search records")
    p.add_argument("--domain", default="[]", help="Odoo domain as JSON (e.g. '[[\"state\",\"=\",\"draft\"]]')")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--fields", help="Comma-separated field names")
    p.add_argument("--order", default="id desc", help="Sort order")

    p = model_subs.add_parser("read", help="Read records by ID")
    p.add_argument("ids", help="Record ID(s) as int or JSON array [1,2,3]")
    p.add_argument("--fields", help="Comma-separated field names")

    p = model_subs.add_parser("create", help="Create a record")
    p.add_argument("values", help="JSON dict of field values")

    p = model_subs.add_parser("write", help="Update records")
    p.add_argument("ids", help="Record ID(s) as int or JSON array [1,2,3]")
    p.add_argument("values", help="JSON dict of field values")

    p = model_subs.add_parser("unlink", help="Delete records")
    p.add_argument("ids", help="Record ID(s) as int or JSON array [1,2,3]")

    p = model_subs.add_parser("fields", help="List model fields")

    p = model_subs.add_parser("count", help="Count records matching domain")
    p.add_argument("--domain", default="[]", help="Odoo domain as JSON")

    p = model_subs.add_parser("call", help="Call a model method")
    p.add_argument("method_name", help="Method name")
    p.add_argument("--method-args", default="[]", help="JSON list of method arguments")

    # --- crm ---
    crm_p = sub.add_parser("crm", help="CRM operations (leads, opportunities)")
    crm_subs = crm_p.add_subparsers(dest="crm_action")

    p = crm_subs.add_parser("list-leads")
    _add_common_list_args(p, "id desc")
    p.add_argument("--user-id", type=int)
    p.add_argument("--team-id", type=int)

    p = crm_subs.add_parser("list-opportunities")
    _add_common_list_args(p, "id desc")
    p.add_argument("--user-id", type=int)
    p.add_argument("--team-id", type=int)

    p = crm_subs.add_parser("get")
    p.add_argument("id", type=int)

    p = crm_subs.add_parser("create")
    p.add_argument("--name", help="Lead/opportunity name")
    p.add_argument("--partner-id", type=int)
    p.add_argument("--email-from")
    p.add_argument("--phone")
    p.add_argument("--description")
    p.add_argument("--type", help="'lead' or 'opportunity'")
    p.add_argument("--stage-id", type=int)
    p.add_argument("--user-id", type=int)
    p.add_argument("--team-id", type=int)
    p.add_argument("--priority")
    p.add_argument("--expected-revenue", type=float)
    p.add_argument("--date-deadline")
    p.add_argument("--probability", type=float)
    p.add_argument("--values", help="Full JSON values dict (overrides named args)")

    p = crm_subs.add_parser("update")
    p.add_argument("ids", help="ID(s) as int or JSON array [1,2,3]")
    p.add_argument("--name")
    p.add_argument("--partner-id", type=int)
    p.add_argument("--email-from")
    p.add_argument("--phone")
    p.add_argument("--description")
    p.add_argument("--type")
    p.add_argument("--stage-id", type=int)
    p.add_argument("--user-id", type=int)
    p.add_argument("--team-id", type=int)
    p.add_argument("--values", help="Full JSON values dict (overrides named args)")

    p = crm_subs.add_parser("delete")
    p.add_argument("ids", help="ID(s) as int or JSON array [1,2,3]")

    p = crm_subs.add_parser("stages")
    p.add_argument("--limit", type=int, default=50)

    p = crm_subs.add_parser("statistics")

    # --- sales ---
    sales_p = sub.add_parser("sales", help="Sales operations (quotations, orders)")
    sales_subs = sales_p.add_subparsers(dest="sales_action")

    for action in ["list-quotations", "list-orders"]:
        p = sales_subs.add_parser(action)
        _add_common_list_args(p)
        if action == "list-quotations":
            p.add_argument("--state", default="draft")
        else:
            p.add_argument("--state", default="sale")
        p.add_argument("--partner-id", type=int)

    p = sales_subs.add_parser("get")
    p.add_argument("id", type=int)

    p = sales_subs.add_parser("create")
    p.add_argument("--partner-id", type=int, required=True)
    p.add_argument("--order-lines", help="JSON array of order line dicts")
    p.add_argument("--date")
    p.add_argument("--user-id", type=int)

    p = sales_subs.add_parser("confirm")
    p.add_argument("id", type=int)

    p = sales_subs.add_parser("cancel")
    p.add_argument("id", type=int)

    p = sales_subs.add_parser("set-state")
    p.add_argument("id", type=int)
    p.add_argument("state", choices=["draft", "sent", "sale", "done", "cancel"])

    p = sales_subs.add_parser("order-lines")
    p.add_argument("id", type=int)
    p.add_argument("--limit", type=int, default=100)

    p = sales_subs.add_parser("products")
    p.add_argument("--limit", type=int, default=50)

    p = sales_subs.add_parser("statistics")

    # --- inventory ---
    inv_p = sub.add_parser("inventory", help="Inventory operations (stock, transfers)")
    inv_subs = inv_p.add_subparsers(dest="inventory_action")

    p = inv_subs.add_parser("check-stock")
    _add_common_list_args(p, "product_id")
    p.add_argument("--product-id", type=int)
    p.add_argument("--location-id", type=int)

    p = inv_subs.add_parser("transfers")
    _add_common_list_args(p, "id desc")
    p.add_argument("--state")

    p = inv_subs.add_parser("get-transfer")
    p.add_argument("id", type=int)

    p = inv_subs.add_parser("move-lines")
    p.add_argument("picking_id", type=int)
    p.add_argument("--limit", type=int, default=100)

    p = inv_subs.add_parser("warehouses")
    p.add_argument("--limit", type=int, default=50)

    p = inv_subs.add_parser("products")
    p.add_argument("--limit", type=int, default=50)

    p = inv_subs.add_parser("create-quant")
    p.add_argument("--product-id", type=int, required=True)
    p.add_argument("--location-id", type=int, required=True)
    p.add_argument("--quantity", type=float, required=True)

    p = inv_subs.add_parser("adjust-stock")
    p.add_argument("id", type=int)
    p.add_argument("--quantity", type=float, required=True)

    p = inv_subs.add_parser("create-transfer")
    p.add_argument("--picking-type-id", type=int, required=True)
    p.add_argument("--src-location-id", type=int, required=True)
    p.add_argument("--dest-location-id", type=int, required=True)
    p.add_argument("--partner-id", type=int)

    p = inv_subs.add_parser("add-move")
    p.add_argument("--product-id", type=int, required=True)
    p.add_argument("--quantity", type=float, required=True)
    p.add_argument("--src-location-id", type=int, required=True)
    p.add_argument("--dest-location-id", type=int, required=True)
    p.add_argument("--picking-id", type=int, required=True)

    p = inv_subs.add_parser("validate-transfer")
    p.add_argument("id", type=int)

    p = inv_subs.add_parser("mark-done")
    p.add_argument("id", type=int)

    p = inv_subs.add_parser("create-warehouse")
    p.add_argument("--name", required=True)
    p.add_argument("--code", required=True)

    p = inv_subs.add_parser("create-location")
    p.add_argument("--name", required=True)
    p.add_argument("--parent-location-id", type=int, required=True)
    p.add_argument("--usage", choices=["supplier","view","internal","customer","inventory","production","transit"])

    p = inv_subs.add_parser("locations")
    p.add_argument("--limit", type=int, default=100)

    p = inv_subs.add_parser("statistics")

    # --- manufacturing ---
    mfg_p = sub.add_parser("manufacturing", help="Manufacturing operations (MRP)")
    mfg_subs = mfg_p.add_subparsers(dest="mfg_action")

    p = mfg_subs.add_parser("list-orders")
    _add_common_list_args(p)
    p.add_argument("--state")

    p = mfg_subs.add_parser("get-order")
    p.add_argument("id", type=int)

    p = mfg_subs.add_parser("create-order")
    p.add_argument("--product-id", type=int, required=True)
    p.add_argument("--qty", type=float, default=1.0)
    p.add_argument("--bom-id", type=int)

    p = mfg_subs.add_parser("confirm")
    p.add_argument("id", type=int)

    p = mfg_subs.add_parser("set-qty-producing")
    p.add_argument("id", type=int)

    p = mfg_subs.add_parser("boms")
    p.add_argument("--limit", type=int, default=50)

    p = mfg_subs.add_parser("get-bom")
    p.add_argument("id", type=int)

    p = mfg_subs.add_parser("bom-lines")
    p.add_argument("bom_id", type=int)
    p.add_argument("--limit", type=int, default=100)

    p = mfg_subs.add_parser("work-orders")
    p.add_argument("production_id", type=int)
    p.add_argument("--limit", type=int, default=50)

    p = mfg_subs.add_parser("statistics")

    # --- purchase ---
    purch_p = sub.add_parser("purchase", help="Purchase operations (RFQs, orders)")
    purch_subs = purch_p.add_subparsers(dest="purchase_action")

    for action in ["list-rfqs", "list-orders"]:
        p = purch_subs.add_parser(action)
        _add_common_list_args(p)
        p.add_argument("--state")
        p.add_argument("--partner-id", type=int)

    p = purch_subs.add_parser("get")
    p.add_argument("id", type=int)

    p = purch_subs.add_parser("create")
    p.add_argument("--partner-id", type=int, required=True)
    p.add_argument("--order-lines", help="JSON array of order line dicts")
    p.add_argument("--date")

    p = purch_subs.add_parser("confirm")
    p.add_argument("id", type=int)

    p = purch_subs.add_parser("cancel")
    p.add_argument("id", type=int)

    p = purch_subs.add_parser("order-lines")
    p.add_argument("id", type=int)
    p.add_argument("--limit", type=int, default=100)

    p = purch_subs.add_parser("statistics")

    # --- accounting ---
    acct_p = sub.add_parser("accounting", help="Accounting operations (invoices, payments)")
    acct_subs = acct_p.add_subparsers(dest="acct_action")

    p = acct_subs.add_parser("invoices")
    _add_common_list_args(p, "id desc")
    p.add_argument("--invoice-type", default="out_invoice", choices=["out_invoice", "out_refund", "in_invoice", "in_refund"])
    p.add_argument("--state")

    p = acct_subs.add_parser("bills")
    _add_common_list_args(p, "id desc")
    p.add_argument("--state")

    p = acct_subs.add_parser("get-invoice")
    p.add_argument("id", type=int)

    p = acct_subs.add_parser("create-invoice")
    p.add_argument("--partner-id", type=int, required=True)
    p.add_argument("--move-type", default="out_invoice")
    p.add_argument("--date")
    p.add_argument("--lines", help="JSON array of invoice line dicts")

    p = acct_subs.add_parser("validate")
    p.add_argument("id", type=int)

    p = acct_subs.add_parser("journal-items")
    p.add_argument("move_id", type=int)
    p.add_argument("--limit", type=int, default=100)

    p = acct_subs.add_parser("payments")
    p.add_argument("--limit", type=int, default=50)

    p = acct_subs.add_parser("statistics")

    p = acct_subs.add_parser("download-pdf")
    p.add_argument("id", type=int)
    p.add_argument("--output")

    # --- hr ---
    hr_p = sub.add_parser("hr", help="HR operations (employees, departments)")
    hr_subs = hr_p.add_subparsers(dest="hr_action")

    p = hr_subs.add_parser("employees")
    _add_common_list_args(p, "name")
    p.add_argument("--department-id", type=int)

    p = hr_subs.add_parser("get-employee")
    p.add_argument("id", type=int)

    p = hr_subs.add_parser("departments")
    p.add_argument("--limit", type=int, default=50)

    p = hr_subs.add_parser("create-employee")
    p.add_argument("--name", required=True)

    p = hr_subs.add_parser("statistics")

    # --- expenses ---
    exp_p = sub.add_parser("expenses", help="Expense operations")
    exp_subs = exp_p.add_subparsers(dest="expense_action")

    p = exp_subs.add_parser("list")
    _add_common_list_args(p)
    p.add_argument("--state")
    p.add_argument("--employee-id", type=int)

    p = exp_subs.add_parser("get")
    p.add_argument("id", type=int)

    p = exp_subs.add_parser("create")
    p.add_argument("--name", required=True)
    p.add_argument("--employee-id", type=int)
    p.add_argument("--product-id", type=int)
    p.add_argument("--price-unit", type=float)
    p.add_argument("--quantity", type=float)
    p.add_argument("--total-amount", type=float)
    p.add_argument("--date")
    p.add_argument("--description")

    p = exp_subs.add_parser("attach")
    p.add_argument("expense_id", type=int)
    p.add_argument("--filename", required=True)
    p.add_argument("--data", required=True, help="Base64-encoded file content")
    p.add_argument("--mimetype", default="application/octet-stream")

    p = exp_subs.add_parser("attachments")
    p.add_argument("expense_id", type=int)
    p.add_argument("--limit", type=int, default=20)

    p = exp_subs.add_parser("submit")
    p.add_argument("id", type=int)

    p = exp_subs.add_parser("approve")
    p.add_argument("id", type=int)

    p = exp_subs.add_parser("refuse")
    p.add_argument("id", type=int)

    p = exp_subs.add_parser("statistics")

    # --- contacts ---
    contact_p = sub.add_parser("contacts", help="Contact/partner operations")
    contact_subs = contact_p.add_subparsers(dest="contact_action")

    p = contact_subs.add_parser("list")
    _add_common_list_args(p, "name")
    p.add_argument("--is-company", type=lambda x: x.lower() == "true" if x else None)

    p = contact_subs.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)

    p = contact_subs.add_parser("get")
    p.add_argument("id", type=int)

    p = contact_subs.add_parser("create")
    p.add_argument("--name", required=True)
    p.add_argument("--email")
    p.add_argument("--phone")
    p.add_argument("--mobile")
    p.add_argument("--website")
    p.add_argument("--street")
    p.add_argument("--city")
    p.add_argument("--zip")
    p.add_argument("--country-id", type=int)
    p.add_argument("--is-company", type=lambda x: x.lower() == "true" if x else None)
    p.add_argument("--parent-id", type=int)

    p = contact_subs.add_parser("update")
    p.add_argument("ids", help="ID(s) as int or JSON array [1,2,3]")
    p.add_argument("values", help="JSON dict of field values to update")

    p = contact_subs.add_parser("delete")
    p.add_argument("ids", help="ID(s) as int or JSON array [1,2,3]")

    p = contact_subs.add_parser("statistics")

    # --- calendar ---
    cal_p = sub.add_parser("calendar", help="Calendar operations (events, meetings)")
    cal_subs = cal_p.add_subparsers(dest="cal_action")

    p = cal_subs.add_parser("events")
    _add_common_list_args(p, "start asc")
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--user-id", type=int)

    p = cal_subs.add_parser("get-event")
    p.add_argument("id", type=int)

    p = cal_subs.add_parser("create-event")
    p.add_argument("--name", required=True)
    p.add_argument("--start", required=True, help="ISO datetime (e.g. 2026-05-15 14:00:00)")
    p.add_argument("--stop", required=True, help="ISO datetime")
    p.add_argument("--description")
    p.add_argument("--location")
    p.add_argument("--allday", action="store_true")
    p.add_argument("--partner-ids", help="JSON array of partner IDs")
    p.add_argument("--user-id", type=int)

    p = cal_subs.add_parser("delete-event")
    p.add_argument("id", type=int)

    p = cal_subs.add_parser("statistics")

    # --- discuss ---
    disc_p = sub.add_parser("discuss", help="Discuss/messaging operations")
    disc_subs = disc_p.add_subparsers(dest="discuss_action")

    p = disc_subs.add_parser("messages")
    _add_common_list_args(p, "date desc")
    p.add_argument("--model", default="res.partner")
    p.add_argument("--res-id", type=int)

    p = disc_subs.add_parser("send")
    p.add_argument("--model", required=True)
    p.add_argument("--res-id", type=int, required=True)
    p.add_argument("--body", required=True)

    p = disc_subs.add_parser("followers")
    p.add_argument("--model", required=True)
    p.add_argument("--res-id", type=int, required=True)
    p.add_argument("--limit", type=int, default=50)

    p = disc_subs.add_parser("activities")
    _add_common_list_args(p)
    p.add_argument("--user-id", type=int)

    p = disc_subs.add_parser("statistics")

    return parser


def _add_common_list_args(parser, default_order="id desc"):
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--fields")
    parser.add_argument("--order", default=default_order)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = _load_config()

    route = {
        "check": lambda a: cmd_check(config),
        "version": lambda a: cmd_version(config),
        "model": lambda a: cmd_model(a, config),
        "crm": lambda a: cmd_crm(a, config),
        "sales": lambda a: cmd_sales(a, config),
        "inventory": lambda a: cmd_inventory(a, config),
        "manufacturing": lambda a: cmd_manufacturing(a, config),
        "purchase": lambda a: cmd_purchase(a, config),
        "accounting": lambda a: cmd_accounting(a, config),
        "hr": lambda a: cmd_hr(a, config),
        "expenses": lambda a: cmd_expenses(a, config),
        "contacts": lambda a: cmd_contacts(a, config),
        "calendar": lambda a: cmd_calendar(a, config),
        "discuss": lambda a: cmd_discuss(a, config),
    }

    handler = route.get(args.command)
    if handler:
        handler(args)
    else:
        _print_json({"ok": False, "error": f"Unknown command: {args.command}"})


if __name__ == "__main__":
    main()
