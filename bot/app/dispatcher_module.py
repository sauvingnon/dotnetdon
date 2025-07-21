from aiogram import Dispatcher
from app.handlers import menu, start, send_links_for_platform, check_dowloand
from app.handlers.menu_commands import buy_subscription, handle_plan_choice, help, start_trial
from app.handlers.menu_commands import about_us, admin_panel, instruction, my_subscriptions
from app.handlers.admin_commands import add_admin_user
from app.handlers.payment import start_payment_process, check_payment
from app.handlers.email import confirm_email, get_email

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
    dp.include_router(admin_panel.router)
    dp.include_router(add_admin_user.router)
    dp.include_router(check_payment.router)
    dp.include_router(start_payment_process.router)
    dp.include_router(confirm_email.router)
    dp.include_router(get_email.router)
    dp.include_router(instruction.router)
    dp.include_router(my_subscriptions.router)