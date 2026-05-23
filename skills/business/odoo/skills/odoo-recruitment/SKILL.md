---
name: odoo-recruitment
description: Odoo Recruitment operations — manage job postings, applicants, and hiring pipeline.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, recruitment, hiring, jobs, applicants]
    parent_skill: odoo
---
# Odoo Recruitment

Manage job postings, applicants, and the hiring pipeline.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List job positions

```
ODOO model hr.job search --limit 20 --fields name,department_id,no_of_recruitment,state
```

### List applicants

```
ODOO model hr.applicant search --limit 20 --fields partner_name,job_id,stage_id,user_id,email_from,partner_phone,create_date
ODOO model hr.applicant search --domain '[["stage_id","=",1]]' --limit 20 --fields partner_name,job_id,email_from
```

### Get applicant

```
ODOO model hr.applicant read 1 --fields partner_name,job_id,stage_id,user_id,email_from,partner_phone,description
```

### Create applicant

```
ODOO model hr.applicant create '{"partner_name":"Jane Smith","job_id":1,"email_from":"jane@example.com","partner_phone":"+1-555-0100"}'
```

### List recruitment stages

```
ODOO model hr.recruitment.stage search --limit 20 --fields name,sequence,job_ids
```

## Key Models

| Model | Use |
|-------|-----|
| `hr.job` | Job positions |
| `hr.applicant` | Job applicants |
| `hr.recruitment.stage` | Recruitment pipeline stages |

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Recruitment
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"hr.applicant\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["partner_name", "job_id", "email_from", "stage_id"]]}},\"id\":2}"
```
