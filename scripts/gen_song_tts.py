import base64
import json
import os
import sys
import urllib.request
import wave

KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "keys", "gemini.txt")
OUT_WAV = os.path.join(os.path.dirname(__file__), "..", "songs", "cppsong1.wav")

with open(KEY_PATH, "r", encoding="utf-8") as f:
    api_key = f.read().strip()

lyrics = """Perform this as a funny, upbeat honky-tonk country song, singing with a
twangy, exaggerated comedic voice, clear rhythm and melody, like a live
tavern performance. Title: Undefined Behavior Blues.

Verse one.
I wrote a little program, just to add up one plus one,
Signed integer overflow, now my program's on the run.
The compiler looked at my code and just began to laugh,
That's U B my friend, I'll optimize your whole class in half!

Chorus.
Oh, undefined behavior, undefined behavior blues,
It compiles clean, runs fine on Tuesdays, crashes when you choose.
The standard says not specified, the standard don't care why,
My nasal demons flew away and now my cat can fly.

Verse two.
I asked for move semantics, they said it's an optimization,
Then rvalue references gave me an identity crisis nation.
I read the cppreference page for std colon colon launder one more time,
Three years later, still don't get it, but I nod like it all makes sense in rhyme.

Chorus.
Oh, undefined behavior, undefined behavior blues,
Whatever you meant, dear standard, I'm afraid I gotta lose.
I dangled a reference, I aliased through a char star,
Now Valgrind's screaming at me like I robbed a candy cart.

Bridge.
Template error messages, forty pages tall,
No matching function found, didn't even try at all!
Enable if, S F I N A E, concepts came to save the day,
But now I need a P H D just to make Foo of Bar compile, okay?

Verse three.
They added modules, coroutines, and ranges to the mix,
Every three years a new standard, and none of my old code fits.
Just recompile it, they tell me, it's backwards compatible, see!
Narrator: it was not compatible, it took down all of Q A.

Final chorus.
Oh, undefined behavior, undefined behavior blues,
Fifty ways to shoot your foot and every one's front page news.
But I still love you, C plus plus, you beautiful cursed machine,
Zero cost abstractions and the fastest bugs I've ever seen!

Spoken outro, deadpan.
Warning: unused variable, my will to live."""

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-preview-tts:generateContent"
)

payload = {
    "contents": [{"parts": [{"text": lyrics}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Puck"}}
        },
    },
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP ERROR", e.code, file=sys.stderr)
    print(e.read().decode("utf-8"), file=sys.stderr)
    sys.exit(1)

candidates = body.get("candidates", [])
if not candidates:
    print("No candidates in response:", json.dumps(body, indent=2), file=sys.stderr)
    sys.exit(1)

parts = candidates[0]["content"]["parts"]
audio_part = next(p for p in parts if "inlineData" in p)
mime = audio_part["inlineData"]["mimeType"]
pcm = base64.b64decode(audio_part["inlineData"]["data"])
print("mime type:", mime, "bytes:", len(pcm))

# mime typically like "audio/L16;codec=pcm;rate=24000"
rate = 24000
for chunk in mime.split(";"):
    chunk = chunk.strip()
    if chunk.startswith("rate="):
        rate = int(chunk.split("=", 1)[1])

os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
with wave.open(OUT_WAV, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate)
    wf.writeframes(pcm)

print("Wrote", OUT_WAV)
