# audio/tts_service.py
from gtts import gTTS
import os
import hashlib

CACHE_DIR = "audio_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def text_to_speech_yandex(text: str) -> bytes:
    tts = gTTS(text=text, lang='ru', slow=False)
    text_hash = hashlib.md5(text.encode()).hexdigest()
    filepath = os.path.join(CACHE_DIR, f"{text_hash}.wav")
    tts.save(filepath)
    with open(filepath, "rb") as f:
        return f.read()

def get_audio(text: str) -> str:
    text_hash = hashlib.md5(text.encode()).hexdigest()
    filepath = os.path.join(CACHE_DIR, f"{text_hash}.wav")

    if not os.path.exists(filepath):
        audio_data = text_to_speech_yandex(text)
        with open(filepath, "wb") as f:
            f.write(audio_data)

    return filepath