#!/bin/bash
# upload_to_r2.sh — Batch upload all WOLD-PM audio to Cloudflare R2
# Runs 5 parallel uploads at a time for speed

BUCKET="wold-pm"
BASE="/home/ron/WOLD-PM.com"
LOG="$BASE/logs/r2_upload.log"

echo "Starting R2 upload $(date)" | tee "$LOG"

upload_file() {
  local f="$1"
  local result
  result=$(npx wrangler r2 object put "$BUCKET/$f" --file="$BASE/$f" 2>&1)
  if echo "$result" | grep -q "Success\|Uploaded\|Created"; then
    echo "OK: $f" | tee -a "$LOG"
  else
    echo "ERR: $f — $result" | tee -a "$LOG"
  fi
}

export -f upload_file
export BUCKET BASE LOG

cd "$BASE"
TOTAL=$(find music bits shows/DjangoHour -name "*.mp3" | wc -l)
echo "Found $TOTAL files to upload..." | tee -a "$LOG"

find music bits shows/DjangoHour -name "*.mp3" | \
  xargs -P 5 -I{} bash -c 'upload_file "$@"' _ {}

echo "Done $(date)" | tee -a "$LOG"
echo "Check $LOG for any errors."
