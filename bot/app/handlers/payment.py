from app.states.subscription import Step
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.inline import platform_keyboard

async def payment(callback: CallbackQuery, state: FSMContext):


    await state.set_state(Step.send_links_for_platform)
    await callback.answer()  # обязательно, чтобы Telegram "заметил" обработку