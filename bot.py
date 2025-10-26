import logging, os
from flask import Flask
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.start import start
from handlers.game import play, answer
from handlers.top import top
from handlers.payout import withdraw, paid
from handlers.admin import admin_handlers

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
app_flask = Flask(__name__)
@app_flask.route("/")
def index():
    return "Bot is alive", 200

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(play,    pattern="^play$"))
application.add_handler(CallbackQueryHandler(answer, pattern="^ans_"))
application.add_handler(CallbackQueryHandler(top,    pattern="^top$"))
application.add_handler(CallbackQueryHandler(withdraw,pattern="^withdraw$"))
application.add_handler(CallbackQueryHandler(paid,   pattern="^paid_"))
for h in admin_handlers():
    application.add_handler(h)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app_flask.run(host="0.0.0.0", port=8080), daemon=True).start()
    application.run_polling()