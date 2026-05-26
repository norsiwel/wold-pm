# WOLD-PM R2 Audio Storage

## Bucket Name
wold-pm

## Public Development URL
https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev

## Usage
All audio files too large for Cloudflare Pages are served from this bucket.
Reference files in playlists as:
  https://pub-70b842d65a4f4ada82dec98f8d446fa2.r2.dev/shows/DjangoHour/filename.mp3

## Folders
- shows/DjangoHour/   — Django Reinhardt special hour MP3s (75 tracks)

## Notes
- Rate limited dev URL — fine for current traffic levels
- For production upgrade: add custom domain audio.wold-pm.com via Custom Domains in R2 settings
- CORS policy needed for browser audio playback — see below

## CORS Policy (add in R2 Settings → CORS Policy)
[
  {
    "AllowedOrigins": ["https://wold-pm.com", "https://www.wold-pm.com"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }
]
