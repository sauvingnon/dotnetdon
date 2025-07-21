# my_subscriptions
from aiogram import Router, F
from app.states.subscription import Step
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import user_service, key_service
from app.helpers.failure_handler import failure_handler
from app.keyboards.inline import empty_keyboard

router = Router()

# @router.message(F.text == "/help")
@router.callback_query(F.data == "my_subscriptions", Step.show_menu)
async def help(callback: CallbackQuery, state: FSMContext):
    # Отправим сообщение с меню
    await callback.message.delete()
    
    keys = await key_service.get_active_keys_for_tg_id(callback.from_user.id)

    await callback.answer()

    if keys is None:
        await failure_handler("Ошибка при получении ключей", callback)
        return
    
    if len(keys) == 0:
        await callback.message.answer("У вас нет активных ключей.", reply_markup=empty_keyboard)
        return
    
    for key in keys:

        formatted_date = key.active_until.strftime("%d.%m.%Y")

        message = (
            f'🔑 *Твой ключ (нажми для копирования):*\n'
            f'`{key.sub_url}`\n\n'
            f'🕐 *Активен до:* `{formatted_date}`\n'
            f'🆔 *ID ключа:* `{key.id}`'
        )

        await callback.message.answer(text=message, parse_mode='Markdown')

    await callback.message.answer(text="Все ваши ключи показаны выше.", reply_markup=empty_keyboard)

