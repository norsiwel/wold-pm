#!/usr/bin/env python3
"""
WOLD-PM Music Fetcher
Downloads public domain jazz tracks from Archive.org
Targets: Django Reinhardt, Louis Armstrong, and Fallout 4 era music
Run: python3 fetch_music.py
"""

import os
import urllib.request
import json
import time

MUSIC_DIR = "/run/media/ron/T7/WOLD-PM.com/music"

# Search targets
SEARCHES = [
    "django reinhardt hot club",
    "louis armstrong 1920s 1930s",
    "ink spots",
    "billie holiday",
    "vera lynn",
    "andrews sisters",
    "nat king cole 1940s",
    "ella fitzgerald 1940s",
]

# Fallout 4 specific tracks (public domain era)
FALLOUT_TRACKS = [
    "Atom Bomb Baby - The Five Stars",
    "Butcher Pete - Roy Brown",
    "Good Neighbor - Magnolia",
    "I Don't Want to Set the World on Fire - Ink Spots",
    "Maybe - The Ink Spots",
    "It's All Over But the Crying - Ink Spots",
    "Civilization - Danny Kaye",
    "Way Back Home - Bob Crosby",
    "Uranium Fever - Elton Britt",
    "Rocket 69 - Todd Rhodes",
    "Nuclear Device - The Stranglers",
]

def search_archive(query, max_results=5):
    """Search Archive.org for public domain audio."""
    url = f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(query)}+mediatype:audio&fl=identifier,title,creator&rows={max_results}&output=json"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            return data.get('response', {}).get('docs', [])
    except Exception as e:
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    print("WOLD-PM Music Fetcher")
    print("Run this tomorrow to search and download new tracks.")
    print("\nFallout 4 era tracks to look for:")
    for t in FALLOUT_TRACKS:
        print(f"  - {t}")
    print("\nSearch targets queued:")
    for s in SEARCHES:
        print(f"  - {s}")
    print("\nReady to run full fetch tomorrow.")
