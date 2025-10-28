import sys, os, logging, threading, time, requests, asyncio
from flask import Flask, request, send_from_directory
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, InlineQueryHandler
)

from config import BOT_TOKEN
from handlers.voice import voice_question, voice_answer
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
# ---------- голосовые вопросы ----------
application.add_handler(CommandHandler("voice", voice_question))
application.add_handler(MessageHandler(filters.VOICE, voice_answer))
for h in admin_handlers():
    application.add_handler(h)

# ---------- Flask routes ----------
@app_flask.route("/")
def index():
    return "Bot is alive", 200

# ---------- webhook: синхронный вход, async-обработка в event-loop ----------
# ---------- webhook: синхронный вход, async-обработка в event-loop ----------
@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    logging.info(f"RAW update: {json_data}")
    update = Update.de_json(json_data, application.bot)

    # запускаем корутину в **уже существующем** loop приложения
    asyncio.run_coroutine_threadsafe(
        application.process_update(update),
        application._loop          # ← рабочий loop после application.start()
    )
    return "ok", 200

# ---------- запуск ----------
# ---------- запуск (async) ----------
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


if __name__ == "__main__":
    asyncio.run(main())