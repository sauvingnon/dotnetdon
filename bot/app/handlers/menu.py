# Тут хранится меню
from aiogram import Router, F
from app.utils.states import Step
from app.keyboards.inline import main_menu
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "show_menu", Step.show_menu)
async def show_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Выбери пункт меню:", reply_markup=main_menu)