from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import key_service, user_service
from app.utils.states import Step
from app.keyboards.inline import key_add_keyboard
from app.helpers.notificate_admin import notificate_admin
from app.services.db import user_service, key_service, order_service
from app.helpers.failure_handler import failure_handler
from app.helpers.get_access_for_user import get_access_for_user
import config

# Выдать доступ для пользователя
async def send_access_for_user(callback: CallbackQuery, state: FSMContext):

    is_trial = False
    data = await state.get_data()
    platform = data.get("platform")
    user_name = data.get("user_name")
    is_trial = data.get("user_get_trial")
    tg_id = callback.from_user.id

    user = await user_service.create_user(tg_id=tg_id, tg_username=user_name)

    if not user: 
        await failure_handler('user из бд не получен', callback)
        return

    order = await order_service.create_order(user.id, platform, 0, False)

    if not order: 
        await failure_handler('order из бд не получен', callback)
        return

    key_content = await get_access_for_user(user.id, order.id)

    if not key_content:
        await failure_handler('Доступ для пользователя не был выдан', callback)
        return

    key = await key_service.get_key_for_order_id(order_id=order.id)

    if not key: 
        await failure_handler('Ключ из бд не получен', callback)
        return

    key_id = key.key_id

    url = f'{config.URL_WEBSITE}{key_id}'

    callback.message.answer('Твой ключ ниже, можешь вставить его в приложение самостоятельно, а можешь нажать кнопку и он добавится автоматически.')

    # if platform == "platform_android":
    #     url = f'v2rayng://install-sub/{key_content}'
    # elif platform == "platform_ios":
    #     url = f'streisand://import/{key_content}'
    
    keyboard = key_add_keyboard(url)

    await callback.message.answer(f'`{key_content}`', parse_mode='Markdown', reply_markup=keyboard)
    
    # await callback.message.answer('На этом все, приятного использования, если есть вопросы, то пиши их' + ' [ему](https://t.me/sauvingnon)', parse_mode='Markdown')

    await notificate_admin("Была упешно оформлена подписка!")

    await callback.answer()