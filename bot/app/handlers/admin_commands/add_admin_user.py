from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import Step
from app.services.xui import xui_service
from app.keyboards.inline import empty_keyboard

router = Router()

# Кнопка "добавить админа"
@router.callback_query(F.data == "add_admin_user", Step.show_menu)
async def add_admin_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Укажи имя для нового пользователя:")
    await state.set_state(Step.waiting_for_username)
    await callback.answer()

# Ответ пользователя с именем
@router.message(Step.waiting_for_username)
async def process_new_admin_name(message: Message, state: FSMContext):

    await state.set_state(Step.show_menu)

    username = message.text.strip()

    client = await xui_service.create_client(username)

    if client == None:
        await message.answer(f"❌ Не удалось создать пользователя '{username}'. Возможно, он уже существует или произошла ошибка.")
    else:
        await message.answer(f"✅ Пользователь '{username}' успешно создан. Вот его подписка для доступа с сервису:")
        await message.answer(f"<code>{client.url_sub}</code>", parse_mode="HTML")
        await message.answer("Выбери пункт меню:", reply_markup=empty_keyboard)

    
