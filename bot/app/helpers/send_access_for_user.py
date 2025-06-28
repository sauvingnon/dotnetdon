from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.xui import xui_service
from app.helpers.notificate_admin import notificate_admin

# Выдать доступ для пользователя
async def send_access_for_user(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_name = data.get("user_name")

    # Запрашиваем ключ от XUI панели
    client = await xui_service.create_client(user_name)
    if client is None:
        print('Клиент из панели не был получен.')
        return None

    url_sub = client.url_sub

    # url = f'{config.URL_WEBSITE}{key_id}'

    await callback.message.answer(
        "🔑 Твой ключ ниже!\n\n"
        "📋 Что делать:\n"
        "1. Нажми на ключ — он скопируется в буфер обмена.\n"
        "2. Открой приложение, нажми ➕ и вставь ключ.\n"
        "3. Подключайся и кайфуй 😎\n\n"
        "👥 Хочешь выдать другу? Просто введи /start снова."
    )


    # if platform == "platform_android":
    #     url = f'v2rayng://install-sub/{key_content}'
    # elif platform == "platform_ios":
    #     url = f'streisand://import/{key_content}'
    
    # keyboard = key_add_keyboard(url)

    await callback.message.answer(f'`{url_sub}`', parse_mode='Markdown')
    
    # await callback.message.answer('На этом все, приятного использования, если есть вопросы, то пиши их' + ' [ему](https://t.me/sauvingnon)', parse_mode='Markdown')
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 Техподдержка", url="https://t.me/sauvingnon")]
    ])

    await callback.message.answer(
        "На этом всё. Приятного использования!\nЕсли возникли вопросы — жми на кнопку ниже:",
        reply_markup=keyboard
    )

    await notificate_admin("Была упешно оформлена подписка!", callback)

    await callback.answer()