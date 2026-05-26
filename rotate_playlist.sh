#!/bin/bash
# rotate_playlist.sh - Regenerate and push a fresh WOLD-PM playlist rotation

cd "$(dirname "$0")" || exit 1

echo "Generating new playlist..."
python3 build_playlist_updated.py || { echo "Playlist generation failed."; exit 1; }

echo "Pushing to station..."
git add tracks_local.js
git commit -m "chore: new playlist rotation"
git push

echo "Done! New rotation is live."
