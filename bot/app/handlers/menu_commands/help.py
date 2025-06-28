# Помощь
from aiogram import Router, F
from app.utils.states import Step
from app.keyboards.inline import help_manu
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "help", Step.show_menu)
async def help(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await callback.message.delete()
    await callback.message.answer("Выбери пункт меню:", reply_markup=help_manu)
    await callback.answer()
    

