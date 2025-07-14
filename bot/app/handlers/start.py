# Стартовое сообщение пользователя
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.utils import resources
from app.states.subscription import Step
from app.keyboards.inline import get_main_menu
from app.services.db import user_service

router = Router()

# Стартовая команда
@router.message(F.text == "/start")
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
        user_name = f"Unknown {message.from_user.id}"

    # await state.update_data(user_name=user_name)

    # Сразу создадим юзера, при первом обращении добавим его в базу
    await user_service.create_user(message.from_user.id, user_name)

    # Установим текущее состояние
    await state.set_state(Step.show_menu)

    # Отправим сообщение с меню
    await message.answer(resources.welcome_message)

    keyboard = get_main_menu(message.from_user.id)

    await message.answer("Выбери пункт меню:", reply_markup=keyboard)

    # Сохраниим сообщение чтобы потом его удалить
    # await state.update_data(last_bot_message_id=sent.message_id)
    
