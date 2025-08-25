# main.py
import sys
import os

# Добавляем корневую папку в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.application import create_bot
from config import TOKEN

if __name__ == "__main__":
    app = create_bot(TOKEN)
    print("Бот запущен...")
    app.run_polling()