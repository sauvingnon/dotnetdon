import asyncio
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from app.dispatcher_module import setup_routers
from aiogram.fsm.storage.memory import MemoryStorage
from app.keyboards.inline import commands
from logger import logger
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk import capture_exception

# Логи в Sentry
sentry_logging = LoggingIntegration(
    level=None,        # все уровни передаем
    event_level="INFO" # только ошибки будут как события
)

# Подготовка Sentry
sentry_sdk.init(
    dsn="https://51514aae0f917f7ae3c3fb747d8b5e0a@o4509921859076096.ingest.de.sentry.io/4509921886928976",
    environment="bot",
    send_default_pii=False,  # отключаем автоматическую отправку личных данных
    integrations=[sentry_logging, AsyncioIntegration()]
)

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=BOT_TOKEN)

async def main():
    logger.info("Бот запущен.")
    setup_routers(dp)
    dp.errors.handlers.append(errors_handler)
    await bot.set_my_commands(commands)
    # asyncio.create_task(notification_loop(bot))
    await dp.start_polling(bot)

async def errors_handler(update: types.Update, exception: Exception):
    # Ловим все ошибки и отправляем в Sentry
    capture_exception(exception)
    return True  # чтобы Aiogram не ругался

if __name__ == "__main__":
    asyncio.run(main())
