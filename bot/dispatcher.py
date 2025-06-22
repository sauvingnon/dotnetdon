from aiogram import Dispatcher
from app.handlers import menu, start

def setup_routers(dp: Dispatcher):
    dp.include_router(menu.router)
    dp.include_router(start.router)