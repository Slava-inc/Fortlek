# 🏃‍♂️ NRC-Style Telegram Fartlek Bot

**Telegram-бот для интервальных тренировок в стиле Nike Run Club**, с голосовым коучем, таймерами и достижениями.

## 🎯 Возможности

- Интервальная тренировка (фортлек) по времени: 30 минут (в целях отладки каждый интервал уменьшен в 10 раз)
- Таймеры и напоминания
- Система достижений
- Хранение прогресса
- Поддержка Telegram на мобильных и десктопах

---

## 🧩 Структура проекта

```
Fartlek/
├── main.py                 # Точка входа
├── config.py               # Конфигурация
├── bot/
│   ├── application.py      # Настройка бота
│   └── handlers.py         # Обработчики команд
├── training/
│   ├── plans/
│   │   └── timed_fartlek_plan.py
│   └── sessions/
│       └── fartlek_session.py
├── user/
│   ├── user.py
│   ├── storage.py
│   └── achievements.py
├── messaging/
│   ├── coach.py
│   └── templates.py
├── audio/
│   ├── tts_service.py
│   └── audio_player.py
├── database/
│   └── sqlite_storage.py
├── utils/
│   └── logger.py
├── audio_cache/            # Кэш аудио
├── users.db                # База данных SQLite
└── requirements.txt
```

---

## 🚀 Установка и запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Slava_inc/fartlek.git
cd fartlek
```

### 2. Создай виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# или
venv\Scripts\activate      # Windows
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Настрой конфигурацию

Создай бота через [@BotFather](https://t.me/BotFather) и получи токен.

В файле `config.py`:

```python
TOKEN = "ВАШ_TELEGRAM_BOT_TOKEN"
YANDEX_API_KEY = "ВАШ_YANDEX_TTS_API_KEY"  # для озвучки
DB_PATH = "users.db"
```

### 5. Запусти бота

```bash
python main.py
```

---

## 🎙️ Как использовать

1. Напиши боту: `/start`
2. Запусти тренировку: `/fartlek`
3. Следуй подсказкам от голосового тренера
4. Получай достижения за прогресс

---

## 🧠 Пример тренировки

**Фортлек по времени (3 минуты в целях отладки):**

- Разминка — 5 мин
- Интервал 1 — 3 мин
- Отдых — 2 мин
- Интервал 2 — 4 мин
- Отдых — 2 мин
- Интервал 3 — 5 мин
- Отдых — 2 мин
- Финальный интервал — 3 мин
- Заминка — 3 мин

---

## 🏆 Достижения

- 🏁 Фортлек-стартер — первая тренировка
- 🔥 Пять подряд — 5 завершённых тренировок
- 🌙 Ночной бегун — тренировка после 22:00

---

## 🧰 Технологии

- Python 3.11+
- `python-telegram-bot` — для Telegram API
- `SQLite` — хранение данных

---

## 📦 Планы на будущее

- [ ] Голосовой тренер
- [ ] Интеграция с Strava
- [ ] Веб-интерфейс
- [ ] Поддержка Apple Watch
- [ ] Персональные планы
- [ ] Групповые челленджи

---

## 📄 Лицензия

MIT — свободно используй и улучшай.

---

## 🙌 Автор

Создано с ❤️ для бегунов и энтузиастов фитнеса.
