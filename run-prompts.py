#!/usr/bin/env python3
"""Run test prompts against a voice sample using Gemini 3.1 Flash Lite."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

AUDIO_FILE = Path("2026-03-26/26_03_2026_16_08.flac")
PROMPTS_DIR = Path("test-prompts")
OUTPUT_DIR = Path("outputs")

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        print("Set GEMINI_API_KEY in .env first")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    print(f"Uploading {AUDIO_FILE}...")
    uploaded = client.files.upload(file=str(AUDIO_FILE))
    print(f"Uploaded: {uploaded.name}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    prompt_files = sorted(PROMPTS_DIR.glob("*.txt"))
    print(f"Found {len(prompt_files)} prompts\n")

    for pf in prompt_files:
        prompt_text = pf.read_text().strip()
        out_file = OUTPUT_DIR / f"{pf.stem}.md"
        print(f"Running: {pf.name}...")

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[prompt_text, uploaded],
        )

        out_file.write_text(f"# {pf.stem.replace('-', ' ').title()}\n\n{response.text}\n")
        print(f"  -> {out_file}")

    print("\nDone!")


if __name__ == "__main__":
    main()
