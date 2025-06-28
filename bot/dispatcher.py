from aiogram import Dispatcher
from app.handlers import menu, start, send_links_for_platform, choose_platform, check_dowloand

def setup_routers(dp: Dispatcher):
    dp.include_router(menu.router)
    dp.include_router(start.router)
    dp.include_router(send_links_for_platform.router)
    dp.include_router(choose_platform.router)
    dp.include_router(check_dowloand.router)