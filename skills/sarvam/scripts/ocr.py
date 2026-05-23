#!/opt/hermes/.venv/bin/python3
"""Sarvam Document OCR — extract text/tables from PDFs and images.
Uses SarvamAI SDK (Document Intelligence).
Outputs .md or .html file directly.
Usage: python3 ocr.py <file> --lang en-IN --format md
"""
import argparse, json, os, sys, zipfile

API_KEY = os.environ.get("SARVAM_API_KEY", "")

LANGS = [
    "hi-IN","bn-IN","ta-IN","te-IN","mr-IN","gu-IN","kn-IN","ml-IN",
    "pa-IN","od-IN","en-IN","as-IN","ur-IN","sa-IN","ne-IN","doi-IN",
    "brx-IN","kok-IN","mai-IN","sd-IN","ks-IN","mni-IN","sat-IN"
]

VALID_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".zip"}

def main():
    parser = argparse.ArgumentParser(description="Sarvam Document OCR")
    parser.add_argument("file", nargs="?", default=None, help="Document (.pdf,.png,.jpg,.zip)")
    parser.add_argument("--lang", default="en-IN", choices=LANGS)
    parser.add_argument("--format", default="md", choices=["md","html"])
    parser.add_argument("--list-languages", action="store_true")
    args = parser.parse_args()

    if args.list_languages:
        print(json.dumps({"languages": LANGS}))
        return
    if not args.file:
        parser.print_help()
        sys.exit(1)
    if not os.path.exists(args.file):
        print(json.dumps({"ok": False, "error": f"File not found: {args.file}"}))
        sys.exit(1)

    ext = os.path.splitext(args.file)[1].lower()
    if ext not in VALID_EXTS:
        print(json.dumps({"ok": False, "error": f"Unsupported format: {ext}. Use .pdf, .png, .jpg, .zip"}))
        sys.exit(1)

    try:
        from sarvamai import SarvamAI
    except ImportError:
        print(json.dumps({"ok": False, "error": "sarvamai SDK not installed. Run: uv pip install sarvamai"}))
        sys.exit(1)

    client = SarvamAI(api_subscription_key=API_KEY)

    job = client.document_intelligence.create_job(language=args.lang, output_format=args.format)
    print(json.dumps({"status": "created", "job_id": job.job_id}))

    job.upload_file(args.file)
    print(json.dumps({"status": "uploaded", "job_id": job.job_id}))

    job.start()
    print(json.dumps({"status": "processing", "job_id": job.job_id}))

    status = job.wait_until_complete()
    state = status.job_state
    metrics = job.get_page_metrics()

    if state not in ("Completed", "PartiallyCompleted"):
        print(json.dumps({"ok": False, "error": f"Job {state}", "pages": metrics}))
        sys.exit(1)

    # Download ZIP and extract to output file
    zip_path = os.path.join(os.path.dirname(os.path.abspath(args.file)) or ".", f"ocr_{os.path.splitext(os.path.basename(args.file))[0]}.zip")
    job.download_output(zip_path)

    # Extract the actual content file
    base = os.path.splitext(os.path.basename(args.file))[0]
    out_path = os.path.join(os.path.dirname(os.path.abspath(args.file)) or ".", f"ocr_{base}.{args.format}")

    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.endswith(f".{args.format}"):
                content = z.read(name).decode("utf-8", errors="replace")
                with open(out_path, "w") as f:
                    f.write(content)
                break

    # Clean up zip
    os.remove(zip_path)

    print(json.dumps({
        "ok": True, "status": "done", "state": state,
        "pages": metrics, "output": os.path.abspath(out_path),
        "preview": content[:500]
    }))

if __name__ == "__main__":
    main()
