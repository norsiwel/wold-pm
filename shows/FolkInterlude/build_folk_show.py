#!/usr/bin/env python3
"""
build_folk_show.py — WOLD-PM Folk Interlude Builder
Lead Belly, Woody Guthrie, Cisco Houston — 6 tracks, no shuffle (keep original order)
"""

import urllib.parse
from pathlib import Path

def r2_url(base, path):
    """Build R2 URL with spaces properly encoded."""
    return base + "/" + urllib.parse.quote(path, safe="/")

SHOW_NAME   = "Folk Interlude"
SHOW_DIR    = Path(__file__).parent
JS_VAR_BASE = "folkInterlude"
INTRO_FILE  = "bits/folk_intro.mp3"
OUTRO_FILE  = "bits/folk_outro.mp3"
R2_BASE_URL = "https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev"
SHUFFLE     = False

music_tracks = sorted(SHOW_DIR.glob("*.mp3"))

if not music_tracks:
    print("No MP3 files found.")
    raise SystemExit(1)

playlist = []
playlist.append({"title": f"~ {SHOW_NAME} ~", "file": r2_url(R2_BASE_URL, INTRO_FILE)})

for track in music_tracks:
    title = track.stem.replace("_", " ")
    playlist.append({
        "title": title,
        "file": r2_url(R2_BASE_URL, f"shows/{SHOW_DIR.name}/{track.name}")
    })

playlist.append({"title": "~ Onward Through the Fog ~", "file": r2_url(R2_BASE_URL, OUTRO_FILE)})

output_file = SHOW_DIR / "show.js"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"const {JS_VAR_BASE} = [\n")
    for item in playlist:
        title = item["title"].replace('"', '\\"')
        fpath = item["file"].replace('"', '\\"')
        f.write(f'  {{ title: "{title}", file: "{fpath}" }},\n')
    f.write("];\n")

print(f"Folk Interlude show written: {output_file}")
print(f"Total: {len(music_tracks)} tracks + intro + outro = {len(playlist)} entries")
