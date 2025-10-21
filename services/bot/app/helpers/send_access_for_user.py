from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.services.remnawave import remnawave_service
from app.helpers.failure_handler import failure_handler
from app.states.subscription import SubscriptionState
from config import TRIAL_DURATION_MONTHS
from logger import logger
from app.keyboards.inline import after_payment_keyboard
from app.helpers.check_user import check_user, add_user
from app.schemas.remnawave.addreq import ClientCreate


async def grant_access(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    username = callback.from_user.username
    try:
        duration = TRIAL_DURATION_MONTHS

        if check_user(tg_id):
            await callback.message.answer("Ты уже получал доступ.") 
            return

        # создаем клиента на панели

        request = ClientCreate(
            tg_id=tg_id,
            tg_username=username,
            duration=duration,
            description=None
        )

        response = await remnawave_service.create_client(request)

        if not response:
            await failure_handler(callback)
            logger.error(f"{tg_id} клиент панели не получен")
            return

        # выдаем ключ пользователю
        await callback.message.answer(f"`{response.subscription_url}`", parse_mode="Markdown")
        await callback.message.answer(
            "Твой ключ выше, можешь самостоятельно добавить его в приложение "
            "или действовать по нашей инструкции, выбирай:",
            reply_markup=after_payment_keyboard()
        )

        add_user(tg_id)

        await state.set_state(SubscriptionState.show_menu)
        await callback.answer()
        logger.info(f"{tg_id} - {username} получил доступ.")

    except Exception as e:
        logger.exception(f"Ошибка при выдаче доступа пользователю {tg_id}: {e}")
        await failure_handler(callback)
