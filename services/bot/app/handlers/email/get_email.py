from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState, ConfirmEmailState
from app.keyboards.inline import email_confirm_kb
from logger import logger
import re

router = Router()

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@router.message(SubscriptionState.get_email)
async def input_email(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        email = message.text.strip()

        # Простая валидация email
        if not re.match(EMAIL_REGEX, email):
            await message.answer("❌ Некорректный email. Попробуйте снова:")
            return

        await state.update_data(email=email)
        await message.answer(f"Вы ввели: {email}\nВсё верно?", reply_markup=email_confirm_kb())
        await state.set_state(ConfirmEmailState.confirm_new)
        logger.info(f"Пользователь {user_id} ввёл email: {email}")

    except Exception as e:
        logger.error(f"Ошибка обработки email от пользователя {user_id}: {e}", exc_info=True)
        await message.answer("❌ Произошла ошибка при обработке email. Попробуйте снова.")
