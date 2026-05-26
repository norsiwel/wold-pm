#!/usr/bin/env python3
"""
build_show.py — WOLD-PM Special Hour Builder Template
Usage: copy this to your show folder and edit the config section.
Automatically splits into multiple volumes if track count exceeds MAX_TRACKS.
"""

import random
from pathlib import Path

# ----- CONFIG — edit these for each show -----

SHOW_NAME    = "My Special Hour"         # Display name
SHOW_DIR     = Path(__file__).parent     # Folder this script lives in
JS_VAR_BASE  = "specialShow"            # JS variable base name (vol2 = specialShow2 etc)

# Paths relative to web root (how the browser will load them)
INTRO_FILE   = "bits/show_intro.mp3"
OUTRO_FILE   = "bits/back_to_regular.mp3"

# All audio served from Cloudflare R2
R2_BASE_URL  = "https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev"

SHUFFLE      = True
MAX_TRACKS   = 30                        # Max music tracks per volume

# ----- END CONFIG -----

music_tracks = sorted(SHOW_DIR.glob("*.mp3"))

if not music_tracks:
    print("No MP3 files found in show folder.")
    raise SystemExit(1)

if SHUFFLE:
    random.shuffle(music_tracks)

# Split into volumes of MAX_TRACKS
volumes = [music_tracks[i:i+MAX_TRACKS] for i in range(0, len(music_tracks), MAX_TRACKS)]

for vol_num, vol_tracks in enumerate(volumes, start=1):
    vol_suffix = f" Vol. {vol_num}" if len(volumes) > 1 else ""
    js_var = f"{JS_VAR_BASE}{vol_num}" if len(volumes) > 1 else JS_VAR_BASE
    output_file = SHOW_DIR / (f"show_vol{vol_num}.js" if len(volumes) > 1 else "show.js")

    playlist = []
    playlist.append({"title": f"~ {SHOW_NAME}{vol_suffix} ~", "file": f"{R2_BASE_URL}/{INTRO_FILE}"})

    for track in vol_tracks:
        title = track.stem.replace("_", " ").replace("-", " - ")
        playlist.append({
            "title": title,
            "file": f"{R2_BASE_URL}/shows/{SHOW_DIR.name}/{track.name}"
        })

    playlist.append({"title": "~ Back to Regular Programming ~", "file": f"{R2_BASE_URL}/{OUTRO_FILE}"})

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"const {js_var} = [\n")
        for item in playlist:
            f.write(f'  {{ title: "{item["title"]}", file: "{item["file"]}" }},\n')
        f.write("];\n")

    print(f"  Vol {vol_num}: {output_file.name} — {len(vol_tracks)} tracks + intro/outro = {len(playlist)} entries")

print(f"\nDone. {len(volumes)} volume(s) written for '{SHOW_NAME}'.")
