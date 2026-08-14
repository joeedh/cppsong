import asyncio
import base64
import os
import sys
import wave

from google import genai
from google.genai import types

KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "keys", "gemini.txt")
OUT_WAV = os.path.join(os.path.dirname(__file__), "..", "songs", "cppsong1_music.wav")

DURATION_SECONDS = 100
SAMPLE_RATE = 48000
CHANNELS = 2
SAMPLE_WIDTH = 2

with open(KEY_PATH, "r", encoding="utf-8") as f:
    api_key = f.read().strip()

client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})


async def main():
    audio_bytes = bytearray()
    stop_event = asyncio.Event()

    async with client.aio.live.music.connect(
        model="models/lyria-realtime-exp"
    ) as session:

        async def receive():
            try:
                async for message in session.receive():
                    if stop_event.is_set():
                        break
                    sc = message.server_content
                    if sc and sc.audio_chunks:
                        for chunk in sc.audio_chunks:
                            audio_bytes.extend(chunk.data)
                    fp = message.filtered_prompt
                    if fp:
                        print("FILTERED PROMPT:", fp, file=sys.stderr)
            except Exception as e:
                print("receive loop ended:", e, file=sys.stderr)

        recv_task = asyncio.create_task(receive())

        await session.set_weighted_prompts(
            prompts=[
                types.WeightedPrompt(text="upbeat honky-tonk country", weight=1.5),
                types.WeightedPrompt(text="banjo and fiddle", weight=1.0),
                types.WeightedPrompt(text="comedic bar band, live tavern energy", weight=1.0),
                types.WeightedPrompt(text="acoustic guitar, twangy", weight=0.8),
            ]
        )
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(bpm=120, temperature=1.1, density=0.6)
        )
        await session.play()

        elapsed = 0
        while elapsed < DURATION_SECONDS:
            await asyncio.sleep(5)
            elapsed += 5
            print(f"...{elapsed}s, buffered {len(audio_bytes)} bytes", file=sys.stderr)

        await session.stop()
        stop_event.set()
        recv_task.cancel()
        try:
            await recv_task
        except asyncio.CancelledError:
            pass

    os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
    with wave.open(OUT_WAV, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(bytes(audio_bytes))

    print("Wrote", OUT_WAV, "bytes:", len(audio_bytes))


asyncio.run(main())
