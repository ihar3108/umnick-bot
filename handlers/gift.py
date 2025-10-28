from telegram import Update
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import add_score

GIFT_BONUS = 10

async def gift(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    now = datetime.utcnow()
    next_gift = ctx.user_data.get("next_gift")

    if next_gift and now < next_gift:
        wait = int((next_gift - now).total_seconds() / 60)
        await update.callback_query.answer(f"⏳ Подарок через {wait} мин", show_alert=True)
        return

    add_score(uid, GIFT_BONUS)
    ctx.user_data["next_gift"] = now + timedelta(hours=1)
    kb = [[InlineKeyboardButton("🎁 Забрать ещё через час", callback_data="gift")]]
    
    await update.callback_query.message.reply_text(
    "📋 Ежечасовый подарок:\n"
    "• Нажимай «🎁 Забрать» каждый час.\n"
    "• Получаешь +10 баллов.\n"
    "• Терпение = деньги!"
)