# cppsong

This repo exists to write and generate funny songs about C++ (the language,
the standard, the committee, template errors, undefined behavior, etc.).
Lyrics live in Markdown, audio is generated via the Gemini API and saved to
`songs/`.

## Layout

- `song.md` — lyrics for the current/canonical song ("Undefined Behavior Blues").
- `scripts/` — standalone Python generation scripts, one per approach/genre.
- `songs/` — generated audio output (mp3). Not cleaned up automatically;
  filenames indicate model/genre (e.g. `cppsong1_lyria3.mp3`, `cppsong1_jpop.mp3`).
- `keys/` — API keys as plain text files, one key per file, no trailing
  content beyond the key. **Gitignored** — never commit this directory or
  paste its contents into a song, commit message, or anywhere else.

## Generating a song

Preferred approach: **Lyria 3** via the Gemini `interactions` API
(`client.interactions.create(model="lyria-3-pro-preview", ...)`), which
produces a full track with real sung vocals and instrumentation in one call.
See `scripts/gen_song_lyria3.py` and `scripts/gen_song_jpop.py` for working
examples — copy one, swap the genre/instrument/vocal description at the top
of the `PROMPT` string, and set a new `OUT_PATH` under `songs/`. Don't
overwrite an existing genre's script/output unless asked; add a new
`gen_song_<genre>.py`.

Notes on the API, learned by trial and error:
- Model names: `lyria-3-pro-preview` (full song, ~2-3 min) and
  `lyria-3-clip-preview` (fixed 30s clip).
- `response_format={"type": "audio"}` — do **not** pass `mime_type` in
  `response_format`; the API rejects it (`Audio mime_type is not supported in
  response_format`). Output comes back as MP3.
- There's no separate structured field for vocal gender/timbre/genre/BPM —
  all of that is steered through the prompt text itself (natural language +
  `[Verse]`/`[Chorus]`/`[Bridge]` section tags). Keep vocal style, genre,
  BPM, and instrument list as an explicit block at the top of the prompt.
- The key is loaded from `keys/gemini.txt` and passed via
  `genai.Client(api_key=...)`.

Older/alternate approaches also live in `scripts/` for reference:
- `gen_song_tts.py` — Gemini TTS reading the lyrics expressively (not
  singing, no melody).
- `gen_music_lyria.py` — Lyria RealTime (`lyria-realtime-exp`), instrumental
  only, streamed live over a WebSocket session; useful if you want a backing
  track to mix under something else, not a full song generator.
Prefer Lyria 3 (`gen_song_lyria3.py`-style) over these for anything where the
goal is "produce a song" — TTS reads the lyrics but doesn't sing, and Lyria
RealTime doesn't do vocals or lyrics at all.

## Editing audio

`ffmpeg` is available on this machine and is the standard tool for trims,
mixes, and format conversion here (e.g. `ffmpeg -y -ss 10 -i in.mp3 -c copy
out.mp3` to cut the first 10s). Prefer `-c copy` for simple trims to avoid
re-encoding when codec/container allow it.

## Conventions

- New songs/lyrics go through `song.md`-style files or inline in the
  generation script's `PROMPT`; keep lyrics text in one place per song so
  edits don't drift between the `.md` file and the script.
- Keep humor tech-literate and specific (real C++ pitfalls: UB, SFINAE,
  template error walls, ABI breaks, etc.) rather than generic "programming is
  hard" jokes — that's the running bit of this repo.
