---
name: odoo-certificate
description: Odoo Certificate operations — manage certificates, templates, and certificate issuance.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, certificate, certifications, templates]
    parent_skill: odoo
---
# Odoo Certificate

Manage certificates and cryptographic keys. No standalone menu — accessible programmatically via the API or through eLearning certifications.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List certificates

```
ODOO model certificate.certificate search --limit 20 --fields name,partner_id,template_id,issue_date,expiration_date,state
ODOO model certificate.certificate search --domain '[["partner_id","=",3]]' --fields name,template_id,issue_date,state
```

### Get certificate details

```
ODOO model certificate.certificate read 1 --fields name,partner_id,template_id,issue_date,expiration_date,state,description,attachment_ids
```

### List certificate templates

```
ODOO model certificate.template search --fields name,description,days_valid,can_be_revoked,require_expiration
```

### Statistics

```
ODOO model certificate.certificate count --domain '[["state","=","valid"]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `certificate.certificate` | Issued certificates |
| `certificate.template` | Certificate templates/configurations |

## States

| State | Meaning |
|-------|---------|
| `draft` | Not yet issued |
| `valid` | Active/valid certificate |
| `expired` | Past expiration date |
| `revoked` | Revoked by issuer |

## Rules

1. **Certificates link to partners**: Each certificate is issued to a `res.partner`.
2. **Templates control validity**: `days_valid` on the template sets how long certificates remain valid.
3. **Certificates can be revoked**: If `can_be_revoked` is True on the template, certificates can be cancelled early.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List certificates
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"certificate.certificate\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"partner_id\",\"issue_date\",\"state\"]}]},\"id\":2}"
```
