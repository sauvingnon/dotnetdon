from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

plans_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 месяц – 299₽"), KeyboardButton(text="3 месяца – 799₽")],
        [KeyboardButton(text="↩️ Назад")]
    ],
    resize_keyboard=True
)

confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Подтвердить"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)
