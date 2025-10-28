# handlers/achievements.py
from telegram import Update
from telegram.ext import ContextTypes

async def achievements_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ачивки пока в разработке 🚧")