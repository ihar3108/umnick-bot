import qrcode, io, requests, datetime as dt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import Session, User, Payout
from config import WITHDRAW_MIN, TON_RATE_URL

def ton_rate():
    try:
        return int(requests.get(TON_RATE_URL).json()["the-open-network"]["rub"])
    except:
        return 300

async def withdraw(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    with Session() as s:
        score = s.get(User, uid).score
    if score < WITHDRAW_MIN:
        await q.edit_message_text(f"❗️ Минимум {WITHDRAW_MIN} баллов.")
        return
    ton  = round(score / 1_000, 3)
    addr = "YOUR_TON_WALLET"          # подмени на свой
    link = f"ton://transfer/{addr}?amount={int(ton*1e9)}&text={uid}"
    img  = qrcode.make(link)
    buf  = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    kb   = [[InlineKeyboardButton("✅ Я перевёл", callback_data=f"paid_{uid}_{score}")]]
    await q.edit_message_text(
        f"📤 Для вывода <b>{ton} TON</b> (~{int(ton*ton_rate())} ₽)\n"
        f"Отсканируй QR или нажми кнопку ниже.", parse_mode="HTML")
    await q.message.reply_photo(buf, reply_markup=InlineKeyboardMarkup(kb))

async def paid(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q   = update.callback_query
    uid, score = map(int, q.data.split("_")[1:])
    with Session() as s:
        user = s.get(User, uid)
        if user.score < score:
            await q.answer("Баллы уже потрачены", show_alert=True)
            return
        user.score -= score
        s.add(Payout(uid=uid, amount=score, wallet="USER_TON", status="done"))
        s.commit()
    await q.edit_message_text("✅ Выплачено. Оплату проверь вручную.")