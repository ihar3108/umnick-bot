from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json, random, pathlib
from cat_reactions import CAT_REACTIONS

router = Router(name="millionaire")

QUESTIONS = json.loads(
    pathlib.Path("data/questions.json").read_text(encoding="utf8")
)

@router.callback_query(F.data == "menu_millionaire")
async def start_game(cb: types.CallbackQuery):
    q = random.choice(QUESTIONS)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=a, callback_data=f"mil_{i}_{q['correct']}")] 
        for i, a in enumerate(q["answers"])
    ])
    await cb.message.answer(f"💰 Вопрос на 100 ⭐:\n{q['question']}", reply_markup=kb)

@router.callback_query(F.data.startswith("mil_"))
async def answer(cb: types.CallbackQuery):
    _, user_ans, correct = cb.data.split("_")
    if user_ans == correct:
        await cb.answer("😺 +1 ⭐", show_alert=True)
    else:
        await cb.answer("😿 Неверно", show_alert=True)