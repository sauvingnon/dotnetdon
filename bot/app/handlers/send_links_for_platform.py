from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.subscription import Step
from app.keyboards.inline import download_check_keyboard

router = Router()

# Обработка выбора платформы
@router.callback_query(F.data.in_({"platform_ios", "platform_android"}), Step.send_links_for_platform)
async def send_links_for_platform(callback: CallbackQuery, state: FSMContext):
    platform = callback.data  # "platform_ios" или "platform_android"

    await callback.message.delete()

    # Сохраняем в state
    await state.update_data(platform=platform)

    # Отвечаем пользователю
    if platform == "platform_ios":
        await callback.message.answer('Скачивай это приложение по' + ' [ссылке](https://apps.apple.com/ru/app/v2raytun/id6476628951)', parse_mode='Markdown', reply_markup=download_check_keyboard)
    elif platform == "platform_android":
        await callback.message.answer('Скачивай это приложение по' + ' [ссылке](https://play.google.com/store/apps/details?id=com.v2raytun.android)', parse_mode='Markdown', reply_markup=download_check_keyboard)
    else:
        print("Платформа пользователя не определена")

    await state.set_state(Step.check_dowloand)
    await callback.answer()
