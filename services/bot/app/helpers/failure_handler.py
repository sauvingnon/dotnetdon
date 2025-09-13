from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from logger import logger


async def failure_handler(update: Message | CallbackQuery):
    """
    Универсальный хендлер ошибок — пишет пользователю и логирует.
    :param update: либо Message, либо CallbackQuery
    """
    try:
        # Определяем, куда отвечать
        if isinstance(update, CallbackQuery):
            chat_id = update.from_user.id
        else:
            chat_id = update.chat.id

        # Пробуем отправить сообщение пользователю
        try:
            await update.bot.send_message(
                chat_id=chat_id,
                text='Что-то пошло не так, напиши в [поддержку](https://t.me/sauvingnon)',
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except TelegramBadRequest:
            logger.error("Не удалось отправить сообщение пользователю. Возможно, бот заблокирован.")

    except Exception as e:
        logger.exception("Ошибка внутри failure_handler: %s", str(e))
