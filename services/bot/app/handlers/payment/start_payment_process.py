from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState
from app.services.db import order_service, user_service
from app.services.payment import payment_service
from app.helpers.failure_handler import failure_handler
from app.schemas.payment.payment_request import AddPaymentRequest
from config import BOT_URL
from app.keyboards.inline import payment_keyboard
from logger import logger

router = Router()

async def start_payment_process(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        data = await state.get_data()
        email = data.get("email")
        price = data.get("price")
        duration = data.get("duration")

        if not email or price is None or duration is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: неверные данные в FSM: {data}")
            return

        price = int(price)
        duration = int(duration)

        payment_request = AddPaymentRequest(
            email=email,
            description=f"Оплата доступа к сервису dotNetDon на {duration} месяцев.",
            return_url=BOT_URL,
            amount=price
        )

        payment = await payment_service.add_payment(payment_request)
        if payment is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: ошибка при создании заявки на оплату.")
            return

        user = await user_service.get_user_for_tg_id(user_id)
        if user is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: отсутствует в базе.")
            return

        order = await order_service.create_order(
            user_id=user.id,
            platform="",
            order_price=price,
            is_paid=False,
            payment_id=payment.id,
            duration=duration
        )

        if order is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: ошибка при создании заказа.")
            return

        await state.set_state(SubscriptionState.confirming)
        await state.update_data(payment_id=payment.id)

        pay_keyboard = payment_keyboard(payment.confirmation.return_url)
        await callback.message.answer(
            "✅ Всё готово!\n\n"
            "Оплатите заказ по кнопке ниже. После оплаты нажмите «Проверить оплату». "
            "Обратите внимание, что ссылка на оплату активна только в течение 10 минут.",
            reply_markup=pay_keyboard
        )

        logger.info(f"Пользователь {user_id} начал процесс оплаты, payment_id={payment.id}")

    except Exception as e:
        logger.error(f"Ошибка в start_payment_process для пользователя {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при создании платежа.")
