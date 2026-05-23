---
name: odoo-survey
description: Odoo Survey operations — manage surveys, questions, and collect user responses.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, survey, forms, questionnaires, feedback]
    parent_skill: odoo
---

# Odoo Survey

Manage surveys, questions, and collect user responses.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List surveys

```
ODOO model survey.survey search --limit 20 --fields title,date_start,date_end,question_count,answer_count,active
ODOO model survey.survey search --domain '[[\"active\",\"=\",true]]' --fields title,date_start,date_end,answer_count
```

**Note:** In Odoo 19, `survey.survey` has no `state` field. Use `active` (boolean) for active/inactive surveys. `question_count` (# questions) and `answer_count` (# responses) replace `questions_count`/`participants_count`.

### Get survey details

```
ODOO model survey.survey read 1 --fields title,description,date_start,date_end,question_count,answer_count,active,question_ids,certification,certificate_template_id
```

### List questions

```
ODOO model survey.question search --domain '[[\"survey_id\",\"=\",1]]' --fields title,question_type,sequence,constr_mandatory,page_id
ODOO model survey.question read 1 --fields title,question_type,survey_id,sequence,constr_mandatory,labels_ids,answer_ids
```

### List responses

```
ODOO model survey.user_input search --domain '[[\"survey_id\",\"=\",1]]' --limit 20 --fields partner_id,email,state,date_create,date_start,date_end,score,quizz_score
ODOO model survey.user_input read 1 --fields partner_id,email,state,date_create,date_start,date_end,score,user_input_line_ids
```

### View response details

```
ODOO model survey.user_input.line search --domain '[[\"user_input_id\",\"=\",1]]' --fields question_id,value,value_score,skipped,answer_type
```

### Statistics

```
ODOO model survey.survey count --domain '[[\"active\",\"=\",true]]'
ODOO model survey.user_input count --domain '[[\"survey_id\",\"=\",1]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `survey.survey` | Surveys |
| `survey.question` | Questions within a survey |
| `survey.question.answer` | Predefined answer options |
| `survey.user_input` | User response submissions |
| `survey.user_input.line` | Individual answer lines |

## Question Types

| Type | Meaning |
|------|---------|
| `simple_choice` | Multiple choice (single) |
| `multiple_choice` | Multiple choice (multi) |
| `textbox` | Free text input |
| `numerical_box` | Numeric input |
| `date` | Date picker |
| `matrix` | Matrix/grid of choices |

## Rules

1. **Surveys can be certified**: Surveys with `certification = True` can issue certificates on completion.
2. **Scoring**: For scored surveys, `quizz_score` shows the percentage. Pass threshold is set on the survey.
3. **Limesurvey import**: Odoo supports importing surveys from Limesurvey format.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List surveys
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"survey.survey\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"title\",\"active\",\"date_start\"]}]},\"id\":2}"
```
