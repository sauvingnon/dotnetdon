from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState
from app.services.payment import payment_service
from app.helpers.choose_platform import choose_platform
from app.helpers.failure_handler import failure_handler

router = Router()

# Кнопка "добавить админа"
@router.callback_query(F.data == "check_payment", SubscriptionState.confirming)
async def check_payment(callback: CallbackQuery, state: FSMContext):

    # await callback.message.delete()

    data = await state.get_data()
    payment_id = data.get("payment_id")
    is_paid = await payment_service.check_payment(payment_id)

    if is_paid == None:
        failure_handler("Не удалось получить статус платежа", callback)
        return

    if(is_paid):
        await callback.message.answer("Оплата прошла успешно.")
        await choose_platform(callback, state)
    else:
        await callback.message.answer("Не оплачено. Оплатите и немного подождите. Обычно это не занимает более 5-ти минут.")

    await callback.answer()

@router.callback_query(F.data == "show_menu", SubscriptionState.confirming)
async def go_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()