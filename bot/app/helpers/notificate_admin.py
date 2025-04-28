import config
from main import bot

# Метод для уведомления админа
async def notificate_admin(message: str):
    await bot.send_message(config.ADMIN_ID, message)