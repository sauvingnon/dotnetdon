from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import ConfirmEmailState, SubscriptionState
from app.services.db import user_service
from app.handlers.payment.start_payment_process import start_payment_process
from logger import logger
import traceback

router = Router()

@router.callback_query(ConfirmEmailState.confirm_existing, F.data.in_(['yes', 'no']))
@router.callback_query(ConfirmEmailState.confirm_new, F.data.in_(['yes', 'no']))
async def confirm_email(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id

    try:
        data = await state.get_data()
        email = data.get("email")
        if not email:
            await callback.message.answer("❌ Ошибка: электронная почта не найдена. Попробуйте заново.")
            logger.warning(f"Пустая почта у пользователя {user_id} в состоянии {await state.get_state()}")
            await state.set_state(SubscriptionState.get_email)
            return

        current_state = await state.get_state()

        if callback.data == 'yes':
            if current_state == ConfirmEmailState.confirm_new:
                updated = await user_service.update_user(user_id, email)
                if not updated:
                    await callback.message.answer("❌ Не удалось обновить почту. Попробуйте снова.")
                    logger.exception(f"Ошибка обновления почты для пользователя {user_id}: {email}")
                    return
            await callback.message.answer("Отлично, переходим к оплате!")
            await start_payment_process(callback, state)
        else:
            await callback.message.answer("Введите новую почту:")
            await state.set_state(SubscriptionState.get_email)

    except Exception as e:
        logger.error(f"Ошибка при подтверждении почты у пользователя {user_id}: {e}\n{traceback.format_exc()}")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте снова позже.")