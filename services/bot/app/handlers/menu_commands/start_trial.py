from aiogram import Router, F
from app.states.subscription import SubscriptionState
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.helpers.send_access_for_user import grant_access
from logger import logger

router = Router()

@router.callback_query(F.data == "start_trial", SubscriptionState.show_menu)
async def start_trial(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        await callback.message.delete()
        await callback.answer()

        # Даем триал
        await grant_access(callback, state)
        logger.info(f"Пользователю {user_id} предоставлен пробный доступ.")
        
    except Exception as e:
        logger.error(f"Ошибка при старте триала для пользователя {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при попытке дать пробный доступ.")
