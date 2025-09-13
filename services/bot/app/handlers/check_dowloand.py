from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.inline import empty_keyboard
from app.helpers.send_another_links import send_another_links

router = Router()

# Проверка, скачал ли пользователь все
@router.callback_query(F.data.in_({"success_dowloand", "error_dowloand"}))
async def handle_check_dowloand(callback: CallbackQuery, state: FSMContext):
    status = callback.data # "success_dowloand" или "error_dowloand"

    if status == "success_dowloand":
        await callback.message.answer("Отлично, добавь ключ в приложение. Нажми плюсик, а затем добавь из буфера обмена твой ключ. Приятного использования.", reply_markup=empty_keyboard)
    elif status == "error_dowloand":
        await send_another_links(callback, state)

    await callback.answer()  # ✅ Telegram будет доволен