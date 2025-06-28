import config

# Метод для уведомления админа
async def notificate_admin(message: str):
    from main import bot
    await bot.send_message(config.ADMIN_ID, message)