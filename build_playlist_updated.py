#!/usr/bin/env python3

import sys
import re
import random
import urllib.parse
from pathlib import Path

def r2_url(base, path):
    """Build R2 URL with spaces properly encoded."""
    return base + "/" + urllib.parse.quote(str(path).replace("\\", "/"), safe="/")

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
    print(f"\n  pip install {' '.join(missing)}\n")
    sys.exit(1)

# ----- Configuration -----

MUSIC_DIR = Path("music")
BITS_DIR  = Path("bits")
SHOWS_DIR = Path("shows")
OUTPUT_FILE = Path("tracks_local.js")

# All audio is served from Cloudflare R2 — never local paths
R2_BASE_URL = "https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev"

SONGS_BEFORE_BIT_MIN = 3
SONGS_BEFORE_BIT_MAX = 6
TARGET_ID_INTERVAL   = 3600  # seconds (~1 hour)

# ----- Helpers -----

def get_duration(file_path):
    try:
        return MP3(file_path).info.length
    except Exception:
        return 180

def title_from_filename(path):
    return path.stem.replace("_", " ")

# ----- Load Special Shows -----
# Any folder under shows/ that contains a show.js is a schedulable show.
# Reads the JS file and parses the track list out of it.

def load_show(show_js_path):
    """Parse a show.js file and return list of {title, file} dicts."""
    text = show_js_path.read_text(encoding="utf-8")
    entries = re.findall(
        r'\{\s*title:\s*"([^"]+)",\s*file:\s*"([^"]+)"\s*\}', text
    )
    return [{"title": t, "file": f} for t, f in entries]

special_shows = []
if SHOWS_DIR.exists():
    for show_folder in sorted(SHOWS_DIR.iterdir()):
        if show_folder.name.startswith("_"):
            continue  # skip _template and other meta folders

        # Collect show JS files — single show.js or split show_vol1.js, show_vol2.js etc
        # Skip _pending and other underscore subfolders
        js_files = sorted(f for f in show_folder.glob("show_vol*.js") 
                         if "_pending" not in str(f))
        if not js_files:
            single = show_folder / "show.js"
            if single.exists():
                js_files = [single]

        for js_file in js_files:
            vol_label = js_file.stem.replace("show", "").replace("_", " ").strip()
            name = f"{show_folder.name}{' ' + vol_label if vol_label else ''}"
            tracks = load_show(js_file)
            if tracks:
                special_shows.append({"name": name, "tracks": tracks})
                print(f"  Loaded: {name} ({len(tracks)} entries)")

# ----- Load Regular Music -----

music_tracks = list(MUSIC_DIR.rglob("*.mp3"))
bit_tracks   = list(BITS_DIR.rglob("*.mp3"))

if not music_tracks:
    print("No music files found.")
    sys.exit(1)

if not bit_tracks:
    print("No bit files found.")
    sys.exit(1)

station_ids = [b for b in bit_tracks if "station_id" in b.name.lower()]

# Paired bits — must stay together, handled by special shows system
paired_names = {"armstrong_intro", "armstrong_outro",
                "django_intro", "folk_intro", "folk_outro",
                "bird_intro", "back_to_regular"}
paired_bits  = [b for b in bit_tracks if b.stem in paired_names]

# Standalone bits — random distribution, one at a time
standalone_bits = [b for b in bit_tracks
                   if b not in station_ids and b not in paired_bits]

# Friendly titles for standalone bits
STANDALONE_TITLES = {
    "Travel-with-Arlo":        "~ Arlo's Traffic Report ~",
    "WOLD-weather-by GTFbeer": "~ WOLD Weather — GTF Beer ~",
    "EveningNews-CrownFTL":   "~ Evening News with Crown FTL ~",
    "PSA-recycling":           "~ PSA: Recycling ~",
    "Phoenix-Atomic-cycles":   "~ Phoenix Atomic Motorcycles ~",
    "mannavator_ad":           "~ mannavator ad ~",
    "Illumination-Station-AD": "~ Illumination Station ~",
    "unearthly_newsflash":     "~ unearthly newsflash ~",
}

other_bits = standalone_bits

random.shuffle(music_tracks)
random.shuffle(other_bits)
random.shuffle(station_ids)

# ----- Build Regular Playlist -----

playlist = []
music_index = 0
bit_index   = 0
id_index    = 0
elapsed_since_id = 0

while music_index < len(music_tracks):

    block_size = random.randint(SONGS_BEFORE_BIT_MIN, SONGS_BEFORE_BIT_MAX)

    for _ in range(block_size):
        if music_index >= len(music_tracks):
            break
        track = music_tracks[music_index]
        playlist.append({
            "title": title_from_filename(track),
            "file": r2_url(R2_BASE_URL, track)
        })
        elapsed_since_id += get_duration(track)
        music_index += 1

    if elapsed_since_id >= TARGET_ID_INTERVAL and station_ids:
        sid = station_ids[id_index % len(station_ids)]
        playlist.append({
            "title": "~ WOLD-PM ~",
            "file": r2_url(R2_BASE_URL, sid)
        })
        elapsed_since_id = 0
        id_index += 1
        continue

    if other_bits:
        bit = other_bits[bit_index % len(other_bits)]
        bit_title = STANDALONE_TITLES.get(bit.stem,
                    f"~ {title_from_filename(bit)} ~")
        playlist.append({
            "title": bit_title,
            "file": r2_url(R2_BASE_URL, bit)
        })
        bit_index += 1

# ----- Insert Special Shows at Midpoint -----
# Each show is inserted at the halfway point of the regular playlist,
# offset slightly so multiple shows don't stack on top of each other.

if special_shows:
    # Space shows evenly through the final total length
    total_show_tracks = sum(len(s["tracks"]) for s in special_shows)
    total_final = len(playlist) + total_show_tracks
    for i, show in enumerate(special_shows):
        spacing = total_final // (len(special_shows) + 1)
        insert_at = spacing * (i + 1)
        insert_at = max(1, min(insert_at, len(playlist) - 1))
        for entry in reversed(show["tracks"]):
            playlist.insert(insert_at, entry)
        print(f"  Inserted '{show['name']}' at position {insert_at} "
              f"({insert_at / (len(playlist) / 100):.0f}% through rotation)")

# ----- Write Output -----

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("const tracks = [\n")
    for item in playlist:
        title = item["title"].replace('"', '\\"')
        fpath = item["file"].replace('"', '\\"')
        f.write(f'  {{ title: "{title}", file: "{fpath}" }},\n')
    f.write("];\n")

print(f"\nGenerated {OUTPUT_FILE}")
print(f"Regular tracks:  {len(music_tracks)}")
print(f"Special shows:   {len(special_shows)}")
print(f"Total scheduled: {len(playlist)}")
