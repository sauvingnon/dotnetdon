from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.subscription import ConfirmEmailState, SubscriptionState
from app.services.db import user_service
from app.keyboards.inline import email_confirm_kb
from logger import logger
from app.utils.resources import PLAN_PRICES, PLAN_DURATIONS

router = Router()

@router.callback_query(lambda c: c.data.startswith("plan_"), SubscriptionState.show_menu)
async def handle_plan_choice(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        await callback.message.delete()
        plan = callback.data.split("_")[1]  # '1m', '3m', '6m', '12m'

        price = PLAN_PRICES.get(plan)
        duration = PLAN_DURATIONS.get(plan)

        if price is None or duration is None:
            await callback.message.answer("❌ Ошибка выбора тарифа. Попробуйте снова.")
            logger.error(f"Пользователь {user_id} выбрал некорректный план: {plan}")
            return

        await state.update_data(price=price, duration=duration)
        await state.set_state(SubscriptionState.check_email)

        await callback.message.answer(f"Вы выбрали тариф на {plan.upper()} — {price}₽.")
        await callback.answer()
        logger.info(f"Пользователь {user_id} выбрал тариф {plan.upper()} за {price}₽ на {duration} мес.")

        user = await user_service.get_user_for_tg_id(user_id)
        if user and user.email:
            await state.update_data(email=user.email)
            await callback.message.answer(
                f"Твоя почта: {user.email}\nВсё верно?",
                reply_markup=email_confirm_kb()
            )
            await state.set_state(ConfirmEmailState.confirm_existing)
        else:
            await callback.message.answer("Введите вашу почту:")
            await state.set_state(SubscriptionState.get_email)

    except Exception as e:
        logger.error(f"Ошибка обработки выбора тарифа пользователем {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при выборе тарифа. Попробуйте снова.")
