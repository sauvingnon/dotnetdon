from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.utils import resources
from app.utils.states import Step
from app.keyboards.inline import start_keyboard

router = Router()

# Стартовая команда
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # удаляем сообщение пользователя
    # await message.delete()

    # Получаем имя пользовтеля
    user_name = message.from_user.username

    # Если там пусто, то берем из другого места
    if(user_name == None):
        user_name = message.from_user.first_name
    
    # Если и там тоже пусто - именуем пользователя как "Unknown"
    if(user_name == None):
        user_name = "Unknown"

    await state.update_data(user_name=user_name)

    # отправляем первое сообщение
    await message.answer(f"Привет, {user_name}!🙌")

    # Отправим сообщение с кнопкой
    await message.answer(resources.welcome_message, reply_markup=start_keyboard)

    # Сохраниим сообщение чтобы потом его удалить
    # await state.update_data(last_bot_message_id=sent.message_id)
    # Установим текущее состояние
    await state.set_state(Step.choose_platform)
