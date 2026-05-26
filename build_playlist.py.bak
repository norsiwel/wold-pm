#!/usr/bin/env python3
"""
WOLD-PM Playlist Generator
Builds the tracks[] array for index.html from the music/ folder.
Inserts station breaks (ad, newsflash, station ID) every ~12 songs (approx hourly).
Usage: python3 build_playlist.py
"""

import os
import re

MUSIC_DIR = "music"
ARCHIVE_BASE = "https://archive.org/download/wold-pm-music"

# Station break files — update filenames when you have them
BREAKS = [
    {"title": "~ WOLD-PM Station ID ~",       "file": "music/station_id.mp3"},
    {"title": "~ WOLD-PM Newsflash ~",         "file": "music/newsflash.mp3"},
    {"title": "~ WOLD-PM Advertisement ~",     "file": "music/ad.mp3"},
]

BREAK_INTERVAL = 12  # Insert a break every N music tracks

def clean_title(filename):
    """Turn filename into a display title."""
    name = os.path.splitext(filename)[0]
    # Remove leading track number like "01 " or "01_"
    name = re.sub(r'^\d+[\s_\-\.]+', '', name)
    return name.strip()

def get_music_tracks():
    """Get all numbered MP3s in sorted order, skip break files and old-name files."""
    skip = {'station_id.mp3', 'newsflash.mp3', 'ad.mp3',
            'dont_get_around.mp3', 'flying_home.mp3',
            'moonlight_serenade.mp3', 'sentimental_journey.mp3',
            'tuxedo_junction.mp3'}
    files = []
    for f in sorted(os.listdir(MUSIC_DIR)):
        if f.lower().endswith('.mp3') and f not in skip:
            files.append(f)
    return files

def build_tracks_js(use_archive=False):
    """Build the JS tracks array string."""
    music = get_music_tracks()
    lines = []
    break_idx = 0

    for i, f in enumerate(music):
        # Insert a break every BREAK_INTERVAL tracks
        if i > 0 and i % BREAK_INTERVAL == 0:
            b = BREAKS[break_idx % len(BREAKS)]
            if use_archive:
                url = f"{ARCHIVE_BASE}/{b['file'].replace('music/', '')}"
            else:
                url = b['file']
            lines.append(f'  {{ title: "{b["title"]}", file: "{url}" }}')
            break_idx += 1

        title = clean_title(f)
        if use_archive:
            url = f"{ARCHIVE_BASE}/{f}"
        else:
            url = f"music/{f}"
        # Escape any quotes in title
        title = title.replace('"', '\\"')
        lines.append(f'  {{ title: "{title}", file: "{url}" }}')

    return "const tracks = [\n" + ",\n".join(lines) + "\n];"

if __name__ == "__main__":
    print("=== LOCAL paths (for testing) ===")
    js_local = build_tracks_js(use_archive=False)
    with open("tracks_local.js", "w") as f:
        f.write(js_local)
    print(f"Written to tracks_local.js")

    print("\n=== ARCHIVE.ORG paths (for production) ===")
    js_archive = build_tracks_js(use_archive=True)
    with open("tracks_archive.js", "w") as f:
        f.write(js_archive)
    print(f"Written to tracks_archive.js")

    # Count stats
    music = get_music_tracks()
    total = len(music) + (len(music) // BREAK_INTERVAL)
    print(f"\nStats: {len(music)} music tracks + {len(music) // BREAK_INTERVAL} breaks = {total} total entries")
    print(f"Approx loop length: ~{len(music) * 3} minutes ({len(music) * 3 // 60} hours)")
