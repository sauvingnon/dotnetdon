from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState
from app.services.remnawave import remnawave_service
from app.keyboards.inline import empty_keyboard
from logger import logger
from app.helpers.failure_handler import failure_handler
import traceback

router = Router()

# Кнопка "добавить пользователя"
@router.callback_query(F.data == "add_admin_user", SubscriptionState.show_menu)
async def add_admin_user(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        await callback.message.answer("Укажи имя для нового пользователя:")
        await state.set_state(SubscriptionState.waiting_for_username)
        await callback.answer()
    except Exception as e:
        logger.exception(f"Ошибка в /add_admin_user: {e}")
        await failure_handler(callback)
    
# Ответ пользователя с именем
@router.message(SubscriptionState.waiting_for_username)
async def process_new_admin_name(message: Message, state: FSMContext):
    username = message.text.strip()

    try:
        client = await remnawave_service.create_client(username)
    except Exception as e:
        await message.answer(
            f"❌ Не удалось создать пользователя '{username}'. Попробуй снова или свяжись с техподдержкой."
        )
        logger.exception(
            f"Ошибка при создании пользователя '{username}' админом {message.from_user.id} - {message.from_user.username}: {e}\n{traceback.format_exc()}"
        )
        return

    if not client:
        await message.answer(
            f"❌ Не удалось создать пользователя '{username}'. Возможно, он уже существует. Введи другое имя:"
        )
        logger.warning(f"Создание пользователя '{username}' админом {message.from_user.id} - {message.from_user.username} вернуло None (админ {message.from_user.id})")
        return  # оставляем состояние для повторного ввода

    # Успешно создали пользователя
    await state.set_state(SubscriptionState.show_menu)
    await message.answer(f"✅ Пользователь '{username}' успешно создан. Вот его подписка для доступа к сервису:")
    await message.answer(f"<code>{client.subscription_url}</code>", parse_mode="HTML")
    await message.answer("Выбери пункт меню:", reply_markup=empty_keyboard)

    logger.info(f"Администратор {message.from_user.id} - {message.from_user.username} успешно создал пользователя '{username}'")
