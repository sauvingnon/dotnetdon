from aiogram import Dispatcher
from app.handlers import menu, start, send_links_for_platform, check_dowloand
from app.handlers.menu_commands import buy_subscription, handle_plan_choice, help, start_trial
from app.handlers.menu_commands import about_us 

def setup_routers(dp: Dispatcher):
    dp.include_router(menu.router)
    dp.include_router(start.router)
    dp.include_router(send_links_for_platform.router)
    dp.include_router(buy_subscription.router)
    dp.include_router(about_us.router)
    dp.include_router(handle_plan_choice.router)
    dp.include_router(help.router)
    dp.include_router(start_trial.router)
    dp.include_router(check_dowloand.router)