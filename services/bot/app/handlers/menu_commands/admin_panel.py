# Партнерская программа
from aiogram import Router, F
from app.states.subscription import SubscriptionState
from app.keyboards.inline import admin_panel
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "admin_panel", SubscriptionState.show_menu)
async def about_us(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await callback.message.delete()
    await callback.message.answer("Выбери пункт меню:", reply_markup=admin_panel)
    await callback.answer()
    

