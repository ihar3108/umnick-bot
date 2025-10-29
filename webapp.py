from aiogram import Router, F, types
from aiogram.types import WebAppInfo

webapp_router = Router(name="webapp")

# заглушка-обработчик, если WebApp ещё не реализован
@webapp_router.message(F.content_type == "web_app_data")
async def web_data(msg: types.Message):
    await msg.answer("WebApp ещё в разработке 😺")