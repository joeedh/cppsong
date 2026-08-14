import os
import sys

from google import genai
from google.genai import types

KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "keys", "gemini.txt")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "songs", "cppsong1_cover.png")

with open(KEY_PATH, "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = genai.Client(api_key=api_key)

PROMPT = """Album cover art for a comedic country song titled "Undefined Behavior Blues".

Square 1:1 composition, vintage 1970s honky-tonk vinyl record sleeve aesthetic:
warm faded amber and dusty teal palette, subtle paper grain and print
misregistration, screen-printed look.

Scene: a weathered cowboy programmer sits on a wooden bar stool in a dim
tavern, cradling an acoustic guitar. Instead of a guitar body, the soundhole
glows with lines of C++ code. Behind him, a saloon wall is papered with
endless torn printouts of compiler error messages cascading to the floor.
Small nasal demons -- tiny impish silhouettes -- fly out of a beer mug and
circle a ceiling fan. A neon bar sign reads "C++" in flickering tubes.

Bold distressed western slab-serif title text across the top reading
"UNDEFINED BEHAVIOR BLUES". Smaller text along the bottom reading
"segfaults & steel guitar".

Text must be spelled exactly as given. No watermark, no signature.
"""

MODELS = [
    "gemini-3-pro-image-preview",
    "gemini-2.5-flash-image",
    "imagen-4.0-generate-001",
]


def save(data: bytes) -> None:
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        f.write(data)
    print("Wrote", OUT_PATH, "bytes:", len(data))


for model in MODELS:
    print("Trying", model, "...", file=sys.stderr)
    try:
        if model.startswith("imagen"):
            resp = client.models.generate_images(
                model=model,
                prompt=PROMPT,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                ),
            )
            save(resp.generated_images[0].image.image_bytes)
            break

        resp = client.models.generate_content(
            model=model,
            contents=PROMPT,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1"),
            ),
        )
        for part in resp.candidates[0].content.parts:
            if part.inline_data is not None:
                save(part.inline_data.data)
                break
        else:
            print("No image part in response from", model, file=sys.stderr)
            continue
        break
    except Exception as e:  # noqa: BLE001 - just fall through to the next model
        print(f"{model} failed: {type(e).__name__}: {e}", file=sys.stderr)
else:
    print("All image models failed.", file=sys.stderr)
    sys.exit(1)
