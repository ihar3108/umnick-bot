from aiogram import Router, F, types
import random, asyncio
from db import add_stars

router = Router(name="fast_math")
fast_math_router = router

@router.callback_query(F.data == "menu_fastmath")
async def start_math(cb: types.CallbackQuery):
    a, b = random.randint(1, 10), random.randint(1, 10)
    ans = a + b
    await cb.message.answer(f"⏱  Реши за 5 сек: {a} + {b} = ?")
    await asyncio.sleep(5)
    await cb.message.answer(f"Ответ: {ans}. +2 ⭐ за участие!")
    await add_stars(cb.from_user.id, 2)