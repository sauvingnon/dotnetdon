# Тут хранится меню
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.helpers.choose_platform import choose_platform

router = Router()

@router.callback_query(lambda c: c.data.startswith("plan_"))
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

    await callback.message.answer(f"Вы выбрали тариф на {plan.upper()} — {price}₽. Обрабатываем...")
    await callback.answer()
    await choose_platform(callback=callback, state=state)
