from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="shop")
shop_router = router          # ЭКСПОРТ

@router.callback_query(F.data == "menu_shop")
async def shop_menu(cb: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕶️ Очки кота – 10 ⭐", callback_data="star_10_glasses")],
        [InlineKeyboardButton(text="💡 50/50 – 5 ⭐",      callback_data="star_5_hint")]
    ])
    await cb.message.answer("🛍️ Выберите товар:", reply_markup=kb)
