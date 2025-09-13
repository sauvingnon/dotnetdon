# Тут хранится меню
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from app.services.db import user_service
from app.keyboards.inline import get_main_menu
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

# @router.message(F.text == "/menu")
@router.callback_query(F.data == "show_menu", SubscriptionState.show_menu)
async def show_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.clear() 

    await state.set_state(SubscriptionState.show_menu)

    user = await user_service.get_user_for_tg_id(callback.from_user.id)

    keyboard = get_main_menu(user)

    await callback.message.answer("Выбери пункт меню:", reply_markup=keyboard)