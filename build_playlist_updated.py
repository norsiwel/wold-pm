#!/usr/bin/env python3

import sys
import random
from pathlib import Path

# ----- Dependency Check -----
missing = []

try:
    from mutagen.mp3 import MP3
except ImportError:
    missing.append("mutagen")

if missing:
    print("\nMissing required Python libraries:\n")
    for lib in missing:
        print(f"  - {lib}")

    print("\nInstall them with:\n")
    print(f"  pip install {' '.join(missing)}\n")
    sys.exit(1)

# ----- Configuration -----

MUSIC_DIR = Path("music")
BITS_DIR = Path("bits")
OUTPUT_FILE = Path("tracks_local.js")

SONGS_BEFORE_BIT_MIN = 3
SONGS_BEFORE_BIT_MAX = 6

TARGET_ID_INTERVAL = 3600  # seconds (~1 hour)

# ----- Helpers -----

def get_duration(file_path):
    try:
        return MP3(file_path).info.length
    except Exception:
        return 180


def title_from_filename(path):
    return path.stem.replace("_", " ")


# ----- Load Files -----

music_tracks = list(MUSIC_DIR.rglob("*.mp3"))
bit_tracks = list(BITS_DIR.rglob("*.mp3"))

if not music_tracks:
    print("No music files found.")
    sys.exit(1)

if not bit_tracks:
    print("No bit files found.")
    sys.exit(1)

station_ids = [b for b in bit_tracks if "station_id" in b.name.lower()]
other_bits = [b for b in bit_tracks if b not in station_ids]

random.shuffle(music_tracks)
random.shuffle(other_bits)
random.shuffle(station_ids)

playlist = []

music_index = 0
bit_index = 0
id_index = 0

elapsed_since_id = 0

while music_index < len(music_tracks):

    block_size = random.randint(
        SONGS_BEFORE_BIT_MIN,
        SONGS_BEFORE_BIT_MAX
    )

    for _ in range(block_size):

        if music_index >= len(music_tracks):
            break

        track = music_tracks[music_index]

        playlist.append({
            "title": title_from_filename(track),
            "file": str(track).replace("\\", "/")
        })

        elapsed_since_id += get_duration(track)

        music_index += 1

    if elapsed_since_id >= TARGET_ID_INTERVAL and station_ids:

        sid = station_ids[id_index % len(station_ids)]

        playlist.append({
            "title": "~ WOLD-PM ~",
            "file": str(sid).replace("\\", "/")
        })

        elapsed_since_id = 0
        id_index += 1

        continue

    if other_bits:

        bit = other_bits[bit_index % len(other_bits)]

        playlist.append({
            "title": f"~ {title_from_filename(bit)} ~",
            "file": str(bit).replace("\\", "/")
        })

        bit_index += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write("const tracks = [\n")

    for item in playlist:
        f.write(
            f'  {{ title: "{item["title"]}", '
            f'file: "{item["file"]}" }},\n'
        )

    f.write("];\n")

print(f"Generated {OUTPUT_FILE}")
print(f"Tracks scheduled: {len(playlist)}")
