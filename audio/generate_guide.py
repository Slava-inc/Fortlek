# audio/generate_guide.py
from pydub import AudioSegment
import os
from audio.tts_service import get_audio

def create_fartlek_guide(phases):
    combined = AudioSegment.silent(duration=0)

    for i, phase in enumerate(phases):
        # Текст фразы
        if phase.phase_type == "warmup":
            text = "🔥 Разминка! 5 минут лёгкого бега. Дыши ровно."
        elif phase.phase_type == "run":
            text = f"🟡 Интервал: {phase.duration // 60} минут в ускоренном темпе!"
        elif phase.phase_type == "rest":
            text = f"🟢 Отдых: {phase.duration // 60} минут. Восстановись."
        elif phase.phase_type == "cooldown":
            text = "🔵 Заминка. 3 минуты ходьбы. Отличная работа!"
        else:
            continue

        print(f"Обрабатываем фазу {i+1}: {text[:30]}...")

        # Получаем аудио
        try:
            audio_path = get_audio(text)
            print(f"Аудио путь: {audio_path}")
            
            if os.path.exists(audio_path):
                audio = AudioSegment.from_file(audio_path)
                combined += audio
                # Добавляем паузу
                combined += AudioSegment.silent(duration=phase.duration * 1000)
                print(f"Добавлена пауза: {phase.duration} сек")
            else:
                print(f"Файл не найден: {audio_path}")
                # Добавляем только паузу
                combined += AudioSegment.silent(duration=phase.duration * 1000)
                
        except Exception as e:
            print(f"Ошибка при обработке фазы: {e}")
            combined += AudioSegment.silent(duration=phase.duration * 1000)

    # Сохраняем
    output_path = os.path.join("audio_cache", "full_guide.wav")
    combined.export(output_path, format="wav")
    print(f"Аудиогид сохранён: {output_path}")
    return output_path