#!/bin/bash
# rotate_playlist.sh - Regenerate and push a fresh WOLD-PM playlist rotation
#
# v002 (2026-07-01): Fixed missing shows/ upload step. The old version only
# uploaded bits/*.mp3 to R2 — every special-show music track (everything
# past the intro bit) was never on the bucket at all, causing the
# "plays intro, then fails on track 2+" bug documented in
# shows/SHOWS_STATUS.md. Confirmed via direct wrangler r2 object get:
# "The specified key does not exist." Old version archived at
# archive/rotate_playlist.sh.bak_2026-07-01_1858.

cd "$(dirname "$0")" || exit 1

MANIFEST="archive/.r2_shows_uploaded.txt"
touch "$MANIFEST"

echo "Generating new playlist..."
python3 build_playlist_updated.py || { echo "Playlist generation failed."; exit 1; }

echo "Syncing bits to R2..."
for f in bits/*.mp3; do
  npx wrangler r2 object put "wold-pm/$f" --file="$f" --remote 2>&1 | grep -E "complete|ERROR|404"
done

echo "Syncing show tracks to R2 (skipping already-uploaded)..."
show_count=0
show_skip=0
while IFS= read -r -d '' f; do
  if grep -qxF "$f" "$MANIFEST"; then
    show_skip=$((show_skip + 1))
    continue
  fi
  result=$(npx wrangler r2 object put "wold-pm/$f" --file="$f" --remote 2>&1)
  echo "$result" | grep -E "complete|ERROR|404"
  if echo "$result" | grep -q "ERROR"; then
    echo "  FAILED: $f (not added to manifest, will retry next run)"
  else
    echo "$f" >> "$MANIFEST"
    show_count=$((show_count + 1))
  fi
done < <(find shows -iname "*.mp3" -print0)
echo "  Uploaded: $show_count new, skipped: $show_skip already on R2"

echo "Pushing to station..."
git add tracks_local.js
git commit -m "chore: new playlist rotation"
git push

echo "Done! New rotation is live."
