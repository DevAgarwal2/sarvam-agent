---
name: odoo-fleet
description: Odoo Fleet operations — manage vehicles, contracts, and vehicle logs.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, fleet, vehicles, contracts]
    parent_skill: odoo
---

# Odoo Fleet

Manage vehicles, contracts, and service logs.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

```
ODOO model fleet.vehicle search --limit 20 --fields name,driver_id,license_plate,model_id,active
ODOO model fleet.vehicle read 1 --fields name,driver_id,license_plate,model_id,active,odometer,description
ODOO model fleet.vehicle create '{"name":"Toyota Camry","model_id":1,"license_plate":"ABC-1234"}'
ODOO model fleet.vehicle.log.contract search --limit 20 --fields name,vehicle_id,start_date,expiration_date,state,amount
```

**Note:** `fleet.vehicle` has no direct `state` field in Odoo 19. Use `active` (boolean) to filter active/inactive vehicles. Vehicle contract states (`futur`, `open`, `expired`, `closed`) are on `fleet.vehicle.log.contract.state`.

## Key Models

| Model | Use |
|-------|-----|
| `fleet.vehicle` | Vehicles |
| `fleet.vehicle.model` | Vehicle models |
| `fleet.vehicle.log.contract` | Contracts/insurance |

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Fleet
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"fleet.vehicle\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"driver_id\",\"license_plate\",\"active\"]}]},\"id\":2}"
```
