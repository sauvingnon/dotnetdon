from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.states.subscription import SubscriptionState, ConfirmEmailState
from app.keyboards.inline import email_confirm_kb

router = Router()

@router.message(SubscriptionState.get_email)
async def input_email(message: Message, state: FSMContext):
    # можно добавить валидацию email через regex

    email = message.text.strip()

    await state.update_data(email=message.text)
    await message.answer(f"Вы ввели: {message.text}\nВсё верно?", reply_markup=email_confirm_kb())
    await state.set_state(ConfirmEmailState.confirm_new)
