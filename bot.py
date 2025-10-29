import asyncio, logging, os
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    MenuButtonWebApp, WebAppInfo, LabeledPrice, PreCheckoutQuery
)
from cat_reactions import CAT_REACTIONS
from db import init_db, add_ref
from webapp import webapp_router          # WebApp-роутер
from shop import shop_router              # Stars-магазин
from referral import ref_router           # рефералы

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- подключаем роутеры ---
dp.include_router(webapp_router)
dp.include_router(shop_router)
dp.include_router(ref_router)

# --- главное меню ---
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "your.domain")
MAIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Вирусный Миллионер",
                          web_app=WebAppInfo(url=f"https://{os.getenv('RENDER_EXTERNAL_URL', 'umnick-bot.onrender.com')}:10000/web"))],
    [InlineKeyboardButton(text="🎵 Песня за 15 сек", callback_data="menu_melody")],
    [InlineKeyboardButton(text="🧠 IQ-Бластер", callback_data="menu_iq")],
    [InlineKeyboardButton(text="🛍️ NFT-магазин (⭐)", callback_data="menu_shop")],
    [InlineKeyboardButton(text="👥 Приведи друга (+10 ⭐)", callback_data="menu_referral")]
])


@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    ref = m.text.split()[1] if len(m.text.split()) > 1 else None
    if ref:
        await add_ref(m.from_user.id, int(ref))

    await bot.set_chat_menu_button(
        chat_id=m.chat.id,
        menu_button=MenuButtonWebApp(text="🚀 Играть",
                                     web_app=WebAppInfo(url=f"https://{os.getenv('RENDER_EXTERNAL_URL', 'umnick-bot.onrender.com')}:10000/web"))
    )
    await m.answer_photo(
        photo="https://i.imgur.com/QwebotN.gif",   # кот в очках
        caption=CAT_REACTIONS["welcome"],
        reply_markup=MAIN_KB
    )


@dp.callback_query(F.data == "menu_melody")
async def melody(cb: types.CallbackQuery):
    audios = [
       {"file": "audio/beatles.wav", "answer": "The Beatles"},
{"file": "audio/queen.wav",  "answer": "Queen"}
    ]
    a = audios[0]
    await cb.message.answer_audio(
        audio=types.FSInputFile(a["file"]),
        caption="🎵 Угадай исполнителя (пиши в чат)"
    )


@dp.callback_query(F.data == "menu_iq")
async def iq(cb: types.CallbackQuery):
    await cb.message.answer(
        "🧠 Открой игру ниже",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🧩 IQ-Бластер",
                                      web_app=WebAppInfo(url=f"https://{RENDER_URL}/iq"))]],
            resize_keyboard=True, one_time_keyboard=True
        )
    )


@dp.message(F.text == "/stars")
async def stars_demo(m: types.Message):
    await bot.send_invoice(
        chat_id=m.from_user.id,
        title="🕶️ NFT-очки кота",
        description="Эксклюзивный скин для аватара",
        payload="nft_glasses",
        currency="XTR",
        prices=[LabeledPrice(label="Очки", amount=10)]
    )


@dp.pre_checkout_query()
async def pre_checkout(q: PreCheckoutQuery):
    await q.answer(ok=True)


@dp.message(F.successful_payment)
async def got_payment(m: types.Message):
    await m.answer("✅ Оплачено! Скин скоро появится в WebApp.")


# --- запуск ---
async def main():
    await init_db()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    # в самый низ файла, ПОСЛЕ всего кода
from aiohttp import web
import threading

def run_dummy_server():
    app = web.Application()
    app.router.add_get("/", lambda _: web.Response(text="Умник 3.0 OK"))
    runner = web.AppRunner(app)
    threading.Thread(target=lambda: web.run_app(runner, host="0.0.0.0", port=10000), daemon=True).start()

run_dummy_server()
# === DUMMY-WEB: убираем «No open ports detected» ===
from aiohttp import web
import threading, asyncio

async def dummy_handler(request):
    return web.Response(text="Умник 3.0 OK")

def run_dummy_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()
    app.router.add_get("/", dummy_handler)
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    loop.run_until_complete(site.start())
    loop.run_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()