from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from quiz_data import get_question
from models import Session, User, add_score   # убедитесь, что add_score экспортирована

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat, question, opts, right = get_question()
    context.user_data["right"] = right
    kb = [[InlineKeyboardButton(opt, callback_data=f"ans_{opt}") for opt in opts]]
    if question.get("img"):
        await q.edit_message_media(
            media=InputMediaPhoto(question["img"], caption=f"Категория: {cat}\n{question}"),
            reply_markup=InlineKeyboardMarkup(kb)
        )
    else:
        await q.edit_message_text(f"Категория: {cat}\n{question}", reply_markup=InlineKeyboardMarkup(kb))

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    ans = q.data.replace("ans_", "")
    uid = q.from_user.id
    if ans == context.user_data.get("right"):
        add_score(uid, 10)
        txt = "✅ Правильно! +10"
    else:
        txt = f"❌ Неправильно. Правильный ответ: {context.user_data['right']}"
    kb = [[InlineKeyboardButton("Ещё вопрос", callback_data="play")]]
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))