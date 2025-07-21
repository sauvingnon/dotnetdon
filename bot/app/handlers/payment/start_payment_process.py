from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState
from app.services.db import order_service, user_service
from app.services.payment import payment_service
from app.helpers.failure_handler import failure_handler
from app.models.payment.payment_request import AddPaymentRequest
from config import BOT_URL
from app.keyboards.inline import payment_keyboard

router = Router()

async def start_payment_process(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    email = data.get("email")
    # price = int(data.get("price"))
    price = 10
    duration = int(data.get("duration"))

    payment_request = AddPaymentRequest(
        email=email,
        description=f"Оплата доступа к сервису dotNetDon на {duration} месяцев.",
        return_url=BOT_URL,
        amount=price)

    payment = await payment_service.add_payment(payment_request)

    if payment is None:
        await failure_handler("❌ Не удалось создать заявку на оплату.", callback)
        return
    
    user = await user_service.get_user_for_tg_id(callback.from_user.id)

    if user is None:
        await failure_handler("❌ Не удалось получить пользователя.", callback)
        return
    
    order = await order_service.create_order(user_id=user.id, platform="", order_price=price, is_paid=False, payment_id=payment.id, duration=duration)

    if order is None:
        await failure_handler("❌ Не создать заявку на оплату в базе данных.", callback)
        return

    await state.set_state(SubscriptionState.confirming)

    await state.update_data(payment_id=payment.id)

    pay_keyboard = payment_keyboard(payment.confirmation.return_url)

    await callback.message.answer(
        f"✅ Всё готово!\n\nОплатите заказ по кнопке ниже. После оплаты нажмите «Проверить оплату». Обратите внимание, что ссылка на оплату активна только в течении 10 минут.",
        reply_markup=pay_keyboard
    )

    
    