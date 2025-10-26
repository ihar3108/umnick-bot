from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import Session, User

def top_text():
    with Session() as s:
        leaders = s.query(User).order_by(User.score.desc()).limit(15).all()
    text = "🏆 ТОП-15:\n"
    for n, u in enumerate(leaders, 1):
        text += f"{n}. <b>{u.full_name}</b> – {u.score:,}\n"
    return text

async def top(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(top_text(), parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Меню", callback_data="menu")]]))