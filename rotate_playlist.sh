#!/bin/bash
# rotate_playlist.sh - Regenerate and push a fresh WOLD-PM playlist rotation

cd "$(dirname "$0")" || exit 1

echo "Generating new playlist..."
python3 build_playlist_updated.py || { echo "Playlist generation failed."; exit 1; }

echo "Syncing bits to R2..."
for f in bits/*.mp3; do
  npx wrangler r2 object put "wold-pm/$f" --file="$f" --remote 2>&1 | grep -E "complete|ERROR|404"
done

echo "Pushing to station..."
git add tracks_local.js
git commit -m "chore: new playlist rotation"
git push

echo "Done! New rotation is live."
