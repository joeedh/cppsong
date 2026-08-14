# cppsong

Funny songs about C++ — the language, the standard, undefined behavior,
template error walls, and everything else that makes C++ programmers laugh
(and cry).

Lyrics are written by hand, then turned into full songs — real sung vocals
and instrumentation, not just text-to-speech — using Google's Lyria 3 model
via the Gemini API.

## Contents

- `song.md` — lyrics for "Undefined Behavior Blues," the flagship track.
- `songs/` — generated audio (mp3). A few takes on the same lyrics in
  different genres/models, e.g.:
  - `cppsong1_lyria3.mp3` — outlaw/honky-tonk country, Lyria 3 Pro, sung vocals + full band.
  - `cppsong1_jpop.mp3` — bright J-pop take on the same lyrics.
  - `cppsong1.mp3` / `cppsong1_full.mp3` — earlier TTS-vocal / Lyria-RealTime-backing-track experiments.
- `scripts/` — the Python generation scripts behind each track.
- `keys/` — API keys (gitignored, not included in this repo).

## Generating your own

1. Drop a Gemini API key in `keys/gemini.txt`.
2. `pip install google-genai`
3. Copy `scripts/gen_song_lyria3.py`, edit the genre/instruments/vocal style
   and lyrics in the `PROMPT` string, point `OUT_PATH` at a new file under
   `songs/`, and run it:
   ```
   python scripts/gen_song_jpop.py
   ```

`ffmpeg` is used for any post-processing (trims, mixing, format conversion).

See `CLAUDE.md` for more detail on the Lyria 3 API quirks and repo conventions.
