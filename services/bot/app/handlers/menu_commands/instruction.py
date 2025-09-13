# instruction
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from app.helpers.choose_platform import choose_platform
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

# @router.message(F.text == "/help")
@router.callback_query(F.data == "instruction", SubscriptionState.show_menu)
async def help(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await callback.message.delete()
    await choose_platform(callback, state)
    await callback.answer()
    

