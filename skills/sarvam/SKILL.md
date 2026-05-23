---
name: sarvam
description: Sarvam AI TTS and STT. Text-to-speech with 30+ Indian voices, speech recognition in 23 languages.
version: 1.1.0
author: community
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [tts, stt, speech, voice, indian-languages]
---

# Sarvam AI — TTS & STT

TTS (Bulbul v3) and STT (Saaras v3) for Indian languages. TTS is wired as a native tool for voice bubbles. STT transcribes voice messages automatically.

## TTS (Bulbul v3)

Native tool — use `/speak` or ask the agent to speak.

```bash
python3 skills/sarvam/scripts/tts.py "Hello" --speaker shubh --lang en-IN
python3 skills/sarvam/scripts/tts.py --list-speakers
python3 skills/sarvam/scripts/tts.py --list-languages
```

## STT (Saaras v3)

Native tool — voice messages auto-transcribe via Saaras.

```bash
python3 skills/sarvam/scripts/stt.py audio.wav --mode translate
python3 skills/sarvam/scripts/stt.py --list-modes
```

## Speakers

shubh (default), aditya, ritu, priya, neha, rahul, pooja, rohan, simran, kavya, amit, dev, ishita, shreya, ratan, varun, manan, sumit, roopa, kabir, aayan, ashutosh, advait, anand, tanya, tarun, sunny, mani, gokul, vijay, shruti, suhani, mohit, kavitha, rehan, soham, rupali

## STT Modes

- `transcribe` — original language script
- `translate` — speech to English
- `verbatim` — exact word-for-word
- `translit` — romanized
- `codemix` — mixed script
