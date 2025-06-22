from app.helpers.notificate_admin import notificate_admin
from aiogram.types import Message, CallbackQuery

# Метод для обработки ошибок
async def failure_handler(message: str, callback: CallbackQuery):
    await callback.message.answer('Что-то пошло не так, напиши в ' + ' [поддержку](https://t.me/sauvingnon)', parse_mode='Markdown')
    print(message)
    await notificate_admin(message)