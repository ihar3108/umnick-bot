from aiogram import Router, F, types

router = Router(name="referral")

async def handle_referral(uid: int, ref_id: str):
    # TODO: сохранить в БД / выдать звёзды
    print(f"referral: {uid} <- {ref_id}")

@router.callback_query(F.data == "menu_referral")
async def ref_link(cb: types.CallbackQuery):
    bot = cb.bot
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start={cb.from_user.id}"
    await cb.message.answer(
        f"👥 Отправь другу эту ссылку:\n{link}\n"
        f"Когда друг запустит бота – вы оба получите 10 ⭐!"
    )