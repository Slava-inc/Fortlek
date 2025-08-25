# bot/application.py
from telegram.ext import Application, CommandHandler
from bot.handlers import start, fartlek

def create_bot(token: str):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fartlek", fartlek))
    return app