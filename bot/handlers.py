# bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from audio.tts_service import get_audio
from training.plans.timed_fartlek_plan import TimedFartlekPlan
import asyncio
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой беговой коуч. Жми /fartlek")

async def fartlek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Отправляем вступление сразу
    intro_text = "🔥 Начинаем фортлек! 5 минут разминки. Приготовься!"
    audio_path = get_audio(intro_text)
    
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title="Начало тренировки",
                caption="🎧 Слушай и следуй указаниям!"
            )
    
    # Запланируем остальные сообщения
    context.application.create_task(send_training_messages(context, chat_id))

async def send_training_messages(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Отправка сообщений по таймеру на основе TimedFartlekPlan"""
    
    # Получаем план тренировки
    plan = TimedFartlekPlan()
    phases = plan.phases
    
    # Создаём список сообщений с таймингами
    messages = []
    cumulative_time = 300  # 5 минут разминки уже прошли
    
    # Обрабатываем фазы из плана
    for phase in phases:
        if phase.phase_type == "warmup":
            continue  # Уже учли в вступлении
            
        elif phase.phase_type == "run":
            minutes = phase.duration // 60
            seconds = phase.duration % 60
            if seconds == 0:
                text = f"🟡 Интервал: {minutes} минут в ускоренном темпе!"
            else:
                text = f"🟡 Интервал: {minutes} минут {seconds} секунд в ускоренном темпе!"
                
        elif phase.phase_type == "rest":
            minutes = phase.duration // 60
            seconds = phase.duration % 60
            if seconds == 0:
                text = f"🟢 Отдых: {minutes} минут. Восстановись."
            else:
                text = f"🟢 Отдых: {minutes} минут {seconds} секунд. Восстановись."
                
        elif phase.phase_type == "cooldown":
            text = "🔵 Заминка: 3 минуты ходьбы. Отличная работа!"
        
        else:
            continue
            
        messages.append({
            "delay": cumulative_time,
            "text": text
        })
        
        cumulative_time += phase.duration
    
    # Добавляем финальное сообщение
    messages.append({
        "delay": cumulative_time,
        "text": "🏆 Тренировка завершена! Ты молодец!"
    })
    
    # Отправляем сообщения по таймеру
    start_time = asyncio.get_event_loop().time()
    
    for item in messages:
        # Ждём нужное время
        delay = item["delay"]
        elapsed = asyncio.get_event_loop().time() - start_time
        sleep_time = max(0, delay - elapsed)
        
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)
        
        # Отправляем как аудио (автопроигрывание)
        text = item["text"]
        try:
            audio_path = get_audio(text)
            if os.path.exists(audio_path):
                with open(audio_path, "rb") as audio:
                    await context.bot.send_audio(
                        chat_id=chat_id,
                        audio=audio,
                        title="Тренер",
                        caption=text
                    )
            else:
                await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"Ошибка отправки аудио: {e}")
            await context.bot.send_message(chat_id=chat_id, text=text)