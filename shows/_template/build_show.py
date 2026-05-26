#!/usr/bin/env python3
"""
build_show.py — WOLD-PM Special Hour Builder Template
Usage: copy this to your show folder and edit the config section.
"""

import random
from pathlib import Path

# ----- CONFIG — edit these for each show -----

SHOW_NAME    = "My Special Hour"         # Display name
SHOW_DIR     = Path(__file__).parent     # Folder this script lives in
OUTPUT_FILE  = SHOW_DIR / "show.js"      # Output JS playlist
JS_VAR_NAME  = "specialShow"             # JS variable name in output

# Paths relative to web root (how the browser will load them)
INTRO_FILE   = "bits/show_intro.mp3"     # Announcement before show
OUTRO_FILE   = "bits/back_to_regular.mp3"  # Sign-off after show

# Shuffle the tracks?
SHUFFLE      = True

# ----- END CONFIG -----

music_tracks = sorted(SHOW_DIR.glob("*.mp3"))

if not music_tracks:
    print("No MP3 files found in show folder.")
    raise SystemExit(1)

if SHUFFLE:
    random.shuffle(music_tracks)

playlist = []

# Intro announcement
playlist.append({"title": f"~ {SHOW_NAME} ~", "file": INTRO_FILE})

# Music tracks
for track in music_tracks:
    title = track.stem.replace("_", " ").replace("-", " - ")
    playlist.append({
        "title": title,
        "file": f"shows/{SHOW_DIR.name}/{track.name}"
    })

# Outro announcement
playlist.append({"title": "~ Back to Regular Programming ~", "file": OUTRO_FILE})

# Write JS
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f"const {JS_VAR_NAME} = [\n")
    for item in playlist:
        f.write(f'  {{ title: "{item["title"]}", file: "{item["file"]}" }},\n')
    f.write("];\n")

print(f"Show playlist written: {OUTPUT_FILE}")
print(f"Total tracks: {len(music_tracks)} + intro + outro = {len(playlist)} entries")
