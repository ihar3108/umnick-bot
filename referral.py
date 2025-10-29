from aiogram import Router, F, types
from db import add_stars

ref_router = Router(name="referral")

@ref_router.callback_query(F.data == "menu_referral")
async def ref_link(cb: types.CallbackQuery):
    bot = cb.bot
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start={cb.from_user.id}"
    await cb.message.answer(f"👥 Отправь другу:\n{link}\nЗа каждого друга – 10 ⭐!")

async def add_ref(uid: int, ref_id: int):
    """+10 ⭐ обоим за реферал"""
    await add_stars(ref_id, 10)
    await add_stars(uid, 10)