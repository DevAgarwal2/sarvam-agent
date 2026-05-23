---
name: sarvam-ocr
description: Extract text and tables from PDFs/images in 23 languages.
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [ocr, document, pdf, text-extraction, indian-languages]
---

# Sarvam Document OCR

Extract text and tables from documents using Sarvam Document Intelligence, powered by Sarvam Vision (3B parameter VLM).

## When to Use

- Extract text from scanned PDFs, screenshots, or document images
- Convert tables to Markdown or HTML
- Process documents in any of 23 Indian languages + English

## Prerequisites

- `SARVAM_API_KEY` env var set
- `sarvamai` SDK installed (`uv pip install sarvamai`)
- Supported formats: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.zip` (max 10 pages)

## Usage

```bash
/opt/hermes/.venv/bin/python3 skills/sarvam-ocr/scripts/ocr.py document.pdf --lang hi-IN --format md
/opt/hermes/.venv/bin/python3 skills/sarvam-ocr/scripts/ocr.py report.pdf --lang en-IN --format html
/opt/hermes/.venv/bin/python3 skills/sarvam-ocr/scripts/ocr.py scan.png --lang ta-IN --format md
/opt/hermes/.venv/bin/python3 skills/sarvam-ocr/scripts/ocr.py --list-languages
```

## Languages

hi-IN, bn-IN, ta-IN, te-IN, mr-IN, gu-IN, kn-IN, ml-IN, pa-IN, od-IN, en-IN, as-IN, ur-IN, sa-IN, ne-IN, doi-IN, brx-IN, kok-IN, mai-IN, sd-IN, ks-IN, mni-IN, sat-IN

## Limitations

- Max 10 pages per document
- Requires Sarvam AI subscription with Document Intelligence access
