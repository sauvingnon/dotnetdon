# Получение пробного доступа
from aiogram import Router, F
from app.states.subscription import Step
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import user_service
from app.helpers.choose_platform import choose_platform
from app.helpers.failure_handler import failure_handler

router = Router()

@router.callback_query(F.data == "start_trial", Step.show_menu)
async def start_trial(callback: CallbackQuery, state: FSMContext):
    # Проверим, а этот пользователь уже брал триал?
    await callback.message.delete()
    user = await user_service.get_user_for_tg_id(callback.from_user.id)

    if not user:
        failure_handler("Ошибка при получении триал-доступа.", callback=callback)
        return

    # Если триал уже был использован, то увы, больше нет
    if user.test_used == True:
        await callback.message.answer("Вы уже использовали свой пробный период. Для возобновления доступа приобретите подписку.")
        return
    
    # Если не был, то дадим ему триал на 3 дня

    await state.update_data(user_get_trial=True)
    
    await state.set_state(Step.choose_platform)

    await choose_platform(callback, state)

    await callback.answer()

