# bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from training.sessions.fartlek_session import TimedFartlekSession
from database.sqlite_storage import SQLiteUserStorage
from config import DB_PATH

storage = SQLiteUserStorage(DB_PATH)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой беговой коуч. Жми /fartlek")

async def fartlek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = TimedFartlekSession(update.effective_user.id, context, storage)
    await session.start()