import asyncio, logging, os
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cat_reactions import CAT_REACTIONS
from games.millionaire import router as millionaire_router
from handlers.shop import shop_router
from referral import referral_router
from db import init_db
from games.fast_math import fast_math_router
from games.guess_melody import melody_router
from games.true_false import truefalse_router

API_TOKEN = os.getenv("BOT_TOKEN")   # добавишь в Render → Environment

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(millionaire_router)
dp.include_router(shop_router)
dp.include_router(referral_router)

@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    ref = m.text.split()[1] if len(m.text.split()) > 1 else None
    if ref:
        await referral_router.handle_referral(m.from_user.id, ref)
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎯 Кто хочет стать миллионером?", callback_data="menu_millionaire")],
    [InlineKeyboardButton(text="⚡ Быстрый счёт", callback_data="menu_fastmath")],
    [InlineKeyboardButton(text="🎵 Угадай мелодию", callback_data="menu_melody")],
    [InlineKeyboardButton(text="🧠 Правда/Ложь", callback_data="menu_truefalse")],
    [InlineKeyboardButton(text="🛍️ Магазин (⭐)", callback_data="menu_shop")],
    [InlineKeyboardButton(text="👥 Приведи друга (+10 ⭐)", callback_data="menu_referral")]
])
    await m.answer(
        CAT_REACTIONS["welcome"],
        reply_markup=kb,
        parse_mode="Markdown"
    )

async def main():
    await dp.start_polling(bot, skip_updates=True)
async def main():
    await init_db()
    dp.include_router(fast_math_router)
    dp.include_router(melody_router)
    dp.include_router(truefalse_router)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())