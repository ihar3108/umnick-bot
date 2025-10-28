from aiogram import Router, F, types
from db import add_stars

router = Router(name="truefalse")
truefalse_router = router

@router.callback_query(F.data == "menu_truefalse")
async def start_tf(cb: types.CallbackQuery):
    await cb.message.answer("🧠 Правда или ложь?\n"
                           "Земля круглая – правда? Да/Нет")
    await add_stars(cb.from_user.id, 1)