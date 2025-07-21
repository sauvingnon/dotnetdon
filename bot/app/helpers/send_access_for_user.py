from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import user_service, key_service, order_service
from app.services.xui import xui_service
from app.helpers.failure_handler import failure_handler
from app.helpers.notificate_admin import notificate_admin
from app.states.subscription import Step
from app.keyboards.inline import after_payment_keyboard
from config import TRIAL_DURATION
from app.utils.convert_date import datetime_from_ms_timestamp

# Выдать доступ для пользователя
async def send_access_for_user(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    payment_id = data.get("payment_id")
    tg_id = callback.from_user.id

    user = await user_service.get_user_for_tg_id(tg_id)

    if user is None:
        await failure_handler('Пользователь не был получен.', callback)
        return
    
    order = await order_service.get_order_by_payment_id(payment_id)

    if order is None:
        await failure_handler('Заказ не был получен.', callback)
        return

    # Запрашиваем ключ от XUI панели
    client = await xui_service.create_client(user.tg_username, order.duration)

    if client is None:
        await failure_handler('Клиент из панели не был получен.', callback)
        return
    
    active_until = datetime_from_ms_timestamp(client.expiryTime)

    key = await key_service.create_key(order_id=order.id, sub_url=client.url_sub, client_email=client.email, active_until=active_until, user_id=user.id)  

    if key is None:
        await failure_handler('Ключ из панели не был получен.', callback)
        return    
    
    await callback.message.answer(f'`{key.sub_url}`', parse_mode='Markdown')

    await callback.message.answer('Твой ключ выше, можешь самостоятельно добавить его в приложение или действовать по нашей инструкции, выбирай:',reply_markup=after_payment_keyboard())
    
    await state.set_state(Step.show_menu)

    await callback.answer()



# Выдать доступ для пользователя
async def send_trial_access_for_user(callback: CallbackQuery, state: FSMContext):

    tg_id = callback.from_user.id

    user = await user_service.get_user_for_tg_id(tg_id)

    if user is None:
        await failure_handler('Пользователь не был получен.', callback)
        return

    # Запрашиваем ключ от XUI панели
    client = await xui_service.create_client(tg_username=user.tg_username, duration=None, trial_duration=TRIAL_DURATION)

    if client is None:
        await failure_handler('Клиент из панели не был получен.', callback)
        return
    
    active_until = datetime_from_ms_timestamp(client.expiryTime)

    key = await key_service.create_key(user_id=user.id, sub_url=client.url_sub, client_email=client.email, active_until=active_until)  

    if key is None:
        await failure_handler('Ключ из панели не был получен.', callback)
        return  
    
    await callback.message.answer(f"Обрати внимание, ключ активен только {TRIAL_DURATION} дня.")
    
    await callback.message.answer(f'`{key.sub_url}`', parse_mode='Markdown')

    await callback.message.answer('Твой ключ выше, можешь самостоятельно добавить его в приложение или действовать по нашей инструкции, выбирай:',reply_markup=after_payment_keyboard())
    
    await state.set_state(Step.show_menu)

    result = await user_service.update_user(user_tg_id=tg_id, new_test_used=True)

    if result:
        await notificate_admin("Был оформлен тестовый доступ.")
    else:
        await failure_handler("Ошибка при обновлении пользователя")

    await callback.answer()