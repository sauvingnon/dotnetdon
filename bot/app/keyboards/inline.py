from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура старта
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подключиться", callback_data="show_menu")]
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

# Клавиатура меню
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пробный период", callback_data="start_trial")],
        [InlineKeyboardButton(text="💳 Купить/Продлить", callback_data="buy_subscription")],
        [InlineKeyboardButton(text="Мои покупки", callback_data="my_subscriptions")],
        [InlineKeyboardButton(text="⚙️Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Наш ТГК", callback_data="check_channel")]
    ]
)

# Клавиатура для ссылки на добавление ключа
def key_add_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить ключ", url=url)]
        ]
    )
