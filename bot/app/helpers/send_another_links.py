from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.inline import keyboard_after_all_links
from app.utils.resources import android_links, ios_links

# Дополнительные ссылки для скачивания
async def send_another_links(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    platform = data.get("platform")

    # Отвечаем пользователю
    if platform == "platform_android":
        links = '\n'.join([f'Ссылка: {link}' for link in android_links])
    elif platform == "platform_ios":
        links = '\n'.join([f'Ссылка: {link}' for link in ios_links])
    
    await callback.message.answer('Попробуй эти источники:\n' + links, parse_mode='Markdown', reply_markup=keyboard_after_all_links)

    await callback.answer()