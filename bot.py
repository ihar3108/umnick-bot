import sys
import os
import logging
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor   # ← пул для Telegram-обработки

# ---------- Telegram & Flask ----------
from flask import Flask, request, send_from_directory
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    InlineQueryHandler
)

# ---------- наши модули ----------
from config import BOT_TOKEN
from handlers.start import start
from handlers.game import play, answer
from handlers.top import top
from handlers.payout import withdraw, paid
from handlers.admin import admin_handlers
from handlers.inline import inline_query

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

for h in admin_handlers():
    application.add_handler(h)

# ---------- Flask routes ----------
@app_flask.route("/")
def index():
    return "Bot is alive", 200

# ---------- синхронный webhook (без async) ----------
executor = ThreadPoolExecutor(max_workers=4)   # пул на 4 потока

@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """Синхронный webhook – выполняем Telegram-логику в пуле потоков"""
    json_data = request.get_json(force=True)
    logging.info(f"RAW update: {json_data}")          # можно убрать позже
    update = Update.de_json(json_data, application.bot)
    # запускаем обработку **в пуле** – не блокируем Flask
    executor.submit(application.process_update, update)
    return "ok", 200

@app_flask.route("/web/2048")
def webapp_2048():
    return send_from_directory("web/2048", "index.html")

# ---------- keep-alive (Render) ----------
def keep_alive():
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

# ---------- запуск ----------
if __name__ == "__main__":
    ext_url = os.getenv("RENDER_EXTERNAL_URL")

    if ext_url:                       # продакшн на Render
        # устанавливаем webhook (синхронно)
        webhook_url = f"{ext_url}/{BOT_TOKEN}"
        application.bot.set_webhook(webhook_url)
        logging.info(f"Webhook set to: {webhook_url}")

        # поток самопинга
        ka_thread = threading.Thread(target=keep_alive, daemon=True)
        ka_thread.start()

        # Flask-сервер (блокирующий, но в отдельном потоке)
        app_flask.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

    else:                             # локальный запуск
        logging.info("Running in development mode (polling)")
        application.run_polling()