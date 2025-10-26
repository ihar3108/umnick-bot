from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from quiz_data import get_question
from models import Session, User

async def play(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat, question, opts, right = get_question()
    ctx.user_data["right"] = right
    kb = [[InlineKeyboardButton(opt, callback_data=f"ans_{opt}") for opt in opts]]
    await q.edit_message_text(f"Категория: {cat}\n{question}", reply_markup=InlineKeyboardMarkup(kb))

async def answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q   = update.callback_query
    ans = q.data.replace("ans_","")
    uid = q.from_user.id
    if ans == ctx.user_data.get("right"):
        with Session() as s:
            s.get(User, uid).score += 10
            s.commit()
        txt = "✅ Правильно! +10"
    else:
        txt = f"❌ Неправильно. Правильный ответ: {ctx.user_data['right']}"
    kb = [[InlineKeyboardButton("Ещё вопрос", callback_data="play")]]
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))