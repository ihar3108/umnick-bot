from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import Session, User
from config import REF_BONUS, CHANNEL_ID

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    name = update.effective_user.full_name
    ref  = int(ctx.args[0]) if ctx.args and ctx.args[0].isdigit() else None

    with Session() as s:
        user = s.get(User, uid)
        if not user:
            user = User(uid=uid, full_name=name, username=update.effective_user.username, ref=ref)
            s.add(user)
            if ref and (ref_user := s.get(User, ref)):
                ref_user.score += REF_BONUS[1]
                user.score     += REF_BONUS[0]
            s.commit()

    kb = [[InlineKeyboardButton("🎮 Играть", callback_data="play")],
          [InlineKeyboardButton("📊 Топ", callback_data="top")],
          [InlineKeyboardButton("💰 Вывести", callback_data="withdraw")],
          [InlineKeyboardButton("⭐️ Купить Premium", callback_data="premium")]]
    await update.message.reply_text(
        f"Привет, {name}! За каждые 1 000 баллов – 1 TON.\n"
        f"Твоя реф-ссылка: https://t.me/{ctx.bot.username}?start={uid}",
        reply_markup=InlineKeyboardMarkup(kb))