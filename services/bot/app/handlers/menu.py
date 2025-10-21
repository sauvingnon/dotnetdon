# Тут хранится меню
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from app.keyboards.inline import get_main_menu
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "show_menu", SubscriptionState.show_menu)
async def show_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.clear() 

    await state.set_state(SubscriptionState.show_menu)

    keyboard = get_main_menu(callback.from_user.id)

    await callback.message.answer("Выбери пункт меню:", reply_markup=keyboard)