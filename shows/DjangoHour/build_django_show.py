#!/usr/bin/env python3
"""
build_django_show.py — WOLD-PM Django Reinhardt Special Hour Builder
Splits 75 tracks into volumes of MAX_TRACKS each.
"""

import random
from pathlib import Path

SHOW_NAME   = "Django Reinhardt Special"
SHOW_DIR    = Path(__file__).parent
JS_VAR_BASE = "djangoShow"
INTRO_FILE  = "bits/django_intro.mp3"
OUTRO_FILE  = "bits/back_to_regular.mp3"
SHUFFLE     = True
MAX_TRACKS  = 30

music_tracks = sorted(SHOW_DIR.glob("*.mp3"))

if not music_tracks:
    print("No MP3 files found.")
    raise SystemExit(1)

if SHUFFLE:
    random.shuffle(music_tracks)

# Remove old show JS files before regenerating
for old in SHOW_DIR.glob("*_show*.js"):
    old.unlink()
for old in SHOW_DIR.glob("show*.js"):
    old.unlink()

volumes = [music_tracks[i:i+MAX_TRACKS] for i in range(0, len(music_tracks), MAX_TRACKS)]

for vol_num, vol_tracks in enumerate(volumes, start=1):
    vol_suffix = f" Vol. {vol_num}" if len(volumes) > 1 else ""
    js_var = f"{JS_VAR_BASE}{vol_num}" if len(volumes) > 1 else JS_VAR_BASE
    output_file = SHOW_DIR / (f"show_vol{vol_num}.js" if len(volumes) > 1 else "show.js")

    playlist = []
    playlist.append({"title": f"~ {SHOW_NAME}{vol_suffix} ~", "file": INTRO_FILE})

    for track in vol_tracks:
        title = track.stem.replace("_", " ").replace("-", " - ")
        playlist.append({
            "title": title,
            "file": f"shows/{SHOW_DIR.name}/{track.name}"
        })

    playlist.append({"title": "~ Back to Regular Programming ~", "file": OUTRO_FILE})

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"const {js_var} = [\n")
        for item in playlist:
            f.write(f'  {{ title: "{item["title"]}", file: "{item["file"]}" }},\n')
        f.write("];\n")

    print(f"  Vol {vol_num}: {output_file.name} — {len(vol_tracks)} tracks + intro/outro = {len(playlist)} entries")

print(f"\nDone. {len(volumes)} volume(s) for '{SHOW_NAME}'.")
