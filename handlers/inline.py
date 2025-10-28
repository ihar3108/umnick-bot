import random
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

async def inline_query(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if query.lower() in ("рулетка", "р", ""):
        number = random.randint(1, 6)
        results.append(
            InlineQueryResultArticle(
                id=str(random.randint(1, 10000)),
                title=f"🎲 Крутить рулетку ({number})",
                input_message_content=InputTextMessageContent(
                    f"🎲 Выпало: {number}"
                )
            )
        )

    await update.inline_query.answer(results, cache_time=1)