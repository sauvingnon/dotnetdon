from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import key_service, user_service
from app.helpers.notificate_admin import notificate_admin
from app.services.db import user_service, key_service, order_service
from app.helpers.failure_handler import failure_handler
from app.helpers.get_access import get_access_for_user

# Выдать доступ для пользователя
async def send_access_for_user(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    platform = data.get("platform")
    is_trial = data.get("user_get_trial")
    tg_id = callback.from_user.id

    user = await user_service.get_user_for_tg_id(tg_id)

    if not user: 
        await failure_handler('user из бд не получен', callback)
        return
    
    if is_trial:
        is_paid = True
        order_price = 0
    else:
        is_paid = False
        order_price = 99

    order = await order_service.create_order(user.id, platform, order_price, is_paid)

    if not order: 
        await failure_handler('order из бд не получен', callback)
        return

    url_sub = await get_access_for_user(user, order)

    if not url_sub:
        await failure_handler('Доступ для пользователя не был выдан', callback)
        return
    
    callback.message.answer('Твой ключ ниже, добавь его в приложение.')

    # if platform == "platform_android":
    #     url = f'v2rayng://install-sub/{key_content}'
    # elif platform == "platform_ios":
    #     url = f'streisand://import/{key_content}'

    # await callback.message.answer(f'`{url_sub}`', parse_mode='Markdown', reply_markup=keyboard)
    
    # await callback.message.answer('На этом все, приятного использования, если есть вопросы, то пиши их' + ' [ему](https://t.me/sauvingnon)', parse_mode='Markdown')

    await notificate_admin("Была упешно оформлена подписка!")

    await callback.answer()