# Политика сервиса
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from app.keyboards.inline import empty_keyboard
from app.utils.resources import service_rules_message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "service_rules", SubscriptionState.show_menu)
async def about_us(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await callback.message.delete()
    await callback.message.answer(service_rules_message, reply_markup=empty_keyboard)
    await callback.answer()
    

