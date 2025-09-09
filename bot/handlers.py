# bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from audio.tts_service import get_audio
from training.plans.timed_fartlek_plan import TimedFartlekPlan
from web.server import WebServer
import os
import shutil
import json

# Глобальный веб-сервер
web_server = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой беговой коуч. Жми /fartlek")

async def fartlek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global web_server
    
    chat_id = update.effective_chat.id
    await update.message.reply_text("🔥 Создаю аудиогид для тренировки...")
    
    try:
        # Создаём плейлист для веб-плеера
        create_web_player_playlist()
        
        # Запускаем веб-сервер
        if web_server is None:
            web_server = WebServer(port=8000)
        
        if not web_server.is_running():
            web_server.start()
        
        # Отправляем ссылку
        await update.message.reply_text(
            "🎧 Аудиогид готов!\n"
            "Откройте в браузере: http://localhost:8000\n"
            "💡 Используйте наушники во время пробежки!"
        )
        
    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")


def create_silence_file(duration_seconds, directory, filename):
    """Создаёт MP3 файл с точной длительностью тишины (без pydub)"""
    
    silence_path = os.path.join(directory, filename)
    
    # Используем готовый тишинный шаблон
    silent_template = os.path.join("audio_cache", "silence_template.mp3")
    
    # Если шаблона нет - создаём
    if not os.path.exists(silent_template):
        create_silence_template(silent_template)
    
    # Создаём файл нужной длительности
    # MP3: ~40KB в секунду для нормального качества
    target_bytes = duration_seconds * 40 * 1024  # 40KB/сек
    
    with open(silence_path, "wb") as outfile:
        bytes_written = 0
        
        with open(silent_template, "rb") as template:
            template_data = template.read()
            
            while bytes_written < target_bytes:
                remaining_bytes = target_bytes - bytes_written
                write_size = min(len(template_data), remaining_bytes)
                outfile.write(template_data[:write_size])
                bytes_written += write_size
    
    print(f"Создана тишина {duration_seconds} секунд: {silence_path}")
    return silence_path

def create_silence_template(template_path):
    """Создаёт шаблон тишины"""
    from gtts import gTTS
    
    # Создаём очень короткий и тихий звук
    tts = gTTS(text=".", lang='ru', slow=True, tld='ru')
    tts.save(template_path)
    
    # Увеличиваем размер файла для лучшего качества
    with open(template_path, "rb") as infile:
        data = infile.read()
    
    with open(template_path, "wb") as outfile:
        for _ in range(10):
            outfile.write(data)

def create_music_file(duration_seconds, directory, filename):
    """Создаёт музыкальный файл (немного больше нужной длительности)"""
    
    music_path = os.path.join(directory, filename)
    print(f"=== Создание музыкального файла: {filename} ({duration_seconds} сек) ===")
    
    # Создаём файл на 15 секунд больше, чтобы точно хватило
    extended_duration = duration_seconds + 15
    
    # Ищем готовый музыкальный файл нужной длительности
    audio_dir = os.path.join("web", "audio")
    if os.path.exists(audio_dir):
        # Ищем файлы с разными именами
        possible_files = [
            f"background_{duration_seconds}sec.mp3",
            f"music_{duration_seconds}sec.mp3",
            f"background_{duration_seconds}.mp3",
            f"music_{duration_seconds}.mp3"
        ]
        
        # Также ищем файлы с немного другой длительностью
        extended_files = [
            f"background_{extended_duration}sec.mp3",
            f"music_{extended_duration}sec.mp3"
        ]
        
        all_possible_files = possible_files + extended_files
        
        for file_name in all_possible_files:
            source_path = os.path.join(audio_dir, file_name)
            if os.path.exists(source_path):
                print(f"✓ Найден готовый файл: {file_name}")
                
                # Создаём файл нужной (или чуть больше) длительности
                create_extended_file(source_path, music_path, duration_seconds)
                actual_size = os.path.getsize(music_path)
                print(f"✓ Создан файл: {filename}, размер: {actual_size} байт")
                return music_path
    
    # Если готовых файлов нет - создаём тишину нужной длительности
    print(f"⚠ Готовые файлы не найдены, создаём тишину на {duration_seconds} секунд")
    silence_file = create_extended_silence(duration_seconds, directory, filename)
    return silence_file

