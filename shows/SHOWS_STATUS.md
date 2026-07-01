# WOLD-PM Special Shows — Known Issues & Fix Plan

## Current Status
All special shows moved to `shows/_inactive/` pending QC fixes.
Regular rotation running clean — 96 tracks, ~4.2 hours.

## Symptom
Shows play intro announcement, then one track, then jump to outro and back to rotation.
Tracks 2+ are silently failing — error handler skips to end of show.

## Root Cause (suspected)
Audio URLs in show JS files may have encoding issues or path mismatches with R2.
The error handler retries twice then skips — happens too fast for slow R2 loads on first track,
then bails out on subsequent tracks entirely.

## Fix Plan

### Step 1 — Build show_validator.py
A script that reads each show's JS file, pings every R2 URL with a HEAD request,
and reports pass/fail for every track before the playlist builder runs.

```python
# Pseudocode
for each show in shows/_inactive/:
    for each track URL in show.js:
        HEAD request to R2 URL
        if 200: pass
        if 404: fail — report filename
```

### Step 2 — Fix any 404s
Re-upload missing files to R2 with correct paths/encoding.

### Step 3 — QC each show with the local player
Use http://localhost:8080/django_test.html (or equivalent) to play through
each show end to end before re-enabling.

### Step 4 — Move shows back to shows/ and re-enable
Once validated, move from `shows/_inactive/` back to `shows/` and run rotate_playlist.sh.

### Step 5 — Build central controller
Integrate validator into rotate_playlist.sh so it runs automatically —
only shows that pass all URL checks get inserted into the rotation.

## Shows Pending Fix
| Show | Tracks | Issue |
|------|--------|-------|
| DjangoHour | 75 (3 vols) | Tracks 2+ failing silently |
| FolkInterlude | 6 | Tracks 2+ failing silently |
| ArmstrongVol1 | 15 | FLACs not converted yet |
| ArmstrongVol2 | 14 | FLACs not converted yet |

## Announcer Bits (all in R2, confirmed working)
- bits/django_intro.mp3 — Ryan
- bits/back_to_regular.mp3 — Ryan  
- bits/folk_intro.mp3 — HFC
- bits/folk_outro.mp3 — HFC
- bits/armstrong_intro.mp3 — Onyx
- bits/armstrong_outro.mp3 — Onyx
- bits/bird_intro.mp3 — Onyx (reserved for Charlie Parker)
