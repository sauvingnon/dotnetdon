import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.utils import resources
from app.states.subscription import SubscriptionState
from app.keyboards.inline import get_main_menu
from app.services.db import user_service
from app.helpers.failure_handler import failure_handler
from logger import logger

router = Router()

def extract_username(user):
    if user.username:
        return user.username
    elif user.first_name:
        return user.first_name
    else:
        return f"Unknown {user.id}"

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    try:
        user_name = extract_username(message.from_user)

        # Создание или получение пользователя
        try:
            user = await user_service.create_user(message.from_user.id, user_name)
        except Exception as e:
            logger.exception(f"Ошибка при создании пользователя {user_name}: {e}")
            await failure_handler(message)
            return

        if not user:
            await failure_handler(message)
            return

        # Устанавливаем FSM-состояние только после успешного создания пользователя
        await state.set_state(SubscriptionState.show_menu)

        await message.answer(resources.welcome_message_free)

        keyboard = get_main_menu(user)
        await message.answer("Выбери пункт меню:", reply_markup=keyboard)

    except Exception as e:
        logger.exception(f"Ошибка в /start: {e}")
        await failure_handler(message)
