import base64
import os
import sys

from google import genai

KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "keys", "gemini.txt")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "songs", "cppsong1_arabesk.mp3")

with open(KEY_PATH, "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = genai.Client(api_key=api_key)

PROMPT = """Genre: Turkish arabesk-pop, ~90 BPM, minor key, dramatic and melancholic but with a modern pop beat underneath.
Instruments: weeping violin section, clarinet, darbuka and pop drums together, synth strings, deep synth bass, occasional saz-style plucked accents.
Vocals: Male arabesk lead singer, deep emotional belting with heavy melisma and vibrato, dramatic swells and pained pauses like classic arabesk, sung (not spoken) in English lyrics but with authentic Turkish arabesk vocal phrasing and ornamentation.
Title: "Undefined Behavior Blues"

Lyrics:

[Verse 1]
I wrote a little program, just to add up one plus one,
Signed integer overflow, now my program's on the run.
The compiler looked at my code and just began to laugh,
That's U-B my friend, I'll optimize your whole class in half!

[Chorus]
Oh, undefined behavior, undefined behavior blues,
It compiles clean, runs fine on Tuesdays, crashes when you choose.
The standard says not specified, the standard don't care why,
My nasal demons flew away and now my cat can fly.

[Verse 2]
I asked for move semantics, they said it's an optimization,
Then rvalue references gave me an identity crisis nation.
I read the cppreference page for std colon colon launder one more time,
Three years later, still don't get it, but I nod like it all makes sense in rhyme.

[Chorus]
Oh, undefined behavior, undefined behavior blues,
Whatever you meant, dear standard, I'm afraid I gotta lose.
I dangled a reference, I aliased through a char star,
Now Valgrind's screaming at me like I robbed a candy cart.

[Bridge]
Template error messages, forty pages tall,
No matching function found, didn't even try at all!
Enable if, S-F-I-N-A-E, concepts came to save the day,
But now I need a P-H-D just to make Foo of Bar compile, okay?

[Verse 3]
They added modules, coroutines, and ranges to the mix,
Every three years a new standard, and none of my old code fits.
Just recompile it, they tell me, it's backwards compatible, see!
Narrator: it was not compatible, it took down all of Q-A.

[Final Chorus]
Oh, undefined behavior, undefined behavior blues,
Fifty ways to shoot your foot and every one's front page news.
But I still love you, C plus plus, you beautiful cursed machine,
Zero cost abstractions and the fastest bugs I've ever seen!

[Outro, spoken deadpan over fading music]
Warning: unused variable, my will to live.
"""

print("Requesting arabesk-pop song from lyria-3-pro-preview ...", file=sys.stderr)

interaction = client.interactions.create(
    model="lyria-3-pro-preview",
    input=PROMPT,
    response_format={"type": "audio"},
)

print("status:", interaction.status, file=sys.stderr)

audio = interaction.output_audio
if audio is None:
    print("No output_audio on interaction. Dumping steps for debugging:", file=sys.stderr)
    for step in interaction.steps or []:
        print(step, file=sys.stderr)
    if interaction.errors:
        print("ERRORS:", interaction.errors, file=sys.stderr)
    sys.exit(1)

data = audio.data
if isinstance(data, str):
    data = base64.b64decode(data)

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "wb") as f:
    f.write(data)

print("Wrote", OUT_PATH, "bytes:", len(data))
