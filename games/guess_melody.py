from aiogram import Router, F, types
from db import add_stars

router = Router(name="melody")
melody_router = router

@router.callback_query(F.data == "menu_melody")
async def start_melody(cb: types.CallbackQuery):
    await cb.message.answer("🎵 Угадай мелодию (пока текстовый режим).\n"
                           "Пример: «Битлз – Yesterday» – напиши в чат.")
    await add_stars(cb.from_user.id, 1)