def create_extended_file(source_path, dest_path, target_duration):
    """Создаёт файл нужной или чуть большей длительности"""
    try:
        from pydub import AudioSegment
        
        # Загружаем исходный файл
        audio = AudioSegment.from_mp3(source_path)
        
        target_duration_ms = target_duration * 1000
        extended_duration_ms = (target_duration + 15) * 1000  # +15 секунд
        
        if len(audio) >= extended_duration_ms:
            # Обрезаем до расширенной длительности
            result_audio = audio[:extended_duration_ms]
        elif len(audio) >= target_duration_ms:
            # Файл уже нужной длительности - оставляем как есть
            result_audio = audio
        else:
            # Повторяем до нужной длительности + запас
            repeat_count = (extended_duration_ms // len(audio)) + 1
            result_audio = (audio * repeat_count)[:extended_duration_ms]
        
        # Сохраняем результат
        result_audio.export(dest_path, format="mp3")
        print(f"✓ Создан расширенный файл: {len(result_audio)/1000} сек")
        
    except Exception as e:
        print(f"❌ Ошибка создания расширенного файла: {e}")
        # Если pydub не работает - обычное копирование
        shutil.copy2(source_path, dest_path)

def create_extended_silence(duration_seconds, directory, filename):
    """Создаёт файл тишины с запасом"""
    
    silence_path = os.path.join(directory, filename)
    extended_duration = duration_seconds + 15  # +15 секунд запаса
    print(f"=== Создание тишины: {filename} ({duration_seconds}+15 сек) ===")
    
    # Используем готовый тишинный шаблон
    silent_template = os.path.join("audio_cache", "silence_template.mp3")
    
    # Если шаблона нет - создаём минимальный звук
    if not os.path.exists(silent_template):
        from gtts import gTTS
        tts = gTTS(text=".", lang='ru', slow=True)
        tts.save(silent_template)
    
    # Создаём файл нужного размера (с запасом)
    target_bytes = extended_duration * 40 * 1024  # 40KB/сек
    
    with open(silence_path, "wb") as outfile:
        bytes_written = 0
        
        with open(silent_template, "rb") as template:
            template_data = template.read()
            
            while bytes_written < target_bytes:
                remaining_bytes = target_bytes - bytes_written
                write_size = min(len(template_data), remaining_bytes)
                outfile.write(template_data[:write_size])
                bytes_written += write_size
    
    actual_size = os.path.getsize(silence_path)
    print(f"✓ Создана расширенная тишина: {filename}, размер: {actual_size} байт")
    return silence_path

def create_web_player_playlist():
    """Создаёт плейлист для веб-плеера"""
    
    # Создаём папку для аудио
    web_audio_dir = os.path.join("web", "audio")
    os.makedirs(web_audio_dir, exist_ok=True)
    
    # Получаем план тренировки
    plan = TimedFartlekPlan()
    
    # Создаём список треков
    playlist = []
    
    # 1. Вступление
    intro_msg = "🔥 Начинаем фортлек! 5 минут разминки. Лёгкий бег или ходьба."
    intro_path = get_audio(intro_msg)
    intro_dest = os.path.join(web_audio_dir, "01_intro.mp3")
    shutil.copy2(intro_path, intro_dest)
    playlist.append({
        "file": "audio/01_intro.mp3",
        "title": "Вступление",
        "type": "speech",
        "duration": 0
    })
    
    print("=== Создаём разминку 5 минут ===")
    
    # 2. Музыка разминки (5 минут = 300 секунд)
    warmup_file = create_music_file(300, web_audio_dir, "02_warmup.mp3")
    playlist.append({
        "file": "audio/02_warmup.mp3",
        "title": "Разминка 5 минут",
        "type": "music",
        "duration": 300
    })
    
    # 3. Основная тренировка
    track_number = 3
    
    for i, phase in enumerate(plan.phases):
        if phase.phase_type == "warmup":
            continue
            
        elif phase.phase_type == "run":
            minutes = phase.duration // 60
            text = f"🟡 Интервал: {minutes} минут в ускоренном темпе!"
            
        elif phase.phase_type == "rest":
            minutes = phase.duration // 60
            text = f"🟢 Отдых: {minutes} минут. Восстановись."
            
        elif phase.phase_type == "cooldown":
            text = "🔵 Заминка: 3 минуты ходьбы. Отличная работа!"
        
        # Добавляем сообщение тренера
        print(f"=== Создаём сообщение {track_number}: {text} ===")
        msg_path = get_audio(text)
        msg_filename = f"{track_number:02d}_message.mp3"
        msg_dest = os.path.join(web_audio_dir, msg_filename)
        shutil.copy2(msg_path, msg_dest)
        playlist.append({
            "file": f"audio/{msg_filename}",
            "title": text,
            "type": "speech",
            "duration": 0
        })
        track_number += 1
        
        # Добавляем музыку/паузу правильной длительности
        music_duration = phase.duration
        music_filename = f"{track_number:02d}_music.mp3"
        
        print(f"=== Создаём музыку {track_number}: {music_duration} сек ===")
        # Создаём музыку правильной длительности
        music_file = create_music_file(music_duration, web_audio_dir, music_filename)
        
        playlist.append({
            "file": f"audio/{music_filename}",
            "title": f"Музыка {music_duration} сек",
            "type": "music", 
            "duration": music_duration
        })
        track_number += 1
    
    # 4. Финал
    final_msg = "🏆 Тренировка завершена! Ты молодец!"
    final_path = get_audio(final_msg)
    final_filename = f"{track_number:02d}_final.mp3"
    final_dest = os.path.join(web_audio_dir, final_filename)
    shutil.copy2(final_path, final_dest)
    playlist.append({
        "file": f"audio/{final_filename}",
        "title": "Финал",
        "type": "speech",
        "duration": 0
    })
    
    # Сохраняем плейлист
    playlist_path = os.path.join("web", "playlist.json")
    with open(playlist_path, "w", encoding="utf-8") as f:
        json.dump(playlist, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Плейлист создан: {len(playlist)} треков")
    
    # Проверяем все созданные файлы
    print("=== Проверка созданных файлов ===")
    for file_info in playlist:
        filepath = os.path.join("web", file_info["file"])
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {file_info['file']}: {size} байт")
        else:
            print(f"❌ {file_info['file']}: файл не найден")
    
    return playlist