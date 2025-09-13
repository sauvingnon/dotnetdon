# Помощь
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from app.keyboards.inline import help_manu
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

# @router.message(F.text == "/help")
@router.callback_query(F.data == "help", SubscriptionState.show_menu)
async def help(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await state.set_state(SubscriptionState.show_menu)
    await callback.message.delete()
    await callback.message.answer("Выбери пункт меню:", reply_markup=help_manu)
    await callback.answer()
    

