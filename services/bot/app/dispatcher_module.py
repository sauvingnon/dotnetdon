from aiogram import Dispatcher
from app.handlers import menu, start, send_links_for_platform, check_dowloand
from app.handlers.menu_commands import help, start_trial
from app.handlers.menu_commands import admin_panel, instruction, service_rules
from app.handlers.admin_commands import add_admin_user

def setup_routers(dp: Dispatcher):
    dp.include_router(menu.router)
    dp.include_router(start.router)
    dp.include_router(send_links_for_platform.router)
    dp.include_router(help.router)
    dp.include_router(start_trial.router)
    dp.include_router(check_dowloand.router)
    dp.include_router(admin_panel.router)
    dp.include_router(add_admin_user.router)
    dp.include_router(instruction.router)
    dp.include_router(service_rules.router)