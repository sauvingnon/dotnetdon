from aiogram import Router
from app.handlers import choose_platform, send_links_for_platform, start, check_dowloand

router = Router()

# Регистрируем сюда все роутеры
router.include_routers(
    start.router,
    send_links_for_platform.router,
    choose_platform.router,
    check_dowloand.router
)
