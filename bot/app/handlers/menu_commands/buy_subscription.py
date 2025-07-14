# Купить подписку
from aiogram import Router, F
from app.states.subscription import Step
from app.keyboards.inline import plans_tariff
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "buy_subscription", Step.show_menu)
async def buy_subscription(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.set_state(Step.show_menu)

    await callback.message.answer("Выбери тарифный план:", reply_markup=plans_tariff)

    await callback.answer()

    

