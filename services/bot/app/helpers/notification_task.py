from datetime import datetime, timedelta
from app.services.db import key_service
import asyncio
from app.keyboards.inline import soon_expire_key_message, expire_key_message, extend_key_keyboard
from logger import logger
from config import WARNING_DAYS

async def notification_loop(bot):
    while True:
        try:
            await process_notifications(bot)
            logger.info(f"Задача уведомления пользователей о истекших ключах завершился без ошибок.")
        except Exception as e:
            logger.error(f"Ошибка в notification_loop: {e}")
        await asyncio.sleep(3600)

async def process_notifications(bot):
    
    now = datetime.utcnow()

    # ключи почти истекают (за 3 дня)
    notify_keys = await key_service.get_keys_for_notifications()

    logger.info(f"Запущена задача уведомления пользователей о истекших ключах. Получено {len(notify_keys)} ключей")

    for key in notify_keys:

        days_left = (key.active_until - now).days

        # 1. Ключ скоро истечет
        if 0 < days_left <= WARNING_DAYS:
            
            try:
                key.warned = True  # ставим флаг что уведомили
                await key_service.update_key(key)
                await bot.send_message(chat_id=key.user.tg_id, text=soon_expire_key_message(key.sub_url, days_left), reply_markup=extend_key_keyboard(key.id))
                logger.info(f"Успешно отправлено уведомление пользователю {key.user.tg_username} об истечении подписки через {days_left} дней")
                await asyncio.sleep(0.5)  # пауза, чтобы не забанили
            except Exception as e:
                logger.error(f"Не удалось отправить пользователю {key.user.tg_id}: {e}")

        # 2. Ключ уже истек
        elif days_left <= 0:
            
            try:
                key.expired_warned = True  # ставим флаг что уведомили
                await key_service.update_key(key)
                await bot.send_message(chat_id=key.user.tg_id, text=expire_key_message(key.sub_url), reply_markup=extend_key_keyboard(key.id))
                logger.info(f"Успешно отправлено уведомление пользователю {key.user.tg_username} об истечении подписки")
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Не удалось отправить пользователю {key.user.tg_id}: {e}")

