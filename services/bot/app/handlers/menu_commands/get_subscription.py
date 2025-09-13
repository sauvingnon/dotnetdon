# Получить бесплатный доступ
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from services.db import user_service
from helpers.send_access_for_user import grant_access
from helpers.failure_handler import failure_handler
from logger import logger

router = Router()

@router.callback_query(F.data == "get_subscription", SubscriptionState.show_menu)
async def buy_subscription(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        await callback.message.delete()
        await callback.answer()

        user = await user_service.get_user_for_tg_id(user_id)
        if user is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: не найден в БД при попытке старта триала.")
            return

        if user.test_used:
            await callback.message.answer(
                "Вы уже использовали свой пробный период. Для возобновления доступа приобретите подписку."
            )
            logger.info(f"Пользователь {user_id} попытался взять триал повторно.")
            return

        # Даем триал
        await grant_access(callback, state, True)
        logger.info(f"Пользователю {user_id} предоставлен пробный доступ на 3 дня.")
        
    except Exception as e:
        logger.error(f"Ошибка при старте триала для пользователя {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при попытке дать пробный доступ.")

    

