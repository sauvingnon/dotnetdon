from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.utils.states import Step
from app.keyboards.inline import platform_keyboard

router = Router()

# Спрашиваем платформу пользователя
@router.callback_query(F.data == "start_input", Step.choose_platform)
async def choose_platform(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()

    await callback.message.answer("Выбери свое устройство:", reply_markup=platform_keyboard)

    await state.set_state(Step.send_links_for_platform)
    await callback.answer()  # обязательно, чтобы Telegram "заметил" обработку
