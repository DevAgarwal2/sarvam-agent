---
name: odoo-project
description: Odoo Project operations — manage projects, tasks, and task stages.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, project, tasks, kanban]
    parent_skill: odoo
---
# Odoo Project

Manage projects, tasks, and stages. Uses the generic `model` command.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List projects

```
ODOO model project.project search --limit 20 --fields name,partner_id,user_id,date_start,date,state
```

### Get project

```
ODOO model project.project read 1 --fields name,partner_id,user_id,date_start,date,task_ids,description
```

### List tasks

```
ODOO model project.task search --limit 20 --fields name,project_id,stage_id,user_id,date_deadline,priority,state
ODOO model project.task search --domain '[["project_id","=",1]]' --limit 20 --fields name,stage_id,user_id,date_deadline,priority
```

### Get task

```
ODOO model project.task read 1 --fields name,project_id,stage_id,user_id,date_deadline,date_assign,description,priority
```

### Create project

```
ODOO model project.project create '{"name":"New Project"}'
```

### Create task

```
ODOO model project.task create '{"name":"New Task","project_id":1}'
```

### Count

```
ODOO model project.task count --domain '[["stage_id","!=",false]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `project.project` | Projects |
| `project.task` | Tasks / to-dos |

## Common Fields

**project.project**: name, partner_id, user_id, date_start, date, state, task_ids, description, privacy_visibility, allow_timesheets

**project.task**: name, project_id, stage_id, user_id, date_deadline, date_assign, priority, state, description, planned_hours, progress

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Project
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"project.project\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "date_start", "state"]]}},\"id\":2}"
```
