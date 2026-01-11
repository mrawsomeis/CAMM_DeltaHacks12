import requests
import sounddevice as sd
import soundfile as sf
import io
import numpy as np

API_KEY = "You don't get my key silly :)"
VOICE_ID = "VsQmyFHffusQDewmHB5v"

def speak(text: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }

    params = {
        "output_format": "mp3_44100_128"  # ✅ Free tier allowed
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    r = requests.post(url, headers=headers, params=params, json=payload)
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}: {r.text[:300]}")

    # Decode MP3 from memory
    audio_bytes = io.BytesIO(r.content)
    data, samplerate = sf.read(audio_bytes, dtype="float32")

    sd.play(data, samplerate)
    sd.wait()