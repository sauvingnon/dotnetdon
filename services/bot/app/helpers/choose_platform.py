from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.inline import platform_keyboard

async def choose_platform(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()

    await callback.message.answer("Выбери свое устройство:", reply_markup=platform_keyboard)
    await callback.answer()  # обязательно, чтобы Telegram "заметил" обработку