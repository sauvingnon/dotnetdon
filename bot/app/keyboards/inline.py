from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура старта
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подключиться", callback_data="start_input")]
    ]
)

# Клавиатура выбора платформы
platform_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="iPhone", callback_data="platform_ios")],
        [InlineKeyboardButton(text="Android", callback_data="platform_android")]
    ]
)

# Клавиатура после скачивания
download_check_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я скачал!✅", callback_data="success_dowloand")],
        [InlineKeyboardButton(text="Что-то не работает, дай другие ссылки!", callback_data="error_dowloand")]
    ]
)

# Клавиатура после отправки доп. ссылок
keyboard_after_all_links = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Я скачал!✅', callback_data='success_dowloand')]
    ])

# Клавиатура для ссылки на добавление ключа
def key_add_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить ключ", url=url)]
        ]
    )
