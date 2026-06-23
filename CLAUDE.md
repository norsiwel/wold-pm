# CLAUDE.md — WOLD-PM Post Meridian Radio
*Last updated: 2026-06-23*

## Project Overview
Live alt-universe pirate radio station at wold-pm.com.
Hosted on Cloudflare Pages (web) and R2 (audio).
GitHub repo: https://github.com/norsiwel/wold-pm
International listenership — early following in Singapore.

## Location
/home/ron/WOLD-PM.com (primary working directory)
T7 backup: /run/media/ron/T7/WOLD-PM.com

## Deployment Chain
local edit → git push origin → GitHub → Cloudflare Pages → live site
Audio served from R2 bucket "wold-pm" at https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev
MP3s never in git (except bits/ which are small). R2 bucket hard limit 10GB without Ron's approval.
CRITICAL: Always use --remote flag with wrangler or uploads go to local simulation only.
Verify R2 auth first: npx wrangler whoami

## Git Remotes
- origin: https://github.com/norsiwel/wold-pm.git (Cloudflare deployment)
- local: /run/media/ron/T7/wold-pm-backup.git (T7 backup)

## Key Files
- build_playlist_updated.py — generates tracks_local.js, always use this
- tracks_local.js — current playlist (auto-generated, do not hand-edit)
- index.html — station player page
- fetch_music.py — MUSIC_DIR=/home/ron/WOLD-PM.com/music

## Playlist Builder Notes
- Shuffles music randomly on every run
- Spaces bits every 3-6 songs
- Station IDs every ~1 hour by duration
- Shows inserted evenly through rotation
- Paired bits (intros/outros) kept separate from standalone bits
- STANDALONE_TITLES dict in build script maps filenames to display names
- Run: python3 build_playlist_updated.py then git add/commit/push

## Current Rotation Stats (June 2026)
- Regular tracks: 85 (numbered 01-73 + originals + Woody Guthrie etc)
- Special shows: 6 (ArmstrongVol1, ArmstrongVol2, DjangoHour x3, FolkInterlude)
- Total scheduled: 224 tracks
- Estimated runtime: ~10.5 hours per loop

## Music Library
- 01-65: Big band era (swing, jazz, blues)
- 66-67: 1925 Blues (LOC/Citizen DJ PD recordings)
- 68-73: 1925 Jazz (LOC/Citizen DJ PD recordings)
- AIN'T GONNA BE TREATED THIS WAY - Woody Guthrie
- DRUNKEN RAT - Cisco Houston
- originals/ — Norsiwel original compositions

## Bits
- station_id_01/02 — station IDs
- armstrong_intro/outro — All That Jazz show open/close
- django_intro, bird_intro — show intros
- folk_intro/outro — Folk Interlude open/close
- back_to_regular — show close
- mannavator_ad — Mannavator sponsor spot
- Illumination-Station-AD — Illumination Station sponsor
- Illumination-Station-AD-original — original ElevenLabs version (archived)
- unearthly_newsflash — newsflash bit
- EveningNews-CrownFTL — Crown FTL evening news
- WOLD-weather-by GTFbeer — weather report by Green Tree Frog Beer
- Travel-with-Arlo — Arlo's traffic report
- PSA-recycling — recycling PSA
- Phoenix-Atomic-cycles — Phoenix Atomic Motorcycles news

## Shows
- shows/ArmstrongVol1/ — Louis Armstrong tracks 01-15 (1923-33)
- shows/ArmstrongVol2/ — Louis Armstrong tracks 16-29 (1923-33)
- shows/DjangoHour/ — Django Reinhardt Vol1/2/3
- shows/FolkInterlude/ — Folk music set
- shows/SciFiSpecial/ — inactive
- shows/_inactive/ — staging area for shows not yet active
- shows/_template/ — template for new shows

## Player Notes
- Player fixed June 2026 — proper error/retry with loadAndPlay() on each retry
- Stall detector polls every 5s — skips if currentTime hasn't moved
- Retries up to 4 times with exponential backoff before skipping
- Music Library section removed from index.html — broadcast only station

## Universe & Lore
WOLD-PM Post Meridian Radio — Alt-universe pirate radio 1170 KC
"The Superposition Station — Broadcasting from... somewhere"
Named after Harry Chapin's 1972 song WOLD.

Taglines: "Don't call us. Just listen." / "Onward through the fog." /
"Signal is ours." / "Management is aware."

Recurring sponsors:
- Mannavator — AI kitchen, "Not just toast. Stay Out Of The Kitchen."
- Crown FTL — faster than light engines
- Phoenix Atomic Motorcycles — "Speed limits are suggestions"
- Green Tree Frog Beer — "It don't taste too good but it gets you where you're going"
- Burman Bros Dragstrip — Ron Farmer's 2048 Studebaker Electro 4, 300mph
- Illumination Station — WOLD-PM sponsor

Running lore: Greater AI Council, The Race Around Jupiter, The Grays buying NJ,
Management always aware but unavailable for comment.
No frogs were harmed. Or the beer.

## TODO
- [ ] armstrong_intro2 (All That Jazz promo) — script written, needs rendering
- [ ] Burman Bros spot — script + voices ready, needs final render and upload
- [ ] sfx_importer_v001.py — standalone SFX import/trim/normalize tool
- [ ] SciFiSpecial show — currently inactive, needs content
- [ ] More bits — spots for other Pantopia universe sponsors
- [ ] wrangler login reminder — auth expires, check before uploads
