---
name: odoo-forum
description: Odoo Forum operations — manage forums, posts, questions, and community engagement.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, forum, community, qanda, posts]
    parent_skill: odoo
---
# Odoo Forum

Manage discussion forums, posts, questions, and community engagement.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List forums

```
ODOO model forum.forum search --limit 20 --fields name,description,moderator_ids,access_level,post_count
ODOO model forum.forum read 1 --fields name,description,moderator_ids,access_level,post_count,user_ids,can_ask
```

### List forum posts/questions

```
ODOO model forum.post search --limit 20 --fields name,forum_id,author_id,post_date,content,reply_count,like_count,is_question
ODOO model forum.post search --domain '[["is_question","=",true]]' --fields name,forum_id,author_id,reply_count,like_count
```

### Get post details

```
ODOO model forum.post read 1 --fields name,forum_id,author_id,post_date,content,reply_count,like_count,parent_id,child_ids
```

### List forum tags

```
ODOO model forum.tag search --fields name,forum_id,post_count
```

## Key Models

| Model | Use |
|-------|-----|
| `forum.forum` | Discussion forums |
| `forum.post` | Posts/questions/replies within forums |
| `forum.tag` | Tags for categorizing posts |

## Rules

1. **Posts support Q&A**: Set `is_question = True` for question posts. They can have marked correct answers.
2. **Access levels**: Forums can be public or restricted by user group via `access_level`.
3. **Posts are threaded**: Posts can be replies to other posts using `parent_id`. Use `child_ids` to find replies.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List posts
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"forum.post\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"forum_id\",\"post_date\"]}]},\"id\":2}"
```
