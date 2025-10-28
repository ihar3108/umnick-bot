from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json, random, pathlib
from db import add_stars, get_stars

router = Router(name="millionaire")
millionaire_router = router

QUESTIONS = json.loads(pathlib.Path("data/questions.json").read_text(encoding="utf8"))
PRIZES = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

class UserState:
    def __init__(self):
        self.q_i = 0
        self.used_50 = False
        self.used_audience = False
        self.used_friend = False

states = {}   # user_id -> UserState

@router.callback_query(F.data == "menu_millionaire")
async def start_game(cb: types.CallbackQuery):
    uid = cb.from_user.id
    states[uid] = UserState()
    await ask_question(cb)

@router.callback_query(F.data.startswith("mil_"))
async def answer(cb: types.CallbackQuery):
    uid = cb.from_user.id
    st = states.get(uid)
    if not st:
        await cb.message.answer("Игра не найдена – нажмите /start")
        return

    _, user_ans, correct = cb.data.split("_")
    if user_ans == correct:
        prize = PRIZES[st.q_i]
        await cb.answer(f"✅ Верно! Ваш счёт: {prize} ⭐")
        st.q_i += 1
        if st.q_i == 15:
            await add_stars(uid, 1000000)
            await cb.message.answer("🎉 Поздравляем! Вы стали МИЛЛИОНЕРОМ! +1 000 000 ⭐")
            states.pop(uid, None)
        else:
            await ask_question(cb)
    else:
        await cb.message.answer(f"❌ Неверно. Вы выиграли {PRIZES[st.q_i-1] if st.q_i else 0} ⭐")
        states.pop(uid, None)

@router.callback_query(F.data == "mil_50")
async def hint_50(cb: types.CallbackQuery):
    uid = cb.from_user.id
    st = states.get(uid)
    if not st or st.used_50:
        await cb.answer("50/50 уже использовано")
        return
    stars = await get_stars(uid)
    if stars < 5:
        await cb.answer("Недостаточно ⭐ (нужно 5)")
        return
    await add_stars(uid, -5)
    st.used_50 = True
    # удалим 2 неверных ответа (упрощённо)
    await cb.answer("50/50 применён")

async def ask_question(cb: types.CallbackQuery):
    st = states[cb.from_user.id]
    q = random.choice(QUESTIONS)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=a, callback_data=f"mil_{i}_{q['correct']}")] for i, a in enumerate(q["answers"])
    ] + [[InlineKeyboardButton(text="💡 50/50 (5 ⭐)", callback_data="mil_50")]])
    await cb.message.answer(f"💰 Вопрос {st.q_i + 1} на {PRIZES[st.q_i]} ⭐:\n{q['question']}", reply_markup=kb)