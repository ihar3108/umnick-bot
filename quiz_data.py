# -*- coding: utf-8 -*-
from quiz_data import get_question

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat, question, opts, right, img = get_question()   # ← теперь 5 элементов
    context.user_data["right"] = right

    kb = [[InlineKeyboardButton(opt, callback_data=f"ans_{opt}") for opt in opts]]

    if img:        # мем-вопрос с картинкой
        await q.edit_message_media(
            media=InputMediaPhoto(img, caption=f"Категория: {cat}\n{question}"),
            reply_markup=InlineKeyboardMarkup(kb)
        )
    else:          # обычный текст
        await q.edit_message_text(
            f"Категория: {cat}\n{question}",
            reply_markup=InlineKeyboardMarkup(kb)
        )