import sys
import os
import logging
import threading
import time
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ---------- Telegram & Flask ----------
from flask import Flask, request, send_from_directory
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, InlineQueryHandler
)

# ---------- наши модули ----------
from config import BOT_TOKEN
from handlers.voice import voice_question, voice_answer
from handlers.start import start
from handlers.game import play, answer
from handlers.top import top
from handlers.payout import withdraw, paid
from handlers.admin import admin_handlers
from handlers.inline import inline_query

# ---------- ОТДЕЛЬНЫЙ event-loop для Telegram-задач ----------
_telegram_loop = None   # будет инициализован ниже

def _init_telegram_loop():
    """Создаёт event-loop в отдельном потоке и хранит его."""
    global _telegram_loop
    _telegram_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_telegram_loop)
    _telegram_loop.run_forever()

# запускаем поток с loop при импорте
_telegram_thread = threading.Thread(target=_init_telegram_loop, daemon=True)
_telegram_thread.start()

# ---------- настройки ----------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

app_flask = Flask(__name__)

# ---------- Telegram handlers ----------
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(play, pattern="^play$"))
application.add_handler(CallbackQueryHandler(answer, pattern="^ans_"))
application.add_handler(CallbackQueryHandler(top, pattern="^top$"))
application.add_handler(CallbackQueryHandler(withdraw, pattern="^withdraw$"))
application.add_handler(CallbackQueryHandler(paid, pattern="^paid_"))
application.add_handler(InlineQueryHandler(inline_query))
# ---------- голосовые вопросы ----------
application.add_handler(CommandHandler("voice", voice_question))
application.add_handler(MessageHandler(filters.VOICE, voice_answer))
for h in admin_handlers():
    application.add_handler(h)

# ---------- Flask routes ----------
@app_flask.route("/")
def index():
    return "Bot is alive", 200

# ---------- webhook: синхронный вход, async-обработка в отдельном loop ----------
@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    logging.info(f"RAW update: {json_data}")
    update = Update.de_json(json_data, application.bot)

    # ставим задачу в отдельный loop – не трогаем loop Flask
    _telegram_loop.call_soon_threadsafe(
        lambda: asyncio.create_task(application.process_update(update))
    )
    return "ok", 200

@app_flask.route("/web/2048")
def webapp_2048():
    return send_from_directory("web/2048", "index.html")

# ---------- keep-alive (Render) ----------
def keep_alive():
    """Фоновый самопинг для Render (без блокировки)"""
    url = os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        return
    while True:
        try:
            resp = requests.get(url, timeout=10)
            logging.info(f"Keep-alive ping: {resp.status_code}")
        except Exception as e:
            logging.error(f"Keep-alive error: {e}")
        time.sleep(300)          # 5 мин

# ---------- запуск (async) ----------
async def main():
    ext_url = os.getenv("RENDER_EXTERNAL_URL")

    if ext_url:                       # продакшн на Render
        # 1. запускаем Application (создаётся event-loop)
        await application.initialize()
        await application.start()

        # 2. ставим webhook
        webhook_url = f"{ext_url}/{BOT_TOKEN}"
        await application.bot.set_webhook(webhook_url)
        logging.info(f"Webhook set to: {webhook_url}")

        # 3. поток самопинга
        ka_thread = threading.Thread(target=keep_alive, daemon=True)
        ka_thread.start()

        # 4. Flask-блок (блокирующий, но в отдельном потоке)
        app_flask.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

    else:                             # локальный polling
        await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())