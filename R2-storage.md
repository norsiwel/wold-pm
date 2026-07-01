# WOLD-PM R2 Audio Storage

## Bucket Name
wold-pm

## Public Development URL
https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev

## Hard Rule
R2 bucket must never exceed 10GB total without Ron's explicit approval.
Always check current usage before uploading large batches.
Current usage: ~4.9GB (as of 2026-05-26)

## Audio Structure
All audio served from R2. Reference files as:
  https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev/music/filename.mp3
  https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev/bits/filename.mp3
  https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev/shows/ShowName/filename.mp3

## Folders in R2
- music/          — 65 big band/swing tracks + originals (~4.5GB)
- bits/           — station IDs, ads, announcements (~4MB)
- shows/DjangoHour/   — 75 Django Reinhardt tracks (~395MB)
- shows/FolkInterlude/ — 6 tracks: Lead Belly, Woody Guthrie, Cisco Houston (~49MB)

## Shows Pending (audio not yet in R2)
- shows/ArmstrongVol1/ — Louis Armstrong Vol 1 (15 tracks, FLACs need converting)
- shows/ArmstrongVol2/ — Louis Armstrong Vol 2 (14 tracks, FLACs need converting)

## Announcer Staff
| Voice    | Engine | Used For                        |
|----------|--------|---------------------------------|
| ryan-high | Piper  | Django Reinhardt intros/outros  |
| hfc_male  | Piper  | Folk Interlude intros/outros    |
| am_onyx   | Kokoro | Louis Armstrong intros/outros   |
| am_onyx   | Kokoro | Bird intro (saved, ready to use)|

## Kokoro Model Location
/home/ron/PlaymakerStudio/kokoro/kokoro-v1.0.onnx
/home/ron/PlaymakerStudio/kokoro/voices-v1.0.bin

## TTS Tips
- Piper: use ... for pauses, CAPS for emphasis, periods between phrases
- Kokoro: use ... for pauses, CAPS for emphasis, speed=0.9 for gravitas, volume=2.0-2.5
- W-O-L-D-PM forces letter-by-letter pronunciation of call sign
- Test with ffplay before committing as final

## Bits Inventory
| File                    | Voice  | Content                                      |
|-------------------------|--------|----------------------------------------------|
| station_id_01.mp3       | —      | Station ID #1                                |
| station_id_02.mp3       | —      | Station ID #2                                |
| back_to_regular.mp3     | Ryan   | "And now back to our regular programming..." |
| django_intro.mp3        | Ryan   | Django Reinhardt special hour intro          |
| folk_intro.mp3          | HFC    | Folk Interlude intro — Lead Belly etc        |
| folk_outro.mp3          | HFC    | "Onward through the fog"                     |
| armstrong_intro.mp3     | Onyx   | "And NOW... Satch HIMSELF! Louis Armstrong..." |
| armstrong_outro.mp3     | Onyx   | "Where the music never stops!"               |
| bird_intro.mp3          | Onyx   | Jazz interlude intro — saved for Bird        |
| unearthly_newsflash.mp3 | —      | Unearthly Report newsflash                   |
| mannavator_ad.mp3       | —      | Mannavator advertisement                     |
| Illumination-Station-AD.mp3 | —  | Illumination Station ad                      |

## CORS Policy (configured in R2 Settings)
[
  {
    "AllowedOrigins": ["https://wold-pm.com", "https://www.wold-pm.com"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }
]

## Notes
- Rate limited dev URL — fine for current traffic
- For production upgrade: add custom domain audio.wold-pm.com via R2 Settings → Custom Domains
- Never put MP3s in git — R2 only, always
