from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import ConfirmEmailState, SubscriptionState
from app.services.db import user_service
from app.handlers.payment.start_payment_process import start_payment_process

router = Router()

@router.callback_query(ConfirmEmailState.confirm_existing, F.data.in_(['yes', 'no']))
@router.callback_query(ConfirmEmailState.confirm_new, F.data.in_(['yes', 'no']))
async def confirm_email(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    email = data["email"]
    user_id = callback.from_user.id
    current_state = await state.get_state()
    await callback.answer()

    if callback.data == 'yes':
        if current_state == ConfirmEmailState.confirm_new:
            await user_service.update_user(user_id, email)
        await callback.message.answer("Отлично, переходим к оплате!")
        # логика оплаты
        await start_payment_process(callback, state)
        # await state.clear()
    else:
        await callback.message.answer("Введите новую почту:")
        await state.set_state(SubscriptionState.get_email)
