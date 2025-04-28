import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.routers import user_router
from config import BOT_TOKEN
from app.handlers import start

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(user_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
