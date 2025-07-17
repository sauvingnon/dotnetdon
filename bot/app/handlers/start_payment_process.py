from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState
from app.services.db import user_service
from app.services.payment import payment_service
from app.helpers.failure_handler import failure_handler
from app.models.payment.payment_request import AddPaymentRequest
from config import BOT_URL
from app.keyboards.inline import payment_keyboard

router = Router()

async def start_payment_process(message_or_callback, state: FSMContext):
    data = await state.get_data()

    email = data.get("email")
    # price = int(data.get("price"))
    price = 10
    duration = data.get("duration")

    payment_request = AddPaymentRequest(
        email=email,
        description=f"Оплата доступа к сервису dotNetDon на {duration} месяцев.",
        return_url=BOT_URL,
        amount=price)

    payment = await payment_service.add_payment(payment_request)

    if payment is None:
        await failure_handler("❌ Не удалось создать заявку на оплату. Попробуйте позже.", message_or_callback)
        return

    await state.set_state(SubscriptionState.confirming)

    await state.update_data(payment_id=payment.id)

    pay_keyboard = payment_keyboard(payment.confirmation.return_url)

    await message_or_callback.answer(
        f"✅ Всё готово!\n\nОплатите заказ по кнопке ниже. После оплаты нажмите «Проверить оплату». Обратите внимание, что ссылка на оплату активна только в течении 10 минут.",
        reply_markup=pay_keyboard
    )

    
    