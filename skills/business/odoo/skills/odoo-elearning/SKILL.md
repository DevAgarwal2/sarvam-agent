---
name: odoo-elearning
description: Odoo eLearning operations — manage courses, slides, certifications, and student progress.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, elearning, courses, slides, certifications, training]
    parent_skill: odoo
---

# Odoo eLearning

Manage courses, slides/lessons, certifications, and track student progress.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List courses

```
ODOO model slide.channel search --limit 20 --fields name,description,visibility,members_count,completion,is_published
ODOO model slide.channel search --domain '[[\"is_published\",\"=\",true]]' --fields name,description,visibility,members_count
```

### Get course details

```
ODOO model slide.channel read 1 --fields name,description,visibility,members_count,completion,slide_ids,user_id,is_published,karma_lower_bound
```

### List slides/lessons

```
ODOO model slide.slide search --limit 20 --fields name,channel_id,slide_type,completion_time,is_published,sequence
ODOO model slide.slide search --domain '[[\"channel_id\",\"=\",1]]' --fields name,slide_type,completion_time,sequence
```

### Get slide content

```
ODOO model slide.slide read 1 --fields name,channel_id,slide_type,description,html_content,url,document_id,completion_time,quiz_first_attempt_reward,is_published
```

### List course members/students

```
ODOO model slide.channel.partner search --domain '[[\"channel_id\",\"=\",1]]' --fields partner_id,completed,completion_time,progress
```

### List quizzes

```
ODOO model slide.question search --domain '[[\"slide_id\",\"=\",1]]' --fields question,question_type,timer_seconds,randomize_answer_order
```

### Statistics

```
ODOO model slide.channel count --domain '[[\"is_published\",\"=\",true]]'
ODOO model slide.slide count --domain '[[\"channel_id\",\"=\",1]]'
```

## Key Models

| Model | Use |
|-------|-----|
| `slide.channel` | Courses |
| `slide.slide` | Individual slides/lessons within a course |
| `slide.channel.partner` | Student enrollment and progress |
| `slide.question` | Quiz questions |
| `slide.answer` | Quiz answer options |

## Slide Types

| Type | Meaning |
|------|---------|
| `infographic` | Static content page |
| `document` | Document (PDF, etc.) |
| `video` | Video lesson |
| `quiz` | Quiz/assessment |
| `webpage` | Embedded webpage |

## Rules

1. **Courses can be certified**: When `survey_id` is set on a channel, completing the survey grants a certification.
2. **Completion tracking**: Students are marked complete when they view all required slides. Quiz slides require passing.
3. **Visibility levels**: `public` (anyone), `portal` (portal users), `private` (by invitation only).

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List courses
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"slide.channel\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"visibility\",\"members_count\"]}]},\"id\":2}"
```
