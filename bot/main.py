import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from dispatcher import setup_routers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

setup_routers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
