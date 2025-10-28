LOTTERY_PRICE = 50   # билет
LOTTERY_TIME  = "20:00"   # UTC

async def lottery_menu(update: Update, ctx):
    kb = [[InlineKeyboardButton(f"🎫 Купить билет – {LOTTERY_PRICE} баллов", callback_data="lottery_buy")]]
    await update.callback_query.message.reply_text(
        f"🎁 Розыгрыш 1 TON каждый день в {LOTTERY_TIME} UTC!\n"
        f"1 билет = {LOTTERY_PRICE} баллов. Чем больше билетов – тем выше шанс.",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def buy_ticket(update: Update, ctx):
    uid = update.effective_user.id
    with Session() as s:
        user = s.get(User, uid)
        if user.score < LOTTERY_PRICE:
            await update.callback_query.answer("Недостаточно баллов", show_alert=True)
            return
        user.score -= LOTTERY_PRICE
        # сохраняем билеты
        tickets = ctx.bot_data.get("lottery_tickets", {})
        tickets[uid] = tickets.get(uid, 0) + 1
        ctx.bot_data["lottery_tickets"] = tickets
        s.commit()
    await update.callback_query.answer("Билет куплен!")