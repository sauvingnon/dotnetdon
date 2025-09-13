from aiogram import Router, F
from app.states.subscription import SubscriptionState
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.db import key_service
from app.helpers.failure_handler import failure_handler
from app.keyboards.inline import empty_keyboard
from logger import logger

router = Router()

@router.callback_query(F.data == "my_subscriptions", SubscriptionState.show_menu)
async def my_subscriptions(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        await callback.message.delete()
        await callback.answer()

        keys = await key_service.get_active_keys_for_tg_id(user_id)
        if keys is None:
            await failure_handler(callback)
            logger.error(f"Пользователь {user_id}: не удалось получить ключи (None).")
            return

        if len(keys) == 0:
            await callback.message.answer(
                "У вас нет активных ключей.",
                reply_markup=empty_keyboard
            )
            logger.info(f"Пользователь {user_id} не имеет активных ключей.")
            return

        for key in keys:
            formatted_date = key.active_until.strftime("%d.%m.%Y")
            message = (
                f"🔑 *Твой ключ (нажми для копирования):*\n"
                f"`{key.sub_url}`\n\n"
                f"🕐 *Активен до:* `{formatted_date}`\n"
                f"🆔 *ID ключа:* `{key.id}`"
            )
            await callback.message.answer(text=message, parse_mode="Markdown")
            logger.info(f"Пользователь {user_id} просмотрел ключ {key.id}, активен до {formatted_date}.")

        await callback.message.answer(
            text="Все ваши ключи показаны выше.",
            reply_markup=empty_keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка при показе ключей пользователю {user_id}: {e}", exc_info=True)
        await callback.message.answer("❌ Произошла ошибка при получении ваших ключей.")
