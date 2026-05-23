# sarvam-agent

A production-ready Hermes Agent Docker instance powered by **Sarvam AI** (chat, TTS, STT, OCR) with **Mistral** vision, **Odoo ERP** integration, browser automation, email, and development skills.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Configuration](#configuration)
  - [API Keys (.env)](#api-keys-env)
  - [Chat — Sarvam](#chat)
  - [TTS — Sarvam Bulbul](#tts)
  - [STT — Sarvam Saaras](#stt)
  - [Vision — Mistral](#vision)
  - [Browser Automation](#browser-automation)
  - [Email — Himalaya](#email)
- [Odoo ERP Setup](#odoo-erp-setup)
- [Skills](#skills)
- [Docker Compose](#docker-compose)
- [Telegram Setup](#telegram-setup)
- [Commands Reference](#commands-reference)
- [Troubleshooting](#troubleshooting)
- [Security](#security)

---

## Quick Start

### Prerequisites

- **Docker** + Docker Compose
- [**Sarvam AI**](https://sarvam.ai) account → API key for chat, TTS, STT, OCR
- [**Mistral AI**](https://console.mistral.ai) account → API key for vision
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- **Odoo instance** (optional) → for ERP features

### 3-Minute Setup

```bash
# 1. Clone the repo
git clone https://github.com/DevAgarwal2/sarvam-agent.git
cd sarvam-agent

# 2. Create your .env from the template
cp .env.example .env

# 3. Edit .env with your actual API keys
#    SARVAM_API_KEY=sk_...
#    MISTRAL_API_KEY=...
#    TELEGRAM_BOT_TOKEN=...

# 4. Create docker-compose.yml next to this directory (see Docker Compose section)
#    Or use the one provided in the parent repo

# 5. Start the container
docker compose up -d hermes-1

# 6. Verify
curl http://localhost:8642/health
docker compose logs -f hermes-1
```

---

## Architecture

```
sarvam-agent/
├── config.yaml              # Hermes config — model, tools, TTS, STT, vision
├── SOUL.md                  # Agent personality
├── .env.example             # API keys template → copy to .env
├── README.md                # This file
├── skills/
│   ├── sarvam/              # TTS (Bulbul v3) + STT (Saaras v3) bridge scripts
│   ├── sarvam-ocr/          # Document OCR via Sarvam Document Intelligence
│   ├── business/odoo/       # Odoo ERP — full suite
│   ├── creative/            # Diagramming, design, media generation
│   ├── data-science/        # Jupyter live kernel
│   ├── email/himalaya/      # IMAP/SMTP email via Himalaya CLI
│   └── software-development/  # Planning, debugging, TDD, code review
└── .config/himalaya/        # Email config (create after setup)
```

---

## Configuration

### API Keys (.env)

```bash
cp .env.example .env
```

Edit `.env`:

```ini
# ---- LLM Provider (Chat, TTS, STT, OCR) ----
SARVAM_API_KEY=sk_your_sarvam_api_key_here

# ---- Vision ----
MISTRAL_API_KEY=your_mistral_api_key_here

# ---- Telegram ----
TELEGRAM_BOT_TOKEN=12345:your_bot_token_here
TELEGRAM_ALLOWED_USERS=your_telegram_user_id

# ---- Optional ----
# FAL_KEY=                  # Image generation
# BROWSERBASE_API_KEY=      # Cloud browser
# EXA_API_KEY=              # Web search
```

### Chat

Sarvam AI as the primary chat model. Configured in `config.yaml`:

```yaml
model:
  default: sarvam-105b      # or sarvam-30b
  provider: custom
  base_url: https://api.sarvam.ai/v1
  api_key: SARVAM_API_KEY_PLACEHOLDER
  api_mode: chat_completions
```

### TTS

Text-to-speech via Sarvam **Bulbul v3**. 30+ Indian-accent speakers, 11 languages. Wired as a native tool — works with `/speak` and Telegram voice bubbles.

```yaml
tts:
  provider: sarvam
  providers:
    sarvam:
      type: command
      command: "python3 /opt/data/skills/sarvam/scripts/tts_bridge.py {input_path} {output_path} shubh en-IN"
      output_format: wav
      voice_compatible: true       # Enables Telegram voice bubbles
```

**Available speakers:** shubh (default), aditya, ritu, priya, neha, rahul, pooja, rohan, simran, kavya, amit, dev, ishita, shreya, ratan, varun, manan, sumit, roopa, kabir, aayan, ashutosh, advait, anand, tanya, tarun, sunny, mani, gokul, vijay, shruti, suhani, mohit, kavitha, rehan, soham, rupali

**Languages:** hi-IN, bn-IN, ta-IN, te-IN, gu-IN, kn-IN, ml-IN, mr-IN, pa-IN, od-IN, en-IN

### STT

Speech-to-text via Sarvam **Saaras v3**. 23 languages, 5 output modes. Auto-transcribes voice messages on Telegram.

```yaml
stt:
  enabled: true
  provider: local_command
```

**STT Modes:**
- `transcribe` — original language script
- `translate` — speech → English text
- `verbatim` — exact word-for-word
- `translit` — romanized output
- `codemix` — mixed script

### Vision

Image analysis via Mistral **pixtral-large-latest**.

```yaml
auxiliary:
  vision:
    provider: mistral
    model: pixtral-large-latest
    base_url: https://api.mistral.ai/v1
    api_key: MISTRAL_API_KEY_PLACEHOLDER
    timeout: 120
```

### Browser Automation

Headless Chromium via **agent-browser**. Zero config — included in Docker image.

```yaml
browser:
  engine: auto
  cloud_provider: local
```

### Email

Himalaya CLI for IMAP/SMTP email. After setup, create `.config/himalaya/config.toml`:

```toml
[accounts.gmail]
email = "you@gmail.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@gmail.com"
backend.auth.type = "password"
backend.auth.raw = "your-16-char-app-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@gmail.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "your-16-char-app-password"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"
```

> For Gmail: enable 2FA → create [App Password](https://myaccount.google.com/apppasswords).

---

## Odoo ERP Setup

This instance connects to an Odoo ERP instance for CRM, sales, inventory, accounting, HR, and contacts.

### Step 1: Start Odoo (if not running)

```bash
# Create network
docker network create odoo-net

# PostgreSQL
docker run -d --name odoo-db --network odoo-net \
  -e POSTGRES_USER=odoo \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_DB=odoo \
  postgres:16-alpine

# Odoo 19.0
docker run -d --name odoo-app --network odoo-net \
  -p 8069:8069 \
  -e HOST=odoo-db \
  -e USER=odoo \
  -e PASSWORD=odoo \
  odoo:19.0
```

Wait 30 seconds for Odoo to initialize, then visit `http://localhost:8069` to complete the web setup (create admin user, install apps).

### Step 2: Install Required Odoo Apps

In Odoo web UI → Apps:
- **Sales** (sale_management)
- **Purchase** (purchase)
- **Inventory** (stock)
- **Accounting** (account_accountant)
- **CRM** (crm)
- **Contacts** (contacts)
- **HR** (hr)

### Step 3: Configure Connection

Create `odoo_config.json` in the `sarvam-agent/` directory:

```json
{
  "url": "http://host.docker.internal:8069",
  "db": "odoo",
  "user": "your_admin_email@example.com",
  "password": "your_odoo_password"
}
```

> Use `host.docker.internal` to reach the host machine from inside the Docker container.

### Step 4: Restart Hermes

```bash
docker compose restart hermes-1
```

### Step 5: Verify

```bash
# Test connection
docker exec hermes-1 python3 /opt/data/skills/business/odoo/scripts/setup.py --check

# Should show: AUTHENTICATED (uid=X)
```

### Odoo Commands Reference

All commands use the `odoo_api.py` script:

```bash
python3 /opt/data/skills/business/odoo/scripts/odoo_api.py <module> <action> [args]
```

#### Sales

```bash
# List draft quotations
odoo_api.py sales list-quotations --state draft --limit 10

# Get order details
odoo_api.py sales get-quotation <order_id>

# Confirm/validate order
odoo_api.py sales confirm <order_id>

# Create quotation
odoo_api.py sales create-quotation --partner-id <id>
```

#### Purchase

```bash
# List draft purchase orders
odoo_api.py purchase list-orders --state draft

# Get order details
odoo_api.py purchase get-order <order_id>

# Confirm order
odoo_api.py purchase confirm <order_id>
```

#### Inventory

```bash
# List warehouses
odoo_api.py inventory warehouses

# List products
odoo_api.py inventory products --limit 20

# List stock locations
odoo_api.py inventory locations --limit 50

# Check stock for a product
odoo_api.py inventory check-stock --product-id <id>

# Create stock quant
odoo_api.py inventory create-quant --product-id <id> --location-id <id> --quantity <n>

# Adjust stock level
odoo_api.py inventory adjust-stock <quant_id> --quantity <n>

# List transfers
odoo_api.py inventory transfers --state assigned

# Get transfer details
odoo_api.py inventory get-transfer <id>

# Create transfer
odoo_api.py inventory create-transfer --picking-type-id <id> --src-location-id <id> --dest-location-id <id>

# Add move line to transfer
odoo_api.py inventory add-move --product-id <id> --quantity <n> --src-location-id <id> --dest-location-id <id> --picking-id <id>

# Validate transfer
odoo_api.py inventory validate-transfer <id>

# Create warehouse
odoo_api.py inventory create-warehouse --name "Warehouse Name" --code "WH"

# Create location
odoo_api.py inventory create-location --name "Shelf A" --parent-location-id <id> --usage internal

# Inventory statistics
odoo_api.py inventory statistics
```

#### Accounting

```bash
# List customer invoices
odoo_api.py accounting invoices --invoice-type out_invoice

# List vendor bills
odoo_api.py accounting bills

# Get invoice details
odoo_api.py accounting get-invoice <invoice_id>

# Create invoice with line items
odoo_api.py accounting create-invoice \
  --partner-id <id> \
  --move-type out_invoice \
  --lines '[{"product_id":30,"name":"Cane Webbing","quantity":5,"price_unit":800}]'

# Validate/post invoice
odoo_api.py accounting validate <invoice_id>

# Download invoice PDF
odoo_api.py accounting download-pdf <invoice_id> --output /path/to/invoice.pdf

# List journal items
odoo_api.py accounting journal-items <move_id>

# List payments
odoo_api.py accounting payments

# Accounting statistics
odoo_api.py accounting statistics
```

#### CRM

```bash
# List leads
odoo_api.py crm list-leads --limit 20

# Get lead details
odoo_api.py crm get-lead <id>

# Create lead
odoo_api.py crm create-lead --name "New Lead" --partner-id <id>

# List opportunities
odoo_api.py crm list-opportunities --limit 20

# Convert lead to opportunity
odoo_api.py crm convert-lead <id>
```

#### HR

```bash
odoo_api.py hr employees
odoo_api.py hr departments
odoo_api.py hr get-employee <id>
odoo_api.py hr create-employee --name "John Doe"
odoo_api.py hr statistics
```

#### Contacts

```bash
odoo_api.py contacts list --limit 20
odoo_api.py contacts get <id>
odoo_api.py contacts create --name "Company Name"
```

#### Generic Model Operations

```bash
# Search any model
odoo_api.py model <model_name> search '<domain>' --limit 10 --fields "name,id"

# Read records
odoo_api.py model <model_name> read <id> --fields "name,email"

# Create record
odoo_api.py model <model_name> create '{"name":"Test"}'

# Update record
odoo_api.py model <model_name> write <id> '{"name":"Updated"}'

# Delete record
odoo_api.py model <model_name> unlink <id>

# Count records
odoo_api.py model <model_name> count '<domain>'

# List fields
odoo_api.py model <model_name> fields
```

---

## Skills

Skills are auto-discovered from `skills/` and loaded by the agent on demand.

### Sarvam AI Stack

| Skill | Capability | Model |
|-------|-----------|-------|
| `sarvam` | TTS + STT | bulbul:v3, saaras:v3 |
| `sarvam-ocr` | Document OCR | Document Intelligence |

```bash
# TTS
python3 skills/sarvam/scripts/tts.py "Hello" --speaker shubh --lang hi-IN
python3 skills/sarvam/scripts/tts.py --list-speakers

# STT
python3 skills/sarvam/scripts/stt.py audio.wav --mode translate
python3 skills/sarvam/scripts/stt.py --list-modes

# OCR
/opt/hermes/.venv/bin/python3 skills/sarvam-ocr/scripts/ocr.py document.pdf --lang hi-IN --format md
/opt/hermes/.venv/bin/python3 skills/sarvam-ocr/scripts/ocr.py --list-languages
```

### Odoo

Full ERP integration — see [Odoo ERP Setup](#odoo-erp-setup).

### Creative

Diagramming (architecture-diagram, excalidraw), ASCII art/video, comic generation (baoyu-comic), infographics (baoyu-infographic), design systems (design-md), manim video, p5.js sketches, pixel art, web design templates (50+ popular designs).

### Software Development

Planning, spike-driven development, TDD, systematic debugging (Python + Node.js), code review, subagent-driven development, hermes-agent skill authoring.

### Email

IMAP/SMTP via Himalaya CLI — read, search, compose, reply, forward, download attachments.

### Data Science

Jupyter live kernel for interactive notebook workflows.

---

## Docker Compose

Create `docker-compose.yml` in the **parent directory** of `sarvam-agent/`:

```yaml
services:
  hermes-1:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-1
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"         # Gateway API
      - "9119:9119"         # Dashboard (optional)
    volumes:
      - ./sarvam-agent:/opt/data
    environment:
      - HERMES_UID=${HERMES_UID:-10000}
      - HERMES_GID=${HERMES_GID:-10000}
      - SARVAM_API_KEY=${SARVAM_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - HERMES_LOCAL_STT_COMMAND=python3 /opt/data/skills/sarvam/scripts/stt_bridge.py {input_path} {output_dir} {model} {language}
      - AGENT_BROWSER_EXECUTABLE_PATH=/opt/hermes/.playwright/chromium_headless_shell-1223/chrome-linux/headless_shell
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

Start with:

```bash
# With env vars inline
SARVAM_API_KEY=sk_... MISTRAL_API_KEY=... docker compose up -d hermes-1

# Or create .env next to docker-compose.yml
echo "SARVAM_API_KEY=sk_..." >> ../.env
echo "MISTRAL_API_KEY=..." >> ../.env
docker compose up -d hermes-1
```

**Multiple instances:** duplicate the service block with different names, ports, and data directories.

---

## Telegram Setup

1. Create a bot with [@BotFather](https://t.me/BotFather) → `/newbot`
2. Copy the token → set `TELEGRAM_BOT_TOKEN` in `.env`
3. Get your user ID from [@userinfobot](https://t.me/userinfobot)
4. Set `TELEGRAM_ALLOWED_USERS` to your user ID

### Group Setup

1. BotFather → `/mybots` → Bot Settings:
   - **Allow Groups?** → ON
   - **Group Privacy** → OFF
2. Add bot to group as **Admin**
3. Forward a group message to @userinfobot to get the group chat ID (negative number)
4. Add to allowed users: `TELEGRAM_ALLOWED_USERS=12345678,-1001234567890`

---

## Commands Reference

```bash
# Start
docker compose up -d hermes-1

# Stop
docker compose stop hermes-1

# Restart (picks up config.yaml changes)
docker compose restart hermes-1

# Recreate (picks up env var changes)
docker compose up -d hermes-1

# View logs
docker compose logs -f hermes-1

# Interactive CLI (TUI mode)
docker exec -it hermes-1 /opt/hermes/.venv/bin/hermes --tui

# Health check
curl http://localhost:8642/health

# Dashboard (if enabled)
open http://localhost:9119

# Test TTS
docker exec hermes-1 python3 /opt/data/skills/sarvam/scripts/tts.py "Hello" --speaker shubh

# Test STT
docker exec hermes-1 python3 /opt/data/skills/sarvam/scripts/stt.py --list-modes

# Test Odoo connection
docker exec hermes-1 python3 /opt/data/skills/business/odoo/scripts/setup.py --check

# Test OCR
docker exec hermes-1 /opt/hermes/.venv/bin/python3 /opt/data/skills/sarvam-ocr/scripts/ocr.py --list-languages

# Clean rebuild
docker compose down && docker compose up -d --build hermes-1

# Upgrade
docker compose pull && docker compose up -d hermes-1
```

---

## Troubleshooting

### Container exits immediately

```bash
docker logs hermes-1 --tail 50
```
Common causes: missing `.env`, invalid API keys, port conflicts.

### Voice messages not working

1. Test TTS in CLI first:
```bash
docker exec -it hermes-1 /opt/hermes/.venv/bin/hermes --tui
# → /speak test
```

2. Check voice_compatible is true in config.yaml
3. Verify `HERMES_LOCAL_STT_COMMAND` env var is set

### Odoo not reachable

```bash
# Test from inside container
docker exec hermes-1 curl -s http://host.docker.internal:8069/web/login
```

On Linux (no `host.docker.internal`):
```bash
# Find host IP
docker exec hermes-1 ip route | awk '/default/ {print $3}'
# Then update odoo_config.json with that IP
```

### Vision not working

Check model name and endpoint:
```bash
curl -s https://api.mistral.ai/v1/models -H "Authorization: Bearer $MISTRAL_API_KEY" | grep pixtral
```

Expected: `pixtral-large-latest`

### OCR not working

OCR needs Sarvam Document Intelligence access:
```bash
docker exec hermes-1 /opt/hermes/.venv/bin/python3 -c "
from sarvamai import SarvamAI
client = SarvamAI(api_subscription_key='$SARVAM_API_KEY')
job = client.document_intelligence.create_job(language='en-IN', output_format='md')
print('Job created:', job.job_id)
"
```

### Browser not working

```bash
docker exec hermes-1 agent-browser --version
docker exec hermes-1 agent-browser --executable-path /opt/hermes/.playwright/chromium_headless_shell-1223/chrome-linux/headless_shell navigate https://example.com snapshot
```

### Skills not loading

Ensure `skills` is in `platform_toolsets.telegram` and `platform_toolsets.cli` in config.yaml. Restart after adding/removing skills.

---

## Security

- **Never commit `.env`** — it's in `.gitignore`; use `.env.example` as template
- **Never commit `odoo_config.json`** — add to `.gitignore`
- **Never commit `.config/himalaya/config.toml`** — contains email credentials
- Rotate API keys regularly
- Use `TELEGRAM_ALLOWED_USERS` to restrict bot access
- The gateway API server is off by default — enable only with `API_SERVER_KEY`
- Run `docker compose restart` after changing config files
