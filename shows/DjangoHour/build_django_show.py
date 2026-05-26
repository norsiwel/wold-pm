#!/usr/bin/env python3
"""
build_django_show.py
Builds the Django Hour show playlist as a JS file.
Structure: django_intro -> shuffled Django tracks -> back_to_regular
"""

import random
from pathlib import Path

SHOW_DIR = Path(__file__).parent
BITS_DIR = Path(__file__).parent.parent.parent / "WOLD-PM.com/bits"
OUTPUT_FILE = SHOW_DIR / "django_show.js"

# Resolve bits relative to the web root
INTRO = "bits/django_intro.mp3"
OUTRO = "bits/back_to_regular.mp3"

# Load all Django mp3s from this folder (exclude this script and the output)
django_tracks = sorted(SHOW_DIR.glob("*.mp3"))
random.shuffle(django_tracks)

playlist = []

# Intro announcement
playlist.append({"title": "~ Django Reinhardt Special ~", "file": INTRO})

# All Django tracks
for track in django_tracks:
    title = track.stem.replace("_", " ").replace("-", " - ")
    playlist.append({
        "title": title,
        "file": f"shows/DjangoHour/{track.name}"
    })

# Outro announcement
playlist.append({"title": "~ Back to Regular Programming ~", "file": OUTRO})

# Write JS
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("const djangoShow = [\n")
    for item in playlist:
        f.write(f'  {{ title: "{item["title"]}", file: "{item["file"]}" }},\n')
    f.write("];\n")

print(f"Django Hour playlist written: {OUTPUT_FILE}")
print(f"Total tracks: {len(django_tracks)} + intro + outro = {len(playlist)} entries")
