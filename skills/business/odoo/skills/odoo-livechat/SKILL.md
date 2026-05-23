---
name: odoo-livechat
description: Odoo Live Chat operations — manage chat channels, conversations, and visitor communications.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, livechat, chat, conversations, support]
    parent_skill: odoo
---
# Odoo Live Chat

Manage live chat channels, conversations, and visitor communications.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

### List live chat channels

```
ODOO model im_livechat.channel search --limit 20 --fields name,channel_type,description,user_ids
ODOO model im_livechat.channel read 1 --fields name,channel_type,description,user_ids,rule_ids,button_text,default_message
```

### List chat conversations

```
ODOO model mail.channel search --domain '[["livechat_visitor_id","!=",false]]' --limit 20 --fields name,livechat_visitor_id,channel_type,create_date
ODOO model mail.channel read 1 --fields name,livechat_visitor_id,channel_type,create_date,anonymous_name
```

### List visitors

```
ODOO model im_livechat.visitor search --limit 20 --fields name,channel_ids,access_token,website_id,country_id
ODOO model im_livechat.visitor search --domain '[["country_id","!=",false]]' --fields name,access_token
```

### List chat rules

```
ODOO model im_livechat.channel.rule search --fields chat_channel_id,action,auto_popup,country_id,url_regex
```

## Key Models

| Model | Use |
|-------|-----|
| `im_livechat.channel` | Live chat channels/queues |
| `mail.channel` | Chat conversations (with livechat_visitor_id) |
| `im_livechat.visitor` | Website visitors |
| `im_livechat.channel.rule` | Routing rules |

## Rules

1. **Channels route to operators**: Each channel has assigned operators (`user_ids`). Unassigned chats go to any available operator.
2. **Visitor is anonymous until identified**: Visitors have `access_token` until they identify via email or login.
3. **Conversations are mail.channel records**: All chat messages in a conversation are `mail.message` records linked to the `mail.channel`.

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List channels
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"im_livechat.channel\",\"search_read\",[[]],{\"limit\":10,\"fields\":[\"name\",\"channel_type\"]}]},\"id\":2}"
```
