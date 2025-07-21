from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState, Step
from app.services.payment import payment_service
from app.services.db import user_service, order_service
from app.helpers.send_access_for_user import send_access_for_user
from app.helpers.failure_handler import failure_handler
from app.helpers.notificate_admin import notificate_admin
from app.keyboards.inline import get_main_menu

router = Router()

# Кнопка "добавить админа"
@router.callback_query(F.data == "check_payment", SubscriptionState.confirming)
async def check_payment(callback: CallbackQuery, state: FSMContext):

    # await callback.message.delete()

    data = await state.get_data()
    payment_id = data.get("payment_id")
    is_paid = await payment_service.check_payment(payment_id)

    if is_paid == None:
        failure_handler("Не удалось получить статус заявки на оплату.", callback)
        return

    if(is_paid):
        await callback.message.answer("Оплата прошла успешно.")
        order = await order_service.update_order(payment_id=payment_id, is_paid=is_paid)

        await notificate_admin("Была упешно оформлена подписка!")

        if order is None:
            failure_handler("Не удалось обновить статус заказа.", callback)
            return

        await send_access_for_user(callback, state)
        
    else:
        await callback.message.answer("Не оплачено. Оплатите и немного подождите. Обычно это не занимает более 5-ти минут.")

    await callback.answer()

@router.callback_query(F.data == "show_menu", SubscriptionState.confirming)
async def go_menu(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.delete()

    await state.set_state(Step.show_menu)

    user = await user_service.get_user_for_tg_id(callback.from_user.id)

    keyboard = get_main_menu(user)

    await callback.message.answer("Выбери пункт меню:", reply_markup=keyboard)
    await callback.answer()