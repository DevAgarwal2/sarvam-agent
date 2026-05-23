#!/usr/bin/env python3
"""
Odoo ERP Health Check Script
Comprehensive health monitoring for Odoo instances
"""

import subprocess
import json
import sys

def run_odoo_command(cmd):
    """Run Odoo API command and return parsed JSON"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception running command: {e}")
        return None

def check_inventory_system():
    """Check inventory system health"""
    print("=== INVENTORY SYSTEM CHECK ===")
    
    # Check stock quants
    quants = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model stock.quant count")
    if quants and quants.get('result', 0) == 0:
        print("❌ CRITICAL: No stock quants found")
    else:
        print(f"✅ Stock quants: {quants.get('result', 0)}")
    
    # Check stock moves
    moves = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model stock.move search --domain '[[\"picked\", \"=\", false]]' --limit 5")
    if moves:
        print(f"⚠️  Pending stock moves: {len(moves.get('result', []))}")
    
    # Check warehouse config
    warehouses = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model stock.warehouse search --limit 3")
    if warehouses:
        print(f"🏭 Warehouses: {len(warehouses.get('result', []))}")

def check_financial_system():
    """Check financial system health"""
    print("\n=== FINANCIAL SYSTEM CHECK ===")
    
    # Check invoices
    invoices = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model account.move search --limit 3 --fields name,state,amount_total")
    if invoices:
        draft_count = sum(1 for inv in invoices.get('result', []) if inv.get('state') == 'draft')
        print(f"📄 Invoices - Total: {len(invoices.get('result', []))}, Draft: {draft_count}")
    
    # Check orders
    sales_orders = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model sale.order search --limit 3 --fields name,state,amount_total")
    if sales_orders:
        draft_count = sum(1 for so in sales_orders.get('result', []) if so.get('state') == 'draft')
        print(f"🛒 Sales Orders - Total: {len(sales_orders.get('result', []))}, Draft: {draft_count}")

def check_operational_health():
    """Check operational health"""
    print("\n=== OPERATIONAL HEALTH CHECK ===")
    
    # Check users
    users = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model res.users count")
    if users:
        print(f"👥 Users: {users.get('result', 0)}")
    
    # Check cron jobs
    cron_jobs = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model ir.cron count")
    if cron_jobs:
        print(f"⏰ Cron Jobs: {cron_jobs.get('result', 0)}")
    
    # Check communications
    messages = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model mail.message count")
    if messages:
        print(f"💬 Messages: {messages.get('result', 0)}")

def main():
    """Run comprehensive health check"""
    print("🔍 Odoo ERP Health Check")
    print("=" * 50)
    
    # Check connection first
    connection = run_odoo_command("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py check")
    if not connection:
        print("❌ Cannot connect to Odoo")
        sys.exit(1)
    
    print(f"✅ Connected to Odoo {connection.get('version', {}).get('server_version', 'Unknown')}")
    
    # Run checks
    check_inventory_system()
    check_financial_system()
    check_operational_health()
    
    print("\n" + "=" * 50)
    print("Health check complete. Review issues above.")

if __name__ == "__main__":
    main()