PRICES = {1: 100, 2: 200, 3: 500}   # уровень: цена

async def shop_menu(update: Update, ctx):
    kb = [
        [InlineKeyboardButton(f"🐱 Уровень 1 – 100 баллов", callback_data="nft_1")],
        [InlineKeyboardButton(f"🦊 Уровень 2 – 200 баллов", callback_data="nft_2")],
        [InlineKeyboardButton(f"🐉 Уровень 3 – 500 баллов", callback_data="nft_3")]
    ]
    await update.callback_query.message.reply_text(
        "Купи уникальный аватар-НФТ – его больше никто не получит!",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def buy_nft(update: Update, ctx):
    level = int(update.callback_query.data.split("_")[1])
    price = PRICES[level]
    uid   = update.effective_user.id
    with Session() as s:
        user = s.get(User, uid)
        if user.score < price:
            await update.callback_query.answer("Недостаточно баллов", show_alert=True)
            return
        user.score -= price
        # генерируем уникальную картинку (ниже)
        img_url = f"https://api.dicebear.com/7.x/bottts-neutral/png?seed={uid}{level}"
        s.commit()
    await update.callback_query.message.reply_photo(
        photo=img_url,
        caption=f"🎉 Уровень {level} НФТ – ваш! Можете ставить его на аватар."
    )