# Тут хранится меню
from aiogram import Router, F
from app.states.subscription import Step
from app.keyboards.inline import get_main_menu
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

# @router.message(F.text == "/menu")
@router.callback_query(F.data == "show_menu", Step.show_menu)
async def show_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.set_state(Step.show_menu)

    keyboard = get_main_menu(callback.from_user.id)

    await callback.message.answer("Выбери пункт меню:", reply_markup=keyboard)