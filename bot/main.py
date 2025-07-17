import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, BOT_TOKEN_TEST
from app.dispatcher_module import setup_routers
from aiogram.fsm.storage.memory import MemoryStorage
from app.keyboards.inline import commands

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())
# bot = Bot(token=BOT_TOKEN)
bot = Bot(token=BOT_TOKEN_TEST)

setup_routers(dp)

async def main():
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
