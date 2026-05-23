#!/usr/bin/env python3
"""Sarvam Bulbul TTS — convert text to speech."""
import argparse, json, os, sys, urllib.request

API_KEY = os.environ.get("SARVAM_API_KEY", "")
BASE = "https://api.sarvam.ai"

SPEAKERS = [
    "shubh", "aditya", "ritu", "priya", "neha", "rahul", "pooja", "rohan",
    "simran", "kavya", "amit", "dev", "ishita", "shreya", "ratan", "varun",
    "manan", "sumit", "roopa", "kabir", "aayan", "ashutosh", "advait", "anand",
    "tanya", "tarun", "sunny", "mani", "gokul", "vijay", "shruti", "suhani",
    "mohit", "kavitha", "rehan", "soham", "rupali"
]

LANGUAGES = {
    "hi-IN": "Hindi", "bn-IN": "Bengali", "ta-IN": "Tamil", "te-IN": "Telugu",
    "gu-IN": "Gujarati", "kn-IN": "Kannada", "ml-IN": "Malayalam",
    "mr-IN": "Marathi", "pa-IN": "Punjabi", "od-IN": "Odia", "en-IN": "English"
}

def main():
    parser = argparse.ArgumentParser(description="Sarvam Bulbul TTS")
    parser.add_argument("text", nargs="?", default=None, help="Text to convert to speech")
    parser.add_argument("--speaker", default="shubh", choices=SPEAKERS)
    parser.add_argument("--lang", default="en-IN", choices=list(LANGUAGES.keys()))
    parser.add_argument("--output", default="/tmp/sarvam_tts.wav")
    parser.add_argument("--pace", type=float, default=1.0)
    parser.add_argument("--list-speakers", action="store_true")
    parser.add_argument("--list-languages", action="store_true")
    args = parser.parse_args()

    if args.list_speakers:
        print(json.dumps({"speakers": SPEAKERS}))
        return
    if args.list_languages:
        print(json.dumps({"languages": LANGUAGES}))
        return
    if not args.text:
        parser.print_help()
        sys.exit(1)

    payload = json.dumps({
        "text": args.text,
        "target_language_code": args.lang,
        "model": "bulbul:v3",
        "speaker": args.speaker,
        "pace": args.pace,
    }).encode()

    req = urllib.request.Request(
        f"{BASE}/text-to-speech",
        data=payload,
        headers={
            "api-subscription-key": API_KEY,
            "Content-Type": "application/json",
        },
    )
    resp = urllib.request.urlopen(req, timeout=60)
    with open(args.output, "wb") as f:
        f.write(resp.read())
    print(json.dumps({"ok": True, "file": args.output, "speaker": args.speaker, "lang": args.lang}))

if __name__ == "__main__":
    main()
