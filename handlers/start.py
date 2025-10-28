from datetime import datetime, timedelta
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, WebAppInfo, ReplyKeyboardMarkup
)
from telegram.ext import ContextTypes
from models import Session, User
from config import REF_BONUS

BONUS_DAY = 50

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

        if user.created.date() == datetime.utcnow().date() and user.score == 0:
            user.score += BONUS_DAY
            context.user_data["next_gift"] = datetime.utcnow() + timedelta(hours=1)
            s.commit()

    # 1. обычная клавиатура
    kb = [
        [KeyboardButton("🎮 Играть 2048", web_app=WebAppInfo(url="https://umnick-bot-1.onrender.com/web/2048"))],
        [KeyboardButton("🎁 Забрать подарок (через 1 ч)")],
        [KeyboardButton("📲 Пригласить друга")],
    ]
    await update.message.reply_text(
        "🔥 Добро пожаловать в <b>Умник 3.0</b> – квиз, мемы, NFT и розыгрыши!\n\n"
        "📋 <b>Кратко о каждой игре:</b>\n\n"
        "🎮 <b>2048</b> – доведи плитку до 2048 и получи +200 баллов.\n"
        "🎁 <b>Подарок</b> – забирай +10 баллов каждый час.\n"
        "🏆 <b>Розыгрыш</b> – покупай билеты за 50 баллов и выиграй 1 TON в 20:00 UTC.\n"
        "🐱 <b>NFT</b> – купи уникальный аватар за баллы и поставь на профиль.\n"
        "🗣 <b>Голос</b> – я задам вопрос голосом, ты отвечаешь голосом – +15 баллов.\n"
        "📲 <b>Рулетка</b> – введи @bot рулетка в любом чате и выиграй баллы.\n"
        "💎 <b>Ачивки</b> – выполняй условия и получай стикеры «🔥 Огненный», «💎 Алмазный».\n\n"
        "Выбирай режим и играй!",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

    # 2. inline-клавиатура
    inline_kb = [
        [InlineKeyboardButton("🏆 Топ-100", callback_data="top"),
         InlineKeyboardButton("💰 Кошелёк", callback_data="withdraw")],
        [InlineKeyboardButton("🎁 Розыгрыш 1 TON", callback_data="lottery_menu")],
        [InlineKeyboardButton("🐱 NFT-магазин", callback_data="shop_menu")],
        [InlineKeyboardButton("🗣 Голосовой вопрос", callback_data="voice")]
    ]
    await update.message.reply_text(
        "Дополнительные действия:",
        reply_markup=InlineKeyboardMarkup(inline_kb)
    )