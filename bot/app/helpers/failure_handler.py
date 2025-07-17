from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from app.helpers.notificate_admin import notificate_admin
import logging

# Логгер (если у тебя есть конфиг логгера — используй его)
logger = logging.getLogger(__name__)

async def failure_handler(error_msg: str, update: Message | CallbackQuery):
    """
    Универсальный хендлер ошибок — пишет пользователю, логирует и шлёт админу.
    :param error_msg: Текст ошибки, который пойдёт админу
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
            logger.warning("Не удалось отправить сообщение пользователю. Возможно, бот заблокирован.")

        # Шлём админу
        await notificate_admin(error_msg)

    except Exception as e:
        logger.exception("Ошибка внутри failure_handler: %s", str(e))

    # Печатаем в консоль (если без логгера)
    print(f"[ERROR] {error_msg}")
