from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import user_service, key_service, order_service
from app.services.remnawave import remnawave_service
from app.helpers.failure_handler import failure_handler
from app.states.subscription import SubscriptionState
from app.keyboards.inline import after_payment_keyboard
from config import TRIAL_DURATION
from logger import logger


async def grant_access(callback: CallbackQuery, state: FSMContext, trial: bool = False):
    tg_id = callback.from_user.id
    try:
        user = await user_service.get_user_for_tg_id(tg_id)
        if not user:
            await failure_handler(callback)
            logger.warning(f"{tg_id} не найден в базе")
            return

        if trial:
            # триал доступ
            duration = None
            trial_duration = TRIAL_DURATION
            payment_id = None
        else:
            # обычная оплата
            data = await state.get_data()
            payment_id = data.get("payment_id")
            if not payment_id:
                await failure_handler(callback)
                logger.error(f"{tg_id} отсутствует payment_id в FSM")
                return
            order = await order_service.get_order_by_payment_id(payment_id)
            if not order:
                await failure_handler(callback)
                logger.error(f"{tg_id} заказ {payment_id} не найден")
                return
            duration = order.duration
            trial_duration = None

        # создаем клиента на панели
        client = await remnawave_service.create_client(
            tg_username=user.tg_username,
            duration=duration,
            trial_duration=trial_duration
        )
        if not client:
            await failure_handler(callback)
            logger.error(f"{tg_id} клиент панели не получен")
            return

        key_kwargs = dict(
            user_id=user.id,
            sub_url=client.subscription_url,
            client_email=client.username,
            active_until=client.expire_at
        )
        if not trial:
            key_kwargs["order_id"] = order.id

        key = await key_service.create_key(**key_kwargs)
        if not key:
            await failure_handler(callback)
            logger.error(f"{tg_id} ключ панели не создан")
            return

        if trial:
            # фиксируем, что тестовый ключ выдан
            updated = await user_service.update_user(user_tg_id=tg_id, new_test_used=True)
            if updated:
                logger.info("Был оформлен тестовый доступ.")
            else:
                await failure_handler(callback)
                logger.error(f"{tg_id} не удалось обновить флаг trial")

        # выдаем ключ пользователю
        if trial:
            await callback.message.answer(f"Обрати внимание, ключ активен только {TRIAL_DURATION} дня.")
        await callback.message.answer(f"`{key.sub_url}`", parse_mode="Markdown")
        await callback.message.answer(
            "Твой ключ выше, можешь самостоятельно добавить его в приложение "
            "или действовать по нашей инструкции, выбирай:",
            reply_markup=after_payment_keyboard()
        )

        await state.set_state(SubscriptionState.show_menu)
        await callback.answer()
        logger.info(f"{tg_id} получил {'trial' if trial else 'оплаченный'} доступ, ключ {key.sub_url}")

    except Exception as e:
        logger.exception(f"Ошибка при выдаче доступа пользователю {tg_id}: {e}")
        await failure_handler(callback)
