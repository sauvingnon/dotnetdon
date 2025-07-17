# Тут хранится меню
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState, ConfirmEmailState
from app.services.db import user_service
from app.keyboards.inline import email_confirm_kb

router = Router()

@router.callback_query(lambda c: c.data.startswith("plan_"), SubscriptionState.choosing_plan)
async def handle_plan_choice(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()

    plan = callback.data.split("_")[1]  # например '1m', '3m', '6m', '12m'
    
    # Тут логика
    if plan == "1m":
        price = 199
        duration = 1
    elif plan == "3m":
        price = 569
        duration = 3
    elif plan == "6m":
        price = 999
        duration = 6
    elif plan == "12m":
        price = 1999
        duration = 12

    await state.set_state(SubscriptionState.check_email)

    await state.update_data(price=price)
    await state.update_data(duration=duration)

    await callback.message.answer(f"Вы выбрали тариф на {plan.upper()} — {price}₽.")
    await callback.answer()

    user = await user_service.get_user_for_tg_id(callback.from_user.id)

    if user and user.email:
        await state.update_data(email=user.email)
        await callback.message.answer(
            f"Твоя почта: {user.email}\nВсё верно?",
            reply_markup=email_confirm_kb()  # Клавиатура с "Да / Нет"
        )
        await state.set_state(ConfirmEmailState.confirm_existing)
    else:
        await callback.message.answer("Введите вашу почту:")
        await state.set_state(SubscriptionState.get_email)

