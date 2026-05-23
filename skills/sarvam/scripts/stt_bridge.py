#!/usr/bin/env python3
"""Bridge: Hermes STT → Sarvam Saaras v3.
Reads audio from input_path, writes transcription to {output_dir}/out.txt
"""
import json, os, sys, urllib.request

API_KEY = os.environ.get("SARVAM_API_KEY", "")
if not API_KEY:
    print(json.dumps({"ok": False, "error": "SARVAM_API_KEY not set"}), file=sys.stderr)
    sys.exit(1)

input_path = sys.argv[1]   # audio file
output_dir = sys.argv[2]   # output directory
model = sys.argv[3] if len(sys.argv) > 3 else "saaras:v3"
lang = sys.argv[4] if len(sys.argv) > 4 else ""

import mimetypes
mime_type = mimetypes.guess_type(input_path)[0] or "audio/wav"

boundary = "----sarvamsttbridge"
body = []
for field, value in [("model", "saaras:v3"), ("mode", "transcribe")]:
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="{field}"'.encode())
    body.append(b"")
    body.append(value.encode())
if lang:
    body.append(f"--{boundary}".encode())
    body.append('Content-Disposition: form-data; name="language_code"'.encode())
    body.append(b"")
    body.append(lang.encode())
body.append(f"--{boundary}".encode())
body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(input_path)}"'.encode())
body.append(f"Content-Type: {mime_type}".encode())
body.append(b"")
with open(input_path, "rb") as f:
    body.append(f.read())
body.append(f"--{boundary}--".encode())
data = b"\r\n".join(body)

req = urllib.request.Request(
    "https://api.sarvam.ai/speech-to-text",
    data=data,
    headers={
        "api-subscription-key": API_KEY,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    },
)
resp = urllib.request.urlopen(req, timeout=120)
result = json.loads(resp.read())
transcript = result.get("transcript", "")

os.makedirs(output_dir, exist_ok=True)
out_path = os.path.join(output_dir, "out.txt")
with open(out_path, "w") as f:
    f.write(transcript)

print(json.dumps({"ok": True, "transcript": transcript}))
