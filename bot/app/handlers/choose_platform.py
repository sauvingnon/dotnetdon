from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.utils.states import Step
from app.helpers import choose_platform

router = Router()

# Спрашиваем платформу пользователя
@router.callback_query(F.data == "choose_platform", Step.choose_platform)
async def choose_platform(callback: CallbackQuery, state: FSMContext):
    await choose_platform(callback, state)
