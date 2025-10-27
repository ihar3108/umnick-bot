from datetime import datetime, timedelta
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, WebAppInfo, ReplyKeyboardMarkup
)
from telegram.ext import ContextTypes
from models import Session, User
from config import REF_BONUS, CHANNEL_ID   # если используете

BONUS_DAY = 50
BONUS_HOUR = 10


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.full_name
    ref = int(context.args[0]) if context.args and context.args[0].isdigit() else None

    with Session() as s:
        user = s.get(User, uid)
        if not user:
            user = User(
                uid=uid,
                full_name=name,
                username=update.effective_user.username,
                ref=ref
            )
            s.add(user)
            if ref and (ref_user := s.get(User, ref)):
                ref_user.score += REF_BONUS[1]
                user.score += REF_BONUS[0]
            s.commit()

        # ежедневный/ежечасовый бонус только при первом старте
        if user.created.date() == datetime.utcnow().date() and user.score == 0:
            user.score += BONUS_DAY
            context.user_data["next_gift"] = datetime.utcnow() + timedelta(hours=1)
            s.commit()

    # основная клавиатура (постоянная)
    kb = [
        [KeyboardButton("🎮 Играть 2048", web_app=WebAppInfo(url="https://umnick-bot-1.onrender.com/web/2048"))],
        [KeyboardButton("🎁 Забрать подарок (через 1 ч)", callback_data="gift")],
        [KeyboardButton("📲 Пригласить друга (+20)", switch_inline_query="")],
        [KeyboardButton("🏆 Топ-100", callback_data="top"),
         KeyboardButton("💰 Кошелёк", callback_data="wallet")]
    ]

    await update.message.reply_text(
        f"🔥 Привет, {name}!\n"
        f"Тебе начислено <b>{BONUS_DAY}</b> баллов + ежечасовой подарок!\n"
        f"За 1 000 баллов – 1 TON. Рефералка 20/10.",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True),
        parse_mode="HTML"
    )