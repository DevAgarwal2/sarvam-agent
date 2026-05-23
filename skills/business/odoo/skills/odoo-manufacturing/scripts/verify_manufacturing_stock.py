#!/usr/bin/env python3
"""
Manufacturing Stock Verification Script
Verifies stock levels after manufacturing order completion
"""

import json
import sys
from hermes_tools import terminal

def verify_manufacturing_stock(product_id):
    """Verify stock levels after MO completion"""
    
    print(f"=== Manufacturing Stock Verification for Product ID: {product_id} ===")
    
    # Check stock quants
    stock_quants = terminal("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model stock.quant search --domain '[[\"product_id\", \"=\", " + str(product_id) + "]]' --limit 5 --fields product_id,quantity")
    
    # Check stock moves
    stock_moves = terminal("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py model stock.move search --domain '[[\"product_id\", \"=\", " + str(product_id) + "]]' --limit 5 --fields product_id,product_qty,picked")
    
    # Check inventory levels
    inventory = terminal("python3 /opt/hermes/skills/business/odoo/scripts/odoo_api.py inventory check-stock --product-id " + str(product_id))
    
    print("\n=== Stock Quants ===")
    print(stock_quants)
    
    print("\n=== Stock Moves ===")
    print(stock_moves)
    
    print("\n=== Inventory Levels ===")
    print(inventory)
    
    # Analysis
    if "result":
        if len(stock_quants["result"]) == 0:
            print("\n⚠️  WARNING: No stock quants found - Manual intervention required")
        else:
            print(f"\n✅ Stock quants found: {len(stock_quants['result'])} records")
    
    if "result" in stock_moves:
        if len(stock_moves["result"]) == 0:
            print("\n⚠️  WARNING: No stock moves found")
        else:
            print(f"\n✅ Stock moves found: {len(stock_moves['result'])} records")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 verify_manufacturing_stock.py PRODUCT_ID")
        sys.exit(1)
    
    product_id = sys.argv[1]
    verify_manufacturing_stock(product_id)