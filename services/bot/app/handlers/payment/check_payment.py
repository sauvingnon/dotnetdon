from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState
from app.services.payment import payment_service
from app.services.db import user_service, order_service
from app.helpers.send_access_for_user import grant_access
from app.helpers.failure_handler import failure_handler
from app.keyboards.inline import get_main_menu
from logger import logger

router = Router()

@router.callback_query(F.data == "check_payment", SubscriptionState.confirming)
async def check_payment(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        data = await state.get_data()
        payment_id = data.get("payment_id")

        if not payment_id:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: отсутствует payment_id в FSM.")
            return

        is_paid = await payment_service.check_payment(payment_id)

        if is_paid is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: ошибка при проверке оплаты {payment_id}.")
            return

        if is_paid:
            await callback.message.answer("✅ Оплата прошла успешно.")

            order = await order_service.update_order(payment_id=payment_id, is_paid=is_paid)
            if order is None:
                await failure_handler(callback)
                logger.error(f"Пользователь {user_id}: ошибка при обновлении заказа {payment_id}.")
                return

            logger.info(f"Была успешно оформлена подписка пользователем {user_id}!")

            await grant_access(callback, state, False)
            logger.info(f"Пользователь {user_id} получил доступ после оплаты {payment_id}.")

        else:
            await callback.message.answer(
                "❌ Не оплачено. Оплатите и немного подождите. Обычно это не занимает более 5 минут."
            )
            logger.info(f"Пользователь {user_id} проверил оплату {payment_id}, оплата не прошла.")

        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка в check_payment для пользователя {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при проверке оплаты.")

@router.callback_query(F.data == "show_menu", SubscriptionState.confirming)
async def go_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        await callback.message.delete()
        await state.set_state(SubscriptionState.show_menu)

        user = await user_service.get_user_for_tg_id(user_id)
        keyboard = get_main_menu(user)

        await callback.message.answer("Выбери пункт меню:", reply_markup=keyboard)
        await callback.answer()

        logger.info(f"Пользователь {user_id} вернулся в главное меню.")

    except Exception as e:
        logger.error(f"Ошибка в go_menu для пользователя {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при отображении меню.")
