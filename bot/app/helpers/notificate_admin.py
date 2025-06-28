import config
from aiogram.types import CallbackQuery

# Метод для уведомления админа
async def notificate_admin(message: str, callback: CallbackQuery):
    await callback.bot.send_message(config.ADMIN_ID, message)