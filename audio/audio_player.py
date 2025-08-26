# audio/audio_player.py
from telegram import Update
from telegram.ext import ContextTypes
from audio.tts_service import get_audio

async def send_voice_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str):
    try:
        filepath = get_audio(text)
        with open(filepath, "rb") as audio:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=audio,
                title="Тренер",
                performer="Алекс"
            )
    except Exception as e:
        print("Ошибка озвучки:", e)
        await context.bot.send_message(chat_id=chat_id, text=text)