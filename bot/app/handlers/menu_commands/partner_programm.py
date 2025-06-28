# Партнерская программа
from aiogram import Router, F
from app.utils.states import Step
from app.keyboards.inline import empty_keyboard
from app.utils.resources import partner_program_message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "about_us", Step.show_menu)
async def about_us(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await callback.message.delete()
    await callback.message.answer(partner_program_message, reply_markup=empty_keyboard)
    await callback.answer()
    

