#!/usr/bin/env python3
"""Sarvam Saaras STT — speech to text with multiple modes."""
import argparse, json, os, sys, urllib.request, urllib.error

API_KEY = os.environ.get("SARVAM_API_KEY", "")
BASE = "https://api.sarvam.ai"

MODES = ["transcribe", "translate", "verbatim", "translit", "codemix"]

def main():
    parser = argparse.ArgumentParser(description="Sarvam Saaras STT")
    parser.add_argument("file", nargs="?", default=None, help="Audio file path (.wav, .mp3, etc.)")
    parser.add_argument("--mode", default="transcribe", choices=MODES)
    parser.add_argument("--lang", default=None, help="BCP-47 language code (auto-detect if not set)")
    parser.add_argument("--list-modes", action="store_true")
    args = parser.parse_args()

    if args.list_modes:
        print(json.dumps({"modes": MODES}))
        return
    if not args.file:
        parser.print_help()
        sys.exit(1)

    import mimetypes
    mime_type = mimetypes.guess_type(args.file)[0] or "audio/wav"

    boundary = "----sarvamformboundary"
    body = []
    for field, value in [("model", "saaras:v3"), ("mode", args.mode)]:
        body.append(f"--{boundary}".encode())
        body.append(f'Content-Disposition: form-data; name="{field}"'.encode())
        body.append(b"")
        body.append(value.encode())
    if args.lang:
        body.append(f"--{boundary}".encode())
        body.append(f'Content-Disposition: form-data; name="language_code"'.encode())
        body.append(b"")
        body.append(args.lang.encode())
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(args.file)}"'.encode())
    body.append(f"Content-Type: {mime_type}".encode())
    body.append(b"")
    with open(args.file, "rb") as f:
        body.append(f.read())
    body.append(f"--{boundary}--".encode())
    data = b"\r\n".join(body)

    req = urllib.request.Request(
        f"{BASE}/speech-to-text",
        data=data,
        headers={
            "api-subscription-key": API_KEY,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
