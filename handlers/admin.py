from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from models import Session, User, Payout

async def stat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    with Session() as s:
        users = s.query(User).count()
        total= sum(u.score for u in s.query(User).all())
        payouts= s.query(Payout).filter_by(status="done").count()
    await update.message.reply_text(
        f"📊 Пользователей: {users}\n"
        f"Общий балланс: {total:,}\n"
        f"Выплат: {payouts}")

async def add(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args or not ctx.args[0].isdigit():
        await update.message.reply_text("Usage: /add 1000")
        return
    uid = update.effective_user.id
    pts = int(ctx.args[0])
    with Session() as s:
        s.get(User, uid).score += pts
        s.commit()
    await update.message.reply_text("✅ Баллы добавлены")

async def broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /broadcast text")
        return
    text = " ".join(ctx.args)
    with Session() as s:
        for u in s.query(User).all():
            try:
                await ctx.bot.send_message(u.uid, text)
            except:
                pass
    await update.message.reply_text("✅ Рассылка завершена")

def admin_handlers():
    return [CommandHandler("stat", stat),
            CommandHandler("add", add),
            CommandHandler("broadcast", broadcast)]