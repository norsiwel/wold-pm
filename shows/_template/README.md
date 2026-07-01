# WOLD-PM Special Hour Pipeline

Complete workflow for producing, testing, and airing a special programming hour.

---

## Pipeline Overview

```
1. Gather audio  →  2. Generate announcements  →  3. Build show  →  4. QC test  →  5. Wire to station
```

---

## Step 1 — Gather Audio

Place all MP3s for the show in a new folder under `shows/`:

```
shows/ArtistNameHour/
```

Extract from zip if needed:
```bash
unzip -j music/artist.zip "*.mp3" -d shows/ArtistNameHour/
```

---

## Step 2 — Generate Announcements with Piper TTS

**Voice:** `en_US-ryan-high` (best quality male, good for announcing)
**Location:** `/home/ron/PlaymakerStudio/voices/en_US-ryan-high.onnx`
**Volume boost:** `2.0` via ffmpeg (raw Piper output is quiet)

### Intro announcement:
```bash
echo "And now... a special music hour featuring ARTIST NAME." | \
  /home/ron/.local/bin/piper \
  --model /home/ron/PlaymakerStudio/voices/en_US-ryan-high.onnx \
  --output_file /tmp/intro_raw.wav

ffmpeg -y -i /tmp/intro_raw.wav -filter:a "volume=2.0" bits/show_intro.mp3
```

### Outro (already exists — reuse for all shows):
```
bits/back_to_regular.mp3
```
"And now... back to our regular programming. Here on W-O-L-D-PM. ... where what comes around, goes around."

### Tips for natural-sounding TTS:
- Use `...` for longer pauses
- Use `-` between letters for call signs: `W-O-L-D-PM`
- Use `.` after a phrase to force a breath before continuing
- Test with ffplay before committing: `ffplay -nodisp -autoexit bits/show_intro.mp3`

---

## Step 3 — Build the Show Playlist

Copy `shows/_template/build_show.py` to your show folder and edit the config section:

```python
SHOW_NAME    = "Django Reinhardt Special Hour"
JS_VAR_NAME  = "djangoShow"
INTRO_FILE   = "bits/django_intro.mp3"
OUTRO_FILE   = "bits/back_to_regular.mp3"
SHUFFLE      = True
```

Then run it:
```bash
cd shows/ArtistNameHour && python3 build_show.py
```

Output: `shows/ArtistNameHour/show.js`

---

## Step 4 — QC Test

Copy `shows/_template/qc_preview.html` to the web root and edit two lines:

```html
<script src="shows/ArtistNameHour/show.js"></script>
```
```javascript
const tracks = specialShow;  // match JS_VAR_NAME from build_show.py
```

Open in browser:
```
file:///home/ron/WOLD-PM.com/artist_test.html
```

**QC checklist:**
- [ ] Intro announcement plays and sounds natural
- [ ] Station call letters pronounced correctly (W-O-L-D-PM)
- [ ] First few music tracks load and play
- [ ] Spot check middle tracks
- [ ] Outro plays correctly at end
- [ ] No file errors reported
- [ ] Delete test HTML when done (not for broadcast)

---

## Step 5 — Wire to Station

Once QC passes, add the show to `index.html`.

Load the show JS after `tracks_local.js` and insert the show tracks
into the playlist at the desired position, or add a button to trigger it.

Then push:
```bash
git add shows/ArtistNameHour/ bits/show_intro.mp3
git commit -m "feat: add Artist Name special hour"
git push
```

---

## Existing Bits

| File | Content |
|------|---------|
| `bits/station_id_01.mp3` | Station ID #1 |
| `bits/station_id_02.mp3` | Station ID #2 |
| `bits/back_to_regular.mp3` | "And now back to our regular programming..." |
| `bits/django_intro.mp3` | Django Reinhardt special hour intro |
| `bits/unearthly_newsflash.mp3` | Unearthly Report newsflash |
| `bits/mannavator_ad.mp3` | Mannavator advertisement |
| `bits/Illumination-Station-AD.mp3` | Illumination Station ad |

---

## Existing Shows

| Folder | Description |
|--------|-------------|
| `shows/DjangoHour/` | Django Reinhardt — 75 tracks, shuffled |

---

## Quick Reference — Rotate Regular Playlist

```bash
~/WOLD-PM.com/rotate_playlist.sh
```

Regenerates and pushes a fresh randomized rotation automatically.
