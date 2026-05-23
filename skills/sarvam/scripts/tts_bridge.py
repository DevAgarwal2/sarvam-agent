#!/usr/bin/env python3
"""Bridge: Hermes TTS → Sarvam Bulbul v3.
Reads text from {input_path}, decodes base64 audio from JSON, writes WAV to {output_path}.
"""
import base64, json, os, sys, urllib.request

API_KEY = os.environ.get("SARVAM_API_KEY", "")
if not API_KEY:
    print(json.dumps({"ok": False, "error": "SARVAM_API_KEY not set"}), file=sys.stderr)
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]
speaker = sys.argv[3] if len(sys.argv) > 3 else "shubh"
lang = sys.argv[4] if len(sys.argv) > 4 else "en-IN"

text = open(input_path).read().strip()
if not text:
    print(json.dumps({"ok": False, "error": "empty text"}), file=sys.stderr)
    sys.exit(1)

payload = json.dumps({
    "text": text[:2500],
    "target_language_code": lang,
    "model": "bulbul:v3",
    "speaker": speaker,
}).encode()

req = urllib.request.Request(
    "https://api.sarvam.ai/text-to-speech",
    data=payload,
    headers={
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json",
    },
)
resp = urllib.request.urlopen(req, timeout=60)
result = json.loads(resp.read())
audios = result.get("audios", [])

if not audios:
    print(json.dumps({"ok": False, "error": "no audio in response"}), file=sys.stderr)
    sys.exit(1)

audio_bytes = base64.b64decode(audios[0])
with open(output_path, "wb") as f:
    f.write(audio_bytes)

print(json.dumps({"ok": True, "output": output_path}))
