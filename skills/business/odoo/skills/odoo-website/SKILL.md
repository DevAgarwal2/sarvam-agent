---
name: odoo-website
description: Odoo Website operations — manage web pages, menus, and site content.
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odoo, website, pages, cms, blog]
    parent_skill: odoo
---
# Odoo Website

Manage website pages, blog posts, menus, and site content.

**Prerequisite:** `odoo` skill must be set up. `ODOO` = `python scripts/odoo_api.py`.

## Usage

```
ODOO model website.page search --limit 20 --fields name,url,is_published,website_id
ODOO model website.page read 1 --fields name,url,is_published,website_id,arch
ODOO model blog.post search --limit 20 --fields name,blog_id,author_id,post_date,visits
ODOO model blog.blog search --limit 20 --fields name,subtitle
ODOO model website.menu search --limit 20 --fields name,url,parent_id,sequence
```

## Key Models

| Model | Use |
|-------|-----|
| `website.page` | CMS pages |
| `website.menu` | Navigation menus |
| `blog.post` | Blog posts |
| `blog.blog` | Blog categories |

## Curl Examples

```bash
# Authenticate
UID=$(curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"authenticate","args":[$ODOO_DB,"$ODOO_USER","$ODOO_PASS",{}]},"id":1}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")

# List Website
curl -s -X POST $ODOO_URL/jsonrpc -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"service\":\"object\",\"method\":\"execute_kw\",\"args\":[\"$ODOO_DB\",$UID,\"$ODOO_PASS\",\"website.page\",\"search_read\",[[]],{\"limit\":10,\"fields\":[["name", "url", "is_published"]]}},\"id\":2}"
```
